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

#Validation 1: Missing Data Analysis (CRITICAL FOR ONCOLOGY)
missing_stage_count = diagnoses["stage"].isna().sum()
print(f"Missing cancer stage count: {missing_stage_count}")

#Validation 2: ICD-10 Terminology Validation (JD CORE)
#It identifies invalid or unmapped ICD-10 diagnosis codes in clinical data,
# which is a critical data quality check before analytics, reporting, or regulatory submissions.
# This filters all diagnosis records where the ICD-10 code does NOT exist in the official reference table.

invalid_icd = diagnoses[
    ~diagnoses["icd10_code"].isin(icd10["code"]) #Official/reference list of valid ICD-10 codes → checks whether each diagnosis code exists in the official list
]
print("\nInvalid ICD-10 codes found:")
print(invalid_icd["icd10_code"].value_counts())


#Validation 3: Future Diagnosis Dates (Data Integrity)
#It identifies diagnosis records that have dates occurring in the future, which are typically invalid in clinical datasets.
#Future-dated diagnoses usually indicate data entry errors, system default dates, timezone issues, or ETL transformation problems.

from datetime import datetime
today = pd.Timestamp(datetime.today().date())

future_diagnoses = diagnoses[
    pd.to_datetime(diagnoses["diagnosis_date"]) > today
    ]
print(f"\nDiagnoses with future dates: {future_diagnoses.shape[0]}")

#Validation 4: Distribution Analysis (Clinical Reasoning)
print("\nDiagnosis count by ICD-10 code:")
print(diagnoses["icd10_code"].value_counts()) #This shows the frequency distribution of diagnosis codes in the dataset.

print("\nCancer stage distribution:")
print(diagnoses["stage"].value_counts(dropna=False))

#bring more clarity (Breast cancer 252 where compared to C50.9 252), add the following
#a Merge diagnoses with ICD-10 reference (BEST PRACTICE)
diagnoses_enriched = diagnoses.merge(
    icd10,
    left_on="icd10_code",
    right_on="code",
    how="left"
)
#b Handle invalid / unmapped ICD-10 codes
diagnoses_enriched["description"] = diagnoses_enriched["description"].fillna(
    "Invalid / Unmapped ICD-10 Code"
)
diagnoses_enriched["cancer_type"] = diagnoses_enriched["cancer_type"].fillna(
    "Unknown"
)
#c Final reporting (clean & readable)
print("\nDiagnosis count by Cancer Description:")
print(diagnoses_enriched["description"].value_counts())

print("\nDiagnosis count by Cancer Type:")
print(diagnoses_enriched["cancer_type"].value_counts())



