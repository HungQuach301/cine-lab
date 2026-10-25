#!/opt/cine/bin/python
"""Luật 1.17.8 (phiên K-1.17.8, 25/10/2026) — CHỈ tập kênh 2 từ T4 (`kenh2_tu_t4: true` hoặc khối `n2p:`). T3 và trước: KHÔNG ÁP (không hồi tố).
Căn cứ (nguyên văn, Asia/Saigon): chủ dự án 26/10 00:07 "Chọn hướng cho cảnh hiện đại: A+B+E (khuyến nghị)" (E = ảnh nền AI TOÀN KHUNG cho góc rộng
2026 máy cố định; AI vẽ lại cả nhà thường; sông, đường bờ, mái vòm St Paul's, toà tháp có tên ghép lại từ 3D; nới ngưỡng px/m riêng cảnh năm ≥ 2020);
25/10 09:08 "…các vấn đề khác đều có thể nới để tăng chất lượng và độ chân thực của hình ảnh / Người xem cũng không phải là người chuyên về khảo cổ…";
25/10 21:35 "Các hình 3D hiện đại đang rất yếu so với hình từ Omni". Khiếu nại ANIMATIC-T4-V2 §8 (checks-appeal.md, mục K-1.17.8). Số đo: reports/k1178/.
Mỗi luật: tham số theo tập/tấm, MẶC ĐỊNH GIỮ HÀNH VI CŨ khi không khai.

LUẬT E — N2+ TOÀN KHUNG HIỆN ĐẠI (tấm `n2p.tam[]` khai `n2p_toan_khung_hien_dai: true`, `nam_min` (mặc định 2020; < 2020 không nhận)):
  Điều kiện hiệu lực (k): tấm `nam` ≥ `nam_min` VÀ máy CODINH (tấm `cu_may` hoặc `cu_may` của shot trong log shot). Thiếu điều kiện → (k) lỗi và tấm
  đo như N2P thường (nhà thường thuộc lớp (a)). Khi hiệu lực, AI được vẽ lại MỌI nhà thường (lớp 'nha_thuong' 215,215,215 của mặt nạ — không cần
  ≥ px/m; BE-MAT-NHA không đo tấm này), lớp nền, phố, cây, thành phố xa ('khac'). Giữ:
  (i)   lớp (a)-E = 'nha' 235 (công trình có tên: mái vòm St Paul's, toà có tên OSM, cầu, tường) ∪ 'nuoc' ∪ dải bờ ±8 px @1080 ∪ 'congsu' 'tau' 'lua'
        'co' 'pin' 'nguoi' (∪ `lop_a` tấm khai thêm) = 0/255 sau ghép (N2P-1 (a)); 0 vật lớp (a) thêm/bớt/đổi theo mô hình (N2P-1 (b), đề bài E — nhà
        thường đổi KHÔNG tính); cụm ΔE dải 20 px quanh (a)-E → (c) người đọc (bóng ma toà ghép lại).
  (iii) T9c + T9b + mô hình (N2P-3, như cũ). (iv) 0 vật chuyển động thêm (N2P-4, đề bài E). (v) nhấp nháy/chuyển tấm (N2P-5: mục `n2p.video` khai
        `n2p_toan_khung_hien_dai: true` → lớp đo = ngoài (a)-E).
  (f)   chân trời mốc (hàng N2P-E): tấm khai `toa_co_ten: [{ten, ma}]` (mọi toà tháp có tên/mốc TRONG KHUNG; `ma` = mã 24 bit R<<16|G<<8|B trong
        `mat_na_ct` — PNG mã công trình) — thiếu → THIẾU. (f1) mỗi toà: ≥ CT_MIN_PX điểm @1080 trong mat_na_ct, mọi điểm thuộc (a)-E, ghép = render
        (0/255) → "có mặt (ghép lại)"; không → lỗi (f). (f2) CẢNH BÁO (w): toà cao KHÔNG TÊN bịa nổi bật cao hơn toà có tên gần nhất — máy: cụm nét
        dọc (|∂L*/∂x| ≥ THAP_GX trên ảnh ghép, nét liền ≥ 9 px) trên TRỜI của render, chân chạm chân trời render, cao ≥ 15 px @1080, đỉnh cao hơn đỉnh
        toà có tên gần nhất (theo x) ≥ NOI_BAT × chiều cao khung; mô hình: mục `thap_bia` do_tin ≥ 0,5 cao hơn mốc gần (chủ dự án chấp nhận sai nhỏ
        ở nhà thường — chỉ Cảnh báo).
  (g)   đêm (tấm `dem: true`; không khai → render có trung vị độ sáng V < DEM_V): 0 chữ/biển/logo AI — máy: PP-OCRv4 dò (điểm ≥ 0,6) hộp chữ MỚI so render,
        ngoài (a)-E, đọc được chữ Latin (độ tin ≥ 0,8, độ đặc < 0,8 — không phải ô cửa sổ); mô hình: mục `chu` / `them` loại chu do_tin ≥ 0,5 → lỗi (g).
        Ban ngày: cùng phép → (w) Cảnh báo.
  (iii) bổ sung: T9b đất→nước CHỈ IN ở tấm E (kính/mái xanh AI vẽ lại bị thước màu đọc là nước — đáp án P9-2026 ngày 26,6 % trên tấm đúng); sông/bờ
        đã khoá trong (a)-E, T9c (c)(d) + mô hình (b) giữ.
  Mô hình nhìn: HAI mô hình (q_n2p_vision: gpt + claude, cùng ảnh), đề bài PROMPT_E (PROMPT_VER_E) — chỉ khi --n2p-vision; không có bộ đệm → THIẾU.
  Hàng N2P-E: Chặn (k), (f), (g) ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo. Không tấm E → KHÔNG ÁP.

K-LAI-3 ↔ KIEM-2-MUC (khiếu nại ANIMATIC-T4-V2 §8): đoạn M-d `muc_kiem: nen` không khai `kiem` → tệp kiểm = `kiem_t1` (Flash) KHI `to_khung` (tờ khung
  soi tay) có thật; thiếu một trong hai → THIẾU. Kết luận Flash phải ĐẠT, hoặc có `ngoai_le_duyet: {nguoi_ky, vai: chu_du_an, ngay: YYYY-MM-DD,
  ket_luan: chap_nhan}` (như ngoại lệ tấm C của K-LAI-3) — áp cả KIEM-2-MUC (b).
Q34 (từ T4): danh mục `type` thêm minh_hoa, tu_lieu, that. Q26b-K2 (từ T4): loại minh_hoa → 'minh_hoa', tu_lieu/that → 'anh'. Q26b (từ T4): thay bằng
  Q26b-K2 (KHÔNG ÁP — cùng ngưỡng (c)(d)(e) đo trên vùng; Q26b không đọc được bối cảnh của đặc tả ghép Python không có hero).
SACH-1 (từ T4): `log_chu` nhận khuôn KHOẢNG `{fmt: khoang, muc: [{t0, t1, role, s, px1080?, box?, alpha?}]}` (giây phim; nở thành mẫu mỗi 12 khung)
  cho đường ghép Python; vai §17 (Kinh thánh, áp từ T4): `the_nhan_vat` (≤ 5 s), `bo_dem_so` (số + ≤ 2 từ), `chu_thich_tu_lieu` (≤ 6 từ, ≤ 8 s) — vượt
  giới hạn → (g); ≤ 2 lớp §17 cùng lúc → (g).
Q37 / NHIP-K2 / Q37 (1.13) (d) khung tĩnh (từ T4): quãng nằm trọn trong một thẻ phương pháp cuối phim (miễn K1173-D6 của (c)) và ≤ 10 s → miễn.
TU-LIEU-OMNI (b) (từ T4): mỗi lần tư liệu chỉ xét với clip M-d GẦN NHẤT mỗi phía (không qua clip M-d khác) — bỏ đếm trùng; tư liệu góc khung trong
  shot 3D kề M-d tính là ghép liền khi cửa sổ hiện của nó (`tu_lieu_lan`) cách ranh clip < 1 s 3D sạch (giữ luật 1.17.6).
BIEN-CO-V: hiệu chuẩn lại trên animatic T4 v2 (K1174-D2) — q_bcv.HIEU_CHUAN_T4 (reports/k1178 §5).
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

NAM_MIN_DUYET = 2020                                  # chủ dự án 26/10 00:07: "nới ngưỡng px/m riêng cảnh năm ≥ 2020"
LOP_A_E = ('nha', 'nuoc', 'congsu', 'tau', 'lua', 'co', 'pin', 'nguoi', 'cau')
NHA_THUONG = (215, 215, 215)                          # = q_k1175.NHA_THUONG
BO_PX_E = 8                                           # dải bờ ±8 px @1080 (= BE-MAT-NHA BO_PX)
CT_MIN_PX = 50                                        # (f1) toà có tên ≥ 50 điểm @1080 trong mat_na_ct
THAP_GX, THAP_VK, THAP_H, NOI_BAT = 2.0, 9, 15, 0.01  # (f2) máy — hiệu chuẩn reports/k1178 §1.4 (đáp án P9-2026: tháp bịa bắt 2/2, nhầm 0/3)
CHU_DIEM, CHU_OCR, CHU_DAC = 0.6, 0.8, 0.8            # (g) máy — PP-OCRv4 dò ≥ 0,6; đọc Latin ≥ 0,8; độ đặc < 0,8
DEM_V = 0.40                                          # (g) đêm suy từ render khi không khai `dem`: trung vị V (HSV) < 0,40 (đáp án: ngày 0,73; đêm tổng hợp 0,29)
TIN = 0.5
PROMPT_VER_E = 'n2p-e-v2 (K-1.17.8, 25/10/2026)'   # v1: Claude chỉ đọc 2–3/10 ảnh ở 6/6 tấm (cả lần gọi lại) → v2 thêm câu buộc mở đủ 10 tệp
LOAI_A_E = {'tau_lon', 'lua_lon', 'co', 'cong_su'}   # 'cong_trinh' chỉ tính khi tâm hộp trong (a)-E (nhà thường đổi được phép)
PP_D_MAX = 10.0                                       # Q37 (d) miễn thẻ PP ≤ 10 s (= q_nhip.MIEN_MAX)
S17 = dict(the_nhan_vat=5.0, chu_thich_tu_lieu=8.0)   # §17: thẻ nhân vật ≤ 5 s; chú thích tư liệu ≤ 8 s
S17_TU = dict(bo_dem_so=2, chu_thich_tu_lieu=6)       # §17: bộ đếm số + ≤ 2 từ; chú thích ≤ 6 từ
S17_LOP = 2                                           # §17: cùng lúc ≤ 2 lớp


def ap_1178(E): return bool(E.get('kenh2_tu_t4') or E.get('n2p'))


def _num(x): return isinstance(x, (int, float)) and not isinstance(x, bool)


# ================================================================ LUẬT E
def e_bat(t): return bool((t or {}).get('n2p_toan_khung_hien_dai'))


def e_dieu_kien(t, LS=None):
    """→ dict(hieu_luc, nam_min, loi[(k)…], ghi[]) cho tấm khai n2p_toan_khung_hien_dai; None khi tấm không khai"""
    if not e_bat(t): return None
    w = f"tấm {t.get('id')}"; loi, ghi = [], []
    nm = t.get('nam_min', NAM_MIN_DUYET)
    if not _num(nm): loi.append(f'(k) {w}: nam_min {nm!r} không phải số — dùng {NAM_MIN_DUYET}'); nm = NAM_MIN_DUYET
    elif nm < NAM_MIN_DUYET: loi.append(f'(k) {w}: nam_min {nm:g} < {NAM_MIN_DUYET} (chủ dự án duyệt E cho năm ≥ {NAM_MIN_DUYET}, 26/10 00:07) — dùng {NAM_MIN_DUYET}'); nm = NAM_MIN_DUYET
    nam = t.get('nam'); ok = True
    if not _num(nam) or float(nam) < float(nm): loi.append(f'(k) {w}: năm {nam!r} < nam_min {nm:g} — E không áp, tấm đo như N2P thường (nhà thường thuộc lớp (a))'); ok = False
    cu = t.get('cu_may')
    if cu is None and LS:
        cu = next((s.get('cu_may') for s in LS if str(s.get('shot')) == str(t.get('shot'))), None); ghi.append(f'cú máy theo log shot {t.get("shot")}: {cu}')
    if str(cu or '').upper() != 'CODINH': loi.append(f'(k) {w}: cú máy {cu!r} ≠ CODINH (E chỉ cho góc rộng máy cố định) — E không áp, tấm đo như N2P thường'); ok = False
    if t.get('be_mat_nha_ai'): ghi.append('(w) tấm khai cả be_mat_nha_ai — E thay B: BE-MAT-NHA không đo tấm này')
    return dict(hieu_luc=ok, nam_min=nm, loi=loi, ghi=ghi)


def bang_e(t): return dict({'nha_thuong': NHA_THUONG}, **((t or {}).get('bang') or {}))


def lop_a_e(t): return tuple(dict.fromkeys(LOP_A_E + tuple((t or {}).get('lop_a') or ())))


def _ct(t, ep_dir, size):
    """mat_na_ct + toa_co_ten → (mảng mã 24 bit | None, [{ten, ma}] | None, lỗi THIẾU)"""
    from checks.ll import q_k1175 as K75, q_n2p as N
    toa = t.get('toa_co_ten'); p = N._p(ep_dir, t.get('mat_na_ct'))
    th = []
    if not isinstance(toa, list) or not toa: th.append(f"(f) tấm {t.get('id')}: chưa khai `toa_co_ten: [{{ten, ma}}]` (mọi toà tháp có tên/mốc trong khung)")
    if not p or not os.path.exists(p): th.append(f"(f) tấm {t.get('id')}: chưa khai/không có `mat_na_ct` (PNG mã công trình 24 bit)")
    if th: return None, toa if isinstance(toa, list) else None, th
    return K75._ma(p, size), toa, []


def _ma_cua(x):
    if _num(x.get('ma')): return int(x['ma'])
    m = x.get('mau')
    if isinstance(m, (list, tuple)) and len(m) == 3: return (int(m[0]) << 16) | (int(m[1]) << 8) | int(m[2])
    return None


def chan_troi(R, G, L, names, A, CT, toa, w='tấm'):
    """(f1) toà có tên có mặt (ghép lại) + (f2) máy: tháp bịa cao hơn toà có tên gần nhất → dict(f1[], f2[], toa[], cum)"""
    import cv2, numpy as np
    H, W = L.shape; s = H / 1080.0; f1, f2, T = [], [], []
    dif = np.abs(G.astype(np.int16) - R.astype(np.int16)).max(-1)
    for x in toa or []:
        ma = _ma_cua(x); ten = str(x.get('ten') or ma)
        if ma is None: f1.append(f'(f) toà {ten}: thiếu `ma` (mã 24 bit) hoặc `mau` [r, g, b]'); continue
        m = CT == ma; n = int(m.sum())
        if n < CT_MIN_PX * s * s: f1.append(f'(f) toà {ten}: mặt nạ mã công trình chỉ {n} điểm (< {CT_MIN_PX} @1080) — toà khai mà không có trong khung/mặt nạ'); continue
        ngoai = int((m & ~A).sum()); lech = int(dif[m].max())
        if ngoai: f1.append(f'(f) toà {ten}: {ngoai} điểm không thuộc lớp (a)-E (mặt nạ lớp ghi nhà thường?) — toà có tên phải ghép lại từ render')
        if lech: f1.append(f'(f) toà {ten}: ghép ≠ render tối đa {lech}/255 ({int((dif[m] > 0).sum())} điểm) — toà có tên không được AI vẽ lại')
        ys, xs = np.nonzero(m)
        T.append(dict(ten=ten, ma=ma, dinh_y=int(ys.min()), x_tam=float(xs.mean()), px=n, W=W, H=H,
                      hop=[round(xs.min() / W, 3), round(ys.min() / H, 3), round(xs.max() / W, 3), round(ys.max() / H, 3)]))
    if not T: return dict(f1=f1, f2=f2, toa=T, cum=0)
    S = L == names.index('troi') if 'troi' in names else np.zeros_like(A)
    sky_bot = np.where(S.all(0), H, np.argmin(S, axis=0))
    Sd = cv2.erode(S.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    g = cv2.GaussianBlur(cv2.cvtColor(G, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32) * 100 / 255, (0, 0), 1.0 * s)
    gx = np.abs(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)) / 8
    M = ((gx >= THAP_GX) & Sd).astype(np.uint8)
    M = cv2.morphologyEx(M, cv2.MORPH_OPEN, np.ones((max(3, int(round(THAP_VK * s))), 1), np.uint8))   # nét dọc liền
    M = cv2.dilate(M, np.ones((1, 7), np.uint8))                                                       # gộp hai mép một tháp
    n, cc, st, _ = cv2.connectedComponentsWithStats(M, 8); cum = 0
    for i in range(1, n):
        x, y, w, h, _a = st[i]
        if h < THAP_H * s: continue
        xs = np.arange(x, x + w)
        if not np.any(y + h >= sky_bot[xs] - 4 * s): continue   # chân chạm chân trời render
        cum += 1; t = min(T, key=lambda z: abs(z['x_tam'] - (x + w / 2)))
        if t['dinh_y'] - y >= NOI_BAT * H:
            f2.append(f"(w) {w}: máy: cụm dựng đứng trên trời render [{int(x)}, {int(y)}, {int(x + w)}, {int(y + h)}] đỉnh cao hơn toà có tên gần nhất ({t['ten']}, đỉnh y {t['dinh_y']}) "
                      f"{t['dinh_y'] - y} px — nghi toà cao KHÔNG TÊN bịa (người đọc)")
    return dict(f1=f1, f2=f2, toa=T, cum=cum)


def chu_may(R, G, A):
    """(g) máy: hộp chữ Latin MỚI so render, ngoài (a)-E → [dict(hop, chu, tin, dac)] (PP-OCRv4 det + rec, checks/models)"""
    from checks.cinecheck import textdet as TD
    Rr, Gr = R[:, :, ::-1].copy(), G[:, :, ::-1].copy()
    br = TD.detect(Rr, CHU_DIEM); bg = TD.detect(Gr, CHU_DIEM)
    ov = lambda b, c: not (b[2] < c[0] or c[2] < b[0] or b[3] < c[1] or c[3] < b[1])
    out = []
    for b in bg:
        bx = b['box']
        if any(ov(bx, c['box']) for c in br): continue
        cy, cx = (bx[1] + bx[3]) // 2, (bx[0] + bx[2]) // 2
        if A[min(A.shape[0] - 1, cy), min(A.shape[1] - 1, cx)]: continue
        s_, cf = TD.recognize(Gr, bx); so = TD.solidity(Gr, bx)
        if TD.is_latin_text(s_, cf, CHU_OCR) and (so is None or so < CHU_DAC): out.append(dict(hop=bx, chu=s_, tin=round(cf, 2), dac=None if so is None else round(so, 2)))
    return out


def la_dem(t, R):
    import cv2, numpy as np
    if isinstance(t.get('dem'), bool): return t['dem'], 'khai `dem`'
    v = float(np.median(cv2.cvtColor(R, cv2.COLOR_BGR2HSV)[..., 2])) / 255
    return v < DEM_V, f'suy từ render (trung vị V {v:.2f} {"<" if v < DEM_V else "≥"} {DEM_V:g})'


PROMPT_E = """You are a strict inspector for a documentary. The scene is {noi} in the year {nam}: a wide view from a FIXED camera.
An AI tool repainted the WHOLE frame for realism. Ordinary buildings are ALLOWED to look different (materials, windows, roofs, small changes of
shape or height are fine and must NOT be reported). After the AI step our own 3D render was composited back for these PROTECTED features: the
river and its banks, the named landmarks listed below, bridges, boats and any fire.
Read ALL the image files below with the Read tool before answering (paths are absolute):
You MUST open every one of the 10 files (2 full frames and 8 quarter enlargements) with the Read tool before answering — small signs and towers
are only visible in the enlargements; an answer based on fewer files is rejected.
BEFORE = our own 3D render (ground truth for the protected features):
{truoc}
AFTER = the final frame (AI repaint + protected features composited back):
{sau}
The quarter images are 1.5x enlargements: q1 top-left, q2 top-right, q3 bottom-left, q4 bottom-right of the full frame.
Named landmarks (approximate box in BEFORE, full-frame normalized [x0, y0, x1, y1]):
{moc}

Task 1 — for EACH named landmark: is it clearly present in AFTER at the same place with the same shape? Is it doubled, ghosted, cut or misaligned?
Task 2 — INVENTED TALL BUILDINGS: list every tower or high-rise that stands out on the skyline of AFTER and does NOT exist in BEFORE (or is clearly
much taller in AFTER than in BEFORE). Say whether its top is higher in the frame than the top of the nearest named landmark.
Task 3 — list every ADDED thing that would move in a time-lapse (people, vehicles, boats, aircraft, birds, smoke or steam plumes, cranes) and any ADDED
or REMOVED bridge, ship or fire.
Task 4 — TEXT AND SIGNS: list every text, letters, numbers, shop sign, billboard, illuminated sign, logo or brand mark visible in AFTER that is not in
BEFORE, even if it is small or illegible.
Task 5 — report any place where LAND became WATER or WATER became LAND.
Task 6 — anything that could not exist in the year {nam}.
Use ONLY these category keys for "loai": {loai}
Give each box in FULL-frame normalized coordinates [x0, y0, x1, y1] (0-1, origin top-left).
Answer with ONLY one JSON object, no other text:
{{"moc": [{{"ten": "<landmark>", "co_mat": true|false, "nhan_doi": true|false, "mo_ta": "<what>", "do_tin": <0-1>}}],
 "thap_bia": [{{"mo_ta": "<what>", "toa_do": [x0, y0, x1, y1], "cao_hon_moc_gan": true|false, "do_tin": <0-1>}}],
 "them": [{{"loai": "<key>", "mo_ta": "<what>", "toa_do": [x0, y0, x1, y1], "thoi_dai_sai": true|false, "ly_do_thoi_dai": "<why or empty>", "nam_xuat_hien": <year or null>, "do_tin": <0-1>}}],
 "bot_doi": [{{"loai": "<key>", "mo_ta": "<what was removed/changed among the PROTECTED features>", "toa_do": [x0, y0, x1, y1], "do_tin": <0-1>}}],
 "chu": [{{"mo_ta": "<text/sign/logo>", "toa_do": [x0, y0, x1, y1], "do_tin": <0-1>}}],
 "doi_loai_vung": [{{"mo_ta": "<land->water or water->land, where>", "toa_do": [x0, y0, x1, y1], "do_tin": <0-1>}}]}}"""


def de_bai_e(T, W, H):
    """danh sách mốc cho đề bài: [ten @ hộp chuẩn hoá] từ mặt nạ mã công trình (đo, không khai)"""
    return '\n'.join(f"- {t['ten']}: {t['hop']}" for t in T) or '- (none listed)'


def ket_luan_e(V, A, anh_tinh, nam, T):
    """mô hình (đề bài E) → (L1 vật (a), L2 thời đại có năm, L2b không năm, L4 chuyển động, VUNG, F2 tháp bịa, CHU)"""
    from checks.ll import q_n2p as N
    L1, L2, L2b, L4, VUNG, F2, CHU = [], [], [], [], [], [], []
    hop = lambda x: x.get('toa_do') if isinstance(x.get('toa_do'), list) and len(x.get('toa_do')) == 4 else [0, 0, 1, 1]
    for mh, rr in sorted((V or {}).items()):
        j = rr.get('json') or {}
        for x in j.get('moc') or []:
            if (x.get('do_tin') or 0) < TIN: continue
            if x.get('co_mat') is False or x.get('nhan_doi') is True:
                L1.append(dict(mh=mh, loai='cong_trinh', mo_ta=f"{x.get('ten')}: {x.get('mo_ta')}", toa_do=[0, 0, 1, 1], dai_a=True,
                               kieu='BỚT/ĐỔI toà có tên' if x.get('co_mat') is False else 'toà có tên NHÂN ĐÔI/bóng ma'))
        for x in j.get('them') or []:
            if (x.get('do_tin') or 0) < TIN: continue
            b = hop(x); it = dict(mh=mh, loai=x.get('loai'), mo_ta=x.get('mo_ta'), toa_do=b, dai_a=N._in(b, A))
            if x.get('loai') in LOAI_A_E or (x.get('loai') == 'cong_trinh' and it['dai_a']): L1.append(dict(it, kieu='THÊM vật lớp (a)-E'))
            if x.get('loai') == 'chu': CHU.append(it)
            if x.get('thoi_dai_sai'):
                ny = x.get('nam_xuat_hien'); co_nam = _num(ny) and ny > float(nam)
                (L2 if co_nam else L2b).append(dict(it, ly_do=x.get('ly_do_thoi_dai'), nam=ny))
            if anh_tinh and x.get('loai') in N.LOAI_DONG: L4.append(it)
        for x in j.get('bot_doi') or []:
            if (x.get('do_tin') or 0) < TIN: continue
            b = hop(x); L1.append(dict(mh=mh, loai=x.get('loai'), mo_ta=x.get('mo_ta'), toa_do=b, dai_a=N._in(b, A), kieu='BỚT/ĐỔI vật lớp (a)-E'))
        for x in j.get('chu') or []:
            if (x.get('do_tin') or 0) >= TIN: CHU.append(dict(mh=mh, loai='chu', mo_ta=x.get('mo_ta'), toa_do=hop(x)))
        for x in j.get('thap_bia') or []:
            if (x.get('do_tin') or 0) < TIN: continue
            b = hop(x)
            gan = min(T, key=lambda z: abs(z['x_tam'] / z['W'] - (b[0] + b[2]) / 2)) if T else None
            cao = x.get('cao_hon_moc_gan') is True or (gan is not None and b[1] < gan['dinh_y'] / gan['H'] - NOI_BAT)
            if cao: F2.append(dict(mh=mh, mo_ta=x.get('mo_ta'), toa_do=b, gan=gan['ten'] if gan else None))
        for x in j.get('doi_loai_vung') or []:
            if (x.get('do_tin') or 0) >= TIN: VUNG.append(dict(mh=mh, mo_ta=x.get('mo_ta'), toa_do=x.get('toa_do')))
    return L1, L2, L2b, L4, VUNG, F2, CHU


def kiem_tam_e(t, ep_dir='.', vision=False, cache=None, out=None, noi='', t4=False, ek=None):
    """một tấm LUẬT E (hiệu lực) → dict như q_n2p.kiem_tam + khoá 'E' (f, g, w)"""
    import cv2, numpy as np
    from checks.ll import q_n2p as N, q_n2p_vision as QV
    rp, gp, mp = N._p(ep_dir, t.get('render')), N._p(ep_dir, t.get('ghep')), N._p(ep_dir, t.get('mat_na'))
    nam = t.get('nam'); tid = str(t.get('id') or os.path.basename(gp or '?'))
    if not (rp and gp and mp and nam is not None): return dict(id=tid, loi_chay=f'tấm {tid}: thiếu render/ghep/mat_na/nam')
    bang, la = bang_e(t), lop_a_e(t)
    D = N.do_tam(rp, gp, mp, la, bang, None, bo_a=BO_PX_E)
    R = cv2.imread(rp); G = cv2.imread(gp)
    if G.shape != R.shape: G = cv2.resize(G, (R.shape[1], R.shape[0]), interpolation=cv2.INTER_AREA)
    H, W = R.shape[:2]; L, names = N.idmap(mp, (W, H), bang); A = D['_A']
    w_, th_ = [x for x in (ek or {}).get('ghi') or [] if x.startswith('(w)')], []
    pnt = float((L == names.index('nha_thuong')).mean() * 100) if 'nha_thuong' in names else 0.0
    if pnt < 0.5: w_.append(f'(w) tấm {tid}: mặt nạ lớp chỉ {pnt:.2f} % nhà thường (215) — mọi nhà còn lại là lớp (a)-E (mặt nạ chưa tách nhà thường?)')
    CT, toa, thc = _ct(t, ep_dir, (W, H)); th_ += thc
    F = chan_troi(R, G, L, names, A, CT, toa, f'tấm {tid}') if CT is not None else dict(f1=[], f2=[], toa=[], cum=0)
    dem, dem_nguon = la_dem(t, R)
    try: CH = chu_may(R, G, A)
    except Exception as e: CH = None; th_.append(f'(g) tấm {tid}: máy dò chữ lỗi: {type(e).__name__}: {e}')   # noqa: BLE001
    pr = PROMPT_E.format(noi=t.get('noi', noi) or 'the place', nam=int(float(nam)), truoc='{truoc}', sau='{sau}', moc=de_bai_e(F['toa'], W, H),
                         loai=', '.join(f'"{a}" ({b})' for a, b in QV.LOAI.items()))
    V = QV.soi(rp, gp, nam, t.get('noi', noi), t.get('t4', t4), out=out, tag=tid, api=vision, cache=cache, de=dict(prompt=pr, ver=PROMPT_VER_E))
    L1, L2, L2b, L4, VUNG, F2, CHU = ket_luan_e(V.get('ket_qua') or {}, A, bool(t.get('anh_tinh', True)), nam, F['toa'])
    Q = None; cache = cache if cache is not None else {}
    if vision or cache.get('qtd', {}).get(tid):
        Q = cache.setdefault('qtd', {}).get(tid)
        if Q is None and vision:
            from checks.ll import q_thoi_dai as QT
            qc = cache.setdefault('o2', {}); od = os.path.join(out or '/var/tmp/n2p-qtd', 'qtd')
            Qg = QT.soi_khung(gp, nam, od, f'{tid}-ghep', t.get('noi', noi), True, qc); Qr = QT.soi_khung(rp, nam, od, f'{tid}-render', t.get('noi', noi), True, qc)
            Q = dict(ghep=Qg, render=Qr, moi=N.qtd_moi(Qg, Qr), loi='; '.join(x for x in (Qg.get('loi'), Qr.get('loi')) if x) or None,
                     chi_phi_usd=round(float(Qg.get('cost_usd') or 0) + float(Qr.get('cost_usd') or 0), 4))
            if not Q['loi']: cache['qtd'][tid] = Q
    EE = dict(f1=F['f1'], f2_may=F['f2'], f2_mh=F2, cum=F['cum'], toa=F['toa'], dem=dem, dem_nguon=dem_nguon, chu_may=CH, chu_mh=CHU, w=w_, thieu=th_,
              vision_loi=V.get('loi'), nha_thuong_pct=round(pnt, 2), lop_a_e_pct=round(float(A.mean() * 100), 2))
    return dict(id=tid, shot=t.get('shot'), nam=nam, anh_tinh=bool(t.get('anh_tinh', True)), do={k: v for k, v in D.items() if not k.startswith('_')},
                V=V, L1=L1, L1b=[], L2=L2, L2b=L2b, L4=L4, VUNG=VUNG, Q=Q, SONG=None, VONG=None, E=EE)


def hang_e(KT, EK):
    """hàng N2P-E. KT: kết quả tấm (đã đo); EK: {id tấm: e_dieu_kien} của mọi tấm khai E"""
    from checks.ll import q_n2p as N
    if not EK: return N.na('không tấm nào khai n2p_toan_khung_hien_dai')
    M = {k: [] for k in 'kfgw'}; th, vals = [], []
    for tid, ek in EK.items():
        M['k'] += [x for x in ek['loi']]
        k = next((x for x in KT or [] if str(x.get('id')) == str(tid)), None)
        if not ek['hieu_luc']: vals.append(f'{tid}: E không hiệu lực'); continue
        if k is None or k.get('loi_chay'): th.append(f"(f) tấm {tid}: {(k or {}).get('loi_chay') or 'chưa đo'}"); continue
        e = k.get('E') or {}; w = f'tấm {tid}'
        M['f'] += e.get('f1') or []; M['w'] += (e.get('f2_may') or []) + (e.get('w') or [])
        M['w'] += [f"(w) {w}: {x['mh']}: toà cao không tên bịa «{str(x.get('mo_ta') or '')[:70]}» @{[round(v, 3) for v in x['toa_do']]} cao hơn mốc gần ({x.get('gan')})" for x in e.get('f2_mh') or []]
        th += e.get('thieu') or []
        chu = [f"(g) {w}: máy: chữ «{x['chu']}» (đọc {x['tin']}) hộp {x['hop']}" for x in e.get('chu_may') or []]
        chu += [f"(g) {w}: {x['mh']}: chữ/biển/logo «{str(x.get('mo_ta') or '')[:70]}» @{[round(v, 3) for v in x['toa_do']]}" for x in e.get('chu_mh') or []]
        if e.get('dem'):
            M['g'] += chu
            if e.get('vision_loi'): th.append(f"(g) {w} (đêm): mô hình nhìn — {e['vision_loi']}")
        else: M['w'] += ['(w)' + x[3:] + ' — ban ngày (Cảnh báo)' for x in chu]
        vals.append(f"{tid}: {len(e.get('toa') or [])} toà có tên, (f1) {len(e.get('f1') or [])} lỗi, tháp bịa máy {len(e.get('f2_may') or [])} / mô hình {len(e.get('f2_mh') or [])}, "
                    f"{'đêm' if e.get('dem') else 'ngày'} ({e.get('dem_nguon')}), chữ máy {len(e.get('chu_may') or [])} / mô hình {len(e.get('chu_mh') or [])}, (a)-E {e.get('lop_a_e_pct')} %, nhà thường {e.get('nha_thuong_pct')} %")
    loi = M['k'] + M['f'] + M['g'] + M['w']
    return N.r(loi, th, val=f'{len(EK)} tấm E · ' + ' · '.join(vals[:4]), muc={k: [x for x in loi + th if x.startswith(f'({k})')] for k in 'kfgw'})


# ================================================================ K-LAI-3 ↔ KIEM-2-MUC (đoạn M-d mức nền)
def tep_kiem_nen(m, base):
    """đoạn mức nen không có `kiem` → (tệp kiem_t1, None) khi to_khung có thật; thiếu → (None, lý do)"""
    from checks.ll import q_n2p as N
    if str(m.get('muc_kiem') or '') != 'nen' or m.get('kiem'): return None, None
    t1, tk = m.get('kiem_t1'), m.get('to_khung')
    thieu = ([] if t1 else ['`kiem_t1` (tệp Flash)']) + ([] if tk and os.path.exists(N._p(base, tk)) else [f'`to_khung` (tờ khung soi tay){" — " + str(tk) + " không có" if tk else ""}'])
    return (t1, None) if not thieu else (None, 'mức nen thiếu ' + ', '.join(thieu) + ' (K-1.17.8: nen = Flash + tờ khung)')


EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')


def ngoai_le_duyet(m):
    """`ngoai_le_duyet` của đoạn M-d → (True, '') khi đủ: nguoi_ky (không email), vai chu_du_an, ngay YYYY-MM-DD, ket_luan chap_nhan"""
    x = m.get('ngoai_le_duyet')
    if not isinstance(x, dict): return False, 'không có ngoai_le_duyet'
    p = []
    if x.get('vai') != 'chu_du_an': p.append(f"vai {x.get('vai')!r} ≠ chu_du_an")
    nk = str(x.get('nguoi_ky') or '')
    if not nk.strip(): p.append('thiếu nguoi_ky')
    elif EMAIL.search(nk): p.append('nguoi_ky chứa email (che email: ghi tên/vai)')
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(x.get('ngay') or '')): p.append('ngay không dạng YYYY-MM-DD')
    if str(x.get('ket_luan') or '') not in ('chap_nhan', 'dong_y'): p.append(f"ket_luan {x.get('ket_luan')!r} không phải chap_nhan")
    return (not p), '; '.join(p)


# ================================================================ Q34 / Q26b-K2 (từ T4)
TYPES_T4 = ('minh_hoa', 'tu_lieu', 'that')
LOAI_K2_T4 = {'minh_hoa': 'minh_hoa', 'tu_lieu': 'anh', 'that': 'anh'}


# ================================================================ SACH-1: log chữ khuôn khoảng + vai §17
def log_chu_khoang(J, fps=24, buoc=12):
    """{fmt: khoang, muc: [{t0, t1, role, s, …}]} → [{f, items}] mẫu mỗi `buoc` khung (giây phim tuyệt đối)"""
    M = {}
    for x in J.get('muc') or []:
        if not (_num(x.get('t0')) and _num(x.get('t1'))) or x['t1'] <= x['t0']: continue
        it = {k: v for k, v in x.items() if k not in ('t0', 't1')}
        f0, f1 = int(round(x['t0'] * fps)), int(round(x['t1'] * fps))
        for f in range((f0 + buoc - 1) // buoc * buoc, f1, buoc): M.setdefault(f, []).append(dict(it))
    return [dict(f=f, items=v) for f, v in sorted(M.items())]


def so_tu(s): return len([w for w in re.split(r'\s+', str(s or '').strip()) if w])


def sach1_s17(TX, step, fps=24):
    """vai §17 (từ T4) trong log chữ → (lỗi (g)[], số mẫu §17). Thẻ nhân vật ≤ 5 s; bộ đếm số + ≤ 2 từ; chú thích tư liệu ≤ 6 từ, ≤ 8 s; ≤ 2 lớp cùng lúc."""
    from checks.ll import q_k116 as K6
    loi, n, run, run_tu, lop_loi = [], 0, {}, set(), 0
    for f, it in sorted((TX or {}).items()):
        lop = set()
        for x in it:
            ro = str(x.get('role') or '')
            if ro not in ('the_nhan_vat', 'bo_dem_so', 'chu_thich_tu_lieu') or not K6._vis(x): continue
            n += 1; lop.add(ro); s_ = str(x.get('s') or '')
            run.setdefault((ro, s_), []).append(f)
            if ro in S17_TU and (ro, s_) not in run_tu:
                run_tu.add((ro, s_))   # một dòng lỗi mỗi chữ (không mỗi mẫu)
                tu = so_tu(re.sub(r'[\d.,%$£€+\-–]+', ' ', s_)) if ro == 'bo_dem_so' else so_tu(s_)
                if tu > S17_TU[ro]: loi.append(f"(g) {ro} «{s_[:40]}» @{K6.mmss(f / fps)}: {tu} từ > {S17_TU[ro]} (§17)")
        if len(lop) > S17_LOP:
            if not lop_loi: loi.append(f"(g) @{K6.mmss(f / fps)}: {len(lop)} lớp §17 cùng lúc > {S17_LOP} ({', '.join(sorted(lop))})")
            lop_loi += 1
    for (ro, s_), fs in run.items():
        if ro not in S17: continue
        for f0, f1 in K6._runs(fs, step):
            d = K6._run_s(f0, f1, step)
            if d > S17[ro] + step / fps / 2: loi.append(f"(g) {ro} «{s_[:40]}» @{K6.mmss(f0 / fps)}: hiện {d:.2f} s > {S17[ro]:g} s (§17)")
    return list(dict.fromkeys(loi)), n


# ================================================================ Q37 (d) — miễn thẻ PP cuối phim (từ T4)
def mien_d(mien, L, a):
    """quãng khung tĩnh [a, a + L] nằm trọn trong một khoảng thẻ PP của `mien` và ≤ 10 s → tên thẻ, không thì None"""
    for m0, m1, k, n in mien or []:
        if k == 'the_pp' and m0 - 0.05 <= a and a + L <= m1 + 0.05 and L <= PP_D_MAX + 1e-6: return n
    return None
