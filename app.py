from flask import Flask, request, jsonify, send_from_directory
import os

from predict import predict_disease, symptoms_list

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True) or {}

        selected_symptoms = data.get("symptoms", [])

        if not isinstance(selected_symptoms, list):
            return jsonify({
                "error": "Symptoms must be provided as a list."
            }), 400

        if not selected_symptoms:
            return jsonify({
                "error": "Please select at least one symptom."
            }), 400

        valid_symptoms = [
            str(symptom).strip().lower()
            for symptom in selected_symptoms
            if isinstance(symptom, str)
            and str(symptom).strip().lower() in symptoms_list
        ]

        if not valid_symptoms:
            return jsonify({
                "error": "No valid symptoms selected."
            }), 400

        result = predict_disease(valid_symptoms)

        return jsonify({
            "success": True,
            "predicted_disease": str(result),
            "message": "This is an educational prediction, not a medical diagnosis."
        })

    except Exception as error:
        print("Prediction error:", error)

        return jsonify({
            "error": "Something went wrong while processing your symptoms."
        }), 500


if __name__ == "__main__":
    print("Starting MediPredict AI...")
    app.run(host="127.0.0.1", port=5000, debug=True)