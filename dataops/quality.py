"""
DataOps Copilot - Deterministic Data Quality Engine

AI should investigate detected problems, not invent them.
This module performs deterministic checks for:
- NULL spikes
- duplicates
- row-count anomalies
- freshness
- schema drift
- business-rule violations
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd


def _result(
    check_type: str,
    status: str,
    metric_name: str,
    metric_value: float,
    threshold: float,
    message: str,
) -> dict[str, Any]:
    return {
        "check_type": check_type,
        "status": status,
        "metric_name": metric_name,
        "metric_value": round(float(metric_value), 4),
        "threshold": threshold,
        "message": message,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def check_nulls(
    df: pd.DataFrame,
    column: str,
    threshold: float = 0.01,
) -> dict[str, Any]:
    """Detect an excessive NULL/blank rate."""

    if column not in df.columns:
        return _result(
            "NULL_CHECK",
            "FAIL",
            f"{column}_null_rate",
            1.0,
            threshold,
            f"Required column '{column}' is missing.",
        )

    null_rate = df[column].isna().mean()

    # Treat empty strings as missing too.
    if df[column].dtype == "object":
        null_rate = max(
            null_rate,
            (df[column].astype("string").str.strip() == "").mean(),
        )

    status = "FAIL" if null_rate > threshold else "PASS"

    return _result(
        "NULL_CHECK",
        status,
        f"{column}_null_rate",
        null_rate,
        threshold,
        (
            f"{column} NULL rate is {null_rate:.2%}, "
            f"threshold is {threshold:.2%}."
        ),
    )


def check_duplicates(
    df: pd.DataFrame,
    key_columns: list[str],
    threshold: float = 0.01,
) -> dict[str, Any]:
    """Detect duplicate business keys."""

    missing = [c for c in key_columns if c not in df.columns]

    if missing:
        return _result(
            "DUPLICATE_CHECK",
            "FAIL",
            "duplicate_rate",
            1.0,
            threshold,
            f"Key columns missing: {missing}",
        )

    duplicate_rate = (
        df.duplicated(subset=key_columns, keep=False).mean()
        if len(df)
        else 0.0
    )

    status = "FAIL" if duplicate_rate > threshold else "PASS"

    duplicate_count = int(
        df.duplicated(subset=key_columns, keep=False).sum()
    )

    return _result(
        "DUPLICATE_CHECK",
        status,
        "duplicate_rate",
        duplicate_rate,
        threshold,
        (
            f"{duplicate_count} records participate in duplicate keys. "
            f"Duplicate rate is {duplicate_rate:.2%}."
        ),
    )


def check_row_count(
    current_rows: int,
    previous_rows: int,
    drop_threshold: float = 0.20,
) -> dict[str, Any]:
    """Detect unusually large row-count changes."""

    if previous_rows <= 0:
        return _result(
            "ROW_COUNT_CHECK",
            "PASS",
            "row_count_change",
            0.0,
            drop_threshold,
            "No previous row count available for comparison.",
        )

    change = (current_rows - previous_rows) / previous_rows

    status = "FAIL" if change < -drop_threshold else "PASS"

    return _result(
        "ROW_COUNT_CHECK",
        status,
        "row_count_change",
        change,
        -drop_threshold,
        (
            f"Row count changed from {previous_rows:,} to "
            f"{current_rows:,} ({change:+.2%})."
        ),
    )


def check_freshness(
    df: pd.DataFrame,
    timestamp_column: str,
    max_age_hours: float = 24,
) -> dict[str, Any]:
    """Detect stale data using the newest timestamp."""

    if timestamp_column not in df.columns:
        return _result(
            "FRESHNESS_CHECK",
            "FAIL",
            "data_age_hours",
            float("inf"),
            max_age_hours,
            f"Timestamp column '{timestamp_column}' is missing.",
        )

    timestamps = pd.to_datetime(
        df[timestamp_column],
        errors="coerce",
        utc=True,
    ).dropna()

    if timestamps.empty:
        return _result(
            "FRESHNESS_CHECK",
            "FAIL",
            "data_age_hours",
            float("inf"),
            max_age_hours,
            "No valid timestamps were found.",
        )

    newest = timestamps.max()
    now = pd.Timestamp.now(tz="UTC")
    age_hours = max(0.0, (now - newest).total_seconds() / 3600)

    status = "FAIL" if age_hours > max_age_hours else "PASS"

    return _result(
        "FRESHNESS_CHECK",
        status,
        "data_age_hours",
        age_hours,
        max_age_hours,
        (
            f"Newest record is {age_hours:.2f} hours old. "
            f"Maximum allowed age is {max_age_hours:.2f} hours."
        ),
    )


def check_schema_drift(
    current_columns: list[str],
    previous_columns: list[str],
) -> dict[str, Any]:
    """Compare the current schema with the previous successful schema."""

    current = set(current_columns)
    previous = set(previous_columns)

    added = sorted(current - previous)
    removed = sorted(previous - current)

    drift = bool(added or removed)

    status = "FAIL" if drift else "PASS"

    return _result(
        "SCHEMA_DRIFT_CHECK",
        status,
        "schema_changed",
        1.0 if drift else 0.0,
        0.0,
        (
            f"Schema drift detected. Added columns: {added}; "
            f"removed columns: {removed}."
            if drift
            else "Schema matches the previous successful run."
        ),
    )


def check_business_rules(
    df: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Run simple business validity checks."""

    results = []

    if "email" in df.columns:
        invalid_email = (
            ~df["email"]
            .astype("string")
            .str.contains("@", na=False)
        ).mean()

        results.append(
            _result(
                "BUSINESS_RULE_CHECK",
                "FAIL" if invalid_email > 0.01 else "PASS",
                "invalid_email_rate",
                invalid_email,
                0.01,
                f"Invalid email rate is {invalid_email:.2%}.",
            )
        )

    if "customer_id" in df.columns:
        blank_ids = (
            df["customer_id"].isna()
            | (
                df["customer_id"]
                .astype("string")
                .str.strip()
                .eq("")
            )
        ).mean()

        results.append(
            _result(
                "BUSINESS_RULE_CHECK",
                "FAIL" if blank_ids > 0.01 else "PASS",
                "invalid_customer_id_rate",
                blank_ids,
                0.01,
                f"Invalid customer ID rate is {blank_ids:.2%}.",
            )
        )

    return results


def run_quality_checks(
    df: pd.DataFrame,
    previous_rows: int | None = None,
    previous_columns: list[str] | None = None,
    timestamp_column: str = "signup_date",
) -> list[dict[str, Any]]:
    """
    Run the complete deterministic quality suite.

    Returns machine-readable quality results that can be stored
    in BigQuery and supplied to the AI investigator as evidence.
    """

    results = []

    if "customer_id" in df.columns:
        results.append(check_nulls(df, "customer_id"))
        results.append(check_duplicates(df, ["customer_id"]))

    if previous_rows is not None:
        results.append(
            check_row_count(
                len(df),
                previous_rows,
            )
        )

    results.append(
        check_freshness(
            df,
            timestamp_column,
        )
    )

    if previous_columns is not None:
        results.append(
            check_schema_drift(
                list(df.columns),
                previous_columns,
            )
        )

    results.extend(check_business_rules(df))

    return results


def quality_summary(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """Create a dashboard-friendly summary."""

    failed = [
        result for result in results
        if result["status"] == "FAIL"
    ]

    passed = [
        result for result in results
        if result["status"] == "PASS"
    ]

    score = (
        len(passed) / len(results) * 100
        if results
        else 100.0
    )

    if len(failed) >= 3:
        severity = "CRITICAL"
    elif len(failed) >= 2:
        severity = "HIGH"
    elif len(failed) == 1:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "total_checks": len(results),
        "passed": len(passed),
        "failed": len(failed),
        "quality_score": round(score, 2),
        "severity": severity,
        "healthy": len(failed) == 0,
    }
