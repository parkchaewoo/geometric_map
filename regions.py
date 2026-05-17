"""Continent -> country region data.

Each bbox is (min_lon, min_lat, max_lon, max_lat) in WGS84 degrees.
Selecting only a continent uses the continent bbox (coarse, whole continent).
Selecting a country uses that country's bbox (detailed).
"""

REGIONS = {
    "Asia": {
        "name": "아시아",
        "bbox": [25.0, -11.0, 180.0, 78.0],
        "countries": [
            {"code": "KR", "name": "대한민국", "bbox": [124.5, 33.0, 131.9, 38.7]},
            {"code": "JP", "name": "일본", "bbox": [122.9, 24.0, 146.0, 45.6]},
            {"code": "CN", "name": "중국", "bbox": [73.5, 18.2, 135.1, 53.6]},
            {"code": "IN", "name": "인도", "bbox": [68.1, 6.7, 97.4, 35.5]},
            {"code": "NP", "name": "네팔", "bbox": [80.0, 26.3, 88.2, 30.5]},
            {"code": "MN", "name": "몽골", "bbox": [87.7, 41.5, 119.9, 52.2]},
            {"code": "ID", "name": "인도네시아", "bbox": [95.0, -11.0, 141.0, 6.1]},
        ],
    },
    "Europe": {
        "name": "유럽",
        "bbox": [-25.0, 34.0, 45.0, 71.5],
        "countries": [
            {"code": "CH", "name": "스위스", "bbox": [5.9, 45.8, 10.5, 47.8]},
            {"code": "FR", "name": "프랑스", "bbox": [-5.2, 41.3, 9.6, 51.1]},
            {"code": "IT", "name": "이탈리아", "bbox": [6.6, 36.6, 18.5, 47.1]},
            {"code": "NO", "name": "노르웨이", "bbox": [4.6, 57.9, 31.1, 71.2]},
            {"code": "ES", "name": "스페인", "bbox": [-9.3, 36.0, 3.3, 43.8]},
            {"code": "GB", "name": "영국", "bbox": [-8.6, 49.9, 1.8, 60.9]},
            {"code": "DE", "name": "독일", "bbox": [5.9, 47.3, 15.0, 55.1]},
        ],
    },
    "Africa": {
        "name": "아프리카",
        "bbox": [-18.0, -35.0, 52.0, 38.0],
        "countries": [
            {"code": "TZ", "name": "탄자니아", "bbox": [29.3, -11.8, 40.5, -0.9]},
            {"code": "ZA", "name": "남아프리카공화국", "bbox": [16.3, -34.9, 32.9, -22.0]},
            {"code": "ET", "name": "에티오피아", "bbox": [32.9, 3.4, 48.0, 14.9]},
            {"code": "EG", "name": "이집트", "bbox": [24.6, 21.7, 36.9, 31.7]},
            {"code": "MA", "name": "모로코", "bbox": [-13.2, 27.6, -0.9, 35.9]},
            {"code": "KE", "name": "케냐", "bbox": [33.9, -4.7, 41.9, 5.5]},
        ],
    },
    "North America": {
        "name": "북아메리카",
        "bbox": [-168.0, 7.0, -52.0, 72.0],
        "countries": [
            {"code": "US", "name": "미국 (본토)", "bbox": [-125.0, 24.5, -66.9, 49.4]},
            {"code": "CA", "name": "캐나다", "bbox": [-141.0, 41.7, -52.6, 70.0]},
            {"code": "MX", "name": "멕시코", "bbox": [-118.4, 14.5, -86.7, 32.7]},
            {"code": "CR", "name": "코스타리카", "bbox": [-85.9, 8.0, -82.6, 11.2]},
            {"code": "GL", "name": "그린란드", "bbox": [-73.0, 59.7, -12.0, 83.6]},
        ],
    },
    "South America": {
        "name": "남아메리카",
        "bbox": [-82.0, -56.0, -34.0, 13.0],
        "countries": [
            {"code": "PE", "name": "페루", "bbox": [-81.4, -18.4, -68.7, -0.0]},
            {"code": "CL", "name": "칠레", "bbox": [-75.7, -55.9, -66.4, -17.5]},
            {"code": "AR", "name": "아르헨티나", "bbox": [-73.6, -55.1, -53.6, -21.8]},
            {"code": "BR", "name": "브라질", "bbox": [-74.0, -33.8, -34.8, 5.3]},
            {"code": "BO", "name": "볼리비아", "bbox": [-69.7, -22.9, -57.5, -9.7]},
            {"code": "EC", "name": "에콰도르", "bbox": [-81.1, -5.0, -75.2, 1.5]},
        ],
    },
    "Oceania": {
        "name": "오세아니아",
        "bbox": [110.0, -48.0, 180.0, 0.0],
        "countries": [
            {"code": "AU", "name": "호주", "bbox": [112.9, -43.7, 153.7, -10.1]},
            {"code": "NZ", "name": "뉴질랜드", "bbox": [166.4, -47.3, 178.6, -34.4]},
            {"code": "PG", "name": "파푸아뉴기니", "bbox": [140.8, -11.7, 156.0, -1.0]},
            {"code": "FJ", "name": "피지", "bbox": [177.0, -19.2, 180.0, -16.0]},
        ],
    },
    "Antarctica": {
        "name": "남극",
        "bbox": [-180.0, -85.0, 180.0, -60.0],
        "countries": [
            {"code": "AP", "name": "남극반도", "bbox": [-65.0, -71.0, -55.0, -63.0]},
        ],
    },
}


def list_regions():
    """Return a UI-friendly structure of continents and their countries."""
    out = []
    for cont_key, cont in REGIONS.items():
        out.append(
            {
                "continent": cont_key,
                "label": cont["name"],
                "countries": [
                    {"code": c["code"], "name": c["name"]}
                    for c in cont["countries"]
                ],
            }
        )
    return out


def resolve_bbox(continent, country=None):
    """Resolve a (continent[, country]) selection to a bbox.

    Returns (bbox, label) or raises KeyError / ValueError.
    """
    if continent not in REGIONS:
        raise KeyError(f"unknown continent: {continent}")
    cont = REGIONS[continent]
    if not country:
        return list(cont["bbox"]), cont["name"]
    for c in cont["countries"]:
        if c["code"] == country:
            return list(c["bbox"]), f"{cont['name']} · {c['name']}"
    raise ValueError(f"unknown country '{country}' in {continent}")
