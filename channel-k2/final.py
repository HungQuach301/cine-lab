"""Gói kênh 2 — VÒNG CUỐI: một thước "kênh mới có bật được không" cho A, B, D, J.
Thước chính (tự tính, không phải chỉ số YouTube): % kênh trẻ (< 730 ngày) ĐÚNG NGÁCH, không lộ mặt, có ≥ 1 video ≥ 8 phút
đăng 14–90 ngày trước NOW đạt ≥ 10 nghìn lượt. Phụ: ≥ 50 nghìn; trung vị lượt xem/video của kênh trẻ đúng ngách. KTC 90 % Wilson.
Tập kênh: kênh có video ≥ 8 phút trong kết quả search.list (90 ngày, US). B dùng lại 659 kênh của 72 câu cầu hiện hành (cache).
Model ghim: Sonnet 5.5 gắn nhãn ngách + mặt; Opus 5.5 kiểm ngẫu nhiên 20 kênh. Tuổi kênh lấy từ API (publishedAt), không đoán.
Quota: chỉ một project/khoá của môi trường; trần đơn vị mỗi lượt chạy qua K2C_BUDGET (đếm cả search = 100).
Dùng: python final.py B | A | D | J [--dry]   (--dry: kiểm cấu hình, không gọi mạng)"""
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
ROUND_CAP = 4.4   # trần $5 của vòng cuối, chừa ~$0,6 cho REVIEWER Opus

def round_spent():
    """Chi phí AI của vòng cuối = các dòng cost.jsonl có tag final-/audit-/review- (vòng trước không tính)."""
    if not collect.LOG.exists(): return 0.0
    rows = [json.loads(l) for l in collect.LOG.read_text().splitlines() if l.strip()]
    return sum(r.get("usd", 0) for r in rows if r["tag"].split("-")[0] in ("final", "audit", "review"))

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
    for q in NICHE[key]["q"]:
        j = get("search", part="id", q=q, type="video", maxResults=25, publishedAfter=AFTER,
                regionCode="US", relevanceLanguage="en", order="relevance")
        ids += [it["id"]["videoId"] for it in j.get("items", [])]
    ids = list(dict.fromkeys(ids))
    return sorted({v["ch"] for v in videos(ids) if v["dur"] >= LONG_S and pubdt(v["pub"]) >= pubdt(AFTER)})

def recent(c):
    j = get("playlistItems", part="snippet,contentDetails", playlistId=c["uploads"], maxResults=50)
    return [dict(id=i["contentDetails"]["videoId"], title=i["snippet"]["title"],
                 pub=i["contentDetails"].get("videoPublishedAt") or i["snippet"]["publishedAt"]) for i in j.get("items", [])]

CRIT_FACE = ("faceless=true only if the channel's videos are explainers or documentaries most likely narrated over graphics/maps/"
             "animation/archival footage WITHOUT an on-camera host (no vlog, podcast, interview, talk show, news broadcast, reaction, "
             "lecture recording, TV network clip, presenter-led show).")

def label(key, ev, model, tag):
    """Gắn nhãn faceless + in_niche theo lô 25 kênh; dừng nếu thiếu nhãn."""
    out, items = {}, list(ev.items())
    B = 25 if key == "B" else 50   # A/D/J: lô 50 kênh để giảm chi phí cố định mỗi lệnh (B đã chạy với lô 25)
    for i in range(0, len(items), B):
        lines = [json.dumps(dict(id=cid, channel=e["name"], about=e["desc"][:400], recent_titles=e["titles"][:10]), ensure_ascii=False)
                 for cid, e in items[i:i+B]]
        p = (f"Label YouTube channels from their ~10 most recent upload titles and 'about' text. {CRIT_FACE} in_niche=true only if "
             f"the channel's MAIN subject is {NICHE[key]['crit']}. Return ONLY JSON {{\"<id>\": {{\"faceless\": true|false, "
             "\"in_niche\": true|false}}}.\n\n" + "\n".join(lines))
        out.update(ai(p, f"{tag}-{key}-{i}", model=model))
    miss = [c for c in ev if c not in out]
    if miss:   # gắn lại một lượt cho lô hỏng JSON
        out.update(label(key, {c: ev[c] for c in miss}, model, tag + "-retry") if tag.count("retry") < 1 else {})
    if any(c not in out for c in ev):
        raise SystemExit(f"thiếu nhãn {key}: {sum(c in out for c in ev)}/{len(ev)}")
    return out

def run(key):
    f = DATA / f"final_{key}.json"
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
    ok = [c for c in ev if lab[c].get("faceless") and lab[c].get("in_niche")]
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
    op = label(key, {c: ev[c] for c in pick}, "claude-opus-5-5", "audit")
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
    f.write_text(json.dumps(res, ensure_ascii=False))
    return res

if __name__ == "__main__":
    key = sys.argv[1]
    cfg = NICHE[key]
    if "--dry" in sys.argv:   # kiểm cấu hình không gọi mạng
        assert cfg["q"] is None or (len(cfg["q"]) == 10 and len(set(cfg["q"])) == 10), "cần đúng 10 câu khác nhau"
        print(key, cfg["name"], "câu hỏi:", len(cfg["q"] or []), "search.list dự kiến:", len(cfg["q"] or []), "OK"); sys.exit()
    purge()
    r = run(key)
    print(json.dumps({k: v for k, v in r.items() if k not in ("labels", "opus", "channels")}, ensure_ascii=False))
    print("calls", collect.calls, "units lượt này", used["units"], f"AI vòng cuối ${round_spent():.2f}")
