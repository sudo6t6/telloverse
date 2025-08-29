from flask import Flask, request, jsonify
import requests
import sys
import random

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route("/api/<path:path>")
def proxy(path):
    url = f"https://api.tellonym.me/{path}"
    if request.query_string:
        url += "?" + request.query_string.decode()

    try:
        session = requests.Session()

        # Rotate User-Agent strings
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
        ]
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://tellonym.me",
            "Referer": "https://tellonym.me/"
        }

        r = session.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return jsonify(r.json())

    except Exception as e:
        print(f"❌ Error fetching {url}: {e}", file=sys.stderr)
        return jsonify({"error": str(e), "url": url}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)