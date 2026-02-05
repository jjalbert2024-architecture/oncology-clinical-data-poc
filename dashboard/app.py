import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Oncology Clinical Analytics",
    layout="wide"
)

st.title("🧬 Oncology Clinical Analytics Dashboard")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "curated" / "oncology_analytics.csv"

df = pd.read_csv(DATA_PATH)

st.success("Curated oncology analytics dataset loaded successfully")
st.write(df.head())

#1. Add Sidebar Title
st.sidebar.header("🔎 Clinical Filters")

#2. Cancer Type Filter
# Why multiselect? Clinicians often compare cohorts

cancer_types = sorted(df["cancer_type"].dropna().unique())
selected_cancer_types = st.sidebar.multiselect(
    "Cancer Type",
    options=cancer_types,
    default=cancer_types
)

#3. Cancer Stage Filter
stages = sorted(df["stage"].dropna().unique())
selected_stages = st.sidebar.multiselect(
    "Cancer Stage",
    options=stages,
    default=stages
)

#4. Data Quality Filter (VERY IMPORTANT) | This is your governance hook.
quality_statuses = sorted(df["data_quality_status"].unique())
selected_quality = st.sidebar.multiselect(
    "Data Quality Status",
    options=quality_statuses,
    default=quality_statuses
)

#4. Apply Filters to Dataset
filtered_df = df[
    (df["cancer_type"].isin(selected_cancer_types)) &
    (df["stage"].isin(selected_stages)) &
    (df["data_quality_status"].isin(selected_quality))
    ]

#6. Show Filtered Record Count
st.markdown("### 📊 Filtered Dataset Preview")
st.write(f"Records after filtering: {filtered_df.shape[0]}")
st.dataframe(filtered_df.head(20))

