import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker()

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

def generate_patients(num_patients=1000):
    patients = []

    for i in range(num_patients):
        patients.append({
            "patient_id": f"P{i:05d}",
            "mrn": fake.unique.bothify(text="MRN#####"),
            "dob": fake.date_of_birth(minimum_age=30, maximum_age=85),
            "gender": random.choice(["M", "F"]),
            "zip": fake.postcode()
        })

    return pd.DataFrame(patients)

def generate_diagnoses(df_patients):
    icd_codes = ["C50.9", "C34.1", "C18.9", "INVALID_CODE"]
    stages = ["I", "II", "III", "IV", None]

    diagnoses = []

    for _, row in df_patients.iterrows():
        diagnoses.append({
            "diagnosis_id": fake.uuid4(),
            "patient_id": row["patient_id"],
            "icd10_code": random.choice(icd_codes),
            "diagnosis_date": fake.date_between(start_date="-5y", end_date="+30d"),
            "stage": random.choice(stages)
        })

    return pd.DataFrame(diagnoses)

if __name__ == "__main__":
    df_patients = generate_patients(1000)
    df_diagnoses = generate_diagnoses(df_patients)

    df_patients.to_csv(RAW_DIR / "patients.csv", index=False)
    df_diagnoses.to_csv(RAW_DIR / "diagnoses.csv", index=False)

    print("patients.csv and diagnoses.csv generated")

