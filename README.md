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


