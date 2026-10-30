
import pandas as pd
import sqlite3
import logging
import schedule
import time
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime

# Logging configuration
logging.basicConfig(
    filename="etl_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline():

    try:
        print("\nStarting ETL Pipeline...")

        # 1. EXTRACT DATA
        df = pd.read_csv("sales_data.csv")
        logging.info("Data extracted successfully")

        # 2. TRANSFORM DATA
        df = df.drop_duplicates(subset=["Order_ID"])

        df["Customer"] = df["Customer"].fillna("Unknown")

        df["Amount"] = pd.to_numeric(
            df["Amount"], errors="coerce"
        )

        df["Quantity"] = pd.to_numeric(
            df["Quantity"], errors="coerce"
        )

        df = df.dropna(
            subset=["Order_ID", "Amount", "Quantity"]
        )

        df["Order_ID"] = df["Order_ID"].astype(int)
        df["Quantity"] = df["Quantity"].astype(int)

        logging.info("Data transformed successfully")

        # 3. LOAD DATA INTO SQLITE
        connection = sqlite3.connect("etl_database.db")

        connection.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                Order_ID INTEGER PRIMARY KEY,
                Customer TEXT,
                Product TEXT,
                Amount REAL,
                Quantity INTEGER
            )
        """)

        records = df[
            ["Order_ID", "Customer", "Product", "Amount", "Quantity"]
        ].values.tolist()

        connection.executemany("""
            INSERT INTO sales
            (Order_ID, Customer, Product, Amount, Quantity)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(Order_ID) DO UPDATE SET
                Customer = excluded.Customer,
                Product = excluded.Product,
                Amount = excluded.Amount,
                Quantity = excluded.Quantity
        """, records)

        connection.commit()

        total_records = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

        total_sales = connection.execute(
            "SELECT SUM(Amount) FROM sales"
        ).fetchone()[0]

        connection.close()

        logging.info("Data loaded into database successfully")

        # 4. GENERATE SUMMARY
        report = f"""
ETL PIPELINE SUMMARY
--------------------
Execution Time: {datetime.now()}
Records Processed: {len(df)}
Database Records: {total_records}
Total Sales: {total_sales}
Status: SUCCESS
"""

        print(report)

        with open("etl_report.txt", "w") as file:
            file.write(report)

        # 5. SEND EMAIL (OPTIONAL)
        sender = os.getenv("ETL_EMAIL")
        password = os.getenv("ETL_APP_PASSWORD")
        receiver = os.getenv("ETL_RECEIVER")

        if sender and password and receiver:

            message = EmailMessage()
            message["Subject"] = "ETL Pipeline Report"
            message["From"] = sender
            message["To"] = receiver
            message.set_content(report)

            with smtplib.SMTP_SSL(
                "smtp.gmail.com", 465
            ) as server:
                server.login(sender, password)
                server.send_message(message)

            print("Email report sent successfully!")

        else:
            print("Email skipped: Email settings not configured.")

        logging.info("ETL pipeline completed successfully")

    except Exception as e:
        logging.exception("ETL pipeline failed")
        print("Pipeline Error:", e)


# Run once immediately
run_pipeline()

# Schedule automatic execution
schedule.every(5).minutes.do(run_pipeline)

print("ETL Pipeline scheduled every 5 minutes.")
print("Press Ctrl+C to stop.")

# Continuous execution
while True:
    schedule.run_pending()
    time.sleep(1)
