"""Continent -> country -> city region data.

Each bbox is (min_lon, min_lat, max_lon, max_lat) in WGS84 degrees.
Selection precedence: city (tight, high detail) > country > continent (coarse).
"""

REGIONS = {
    "Asia": {
        "name": "아시아",
        "bbox": [25.0, -11.0, 180.0, 78.0],
        "countries": [
            {"code": "KR", "name": "대한민국", "bbox": [124.5, 33.0, 131.9, 38.7],
             "cities": [
                 {"code": "SEOUL", "name": "서울", "bbox": [126.76, 37.42, 127.18, 37.70]},
                 {"code": "BUSAN", "name": "부산", "bbox": [128.95, 35.05, 129.25, 35.30]},
                 {"code": "JEJU", "name": "제주·한라산", "bbox": [126.30, 33.20, 126.75, 33.55]},
                 {"code": "SEORAK", "name": "속초·설악산", "bbox": [128.30, 38.05, 128.65, 38.30]},
             ]},
            {"code": "JP", "name": "일본", "bbox": [122.9, 24.0, 146.0, 45.6],
             "cities": [
                 {"code": "TOKYO", "name": "도쿄", "bbox": [139.55, 35.55, 139.92, 35.82]},
                 {"code": "FUJI", "name": "후지산", "bbox": [138.55, 35.25, 138.90, 35.50]},
             ]},
            {"code": "CN", "name": "중국", "bbox": [73.5, 18.2, 135.1, 53.6],
             "cities": [
                 {"code": "BEIJING", "name": "베이징", "bbox": [116.10, 39.70, 116.70, 40.10]},
                 {"code": "SHANGHAI", "name": "상하이", "bbox": [121.20, 31.05, 121.70, 31.45]},
             ]},
            {"code": "IN", "name": "인도", "bbox": [68.1, 6.7, 97.4, 35.5],
             "cities": [
                 {"code": "DELHI", "name": "델리", "bbox": [76.95, 28.40, 77.45, 28.85]},
                 {"code": "MUMBAI", "name": "뭄바이", "bbox": [72.70, 18.90, 73.05, 19.30]},
             ]},
            {"code": "NP", "name": "네팔", "bbox": [80.0, 26.3, 88.2, 30.5],
             "cities": [
                 {"code": "KTM", "name": "카트만두", "bbox": [85.10, 27.55, 85.55, 27.85]},
                 {"code": "EVEREST", "name": "에베레스트", "bbox": [86.70, 27.80, 87.15, 28.20]},
             ]},
            {"code": "MN", "name": "몽골", "bbox": [87.7, 41.5, 119.9, 52.2],
             "cities": [
                 {"code": "ULN", "name": "울란바토르", "bbox": [106.60, 47.75, 107.25, 48.10]},
             ]},
            {"code": "ID", "name": "인도네시아", "bbox": [95.0, -11.0, 141.0, 6.1],
             "cities": [
                 {"code": "JAKARTA", "name": "자카르타", "bbox": [106.65, -6.40, 107.10, -6.05]},
                 {"code": "BALI", "name": "발리·아궁산", "bbox": [114.95, -8.55, 115.45, -8.10]},
             ]},
        ],
    },
    "Europe": {
        "name": "유럽",
        "bbox": [-25.0, 34.0, 45.0, 71.5],
        "countries": [
            {"code": "CH", "name": "스위스", "bbox": [5.9, 45.8, 10.5, 47.8],
             "cities": [
                 {"code": "ZRH", "name": "취리히", "bbox": [8.35, 47.25, 8.75, 47.50]},
                 {"code": "MATTERHORN", "name": "체르마트·마터호른", "bbox": [7.55, 45.90, 7.95, 46.15]},
             ]},
            {"code": "FR", "name": "프랑스", "bbox": [-5.2, 41.3, 9.6, 51.1],
             "cities": [
                 {"code": "PARIS", "name": "파리", "bbox": [2.10, 48.70, 2.60, 49.00]},
                 {"code": "MONTBLANC", "name": "샤모니·몽블랑", "bbox": [6.65, 45.78, 7.10, 46.05]},
             ]},
            {"code": "IT", "name": "이탈리아", "bbox": [6.6, 36.6, 18.5, 47.1],
             "cities": [
                 {"code": "ROME", "name": "로마", "bbox": [12.30, 41.75, 12.75, 42.05]},
                 {"code": "VENICE", "name": "베네치아", "bbox": [12.20, 45.30, 12.55, 45.55]},
             ]},
            {"code": "NO", "name": "노르웨이", "bbox": [4.6, 57.9, 31.1, 71.2],
             "cities": [
                 {"code": "OSLO", "name": "오슬로", "bbox": [10.55, 59.78, 11.00, 60.05]},
                 {"code": "BERGEN", "name": "베르겐·피오르드", "bbox": [5.10, 60.25, 5.60, 60.55]},
             ]},
            {"code": "ES", "name": "스페인", "bbox": [-9.3, 36.0, 3.3, 43.8],
             "cities": [
                 {"code": "MADRID", "name": "마드리드", "bbox": [-3.95, 40.25, -3.50, 40.60]},
                 {"code": "BCN", "name": "바르셀로나", "bbox": [1.95, 41.25, 2.45, 41.55]},
             ]},
            {"code": "GB", "name": "영국", "bbox": [-8.6, 49.9, 1.8, 60.9],
             "cities": [
                 {"code": "LONDON", "name": "런던", "bbox": [-0.40, 51.35, 0.15, 51.65]},
                 {"code": "EDIN", "name": "에든버러", "bbox": [-3.45, 55.85, -2.95, 56.05]},
             ]},
            {"code": "DE", "name": "독일", "bbox": [5.9, 47.3, 15.0, 55.1],
             "cities": [
                 {"code": "BERLIN", "name": "베를린", "bbox": [13.20, 52.38, 13.65, 52.65]},
                 {"code": "MUNICH", "name": "뮌헨·알프스", "bbox": [11.35, 48.00, 11.80, 48.30]},
             ]},
        ],
    },
    "Africa": {
        "name": "아프리카",
        "bbox": [-18.0, -35.0, 52.0, 38.0],
        "countries": [
            {"code": "TZ", "name": "탄자니아", "bbox": [29.3, -11.8, 40.5, -0.9],
             "cities": [
                 {"code": "DAR", "name": "다르에스살람", "bbox": [39.10, -6.95, 39.50, -6.60]},
                 {"code": "KILI", "name": "킬리만자로", "bbox": [37.15, -3.25, 37.60, -2.90]},
             ]},
            {"code": "ZA", "name": "남아프리카공화국", "bbox": [16.3, -34.9, 32.9, -22.0],
             "cities": [
                 {"code": "CPT", "name": "케이프타운·테이블산", "bbox": [18.25, -34.10, 18.65, -33.75]},
                 {"code": "JNB", "name": "요하네스버그", "bbox": [27.85, -26.35, 28.30, -26.05]},
             ]},
            {"code": "ET", "name": "에티오피아", "bbox": [32.9, 3.4, 48.0, 14.9],
             "cities": [
                 {"code": "ADD", "name": "아디스아바바", "bbox": [38.55, 8.85, 39.00, 9.20]},
             ]},
            {"code": "EG", "name": "이집트", "bbox": [24.6, 21.7, 36.9, 31.7],
             "cities": [
                 {"code": "CAIRO", "name": "카이로", "bbox": [31.05, 29.90, 31.50, 30.20]},
             ]},
            {"code": "MA", "name": "모로코", "bbox": [-13.2, 27.6, -0.9, 35.9],
             "cities": [
                 {"code": "MARRA", "name": "마라케시·아틀라스", "bbox": [-8.20, 31.10, -7.55, 31.80]},
                 {"code": "RABAT", "name": "라바트", "bbox": [-7.05, 33.90, -6.60, 34.15]},
             ]},
            {"code": "KE", "name": "케냐", "bbox": [33.9, -4.7, 41.9, 5.5],
             "cities": [
                 {"code": "NAIROBI", "name": "나이로비", "bbox": [36.65, -1.45, 37.05, -1.10]},
             ]},
        ],
    },
    "North America": {
        "name": "북아메리카",
        "bbox": [-168.0, 7.0, -52.0, 72.0],
        "countries": [
            {"code": "US", "name": "미국 (본토)", "bbox": [-125.0, 24.5, -66.9, 49.4],
             "cities": [
                 {"code": "NYC", "name": "뉴욕", "bbox": [-74.20, 40.55, -73.75, 40.90]},
                 {"code": "SF", "name": "샌프란시스코", "bbox": [-122.55, 37.65, -122.30, 37.90]},
                 {"code": "GRANDCNY", "name": "그랜드캐니언", "bbox": [-112.40, 35.95, -111.90, 36.30]},
                 {"code": "ROCKIES", "name": "콜로라도 로키", "bbox": [-105.90, 39.50, -105.20, 39.95]},
             ]},
            {"code": "CA", "name": "캐나다", "bbox": [-141.0, 41.7, -52.6, 70.0],
             "cities": [
                 {"code": "TORONTO", "name": "토론토", "bbox": [-79.60, 43.55, -79.15, 43.80]},
                 {"code": "VAN", "name": "밴쿠버", "bbox": [-123.30, 49.15, -122.80, 49.40]},
                 {"code": "BANFF", "name": "밴프·로키산맥", "bbox": [-115.90, 51.00, -115.20, 51.40]},
             ]},
            {"code": "MX", "name": "멕시코", "bbox": [-118.4, 14.5, -86.7, 32.7],
             "cities": [
                 {"code": "CDMX", "name": "멕시코시티", "bbox": [-99.35, 19.25, -98.90, 19.60]},
             ]},
            {"code": "CR", "name": "코스타리카", "bbox": [-85.9, 8.0, -82.6, 11.2],
             "cities": [
                 {"code": "SJO", "name": "산호세", "bbox": [-84.30, 9.80, -83.85, 10.10]},
             ]},
            {"code": "GL", "name": "그린란드", "bbox": [-73.0, 59.7, -12.0, 83.6],
             "cities": [
                 {"code": "NUUK", "name": "누크", "bbox": [-52.10, 64.05, -51.30, 64.35]},
             ]},
        ],
    },
    "South America": {
        "name": "남아메리카",
        "bbox": [-82.0, -56.0, -34.0, 13.0],
        "countries": [
            {"code": "PE", "name": "페루", "bbox": [-81.4, -18.4, -68.7, -0.0],
             "cities": [
                 {"code": "LIMA", "name": "리마", "bbox": [-77.20, -12.20, -76.85, -11.90]},
                 {"code": "CUSCO", "name": "쿠스코·안데스", "bbox": [-72.20, -13.70, -71.70, -13.30]},
             ]},
            {"code": "CL", "name": "칠레", "bbox": [-75.7, -55.9, -66.4, -17.5],
             "cities": [
                 {"code": "SCL", "name": "산티아고·안데스", "bbox": [-70.85, -33.60, -70.10, -33.20]},
             ]},
            {"code": "AR", "name": "아르헨티나", "bbox": [-73.6, -55.1, -53.6, -21.8],
             "cities": [
                 {"code": "BA", "name": "부에노스아이레스", "bbox": [-58.60, -34.75, -58.20, -34.45]},
                 {"code": "BARILOCHE", "name": "바릴로체·안데스", "bbox": [-71.60, -41.30, -71.00, -40.95]},
             ]},
            {"code": "BR", "name": "브라질", "bbox": [-74.0, -33.8, -34.8, 5.3],
             "cities": [
                 {"code": "RIO", "name": "리우데자네이루", "bbox": [-43.45, -23.05, -42.95, -22.75]},
                 {"code": "SP", "name": "상파울루", "bbox": [-46.85, -23.70, -46.40, -23.40]},
             ]},
            {"code": "BO", "name": "볼리비아", "bbox": [-69.7, -22.9, -57.5, -9.7],
             "cities": [
                 {"code": "LPB", "name": "라파스·안데스", "bbox": [-68.35, -16.65, -67.90, -16.35]},
             ]},
            {"code": "EC", "name": "에콰도르", "bbox": [-81.1, -5.0, -75.2, 1.5],
             "cities": [
                 {"code": "UIO", "name": "키토·안데스", "bbox": [-78.65, -0.35, -78.30, 0.00]},
             ]},
        ],
    },
    "Oceania": {
        "name": "오세아니아",
        "bbox": [110.0, -48.0, 180.0, 0.0],
        "countries": [
            {"code": "AU", "name": "호주", "bbox": [112.9, -43.7, 153.7, -10.1],
             "cities": [
                 {"code": "SYD", "name": "시드니", "bbox": [151.00, -34.05, 151.45, -33.70]},
                 {"code": "MEL", "name": "멜버른", "bbox": [144.75, -37.95, 145.20, -37.65]},
             ]},
            {"code": "NZ", "name": "뉴질랜드", "bbox": [166.4, -47.3, 178.6, -34.4],
             "cities": [
                 {"code": "AKL", "name": "오클랜드", "bbox": [174.55, -37.00, 175.00, -36.70]},
                 {"code": "QUEENS", "name": "퀸스타운·남알프스", "bbox": [168.40, -45.20, 168.95, -44.85]},
             ]},
            {"code": "PG", "name": "파푸아뉴기니", "bbox": [140.8, -11.7, 156.0, -1.0],
             "cities": [
                 {"code": "POM", "name": "포트모르즈비", "bbox": [147.00, -9.60, 147.40, -9.25]},
             ]},
            {"code": "FJ", "name": "피지", "bbox": [177.0, -19.2, 180.0, -16.0],
             "cities": [
                 {"code": "SUVA", "name": "수바", "bbox": [178.30, -18.25, 178.60, -18.00]},
             ]},
        ],
    },
    "Antarctica": {
        "name": "남극",
        "bbox": [-180.0, -85.0, 180.0, -60.0],
        "countries": [
            {"code": "AP", "name": "남극반도", "bbox": [-65.0, -71.0, -55.0, -63.0],
             "cities": []},
        ],
    },
}


def list_regions():
    """Return a UI-friendly structure of continents, countries and cities."""
    out = []
    for cont_key, cont in REGIONS.items():
        out.append(
            {
                "continent": cont_key,
                "label": cont["name"],
                "countries": [
                    {
                        "code": c["code"],
                        "name": c["name"],
                        "cities": [
                            {"code": ct["code"], "name": ct["name"]}
                            for ct in c.get("cities", [])
                        ],
                    }
                    for c in cont["countries"]
                ],
            }
        )
    return out


def resolve_bbox(continent, country=None, city=None):
    """Resolve a (continent[, country[, city]]) selection to a bbox.

    Returns (bbox, label). Raises KeyError / ValueError on bad input.
    """
    if continent not in REGIONS:
        raise KeyError(f"unknown continent: {continent}")
    cont = REGIONS[continent]
    if not country:
        return list(cont["bbox"]), cont["name"]
    country_obj = next(
        (c for c in cont["countries"] if c["code"] == country), None
    )
    if country_obj is None:
        raise ValueError(f"unknown country '{country}' in {continent}")
    if not city:
        return list(country_obj["bbox"]), f"{cont['name']} · {country_obj['name']}"
    city_obj = next(
        (ct for ct in country_obj.get("cities", []) if ct["code"] == city), None
    )
    if city_obj is None:
        raise ValueError(f"unknown city '{city}' in {country}")
    return (
        list(city_obj["bbox"]),
        f"{country_obj['name']} · {city_obj['name']}",
    )
