
import streamlit as st
import google.generativeai as genai
import os

def get_gemini_response(api_key, prompt, document_text, question):
    """Queries the Gemini API to get an answer to a question based on the document."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = f"{prompt}\n\n---\n\nDOCUMENT:\n{document_text}\n\n---\n\nQUESTION:\n{question}"
        
        with st.spinner("AI is searching the document for an answer..."):
            response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

st.set_page_config(page_title="Document Q&A", page_icon="❓")

st.title("❓ Document Q&A Chatbot")

st.write("Ask a question about the uploaded document. The AI will answer based only on the document's content.")

# Initialize chat history in session state
if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []

document_text = st.session_state.get("document_text", "")

if document_text:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key is not configured. Please contact the administrator.")
    else:
        question = st.text_input("Ask a question (e.g., 'What happens if I break the lease early?')", key="qa_input")

        if st.button("Get Answer", key="qa_button"):
            if question:
                prompt = ("You are a chatbot that can only answer questions based on the provided legal document. "
                          "Do not use any outside knowledge or give legal advice. Based ONLY on the text of the document provided, answer the question. "
                          "If the document does not contain the answer, you MUST state 'The document does not provide an answer to that question.'")

                answer = get_gemini_response(api_key, prompt, document_text, question)
                
                # Add the new Q&A to the history
                st.session_state.qa_history.insert(0, {"question": question, "answer": answer})
            else:
                st.warning("Please enter a question.")

    # Display chat history
    if st.session_state.qa_history:
        st.subheader("Conversation History")
        for i, qa in enumerate(st.session_state.qa_history):
            with st.expander(f"Q: {qa['question']}", expanded=(i==0)):
                st.markdown(qa['answer'])

else:
    st.warning("Please upload a document on the main page first.")
    st.page_link("app.py", label="Back to Home", icon="🏠")
