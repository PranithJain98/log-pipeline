#!/usr/bin/env python3
import re
import os
import time
import sqlite3

# Path to the log file we're tailing
LOG_FILE = 'logs/access.log'

# We'll store how many bytes we've read in a simple text file
OFFSET_FILE = 'logs/.offset'

# SQLite database file
DB_FILE = 'logs.db'

# Regex pattern to parse Apache-like log lines:
#   IP - - [timestamp] "GET url HTTP/1.1" status - "user_agent"
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\]\s+'
    r'"GET\s+(?P<url>\S+)\s+HTTP/1.1"\s+'
    r'(?P<status>\d+)\s+-\s+'
    r'"(?P<user_agent>[^"]+)"'
)

def create_table_if_not_exists(conn):
    """
    Creates the logs table in the SQLite database if it does not exist.
    """
    with conn:
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

def parse_log_line(line: str):
    """
    Parses a single log line using the LOG_PATTERN regex.
    Returns a dict of parsed fields if matched, or None if it fails.
    """
    match = LOG_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

def save_to_db(conn, parsed):
    """
    Inserts a parsed log line (dict) into the SQLite database.
    """
    with conn:
        conn.execute('''
            INSERT INTO logs (ip, timestamp, url, status, user_agent)
            VALUES (:ip, :timestamp, :url, :status, :user_agent)
        ''', {
            'ip': parsed['ip'],
            'timestamp': parsed['timestamp'],
            'url': parsed['url'],
            'status': int(parsed['status']),
            'user_agent': parsed['user_agent']
        })

def read_offset():
    """
    Reads the last-known file offset from OFFSET_FILE.
    If not found, returns 0 (meaning start from beginning).
    """
    if not os.path.exists(OFFSET_FILE):
        return 0
    with open(OFFSET_FILE, 'r') as f:
        return int(f.read().strip())

def write_offset(offset):
    """
    Writes the current file offset to OFFSET_FILE.
    """
    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(OFFSET_FILE), exist_ok=True)
    with open(OFFSET_FILE, 'w') as f:
        f.write(str(offset))

def tail_and_parse_log():
    """
    Continuously tails the LOG_FILE, parses new lines, and stores them in SQLite.
    Keeps track of file offset so we don't parse the same lines multiple times.
    """
    # Connect (or create) the SQLite DB
    conn = sqlite3.connect(DB_FILE)
    create_table_if_not_exists(conn)

    # Get the last known offset
    last_offset = read_offset()

    print("Starting continuous parse. Press Ctrl+C to stop.")
    while True:
        # If the log file doesn't exist yet, just wait and retry
        if not os.path.exists(LOG_FILE):
            time.sleep(2)
            continue

        # Open the file in read mode
        with open(LOG_FILE, 'r') as f:
            # Move to the last read position
            f.seek(last_offset)

            # Process any new lines
            for line in f:
                line = line.rstrip('\n')
                parsed = parse_log_line(line)
                if parsed:
                    save_to_db(conn, parsed)

            # Update offset to new end-of-file position
            last_offset = f.tell()
            write_offset(last_offset)

        # Sleep a bit before checking again
        time.sleep(3)

def main():
    try:
        tail_and_parse_log()
    except KeyboardInterrupt:
        print("\nStopping continuous parse.")

if __name__ == "__main__":
    main()
