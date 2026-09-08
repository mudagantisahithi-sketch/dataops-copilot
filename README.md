📊 DataOps Copilot
Real-Time Data Quality Monitoring & Automatic Data Repair

DataOps Copilot is an automated data-quality pipeline that detects common problems in incoming CSV datasets, repairs supported issues, validates the cleaned data, and reports the final quality status.

🚀 Live Demo: https://dataops-copilot.streamlit.app/

💻 GitHub: https://github.com/mudagantisahithi-sketch/dataops-copilot

🎯 Project Overview

Modern data pipelines frequently receive datasets containing quality problems such as:

Missing customer IDs
Duplicate customer IDs
Missing email addresses
Other schema and data-quality issues

Manually detecting and fixing these problems can delay downstream processing.

DataOps Copilot automates the workflow:

Detect → Diagnose → Repair → Validate → Report

✨ Key Features
🔍 Automated Data Quality Checks

The pipeline validates:

Customer ID completeness
Duplicate customer IDs
Missing email addresses
Overall quality score
🤖 Automatic Data Repair

When supported data-quality issues are detected, the repair engine automatically processes the dataset.

Example:

100 missing customer IDs
        ↓
Automatic repair
        ↓
100 IDs fixed
        ↓
Final validation
        ↓
100% Quality Score

⚡ Real-Time File Monitoring

The local real-time monitor continuously watches the incoming/ directory.

When a new CSV file arrives:

CSV File
   ↓
Real-Time Detection
   ↓
Initial Quality Check
   ↓
Issue Detection
   ↓
Automatic Repair
   ↓
Final Quality Check
   ↓
Pipeline Status


The latest pipeline state is written to:

pipeline_status.json

📊 Interactive Dashboard

The Streamlit dashboard provides:

CSV dataset upload
Dataset information
Quality score
Missing-ID detection
Duplicate detection
Missing-email detection
Automatic repair status
Final validation
Processing timestamps
Real-time dashboard refresh
🏗️ Architecture
                    ┌──────────────────────┐
                    │     Incoming CSV     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Real-Time Monitor   │
                    │ realtime_monitor.py  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    DataOps Copilot   │
                    │     copilot.py       │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
        ┌──────────────────┐      ┌──────────────────┐
        │ Quality Checks   │      │   Data Repair    │
        │quality_checks.py │      │   fix_data.py    │
        └────────┬─────────┘      └────────┬─────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    ┌──────────────────────┐
                    │  Final Quality Check │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ pipeline_status.json │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Streamlit Dashboard  │
                    │    dashboard.py      │
                    └──────────────────────┘

🧰 Technology Stack
Python
Pandas
Streamlit
CSV data processing
Real-time file monitoring
Git & GitHub
Google BigQuery (planned/extended integration)
📁 Project Structure
dataops-copilot/
│
├── dashboard.py
├── copilot.py
├── realtime_monitor.py
├── quality_checks.py
├── fix_data.py
│
├── generate_data.py
├── create_bad_data.py
├── inspect_data.py
├── hello.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── incoming/
│   └── sample CSV files
│
├── data/
│   └── processed datasets
│
└── reports/
    └── quality reports

🚀 Run Locally
1. Clone the repository
git clone https://github.com/mudagantisahithi-sketch/dataops-copilot.git
cd dataops-copilot

2. Create a virtual environment
python -m venv .venv

3. Activate the environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

4. Install dependencies
pip install -r requirements.txt

▶️ Run the DataOps Pipeline

Run the pipeline directly against a CSV:

python .\copilot.py .\incoming\customers_bad_nulls.csv


The pipeline performs:

Initial quality check
Issue detection
Automatic repair
Final quality check
Status reporting
⚡ Run Real-Time Monitoring

Start the real-time monitor:

python .\realtime_monitor.py


You should see:

DATAOPS COPILOT - REAL-TIME PIPELINE

Watching folder: incoming

Drop a CSV file into the incoming folder.
The pipeline will automatically process new files.


Now place a new CSV file inside:

incoming/


The monitor detects the new file and automatically starts the pipeline.

📊 Run the Dashboard

Start Streamlit:

streamlit run dashboard.py


Open:

http://localhost:8501


The dashboard provides a visual interface for uploading datasets and viewing their quality results.

🧪 Example Result

A test dataset containing 1,000 rows and 100 missing customer IDs produced:

Initial Quality Score: 66.67%

Missing Customer IDs: 100
Duplicate Customer IDs: 0
Missing Emails: 0

STATUS: FAILED


The automatic repair engine then processed the dataset.

Final result:

Final Quality Score: 100.00%

Customer IDs: PASS
Duplicates: PASS
Emails: PASS

STATUS: PASSED


This demonstrates the complete:

Detection
    ↓
Diagnosis
    ↓
Repair
    ↓
Validation
    ↓
Reporting


workflow.

🔄 Real-Time Workflow

The real-time pipeline continuously monitors the incoming directory.

incoming/
    ↓
CSV detected
    ↓
Pipeline started
    ↓
Initial quality check
    ↓
Problems detected
    ↓
Automatic repair
    ↓
Final quality check
    ↓
Status recorded
    ↓
Dashboard updated


Pipeline state is stored in:

pipeline_status.json


Example:

{
    "status": "PASSED",
    "stage": "COMPLETED",
    "message": "Pipeline completed successfully",
    "score": 100.0,
    "input_file": "realtime_testing.csv",
    "rows": 1000
}

🌐 Live Application

Try the deployed Streamlit application:

https://dataops-copilot.streamlit.app/

The application provides a browser-based interface for uploading CSV datasets and viewing data-quality results.

🎥 Demonstration

The project demonstrates:

Opening the DataOps Copilot dashboard
Uploading a CSV dataset
Detecting missing customer IDs
Calculating the initial quality score
Automatically repairing the dataset
Running final validation
Displaying the final 100% quality score
🔮 Future Improvements

Potential production enhancements include:

Apache Kafka event streaming
Cloud Storage event triggers
BigQuery streaming ingestion
Configurable data-quality rules
Email and Slack alerts
Historical quality dashboards
Data-quality trend analysis
Distributed processing for multi-GB datasets
Authentication and role-based access
Production monitoring and logging
Cloud-native deployment
🎯 Project Goal

The goal of DataOps Copilot is to demonstrate how automated data-quality validation and repair can be integrated into a real-time data pipeline.

Instead of manually inspecting every dataset, the system automatically:

Detects → Diagnoses → Repairs → Validates → Reports

👩‍💻 Author
Sahithi Mudaganti

GitHub:
https://github.com/mudagantisahithi-sketch

📄 License

This project is intended for educational, demonstration, and portfolio purposes.
