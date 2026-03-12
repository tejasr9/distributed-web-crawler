from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Mini Search Engine</title>
</head>
<body>

<h2>Web Crawler Search</h2>

<form method="GET">
<input type="text" name="query" placeholder="Search URL">
<button type="submit">Search</button>
</form>

<hr>

<ul>
{% for url in results %}
<li><a href="{{ url }}" target="_blank">{{ url }}</a></li>
{% endfor %}
</ul>

</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():

    query = request.args.get("query", "")

    conn = sqlite3.connect("crawler.db")
    cursor = conn.cursor()

    if query:
        cursor.execute(
            "SELECT url FROM pages WHERE url LIKE ?",
            ("%" + query + "%",)
        )
    else:
        cursor.execute("SELECT url FROM pages LIMIT 20")

    rows = cursor.fetchall()

    results = [row[0] for row in rows]

    return render_template_string(HTML, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)