import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_DIR, exist_ok=True)

# Load dataset
data = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")
print("Original dataset shape:", data.shape)

# Clean column names
data.columns = data.columns.str.strip()

# Separate symptoms and disease labels
X_raw = data.drop(columns=["Disease"])
y = data["Disease"].astype(str).str.strip()

# Clean symptom values
X_raw = X_raw.fillna("")
X_raw = X_raw.astype(str).apply(
    lambda col: col.str.strip().str.lower()
)

# Collect unique symptoms
all_symptoms = sorted({
    value
    for value in X_raw.to_numpy().flatten()
    if value and value != "nan"
})

# Create binary symptom matrix
X = pd.DataFrame(
    0,
    index=data.index,
    columns=all_symptoms
)

for column in X_raw.columns:
    for index, symptom in X_raw[column].items():
        if symptom and symptom != "nan":
            X.at[index, symptom] = 1

# Remove duplicate symptom patterns
X["Disease"] = y

X = X.drop_duplicates()

y = X["Disease"]
X = X.drop(columns=["Disease"])

print("\n========== DATASET INFORMATION ==========")
print("Unique symptom patterns:", len(X))
print("Number of diseases:", y.nunique())
print("Number of symptoms:", len(all_symptoms))

# Check whether every disease has enough unique examples
class_counts = y.value_counts()

print("\nMinimum examples per disease:", class_counts.min())

if class_counts.min() < 2:
    raise ValueError(
        "Some diseases have fewer than 2 unique patterns. "
        "A stratified train/test split is not possible."
    )

# Split unique patterns into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

print("\nTraining Random Forest model...")
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n========== MODEL RESULTS ==========")
print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# Save trained model and symptom list
joblib.dump(
    model,
    os.path.join(MODEL_DIR, "disease_model.pkl")
)

joblib.dump(
    all_symptoms,
    os.path.join(MODEL_DIR, "symptoms_list.pkl")
)

print("\nModel saved successfully!")
print("Location: model/disease_model.pkl")