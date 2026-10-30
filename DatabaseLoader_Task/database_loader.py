
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.sqlite import insert

# Create database connection
engine = create_engine("sqlite:///database.db")

Base = declarative_base()

# Create table schema
class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    customer = Column(String(50))
    product = Column(String(50))
    amount = Column(Float)
    quantity = Column(Integer)

# Create table automatically
Base.metadata.create_all(engine)

# Sample data
data = [
    {"order_id": 1, "customer": "Alice",
     "product": "Laptop", "amount": 50000, "quantity": 1},

    {"order_id": 2, "customer": "Bob",
     "product": "Mobile", "amount": 20000, "quantity": 2},

    {"order_id": 3, "customer": "Charlie",
     "product": "Keyboard", "amount": 1500, "quantity": 1},

    {"order_id": 4, "customer": "David",
     "product": "Mouse", "amount": 800, "quantity": 3},

    {"order_id": 5, "customer": "Eva",
     "product": "Monitor", "amount": 12000, "quantity": 1}
]

# Perform batch upsert
try:
    with engine.begin() as connection:

        statement = insert(Orders).values(data)

        statement = statement.on_conflict_do_update(
            index_elements=["order_id"],
            set_={
                "customer": statement.excluded.customer,
                "product": statement.excluded.product,
                "amount": statement.excluded.amount,
                "quantity": statement.excluded.quantity
            }
        )

        connection.execute(statement)

    print("Database connected successfully!")
    print("Table created successfully!")
    print("Data inserted or updated successfully!")
    print("Transaction completed successfully!")

except Exception as e:
    print("Database Error:", e)
