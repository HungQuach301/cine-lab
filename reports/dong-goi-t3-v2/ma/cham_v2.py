#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 v2 việc 5 · chấm mù 10 thumbnail X01…X10 (V1…V8 + A2/B1 vòng 1) ở CỠ NHỎ: lưới 360×202 + lưới 168×94; 3 người chấm như vòng 1 (claude-sonnet-5-5).
Tiêu chí: muốn bấm, rõ, trung lập, "trông như tranh AI" (0–10; 10 = rõ là tranh AI), đọc ở 168. Ghi thumbnail/cham-mu/*.json + gop.json"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).parent)); import ai
REP = Path(__file__).resolve().parent.parent / "thumbnail"; X = REP / "xuat-dieu-phoi"; OUT = REP / "cham-mu"; OUT.mkdir(parents=True, exist_ok=True); TMP = Path(sys.argv[1]); TMP.mkdir(parents=True, exist_ok=True)
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16); IDS = [f"X{i:02d}" for i in range(1, 11)]
def sheet(sz, cols, gap):
    w, h = map(int, sz.split("x")); rows = (len(IDS) + cols - 1) // cols; S = Image.new("RGB", (cols * (w + gap) + gap, rows * (h + 26 + gap) + gap), (255, 255, 255)); D = ImageDraw.Draw(S)
    for k, t in enumerate(IDS):
        x, y = gap + (k % cols) * (w + gap), gap + (k // cols) * (h + 26 + gap); D.text((x, y), t, fill=(0, 0, 0), font=F); S.paste(Image.open(X / f"{t}-{sz}.png"), (x, y + 22))
    p = TMP / f"luoi-{sz}.png"; S.save(p); return p
s1, s2 = sheet("360x202", 2, 16), sheet("168x94", 5, 12)
P = {"R1": "You are a 34-year-old YouTube viewer in the US who watches history documentaries and 3D map/timelapse videos most evenings, mostly on your phone.",
     "R2": "You are a 41-year-old viewer from Andalusia, Spain (family in La Línea de la Concepción), fluent in English, who watches history videos on YouTube and notices immediately when imagery about Gibraltar leans British or treats Spain's view as illegitimate.",
     "R3": "You are a 58-year-old British viewer from Portsmouth, ex-Royal Navy, who has visited Gibraltar and watches naval and military history on YouTube; you notice when imagery leans Spanish, is hostile to Britain, or gets history wrong."}
Q = """{persona}

Use the Read tool to open these two images (the same 10 YouTube thumbnails, labelled X01…X10, candidates for ONE long history video about Gibraltar):
{IMAGES}
The first image shows them at phone size (360×202), the second at desktop-sidebar size (168×94). Judge them as thumbnails you meet in search results. Be discriminating; use the full range.
For each thumbnail give:
 click: how much YOU would want to click (1–10)
 clear: how clearly you understand at a glance what the video is about (1–10)
 neutral: how free of bias toward Britain or Spain (10 = fully neutral)
 ai_look: how much it looks like AI-generated art (0 = not at all, 10 = obviously AI art)
 small_legible: at 168×94, can you read the text and recognise the subject (1–10)
 note: max 15 words.
Then pick your top 3 (best first).
Return ONLY JSON: {{"items": [{{"id": "X01", "click": n, "clear": n, "neutral": n, "ai_look": n, "small_legible": n, "note": "..."}}], "top3": ["X..", "X..", "X.."]}}"""
def run(r): return r, ai.ai(Q.format(persona=P[r], IMAGES="{IMAGES}"), f"thumb-{r}", images=[str(s1), str(s2)], out=OUT)
with ThreadPoolExecutor(3) as ex: res = dict(ex.map(run, P))
C = ("click", "clear", "neutral", "ai_look", "small_legible"); agg = {t: {c: [] for c in C} | {"top3_diem": 0} for t in IDS}
for r, j in res.items():
    for it in (j or {}).get("items", []):
        if it.get("id") in agg: [agg[it["id"]][c].append(it[c]) for c in C]
    for i, t in enumerate((j or {}).get("top3", [])[:3]):
        if t in agg: agg[t]["top3_diem"] += 3 - i
k = json.load(open(REP / "khoa.json"))["khoa"]
for t, a in agg.items():
    for c in C: a[c + "_tb"] = round(sum(a[c]) / len(a[c]), 2) if a[c] else None
    a["tong_4"] = round(((a["click_tb"] or 0) + (a["clear_tb"] or 0) + (a["neutral_tb"] or 0) + (a["small_legible_tb"] or 0)) / 4, 2); a["ung_vien"] = k[t]["ung_vien"]
json.dump(agg, open(OUT / "gop.json", "w"), indent=1, ensure_ascii=False)
for t, a in sorted(agg.items(), key=lambda kv: -kv[1]["click_tb"]): print(t, a["ung_vien"], [a[c + "_tb"] for c in C], a["tong_4"], "top3", a["top3_diem"])
print("chi phí luỹ kế $%.3f" % ai.spent())
