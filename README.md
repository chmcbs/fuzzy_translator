# Fuzzy Translator

A simple translation API for English to Korean using the [Facebook NLLB](https://huggingface.co/facebook/nllb-200-distilled-600M) transformer from HuggingFace.

---

### Installation
- Clone this repository

**With Docker:**

- `docker build -t fuzzy_translator .`
- `docker run -p 8000:8000 fuzzy_translator`

**Without Docker:**
- Create a fresh virtual environment (recommended)
- `pip install -r requirements.txt`
- `uvicorn app:app --reload`

---

### Example Usage
- `curl -X POST "http://127.0.0.1:8000/translate" -H "Content-Type: application/json" -d '"YOUR TEXT HERE"'`
- Interactive API docs (Swagger UI) can be found at **http://127.0.0.1:8000/docs**

---

### Testing

**With Docker:**
- `docker run fuzzy pytest tests.py`

**Locally:**
- `pytest tests.py`