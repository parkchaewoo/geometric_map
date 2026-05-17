"use strict";
/* Self-contained elevation engine (port of elevation.py).
 * Fetches AWS Terrarium DEM tiles directly (CORS is open) and builds an
 * elevation grid entirely in the browser/WebView. No backend required.
 *
 * Terrarium decode:  elevation_m = (R*256 + G + B/256) - 32768
 */
const Geo = (() => {
  const TILE_URL =
    "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png";
  const TILE = 256;

  function lonToTileX(lon, z) {
    return ((lon + 180) / 360) * 2 ** z;
  }
  function latToTileY(lat, z) {
    lat = Math.max(Math.min(lat, 85.05112878), -85.05112878);
    const r = (lat * Math.PI) / 180;
    return ((1 - Math.asinh(Math.tan(r)) / Math.PI) / 2) * 2 ** z;
  }
  function tileXToLon(x, z) {
    return (x / 2 ** z) * 360 - 180;
  }
  function tileYToLat(y, z) {
    const n = Math.PI - (2 * Math.PI * y) / 2 ** z;
    return (180 / Math.PI) * Math.atan(Math.sinh(n));
  }

  function tileRange(bbox, z) {
    const [minLon, minLat, maxLon, maxLat] = bbox;
    const n = 2 ** z;
    const cl = (v) => Math.max(0, Math.min(v, n - 1));
    return {
      x0: cl(Math.floor(lonToTileX(minLon, z))),
      x1: cl(Math.floor(lonToTileX(maxLon, z))),
      y0: cl(Math.floor(latToTileY(maxLat, z))), // north -> smaller y
      y1: cl(Math.floor(latToTileY(minLat, z))),
    };
  }

  function pickZoom(bbox, maxTiles, maxZoom) {
    let chosen = 0;
    for (let z = 0; z <= maxZoom; z++) {
      const r = tileRange(bbox, z);
      const count = (r.x1 - r.x0 + 1) * (r.y1 - r.y0 + 1);
      if (count <= maxTiles) chosen = z;
      else break;
    }
    return chosen;
  }

  function fetchTile(z, x, y, retries = 3) {
    const url = TILE_URL.replace("{z}", z).replace("{x}", x).replace("{y}", y);
    return new Promise((resolve, reject) => {
      let attempt = 0;
      const tryOnce = () => {
        const img = new Image();
        img.crossOrigin = "anonymous";
        img.onload = () => {
          const c = document.createElement("canvas");
          c.width = TILE;
          c.height = TILE;
          const ctx = c.getContext("2d", { willReadFrequently: true });
          ctx.drawImage(img, 0, 0);
          resolve(ctx.getImageData(0, 0, TILE, TILE).data);
        };
        img.onerror = () => {
          attempt += 1;
          if (attempt > retries) reject(new Error(`tile ${z}/${x}/${y}`));
          else setTimeout(tryOnce, 600 * attempt);
        };
        img.src = url;
      };
      tryOnce();
    });
  }

  async function buildGrid(bbox, opts) {
    const o = opts || {};
    const target = o.target || 170;
    const maxTiles = o.maxTiles || 36;
    const maxZoom = o.maxZoom || 12;
    const [minLon, minLat, maxLon, maxLat] = bbox;

    const z = pickZoom(bbox, maxTiles, maxZoom);
    const r = tileRange(bbox, z);
    const cols = r.x1 - r.x0 + 1;
    const rows = r.y1 - r.y0 + 1;
    const W = cols * TILE;
    const H = rows * TILE;
    const mosaic = new Float32Array(W * H);

    let done = 0;
    const totalTiles = cols * rows;
    for (let ty = r.y0; ty <= r.y1; ty++) {
      for (let tx = r.x0; tx <= r.x1; tx++) {
        const data = await fetchTile(z, tx, ty);
        const ox = (tx - r.x0) * TILE;
        const oy = (ty - r.y0) * TILE;
        for (let py = 0; py < TILE; py++) {
          const rowBase = (oy + py) * W + ox;
          const src = py * TILE * 4;
          for (let px = 0; px < TILE; px++) {
            const i = src + px * 4;
            mosaic[rowBase + px] =
              data[i] * 256 + data[i + 1] + data[i + 2] / 256 - 32768;
          }
        }
        done += 1;
        if (o.onProgress) o.onProgress(done, totalTiles);
      }
    }

    const mLon0 = tileXToLon(r.x0, z);
    const mLon1 = tileXToLon(r.x1 + 1, z);
    const mLat0 = tileYToLat(r.y0, z); // north
    const mLat1 = tileYToLat(r.y1 + 1, z); // south

    const lonToPx = (lon) =>
      Math.round(((lon - mLon0) / (mLon1 - mLon0)) * (W - 1));
    const latToPy = (lat) =>
      Math.round(((mLat0 - lat) / (mLat0 - mLat1)) * (H - 1));

    let px0 = Math.max(0, Math.min(lonToPx(minLon), W - 1));
    let px1 = Math.max(0, Math.min(lonToPx(maxLon), W - 1));
    let py0 = Math.max(0, Math.min(latToPy(maxLat), H - 1));
    let py1 = Math.max(0, Math.min(latToPy(minLat), H - 1));
    if (px1 <= px0) px1 = Math.min(px0 + 1, W - 1);
    if (py1 <= py0) py1 = Math.min(py0 + 1, H - 1);

    const cw = px1 - px0 + 1;
    const ch = py1 - py0 + 1;
    const stepX = Math.max(1, Math.floor(cw / target));
    const stepY = Math.max(1, Math.floor(ch / target));

    const lons = [];
    const lats = [];
    const zg = [];
    let landMax = 0;
    for (let gy = py0; gy <= py1; gy += stepY) {
      const row = [];
      for (let gx = px0; gx <= px1; gx += stepX) {
        let v = mosaic[gy * W + gx];
        if (!isFinite(v)) v = 0;
        const land = Math.max(v, 0);
        if (land > landMax) landMax = land;
        row.push(v);
      }
      zg.push(row);
      lats.push(
        +(maxLat - ((gy - py0) / (py1 - py0 || 1)) * (maxLat - minLat)).toFixed(5)
      );
    }
    for (let gx = px0; gx <= px1; gx += stepX) {
      lons.push(
        +(minLon + ((gx - px0) / (px1 - px0 || 1)) * (maxLon - minLon)).toFixed(5)
      );
    }

    const seaZ = -Math.max(40, 0.05 * landMax);
    for (let i = 0; i < zg.length; i++) {
      for (let j = 0; j < zg[i].length; j++) {
        zg[i][j] = zg[i][j] <= 0 ? +seaZ.toFixed(1) : +zg[i][j].toFixed(1);
      }
    }

    return {
      lons,
      lats,
      z: zg,
      zmin: +seaZ.toFixed(1),
      zmax: +landMax.toFixed(1),
      sea_z: +seaZ.toFixed(1),
      zoom: z,
      shape: [zg.length, zg[0] ? zg[0].length : 0],
    };
  }

  // Port of regions.resolve_bbox using the bundled regions data.
  function resolveBbox(regionsObj, continent, country, city) {
    const cont = regionsObj[continent];
    if (!cont) throw new Error("unknown continent: " + continent);
    if (!country) return { bbox: cont.bbox.slice(), label: cont.name };
    const co = cont.countries.find((c) => c.code === country);
    if (!co) throw new Error("unknown country: " + country);
    if (!city)
      return { bbox: co.bbox.slice(), label: cont.name + " · " + co.name };
    const ci = (co.cities || []).find((c) => c.code === city);
    if (!ci) throw new Error("unknown city: " + city);
    return { bbox: ci.bbox.slice(), label: co.name + " · " + ci.name };
  }

  return { buildGrid, resolveBbox, pickZoom, tileRange };
})();
