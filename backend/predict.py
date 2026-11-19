
import os
import joblib
import pandas as pd

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# Load trained model
model = joblib.load(
    os.path.join(MODEL_DIR, "disease_model.pkl")
)

symptoms_list = joblib.load(
    os.path.join(MODEL_DIR, "symptoms_list.pkl")
)


def prepare_input(selected_symptoms):
    input_data = pd.DataFrame(
        0,
        index=[0],
        columns=symptoms_list
    )

    for symptom in selected_symptoms:
        if not isinstance(symptom, str):
            continue

        symptom = symptom.strip().lower()

        if symptom in input_data.columns:
            input_data.at[0, symptom] = 1

    return input_data


def predict_disease(selected_symptoms):
    input_data = prepare_input(selected_symptoms)

    prediction = model.predict(input_data)[0]

    return str(prediction)


def predict_top_conditions(selected_symptoms, top_n=3):
    input_data = prepare_input(selected_symptoms)

    scores = model.predict_proba(input_data)[0]

    top_indices = scores.argsort()[::-1][:top_n]

    results = []

    for index in top_indices:
        results.append({
            "disease": str(model.classes_[index]),
            "score": round(float(scores[index]) * 100, 2)
        })

    return results
