import os
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry

from agents.ingestor_agent import IngestorAgent
from agents.translation_agent import TranslationAgent
from agents.research_agent import ResearchAgent
from agents.insightReport_agent import InsightReportAgent

# Default collection for Qdrant
COLLECTION_NAME = os.getenv("DEFAULT_QDRANT_COLLECTION", "test_translated_collection")

@strawberry.type
class Mutation:
    @strawberry.mutation
    def ingest_csv(self, path: str, collection: str) -> str:
        return IngestorAgent(path, collection).run()

    @strawberry.mutation
    def translate_collection(self, source: str, target: str) -> str:
        return TranslationAgent(source, target).run()

    @strawberry.mutation
    def research_topic(self, query: str) -> str:
        return ResearchAgent(collection_name=COLLECTION_NAME).run(query)

    @strawberry.mutation
    def generate_insight_report(self, text: str, question: str = "Summarize the following text") -> str:
        return InsightReportAgent().run(text=text, question=question)

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from DruginfoAgent!"

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI(title="DruginfoAgent Agent API")

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": " Welcome to DruginfoAgent - Agentic API powered by FastAPI & Strawberry GraphQL"}
