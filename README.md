# Fuzzy Translator

A simple translation API for English to Korean using the [Facebook NLLB](https://huggingface.co/facebook/nllb-200-distilled-600M) transformer from HuggingFace.

### Installation
- Clone this repository
- Create a fresh virtual environment in your IDE of choice
- Install dependencies (`pip install -r requirements.txt`)
- Start a uvicorn server (`uvicorn app:app --reload`)

### Example Usage
- With uvicorn running, open a **new terminal tab** and enter your text to be translated:
`curl -X POST "http://127.0.0.1:8000/translate" -H "Content-Type: application/json" -d '"YOUR TEXT HERE"'`
- Interactive API docs (Swagger UI) can be found at **http://127.0.0.1:8000/docs**

### Testing
- Run tests with `pytest tests.py`