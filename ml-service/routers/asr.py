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
'''from fastapi import APIRouter, UploadFile, File, Form
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
            os.remove(temp_path)'''
from fastapi import APIRouter, UploadFile, File, Form
import whisper
import os
import uuid

router = APIRouter()

# Whisper small — better Hindi accuracy, fits in 8GB RAM
model = whisper.load_model("small")
print("✅ Whisper small model loaded")

LANG_MAP = {
    "hi": "hi",
    "bn": "bn",
    "ta": "ta",
    "te": "te",
    "mr": "mr",
    "en": "en",
}

# Native script prompts — small model handles these reliably
# Forces correct script output without causing hallucination loops
INITIAL_PROMPTS = {
    "hi": "मुझे बुखार है और सिर दर्द है।",
    "mr": "मला ताप आहे आणि डोकेदुखी आहे।",
    "bn": "আমার জ্বর আছে এবং মাথাব্যথা আছে।",
    "ta": "எனக்கு காய்ச்சல் இருக்கிறது.",
    "te": "నాకు జ్వరం ఉంది.",
    "en": None,
}

def is_hallucination(text: str) -> bool:
    """Detect repetition loops from Whisper hallucination"""
    if not text or len(text.strip()) < 2:
        return True
    words = text.strip().split()
    if len(words) == 0:
        return True
    # If more than 60% of words are the same word
    if len(words) >= 3:
        most_common = max(set(words), key=words.count)
        if words.count(most_common) / len(words) > 0.6:
            return True
    # If almost no unique characters
    if len(set(text.replace(" ", ""))) < 3:
        return True
    return False

@router.post("/")
async def asr(
    file: UploadFile = File(...),
    lang: str = Form("hi")
):
    ext  = os.path.splitext(file.filename)[1] or ".webm"
    path = f"uploads/temp_{uuid.uuid4()}{ext}"

    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        whisper_lang   = LANG_MAP.get(lang, "hi")
        initial_prompt = INITIAL_PROMPTS.get(whisper_lang)

        result = model.transcribe(
            path,
            language=whisper_lang,
            task="transcribe",
            fp16=False,
            temperature=[0, 0.2, 0.4],
            condition_on_previous_text=False,
            initial_prompt=initial_prompt,
            no_speech_threshold=0.6,
            logprob_threshold=-1.0,
            compression_ratio_threshold=2.4,
        )

        text = result["text"].strip()

        if is_hallucination(text):
            print(f"   ASR [{lang}]: Hallucination rejected: {text[:50]}")
            return {
                "text": "",
                "error": "Could not understand speech. Please speak again."
            }

        print(f"   ASR [{lang}]: {text[:80]}")
        return {"text": text}

    except Exception as e:
        print(f"   ASR error: {e}")
        return {"text": "", "error": str(e)}

    finally:
        if os.path.exists(path):
            os.remove(path)