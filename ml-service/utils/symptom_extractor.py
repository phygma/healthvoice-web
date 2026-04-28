# symptom_extractor.py
# Converts free-form symptom text → binary feature vector
# for the Random Forest model

import re

# Full list of symptoms (must match dataset columns)
ALL_SYMPTOMS = [
    'itching','skin_rash','nodal_skin_eruptions','continuous_sneezing',
    'shivering','chills','joint_pain','stomach_pain','acidity',
    'ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition',
    'spotting_urination','fatigue','weight_gain','anxiety',
    'cold_hands_and_feets','mood_swings','weight_loss','restlessness',
    'lethargy','patches_in_throat','irregular_sugar_level','cough',
    'high_fever','sunken_eyes','breathlessness','sweating','dehydration',
    'indigestion','headache','yellowish_skin','dark_urine','nausea',
    'loss_of_appetite','pain_behind_the_eyes','back_pain','constipation',
    'abdominal_pain','diarrhoea','mild_fever','yellow_urine',
    'yellowing_of_eyes','acute_liver_failure','fluid_overload',
    'swelling_of_stomach','swelled_lymph_nodes','malaise',
    'blurred_and_distorted_vision','phlegm','throat_irritation',
    'redness_of_eyes','sinus_pressure','runny_nose','congestion',
    'chest_pain','weakness_in_limbs','fast_heart_rate',
    'pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
    'irritation_in_anus','neck_pain','dizziness','cramps','bruising',
    'obesity','swollen_legs','swollen_blood_vessels','puffy_face_and_eyes',
    'enlarged_thyroid','brittle_nails','swollen_extremeties',
    'excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
    'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness',
    'stiff_neck','swelling_joints','movement_stiffness','spinning_movements',
    'loss_of_balance','unsteadiness','weakness_of_one_body_side',
    'loss_of_smell','bladder_discomfort','foul_smell_of_urine',
    'continuous_feel_of_urine','passage_of_gases','internal_itching',
    'toxic_look_(typhos)','depression','irritability','muscle_pain',
    'altered_sensorium','red_spots_over_body','belly_pain',
    'abnormal_menstruation','dischromic_patches','watering_from_eyes',
    'increased_appetite','polyuria','family_history','mucoid_sputum',
    'rusty_sputum','lack_of_concentration','visual_disturbances',
    'receiving_blood_transfusion','receiving_unsterile_injections','coma',
    'stomach_bleeding','distention_of_abdomen','history_of_alcohol_consumption',
    'fluid_overload.1','blood_in_sputum','prominent_veins_on_calf',
    'palpitations','painful_walking','pus_filled_pimples','blackheads',
    'scurring','skin_peeling','silver_like_dusting','small_dents_in_nails',
    'inflammatory_nails','blister','red_sore_around_nose',
    'yellow_crust_ooze'
]

# Keyword mapping (real-world text → dataset symptoms)
KEYWORD_MAP = {
    # Fever
    "fever": "high_fever",
    "bukhar": "high_fever",
    "temperature": "high_fever",

    # Head
    "headache": "headache",
    "sir dard": "headache",

    # Cough
    "cough": "cough",
    "khansi": "cough",

    # Vomiting
    "vomit": "vomiting",
    "ulti": "vomiting",
    "nausea": "nausea",

    # Pain
    "joint pain": "joint_pain",
    "body pain": "muscle_pain",
    "back pain": "back_pain",
    "chest pain": "chest_pain",
    "stomach pain": "stomach_pain",

    # Fatigue
    "fatigue": "fatigue",
    "weakness": "fatigue",
    "kamzori": "fatigue",

    # Skin
    "rash": "skin_rash",
    "itching": "itching",

    # Breathing
    "breath": "breathlessness",

    # Digestive
    "diarrhea": "diarrhoea",
    "loose motion": "diarrhoea",
    "constipation": "constipation",

    # Other
    "chills": "chills",
    "sweating": "sweating",
    "dizziness": "dizziness",
}

def extract_symptoms(text: str, feature_cols: list):
    """
    Convert text → feature vector
    
    Returns:
        feature_vector (list)
        detected_symptoms (list)
    """

    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)

    detected = set()

    # 1. Direct matching
    for symptom in ALL_SYMPTOMS:
        readable = symptom.replace("_", " ")
        if readable in text:
            detected.add(symptom)

    # 2. Keyword matching
    for keyword, symptom in KEYWORD_MAP.items():
        if keyword in text and symptom in feature_cols:
            detected.add(symptom)

    # Build vector
    feature_vector = [
        1 if col in detected else 0
        for col in feature_cols
    ]

    detected_list = [s.replace("_", " ") for s in detected]

    return feature_vector, detected_list