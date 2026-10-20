#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 1 · chấm mù 12 tiêu đề: 3 người chấm AI (claude-sonnet-5-5, thư mục trống), mỗi người một thứ tự xáo riêng, nhãn trung tính.
Tiêu chí 1–10: muốn bấm, rõ chủ đề, không thiên vị (10 = trung lập), không giật gân (10 = điềm tĩnh) + chọn 3. Ghi tieu-de/cham-mu/*.json + gop.json"""
import json, random, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import ai
OUT = Path(__file__).resolve().parent.parent / "tieu-de" / "cham-mu"
T = json.load(open(OUT.parent / "ung-vien.json"))["ung_vien"]
P = {"R1": "You are a 34-year-old YouTube viewer in the US who watches history documentaries and 3D map/timelapse videos most evenings. You click fast on what looks rewarding and skip what looks like clickbait or a lecture.",
     "R2": "You are a 41-year-old viewer from Andalusia, Spain (you have family in La Línea de la Concepción), fluent in English, who watches history videos on YouTube. You notice immediately when a title about Gibraltar leans British, treats Spain's view as illegitimate, or simplifies the dispute.",
     "R3": "You are a 58-year-old British viewer from Portsmouth, ex-Royal Navy, who has visited Gibraltar several times and watches military and naval history on YouTube. You notice immediately when a title about Gibraltar leans Spanish, sounds hostile to Britain, or gets naval history wrong."}
Q = """{persona}

You are scrolling YouTube search results. Below are candidate titles for ONE long video (10–12 minutes). Judge each title on its own, as it would appear in the results list. Be honest and discriminating; use the full 1–10 range.
For each title give:
 click: how much YOU would want to click (1–10)
 clear: how clearly you understand what the video is about and what you'd get (1–10)
 neutral: how free of bias toward either Britain or Spain (10 = fully neutral)
 calm: how free of sensationalism/clickbait (10 = not sensational at all)
 note: max 15 words.
Then pick your top 3 (ids, best first) for the video's real title.
Return ONLY JSON: {{"items": [{{"id": "...", "click": n, "clear": n, "neutral": n, "calm": n, "note": "..."}}], "top3": ["id", "id", "id"]}}

TITLES:
{titles}"""
def run(r):
    rnd = random.Random(hash(r) % 1000 + 19); items = list(T.items()); rnd.shuffle(items)
    txt = "\n".join(f"{T_ID[k]}: {v}" for k, v in items)
    return r, ai.ai(Q.format(persona=P[r], titles=txt), f"tieu-de-{r}", out=OUT)
ids = list(T); rnd0 = random.Random(1910); lab = [f"t{i:02d}" for i in range(1, len(ids) + 1)]; rnd0.shuffle(lab); T_ID = dict(zip(ids, lab))
(OUT).mkdir(parents=True, exist_ok=True); (OUT / "khoa-nhan.json").write_text(json.dumps(T_ID, indent=1))
with ThreadPoolExecutor(3) as ex: res = dict(ex.map(run, P))
inv = {v: k for k, v in T_ID.items()}; agg = {k: {"click": [], "clear": [], "neutral": [], "calm": [], "top3_diem": 0} for k in ids}
for r, j in res.items():
    for it in (j or {}).get("items", []):
        k = inv.get(it["id"]); 
        if k: [agg[k][c].append(it[c]) for c in ("click", "clear", "neutral", "calm")]
    for i, t in enumerate((j or {}).get("top3", [])[:3]):
        if t in inv: agg[inv[t]]["top3_diem"] += 3 - i
for k, a in agg.items():
    for c in ("click", "clear", "neutral", "calm"): a[c + "_tb"] = round(sum(a[c]) / len(a[c]), 2) if a[c] else None
    a["tong_4"] = round(sum(a[c + "_tb"] or 0 for c in ("click", "clear", "neutral", "calm")) / 4, 2)
json.dump({"khoa_nhan": T_ID, "gop": agg}, open(OUT / "gop.json", "w"), indent=1, ensure_ascii=False)
for k, a in sorted(agg.items(), key=lambda kv: -kv[1]["tong_4"]): print(k, a["click_tb"], a["clear_tb"], a["neutral_tb"], a["calm_tb"], a["tong_4"], a["top3_diem"], T[k])
print("chi phí luỹ kế $%.3f" % ai.spent())
