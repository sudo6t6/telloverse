from flask import Flask, request, jsonify
import requests
import sys

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/api/<path:path>")
def proxy(path):
    url = f"https://api.tellonym.me/{path}"
    if request.query_string:
        url += "?" + request.query_string.decode()

    try:
        r = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://tellonym.me",
            "Referer": "https://tellonym.me/"
        })
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}", file=sys.stderr)
        return jsonify({"error": str(e), "url": url}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)