
import streamlit as st
import google.generativeai as genai
import textwrap

def get_gemini_response(api_key, prompt, document_text):
    """Queries the Gemini API to get a response based on the prompt and document."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = f"{prompt}\n\n---\n\nDocument:\n\n{document_text}"
        
        with st.spinner("AI is searching for loopholes... This may take a moment."):
            response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        if "API_KEY_INVALID" in str(e):
            return "Error: The provided API key is invalid. Please check your key and try again."
        else:
            return f"An error occurred: {e}"

st.set_page_config(page_title="Loopholes Analysis", page_icon="🔎")

st.title("🔎 Loopholes Analysis")

import os

st.write("This page analyzes the document for potential loopholes, such as ambiguities, omissions, or exploitable clauses.")

document_text = st.session_state.get("document_text", "")

if document_text:
    # Get the API key from the environment variable
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error("API Key is not configured. Please contact the administrator.")
    else:
        st.info("Click the button below to generate the analysis.")
        if st.button("Find Loopholes", key="loopholes_button"):
            prompt = ("Analyze the following legal document for potential loopholes or ambiguities. For each one you find, create a distinct section starting with '### 🌀'. "
                      "Describe the potential loophole or ambiguity clearly and then explain the potential risk or implication.")

            analysis = get_gemini_response(api_key, prompt, document_text)
            
            st.subheader("Potential Loopholes Found")
            # Split the analysis into individual loopholes and display each in a warning box
            loopholes = analysis.split('### 🌀')
            loopholes = [l.strip() for l in loopholes if l.strip()]

            if loopholes:
                for loophole in loopholes:
                    st.warning(f"**🌀 Ambiguity/Loophole:**\n\n{loophole}")
            else:
                st.success("No significant loopholes or ambiguities were detected.")

    st.subheader("Full Document Text")
    with st.expander("Click to view the full text of the document"):
        st.text_area("", document_text, height=300)

else:
    st.warning("No document has been uploaded. Please go to the main page to upload a document first.")
    st.page_link("app.py", label="Back to Home", icon="🏠")
