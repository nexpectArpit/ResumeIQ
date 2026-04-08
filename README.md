# ResumeIQ: Professional Multi-Agent Resume Optimization

ResumeIQ is an advanced AI-driven suite designed to bridge the gap between talented professionals and complex Applicant Tracking Systems (ATS). By orchestrating a sequential workforce of four specialized agents, ResumeIQ transforms raw, unoptimized resumes into high-impact professional documents.

## 🌉 The Multi-Agent Pipeline

The core of ResumeIQ is a **Stateful Language Graph** that maintains context as it passes your information through four distinct stages of intelligence:

```mermaid
graph LR
    User([PDF Upload]) --> Parser{{1. Parser Agent}}
    Parser --> ATS{{2. ATS Evaluator}}
    ATS --> Coach{{3. Improvement Coach}}
    Coach --> Rewrite{{4. Rewrite Agent}}
    Rewrite --> Result([Final Optimized Draft])
    
    style User fill:#f9f,stroke:#333,stroke-width:2px
    style Result fill:#00ff00,stroke:#333,stroke-width:2px
```

### 🧠 Agent Responsibilities

1.  **Parser Agent**: Strategically deconstructs the PDF into structured data (Skills, Education, Experience) ensuring no vital info is lost in transit.
2.  **ATS Evaluator (Mathematical)**: Applies a cold, objective mathematical rubric (starting from base 40) to calculate your resume's "vulnerability score" based on keywords and metrics.
3.  **Improvement Coach**: Identifies weak bullet points and coaches you on quantifying impact using specific industry action verbs.
4.  **Rewrite Agent**: Synthesizes all criticisms and keywords into a final, polished draft that is ready for submission.

## 🔑 Bring Your Own Key (BYOK)

To ensure maximum security and privacy, **ResumeIQ does not store API keys.** 
- When running locally or on the deployed version, you must provide your own **Groq API Key** (or compatible vendor key).
- All processing happens in-memory and is purged immediately after your session ends.

---

## 💻 Local Setup & Development

Follow these steps to get ResumeIQ running on your local machine:

### 1. Environment Preparation
Create and activate a virtual environment to keep your dependencies isolated:

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the Streamlit web server:
```bash
streamlit run multi_agent_system.py
```

### 🛑 How to stop & Clean up

- **Stop the App**: Press `Ctrl + C` in your terminal to shut down the Streamlit server.
- **Deactivate Environment**: Once you are done, simply run:
  ```bash
  deactivate
  ```
