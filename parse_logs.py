import re
import csv
import os

INPUT_LOG_FILE = 'logs/access.log'
OUTPUT_CSV_FILE = 'parsed_logs.csv'

# A simple regex to parse common Apache-style logs
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

def parse_logs():
    # Read the log file
    if not os.path.exists(INPUT_LOG_FILE):
        print(f"No log file found at {INPUT_LOG_FILE}. Exiting.")
        return

    # Open CSV in append mode so we can keep adding parsed lines
    with open(OUTPUT_CSV_FILE, 'a', newline='') as csvfile:
        fieldnames = ['ip', 'timestamp', 'url', 'status', 'user_agent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If file is empty, write header
        if os.stat(OUTPUT_CSV_FILE).st_size == 0:
            writer.writeheader()

        with open(INPUT_LOG_FILE, 'r') as logfile:
            for line in logfile:
                parsed = parse_log_line(line)
                if parsed:
                    writer.writerow(parsed)

if __name__ == "__main__":
    parse_logs()
    print(f"Logs parsed and appended to {OUTPUT_CSV_FILE}")
