
import pandas as pd
import re
import os

# Read the original dataset
df = pd.read_csv("raw_data.csv")

print("Original Data:")
print(df)

# Store original information
original_rows = len(df)
missing_before = int(df.isnull().sum().sum())

# 1. Remove duplicate records
df = df.drop_duplicates(subset=["Order_ID"], keep="first")

# 2. Handle missing values
df["Customer"] = df["Customer"].fillna("Unknown")

# 3. Normalize currency values
def clean_currency(value):
    if pd.isna(value):
        return None

    value = str(value)
    value = re.sub(r"(?i)INR|Rs\.?|₹|\$", "", value)
    value = value.replace(",", "").strip()

    return pd.to_numeric(value, errors="coerce")

df["Amount"] = df["Amount"].apply(clean_currency)

# 4. Normalize date formats
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

# 5. Convert quantity into numeric format
df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)

# 6. Schema validation
required_columns = [
    "Order_ID", "Customer", "Amount",
    "Order_Date", "Quantity"
]

if list(df.columns) != required_columns:
    raise ValueError("Invalid dataset columns!")

# Check invalid records
invalid = (
    df["Order_ID"].isna() |
    df["Amount"].isna() |
    df["Order_Date"].isna() |
    df["Quantity"].isna() |
    (df["Amount"] < 0) |
    (df["Quantity"] <= 0)
)

# Save rejected records
rejected = df[invalid].copy()
rejected.to_csv("rejected_records.csv", index=False)

# Keep only valid records
df = df[~invalid].copy()

# Set correct data types
df["Order_ID"] = df["Order_ID"].astype(int)
df["Amount"] = df["Amount"].astype(float)
df["Quantity"] = df["Quantity"].astype(int)

# Format dates
df["Order_Date"] = df["Order_Date"].dt.strftime("%Y-%m-%d")

# Save cleaned dataset
df.to_csv("cleaned_data.csv", index=False)

# 7. Generate quality report
missing_after = int(df.isnull().sum().sum())
duplicates_removed = original_rows - (
    len(df) + len(rejected)
)

with open("quality_report.txt", "w") as file:
    file.write("DATA CLEANING QUALITY REPORT\n")
    file.write("----------------------------\n")
    file.write(f"Original Records: {original_rows}\n")
    file.write(f"Cleaned Records: {len(df)}\n")
    file.write(f"Rejected Records: {len(rejected)}\n")
    file.write(f"Duplicates Removed: {duplicates_removed}\n")
    file.write(f"Missing Values Before: {missing_before}\n")
    file.write(f"Missing Values After: {missing_after}\n")

print("\nData Cleaning Completed!")
print("Original Records:", original_rows)
print("Cleaned Records:", len(df))
print("Rejected Records:", len(rejected))
print("Duplicates Removed:", duplicates_removed)

print("\nCleaned Data:")
print(df)

print("\nAll output files created successfully!")
