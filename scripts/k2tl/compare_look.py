"""V5b-1b · bảng TRƯỚC → SAU cho khung tĩnh (dùng measure_look.measure: 640×360, vùng giữa x/y 15–85 %, khung không chữ).
Dùng: compare_look.py --pairs "nhãn:trước.jpg:sau.jpg" ... [--mask sau.mask.json] [--json ra.json]  → bảng Markdown + JSON
Mục tiêu (lệnh 16/10): bão hoà trung vị ≥ 0,35 · colorfulness ≥ 35 · chi tiết ≥ 16 (cận dưới đối thủ) · cháy sáng ≤ 1 %."""
import argparse, json
from measure_look import measure

T = dict(sat_med=0.35, colorful=35.0, detail=16.0)

def main():
    a = argparse.ArgumentParser(); a.add_argument("--pairs", nargs="+", required=True); a.add_argument("--json"); a.add_argument("--mask", nargs="*", default=[])
    o = a.parse_args(); mk = {}
    for m in o.mask:
        for r in json.load(open(m)): mk[r["f"]] = r
    rows = []
    for p in o.pairs:
        lab, b, s = p.split(":"); B, S = measure(b), measure(s); f = int(s.rsplit("/", 1)[-1].split(".")[0]) if s.rsplit("/", 1)[-1].split(".")[0].isdigit() else None
        rows.append(dict(label=lab, before=B, after=S, mask=mk.get(f)))
    print("| Khung | Bão hoà trước → sau | Colorfulness trước → sau | Chi tiết trước → sau | Cháy sáng sau | Nội dung hình học / + nền phố (sau) |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        B, S, m = r["before"], r["after"], r["mask"]
        ok = lambda k: "✓" if S[k] >= T[k] else "✗"
        print(f"| {r['label']} | {B['sat_med']:.3f} → **{S['sat_med']:.3f}** {ok('sat_med')} | {B['colorful']:.1f} → **{S['colorful']:.1f}** {ok('colorful')} | {B['detail']:.1f} → **{S['detail']:.1f}** {ok('detail')} | {S['clip_pct']:.2f} % | "
              + (f"{m['content_pct']} % / {m['fabric_pct']} %" if m else "—") + " |")
    import statistics as st
    for k in ("sat_med", "colorful", "detail"):
        print(f"<!-- trung vị {k}: {st.median(r['before'][k] for r in rows):.3f} → {st.median(r['after'][k] for r in rows):.3f} -->")
    if o.json: json.dump(dict(targets=T, rows=rows), open(o.json, "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
