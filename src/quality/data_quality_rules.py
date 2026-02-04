import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
REF_DIR = BASE_DIR / "data" / "reference"

patients = pd.read_csv(RAW_DIR / "patients.csv")
diagnoses = pd.read_csv(RAW_DIR / "diagnoses.csv")
icd10 = pd.read_csv(REF_DIR / "icd10.csv")

diagnoses["diagnosis_date"] = pd.to_datetime(diagnoses["diagnosis_date"])
today = pd.Timestamp(datetime.today().date())

results = []

# RULE 1 – Valid ICD-10
invalid_icd = diagnoses[
    ~diagnoses["icd10_code"].isin(icd10["code"])
]
results.append({
    "rule": "Valid ICD-10 Code",
    "severity": "CRITICAL",
    "failed_records": invalid_icd.shape[0]
})

# RULE 2 – Cancer stage present
missing_stage = diagnoses[diagnoses["stage"].isna()]
results.append({
    "rule": "Cancer Stage Present",
    "severity": "CRITICAL",
    "failed_records": missing_stage.shape[0]
})

# RULE 3 – Diagnosis date not in future
future_dates = diagnoses[diagnoses["diagnosis_date"] > today]
results.append({
    "rule": "Diagnosis Date Not in Future",
    "severity": "WARNING",
    "failed_records": future_dates.shape[0]
})

# RULE 4 – Valid patient reference
invalid_patient = diagnoses[
    ~diagnoses["patient_id"].isin(patients["patient_id"])
]
results.append({
    "rule": "Valid Patient Reference",
    "severity": "CRITICAL",
    "failed_records": invalid_patient.shape[0]
})

df_results = pd.DataFrame(results)

print("\nDATA QUALITY SUMMARY")
print(df_results.to_string(index=False))

