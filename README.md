## Oncology Clinical Data POC

### Objective
Demonstrate clinical data quality, profiling, and reconciliation
patterns used in oncology analytics pipelines.

### Key Data Quality Rules
- ICD-10 code validation
- Mandatory cancer staging
- Diagnosis date sanity checks
- Patient reference integrity

### Project Structure
- src/profiling – data profiling checks
- src/quality – rule-based validations
- src/reconciliation – source-to-source checks
- docs – business and clinical rules

### Tech Stack
- Python
- Pandas
- PySpark (future)
- Snowflake-ready design

### How to Run
```bash
pip install -r requirements.txt
python src/profiling/data_profiling.py

