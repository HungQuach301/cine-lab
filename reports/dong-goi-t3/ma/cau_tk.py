#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 1 · thống kê cầu từ dữ liệu thô (thư mục tạm): truy vấn "gibraltar" (2 năm, theo lượt xem) + q6 "gibraltar history",
q4 "siege history animated", q5 "contested territory border history" của quét ngách (đăng ≥ 2023). Cửa sổ: 90 ngày (≥ 21/7/2026) và 2 năm (≥ 19/10/2024).
Repo nhận: video_id, ngày, lượt xem, thời lượng, kênh_id, cờ chủ đề (regex trên tiêu đề) — không tiêu đề. Dùng: cau_tk.py <tạm> <ra>"""
import json, re, statistics as st, sys
from pathlib import Path
T, O = Path(sys.argv[1]), Path(sys.argv[2]); O.mkdir(parents=True, exist_ok=True)
g = json.load(open(T / "cau-gibraltar-raw.json")); q = json.load(open(T / "videos-raw.json"))
FL = {"siege": r"siege|besieg", "border_runway": r"border|frontier|runway|airport|gate|fence|schengen|treaty", "why_british_owns": r"why .*(british|own|spain|uk)|british|owns?\b",
      "history": r"histor|ww2|wwii|war|1704|1779|1782|utrecht", "gibraltar": r"gibraltar"}
def flags(t): return {k: bool(re.search(p, t, re.I)) for k, p in FL.items()}
def row(v, src): return {"video_id": v["id"], "nguon": src, "ngay": v["pub"], "luot_xem": v["views"], "thoi_luong_s": v["dur"], "kenh_id": v["ch"], **flags(v["title"])}
rows = [row(v, "q_gibraltar_2nam_theo_luot_xem") for v in g] + [row(v, k) for v in q for k in sorted({x for x, _ in v["q"]}) if k in ("q6_gibraltar", "q4_siege", "q5_contested_border")]
json.dump(rows, open(O / "cau.json", "w"), indent=1, ensure_ascii=False)
def summ(R):
    if not R: return {"n": 0}
    v = sorted((r["luot_xem"] for r in R), reverse=True); return {"n": len(R), "tong_luot_xem": sum(v), "trung_vi": int(st.median(v)), "lon_nhat": v[0], "top5": v[:5], "dai_gt_180s": sum(1 for r in R if r["thoi_luong_s"] > 180)}
out = {}
for src in ("q_gibraltar_2nam_theo_luot_xem", "q6_gibraltar", "q4_siege", "q5_contested_border"):
    R = [r for r in rows if r["nguon"] == src]
    for nm, d0 in (("90_ngay", "2026-07-21"), ("2_nam", "2024-10-19")):
        W = [r for r in R if r["ngay"] >= d0]
        out[f"{src}|{nm}"] = {"tat_ca": summ(W), **{f"chu_de_{k}": summ([r for r in W if r[k]]) for k in FL if not (src == "q_gibraltar_2nam_theo_luot_xem" and k == "gibraltar")}}
json.dump(out, open(O / "cau-thong-ke.json", "w"), indent=1, ensure_ascii=False)
for k, v in out.items(): print(k, json.dumps(v["tat_ca"]), "| siege", v["chu_de_siege"].get("n"), v["chu_de_siege"].get("tong_luot_xem"), "| border", v["chu_de_border_runway"].get("n"), v["chu_de_border_runway"].get("tong_luot_xem"), "| why/brit", v["chu_de_why_british_owns"].get("n"), v["chu_de_why_british_owns"].get("tong_luot_xem"))
