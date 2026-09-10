from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


DATA_DIR = Path("data")
REPORT_DIR = Path("reports")


def load_incident_data(
    file_name: str = "customers_incident.csv",
) -> pd.DataFrame:
    """Load the incident dataset."""

    path = DATA_DIR / file_name

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    return pd.read_csv(path)


def inspect_schema(
    file_name: str = "customers_incident.csv",
) -> dict[str, Any]:
    """Inspect the incoming dataset schema."""

    df = load_incident_data(file_name)

    expected_columns = [
        "customer_id",
        "customer_name",
        "email",
        "country",
        "signup_date",
        "ingested_at",
    ]

    actual_columns = list(df.columns)

    added = [
        column
        for column in actual_columns
        if column not in expected_columns
    ]

    missing = [
        column
        for column in expected_columns
        if column not in actual_columns
    ]

    return {
        "expected_columns": expected_columns,
        "actual_columns": actual_columns,
        "unexpected_columns": added,
        "missing_columns": missing,
        "schema_changed": bool(
            added or missing
        ),
    }


def inspect_quality(
    file_name: str = "customers_incident.csv",
) -> dict[str, Any]:
    """Perform detailed investigation checks."""

    df = load_incident_data(file_name)

    expected_rows = 1000
    actual_rows = len(df)

    null_customer_ids = int(
        df["customer_id"].isna().sum()
    )

    duplicate_customer_ids = int(
        df.duplicated(
            subset=["customer_id"],
            keep=False,
        ).sum()
    )

    invalid_emails = int(
        (
            ~df["email"]
            .astype("string")
            .str.contains(
                "@",
                na=False,
            )
        ).sum()
    )

    return {
        "expected_rows": expected_rows,
        "actual_rows": actual_rows,
        "volume_drop": expected_rows - actual_rows,
        "volume_drop_percent": round(
            (
                (expected_rows - actual_rows)
                / expected_rows
            )
            * 100,
            2,
        ),
        "null_customer_ids": null_customer_ids,
        "duplicate_customer_ids": duplicate_customer_ids,
        "invalid_emails": invalid_emails,
    }


def investigate_incident() -> dict[str, Any]:
    """
    Produce a complete evidence package
    for the Gemini investigation agent.
    """

    schema = inspect_schema()
    quality = inspect_quality()

    evidence = {
        "incident_type": "DATA_QUALITY",
        "dataset": "customers_incident.csv",
        "schema": schema,
        "quality": quality,
        "observations": [
            (
                "The pipeline processed significantly "
                "fewer records than the healthy baseline."
            ),
            (
                "A large number of customer IDs are NULL."
            ),
            (
                "Duplicate customer records are present."
            ),
            (
                "Invalid email addresses are present."
            ),
            (
                "An unexpected phone_number column "
                "was introduced."
            ),
        ],
    }

    return evidence


def save_evidence(
    evidence: dict[str, Any],
) -> Path:
    """Save evidence for auditing."""

    REPORT_DIR.mkdir(exist_ok=True)

    path = (
        REPORT_DIR
        / "investigation_evidence.json"
    )

    path.write_text(
        json.dumps(
            evidence,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    return path
