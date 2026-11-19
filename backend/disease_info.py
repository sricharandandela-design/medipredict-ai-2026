import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

description_df = pd.read_csv(
    os.path.join(DATASET_DIR, "symptom_Description.csv")
)

precaution_df = pd.read_csv(
    os.path.join(DATASET_DIR, "symptom_precaution.csv")
)


def get_disease_info(disease):
    description = "No description available."
    precautions = []

    description_row = description_df[
        description_df["Disease"].str.lower() == disease.lower()
    ]

    if not description_row.empty:
        description = str(description_row.iloc[0]["Description"])

    precaution_row = precaution_df[
        precaution_df["Disease"].str.lower() == disease.lower()
    ]

    if not precaution_row.empty:
        row = precaution_row.iloc[0]

        for column in precaution_df.columns:
            if column.lower().startswith("precaution"):
                value = row[column]

                if pd.notna(value) and str(value).strip():
                    precautions.append(str(value).replace("_", " "))

    return {
        "description": description,
        "precautions": precautions
    }