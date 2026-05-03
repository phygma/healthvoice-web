'''from fastapi import APIRouter
from pydantic import BaseModel
from gtts import gTTS
import uuid

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    lang: str = "en"

@router.post("/")
def tts(req: TTSRequest):
    filename = f"audio_{uuid.uuid4().hex}.mp3"
    gTTS(text=req.text, lang=req.lang).save(filename)

    return {"file": filename}'''

'''from fastapi import APIRouter
from pydantic import BaseModel
from gtts import gTTS
import uuid

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    lang: str = "en"

@router.post("/")
def tts(req: TTSRequest):
    filename = f"audio_{uuid.uuid4().hex}.mp3"

    tts = gTTS(text=req.text, lang=req.lang)
    tts.save(filename)

    return {
        "file": filename
    }'''
'''from fastapi import APIRouter
from pydantic import BaseModel
from gtts import gTTS
import uuid
import os

router = APIRouter()

# Map language codes to gTTS supported codes
LANG_MAP = {
    "hi": "hi",   # Hindi
    "bn": "bn",   # Bengali
    "ta": "ta",   # Tamil
    "te": "te",   # Telugu
    "mr": "mr",   # Marathi
    "en": "en",   # English
}

class TTSRequest(BaseModel):
    text: str
    lang: str = "hi"          # language code
    outputPath: str = ""      # optional — Node.js may send this

@router.post("/")
def tts(req: TTSRequest):
    try:
        lang_code = LANG_MAP.get(req.lang, "hi")

        # Always save to uploads/ folder so /audio/ can serve it
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        save_path = os.path.join("uploads", filename)

        os.makedirs("uploads", exist_ok=True)

        tts_obj = gTTS(text=req.text, lang=lang_code)
        tts_obj.save(save_path)

        return {
            "filename": filename,              # just the filename
            "audioPath": save_path,            # relative path
            "audioUrl": f"/audio/{filename}"   # URL to access via /audio/
        }

    except Exception as e:
        print(f"TTS error: {e}")
        return {
            "filename": "",
            "audioPath": "",
            "audioUrl": "",
            "error": str(e)
        }'''
from fastapi import APIRouter
from pydantic import BaseModel
from gtts import gTTS
import uuid
import os

router = APIRouter()

# Map language codes to gTTS supported codes
LANG_MAP = {
    "hi": "hi",   # Hindi
    "bn": "bn",   # Bengali
    "ta": "ta",   # Tamil
    "te": "te",   # Telugu
    "mr": "mr",   # Marathi
    "en": "en",   # English
}

class TTSRequest(BaseModel):
    text: str
    lang: str = "hi"          # language code
    outputPath: str = ""      # optional — Node.js may send this

@router.post("/")
def tts(req: TTSRequest):
    try:
        lang_code = LANG_MAP.get(req.lang, "hi")

        # Always save to uploads/ folder so /audio/ can serve it
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        save_path = os.path.join("uploads", filename)

        os.makedirs("uploads", exist_ok=True)

        tts_obj = gTTS(text=req.text, lang=lang_code)
        tts_obj.save(save_path)

        return {
            "filename": filename,              # just the filename
            "audioPath": save_path,            # relative path
            "audioUrl": f"/audio/{filename}"   # URL to access via /audio/
        }

    except Exception as e:
        print(f"TTS error: {e}")
        return {
            "filename": "",
            "audioPath": "",
            "audioUrl": "",
            "error": str(e)
        }