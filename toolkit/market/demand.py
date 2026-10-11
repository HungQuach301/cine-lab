"""Hồ sơ cầu một đề tài (`market topic <slug>`): hợp nhất channel-k2 collect.labels/durable/demand + current.demand.

Định nghĩa (giữ đúng channel-k2, tự tính, không phải chỉ số YouTube):
- **Cầu hiện hành:** video ≥ `long_min_s` đăng trong 90 ngày (region của gói), qua câu hỏi khán giả của đề tài; trong số video
  ≥ `big_views` (50 nghìn) model `judge` chấm "đối thủ trực tiếp". ≥ 2 → Mạnh, 1 → Yếu, 0 → Không.
- **Cầu bền:** top video dài toàn thời gian theo độ liên quan; ≥ 1 video đúng đề tài ≥ `durable_views` (500 nghìn) → Có.
- **Khoảng trống:** top 5 video đúng đề tài; `judge` đọc tiêu đề + mô tả, đếm video có dấu hiệu số liệu thật có nguồn;
  ≤ 1/5 → Có.
- **Vượt trội:** lượt xem video ÷ trung vị lượt xem video dài gần nhất của chính kênh (≤ 50 lượt tải lên); nhãn ≥ 3× / ≥ 5×.
- **Dải thời lượng thắng:** tứ phân vị 25–75 % số phút của video đúng đề tài ≥ 50 nghìn (làm tròn phút).
- **Câu hỏi, hoàn cảnh, điểm yếu, yêu cầu, mẫu tiêu đề:** `classify` gắn loại bình luận, `judge` tổng hợp (diễn đạt lại,
  không tên người, không trích nguyên văn).
Số liệu thô ở `$MARKET_DATA/<gói>/`; hàm `summary()` chỉ trả nhãn/dải/định danh cho repo.
"""
import datetime as dt, json, statistics as st
from core import MarketError, get, videos, channels, pubdt, pack_dir
import ai

KINDS = ("question", "situation", "rebuttal", "request")


def _search(pack, quota, q, days=None, n=25):
    p = dict(part="id", q=q, type="video", maxResults=n, regionCode=pack["region"],
             relevanceLanguage=pack["language"], order="relevance")
    if days:
        p["publishedAfter"] = days
    return [it["id"]["videoId"] for it in get(pack, quota, "search", **p).get("items", [])]


def relevance(pack, slug, vids):
    if not vids:
        return {}
    t = pack["topics"][slug]["title"]
    lines = [f'{v["id"]} | {v["title"]} | {v["desc"][:400]!r}' for v in vids]
    p = (f"Planned explainer episode: \"{t}\". For each YouTube video (title + description) decide on_topic=true "
         "only if a viewer searching for that episode's subject would see it as a direct competitor (same subject and similar "
         "question), not merely the same broad field (news clips, vlogs, product reviews, unrelated how-tos are off-topic). "
         "Return ONLY JSON {\"<videoId>\": {\"on_topic\": true|false}}.\n\n" + "\n".join(lines))
    return ai.ask_cover(pack, "judge", p, f"rel-{slug}", [v["id"] for v in vids])


def gap(pack, slug, top):
    if not top:
        return {}
    lines = [f'{v["id"]} | {v["title"]} | {v["desc"][:500]!r}' for v in top]
    p = ("For each YouTube video (title + description), judge ONLY from the text whether it shows evidence of using "
         "real, named data sources (statistics agencies, archives, filings, academic papers, or a source list). "
         "Return ONLY JSON {\"<videoId>\": {\"real_data\": true|false}}.\n\n" + "\n".join(lines))
    return ai.ask_cover(pack, "judge", p, f"gap-{slug}", [v["id"] for v in top])


def outlier_ratio(pack, quota, cmeta, v):
    """Lượt xem ÷ trung vị video dài gần nhất của kênh (không tính chính nó). Không đủ 3 video → dùng ÷ người đăng ký."""
    c = cmeta.get(v["ch"])
    if not c:
        return None
    j = get(pack, quota, "playlistItems", part="contentDetails", playlistId=c["uploads"], maxResults=50)
    ids = [i["contentDetails"]["videoId"] for i in j.get("items", [])]
    other = [w["views"] for w in videos(pack, quota, ids) if w["dur"] >= pack["long_min_s"] and w["id"] != v["id"]]
    if len(other) >= 3 and st.median(other) > 0:
        return v["views"] / st.median(other)
    return v["views"] / c["subs"] if c["subs"] else None


def classify(pack, slug, items):
    out = {}
    for i in range(0, len(items), 60):
        b = items[i:i + 60]
        p = ("You label YouTube comments left under explainer videos. For each comment choose ONE kind:\n"
             "question = asks something about the subject; situation = describes the commenter's own job, workplace, family or "
             "experience related to the topic; rebuttal = disputes, corrects or adds a missing fact to the video; request = asks "
             "the creator for a future video/topic or more detail; drop = spam, generic praise, jokes, insults, off-topic.\n"
             "Also write gist: a neutral paraphrase in <= 18 words, no names, no usernames, no quotes.\n"
             "Return ONLY JSON {\"<id>\": {\"k\": \"question|situation|rebuttal|request|drop\", \"gist\": \"...\"}}.\n\n"
             + "\n".join(f'{c["cid"]} | {c["text"][:450]!r}' for c in b))
        out.update(ai.ask_cover(pack, "classify", p, f"cls-{slug}-{i}", [c["cid"] for c in b], min_cov=0.95))
    return out


def synth(pack, slug, buckets, comp):
    t = pack["topics"][slug]["title"]
    p = (f"Planned episode: \"{t}\" for the channel: {pack['niche']}. Below: labelled viewer comments from the top competing "
         "videos as weighted gists (weight = 1 + likes + replies), and the competing videos' titles. Write in Vietnamese (keep "
         "English titles/terms and the questions in English). Do NOT state any numeric fact as true. Do not name commenters or "
         "channels. Return ONLY JSON with keys: top_questions (5 items: {q_en, weight: \"cao|vừa|thấp\"}), situations (3 items: "
         "{vi}), competitor_weaknesses (3-5 items: {vi, evidence: \"bình luận|máy đọc tiêu đề/mô tả\"}), requests (<=4 items: {vi}), "
         "title_patterns (3 abstract fill-in templates in English that capture the winning titles' structure without copying any "
         "title, e.g. \"In YEAR, X Was Expected To Y. Then What?\"), keywords (6-8 English search phrases).\n\n"
         "COMPETITOR TITLES:\n" + json.dumps([c["title"] for c in comp], ensure_ascii=False) +
         "\n\nCOMMENTS BY KIND:\n" + json.dumps(buckets, ensure_ascii=False))
    r = ai.ask(pack, "judge", p, f"synth-{slug}")
    need = ("top_questions", "situations", "competitor_weaknesses", "title_patterns")
    if not isinstance(r, dict) or any(k not in r for k in need) or len(r["top_questions"]) < 5:
        raise MarketError(f"tổng hợp {slug} thiếu mục {need} hoặc < 5 câu hỏi — dừng")
    return r


def build(pack, quota, slug, now=None):
    """Thu + tính. Trả bản thô (lưu ngoài git). Gọi summary() để lấy phần được ghi vào repo."""
    now = now or dt.datetime.now(dt.timezone.utc)
    T = pack["topics"][slug]
    th = pack.get("thresholds", {})
    BIG, DUR, LONG = th.get("big_views", 50_000), th.get("durable_views", 500_000), pack["long_min_s"]
    after = (now - dt.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    qs, dq = T["questions"], T.get("durable_questions", T["questions"][:3])
    cur_ids, dur_ids = [], []
    for q in qs:
        cur_ids += _search(pack, quota, q, days=after, n=25)
    for q in dq:
        dur_ids += _search(pack, quota, q, n=15)
    allv = {v["id"]: v for v in videos(pack, quota, list(dict.fromkeys(cur_ids + dur_ids)))}
    cur = [allv[i] for i in dict.fromkeys(cur_ids) if i in allv and allv[i]["dur"] >= LONG and pubdt(allv[i]["pub"]) >= pubdt(after)]
    dura = [allv[i] for i in dict.fromkeys(dur_ids) if i in allv and allv[i]["dur"] >= LONG]
    cand = {v["id"]: v for v in cur if v["views"] >= BIG}
    cand.update({v["id"]: v for v in dura[:15]})
    rel = relevance(pack, slug, sorted(cand.values(), key=lambda v: -v["views"]))
    on = lambda v: bool(rel.get(v["id"], {}).get("on_topic"))
    cur_on = sorted([v for v in cur if v["views"] >= BIG and on(v)], key=lambda v: -v["views"])
    dur_on = sorted([v for v in dura if on(v)], key=lambda v: -v["views"])
    comp = sorted({v["id"]: v for v in cur_on + dur_on}.values(), key=lambda v: -v["views"])
    top5 = comp[:5]
    g = gap(pack, slug, top5)
    cmeta = channels(pack, quota, [v["ch"] for v in comp[:10]])
    for v in comp[:10]:
        v["ratio"] = outlier_ratio(pack, quota, cmeta, v)
    comments = []
    for v in top5:
        j = get(pack, quota, "commentThreads", part="snippet", videoId=v["id"], maxResults=50, order="relevance", textFormat="plainText")
        for it in j.get("items", []):
            s = it["snippet"]; tl = s["topLevelComment"]["snippet"]
            comments.append(dict(cid=it["id"], vid=v["id"], text=tl.get("textDisplay", ""),
                                 w=1 + int(tl.get("likeCount", 0)) + int(s.get("totalReplyCount", 0))))
    lab = classify(pack, slug, comments) if comments else {}
    buckets = {k: sorted([dict(w=c["w"], gist=lab[c["cid"]].get("gist", "")) for c in comments
                          if lab.get(c["cid"], {}).get("k") == k], key=lambda x: -x["w"])[:60] for k in KINDS}
    sy = synth(pack, slug, buckets, comp[:15])
    import render
    ai_texts = [x.get(k, "") for sec in ("top_questions", "situations", "competitor_weaknesses", "requests") for x in sy.get(sec, [])
                for k in ("q_en", "vi")] + list(sy.get("title_patterns", [])) + [b["gist"] for k in KINDS for b in buckets[k]]
    bad = render.verbatim(ai_texts, [c["text"] for c in comments] + [v["title"] for v in allv.values()])
    if bad:
        raise MarketError(f"tổng hợp {slug} chép nguyên văn ≥ 8 từ của bình luận/tiêu đề: {bad[:2]} — dừng, chạy lại")
    guard = sorted({x for v in allv.values() for x in (v["views"], v["likes"], v["comments"]) if x >= 1000}
                   | {c["subs"] for c in cmeta.values() if c["subs"] >= 1000} | {c["w"] - 1 for c in comments if c["w"] > 1000})
    return dict(slug=slug, title=T["title"], made=now.isoformat(), questions=qs, durable_questions=dq,
                n_cur_long=len(cur), n_cur_big_raw=sum(v["views"] >= BIG for v in cur), cur_on=cur_on, dur_on=dur_on,
                comp=comp, gap=g, n_comments=len(comments), kinds={k: len(v) for k, v in buckets.items()}, synth=sy,
                thresholds=dict(big=BIG, durable=DUR), guard=guard)


def _band(views):
    return ("≥ 500 nghìn" if views >= 500_000 else "50–500 nghìn" if views >= 50_000
            else "10–50 nghìn" if views >= 10_000 else "< 10 nghìn")


def _ratio_label(r):
    return "≥ 5×" if r and r >= 5 else "≥ 3×" if r and r >= 3 else "< 3×" if r else "không đo được"


def summary(raw):
    """Phần ĐƯỢC ghi vào repo: nhãn, dải, định danh kênh/video, câu diễn đạt lại. Không lượt xem/like/bình luận thô."""
    n_cur = len(raw["cur_on"])
    current = "Mạnh" if n_cur >= 2 else "Yếu" if n_cur == 1 else "Không"
    durable = "Có" if any(v["views"] >= raw["thresholds"]["durable"] for v in raw["dur_on"]) else "Không"
    top5 = raw["comp"][:5]
    n_real = sum(bool(raw["gap"].get(v["id"], {}).get("real_data")) for v in top5)
    gap_label = "Có" if top5 and n_real <= 1 else "Không" if top5 else "chưa đo"
    big = [v for v in raw["comp"] if v["views"] >= raw["thresholds"]["big"]]
    mins = sorted(round(v["dur"] / 60) for v in big)
    if len(mins) >= 4:
        q = st.quantiles(mins, n=4)
        band = f"{int(q[0])}–{int(round(q[2]))} phút"
    elif mins:
        band = f"{mins[0]}–{mins[-1]} phút (ít mẫu: {len(mins)})"
    else:
        band = "chưa đủ mẫu"
    outl = sorted([v for v in raw["comp"] if v.get("ratio") and v["ratio"] >= 3], key=lambda v: -v["ratio"])[:3]
    days = [pubdt(v["pub"]).astimezone(__import__("zoneinfo").ZoneInfo("America/New_York")) for v in big]
    when = {}
    for d in days:
        when[d.strftime("%a")] = when.get(d.strftime("%a"), 0) + 1
    s = raw["synth"]
    return dict(slug=raw["slug"], title=raw["title"], made=raw["made"][:10], current=current, n_cur_on=n_cur,
                n_cur_long=raw["n_cur_long"], durable=durable, gap=gap_label, gap_real=f"{n_real}/{len(top5)}",
                band=band, n_band=len(mins),
                outliers=[dict(ch=v["chname"], id=v["id"], min=round(v["dur"] / 60), ratio=_ratio_label(v["ratio"]),
                               views=_band(v["views"])) for v in outl],
                competitors=[dict(ch=v["chname"], id=v["id"], min=round(v["dur"] / 60), views=_band(v["views"]),
                                  ratio=_ratio_label(v.get("ratio")),
                                  real_data=bool(raw["gap"].get(v["id"], {}).get("real_data"))) for v in top5],
                questions=s["top_questions"][:5], situations=s["situations"][:3],
                weaknesses=s["competitor_weaknesses"][:5], requests=s.get("requests", [])[:4],
                title_patterns=s["title_patterns"][:3], keywords=s.get("keywords", [])[:8],
                weekdays_et=when, n_comments=raw["n_comments"], kinds=raw["kinds"],
                queries=raw["questions"], durable_queries=raw["durable_questions"])


def save_raw(pack, raw):
    f = pack_dir(pack) / f"topic_{raw['slug']}.json"
    f.write_text(json.dumps(raw, ensure_ascii=False))
    return f
