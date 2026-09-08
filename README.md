📊 DataOps Copilot
Real-time data quality monitoring, automated data repair, and validation for incoming CSV datasets.
🚀 Live Demo
Open DataOps Copilot
View Source Code
📌 Overview
DataOps Copilot is an automated data-quality pipeline designed to detect, repair, and validate common problems in incoming customer datasets.
Instead of manually inspecting every CSV file, the system automatically runs a quality-control workflow:
CSV Dataset
    ↓
Real-Time Detection
    ↓
Initial Quality Check
    ↓
Issue Detection
    ↓
Automatic Data Repair
    ↓
Final Quality Check
    ↓
Quality Score
    ↓
Pipeline Status
The project combines a Python-based data pipeline, a real-time folder monitor, and a Streamlit dashboard.

🎯 Problem
Data pipelines can receive datasets containing:

Missing customer IDs
Duplicate customer IDs
Missing email addresses
Other data-quality problems
If these issues are not detected before downstream processing, they can cause incorrect analytics, failed transformations, or unreliable business data.

The goal
Automatically identify data-quality issues before the dataset moves downstream.

✨ Features
Feature	Description
🔍 Quality Checks	Detect missing IDs, duplicates, and missing emails
🤖 Automatic Repair	Fix supported data-quality issues automatically
⚡ Real-Time Monitoring	Detect new CSV files placed in incoming/
📊 Quality Score	Calculate an overall dataset quality score
✅ Final Validation	Re-check the repaired dataset
📈 Streamlit Dashboard	View pipeline results through a web interface
📝 Pipeline Status	Store the latest pipeline state
🐍 Python Pipeline	Fully executable locally from PowerShell
🏗️ Architecture
    ┌─────────────────────┐
                         │     Incoming CSV    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Real-Time Monitor  │
                         │ realtime_monitor.py │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    DataOps Copilot  │
                         │     copilot.py      │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
          ┌──────────────────┐             ┌──────────────────┐
          │ Quality Checks   │             │ Automatic Repair │
          │quality_checks.py │             │   fix_data.py    │
          └────────┬─────────┘             └────────┬─────────┘
                   │                                │
                   └──────────────┬─────────────────┘
                                  ▼
                       ┌─────────────────────┐
                       │ Final Quality Check │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Pipeline Status     │
                       │ pipeline_status.json│
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Streamlit Dashboard │
                       │    dashboard.py     │
                       └─────────────────────┘
🔄 Real-Time Pipeline
The real-time monitor continuously watches the incoming/ directory.

Start it with:

python .\realtime_monitor.py
Then place a CSV file into:

incoming/
The monitor automatically detects the new file and starts the pipeline.

Example
incoming/realtime_testing.csv
          ↓
     File detected
          ↓
    Quality check
          ↓
    66.67% detected
          ↓
    Automatic repair
          ↓
    Final validation
          ↓
       100.00%
          ↓
      PASSED
The latest pipeline state is written to:

pipeline_status.json
Example:

{
    "status": "PASSED",
    "stage": "COMPLETED",
    "message": "Pipeline completed successfully",
    "score": 100.0,
    "input_file": "realtime_testing.csv",
    "rows": 1000,
    "error": null
}
📊 Example Result
A test dataset containing 1,000 rows with 100 missing customer IDs was processed.

Before repair
Rows:                 1,000
Missing Customer IDs:   100
Duplicate IDs:            0
Missing Emails:            0

Quality Score:         66.67%
Status:                FAILED
The pipeline automatically detected the missing IDs and ran the repair process.

After repair
Rows:                 1,000
Missing Customer IDs:     0
Duplicate IDs:            0
Missing Emails:            0

Quality Score:        100.00%
Status:                PASSED
Result
66.67% → 100.00%

The dataset passed the final quality validation.

🖥️ Streamlit Dashboard
The project includes a web dashboard for interactive data-quality monitoring.

Dashboard capabilities
Upload CSV datasets
Display dataset information
Show quality score
Display individual quality checks
Show automatic repair status
Display final validation
Show processing timestamps
Refresh pipeline information automatically
Run locally
streamlit run dashboard.py
Then open:

http://localhost:8501
🌐 Live Dashboard
https://dataops-copilot.streamlit.app/

🚀 Quick Start
1. Clone the repository
git clone https://github.com/mudagantisahithi-sketch/dataops-copilot.git
cd dataops-copilot
2. Create a virtual environment
python -m venv .venv
3. Activate it
.\.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
▶️ Run the Pipeline
To process a specific CSV:

python .\copilot.py .\incoming\customers_bad_nulls.csv
The pipeline performs:

Initial Quality Check
        ↓
Automatic Repair
        ↓
Final Quality Check
        ↓
Pipeline Completion
⚡ Run Real-Time Monitoring
Start the monitor:

python .\realtime_monitor.py
You should see:

============================================================
       DATAOPS COPILOT - REAL-TIME PIPELINE
============================================================

Watching folder: incoming
Drop a CSV file into the incoming folder.
The pipeline will automatically process new files.
Press Ctrl+C to stop.
Now add a CSV file to:

incoming/
The pipeline will automatically process it.

📁 Project Structure
dataops-copilot/
│
├── dashboard.py
├── copilot.py
├── realtime_monitor.py
│
├── quality_checks.py
├── fix_data.py
│
├── generate_data.py
├── create_bad_data.py
├── inspect_data.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── incoming/
│   └── CSV input files
│
├── data/
│   └── processed datasets
│
└── reports/
    └── quality reports
🧰 Technology Stack
Core
Python
Pandas
CSV processing
Dashboard
Streamlit
Automation
Python subprocess
Real-time directory monitoring
JSON pipeline status
Development
Git
GitHub
Virtual environments
🔮 Future Roadmap
The current project provides a working local real-time data-quality pipeline and deployed dashboard.

Future improvements could include:

 Kafka-based event streaming
 Google Cloud Storage triggers
 BigQuery integration
 Configurable quality rules
 Email and Slack alerts
 Historical quality metrics
 Quality trend dashboards
 Large-file distributed processing
 Authentication and role-based access
 Cloud-native deployment
 Automated testing and CI/CD
🎓 What This Project Demonstrates
This project demonstrates practical skills in:

Data quality engineering
Python data processing
Automated data validation
Data cleansing
Real-time pipeline design
Streamlit application development
JSON status tracking
Git and GitHub
Pipeline monitoring
End-to-end ETL concepts
👩‍💻 Author
Sahithi Mudaganti

GitHub:
https://github.com/mudagantisahithi-sketch

