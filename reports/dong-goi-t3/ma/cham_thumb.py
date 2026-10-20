#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 2 · chấm mù 8 thumbnail T1…T8 ở CỠ NHỎ: tờ lưới 360×202 (điện thoại) + tờ lưới 168×94 (thanh bên máy tính), nhãn trung tính.
3 người chấm AI (claude-sonnet-5-5, như chấm tiêu đề). Không cho người chấm biết hướng thiết kế. Ghi thumbnail/cham-mu/*.json + gop.json"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).parent)); import ai
REP = Path(__file__).resolve().parent.parent / "thumbnail"; X = REP / "xuat-dieu-phoi"; OUT = REP / "cham-mu"; OUT.mkdir(parents=True, exist_ok=True)
TMP = Path(sys.argv[1]); TMP.mkdir(parents=True, exist_ok=True)
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
def sheet(sz, cols, gap):
    w, h = map(int, sz.split("x")); ims = [(f"T{i}", Image.open(X / f"T{i}-{sz}.png")) for i in range(1, 9)]; rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * (w + gap) + gap, rows * (h + 26 + gap) + gap), (255, 255, 255)); D = ImageDraw.Draw(S)
    for k, (lab, im) in enumerate(ims):
        x, y = gap + (k % cols) * (w + gap), gap + (k // cols) * (h + 26 + gap); D.text((x, y), lab, fill=(0, 0, 0), font=F); S.paste(im, (x, y + 22))
    p = TMP / f"luoi-{sz}.png"; S.save(p); return p
s1, s2 = sheet("360x202", 2, 16), sheet("168x94", 4, 12)
P = {"R1": "You are a 34-year-old YouTube viewer in the US who watches history documentaries and 3D map/timelapse videos most evenings, mostly on your phone.",
     "R2": "You are a 41-year-old viewer from Andalusia, Spain (family in La Línea de la Concepción), fluent in English, who watches history videos on YouTube and notices immediately when imagery about Gibraltar leans British or treats Spain's view as illegitimate.",
     "R3": "You are a 58-year-old British viewer from Portsmouth, ex-Royal Navy, who has visited Gibraltar and watches naval and military history on YouTube; you notice when imagery leans Spanish, is hostile to Britain, or gets history wrong."}
Q = """{persona}

Use the Read tool to open these two images (the same 8 YouTube thumbnails, labelled T1…T8, for ONE long history video about Gibraltar):
{IMAGES}
The first image shows them at phone size (360×202), the second at desktop-sidebar size (168×94). Judge them as thumbnails you meet in search results. Be discriminating; use the full 1–10 range.
For each thumbnail give:
 click: how much YOU would want to click (1–10)
 clear: how clearly you understand at a glance what the video is about (1–10)
 neutral: how free of bias toward Britain or Spain (10 = fully neutral)
 calm: how free of sensationalism/clickbait (10 = not sensational)
 small_legible: at 168×94, can you read any text and recognise the subject (1–10; give 10 if there is no text and the subject is clear)
 reads_as_3d_timelapse: true/false (does it signal a 3D timelapse / reconstruction video)
 note: max 15 words.
Then pick your top 3 (best first).
Return ONLY JSON: {{"items": [{{"id": "T1", "click": n, "clear": n, "neutral": n, "calm": n, "small_legible": n, "reads_as_3d_timelapse": true, "note": "..."}}], "top3": ["T?", "T?", "T?"]}}"""
def run(r): return r, ai.ai(Q.format(persona=P[r], IMAGES="{IMAGES}"), f"thumb-{r}", images=[str(s1), str(s2)], out=OUT)
with ThreadPoolExecutor(3) as ex: res = dict(ex.map(run, P))
C = ("click", "clear", "neutral", "calm", "small_legible"); agg = {f"T{i}": {c: [] for c in C} | {"ts3d": 0, "top3_diem": 0} for i in range(1, 9)}
for r, j in res.items():
    for it in (j or {}).get("items", []):
        a = agg.get(it["id"])
        if a: [a[c].append(it[c]) for c in C]; a["ts3d"] += bool(it.get("reads_as_3d_timelapse"))
    for i, t in enumerate((j or {}).get("top3", [])[:3]):
        if t in agg: agg[t]["top3_diem"] += 3 - i
for t, a in agg.items():
    for c in C: a[c + "_tb"] = round(sum(a[c]) / len(a[c]), 2) if a[c] else None
    a["tong_5"] = round(sum(a[c + "_tb"] or 0 for c in C) / 5, 2)
json.dump(agg, open(OUT / "gop.json", "w"), indent=1, ensure_ascii=False)
for t, a in sorted(agg.items(), key=lambda kv: -kv[1]["tong_5"]): print(t, [a[c + "_tb"] for c in C], a["tong_5"], "3D", a["ts3d"], "top3", a["top3_diem"])
print("chi phí luỹ kế $%.3f" % ai.spent())
