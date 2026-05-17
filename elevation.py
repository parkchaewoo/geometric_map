"""DEM (digital elevation model) processing.

Source: AWS Open Data "Terrarium" terrain tiles
  https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png
No authentication required, global coverage.

Elevation decode (Terrarium encoding):
  elevation_m = (R * 256 + G + B / 256) - 32768
"""

import io
import math
import os
import time

import numpy as np
import requests
from PIL import Image

TILE_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
TILE_SIZE = 256
CACHE_DIR = os.path.join("/tmp", "geomap_tiles")
os.makedirs(CACHE_DIR, exist_ok=True)

# Upper bound on number of tiles fetched per request. Keeps very large
# (continent) bboxes tractable: a coarser zoom is chosen instead of failing.
MAX_TILES = 64


def lon_to_tile_x(lon, z):
    return (lon + 180.0) / 360.0 * (2 ** z)


def lat_to_tile_y(lat, z):
    lat = max(min(lat, 85.05112878), -85.05112878)
    rad = math.radians(lat)
    return (1.0 - math.asinh(math.tan(rad)) / math.pi) / 2.0 * (2 ** z)


def tile_x_to_lon(x, z):
    return x / (2 ** z) * 360.0 - 180.0


def tile_y_to_lat(y, z):
    n = math.pi - 2.0 * math.pi * y / (2 ** z)
    return math.degrees(math.atan(math.sinh(n)))


def tile_range(bbox, z):
    """Return inclusive tile index ranges (x0, x1, y0, y1) covering bbox."""
    min_lon, min_lat, max_lon, max_lat = bbox
    x0 = int(math.floor(lon_to_tile_x(min_lon, z)))
    x1 = int(math.floor(lon_to_tile_x(max_lon, z)))
    # Note: tile Y grows southward, so max_lat -> smaller y.
    y0 = int(math.floor(lat_to_tile_y(max_lat, z)))
    y1 = int(math.floor(lat_to_tile_y(min_lat, z)))
    n = 2 ** z
    x0 = max(0, min(x0, n - 1))
    x1 = max(0, min(x1, n - 1))
    y0 = max(0, min(y0, n - 1))
    y1 = max(0, min(y1, n - 1))
    return x0, x1, y0, y1


def pick_zoom(bbox, max_tiles=MAX_TILES, max_zoom=12):
    """Pick the highest zoom whose tile count stays within max_tiles."""
    chosen = 0
    for z in range(0, max_zoom + 1):
        x0, x1, y0, y1 = tile_range(bbox, z)
        count = (x1 - x0 + 1) * (y1 - y0 + 1)
        if count <= max_tiles:
            chosen = z
        else:
            break
    return chosen


def fetch_tile(z, x, y, retries=4):
    """Fetch one terrarium tile as an RGB numpy array, with disk cache."""
    cache_path = os.path.join(CACHE_DIR, f"{z}_{x}_{y}.png")
    if os.path.exists(cache_path):
        try:
            with Image.open(cache_path) as im:
                return np.asarray(im.convert("RGB"), dtype=np.float64)
        except Exception:
            os.remove(cache_path)

    url = TILE_URL.format(z=z, x=x, y=y)
    last_err = None
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=15, headers={"User-Agent": "geomap/1.0"})
            if resp.status_code == 200:
                with open(cache_path, "wb") as f:
                    f.write(resp.content)
                with Image.open(io.BytesIO(resp.content)) as im:
                    return np.asarray(im.convert("RGB"), dtype=np.float64)
            last_err = f"HTTP {resp.status_code}"
        except requests.RequestException as e:
            last_err = str(e)
        time.sleep(2 ** attempt)
    raise RuntimeError(f"tile fetch failed {z}/{x}/{y}: {last_err}")


def decode_elevation(rgb):
    """Terrarium RGB -> elevation in metres."""
    r = rgb[..., 0]
    g = rgb[..., 1]
    b = rgb[..., 2]
    return (r * 256.0 + g + b / 256.0) - 32768.0


def build_grid(bbox, target=200, max_tiles=MAX_TILES):
    """Build an elevation grid for bbox.

    Returns dict with:
      lons: 1D list (length W) of longitudes
      lats: 1D list (length H) of latitudes
      z:    2D list (H x W) of elevations in metres
      zmin, zmax: scalars
      zoom: chosen tile zoom level
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    z = pick_zoom(bbox, max_tiles=max_tiles)
    x0, x1, y0, y1 = tile_range(bbox, z)

    cols = x1 - x0 + 1
    rows = y1 - y0 + 1
    mosaic = np.empty((rows * TILE_SIZE, cols * TILE_SIZE), dtype=np.float64)
    for ty in range(y0, y1 + 1):
        for tx in range(x0, x1 + 1):
            tile = fetch_tile(z, tx, ty)
            elev = decode_elevation(tile)
            ry = (ty - y0) * TILE_SIZE
            rx = (tx - x0) * TILE_SIZE
            mosaic[ry:ry + TILE_SIZE, rx:rx + TILE_SIZE] = elev

    # Geographic extent actually covered by the mosaic of whole tiles.
    mosaic_lon0 = tile_x_to_lon(x0, z)
    mosaic_lon1 = tile_x_to_lon(x1 + 1, z)
    mosaic_lat0 = tile_y_to_lat(y0, z)        # north edge (top row)
    mosaic_lat1 = tile_y_to_lat(y1 + 1, z)    # south edge (bottom row)

    H, W = mosaic.shape

    # Crop mosaic to the requested bbox via pixel index mapping.
    def lon_to_px(lon):
        frac = (lon - mosaic_lon0) / (mosaic_lon1 - mosaic_lon0)
        return int(round(frac * (W - 1)))

    def lat_to_py(lat):
        frac = (mosaic_lat0 - lat) / (mosaic_lat0 - mosaic_lat1)
        return int(round(frac * (H - 1)))

    px0 = max(0, min(lon_to_px(min_lon), W - 1))
    px1 = max(0, min(lon_to_px(max_lon), W - 1))
    py0 = max(0, min(lat_to_py(max_lat), H - 1))   # north
    py1 = max(0, min(lat_to_py(min_lat), H - 1))   # south
    if px1 <= px0:
        px1 = min(px0 + 1, W - 1)
    if py1 <= py0:
        py1 = min(py0 + 1, H - 1)

    cropped = mosaic[py0:py1 + 1, px0:px1 + 1]
    ch, cw = cropped.shape

    # Downsample to target grid using simple striding.
    step_y = max(1, ch // target)
    step_x = max(1, cw // target)
    grid = cropped[::step_y, ::step_x]
    gh, gw = grid.shape

    lons = np.linspace(min_lon, max_lon, gw)
    lats = np.linspace(max_lat, min_lat, gh)  # row 0 = north

    # "해발 고도" view: clamp non-finite and sub-sea bathymetry to sea level
    # so ocean depth does not crush land relief in the surface graph.
    grid = np.where(np.isfinite(grid), grid, 0.0)
    grid = np.maximum(grid, 0.0)

    return {
        "lons": [round(float(v), 5) for v in lons],
        "lats": [round(float(v), 5) for v in lats],
        "z": [[round(float(v), 1) for v in row] for row in grid],
        "zmin": round(float(np.nanmin(grid)), 1),
        "zmax": round(float(np.nanmax(grid)), 1),
        "zoom": z,
        "shape": [int(gh), int(gw)],
    }
