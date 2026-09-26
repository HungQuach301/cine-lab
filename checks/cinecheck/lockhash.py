"""SHA-256 của toàn thư mục checks/ (trừ LOCK và tệp sinh ra khi chạy Python)."""
import hashlib
from pathlib import Path

EXCLUDE_NAMES = {"LOCK"}
EXCLUDE_PARTS = {"__pycache__"}


def files(root):
    root = Path(root)
    out = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if not p.is_file() or rel.as_posix() in EXCLUDE_NAMES:
            continue
        if any(part in EXCLUDE_PARTS for part in rel.parts) or p.suffix == ".pyc":
            continue
        out.append(rel.as_posix())
    return out


def manifest(root):
    """Dòng 'sha256  đường_dẫn' cho từng file, sắp theo đường dẫn."""
    root = Path(root)
    return [f"{hashlib.sha256((root / r).read_bytes()).hexdigest()}  {r}" for r in files(root)]


def tree_hash(root):
    """SHA-256 của chuỗi manifest (mỗi dòng kết thúc bằng \\n)."""
    return hashlib.sha256("".join(l + "\n" for l in manifest(root)).encode()).hexdigest()


def read_lock(root):
    p = Path(root) / "LOCK"
    if not p.is_file():
        return None
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("TREE_SHA256:"):
            return line.split(":", 1)[1].strip()
    return None
