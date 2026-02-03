import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
REF_DIR = BASE_DIR / "data" / "reference"

patients = pd.read_csv(RAW_DIR / "patients.csv")
diagnoses = pd.read_csv(RAW_DIR / "diagnoses.csv")
icd10 = pd.read_csv(REF_DIR / "icd10.csv")

#addition 1
print("Patients count:", patients.shape[0])
print("Diagnoses count:", diagnoses.shape[0])

print("\nDiagnoses columns:")
print(diagnoses.dtypes)
