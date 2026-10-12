#!/opt/cine/bin/python
"""K2C-T1-06 · tính timeline ước của shot list (151,2 từ/phút, Eric) và đo các luật kênh 2 ở G1a — tự đo của phiên P, KHÔNG phải checks/.
  shotlist.py [shots.yaml]   → in bảng + ghi SHOTLIST.md
Đo: tỷ lệ card ("the") ≤ 25 % và ≤ 90 s liên tục; ảnh+tài liệu+footage ≤ 40 %, mỗi clip ≤ 8 s, document ≤ 3 s;
cùng (scene_id, camera_id) ≤ 2 lần xuất hiện; số neo hiện bằng chart3d/scene3d ≥ 60 %; mỗi địa danh có shot map; mỗi người có photo hoặc ly_do;
bối cảnh 3D ≤ 25 % và ≤ 90 s liên tục; nửa sau ≥ 3 bối cảnh (BAI-HOC #96, K6)."""
import re, sys, yaml
from collections import defaultdict
from pathlib import Path

H = Path(__file__).resolve().parent
spec = yaml.safe_load(open(sys.argv[1] if len(sys.argv) > 1 else H / "shots.yaml"))
WPS = spec["wpm"] / 60.0
PAUSE = 0.6                        # lặng giữa đoạn (ước)
script = (H / spec["script"]).read_text()

def words(t):
    t = re.sub(r"\{C[^}]*\}", "", t)
    return re.findall(r"[A-Za-z0-9'’\-.,%$]+", t)

segtext = {}
for seg in re.split(r"(?=\[\d\d )", script)[1:]:
    segtext[seg[1:3]] = words(seg.split("]", 1)[1])

def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())

def find(ws, phrase):
    n = 1
    if "#" in phrase: phrase, n = phrase.split("#"); n = int(n)
    p = [norm(x) for x in phrase.split()]
    hits = [i for i in range(len(ws)) if [norm(x) for x in ws[i:i + len(p)]] == p]
    if len(hits) < n: raise SystemExit(f"không thấy mốc '{phrase}'")
    return hits[n - 1]

rows, t = [], 0.0
for seg in spec["segments"]:
    ws = segtext[seg["id"]]; dur = len(ws) / WPS
    starts = [find(ws, s["at"]) / WPS for s in seg["shots"]]
    if starts != sorted(starts) or starts[0] != 0: raise SystemExit(f"đoạn {seg['id']}: mốc sai thứ tự hoặc shot đầu không ở 0: {starts}")
    ends = starts[1:] + [dur + PAUSE]
    for s, a, b in zip(seg["shots"], starts, ends):
        rows.append(dict(s, seg=seg["id"], t0=t + a, t1=t + b, d=b - a))
    t += dur + PAUSE
T = t

def pct(x): return 100 * x / T
by = defaultdict(float)
for r in rows: by[r["type"]] += r["d"]
ext = sum(by[k] for k in ("photo", "document", "footage"))
out = [f"# K2C-T1-06 — SHOT LIST (ước) · {spec['script']}", "",
       f"> Tự đo của phiên P từ `shots.yaml` bằng `shotlist.py` (151,2 từ/phút, lặng {PAUSE} s/đoạn). **Không phải kết quả checks/**; checks 1.10.1 chạy trên đặc tả `episode.yaml` khi dựng.",
       f"> Tổng ước: **{T/60:.2f} phút** ({T:.0f} s), {len(rows)} shot.", ""]
out += ["## 1. Tỷ lệ theo loại shot", "| type | giây | % | trần/luật |", "|---|---|---|---|"]
lim = {"card": "≤ 25 % (Q26b `the`, Q34)", "photo": "cộng vào ≤ 40 %", "document": "cộng vào ≤ 40 %; ≤ 3 s/shot", "footage": "cộng vào ≤ 40 %; ≤ 8 s/clip"}
for k in ("scene3d", "chart3d", "map", "card", "photo", "document", "footage"):
    out.append(f"| {k} | {by[k]:.1f} | {pct(by[k]):.1f} % | {lim.get(k, '')} |")
out.append(f"| **ảnh + tài liệu + footage** | {ext:.1f} | **{pct(ext):.1f} %** | ≤ 40 % (QUAN-TRI-RUI-RO §6.3, Q32/Q34d) |")
# card liên tục
run = best = 0.0
for r in rows:
    run = run + r["d"] if r["type"] == "card" else 0.0; best = max(best, run)
out.append(f"| card liên tục dài nhất | {best:.1f} | — | ≤ 90 s |")
# clip dài
bad = [r for r in rows if (r["type"] in ("footage", "photo") and r["d"] > 8) or (r["type"] == "document" and r["d"] > 3)]
out += ["", "## 2. Luật từng shot", f"- footage/ảnh > 8 s hoặc document > 3 s: **{len(bad)}** " + ", ".join(f"{r['id']} ({r['type']} {r['d']:.1f} s)" for r in bad)]
docs = [r for r in rows if r["type"] == "document" and not (r.get("p", {}).get("paper") and r.get("p", {}).get("date"))]
out.append(f"- document thiếu p.paper/p.date: **{len(docs)}**")
lab = [r for r in rows if r["type"] in ("photo", "footage", "document") and not r.get("label")]
out.append(f"- ảnh/footage/tài liệu thiếu nhãn năm/nguồn: **{len(lab)}**")
# lặp góc (chuỗi liền nhau cùng cặp = một lần)
app, prev = defaultdict(int), None
for r in rows:
    key = (r["scene_id"], r["camera_id"])
    if key != prev: app[key] += 1
    prev = key
rep = {k: v for k, v in app.items() if v > 2}
two = [f"{a}/{b}" for (a, b), v in app.items() if v == 2]
out.append(f"- cùng (scene_id, camera_id) > 2 lần: **{len(rep)}** {rep if rep else ''}; đúng 2 lần (bằng ngưỡng): {', '.join(two) if two else 'không'}")
# bối cảnh 3D (scene3d theo scene_id) + card là 'the'
ctx = defaultdict(float); runs = defaultdict(float); cur, cr = None, 0.0
for r in rows:
    k = r["scene_id"] if r["type"] == "scene3d" else ("the" if r["type"] == "card" else None)
    if k: ctx[k] += r["d"]
    if k and k == cur: cr += r["d"]
    elif k: cur, cr = k, r["d"]
    if k: runs[k] = max(runs[k], cr)
half = {r["scene_id"] for r in rows if r["type"] == "scene3d" and r["t0"] >= T / 2}
out.append("- bối cảnh (scene3d theo bộ cảnh; `the` = card): " + ", ".join(f"{k} {pct(v):.1f} % (liên tục ≤ {runs[k]:.0f} s)" for k, v in sorted(ctx.items(), key=lambda x: -x[1])) + f"; nửa sau có {len(half)} bộ cảnh 3D: {', '.join(sorted(half))}")
# số neo
sid = {r["id"]: r for r in rows}
an = spec["anchors"]; ok = [a for a in an if sid[a["shot"]]["type"] in ("chart3d", "scene3d")]
miss = [a for a in an if a["claim"] not in (sid[a["shot"]].get("nums") or [])]
out.append(f"- số neo hiện bằng chart3d/scene3d: **{len(ok)}/{len(an)} = {100*len(ok)/len(an):.0f} %** (≥ 60 %); số neo trên map: {sum(sid[a['shot']]['type']=='map' for a in an)}, photo: {sum(sid[a['shot']]['type']=='photo' for a in an)}, card: {sum(sid[a['shot']]['type']=='card' for a in an)}, document: {sum(sid[a['shot']]['type']=='document' for a in an)}; mã claim không khớp `nums` của shot: {len(miss)}")
pl = [p for p in spec["places"] if sid.get(p["shot"], {}).get("type") != "map" and not any(r["type"] == "map" and r["camera_id"].startswith(p["shot"]) for r in rows)]
out.append(f"- địa danh không có shot map: **{len(pl)}** ({len(spec['places'])} địa danh)")
pp = [p for p in spec["people"] if not (p.get("photo") or p.get("ly_do"))]
out.append(f"- người thiếu photo/ly_do: **{len(pp)}** ({len(spec['people'])} người)")
out += ["", "## 3. Bảng shot", "| # | đoạn | bắt đầu | dài (s) | type | scene_id | camera_id | số (claim) | nội dung | nguồn / nhãn |", "|---|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    m, s = divmod(r["t0"], 60)
    out.append(f"| {r['id']} | {r['seg']} | {int(m)}:{s:04.1f} | {r['d']:.1f} | {r['type']} | {r['scene_id']} | {r['camera_id']} | {', '.join(r.get('nums') or [])} | {r['desc']} | {(r.get('src','') + ' · ' + r.get('label','')).strip(' ·')} |")
out += ["", "## 4. places / people / anchors", "**places:** " + "; ".join(f"{p['name']} → {p['shot']}" for p in spec["places"]),
        "", "**people:** " + "; ".join(f"{p['name']} → " + (f"photo `{p['photo']}`" if p.get('photo') else f"ly_do: {p['ly_do']}") for p in spec["people"]),
        "", "**anchors:** " + "; ".join(f"{a['num']} ({a['claim']}) → {a['shot']} [{sid[a['shot']]['type']}]" for a in an)]
(H / "SHOTLIST.md").write_text("\n".join(out) + "\n")
print("\n".join(out[:40]))
