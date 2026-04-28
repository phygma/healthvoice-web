# train_diagnosis_model.py
# Run this file once to train and save the model

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("Loading dataset...")

# Load dataset
train_df = pd.read_csv('data/Training.csv')
test_df  = pd.read_csv('data/Testing.csv')

# Remove unwanted columns (if present)
train_df = train_df.loc[:, ~train_df.columns.str.contains('^Unnamed')]
test_df  = test_df.loc[:,  ~test_df.columns.str.contains('^Unnamed')]

# Features and labels
feature_cols = [col for col in train_df.columns if col != 'prognosis']

X_train = train_df[feature_cols].values
y_train = train_df['prognosis'].values

X_test = test_df[feature_cols].values
y_test = test_df['prognosis'].values

print(f"Training samples: {X_train.shape[0]}")
print(f"Features: {X_train.shape[1]}")
print(f"Diseases: {len(set(y_train))}")

# Train model
print("\nTraining model...")
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\nModel trained successfully!")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
os.makedirs('models', exist_ok=True)

joblib.dump(model, 'models/diagnosis_model.pkl')
joblib.dump(feature_cols, 'models/diagnosis_columns.pkl')

print("\nModel saved successfully!")