import pytest
from fastapi.testclient import TestClient
from api.main import app  # Make sure your FastAPI app is in `api/main.py`

client = TestClient(app)

@pytest.mark.parametrize("query,expected_key", [
    (
        '''
        mutation {
            ingestCsv(path: "data/multilingual_feedback.csv", collection: "graphql_test_ingest")
        }
        ''',
        "ingestCsv"
    ),
    (
        '''
        mutation {
            translateCollection(source: "graphql_test_ingest", target: "graphql_test_translated")
        }
        ''',
        "translateCollection"
    ),
    (
        '''
        mutation {
            researchTopic(query: "What is Metformin?")
        }
        ''',
        "researchTopic"
    ),
    (
        '''
        mutation {
            summarizeText(text: "Metformin is commonly used to treat type 2 diabetes. " repeated 10 times)
        }
        ''',
        "summarizeText"
    ),
])
def test_graphql_mutations(query, expected_key):
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data and expected_key in data["data"]
