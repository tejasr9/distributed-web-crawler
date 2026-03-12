import requests
from bs4 import BeautifulSoup
from collections import deque
import threading
import sqlite3
from urllib.parse import urljoin, urlparse
import urllib.robotparser
import time

# ---------------- DATABASE ----------------

conn = sqlite3.connect("crawler.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pages (
    url TEXT PRIMARY KEY
)
""")

# ---------------- SETTINGS ----------------

start_url = "https://quotes.toscrape.com"

allowed_domain = urlparse(start_url).netloc

max_depth = 2
max_pages = 10
pages_crawled = 0

visited = set()
queue = deque()

queue.append((start_url, 0))

lock = threading.Lock()

# ---------------- ROBOTS.TXT ----------------

robots_url = start_url + "/robots.txt"

rp = urllib.robotparser.RobotFileParser()
rp.set_url(robots_url)
rp.read()

# ---------------- TIMER ----------------

start_time = time.time()

# ---------------- CRAWLER FUNCTION ----------------

def crawl():

    global pages_crawled

    while True:

        with lock:
            if not queue or pages_crawled >= max_pages:
                return

            url, depth = queue.popleft()

            if url in visited or depth > max_depth:
                continue

            visited.add(url)
            pages_crawled += 1

        # robots.txt check
        if not rp.can_fetch("*", url):
            print("Blocked by robots.txt:", url)
            continue

        print("Crawling:", url)

        try:

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            # rate limiting
            time.sleep(1)

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print("Skipped:", url)
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # save to database
            cursor.execute(
                "INSERT OR IGNORE INTO pages (url) VALUES (?)",
                (url,)
            )

            conn.commit()

            for link in soup.find_all("a"):

                href = link.get("href")

                if not href:
                    continue

                full_url = urljoin(url, href)

                parsed = urlparse(full_url)

                # domain restriction
                if parsed.netloc == allowed_domain:

                    with lock:
                        queue.append((full_url, depth + 1))

        except Exception as e:
            print("Error:", e)


# ---------------- THREADS ----------------

threads = []

for i in range(5):
    t = threading.Thread(target=crawl)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# ---------------- STATS ----------------

end_time = time.time()

total_time = end_time - start_time

print("\nCrawling finished.")

print("Pages crawled:", pages_crawled)
print("Time taken:", round(total_time, 2), "seconds")

if total_time > 0:
    speed = pages_crawled / total_time
    print("Crawl speed:", round(speed, 2), "pages/sec")