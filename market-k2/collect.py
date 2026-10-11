"""Kênh 2 — thu thập dữ liệu thị trường bằng YouTube Data API v3 (proxy gắn khoá; không có khoá trong mã).
Số liệu thô lưu NGOÀI git ở $K2_DATA (mặc định ~/.cache/cine-market-k2) và tự xoá file > 30 ngày.
Ngân sách: 48 search.list (8/ngách × 6), 25 kết quả/lượt; ≤ 15 kênh/ngách; ≤ 50 video dài gần nhất/kênh."""
import json, os, re, subprocess, sys, time, datetime as dt, statistics as st
from pathlib import Path
import requests

API = "https://www.googleapis.com/youtube/v3/"
DATA = Path(os.environ.get("K2_DATA", Path.home() / ".cache/cine-market-k2"))
DATA.mkdir(parents=True, exist_ok=True)
NOW = dt.datetime(2026, 10, 11, tzinfo=dt.timezone.utc)
LONG_S = 480          # "video dài" = ≥ 8 phút (đủ chèn quảng cáo giữa video)
MAX_CH, MAX_VID = 15, 50
LOG = DATA / "cost.jsonl"

def purge():
    """Tự xoá số liệu thô > 30 ngày (chỉ file do mã này tạo)."""
    for pat in ("niche_*.json", "haiku_*.json", "metrics.json", "calls.json", "cost.jsonl", "diff.txt"):
        for f in DATA.glob(pat):
            if time.time() - f.stat().st_mtime > 30 * 86400:
                f.unlink()

NICHES = {
 "A": ("lịch sử tiền/ngân hàng/hệ thống kinh tế", [
   "how does the federal reserve create money", "why did the gold standard end",
   "how do banks make money from deposits", "how did the 2008 financial crisis happen",
   "what causes hyperinflation history", "how does the global financial system work",
   "why is the us dollar the world reserve currency", "history of banking explained"]),
 "B": ("lịch sử doanh nghiệp/ngành", [
   "how did walmart get so big", "what happened to sears", "why did kodak fail",
   "how did coca cola take over the world", "rise and fall of a company documentary",
   "how did nvidia become so valuable", "why did blockbuster go bankrupt",
   "how the airline industry works history"]),
 "D": ("bí ẩn trên bản đồ", [
   "why is this border so weird", "why does nobody live here map",
   "strange places on google maps explained", "why are cities located where they are",
   "mysterious island explained", "why is this country shaped like this",
   "why was this town abandoned", "strange geography explained"]),
 "E": ("công cụ & AI thay đổi cách làm việc", [
   "how ai is changing jobs", "will ai replace programmers",
   "how technology changed the office history", "which jobs will automation replace",
   "how companies use ai agents at work", "history of the personal computer at work",
   "how automation changed factories", "is ai making workers more productive"]),
 "J": ("nhà ở & đô thị", [
   "why are houses so expensive in america", "why american cities are built for cars",
   "why can't america build housing", "how zoning laws shape cities",
   "why suburbs are financially unsustainable", "why is rent so high",
   "how american cities grew history", "why public transit fails in the us"]),
 "L": ("năng lượng & hạ tầng", [
   "how does the power grid work", "why is the us power grid failing",
   "how nuclear power plants work", "why are electricity prices rising",
   "how oil shaped the modern world", "will ai data centers break the power grid",
   "how water infrastructure works", "history of the electric grid"]),
}

calls = {"search.list": 0, "other": 0}
def get(ep, **p):
    for i in range(4):
        try:
            r = requests.get(API + ep, params=p, timeout=60)
        except requests.RequestException as e:   # chỉ in tên lỗi, không in URL
            print(f"{ep}: {type(e).__name__}", file=sys.stderr); time.sleep(2 ** (i + 1)); continue
        if r.status_code == 200:
            calls["search.list" if ep == "search" else "other"] += 1
            return r.json()
        time.sleep(2 ** (i + 1))
    raise SystemExit(f"{ep}: thất bại sau 4 lần")   # không in URL/khoá

def dur(s):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    d, h, mi, se = (int(x or 0) for x in m.groups()) if m else (0,) * 4
    return d * 86400 + h * 3600 + mi * 60 + se

def videos(ids):
    out = []
    for i in range(0, len(ids), 50):
        j = get("videos", part="snippet,contentDetails,statistics", id=",".join(ids[i:i+50]), maxResults=50)
        for v in j.get("items", []):
            s, c = v["snippet"], v.get("statistics", {})
            out.append(dict(id=v["id"], ch=s["channelId"], chname=s["channelTitle"], title=s["title"],
                            desc=s.get("description", "")[:1500], pub=s["publishedAt"],
                            dur=dur(v["contentDetails"].get("duration")), views=int(c.get("viewCount", 0)),
                            likes=int(c.get("likeCount", 0)), comments=int(c.get("commentCount", 0))))
    return out

def haiku(prompt, tag):
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ["CONSOLE_API_KEY"])
    for _ in range(3):
        r = subprocess.run(["claude", "-p", "--model", "claude-haiku-5-5", "--output-format", "json", prompt],
                           capture_output=True, text=True, env=env, cwd=str(DATA), timeout=600)
        try:
            d = json.loads(r.stdout)
        except Exception:
            continue
        with open(LOG, "a") as f:
            f.write(json.dumps({"tag": tag, "usd": d.get("total_cost_usd", 0)}) + "\n")
        txt = d.get("result", "")
        m = re.search(r"\{.*\}", txt, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return {}

def classify_channels(niche, cands):
    """Haiku đọc tiêu đề + mô tả: kênh không lộ mặt, dạng giải thích/tài liệu?"""
    lines = []
    for cid, vs in cands.items():
        v = vs[0]
        lines.append(f'{cid} | channel: {v["chname"]} | title: {v["title"]} | desc: {v["desc"][:300]!r}')
    prompt = ("You classify YouTube channels from ONE sample video's title and description. "
              "faceless_explainer=true only if the content is an explainer or documentary-style video that is "
              "most likely narrated over graphics/maps/animation/archival footage WITHOUT an on-camera host "
              "(no vlog, podcast, interview, talk show, news broadcast, reaction, lecture recording, TV network clip). "
              "Return ONLY JSON: {\"<channelId>\": {\"faceless_explainer\": true|false}}.\n\n" + "\n".join(lines))
    return haiku(prompt, f"filter-{niche}")

def main():
    purge()
    after = (NOW - dt.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {}
    for key, (name, qs) in NICHES.items():
        f = DATA / f"niche_{key}.json"
        if f.exists():
            out[key] = json.loads(f.read_text()); continue
        hits = []
        for q in qs:
            j = get("search", part="id", q=q, type="video", maxResults=25, publishedAfter=after,
                    regionCode="US", relevanceLanguage="en", order="relevance")
            hits += [(q, it["id"]["videoId"]) for it in j.get("items", [])]
        ids = list(dict.fromkeys(v for _, v in hits))
        qof = {}
        for q, v in hits: qof.setdefault(v, q)
        sv = [v for v in videos(ids) if v["dur"] >= LONG_S]
        for v in sv: v["q"] = qof[v["id"]]
        cands = {}
        for v in sorted(sv, key=lambda x: -x["views"]):
            cands.setdefault(v["ch"], []).append(v)
        cls = classify_channels(key, cands)
        keep = [c for c in cands if cls.get(c, {}).get("faceless_explainer")]
        # ưu tiên kênh có nhiều kết quả, rồi tổng lượt xem trong mẫu tìm kiếm
        keep.sort(key=lambda c: (-len(cands[c]), -sum(v["views"] for v in cands[c])))
        keep = keep[:MAX_CH]
        chans = {}
        if keep:
            j = get("channels", part="snippet,statistics,contentDetails", id=",".join(keep), maxResults=50)
            for c in j.get("items", []):
                chans[c["id"]] = dict(name=c["snippet"]["title"], created=c["snippet"]["publishedAt"],
                    country=c["snippet"].get("country"), subs=int(c["statistics"].get("subscriberCount", 0) or 0),
                    hidden_subs=c["statistics"].get("hiddenSubscriberCount", False),
                    uploads=c["contentDetails"]["relatedPlaylists"]["uploads"])
        for cid, c in chans.items():
            longv, tok, pages = [], None, 0
            while len(longv) < MAX_VID and pages < 6:
                p = dict(part="contentDetails", playlistId=c["uploads"], maxResults=50)
                if tok: p["pageToken"] = tok
                try:
                    j = get("playlistItems", **p)
                except SystemExit:
                    break
                ids2 = [i["contentDetails"]["videoId"] for i in j.get("items", [])]
                longv += [v for v in videos(ids2) if v["dur"] >= LONG_S]
                tok, pages = j.get("nextPageToken"), pages + 1
                if not tok: break
            c["videos"] = sorted(longv, key=lambda v: v["pub"], reverse=True)[:MAX_VID]
        out[key] = dict(name=name, queries=qs, search_videos=sv, n_search_ids=len(ids),
                        n_candidates=len(cands), classified=cls, channels=chans)
        f.write_text(json.dumps(out[key]))
        print(key, "search ids", len(ids), "long", len(sv), "cands", len(cands), "kept", len(chans), calls, flush=True)
    (DATA / "calls.json").write_text(json.dumps(calls))

if __name__ == "__main__":
    main()
