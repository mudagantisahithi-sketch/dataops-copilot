from __future__ import annotations

import pandas as pd

from dataops.quality import (
    quality_summary,
    run_quality_checks,
)
from dataops.incidents import create_incident


HEALTHY_FILE = "data/customers_healthy.csv"
INCIDENT_FILE = "data/customers_incident.csv"


EXPECTED_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "country",
    "signup_date",
    "ingested_at",
]


def run_pipeline(file_path: str):

    print()
    print("=" * 70)
    print("DATAOPS COPILOT PIPELINE RUN")
    print("=" * 70)

    print()
    print(f"Input: {file_path}")

    # ---------------------------------------------------------
    # Load data
    # ---------------------------------------------------------

    df = pd.read_csv(file_path)

    print(f"Rows processed: {len(df):,}")

    print()
    print("Columns:")
    for column in df.columns:
        print(f"  - {column}")

    # ---------------------------------------------------------
    # Run deterministic quality checks
    # ---------------------------------------------------------

    results = run_quality_checks(
        df,
        previous_rows=1000,
        previous_columns=EXPECTED_COLUMNS,
        timestamp_column="ingested_at",
    )

    # ---------------------------------------------------------
    # Display checks
    # ---------------------------------------------------------

    print()
    print("QUALITY CHECKS")
    print("-" * 70)

    for result in results:

        icon = (
            "[PASS]"
            if result["status"] == "PASS"
            else "[FAIL]"
        )

        print(
            f"{icon} "
            f"{result['check_type']}: "
            f"{result['message']}"
        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    summary = quality_summary(results)

    print()
    print("QUALITY SUMMARY")
    print("-" * 70)

    print(
        f"Checks: {summary['total_checks']}"
    )

    print(
        f"Passed: {summary['passed']}"
    )

    print(
        f"Failed: {summary['failed']}"
    )

    print(
        f"Quality score: {summary['quality_score']}%"
    )

    print(
        f"Severity: {summary['severity']}"
    )

    # ---------------------------------------------------------
    # Incident
    # ---------------------------------------------------------

    run_id = (
        "run-local-demo"
    )

    incident = create_incident(
        run_id,
        results,
    )

    print()

    if incident.get("incident_created"):

        print("=" * 70)
        print("INCIDENT CREATED")
        print("=" * 70)

        print(
            f"Incident ID: "
            f"{incident['incident_id']}"
        )

        print(
            f"Severity: "
            f"{incident['severity']}"
        )

        print(
            f"Status: "
            f"{incident['status']}"
        )

        print(
            f"Title: "
            f"{incident['title']}"
        )

        print()
        print(
            "Evidence has been saved "
            "to the reports/ directory."
        )

    else:

        print(
            "Pipeline completed successfully. "
            "No incident created."
        )

    return {
        "run_id": run_id,
        "quality_results": results,
        "summary": summary,
        "incident": incident,
    }


if __name__ == "__main__":

    run_pipeline(
        INCIDENT_FILE
    )
