"""FastAPI app for translating English to Korean"""

from fastapi import FastAPI, Body, Request, HTTPException
from fastapi.responses import JSONResponse
from transformers import pipeline
from contextlib import asynccontextmanager

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

# Define the translation function
def translate_eng_kor(text: str):
    translation = app.state.translator(text, src_lang="eng_Latn", tgt_lang="kor_Hang", max_new_tokens=200)
    return translation[0]["translation_text"]

@app.post("/translate")
def translate(text: str = Body(..., min_length=1, max_length=100)):
    """Translate text from English to Korean"""
    if not hasattr(app.state, "translator"):
        raise HTTPException(status_code=503, detail="Translator not loaded")
    return translate_eng_kor(text)

@app.get("/health")
def health():
    """Check the health of the server"""
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    return JSONResponse(status_code=500, content={"error": "Internal server error"})