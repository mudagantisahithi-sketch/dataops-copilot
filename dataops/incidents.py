from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


def create_incident(
    run_id: str,
    quality_results: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Convert failed quality checks into a DataOps incident.

    Deterministic quality checks provide the evidence.
    The Gemini/ADK agent will investigate the evidence later.
    """

    failures = [
        result
        for result in quality_results
        if result.get("status") == "FAIL"
    ]

    # No failures = no incident
    if not failures:
        return {
            "incident_created": False,
            "message": "No quality failures detected.",
        }

    # Generate incident ID
    incident_id = (
        f"INC-{uuid.uuid4().hex[:10].upper()}"
    )

    # Determine severity
    if len(failures) >= 4:
        severity = "CRITICAL"
    elif len(failures) >= 3:
        severity = "HIGH"
    elif len(failures) == 2:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    # Get failed check names
    check_names = [
        str(failure.get("check_type", "Unknown"))
        for failure in failures
    ]

    title = (
        "Customer pipeline data-quality incident: "
        + ", ".join(check_names)
    )

    # Create incident
    incident = {
        "incident_id": incident_id,
        "run_id": run_id,
        "severity": severity,
        "status": "OPEN",
        "title": title,
        "root_cause": None,
        "impact": None,
        "recommendation": None,
        "failed_checks": failures,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    # Save evidence locally
    report_path = (
        REPORT_DIR / f"{incident_id}.json"
    )

    report_path.write_text(
        json.dumps(
            incident,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    return incident
