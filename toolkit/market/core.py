"""Lõi dùng chung của toolkit/market (phiên M "Nhà máy dữ liệu", 11/10/2026; hợp nhất channel-k2 collect/current/final).

- Gói kênh (channel-pack) ở `packs/<tên>.json`: ngách, đề tài + câu hỏi mẫu, model ghim, trần chi AI, ngưỡng.
- Số liệu thô YouTube (kể cả kênh khác, bình luận nguyên văn) chỉ ở `$MARKET_DATA` (mặc định `~/.cache/cine-market`),
  NGOÀI git. Mã từ chối chạy nếu thư mục dữ liệu nằm trong một cây git (fail closed).
- Mỗi lệnh tự `purge()`: xoá tệp thô > 30 ngày (YouTube API Developer Policies III.E.4); giữ sổ chi AI và sổ quota.
- Gọi API qua proxy gắn khoá (không có khoá trong mã, không in URL). Mọi lỗi → MarketError → thoát mã 2, không ghi đầu ra.
- Mọi chỉ số tính ra là "tự tính, không phải chỉ số YouTube".
"""
import datetime as dt, hashlib, json, os, re, subprocess, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
API = "https://www.googleapis.com/youtube/v3/"
MAX_DAYS = 30
KEEP = {"ai-ledger.jsonl"}           # sổ chi giữ qua purge để trần không bị đặt lại
LABEL_SELF = "tự tính, không phải chỉ số YouTube"


class MarketError(Exception):
    """Lỗi dừng hẳn (fail closed): CLI in lý do, thoát mã 2, không ghi đầu ra dở."""


# ---------- gói kênh ----------
PACK_KEYS = ("name", "channel", "niche", "region", "language", "long_min_s", "models", "ai_cap_usd", "topics", "out")
MODEL_ROLES = ("classify", "judge", "reviewer")


def load_pack(name):
    f = HERE / "packs" / f"{name}.json"
    if not f.exists():
        raise MarketError(f"không có gói kênh '{name}' (toolkit/market/packs/)")
    p = json.loads(f.read_text())
    miss = [k for k in PACK_KEYS if k not in p]
    if miss:
        raise MarketError(f"gói {name} thiếu trường: {miss}")
    for r in MODEL_ROLES:
        m = p["models"].get(r, "")
        if not re.fullmatch(r"claude-[a-z]+-\d+-\d+", m):   # ghim đủ tên, không bí danh
            raise MarketError(f"gói {name}: model vai '{r}' phải ghim đủ tên (vd claude-sonnet-5-5), đang là {m!r}")
    for slug, t in p["topics"].items():
        if not t.get("title") or not (2 <= len(t.get("questions", [])) <= 6):
            raise MarketError(f"gói {name}: đề tài {slug} cần title và 2–6 câu hỏi khán giả")
    return p


# ---------- thư mục số liệu thô (ngoài git) ----------
def data_root():
    d = Path(os.environ.get("MARKET_DATA", Path.home() / ".cache/cine-market")).expanduser().resolve()
    d.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["git", "-C", str(d), "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip() == "true":
        raise MarketError(f"MARKET_DATA nằm trong cây git ({d}) — số liệu thô phải ở ngoài git")
    return d


def pack_dir(pack):
    d = data_root() / pack["name"]
    d.mkdir(parents=True, exist_ok=True)
    return d


def purge(now=None):
    """Xoá mọi tệp thô > 30 ngày (theo mtime) trong $MARKET_DATA, trừ sổ chi AI. Trả danh sách đã xoá."""
    now = now or time.time()
    gone = []
    for f in data_root().rglob("*"):
        if f.is_file() and f.name not in KEEP and now - f.stat().st_mtime > MAX_DAYS * 86400:
            f.unlink()
            gone.append(f)
    return gone


# ---------- YouTube Data API ----------
def http_get(url, params):
    """Một lệnh GET (tests thay hàm này bằng fixture). Trả (mã HTTP, văn bản)."""
    import requests
    try:
        r = requests.get(url, params=params, timeout=60)
    except requests.RequestException as e:          # chỉ in tên lỗi, không in URL
        return 0, type(e).__name__
    return r.status_code, r.text


def cache_key(ep, p):
    return f"api_{ep}_{hashlib.sha1(json.dumps(p, sort_keys=True).encode()).hexdigest()[:12]}.json"


def get(pack, quota, ep, ttl_s=MAX_DAYS * 86400, **p):
    """Đọc cache nếu còn hạn; nếu không thì xin quota TRƯỚC khi gọi, gọi, ghi cache. Lỗi → MarketError."""
    f = pack_dir(pack) / "api" / cache_key(ep, p)
    if f.exists() and time.time() - f.stat().st_mtime <= ttl_s:
        return json.loads(f.read_text())
    for i in range(3):
        quota.charge(ep)                             # xin quota TRƯỚC mỗi lượt gọi (lượt lỗi cũng tốn đơn vị)
        code, text = http_get(API + ep, p)
        if code == 200:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text)
            return json.loads(text)
        if code in (500, 502, 503, 0) and i < 2:
            time.sleep(2 ** i)
            continue
        break
    if code == 403 and ep == "commentThreads" and "commentsDisabled" in text:   # chỉ khi video tắt bình luận
        return {"items": [], "disabled": True}
    raise MarketError(f"{ep}: HTTP {code} — dừng (quota/khoá/mạng); cache giữ phần đã thu")


def dur(s):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    d, h, mi, se = (int(x or 0) for x in m.groups()) if m else (0,) * 4
    return d * 86400 + h * 3600 + mi * 60 + se


def pubdt(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def videos(pack, quota, ids, ttl_s=MAX_DAYS * 86400):
    out = {}
    ids = list(dict.fromkeys(ids))
    for i in range(0, len(ids), 50):
        j = get(pack, quota, "videos", ttl_s=ttl_s, part="snippet,contentDetails,statistics",
                id=",".join(ids[i:i + 50]), maxResults=50)
        for v in j.get("items", []):
            s, c = v["snippet"], v.get("statistics", {})
            out[v["id"]] = dict(id=v["id"], ch=s["channelId"], chname=s["channelTitle"], title=s["title"],
                                desc=s.get("description", "")[:1200], pub=s["publishedAt"],
                                dur=dur(v["contentDetails"].get("duration")), views=int(c.get("viewCount", 0)),
                                likes=int(c.get("likeCount", 0)), comments=int(c.get("commentCount", 0)))
    return [out[i] for i in ids if i in out]


def channels(pack, quota, cids):
    out = {}
    cids = list(dict.fromkeys(cids))
    for i in range(0, len(cids), 50):
        j = get(pack, quota, "channels", part="snippet,statistics,contentDetails", id=",".join(cids[i:i + 50]), maxResults=50)
        for c in j.get("items", []):
            out[c["id"]] = dict(name=c["snippet"]["title"], created=c["snippet"]["publishedAt"],
                                desc=c["snippet"].get("description", "")[:600],
                                subs=int(c["statistics"].get("subscriberCount", 0) or 0),
                                uploads=c["contentDetails"]["relatedPlaylists"]["uploads"])
    return out


def write_atomic(path, text):
    """Ghi đầu ra một lần ở cuối (không để tệp dở khi dừng giữa chừng)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)
