# ETL Process

This folder contains the Extract, Transform, and Load (ETL) resources used for the ABC Foodmart Database Systems project.

The ETL process prepares the generated operational data before it is loaded into the PostgreSQL database.

---

## Workflow

```text
Business Scenario
        ↓
generate_data.py
        ↓
Generated CSV Files
        ↓
ETL Notebook
        ↓
Cleaned CSV Files
        ↓
load_data.py
        ↓
PostgreSQL Database
```

---

## Contents

### project_checkpoint4_group1.ipynb

This Jupyter Notebook performs the **Extract** and **Transform** stages of the ETL process.

The notebook:

- Reads the generated source data
- Standardizes column names
- Cleans and formats values
- Converts dates and times
- Handles missing values
- Standardizes categorical fields
- Removes invalid records when necessary
- Produces cleaned CSV files
- Generates an ETL summary report

---

## Relationship to the Backend

This notebook prepares the data only.

Database loading is performed separately by:

```text
app/scripts/load_data.py
```

The loading script imports the cleaned CSV files into PostgreSQL while maintaining primary and foreign key relationships.

---

## Project Structure

```text
abc-foodmart-api/

etl/
    project_checkpoint4_group1.ipynb

app/
    scripts/
        generate_data.py
        load_data.py

data/
```

---

## Technologies

- Python
- Jupyter Notebook
- Pandas
- PostgreSQL

---

## Notes

This notebook is part of the project's complete ETL pipeline.

It prepares the operational datasets used to populate the normalized PostgreSQL database that powers the FastAPI backend and React executive dashboard.