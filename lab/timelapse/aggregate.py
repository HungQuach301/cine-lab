"""Gộp số liệu teardown (ngoài git) thành research/timelapse/teardown.json — chỉ số liệu và nhãn, không văn bản bình luận gốc."""
import json, os, re, statistics as st, collections, datetime as dt
from pathlib import Path

DATA = Path(os.environ.get("TL_DATA", Path.home() / ".cache/cine-timelapse"))
OUT = Path(__file__).resolve().parents[2] / "research/timelapse/teardown.json"
NOW = dt.datetime(2026, 10, 15, 18, tzinfo=dt.timezone.utc)
CITY_RX = r"(PARIS|ROME|LONDON|ISTANBUL|DUBAI|ATHENS|MOSCOW|LISBON|BARCELONA|AMSTERDAM|PRAGUE|BERLIN|VIENNA|WARSAW|NEW YORK|MANHATTAN|MEXICO|TENOCHTITLAN|LAS VEGAS|CHICAGO|RIO DE JANEIRO|SÃO PAULO|SAO PAULO|JERUSALEM|STOCKHOLM|VENICE|SAINT PETERSBURG|GOTHENBURG|TOKYO|KYIV|GLASGOW|SYDNEY|MANILA|SHANGHAI|HONG KONG|CAIRO|BANGKOK|LOS ANGELES|SAN FRANCISCO|NEW ORLEANS|KYOTO|JERSEY CITY|WASHINGTON|BOSTON|PHILADELPHIA|DELHI|CONSTANTINOPLE|SHENZHEN|CORK|EDINBURGH|LOUVRE|ARC DE TRIOMPHE|HANOI|DHAKA|JAKARTA|BEIJING|MADRID|BUDAPEST)"
NORM = {"MANHATTAN": "NEW YORK", "TENOCHTITLAN": "MEXICO CITY", "MEXICO": "MEXICO CITY", "SAO PAULO": "SÃO PAULO",
        "CONSTANTINOPLE": "ISTANBUL", "LOUVRE": "PARIS", "ARC DE TRIOMPHE": "PARIS"}
FORMAT_3D = re.compile(r"3D|TIMELAPSE|TIME-LAPSE|EVOLUTION|GROW|BUILT", re.I)

def age_d(pub):
    return max(1.0, (NOW - dt.datetime.fromisoformat(pub.replace("Z", "+00:00"))).total_seconds() / 86400)

def vrow(v):
    return dict(id=v["id"], channel=v["chname"], pub=v["pub"][:10], dur_s=v["dur"], views=v["views"],
                views_per_day=round(v["views"] / age_d(v["pub"]), 1), likes=v["likes"], comments=v["comments"], title=v["title"])

def cadence(vs):
    longs = sorted(dt.date.fromisoformat(v["pub"][:10]) for v in vs if v["dur"] >= 120)
    if len(longs) < 2: return None
    span = (longs[-1] - longs[0]).days or 1
    return round(7 * (len(longs) - 1) / span, 2)

def city_of(title):
    m = re.search(CITY_RX, title.upper())
    if not m: return None
    c = m.group(1); return NORM.get(c, c)

def main():
    lat = json.loads((DATA / "latos.json").read_text())
    comp = json.loads((DATA / "comp.json").read_text())
    srch = json.loads((DATA / "search.json").read_text())
    com = json.loads((DATA / "comments.json").read_text())
    q = [json.loads(l) for l in (DATA / "quota.jsonl").read_text().splitlines()]
    out = {"collected": "2026-10-15", "quota_units": sum(x["u"] for x in q),
           "quota_calls": collections.Counter(x["ep"] for x in q),
           "queries": ["3D timelapse city grow", "city growth timelapse", "watch city grow from to 2026 3D timelapse"]}
    ch = lat["channel"]; lv = lat["videos"]
    out["latos"] = dict(channel=dict(handle=ch["handle"], created=ch["created"][:10], subs=ch["subs"], videos=ch["vids"], total_views=ch["views"],
                                     country=ch["country"], first_timelapse=min(v["pub"] for v in lv)[:10],
                                     uploads_per_week=cadence(lv)),
                        videos=sorted((vrow(v) for v in lv), key=lambda r: r["pub"]),
                        median_dur_s=st.median(v["dur"] for v in lv),
                        median_views_per_day=round(st.median(vrow(v)["views_per_day"] for v in lv), 1))
    chans = []
    for cid, c in comp["channels"].items():
        vs = comp["videos"][cid]
        tl = [v for v in vs if FORMAT_3D.search(v["title"]) and city_of(v["title"])]
        chans.append(dict(name=c["name"], handle=c["handle"], created=c["created"][:10], country=c["country"], subs=c["subs"],
                          videos=c["vids"], timelapse_videos=len(tl),
                          first_timelapse=min((v["pub"] for v in tl), default="")[:10],
                          uploads_per_week=cadence(tl),
                          best=vrow(max(tl, key=lambda v: v["views"])) if tl else None,
                          median_dur_s=st.median(v["dur"] for v in tl) if tl else None,
                          median_views_per_day=round(st.median(vrow(v)["views_per_day"] for v in tl), 1) if tl else None,
                          timelapse=[vrow(v) for v in sorted(tl, key=lambda v: v["pub"])]))
    out["competitors"] = sorted(chans, key=lambda c: -(c["best"] or {}).get("views", 0))
    # bảng thành phố đã làm (mọi kênh thấy được: Latos + 10 kênh + kết quả tìm kiếm có dạng 3D/timelapse)
    allv = {v["id"]: v for v in lv}
    for vs in comp["videos"].values():
        for v in vs: allv[v["id"]] = v
    for v in srch: allv.setdefault(v["id"], v)
    done = collections.defaultdict(list)
    for v in allv.values():
        c = city_of(v["title"])
        if c and FORMAT_3D.search(v["title"]) and v["dur"] >= 45:
            done[c].append(dict(channel=v["chname"], views=v["views"], pub=v["pub"][:10], dur_s=v["dur"]))
    out["cities_done"] = {c: dict(n_videos=len(x), n_channels=len({y["channel"] for y in x}), max_views=max(y["views"] for y in x),
                                  sum_views=sum(y["views"] for y in x), by=sorted(x, key=lambda y: -y["views"]))
                          for c, x in sorted(done.items(), key=lambda kv: -sum(y["views"] for y in kv[1]))}
    # bình luận
    names = {"Vs0LO6HMxIw": "Latos PRAGUE", "UqbSM0g5ytM": "Latos ATHENS", "bFHteO3MFpQ": "Latos LISBON",
             "50dWQdlHmYI": "CityEons ROME (bắt chước)", "IFhKB5zHWFg": "CITY 3D TIMELAPSE PARIS (kênh gốc)"}
    cm = {}; req = collections.Counter(); tot = collections.Counter(); totw = collections.Counter(); W = 0; N = 0
    for vid, cs in com.items():
        cl = json.loads((DATA / f"cls_{vid}.json").read_text())
        cat = collections.Counter(); catw = collections.Counter(); errs = []; w = 0
        for i, c in enumerate(cs):
            r = cl.get(str(i), {}); wt = 1 + c["likes"]; w += wt
            for k in set(r.get("c", [])): cat[k] += 1; catw[k] += wt
            for city in r.get("cities", []): req[city] += 1
            if r.get("err"): errs.append(dict(likes=c["likes"], claim_summary=r["err"]))
        acc = cat["accuracy_error"] + cat["missing_landmark_or_event"] + cat["accuracy_question"]
        accw = catw["accuracy_error"] + catw["missing_landmark_or_event"] + catw["accuracy_question"]
        cm[vid] = dict(video=names[vid], n=len(cs), categories=dict(cat.most_common()),
                       accuracy_share=round(acc / len(cs), 3), accuracy_share_like_weighted=round(accw / w, 3),
                       top_accuracy_claims=sorted(errs, key=lambda e: -e["likes"])[:8])
        tot.update(cat); totw.update(catw); W += w; N += len(cs)
    out["comments"] = dict(method="commentThreads order=relevance, 100/video; nhãn: claude-haiku-5-5 (research/timelapse/cost.jsonl); số like +1 làm trọng số",
                           per_video=cm, total=dict(tot.most_common()), n=N,
                           accuracy_share=round((tot["accuracy_error"] + tot["missing_landmark_or_event"] + tot["accuracy_question"]) / N, 3),
                           accuracy_share_like_weighted=round((totw["accuracy_error"] + totw["missing_landmark_or_event"] + totw["accuracy_question"]) / W, 3),
                           wants_info_or_readability=tot["wants_info"] + tot["readability"])
    donekeys = {k.upper() for k in out["cities_done"]}
    out["cities_requested"] = [dict(city=c, mentions=n, already_done=c.upper().replace("SAO", "SÃO") in donekeys or c.upper() in donekeys)
                               for c, n in req.most_common()]
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("ok", OUT, out["quota_units"])

if __name__ == "__main__":
    main()
