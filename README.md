# log-pipeline
Log Ingestion and Aggregation Pipeline
This project demonstrates a simple pipeline to generate, parse, and analyze log data using Python and SQLite. It’s designed to run locally on a Mac (or any environment with Python 3.8+).

Table of Contents
Overview
Project Structure
Prerequisites
Setup
Usage
1. Generating Logs
2. Parsing Logs (CSV or SQLite)
3. Aggregating Logs
Project Extensions
Contributing
License
Overview
Generate Logs: We simulate Apache-style access logs with random IPs, URLs, status codes, and user agents.
Parse Logs: We read unstructured log lines, parse them into structured data (CSV or SQLite).
Aggregate/Analyze: We perform basic analytics, such as counting status codes or finding the most visited URLs.
The goal is to illustrate a local data pipeline without heavy dependencies. However, the same patterns can be extended to real logs, cloud databases, or big data frameworks.

Project Structure
text
Copy code
log-pipeline/
├── venv/                  # Python virtual environment (not in Git if .gitignore is set up)
├── logs/
│   └── access.log         # Generated logs appear here
├── generate_logs.py       # Script to generate fake logs
├── parse_logs.py          # Script to parse logs into CSV
├── parse_to_db.py         # Script to parse logs into SQLite DB
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

Creates the logs/ folder (if it doesn’t exist).
Appends 10 random log lines every 5 seconds to logs/access.log.
Continues indefinitely until you press Ctrl + C to stop.
If you already have real application logs, feel free to skip generating logs and place your own logs in the logs/access.log path (adjust as needed).

2. Parsing Logs (CSV or SQLite)
You have two main approaches for parsing:

2.1 Parsing into CSV
bash
Copy code
(venv) python parse_logs.py
This script:

Reads each line in logs/access.log.
Applies a regex to extract IP, timestamp, URL, status, user_agent.
Appends them to parsed_logs.csv.
2.2 Parsing into SQLite Database
bash
Copy code
(venv) python parse_to_db.py
This script:

Reads logs/access.log.
Creates (or connects to) a local SQLite database named logs.db.
Inserts log entries into a logs table.
3. Aggregating Logs
Once the logs are parsed, you can aggregate them in CSV or SQLite.

3.1 Aggregating CSV
bash
Copy code
(venv) python aggregate_csv.py
Reads parsed_logs.csv.
Counts how many times each status code appears.
Lists the most visited URLs.
Prints results to the terminal.
3.2 Aggregating SQLite
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
