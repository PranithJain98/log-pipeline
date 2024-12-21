import re
import os
import sqlite3

INPUT_LOG_FILE = 'logs/access.log'
DB_FILE = 'logs.db'

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\] '
    r'"GET (?P<url>\S+) HTTP/1.1" '
    r'(?P<status>\d+) - '
    r'"(?P<user_agent>[^"]+)"'
)

def parse_log_line(line: str):
    match = LOG_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

def create_table_if_not_exists(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            timestamp TEXT,
            url TEXT,
            status INTEGER,
            user_agent TEXT
        )
    ''')

def parse_logs_to_db():
    if not os.path.exists(INPUT_LOG_FILE):
        print(f"No log file found at {INPUT_LOG_FILE}. Exiting.")
        return

    conn = sqlite3.connect(DB_FILE)
    create_table_if_not_exists(conn)

    with open(INPUT_LOG_FILE, 'r') as logfile:
        for line in logfile:
            parsed = parse_log_line(line)
            if parsed:
                conn.execute('''
                    INSERT INTO logs (ip, timestamp, url, status, user_agent)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    parsed['ip'],
                    parsed['timestamp'],
                    parsed['url'],
                    int(parsed['status']),
                    parsed['user_agent']
                ))
    conn.commit()
    conn.close()
    print(f"Logs inserted into {DB_FILE}")

if __name__ == "__main__":
    parse_logs_to_db()
