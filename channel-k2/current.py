"""Gói kênh 2 — kiểm cầu hiện hành (12 đề tài × 6 câu hỏi) và kiểm nhãn bộ lọc kênh cũ.
Dùng lại get/videos/ai của collect.py (cache API, số liệu thô ngoài git ở $K2C_DATA, xoá > 30 ngày, trần AI $5).
Model ghim (chủ dự án 11/10): lọc kênh + liên quan/khoảng trống = claude-sonnet-5-5; bộ lọc CŨ tái lập đúng như market-k2
(Haiku, cùng prompt) chỉ để đo sai số của nó; REVIEWER = claude-opus-5-5. Mọi chỉ số: tự tính, không phải chỉ số YouTube.
Dùng: K2C_NOWAIT=1 python current.py demand | labels | all"""
import json, os, random, statistics as st, sys, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import collect
from collect import DATA, NOW, LONG_S, get, videos, ai, purge

AFTER = (NOW - dt.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
BIG = 50_000
SEED = 20261011

# 6 câu hỏi khán giả/đề tài (≤ 72 search.list). Câu trùng nguyên văn với lượt `labels` trước dùng lại cache, không tốn quota.
Q = {
 "container": ["how shipping containers changed the world", "how does container shipping work", "why is shipping so cheap",
               "how do container ships work", "how do ports work", "how global supply chains work"],
 "jet-airliner": ["why are there only two airplane manufacturers", "why can't anyone compete with boeing and airbus",
                  "how hard is it to build a commercial airplane", "how are airplanes built",
                  "why is building a new airliner so expensive", "how are jet engines made"],
 "card-networks": ["how do visa and mastercard make money", "what happens when you swipe a credit card",
                   "who pays credit card swipe fees", "how do credit card companies make money",
                   "how does a card payment work", "what are interchange fees"],
 "amazon-warehouse": ["what happens when amazon builds a warehouse in your town", "how amazon warehouses change towns",
                      "how amazon fulfillment centers work", "is amazon good for local economies",
                      "how warehouses changed small towns", "why amazon builds warehouses everywhere"],
 "chips": ["why is it so hard to make semiconductors", "why can only taiwan make advanced chips", "how are computer chips made",
           "why are chip factories so expensive", "how does asml make chip machines", "why can't america make advanced chips"],
 "airlines": ["how do airlines make money", "how airlines really make money", "why airlines make money from credit cards",
              "how do airline loyalty programs make money", "why are airlines so unprofitable", "how airline ticket pricing works"],
 "dollar-general": ["how dollar general took over rural america", "why are there so many dollar general stores",
                    "how dollar stores make money", "what happens when dollar general comes to town",
                    "why dollar stores are everywhere", "how dollar general chooses locations"],
 "malls": ["why are american malls dying", "what happened to shopping malls", "the death of the american mall",
           "why malls are failing", "what is replacing dead malls", "how malls make money"],
 "factory-town": ["how a factory changed a small town", "what happens to a town when the factory closes",
                  "company towns in america explained", "how one plant can support a whole town",
                  "why factory towns decline", "how manufacturing shaped small town america"],
 "card-rewards": ["who pays for credit card rewards", "how do credit card rewards work", "how do credit card companies afford rewards",
                  "are credit card points a scam", "how credit card points make money for banks", "why do credit cards give cash back"],
 "supermarkets": ["how do supermarkets make money", "how grocery stores make money", "the economics of grocery stores",
                  "how supermarket margins work", "why grocery stores put milk in the back", "how do grocery chains compete"],
 "retail-abroad": ["why american retailers fail abroad", "why walmart failed in germany", "why target failed in canada",
                   "why american companies fail in china", "why us stores fail in europe", "why some brands fail internationally"],
}
TITLE = {"container": "The Steel Box That Rewired World Trade", "jet-airliner": "Why Only Two Companies Can Still Build a Jet Airliner",
         "card-networks": "How Visa and Mastercard Make Money Without Lending a Cent", "amazon-warehouse": "How a Single Amazon Warehouse Changes Its Town",
         "chips": "Why Only a Handful of Countries Can Make Advanced Chips", "airlines": "How Airlines Really Make Money (It's Not the Seats)",
         "dollar-general": "How a Single Dollar General Changes a Rural Town", "malls": "The Collapse of the American Shopping Mall",
         "factory-town": "How a Single Factory Holds Up a Small Town", "card-rewards": "Who Actually Pays for Credit Card Rewards?",
         "supermarkets": "How Supermarkets Really Make Money", "retail-abroad": "Why American Retailers Usually Fail Abroad"}
# Điểm thí điểm = số video ≥ 50 nghìn ĐÚNG ĐỀ TÀI × hợp 3D (1–3) × rủi ro pháp lý thấp (1–3). Hai thang định tính
# đặt TRƯỚC khi có số đo, theo NHAN-DIEN.md (bộ cảnh) và LUAT-NOI-DUNG.md (công ty đơn lẻ, YMYL, tranh chấp).
FIT3D = {"container": 3, "jet-airliner": 3, "chips": 3, "factory-town": 3, "amazon-warehouse": 2, "dollar-general": 2, "malls": 2,
         "airlines": 2, "card-networks": 2, "supermarkets": 2, "card-rewards": 1, "retail-abroad": 1}
LEGAL = {"container": 3, "malls": 3, "factory-town": 3, "supermarkets": 3, "jet-airliner": 2, "chips": 2, "amazon-warehouse": 2,
         "airlines": 2, "retail-abroad": 2, "dollar-general": 1, "card-networks": 1, "card-rewards": 1}

def pubdt(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))

def search_topic(slug):
    hits = []
    for q in Q[slug]:
        j = get("search", part="id", q=q, type="video", maxResults=25, publishedAfter=AFTER,
                regionCode="US", relevanceLanguage="en", order="relevance")
        hits += [(q, it["id"]["videoId"]) for it in j.get("items", [])]
    ids = list(dict.fromkeys(v for _, v in hits))
    qof = {}
    for q, v in hits: qof.setdefault(v, q)
    lv = [v for v in videos(ids) if v["dur"] >= LONG_S and pubdt(v["pub"]) >= pubdt(AFTER)]
    for v in lv: v["q"] = qof[v["id"]]
    return lv

def channels_meta(cids):
    out = {}
    cids = list(dict.fromkeys(cids))
    for i in range(0, len(cids), 50):
        j = get("channels", part="snippet,statistics,contentDetails", id=",".join(cids[i:i+50]), maxResults=50)
        for c in j.get("items", []):
            out[c["id"]] = dict(name=c["snippet"]["title"], created=c["snippet"]["publishedAt"],
                                desc=c["snippet"].get("description", "")[:600],
                                subs=int(c["statistics"].get("subscriberCount", 0) or 0),
                                uploads=c["contentDetails"]["relatedPlaylists"]["uploads"])
    return out

def relevance(slug, vids):
    """Sonnet: video ≥ 50 nghìn có ĐÚNG đề tài không (search trả cả video lạc đề)."""
    if not vids: return {}
    lines = [f'{v["id"]} | {v["title"]} | {v["desc"][:400]!r}' for v in vids]
    p = (f"Planned explainer episode: \"{TITLE[slug]}\". For each YouTube video (title + description) decide on_topic=true "
         "only if a viewer searching for that episode's subject would see it as a direct competitor (same subject and similar "
         "question), not merely the same broad field (e.g. personal-finance tips, news clips, travel vlogs, product reviews are "
         "off-topic unless they answer the episode's question). Return ONLY JSON {\"<videoId>\": {\"on_topic\": true|false}}.\n\n"
         + "\n".join(lines))
    r = ai(p, f"rel-{slug}", model="claude-sonnet-5-5")
    miss = [v["id"] for v in vids if v["id"] not in r]
    if miss:
        raise SystemExit(f"nhãn liên quan thiếu {slug}: {len(miss)}/{len(vids)}")
    return r

def demand():
    f = DATA / "current_demand.json"
    if f.exists(): return json.loads(f.read_text())
    res, allv = {}, {}
    for slug in Q:
        allv[slug] = search_topic(slug)
        print(slug, len(allv[slug]), "video dài 90 ngày", collect.calls, flush=True)
    meta = channels_meta([v["ch"] for vs in allv.values() for v in vs])
    for slug, lv in allv.items():
        big = sorted([v for v in lv if v["views"] >= BIG], key=lambda v: -v["views"])
        rel = relevance(slug, big)
        on = [v for v in big if rel.get(v["id"], {}).get("on_topic")]
        def young(cid):
            c = meta.get(cid)
            return bool(c) and (NOW - pubdt(c["created"])).days < 730
        top = max(lv, key=lambda v: v["views"]) if lv else None
        ontop = on[0] if on else None
        label = "Mạnh" if len(on) >= 2 else ("Yếu" if len(on) == 1 else "Không")
        res[slug] = dict(title=TITLE[slug], n_long=len(lv), n_ch_long=len({v["ch"] for v in lv}),
                         n_big_raw=len(big), n_big=len(on), n_big_ch=len({v["ch"] for v in on}),
                         young_share_big=(sum(young(v["ch"]) for v in on) / len(on)) if on else None,
                         young_share_long=(sum(young(v["ch"]) for v in lv) / len(lv)) if lv else None,
                         top_any=dict(title=top["title"], views=top["views"], ch=top["chname"], pub=top["pub"][:10],
                                      on_topic=rel.get(top["id"], {}).get("on_topic")) if top else None,
                         top_on=dict(title=ontop["title"], views=ontop["views"], ch=ontop["chname"], pub=ontop["pub"][:10],
                                     min=round(ontop["dur"] / 60, 1), young=young(ontop["ch"])) if ontop else None,
                         big=[dict(title=v["title"], views=v["views"], ch=v["chname"], pub=v["pub"][:10], min=round(v["dur"] / 60, 1),
                                   on_topic=rel.get(v["id"], {}).get("on_topic"), young=young(v["ch"])) for v in big],
                         label=label, fit3d=FIT3D[slug], legal=LEGAL[slug], score=len(on) * FIT3D[slug] * LEGAL[slug])
    out = dict(topics=res, videos={s: lv for s, lv in allv.items()}, channels=meta, calls=dict(collect.calls))
    f.write_text(json.dumps(out, ensure_ascii=False))
    return out

# ---------- Kiểm nhãn bộ lọc kênh cũ ----------
OLD_PROMPT = ("You classify YouTube channels from ONE sample video's title and description. "   # nguyên văn market-k2/collect.py
              "faceless_explainer=true only if the content is an explainer or documentary-style video that is "
              "most likely narrated over graphics/maps/animation/archival footage WITHOUT an on-camera host "
              "(no vlog, podcast, interview, talk show, news broadcast, reaction, lecture recording, TV network clip). "
              "Return ONLY JSON: {\"<channelId>\": {\"faceless_explainer\": true|false}}.\n\n")

def old_filter(cands):
    """Tái lập đúng bộ lọc market-k2: Haiku, 1 video mẫu (video nhiều lượt xem nhất của kênh trong mẫu tìm kiếm)."""
    f = DATA / "oldfilter.json"
    if f.exists(): return json.loads(f.read_text())
    out, items = {}, list(cands.items())
    for i in range(0, len(items), 80):
        lines = [f'{cid} | channel: {vs[0]["chname"]} | title: {vs[0]["title"]} | desc: {vs[0]["desc"][:300]!r}' for cid, vs in items[i:i+80]]
        out.update(ai(OLD_PROMPT + "\n".join(lines), f"oldfilter-{i}", model="claude-haiku-5-5"))
    if len(set(out) & set(cands)) < 0.95 * len(cands):
        raise SystemExit(f"bộ lọc cũ thiếu nhãn: {len(set(out) & set(cands))}/{len(cands)}")
    f.write_text(json.dumps(out))
    return out

def recent_long(c):
    j = get("playlistItems", part="contentDetails", playlistId=c["uploads"], maxResults=50)
    ids = [i["contentDetails"]["videoId"] for i in j.get("items", [])]
    return sorted([v for v in videos(ids) if v["dur"] >= LONG_S], key=lambda v: v["pub"], reverse=True)

def exploded(c, vs):
    """Định nghĩa market-k2: ≥ 3× trung vị kênh trong ±90 ngày hoặc ≥ 3× người đăng ký, cộng điều kiện ≥ 10 nghìn; bỏ video < 14 ngày."""
    ok = [v for v in vs if (NOW - pubdt(v["pub"])).days >= 14]
    for v in ok:
        win = [w["views"] for w in ok if abs((pubdt(w["pub"]) - pubdt(v["pub"])).days) <= 90]
        med = st.median(win) if win else 0
        if v["views"] >= 10_000 and (v["views"] >= 3 * med or (c["subs"] and v["views"] >= 3 * c["subs"])):
            return True
    return False

def labels(dem):
    f = DATA / "label_audit.json"
    if f.exists(): return json.loads(f.read_text())
    cands = {}
    for slug, lv in dem["videos"].items():
        for v in sorted(lv, key=lambda x: -x["views"]):
            cands.setdefault(v["ch"], []).append(v)
    for cid in cands: cands[cid].sort(key=lambda v: -v["views"])
    old = old_filter(cands)
    passed = sorted(c for c in cands if old.get(c, {}).get("faceless_explainer"))
    random.Random(SEED).shuffle(passed)
    sample = passed[:50]
    meta = channels_meta(sample)
    ev = {}
    for cid in sample:
        c = meta[cid]
        vs = recent_long(c)
        ev[cid] = dict(name=c["name"], desc=c["desc"], created=c["created"][:10], subs=c["subs"],
                       young=(NOW - pubdt(c["created"])).days < 730, exploded=exploded(c, vs),
                       titles=[v["title"] for v in vs[:10]], sample_desc=[v["desc"][:300] for v in vs[:2]])
    lines = [json.dumps(dict(id=cid, channel=e["name"], about=e["desc"][:400], recent_long_titles=e["titles"],
                             two_descriptions=e["sample_desc"]), ensure_ascii=False) for cid, e in ev.items()]
    crit = ("faceless_explainer=true only if the channel's long videos are explainers or documentaries most likely narrated over "
            "graphics/maps/animation/archival footage WITHOUT an on-camera host (no vlog, podcast, interview, talk show, news "
            "broadcast, reaction, lecture recording, TV network clip, presenter-led show). in_niche_B=true only if the channel's "
            "main subject is business/industry history or the economics of companies and industries.")
    son = ai("You audit YouTube channel labels using ~10 recent long video titles, the channel 'about' text and two "
             "descriptions. " + crit + " Return ONLY JSON {\"<id>\": {\"faceless_explainer\": true|false, \"in_niche_B\": "
             "true|false, \"why\": \"<= 15 words\"}}.\n\n" + "\n".join(lines), "audit-sonnet", model="claude-sonnet-5-5")
    if len(set(son) & set(ev)) < len(ev):
        raise SystemExit(f"Sonnet thiếu nhãn {len(set(son) & set(ev))}/{len(ev)}")
    rv = ai("You are the REVIEWER. A cheap filter labelled every channel below faceless_explainer=true from ONE video title. "
            "A second model re-labelled them with more evidence (sonnet field). Decide the final labels yourself from the evidence; "
            + crit + " Return ONLY JSON {\"<id>\": {\"faceless_explainer\": true|false, \"in_niche_B\": true|false, "
            "\"agree_sonnet\": true|false, \"why\": \"<= 15 words\"}}.\n\n"
            + "\n".join(json.dumps(dict(json.loads(l), sonnet=son.get(json.loads(l)["id"])), ensure_ascii=False) for l in lines),
            "audit-opus", model="claude-opus-5-5")
    if len(set(rv) & set(ev)) < len(ev):
        raise SystemExit(f"Opus thiếu nhãn {len(set(rv) & set(ev))}/{len(ev)}")
    out = dict(n_cands=len(cands), n_old_cov=len(set(old) & set(cands)), n_passed=len(passed), sample=sample, ev=ev, sonnet=son, opus=rv)
    f.write_text(json.dumps(out, ensure_ascii=False))
    return out

def summarize(dem, lab):
    T = dem["topics"]
    strong = [s for s in T if T[s]["label"] == "Mạnh"]
    print("== CẦU HIỆN HÀNH (tự tính)")
    for s, t in T.items():
        print(s, t["label"], "big", t["n_big"], "/raw", t["n_big_raw"], "ch", t["n_big_ch"], "long", t["n_long"],
              "young_big", t["young_share_big"], "score", t["score"], "| top_on", t["top_on"], "| top_any", t["top_any"])
    print("Mạnh:", len(strong), strong)
    if lab:
        ev, so, op = lab["ev"], lab["sonnet"], lab["opus"]
        n = len(ev)
        wrong_f = [c for c in ev if not op[c]["faceless_explainer"]]
        wrong_n = [c for c in ev if not op[c]["in_niche_B"]]
        agree = sum(so[c]["faceless_explainer"] == op[c]["faceless_explainer"] and so[c]["in_niche_B"] == op[c]["in_niche_B"] for c in ev)
        yg = [c for c in ev if ev[c]["young"]]
        yg_ok = [c for c in yg if op[c]["faceless_explainer"]]
        yg_ok2 = [c for c in yg_ok if op[c]["in_niche_B"]]
        print("== KIỂM NHÃN", dict(cands=lab["n_cands"], passed=lab["n_passed"], sample=n, wrong_faceless=len(wrong_f),
              wrong_niche=len(wrong_n), sonnet_opus_agree=agree,
              young=len(yg), young_expl=sum(ev[c]["exploded"] for c in yg),
              young_ok=len(yg_ok), young_ok_expl=sum(ev[c]["exploded"] for c in yg_ok),
              young_ok_niche=len(yg_ok2), young_ok_niche_expl=sum(ev[c]["exploded"] for c in yg_ok2)))
        for c in ev:
            print(" ", ev[c]["name"][:30], "| young", ev[c]["young"], "expl", ev[c]["exploded"], "| S", so[c]["faceless_explainer"], so[c]["in_niche_B"],
                  "| O", op[c]["faceless_explainer"], op[c]["in_niche_B"], op[c].get("why", ""))

if __name__ == "__main__":
    purge()
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    dem = demand()
    lab = labels(dem) if what in ("labels", "all") else None
    summarize(dem, lab)
    print("calls", collect.calls, f"AI ${collect.spent():.2f}")

# ---------- Độ nhạy: chuẩn liên quan RỘNG (chỉ để báo cáo; nhãn chính vẫn theo chuẩn "đối thủ trực tiếp") ----------
def sensitivity(dem):
    f = DATA / "current_sens.json"
    if f.exists(): return json.loads(f.read_text())
    out = {}
    for slug, t in dem["topics"].items():
        vids = [v for v in dem["videos"][slug] if v["views"] >= BIG]
        if not vids:
            out[slug] = 0; continue
        lines = [f'{v["id"]} | {v["title"]} | {v["desc"][:400]!r}' for v in vids]
        p = (f"Planned explainer episode: \"{TITLE[slug]}\". For each YouTube video decide same_subject=true if it is about the "
             "same industry/subject and would draw the same audience, even from a different angle (e.g. how the business works, "
             "its history, life inside it). Mark false for entertainment, unrelated news, personal-finance product tips, "
             "or a different industry. Return ONLY JSON {\"<videoId>\": {\"same_subject\": true|false}}.\n\n" + "\n".join(lines))
        r = ai(p, f"sens-{slug}", model="claude-sonnet-5-5")
        if any(v["id"] not in r for v in vids): raise SystemExit(f"độ nhạy thiếu nhãn {slug}")
        out[slug] = sum(bool(r[v["id"]].get("same_subject")) for v in vids)
    f.write_text(json.dumps(out))
    return out

if __name__ == "__main__" and "sens" in sys.argv:
    s = sensitivity(dem)
    lab = lambda n: "Mạnh" if n >= 2 else ("Yếu" if n == 1 else "Không")
    print({k: (v, lab(v)) for k, v in s.items()}, "Mạnh:", sum(v >= 2 for v in s.values()), f"AI ${collect.spent():.2f}")
