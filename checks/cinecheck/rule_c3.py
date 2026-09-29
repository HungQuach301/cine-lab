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
v1.5 (trục đầu, RUN.md 3.6): đầu nhìn thấy có thể rộng hơn cao (mũ che đỉnh, tai vểnh; Cas 'bl' 0°/180°: rộng 782,
cao 481 px mặt nạ); khi đó trục chính PCA lật ngang và "độ dài đầu" thành bề ngang, và nhảy bậc khi trục chính quanh
45° (Cas ±135°: 42°). Model sheet khai 'c3_head_axis': 'doc' = độ dài đầu là bề dài chiếu mặt nạ đầu lên trục dọc thân
(vectơ đơn vị từ tâm mặt nạ thân tới tâm mặt nạ đầu cùng khung; thiếu thân: phương dọc ảnh), liên tục, không lật;
'pca' (mặc định khi không khai) = trục chính như v1.4. c3_views phải đo bằng đúng cách đã khai. Bộ phận khác: trục chính.
"""
import json
import math
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from .common import FAIL, MISSING, PASS, REVIEW, frame_count, metric, probe, read_rgb, result, stream

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
# v1.4 (khiếu nại C3 theo tư thế/góc, chủ dự án chọn B-i): chỉ so tỷ lệ ở mẫu đo được
VIEW_MAX = 30.0     # góc 3D giữa hướng nhìn và góc tham chiếu gần nhất trong c3_views (quyết định chủ dự án)
FORESHORT_MAX = 0.02  # co ngắn do tư thế: |độ dài chiếu xương bây giờ / ở tư thế turnaround − 1| (nội bộ)
HIDDEN_MAX = 0.10   # tỷ lệ điểm ảnh bộ phận bị vật ngoài thân nhân vật che (nội bộ)
DEPTH_MAX = 0.02    # phối cảnh: |khoảng cách máy→giữa bộ phận / máy→tâm đầu − 1| (nội bộ; K thêm, xem RULES.md)
UP = np.array([0.0, 1.0])  # v1.5: phương dọc ảnh (trục dọc dự phòng)
HEAD_AXES = ("pca", "doc")  # v1.5: cách đo độ dài đầu khai trong model sheet 'c3_head_axis' (mặc định 'pca' = v1.4)


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


def _pca(m):
    ys, xs = np.nonzero(m)
    if len(xs) < 5:
        return None
    P = np.stack([xs, ys], 1).astype(np.float64)
    P -= P.mean(0)
    w, v = np.linalg.eigh(np.cov(P.T))  # trị riêng tăng dần: v[:, 1] là trục chính
    return P, w, v


def length_px(m, ref=None):
    """Bề dài chiếu các điểm ảnh lên trục chính PCA + 1 px. ref (v1.5, đầu ở cách đo 'doc'): chiếu lên chính ref."""
    r = _pca(m)
    if r is None:
        return None
    P, _, v = r
    a = P @ (v[:, 1] if ref is None else np.asarray(ref, np.float64))
    return float(a.max() - a.min() + 1)


def body_axis(masks):
    """v1.5: trục dọc thân trên ảnh = vectơ đơn vị từ tâm mặt nạ thân tới tâm mặt nạ đầu (không ngưỡng, không phụ
    thuộc thân thuôn hay bè). Thiếu thân hoặc đầu → phương dọc ảnh. Trả (vectơ, nguồn)."""
    h, t = masks.get("head"), masks.get("torso")
    if h is None or t is None or h.sum() < 5 or t.sum() < 5:
        return UP, "dọc ảnh"
    hy, hx = np.nonzero(h)
    ty, tx = np.nonzero(t)
    d = np.array([hx.mean() - tx.mean(), hy.mean() - ty.mean()])
    n = float(np.hypot(*d))
    if n < 1.0:
        return UP, "dọc ảnh"
    return d / n, "thân→đầu"


def head_flipped(head, ref):
    """v1.5: trục chính của mặt nạ đầu lệch trục dọc thân > 45° (đầu rộng hơn cao): cách 'pca' đo bề ngang."""
    r = _pca(head)
    if r is None:
        return False
    v = r[2]
    return abs(float(v[:, 0] @ ref)) > abs(float(v[:, 1] @ ref)) + 1e-9


def lengths(masks, head_axis="pca"):
    """Độ dài mọi bộ phận của một khung (px mặt nạ). head_axis (v1.5, khai trong model sheet 'c3_head_axis'):
    'pca' = trục chính như v1.4; 'doc' = đầu đo theo trục dọc thân (thân→đầu). Bộ phận khác luôn theo trục chính."""
    ref = body_axis(masks)[0] if head_axis == "doc" else None
    return {p: length_px(m, ref if p == "head" else None) for p, m in masks.items()}


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




# ------------------------------------------------------------------ v1.4: lược đồ, góc nhìn, tư thế
class FormatError(ValueError):
    """parts.json hoặc model sheet sai định dạng: C3 báo THIẾU kèm thông báo, không để lộ lỗi Python."""


_ANG = re.compile(r"^\s*([+\-−]?\d+(?:[.,]\d+)?)\s*(?:°|deg)?\s*$")


def _num(x, what, lo=None, hi=None):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise FormatError(f"{what} phải là số (gặp {x!r}).")
    if (lo is not None and x < lo) or (hi is not None and x > hi):
        raise FormatError(f"{what} = {x} nằm ngoài khoảng cho phép [{lo}, {hi}].")
    return float(x)


def wrap180(a):
    return (float(a) + 180.0) % 360.0 - 180.0


def view_angle(key):
    """Khoá góc của c3_views ('0°', '45°', '-90°', '−90°', '90', 45) → độ trong (−180, 180]."""
    m = _ANG.match(str(key))
    if not m:
        raise FormatError(f"c3_views: khoá góc '{key}' không đọc được (dạng '0°', '45°', '-90°').")
    a = wrap180(float(m.group(1).replace("−", "-").replace(",", ".")))
    return 180.0 if a == -180.0 else a


def _has_len(d, k):
    return isinstance(d, dict) and isinstance(d.get(k), dict) and "length" in d[k]


def sheet_model(sheet):
    """Đọc model sheet theo lược đồ RUN.md 3.6. Trả (names, base, src, refs):
    names = bộ phận đo (trừ đầu); base = {bộ phận: tỷ lệ/đầu} từ độ dài cấp gốc, nếu thiếu thì từ parts{} (một
    nguồn cho mọi bộ phận, không trộn); refs = {góc: {bộ phận: tỷ lệ/đầu hoặc None}} từ c3_views (nếu có)."""
    if not isinstance(sheet, dict):
        raise FormatError("model sheet phải là một object JSON.")
    nested = sheet.get("parts") if isinstance(sheet.get("parts"), dict) else {}
    mp = sheet.get("measured_parts")
    if mp is None:
        mp = [k for k in sheet if _has_len(sheet, k)] or [k for k in nested if _has_len(nested, k)]
        if not mp and isinstance(sheet.get("c3_views"), dict):
            rows = [r for r in sheet["c3_views"].values() if isinstance(r, dict)]
            mp = sorted({k for r in rows for k in r})
    if not isinstance(mp, list) or not all(isinstance(p, str) for p in mp):
        raise FormatError("measured_parts phải là danh sách tên bộ phận (chuỗi).")
    names = [p for p in dict.fromkeys(mp) if p != "head"]
    if not names:
        raise FormatError("measured_parts không có bộ phận nào ngoài 'head'.")
    need = ["head"] + names
    base, src = None, None
    for label, d in (("cấp gốc", sheet), ("parts{}", nested)):
        if all(_has_len(d, k) for k in need):
            L = {k: _num(d[k]["length"], f"model sheet {label}: {k}.length", lo=1e-9) for k in need}
            base, src = {p: L[p] / L["head"] for p in names}, label
            break
    refs = {}
    cv = sheet.get("c3_views")
    if cv is not None:
        if not isinstance(cv, dict) or not cv:
            raise FormatError("c3_views phải là object {góc: {bộ phận: tỷ lệ so với đầu hoặc null}}.")
        for k, row in cv.items():
            a = view_angle(k)
            if a in refs:
                raise FormatError(f"c3_views: góc {a:g}° ghi hai lần.")
            if not isinstance(row, dict):
                raise FormatError(f"c3_views['{k}'] phải là object {{bộ phận: tỷ lệ}}.")
            miss = [p for p in names if p not in row]
            if miss:
                raise FormatError(f"c3_views['{k}'] thiếu bộ phận {miss} (ghi null nếu bộ phận khuất ở góc này).")
            h = _num(row.get("head", 1.0), f"c3_views['{k}'].head", lo=1e-9)
            refs[a] = {p: (None if row[p] is None else _num(row[p], f"c3_views['{k}'].{p}", lo=1e-9) / h)
                       for p in names}
        if base is not None and 0.0 in refs:
            bad = [p for p in names if refs[0.0][p] is not None and abs(refs[0.0][p] / base[p] - 1) > 1e-3]
            if bad:
                raise FormatError(f"c3_views góc 0° khác độ dài {src} ở {bad}: sheet mâu thuẫn, sửa một nguồn.")
    if base is None and not refs:
        lack = {lbl: [k for k in need if not _has_len(d, k)] for lbl, d in (("cấp gốc", sheet), ("parts{}", nested))}
        raise FormatError("không tìm thấy độ dài bộ phận. Cần {bộ phận: {\"length\": số}} cho 'head' và mọi bộ phận "
                          f"trong measured_parts, ở cấp gốc hoặc trong parts{{}}, hoặc bảng c3_views. Thiếu: {lack}.")
    head_axis = sheet.get("c3_head_axis", "pca")
    if head_axis not in HEAD_AXES:
        raise FormatError(f"c3_head_axis phải là 'pca' hoặc 'doc' (gặp {head_axis!r}).")
    return names, base, src, refs, head_axis


def load_sheet(spec, parts_dir, repo):
    ms = spec.get("model_sheet")
    if not isinstance(ms, str) or not ms:
        raise FormatError("parts.json thiếu trường 'model_sheet' (đường dẫn model sheet).")
    for b in (parts_dir, repo):
        p = Path(b) / ms
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8")), p
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                raise FormatError(f"model sheet {ms} không phải JSON hợp lệ: {e}.")
    raise FormatError(f"không thấy model sheet '{ms}' (tìm từ thư mục parts/ rồi từ gốc repo).")


def parse_views(spec, frames, names):
    """views (v1.4, tuỳ chọn): {khung: {view_deg, elev_deg, parts: {bộ phận: {foreshorten, hidden, depth}}}}.
    Có 'views' thì phải có cho mọi khung trong frames, đủ trường cho 'head' và mọi bộ phận đo có mặt nạ."""
    V = spec.get("views")
    if V is None:
        return None
    if not isinstance(V, dict):
        raise FormatError("parts.json: 'views' phải là object {khung: {...}}.")
    out = {}
    for k in frames:
        e = V.get(str(k))
        if not isinstance(e, dict):
            raise FormatError(f"views thiếu khung {k}: có 'views' thì mọi khung trong 'frames' phải có mục.")
        pv = e.get("parts")
        if not isinstance(pv, dict):
            raise FormatError(f"views['{k}'].parts phải là object {{bộ phận: {{foreshorten, hidden, depth}}}}.")
        row = dict(view=_num(e.get("view_deg"), f"views['{k}'].view_deg", -360, 360),
                   elev=_num(e.get("elev_deg"), f"views['{k}'].elev_deg", -90, 90), parts={})
        for p in ["head"] + names:
            if p not in frames[k]:
                continue
            q = pv.get(p)
            if not isinstance(q, dict):
                raise FormatError(f"views['{k}'].parts thiếu '{p}' (bộ phận có mặt nạ ở khung này).")
            row["parts"][p] = dict(fs=_num(q.get("foreshorten"), f"views['{k}'].parts.{p}.foreshorten", 0, 100),
                                   hidden=_num(q.get("hidden"), f"views['{k}'].parts.{p}.hidden", 0, 1),
                                   depth=_num(q.get("depth"), f"views['{k}'].parts.{p}.depth", 1e-6, 1e6))
        out[k] = row
    return out


def view_dev(view, elev, ref):
    """Góc 3D (độ) giữa hướng nhìn thật (yaw view, ngẩng elev) và hướng nhìn tham chiếu (yaw ref, ngẩng 0)."""
    c = math.cos(math.radians(elev)) * math.cos(math.radians(wrap180(view - ref)))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def touches_edge(m):
    return bool(m[0].any() or m[-1].any() or m[:, 0].any() or m[:, -1].any())


def _shots(video, n):
    """Ranh giới shot như G3b (PySceneDetect). Lỗi dò → cả file là một shot (ghi chú)."""
    try:
        from .rule_g3b import shots
        st = sorted(set(int(x) for x in shots(video) if 0 <= int(x) < max(n, 1)) | {0})
        return st, None
    except Exception as e:  # không để lỗi dò shot làm mất kết quả đo
        return [0], f"Không tách được shot ({type(e).__name__}); coi cả file là một shot."


def check_c3(video, profile, parts_dir=None, repo=".", audit=False, assets=None):
    """audit=True (run.py): bắt buộc kiểm toán ngẫu nhiên; gọi trực tiếp (selftest cũ) thì chỉ đo."""
    parts_dir = Path(parts_dir)
    try:
        try:
            spec = json.loads((parts_dir / "parts.json").read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise FormatError(f"parts.json không phải JSON hợp lệ: {e}.")
        if not isinstance(spec, dict):
            raise FormatError("parts.json phải là một object JSON.")
        if spec.get("no_character") is True:
            return result("C3", None, [metric("khai báo không có nhân vật", 1, "==", 1)],
                          notes=["parts.json khai báo shot không có nhân vật (no_character). Người duyệt xác nhận."])
        sheet, sheet_path = load_sheet(spec, parts_dir, repo)
        names, base, src, refs, head_axis = sheet_model(sheet)
        fr_raw = spec.get("frames")
        if not isinstance(fr_raw, dict) or not fr_raw:
            raise FormatError("parts.json thiếu 'frames' {khung: {bộ phận: đường dẫn PNG}}.")
        frames = {}
        for k, v in fr_raw.items():
            if not str(k).isdigit() or not isinstance(v, dict) or not all(isinstance(x, str) for x in v.values()):
                raise FormatError(f"frames['{k}'] phải có khoá là số khung và giá trị {{bộ phận: đường dẫn PNG}}.")
            for part, f in v.items():
                if not (parts_dir / f).is_file():
                    raise FormatError(f"frames['{k}'].{part}: không thấy file {f}.")
            frames[int(k)] = v
        views = parse_views(spec, frames, names)
        if views is not None:
            if not refs:
                refs = {0.0: base}
            default = None
        else:
            default = base if base is not None else refs.get(0.0)
            if default is None:
                raise FormatError("parts.json không có 'views' và model sheet không có độ dài góc 0° (cấp gốc, "
                                  "parts{} hoặc c3_views['0°']): không biết so với số nào.")
    except FormatError as e:
        return result("C3", MISSING, notes=[f"Sai định dạng (RUN.md mục 3.6): {e}"])
    v = stream(probe(video), "video")
    vw, vh = int(v["width"]), int(v["height"])
    declared = spec.get("scale")
    n = frame_count(video)
    required = set(range(0, n, STEP))
    missing = sorted(required - set(frames))
    rgb = read_rgb(video, [k for k in frames if k < n])
    rows, skipped, fids, sure_fail, unproven, head_px = [], [], {}, 0, 0, []
    sizes, xs_all, ys_all, scales, ramps = set(), [], [], [], []
    char_frames, measured_by_frame, total_by_frame, flips = [], {}, {}, []
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
        present = any(m.any() for m in masks.values())
        if present:
            char_frames.append(k)
            total_by_frame[k] = len(names)
            measured_by_frame[k] = 0

        if present and k in rgb:  # chống mặt nạ giả: đo ở mọi khung có nhân vật, kể cả khung không đo được tỷ lệ
            sil = np.zeros(next(iter(masks.values())).shape, bool)
            for m in masks.values():
                sil |= m
            h, w = rgb[k].shape[:2]
            if sil.shape != (h, w):
                sil = cv2.resize(sil.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA) >= 0.5
            fids[k] = fidelity(sil, rgb[k]) if sil.shape == rgb[k].shape[:2] else None

        def skip(p, why, detail=""):
            skipped.append(dict(khung=k, bo_phan=p, ly_do=why, chi_tiet=detail))

        lens = lengths(masks, head_axis)
        lh = lens.get("head")
        if lh is not None:
            ref, ref_src = body_axis(masks)
            if head_flipped(masks["head"], ref):  # v1.5: trục chính đầu lệch trục dọc > 45°
                flips.append(dict(khung=k, truc_doc=ref_src, dau_truc_chinh=round(length_px(masks["head"]) / scale, 1),
                                  dau_theo_truc_doc=round(length_px(masks["head"], ref) / scale, 1)))
        if lh is None:
            if present:
                for p in names:
                    skip(p, "không có mặt nạ đầu (khuất hoặc ngoài khung)")
            continue
        head_px.append(lh / scale)
        V = views.get(k) if views is not None else None
        # lý do cả khung không đo được: đầu bị cắt khung, bị gập/che/xoay, hoặc góc nhìn lệch mọi góc tham chiếu
        frame_why, ref_ang, want = None, None, default
        if touches_edge(masks["head"]):
            frame_why = ("đầu chạm mép khung (bị cắt)", "")
        elif V is not None:
            ref_ang = min(refs, key=lambda a: view_dev(V["view"], V["elev"], a))
            dv = view_dev(V["view"], V["elev"], ref_ang)
            hq = V["parts"]["head"]
            if dv > VIEW_MAX:
                frame_why = (f"góc nhìn lệch > {VIEW_MAX:g}° mọi góc tham chiếu",
                             f"lệch {dv:.1f}° so với {ref_ang:g}° (view {V['view']:g}°, ngẩng {V['elev']:g}°)")
            elif abs(hq["fs"] - 1) > FORESHORT_MAX:
                frame_why = (f"đầu cúi/ngẩng/nghiêng: co ngắn > {100 * FORESHORT_MAX:g}%", f"foreshorten {hq['fs']:.3f}")
            elif hq["hidden"] > HIDDEN_MAX:
                frame_why = (f"đầu bị che > {100 * HIDDEN_MAX:g}%", f"{100 * hq['hidden']:.0f}%")
            want = refs[ref_ang]
        if frame_why:
            for p in names:
                skip(p, *frame_why)
            continue
        for p in names:
            q = V["parts"].get(p) if V is not None else None
            if want.get(p) is None:
                skip(p, "khuất ở góc tham chiếu (c3_views ghi null)", f"{ref_ang:g}°")
                continue
            if q is not None and q["hidden"] > HIDDEN_MAX:
                skip(p, f"bị che > {100 * HIDDEN_MAX:g}%", f"{100 * q['hidden']:.0f}%")
                continue
            if lens.get(p) is None:  # không có mặt nạ mà không khai bị che: lỗi như v1.3
                rows.append(dict(khung=k, bo_phan=p, ket_qua="thiếu mặt nạ"
                                 + (" (views khai không bị che)" if q is not None else "")))
                unproven += 1
                measured_by_frame[k] += 1
                continue
            if touches_edge(masks[p]):
                skip(p, "chạm mép khung (bị cắt)")
                continue
            if q is not None and abs(q["fs"] - 1) > FORESHORT_MAX:
                skip(p, f"gập: co ngắn do tư thế > {100 * FORESHORT_MAX:g}%", f"foreshorten {q['fs']:.3f}")
                continue
            if q is not None and abs(q["depth"] - 1) > DEPTH_MAX:
                skip(p, f"phối cảnh: độ sâu lệch đầu > {100 * DEPTH_MAX:g}%", f"depth {q['depth']:.3f}")
                continue
            lp = lens[p]
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
            measured_by_frame[k] += 1
            rows.append(dict(khung=k, bo_phan=p, goc_tham_chieu=ref_ang, ty_le=round(lp / lh, 4),
                             sheet=round(want[p], 4), lech_pct=round(100 * dev, 2), U_pct=round(100 * u, 2),
                             ket_qua=verdict))
    if not char_frames:
        return result("C3", FAIL, notes=["Không khung nào có mặt nạ bộ phận: không đo được. Shot không có nhân vật "
                                         "thì khai {\"no_character\": true}."])
    # theo shot: tỷ lệ mẫu đo được; shot có nhân vật mà không mẫu nào đo được → CẦN NGƯỜI XEM
    starts, shot_note = _shots(video, n)
    bounds = list(zip(starts, starts[1:] + [max(n, max(frames) + 1)]))
    per_shot, review = [], []
    for i, (a, b) in enumerate(bounds):
        cf = [k for k in char_frames if a <= k < b]
        if not cf:
            continue
        tot = sum(total_by_frame[k] for k in cf)
        got = sum(measured_by_frame[k] for k in cf)
        per_shot.append(dict(shot=i + 1, khung=[a, b - 1], khung_nhan_vat=len(cf), mau=tot, do_duoc=got,
                             ty_le_pct=round(100 * got / tot, 1) if tot else 0.0))
        if got == 0:
            review.append(i + 1)
    sx = [a for a, _ in scales]
    sy = [b for _, b in scales]
    s_meas = float(np.median(sx))
    uniform = len(sizes) == 1 and all(abs(a - b) <= SCALE_TOL * max(a, b) for a, b in scales)
    in_range = SCALE_RANGE[0] - SCALE_TOL <= min(sx + sy) and max(sx + sy) <= SCALE_RANGE[1] + SCALE_TOL
    decl_ok = declared is None or (isinstance(declared, (int, float)) and not isinstance(declared, bool)
                                   and abs(float(declared) - s_meas) <= SCALE_TOL * s_meas)
    pos = np.concatenate([np.concatenate(xs_all) if xs_all else np.array([]),
                          np.concatenate(ys_all) if ys_all else np.array([])])
    share = phase_share(pos, s_meas) if s_meas >= 1.5 else None
    fv = [v for v in fids.values() if v is not None]
    worst_fid = min(fv) if fv else 0.0
    meas = [r for r in rows if "lech_pct" in r]
    max_dev = max(abs(r["lech_pct"]) for r in meas) if meas else None
    upper = max([abs(r["lech_pct"]) + r["U_pct"] for r in meas], default=0.0)
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
    small_head = bool(head_px) and min(head_px) < HEAD_4X
    ms.append(metric(f"đầu < {HEAD_4X:g} px video thì mặt nạ ≥ 4× (Q-δ): hệ số đo khi đầu nhỏ",
                     round(min(sx + sy), 4) if small_head else 4.0, ">=", 4.0 - SCALE_TOL * 4, "×",
                     near_check=small_head))
    ms += [metric("biên trên |lệch| + U lớn nhất (mẫu đo được)", upper, "<=", 100 * TOL, "%", near_check=bool(meas)),
           metric("bộ phận–khung lệch chắc chắn > 3%", sure_fail, "<=", 0),
           metric("bộ phận–khung không chứng minh được ≤ 3% (nhiễu đo)", unproven, "<=", 0),
           metric("khung mẫu (mỗi 12 khung) thiếu mặt nạ", len(missing), "<=", 0),
           metric("độ khớp biên mặt nạ–cạnh ảnh render thấp nhất", worst_fid, ">=", FID_MIN)]
    review_m = metric("shot có nhân vật mà không mẫu nào đo được (→ CẦN NGƯỜI XEM, không ĐẠT)", len(review), "<=", 0,
                      near_check=False)
    tot_all = sum(total_by_frame.values())
    got_all = sum(measured_by_frame.values())
    sizes_s = sorted(sizes)[0]
    notes = [f"Model sheet: {sheet_path.name} (độ dài: {src or 'chỉ c3_views'}; đầu đo theo '{head_axis}'; "
             f"góc tham chiếu: {', '.join(f'{a:g}°' for a in sorted(refs)) if views is not None else '0° (không có views)'}). "
             f"Mặt nạ {sizes_s[1]}×{sizes_s[0]} px trên khung {vw}×{vh} → hệ số đo ×{s_meas:.3g} "
             f"(khai báo: {declared if declared is not None else 'không'}). "
             + (f"Đầu cao {min(head_px):.1f}–{max(head_px):.1f} px video. " if head_px else "")
             + f"Lệch lớn nhất (mẫu đo được) {max_dev}%. {len(pos)} vị trí biên phân biệt; tỷ lệ dồn 1 pha "
             f"{'—' if share is None else f'{share:.2f}'} (trải đều ≈ {1 / max(1, round(s_meas)):.2f}).",
             f"Mẫu bộ phận đo được: {got_all}/{tot_all} ({100 * got_all / max(tot_all, 1):.1f}%) trên "
             f"{len(char_frames)} khung có nhân vật. Theo shot: "
             + "; ".join(f"shot {r['shot']} (khung {r['khung'][0]}–{r['khung'][1]}): {r['do_duoc']}/{r['mau']} "
                         f"({r['ty_le_pct']:g}%)" for r in per_shot) + "."]
    if skipped:
        why = {}
        for r in skipped:
            why[r["ly_do"]] = why.get(r["ly_do"], 0) + 1
        notes.append(f"Không đo được: {len(skipped)} mẫu bộ phận — "
                     + "; ".join(f"{k}: {v}" for k, v in why.items()) + ". Danh sách đầy đủ trong bằng chứng "
                     "'khong_do_duoc'.")
    if head_axis == "doc":
        notes.append("v1.5: model sheet khai c3_head_axis = 'doc': độ dài đầu = bề dài chiếu lên trục dọc thân "
                     f"(thân→đầu), không lật. {len(flips)} khung có đầu rộng hơn cao (trục chính sẽ lật).")
    elif flips:
        notes.append(f"v1.5 (trục đầu): {len(flips)}/{len(head_px)} khung có mặt nạ đầu rộng hơn cao (trục chính lệch trục "
                     "dọc thân > 45°): cách 'pca' (mặc định, như v1.4) đo bề ngang đầu ở các khung này, và số nhảy bậc khi "
                     "trục chính quanh 45°. Nên đo lại c3_views theo 'doc' và khai c3_head_axis = 'doc' (RUN.md 3.6.1). "
                     "Danh sách trong bằng chứng 'dau_rong_hon_cao' (px video).")
    if views is None:
        notes.append("parts.json không có 'views' (v1.4): mọi mẫu so với góc 0° như v1.3; chỉ loại mẫu bị cắt khung. "
                     "Xuất 'views' từ render để máy loại mẫu lệch góc, gập, bị che, phối cảnh (RUN.md 3.6).")
    if shot_note:
        notes.append(shot_note)
    if review:
        notes.append(f"Shot {review}: có nhân vật nhưng không mẫu nào đo được. C3 = CẦN NGƯỜI XEM: người duyệt so "
                     "nhân vật với model sheet bằng mắt; máy không cho ĐẠT.")
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
    ev = dict(do=rows[:300], khong_do_duoc=skipped[:300], theo_shot=per_shot,
              do_khop_bien={str(k): (round(v, 2) if v is not None else None) for k, v in fids.items()},
              khung_thieu=missing[:100], dau_rong_hon_cao=flips[:300])
    hard_ok = all(m["ok"] for m in ms)
    if audit:
        from . import audit as au
        a_ms, a_notes, audit_ev, has_req = au.verify(video, parts_dir, repo, spec, load_mask,
                                                     lambda ms_: lengths(ms_, head_axis), uncertainty, assets)
        notes += a_notes
        ev["kiem_toan"] = audit_ev or None
        if not has_req:
            st = FAIL if not hard_ok else MISSING
            return result("C3", st, ms + [review_m], notes, evidence=ev)
        ms += a_ms
        hard_ok = all(m["ok"] for m in ms)
    st = FAIL if not hard_ok else (REVIEW if review else PASS)
    return result("C3", st, ms + [review_m], notes, evidence=ev)
