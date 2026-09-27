"""Kiểm toán ngẫu nhiên mặt nạ C3 (v1.3). Chỉ phiên P phát yêu cầu; phiên xưởng đọc yêu cầu và nộp render lại.
Dùng:
  /opt/cine/bin/python checks/audit.py issue <video> [--parts DIR] [--by P]   # phiên P: chọn khung, ghi request.json
  /opt/cine/bin/python checks/audit.py show  <video>                          # phiên xưởng: xem khung phải render lại
Xem checks/RUN.md mục 3.7."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cinecheck.audit import audit_dir, issue  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("cmd", choices=["issue", "show"])
ap.add_argument("video")
ap.add_argument("--parts")
ap.add_argument("--by", default="P")
a = ap.parse_args()
v = Path(a.video).resolve()
if a.cmd == "issue":
    parts = Path(a.parts) if a.parts else v.with_name(v.stem + ".parts")
    body = issue(v, parts, a.by)
    print(json.dumps(body, indent=1, ensure_ascii=False))
    print(f"Đã ghi {audit_dir(v) / 'request.json'}. Giao phiên xưởng render lại khung {body['frames']}.")
else:
    req = audit_dir(v) / "request.json"
    if not req.is_file():
        sys.exit(f"Chưa có yêu cầu kiểm toán: {req}")
    body = json.loads(req.read_text(encoding="utf-8"))
    d = audit_dir(v)
    print(f"Khung phải render lại: {body['frames']} (hạt giống {body['seed']}).")
    for f in body["frames"]:
        print(f"  mặt nạ → {d}/rerender/{f:05d}/<bộ phận>.png   (đủ các bộ phận như parts.json khung {f})")
    print(f"  log    → {d}/render.log  (dòng 'SCENE <file cảnh> SHA256 <hex>' và 'FRAME <khung> CMD <lệnh>')")
