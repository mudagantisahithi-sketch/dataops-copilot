import sys
sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd
import re

INPUT_FILE = "data/customers_bad_nulls.csv"
OUTPUT_FILE = "data/customers_cleaned.csv"

# Read the bad dataset
df = pd.read_csv(INPUT_FILE)

print("=== DATA CLEANING ===")
print(f"Rows before cleaning: {len(df)}")

# Find missing customer IDs
missing_ids = df["customer_id"].isna()

print(f"Missing customer IDs found: {missing_ids.sum()}")

# Get existing customer IDs
existing_ids = set(
    df["customer_id"].dropna().astype(str)
)

# Find the highest existing numeric ID
numbers = []

for customer_id in existing_ids:
    match = re.search(r"(\d+)$", customer_id)

    if match:
        numbers.append(int(match.group(1)))

next_number = max(numbers) + 1

# Fill missing IDs
for index in df[missing_ids].index:

    new_id = f"CUST{next_number:05d}"

    while new_id in existing_ids:
        next_number += 1
        new_id = f"CUST{next_number:05d}"

    df.loc[index, "customer_id"] = new_id

    existing_ids.add(new_id)
    next_number += 1

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print(f"Rows after cleaning: {len(df)}")
print(f"Cleaned dataset saved to: {OUTPUT_FILE}")
print("✅ Missing customer IDs fixed!")
