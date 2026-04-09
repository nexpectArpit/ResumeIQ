import io
import streamlit as st
import PyPDF2
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

# Streamlit Page Configuration
st.set_page_config(
    page_title="ResumeIQ", 
    page_icon="None", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Core LangGraph / LangChain Logic below
class AgentState(TypedDict):
    resume_text: str
    parsed_data: str
    ats_score: str
    missing_keywords: str
    suggestions: str
    final_resume: str
    groq_api_key: str

# function1
def parser_agent(state: AgentState):
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0, groq_api_key=state['groq_api_key'])
    sys_msg = SystemMessage(content="You are an expert Resume Parser. Convert raw resume text into structured text. Extract: Name, Skills, Education, Experience, and Projects.")
    user_msg = HumanMessage(content=f"Raw Resume:\n{state['resume_text']}\n\nReturn structured parsing.")
    response = llm.invoke([sys_msg, user_msg])
    return {"parsed_data": response.content}

# function2
def ats_scoring_agent(state: AgentState):
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0, groq_api_key=state['groq_api_key'])
    sys_msg = SystemMessage(content="""You are a brutally strict, highly analytical ATS (Applicant Tracking System) Evaluator. 
You MUST calculate the ATS score mathematically. Do NOT default to generic scores like 82.
Start at a BASE SCORE of 40 out of 100.
Adjust the score using this strict rubric:
+15 for having clear, distinct technical skills listed.
+20 for heavily quantified achievements (using numbers, metrics, or percentages) in experience.
+10 for strong action verbs at the start of bullet points.
+15 for excellent formatting, clean sections, and industry standard keywords.
-15 for vague, generic descriptions without impact.
-10 for missing education or contact details.

Your evaluation must be entirely objective. Be extremely harsh. Most standard resumes should score between 30 and 65. Only truly elite, highly-optimized resumes should score above 80.
""")
    user_msg = HumanMessage(content=f"""Evaluate the following parsed resume data. 
1. Calculate a strict ATS score out of 100 using the mathematical rubric above.
2. Provide a brief 1-line justification of how you calculated the points.
3. List missing keywords and weak areas specifically.

Format your response EXACTLY as follows:
SCORE: [your calculated score out of 100] ([1-line justification of points added/subtracted])
MISSING: [your specific list of missing keywords and weak areas]

Parsed Data:
{state['parsed_data']}
""")
    response = llm.invoke([sys_msg, user_msg])
    content = response.content
    
    score_part = "N/A"
    missing_part = "N/A"
    if "MISSING:" in content:
        parts = content.split("MISSING:")
        score_part = parts[0].replace("SCORE:", "").strip()
        missing_part = parts[1].strip()
    else:
        score_part = content
        missing_part = content

    return {"ats_score": score_part, "missing_keywords": missing_part}


# function3
def improvement_agent(state: AgentState):
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0, groq_api_key=state['groq_api_key'])
    sys_msg = SystemMessage(content="You are an expert Resume Coach. Provide actionable suggestions using action verbs and quantified impact.")
    user_msg = HumanMessage(content=f"""Based on parsing and missing keywords, suggest improvements. Focus on actionable bullet points and quantified impact.
Parsed Data:
{state['parsed_data']}

Missing Keywords / Weak Areas:
{state['missing_keywords']}
""")
    response = llm.invoke([sys_msg, user_msg])
    return {"suggestions": response.content}

# function4
def rewrite_agent(state: AgentState):
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0, groq_api_key=state['groq_api_key'])
    sys_msg = SystemMessage(content="You are an expert Professional Resume Writer. Write highly professional, impactful, and strong resumes.")
    user_msg = HumanMessage(content=f"""Create a professional, final rewritten resume using the following structure. Incorporate impact suggestions and missing keywords.
Parsed Data:
{state['parsed_data']}

Improvement Suggestions:
{state['suggestions']}
""")
    response = llm.invoke([sys_msg, user_msg])
    return {"final_resume": response.content}


@st.cache_resource
def build_workflow():
    workflow = StateGraph(AgentState)
    workflow.add_node("parser", parser_agent)
    workflow.add_node("ats", ats_scoring_agent)
    workflow.add_node("improve", improvement_agent)
    workflow.add_node("rewrite", rewrite_agent)
    
    workflow.set_entry_point("parser")
    workflow.add_edge("parser", "ats")
    workflow.add_edge("ats", "improve")
    workflow.add_edge("improve", "rewrite")
    workflow.add_edge("rewrite", END)
    
    return workflow.compile()

app = build_workflow()


# Helpers
def extract_text_from_pdf(uploaded_file) -> str:
    """Reset internal file pointer and extract text from PDF."""
    uploaded_file.seek(0)
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text


# Streamlit UI
def main():
    if "analysis_results" not in st.session_state:
        st.session_state["analysis_results"] = None
    if "uploaded_pdf" not in st.session_state:
        st.session_state["uploaded_pdf"] = None
    if "api_key_valid" not in st.session_state:
        st.session_state["api_key_valid"] = False

    st.title("ResumeIQ")
    st.markdown("### The Multi-Agent Resume Reviewer")
    
    # UI Control Logic: Configuration and Upload
    if st.session_state["analysis_results"] is None:
        st.subheader("Configuration")
        
        # Main Configuration Row natively scoped in a form to disable "Press Enter" hint
        with st.form("api_key_form", border=False):
            col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
            
            with col1:
                api_key = st.text_input("API Key", type="password", help="Enter your target API Key")
            
            with col2:
                validate_clicked = st.form_submit_button("Save Key", use_container_width=True)
        
        # Validation Logic Trigger
        validation_placeholder = st.empty()
        
        if validate_clicked:
            if api_key.strip():
                st.session_state["api_key_valid"] = True
            else:
                validation_placeholder.warning("Please enter a key before saving.")

        if st.session_state["api_key_valid"]:
            st.success("API Key Validated Successfully")
            st.divider()
            
            st.markdown("Upload your resume in PDF format below for a professional evaluation.")
            
            if st.session_state["uploaded_pdf"] is None:
                uploaded_file = st.file_uploader(
                    "Upload your Resume (Single PDF)", 
                    type=["pdf"], 
                    accept_multiple_files=False,
                    key="resume_uploader",
                    label_visibility="collapsed"
                )
                if uploaded_file is not None:
                    st.session_state["uploaded_pdf"] = uploaded_file
                    st.rerun()
            else:
                st.info(f"Analyzing: **{st.session_state['uploaded_pdf'].name}**")
                
                with st.spinner("Analyzing document..."):
                    raw_text = extract_text_from_pdf(st.session_state["uploaded_pdf"])
                    
                if not raw_text.strip():
                    st.error("Error: Could not extract readable text from the PDF.")
                    st.session_state["uploaded_pdf"] = None
                    if st.button("Try Again"):
                        st.rerun()
                    st.stop()
                    
                initial_state = {
                    "resume_text": raw_text,
                    "parsed_data": "",
                    "ats_score": "",
                    "missing_keywords": "",
                    "suggestions": "",
                    "final_resume": "",
                    "groq_api_key": api_key
                }
                
                with st.status("Initializing Multi-Agent Workflow...", expanded=True) as status:
                    final_state = initial_state.copy()
                    try:
                        for step_output in app.stream(initial_state):
                            for node_name, state_update in step_output.items():
                                if node_name == "parser":
                                    st.write("✅ **1. Parser Agent**: Extracted structured information from raw text.")
                                elif node_name == "ats":
                                    st.write("✅ **2. ATS Evaluator**: Assigned analytical vulnerability score.")
                                elif node_name == "improve":
                                    st.write("✅ **3. Improvement Coach**: Generated strategic performance feedback.")
                                elif node_name == "rewrite":
                                    st.write("✅ **4. Rewrite Agent**: Drafted final polished resume.")
                            
                            # Keep track of the full state as it passes through the graph
                            final_state.update(list(step_output.values())[0])

                        st.session_state["analysis_results"] = final_state
                        st.session_state["uploaded_pdf"] = None
                        status.update(label="Analysis Complete", state="complete", expanded=False)
                        st.rerun()
                        
                    except Exception as e:
                        status.update(label="Error occurred", state="error")
                        st.error(f"Execution Error: {e}")
                        if st.button("Reset"):
                            st.session_state["uploaded_pdf"] = None
                            st.rerun()
        else:
            st.info("Enter your API Key and click **Save Key** to unlock the analysis tools.")

    else:
        # Results View
        final_state = st.session_state["analysis_results"]
        
        col_res1, col_res2 = st.columns([3, 1], vertical_alignment="bottom")
        with col_res1:
            st.success("Analysis Complete")
        with col_res2:
            if st.button("Analyze New Resume", use_container_width=True):
                st.session_state["analysis_results"] = None
                st.session_state["uploaded_pdf"] = None
                st.rerun()
        
        tab1, tab2, tab3, tab4 = st.tabs(["ATS Scoring", "Keywords", "Suggestions", "Final Rewrite"])
        
        with tab1:
            st.subheader("ATS Vulnerability Score")
            st.write(final_state.get("ats_score", ""))
            
        with tab2:
            st.subheader("Missing Industry Keywords")
            st.markdown(final_state.get("missing_keywords", ""))
            
        with tab3:
            st.subheader("Performance Suggestions")
            st.markdown(final_state.get("suggestions", ""))
            
        with tab4:
            st.subheader("Rewritten Professional Draft")
            final_resume_text = final_state.get("final_resume", "")
            st.markdown(final_resume_text)
            
            st.download_button(
                label="Download Final Rewrite (TXT)",
                data=final_resume_text,
                file_name="ResumeIQ_Improved_Resume.txt",
                mime="text/plain"
            )


if __name__ == "__main__":
    main()
