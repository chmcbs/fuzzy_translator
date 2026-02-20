"""Multi-language FastAPI translation API using Facebook NLLB"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from transformers import pipeline
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field, field_validator

SUPPORTED_LANGUAGES = {
    "english": "eng_Latn",
    "korean": "kor_Hang",
    "chinese_simplified": "zho_Hans",
    "chinese_traditional": "zho_Hant",
    "spanish": "spa_Latn",
    "greek": "ell_Grek",
}

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=100)
    source: str
    target: str

    @field_validator("source", "target")
    @classmethod
    def validate_language(cls, v: str):
        if v.lower() not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {v}. Supported: {list(SUPPORTED_LANGUAGES.keys())}")
        return v.lower()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Preload the translator before the app starts"""
    print("Loading translator...")
    try:
        app.state.translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")
        print("Translator loaded successfully.")
    except Exception as e:
        print(f"Error loading translator: {e}")
        raise
    yield

app = FastAPI(lifespan=lifespan)

def translate_text(text: str, source: str, target: str):
    translation = app.state.translator(text, src_lang=source, tgt_lang=target, max_new_tokens=200)
    return translation[0]["translation_text"]

@app.post("/translate")
def translate(request: TranslateRequest):
    if not hasattr(app.state, "translator"):
        raise HTTPException(status_code=503, detail="Translator not loaded")
    return translate_text(request.text, SUPPORTED_LANGUAGES[request.source], SUPPORTED_LANGUAGES[request.target])

@app.get("/languages")
def languages():
    return list(SUPPORTED_LANGUAGES.keys())

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})