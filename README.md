DataOps Copilot

Real-Time Data Quality Monitoring and Automatic Data Repair



DataOps Copilot is a real-time data quality pipeline that automatically detects problems in incoming customer CSV datasets, repairs supported issues, and validates the cleaned dataset.



Features

Real-time CSV file monitoring

Automatic data-quality checks

Missing customer ID detection

Duplicate customer ID detection

Missing email detection

Automatic data repair

Final quality validation

Quality score calculation

Pipeline status tracking

Streamlit monitoring dashboard

Architecture

Incoming CSV

&#x20;    |

&#x20;    v

Real-Time Monitor

&#x20;    |

&#x20;    v

DataOps Copilot

&#x20;    |

&#x20;    +----> Initial Quality Check

&#x20;    |

&#x20;    +----> Automatic Data Repair

&#x20;    |

&#x20;    +----> Final Quality Check

&#x20;    |

&#x20;    v

pipeline\_status.json

&#x20;    |

&#x20;    v

Streamlit Dashboard



Project Structure

dataops-copilot/

│

├── copilot.py

├── quality\_checks.py

├── fix\_data.py

├── realtime\_monitor.py

├── dashboard.py

├── requirements.txt

├── README.md

├── .gitignore

│

├── incoming/

└── data/



How It Works

A CSV dataset is placed in the incoming folder.

The real-time monitor detects the new file.

DataOps Copilot runs the initial quality checks.

Data quality issues are identified.

The repair engine automatically fixes supported issues.

A final quality check is performed.

The pipeline writes its current state to pipeline\_status.json.

The Streamlit dashboard displays the result.

Quality Checks



The current pipeline checks:



Missing customer IDs

Duplicate customer IDs

Missing emails



The quality score is calculated from the three checks.



Running the Pipeline



Activate the virtual environment:



.\\.venv\\Scripts\\Activate.ps1





Run the real-time monitor:



python realtime\_monitor.py





Then place a CSV file into:



incoming/





The pipeline automatically processes the new dataset.



Running the Dashboard



In another terminal:



.\\.venv\\Scripts\\Activate.ps1

streamlit run dashboard.py





Open the local Streamlit URL shown in the terminal.



Example Result



A dataset containing 100 missing customer IDs may initially produce:



QUALITY SCORE: 66.67%

STATUS: FAILED





After automatic repair:



QUALITY SCORE: 100.00%

STATUS: PASSED



Technology

Python

Pandas

Streamlit

Google Cloud BigQuery

PowerShell

Real-time file monitoring

Project Status



Core real-time ingestion, quality checking, automatic repair, status tracking, and dashboard functionality are implemented and tested.

