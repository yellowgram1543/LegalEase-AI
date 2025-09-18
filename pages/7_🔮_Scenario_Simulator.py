
import streamlit as st
import google.generativeai as genai
import os

def get_gemini_response(api_key, prompt, document_text, scenario):
    """Queries the Gemini API to simulate a scenario based on the document."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = f"{prompt}\n\n---\n\nDOCUMENT:\n{document_text}\n\n---\n\nSCENARIO:\n{scenario}"
        
        with st.spinner("AI is simulating the scenario based on the document..."):
            response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

st.set_page_config(page_title="Scenario Simulator", page_icon="🔮")

st.title("🔮 Scenario Simulator")

st.write("Ask a 'What if...' question to simulate the consequences based on the document's clauses.")

document_text = st.session_state.get("document_text", "")

if document_text:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key is not configured. Please contact the administrator.")
    else:
        scenario = st.text_area("Describe a scenario:", 
                                placeholder="e.g., What if I miss a rent payment by 5 days? What if I need to terminate the contract 6 months early?", 
                                key="scenario_input", height=100)

        if st.button("Simulate Consequences", key="scenario_button"):
            if scenario:
                prompt = ("You are a scenario simulator. Based ONLY on the legal document provided, explain the likely consequences of the described scenario. "
                          "Present the outcome as a step-by-step breakdown or timeline of events. "
                          "Quote the specific clauses from the document that determine the outcome, including clause numbers if available. "
                          "Do not invent consequences not supported by the text. If the document does not specify a consequence, state that clearly.")

                answer = get_gemini_response(api_key, prompt, document_text, scenario)
                
                st.subheader("Simulation Result")
                st.markdown(answer, unsafe_allow_html=True)
            else:
                st.warning("Please describe a scenario to simulate.")

else:
    st.warning("Please upload a document on the main page first.")
    st.page_link("app.py", label="Back to Home", icon="🏠")

