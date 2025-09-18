
import streamlit as st
import google.generativeai as genai
import os

def get_gemini_response(api_key, prompt, document_text):
    """Queries the Gemini API to get a response based on the prompt and document."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = f"{prompt}\n\n---\n\nDocument:\n\n{document_text}"
        
        with st.spinner("AI is analyzing the document for risks and obligations..."):
            response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

st.set_page_config(page_title="Risk & Obligation Detector", page_icon="🚨")

st.title("🚨 Risk & Obligation Detector")

st.write("This page scans the document for potential red flags, your key obligations, and questions you might want to ask a lawyer.")

document_text = st.session_state.get("document_text", "")

if document_text:
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error("API Key is not configured. Please contact the administrator.")
    else:
        role_options = ["", "Tenant", "Landlord", "Borrower", "Lender", "Employee", "Employer", "Contractor", "Client", "General User"]
        role = st.selectbox("Select your role in this agreement:", options=role_options, key="role_risk")

        st.info("Click the button below to generate the risk analysis from your perspective.")
        if st.button("Analyze Risks & Obligations", key="risk_button"):
            if role:
                prompt = (f"Analyze the following legal document from the perspective of the '{role}'. "
                          "Create three distinct sections using markdown: '## 🚩 Potential Red Flags', '## 📝 Key Obligations', and '## ⚖️ Questions to Ask a Lawyer'."
                          "Under 'Red Flags', identify any clauses that seem unusually one-sided, contain hidden fees, auto-renewal traps, or are generally unfavorable to you as the '{role}'."
                          "Under 'Key Obligations', list your specific duties, deadlines, notice requirements, and potential penalties."
                          "Under 'Questions to Ask a Lawyer', suggest specific, pointed questions about ambiguous or high-risk clauses that you, as the '{role}', should have a legal professional review.")

                analysis = get_gemini_response(api_key, prompt, document_text)
                
                # Process and display the analysis in expanders
                st.subheader(f"Analysis for: {role}")
                sections = analysis.split('## ')
                
                # Filter out empty strings that may result from splitting
                sections = [s for s in sections if s.strip()]

                with st.expander("🚩 Potential Red Flags", expanded=True):
                    red_flags = next((s for s in sections if s.startswith('🚩 Potential Red Flags')), None)
                    if red_flags:
                        st.markdown(red_flags.replace("🚩 Potential Red Flags", ""), unsafe_allow_html=True)
                    else:
                        st.write("No specific red flags identified.")

                with st.expander("📝 Key Obligations", expanded=True):
                    obligations = next((s for s in sections if s.startswith('📝 Key Obligations')), None)
                    if obligations:
                        st.markdown(obligations.replace("📝 Key Obligations", ""), unsafe_allow_html=True)
                    else:
                        st.write("No specific key obligations identified.")

                with st.expander("⚖️ Questions to Ask a Lawyer", expanded=True):
                    questions = next((s for s in sections if s.startswith('⚖️ Questions to Ask a Lawyer')), None)
                    if questions:
                        st.markdown(questions.replace("⚖️ Questions to Ask a Lawyer", ""), unsafe_allow_html=True)
                    else:
                        st.write("No specific questions suggested.")

            else:
                st.warning("Please enter your role to get a personalized analysis.")

    st.subheader("Full Document Text")
    with st.expander("Click to view the full text"):
        st.text_area("", document_text, height=300)
else:
    st.warning("Please upload a document on the main page first.")
    st.page_link("app.py", label="Back to Home", icon="🏠")
