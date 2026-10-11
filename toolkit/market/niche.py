"""Thước "kênh mới có bật được không" cho một ngách (`market niche <key>`; port channel-k2/final.py, bỏ phần riêng ngách G).

Thước chính (tự tính, không phải chỉ số YouTube): % kênh trẻ (< 730 ngày) ĐÚNG NGÁCH, không lộ mặt, có ≥ 1 video ≥ 8 phút
đăng 14–90 ngày trước đạt ≥ 10 nghìn lượt. Phụ: ≥ 50 nghìn; trung vị lượt xem/video. KTC 90 % Wilson.
Nhãn: model `judge` (lô 25 kênh); `reviewer` kiểm ngẫu nhiên 20 kênh (seed cố định).
"""
import datetime as dt, json, random, statistics as st
from math import sqrt
from core import MarketError, get, videos, channels, pubdt, pack_dir
import ai

SEED = 20261011
CRIT_FACE = ("faceless=true only if the channel's videos are explainers or documentaries most likely narrated over graphics/maps/"
             "animation/archival footage WITHOUT an on-camera host (no vlog, podcast, interview, talk show, news broadcast, reaction, "
             "lecture recording, TV network clip, presenter-led show).")


def wilson(k, n, z=1.645):
    if n == 0:
        return (None, None)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - h) / d * 100, 1), round((c + h) / d * 100, 1))


def plan(pack, key):
    q = pack["niches"][key]["q"]
    return {"search": len(q), "videos": len(q) + 40, "channels": 4, "playlistItems": 150}


def label(pack, key, ev, role, tag):
    crit = pack["niches"][key]["crit"]
    out = {}
    items = list(ev.items())
    for i in range(0, len(items), 25):
        lines = [json.dumps(dict(id=c, channel=e["name"], about=e["desc"][:400], recent_titles=e["titles"][:10]), ensure_ascii=False)
                 for c, e in items[i:i + 25]]
        p = (f"Label YouTube channels from their ~10 most recent upload titles and 'about' text. {CRIT_FACE} in_niche=true only if "
             f"the channel's MAIN subject is {crit}. Return ONLY JSON {{\"<id>\": {{\"faceless\": true|false, \"in_niche\": true|false}}}}.\n\n"
             + "\n".join(lines))
        out.update(ai.ask_cover(pack, role, p, f"{tag}-{key}-{i}", [c for c, _ in items[i:i + 25]]))
    return out


def run(pack, quota, key, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    LONG = pack["long_min_s"]
    after = (now - dt.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ids = []
    for q in pack["niches"][key]["q"]:
        j = get(pack, quota, "search", part="id", q=q, type="video", maxResults=25, publishedAfter=after,
                regionCode=pack["region"], relevanceLanguage=pack["language"], order="relevance")
        ids += [it["id"]["videoId"] for it in j.get("items", [])]
    lv = [v for v in videos(pack, quota, ids) if v["dur"] >= LONG and pubdt(v["pub"]) >= pubdt(after)]
    cands = sorted({v["ch"] for v in lv})
    meta = channels(pack, quota, cands)
    young = [c for c in cands if c in meta and (now - pubdt(meta[c]["created"])).days < 730]
    ev = {}
    for c in young:
        j = get(pack, quota, "playlistItems", part="snippet,contentDetails", playlistId=meta[c]["uploads"], maxResults=50)
        r = [dict(id=i["contentDetails"]["videoId"], title=i["snippet"]["title"],
                  pub=i["contentDetails"].get("videoPublishedAt") or i["snippet"]["publishedAt"]) for i in j.get("items", [])]
        ev[c] = dict(name=meta[c]["name"], desc=meta[c]["desc"], titles=[x["title"] for x in r[:10]], recent=r)
    lab = label(pack, key, ev, "judge", "niche")
    ok = [c for c in ev if lab[c].get("faceless") and lab[c].get("in_niche")]
    wids = [x["id"] for c in ok for x in ev[c]["recent"] if 14 <= (now - pubdt(x["pub"])).days <= 90]
    vs = [v for v in videos(pack, quota, wids) if v["dur"] >= LONG]
    by = {c: [v for v in vs if v["ch"] == c] for c in ok}
    act = [c for c in ok if by[c]]
    k10 = sum(any(v["views"] >= 10_000 for v in by[c]) for c in act)
    k50 = sum(any(v["views"] >= 50_000 for v in by[c]) for c in act)
    allv = [v["views"] for c in act for v in by[c]]
    pick = sorted(ev); random.Random(SEED).shuffle(pick); pick = pick[:20]
    op = label(pack, key, {c: ev[c] for c in pick}, "reviewer", "audit") if pick else {}
    agree = sum(bool(op[c].get("faceless") and op[c].get("in_niche")) == bool(lab[c].get("faceless") and lab[c].get("in_niche")) for c in pick)
    res = dict(key=key, name=pack["niches"][key]["name"], n_cands=len(cands), n_young=len(young), n_young_ok=len(ok),
               n_active=len(act), k10=k10, pct10=round(100 * k10 / len(act), 1) if act else None, ci10=wilson(k10, len(act)),
               k50=k50, ci50=wilson(k50, len(act)), med_views_video=st.median(allv) if allv else None,
               reviewer_n=len(pick), reviewer_agree=agree)
    (pack_dir(pack) / f"niche_{key}.json").write_text(json.dumps(dict(res, labels=lab, reviewer=op), ensure_ascii=False))
    return res
