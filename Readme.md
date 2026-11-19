# 🩺 MediPredict AI
### AI-Based Disease Prediction System Using Symptoms

**Understand Your Symptoms. Explore Your Health.**

MediPredict AI is a machine learning-based web application that analyzes user-selected symptoms and presents three possible conditions using a trained Random Forest classification model.

> ⚠️ Disclaimer: This project is developed for educational purposes only. It does not provide medical diagnoses or replace professional medical advice.

## 🚀 Features

- Select symptoms from an interactive symptom library.
- Search and filter available symptoms.
- Predict three possible conditions.
- Display model scores for predicted conditions.
- View disease descriptions.
- Display general precautions from the dataset.
- Responsive healthcare dashboard interface.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Machine Learning | Scikit-learn, Random Forest |
| Data Processing | Pandas, NumPy |
| Model Storage | Joblib |
| Dataset | CSV files |

## 🧠 Machine Learning Model

The project uses a Random Forest Classifier.

**Dataset information:**
- Original records: 4,920
- Unique symptom patterns after deduplication: 304
- Disease classes: 41
- Unique symptoms: 131

**Model evaluation:**
- Training/testing split: 75% / 25%
- Test records: 76
- Test accuracy: 100%
- Five-fold cross-validation average: 100%

Note: These results are based on a structured dataset. They do not demonstrate real-world medical accuracy. Model scores are not calibrated medical probabilities.

## 📁 Project Structure

```text
MediPredict-AI/
│
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── predict.py
│   ├── disease_info.py
│   └── evaluate_model.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── dataset/
│   ├── dataset.csv
│   ├── Symptom-severity.csv
│   ├── symptom_Description.csv
│   └── symptom_precaution.csv
│
├── model/
│   ├── disease_model.pkl
│   └── symptoms_list.pkl
│
├── Readme.md
├── requirements.txt
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sricharandandela-design/medipredict-ai-2026.git
```

### 2. Open the project directory

```bash
cd medipredict-ai-2026
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python -u backend/app.py
```

### 7. Open in your browser

```text
http://127.0.0.1:5000
```

## 🔄 Project Workflow

1. User selects symptoms.
2. Frontend sends symptoms to Flask backend.
3. Backend prepares the input features.
4. Random Forest model processes the symptoms.
5. System returns the top three model predictions.
6. Disease information and dataset precautions are displayed.

## 🎯 Project Objective

The objective of MediPredict AI is to demonstrate how machine learning can be integrated into a web application to explore symptom-based disease prediction.

## 👨‍💻 Developer

**GitHub:** [sricharandandela-design](https://github.com/sricharandandela-design)

**Project:** MediPredict AI

---

⭐ If you find this project interesting, consider starring the repository!