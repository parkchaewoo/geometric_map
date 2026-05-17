"""3D elevation map web app.

Run:  python app.py   then open  http://localhost:5000
"""

import os

from flask import Flask, jsonify, request, send_from_directory

import elevation
import regions

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
PLOTLY_JS = os.path.join(STATIC_DIR, "plotly.min.js")

app = Flask(__name__, static_folder=None)


def ensure_plotly_js():
    """Write Plotly's bundled offline JS locally (no CDN dependency)."""
    if os.path.exists(PLOTLY_JS) and os.path.getsize(PLOTLY_JS) > 1000:
        return
    import plotly.offline

    os.makedirs(STATIC_DIR, exist_ok=True)
    with open(PLOTLY_JS, "w", encoding="utf-8") as f:
        f.write(plotly.offline.get_plotlyjs())


@app.after_request
def add_cors(resp):
    # Permit calls from a future Android WebView / native client.
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)


@app.route("/api/regions")
def api_regions():
    return jsonify(regions.list_regions())


@app.route("/api/elevation")
def api_elevation():
    continent = request.args.get("continent", "").strip()
    country = request.args.get("country", "").strip() or None
    if not continent:
        return jsonify({"error": "continent is required"}), 400
    try:
        bbox, label = regions.resolve_bbox(continent, country)
    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

    # Continent view: coarser (more area, fewer tiles allowed per side).
    # Country view: denser detail.
    max_tiles = 48 if country else 80
    try:
        data = elevation.build_grid(bbox, target=220, max_tiles=max_tiles)
    except RuntimeError as e:
        return jsonify({"error": f"elevation fetch failed: {e}"}), 502

    data["label"] = label
    data["bbox"] = bbox
    return jsonify(data)


if __name__ == "__main__":
    ensure_plotly_js()
    # macOS AirPlay Receiver occupies 5000; default to 5050, override via PORT.
    port = int(os.environ.get("PORT", "5050"))
    print(f"3D elevation map running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
