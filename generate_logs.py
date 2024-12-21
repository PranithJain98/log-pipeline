import time
import random
import datetime
import os

LOG_FILE = 'logs/access.log'

STATUS_CODES = [200, 301, 404, 500]
URLS = ['/home', '/about', '/contact', '/products', '/blog']
USER_AGENTS = ['Mozilla/5.0', 'curl/7.68.0', 'Safari/537.36', 'Chrome/88.0']

def generate_log_line():
    ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    timestamp = datetime.datetime.utcnow().strftime('%d/%b/%Y:%H:%M:%S +0000')
    url = random.choice(URLS)
    status = random.choice(STATUS_CODES)
    user_agent = random.choice(USER_AGENTS)
    return f'{ip} - - [{timestamp}] "GET {url} HTTP/1.1" {status} - "{user_agent}"\n'

def generate_logs(num_lines=100):
    os.makedirs('logs', exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        for _ in range(num_lines):
            line = generate_log_line()
            f.write(line)

if __name__ == "__main__":
    while True:
        generate_logs(num_lines=10)
        print("Wrote 10 new log lines.")
        time.sleep(5)
