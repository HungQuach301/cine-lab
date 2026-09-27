"""P1 (chữ đè chữ theo điểm ảnh nét) và G4 (tương phản chữ), đo trên matte chữ xuất từ render
đối chiếu với khung hình render cuối.

Định dạng thư mục chữ (<video>.text/): elements.json
  {"elements": [{"id": "title", "first_frame": 0, "last_frame": 47,
                 "matte": "title.png" | "title/%05d.png"}]}
Matte: PNG RGBA đúng kích thước khung, alpha thẳng, màu = màu nét chữ; chỉ số khung bắt đầu từ 0.
"""
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from .common import FAIL, PASS, frame_count, metric, read_rgb, result

FIDELITY_TOL = 24
FIDELITY_MIN = 90.0
G4_MIN = 4.5
G4_SAMPLES = 24


def load_elements(text_dir):
    text_dir = Path(text_dir)
    spec = json.loads((text_dir / "elements.json").read_text(encoding="utf-8"))
    els = spec.get("elements", [])
    for e in els:
        e["_dir"] = text_dir
    return els


_cache = {}


def matte(e, idx):
    """Trả về mảng RGBA float [0,1] của phần tử e ở khung idx."""
    name = e["matte"]
    p = e["_dir"] / (name % idx if "%" in name else name)
    key = str(p)
    if key not in _cache:
        if len(_cache) > 64:
            _cache.clear()
        _cache[key] = np.asarray(Image.open(p).convert("RGBA"), dtype=np.float32) / 255.0
    return _cache[key]


def active(els, idx):
    return [e for e in els if e["first_frame"] <= idx <= e["last_frame"]]


def stroke(m, thr=0.5):
    return (m[..., 3] >= thr).astype(np.uint8)


def core(m):
    c = (m[..., 3] >= 0.98).astype(np.uint8)
    return cv2.erode(c, np.ones((3, 3), np.uint8)).astype(bool)


def fidelity(m, frame):
    c = core(m)
    if c.sum() < 20:
        return None
    diff = np.abs(m[..., :3][c] * 255.0 - frame[c].astype(np.float32)).max(axis=1)
    return 100.0 * float(np.mean(diff <= FIDELITY_TOL))


def _p1_frames(els, n):
    frames = set()
    for a in els:
        for b in els:
            if a is b:
                continue
            lo = max(a["first_frame"], b["first_frame"])
            hi = min(a["last_frame"], b["last_frame"], n - 1)
            frames.update(range(lo, hi + 1))
    return sorted(frames)


def _sample(e, n):
    lo, hi = e["first_frame"], min(e["last_frame"], n - 1)
    if hi < lo:
        return []
    return sorted(set(np.linspace(lo, hi, min(G4_SAMPLES, hi - lo + 1)).round().astype(int).tolist()))


def _fid_pass(els, n, video):
    """Kiểm độ khớp matte–render trên các khung mẫu của mọi phần tử."""
    per = {}
    idxs = sorted({i for e in els for i in _sample(e, n)})
    frames = read_rgb(video, idxs)
    for e in els:
        vals = [fidelity(matte(e, i), frames[i]) for i in _sample(e, n) if i in frames]
        vals = [v for v in vals if v is not None]
        per[e["id"]] = round(min(vals), 2) if vals else None
    return per, frames


def check_p1(video, profile, text_dir=None):
    els = load_elements(text_dir)
    n = frame_count(video)
    if not els:
        return result("P1", PASS, notes=["elements.json rỗng: không có chữ theo matte xuất ra. "
                                         "v0 chưa có máy dò chữ độc lập (xem quyết định trong RUN.md)."])
    fid, _ = _fid_pass(els, n, video)
    worst_fid = min([v for v in fid.values() if v is not None], default=0.0)
    collisions, where = 0, []
    k = np.ones((3, 3), np.uint8)
    for idx in _p1_frames(els, n):
        act = active(els, idx)
        if len(act) < 2:
            continue
        acc = None
        for e in act:
            s = cv2.dilate(stroke(matte(e, idx)), k).astype(np.uint8)
            acc = s if acc is None else acc + s
        c = int(np.sum(acc >= 2))
        if c:
            collisions += c
            if len(where) < 30:
                ys, xs = np.nonzero(acc >= 2)
                where.append(dict(khung=idx, diem_anh=c, phan_tu=[e["id"] for e in act],
                                  hop=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]))
    ms = [metric("điểm ảnh nét chữ va chạm", collisions, "<=", 0, "px"),
          metric("độ khớp matte–render thấp nhất", worst_fid, ">=", FIDELITY_MIN, "%")]
    notes = []
    if worst_fid < FIDELITY_MIN:
        notes.append("Matte không khớp khung render: số đo chữ không đáng tin, coi như trượt.")
    return result("P1", None, ms, notes, evidence=dict(va_cham=where, do_khop=fid))


def rel_lum(rgb):
    c = rgb.astype(np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def check_g4(video, profile, text_dir=None):
    els = load_elements(text_dir)
    n = frame_count(video)
    if not els:
        return result("G4", PASS, notes=["elements.json rỗng: không có chữ theo matte xuất ra."])
    fid, frames = _fid_pass(els, n, video)
    worst_fid = min([v for v in fid.values() if v is not None], default=0.0)
    per, worst = {}, float("inf")
    d2 = np.ones((5, 5), np.uint8)
    d6 = np.ones((13, 13), np.uint8)
    for e in els:
        vals = []
        for i in _sample(e, n):
            if i not in frames:
                continue
            f = frames[i]
            m = matte(e, i)
            c = core(m)
            if c.sum() < 20:
                continue
            s = stroke(m, 0.02)
            ring = cv2.dilate(s, d6).astype(bool) & ~cv2.dilate(s, d2).astype(bool)
            for o in active(els, i):
                ring &= ~cv2.dilate(stroke(matte(o, i), 0.02), d2).astype(bool)
            if ring.sum() < 20:
                continue
            lt = float(np.median(rel_lum(f[c])))
            lb = rel_lum(f[ring])
            ratio = (np.maximum(lt, lb) + 0.05) / (np.minimum(lt, lb) + 0.05)
            vals.append((float(np.percentile(ratio, 10)), i))
        if vals:
            v, i = min(vals)
            per[e["id"]] = dict(ty_le_p10=round(v, 2), khung=i)
            worst = min(worst, v)
    if worst == float("inf"):
        return result("G4", FAIL, notes=["Không đo được: không có lõi nét hoặc vành nền đủ điểm ảnh."])
    ms = [metric("tương phản chữ/nền (P10) thấp nhất", worst, ">=", G4_MIN, ":1"),
          metric("độ khớp matte–render thấp nhất", worst_fid, ">=", FIDELITY_MIN, "%")]
    return result("G4", None, ms, evidence=dict(theo_phan_tu=per, do_khop=fid))
