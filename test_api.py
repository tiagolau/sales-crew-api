import sys
from unittest.mock import MagicMock

# MOCK EVERYTHING before importing main, because 'crewai' library requires Python 3.10+
# and this environment is 3.9.
mock_crew_module = MagicMock()
sys.modules['crew'] = mock_crew_module
sys.modules['crewai'] = MagicMock()
sys.modules['langchain_community.tools'] = MagicMock()

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_followup_success():
    # Setup the mock
    mock_crew_instance = mock_crew_module.SalesCrew.return_value
    mock_crew_instance.run.return_value = "Olá Carlos! Vi essa notícia sobre Turnover..."
    
    payload = {
        "client_name": "Carlos",
        "pain_points": "Turnover",
        "meeting_date": "Quinta 14h"
    }
    
    response = client.post("/generate-followup", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {
        "message": "Olá Carlos! Vi essa notícia sobre Turnover...",
        "status": "success"
    }

def test_missing_field():
    # Test validatior error (missing pain_points)
    payload = {
        "client_name": "Carlos",
        "meeting_date": "Quinta 14h"
    }
    
    response = client.post("/generate-followup", json=payload)
    assert response.status_code == 422
