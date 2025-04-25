from agents.ingestor_agent import IngestorAgent
from agents.translation_agent import TranslationAgent
from agents.research_agent import ResearchAgent
from agents.insightReport_agent import InsightReportAgent

def test_ingestor_agent():
    agent = IngestorAgent("data/multilingual_patient_feedback.csv", "test_ingest_collection")
    result = agent.run()
    assert "Uploaded" in result

def test_translation_agent():
    agent = TranslationAgent("test_ingest_collection", "test_translated_collection")
    result = agent.run()
    assert "Translated and stored" in result



def test_research_to_insight_report_pipeline(tmp_path):
    # Step 1: ResearchAgent gets the answer
    research_agent = ResearchAgent(collection_name="test_translated_collection")
    question = "What are common side effects of chemotherapy?"
    answer = research_agent.run(question)
    assert isinstance(answer, str) and len(answer.strip()) > 0

    # Step 2: InsightReportAgent summarizes + generates report
    insight_agent = InsightReportAgent()
    report_path = tmp_path / "insight_report.md"
    result = insight_agent.run(answer, question=question, path=str(report_path))

    # Step 3: Assert and output
    assert report_path.exists()
    print(f"\n Insight report content:\n{open(report_path).read()}")
    print(f"\n {result}")


