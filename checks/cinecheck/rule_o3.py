"""O3 — mọi tài sản lấy từ thư viện có SHA; tính lại SHA từ đĩa, không tin số khai.

Thư viện (mặc định assets/LIBRARY.json, phiên P khoá):
  {"assets": [{"id": "CHR-hero-v1", "path": "assets/characters/hero_v1.blend",
               "sha256": "<64 hex>", "rights": "R-001"}]}
Danh sách dùng của shot (<video>.assets.json, bản xuất từ phần mềm dựng):
  {"workdir": "shots/sq01_sh010", "scene_files": ["shots/sq01_sh010/sh010.blend"],
   "assets": ["assets/characters/hero_v1.blend", ...]}
scene_files: file cảnh lắp ráp của shot (chỉ liên kết tài sản thư viện); được miễn quét và liệt kê
trong báo cáo.
Đường dẫn tính từ gốc repo (--repo, mặc định thư mục cha của checks/).
"""
import hashlib
import json
from pathlib import Path

from .common import metric, result

MEDIA_EXT = {".blend", ".fbx", ".obj", ".glb", ".gltf", ".abc", ".usd", ".usda", ".usdc", ".usdz",
             ".png", ".jpg", ".jpeg", ".exr", ".tif", ".tiff", ".webp", ".svg", ".psd", ".kra",
             ".wav", ".flac", ".mp3", ".ogg", ".aif", ".aiff", ".m4a",
             ".ttf", ".otf", ".woff", ".woff2"}
SKIP_DIRS = {"render", "out", "cache", "frames", "__pycache__", ".git"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def check_o3(video, profile, manifest_path=None, library_path=None, repo=None):
    repo = Path(repo).resolve()
    lib = json.load(open(library_path, encoding="utf-8"))
    by_path = {str(Path(a["path"])): a for a in lib.get("assets", [])}
    man = json.load(open(manifest_path, encoding="utf-8"))
    used = [str(Path(p)) for p in man.get("assets", [])]
    not_in_lib, sha_bad, missing_file, lib_sha = [], [], [], {}
    for p in used:
        if p not in by_path:
            not_in_lib.append(p)
            continue
        f = repo / p
        if not f.is_file():
            missing_file.append(p)
            continue
        got = sha256(f)
        lib_sha[p] = got
        if got != by_path[p].get("sha256", "").lower():
            sha_bad.append(dict(path=p, thu_vien=by_path[p].get("sha256"), tren_dia=got))
    strays = []
    notes = []
    scene_files = {str(Path(p)) for p in man.get("scene_files", [])}
    if scene_files:
        notes.append("File cảnh của shot (được miễn quét, v1 sẽ đọc liên kết bên trong): "
                     + ", ".join(sorted(scene_files)))
    wd = man.get("workdir")
    if wd:
        root = (repo / wd).resolve()
        lib_hashes = {a.get("sha256", "").lower() for a in lib.get("assets", [])}
        for f in sorted(root.rglob("*")) if root.is_dir() else []:
            if not f.is_file() or f.suffix.lower() not in MEDIA_EXT:
                continue
            if any(part in SKIP_DIRS for part in f.relative_to(root).parts[:-1]):
                continue
            rel = str(f.relative_to(repo))
            if rel in by_path:
                continue
            if rel in scene_files:
                continue
            if sha256(f) in lib_hashes:
                strays.append(dict(path=rel, ly_do="bản sao của tài sản thư viện; phải dùng đường dẫn thư viện"))
            else:
                strays.append(dict(path=rel, ly_do="file media không có trong thư viện"))
    else:
        notes.append("Danh sách dùng không có 'workdir': không quét được file media lạ.")
    ms = [metric("tài sản không có trong thư viện", len(not_in_lib), "<=", 0),
          metric("tài sản lệch SHA so với thư viện", len(sha_bad), "<=", 0),
          metric("tài sản thư viện thiếu file trên đĩa", len(missing_file), "<=", 0),
          metric("file media lạ trong thư mục làm việc", len(strays), "<=", 0)]
    if not used:
        notes.append("Danh sách tài sản dùng rỗng.")
    return result("O3", None, ms, notes,
                  evidence=dict(so_tai_san_dung=len(used), ngoai_thu_vien=not_in_lib, lech_sha=sha_bad,
                                thieu_file=missing_file, file_la=strays[:100]))
