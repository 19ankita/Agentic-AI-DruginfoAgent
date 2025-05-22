🧠 Project Overview
Agentic-AI-DruginfoAgent is an autonomous AI agent designed to provide detailed and accurate drug information. Leveraging advanced language models and vector databases, this agent can understand user queries and retrieve relevant drug data efficiently.

📄 README.md
markdown
Copy
Edit
# 💊 Agentic-AI-DruginfoAgent

An autonomous AI agent that provides comprehensive drug information by integrating advanced language models with vector databases.

## 🚀 Features

- **Natural Language Understanding**: Interprets user queries to fetch relevant drug information.
- **Vector Search Integration**: Utilizes Qdrant for efficient similarity searches.
- **Streamlit Interface**: Offers an intuitive web interface for user interaction.
- **Dockerized Deployment**: Ensures easy setup and scalability.

## 🛠️ Tech Stack

- **Programming Language**: Python
- **Frameworks & Libraries**:
  - [LangChain](https://github.com/hwchase17/langchain)
  - [Streamlit](https://streamlit.io/)
  - [Qdrant](https://qdrant.tech/)
  - [FastAPI](https://fastapi.tiangolo.com/)
- **Containerization**: Docker

## 📦 Installation
✅ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt


## ▶️ Run the Application
bash
Copy
Edit
streamlit run streamlit_app.py
The application will be accessible at http://localhost:8501

## 🐳 Docker Deployment
🔧 Build the Docker Image
bash
Copy
Edit
docker build -t druginfo-agent .

## 🚀 Run the Docker Container
bash
Copy
Edit
docker run -p 8501:8501 druginfo-agent
Visit the app at http://localhost:8501

## 📁 Project Structure
kotlin
Copy
Edit
├── agents/
│   └── agent_logic.py
├── api/
│   └── api_endpoints.py
├── data/
│   └── drug_data.csv
├── qdrant_data/
│   └── vector_store.db
├── tests/
│   └── test_agent.py
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
└── README.md

## 🧪 Testing
Run the test suite using:

bash
Copy
Edit
pytest tests/
