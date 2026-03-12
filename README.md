project created as a part of understanding backend systems
# Distributed Web Crawler & Mini Search Engine

A Python-based multi-threaded web crawler that collects URLs from websites and stores them in a SQLite database.
A simple Flask web application allows users to search through the crawled URLs using a browser interface.

---

## Features

* Multi-threaded web crawling
* BFS-based link traversal
* Domain-restricted crawling
* robots.txt compliance
* Rate limiting for ethical crawling
* SQLite database storage
* Flask-based search interface

---

## Tech Stack

* Python
* Flask
* Requests
* BeautifulSoup
* SQLite

Libraries used include:

* Flask
* Requests
* Beautiful Soup
* SQLite

---

## Project Structure

```
web_crawler
│
├ crawler.py          # Multi-threaded web crawler
├ search_app.py       # Flask search interface
├ crawler.db          # SQLite database storing crawled URLs
├ requirements.txt    # Project dependencies
└ README.md           # Project documentation
```

---

## How It Works

1. The crawler starts from a seed URL.
2. It downloads the webpage and extracts links.
3. Links are added to a queue for further crawling.
4. URLs are stored in a SQLite database.
5. A Flask web app provides a search interface to query the database.

Architecture overview:

```
Websites
   ↓
Crawler (Python)
   ↓
SQLite Database
   ↓
Flask Web Application
   ↓
Browser Search Interface
```

---

## How to Run the Project

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run the crawler

```
python crawler.py
```

This will crawl webpages and store URLs in the database.

### 3. Start the search interface

```
python search_app.py
```

### 4. Open in browser

```
http://127.0.0.1:5000
```

You can now search for URLs stored by the crawler.

---

## Example Output

Crawler output:

```
Crawling: https://quotes.toscrape.com
Crawling: https://quotes.toscrape.com/page/2

Crawling finished.
Pages crawled: 10
Time taken: 12.4 seconds
Crawl speed: 0.8 pages/sec
```

---

## Future Improvements

* Implement page ranking for better search results
* Add a frontend UI for better user experience
* Implement distributed crawling across multiple nodes
* Add keyword indexing for faster search

---

## Author

**Tejas Ruikar**
Final Year B.Tech – Artificial Intelligence & Data Science
