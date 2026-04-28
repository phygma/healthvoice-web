'''from fastapi import FastAPI
from routers import diagnose

app = FastAPI(
    title="HealthVoice ML Service",
    description="Disease prediction using Machine Learning",
    version="1.0"
)

# Register diagnose route
app.include_router(
    diagnose.router,
    prefix="/diagnose",
    tags=["Diagnosis"]
)

# Root endpoint (optional but useful)
@app.get("/")
def home():
    return {"message": "ML Service is running 🚀"}'''
'''from fastapi import FastAPI
from routers import diagnose

app = FastAPI()

app.include_router(diagnose.router, prefix="/diagnose")

@app.get("/")
def home():
    return {"message": "ML Service running"}'''

'''from fastapi import FastAPI
from routers import diagnose, translate, tts, asr

app = FastAPI(
    title="HealthVoice ML Service",
    version="1.0"
)

@app.get("/")
def home():
    return {"message": "ML Service Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Register all routes
app.include_router(diagnose.router, prefix="/diagnose", tags=["Diagnosis"])
app.include_router(translate.router, prefix="/translate", tags=["Translation"])
app.include_router(tts.router, prefix="/tts", tags=["Text To Speech"])
app.include_router(asr.router, prefix="/asr", tags=["Speech To Text"])'''

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import diagnose, translate, tts, asr
import os

app = FastAPI(
    title="HealthVoice ML Service",
    version="1.0"
)

# Allow requests from Node.js backend and frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production restrict this, fine for demo
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "ML Service Running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "healthvoice-ml",
        "components": {
            "whisper": "loaded",
            "translator": "ready",
            "tts": "ready",
            "diagnosis": "ready"
        }
    }

# Ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)

# Serve audio files at /audio/filename.mp3
app.mount("/audio", StaticFiles(directory="uploads"), name="audio")

# Routers
app.include_router(asr.router,       prefix="/asr",      tags=["Speech To Text"])
app.include_router(translate.router, prefix="/translate", tags=["Translation"])
app.include_router(tts.router,       prefix="/tts",      tags=["Text To Speech"])
app.include_router(diagnose.router,  prefix="/diagnose", tags=["Diagnosis"])