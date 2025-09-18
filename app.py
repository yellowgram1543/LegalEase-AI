import streamlit as st
import PyPDF2
import io
import docx
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="LegalEase AI",
    page_icon="📜",
    layout="wide"
)

# --- App Header ---
st.title("LegalEase AI 📜")
st.write("Understand contracts. Spot risks. Make confident decisions.")

# --- Session State Initialization ---
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "file_name" not in st.session_state:
    st.session_state.file_name = ""
if "document_text_b" not in st.session_state:
    st.session_state.document_text_b = ""
if "file_name_b" not in st.session_state:
    st.session_state.file_name_b = ""

# --- Text Extraction Functions ---
def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

def extract_text_from_txt(file):
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading TXT file: {e}")
        return None

def extract_text_from_docx(file):
    try:
        document = docx.Document(file)
        text = "\n".join(para.text for para in document.paragraphs)
        return text
    except Exception as e:
        st.error(f"Error reading DOCX file: {e}")
        return None

def process_uploaded_file(uploaded_file):
    if not uploaded_file:
        return None
    
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    file_bytes = io.BytesIO(uploaded_file.getvalue())

    if file_extension == ".pdf":
        return extract_text_from_pdf(file_bytes)
    elif file_extension == ".txt":
        return extract_text_from_txt(file_bytes)
    elif file_extension == ".docx":
        return extract_text_from_docx(file_bytes)
    else:
        st.error(f"Unsupported file type: {uploaded_file.name}")
        return None

# --- UI for File Upload ---
compare_mode = st.checkbox("Compare Two Documents", key="compare_mode")

if compare_mode:
    st.info("Upload two documents to compare them.")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file_a = st.file_uploader("Upload Document A", type=["pdf", "txt", "docx"], key="uploader_a")
    with col2:
        uploaded_file_b = st.file_uploader("Upload Document B", type=["pdf", "txt", "docx"], key="uploader_b")

    if uploaded_file_a and uploaded_file_b:
        with st.spinner("Processing documents..."):
            st.session_state.document_text = process_uploaded_file(uploaded_file_a)
            st.session_state.file_name = uploaded_file_a.name
            st.session_state.document_text_b = process_uploaded_file(uploaded_file_b)
            st.session_state.file_name_b = uploaded_file_b.name
            
            if st.session_state.document_text and st.session_state.document_text_b:
                st.success("Both documents processed! Go to the '🔄 Comparative Analysis' page.")
            else:
                st.error("Failed to process one or both documents. Please try again.")

else:
    st.info("Upload a single document for analysis.")
    uploaded_file = st.file_uploader("Upload your legal document", type=["pdf", "txt", "docx"], key="uploader_single")
    
    if uploaded_file:
        with st.spinner("Processing document..."):
            st.session_state.document_text = process_uploaded_file(uploaded_file)
            st.session_state.file_name = uploaded_file.name
            st.session_state.document_text_b = ""
            st.session_state.file_name_b = ""

            if st.session_state.document_text:
                st.success("Document processed! Select an analysis from the sidebar.")
            else:
                st.error("Could not extract text from the document. Please try another file.")

# --- Sidebar Information ---
st.sidebar.header("About LegalEase AI")
st.sidebar.info(
    "This app uses generative AI to analyze legal documents. "
    "It is for informational purposes only and does not constitute legal advice. "
    "Always consult with a qualified legal professional before making decisions."
)