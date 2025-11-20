import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import os
import json

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

st.title("PDF Analyzer Agent")
st.subheader("Upload the legislative PDF of internship assignment")

file = st.file_uploader("Upload PDF", type=["pdf"])

sections = [
    "Summary",
    "Key Legislative Sections (JSON)",~
    "Legislative Rule Checks",
    "Generate Full Final Report JSON"
]

task = st.selectbox("Select a task", sections)

if file:
    file_path = "uploaded.pdf"
    with open(file_path, "wb") as f:
        f.write(file.read())

    loader = PyPDFLoader(file_path)
    docs = loader.load()
    full_text = "\n".join([d.page_content for d in docs])

    parser = StrOutputParser()
    json_parser = JsonOutputParser()

    summary_prompt = PromptTemplate(
        template="""
Summarize the Universal Credit Act 2025 in 5–10 bullet points focusing on:
- Purpose
- Key definitions
- Eligibility
- Obligations
- Enforcement elements

TEXT:
{text}
""",
        input_variables=["text"]
    )

    section_prompt = PromptTemplate(
    template="""
Extract the following fields in STRICT JSON:

{{
  "definitions": "",
  "obligations": "",
  "responsibilities": "",
  "eligibility": "",
  "payments": "",
  "penalties": "",
  "record_keeping": ""
}}

TEXT:
{text}

Return ONLY valid JSON.
""",
    input_variables=["text"]
)

    rules = [
        "Act must define key terms",
        "Act must specify eligibility criteria",
        "Act must specify responsibilities of the administering authority",
        "Act must include enforcement or penalties",
        "Act must include payment calculation or entitlement structure",
        "Act must include record-keeping or reporting requirements"
    ]

    rule_prompt = PromptTemplate(
        template="""
Check this rule strictly against the legislative text.

RULE: "{rule}"

Return JSON:
{{
  "rule": "{rule}",
  "status": "",
  "evidence": "",
  "confidence": ""
}}

TEXT:
{text}

Return ONLY JSON.
""",
        input_variables=["rule", "text"]
    )

    if task == "Summary":
        summary_chain = summary_prompt | llm | parser
        result = summary_chain.invoke({"text": full_text})
        st.subheader("Summary Output")
        st.write(result)

    elif task == "Key Legislative Sections (JSON)":
        section_chain = section_prompt | llm | json_parser
        result = section_chain.invoke({"text": full_text})
        st.subheader("Structured Sections")
        st.json(result)

    elif task == "Legislative Rule Checks":
        rule_chain = rule_prompt | llm | json_parser
        outputs = []
        for r in rules:
            outputs.append(rule_chain.invoke({"rule": r, "text": full_text}))
        st.subheader("Rule Validation Results")
        st.json(outputs)

    elif task == "Generate Full Final Report JSON":
        summary_chain = summary_prompt | llm | parser
        summary_output = summary_chain.invoke({"text": full_text})

        section_chain = section_prompt | llm | json_parser
        sections_json = section_chain.invoke({"text": full_text})

        rule_chain = rule_prompt | llm | json_parser
        rule_results = []
        for r in rules:
            rule_results.append(rule_chain.invoke({"rule": r, "text": full_text}))

        final_report = {
            "summary": summary_output,
            "sections": sections_json,
            "rule_checks": rule_results
        }

        with open("final_report.json", "w", encoding="utf-8") as f:
            json.dump(final_report, f, indent=4, ensure_ascii=False)

        st.subheader("Final Report JSON")
        st.json(final_report)
        st.success("Saved as final_report.json")
