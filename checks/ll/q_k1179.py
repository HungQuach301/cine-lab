#!/opt/cine/bin/python
"""Luật 1.17.9 (phiên K-1.17.9, 26/10/2026) — khiếu nại BAN-CUOI-T4-A KN-1, KN-2, KN-4, KN-5, KN-6, KN-7 (KN-3 đã rút) + KN-8 (điều phối).
CHỈ tập kênh 2 từ T4 (`kenh2_tu_t4: true` hoặc khối `n2p:`). Mỗi luật: tham số theo tấm/đoạn, MẶC ĐỊNH GIỮ HÀNH VI 1.17.8 khi không khai.
Căn cứ (Asia/Saigon): chủ dự án 26/10/2026 07:39 chọn hướng (a) cho H3-05b (→ KN-7); lệnh K-1.17.9 = "Duyệt PHIẾU-A theo khuyến nghị điều phối";
26/10 00:07 "A+B+E" (LUẬT E: "toà THÁP có tên ghép lại từ 3D"); 25/10 09:08 "…các vấn đề khác đều có thể nới…". Phán quyết: checks-appeal.md
"Phán quyết K — checks 1.17.9"; số đo: reports/k1179/.

KN-1 · ngoại lệ "bờ" của MÔ HÌNH trên tấm E (hướng K1178-D2, phương án A có khuôn máy đọc được) — tấm E khai
  `ngoai_le: [{hang: ["N2P-1 (b)", "N2P-3 (b)"], hop: [x0, y0, x1, y1] (chuẩn hoá 0–1), ly_do: "<…>",
               duyet_chu_du_an: {nguoi_ky, vai: chu_du_an, ngay: YYYY-MM-DD, ket_luan: chap_nhan}}]` (không email).
  Một báo của mô hình (N2P-1 (b) / N2P-3 (b)) được hạ xuống (w) Cảnh báo khi ĐỦ: (1) duyệt hợp lệ (q_k1178.ngoai_le_duyet); (2) tâm hộp mô hình nằm trong
  `hop` khai (nở 0,01); (3) phần hộp nằm trong lõi (a)-E (= (a)-E trừ dải bờ ±8 px: toà có tên, cầu, nước…) ≤ 25 % — hộp chủ yếu
  ở lớp AI được phép (lõi đã được máy khoá 0/255; đáp án KN-1: hộp GPT 6,3 % trong lõi = mẩu kè 'nha' 307 điểm); (4) MÁY của tấm sạch: N2P-1 (a) 0/255, T9c 0 đoạn
  bờ lấn và giữa nước ≤ 2 % (T9b đất→nước của tấm E chỉ in từ 1.17.8 — giữ). Thiếu một điều kiện → báo giữ Chặn + lý do không nhận.
  Máy (N2P-1 (a), T9b, T9c) KHÔNG bao giờ được miễn.
KN-2 · Q37 / NHIP-K2 / Q37 (1.13) từ T4: biến cố ĐO từ LOG MÁY (`log_may` khai trong log shot; không khai beats) cộng vào (b)(c) như I8 (1.15) của T3:
  (n1) mặt trời qua chân trời hoặc hoàng hôn dân sự (sun_el đổi dấu qua 0° / −6°); (n2) đổi pha máy ĐỨNG ↔ CHẠY (tốc độ máy — dịch vị trí / khoảng cách
  nhìn + góc quay hướng nhìn mỗi khung — qua 10 % đỉnh của shot). Không nhận: năm nhảy số (đồng hồ chạy — I8 cũng không nhận), `fire` (đơn vị log chưa
  hiệu chuẩn thấy được), beats tự khai `bien_co_tl` (A4 1.17.7 giữ). BIEN-CO-V T4 vẫn chưa hiệu chuẩn (K1178-D4) — hiệu chuẩn lại trên master 1080p.
KN-4 · NHAN-VAT-TEN đọc `cat_clip` của đoạn: [k0, k1] (khung, gồm hai đầu, 0 = khung đầu clip) hoặc {t0, t1} (giây trong clip) → chỉ đo mặt trong cửa sổ
  dùng. Cửa sổ dài khác thời lượng đoạn > 1 khung → (k). Không khai → cả clip (như 1.17.8).
KN-5 · LUẬT E "toà có tên" (bắt buộc ghép lại từ 3D; mọi toà OSM có tên KHÁC = nhà thường, AI vẽ lại được): (i) toà có tên OSM đỉnh ≥ 75 m ODN
  (`loai: thap`, `dinh_odn_m` hoặc `y1_m`); (ii) công trình lịch sử có tên (`loai: lich_su` + `nguon_lich_su` không rỗng — NHLE/Historic England, sách…; trường `nguon` của
  toa.json phía dựng là nguồn MẶT NẠ, không thay được);
  (iii) mái vòm/nhà thờ St Paul's (`loai: mai_vom` hoặc tên chứa "St Paul"). Mục `toa_co_ten` khai `loai` sai định nghĩa → (k) Chặn ở G2; không khai
  `loai` → hành vi 1.17.8 (mọi mục coi là toà có tên; chỉ in số mục chưa khai ở giá trị hàng).
KN-6 · đẩy/trượt 2D trên tấm E: mục `n2p.video[]` (n2p_toan_khung_hien_dai) khai `day_2d: {kieu: day | truot, toc_do_pct_s}` — đo trên video ghép:
  phép đồng dạng (ORB + RANSAC) khung 0 → khung t; tốc độ = hệ số góc (bình phương nhỏ nhất qua gốc) của max(|tỉ lệ − 1|, dịch tâm khung / chiều rộng) theo giây ≤ 1,5 %/s; cả khung một phép 2D:
  sai khác sau bù trong (a)-E (mặt nạ đã biến đổi) ≤ max(3,0/255, 2 × ngoài (a)-E) — lớp (a)-E dựng 3D có thị sai/khác quỹ đạo → (h).
  Cấp: (h) Chặn ở G2 · Cảnh báo animatic. Máy 3D của shot vẫn CODINH (MAY-19 (b) đo log máy như cũ).
KN-7 · NHAN-VAT-TEN (k): nhân vật có tên KHÔNG có chân dung xác thực/sạch quyền — miễn `chan_dung_tham_chieu` khi ĐỦ: `chan_dung: khong_co`;
  `chan_dung_nguon_da_tra.noi` ≥ 1 mục; YuNet (máy K, cùng thước NHAN-VAT-TEN) đo được và MỌI hộp điểm ≥ 0,60 cao ≤ 1/8 (chặt hơn (a): không có
  chân dung thì không nhận cả hộp mức (w)); `duyet_chu_du_an` có dòng AUTHORSHIP.md cùng ngày (YYYY-MM-DD) + giờ (HH:MM) + mã shot. (a) cận mặt vẫn Chặn.
KN-8 · LUẬT E nước AI (`nuoc_ai: true` trên tấm E): (a)-E bỏ MỌI điểm nước của mặt nạ — dải bờ ±8 px chỉ giữ PHÍA ĐẤT, cầu/kè/tường (nha 235), tàu…
  vẫn = render; mặt nước lấy từ ảnh AI. Kiểm thêm (n): mô hình báo THÊM cầu/công trình/tàu/thuyền/vật nổi có tâm hộp trên nước → N2P-1 (b) Chặn;
  máy T9c (đối chứng render) trên tấm nuoc_ai CHỈ IN — ghép thử K-1.17.9: T9c báo 7 đoạn bờ lấn tới 70 px trên tấm sạch và không tách được 3 ca âm
  tổng hợp (reports/k1179 §KN-8) → không dùng làm thước Chặn; mỗi tấm nuoc_ai phải có `duyet_chu_du_an` (tờ so người soi) — thiếu → (u) THIẾU.
"""
import json, math, os, re

DAY_MAX, DAY_SAI = 1.5, 0.02                          # KN-6: §19 (c) ảnh thật (cập nhật 25/10 mục (3)) ≤ 1,5 %/s; sai số đo 2 % (ca 1,5 %/s tổng hợp đo 1,505)
DAY_DU_SAN, DAY_DU_K = 3.0, 2.0                       # KN-6: sai khác sau bù trong (a)-E ≤ max(3,0/255, 2 × ngoài) — chọn trên ca tổng hợp từ tấm P9 thật (reports/k1179/do/kn6-day2d.json)
THAP_ODN_M = 75.0                                     # KN-5: tháp = đỉnh ≥ 75 m ODN (phiên A đề xuất; ngưỡng OSM/LiDAR của mặt nạ "tháp")
LOG_PHA = 0.10                                        # KN-2 (n2): ĐỨNG < 10 % tốc độ đỉnh của shot
SUN_MOC = (0.0, -6.0)                                 # KN-2 (n1)
MAT_TRAN = 1.0 / 8.0
LOI_MAX = 0.25                                        # KN-1 (3): phần hộp mô hình trong lõi (a)-E ≤ 25 % (lõi đã được máy khoá 0/255)
LOAI_NUOC = {'cong_trinh', 'tau_lon', 'thuyen_nho', 'khac', 'do_dac'}   # KN-8 (n): vật THÊM trên mặt nước AI


def ap_1179(E): return bool((E or {}).get('kenh2_tu_t4') or (E or {}).get('n2p'))


def _num(x): return isinstance(x, (int, float)) and not isinstance(x, bool)


# ================================================================ KN-1 ngoại lệ mô hình trên tấm E
def ngoai_le_e(t):
    """→ ([mục hợp lệ {hang, hop, ly_do}], [lý do mục không nhận])"""
    from checks.ll import q_k1178 as K78
    ok, bad = [], []
    for i, x in enumerate((t or {}).get('ngoai_le') or []):
        if not isinstance(x, dict): bad.append(f'ngoai_le[{i}] không phải dict'); continue
        d, why = K78.ngoai_le_duyet({'ngoai_le_duyet': x.get('duyet_chu_du_an')})
        hop = x.get('hop'); hang = [str(h) for h in x.get('hang') or []]
        p = ([] if d else [f'duyet_chu_du_an: {why}']) + ([] if isinstance(hop, list) and len(hop) == 4 and all(_num(v) for v in hop) else ['thiếu `hop` [x0, y0, x1, y1]'])
        p += [] if hang and all(h in ('N2P-1 (b)', 'N2P-3 (b)') for h in hang) else ['`hang` chỉ nhận "N2P-1 (b)", "N2P-3 (b)" (máy không miễn)']
        p += [] if str(x.get('ly_do') or '').strip() else ['thiếu `ly_do`']
        (bad.append(f"ngoai_le[{i}]: {'; '.join(p)}") if p else ok.append(dict(hang=hang, hop=[float(v) for v in hop], ly_do=str(x['ly_do']).strip())))
    return ok, bad


def may_sach(k):
    """KN-1 (4): máy của tấm sạch → (bool, mô tả)"""
    i, iii = k['do']['i'], k['do']['iii']; c9 = iii.get('t9c') or {}
    p = []
    if i['max_trong_a'] > 0: p.append(f"N2P-1 (a) {i['max_trong_a']}/255")
    if c9.get('ap') is not False and (c9.get('so_doan_lan') or c9.get('giua_pct', 0) > 2.0): p.append(f"T9c {c9.get('so_doan_lan')} đoạn bờ lấn, giữa nước {c9.get('giua_pct')} %")
    return (not p), ', '.join(p) or 'máy sạch (N2P-1 (a) 0/255, T9c 0)'


def loi_a_e(D, s):
    """lõi (a)-E = (a)-E trừ dải bờ ±8 px quanh nước"""
    import cv2, numpy as np
    A = D['_A']; L, names = D.get('_L'), D.get('_names')
    if L is None or 'nuoc' not in (names or []): return A
    kb = 2 * max(1, int(round(8 * s))) + 1
    bo = cv2.dilate((cv2.morphologyEx((L == names.index('nuoc')).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0).astype(np.uint8), np.ones((kb, kb), np.uint8)) > 0
    return A & ~bo


def ty_loi(b, M):
    """phần diện tích hộp chuẩn hoá b nằm trong mặt nạ M"""
    H, W = M.shape; x0, y0, x1, y1 = [int(round(v * q)) for v, q in zip(b, (W, H, W, H))]
    x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(W, max(x1, x0 + 1)), min(H, max(y1, y0 + 1))
    return float(M[y0:y1, x0:x1].mean())


def ap_ngoai_le(k, t):
    """KN-1: chuyển báo mô hình N2P-1 (b) (k['L1']) / N2P-3 (b) (k['VUNG']) đủ điều kiện sang k['NL_W'] (Cảnh báo); ghi k['NL_GHI']"""
    from checks.ll import q_n2p as N
    NL, bad = ngoai_le_e(t)
    k['NL_W'], k['NL_GHI'] = [], [f'(w) tấm {k["id"]}: {b} — không nhận' for b in bad]
    if k.get('E') is None: return k
    if not NL: k['E'].setdefault('w', []).extend(k['NL_GHI']); return k
    sach, mt = may_sach(k)
    if not sach:
        k['NL_GHI'].append(f'(w) tấm {k["id"]}: ngoai_le không áp — {mt} (máy phải sạch)'); k['E'].setdefault('w', []).extend(k['NL_GHI']); return k
    LOI = k.get('_LOI'); nho = lambda b, h: h[0] - 0.01 <= (b[0] + b[2]) / 2 <= h[2] + 0.01 and h[1] - 0.01 <= (b[1] + b[3]) / 2 <= h[3] + 0.01
    for key, hang in (('L1', 'N2P-1 (b)'), ('VUNG', 'N2P-3 (b)')):
        giu = []
        for x in k.get(key) or []:
            b = x.get('toa_do') if isinstance(x.get('toa_do'), list) and len(x.get('toa_do')) == 4 else None
            m = next((n for n in NL if hang in n['hang'] and b and nho(b, n['hop'])), None)
            cham = bool(b is not None and LOI is not None and ty_loi(b, LOI) > LOI_MAX)
            if m and not cham: k['NL_W'].append(dict(x, hang=hang, ly_do=m['ly_do'])); continue
            if m and cham: k['NL_GHI'].append(f'(w) tấm {k["id"]}: {hang} «{str(x.get("mo_ta") or "")[:50]}» hộp nằm {100 * ty_loi(b, LOI):.1f} % trong lõi (a)-E > {100 * LOI_MAX:g} % — ngoại lệ không nhận')
            giu.append(x)
        k[key] = giu
    w = f'tấm {k["id"]}'
    k['E'].setdefault('w', [])
    k['E']['w'] += [f"(w) {w}: {x['hang']} của mô hình hạ Cảnh báo — ngoại lệ chủ dự án duyệt (KN-1) «{str(x.get('mo_ta') or '')[:60]}» @{[round(v, 3) for v in x['toa_do']]}; {x['ly_do'][:60]}; {mt}"
                    for x in k['NL_W']] + k['NL_GHI']
    return k


# ================================================================ KN-2 biến cố đo từ log máy
def _ld(base, p):
    q = p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))
    return json.load(open(q)) if os.path.exists(q) else None


def bien_co_log(E, LS, ep_dir='.'):
    """→ [(t tuyệt đối, shot, 'log:n1'|'log:n2', mô tả)] cho Q37 (b)(c) — chỉ tập từ T4; shot có `log_may`, t0, dur"""
    if not ap_1179(E) or not LS: return []
    out = []
    for s in LS:
        p = s.get('log_may')
        if not p or not _num(s.get('t0')) or not _num(s.get('dur')): continue
        try: Lm = _ld(ep_dir, p)
        except (OSError, ValueError): Lm = None
        if not Lm or not isinstance(Lm.get('frames'), list): continue
        fps = float((Lm.get('shot') or {}).get('fps') or 24); F = Lm['frames'][:int(round(float(s['dur']) * fps))]; t0 = float(s['t0']); sid = str(s.get('shot'))
        for a, b in zip(F, F[1:]):
            for z in SUN_MOC:
                if _num(a.get('sun_el')) and _num(b.get('sun_el')) and (a['sun_el'] - z) * (b['sun_el'] - z) < 0:
                    out.append((round(t0 + b['f'] / fps, 3), sid, 'log:n1', f'mặt trời qua {z:g}°'))
        sp = []
        for a, b in zip(F, F[1:]):
            try:
                pa, pb, la, lb = a['cam']['p'], b['cam']['p'], a['cam']['l'], b['cam']['l']
                d = max(1.0, math.dist(pa, la)); u = [x - y for x, y in zip(la, pa)]; v = [x - y for x, y in zip(lb, pb)]
                c = sum(x * y for x, y in zip(u, v)) / (math.hypot(*u) * math.hypot(*v) + 1e-9)
                sp.append(math.dist(pa, pb) / d + math.acos(max(-1.0, min(1.0, c))))
            except (KeyError, TypeError, ValueError): sp.append(None)
        if sp and all(x is not None for x in sp) and max(sp) > 0:
            th = LOG_PHA * max(sp); st = [x >= th for x in sp]
            for i in range(1, len(st)):
                if st[i] != st[i - 1]: out.append((round(t0 + (i + 1) / fps, 3), sid, 'log:n2', 'máy chạy' if st[i] else 'máy dừng'))
    return sorted(set(out))


# ================================================================ KN-4 cat_clip
def cua_so(m, fps, dur=None):
    """`cat_clip` → ((t0, t1) giây trong clip | None, lỗi (k) | None)"""
    c = (m or {}).get('cat_clip')
    if c is None: return None, None
    if isinstance(c, (list, tuple)) and len(c) == 2 and all(_num(v) for v in c) and c[1] >= c[0] >= 0: a, b = c[0] / fps, (c[1] + 1) / fps; kieu = f'khung {c[0]}–{c[1]}'
    elif isinstance(c, dict) and _num(c.get('t0')) and _num(c.get('t1')) and c['t1'] > c['t0'] >= 0: a, b = float(c['t0']), float(c['t1']); kieu = f"{a:g}–{b:g} s"
    else: return None, f'`cat_clip` {c!r} không đúng khuôn [k0, k1] (khung) hoặc {{t0, t1}} (giây)'
    if dur is not None and abs((b - a) - float(dur)) > 1.0 / fps + 1e-6:
        return (a, b), f'`cat_clip` {kieu} dài {b - a:.3f} s ≠ thời lượng đoạn {float(dur):.3f} s (> 1 khung)'
    return (a, b), None


# ================================================================ KN-5 toà có tên
def la_toa_co_ten(x):
    """mục toa_co_ten → (loại, lỗi (k) | None, ghi (w) | None)"""
    ten = str(x.get('ten') or ''); lo = x.get('loai')
    if lo is None: return None, None, f'(w) toà {ten}: chưa khai `loai` (thap | lich_su | mai_vom — 1.17.9 KN-5); coi là toà có tên như 1.17.8'
    if lo == 'mai_vom' or (lo == 'lich_su' and "st paul" in ten.lower()): return lo, None, None
    if lo == 'thap':
        h = x.get('dinh_odn_m', x.get('y1_m'))
        if not _num(h): return lo, f'(k) KN-5 toà {ten}: loai thap nhưng thiếu `dinh_odn_m` (đỉnh m ODN)', None
        if float(h) < THAP_ODN_M: return lo, f'(k) KN-5 toà {ten}: đỉnh {float(h):.1f} m ODN < {THAP_ODN_M:g} m — không phải tháp: xếp nhà thường (AI vẽ lại) hoặc khai lich_su có nguồn', None
        return lo, None, None
    if lo == 'lich_su':
        if not str(x.get('nguon_lich_su') or '').strip(): return lo, f'(k) KN-5 toà {ten}: loai lich_su thiếu `nguon_lich_su` (danh mục NHLE/Historic England, sách…)', None
        return lo, None, None
    return lo, f'(k) KN-5 toà {ten}: loai {lo!r} ngoài thap | lich_su | mai_vom', None


def kiem_toa(toa):
    """→ (lỗi (k) KN-5, số toà chưa khai `loai` — chỉ in ở giá trị, không thành Cảnh báo: không khai → hành vi 1.17.8)"""
    loi, n = [], 0
    for x in toa or []:
        if not isinstance(x, dict): continue
        _, e, g = la_toa_co_ten(x)
        if e: loi.append(e)
        if g: n += 1
    return loi, n


# ================================================================ KN-6 đẩy/trượt 2D trên tấm E
def _sim(a, b):
    """phép đồng dạng a → b (ORB + RANSAC) → ma trận 2×3 | None"""
    import cv2, numpy as np
    o = cv2.ORB_create(3000); g1, g2 = (cv2.cvtColor(x, cv2.COLOR_BGR2GRAY) for x in (a, b))
    k1, d1 = o.detectAndCompute(g1, None); k2, d2 = o.detectAndCompute(g2, None)
    if d1 is None or d2 is None: return None
    m = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d1, d2), key=lambda z: z.distance)[:1500]
    if len(m) < 20: return None
    P1 = np.float32([k1[x.queryIdx].pt for x in m]); P2 = np.float32([k2[x.trainIdx].pt for x in m])
    M, _ = cv2.estimateAffinePartial2D(P1, P2, method=cv2.RANSAC, ransacReprojThreshold=1.5, maxIters=5000)
    return M


def do_day_2d(ghep_mp4, mat_na_png=None, lop_a=None, bang=None, buoc=6):
    """→ dict(toc_do_pct_s, du_a, du_ngoai, khung[]) — đo trên video ghép (KN-6)"""
    import cv2, numpy as np
    from checks.ll import q_n2p as N
    cap = cv2.VideoCapture(ghep_mp4); fps = cap.get(cv2.CAP_PROP_FPS) or 24.0; F = []; i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        if i % buoc == 0: F.append((i, f))
        i += 1
    if len(F) < 2: return dict(loi='video < 2 khung đo')
    f0 = F[0][1]; H, W = f0.shape[:2]
    A = None
    if mat_na_png:
        L, names = N.idmap(mat_na_png, (W, H), bang); A = N.lop(L, names, lop_a or N.LOP_A)
    C = np.float32([[0, 0], [W, 0], [0, H], [W, H]]); out, tocs, dus = [], [], []
    for j, f in F[1:]:
        M = _sim(f0, f)
        if M is None: out.append(dict(khung=j, loi='không khớp được')); continue
        t = j / fps; sc = float(np.hypot(M[0, 0], M[1, 0])); c = np.float32([W / 2, H / 2]); c2 = M[:, :2] @ c + M[:, 2]
        z, pn = abs(sc - 1) * 100, float(np.linalg.norm(c2 - c)) / W * 100; toc = max(z, pn) / t   # %: phóng (tỉ lệ) | trượt (tâm khung / chiều rộng)
        Wp = cv2.warpAffine(f0, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        val = cv2.warpAffine(np.ones((H, W), np.uint8), M, (W, H), flags=cv2.INTER_NEAREST) > 0
        val = cv2.erode(val.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        d = np.abs(Wp.astype(np.int16) - f.astype(np.int16)).mean(-1)
        if A is not None:
            Aw = cv2.warpAffine(A.astype(np.uint8), M, (W, H), flags=cv2.INTER_NEAREST) > 0
            ia, io = val & Aw, val & ~Aw
            da = float(d[ia].mean()) if ia.any() else 0.0; dn = float(d[io].mean()) if io.any() else 0.0
        else: da, dn = 0.0, float(d[val].mean())
        out.append(dict(khung=j, toc_do_pct_s=round(toc, 3), du_a=round(da, 2), du_ngoai=round(dn, 2))); tocs.append((t, z, pn)); dus.append((da, dn))
    if not tocs: return dict(loi='không khung nào khớp được', khung=out)
    da, dn = max(dus, key=lambda z: z[0] - DAY_DU_K * z[1])
    tt = sum(t * t for t, _, _ in tocs); toc = max(sum(t * z for t, z, _ in tocs), sum(t * p for t, _, p in tocs)) / tt   # hệ số góc bình phương nhỏ nhất qua gốc
    return dict(toc_do_pct_s=round(toc, 3), du_a=round(da, 2), du_ngoai=round(dn, 2), khung=out, fps=fps)


def kiem_day_2d(v, ep_dir='.', lop_a=None, bang=None):
    """mục n2p.video khai day_2d → (lỗi (h)[], thiếu[], giá trị)"""
    from checks.ll import q_n2p as N
    dd = v.get('day_2d')
    if not dd: return [], [], None
    w = f"video {v.get('shot')}"
    if not isinstance(dd, dict) or dd.get('kieu') not in ('day', 'truot'): return [f"(h) {w}: `day_2d` cần {{kieu: day | truot, toc_do_pct_s}}"], [], None
    g = N._p(ep_dir, v.get('ghep'))
    if not g or not os.path.exists(g): return [], [f'(h) {w}: không có video ghép để đo đẩy/trượt 2D'], None
    R = do_day_2d(g, N._p(ep_dir, v.get('mat_na')), lop_a, bang)
    if R.get('loi'): return [], [f"(h) {w}: {R['loi']}"], R
    loi = []
    if R['toc_do_pct_s'] > DAY_MAX * (1 + DAY_SAI): loi.append(f"(h) {w}: đẩy/trượt 2D {R['toc_do_pct_s']:.2f} %/s > {DAY_MAX:g} %/s")
    tran = max(DAY_DU_SAN, DAY_DU_K * R['du_ngoai'])
    if R['du_a'] > tran: loi.append(f"(h) {w}: lớp (a)-E không theo cùng phép 2D của cả khung — sai sau bù {R['du_a']:.2f}/255 > {tran:.2f} (ngoài {R['du_ngoai']:.2f}) — thị sai/khác quỹ đạo 3D")
    return loi, [], R


# ================================================================ KN-7 miễn (k) khi không có chân dung
def mien_k(m_get, sid, ep_dir, R):
    """m_get(k) đọc trường đoạn; R = kết quả đo mặt (do_mat) | None → (True, mô tả) | (False, lý do không miễn)"""
    from checks.ll import q_k117 as K7
    if str(m_get('chan_dung') or '') != 'khong_co': return False, 'không khai `chan_dung: khong_co`'
    ng = m_get('chan_dung_nguon_da_tra'); noi = (ng or {}).get('noi') if isinstance(ng, dict) else None
    if not isinstance(noi, list) or not [x for x in noi if str(x).strip()]: return False, '`chan_dung_nguon_da_tra.noi` rỗng (ghi nơi đã tra)'
    if R is None: return False, 'chưa đo được mặt YuNet (clip/master)'
    mx = max([R.get('max_ty') or 0] + [x[1] for x in R.get('nghi') or []])
    if mx > MAT_TRAN: return False, f'YuNet mặt lớn nhất {mx:.3f} > 1/8 (kể cả hộp điểm 0,60–0,75)'
    dy = str(m_get('duyet_chu_du_an') or '')
    mm = re.search(r'(\d{4}-\d{2}-\d{2})\D{1,3}(\d{1,2}:\d{2})', dy)
    if not mm: return False, '`duyet_chu_du_an` không nêu dòng AUTHORSHIP dạng "YYYY-MM-DD HH:MM"'
    A = K7._authorship(ep_dir)
    if A is None: return False, 'không tìm thấy AUTHORSHIP.md'
    if not [l for l in A.splitlines() if mm.group(1) in l and mm.group(2) in l and re.search(r'(?<![\w.])' + re.escape(sid) + r'(?![\w])', l)]:
        return False, f'AUTHORSHIP.md không có dòng {mm.group(1)} {mm.group(2)} nêu {sid}'
    return True, f"miễn (k) KN-7: không có chân dung ({len(noi)} nơi đã tra), YuNet ≤ {mx:.3f} ≤ 1/8, AUTHORSHIP {mm.group(1)} {mm.group(2)}"


# ================================================================ KN-8 nước AI
def nuoc_ai(t): return bool((t or {}).get('nuoc_ai'))


PROMPT_VER_NUOC = 'n2p-e-v2-nuoc (K-1.17.9, 26/10/2026)'   # đề bài E cho tấm nước AI: mặt nước KHÔNG còn là phần được bảo vệ (lượt đầu GPT báo "sông bảo vệ bị đổi")
_E_CU = ("After the AI step our own 3D render was composited back for these PROTECTED features: the\nriver and its banks, the named landmarks listed below, "
         "bridges, boats and any fire.")
_E_NUOC = ("After the AI step our own 3D render was composited back for these PROTECTED features: the\nriver BANKS (the land edge of the embankments), the named "
           "landmarks listed below, bridges, boats and any fire. The WATER SURFACE of the river\nwas repainted by the AI and is ALLOWED to look different (colour, "
           "ripples, reflections, haze) — do NOT report the water surface itself as changed. DO report every bridge,\npier, boat, ship, barge, floating object or "
           "patch of land that appears ON THE WATER in AFTER but not in BEFORE, and any place where the shoreline moved.")


def de_bai_nuoc(pr):
    """đề bài E (q_k1178.PROMPT_E đã điền) → bản cho tấm nuoc_ai (chỉ thay câu phần được bảo vệ)"""
    assert _E_CU in pr, 'PROMPT_E đổi — cập nhật _E_CU'
    return pr.replace(_E_CU, _E_NUOC)


def bo_nuoc_khoi_a(A, L, names):
    """(a)-E bỏ mọi điểm nước của mặt nạ (dải bờ chỉ còn phía đất)"""
    return A & ~(L == names.index('nuoc')) if 'nuoc' in names else A


def vat_tren_nuoc(V, L, names):
    """mô hình: vật THÊM (cầu/công trình/tàu/thuyền/vật nổi) có tâm hộp trên mặt nước → [mục]"""
    if 'nuoc' not in names: return []
    Wt = L == names.index('nuoc'); H, W = Wt.shape; out = []
    for mh, rr in sorted((V or {}).items()):
        for x in (rr.get('json') or {}).get('them') or []:
            b = x.get('toa_do')
            if (x.get('do_tin') or 0) < 0.5 or x.get('loai') not in LOAI_NUOC or not (isinstance(b, list) and len(b) == 4): continue
            cx, cy = min(W - 1, int((b[0] + b[2]) / 2 * W)), min(H - 1, int((b[1] + b[3]) / 2 * H))
            if Wt[cy, cx]: out.append(dict(mh=mh, loai=x.get('loai'), mo_ta=x.get('mo_ta'), toa_do=b, dai_a=False, kieu='THÊM vật trên mặt nước AI (KN-8)'))
    return out
