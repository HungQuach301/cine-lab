"""C3 — đúng model: tỷ lệ bộ phận nhân vật đo từ mặt nạ render so với model sheet, có tính nhiễu đo.

Thư mục <video>.parts/parts.json (xuất từ render, cùng phép biến đổi với khung hình):
  {"model_sheet": "bible/characters/hero.model.json",   # tính từ thư mục parts/ rồi từ gốc repo
   "scale": 4,                                           # tuỳ chọn; máy đo hệ số từ kích thước PNG
   "frames": {"0": {"head": "00000/head.png", "torso": "00000/torso.png", ...}, "12": {...}}}
Mỗi mặt nạ: PNG, bộ phận ≥ 128 (kênh xám hoặc alpha). Khung mà mặt nạ đầu rỗng = nhân vật không hiện.
Độ dài = bề dài chiếu lên trục chính (PCA) của tâm điểm ảnh + 1 px. Tỷ lệ = độ dài bộ phận / độ dài đầu.
v1.1 (Q-C3): mặt nạ BẮT BUỘC có độ phân giải gấp s = 2–4 lần khung video. s đo từ kích thước PNG
(rộng mặt nạ / rộng video, cao mặt nạ / cao video; hai hệ số phải bằng nhau), không tin trường "scale";
nếu có khai "scale" thì phải khớp số đo. Chống phóng to mặt nạ 1× lên: vị trí biên (x của chuyển tiếp
ngang, y của chuyển tiếp dọc, lấy tập giá trị phân biệt) quy về pha lưới s; mặt nạ phóng to từ ảnh nhị
phân thấp hơn có biên dồn vào 1 pha, mặt nạ render thật trải đều.
Nhiễu đo U(s) = sqrt((δ/(s·L_bộ_phận))² + (δ/(s·L_đầu))²), L tính bằng px video, δ = 2 px MẶT NẠ (v1.2; v1.1: 1):
hiệu chuẩn Monte Carlo (selftest) ở s = 1, 2, 4 — phủ 100% sai số thật ở đầu 40–146 px video.
v1.2 (Q-C3b): (1) mặt nạ xám (khử răng cưa) có dải chuyển tiếp biên rộng hơn RAMP_MAX px mặt nạ = phóng to
từ ảnh thấp hơn còn giữ mức xám → trượt; (2) mặt nạ phóng to từ matte 1× có khử răng cưa rồi ngưỡng hoá bằng
nhân mượt (song tuyến, bicubic, Lanczos) KHÔNG phân biệt được đáng tin với render thật bằng phân tích ảnh
(khảo sát v1.2: chỉ số dựng lại từ 1× của hai loại chồng nhau trên hình đa giác). Thay vào đó δ được nâng lên
2,0 px mặt nạ, đủ phủ sai số của cả loại này (tối đa 1,557·U(δ=1) trên ~770 mẫu, s = 2–4, đầu 40–146 px) và
của mặt nạ thật ở mọi cỡ đầu (tối đa 1,21·U(δ=1): mô hình δ = 1 của v1.1 che thiếu khi khảo sát thêm cỡ đầu):
mặt nạ phóng to không thể dẫn tới kết luận "đạt" sai.
v1.3: (Q-δ) đầu nhân vật cao < 100 px video ở bất kỳ khung mẫu nào thì mặt nạ phải ≥ 4×. (Q-C3c) kiểm toán ngẫu
nhiên (cinecheck/audit.py) khi chạy qua run.py: thiếu yêu cầu kiểm toán → THIẾU; đối chiếu trượt → TRƯỢT.
Quy tắc quyết định kiểu ISO 14253-1 (dải bảo vệ):
  đạt khi |lệch| + U ≤ 3%; trượt chắc chắn khi |lệch| − U > 3%; còn lại = không chứng minh được.
"""
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from .common import FAIL, MISSING, frame_count, metric, probe, read_rgb, result, stream

TOL = 0.03          # khung mục 4.C (nội bộ)
DELTA_PX = 2.0      # sai số đầu mút tổng mỗi độ dài (px mặt nạ); v1.2 nâng từ 1,0 (xem đầu file), hiệu chuẩn selftest
HEAD_4X = 100.0     # v1.3 (Q-δ): đầu < 100 px video thì mặt nạ bắt buộc ≥ 4×
RAMP_MAX = 2.5      # độ rộng dải xám ở biên (px mặt nạ / px biên); render AA thật ≈ 1–2, phóng to xám ≈ s × (1–2)
STEP = 12           # phải có mặt nạ cho mọi khung chia hết cho 12
FID_MIN = 1.5       # độ khớp biên mặt nạ với cạnh ảnh render (nội bộ)
SHIFT = 6
SCALE_RANGE = (2.0, 4.0)  # Q-C3: mặt nạ gấp 2–4 lần khung
SCALE_TOL = 0.005         # sai lệch tương đối cho phép giữa hệ số ngang/dọc và với số khai
# tỷ lệ vị trí biên dồn vào 1 pha lưới s: trải đều ≈ 1/k, phóng to ≈ 1,0; ngưỡng = giữa hai mức (nội bộ)
def phase_max(s):
    k = max(1, int(round(s)))
    return 1 / k + 0.5 * (1 - 1 / k)
PHASE_MIN_POS = 40        # cần ≥ 40 vị trí biên phân biệt để kết luận pha


def load_raw(p):
    """Kênh mặt nạ uint8 (xám, alpha, hoặc max RGB)."""
    im = Image.open(p)
    if im.mode == "L" and "transparency" not in im.info:
        return np.asarray(im)
    if im.mode in ("RGBA", "LA") or "transparency" in im.info:
        return np.asarray(im.convert("RGBA"))[..., 3]
    return np.asarray(im.convert("RGB")).max(-1)


def load_mask(p):
    return load_raw(p) >= 128


def ramp_width(raw):
    """Số điểm ảnh xám (6–249) trên mỗi điểm ảnh biên của mặt nạ ngưỡng hoá. Nhị phân: 0; AA thật ≈ 1–2."""
    m = raw >= 128
    b = int((m ^ cv2.erode(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)).sum())
    if b == 0:
        return None
    return float(((raw > 5) & (raw < 250)).sum()) / b


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


def edge_positions(m):
    """Tập vị trí biên phân biệt: x của chuyển tiếp theo hàng, y của chuyển tiếp theo cột."""
    xs = np.unique(np.nonzero(m[:, 1:] != m[:, :-1])[1] + 1)
    ys = np.unique(np.nonzero(m[1:, :] != m[:-1, :])[0] + 1)
    return xs, ys


def phase_share(positions, s):
    """Tỷ lệ vị trí rơi vào pha đông nhất của lưới s (k = round(s) ngăn)."""
    k = max(1, int(round(s)))
    if len(positions) == 0:
        return None
    # pha = (x mod s)·k/s; cộng 1e-6 để x = s/3 không rơi nhầm ngăn 0 do làm tròn số thực
    ph = np.floor(np.mod(np.asarray(positions, np.float64), s) * k / s + 1e-6).astype(int) % k
    return float(np.bincount(ph, minlength=k).max() / len(ph))


def _sheet(spec, parts_dir, repo):
    for base in (parts_dir, repo):
        p = Path(base) / spec["model_sheet"]
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8")), p
    raise FileNotFoundError(f"Không thấy model sheet {spec['model_sheet']}")


def check_c3(video, profile, parts_dir=None, repo=".", audit=False, assets=None):
    """audit=True (run.py): bắt buộc kiểm toán ngẫu nhiên; gọi trực tiếp (selftest cũ) thì chỉ đo."""
    parts_dir = Path(parts_dir)
    spec = json.loads((parts_dir / "parts.json").read_text(encoding="utf-8"))
    if spec.get("no_character") is True:
        return result("C3", None, [metric("khai báo không có nhân vật", 1, "==", 1)],
                      notes=["parts.json khai báo shot không có nhân vật (no_character). Người duyệt xác nhận."])
    sheet, sheet_path = _sheet(spec, parts_dir, repo)
    v = stream(probe(video), "video")
    vw, vh = int(v["width"]), int(v["height"])
    declared = spec.get("scale")
    names = [p for p in sheet.get("measured_parts", [k for k, v in sheet.items()
                                                       if isinstance(v, dict) and "length" in v]) if p != "head"]
    want = {p: sheet[p]["length"] / sheet["head"]["length"] for p in names}
    n = frame_count(video)
    frames = {int(k): v for k, v in spec.get("frames", {}).items()}
    required = set(range(0, n, STEP))
    missing = sorted(required - set(frames))
    rgb = read_rgb(video, [k for k in frames if k < n])
    rows, fids, sure_fail, unproven, head_px = [], {}, 0, 0, []
    sizes, xs_all, ys_all, scales, ramps = set(), [], [], [], []
    for k in sorted(frames):
        raws = {p: load_raw(parts_dir / f) for p, f in frames[k].items()}
        for r_ in raws.values():
            rw_ = ramp_width(r_)
            if rw_ is not None:
                ramps.append(rw_)
        masks = {p: r_ >= 128 for p, r_ in raws.items()}
        for m in masks.values():
            sizes.add(m.shape)
        shp = next(iter(masks.values())).shape if masks else (vh, vw)
        scale = shp[1] / vw
        scales.append((shp[1] / vw, shp[0] / vh))
        for m in masks.values():
            ex, ey = edge_positions(m)
            xs_all.append(ex)
            ys_all.append(ey)
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
            u = uncertainty(lp, lh)  # δ = DELTA_PX
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
            h, w = rgb[k].shape[:2]
            if sil.shape != (h, w):
                sil = cv2.resize(sil.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA) >= 0.5
            if sil.shape == rgb[k].shape[:2]:
                fids[k] = fidelity(sil, rgb[k])
            else:
                fids[k] = None
    if not rows:
        return result("C3", FAIL, notes=["Không khung nào có mặt nạ đầu: không đo được."])
    sx = [a for a, _ in scales]
    sy = [b for _, b in scales]
    s_meas = float(np.median(sx))
    uniform = len(sizes) == 1 and all(abs(a - b) <= SCALE_TOL * max(a, b) for a, b in scales)
    in_range = SCALE_RANGE[0] - SCALE_TOL <= min(sx + sy) and max(sx + sy) <= SCALE_RANGE[1] + SCALE_TOL
    decl_ok = declared is None or abs(float(declared) - s_meas) <= SCALE_TOL * s_meas
    pos = np.concatenate([np.concatenate(xs_all) if xs_all else np.array([]),
                          np.concatenate(ys_all) if ys_all else np.array([])])
    share = phase_share(pos, s_meas) if s_meas >= 1.5 else None
    fv = [v for v in fids.values() if v is not None]
    worst_fid = min(fv) if fv else 0.0
    max_dev = max(abs(r["lech_pct"]) for r in rows if "lech_pct" in r) if any("lech_pct" in r for r in rows) else None
    upper = max([abs(r["lech_pct"]) + r["U_pct"] for r in rows if "lech_pct" in r], default=float("inf"))
    ms = [metric("hệ số phân giải mặt nạ/khung đo từ kích thước PNG (nhỏ nhất)", round(min(sx + sy), 4), ">=",
                 SCALE_RANGE[0], "×"),
          metric("hệ số phân giải mặt nạ/khung đo từ kích thước PNG (lớn nhất)", round(max(sx + sy), 4), "<=",
                 SCALE_RANGE[1], "×"),
          metric("mặt nạ cùng kích thước, hệ số ngang = dọc", uniform, "==", True),
          metric("'scale' khai báo khớp hệ số đo (bỏ trống được)", decl_ok, "==", True)]
    if share is not None:
        ms.append(metric("vị trí biên phân biệt để kiểm pha lưới", len(pos), ">=", PHASE_MIN_POS, near_check=False))
        ms.append(metric("vị trí biên dồn vào 1 pha lưới (phóng to từ mặt nạ thấp hơn)", share, "<=",
                         round(phase_max(s_meas), 4)))
    ramp_max = max(ramps) if ramps else 0.0
    ms.append(metric("dải xám ở biên mặt nạ (phóng to còn giữ mức xám), lớn nhất", ramp_max, "<=", RAMP_MAX,
                     "px/px biên"))
    small_head = min(head_px) < HEAD_4X
    ms.append(metric(f"đầu < {HEAD_4X:g} px video thì mặt nạ ≥ 4× (Q-δ): hệ số đo khi đầu nhỏ",
                     round(min(sx + sy), 4) if small_head else 4.0, ">=", 4.0 - SCALE_TOL * 4, "×",
                     near_check=small_head))
    ms += [metric("biên trên |lệch| + U lớn nhất", upper, "<=", 100 * TOL, "%"),
          metric("bộ phận–khung lệch chắc chắn > 3%", sure_fail, "<=", 0),
          metric("bộ phận–khung không chứng minh được ≤ 3% (nhiễu đo)", unproven, "<=", 0),
          metric("khung mẫu (mỗi 12 khung) thiếu mặt nạ", len(missing), "<=", 0),
          metric("độ khớp biên mặt nạ–cạnh ảnh render thấp nhất", worst_fid, ">=", FID_MIN)]
    notes = [f"Model sheet: {sheet_path.name}. Mặt nạ {sorted(sizes)[0][1]}×{sorted(sizes)[0][0]} px trên khung "
             f"{vw}×{vh} → hệ số đo ×{s_meas:.3g} (khai báo: {declared if declared is not None else 'không'}). "
             f"Đầu cao {min(head_px):.1f}–{max(head_px):.1f} px video. Lệch lớn nhất {max_dev}%. "
             f"{len(pos)} vị trí biên phân biệt; tỷ lệ dồn 1 pha "
             f"{'—' if share is None else f'{share:.2f}'} (trải đều ≈ {1 / max(1, round(s_meas)):.2f})."]
    if not in_range:
        notes.append("Q-C3: mặt nạ phải render ở độ phân giải gấp 2–4 lần khung video (đo từ kích thước PNG).")
    if share is not None and share > phase_max(s_meas):
        notes.append("Biên mặt nạ nằm trên lưới thô: mặt nạ có vẻ được phóng to từ độ phân giải thấp hơn, "
                     "không phải render ở hệ số khai. Render lại mặt nạ ở độ phân giải thật.")
    if ramp_max > RAMP_MAX:
        notes.append("Biên mặt nạ là dải xám rộng: mặt nạ có vẻ được phóng to từ ảnh độ phân giải thấp hơn. "
                     "Render mặt nạ ở độ phân giải thật (nhị phân hoặc khử răng cưa ở chính độ phân giải đó).")
    if small_head and min(sx + sy) < 4.0 - SCALE_TOL * 4:
        notes.append(f"Đầu nhỏ nhất {min(head_px):.1f} px video < {HEAD_4X:g} px: bắt buộc mặt nạ 4× (Q-δ).")
    if unproven:
        notes.append("Có số đo nằm trong dải nhiễu quanh 3%: render mặt nạ ở độ phân giải cao hơn (scale 2–4) "
                     "hoặc chọn khung có đầu lớn hơn để chứng minh.")
    audit_ev = {}
    if audit:
        from . import audit as au
        a_ms, a_notes, audit_ev, has_req = au.verify(video, parts_dir, repo, spec, load_mask, length_px,
                                                     uncertainty, assets)
        notes += a_notes
        if not has_req:
            st = FAIL if not all(m["ok"] for m in ms) else MISSING
            return result("C3", st, ms, notes, evidence=dict(
                do=rows[:300], do_khop_bien={str(k): (round(v, 2) if v is not None else None) for k, v in fids.items()},
                khung_thieu=missing[:100], kiem_toan=None))
        ms += a_ms
    return result("C3", None, ms, notes, evidence=dict(kiem_toan=audit_ev,
        do=rows[:300], do_khop_bien={str(k): (round(v, 2) if v is not None else None) for k, v in fids.items()},
        khung_thieu=missing[:100]))
