import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from agents.base_agent import BaseAgent
from langchain.chains.summarize import load_summarize_chain
from langchain_community.llms import HuggingFaceHub
from langchain_core.documents import Document

class InsightReportAgent(BaseAgent):
    def __init__(self):
        self.llm = HuggingFaceHub(
            repo_id="google/flan-t5-base",
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            model_kwargs={
                "temperature": 0.3,
                "max_length": 200
            },
        )
        self.chain = load_summarize_chain(self.llm, chain_type="stuff")

    def run(self, text: str, question: str = "Summarize the following text", path: str = "insight_report.md") -> str:
        if not text.strip():
            return "❗️No text provided to summarize."

        docs = [Document(page_content=text)]
        result = self.chain.invoke(docs)
        summary = result["output_text"]

        report = f"""
## Patient Insight Report

**Date:** {datetime.now().strftime('%Y-%m-%d')}

**Question:**
{question}

**Answer:**
{summary}
"""
        with open(path, "w") as f:
            f.write(report)

        return f"Report generated at `{path}`"
