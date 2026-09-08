import pandas as pd

# Read the healthy customer data
input_file = "data/customers.csv"

df = pd.read_csv(input_file)

# Introduce a data-quality problem:
# Make 100 customer IDs NULL
df.loc[0:99, "customer_id"] = None

# Save the faulty dataset
output_file = "data/customers_bad_nulls.csv"

df.to_csv(output_file, index=False)

print("Bad dataset created!")
print(f"Saved to: {output_file}")
print(f"Total rows: {len(df)}")
print(f"Missing customer IDs: {df['customer_id'].isnull().sum()}")
