# **PDF analyzer Agent**

This project is my submission for the 48-Hour AI Internship Assignment.
The goal is to design an AI-powered PDF Analyzer Agent that can:

✔ Extract full text from a legislative PDF <br>
✔ Summarize the Act <br>
✔ Extract structured sections in JSON <br>
✔ Evaluate the Act against legislative rule checks <br>
✔ Generate a final machine-readable JSON report <br>
✔ Provide an interactive Streamlit UI <br>

## 🚀 Features
### 1️⃣ Upload & Extract Text

Upload any legislative PDF.

Extracts clean, structured text using PyPDFLoader.

### 2️⃣ Summary Generator

Generates a 5–10 point summary covering:

Purpose <br>
Key definitions <br>
Eligibility <br>
Obligations <br>
Enforcement elements <br>

Uses Gemini 2.5 Flash with LangChain.

### 3️⃣ Key Legislative Sections in JSON

Extracts structured sections:

{
  "definitions": "",
  "obligations": "",
  "responsibilities": "",
  "eligibility": "",
  "payments": "",
  "penalties": "",
  "record_keeping": ""
}

### 4️⃣ Legislative Rule Checks

Checks the act against 6 mandatory rules:

Defines key terms<br>
Specifies eligibility<br>
Specifies administrative responsibilities<br>
Mentions enforcement/penalties<br>
Includes payment/entitlement calculation<br>
Includes record-keeping or reporting requirements<br>

Outputs each check as JSON with:status, evidence and confidence score

### 5️⃣ Generate Final Report JSON

Combines Summary ,Key sections, Rule results and exports them into "final_report.json" for submission.

## 🚀 Tech Stack <br>
Component	Tools Used <br>
LLM	:Google Gemini 2.5 Flash <br>
Framework:LangChain <br>
UI:	Streamlit <br>
PDF Loading:PyPDFLoader <br>
JSON Parsing:LangChain JSON Parser<br>
Environment	Python 3.11 + Virtualenv<br>

## 📁 Project Structure<br>
```
📁 internship_agent
│── 📁venv
│── project.py 
│── final_report.json  
│── requirements.txt
│── README.md
│── uploaded.pdf (runtime)
│── .env 
│── .gitignore
```
## ⚙️Installation & Setup
1. Clone the Repo
git clone https://github.com/<your-username>/legislative-pdf-agent.git
cd legislative-pdf-agent

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

3. Install Requirements
pip install -r requirements.txt

4. Add API Key

Create a .env file:

GOOGLE_API_KEY=your_key_here

5. Run the App
streamlit run proj.py

## 🖼️ How It Works
```
Upload the PDF
Choose a task:
Summary
Key Sections
Rule Checks
Full Report
AI analyzes the PDF using LangChain + Gemini
Output is displayed in the UI and JSON is saved
```

## 🏗️ Architecture Overview
```
✔ Document Loader → PyPDFLoader
✔ Text Processing → LangChain PromptTemplate
✔ LLM → Gemini 2.5 Flash
✔ Chain Composition → LCEL (LangChain Expression Language)
✔ JSON Parsing → JsonOutputParser
✔ UI → Streamlit
```
The system uses a modular chain architecture, allowing each task to be independently executed using the same extracted text.

### Thank You for visiting❤️