# routers/diagnose.py
# POST /diagnose
# Accepts symptom text, extracts symptoms,
# runs Random Forest model, returns prediction.

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

from utils.symptom_extractor import extract_symptoms

router = APIRouter()

# Load model once at startup
MODEL_PATH   = './models/diagnosis_model.pkl'
COLUMNS_PATH = './models/diagnosis_columns.pkl'

_model        = None
_feature_cols = None

def get_model():
    global _model, _feature_cols
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(
                f"Model not found at {MODEL_PATH}. "
                "Run: python train_diagnosis_model.py"
            )
        print("Loading diagnosis model...")
        _model        = joblib.load(MODEL_PATH)
        _feature_cols = joblib.load(COLUMNS_PATH)
        print(f"✅ Diagnosis model loaded ({len(_feature_cols)} features, "
              f"{len(_model.classes_)} diseases)")
    return _model, _feature_cols

# Specialist recommendations
SPECIALIST_MAP = {
    'Dengue':             'General Physician',
    'Malaria':            'General Physician',
    'Typhoid':            'General Physician',
    'Viral Fever':        'General Physician',
    'Diabetes':           'Endocrinologist',
    'Hypertension':       'Cardiologist',
    'Bronchial Asthma':   'Pulmonologist',
    'Migraine':           'Neurologist',
    'Jaundice':           'Gastroenterologist',
    'Hepatitis A':        'Gastroenterologist',
    'Hepatitis B':        'Gastroenterologist',
    'Hepatitis C':        'Gastroenterologist',
    'Hepatitis D':        'Gastroenterologist',
    'Hepatitis E':        'Gastroenterologist',
    'Gastroenteritis':    'Gastroenterologist',
    'AIDS':               'Infectious Disease Specialist',
    'Chicken pox':        'General Physician',
    'Fungal infection':   'Dermatologist',
    'Allergy':            'Allergist',
    'Paralysis (brain hemorrhage)': 'Neurologist',
}

URGENCY_MAP = {
    'Dengue':       'high',
    'Malaria':      'high',
    'AIDS':         'high',
    'Hepatitis B':  'high',
    'Hepatitis C':  'high',
    'Paralysis (brain hemorrhage)': 'emergency',
    'Hypertension': 'moderate',
    'Diabetes':     'moderate',
    'Typhoid':      'moderate',
}

class DiagnoseRequest(BaseModel):
    text:       str
    sourceLang: str = 'hi'

@router.post('/')
async def diagnose(req: DiagnoseRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail='text is required')

    try:
        model, feature_cols = get_model()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    # Extract symptoms from text
    feature_vector, detected_symptoms = extract_symptoms(
        req.text, feature_cols
    )

    # If no symptoms detected, return informative error
    if sum(feature_vector) == 0:
        raise HTTPException(
            status_code=422,
            detail='No recognizable symptoms found in text. '
                   'Please describe symptoms more specifically.'
        )

    # Run model prediction
    X = np.array([feature_vector])
    predicted_disease = model.predict(X)[0]

    # Get probability scores for all diseases
    probabilities = model.predict_proba(X)[0]

    # Build top 3 conditions
    top_indices = np.argsort(probabilities)[::-1][:3]
    top_conditions = [
        {
            'disease':     model.classes_[i],
            'probability': round(float(probabilities[i]), 3),
        }
        for i in top_indices
        if probabilities[i] > 0.01  # only include if >1% probability
    ]

    confidence = round(float(probabilities[top_indices[0]]), 3)

    return {
        'predictedDisease':      predicted_disease,
        'confidence':            confidence,
        'topConditions':         top_conditions,
        'detectedSymptoms':      detected_symptoms,
        'recommendedSpecialist': SPECIALIST_MAP.get(predicted_disease, 'General Physician'),
        'urgency':               URGENCY_MAP.get(predicted_disease, 'low'),
        'disclaimer':            'This is an AI-assisted preliminary screening only. '
                                 'Not a substitute for professional medical advice.',
    }
