from flask import Flask, request, Response
import requests, sys, random, os

app = Flask(__name__)

# ✅ User-Agents pool
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.6312.60 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
]

# ✅ Load proxy list from environment variable (comma-separated)
# Example in Vercel dashboard: HTTP://user:pass@host:port,HTTP://host2:port
PROXIES = os.getenv("PROXY_LIST", "").split(",")

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/api/<path:path>")
def proxy(path):
    url = f"https://api.tellonym.me/{path}"
    if request.query_string:
        url += "?" + request.query_string.decode()

    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),  # 🔀 Rotate UA
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://tellonym.me",
            "Referer": "https://tellonym.me/",
        }

        # 🔀 Rotate proxies if provided
        proxies = None
        if PROXIES and PROXIES[0] != "":
            proxy = random.choice(PROXIES).strip()
            proxies = {"http": proxy, "https": proxy}

        r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        return Response(r.content, r.status_code, dict(r.headers))
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}", file=sys.stderr)
        return {"error": str(e), "url": url}, 500

if __name__ == "__main__":
    app.run(debug=True)