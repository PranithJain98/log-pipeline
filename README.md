**Log Ingestion and Aggregation Pipeline**

This project demonstrates a simple pipeline to generate, parse, and analyze log data using **Python** and **SQLite**. It’s designed to run locally on a Mac (or any environment with Python 3.8+).

---

## Table of Contents

1. [Overview](#overview)  
2. [Project Structure](#project-structure)  
3. [Prerequisites](#prerequisites)  
4. [Setup](#setup)  
5. [Usage](#usage)  
   1. [Generating Logs](#1-generating-logs)  
   2. [One-Time Parsing (CSV or SQLite)](#2-one-time-parsing-csv-or-sqlite)  
   3. [Real-Time Continuous Parsing (SQLite)](#3-real-time-continuous-parsing-sqlite)  
   4. [Aggregating Logs](#4-aggregating-logs)  
6. [Project Extensions](#project-extensions)  
7. [Contributing](#contributing)  
8. [License](#license)

---

## Overview

1. **Generate Logs**: We simulate Apache-style access logs with random IPs, URLs, status codes, and user agents.  
2. **Parse Logs**: We read unstructured log lines, parse them into structured data (either CSV or SQLite).  
3. **Aggregate/Analyze**: We perform basic analytics, such as counting status codes or finding the most visited URLs.

The goal is to illustrate a local data pipeline without heavy dependencies. However, the same patterns can be extended to real logs, cloud databases, or big data frameworks.

---

## Project Structure

```text
log-pipeline/
├── venv/                  # Python virtual environment (not in Git if .gitignore is set up)
├── logs/
│   └── access.log         # Generated logs appear here
├── generate_logs.py       # Script to generate fake logs
├── parse_logs.py          # Script to parse logs into CSV (one-time parse)
├── parse_to_db.py         # Script to parse logs into SQLite (one-time parse)
├── continuous_parse_logs.py  # Script to continuously parse logs into SQLite (real-time)
├── aggregate_csv.py       # Aggregation (CSV-based)
├── aggregate_db.py        # Aggregation (SQLite-based)
├── requirements.txt       # Python dependencies
├── .gitignore             # Files/folders to ignore in Git
└── README.md              # This file!
Note: The venv/ folder is created by Python for the virtual environment and may be excluded from the repository via .gitignore.

Prerequisites
Python 3.8+ (Check via python --version)
Git (for cloning/pushing this repo)
SQLite (likely pre-installed on macOS; check with sqlite3 --version or install via Homebrew if needed)
Setup
Clone the Repository
If you haven’t already cloned this repo, do:

bash
Copy code
git clone https://github.com/<YOUR_USERNAME>/<REPO_NAME>.git
cd <REPO_NAME>
Create and Activate a Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows PowerShell
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Note: If you haven’t created a requirements.txt yet, you can generate one after installing needed packages by running pip freeze > requirements.txt.

Verify SQLite

macOS often comes with SQLite already installed.
If needed, install via Homebrew:
bash
Copy code
brew install sqlite
Ensure sqlite3 --version works.
Usage
1. Generating Logs
Run the log generator in one terminal. By default, it writes to logs/access.log every 5 seconds:

bash
Copy code
(venv) python generate_logs.py
This script:

Creates the logs/ folder if it doesn’t exist.
Appends 10 random log lines every 5 seconds to logs/access.log.
Continues indefinitely until you press Ctrl + C to stop.
If you have real application logs, feel free to skip generating logs and place your own logs in the logs/access.log path (adjust as needed).

2. One-Time Parsing (CSV or SQLite)
If you prefer a one-time parse of the entire access.log file—e.g., after logs are fully generated—use one of these scripts:

2.1 Parsing into CSV
bash
Copy code
(venv) python parse_logs.py
Reads each line in logs/access.log.
Applies a regex to extract IP, timestamp, URL, status, and user_agent.
Appends them to parsed_logs.csv.
Stops after it finishes parsing the file.
2.2 Parsing into SQLite
bash
Copy code
(venv) python parse_to_db.py
Reads logs/access.log.
Creates (or connects to) a local SQLite database named logs.db.
Inserts log entries into a logs table.
Stops after it finishes parsing the file.
3. Real-Time Continuous Parsing (SQLite)
For a live ingestion approach—parsing new lines in real-time—use:

bash
Copy code
(venv) python continuous_parse_logs.py
Continuously tails the logs/access.log file (similar to tail -f).
Maintains a file offset (in logs/.offset) so it doesn’t re-parse old lines.
Inserts parsed data into logs.db as soon as new lines appear.
Keeps running until you press Ctrl + C to stop.
Example Workflow for real-time parsing:

Terminal A:

bash
Copy code
(venv) python generate_logs.py
This keeps writing new lines to logs/access.log.

Terminal B:

bash
Copy code
(venv) python continuous_parse_logs.py
This will read any new lines from logs/access.log every few seconds and insert them into logs.db.

Check or Aggregate (in a third terminal, or whenever you like):

bash
Copy code
(venv) python aggregate_db.py
to see updated counts of status codes, top URLs, etc.

4. Aggregating Logs
Once the logs are parsed, you can aggregate them using these scripts:

4.1 Aggregating CSV
bash
Copy code
(venv) python aggregate_csv.py
Reads parsed_logs.csv.
Counts how many times each status code appears.
Lists the most visited URLs.
Prints results in the terminal.
4.2 Aggregating SQLite
bash
Copy code
(venv) python aggregate_db.py
Connects to logs.db.
Runs basic SQL queries: e.g., counts of status codes, top URLs.
Prints aggregated results in the terminal.
Project Extensions
Scheduling: Use cron or an orchestrator like Airflow to parse logs periodically (e.g., every minute).
Docker: Containerize the pipeline for easy deployment.
Elasticsearch/Kibana: Instead of CSV/SQLite, store logs in Elasticsearch for real-time search and visualization in Kibana.
Cloud Integration: Ingest logs into AWS RDS or DynamoDB.
Kafka: Stream logs in real time and process them with Apache Kafka or Spark Streaming.
Contributing
Fork this repo on GitHub.
Create a branch for your feature or bug fix:
bash
Copy code
git checkout -b feature/my-new-feature
Commit your changes:
bash
Copy code
git commit -am "Add a new feature"
Push to your branch:
bash
Copy code
git push origin feature/my-new-feature
Submit a Pull Request to the main branch.
We welcome feedback, bug reports, and contributions!

License
This project is provided under the MIT License. See the LICENSE file for more details.