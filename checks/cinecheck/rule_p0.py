"""P0 — máy dò chữ độc lập trên khung render. Không dựa vào matte: chữ dò được mà không có matte
tương ứng trong <video>.text/ thì trượt (vá giới hạn 2 của v0: P1/G4 chỉ thấy chữ có matte).

v1.1 (Q-P0): phần tử có "diegetic": true (chữ trong thế giới phim: biển hiệu, tên phố) vẫn phải có
matte (P0) và qua P1, nhưng được miễn G4. Chống lạm dụng: chữ máy đọc được trong matte của phần tử
diegetic mà trùng nội dung phụ đề/tiêu đề (dòng thoại trong <video>.script.txt, chữ đọc được trong
matte của phần tử không diegetic, trường "text" khai cho phần tử không diegetic) thì trượt.
"""
import difflib
import re

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


def check_p0(video, profile, text_dir=None, script=None):
    from .rule_j1 import normalize
    from .rules_text import load_elements
    els = load_elements(text_dir) if text_dir is not None else []
    n = frame_count(video)
    idxs = _sample(n, els)
    frames = read_rgb(video, idxs)
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
                unmatted.append(dict(khung=i, hop=d["box"], chu=s[:80], do_tin=round(conf, 2),
                                     phu_matte=round(cover, 2)))
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
                                phan_tu_may_do_khong_thay=unseen, diegetic_trung_phu_de=abuse[:60],
                                chu_doc_trong_matte=[dict(khung=i, phan_tu=e, diegetic=g, chu=t[:80])
                                                     for i, e, g, t in read[:120]]))
