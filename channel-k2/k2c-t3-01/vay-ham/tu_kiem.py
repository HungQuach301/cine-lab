"""T3b · tự kiểm bảng shot (treatment) theo luật đề xuất: Q26b-K2, NC-H1, NC-H2, NC-H3, lặp vùng+góc, footage.
Đọc vay-ham/treatment.json, ghi vay-ham/tu-kiem.json, in bảng markdown. Không dựng hình; số là số của BẢNG SHOT (thời lượng ước theo lời chưa viết).
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/vay-ham/tu_kiem.py"""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOAI = ["3D phố", "3D vùng", "bản đồ lịch sử", "tranh Ken Burns", "ảnh", "footage", "thẻ số"]
LOAI_3D = {"3D phố", "3D vùng"}


def main():
    tr = json.loads((HERE / "treatment.json").read_text())
    shots = tr["shots"]
    t = 0.0
    for s in shots:
        assert s["loai"] in LOAI, s["id"]
        s["t0"] = round(t, 1); t += s["dur"]
    T = t; half = T / 2
    out = {"tong_s": round(T, 1), "so_shot": len(shots)}

    # Q26b-K2: mỗi nửa ≥ 3 loại cảnh, một loại ≤ 70 % (theo thời lượng của nửa đó)
    halves = [Counter(), Counter()]
    for s in shots:
        a, b = s["t0"], s["t0"] + s["dur"]
        if a < half: halves[0][s["loai"]] += min(b, half) - a
        if b > half: halves[1][s["loai"]] += b - max(a, half)
    q26 = []
    for i, c in enumerate(halves):
        tot = sum(c.values()); top = c.most_common(1)[0]
        q26.append({"nua": i + 1, "so_loai": len(c), "loai_lon_nhat": top[0], "ty_le_lon_nhat": round(top[1] / tot, 3),
                    "chia": {k: round(v / tot, 3) for k, v in c.most_common()}, "dat": len(c) >= 3 and top[1] / tot <= 0.70})
    out["Q26b_K2"] = q26

    # NC-H2: AGL > 50 km ≤ 1 lần, ≤ 3 s
    glob = [s for s in shots if s.get("agl_max_km", 0) > 50]
    out["NC_H2"] = {"so_lan": len(glob), "giay": [s.get("s_tren_50km", s["dur"]) for s in glob], "shot": [s["id"] for s in glob],
                    "dat": len(glob) <= 1 and all(s.get("s_tren_50km", s["dur"]) <= 3 for s in glob)}

    # NC-H3: trong thời lượng 3D, ≥ 70 % ở AGL ≤ 60 km; ≥ 40 % ở AGL ≤ 3 km (theo AGL đại diện của shot; phần bay trên ngưỡng tính riêng nếu khai)
    d3 = sum(s["dur"] for s in shots if s["loai"] in LOAI_3D)
    le60 = sum(s["dur"] - s.get("s_tren_60km", 0) for s in shots if s["loai"] in LOAI_3D and s["agl_km"] <= 60)
    le3 = sum(s["dur"] - s.get("s_tren_3km", 0) for s in shots if s["loai"] in LOAI_3D and s["agl_km"] <= 3)
    out["NC_H3"] = {"tong_3D_s": round(d3, 1), "ty_le_3D_phim": round(d3 / T, 3), "le60km": round(le60 / d3, 3), "le3km": round(le3 / d3, 3),
                    "dat": le60 / d3 >= 0.70 and le3 / d3 >= 0.40}

    # NC-H1: shot nói tới phố (noi == thanh_pho) phải có nguồn nhà đúng thời kỳ; không có → phải là bản đồ lịch sử phẳng/tranh/ảnh
    h1 = []
    for s in shots:
        if s.get("noi") == "thanh_pho":
            ok = (s["loai"] not in LOAI_3D) or bool(s.get("du_lieu_nha"))
            h1.append({"shot": s["id"], "loai": s["loai"], "moc": s.get("moc_nam"), "du_lieu_nha": s.get("du_lieu_nha", ""), "dat": ok})
    out["NC_H1"] = {"so_shot_pho": len(h1), "loi": [x for x in h1 if not x["dat"]], "dat": all(x["dat"] for x in h1),
                    "shot_3D_pho": [x["shot"] for x in h1 if x["loai"] in LOAI_3D]}

    # Lặp vùng + góc > 2
    rep = Counter((s["vung"], s["goc"]) for s in shots if s["loai"] in LOAI_3D or s["loai"] == "bản đồ lịch sử")
    out["lap_vung_goc"] = {"max": max(rep.values()), "vuot_2": [list(k) + [v] for k, v in rep.items() if v > 2], "dat": max(rep.values()) <= 2}

    # Footage ≤ 20 %; hồ sơ thật (tranh + ảnh + bản đồ lịch sử) — Kinh thánh §4 10–15 % (chỉ báo)
    by = Counter()
    for s in shots: by[s["loai"]] += s["dur"]
    out["ty_le_loai"] = {k: round(v / T, 3) for k, v in by.most_common()}
    out["footage"] = {"ty_le": round(by["footage"] / T, 3), "dat": by["footage"] / T <= 0.20}
    out["ho_so_that"] = round((by["tranh Ken Burns"] + by["ảnh"] + by["bản đồ lịch sử"]) / T, 3)

    # Mỗi shot gắn ≥ 1 claim; mốc đinh
    out["shot_khong_claim"] = [s["id"] for s in shots if not s.get("claims")]
    out["moc_dinh"] = [{"shot": s["id"], "t": s["t0"], "moc": s.get("moc_dinh")} for s in shots if s.get("moc_dinh")]
    out["cu_lien_hoan"] = sorted({s["cu"] for s in shots if s.get("cu")})
    ch = defaultdict(float)
    for s in shots: ch[s["ch"]] += s["dur"]
    out["chuong_s"] = {k: round(v, 1) for k, v in ch.items()}

    # ±5 % quanh ngưỡng
    near = []
    def chk(name, v, thr):
        if thr and abs(v - thr) / thr <= 0.05: near.append({"chi_so": name, "do": v, "nguong": thr, "lech_pct": round((v - thr) / thr * 100, 1)})
    for q in q26: chk(f"Q26b-K2 nửa {q['nua']} loại lớn nhất", q["ty_le_lon_nhat"], 0.70)
    chk("NC-H3 ≤ 60 km", out["NC_H3"]["le60km"], 0.70); chk("NC-H3 ≤ 3 km", out["NC_H3"]["le3km"], 0.40)
    chk("footage", out["footage"]["ty_le"], 0.20)
    for g in out["NC_H2"]["giay"]: chk("NC-H2 giây trên 50 km", g, 3.0)
    out["sat_nguong_5pct"] = near

    (HERE / "tu-kiem.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    ok = all([q26[0]["dat"], q26[1]["dat"], out["NC_H2"]["dat"], out["NC_H3"]["dat"], out["NC_H1"]["dat"], out["lap_vung_goc"]["dat"], out["footage"]["dat"], not out["shot_khong_claim"]])
    print("TU KIEM:", "ĐẠT" if ok else "TRƯỢT", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
