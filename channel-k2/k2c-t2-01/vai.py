#!/opt/cine/bin/python
"""K2C-T2-01 · sổ token/$ theo VAI (lệnh T2 15/10: ghi riêng từng vai để quyết giữ/bỏ; bỏ nếu +25 % chi phí không đo được lợi).
  vai.py mark <vai> start|end      ghi mốc thời gian (UTC) vào so-vai.jsonl
  vai.py sum                        cộng token phiên (trường `usage` trong log phiên, khử trùng theo mã tin nhắn — BAI-HOC LL #56)
                                    theo cửa sổ mốc của từng vai + $ `claude -p` theo tag trong kiem-mu/cost.jsonl (tiền tố vai)
Vai: P (điều phối), dong-goi, bien-kich, dao-dien, dung. Phần ngoài mọi cửa sổ vai tính cho P."""
import glob, json, os, sys, datetime as dt
from pathlib import Path
HERE = Path(__file__).resolve().parent
LOG = HERE / "so-vai.jsonl"; COST = HERE / "kiem-mu" / "cost.jsonl"
# giá niêm yết $/triệu token (đầu vào, đầu ra, ghi cache, đọc cache) — chỉ để quy đổi phần token trong phiên; ghi rõ là ước theo bảng giá
PRICE = {"opus": (5.0, 25.0, 6.25, 0.5), "sonnet": (3.0, 15.0, 3.75, 0.3), "haiku": (1.0, 5.0, 1.25, 0.1)}

def now(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

def windows():
    W, open_ = [], {}
    for l in LOG.read_text().splitlines() if LOG.exists() else []:
        m = json.loads(l)
        if m["ev"] == "start": open_[m["vai"]] = m["ts"]
        elif m["vai"] in open_: W.append((m["vai"], open_.pop(m["vai"]), m["ts"]))
    W += [(v, t, now()) for v, t in open_.items()]
    return W

def role_of(ts, W):
    for v, a, b in W:
        if a <= ts <= b: return v
    return "P"

def summ():
    W = windows(); seen = set(); agg = {}
    amap = json.loads((HERE / "vai-agent.json").read_text()) if (HERE / "vai-agent.json").exists() else {}   # tác tử con → vai (chạy song song nên không theo cửa sổ giờ)
    for f in glob.glob(os.path.expanduser("~/.claude/projects/-home-user-cine-lab/**/*.jsonl"), recursive=True):   # phiên + tác tử con; `claude -p` tính riêng qua cost.jsonl
        fixed = next((v for k, v in amap.items() if k in os.path.basename(f)), None)
        for l in open(f):
            try: e = json.loads(l)
            except Exception: continue
            m = e.get("message") or {}
            u = m.get("usage"); mid = m.get("id")
            if not u or not mid or mid in seen: continue
            seen.add(mid); ts = dt.datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")).isoformat(timespec="seconds")
            k = fixed or role_of(ts, W); fam = next((x for x in PRICE if x in (m.get("model") or "")), "opus"); p = PRICE[fam]
            a = agg.setdefault(k, dict(out=0, inp=0, cw=0, cr=0, usd=0.0, api_usd=0.0))
            i, o, cw, cr = u.get("input_tokens", 0), u.get("output_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0)
            a["inp"] += i; a["out"] += o; a["cw"] += cw; a["cr"] += cr
            a["usd"] += (i * p[0] + o * p[1] + cw * p[2] + cr * p[3]) / 1e6
    for l in COST.read_text().splitlines() if COST.exists() else []:
        c = json.loads(l); v = c["tag"].split(":")[0] if ":" in c["tag"] else "P"
        agg.setdefault(v, dict(out=0, inp=0, cw=0, cr=0, usd=0.0, api_usd=0.0))["api_usd"] += c["usd"]
    print(json.dumps(agg, indent=1)); return agg

if __name__ == "__main__":
    if sys.argv[1] == "mark":
        with open(LOG, "a") as f: f.write(json.dumps({"vai": sys.argv[2], "ev": sys.argv[3], "ts": now()}) + "\n")
    else: summ()
