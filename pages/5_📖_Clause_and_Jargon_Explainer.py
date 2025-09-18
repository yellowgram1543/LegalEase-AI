import streamlit as st
import google.generativeai as genai
import os

def get_gemini_response(api_key, prompt, clause_text):
    """Queries the Gemini API to get a response based on the prompt and clause."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = f"{prompt}\n\n---\n\nClause:\n\n{clause_text}"
        
        with st.spinner("AI is explaining the clause..."):
            response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

st.set_page_config(page_title="Clause Explainer", page_icon="💬")

st.title("💬 Clause & Jargon Explainer")

st.write("Paste any clause from your document below to get a simple explanation, a definition of legal jargon, and a real-world example.")

clause = st.text_area("Paste the clause here:", height=150, key="clause_input")

if st.button("Explain Clause", key="explain_button"):
    if not clause.strip():
        st.warning("Please paste a clause to explain.")
    else:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            st.error("API Key is not configured. Please contact the administrator.")
        else:
            prompt = """Explain the following legal clause in simple, conversational language. Use markdown for formatting. 
                      First, create a section '## सिंपल एक्सप्लेनेशन' and provide a clear and simple explanation. 
                      Second, create a section '## कानूनी शब्दावली' and define any legal or technical jargon in the clause. 
                      Finally, create a section '## रियल वर्ल्ड उदाहरण' and provide a practical, real-world example of how this clause might apply."""

            explanation = get_gemini_response(api_key, prompt, clause)
            
            st.subheader("Clause Explanation")
            st.markdown(explanation, unsafe_allow_html=True)