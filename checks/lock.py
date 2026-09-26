"""Chỉ phiên K chạy: tính SHA-256 toàn thư mục checks/ (trừ LOCK) và ghi checks/LOCK.
Dùng: /opt/cine/bin/python checks/lock.py [--verify]"""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cinecheck import VERSION  # noqa: E402
from cinecheck.lockhash import manifest, read_lock, tree_hash  # noqa: E402

ROOT = Path(__file__).resolve().parent

if "--verify" in sys.argv:
    got, want = tree_hash(ROOT), read_lock(ROOT)
    print(f"LOCK: {want}\nTính lại: {got}\n{'KHỚP' if got == want else 'KHÔNG KHỚP'}")
    sys.exit(0 if got == want else 1)

lines = manifest(ROOT)
h = tree_hash(ROOT)
text = (
    "# CINE LAB — khoá luật kiểm (chỉ phiên K sửa)\n"
    f"VERSION: {VERSION}\n"
    f"DATE_UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
    "ALGO: sha256 của chuỗi các dòng '<sha256 file>  <đường dẫn tương đối>\\n', sắp theo đường dẫn,\n"
    "      mọi file trong checks/ trừ LOCK, __pycache__/ và *.pyc\n"
    f"TREE_SHA256: {h}\n"
    "\n# FILES\n" + "".join(l + "\n" for l in lines)
)
(ROOT / "LOCK").write_text(text, encoding="utf-8")
print(h)
