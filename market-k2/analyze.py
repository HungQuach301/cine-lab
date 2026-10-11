"""Kênh 2 — tính 6 chỉ số (tự tính, không phải chỉ số YouTube) từ số liệu thô ngoài git; metrics.json cũng ở ngoài git, kết luận viết tay vào REPORT.md."""
import json, math, os, re, statistics as st, datetime as dt, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from collect import DATA, NOW, haiku

YOUNG = NOW - dt.timedelta(days=730)
MIN_AGE = dt.timedelta(days=14)          # bỏ video < 14 ngày (chưa kịp tích luỹ lượt xem)
FLOOR = 10_000                           # biến thể: nổ phải ≥ 10 nghìn lượt xem
SPONSOR = re.compile(r"sponsor|use code|promo code|affiliate|% off|discount|patreon\.com|nordvpn|"
                     r"brilliant\.org|ground\.news|squarespace|skillshare|audible|incogni|aura\.com|"
                     r"amzn\.to|bit\.ly|geni\.us|partner", re.I)
# CPM công khai (CPM, KHÔNG phải RPM), USD/1.000 lần hiển thị quảng cáo, khán giả Mỹ — ghép dòng gần nhất:
# OK = OutlierKit cập nhật 13/09/2026; VP = VloggingPro 2026.
CPM = {"A": ([(18, 45, "OK Personal Finance & Investing"), (5, 12, "OK History")]),
       "B": ([(14, 35, "OK Business & Entrepreneurship"), (5, 12, "OK History")]),
       "D": ([(3, 8, "VP Travel (không có dòng địa lý)"), (5, 12, "OK History")]),
       "E": ([(8, 20, "OK AI & Technology")]),
       "J": ([(12, 30, "OK Real Estate"), (5, 12, "OK History")]),
       "L": ([(8, 20, "OK AI & Technology (không có dòng năng lượng)"), (5, 12, "OK History")])}
# Tận dụng nhà máy (3D Blender, quy trình nguồn xác minh, bộ kiểm) — chấm định tính 0–10, lý do ở REPORT.
FACTORY = {"A": 7, "B": 6, "D": 9, "E": 7, "J": 8, "L": 9}
# Rủi ro chính sách (0–10, định tính): persona AI chuyên gia/YMYL + inauthentic content.
POLICY = {"A": 7, "B": 3, "D": 3, "E": 5, "J": 5, "L": 3}

ts = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
med = lambda xs: st.median(xs) if xs else 0
def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * (len(xs) - 1) + 0.5))] if xs else 0

def breakouts(ch):
    vs = [v for v in ch["videos"] if NOW - ts(v["pub"]) >= MIN_AGE]
    res = []
    for v in vs:
        peers = [w["views"] for w in vs if w is not v and abs(ts(w["pub"]) - ts(v["pub"])).days <= 90]
        r_med = v["views"] / med(peers) if len(peers) >= 3 and med(peers) > 0 else 0
        r_sub = v["views"] / ch["subs"] if ch["subs"] > 0 and not ch["hidden_subs"] else 0
        res.append((v, r_med >= 3 or r_sub >= 3))
    return res

def cached(name, fn):
    f = DATA / f"haiku_{name}.json"
    if f.exists(): return json.loads(f.read_text())
    r = fn(); f.write_text(json.dumps(r)); return r

def main():
    rows = {}
    for k in "ABDEJL":
        d = json.loads((DATA / f"niche_{k}.json").read_text())
        chs = d["channels"]
        allv, bo, bo10, young, young_bo = [], [], [], [], 0
        for cid, ch in chs.items():
            r = breakouts(ch)
            allv += [v for v, _ in r]
            b = [v for v, x in r if x]; bo += b; bo10 += [v for v in b if v["views"] >= FLOOR]
            if ts(ch["created"]) >= YOUNG:
                young.append(ch); young_bo += any(v["views"] >= FLOOR for v in b)
        # a. cầu + cờ thời sự (Haiku)
        top_bo = sorted(bo10, key=lambda v: -v["views"])[:40]
        tag = cached(f"news_{k}", lambda: haiku(
            "For each YouTube video title, is it news-pegged/topical (tied to a current event of 2026 that will date "
            "quickly) or evergreen? Return ONLY JSON {\"<id>\": \"news\"|\"evergreen\"}.\n" +
            "\n".join(f'{v["id"]} | {v["title"]}' for v in top_bo), f"news-{k}"))
        news = sum(1 for v in top_bo if tag.get(v["id"]) == "news") / max(1, len(top_bo))
        # b. kênh trẻ + tập trung top 5 (lượt xem mẫu tìm kiếm 90 ngày của kênh đạt lọc)
        passed = {c for c, x in d["classified"].items() if x.get("faceless_explainer")}
        byc = {}
        for v in d["search_videos"]:
            if v["ch"] in passed: byc[v["ch"]] = byc.get(v["ch"], 0) + v["views"]
        tot = sum(byc.values()) or 1
        top5 = sum(sorted(byc.values(), reverse=True)[:5]) / tot
        # c. khoảng trống: 10 video đứng đầu (lượt xem) trong mẫu tìm kiếm của kênh đạt lọc
        lead = sorted([v for v in d["search_videos"] if v["ch"] in passed], key=lambda v: -v["views"])[:10]
        gap = cached(f"gap_{k}", lambda: haiku(
            "For each top YouTube explainer video, judge from title + description only: real_data=true if it "
            "visibly relies on real data/cited sources (numbers, studies, archives, source lists); "
            "rich_visuals=true if it signals elaborate custom visuals (animation, 3D, motion graphics, custom maps). "
            "Return ONLY JSON {\"<id>\": {\"real_data\": bool, \"rich_visuals\": bool}}.\n" +
            "\n".join(f'{v["id"]} | {v["title"]} | {v["desc"][:600]!r}' for v in lead), f"gap-{k}"))
        both = sum(1 for v in lead if gap.get(v["id"], {}).get("real_data") and gap.get(v["id"], {}).get("rich_visuals"))
        gap_share = 1 - both / max(1, len(lead))
        # d. tốc độ bật kiếm tiền
        dur_bo = med([v["dur"] for v in bo10]) / 60
        ym = [med([v["views"] for v in ch["videos"] if NOW - ts(v["pub"]) >= MIN_AGE] or [0]) for ch in young]
        v_typ, v_p75 = med(ym), pct(ym, 0.75)
        def eps(views, hours):
            per = views * dur_bo * 60 / 3600
            return (hours / (per * 0.45), hours / (per * 0.35)) if per > 0 else (float("inf"),) * 2
        # e. doanh thu: CPM ghép + tỷ lệ video nổ có tài trợ/affiliate trong mô tả
        cpm_lo = st.mean(a for a, _, _ in CPM[k]); cpm_hi = st.mean(b for _, b, _ in CPM[k])
        spons = sum(1 for v in bo10 if SPONSOR.search(v["desc"])) / max(1, len(bo10))
        # f. trùng khán giả (Haiku đọc 15 tiêu đề gần nhất của mỗi kênh)
        ov = cached(f"overlap_{k}", lambda: haiku(
            "For each YouTube channel (name + recent titles) answer: pf=true if it regularly covers US personal finance "
            "(budgeting, investing, retirement, credit, saving money); ll=true if it regularly covers history of jobs/"
            "professions, automation or AI replacing work. Return ONLY JSON {\"<channelId>\": {\"pf\": bool, \"ll\": bool}}.\n" +
            "\n".join(f'{cid} | {ch["name"]} | ' + " ; ".join(v["title"] for v in ch["videos"][:15]) for cid, ch in chs.items()),
            f"overlap-{k}"))
        pf = sum(1 for c in chs if ov.get(c, {}).get("pf")) / max(1, len(chs))
        ll = sum(1 for c in chs if ov.get(c, {}).get("ll")) / max(1, len(chs))
        slop = sum(1 for ch in young if len(ch["videos"]) >= 20) / max(1, len(chs))  # kênh trẻ ra ≥20 video dài
        rows[k] = dict(name=d["name"], n_ch=len(chs), n_vid=len(allv), cand=d["n_candidates"], passed=len(passed),
            bo_rate=len(bo) / max(1, len(allv)), bo10_rate=len(bo10) / max(1, len(allv)), news=news,
            young=len(young), young_bo=young_bo / max(1, len(young)), top5=top5, gap=gap_share,
            dur_bo=dur_bo, v_typ=v_typ, v_p75=v_p75, eps4k_p75=eps(v_p75, 4000), eps8k_p75=eps(v_p75, 8000),
            eps4k_typ=eps(v_typ, 4000), cpm=(cpm_lo, cpm_hi), cpm_src=[s for *_, s in CPM[k]], spons=spons,
            pf=pf, ll=ll, slop=slop, policy=POLICY[k], factory=FACTORY[k],
            top_bo=[dict(t=v["title"], ch=chs[v["ch"]]["name"], views=v["views"], min=round(v["dur"] / 60),
                         news=tag.get(v["id"]) == "news") for v in top_bo[:25]])
    score(rows)
    Path(DATA / "metrics.json").write_text(json.dumps(rows, indent=1, default=str))

def norm(vals):
    lo, hi = min(vals.values()), max(vals.values())
    return {k: 10 * (v - lo) / (hi - lo) if hi > lo else 5 for k, v in vals.items()}

def score(rows):
    K = list(rows)
    E = {k: 0.7 * n1 + 0.3 * n2 for k, n1, n2 in zip(K, norm({k: sum(rows[k]["cpm"]) / 2 for k in K}).values(),
                                                         norm({k: rows[k]["spons"] for k in K}).values())}
    D = norm({k: -math.log(min(rows[k]["eps4k_p75"][1], 1e4)) for k in K})  # thang log: tránh một ngách ngoại lai ép dẹt phần còn lại
    AC = {k: (a + c) / 2 for k, a, c in zip(K, norm({k: rows[k]["bo10_rate"] * (1 - 0.5 * rows[k]["news"]) for k in K}).values(),
                                               norm({k: rows[k]["gap"] for k in K}).values())}
    F = {k: rows[k]["factory"] for k in K}
    B = {k: (a + b) / 2 for k, a, b in zip(K, norm({k: rows[k]["young_bo"] for k in K}).values(),
                                           norm({k: -rows[k]["top5"] for k in K}).values())}
    R = {k: (rows[k]["policy"] + 10 * rows[k]["pf"] + 10 * rows[k]["ll"] + 10 * rows[k]["slop"]) / 4 for k in K}
    comp = dict(e=E, d=D, ac=AC, fac=F, b=B, f=R)
    W = dict(e=25, d=20, ac=20, fac=15, b=10, f=-10)
    tot = lambda w: {k: sum(w[c] * comp[c][k] for c in w) / 10 for k in K}
    base = tot(W)
    sens = []
    for c in W:
        for dlt in (-5, 5):
            w = dict(W); w[c] = W[c] + (dlt if c != "f" else -dlt)
            s = tot(w); r = sorted(K, key=lambda k: -s[k])
            sens.append((c, dlt, r[0], r[1]))
    for k in K:
        rows[k]["sc"] = {c: round(comp[c][k], 1) for c in comp}; rows[k]["total"] = round(base[k], 1)
    rows["_sens"] = sens

if __name__ == "__main__":
    main()
