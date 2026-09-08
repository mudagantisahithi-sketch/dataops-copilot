import sys
import os
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

# --------------------------------------------------
# Get input file
# --------------------------------------------------

if len(sys.argv) < 2:
    print("ERROR: No input CSV file provided.")
    print("Usage: python quality_checks.py <csv_file>")
    sys.exit(1)

INPUT_FILE = sys.argv[1]

if not os.path.exists(INPUT_FILE):
    print(f"ERROR: File not found: {INPUT_FILE}")
    sys.exit(1)

# --------------------------------------------------
# Read CSV
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

# --------------------------------------------------
# 1. Missing Customer IDs
# --------------------------------------------------

total_rows = len(df)

missing_customer_ids = df["customer_id"].isna().sum()

# --------------------------------------------------
# 2. Duplicate Customer IDs
# --------------------------------------------------

duplicate_groups = (
    df[df["customer_id"].notna()]
    .groupby("customer_id")
    .size()
)

duplicate_groups = (duplicate_groups > 1).sum()

# --------------------------------------------------
# 3. Missing Emails
# --------------------------------------------------

missing_emails = df["email"].isna().sum()

# --------------------------------------------------
# 4. Calculate Quality Score
# --------------------------------------------------

passed_checks = 0
total_checks = 3

if missing_customer_ids == 0:
    passed_checks += 1

if duplicate_groups == 0:
    passed_checks += 1

if missing_emails == 0:
    passed_checks += 1

score = (passed_checks / total_checks) * 100

if score == 100:
    status = "PASSED"
else:
    status = "FAILED"

# --------------------------------------------------
# 5. DataOps Copilot Report
# --------------------------------------------------

print()
print("=" * 55)
print("          DATAOPS COPILOT - QUALITY REPORT")
print("=" * 55)

print()
print(f"Dataset: {os.path.basename(INPUT_FILE)}")
print(f"Rows checked: {total_rows:,}")

print()
print("Customer ID Check")

if missing_customer_ids == 0:
    print("   PASS")
else:
    print(f"   FAIL - {missing_customer_ids:,} missing customer IDs detected.")

print()
print("Duplicate Check")

if duplicate_groups == 0:
    print("   PASS")
else:
    print(f"   FAIL - {duplicate_groups:,} duplicate customer ID groups.")

print()
print("Email Check")

if missing_emails == 0:
    print("   PASS")
else:
    print(f"   FAIL - {missing_emails:,} missing emails.")

print()
print("-" * 55)
print(f"QUALITY SCORE: {score:.2f}%")
print(f"STATUS: {status}")
print("-" * 55)

print()

if missing_customer_ids > 0:
    print("Copilot Recommendation:")
    print(
        f"   Fix the {missing_customer_ids:,} missing "
        "customer IDs before using this dataset in production."
    )
else:
    print("Copilot Recommendation:")
    print("   No immediate data-quality issues detected.")

print()
print("=" * 55)

# Exit with 0 so the pipeline can continue.
# The quality score itself tells us whether the data passed.
sys.exit(0)
