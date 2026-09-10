import pandas as pd
import random
from datetime import datetime, timedelta

NUM_CUSTOMERS = 1000

countries = ["India", "USA", "UK", "Canada", "Australia"]

customers = []

for i in range(1, NUM_CUSTOMERS + 1):
    signup_date = datetime.now() - timedelta(days=random.randint(1, 1000))

    customers.append({
        "customer_id": f"CUST{i:05d}",
        "customer_name": f"Customer {i}",
        "email": f"customer{i}@example.com",
        "country": random.choice(countries),
        "signup_date": signup_date.strftime("%Y-%m-%d")
    })

df = pd.DataFrame(customers)

output_file = "data/customers.csv"

df.to_csv(output_file, index=False)

print(f"Created {len(df)} customers")
print(f"Saved to {output_file}")
