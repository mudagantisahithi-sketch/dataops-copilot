📊 DataOps Copilot
Real-Time Data Quality Monitoring & Automatic Data Repair

DataOps Copilot is a real-time data quality pipeline that automatically detects common data-quality problems, repairs supported issues, and validates the cleaned dataset before it is used downstream.

🚀 Live Demo: https://dataops-copilot.streamlit.app/

💻 GitHub: https://github.com/mudagantisahithi-sketch/dataops-copilot

🎯 Problem

Data pipelines frequently receive datasets containing:

Missing customer IDs
Duplicate customer IDs
Missing email addresses
Other data-quality issues

Manually identifying and fixing these problems can delay data pipelines and introduce errors.

DataOps Copilot automates this process.

💡 Solution

The system follows an automated quality-control workflow:

CSV Dataset
     │
     ▼
Real-Time Detection
     │
     ▼
Initial Data Quality Check
     │
     ├── Missing IDs
     ├── Duplicate IDs
     └── Missing Emails
     │
     ▼
Automatic Data Repair
     │
     ▼
Final Quality Check
     │
     ▼
Quality Score
     │
     ├── PASSED
     └── FAILED

✨ Key Features
🔍 Automated Data Quality Checks

The pipeline checks:

Missing customer IDs
Duplicate customer IDs
Missing email addresses
Overall data-quality score
🤖 Automatic Data Repair

When supported data-quality problems are detected, the pipeline automatically runs the repair engine.

For example:

100 missing customer IDs
        ↓
Automatic repair
        ↓
100 IDs fixed
        ↓
Final validation
        ↓
100% Quality Score

⚡ Real-Time Monitoring

The local monitoring service continuously watches the incoming directory for new CSV files.

When a new dataset arrives:

New CSV
  ↓
Detection
  ↓
Quality Check
  ↓
Repair
  ↓
Validation
  ↓
Status Update

📊 Interactive Dashboard

The Streamlit dashboard provides:

Dataset upload
Quality score
Quality-check results
Automatic repair status
Final validation
Dataset information
Processing timestamps
🏗️ Architecture
                   ┌──────────────────────┐
                   │     Incoming CSV     │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Real-Time Monitor    │
                   │ realtime_monitor.py  │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ DataOps Copilot      │
                   │ copilot.py            │
                   └──────────┬───────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
          ┌──────────────────┐  ┌──────────────────┐
          │ Quality Checks   │  │ Data Repair      │
          │ quality_checks.py│  │ fix_data.py      │
          └────────┬─────────┘  └────────┬─────────┘
                   │                     │
                   └──────────┬──────────┘
                              ▼
                   ┌──────────────────────┐
                   │ Final Quality Check  │
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
                   └──────────────────────┘

🧰 Technologies
Python
Pandas
Streamlit
Google BigQuery
Git & GitHub
CSV data processing
Real-time file monitoring
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

5. Run the pipeline
python .\copilot.py .\incoming\customers_bad_nulls.csv

6. Run the real-time monitor
python .\realtime_monitor.py


Then place a CSV file into:

incoming/


The pipeline automatically detects and processes the new dataset.

7. Run the dashboard
streamlit run dashboard.py


Open:

http://localhost:8501

📊 Example Result

A test dataset containing 100 missing customer IDs produced:

Initial Quality Score
66.67%

Missing Customer IDs
100

Duplicate Customer IDs
0

Missing Emails
0


The automatic repair process then produced:

Final Quality Score
100.00%

STATUS
PASSED


This demonstrates the complete detection → repair → validation workflow.

🔄 Real-Time Workflow

The real-time monitor watches the incoming directory:

incoming/


When a new CSV appears:

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


The latest pipeline state is stored in:

pipeline_status.json

🌐 Live Application

The Streamlit application is publicly available:

🚀 DataOps Copilot

https://dataops-copilot.streamlit.app/

Upload a CSV dataset to see the data-quality analysis through the web dashboard.

🎥 Demo

A short demonstration video will show:

Opening the DataOps Copilot dashboard
Uploading a dataset containing quality problems
Detecting missing customer IDs
Displaying the initial quality score
Running automatic repair
Running the final quality check
Showing the final 100% quality score

Demo video: Coming soon

🔮 Future Improvements

Possible production enhancements include:

Apache Kafka event streaming
Cloud Storage event triggers
BigQuery streaming ingestion
Data quality rules configurable from the UI
Email/Slack alerts
Historical quality dashboards
Data-quality trend analysis
Large-file processing with distributed systems
Authentication and role-based access
Production monitoring and logging
🎯 Project Goal

The goal of DataOps Copilot is to demonstrate how automated data-quality validation and repair can be integrated into a real-time data pipeline.

Instead of manually inspecting datasets, the system automatically:

Detects → Diagnoses → Repairs → Validates → Reports

👩‍💻 Author

Sahithi Mudaganti

GitHub:

https://github.com/mudagantisahithi-sketch

📄 License

This project is intended for educational, demonstration, and portfolio purposes.
