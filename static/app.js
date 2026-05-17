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

function render(data) {
  lastData = data;
  const trace = {
    type: "surface",
    x: data.lons,
    y: data.lats,
    z: data.z,
    colorscale: els.colorscale.value,
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
      aspectratio: { x: 1.6, y: 1.2, z: aspectZ() },
      xaxis: { title: "경도", color: "#9aa4b2", backgroundcolor: "#0e1117" },
      yaxis: { title: "위도", color: "#9aa4b2", backgroundcolor: "#0e1117" },
      zaxis: { title: "고도 (m)", color: "#9aa4b2", backgroundcolor: "#0e1117" },
      camera: { eye: { x: 1.5, y: 1.5, z: 1.0 } },
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
