# Database Loader Module

## Project Description
This project uses Python, SQLAlchemy and SQLite to create and manage a database with automated data insertion and updating.

## Technologies Used
- Python 3
- SQLAlchemy
- SQLite

## Features
- Database connection.
- Automatic table creation.
- Primary key implementation.
- Batch data insertion.
- Upsert operations (insert or update).
- Transaction safety.
- SQL query verification.

## Files
1. database_loader.py
2. verify_data.py
3. database.db

## How to Run

Install SQLAlchemy:

```bash
pip install sqlalchemy
```

Run the database loader:

```bash
python database_loader.py
```

Verify database records:

```bash
python verify_data.py
```

## Result
Successfully created an SQLite database, inserted or updated records, and verified the database using SQL queries.