import pandas as pd

file = "data/customers.csv"

df = pd.read_csv(file)

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- COLUMNS ---")
print(df.columns.tolist())

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- TOTAL ROWS ---")
print(len(df))
