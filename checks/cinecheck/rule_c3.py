"""C3 — đúng model: tỷ lệ bộ phận nhân vật đo từ mặt nạ render so với model sheet, có tính nhiễu đo.

Thư mục <video>.parts/parts.json (xuất từ render, cùng phép biến đổi với khung hình):
  {"model_sheet": "bible/characters/hero.model.json",   # tính từ thư mục parts/ rồi từ gốc repo
   "scale": 1,                                           # px mặt nạ / px video (render mặt nạ 2×, 4× được)
   "frames": {"0": {"head": "00000/head.png", "torso": "00000/torso.png", ...}, "12": {...}}}
Mỗi mặt nạ: PNG, bộ phận ≥ 128 (kênh xám hoặc alpha). Khung mà mặt nạ đầu rỗng = nhân vật không hiện.
Độ dài = bề dài chiếu lên trục chính (PCA) của tâm điểm ảnh + 1 px. Tỷ lệ = độ dài bộ phận / độ dài đầu.
Nhiễu đo U = sqrt((δ/L_bộ_phận)² + (δ/L_đầu)²), δ = 1 px mặt nạ: hiệu chuẩn Monte Carlo (selftest) —
phủ 100% sai số thật ở đầu 40–146 px. Quy tắc quyết định kiểu ISO 14253-1 (dải bảo vệ):
  đạt khi |lệch| + U ≤ 3%; trượt chắc chắn khi |lệch| − U > 3%; còn lại = không chứng minh được.
"""
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from .common import FAIL, frame_count, metric, read_rgb, result

TOL = 0.03          # khung mục 4.C (nội bộ)
DELTA_PX = 1.0      # sai số đầu mút tổng mỗi độ dài (px mặt nạ), hiệu chuẩn trong selftest
STEP = 12           # phải có mặt nạ cho mọi khung chia hết cho 12
FID_MIN = 1.5       # độ khớp biên mặt nạ với cạnh ảnh render (nội bộ)
SHIFT = 6


def load_mask(p):
    im = Image.open(p)
    a = np.asarray(im.convert("RGBA"))
    m = a[..., 3] if im.mode in ("RGBA", "LA") or "transparency" in im.info else a[..., :3].max(-1)
    return m >= 128


def length_px(m):
    ys, xs = np.nonzero(m)
    if len(xs) < 5:
        return None
    P = np.stack([xs, ys], 1).astype(np.float64)
    P -= P.mean(0)
    _, v = np.linalg.eigh(np.cov(P.T))
    a = P @ v[:, 1]
    return float(a.max() - a.min() + 1)


def uncertainty(lp, lh, delta=DELTA_PX):
    return float(np.sqrt((delta / lp) ** 2 + (delta / lh) ** 2))


def fidelity(sil, frame):
    """Cạnh ảnh render trên biên bóng nhân vật so với biên dịch ±6 px (trung vị 8 hướng)."""
    g = cv2.GaussianBlur(frame.astype(np.float32), (0, 0), 1.0)
    e = np.max([np.hypot(cv2.Sobel(g[..., c], cv2.CV_32F, 1, 0), cv2.Sobel(g[..., c], cv2.CV_32F, 0, 1))
                for c in range(3)], axis=0)
    s = sil.astype(np.uint8)
    b = (s & ~cv2.erode(s, np.ones((3, 3), np.uint8)).astype(bool)).astype(bool)
    if b.sum() < 20:
        return None
    on = float(e[b].mean())
    off = []
    for dx, dy in ((SHIFT, 0), (-SHIFT, 0), (0, SHIFT), (0, -SHIFT), (SHIFT, SHIFT), (-SHIFT, -SHIFT),
                   (SHIFT, -SHIFT), (-SHIFT, SHIFT)):
        bs = np.roll(np.roll(b, dy, 0), dx, 1)
        off.append(float(e[bs].mean()))
    return on / max(np.median(off), 1e-6)


def _sheet(spec, parts_dir, repo):
    for base in (parts_dir, repo):
        p = Path(base) / spec["model_sheet"]
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8")), p
    raise FileNotFoundError(f"Không thấy model sheet {spec['model_sheet']}")


def check_c3(video, profile, parts_dir=None, repo="."):
    parts_dir = Path(parts_dir)
    spec = json.loads((parts_dir / "parts.json").read_text(encoding="utf-8"))
    if spec.get("no_character") is True:
        return result("C3", None, [metric("khai báo không có nhân vật", 1, "==", 1)],
                      notes=["parts.json khai báo shot không có nhân vật (no_character). Người duyệt xác nhận."])
    sheet, sheet_path = _sheet(spec, parts_dir, repo)
    scale = float(spec.get("scale", 1))
    names = [p for p in sheet.get("measured_parts", [k for k, v in sheet.items()
                                                       if isinstance(v, dict) and "length" in v]) if p != "head"]
    want = {p: sheet[p]["length"] / sheet["head"]["length"] for p in names}
    n = frame_count(video)
    frames = {int(k): v for k, v in spec.get("frames", {}).items()}
    required = set(range(0, n, STEP))
    missing = sorted(required - set(frames))
    rgb = read_rgb(video, [k for k in frames if k < n])
    rows, fids, sure_fail, unproven, head_px = [], {}, 0, 0, []
    for k in sorted(frames):
        masks = {p: load_mask(parts_dir / f) for p, f in frames[k].items()}
        if "head" not in masks or length_px(masks["head"]) is None:
            continue
        lh = length_px(masks["head"])
        head_px.append(lh / scale)
        for p in names:
            if p not in masks or length_px(masks[p]) is None:
                rows.append(dict(khung=k, bo_phan=p, ket_qua="thiếu mặt nạ"))
                unproven += 1
                continue
            lp = length_px(masks[p])
            dev = (lp / lh) / want[p] - 1
            u = uncertainty(lp, lh)
            if abs(dev) - u > TOL:
                verdict = "trượt chắc chắn"
                sure_fail += 1
            elif abs(dev) + u <= TOL:
                verdict = "đạt"
            else:
                verdict = "không chứng minh được"
                unproven += 1
            rows.append(dict(khung=k, bo_phan=p, ty_le=round(lp / lh, 4), sheet=round(want[p], 4),
                             lech_pct=round(100 * dev, 2), U_pct=round(100 * u, 2), ket_qua=verdict))
        if k in rgb:
            sil = np.zeros(next(iter(masks.values())).shape, bool)
            for m in masks.values():
                sil |= m
            if scale != 1:
                h, w = rgb[k].shape[:2]
                sil = cv2.resize(sil.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA) >= 0.5
            if sil.shape == rgb[k].shape[:2]:
                fids[k] = fidelity(sil, rgb[k])
            else:
                fids[k] = None
    if not rows:
        return result("C3", FAIL, notes=["Không khung nào có mặt nạ đầu: không đo được."])
    fv = [v for v in fids.values() if v is not None]
    worst_fid = min(fv) if fv else 0.0
    max_dev = max(abs(r["lech_pct"]) for r in rows if "lech_pct" in r) if any("lech_pct" in r for r in rows) else None
    upper = max([abs(r["lech_pct"]) + r["U_pct"] for r in rows if "lech_pct" in r], default=float("inf"))
    ms = [metric("biên trên |lệch| + U lớn nhất", upper, "<=", 100 * TOL, "%"),
          metric("bộ phận–khung lệch chắc chắn > 3%", sure_fail, "<=", 0),
          metric("bộ phận–khung không chứng minh được ≤ 3% (nhiễu đo)", unproven, "<=", 0),
          metric("khung mẫu (mỗi 12 khung) thiếu mặt nạ", len(missing), "<=", 0),
          metric("độ khớp biên mặt nạ–cạnh ảnh render thấp nhất", worst_fid, ">=", FID_MIN)]
    notes = [f"Model sheet: {sheet_path.name}. Đầu cao {min(head_px):.1f}–{max(head_px):.1f} px video "
             f"(mặt nạ ×{scale:g}). Lệch lớn nhất {max_dev}%."]
    if unproven:
        notes.append("Có số đo nằm trong dải nhiễu quanh 3%: render mặt nạ ở độ phân giải cao hơn (scale 2–4) "
                     "hoặc chọn khung có đầu lớn hơn để chứng minh.")
    return result("C3", None, ms, notes, evidence=dict(
        do=rows[:300], do_khop_bien={str(k): (round(v, 2) if v is not None else None) for k, v in fids.items()},
        khung_thieu=missing[:100]))
