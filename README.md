# 🧬 Oncology Clinical Analytics POC

## Overview
This project demonstrates a **clinical data analytics workflow** commonly used in **oncology and healthcare data platforms**. It focuses on **data quality, standardization, reconciliation, and safe analytics consumption**, ending with an **interactive Streamlit dashboard** suitable for clinical and business stakeholders.

The POC mirrors real-world patterns used in **EHR / oncology analytics pipelines**, while remaining **fully local, reproducible, and cost-free**.

---

## 🎯 Objectives
- Ingest raw clinical encounter data
- Standardize clinical terminology (ICD-10)
- Profile and validate oncology datasets
- Apply rule-based data quality checks
- Reconcile clinical records against reference data
- Produce a **curated analytics dataset**
- Present insights via an **interactive Streamlit dashboard**
- Surface **data trust context** alongside analytics

---

## 🏗️ High-Level Architecture (Conceptual)
```text
Clinical Source Files (CSV / JSON)
        ↓
RAW Layer (data/raw)
        ↓
Profiling & Validation (Python)
        ↓
Reconciliation & Quality Rules
        ↓
CURATED Layer (data/curated)
        ↓
Analytics & Dashboard (Streamlit)
```

> This design maps cleanly to cloud-native architectures  
> (ADLS → Synapse Spark → Delta Lake → Serverless SQL).

## 📂 Project Structure

```text
oncology-clinical-data-poc/
│
├── dashboard/
│   └── app.py                  # Streamlit analytics dashboard
│
├── data/
│   ├── raw/                    # Raw clinical datasets
│   ├── reference/              # ICD-10 and clinical reference data
│   └── curated/                # Analytics-ready datasets
│
├── src/
│   ├── data_generation/        # Synthetic data generation
│   ├── profiling/              # Data profiling & exploration
│   ├── quality/                # Data quality rules
│   └── reconciliation/         # Source-to-reference reconciliation
│
├── docs/                       # Clinical & business documentation
├── sql/                        # SQL-based analysis (optional)
├── requirements.txt
└── README.md
```

## 🧪 Key Data Quality Rules

The following data quality rules are applied to ensure **clinical accuracy, trust, and usability** of oncology data:

| Rule | Severity | Description |
|------|----------|-------------|
| Valid ICD-10 Code | Critical | Diagnosis must map to a valid ICD-10 reference |
| Cancer Stage Present | Critical | Oncology staging is mandatory for analysis |
| Diagnosis Date Sanity | Warning | Diagnosis date cannot be in the future |
| Patient Reference Integrity | Critical | Diagnosis must link to a valid patient |

Each rule is **clinically meaningful, measurable, and explainable** to both technical and non-technical stakeholders.
