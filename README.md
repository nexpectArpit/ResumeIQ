# ResumeIQ: The Multi-Agent Resume Reviewer

ResumeIQ is a professional-grade, AI-driven resume optimization suite. Built with **Streamlit**, **LangChain**, and **LangGraph**, it orchestrates a specialized workforce of four AI agents to transform raw resumes into high-performance, ATS-ready professional documents.

## 🧠 The Agent Workforce

ResumeIQ utilizes a sequential Language Graph (LangGraph) to pass state through four independent intelligence layers:

1.  **Parser Agent**: Deconstructs raw PDF extraction into structured professional entities (Skills, Education, Experience).
2.  **ATS Evaluator (Mathematical)**: Performs a non-polite, rubric-based mathematical scoring (starting from base 40) to provide realistic ATS feedback.
3.  **Improvement Coach**: Analyzes bullet points to suggest quantifiable impact (using metrics and action verbs).
4.  **Rewrite Agent**: Crafts the final polished document, synthesizing feedback and keywords into a professional draft.

## ✨ Key Features

-   **Dynamic Agent Streaming**: Watch the agents report their progress step-by-step with real-time feedback.
-   **Zero-CSS Native UI**: Optimized for stability and professional aesthetics using native Streamlit layout primitives.
-   **Mathematical ATS Rubric**: No "polite" generic scores; get a hard, analytical calculation of your resume's strength.
-   **Instant Processing**: Zero-latency workflow—the moment you drop your PDF, the agent workflow initializes automatically.
-   **Privacy First**: No files are stored locally; all data lives in session state and is purged immediately after use.

## 🚀 Setup & Installation

### 1. Requirements
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt
```

### 2. Local Execution
Run the application using Streamlit:
```bash
streamlit run multi_agent_system.py
```

## ☁️ Deployment Guide (Streamlit Cloud)

### 1. Prep for Git
Before pushing, ensure your `.gitignore` includes:
```text
.env
.venv/
__pycache__/
```

### 2. Git Commands
Initialize your repo and push to GitHub:
```bash
git init
git add .
git commit -m "Initial release of ResumeIQ"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 3. Streamlit Cloud Deploy
1. Sign in to [share.streamlit.io](https://share.streamlit.io/).
2. Click **"New app"**.
3. Select this repository and the `main` branch.
4. Set the main file path to `multi_agent_system.py`.
5. Click **Deploy!**
