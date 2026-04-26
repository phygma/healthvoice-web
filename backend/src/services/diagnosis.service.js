// diagnosis.service.js
// Calls the Python ML service /diagnose endpoint.
// Falls back to mock data when DIAGNOSIS_MOCK=true.

const axios = require('axios');

const ML_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';
const USE_MOCK = process.env.DIAGNOSIS_MOCK === 'true';

// Specialist mapping based on predicted disease
// Used in both mock and real modes
const SPECIALIST_MAP = {
  'Dengue':                  'General Physician',
  'Malaria':                 'General Physician',
  'Typhoid':                 'General Physician',
  'Viral Fever':             'General Physician',
  'Diabetes':                'Endocrinologist',
  'Hypertension':            'Cardiologist',
  'Bronchial Asthma':        'Pulmonologist',
  'Migraine':                'Neurologist',
  'Cervical spondylosis':    'Orthopedist',
  'Jaundice':                'Gastroenterologist',
  'Hepatitis A':             'Gastroenterologist',
  'Hepatitis B':             'Gastroenterologist',
  'Hepatitis C':             'Gastroenterologist',
  'Hepatitis D':             'Gastroenterologist',
  'Hepatitis E':             'Gastroenterologist',
  'Gastroenteritis':         'Gastroenterologist',
  'Peptic ulcer disease':    'Gastroenterologist',
  'GERD':                    'Gastroenterologist',
  'AIDS':                    'Infectious Disease Specialist',
  'Chicken pox':             'General Physician',
  'Fungal infection':        'Dermatologist',
  'Allergy':                 'Allergist',
  'Drug Reaction':           'General Physician',
  'Paralysis (brain hemorrhage)': 'Neurologist',
  'default':                 'General Physician',
};

const URGENCY_MAP = {
  'Dengue':       'high',
  'Malaria':      'high',
  'Typhoid':      'moderate',
  'AIDS':         'high',
  'Hepatitis B':  'high',
  'Hepatitis C':  'high',
  'Paralysis (brain hemorrhage)': 'emergency',
  'Hypertension': 'moderate',
  'Diabetes':     'moderate',
  'default':      'low',
};

// ── MOCK DATA ─────────────────────────────────────────────────────────────
const MOCK_RESPONSE = {
  predictedDisease: 'Viral Fever',
  confidence: 0.82,
  topConditions: [
    { disease: 'Viral Fever', probability: 0.82 },
    { disease: 'Dengue',      probability: 0.11 },
    { disease: 'Malaria',     probability: 0.07 },
  ],
  detectedSymptoms: ['fever', 'headache', 'fatigue'],
  recommendedSpecialist: 'General Physician',
  urgency: 'moderate',
  disclaimer: 'This is an AI-assisted preliminary screening only. Not a substitute for professional medical advice.',
};

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// ── MAIN FUNCTION ─────────────────────────────────────────────────────────
exports.getDiagnosis = async (symptomText, sourceLang) => {
  const start = Date.now();

  if (USE_MOCK) {
    await sleep(600); // simulate model inference time
    console.log('   🩺 [MOCK] Diagnosis returned');
    return {
      diagnosis: MOCK_RESPONSE,
      latencyMs: Date.now() - start,
    };
  }

  // Call real Python ML service
  const response = await axios.post(
    `${ML_URL}/diagnose`,
    { text: symptomText, sourceLang },
    { timeout: 15000 }
  );

  const data = response.data;

  // Enrich with specialist + urgency if Python side didn't include them
  if (!data.recommendedSpecialist) {
    data.recommendedSpecialist =
      SPECIALIST_MAP[data.predictedDisease] || SPECIALIST_MAP['default'];
  }
  if (!data.urgency) {
    data.urgency =
      URGENCY_MAP[data.predictedDisease] || URGENCY_MAP['default'];
  }
  if (!data.disclaimer) {
    data.disclaimer =
      'This is an AI-assisted preliminary screening only. Not a substitute for professional medical advice.';
  }

  console.log(`   🩺 Diagnosis: ${data.predictedDisease} (${(data.confidence * 100).toFixed(0)}% confidence) in ${Date.now() - start}ms`);

  return {
    diagnosis: data,
    latencyMs: Date.now() - start,
  };
};