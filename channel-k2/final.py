"""Gói kênh 2 — VÒNG CUỐI: một thước "kênh mới có bật được không" cho A, B, D, J.
Thước chính (tự tính, không phải chỉ số YouTube): % kênh trẻ (< 730 ngày) ĐÚNG NGÁCH, không lộ mặt, có ≥ 1 video ≥ 8 phút
đăng 14–90 ngày trước NOW đạt ≥ 10 nghìn lượt. Phụ: ≥ 50 nghìn; trung vị lượt xem/video của kênh trẻ đúng ngách. KTC 90 % Wilson.
Tập kênh: kênh có video ≥ 8 phút trong kết quả search.list (90 ngày, US). B dùng lại 659 kênh của 72 câu cầu hiện hành (cache).
Model ghim: Sonnet 5.5 gắn nhãn ngách + mặt; Opus 5.5 kiểm ngẫu nhiên 20 kênh. Tuổi kênh lấy từ API (publishedAt), không đoán.
Quota: chỉ một project/khoá của môi trường; trần đơn vị mỗi lượt chạy qua K2C_BUDGET (đếm cả search = 100).
G (chủ dự án 11/10 20:00): "Quyền lực kinh tế qua ba tầng"; nhãn thêm khung âm mưu (đếm riêng, không tính đúng ngách) và tầng.
Dùng: python final.py B | A | D | J | G [--nq N] [--noaudit] [--dry]   (--nq: chỉ N câu đầu, dùng cho đo nhanh G tối 11/10)"""
import json, os, random, statistics as st, sys, datetime as dt
from math import sqrt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import collect
from collect import DATA, NOW, LONG_S, get as _get, ai, purge

AFTER = (NOW - dt.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
SEED = 20261011
BUDGET = int(os.environ.get("K2C_BUDGET", "1000"))
used = {"units": 0}
NQ = int(sys.argv[sys.argv.index("--nq") + 1]) if "--nq" in sys.argv else None   # chỉ N câu đầu (đo nhanh)
ROUND_CAP = 11.0  # trần $12 của vòng cuối (chủ dự án 11/10 20:00), mã dừng ở $11, chừa phần cho REVIEWER Opus
PRIOR = 2.56      # chi phí vòng cuối đã tiêu ở container phiên trước (B: Sonnet $1,93 + Opus $0,63, REPORT.md); cost.jsonl đó đã mất

def round_spent():
    """Chi phí AI của vòng cuối = các dòng cost.jsonl có tag final-/audit-/review- (vòng trước không tính)."""
    if not collect.LOG.exists(): return PRIOR
    rows = [json.loads(l) for l in collect.LOG.read_text().splitlines() if l.strip()]
    return PRIOR + sum(r.get("usd", 0) for r in rows if r["tag"].split("-")[0] in ("final", "audit", "review", "gtop"))

collect.spent = lambda: round_spent() * collect.COST_CAP / ROUND_CAP   # ai() dừng khi chi phí vòng > ROUND_CAP

def get(ep, **p):
    """Như collect.get nhưng đếm đơn vị cho lệnh KHÔNG có trong cache, và dừng trước khi vượt trần."""
    key = DATA / f"api_{ep}_{collect.hashlib.sha1(json.dumps(p, sort_keys=True).encode()).hexdigest()[:12]}.json"
    cost = 0 if key.exists() else (100 if ep == "search" else 1)
    if used["units"] + cost > BUDGET:
        raise SystemExit(f"dừng: chạm trần {BUDGET} đơn vị lượt này (đã dùng {used['units']}); chạy lại sau khi quota đặt lại")
    used["units"] += cost
    return _get(ep, **p)

NICHE = {
 "A": dict(name="lịch sử tiền/ngân hàng/hệ thống kinh tế",
           crit="history of money, banking, central banks, currencies and economic/monetary systems, or the history of financial crises (explanatory; NOT personal-finance tips, investing or trading advice)",
           q=["history of the us dollar explained", "how did ancient people use money", "why do countries have central banks",
              "how did the 1970s inflation happen", "what was the panic of 1907", "how did medieval banking work",
              "why did the soviet economy collapse", "how did the dollar replace the british pound",
              "why did weimar germany print money", "how did the bank of england start"]),
 "B": dict(name="cơ chế kinh tế ngành / lịch sử doanh nghiệp",
           crit="the economic mechanisms of industries or companies: how an industry or business works and makes money, supply chains, business or industry history (NOT personal finance, investing tips, generic tech news or engineering-only content)",
           q=None),   # dùng tập kênh của current.py (72 câu, cache)
 "D": dict(name="bí ẩn trên bản đồ",
           crit="geography and map explainers: strange borders, enclaves, why places are where they are, empty or unusual regions, map mysteries (NOT travel vlogs or general trivia)",
           q=["why do borders look like this", "places that are not part of any country", "why do some countries have exclaves",
              "geography mysteries explained", "how enclaves and exclaves work", "why is nobody allowed to visit this island",
              "why does this river cause a border dispute", "why is this region empty on the map",
              "map facts that will surprise you", "why are some cities built in deserts"]),
 "J": dict(name="nhà ở & đô thị",
           crit="housing and cities: housing costs, zoning, urban planning, suburbs, transit, how cities are built (explanatory; NOT real-estate investing or home-buying advice)",
           q=["why are starter homes disappearing", "how single family zoning started", "why do american cities have so many parking lots",
              "why is it so hard to build apartments in the us", "how highways destroyed american neighborhoods", "why are new houses so big",
              "why are mobile homes so cheap", "how cities decide where to build", "why did tokyo keep housing affordable",
              "why do americans live in suburbs"]),
}
# G: câu hỏi trộn 3 tầng (1 gia tộc/tập đoàn lịch sử gắn ngành + địa lý · 2 địa chính trị gần đây · 3 sản phẩm kinh tế mới).
# 7 câu đầu đo nhanh tối 11/10 (3/2/2 tầng); 3 câu sau chạy 12/10. Không trùng câu của A.
G_Q = [("how did andrew carnegie build the steel industry", 1), ("how did rockefeller control the oil industry", 1),
       ("history of the rothschild banking family", 1), ("how do tariffs actually work", 2),
       ("how do sanctions affect russia's economy", 2), ("what are stablecoins and how do they work", 3),
       ("what is a central bank digital currency", 3), ("how jp morgan saved the us financial system", 1),
       ("why are countries moving away from the us dollar", 2), ("what is private credit and why is it growing", 3)]
NICHE["G"] = dict(name="quyền lực kinh tế qua ba tầng",
    crit="economic power explained through mechanisms and sources, in any of three layers: (1) historical business dynasties, "
         "trusts and banking houses tied to their industries (steel, oil, railroads, banking) and geography; (2) recent "
         "geopolitical-economic shifts (tariffs, sanctions, supply chains, energy, reserve currencies); (3) new economic or "
         "financial products and systems (stablecoins, CBDCs, asset tokenization, private credit, new payment systems) "
         "(explanatory; NOT investing/trading advice, NOT crypto price talk, NOT conspiracy content)",
    q=[q for q, _ in G_Q])
G_EXTRA = ("ALSO give: conspiracy=true if the channel frames families or groups of people as hidden forces secretly controlling "
           "the world/events, or uses ethnic or religious stereotypes; tier = 1 (historical dynasties/trusts/banking houses), "
           "2 (recent geopolitics/economic shifts), 3 (new financial products/systems), \"bridge\" (regularly connects layers) "
           "or null if none; templated=true if the recent titles repeat one fill-in-the-blank formula (mass-production pattern). "
           "Return ONLY JSON {\"<id>\": {\"faceless\": true|false, \"in_niche\": true|false, \"conspiracy\": true|false, "
           "\"tier\": 1|2|3|\"bridge\"|null, \"templated\": true|false}}.")

def pubdt(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))

def wilson(k, n, z=1.645):
    if n == 0: return (None, None)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - h) / d * 100, 1), round((c + h) / d * 100, 1))

def videos(ids):
    out = []
    for i in range(0, len(ids), 50):
        j = get("videos", part="snippet,contentDetails,statistics", id=",".join(ids[i:i+50]), maxResults=50)
        for v in j.get("items", []):
            out.append(dict(id=v["id"], ch=v["snippet"]["channelId"], title=v["snippet"]["title"], desc=v["snippet"].get("description", "")[:600],
                            pub=v["snippet"]["publishedAt"], dur=collect.dur(v["contentDetails"].get("duration")),
                            views=int(v.get("statistics", {}).get("viewCount", 0))))
    return out

def channels(cids):
    out = {}
    cids = list(dict.fromkeys(cids))
    for i in range(0, len(cids), 50):   # cùng tham số với current.channels_meta → trúng cache cho B
        j = get("channels", part="snippet,statistics,contentDetails", id=",".join(cids[i:i+50]), maxResults=50)
        for c in j.get("items", []):
            out[c["id"]] = dict(name=c["snippet"]["title"], created=c["snippet"]["publishedAt"], desc=c["snippet"].get("description", "")[:600],
                                subs=int(c["statistics"].get("subscriberCount", 0) or 0), uploads=c["contentDetails"]["relatedPlaylists"]["uploads"])
    return out

def candidates(key):
    """Tập kênh ứng viên: kênh có video ≥ 8 phút trong kết quả tìm kiếm 90 ngày, US."""
    if key == "B":
        dem = json.loads((DATA / "current_demand.json").read_text())
        return sorted({v["ch"] for vs in dem["videos"].values() for v in vs})
    ids = []
    for q in NICHE[key]["q"][:NQ]:
        j = get("search", part="id", q=q, type="video", maxResults=25, publishedAfter=AFTER,
                regionCode="US", relevanceLanguage="en", order="relevance")
        ids += [it["id"]["videoId"] for it in j.get("items", [])]
    ids = list(dict.fromkeys(ids))
    lv = [v for v in videos(ids) if v["dur"] >= LONG_S and pubdt(v["pub"]) >= pubdt(AFTER)]
    SEARCH_LONG[key] = lv
    return sorted({v["ch"] for v in lv})

SEARCH_LONG = {}

def gtop(lv, qtier):
    """G: 20 video ≥ 8 phút nhiều lượt xem nhất trong mẫu tìm kiếm (đăng 14–90 ngày) — Sonnet chấm khung âm mưu + tầng."""
    top = sorted([v for v in lv if (NOW - pubdt(v["pub"])).days >= 14], key=lambda v: -v["views"])[:20]
    cf = DATA / "gtop_labels.json"
    cache = json.loads(cf.read_text()) if cf.exists() else {}
    need = [v for v in top if v["id"] not in cache]
    if need:
        p = ("For each YouTube video (title + description) answer: conspiracy=true if it frames families or groups of people as "
             "hidden forces secretly controlling the world/events, or uses ethnic or religious stereotypes; tier = 1 (historical "
             "dynasties/trusts/banking houses tied to industries), 2 (recent geopolitics/economic shifts: tariffs, sanctions, supply "
             "chains, energy, reserve currencies), 3 (new financial products/systems: stablecoins, CBDCs, tokenization, private "
             "credit, payments), \"bridge\" (connects layers) or null (none of these). Return ONLY JSON {\"<id>\": "
             "{\"conspiracy\": true|false, \"tier\": 1|2|3|\"bridge\"|null}}.\n\n" +
             "\n".join(f'{v["id"]} | {v["title"]} | {v["desc"][:400]!r}' for v in need))
        cache.update({k: x for k, x in ai(p, f"gtop-G-{len(cache)}", model="claude-sonnet-5-5").items()})
        cf.write_text(json.dumps(cache))
    if any(v["id"] not in cache for v in top):
        raise SystemExit("thiếu nhãn video top G")
    return [dict(id=v["id"], title=v["title"], views=v["views"], min=round(v["dur"] / 60), q_tier=qtier.get(v["id"]),
                 **cache[v["id"]]) for v in top]

def recent(c):
    j = get("playlistItems", part="snippet,contentDetails", playlistId=c["uploads"], maxResults=50)
    return [dict(id=i["contentDetails"]["videoId"], title=i["snippet"]["title"],
                 pub=i["contentDetails"].get("videoPublishedAt") or i["snippet"]["publishedAt"]) for i in j.get("items", [])]

CRIT_FACE = ("faceless=true only if the channel's videos are explainers or documentaries most likely narrated over graphics/maps/"
             "animation/archival footage WITHOUT an on-camera host (no vlog, podcast, interview, talk show, news broadcast, reaction, "
             "lecture recording, TV network clip, presenter-led show).")

def label(key, ev, model, tag):
    """Gắn nhãn faceless + in_niche theo lô 25 kênh; dừng nếu thiếu nhãn. Cache theo kênh (gộp mẫu G qua hai ngày không gắn lại)."""
    cf = DATA / f"labels_{key}_{model}.json"
    cache = json.loads(cf.read_text()) if cf.exists() else {}
    out = {c: cache[c] for c in ev if c in cache}
    items = [(c, e) for c, e in ev.items() if c not in cache]
    B = 25   # cùng cỡ lô cho mọi ngách, gắn nhãn y như B (chủ dự án 11/10)
    for i in range(0, len(items), B):
        lines = [json.dumps(dict(id=cid, channel=e["name"], about=e["desc"][:400], recent_titles=e["titles"][:10]), ensure_ascii=False)
                 for cid, e in items[i:i+B]]
        p = (f"Label YouTube channels from their ~10 most recent upload titles and 'about' text. {CRIT_FACE} in_niche=true only if "
             f"the channel's MAIN subject is {NICHE[key]['crit']}. Return ONLY JSON {{\"<id>\": {{\"faceless\": true|false, "
             "\"in_niche\": true|false}}}.\n\n" + "\n".join(lines))
        if key == "G":   # G: prompt gốc + phần thêm (khung âm mưu, tầng, khuôn tiêu đề)
            fmt = 'Return ONLY JSON {"<id>": {"faceless": true|false, "in_niche": true|false}}}.'   # nguyên văn prompt gốc (kể cả dấu } thừa)
            assert fmt in p
            p = p.replace(fmt, G_EXTRA, 1)
        got = {c: x for c, x in ai(p, f"{tag}-{key}-{i}", model=model).items() if c in ev}
        out.update(got); cache.update(got); cf.write_text(json.dumps(cache))
    miss = [c for c in ev if c not in out]
    if miss:   # gắn lại một lượt cho lô hỏng JSON
        out.update(label(key, {c: ev[c] for c in miss}, model, tag + "-retry") if tag.count("retry") < 1 else {})
    if any(c not in out for c in ev):
        raise SystemExit(f"thiếu nhãn {key}: {sum(c in out for c in ev)}/{len(ev)}")
    return out

def run(key):
    f = DATA / f"final_{key}{'_nq%d' % NQ if NQ else ''}.json"
    if f.exists(): return json.loads(f.read_text())
    cands = candidates(key)
    if key == "B":   # siêu dữ liệu kênh đã có trong cache của current.py (0 đơn vị)
        meta = {c: m for c, m in json.loads((DATA / "current_demand.json").read_text())["channels"].items() if c in set(cands)}
    else:
        meta = channels(cands)
    young = [c for c in cands if c in meta and (NOW - pubdt(meta[c]["created"])).days < 730]
    ev = {}
    for cid in young:
        r = recent(meta[cid])
        ev[cid] = dict(name=meta[cid]["name"], desc=meta[cid]["desc"], created=meta[cid]["created"][:10], subs=meta[cid]["subs"],
                       titles=[x["title"] for x in r[:10]], recent=r)
    lab = label(key, ev, "claude-sonnet-5-5", "final")
    # G: kênh khung âm mưu KHÔNG tính đúng ngách (đếm riêng)
    ok = [c for c in ev if lab[c].get("faceless") and lab[c].get("in_niche") and not lab[c].get("conspiracy")]
    # video 14–90 ngày trước NOW của kênh trẻ đúng ngách (gom 50 ID/lệnh)
    ids = [x["id"] for c in ok for x in ev[c]["recent"] if 14 <= (NOW - pubdt(x["pub"])).days <= 90]
    vs = [v for v in videos(ids) if v["dur"] >= LONG_S]
    by = {c: [v for v in vs if v["ch"] == c] for c in ok}
    act = [c for c in ok if by[c]]           # kênh có ≥ 1 video dài trong cửa sổ (kênh còn hoạt động)
    k10 = sum(any(v["views"] >= 10_000 for v in by[c]) for c in act)
    k50 = sum(any(v["views"] >= 50_000 for v in by[c]) for c in act)
    allv = [v["views"] for c in act for v in by[c]]
    chmed = [st.median(v["views"] for v in by[c]) for c in act]
    # Opus kiểm ngẫu nhiên 20 kênh trẻ (trong toàn bộ kênh trẻ đã gắn nhãn)
    pick = sorted(ev); random.Random(SEED).shuffle(pick); pick = pick[:20]
    if "--noaudit" in sys.argv: pick = []
    op = label(key, {c: ev[c] for c in pick}, "claude-opus-5-5", "audit") if pick else {}
    agree = sum(op[c].get("faceless") == lab[c].get("faceless") and op[c].get("in_niche") == lab[c].get("in_niche") for c in pick)
    agree_ok = sum(bool(op[c].get("faceless") and op[c].get("in_niche")) == bool(lab[c].get("faceless") and lab[c].get("in_niche")) for c in pick)
    res = dict(key=key, name=NICHE[key]["name"], n_cands=len(cands), n_meta=len(meta), n_young=len(young), n_young_ok=len(ok),
               n_active=len(act), k10=k10, k50=k50, pct10=round(100 * k10 / len(act), 1) if act else None, ci10=wilson(k10, len(act)),
               pct50=round(100 * k50 / len(act), 1) if act else None, ci50=wilson(k50, len(act)),
               med_views_video=st.median(allv) if allv else None, med_of_channel_medians=st.median(chmed) if chmed else None,
               n_videos=len(allv), opus_n=len(pick), opus_agree_both=agree, opus_agree_ok=agree_ok,
               units=used["units"], labels=lab, opus=op,
               channels={c: dict(name=ev[c]["name"], created=ev[c]["created"], subs=ev[c]["subs"],
                                 best=max([v["views"] for v in by.get(c, [])], default=None)) for c in ok})
    if key == "G":
        res.update(g_extra(ev, lab, ok, act, by, pick, op))
    f.write_text(json.dumps(res, ensure_ascii=False))
    return res

def g_extra(ev, lab, ok, act, by, pick, op):
    """G: khung âm mưu (kênh + video top), tầng có cầu, kênh trẻ làm hàng loạt."""
    qt = {}
    for q, t in G_Q[:NQ]:   # tầng theo câu hỏi đã tìm (để biết video top đến từ câu tầng nào)
        j = get("search", part="id", q=q, type="video", maxResults=25, publishedAfter=AFTER,
                regionCode="US", relevanceLanguage="en", order="relevance")   # trúng cache, 0 đơn vị
        for it in j.get("items", []): qt.setdefault(it["id"]["videoId"], t)
    top = gtop(SEARCH_LONG["G"], qt)
    face = [c for c in ev if lab[c].get("faceless")]
    consp = [c for c in ev if lab[c].get("conspiracy")]
    tiers = {}
    for t in (1, 2, 3, "bridge"):
        a = [c for c in act if lab[c].get("tier") == t]
        tv = [v for v in top if v["tier"] == t]
        tiers[str(t)] = dict(young_ok=sum(lab[c].get("tier") == t for c in ok), active=len(a),
                             k10=sum(any(v["views"] >= 10_000 for v in by[c]) for c in a),
                             top20=len(tv), top20_views=sum(v["views"] for v in tv))
    sq = [v for v in SEARCH_LONG["G"] if (NOW - pubdt(v["pub"])).days >= 14]
    for t in (1, 2, 3):   # cầu theo câu hỏi tầng t: số video ≥ 10 nghìn và lượt xem cao nhất trong kết quả
        vt = [v for v in sq if qt.get(v["id"]) == t]
        tiers[str(t)].update(q_n=sum(tt == t for _, tt in G_Q[:NQ]), q_long=len(vt), q_10k=sum(v["views"] >= 10_000 for v in vt),
                             q_max=max([v["views"] for v in vt], default=0))
    # hàng loạt: nhịp dày = ≥ 12 video tải lên trong 28 ngày trước NOW (≥ 3/tuần); khuôn tiêu đề = nhãn Sonnet templated
    dense = {c: sum(0 <= (NOW - pubdt(x["pub"])).days <= 28 for x in ev[c]["recent"]) >= 12 for c in ok}
    tmpl = {c: bool(lab[c].get("templated")) for c in ok}
    return dict(g_consp_young=len(consp), g_consp_faceless=sum(c in consp for c in face),
                g_consp_rate_faceless=round(100 * sum(c in consp for c in face) / len(face), 1) if face else None,
                g_top20=top, g_top_consp=sum(v["conspiracy"] for v in top), g_top_n=len(top),
                g_top_consp_ci=wilson(sum(v["conspiracy"] for v in top), len(top)), g_tiers=tiers,
                g_mass=dict(n=len(ok), dense=sum(dense.values()), templated=sum(tmpl.values()),
                            both=sum(dense[c] and tmpl[c] for c in ok), either=sum(dense[c] or tmpl[c] for c in ok)),
                g_opus_consp_agree=sum(bool(op[c].get("conspiracy")) == bool(lab[c].get("conspiracy")) for c in pick) if pick else None)

if __name__ == "__main__":
    key = sys.argv[1]
    cfg = NICHE[key]
    if "--dry" in sys.argv:   # kiểm cấu hình không gọi mạng
        assert cfg["q"] is None or (len(cfg["q"]) == 10 and len(set(cfg["q"])) == 10), "cần đúng 10 câu khác nhau"
        assert not set(NICHE["G"]["q"]) & set(NICHE["A"]["q"]), "G trùng câu A"
        print(key, cfg["name"], "câu hỏi:", len(cfg["q"] or []), "search.list dự kiến:", len(cfg["q"] or []), "OK"); sys.exit()
    purge()
    r = run(key)
    print(json.dumps({k: v for k, v in r.items() if k not in ("labels", "opus", "channels", "g_top20")}, ensure_ascii=False))
    print("calls", collect.calls, "units lượt này", used["units"], f"AI vòng cuối ${round_spent():.2f}")
