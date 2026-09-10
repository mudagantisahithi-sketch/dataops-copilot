from pathlib import Path
from datetime import datetime, timedelta
import random

import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)


# Configuration
NUM_CUSTOMERS = 1000

COUNTRIES = [
    "India",
    "USA",
    "UK",
    "Canada",
    "Australia",
]


def generate_healthy():
    """
    Generate the baseline healthy customer dataset.

    This represents a successful pipeline run.
    """

    random.seed(42)

    customers = []

    for i in range(1, NUM_CUSTOMERS + 1):

        # Historical customer signup date
        signup_date = datetime.now() - timedelta(
            days=random.randint(1, 1000)
        )

        # Current pipeline ingestion timestamp
        ingested_at = datetime.now()

        customers.append(
            {
                "customer_id": f"CUST{i:05d}",
                "customer_name": f"Customer {i}",
                "email": f"customer{i}@example.com",
                "country": random.choice(COUNTRIES),
                "signup_date": signup_date.strftime("%Y-%m-%d"),
                "ingested_at": ingested_at.isoformat(),
            }
        )

    df = pd.DataFrame(customers)

    path = DATA_DIR / "customers_healthy.csv"

    df.to_csv(
        path,
        index=False,
    )

    return df, path


def generate_null_spike(df):
    """
    Scenario 1:
    Introduce a large number of NULL customer IDs.
    """

    bad = df.copy()

    # First 100 customer IDs become NULL
    bad.loc[0:99, "customer_id"] = None

    path = DATA_DIR / "customers_bad_nulls.csv"

    bad.to_csv(
        path,
        index=False,
    )

    return bad, path


def generate_duplicates(df):
    """
    Scenario 2:
    Introduce duplicate customer records.
    """

    bad = df.copy()

    # Duplicate the first 100 records
    duplicates = bad.iloc[0:100].copy()

    bad = pd.concat(
        [
            bad,
            duplicates,
        ],
        ignore_index=True,
    )

    path = DATA_DIR / "customers_bad_duplicates.csv"

    bad.to_csv(
        path,
        index=False,
    )

    return bad, path


def generate_volume_drop(df):
    """
    Scenario 3:
    Simulate a pipeline processing significantly fewer rows.
    """

    # Keep only 650 of the original 1000 records
    bad = df.iloc[:650].copy()

    path = DATA_DIR / "customers_bad_volume.csv"

    bad.to_csv(
        path,
        index=False,
    )

    return bad, path


def generate_schema_drift(df):
    """
    Scenario 4:
    Introduce an unexpected column.
    """

    bad = df.copy()

    bad["phone_number"] = [
        f"+91-90000-{i:04d}"
        for i in range(len(bad))
    ]

    path = DATA_DIR / "customers_bad_schema.csv"

    bad.to_csv(
        path,
        index=False,
    )

    return bad, path


def generate_business_rule_failure(df):
    """
    Scenario 5:
    Introduce invalid email addresses.
    """

    bad = df.copy()

    # Make 50 email addresses invalid
    for i in range(50):
        bad.loc[i, "email"] = "invalid-email"

    path = DATA_DIR / "customers_bad_business.csv"

    bad.to_csv(
        path,
        index=False,
    )

    return bad, path


def generate_combined_incident(df):
    """
    Main DataOps Copilot demo scenario.

    Combines several problems into one realistic incident:
    - volume drop
    - NULL customer IDs
    - invalid emails
    - duplicate records
    - schema drift
    """

    bad = df.copy()

    # ---------------------------------------------------------
    # 1. Volume drop
    # ---------------------------------------------------------

    bad = bad.iloc[:650].copy()

    # ---------------------------------------------------------
    # 2. NULL customer IDs
    # ---------------------------------------------------------

    bad.loc[0:64, "customer_id"] = None

    # ---------------------------------------------------------
    # 3. Invalid email addresses
    # ---------------------------------------------------------

    for i in range(65, 100):
        bad.loc[i, "email"] = "invalid-email"

    # ---------------------------------------------------------
    # 4. Duplicate records
    # ---------------------------------------------------------

    duplicates = bad.iloc[100:150].copy()

    bad = pd.concat(
        [
            bad,
            duplicates,
        ],
        ignore_index=True,
    )

    # ---------------------------------------------------------
    # 5. Schema drift
    # ---------------------------------------------------------

    bad["phone_number"] = [
        f"+91-90000-{i:04d}"
        for i in range(len(bad))
    ]

    path = DATA_DIR / "customers_incident.csv"

    bad.to_csv(
        path,
        index=False,
    )

    return bad, path


def print_scenario_details(
    name,
    df,
    path,
):
    """
    Print useful information about a generated scenario.
    """

    print()
    print("-" * 60)
    print(f"Scenario: {name}")
    print(f"File: {path.name}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {list(df.columns)}")

    if "customer_id" in df.columns:

        null_count = int(
            df["customer_id"].isna().sum()
        )

        print(
            f"NULL customer IDs: {null_count:,}"
        )

        duplicate_count = int(
            df.duplicated(
                subset=["customer_id"],
                keep=False,
            ).sum()
        )

        print(
            f"Duplicate customer records: {duplicate_count:,}"
        )

    if "email" in df.columns:

        invalid_email_count = int(
            (
                ~df["email"]
                .astype("string")
                .str.contains(
                    "@",
                    na=False,
                )
            ).sum()
        )

        print(
            f"Invalid emails: {invalid_email_count:,}"
        )


def main():

    print()
    print("=" * 70)
    print("DATAOPS COPILOT - SYNTHETIC DATA GENERATOR")
    print("=" * 70)

    # ---------------------------------------------------------
    # Generate healthy baseline
    # ---------------------------------------------------------

    healthy, healthy_path = generate_healthy()

    print()
    print("Healthy baseline created")
    print(f"File: {healthy_path}")
    print(f"Rows: {len(healthy):,}")
    print(f"Columns: {list(healthy.columns)}")

    # ---------------------------------------------------------
    # Generate individual failure scenarios
    # ---------------------------------------------------------

    scenarios = [
        (
            "NULL spike",
            generate_null_spike,
        ),
        (
            "Duplicate records",
            generate_duplicates,
        ),
        (
            "Volume drop",
            generate_volume_drop,
        ),
        (
            "Schema drift",
            generate_schema_drift,
        ),
        (
            "Business rule failure",
            generate_business_rule_failure,
        ),
    ]

    for name, generator in scenarios:

        bad, path = generator(healthy)

        print_scenario_details(
            name,
            bad,
            path,
        )

    # ---------------------------------------------------------
    # Generate main combined incident
    # ---------------------------------------------------------

    incident, incident_path = generate_combined_incident(
        healthy
    )

    print_scenario_details(
        "COMBINED PIPELINE INCIDENT",
        incident,
        incident_path,
    )

    # ---------------------------------------------------------
    # Final message
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("SYNTHETIC DATA GENERATION COMPLETE")
    print("=" * 70)

    print()
    print("Generated files:")

    for file in sorted(DATA_DIR.glob("customers_*.csv")):
        print(f"  - {file.name}")

    print()
    print("Main demo file:")
    print(f"  {incident_path}")

    print()
    print("The combined incident contains:")
    print("  [FAIL] Volume drop")
    print("  [FAIL] NULL customer IDs")
    print("  [FAIL] Duplicate records")
    print("  [FAIL] Invalid email addresses")
    print("  [FAIL] Schema drift")

    print()
    print("Ready for DataOps Copilot investigation.")


if __name__ == "__main__":
    main()
