from agents.base_agent import BaseAgent
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

class IngestorAgent(BaseAgent):
    def __init__(self, csv_path: str, collection_name: str):
        self.csv_path = csv_path
        self.collection_name = collection_name
        self.embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.client = QdrantClient(host="localhost", port=6333)

    def run(self) -> str:
        loader = CSVLoader(file_path=self.csv_path, 
                           csv_args={"delimiter": ","},
                           encoding="utf-8")
        
        documents = loader.load()
        
        # Split long documents
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.split_documents(documents)
            
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

        Qdrant.from_documents(
            documents=docs,
            embedding=self.embedding,
            url="http://localhost:6333",
            collection_name=self.collection_name
        )
        return f"Uploaded {len(documents)} documents to '{self.collection_name}'"