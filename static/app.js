"use strict";

const els = {
  continent: document.getElementById("continent"),
  country: document.getElementById("country"),
  colorscale: document.getElementById("colorscale"),
  exag: document.getElementById("exag"),
  exagVal: document.getElementById("exagVal"),
  load: document.getElementById("load"),
  status: document.getElementById("status"),
  plot: document.getElementById("plot"),
};

let regionsData = [];
let lastData = null;

function setStatus(msg, isError) {
  els.status.textContent = msg;
  els.status.classList.toggle("error", !!isError);
}

async function loadRegions() {
  const res = await fetch("/api/regions");
  regionsData = await res.json();
  els.continent.innerHTML = "";
  regionsData.forEach((c) => {
    const o = document.createElement("option");
    o.value = c.continent;
    o.textContent = c.label;
    els.continent.appendChild(o);
  });
  populateCountries();
}

function populateCountries() {
  const cont = regionsData.find((c) => c.continent === els.continent.value);
  els.country.innerHTML = "";
  const all = document.createElement("option");
  all.value = "";
  all.textContent = "(대륙 전체)";
  els.country.appendChild(all);
  if (!cont) return;
  cont.countries.forEach((ct) => {
    const o = document.createElement("option");
    o.value = ct.code;
    o.textContent = ct.name;
    els.country.appendChild(o);
  });
}

function aspectZ() {
  return parseFloat(els.exag.value);
}

// Geographic aspect so the top-down view is not stretched: longitude
// degrees are physically shorter than latitude by cos(latitude).
function geoAspect(bbox) {
  const [minLon, minLat, maxLon, maxLat] = bbox;
  const meanLat = ((minLat + maxLat) / 2) * (Math.PI / 180);
  const nx = Math.abs(maxLon - minLon) * Math.cos(meanLat);
  const ny = Math.abs(maxLat - minLat);
  const m = Math.max(nx, ny) || 1;
  return { x: (nx / m) * 1.8, y: (ny / m) * 1.8, z: aspectZ() };
}

// Land ramps: list of colours from low to high elevation.
const LAND_RAMPS = {
  terrain: ["#1a9850", "#a6d96a", "#fee08b", "#d8843b", "#8c5109", "#ffffff"],
  green: ["#00441b", "#238b45", "#66c2a4", "#ccece6"],
  viridis: ["#440154", "#3b528b", "#21908d", "#5dc962", "#fde725"],
  gray: ["#222222", "#666666", "#aaaaaa", "#ffffff"],
};
// Water ramp: deep -> shallow, used for everything below sea level.
const WATER_RAMP = ["#08306b", "#08519c", "#2171b5", "#6baed6"];

// Build a Plotly colorscale whose colour breaks exactly at elevation 0,
// so sea (blue) and land (terrain) are unmistakable.
function landSeaColorscale(zmin, zmax, paletteKey) {
  const land = LAND_RAMPS[paletteKey] || LAND_RAMPS.terrain;
  const span = zmax - zmin;
  let f0 = span > 0 ? (0 - zmin) / span : 0; // fraction at elevation 0
  f0 = Math.max(0, Math.min(1, f0));
  const cs = [];
  if (f0 <= 0) {
    land.forEach((c, i) => cs.push([i / (land.length - 1), c]));
    return cs;
  }
  if (f0 >= 1) {
    WATER_RAMP.forEach((c, i) => cs.push([i / (WATER_RAMP.length - 1), c]));
    return cs;
  }
  WATER_RAMP.forEach((c, i) =>
    cs.push([(i / (WATER_RAMP.length - 1)) * f0 * 0.999, c])
  );
  cs.push([f0, WATER_RAMP[WATER_RAMP.length - 1]]); // end of water band
  land.forEach((c, i) =>
    cs.push([f0 + (i / (land.length - 1)) * (1 - f0), c])
  );
  cs[0][0] = 0;
  cs[cs.length - 1][0] = 1;
  return cs;
}

function render(data) {
  lastData = data;
  const trace = {
    type: "surface",
    x: data.lons,
    y: data.lats,
    z: data.z,
    colorscale: landSeaColorscale(data.zmin, data.zmax, els.colorscale.value),
    cmin: data.zmin,
    cmax: data.zmax,
    colorbar: { title: "고도 (m)", tickfont: { color: "#cfd6e0" } },
    hovertemplate:
      "위도 %{y:.3f}°<br>경도 %{x:.3f}°<br>고도 %{z:.0f} m<extra></extra>",
    contours: { z: { show: false } },
  };
  const layout = {
    paper_bgcolor: "#0e1117",
    font: { color: "#cfd6e0" },
    margin: { l: 0, r: 0, t: 28, b: 0 },
    title: {
      text: `${data.label}  ·  고도 ${data.zmin}~${data.zmax} m  (zoom ${data.zoom})`,
      font: { size: 14 },
    },
    scene: {
      dragmode: "orbit",
      aspectmode: "manual",
      aspectratio: geoAspect(data.bbox),
      xaxis: { title: "경도 (서→동)", color: "#9aa4b2", backgroundcolor: "#0e1117" },
      yaxis: { title: "위도 (남→북)", color: "#9aa4b2", backgroundcolor: "#0e1117" },
      zaxis: { title: "고도 (m)", color: "#9aa4b2", backgroundcolor: "#0e1117" },
      // Initial view: straight down (map-like), north up / east right.
      camera: {
        eye: { x: 0, y: 0, z: 2.2 },
        up: { x: 0, y: 1, z: 0 },
        center: { x: 0, y: 0, z: 0 },
      },
    },
  };
  const config = { responsive: true, displaylogo: false, scrollZoom: true };
  Plotly.react(els.plot, [trace], layout, config);
}

async function loadElevation() {
  const continent = els.continent.value;
  const country = els.country.value;
  const params = new URLSearchParams({ continent });
  if (country) params.set("country", country);

  els.load.disabled = true;
  setStatus("고도 데이터를 불러오는 중… (타일 다운로드, 잠시 걸릴 수 있습니다)");
  try {
    const res = await fetch(`/api/elevation?${params.toString()}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
    render(data);
    const [h, w] = data.shape;
    setStatus(
      `${data.label} 표시 완료 — 격자 ${w}×${h}, 고도 ${data.zmin}~${data.zmax} m. ` +
        `드래그로 회전, 휠/핀치로 확대.`
    );
  } catch (e) {
    setStatus(`불러오기 실패: ${e.message}`, true);
  } finally {
    els.load.disabled = false;
  }
}

els.continent.addEventListener("change", populateCountries);
els.colorscale.addEventListener("change", () => {
  if (lastData) render(lastData);
});
els.exag.addEventListener("input", () => {
  els.exagVal.textContent = aspectZ().toFixed(1) + "×";
  if (lastData) {
    Plotly.relayout(els.plot, { "scene.aspectratio.z": aspectZ() });
  }
});
els.load.addEventListener("click", loadElevation);

loadRegions().catch((e) => setStatus("지역 목록 로드 실패: " + e.message, true));
