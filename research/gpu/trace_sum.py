"""GPU-RD · tóm tắt Chrome trace (JSON từ browser.startTracing) theo tiến trình/luồng: tổng thời gian lát cắt cấp cao nhất (ms) và 30 sự kiện tốn nhất (thời gian gộp, kể cả lồng).
Dùng: /opt/cine/bin/python research/gpu/trace_sum.py <trace.json> [--out tóm-tắt.json]"""
import argparse, collections, json
from pathlib import Path

ap = argparse.ArgumentParser(); ap.add_argument("trace"); ap.add_argument("--out"); a = ap.parse_args()
d = json.loads(Path(a.trace).read_text()); ev = d["traceEvents"] if isinstance(d, dict) else d
pname, tname = {}, {}
for e in ev:
    if e.get("ph") == "M" and e.get("name") == "process_name": pname[e["pid"]] = e["args"]["name"]
    if e.get("ph") == "M" and e.get("name") == "thread_name": tname[(e["pid"], e["tid"])] = e["args"]["name"]
per_thread, per_name = collections.Counter(), collections.Counter()
stack = collections.defaultdict(list)   # chỉ cộng lát cắt không lồng (X có dur; B/E ghép cặp)
xs = collections.defaultdict(list)
for e in ev:
    if e.get("ph") == "X" and "dur" in e: xs[(e["pid"], e["tid"])].append((e["ts"], e["ts"] + e["dur"], e["name"]))
for k, L in xs.items():
    L.sort(); end = -1
    for s, t, n in L:
        per_name[(pname.get(k[0], k[0]), tname.get(k, k[1]), n)] += (t - s) / 1000   # bao gồm lát cắt lồng (thời gian gộp)
        if s >= end: per_thread[k] += (t - s) / 1000; end = t
ts = [e["ts"] for e in ev if "ts" in e and e.get("ph") != "M"]; span = (max(ts) - min(ts)) / 1000 if ts else 0
rows = sorted(((pname.get(k[0], str(k[0])), tname.get(k, str(k[1])), round(v, 1)) for k, v in per_thread.items()), key=lambda r: -r[2])
out = dict(span_ms=round(span, 1), threads=[dict(process=p, thread=t, busy_ms=v) for p, t, v in rows[:20]],
           top_events=[dict(process=p, thread=t, name=n, ms=round(v, 1)) for (p, t, n), v in per_name.most_common(30)])
print(json.dumps(out, ensure_ascii=False, indent=1))
if a.out: Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1))
