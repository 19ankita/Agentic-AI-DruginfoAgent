from transformers import pipeline
from agents.base_agent import BaseAgent
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

class TranslationAgent(BaseAgent):
    def __init__(self, source_collection: str, target_collection: str):
        self.translator = pipeline("translation", 
                                   model="Helsinki-NLP/opus-mt-mul-en",
                                   token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
                                   )
        
        self.client = QdrantClient(host="localhost", port=6333)
        self.embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.source_collection = source_collection
        self.target_collection = target_collection

    def run(self) -> str:
        vectorstore = Qdrant(
            client=self.client,
            collection_name=self.source_collection,
            embeddings=self.embedding
        )
        docs = vectorstore.similarity_search(query="*", k=10)
        translated_docs = [
            self.translator(doc.page_content, max_length=512)[0]["translation_text"]
            for doc in docs
        ]
        if not self.client.collection_exists(self.target_collection):
            self.client.create_collection(
                collection_name=self.target_collection,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
        Qdrant.from_texts(
            translated_docs,
            embedding=self.embedding,
            url="http://localhost:6333",
            collection_name=self.target_collection
        )
        return f"Translated and stored {len(translated_docs)} English documents in '{self.target_collection}'"
