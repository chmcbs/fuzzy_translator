"""FastAPI app for translating English to Korean"""

from fastapi import FastAPI, Body
from transformers import pipeline

app = FastAPI()

# Initialise the Facebook NLLB translator
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M")

def translate_eng_kor(text: str):
    """Translate text from English to Korean"""
    translation = translator(text, src_lang="eng_Latn", tgt_lang="kor_Hang")
    return translation[0]["translation_text"] # translation is a list of dictionaries, so this is required to extract the translated string

@app.post("/translate")
def translate(text: str = Body()): # Body() extracts the string from the body of the request
    return translate_eng_kor(text)