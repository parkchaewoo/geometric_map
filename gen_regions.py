"""Generate web/regions.json from regions.py (single source of truth).

Run after editing regions.py:  python3 gen_regions.py
"""

import json
import os

import regions

OUT = os.path.join(os.path.dirname(__file__), "web", "regions.json")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    payload = {
        "list": regions.list_regions(),
        "regions": regions.REGIONS,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
