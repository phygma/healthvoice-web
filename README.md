# 🏥 HealthVoice
### AI-Powered Multilingual Medical Voice Translation & Diagnosis System

> **Breaking Language Barriers in Indian Rural Healthcare**

[![Next.js](https://img.shields.io/badge/Next.js-16.2.4-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![Node.js](https://img.shields.io/badge/Node.js-22.x-green?style=flat-square&logo=node.js)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?style=flat-square&logo=postgresql)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Supported Languages](#supported-languages)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [Backend Setup](#1-backend-setup)
  - [ML Service Setup](#2-ml-service-setup)
  - [Frontend Setup](#3-frontend-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [ML Model](#ml-model)
- [Team](#team)

---

## Overview

India has over **900 million rural patients** who speak different languages from their healthcare workers. HealthVoice is a full-stack, AI-powered web application that eliminates this communication barrier.

A healthcare worker records a patient speaking symptoms in **Hindi** — the system transcribes using OpenAI Whisper, translates to **Tamil** using Google NMT, generates Tamil audio via gTTS, and provides a preliminary disease prediction using a trained Random Forest classifier. The entire pipeline completes in **6–11 seconds** on commodity hardware.

All sessions are saved to PostgreSQL as electronic health records accessible via the Records page.

---

## Features

- 🎙️ **Real-time Voice Translation** — Hold-to-record mic capture via MediaRecorder API
- 🌐 **Neural Machine Translation** — Supports 5 major Indian language pairs
- 🔊 **Audio Output** — gTTS generates natural-sounding speech in target language
- 🩺 **AI Diagnosis** — Random Forest classifier predicts disease from symptom text
- 📋 **Health Records** — Persistent PostgreSQL storage of all translation sessions
- 🔄 **Mock Mode** — Full development mode without ML service dependency
- 🌍 **Cross-machine deployment** — ngrok tunnel for distributed team development

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (localhost:3000)                  │
│         Next.js 16 · React 19 · MediaRecorder API           │
└──────────────────────┬──────────────────────────────────────┘
                       │  HTTP REST (multipart/form-data + JSON)
┌──────────────────────▼──────────────────────────────────────┐
│                NODE.JS BACKEND (localhost:4000)              │
│        Express 4 · Prisma ORM · Multer · Axios              │
└──────────┬───────────────────────────┬───────────────────────┘
           │  PostgreSQL TCP            │  HTTPS via ngrok
┌──────────▼──────────┐   ┌────────────▼──────────────────────┐
│   POSTGRESQL 17     │   │   PYTHON ML SERVICE (port 8000)   │
│   HealthRecord      │   │   FastAPI · Whisper · NMT         │
│   User              │   │   gTTS · Random Forest            │
│   TranslationSession│   │   StaticFiles /audio/             │
└─────────────────────┘   └───────────────────────────────────┘
```

### End-to-End Flow

1. User holds mic button → speaks symptoms in source language
2. Browser MediaRecorder captures audio as `audio/webm` blob
3. Frontend POSTs `multipart/form-data` to `/api/translate`
4. Backend validates and forwards to Python `/asr` → Whisper transcribes
5. Backend calls `/translate` → Google NMT translates text
6. Backend calls `/tts` → gTTS generates MP3 audio
7. Backend saves `HealthRecord` to PostgreSQL via Prisma
8. Frontend renders transcription, translation, audio player
9. User clicks "Get AI Diagnosis" → Random Forest predicts disease
10. Diagnosis saved to `HealthRecord.diagnosis` (JSONB)

---

## Tech Stack

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| Next.js | 16.2.4 | React framework with App Router |
| React | 19.2.4 | UI component library |
| MediaRecorder API | Browser native | Microphone audio capture |
| CSS Modules | CSS3 | Scoped component styling |

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Node.js | 22.x | JavaScript runtime |
| Express | 4.18.2 | REST API framework |
| Prisma ORM | 5.6.0 | Type-safe PostgreSQL client |
| PostgreSQL | 17 | Relational database |
| Multer | 1.4.5 | Audio file upload handling |
| Axios | 1.6.0 | HTTP client for ML service calls |

### ML Service
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | ML service language |
| FastAPI | 0.104.1 | Async API framework |
| OpenAI Whisper | 20231117 | Multilingual speech recognition |
| deep-translator | 1.11.4 | Google NMT wrapper |
| gTTS | 2.4.0 | Text-to-speech synthesis |
| scikit-learn | 1.3.2 | Random Forest classifier |
| PyTorch | 2.1.0 | Whisper inference backend |

---

## Supported Languages

| Code | Language | Script | Speakers |
|---|---|---|---|
| `hi` | Hindi | Devanagari | ~600M |
| `bn` | Bengali | Bengali | ~230M |
| `ta` | Tamil | Tamil | ~80M |
| `te` | Telugu | Telugu | ~95M |
| `mr` | Marathi | Devanagari | ~95M |

---

## Project Structure

```
healthvoice-web/
├── backend/                        # Node.js Express API
│   ├── prisma/
│   │   └── schema.prisma           # Database schema
│   ├── src/
│   │   ├── controllers/
│   │   │   ├── translate.controller.js
│   │   │   ├── records.controller.js
│   │   │   └── diagnose.controller.js
│   │   ├── middleware/
│   │   │   └── upload.middleware.js
│   │   ├── routes/
│   │   │   ├── health.route.js
│   │   │   ├── translate.route.js
│   │   │   ├── records.route.js
│   │   │   └── diagnose.route.js
│   │   ├── services/
│   │   │   ├── ml.service.js       # ML service client (mock + real)
│   │   │   └── diagnosis.service.js
│   │   └── index.js
│   ├── uploads/                    # Runtime audio files
│   ├── .env.example
│   └── package.json
│
├── frontend/                       # Next.js application
│   ├── app/
│   │   ├── layout.js
│   │   ├── globals.css
│   │   ├── page.js                 # Landing page
│   │   ├── translate/
│   │   │   └── page.js             # Main translate interface
│   │   └── records/
│   │       └── page.js             # Health records history
│   ├── components/
│   │   ├── Navbar.js
│   │   ├── MicButton.js
│   │   ├── LanguageSelector.js
│   │   └── DiagnosisCard.js
│   ├── hooks/
│   │   └── useAudioRecorder.js
│   ├── utils/
│   │   └── languages.js
│   └── .env.local.example
│
└── ml-service/                     # Python FastAPI ML service
    ├── routers/
    │   ├── asr.py                  # Whisper speech recognition
    │   ├── translate.py            # Google NMT translation
    │   ├── tts.py                  # gTTS audio synthesis
    │   └── diagnose.py             # Random Forest diagnosis
    ├── utils/
    │   └── symptom_extractor.py    # Text → feature vector
    ├── models/                     # Trained .pkl files (generated)
    ├── data/                       # Kaggle dataset CSVs
    ├── main.py
    ├── train_diagnosis_model.py
    └── requirements.txt
```

---

## Prerequisites

| Tool | Version | Notes |
|---|---|---|
| Node.js | v18+ | v22.13.1 used |
| npm | v9+ | Bundled with Node.js |
| Python | 3.10+ | For ML service |
| PostgreSQL | 15+ | v17 used |
| ffmpeg | Any | Required by Whisper — must be on PATH |
| Git | Any | Version control |

### Windows-Specific Notes

> ⚠️ All development was done on **Windows 11 native** (no WSL).

- Add PostgreSQL `bin` folder to System PATH after install
- Add ffmpeg `bin` folder to System PATH
- Do **not** use quotes around values in `.env` files
- Use `node node_modules/next/dist/bin/next dev` if `npm run dev` fails

---

## Installation & Setup

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/phygma/healthvoice-web.git
cd healthvoice-web/backend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env with your values (see Environment Variables section)

# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE healthvoice;"

# Push schema to database
npx prisma db push

# Start development server
npm run dev
```

Server starts at `http://localhost:4000`

Verify: `curl http://localhost:4000/api/health`

---

### 2. ML Service Setup

```bash
cd ml-service

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies (takes 15-25 min for PyTorch)
pip install -r requirements.txt

# Download Kaggle dataset
# Go to: https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
# Download and place Training.csv + Testing.csv in data/

# Train the diagnosis model (runs once, takes ~60 seconds)
python train_diagnosis_model.py

# Start ML service
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Service starts at `http://localhost:8000`

Verify: `http://localhost:8000/docs` (Swagger UI)

#### Cross-Machine Setup (ngrok)

If ML service runs on a different machine:

```bash
# Install ngrok and authenticate
ngrok config add-authtoken YOUR_TOKEN

# Start tunnel
ngrok http 8000

# Copy the forwarding URL (e.g. https://xyz.ngrok-free.app)
# Set ML_SERVICE_URL in backend .env to this URL
```

---

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local
# Set NEXT_PUBLIC_BACKEND_URL=http://localhost:4000

# Start development server
npm run dev
# OR if npm run dev fails on Windows:
node node_modules/next/dist/bin/next dev
```

Application opens at `http://localhost:3000`

---

## Environment Variables

### Backend (`backend/.env`)

```env
PORT=4000
DATABASE_URL=postgresql://postgres:password@localhost:5432/healthvoice
ML_SERVICE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
UPLOAD_DIR=./uploads
MAX_AUDIO_SIZE_MB=10
USE_MOCK_ML=true
DIAGNOSIS_MOCK=true
```

> ⚠️ **Windows**: Do NOT use quotes around values in `.env`

> 💡 Set `USE_MOCK_ML=false` and `DIAGNOSIS_MOCK=false` when ML service is running

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:4000
```

---

## API Reference

### Base URL: `http://localhost:4000`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Backend + ML service status |
| POST | `/api/translate` | Full ASR→NMT→TTS pipeline |
| GET | `/api/records` | All health records |
| GET | `/api/records/:id` | Single record by ID |
| DELETE | `/api/records/:id` | Delete record + audio files |
| POST | `/api/diagnose` | AI disease prediction |
| GET | `/audio/:filename` | Serve TTS audio files |

### POST `/api/translate`

```
Content-Type: multipart/form-data

Fields:
  audio       (file)    Audio recording — required
  sourceLang  (string)  hi | bn | ta | te | mr — required
  targetLang  (string)  hi | bn | ta | te | mr — required
  patientName (string)  Optional patient identifier
```

**Response:**
```json
{
  "success": true,
  "recordId": "clx7abc123",
  "originalText": "मुझे बुखार है",
  "translatedText": "எனக்கு காய்ச்சல் இருக்கிறது",
  "audioUrl": "https://xyz.ngrok-free.app/audio/tts_abc.mp3",
  "latencyMs": 7200
}
```

### POST `/api/diagnose`

```json
{
  "symptomText": "I have fever, headache and joint pain",
  "sourceLang": "en",
  "recordId": "clx7abc123"
}
```

**Response:**
```json
{
  "success": true,
  "diagnosis": {
    "predictedDisease": "Dengue",
    "confidence": 0.72,
    "topConditions": [
      { "disease": "Dengue", "probability": 0.72 },
      { "disease": "Malaria", "probability": 0.15 }
    ],
    "detectedSymptoms": ["high fever", "headache", "joint pain"],
    "recommendedSpecialist": "General Physician",
    "urgency": "high",
    "disclaimer": "AI-assisted preliminary screening only."
  }
}
```

---

## ML Model

### Disease Prediction — Random Forest

| Property | Value |
|---|---|
| Dataset | Kaggle — Disease Prediction (kaushil268) |
| Training samples | 4,920 |
| Test samples | 42 |
| Feature columns | 132 binary symptom features |
| Disease classes | 41 |
| Algorithm | Random Forest (n_estimators=100) |
| Test accuracy | **97.62%** |

### Symptom Extraction

Free-form patient text is converted to a 132-dimensional binary feature vector using:
1. **Direct matching** — column names matched against input text
2. **Keyword map** — 100+ synonyms and Hindi transliterations mapped to dataset columns

### Disease Suppression

Clinically impossible predictions are filtered out. For example, AIDS is suppressed unless `extra_marital_contacts`, `receiving_blood_transfusion`, or `receiving_unsterile_injections` are detected.

### Speech Recognition — Whisper

| Model | Parameters | RAM | Used For |
|---|---|---|---|
| tiny | 39M | ~400MB | Low-RAM machines |
| **small** | 244M | ~2GB | **Recommended** |
| medium | 769M | ~5GB | High-accuracy production |

The `small` model is recommended for best accuracy on 8GB RAM machines.

---

## Running Tests

### Backend API Tests (Postman)

Import and run the collection covering all 7 endpoints:

```
GET  /api/health
POST /api/translate  (with audio file)
GET  /api/records
GET  /api/records/:id
DELETE /api/records/:id
POST /api/diagnose
GET  /audio/:filename
```

### ML Service Tests (FastAPI Docs)

Open `http://localhost:8000/docs` and test each endpoint via the Swagger UI.

**Recommended test sentences:**

| Symptom Input | Expected Disease |
|---|---|
| I have itching, skin rash and nodal skin eruptions | Fungal infection |
| I have high fever, chills and sweating | Malaria |
| I have high fever, headache, joint pain and pain behind the eyes | Dengue |
| I have breathlessness, cough and chest pain | Bronchial Asthma |
| I have excessive hunger, polyuria and weight loss | Diabetes |

---

## Port Reference

| Service | Port | Command |
|---|---|---|
| Next.js Frontend | 3000 | `npm run dev` |
| Node.js Backend | 4000 | `npm run dev` |
| Python ML Service | 8000 | `uvicorn main:app --reload` |
| PostgreSQL | 5432 | Auto-started as service |
| Prisma Studio | 5555 | `npx prisma studio` |
| ngrok Dashboard | 4040 | `http://127.0.0.1:4040` |

---

## Known Limitations

- **Whisper accuracy** — Small model may mishear Hindi speech; upgrade to medium for production
- **Translation quality** — Google NMT is good but IndicTrans2 would be superior for Indic pairs
- **Audio storage** — No persistent cloud storage; audio files lost on server restart
- **Authentication** — No user auth implemented; `userId` nullable in schema, planned for v2
- **Render cold start** — Free tier ML deployment sleeps after 15 min inactivity

---

## Team

| Name | Roll Number | Role |
|---|---|---|
| Aman Arora | 2200271530015 | Backend + Frontend |
| Krish Kumar | 2200271530063 | ML Service |
| Krrish Kumar | 2200271530064 | ML Service |
| Harsh Dubey | 2200271530054 | Backend + Frontend |

**Mentor:** Asst. Prof. Mrs. Juli Yadav
**Department:** Computer Science & Engineering (AIML)
**Academic Year:** 2025–2026

---

## License

This project is licensed under the MIT License.

---

<div align="center">
  <strong>HealthVoice</strong> — Code · Create · Conquer
  <br>
  Built for India's 900 million rural patients
</div>
