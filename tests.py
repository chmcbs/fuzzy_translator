from fastapi.testclient import TestClient
from app import app, SUPPORTED_LANGUAGES

def mock_translator(text, **kwargs):
    return [{"translation_text": "안녕하세요!"}]

app.state.translator = mock_translator

client = TestClient(app)

def test_translate_success():
    response = client.post("/translate", json={"text": "Hello!", "source": "english", "target": "korean"})
    assert response.status_code == 200
    assert response.json() == "안녕하세요!"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_languages():
    response = client.get("/languages")
    assert response.status_code == 200
    assert response.json() == list(SUPPORTED_LANGUAGES.keys())

def test_unsupported_language():
    response = client.post("/translate", json={"text": "Hello!", "source": "english", "target": "italian"})
    assert response.status_code == 422

def test_translate_too_long():
    long_text = "test " * 50
    response = client.post("/translate", json={"text": long_text, "source": "english", "target": "korean"})
    assert response.status_code == 422

def test_translate_empty_string():
    response = client.post("/translate", json={"text": "", "source": "english", "target": "korean"})
    assert response.status_code == 422