# ETL Pipeline

The ETL process consists of two stages:

## 1. Extract & Transform
`project_checkpoint4_group1.ipynb`

- Reads the original Excel workbook
- Cleans and standardizes the data
- Exports cleaned CSV files
- Produces an ETL summary

## 2. Load
`app/scripts/load_data.py`

- Imports cleaned CSV files into PostgreSQL
- Loads tables in dependency order
- Maintains foreign-key relationships
- Populates the relational database