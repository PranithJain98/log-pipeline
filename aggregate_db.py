import sqlite3
from collections import Counter

DB_FILE = 'logs.db'

def aggregate_db_logs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Count status codes
    cursor.execute("SELECT status, COUNT(*) FROM logs GROUP BY status")
    rows = cursor.fetchall()
    print("Status code counts:")
    for status, count in rows:
        print(f"{status}: {count}")

    # Count most visited URLs
    cursor.execute("SELECT url, COUNT(*) as cnt FROM logs GROUP BY url ORDER BY cnt DESC")
    rows = cursor.fetchall()
    print("\nMost visited URLs:")
    for url, count in rows:
        print(f"{url}: {count}")

    conn.close()

if __name__ == "__main__":
    aggregate_db_logs()
