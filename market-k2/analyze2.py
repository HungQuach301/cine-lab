"""Kênh 2 — vòng xác nhận: 6 chỉ số của A và B trên mẫu GỘP (cũ + mới), bootstrap theo kênh (1.000 lần) → KTC 90 % của B − A.
Chuẩn hoá min–max vẫn trên 6 ngách: D, E, J, L giữ nguyên đầu vào vòng trước (lấy từ bảng REPORT.md, đã làm tròn),
nên điểm của A và B so được với vòng trước. Kiểm mốc: tái lập điểm vòng trước từ bảng (selfcheck).
Tự tính, không phải chỉ số YouTube. metrics_v2.json ở ngoài git."""
import json, math, random, sys, statistics as st, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from collect import DATA, NOW, haiku
from analyze import YOUNG, MIN_AGE, FLOOR, SPONSOR, CPM, FACTORY, POLICY, ts, med, pct, breakouts, norm

# Đầu vào vòng trước (REPORT.md bảng 6 ngách). eps = số tập tới 4 000 h, cận trên (tỷ lệ xem 35 %), phân vị 75.
OLD = {
 "A": dict(bo10=.13, news=.18, young_bo=4/7, top5=.91, gap=1.0, eps=1.4, spons=.05, pf=.20, ll=.07, slop=.33),
 "B": dict(bo10=.23, news=.08, young_bo=4/5, top5=.71, gap=1.0, eps=2.3, spons=.28, pf=0, ll=0, slop=.27),
 "D": dict(bo10=.19, news=.08, young_bo=3/4, top5=.91, gap=1.0, eps=0.9, spons=.19, pf=0, ll=0, slop=.13),
 "E": dict(bo10=.05, news=.25, young_bo=2/8, top5=1.0, gap=1.0, eps=162, spons=.06, pf=.07, ll=.27, slop=.27),
 "J": dict(bo10=.22, news=.15, young_bo=11/12, top5=.88, gap=.9, eps=1.9, spons=.17, pf=.13, ll=.13, slop=.53),
 "L": dict(bo10=.18, news=.28, young_bo=6/11, top5=.98, gap=.9, eps=7.1, spons=.16, pf=.13, ll=.07, slop=.47),
}
W = dict(e=25, d=20, ac=20, fac=15, b=10, f=-10)

def score(R):
    """R: {niche: dict(bo10, news, young_bo, top5, gap, eps, spons, pf, ll, slop)} → (tổng, thành phần). Cùng công thức analyze.score."""
    K = list(R)
    cpm = {k: (st.mean(a for a, _, _ in CPM[k]) + st.mean(b for _, b, _ in CPM[k])) / 2 for k in K}
    E = {k: .7 * a + .3 * b for k, a, b in zip(K, norm(cpm).values(), norm({k: R[k]["spons"] for k in K}).values())}
    D = norm({k: -math.log(min(R[k]["eps"], 1e4)) for k in K})
    AC = {k: (a + c) / 2 for k, a, c in zip(K, norm({k: R[k]["bo10"] * (1 - .5 * R[k]["news"]) for k in K}).values(),
                                           norm({k: R[k]["gap"] for k in K}).values())}
    F = {k: FACTORY[k] for k in K}
    B = {k: (a + b) / 2 for k, a, b in zip(K, norm({k: R[k]["young_bo"] for k in K}).values(),
                                          norm({k: -R[k]["top5"] for k in K}).values())}
    P = {k: (POLICY[k] + 10 * (R[k]["pf"] + R[k]["ll"] + R[k]["slop"])) / 4 for k in K}
    comp = dict(e=E, d=D, ac=AC, fac=F, b=B, f=P)
    return {k: sum(W[c] * comp[c][k] for c in W) / 10 for k in K}, comp

def load(k):
    old = json.loads((DATA / f"k2v2_old_{k}.json").read_text())
    new = json.loads((DATA / f"k2v2_new_{k}.json").read_text())
    chs = {**old["channels"], **new["channels"]}
    passed = {c for s in (old, new) for c, x in s["classified"].items() if x.get("faceless_explainer")}
    sv = {v["id"]: v for s in (old, new) for v in s["search_videos"] if v["ch"] in passed}
    return old, new, chs, passed, list(sv.values())

def chunks(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]

def cached(name, fn):
    f = DATA / f"haiku_v2_{name}.json"
    if f.exists(): return json.loads(f.read_text())
    r = fn()
    if not r: raise SystemExit(f"Haiku trả rỗng: {name} (không ghi cache)")   # không để nhãn hỏng thành 0 im lặng
    f.write_text(json.dumps(r)); return r

def tags(k, chs, sv, pre):
    """Haiku chấm một lần trên toàn mẫu gộp (để bootstrap không gọi lại): thời sự cho MỌI video nổ ≥ 10 nghìn,
    dữ liệu thật + hình công phu cho 80 video dẫn đầu, trùng khán giả cho mọi kênh. Prompt giữ nguyên vòng trước."""
    bo10 = sorted({v["id"]: v for c in pre.values() for v in c["bo10"]}.values(), key=lambda v: -v["views"])
    news = {}
    for i, part in enumerate(chunks(bo10, 60)):
        news.update(cached(f"news_{k}_{i}", lambda: haiku(
            "For each YouTube video title, is it news-pegged/topical (tied to a current event of 2026 that will date "
            "quickly) or evergreen? Return ONLY JSON {\"<id>\": \"news\"|\"evergreen\"}.\n" +
            "\n".join(f'{v["id"]} | {v["title"]}' for v in part), f"v2-news-{k}")))
    lead = sorted(sv, key=lambda v: -v["views"])[:80]
    gap = {}
    for i, part in enumerate(chunks(lead, 20)):
        gap.update(cached(f"gap_{k}_{i}", lambda: haiku(
            "For each top YouTube explainer video, judge from title + description only: real_data=true if it "
            "visibly relies on real data/cited sources (numbers, studies, archives, source lists); "
            "rich_visuals=true if it signals elaborate custom visuals (animation, 3D, motion graphics, custom maps). "
            "Return ONLY JSON {\"<id>\": {\"real_data\": bool, \"rich_visuals\": bool}}.\n" +
            "\n".join(f'{v["id"]} | {v["title"]} | {v["desc"][:600]!r}' for v in part), f"v2-gap-{k}")))
    ov = {}
    for i, part in enumerate(chunks(list(chs.items()), 20)):
        ov.update(cached(f"overlap_{k}_{i}", lambda: haiku(
            "For each YouTube channel (name + recent titles) answer: pf=true if it regularly covers US personal finance "
            "(budgeting, investing, retirement, credit, saving money); ll=true if it regularly covers history of jobs/"
            "professions, automation or AI replacing work. Return ONLY JSON {\"<channelId>\": {\"pf\": bool, \"ll\": bool}}.\n" +
            "\n".join(f'{cid} | {ch["name"]} | ' + " ; ".join(v["title"] for v in ch["videos"][:15]) for cid, ch in part),
            f"v2-overlap-{k}")))
    # độ phủ: thiếu nhãn là lỗi, không phải 0
    assert set(v["id"] for v in bo10) <= set(news), f"thiếu nhãn thời sự {k}"
    assert set(v["id"] for v in lead) <= set(gap), f"thiếu nhãn khoảng trống {k}"
    assert set(chs) <= set(ov), f"thiếu nhãn trùng khán giả {k}"
    return news, gap, ov

def prep(chs):
    """Tính sẵn theo kênh (không phụ thuộc kênh khác) để bootstrap nhanh."""
    pre = {}
    for cid, ch in chs.items():
        r = breakouts(ch)
        b = [v for v, x in r if x]
        b10 = [v for v in b if v["views"] >= FLOOR]
        young = ts(ch["created"]) >= YOUNG
        pre[cid] = dict(n=len(r), bo=len(b), bo10=b10, young=young, young_bo=bool(b10),
                        medv=med([v["views"] for v, _ in r] or [0]), slop=young and len(ch["videos"]) >= 20)
    return pre

def metrics(cids, pids, pre, sv_by, news, gap, ov):
    """cids: kênh trong mẫu (có thể lặp khi bootstrap); pids: kênh đạt lọc (cho top 5 và khoảng trống)."""
    n = sum(pre[c]["n"] for c in cids) or 1
    bo10 = [v for c in cids for v in pre[c]["bo10"]]
    top = sorted(bo10, key=lambda v: -v["views"])[:40]
    nw = sum(1 for v in top if news.get(v["id"]) == "news") / max(1, len(top))
    young = [c for c in cids if pre[c]["young"]]
    tot = [sum(v["views"] for v in sv_by.get(c, [])) for c in pids]
    top5 = sum(sorted(tot, reverse=True)[:5]) / (sum(tot) or 1)
    lead = sorted({v["id"]: v for c in set(pids) for v in sv_by.get(c, [])}.values(), key=lambda v: -v["views"])[:10]
    both = sum(1 for v in lead if gap.get(v["id"], {}).get("real_data") and gap.get(v["id"], {}).get("rich_visuals"))
    dur = med([v["dur"] for v in bo10]) / 60
    ym = [pre[c]["medv"] for c in young]
    def eps(views, rate=.35):
        per = views * dur * 60 / 3600
        return 4000 / (per * rate) if per > 0 else 1e4
    return dict(bo10=len(bo10) / n, bo=sum(pre[c]["bo"] for c in cids) / n, news=nw,
                young_bo=sum(pre[c]["young_bo"] for c in young) / max(1, len(young)), n_young=len(young),
                n_young_uniq=len(set(young)), top5=top5, gap=1 - both / max(1, len(lead)), dur=dur,
                v_p75=pct(ym, .75), v_med=med(ym), eps=eps(pct(ym, .75)), eps_lo=eps(pct(ym, .75), .45),
                eps_med=eps(med(ym)), eps_med_lo=eps(med(ym), .45),
                spons=sum(1 for v in bo10 if SPONSOR.search(v["desc"])) / max(1, len(bo10)),
                pf=sum(1 for c in cids if ov.get(c, {}).get("pf")) / max(1, len(cids)),
                ll=sum(1 for c in cids if ov.get(c, {}).get("ll")) / max(1, len(cids)),
                slop=sum(pre[c]["slop"] for c in cids) / max(1, len(cids)), n_ch=len(cids))

def selfcheck():
    s, _ = score(OLD)
    want = dict(A=61.1, B=73.6, D=59.9, E=27.5, J=56.4, L=41.4)
    return {k: (round(s[k], 1), want[k]) for k in s}

def main(n_boot=1000, seed=20261011):
    out = {"selfcheck": selfcheck()}
    S = {}
    for k in "AB":
        old, new, chs, passed, sv = load(k)
        pre = prep(chs)
        sv_by = {}
        for v in sv: sv_by.setdefault(v["ch"], []).append(v)
        news, gap, ov = tags(k, chs, sv, pre)
        S[k] = dict(cids=list(chs), pids=sorted(passed), pre=pre, sv_by=sv_by, news=news, gap=gap, ov=ov)
        m = metrics(S[k]["cids"], S[k]["pids"], pre, sv_by, news, gap, ov)
        young_new = [c for c in new["channels"] if pre[c]["young"]]
        young_old = [c for c in old["channels"] if pre[c]["young"]]
        m.update(n_old=len(old["channels"]), n_new=len(new["channels"]),
                 n_overlap=len(set(old["channels"]) & set(new["channels"])), n_passed=len(passed),
                 n_young_new=len(young_new), n_young_old=len(young_old),
                 new_cands=new["n_candidates"], new_passed=sum(1 for x in new["classified"].values() if x.get("faceless_explainer")),
                 old_cands=old["n_candidates"], old_passed=sum(1 for x in old["classified"].values() if x.get("faceless_explainer")),
                 top_bo=[dict(t=v["title"], ch=chs[v["ch"]]["name"], views=v["views"], min=round(v["dur"] / 60),
                              news=news.get(v["id"]) == "news", young=pre[v["ch"]]["young"])
                         for v in sorted([v for c in chs for v in pre[c]["bo10"]], key=lambda v: -v["views"])[:30]],
                 young_list=[dict(name=chs[c]["name"], created=chs[c]["created"][:10], medv=pre[c]["medv"],
                                  bo=pre[c]["young_bo"], n=len(chs[c]["videos"])) for c in chs if pre[c]["young"]])
        out[k] = m
    def total(mA, mB):
        R = dict(OLD); R["A"] = {x: mA[x] for x in OLD["A"]}; R["B"] = {x: mB[x] for x in OLD["B"]}
        return score(R)
    s, comp = total(out["A"], out["B"])
    out["total"] = {k: round(v, 1) for k, v in s.items()}
    out["comp"] = {k: {c: round(comp[c][k], 1) for c in comp} for k in "AB"}
    rnd = random.Random(seed)
    diffs, totA, totB = [], [], []
    for _ in range(n_boot):
        mm = {}
        for k in "AB":
            z = S[k]
            c = [rnd.choice(z["cids"]) for _ in z["cids"]]
            p = [rnd.choice(z["pids"]) for _ in z["pids"]]
            mm[k] = metrics(c, p, z["pre"], z["sv_by"], z["news"], z["gap"], z["ov"])
        sb, _ = total(mm["A"], mm["B"])
        diffs.append(sb["B"] - sb["A"]); totA.append(sb["A"]); totB.append(sb["B"])
    diffs.sort()
    out["boot"] = dict(n=n_boot, seed=seed, diff_point=round(s["B"] - s["A"], 1),
                       ci90=(round(pct(diffs, .05), 1), round(pct(diffs, .95), 1)),
                       p_B_gt_A=round(sum(d > 0 for d in diffs) / n_boot, 3),
                       A_ci90=(round(pct(sorted(totA), .05), 1), round(pct(sorted(totA), .95), 1)),
                       B_ci90=(round(pct(sorted(totB), .05), 1), round(pct(sorted(totB), .95), 1)))
    # độ nhạy: mỗi trọng số ±5 điểm
    sens = []
    R = dict(OLD); R["A"] = {x: out["A"][x] for x in OLD["A"]}; R["B"] = {x: out["B"][x] for x in OLD["B"]}
    _, comp = score(R)
    for c in W:
        for d in (-5, 5):
            w = dict(W); w[c] += d if c != "f" else -d
            t = {k: sum(w[x] * comp[x][k] for x in w) / 10 for k in R}
            sens.append((c, d, round(t["B"] - t["A"], 1), sorted(t, key=lambda k: -t[k])[0]))
    out["sens"] = sens
    dd = [x[2] for x in sens]
    out["sens_AB"] = dict(B=sum(x > 0 for x in dd), A=sum(x < 0 for x in dd), tie=sum(x == 0 for x in dd),
                          lo=min(dd), hi=max(dd))
    # tách mẫu cũ / mới (cùng nhãn, cùng công thức), để so với vòng 1 và xem mẫu mới riêng
    out["split"] = {}
    for part in ("old", "new"):
        mm = {}
        for k in "AB":
            z = S[k]; smp = json.loads((DATA / f"k2v2_{part}_{k}.json").read_text())
            p = sorted(c for c, x in smp["classified"].items() if x.get("faceless_explainer"))
            mm[k] = metrics(list(smp["channels"]), p, z["pre"], z["sv_by"], z["news"], z["gap"], z["ov"])
        t, _ = total(mm["A"], mm["B"])
        out["split"][part] = {k: dict(total=round(t[k], 1), **{x: round(mm[k][x], 3) for x in
                              ("bo10", "news", "young_bo", "n_young", "top5", "eps", "eps_med", "spons", "pf", "ll", "slop")})
                              for k in "AB"}
    (DATA / "metrics_v2.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: out[k] for k in ("selfcheck", "total", "comp", "boot", "sens_AB", "split")}, indent=1, default=str))

if __name__ == "__main__":
    if sys.argv[1:] == ["selfcheck"]:
        print(selfcheck())
    else:
        main()
