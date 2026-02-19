from fastapi.testclient import TestClient
from app import app

# Mock translator function
def mock_translator(text, **kwargs):
    return [{"translation_text": "안녕하세요!"}]

app.state.translator = mock_translator

client = TestClient(app)

# Test endpoints
def test_translate_success():
    response = client.post("/translate", content='"Hello!"', headers={"Content-Type": "application/json"})
    assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# Test input validation
def test_translate_too_long():
    long_text = '"' + "test " * 50 + '"'
    response = client.post("/translate", content=long_text, headers={"Content-Type": "application/json"})
    assert response.status_code == 422

def test_translate_empty_string():
    response = client.post("/translate", content='""', headers={"Content-Type": "application/json"})
    assert response.status_code == 422