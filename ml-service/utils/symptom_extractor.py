'''# symptom_extractor.py
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

    return feature_vector, detected_list'''
# symptom_extractor.py
# Converts free-form symptom text → 132-dimensional binary feature vector
# for the Random Forest disease prediction model
#
# Two-pass strategy:
#   Pass 1: Direct column name matching (English medical terms)
#   Pass 2: Keyword map (synonyms + Hindi Romanized transliterations)

import re

# All 132 symptom column names from the Kaggle dataset
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

# Comprehensive keyword map covering:
#   - English synonyms and alternate phrasings
#   - Hindi Romanized transliterations (what Whisper base outputs for Hindi)
#   - Common misspellings Whisper produces
KEYWORD_MAP = {

    # ── Fever ─────────────────────────────────────────────────────────────
    "fever":            "high_fever",
    "high fever":       "high_fever",
    "mild fever":       "mild_fever",
    "temperature":      "high_fever",
    "bukhar":           "high_fever",
    "bukhaar":          "high_fever",
    "bhukhar":          "high_fever",   # common Whisper output
    "bhukhaar":         "high_fever",
    "tap":              "high_fever",
    "tez bukhaar":      "high_fever",
    "tez bukhar":       "high_fever",
    "hafta se bukhar":  "high_fever",
    "kal se bukhar":    "high_fever",
    "mujhe bukhar":     "high_fever",
    "muje bukhar":      "high_fever",   # Whisper drops nasalization
    "mujhe bukhaar":    "high_fever",

    # ── Headache ──────────────────────────────────────────────────────────
    "headache":         "headache",
    "head ache":        "headache",
    "head pain":        "headache",
    "sir dard":         "headache",
    "sar dard":         "headache",
    "sirdard":          "headache",
    "sir me dard":      "headache",
    "sar me dard":      "headache",
    "sir mein dard":    "headache",
    "dimag dard":       "headache",

    # ── Cough ─────────────────────────────────────────────────────────────
    "cough":            "cough",
    "khansi":           "cough",
    "khaansi":          "cough",
    "khasi":            "cough",
    "dry cough":        "cough",
    "wet cough":        "cough",

    # ── Vomiting / Nausea ─────────────────────────────────────────────────
    "vomit":            "vomiting",
    "vomiting":         "vomiting",
    "ulti":             "vomiting",
    "ultee":            "vomiting",
    "qaay":             "vomiting",
    "nausea":           "nausea",
    "nauseous":         "nausea",
    "feel like vomit":  "nausea",
    "matli":            "nausea",
    "ji michlana":      "nausea",
    "ji machlaana":     "nausea",

    # ── Fatigue / Weakness ────────────────────────────────────────────────
    "fatigue":          "fatigue",
    "tired":            "fatigue",
    "tiredness":        "fatigue",
    "weakness":         "fatigue",
    "weak":             "fatigue",
    "kamzori":          "fatigue",
    "kamzoli":          "fatigue",   # Whisper mishearing of kamzori
    "kamzoree":         "fatigue",
    "thakan":           "fatigue",
    "thakaan":          "fatigue",
    "thaka hua":        "fatigue",
    "lethargy":         "lethargy",
    "lethargic":        "lethargy",
    "no energy":        "fatigue",

    # ── Joint / Body Pain ─────────────────────────────────────────────────
    "joint pain":       "joint_pain",
    "joints pain":      "joint_pain",
    "jodon mein dard":  "joint_pain",
    "jodo mein dard":   "joint_pain",
    "gathiya":          "joint_pain",
    "body pain":        "muscle_pain",
    "muscle pain":      "muscle_pain",
    "body ache":        "muscle_pain",
    "back pain":        "back_pain",
    "peeth dard":       "back_pain",
    "peeth mein dard":  "back_pain",
    "kamar dard":       "back_pain",
    "chest pain":       "chest_pain",
    "seene mein dard":  "chest_pain",
    "seene dard":       "chest_pain",
    "stomach pain":     "stomach_pain",
    "pet dard":         "stomach_pain",
    "pet me dard":      "stomach_pain",
    "pet mein dard":    "abdominal_pain",
    "abdominal pain":   "abdominal_pain",
    "belly pain":       "belly_pain",
    "knee pain":        "knee_pain",
    "ghutne mein dard": "knee_pain",
    "neck pain":        "neck_pain",
    "gardan dard":      "neck_pain",

    # ── Skin ──────────────────────────────────────────────────────────────
    "rash":             "skin_rash",
    "skin rash":        "skin_rash",
    "itching":          "itching",
    "itchy":            "itching",
    "khujli":           "itching",
    "khujalee":         "itching",
    "nodal skin":       "nodal_skin_eruptions",

    # ── Breathing ─────────────────────────────────────────────────────────
    "breathless":       "breathlessness",
    "breathlessness":   "breathlessness",
    "short of breath":  "breathlessness",
    "difficulty breathing": "breathlessness",
    "breathing problem": "breathlessness",
    "sans":             "breathlessness",
    "sans lena":        "breathlessness",
    "sans fulna":       "breathlessness",
    "dama":             "breathlessness",

    # ── Digestive ─────────────────────────────────────────────────────────
    "diarrhea":         "diarrhoea",
    "diarrhoea":        "diarrhoea",
    "loose motion":     "diarrhoea",
    "loose motions":    "diarrhoea",
    "dast":             "diarrhoea",
    "loose stool":      "diarrhoea",
    "constipation":     "constipation",
    "kabz":             "constipation",
    "indigestion":      "indigestion",
    "acidity":          "acidity",
    "gas":              "acidity",
    "loss of appetite": "loss_of_appetite",
    "no appetite":      "loss_of_appetite",
    "bhookh nahi":      "loss_of_appetite",
    "bhukh nahi":       "loss_of_appetite",
    "khana nahi":       "loss_of_appetite",
    "excessive hunger": "excessive_hunger",
    "bahut bhookh":     "excessive_hunger",

    # ── Eyes ──────────────────────────────────────────────────────────────
    "yellow eyes":      "yellowing_of_eyes",
    "yellowish eyes":   "yellowing_of_eyes",
    "red eyes":         "redness_of_eyes",
    "aankhon mein dard":"redness_of_eyes",
    "aankhon mein lali":"redness_of_eyes",
    "pain behind eyes": "pain_behind_the_eyes",
    "eye pain":         "pain_behind_the_eyes",
    "blurred vision":   "blurred_and_distorted_vision",
    "watering eyes":    "watering_from_eyes",
    "aankhon se paani": "watering_from_eyes",

    # ── Fever related ─────────────────────────────────────────────────────
    "chills":           "chills",
    "thand":            "chills",
    "kaanpna":          "shivering",
    "kaampna":          "shivering",
    "shivering":        "shivering",
    "sweating":         "sweating",
    "sweats":           "sweating",
    "pasina":           "sweating",
    "night sweats":     "sweating",
    "dehydration":      "dehydration",

    # ── Skin / Yellow ─────────────────────────────────────────────────────
    "yellow skin":      "yellowish_skin",
    "yellowish skin":   "yellowish_skin",
    "jaundice":         "yellowish_skin",
    "peela":            "yellowish_skin",

    # ── Urine ─────────────────────────────────────────────────────────────
    "dark urine":       "dark_urine",
    "yellow urine":     "yellow_urine",
    "burning urination":"burning_micturition",
    "peshab mein jalan":"burning_micturition",
    "peshab":           "burning_micturition",
    "frequent urination":"continuous_feel_of_urine",
    "polyuria":         "polyuria",
    "bar bar peshab":   "continuous_feel_of_urine",

    # ── Heart / Blood ─────────────────────────────────────────────────────
    "palpitations":     "palpitations",
    "dil tez":          "fast_heart_rate",
    "dil ki dhadkan":   "palpitations",
    "fast heartbeat":   "fast_heart_rate",
    "heart racing":     "fast_heart_rate",

    # ── Mental / Mood ─────────────────────────────────────────────────────
    "anxiety":          "anxiety",
    "ghabrahat":        "anxiety",
    "depression":       "depression",
    "udaasi":           "depression",
    "mood swings":      "mood_swings",
    "irritability":     "irritability",
    "restlessness":     "restlessness",
    "bechaini":         "restlessness",

    # ── Weight ────────────────────────────────────────────────────────────
    "weight loss":      "weight_loss",
    "wajan kam":        "weight_loss",
    "weight gain":      "weight_gain",
    "wajan badhna":     "weight_gain",

    # ── Other common ──────────────────────────────────────────────────────
    "dizziness":        "dizziness",
    "dizzy":            "dizziness",
    "chakkar":          "dizziness",
    "chakkar aana":     "dizziness",
    "swelling":         "swelling_joints",
    "runny nose":       "runny_nose",
    "naak se paani":    "runny_nose",
    "sore throat":      "patches_in_throat",
    "throat pain":      "patches_in_throat",
    "gale mein dard":   "patches_in_throat",
    "gala dard":        "patches_in_throat",
    "phlegm":           "phlegm",
    "balgam":           "phlegm",
    "coughing blood":   "blood_in_sputum",
    "blood in sputum":  "blood_in_sputum",
    "stiff neck":       "stiff_neck",
    "gardan akad":      "stiff_neck",
    "muscle weakness":  "muscle_weakness",
    "loss of smell":    "loss_of_smell",
    "smell gone":       "loss_of_smell",
    "sunken eyes":      "sunken_eyes",
    "aankhein dhasi":   "sunken_eyes",

    # ── Whisper base common mishearings / alternate spellings ─────────────
    "siddharth":        "fatigue",    # Whisper mishears kamzoli as siddharth
    "al aheer":         "high_fever", # Whisper mishear
    "alaheer":          "high_fever",
    "dal or":           "fatigue",# Whisper mishear

    # Whisper mishearing fixes for chills/cold
    "तन्द":         "chills",
    "tand":          "chills",
    "thund":         "chills",
    "thand":         "chills",
    "kaampna":       "shivering",
    "kaanpna":       "shivering",

    # Jaundice / Yellow symptoms — Hindi variations
    "tuvcha peeli":     "yellowish_skin",
    "twacha peeli":     "yellowish_skin",
    "tvach peeli":      "yellowish_skin",
    "charm peela":      "yellowish_skin",
    "peeli tvacha":     "yellowish_skin",
    "peeli twach":      "yellowish_skin",
    "skin peeli":       "yellowish_skin",
    "body peela":       "yellowish_skin",
    "peela ho":         "yellowish_skin",

    "aankhein peeli":   "yellowing_of_eyes",
    "aankhe peeli":     "yellowing_of_eyes",
    "aakhe peeli":      "yellowing_of_eyes",   # Whisper mishear
    "aankhon mein peela": "yellowing_of_eyes",
    "eyes peeli":       "yellowing_of_eyes",
    "yellow eyes":      "yellowing_of_eyes",

    "peshab gehra":     "dark_urine",
    "peshab gehre":     "dark_urine",
    "gehre rang peshab": "dark_urine",
    "dark peshab":      "dark_urine",
    "peshab ka rang":   "dark_urine",
    "pesha gehra":      "dark_urine",
    "gehra peshab":     "dark_urine",
}


def extract_symptoms(text: str, feature_cols: list):
    """
    Convert free-form symptom text → binary feature vector.

    Args:
        text        : lowercased symptom description (English preferred)
        feature_cols: ordered list of 132 column names from the model

    Returns:
        feature_vector   : list of 132 ints (0 or 1)
        detected_symptoms: list of readable symptom names detected
    """
    # Normalize: lowercase, remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    detected = set()

    # Pass 1: Direct column name matching
    # e.g. "high fever" matches column "high_fever"
    for symptom in ALL_SYMPTOMS:
        readable = symptom.replace("_", " ")
        if readable in text:
            detected.add(symptom)

    # Pass 2: Keyword map matching
    # Catches Hindi transliterations, synonyms, Whisper mishearings
    for keyword, symptom_col in KEYWORD_MAP.items():
        if keyword in text and symptom_col in feature_cols:
            detected.add(symptom_col)

    # Build binary vector in exact column order the model expects
    feature_vector = [
        1 if col in detected else 0
        for col in feature_cols
    ]

    # Human-readable symptom names for the response
    detected_list = [s.replace("_", " ") for s in detected]

    return feature_vector, detected_list
