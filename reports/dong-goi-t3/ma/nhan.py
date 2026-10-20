#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 0 · gắn nhãn bằng mô hình (claude-sonnet-5-5): (a) bố cục thumbnail trên tờ lưới 12 ảnh; (b) đặc trưng tiêu đề.
Đầu vào/ra thô ở thư mục tạm (có tiêu đề + ảnh đối thủ); repo chỉ nhận nhãn đã gộp theo video_id (dactrung.py)."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import ai
T = Path(sys.argv[1]); order = json.load(open(T / "order.json")); raw = {v["id"]: v for v in json.load(open(T / "videos-raw.json"))}
sheets = sorted((T.parent / "sheets").glob("s*.jpg"))
PV = """You label YouTube thumbnails for a quantitative packaging study. Read each image file listed below with the Read tool. Each is a grid of up to 12 thumbnails, each labelled #N above it.
{IMAGES}
For EVERY thumbnail #N visible, return one JSON object. Be literal; judge what is visible at a glance.
Fields:
 "n": int,
 "style": "3d_render" | "photo" | "flat_map" | "illustration_2d" | "ai_painting" | "game_screenshot" | "other",
 "aerial_city_fills_frame": bool  (a city/town seen from above fills most of the frame),
 "focus": "single_object" | "panorama" | "person_face" | "map" | "text_dominant" | "split" ,
 "split_then_now": bool (frame split into two eras/states side by side or diagonally),
 "year_band": bool (visible text of a year or year range like 1500 → 2026 / 0 to 2026),
 "big_place_name": bool (a place name in large letters),
 "night_or_dark": bool, "fire_or_smoke": bool, "flag_prominent": bool (a national flag is a main visual element),
 "conflict_imagery": bool (weapons, soldiers, battle, siege, explosions),
 "arrow_or_circle": bool, "sky_frac": number 0..1 rounded to 0.1 (share of frame that is sky),
 "dominant_palette": "warm" | "cool" | "neutral" | "mixed"
Return ONLY a JSON array of objects, ordered by n."""
PT = """You extract features from YouTube video titles for a quantitative packaging study (history / cities / timelapse / siege / border niche).
For each numbered title return one JSON object:
 "n": int,
 "on_topic": bool (true if the video is a non-fiction documentary/explainer/timelapse about real places, cities, history, wars, borders or sieges; false for video games, fiction, music, movies, Minecraft/city-builder games, product trailers),
 "lane": "timelapse_3d" | "history_explainer" | "battle_siege" | "travel_facts" | "other",
 "first_word": the first word (lowercased, no punctuation),
 "place_word_index": int or null (1-based index of the first word that is a real place name: city, country, region, rock, strait),
 "question": bool (title asks a question, with or without '?'),
 "opens_with": "why" | "how" | "what" | "place" | "number" | "year" | "evolution_of" | "the" | "other",
 "promise": "visual" (promises to SHOW change/growth/animation: timelapse, 3D, watch it grow, brought to life) | "story" (promises to EXPLAIN why/how/what happened) | "both" | "other",
 "conflict_word": bool (siege, war, battle, fought, attack, conquer, invasion, survive, fall),
 "ownership_contest": bool (promises who owns / changed hands / why contested / why fought over / why still British etc.),
 "growth_word": bool (grow, growth, evolution, rise, built, became),
 "format_tag": bool (title carries a format label such as '3D Timelapse', 'Animated', 'Explained', 'Documentary', '4K', 'No AI'),
 "separator": "pipe" | "dash" | "colon" | "none"
Return ONLY a JSON array ordered by n.
TITLES:
"""
def vis():
    out = []
    for i in range(0, len(sheets), 4):
        j = ai.ai(PV, f"nhan-anh-{i // 4}", images=[str(p) for p in sheets[i:i + 4]], out=T / "nhan")
        out += j or []
    return out
def tit():
    txt = "\n".join(f"{n}. {raw[v]['title']}" for n, v in enumerate(order))
    return ai.ai(PT + txt, "nhan-tieu-de", out=T / "nhan") or []
with ThreadPoolExecutor(2) as ex: a, b = ex.submit(vis), ex.submit(tit); A, B = a.result(), b.result()
json.dump({"anh": A, "tieu_de": B}, open(T / "nhan.json", "w"), indent=1, ensure_ascii=False)
print(len(A), "nhãn ảnh;", len(B), "nhãn tiêu đề; chi phí luỹ kế $%.3f" % ai.spent())
