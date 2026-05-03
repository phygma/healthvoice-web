'''# routers/diagnose.py
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
    }'''
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os
from deep_translator import GoogleTranslator
from utils.symptom_extractor import extract_symptoms

router = APIRouter()

MODEL_PATH   = "./models/diagnosis_model.pkl"
COLUMNS_PATH = "./models/diagnosis_columns.pkl"

_model        = None
_feature_cols = None


def get_model():
    global _model, _feature_cols
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(
                "Model not found. Run: python train_diagnosis_model.py"
            )
        _model        = joblib.load(MODEL_PATH)
        _feature_cols = joblib.load(COLUMNS_PATH)
        print(f"✅ Diagnosis model loaded — "
              f"{len(_feature_cols)} features, "
              f"{len(_model.classes_)} diseases")
    return _model, _feature_cols


# Pre-load model at startup
try:
    get_model()
except Exception as e:
    print(f"⚠️  Could not pre-load model: {e}")


# ── Specialist recommendations ────────────────────────────────────────────
SPECIALIST_MAP = {
    "Dengue":                       "General Physician",
    "Malaria":                      "General Physician",
    "Typhoid":                      "General Physician",
    "Viral Fever":                  "General Physician",
    "Common Cold":                  "General Physician",
    "Chicken pox":                  "General Physician",
    "Drug Reaction":                "General Physician",
    "Allergy":                      "Allergist",
    "Diabetes":                     "Endocrinologist",
    "Hypothyroidism":               "Endocrinologist",
    "Hyperthyroidism":              "Endocrinologist",
    "Hypoglycemia":                 "Endocrinologist",
    "Hypertension":                 "Cardiologist",
    "Bronchial Asthma":             "Pulmonologist",
    "Tuberculosis":                 "Pulmonologist",
    "Pneumonia":                    "Pulmonologist",
    "Migraine":                     "Neurologist",
    "Cervical spondylosis":         "Neurologist",
    "Paralysis (brain hemorrhage)": "Neurologist",
    "Jaundice":                     "Gastroenterologist",
    "Hepatitis A":                  "Gastroenterologist",
    "Hepatitis B":                  "Gastroenterologist",
    "Hepatitis C":                  "Gastroenterologist",
    "Hepatitis D":                  "Gastroenterologist",
    "Hepatitis E":                  "Gastroenterologist",
    "Gastroenteritis":              "Gastroenterologist",
    "Peptic ulcer disease":         "Gastroenterologist",
    "GERD":                         "Gastroenterologist",
    "Chronic cholestasis":          "Gastroenterologist",
    "AIDS":                         "Infectious Disease Specialist",
    "Fungal infection":             "Dermatologist",
    "Psoriasis":                    "Dermatologist",
    "Impetigo":                     "Dermatologist",
    "Acne":                         "Dermatologist",
    "Urinary tract infection":      "Urologist",
    "Dimorphic hemmorhoids(piles)": "Proctologist",
    "Arthritis":                    "Rheumatologist",
    "Osteoarthristis":              "Orthopedist",
}

# ── Urgency levels ────────────────────────────────────────────────────────
URGENCY_MAP = {
    "Dengue":                       "high",
    "Malaria":                      "high",
    "AIDS":                         "high",
    "Hepatitis B":                  "high",
    "Hepatitis C":                  "high",
    "Paralysis (brain hemorrhage)": "emergency",
    "Tuberculosis":                 "high",
    "Pneumonia":                    "high",
    "Typhoid":                      "moderate",
    "Hypertension":                 "moderate",
    "Diabetes":                     "moderate",
    "Hypoglycemia":                 "moderate",
    "Bronchial Asthma":             "moderate",
    "Urinary tract infection":      "moderate",
    "Hepatitis A":                  "moderate",
    "Hepatitis D":                  "moderate",
    "Hepatitis E":                  "moderate",
    "Gastroenteritis":              "moderate",
    "Jaundice":                     "moderate",
    "Chicken pox":                  "moderate",
}

# ── Disease suppression rules ─────────────────────────────────────────────
# Each disease maps to a set of symptoms where AT LEAST ONE
# must be present for the disease to be a valid prediction.
# If NONE of the required symptoms are detected the disease
# is suppressed from both the prediction and the display list.
DISEASE_REQUIRED_SYMPTOMS = {

    # AIDS requires transmission-specific symptoms
    "AIDS": {
        "extra marital contacts",
        "receiving blood transfusion",
        "receiving unsterile injections",
    },

    # Skin diseases require at least one skin symptom
    "Impetigo": {
        "skin rash",
        "pus filled pimples",
        "blackheads",
        "scurring",
        "blister",
        "red sore around nose",
    },
    "Psoriasis": {
        "skin rash",
        "skin peeling",
        "silver like dusting",
        "small dents in nails",
        "inflammatory nails",
    },
    "Acne": {
        "skin rash",
        "pus filled pimples",
        "blackheads",
        "scurring",
    },
    "Fungal infection": {
        "itching",
        "skin rash",
        "nodal skin eruptions",
        "dischromic patches",
    },
    "Drug Reaction": {
        "skin rash",
        "itching",
        "burning micturition",
    },

    # Ano-rectal diseases require GI-specific symptoms
    "Dimorphic hemmorhoids(piles)": {
        "constipation",
        "pain in anal region",
        "bloody stool",
        "irritation in anus",
        "pain during bowel movements",
    },

    # Neurological diseases require neuro-specific symptoms
    "Cervical spondylosis": {
        "neck pain",
        "loss of balance",
        "weakness in limbs",
        "stiff neck",
    },
    "Paralysis (brain hemorrhage)": {
        "weakness of one body side",
        "slurred speech",
        "altered sensorium",
        "loss of balance",
    },

    # Urological diseases require urinary symptoms
    "Urinary tract infection": {
        "burning micturition",
        "spotting urination",
        "foul smell of urine",
        "bladder discomfort",
        "continuous feel of urine",
    },

    # Liver diseases require liver-specific symptoms
    "Chronic cholestasis": {
        "yellowish skin",
        "dark urine",
        "yellowing of eyes",
        "itching",
    },
    "Jaundice": {
        "yellowish skin",
        "dark urine",
        "yellowing of eyes",
        "yellow urine",
    },

    # GI diseases require GI-specific symptoms
    "Peptic ulcer disease": {
        "vomiting",
        "indigestion",
        "loss of appetite",
        "abdominal pain",
    },
    "GERD": {
        "acidity",
        "indigestion",
        "stomach pain",
        "vomiting",
    },

    # Orthopaedic diseases require joint-specific symptoms
    "Osteoarthristis": {
        "joint pain",
        "knee pain",
        "hip joint pain",
        "swelling joints",
    },
    "Arthritis": {
        "joint pain",
        "swelling joints",
        "movement stiffness",
        "painful walking",
    },
    "Heart attack": {
    "chest pain",
    "fast heart rate",
    "palpitations",
    "vomiting",
    },
}


def is_suppressed(disease: str, detected_set: set) -> bool:
    """
    Returns True if the disease should be suppressed.
    A disease is suppressed if it has required symptoms defined
    AND none of those required symptoms were detected.
    """
    required = DISEASE_REQUIRED_SYMPTOMS.get(disease, set())
    if not required:
        return False  # no restriction — allow prediction
    return not detected_set.intersection(required)


class DiagnoseRequest(BaseModel):
    text:       str
    sourceLang: str = "en"


@router.post("/")
async def diagnose(req: DiagnoseRequest):

    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text is required")

    try:
        model, feature_cols = get_model()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    # ── Translate to English if needed ────────────────────────────
    text = req.text
    if req.sourceLang != "en":
        try:
            text = GoogleTranslator(
                source="auto", target="en"
            ).translate(text)
            print(f"   Translated for diagnosis: {text[:80]}")
        except Exception as e:
            print(f"   Translation failed: {e} — using original text")

    # ── Extract symptoms ──────────────────────────────────────────
    feature_vector, detected_symptoms = extract_symptoms(
        text.lower(), feature_cols
    )

    if sum(feature_vector) == 0:
        raise HTTPException(
            status_code=422,
            detail=(
                "No recognizable symptoms found in text. "
                "Please describe symptoms more specifically. "
                "Example: 'I have fever, headache and joint pain'"
            )
        )

    # ── Run Random Forest ─────────────────────────────────────────
    X             = np.array([feature_vector])
    probabilities = model.predict_proba(X)[0]

    # Sort all candidates by probability descending
    all_indices   = np.argsort(probabilities)[::-1]
    detected_set  = set(detected_symptoms)

    # ── Find best non-suppressed prediction ───────────────────────
    final_disease    = None
    final_confidence = 0.0

    for idx in all_indices:
        candidate = model.classes_[idx]
        cand_prob = probabilities[idx]

        if cand_prob < 0.01:
            break

        if is_suppressed(candidate, detected_set):
            print(f"   ⚠️  Suppressed: {candidate} "
                  f"({cand_prob*100:.0f}%) — required symptoms absent")
            continue

        final_disease    = candidate
        final_confidence = round(float(cand_prob), 3)
        break

    # Ultimate fallback — should never reach here
    if final_disease is None:
        final_disease    = model.classes_[all_indices[0]]
        final_confidence = round(float(probabilities[all_indices[0]]), 3)

    # ── Build top 3 display list (suppressed diseases excluded) ───
    top_conditions = []
    for idx in all_indices:
        if len(top_conditions) >= 3:
            break
        candidate = model.classes_[idx]
        cand_prob = probabilities[idx]

        if cand_prob < 0.01:
            break

        if is_suppressed(candidate, detected_set):
            continue  # don't show suppressed diseases in list either

        top_conditions.append({
            "disease":     candidate,
            "probability": round(float(cand_prob), 3),
        })

    # Fallback — show raw top 3 if everything was suppressed
    if not top_conditions:
        top_conditions = [
            {
                "disease":     model.classes_[i],
                "probability": round(float(probabilities[i]), 3),
            }
            for i in all_indices[:3]
            if probabilities[i] > 0.01
        ]

    print(f"   🩺 Prediction: {final_disease} "
          f"({final_confidence * 100:.0f}%)")
    print(f"   Detected: {detected_symptoms}")

    return {
        "predictedDisease":      final_disease,
        "confidence":            final_confidence,
        "topConditions":         top_conditions,
        "detectedSymptoms":      detected_symptoms,
        "recommendedSpecialist": SPECIALIST_MAP.get(
                                     final_disease, "General Physician"),
        "urgency":               URGENCY_MAP.get(final_disease, "low"),
        "disclaimer": (
            "This is an AI-assisted preliminary screening only. "
            "Not a substitute for professional medical advice."
        ),
    }
