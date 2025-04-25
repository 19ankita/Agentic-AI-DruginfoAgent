import os
from dotenv import load_dotenv
load_dotenv()

from agents.base_agent import BaseAgent
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
#from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool

from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from qdrant_client import QdrantClient

class ResearchAgent(BaseAgent):
    def __init__(self, collection_name: str):
        #self.search_tool = DuckDuckGoSearchRun()
        self.search_tool = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

        self.embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.qdrant_client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name

        self.vectorstore = Qdrant(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            embeddings=self.embedding
        )

        self.llm = HuggingFaceEndpoint(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            temperature=0.2,
            max_new_tokens=200,
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever()
        )

        self.agent = initialize_agent(
            tools=[
                Tool(
                    name="WebSearch",
                    func=self.search_tool.run,
                    description="Useful for real-time drug news, regulations, and external information."
                ),
                Tool(
                    name="PatientRAG",
                    func=self.qa_chain.run,
                    description="Answers questions based on patient feedback stored in vector DB."
                )
            ],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )

    def run(self, query: str) -> str:
        result = self.agent.invoke({"input": query})
        return result.get("output", str(result))
