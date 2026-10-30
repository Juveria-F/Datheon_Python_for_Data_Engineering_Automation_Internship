
from sqlalchemy import create_engine, text

# Connect to database
engine = create_engine("sqlite:///database.db")

# Display all records
with engine.connect() as connection:

    result = connection.execute(
        text("SELECT * FROM orders")
    )

    print("DATABASE RECORDS")
    print("----------------")

    for row in result:
        print(row)

    # Count total records
    count = connection.execute(
        text("SELECT COUNT(*) FROM orders")
    ).scalar()

    print("\nTotal Records:", count)

    # Calculate total sales
    total = connection.execute(
        text("SELECT SUM(amount) FROM orders")
    ).scalar()

    print("Total Sales:", total)

    print("\nDatabase verification completed!")
