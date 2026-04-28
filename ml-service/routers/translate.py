'''from fastapi import APIRouter
from pydantic import BaseModel
from deep_translator import GoogleTranslator

router = APIRouter()

class TranslateRequest(BaseModel):
    text: str
    source: str = "auto"
    target: str = "en"

@router.post("/")
def translate(req: TranslateRequest):
    result = GoogleTranslator(
        source=req.source,
        target=req.target
    ).translate(req.text)

    return {"translated": result}'''
'''from fastapi import APIRouter
from pydantic import BaseModel
from deep_translator import GoogleTranslator

router = APIRouter()

class TranslateRequest(BaseModel):
    text: str
    source: str = "auto"
    target: str = "en"

@router.post("/")
def translate(req: TranslateRequest):
    result = GoogleTranslator(
        source=req.source,
        target=req.target
    ).translate(req.text)

    return {
        "translated": result
    }'''
from fastapi import APIRouter
from pydantic import BaseModel
from deep_translator import GoogleTranslator

router = APIRouter()

# Map our language codes to codes deep-translator understands
LANG_MAP = {
    "hi": "hi",   # Hindi
    "bn": "bn",   # Bengali
    "ta": "ta",   # Tamil
    "te": "te",   # Telugu
    "mr": "mr",   # Marathi
    "en": "en",   # English (fallback)
}

class TranslateRequest(BaseModel):
    text: str
    sourceLang: str = "hi"   # matches what Node.js sends
    targetLang: str = "en"   # matches what Node.js sends

@router.post("/")
def translate(req: TranslateRequest):
    try:
        source = LANG_MAP.get(req.sourceLang, "auto")
        target = LANG_MAP.get(req.targetLang, "en")

        result = GoogleTranslator(
            source=source,
            target=target
        ).translate(req.text)

        return {
            "translatedText": result  # matches what Node.js expects
        }

    except Exception as e:
        print(f"Translation error: {e}")
        return {
            "translatedText": req.text,  # fallback: return original text
            "error": str(e)
        }