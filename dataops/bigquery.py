from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from google.cloud import bigquery


PROJECT_ID = "project-0212c7fc-1c9b-45a7-abc"

RAW_DATASET = "dataops_raw"
MONITORING_DATASET = "dataops_monitoring"

client = bigquery.Client(project=PROJECT_ID)


def generate_run_id() -> str:
    """Create a unique pipeline run ID."""
    return f"run-{uuid.uuid4().hex[:12]}"


def generate_incident_id() -> str:
    """Create a unique incident ID."""
    return f"INC-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"


def get_customer_count() -> int:
    """Return current customer row count."""

    query = f"""
        SELECT COUNT(*) AS row_count
        FROM `{PROJECT_ID}.{RAW_DATASET}.customers`
    """

    rows = list(client.query(query).result())

    return int(rows[0].row_count)


def get_customer_schema() -> list[str]:
    """Return column names from the BigQuery customer table."""

    table_ref = f"{PROJECT_ID}.{RAW_DATASET}.customers"

    table = client.get_table(table_ref)

    return [
        field.name
        for field in table.schema
    ]


def get_recent_customers(limit: int = 20) -> list[dict[str, Any]]:
    """Retrieve recent customer records for investigation."""

    query = f"""
        SELECT
            customer_id,
            customer_name,
            email,
            country,
            signup_date,
            ingested_at
        FROM `{PROJECT_ID}.{RAW_DATASET}.customers`
        ORDER BY ingested_at DESC
        LIMIT {limit}
    """

    rows = client.query(query).result()

    return [
        dict(row.items())
        for row in rows
    ]


def run_query(query: str) -> list[dict[str, Any]]:
    """
    Controlled BigQuery query helper.

    The agent will eventually use this through MCP Toolbox.
    """

    rows = client.query(query).result()

    return [
        dict(row.items())
        for row in rows
    ]
