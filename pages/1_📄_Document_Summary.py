
import streamlit as st
import google.generativeai as genai
import textwrap

def get_gemini_response(api_key, prompt, document_text):
    """Queries the Gemini API to get a response based on the prompt and document."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = f"{prompt}\n\n---\n\nDocument:\n\n{document_text}"
        
        # The response generation can be a long-running task
        with st.spinner("AI is analyzing the document... This may take a moment."):
            response = model.generate_content(full_prompt)
        
        # Using textwrap to format the output nicely
        return textwrap.fill(response.text, width=80)
    except Exception as e:
        # More specific error handling for API key issues
        if "API_KEY_INVALID" in str(e):
            return "Error: The provided API key is invalid. Please check your key and try again."
        else:
            return f"An error occurred: {e}"

st.set_page_config(page_title="Document Summary", page_icon="📄")

st.title("📄 Document Summary")

import os

st.write("This page provides a concise summary of the uploaded document's key points.")

# Get document text from session state
document_text = st.session_state.get("document_text", "")

if document_text:
    # Get the API key from the environment variable
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error("API Key is not configured. Please contact the administrator.")
    else:
        st.info("Click the button below to generate the summary.")
        if st.button("Generate Summary", key="summarize_button"):
            prompt = ("First, provide a 'Quick Summary' of the following document in no more than 2-3 sentences. "
                      "Then, provide a 'Detailed Summary' as a bulleted list, with each major section of the document summarized in its own bullet point. "
                      "Use markdown for formatting.")
            
            summary = get_gemini_response(api_key, prompt, document_text)
            
            st.subheader("Generated Summary")
            st.markdown(summary, unsafe_allow_html=True)
        
    st.subheader("Full Document Text")
    with st.expander("Click to view the full text of the document"):
        st.text_area("", document_text, height=300)

else:
    st.warning("No document has been uploaded. Please go to the main page to upload a document first.")
    st.page_link("app.py", label="Back to Home", icon="🏠")
