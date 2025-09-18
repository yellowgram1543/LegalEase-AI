
import streamlit as st
import google.generativeai as genai
import os

def get_gemini_response(api_key, prompt, doc_a, doc_b):
    """Queries the Gemini API to get a comparison of two documents."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = f"{prompt}\n\n---\n\nDOCUMENT A:\n{doc_a}\n\n---\n\nDOCUMENT B:\n{doc_b}"
        
        with st.spinner("AI is comparing the two documents... This may take a while."):
            response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

st.set_page_config(page_title="Comparative Analysis", page_icon="🔄")

st.title("🔄 Comparative Analysis")

st.write("Compare two documents side-by-side to understand the differences in their terms, risks, and costs.")

# Get document texts from session state
doc_a_text = st.session_state.get("document_text", "")
doc_a_name = st.session_state.get("file_name", "Document A")
doc_b_text = st.session_state.get("document_text_b", "")
doc_b_name = st.session_state.get("file_name_b", "Document B")

if doc_a_text and doc_b_text:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key is not configured. Please contact the administrator.")
    else:
        st.info("Click the button below to generate a side-by-side comparison.")
        if st.button("Compare Documents", key="compare_button"):
            prompt = ("You are a legal document comparison assistant. Compare the two legal documents below (Document A and Document B). "
                      f"First, provide a main summary of the key differences between Document A ({doc_a_name}) and Document B ({doc_b_name}). "
                      "Then, create a detailed 'Risk & Cost Comparison' section. In this section, generate a markdown table that compares critical items side-by-side. "
                      "The table should include rows for items like: Interest Rates, Loan Amount, Contract Duration, Termination Penalties, Late Fees, and any other significant financial or risk-related terms you can identify. "
                      "Use ⚠️ icons for risks and 💰 icons for costs.")

            comparison = get_gemini_response(api_key, prompt, doc_a_text, doc_b_text)
            
            st.subheader("Comparison Result")
            st.markdown(comparison, unsafe_allow_html=True)

    # Display full texts for reference
    st.subheader("Full Document Texts")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander(f"View Text of {doc_a_name}"):
            st.text_area("", doc_a_text, height=300, key="doc_a_expander")
    with col2:
        with st.expander(f"View Text of {doc_b_name}"):
            st.text_area("", doc_b_text, height=300, key="doc_b_expander")

else:
    st.warning("Please use the 'Compare Two Documents' option on the main page to upload two documents first.")
    st.page_link("app.py", label="Back to Home", icon="🏠")
