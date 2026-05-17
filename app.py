"""Desktop dev server: serves the self-contained web app in web/.

The web app is fully client-side (tile fetch + elevation decode happen in
the browser via web/geo.js), so this is just a static file server for
local development. The same web/ directory is bundled into the Android
app as WebView assets.

Run:  python app.py   then open  http://localhost:5050
"""

import os

from flask import Flask, send_from_directory

WEB_DIR = os.path.join(os.path.dirname(__file__), "web")
PLOTLY_JS = os.path.join(WEB_DIR, "plotly.min.js")

app = Flask(__name__, static_folder=None)


def ensure_plotly_js():
    """Write Plotly's bundled offline JS into web/ (no CDN dependency)."""
    if os.path.exists(PLOTLY_JS) and os.path.getsize(PLOTLY_JS) > 1000:
        return
    import plotly.offline

    os.makedirs(WEB_DIR, exist_ok=True)
    with open(PLOTLY_JS, "w", encoding="utf-8") as f:
        f.write(plotly.offline.get_plotlyjs())


@app.route("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")


@app.route("/<path:filename>")
def assets(filename):
    return send_from_directory(WEB_DIR, filename)


if __name__ == "__main__":
    ensure_plotly_js()
    # macOS AirPlay Receiver occupies 5000; default to 5050, override via PORT.
    port = int(os.environ.get("PORT", "5050"))
    print(f"3D elevation map (dev) running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
