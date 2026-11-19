import os
import pandas as pd

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier

# --------------------------------
# 1. Project paths
# --------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(
    BASE_DIR, "dataset", "dataset.csv"
)

# --------------------------------
# 2. Load dataset
# --------------------------------

data = pd.read_csv(DATASET_PATH)

data.columns = data.columns.str.strip()

print("Dataset loaded successfully!")
print("Original dataset shape:", data.shape)

if "Disease" not in data.columns:
    raise ValueError("Disease column not found in dataset.")

# --------------------------------
# 3. Separate features and labels
# --------------------------------

y = data["Disease"].astype(str).str.strip()

X_raw = data.drop(columns=["Disease"])

# Clean symptom values
X_raw = X_raw.fillna("")

X_raw = X_raw.astype(str).apply(
    lambda column: column.str.strip().str.lower()
)

# --------------------------------
# 4. Create symptom list
# --------------------------------

all_symptoms = sorted({
    symptom
    for symptom in X_raw.to_numpy().flatten()
    if symptom and symptom != "nan"
})

# --------------------------------
# 5. Convert symptoms into binary data
# --------------------------------

X = pd.DataFrame(
    0,
    index=data.index,
    columns=all_symptoms
)

for column in X_raw.columns:
    for index, symptom in X_raw[column].items():

        if symptom and symptom != "nan":
            X.at[index, symptom] = 1

# --------------------------------
# 6. Remove duplicate patterns
# --------------------------------

X["Disease"] = y

combined = X.drop_duplicates()

y = combined["Disease"]

X = combined.drop(columns=["Disease"])

print("\n========== DATASET INFORMATION ==========")

print("Unique symptom patterns:", len(X))
print("Number of diseases:", y.nunique())
print("Number of symptoms:", len(all_symptoms))

# --------------------------------
# 7. Check minimum samples
# --------------------------------

class_counts = y.value_counts()

minimum_samples = class_counts.min()

print("Minimum examples per disease:", minimum_samples)

if minimum_samples < 5:
    raise ValueError(
        "Some diseases have fewer than 5 unique patterns. "
        "Five-fold evaluation cannot be performed reliably."
    )

# --------------------------------
# 8. Five-fold cross-validation
# --------------------------------

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

print("\nEvaluating Random Forest model...")

scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="accuracy"
)

# --------------------------------
# 9. Display results
# --------------------------------

print("\n========== 5-FOLD CROSS VALIDATION ==========")

for i, score in enumerate(scores, start=1):
    print("Fold", i, "Accuracy:", round(score * 100, 2), "%")

print("\nAverage Accuracy:", round(scores.mean() * 100, 2), "%")

print(
    "Standard Deviation:",
    round(scores.std() * 100, 2),
    "%"
)

print("\nEvaluation completed successfully!")