import joblib
from utils.symptom_extractor import extract_symptoms

cols = joblib.load("models/diagnosis_columns.pkl")

text = "mujhe bukhar hai aur sir dard ho raha hai"

vec, symptoms = extract_symptoms(text, cols)

print(symptoms)
print(sum(vec))