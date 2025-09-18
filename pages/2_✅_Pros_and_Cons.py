
import streamlit as st
import google.generativeai as genai
import textwrap

def get_gemini_response(api_key, prompt, document_text):
    """Queries the Gemini API to get a response based on the prompt and document."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = f"{prompt}\n\n---\n\nDocument:\n\n{document_text}"
        
        with st.spinner("AI is analyzing the document... This may take a moment."):
            response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        if "API_KEY_INVALID" in str(e):
            return "Error: The provided API key is invalid. Please check your key and try again."
        else:
            return f"An error occurred: {e}"

st.set_page_config(page_title="Pros and Cons Analysis", page_icon="👍👎")

st.title("👍👎 Pros and Cons Analysis")

import os

st.write("This page analyzes the advantages (Pros) and disadvantages (Cons) of the document from a specific perspective.")

document_text = st.session_state.get("document_text", "")

if document_text:
    # Get the API key from the environment variable
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error("API Key is not configured. Please contact the administrator.")
    else:
        role_options = ["", "Tenant", "Landlord", "Borrower", "Lender", "Employee", "Employer", "Contractor", "Client", "General User"]
        role = st.selectbox("Select your role in this agreement:", options=role_options, key="role_pros_cons")
        
        st.info("Click the button below to generate the analysis from your perspective.")
        if st.button("Analyze Pros and Cons", key="pros_cons_button"):
            if role:
                prompt = (f"Analyze the following legal document from the perspective of the '{role}'. "
                          "List the potential 'Pros' (advantages, favorable clauses, protections) and 'Cons' (disadvantages, risks, obligations, unfavorable terms). "
                          "Present the output in two distinct sections: '## Pros' and '## Cons'. Use bullet points for each item.")

                analysis = get_gemini_response(api_key, prompt, document_text)
                
                st.subheader(f"Analysis for: {role}")
                st.markdown(analysis, unsafe_allow_html=True)
            else:
                st.warning("Please enter your role to get a personalized analysis.")

    st.subheader("Full Document Text")
    with st.expander("Click to view the full text of the document"):
        st.text_area("", document_text, height=300)

else:
    st.warning("No document has been uploaded. Please go to the main page to upload a document first.")
    st.page_link("app.py", label="Back to Home", icon="🏠")

