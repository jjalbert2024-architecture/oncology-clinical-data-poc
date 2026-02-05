import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
REF_DIR = BASE_DIR / "data" / "reference"
CURATED_DIR = BASE_DIR / "data" / "curated"

CURATED_DIR.mkdir(parents=True, exist_ok=True)

# 1️⃣ Load required datasets
diagnoses = pd.read_csv(RAW_DIR / "diagnoses.csv")
patients = pd.read_csv(RAW_DIR / "patients.csv")
icd10 = pd.read_csv(REF_DIR / "icd10.csv")

#2️⃣ Enrich diagnoses with ICD-10 reference
#This is your clinical standardization step.

analytics = diagnoses.merge(
    icd10,
    how="left",
    left_on="icd10_code",
    right_on="code"
)
# After this:  Mapped diagnoses have cancer type & Unmapped ones are clearly visible

#3️⃣ Add reconciliation & quality flags
analytics["diagnosis_date"] = pd.to_datetime(analytics["diagnosis_date"])
today = pd.Timestamp(datetime.today().date())

analytics["is_valid_icd"] = analytics["description"].notna()
analytics["has_stage"] = analytics["stage"].notna()
analytics["is_future_date"] = analytics["diagnosis_date"] > today

analytics["reconciliation_status"] = analytics["is_valid_icd"].apply(
    lambda x: "MAPPED" if x else "UNMAPPED"
)

#4️⃣ Derive overall data quality status (KEY STEP)
def derive_quality_status(row):
    if not row["is_valid_icd"]:
        return "REVIEW_NEEDED"
    if not row["has_stage"]:
        return "REVIEW_NEEDED"
    if row["is_future_date"]:
        return "REVIEW_NEEDED"
    return "TRUSTED"

analytics["data_quality_status"] = analytics.apply(derive_quality_status, axis=1)
#This lets you filter dashboards by trust — very powerful.

#5️⃣ Select final analytics columns
final_columns = [
    "patient_id",
    "diagnosis_id",
    "diagnosis_date",
    "stage",
    "cancer_type",
    "description",
    "reconciliation_status",
    "is_valid_icd",
    "has_stage",
    "is_future_date",
    "data_quality_status"
]
analytics_final = analytics[final_columns]

#6️⃣ Write curated analytics dataset
analytics_final.to_csv(
    CURATED_DIR / "oncology_analytics.csv",
    index=False
)
print("Curated analytics dataset created: data/curated/oncology_analytics.csv")
print(analytics_final["data_quality_status"].value_counts())

#You now have:
#✔ A curated analytics dataset
#✔ Enriched clinical meaning
#✔ Embedded data quality context
#✔ A dataset ready for Power BI / Streamlit
#✔ A clean “Delta-like” layer

#“After profiling, validation, and reconciliation, I created a curated oncology analytics dataset with embedded data quality flags so dashboards always reflect trust context.”
#Output Generated
#Curated analytics dataset created: data/curated/oncology_analytics.csv
#data_quality_status
#TRUSTED          606
#REVIEW_NEEDED    394
#Name: count, dtype: int64

#*
# You now have:
#
# ✔ A curated analytics dataset
# ✔ Enriched clinical meaning
# ✔ Embedded data quality context
# ✔ A dataset ready for Power BI / Streamlit
# ✔ A clean “Delta-like” layer
#
# This is exactly what a Clinical Data Architect or Analyst hands off for reporting.

#“After profiling, validation, and reconciliation,
# I created a curated oncology analytics dataset
# with embedded data quality flags so dashboards always reflect trust context.”
