
from flask import Flask, request, jsonify, send_from_directory
import os

from predict import (
    predict_disease,
    predict_top_conditions,
    symptoms_list
)

from disease_info import get_disease_info

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/symptoms")
def get_symptoms():
    return jsonify({"symptoms": symptoms_list})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True) or {}
        selected_symptoms = data.get("symptoms", [])

        if not isinstance(selected_symptoms, list) or not selected_symptoms:
            return jsonify({
                "error": "Please select symptoms."
            }), 400

        valid_symptoms = [
            symptom.strip().lower()
            for symptom in selected_symptoms
            if isinstance(symptom, str)
            and symptom.strip().lower() in symptoms_list
        ]

        if not valid_symptoms:
            return jsonify({
                "error": "No valid symptoms selected."
            }), 400

        # Top 3 model predictions
        top_conditions = predict_top_conditions(
            valid_symptoms,
            top_n=3
        )

        # Primary prediction
        disease = top_conditions[0]["disease"]

        disease_info = get_disease_info(disease)

        return jsonify({
            "success": True,
            "predicted_disease": disease,
            "top_conditions": top_conditions,
            "description": disease_info["description"],
            "precautions": disease_info["precautions"],
            "message": (
                "Educational prediction only, "
                "not a medical diagnosis."
            )
        })

    except Exception as error:
        print("Prediction error:", error)

        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    print("Starting MediPredict AI...")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
    