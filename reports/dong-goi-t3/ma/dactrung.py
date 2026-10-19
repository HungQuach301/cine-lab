#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 0 · gộp số liệu quét + số đo ảnh + nhãn → reports/dong-goi-t3/quet-ngach/dac-trung.json (CHỈ video_id + đặc trưng + số; không tiêu đề, không ảnh)
và thống kê đặc trưng ↔ điểm vượt trội (trung vị, TB log10 + khoảng tin cậy 95 % bootstrap, cỡ mẫu) → thong-ke.json.
Dùng: dactrung.py <thư mục tạm quét> <thư mục ra trong repo>"""
import json, math, random, re, statistics as stt, sys
from pathlib import Path
T, O = Path(sys.argv[1]), Path(sys.argv[2]); O.mkdir(parents=True, exist_ok=True)
raw = {v["id"]: v for v in json.load(open(T / "videos-raw.json"))}; order = json.load(open(T / "order.json"))
do = json.load(open(T / "thumbs-do.json")); nh = json.load(open(T / "nhan.json"))
NA = {x["n"]: x for x in nh["anh"]}; NT = {x["n"]: x for x in nh["tieu_de"]}
YR = re.compile(r"\b(1[0-9]{3}|20[0-9]{2}|[1-9][0-9]{0,2} ?(?:AD|BC|BCE|CE))\b")
RANGE = re.compile(r"(\b\d{1,4}(?: ?(?:AD|BC|BCE))?\b)\s*(?:-|–|—|→|->|to|until)\s*(\b\d{3,4}\b|now|today|present|NOW|TODAY)", re.I)
EMO = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")
rows = []
for n, vid in enumerate(order):
    v = raw[vid]; t = v["title"]; a = NA.get(n, {}); tl = NT.get(n, {}); m = do.get(vid, {})
    words = t.split()
    r = {"video_id": vid, "truy_van": sorted({q for q, _ in v["q"]}), "hang_tot_nhat": min(r for _, r in v["q"]), "ngay": v["pub"], "luot_xem": v["views"], "thoi_luong_s": v["dur"],
         "kenh_id": v["ch"], "nguoi_dang_ky": v["subs"], "kenh_trung_vi_20": v["ch_median20"], "kenh_n_gan": v["ch_n_recent"], "diem_vuot_troi": round(v["outlier"], 3) if v["outlier"] else None,
         # tiêu đề (chỉ đặc trưng)
         "td_ky_tu": len(t), "td_so_tu": len(words), "td_co_nam": bool(YR.search(t)), "td_dai_nam": bool(RANGE.search(t)), "td_mui_ten": ("→" in t or "->" in t),
         "td_3d": bool(re.search(r"\b3D\b", t, re.I)), "td_timelapse": bool(re.search(r"time ?-?lapse", t, re.I)), "td_grow_evolution": bool(re.search(r"\b(grow|growth|evolution|evolve|rise)\b", t, re.I)),
         "td_hoi": ("?" in t) or bool(tl.get("question")), "td_mo_bang": tl.get("opens_with"), "td_noi_vi_tri": tl.get("place_word_index"),
         "td_noi_3_tu_dau": (tl.get("place_word_index") or 99) <= 3, "td_loi_hua": tl.get("promise"), "td_xung_dot": tl.get("conflict_word"), "td_tranh_chu": tl.get("ownership_contest"),
         "td_nhan_dinh_dang": tl.get("format_tag"), "td_phan_cach": tl.get("separator"), "td_chu_hoa_tu": sum(1 for w in words if len(w) > 2 and w.isupper()), "td_emoji": bool(EMO.search(t)),
         "dung_chu_de": tl.get("on_topic"), "lan": tl.get("lane"),
         # ảnh (số đo máy + nhãn mô hình nhìn)
         **{"anh_" + k: val for k, val in m.items() if not k.startswith("_")},
         **{"anh_" + k: a.get(k) for k in ("style", "aerial_city_fills_frame", "focus", "split_then_now", "year_band", "big_place_name", "night_or_dark", "fire_or_smoke", "flag_prominent", "conflict_imagery", "arrow_or_circle", "sky_frac", "dominant_palette")}}
    rows.append(r)
json.dump(rows, open(O / "dac-trung.json", "w"), indent=1, ensure_ascii=False)
# ---------- thống kê ----------
random.seed(19102026)
def boot(xs, k=4000):
    if len(xs) < 2: return [None, None]
    ms = sorted(stt.fmean(random.choices(xs, k=len(xs))) for _ in range(k)); return [round(ms[int(0.025 * k)], 3), round(ms[int(0.975 * k)], 3)]
def boot_diff(a, b, k=4000):
    if len(a) < 2 or len(b) < 2: return [None, None]
    ds = sorted(stt.fmean(random.choices(a, k=len(a))) - stt.fmean(random.choices(b, k=len(b))) for _ in range(k)); return [round(ds[int(0.025 * k)], 3), round(ds[int(0.975 * k)], 3)]
def spearman(x, y):
    def rk(v): s = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); [r.__setitem__(i, j) for j, i in enumerate(s)]; return r
    rx, ry = rk(x), rk(y); n = len(x); mx, my = stt.fmean(rx), stt.fmean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry)); den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)); return num / den if den else 0
def spearman_ci(x, y, k=2000):
    idx = list(range(len(x))); vs = sorted(spearman([x[i] for i in s], [y[i] for i in s]) for s in (random.choices(idx, k=len(idx)) for _ in range(k))); return [round(vs[int(0.025 * k)], 3), round(vs[int(0.975 * k)], 3)]
def subset(name, S):
    S = [r for r in S if r["diem_vuot_troi"] and r["diem_vuot_troi"] > 0 and r["kenh_n_gan"] >= 5]
    lg = lambda r: math.log10(r["diem_vuot_troi"])
    out = {"tap": name, "n": len(S), "trung_vi_vuot_troi": round(stt.median([r["diem_vuot_troi"] for r in S]), 3) if S else None, "bool": {}, "lien_tuc": {}, "nhom": {}}
    BOOL = ["td_co_nam", "td_dai_nam", "td_mui_ten", "td_3d", "td_timelapse", "td_grow_evolution", "td_hoi", "td_noi_3_tu_dau", "td_xung_dot", "td_tranh_chu", "td_nhan_dinh_dang", "td_emoji",
            "anh_aerial_city_fills_frame", "anh_split_then_now", "anh_year_band", "anh_big_place_name", "anh_night_or_dark", "anh_fire_or_smoke", "anh_flag_prominent", "anh_conflict_imagery", "anh_arrow_or_circle"]
    for f in BOOL:
        a = [lg(r) for r in S if r.get(f) is True]; b = [lg(r) for r in S if r.get(f) is False]
        out["bool"][f] = {"n_co": len(a), "n_khong": len(b), "tb_log_co": round(stt.fmean(a), 3) if a else None, "tb_log_khong": round(stt.fmean(b), 3) if b else None,
                          "trung_vi_co": round(10 ** stt.median(a), 2) if a else None, "trung_vi_khong": round(10 ** stt.median(b), 2) if b else None, "hieu_log_ci95": boot_diff(a, b)}
    CONT = ["td_ky_tu", "td_so_tu", "anh_L_mean", "anh_sat_mean", "anh_contrast_rms", "anh_colorfulness", "anh_warm_frac", "anh_night_frac", "anh_text_area", "anh_text_words", "anh_text_hmax", "anh_sky_frac", "nguoi_dang_ky"]
    for f in CONT:
        P = [(r[f], lg(r)) for r in S if isinstance(r.get(f), (int, float)) and not isinstance(r.get(f), bool)]
        if len(P) >= 8:
            x, y = zip(*P); out["lien_tuc"][f] = {"n": len(P), "spearman": round(spearman(list(x), list(y)), 3), "ci95": spearman_ci(list(x), list(y)), "trung_vi_gia_tri": round(stt.median(x), 3)}
    for f in ["td_mo_bang", "td_loi_hua", "anh_style", "anh_focus", "anh_dominant_palette", "lan"]:
        g = {}
        for r in S: g.setdefault(str(r.get(f)), []).append(lg(r))
        out["nhom"][f] = {k: {"n": len(v), "trung_vi": round(10 ** stt.median(v), 2), "tb_log": round(stt.fmean(v), 3), "ci95_tb_log": boot(v)} for k, v in sorted(g.items(), key=lambda kv: -len(kv[1]))}
    return out
long_ = [r for r in rows if r["thoi_luong_s"] > 180]
on = [r for r in long_ if r["dung_chu_de"]]
tl3d = [r for r in on if r["lan"] == "timelapse_3d" or r["td_timelapse"]]
hist = [r for r in on if r["lan"] in ("history_explainer", "battle_siege", "travel_facts")]
stats = {"tap": [subset("dai_dung_chu_de", on), subset("lan_timelapse_3d", tl3d), subset("lan_lich_su", hist)]}
# khoảng trống: lời hứa theo làn
gap = {}
for nm, S in (("timelapse_3d", tl3d), ("lich_su", hist)):
    gap[nm] = {"n": len(S), "loi_hua": {k: sum(1 for r in S if r["td_loi_hua"] == k) for k in ("visual", "story", "both", "other")},
               "tranh_chu": sum(1 for r in S if r["td_tranh_chu"]), "xung_dot_tieu_de": sum(1 for r in S if r["td_xung_dot"]),
               "anh_dem": sum(1 for r in S if r["anh_night_or_dark"]), "anh_lua_khoi": sum(1 for r in S if r["anh_fire_or_smoke"]), "anh_xung_dot": sum(1 for r in S if r["anh_conflict_imagery"]),
               "anh_co": sum(1 for r in S if r["anh_flag_prominent"]), "anh_3d": sum(1 for r in S if r["anh_style"] == "3d_render"), "anh_ban_do_phang": sum(1 for r in S if r["anh_style"] == "flat_map"),
               "anh_dai_nam": sum(1 for r in S if r["anh_year_band"]), "anh_ten_noi_lon": sum(1 for r in S if r["anh_big_place_name"]), "anh_chia_doi": sum(1 for r in S if r["anh_split_then_now"]),
               "td_hoi": sum(1 for r in S if r["td_hoi"]), "td_dai_nam": sum(1 for r in S if r["td_dai_nam"])}
both = [r for r in on if (r["td_timelapse"] or r["anh_style"] == "3d_render") and (r["td_xung_dot"] or r["td_tranh_chu"] or r["anh_conflict_imagery"])]
gap["giao_hai_lan"] = {"n": len(both), "video_id": [r["video_id"] for r in both], "diem_vuot_troi": [r["diem_vuot_troi"] for r in both]}
stats["khoang_trong"] = gap
stats["co_mau"] = {"tong_ket_qua": len(rows), "dai_gt_180s": len(long_), "dung_chu_de": len(on), "timelapse_3d": len(tl3d), "lich_su": len(hist)}
json.dump(stats, open(O / "thong-ke.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(stats["co_mau"]), json.dumps(gap, ensure_ascii=False)[:1500])
