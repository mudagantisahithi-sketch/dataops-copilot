import time
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INCOMING_DIR = BASE_DIR / "incoming"
COPILOT = BASE_DIR / "copilot.py"

INCOMING_DIR.mkdir(exist_ok=True)

PYTHON = sys.executable

processed_files = {}


def get_file_signature(file):
    try:
        stat = file.stat()
        return (stat.st_size, stat.st_mtime_ns)
    except FileNotFoundError:
        return None


def process_file(file):
    print()
    print("=" * 60)
    print("🚨 NEW DATASET DETECTED")
    print("=" * 60)
    print(f"File: {file.name}")
    print(f"Size: {file.stat().st_size / (1024 * 1024):.2f} MB")
    print()
    print("▶ Starting DataOps Copilot...")
    print("=" * 60)

    try:
        result = subprocess.run(
            [
                PYTHON,
                str(COPILOT),
                str(file)
            ],
            cwd=BASE_DIR,
            text=True
        )

        print()
        print("=" * 60)

        if result.returncode == 0:
            print("✅ COPILOT PIPELINE COMPLETED")
        else:
            print("❌ COPILOT PIPELINE FAILED")

        print("=" * 60)

    except Exception as e:
        print()
        print("❌ PIPELINE ERROR")
        print(e)


def scan():
    csv_files = list(INCOMING_DIR.glob("*.csv"))

    for file in csv_files:

        signature = get_file_signature(file)

        if signature is None:
            continue

        old_signature = processed_files.get(str(file))

        if old_signature == signature:
            continue

        # Wait until file stops changing.
        time.sleep(1)

        new_signature = get_file_signature(file)

        if new_signature != signature:
            continue

        processed_files[str(file)] = signature

        process_file(file)


print("=" * 60)
print("       DATAOPS COPILOT - REAL-TIME PIPELINE")
print("=" * 60)
print()
print(f"Watching: {INCOMING_DIR}")
print("Polling interval: 2 seconds")
print()
print("Waiting for CSV files...")
print("Press Ctrl+C to stop.")
print()


try:

    while True:

        scan()

        time.sleep(2)

except KeyboardInterrupt:

    print()
    print("=" * 60)
    print("REAL-TIME MONITOR STOPPED")
    print("=" * 60)
