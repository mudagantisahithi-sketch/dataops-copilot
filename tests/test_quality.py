import pandas as pd

from dataops.quality import (
    check_duplicates,
    check_nulls,
    check_row_count,
    check_schema_drift,
    quality_summary,
    run_quality_checks,
)


def test_null_detection():
    df = pd.DataFrame({
        "customer_id": ["C1", "C2", None, None],
    })

    result = check_nulls(df, "customer_id", threshold=0.01)

    assert result["status"] == "FAIL"


def test_duplicate_detection():
    df = pd.DataFrame({
        "customer_id": ["C1", "C1", "C2"],
    })

    result = check_duplicates(df, ["customer_id"])

    assert result["status"] == "FAIL"


def test_row_count_drop():
    result = check_row_count(
        current_rows=7000,
        previous_rows=10000,
    )

    assert result["status"] == "FAIL"


def test_schema_drift():
    result = check_schema_drift(
        ["customer_id", "name", "email", "phone"],
        ["customer_id", "name", "email"],
    )

    assert result["status"] == "FAIL"


def test_healthy_dataset():
    df = pd.DataFrame({
        "customer_id": ["C1", "C2", "C3"],
        "name": ["A", "B", "C"],
        "email": [
            "a@example.com",
            "b@example.com",
            "c@example.com",
        ],
        "created_at": pd.Timestamp.now(tz="UTC"),
    })

    results = run_quality_checks(df)

    summary = quality_summary(results)

    assert summary["healthy"] is True
