#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 v2 việc 6 · kiểm tiêu đề c5 với nội dung phim (mở đầu V7B) + chấm mù 6 biến thể: 3 người chấm (claude-sonnet-5-5) được đọc TÓM TẮT TRUNG THỰC nội dung phim
(do P viết từ V7B §6 + lời khoá v4.2) rồi chấm: muốn bấm, rõ, lời hứa khớp nội dung (10 = khớp hoàn toàn), trung lập. Ghi tieu-de/*.json"""
import json, random, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import ai
OUT = Path(__file__).resolve().parent.parent / "tieu-de"
T = {"c5": "Gibraltar: 14 Sieges in 3D | Timelapse 1309–2026", "c1": "Gibraltar Under Siege: 1309 → 1783 | 3D Timelapse",
     "k1": "Gibraltar: From 14 Sieges to a Runway | 3D Timelapse", "k2": "Gibraltar, 1309–2026: 14 Sieges, Then a Runway | 3D",
     "k3": "Gibraltar: 700 Years Fought Over, in 3D | 1309–2026", "a2": "Why Gibraltar Was Besieged 14 Times"}
SYN = """WHAT THE VIDEO ACTUALLY CONTAINS (11–12 minutes, 3D timelapse reconstruction, narrated):
- Opening (first ~45 s): Gibraltar's border at night in 2026; then a fixed 3D view of the Rock steps back through time year by year — 1309, 1316, 1333, 1350, 1411, 1436, 1462, 1467, 1506, 1704, 1705, 1727, 1779 — with a puff of smoke over the town at each siege year (about half a second each), then the night of 13 September 1782 when ten floating batteries burn in the bay.
- Chapter 1: the 1704 capture and the 1713 Treaty of Utrecht (≈ 2 min).
- Chapter 2: the Great Siege 1779–83 in detail (≈ 3.5 min).
- Chapter 3: the neutral ground and the 1909 fence (≈ 1.5 min).
- Chapter 4: the airstrip and runway built across the isthmus 1934–1943, WWII (≈ 2 min).
- Chapter 5: the border closure 1969–85, today's cross-border workers, the 2026 UK–EU treaty (≈ 2 min).
Only two sieges (1704 and 1779–83) are shown at length; the other twelve appear only as brief counter steps with smoke."""
P = {"R1": "You are a 34-year-old YouTube viewer in the US who watches history documentaries and 3D timelapse videos.",
     "R2": "You are a 41-year-old viewer from Andalusia, Spain, fluent in English, who watches history videos and dislikes titles that oversell.",
     "R3": "You are a 58-year-old British ex-Royal Navy viewer who watches military history and dislikes titles that promise battles a video doesn't show."}
Q = """{persona}

{syn}

Candidate titles for this video:
{titles}

For each title give: click (1–10, would you click it in search results), clear (1–10), promise_match (1–10: does the title promise what the video above actually delivers; 10 = exactly), neutral (1–10, free of bias toward Britain or Spain), note (≤ 15 words).
Then pick the best title for this video (best first, top 3).
Return ONLY JSON: {{"items": [{{"id": "...", "click": n, "clear": n, "promise_match": n, "neutral": n, "note": "..."}}], "top3": ["..", "..", ".."]}}"""
ids = list(T); lab = [f"t{i}" for i in range(1, len(ids) + 1)]; random.Random(7).shuffle(lab); K = dict(zip(ids, lab)); inv = {v: k for k, v in K.items()}
def run(r):
    it = list(T.items()); random.Random(hash(r) % 97).shuffle(it)
    return r, ai.ai(Q.format(persona=P[r], syn=SYN, titles="\n".join(f"{K[k]}: {v}" for k, v in it)), f"c5-{r}", out=OUT)
with ThreadPoolExecutor(3) as ex: res = dict(ex.map(run, P))
C = ("click", "clear", "promise_match", "neutral"); agg = {k: {c: [] for c in C} | {"top3_diem": 0, "tieu_de": T[k], "ky_tu": len(T[k])} for k in ids}
for r, j in res.items():
    for x in (j or {}).get("items", []):
        k = inv.get(x.get("id"))
        if k: [agg[k][c].append(x[c]) for c in C]
    for i, t in enumerate((j or {}).get("top3", [])[:3]):
        if t in inv: agg[inv[t]]["top3_diem"] += 3 - i
for k, a in agg.items():
    for c in C: a[c + "_tb"] = round(sum(a[c]) / len(a[c]), 2) if a[c] else None
json.dump({"tom_tat_noi_dung": SYN, "khoa_nhan": K, "gop": agg}, open(OUT / "kiem-c5.json", "w"), indent=1, ensure_ascii=False)
for k, a in sorted(agg.items(), key=lambda kv: -(kv[1]["promise_match_tb"] or 0)): print(k, a["ky_tu"], [a[c + "_tb"] for c in C], "top3", a["top3_diem"], a["tieu_de"])
print("chi phí luỹ kế $%.3f" % ai.spent())
