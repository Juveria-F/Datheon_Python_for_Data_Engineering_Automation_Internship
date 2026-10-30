# Automated ETL Pipeline

## Project Description
This project automates the Extract, Transform and Load (ETL) process using Python.

## Technologies Used
- Python 3
- Pandas
- SQLite
- Schedule
- Logging
- SMTP

## Features
- Automated data extraction from CSV.
- Data cleaning and transformation.
- Duplicate record removal.
- Database loading using SQLite.
- Upsert operations.
- Automated scheduling every 5 minutes.
- Execution logging.
- Summary report generation.
- Optional email notifications.

## Files
1. etl_pipeline.py
2. sales_data.csv
3. etl_database.db
4. etl_log.txt
5. etl_report.txt

## Installation

```bash
pip install pandas sqlalchemy schedule
```

## Execution

```bash
python etl_pipeline.py
```

## Result
Successfully implemented an automated ETL pipeline with scheduling, database storage, logging and summary report generation.