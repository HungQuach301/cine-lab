"""Ghi báo cáo JSON + Markdown."""
import json
from pathlib import Path

ICON = {"PASS": "ĐẠT", "FAIL": "TRƯỢT", "MISSING": "THIẾU", "N/A": "—", "ERROR": "LỖI ĐO", "REVIEW": "CẦN NGƯỜI XEM"}


def _fmt(v):
    if isinstance(v, float):
        return f"{v:.4g}"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    return str(v)


def write_reports(rep, out_dir, stem):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    jp = out / f"{stem}.checks.json"
    jp.write_text(json.dumps(rep, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    L = [f"# Báo cáo kiểm L1 — {Path(rep['file']).name}", "",
         f"- Kết luận: **{rep['verdict']}**",
         f"- Profile: `{rep['profile']}` · Công cụ: {rep['tool']} · Thời điểm (UTC): {rep['created_utc']}",
         f"- LOCK: {'khớp' if rep['lock']['match'] else '**KHÔNG KHỚP**'} (`{rep['lock']['actual']}`)",
         f"- Đếm: " + ", ".join(f"{ICON[k]} {v}" for k, v in rep["counts"].items() if v), "",
         "| Mã | Luật | Cấp | Kết quả | Số đo chính |", "|---|---|---|---|---|"]
    for r in rep["results"]:
        ms = "; ".join(f"{m['name']} = {_fmt(m['value'])} {m['unit']} (ngưỡng {m['op']} {_fmt(m['threshold'])})"
                       + (" ⚠ sát ngưỡng" if m.get("near") else "") + ("" if m["ok"] else " ✗")
                       for m in r["metrics"]) or "; ".join(r["notes"])
        L.append(f"| {r['code']} | {r['title']} | {r['level']} | **{ICON[r['status']]}** | {ms} |")
    L += ["", "## Chỉ số nằm trong ±5% quanh ngưỡng"]
    L += [f"- {n['code']} — {n['metric']}: {_fmt(n['value'])} (ngưỡng {_fmt(n['threshold'])})"
          for n in rep["near_threshold"]] or ["- Không có."]
    L += ["", "## Chi tiết từng luật"]
    for r in rep["results"]:
        L += ["", f"### {r['code']} — {r['title']} ({r['section']}, cấp {r['level']}): {ICON[r['status']]}",
              f"- Định nghĩa đo: {r['measure']}", f"- Ngưỡng: {r['threshold_text']}"]
        L += [f"- Ghi chú: {n}" for n in r["notes"]]
        ev = {k: v for k, v in r.get("evidence", {}).items() if k != "traceback" and v not in ([], {}, None, "")}
        if ev:
            L.append("- Bằng chứng: `" + json.dumps(ev, ensure_ascii=False, default=str)[:1500] + "`")
    mp = out / f"{stem}.checks.md"
    mp.write_text("\n".join(L) + "\n", encoding="utf-8")
    return jp, mp
