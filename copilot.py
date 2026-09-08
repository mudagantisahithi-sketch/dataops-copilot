import subprocess
import os
import sys
import shutil
import json
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.join(BASE_DIR, "data")
STATUS_FILE = os.path.join(BASE_DIR, "pipeline_status.json")
CLEANED_FILE = os.path.join(DATA_FOLDER, "customers_cleaned.csv")

os.makedirs(DATA_FOLDER, exist_ok=True)


def update_status(
    status,
    stage,
    message,
    score=None,
    input_file=None,
    rows=None,
    error=None
):
    data = {
        "status": status,
        "stage": stage,
        "message": message,
        "score": score,
        "input_file": input_file,
        "rows": rows,
        "error": error,
        "updated_at": datetime.now().isoformat()
    }

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def run_command(command):

    print("\n" + "=" * 60)
    print("Running:", command)
    print("=" * 60)

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    return result


def extract_quality(output):

    score = 0.0
    missing_ids = 0
    duplicate_groups = 0
    missing_emails = 0
    rows = 0

    for line in output.splitlines():

        if "Rows checked:" in line:
            try:
                rows = int(
                    line.split(":")[1]
                    .strip()
                    .replace(",", "")
                )
            except:
                pass

        if "QUALITY SCORE:" in line:
            try:
                score = float(
                    line.split(":")[1]
                    .replace("%", "")
                    .strip()
                )
            except:
                pass

        match = re.search(
            r"(\d[\d,]*) missing customer IDs",
            line
        )

        if match:
            try:
                missing_ids = int(
                    match.group(1).replace(",", "")
                )
            except:
                pass

        match = re.search(
            r"(\d[\d,]*) duplicate customer ID groups",
            line
        )

        if match:
            try:
                duplicate_groups = int(
                    match.group(1).replace(",", "")
                )
            except:
                pass

        match = re.search(
            r"(\d[\d,]*) missing emails",
            line
        )

        if match:
            try:
                missing_emails = int(
                    match.group(1).replace(",", "")
                )
            except:
                pass

    return (
        score,
        missing_ids,
        duplicate_groups,
        missing_emails,
        rows
    )


def main():

    print("=" * 60)
    print("          DATAOPS COPILOT")
    print("=" * 60)

    if len(sys.argv) < 2:

        print("ERROR: No incoming CSV file provided.")

        update_status(
            "ERROR",
            "ERROR",
            "No incoming CSV file provided",
            error="Missing input file"
        )

        return

    incoming_file = sys.argv[1]

    print()
    print("Incoming file:")
    print(incoming_file)

    if not os.path.exists(incoming_file):

        print("ERROR: Incoming file not found.")

        update_status(
            "ERROR",
            "ERROR",
            "Incoming file not found",
            input_file=incoming_file,
            error="File does not exist"
        )

        return

    update_status(
        "RUNNING",
        "FILE_DETECTED",
        "New dataset detected",
        input_file=os.path.basename(incoming_file)
    )

    print()
    print("Input dataset found.")

    input_file = os.path.join(
        DATA_FOLDER,
        os.path.basename(incoming_file)
    )

    update_status(
        "RUNNING",
        "COPYING",
        "Copying incoming dataset",
        input_file=os.path.basename(incoming_file)
    )

    shutil.copy2(
        incoming_file,
        input_file
    )

    print()
    print("Input file copied to:")
    print(input_file)

    update_status(
        "RUNNING",
        "QUALITY_CHECK",
        "Running initial data quality checks",
        input_file=os.path.basename(incoming_file)
    )

    print()
    print("Running initial quality check...")

    quality_command = (
        f'"{sys.executable}" '
        f'"{os.path.join(BASE_DIR, "quality_checks.py")}" '
        f'"{input_file}"'
    )

    quality_result = run_command(
        quality_command
    )

    (
        score,
        missing_ids,
        duplicate_groups,
        missing_emails,
        rows
    ) = extract_quality(
        quality_result.stdout
    )

    update_status(
        "RUNNING",
        "QUALITY_CHECK_COMPLETE",
        f"Initial quality check completed: {score:.2f}%",
        score=score,
        input_file=os.path.basename(incoming_file),
        rows=rows
    )

    if score < 100:

        update_status(
            "RUNNING",
            "REPAIRING",
            f"Repairing {missing_ids:,} missing customer IDs",
            score=score,
            input_file=os.path.basename(incoming_file),
            rows=rows
        )

        print()
        print("Running automatic data repair...")

        fix_command = (
            f'"{sys.executable}" '
            f'"{os.path.join(BASE_DIR, "fix_data.py")}" '
            f'"{input_file}" '
            f'"{CLEANED_FILE}"'
        )

        fix_result = run_command(
            fix_command
        )

        if fix_result.returncode != 0:

            update_status(
                "ERROR",
                "REPAIR_FAILED",
                "Automatic data repair failed",
                score=score,
                input_file=os.path.basename(incoming_file),
                rows=rows,
                error=fix_result.stderr
            )

            return

    else:

        print()
        print("No repair required.")

        shutil.copy2(
            input_file,
            CLEANED_FILE
        )

    if not os.path.exists(CLEANED_FILE):

        update_status(
            "ERROR",
            "REPAIR_FAILED",
            "Cleaned dataset was not created",
            score=score,
            input_file=os.path.basename(incoming_file),
            rows=rows,
            error="customers_cleaned.csv not found"
        )

        return

    print()
    print("Cleaned dataset created.")

    update_status(
        "RUNNING",
        "FINAL_QUALITY_CHECK",
        "Running final quality validation",
        score=score,
        input_file=os.path.basename(incoming_file),
        rows=rows
    )

    print()
    print("Running final quality check...")

    final_command = (
        f'"{sys.executable}" '
        f'"{os.path.join(BASE_DIR, "quality_checks.py")}" '
        f'"{CLEANED_FILE}"'
    )

    final_result = run_command(
        final_command
    )

    (
        final_score,
        final_missing_ids,
        final_duplicates,
        final_missing_emails,
        final_rows
    ) = extract_quality(
        final_result.stdout
    )

    if final_score == 100:

        update_status(
            "PASSED",
            "COMPLETED",
            "Pipeline completed successfully",
            score=final_score,
            input_file=os.path.basename(incoming_file),
            rows=final_rows
        )

        print()
        print("=" * 60)
        print("          COPILOT RUN COMPLETE")
        print("=" * 60)
        print("Pipeline finished successfully.")

    else:

        update_status(
            "FAILED",
            "COMPLETED",
            "Pipeline completed with data quality issues",
            score=final_score,
            input_file=os.path.basename(incoming_file),
            rows=final_rows
        )

        print()
        print("=" * 60)
        print("          COPILOT RUN COMPLETE")
        print("=" * 60)
        print("Pipeline finished with quality issues.")


if __name__ == "__main__":
    main()
