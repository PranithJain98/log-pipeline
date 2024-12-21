import csv
from collections import Counter

CSV_FILE = 'parsed_logs.csv'

def aggregate_csv_logs():
    status_counter = Counter()
    url_counter = Counter()

    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            status_counter[row['status']] += 1
            url_counter[row['url']] += 1

    print("Status code counts:")
    for status, count in status_counter.most_common():
        print(f"{status}: {count}")

    print("\nMost visited URLs:")
    for url, count in url_counter.most_common():
        print(f"{url}: {count}")

if __name__ == "__main__":
    aggregate_csv_logs()

