"""P0 — máy dò chữ độc lập trên khung render. Không dựa vào matte: chữ dò được mà không có matte
tương ứng trong <video>.text/ thì trượt (vá giới hạn 2 của v0: P1/G4 chỉ thấy chữ có matte).

v1.1 (Q-P0): phần tử có "diegetic": true (chữ trong thế giới phim: biển hiệu, tên phố) vẫn phải có
matte (P0) và qua P1, nhưng được miễn G4. Chống lạm dụng: chữ máy đọc được trong matte của phần tử
diegetic mà trùng nội dung phụ đề/tiêu đề (dòng thoại trong <video>.script.txt, chữ đọc được trong
matte của phần tử không diegetic, trường "text" khai cho phần tử không diegetic) thì trượt.

v1.5 (khiếu nại Cổng 5 "56" ở mắt Cas s42a, "MA" ở dáng hai nhân vật s33; chủ dự án chấp nhận 29/09/2026): vùng máy đọc
ra chữ nhưng thật ra là nhân vật. Vùng chữ không matte được MIỄN khi đủ cả năm điều kiện:
  (1) chuỗi đọc được ≤ 3 ký tự (không kể khoảng trắng): chữ thật ≥ 4 ký tự luôn bị bắt, kể cả trên người nhân vật;
  (2) khung có mặt nạ nhân vật trong <video>.parts/ (mặt nạ bộ phận C3 của đúng khung đó và/hoặc 'silhouettes');
  (3) mặt nạ khớp cạnh ảnh render NGAY QUANH hộp chữ (hộp nới 16 px): độ khớp biên cục bộ ≥ FID_MIN của C3 (1,5), cùng
      cách tính với C3 (cạnh ảnh trên biên mặt nạ / trung vị 8 hướng dịch ±6 px). Mặt nạ vẽ thêm để che chữ thật không
      khớp hình ở chỗ đó (thử: khối giả che "56" trên tường 1,04) nên không được miễn, dù phần còn lại của mặt nạ đúng;
  (4) mặt nạ (nới 2 px) chạm hộp chữ;
  (5) phản chứng: xoá phần nhân vật trong khung (tô lại từ nền quanh, cv2.inpaint) rồi đọc lại đúng hộp đó, máy KHÔNG
      còn đọc ra chữ Latin (cùng tiêu chí is_latin_text, độ tin 0,8). Tức là thứ máy đọc thành chữ nằm trên nhân vật.
      Chữ thật trên tường cạnh nhân vật vẫn còn sau khi xoá nhân vật → vẫn trượt.
Đo "nằm phần lớn trong mặt nạ" bằng phản chứng (5) chứ không bằng tỷ lệ diện tích: hộp "MA" (s33) rộng 266×165 px, phần
lớn là tường giữa hai người; nhân vật chỉ phủ 16% hộp, 29% vùng xác suất chữ, nhưng chính hai dáng người là thứ bị đọc.
Vùng được miễn vẫn liệt kê trong bằng chứng 'vung_nhan_vat_mien' để người duyệt soi.
"""
import difflib
import json
import re
from pathlib import Path

import numpy as np
import cv2

from .common import frame_count, metric, read_rgb, result
from .textdet import detect, is_latin_text, recognize, solidity

STEP = 12          # 2 khung/giây
MAX_FRAMES = 240
MIN_COVER = 0.5    # tỷ lệ diện tích hộp chữ nằm trong vùng matte (nét nới) để coi là có matte
MIN_DET = 0.6      # điểm hộp tối thiểu của mô hình dò
MIN_REC = 0.8      # độ tin nhận dạng tối thiểu để xác nhận là chữ Latin
SOLID_MAX = 0.85   # ký tự có nét (độ đặc 0,4–0,7 đo được); ô cửa sổ/lưới là khối đặc (≈ 1,0)
DUP_LINE = 0.80    # tỷ lệ giống (difflib, ký tự) giữa chữ diegetic và cả một dòng phụ đề/tiêu đề
DUP_PART = 0.85    # tỷ lệ giống với một đoạn liền của dòng (≥ 2 từ và ≥ 50% số từ của dòng)
MAX_CHARS = 3      # v1.5: chuỗi ≤ 3 ký tự mới được xét miễn (phán quyết chủ dự án 29/09/2026)
CHAR_GROW = 2      # v1.5: nới mặt nạ nhân vật 2 px video trước khi xoá (dải khử răng cưa, lớp vẽ) (nội bộ)
INPAINT_R = 5      # v1.5: bán kính cv2.inpaint (Telea) khi xoá nhân vật (nội bộ)
FID_MARGIN = 16    # v1.5: vùng đo độ khớp biên cục bộ = hộp chữ nới 16 px video (nội bộ)
FID_BMIN = 20      # v1.5: cần ≥ 20 điểm biên mặt nạ trong vùng đó mới kết luận (như C3)


def is_diegetic(e):
    return e.get("diegetic") is True


def script_lines(path):
    """Dòng thoại (= phụ đề) từ kịch bản, cùng quy tắc bỏ nhãn/chỉ dẫn như J1; tách thêm từng câu;
    chuẩn hoá thành từ."""
    from .rule_j1 import normalize
    out = []
    if path is None:
        return out
    for line in open(path, encoding="utf-8"):
        t = line.strip()
        if not t or t.startswith("#"):
            continue
        t = re.sub(r"^[A-Z][A-Z0-9 .'\-]{0,30}:\s+", "", t)
        t = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", t)
        # mỗi dòng và mỗi câu trong dòng là một đơn vị phụ đề
        for u in [t] + (re.split(r"(?<=[.!?…;])\s+", t.strip()) if re.search(r"[.!?…;]\s", t) else []):
            w = normalize(u)
            if w:
                out.append(w)
    return out


def duplicates(words, ref):
    """Chữ diegetic (danh sách từ) có trùng dòng phụ đề/tiêu đề ref không."""
    if not words or not ref:
        return False
    t, r = " ".join(words), " ".join(ref)
    if (len(ref) >= 2 or len(r) >= 6) and difflib.SequenceMatcher(None, t, r).ratio() >= DUP_LINE:
        return True
    k = len(words)
    if k >= 2 and k <= len(ref) and k >= 0.5 * len(ref):
        for i in range(len(ref) - k + 1):
            if difflib.SequenceMatcher(None, t, " ".join(ref[i:i + k])).ratio() >= DUP_PART:
                return True
    return False


def _sample(n, els=()):
    step = STEP if n // STEP <= MAX_FRAMES else int(np.ceil(n / MAX_FRAMES))
    idx = list(range(0, n, step))
    if n and idx[-1] != n - 1:
        idx.append(n - 1)
    # mỗi phần tử chữ được đọc ít nhất ở khung giữa khoảng hiện (phần tử ngắn hơn bước lấy mẫu)
    for e in els:
        lo, hi = max(0, e["first_frame"]), min(e["last_frame"], n - 1)
        if hi >= lo:
            idx.append((lo + hi) // 2)
    return sorted(set(idx))


def _zones(els, i, shape, box_h):
    """Vùng nét matte (alpha ≥ 0,02, nới 0,35 × chiều cao hộp) của từng phần tử đang hiện."""
    from .rules_text import active, matte
    k = max(3, int(round(0.35 * box_h)) | 1)
    ker = np.ones((k, k), np.uint8)
    return {e["id"]: (e, cv2.dilate((matte(e, i)[..., 3] >= 0.02).astype(np.uint8), ker).astype(bool))
            for e in active(els, i)}


# ------------------------------------------------------------------ v1.5: mặt nạ nhân vật
def char_sources(parts_dir):
    """{khung: [đường dẫn PNG]} từ <video>.parts/parts.json: mặt nạ bộ phận C3 ('frames') và bóng mọi nhân vật
    ('silhouettes': {khung: PNG}). Trả (nguồn, ghi chú lỗi hoặc None). Không có/không đọc được → {}."""
    if parts_dir is None:
        return {}, None
    pj = Path(parts_dir) / "parts.json"
    if not pj.is_file():
        return {}, None
    try:
        spec = json.loads(pj.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return {}, f"parts.json không phải JSON hợp lệ ({e}): không dùng mặt nạ nhân vật."
    if not isinstance(spec, dict) or spec.get("no_character") is True:
        return {}, None
    src, bad = {}, []
    for key in ("frames", "silhouettes"):
        blk = spec.get(key)
        if blk is None:
            continue
        if not isinstance(blk, dict):
            bad.append(f"'{key}' phải là object {{khung: …}}")
            continue
        for k, v in blk.items():
            vals = list(v.values()) if key == "frames" and isinstance(v, dict) else ([v] if isinstance(v, str) else None)
            if not str(k).isdigit() or not isinstance(vals, list) or not all(isinstance(x, str) for x in vals):
                bad.append(f"{key}['{k}']")
                continue
            for x in vals:
                if (Path(parts_dir) / x).is_file():
                    src.setdefault(int(k), []).append(Path(parts_dir) / x)
                else:
                    bad.append(f"{key}['{k}']: không thấy {x}")
    note = ("Mặt nạ nhân vật sai định dạng (RUN.md 3.6.3), bỏ qua: " + "; ".join(bad[:8])) if bad else None
    return src, note


def char_mask(paths, shape):
    """Hợp các mặt nạ (≥ 128), quy về cỡ khung (INTER_AREA, ≥ 0,5). Tỷ lệ khung khác → None."""
    from .rule_c3 import load_mask
    h, w = shape[:2]
    out = np.zeros((h, w), bool)
    for p in paths:
        m = load_mask(p)
        if abs(m.shape[1] / w - m.shape[0] / h) > 0.005 * m.shape[1] / w:
            return None
        if m.shape != (h, w):
            m = cv2.resize(m.astype(np.float32), (w, h), interpolation=cv2.INTER_AREA) >= 0.5
        out |= m
    return out


def local_fidelity(mask, f, box):
    """Độ khớp biên mặt nạ–cạnh ảnh chỉ trong hộp chữ nới FID_MARGIN px: trung bình cạnh ảnh trên biên mặt nạ chia
    trung vị của 8 lần dịch ±SHIFT px (cùng cách C3.fidelity, không cuộn vòng). Ít hơn FID_BMIN điểm biên → None."""
    from .rule_c3 import SHIFT
    H, W = mask.shape
    x0, y0, x1, y1 = box
    X0, Y0 = max(0, x0 - FID_MARGIN - SHIFT), max(0, y0 - FID_MARGIN - SHIFT)
    X1, Y1 = min(W, x1 + 1 + FID_MARGIN + SHIFT), min(H, y1 + 1 + FID_MARGIN + SHIFT)
    mc = mask[Y0:Y1, X0:X1].astype(np.uint8)
    if min(mc.shape) <= 2 * SHIFT:
        return None
    g = cv2.GaussianBlur(f[Y0:Y1, X0:X1].astype(np.float32), (0, 0), 1.0)
    e = np.max([np.hypot(cv2.Sobel(g[..., c], cv2.CV_32F, 1, 0), cv2.Sobel(g[..., c], cv2.CV_32F, 0, 1))
                for c in range(3)], axis=0)
    b = mc.astype(bool) & ~cv2.erode(mc, np.ones((3, 3), np.uint8)).astype(bool)
    inner = np.zeros_like(b)
    inner[SHIFT:-SHIFT, SHIFT:-SHIFT] = True
    b &= inner
    if b.sum() < FID_BMIN:
        return None
    ys, xs = np.nonzero(b)
    off = [float(e[ys + dy, xs + dx].mean()) for dx, dy in ((SHIFT, 0), (-SHIFT, 0), (0, SHIFT), (0, -SHIFT),
                                                             (SHIFT, SHIFT), (-SHIFT, -SHIFT), (SHIFT, -SHIFT), (-SHIFT, SHIFT))]
    return float(e[b].mean()) / max(float(np.median(off)), 1e-6)


def reread_without(f, mask, box):
    """Xoá phần nhân vật (mặt nạ nới CHAR_GROW px) bằng inpaint Telea trên vùng quanh hộp, đọc lại đúng hộp."""
    x0, y0, x1, y1 = box
    H, W = mask.shape
    pad = 3 * INPAINT_R + CHAR_GROW + 8
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + 1 + pad), min(H, y1 + 1 + pad)
    k = 2 * CHAR_GROW + 1
    m = cv2.dilate(mask[Y0:Y1, X0:X1].astype(np.uint8), np.ones((k, k), np.uint8))
    crop = np.ascontiguousarray(f[Y0:Y1, X0:X1, ::-1])
    g = cv2.inpaint(crop, m, INPAINT_R, cv2.INPAINT_TELEA)[..., ::-1]
    return recognize(np.ascontiguousarray(g), [x0 - X0, y0 - Y0, x1 - X0, y1 - Y0])


def n_chars(s):
    return len(re.sub(r"\s", "", s))


def check_p0(video, profile, text_dir=None, script=None, parts_dir=None):
    from .rule_c3 import FID_MIN
    from .rule_j1 import normalize
    from .rules_text import load_elements
    els = load_elements(text_dir) if text_dir is not None else []
    n = frame_count(video)
    idxs = _sample(n, els)
    frames = read_rgb(video, idxs)
    csrc, cnote = char_sources(parts_dir)
    cmask = {}  # khung → mặt nạ nhân vật cỡ khung (None: khác tỷ lệ) — tính khi cần
    exempt, no_mask = [], []
    unmatted, matted, rejected, solid = [], 0, 0, []
    seen_ids = set()
    read = []  # (khung, id phần tử, diegetic, chữ đọc được)
    for i in idxs:
        f = frames.get(i)
        if f is None:
            continue
        for d in detect(f, min_score=MIN_DET):
            s, conf = recognize(f, d["box"])
            if not is_latin_text(s, conf, MIN_REC):
                rejected += 1
                continue
            sol = solidity(f, d["box"])
            if sol is not None and sol >= SOLID_MAX:
                solid.append(dict(khung=i, hop=d["box"], chu=s[:40], do_tin=round(conf, 2), do_dac=round(sol, 2)))
                continue
            x0, y0, x1, y1 = d["box"]
            cover = 0.0
            if els:
                zs = _zones(els, i, f.shape, y1 - y0)
                if zs:
                    union = np.any([z for _, z in zs.values()], axis=0)
                    cover = float(union[y0:y1 + 1, x0:x1 + 1].mean())
            if cover >= MIN_COVER:
                matted += 1
                seen_ids.update(zs)
                per = {eid: float(z[y0:y1 + 1, x0:x1 + 1].mean()) for eid, (_, z) in zs.items()}
                best = max(per, key=per.get)
                read.append((i, best, is_diegetic(zs[best][0]), s))
            else:
                row = dict(khung=i, hop=d["box"], chu=s[:80], do_tin=round(conf, 2), phu_matte=round(cover, 2))
                if n_chars(s) <= MAX_CHARS:  # v1.5: chữ ngắn — xét có phải nhân vật bị đọc thành chữ
                    if i not in csrc:
                        no_mask.append(row)
                    else:
                        if i not in cmask:
                            cmask[i] = char_mask(csrc[i], f.shape)
                        cm = cmask[i]
                        fid = local_fidelity(cm, f, d["box"]) if cm is not None else None
                        k = 2 * CHAR_GROW + 1
                        touch = cm is not None and bool(cv2.dilate(cm[y0:y1 + 1, x0:x1 + 1].astype(np.uint8),
                                                                    np.ones((k, k), np.uint8)).any())
                        row.update(phu_nhan_vat=round(float(cm[y0:y1 + 1, x0:x1 + 1].mean()), 3) if cm is not None else None,
                                   do_khop_bien_cuc_bo=None if fid is None else round(fid, 2))
                        if cm is None:
                            row["ly_do_khong_mien"] = "mặt nạ nhân vật khác tỷ lệ khung"
                        elif not touch:
                            row["ly_do_khong_mien"] = "hộp chữ không chạm mặt nạ nhân vật"
                        elif fid is None or fid < FID_MIN:
                            row["ly_do_khong_mien"] = (f"mặt nạ nhân vật quanh hộp chữ không khớp cạnh ảnh (độ khớp biên "
                                                       f"cục bộ < {FID_MIN:g} hoặc < {FID_BMIN} điểm biên)")
                        else:
                            s2, c2 = reread_without(f, cm, d["box"])
                            row.update(doc_lai=s2[:40], do_tin_doc_lai=round(c2, 2))
                            if is_latin_text(s2, c2, MIN_REC):
                                row["ly_do_khong_mien"] = "xoá nhân vật rồi vẫn đọc ra chữ"
                            else:
                                exempt.append(row)
                                continue
                unmatted.append(row)
    unseen = sorted({e["id"] for e in els} - seen_ids)
    # chống lạm dụng nhãn diegetic: chữ trong matte diegetic trùng phụ đề/tiêu đề
    refs = [("thoại/phụ đề (script)", w) for w in script_lines(script)]
    refs += [(f"chữ đọc trong phần tử '{eid}'", normalize(t)) for _, eid, dg, t in read if not dg]
    refs += [(f"'text' khai của '{e['id']}'", normalize(e["text"])) for e in els
             if not is_diegetic(e) and isinstance(e.get("text"), str)]
    abuse = []
    for i, eid, dg, t in read:
        if not dg:
            continue
        w = normalize(t)
        hit = next((src for src, r in refs if duplicates(w, r)), None)
        if hit:
            abuse.append(dict(khung=i, phan_tu=eid, chu=t[:80], trung_voi=hit))
    dieg = sorted({e["id"] for e in els if is_diegetic(e)})
    ms = [metric("vùng chữ dò được không có matte", len(unmatted), "<=", 0, "vùng·khung"),
          metric("chữ gắn diegetic trùng phụ đề/tiêu đề", len(abuse), "<=", 0, "vùng·khung")]
    notes = [f"Lấy mẫu {len(idxs)} khung (≈ 2 khung/giây). Vùng máy dò nghi là chữ nhưng nhận dạng "
             f"không xác nhận chữ Latin (cửa sổ, lưới, hoa văn): {rejected} (bỏ qua)."]
    if solid:
        notes.append(f"Vùng đọc ra chữ nhưng là khối đặc (độ đặc ≥ {SOLID_MAX}, cửa sổ/lưới), bị loại: {len(solid)} "
                     "(liệt kê trong bằng chứng để người duyệt soi).")
    if not els:
        notes.append("Không có matte chữ (thiếu <video>.text/ hoặc elements rỗng): mọi chữ dò được đều trượt.")
    if exempt:
        notes.append(f"v1.5: {len(exempt)} vùng đọc ra chuỗi ≤ {MAX_CHARS} ký tự nằm trên nhân vật (xoá nhân vật thì máy "
                     "không còn đọc ra chữ; mặt nạ khớp cạnh ảnh) được miễn: "
                     + "; ".join(f"khung {r['khung']} '{r['chu']}'" for r in exempt[:12])
                     + ". Liệt kê trong bằng chứng 'vung_nhan_vat_mien' để người duyệt soi.")
    if no_mask:
        notes.append(f"v1.5: {len(no_mask)} vùng chữ ngắn (≤ {MAX_CHARS} ký tự) không có matte, ở khung không có mặt nạ "
                     "nhân vật: " + ", ".join(str(r["khung"]) for r in no_mask[:20]) + ". Nếu đó là nhân vật, xuất "
                     "'silhouettes' cho đúng các khung này (RUN.md 3.6.3) rồi chạy lại; nếu là chữ thật, thêm matte.")
    if cnote:
        notes.append(cnote)
    if dieg:
        notes.append(f"Phần tử diegetic (miễn G4, vẫn phải có matte và qua P1): {', '.join(dieg)}. "
                     f"Đã đọc {sum(1 for r in read if r[2])} vùng chữ trong matte diegetic; so với "
                     f"{len(refs)} dòng phụ đề/tiêu đề tham chiếu"
                     + ("" if script is not None else " (không có <video>.script.txt: chỉ so với chữ không diegetic)")
                     + ".")
    if abuse:
        notes.append("Chữ gắn nhãn diegetic nhưng trùng nội dung phụ đề/tiêu đề: nhãn diegetic không được dùng "
                     "để né G4. Bỏ nhãn hoặc khiếu nại vào checks-appeal.md nếu đây thật là chữ trong thế giới phim.")
    if unseen:
        notes.append("Phần tử có matte nhưng máy dò không thấy ở khung mẫu nào (tham khảo, không trượt): "
                     + ", ".join(unseen))
    return result("P0", None, ms, notes,
                  evidence=dict(chu_khong_matte=unmatted[:60], vung_co_matte=matted,
                                vung_bi_loai=rejected, vung_khoi_dac=solid[:60], khung_lay_mau=len(idxs),
                                ds_khung_lay_mau=idxs, vung_nhan_vat_mien=exempt[:60],
                                chu_ngan_khong_mat_na=no_mask[:60], khung_co_mat_na_nhan_vat=len(csrc),
                                phan_tu_may_do_khong_thay=unseen, diegetic_trung_phu_de=abuse[:60],
                                chu_doc_trong_matte=[dict(khung=i, phan_tu=e, diegetic=g, chu=t[:80])
                                                     for i, e, g, t in read[:120]]))
