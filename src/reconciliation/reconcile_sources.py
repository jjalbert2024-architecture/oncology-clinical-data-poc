import pandas as pd
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
REF_DIR = BASE_DIR / "data" / "reference"

# Load datasets
diagnoses = pd.read_csv(RAW_DIR / "diagnoses.csv")
icd10 = pd.read_csv(REF_DIR / "icd10.csv")

# Reconcile diagnoses with ICD-10 reference
reconciled = diagnoses.merge(
    icd10,
    how="left",
    left_on="icd10_code",
    right_on="code"
)

# Identify unmapped diagnosis records
unmapped = reconciled[reconciled["description"].isna()]

print(f"Unmapped diagnosis records: {unmapped.shape[0]}")
print("\nUnmapped ICD-10 codes:")
print(unmapped["icd10_code"].value_counts())

# Reconciliation status classification
#It assigns a reconciliation status to every diagnosis record, clearly indicating whether the ICD-10 code was successfully mapped to the reference table or not.


#reconciled["reconciliation_status"] = reconciled["description"].apply(
#    lambda x: "MAPPED" if pd.notna(x) else "UNMAPPED"
#)
reconciled["reconciliation_status"] = (
    reconciled["description"].notna()
    .map({True: "MAPPED", False: "UNMAPPED"})
)

print("\nReconciliation status distribution:")
print(reconciled["reconciliation_status"].value_counts())

# Clinical impact summary
impact = reconciled.groupby("reconciliation_status").size().reset_index(name="count")
print("\nClinical impact summary:")
print(impact)
