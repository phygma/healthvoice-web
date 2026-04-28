'''from fastapi import APIRouter, UploadFile, File
import whisper
import os

router = APIRouter()

model = None

def get_model():
    global model
    if model is None:
        print("Loading Whisper tiny...")
        model = whisper.load_model("tiny")
    return model

@router.post("/")
async def asr(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    m = get_model()
    result = m.transcribe(path)

    os.remove(path)

    return {"text": result["text"]}'''
'''from fastapi import APIRouter, UploadFile, File
import whisper
import os

router = APIRouter()

model = None

def get_model():
    global model
    if model is None:
        print("Loading Whisper tiny...")
        model = whisper.load_model("tiny")
    return model

@router.post("/")
async def asr(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    m = get_model()

    result = m.transcribe(path, fp16=False)

    os.remove(path)

    return {"text": result["text"].strip()}'''
from fastapi import APIRouter, UploadFile, File, Form
import whisper
import os
import uuid

router = APIRouter()
model = None

def get_model():
    global model
    if model is None:
        print("Loading Whisper tiny model...")
        model = whisper.load_model("tiny")
        print("✅ Whisper tiny loaded")
    return model

# Load model at startup so first request isn't slow
get_model()

@router.post("/")
async def asr(
    file: UploadFile = File(...),
    lang: str = Form("hi")  # language code: hi, ta, bn, te, mr
):
    # Save with UUID filename to prevent collisions
    ext = os.path.splitext(file.filename)[1] or ".webm"
    temp_path = f"uploads/temp_{uuid.uuid4()}{ext}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        m = get_model()

        # Map language codes to Whisper language names
        lang_map = {
            "hi": "hindi",
            "bn": "bengali",
            "ta": "tamil",
            "te": "telugu",
            "mr": "marathi",
        }
        whisper_lang = lang_map.get(lang, "hindi")

        result = m.transcribe(
            temp_path,
            language=whisper_lang,
            fp16=False  # fp16=False required on CPU
        )

        return {"text": result["text"].strip()}

    except Exception as e:
        return {"error": str(e), "text": ""}

    finally:
        # Always clean up temp file even if transcription fails
        if os.path.exists(temp_path):
            os.remove(temp_path)