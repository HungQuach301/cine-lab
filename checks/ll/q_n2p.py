#!/opt/cine/bin/python
"""Luật N2+ (Kinh thánh §15, áp từ T4 — nháp nguyên văn reports/NC-N2P-BAO-CAO.md §6.3; lệnh K-1.17 21/10/2026) — bản 1.17.0 (phiên K-1.17).
CHỈ tập kênh 2 từ T4: episode.yaml khai `kenh2_tu_t4: true` hoặc khối `n2p:`. Tập cũ (T1–T3): mọi hàng N2P KHÔNG ÁP, luật cũ giữ đúng 1.16.1.
Chuyển từ reports/nc-n2p/ma/kiem_n2p.py + n2p_lib.py (NC-N2P; kiểm có đáp án 6/6 mỗi mô hình, đối chứng 0 báo). Mô hình nhìn: q_n2p_vision.py.

Đầu vào (đường dẫn tương đối thư mục episode.yaml):
  n2p:
    noi: <nơi trong đề bài mô hình>        t4: true|false (thêm danh sách CẤM London 1666)
    tam: [{id, shot, render, ghep, mat_na, nam, anh_tinh?: true, lop_a?: [tên lớp], bang?: {tên: [r, g, b]}}]
         render = khung render của ta; ghep = khung AI ĐÃ GHÉP lớp (a) (PNG, không nén mất); mat_na = mặt nạ ID (bảng màu V7C idmask_v7c.js)
    video: [{shot, ghep: <mp4>, render: <mp4 đối chứng>, mat_na: <PNG khung đầu, máy cố định>, chuyen_tam?: [{t, kieu: hoa|cat, dur}]}]
  log_shot mỗi shot: `ai_nen` (bool hoặc {tam: [id], chuyen_tam: [...]}) = shot dùng tấm nền N2+; `minh_hoa` (bool) = minh hoạ toàn khung
  AI (M-d / N2); `ai_image` / `ai_texture` = N1 (1.15). Thời lượng = `dur` (hoặc t1 − t0).

Hàng (cấp ở cap112.py: Chặn ở cổng G2 · Cảnh báo ở animatic (`animatic: true`), như K116-D5; không khai cổng → G2):
  N2P-1 (i) lớp (a) sau ghép: (a) max |ghép − render| trong mặt nạ (a) = 0/255 (8 bit; ⇔ < 1/255); (b) 0 vật loại lớp (a) (cờ, công trình,
        công sự, tàu lớn, chữ, đèn, lửa lớn) THÊM/BỚT/ĐỔI ở BẤT KỲ đâu theo ít nhất một mô hình (do_tin ≥ 0,5; trong dải 20 px quanh (a) ghi
        'dải (a)'); (c) máy: cụm ΔE76 ≥ 30 (ảnh mờ σ 1,5) ≥ 80 px trong DẢI 20 px quanh (a) (px quy về 1080p) — CẢNH BÁO cho người đọc tờ so.
        1.17.5: (d) vòng bảo vệ khớp màu cục bộ (khai `khop_mau_cuc_bo`), (e) lớp sống cộng hiệu (khai `song: {render_co, render_khong, nen}`) — q_k1175.
  N2P-2 (ii) lỗi thời đại: (a) vật THÊM có thoi_dai_sai (do_tin ≥ 0,5) VÀ (năm xuất hiện mô hình nêu > năm khung, hoặc loại máy bay/xe máy ở
        cảnh < 1900) ở ÍT NHẤT MỘT trong hai mô hình; không kèm năm → 'nghi vấn không năm' (ghi, người đọc; không tính lỗi);
        (b) q_thoi_dai.py (O2, khi --vision): nghi vấn trên khung ghép KHÔNG trùng nghi vấn của chính render (đối chứng) → lỗi.
        Giới hạn đã biết (K-1.15, NC-N2P §2): cờ ~20–25 px @1080 không đọc được mẫu → q_thoi_dai báo nhầm/bỏ sót cờ nhỏ; bảo vệ cờ bằng cấu trúc
        (cờ thuộc lớp (a), (i) bắt) + người đọc tờ so.
  N2P-3 (iii) đổi loại vùng: (a) T9b mỗi chiều ≤ 2 % (đất→nước: % điểm đất của mặt nạ có 'màu nước' HSV H 85–130, S ≥ 40, V ≥ 30 ở ghép mà render
        không; nước→đất: % điểm nước-màu-nước của render mất màu nước; bỏ loé nắng V ≥ 0,85 & S ≤ 0,25 và dải 8 px quanh bờ — px quy về 1080p);
        (b) 0 báo đổi đất↔nước của mô hình (do_tin ≥ 0,5).
        1.17.5 (A1/A2, q_k1175.t9c): chiều nước→đất đo bằng T9c (đường bờ đo, đối chứng render — AI đổi sắc nước không còn là lỗi; phản chiếu có
        trong render giữ; phản chiếu AI tự vẽ không miễn): (c) bờ lấn sâu ≥ 6 px @1080, dài ≥ 12 px; (d) khác nước giữa nước > 2 %. T9b nước→đất chỉ in.
  N2P-4 (iv) đóng băng (tấm tĩnh, `anh_tinh` mặc định true): (a) 0 vật THÊM loại chuyển động (người, động vật, chim, thuyền nhỏ, xe chạy, khói,
        lửa trại, máy bay, xe máy) theo ít nhất một mô hình — người/động vật luôn là chuyển động (B3).
  N2P-5 (v) nhấp nháy + chuyển tấm (video shot tấm nền): (a) mỗi chuyển tấm khai `kieu: hoa` và `dur` ≥ 2 s; (b) bước nhảy chuyển tấm: max theo
        bước khung của ΔE76 TB trên lớp (c) ≤ 1,0 ΔE/khung; (c) nhấp nháy: TB |Δ xám|/khung trên lớp (c) ngoài cửa sổ hoà ≤ 1,5 × đối chứng render
        (sàn đo SAN_NHAP = 0,02 mức xám/khung khi đối chứng ≈ 0).
  N2P-6 (vi) trần §15(d) (log shot): (a) tấm nền `ai_nen` ≤ 50 % thời lượng; (b) minh hoạ `minh_hoa` (M-d) — 1.17.4 (Q2): KHÔNG trần cứng, chỉ ghi %; (c) tổng khung có AI (ai_nen ∪
        minh_hoa ∪ ai_image ∪ ai_texture) ≤ 70 %; (d) không chồng: một shot không vừa `ai_nen` vừa `minh_hoa`.
Mô hình nhìn MẶC ĐỊNH TẮT (chi phí ≈ $0,2/khung + q_thoi_dai ≈ $0,04 × 2): `--vision` (k2check `--n2p-vision`) mới gọi; không cờ → đọc bộ đệm
<out>/n2p-vision-cache.json; khung chưa soi → THIẾU (Chặn ở G2).

  q_n2p.py --render r.png --ghep g.png --mat-na id.png --nam 1666 [--noi London] [--t4] [--anh-tinh 0|1] [--vision] [--out d] [--json ra.json]
  q_n2p.py <episode.yaml> [--tl timeline.json] [--vision] [--json ra.json]
"""
import json, os, statistics, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base  # noqa: E402

# ---- bảng màu mặt nạ ID V7C (design/k2v/v7c/idmask_v7c.js; n2p_lib.PAL) và lớp N2+
PAL = {'troi': (40, 80, 200), 'nuoc': (0, 170, 190), 'bang': (200, 170, 90), 'suon': (150, 120, 70), 'da': (110, 100, 95), 'pho': (255, 200, 220), 'nha': (235, 235, 235),
       'trai': (245, 225, 160), 'congsu': (170, 150, 120), 'tau': (255, 0, 0), 'co': (255, 255, 0), 'pin': (255, 0, 255), 'lua': (255, 128, 0), 'nguoi': (0, 255, 0),
       'khac': (128, 128, 128), 'cay': (60, 140, 60)}
LOP_A = ('pho', 'nha', 'trai', 'congsu', 'tau', 'co', 'pin', 'lua', 'nguoi', 'khac')
DAT = ('bang', 'suon', 'da', 'pho')
LOAI_A = {'co', 'cong_trinh', 'cong_su', 'tau_lon', 'chu', 'den', 'lua_lon'}
LOAI_DONG = {'nguoi', 'dong_vat', 'chim', 'thuyen_nho', 'xe_chay', 'khoi', 'lua_trai', 'may_bay', 'xe_may'}
LOAI_HIEN_DAI = {'may_bay', 'xe_may'}
TIN = 0.5
DAI_PX, CUM_DE, CUM_PX = 20, 30.0, 80          # (i) dải 20 px @1080 quanh (a); cụm ΔE ≥ 30 ≥ 80 px @1080 (người đọc)
T9B_MAX, BO_PX = 2.0, 8                          # (iii) ≤ 2 % mỗi chiều; bỏ dải 8 px @1080 quanh bờ
HOA_MIN, BUOC_MAX, NHAP_K, SAN_NHAP = 2.0, 1.0, 1.5, 0.02   # (v)
TRAN_NEN, TRAN_MH, TRAN_TONG = 50.0, 20.0, 70.0  # (vi) §15(d) theo lệnh K-1.17
ROWS = ('N2P-1', 'N2P-2', 'N2P-3', 'N2P-4', 'N2P-5', 'N2P-6')
K75_GIUA, K75_VONG_MAX = 2.0, 40   # = q_k1175.T9C['GIUA'], q_k1175.VONG_MAX (1.17.5)


def ap_n2p(E): return bool(E.get('kenh2_tu_t4') or E.get('n2p'))


def r(loi=(), thieu=(), val='', ket_qua=None, **kw):
    loi, thieu = list(loi), list(thieu)
    return dict(ok=not loi and not thieu, ket_qua=ket_qua or ('THIẾU' if thieu and not loi else None), loi=loi, thieu=thieu, val=val, **kw)


def na(why): return dict(ok=True, ket_qua='KHÔNG ÁP', loi=[], val=why)


def sat(ten, v, nguong):
    return [f'{ten} {v} (ngưỡng {nguong})'] if nguong and abs(v - nguong) <= 0.05 * abs(nguong) else []


def _p(base_, x): return x if not x or os.path.isabs(x) else os.path.normpath(os.path.join(base_, x))


# ================================================================ máy: mặt nạ, (i), (iii)
def idmap(png, size=None, bang=None, cay_max=0.003):
    """PNG mặt nạ ID → (mảng nhãn, tên lớp). Cụm 'nuoc' nhỏ (< cay_max diện tích) không chạm cụm nước lớn nhất → 'cay' (cây instanced V7C)."""
    import cv2, numpy as np
    pal = dict(PAL, **{k: tuple(v) for k, v in (bang or {}).items()}); names = list(pal)
    im = cv2.imread(png, cv2.IMREAD_COLOR)
    if im is None: raise FileNotFoundError(png)
    im = im[:, :, ::-1]
    if size and (im.shape[1], im.shape[0]) != size: im = cv2.resize(im, size, interpolation=cv2.INTER_NEAREST)
    P = np.array([pal[n] for n in names], np.int32)
    key = (im[..., 0].astype(np.int32) << 16) | (im[..., 1].astype(np.int32) << 8) | im[..., 2]
    pk = (P[:, 0] << 16) | (P[:, 1] << 8) | P[:, 2]; o = np.argsort(pk); ix = np.searchsorted(pk[o], key).clip(0, len(pk) - 1)
    L = o[ix].astype(np.uint8); bad = pk[o][ix] != key
    if bad.any():   # điểm không đúng màu bảng (khử răng cưa, hiếm) → màu gần nhất
        L[bad] = ((im[bad][:, None, :].astype(np.int32) - P[None]) ** 2).sum(-1).argmin(-1)
    if 'nuoc' in names and 'cay' in names:
        w = (L == names.index('nuoc')).astype(np.uint8); n, cc, st, _ = cv2.connectedComponentsWithStats(w, 8)
        if n > 2:
            big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); small = [i for i in range(1, n) if i != big and st[i, cv2.CC_STAT_AREA] < cay_max * L.size]
            if small: L[np.isin(cc, small)] = names.index('cay')
    return L, names


def lop(L, names, ten):
    import numpy as np
    return np.isin(L, [names.index(n) for n in ten if n in names])


def _lab(b):
    import cv2, numpy as np
    return cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32) - np.array([0, 128, 128], np.float32)


def _blue(bgr):
    import cv2
    h = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV); return (h[..., 0] >= 85) & (h[..., 0] <= 130) & (h[..., 1] >= 40) & (h[..., 2] >= 30)


def do_tam(render_p, ghep_p, mat_na_p, lop_a=LOP_A, bang=None, tru=None):
    """số đo máy một tấm: (i) lệch trong (a), dải 20 px, cụm ΔE; (iii) T9 + T9b. Px ngưỡng quy theo chiều cao khung / 1080.
    1.17.6 (KN-2): `tru` = vùng loại khỏi (a) và khỏi dải 20 px (nhà đo được nở 1 px của tấm be_mat_nha_ai — do BE-MAT-NHA (a)(b) kiểm)."""
    import cv2, numpy as np
    R = cv2.imread(render_p, cv2.IMREAD_COLOR); G = cv2.imread(ghep_p, cv2.IMREAD_COLOR)
    if R is None: raise FileNotFoundError(render_p)
    if G is None: raise FileNotFoundError(ghep_p)
    if G.shape != R.shape: G = cv2.resize(G, (R.shape[1], R.shape[0]), interpolation=cv2.INTER_AREA)
    L, names = idmap(mat_na_p, (R.shape[1], R.shape[0]), bang); A = lop(L, names, lop_a); s = R.shape[0] / 1080.0
    A0 = A
    if tru is not None: A = A & ~tru
    dif = np.abs(G.astype(np.int16) - R.astype(np.int16)).max(-1)
    rad = max(1, int(round(DAI_PX * s))); band = (cv2.dilate(A.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rad + 1,) * 2)) > 0) & ~A
    if tru is not None: band &= ~tru
    dE = np.sqrt(((_lab(cv2.GaussianBlur(G, (0, 0), 1.5)) - _lab(cv2.GaussianBlur(R, (0, 0), 1.5))) ** 2).sum(-1))
    n, cc, st, _ = cv2.connectedComponentsWithStats(((dE >= CUM_DE) & band).astype(np.uint8), 8); amin = max(1, int(round(CUM_PX * s * s)))
    cum = sorted([dict(hop=[int(st[i, 0]), int(st[i, 1]), int(st[i, 0] + st[i, 2]), int(st[i, 1] + st[i, 3])], px=int(st[i, 4])) for i in range(1, n) if st[i, 4] >= amin], key=lambda x: -x['px'])
    D = lop(L, names, DAT); Wt = L == names.index('nuoc') if 'nuoc' in names else np.zeros_like(A)
    br, bg = _blue(R), _blue(G)
    d2n = float((D & bg & ~br).sum() / max(1, D.sum()) * 100); n2d = float((Wt & br & ~bg).sum() / max(1, (Wt & br).sum()) * 100)
    hs = cv2.cvtColor(G, cv2.COLOR_BGR2HSV); loe = (hs[..., 2] >= 217) & (hs[..., 1] <= 64); k = 2 * max(1, int(round(BO_PX * s))) + 1
    bo = cv2.dilate((cv2.morphologyEx(Wt.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0).astype(np.uint8), np.ones((k, k), np.uint8)) > 0
    d2n_b = float((D & bg & ~br & ~bo).sum() / max(1, D.sum()) * 100); n2d_b = float((Wt & br & ~bg & ~loe & ~bo).sum() / max(1, (Wt & br).sum()) * 100)
    from checks.ll import q_k1175 as K75
    t9c = K75.t9c(R, G, L, names); t9c.pop('win', None)   # 1.17.5 (A1/A2): đường bờ đo, đối chứng render — thay T9b chiều nước→đất
    return dict(i=dict(max_trong_a=int(dif[A].max()) if A.any() else 0, diem_lech_trong_a=int((dif[A] > 0).sum()), dien_tich_a_pct=round(float(A.mean() * 100), 2),
                       dai20_pct=round(float(band.mean() * 100), 2), dai20_cum_dE30=len(cum), dai20_cum_lon=cum[:15],
                       **(dict(tru_bmn_pct=round(float((A0 & tru).mean() * 100), 2), max_trong_a_chua_tru=int(dif[A0].max()) if A0.any() else 0) if tru is not None else {})),
                iii=dict(t9_dat_thanh_nuoc_pct=round(d2n, 2), t9_nuoc_thanh_dat_pct=round(n2d, 2), t9b_dat_thanh_nuoc_pct=round(d2n_b, 2), t9b_nuoc_thanh_dat_pct=round(n2d_b, 2), t9c=t9c),
                _band=band, _A=A, W=R.shape[1], H=R.shape[0])


def _in(box, M):
    H, W = M.shape; x0, y0, x1, y1 = [int(round(v * q)) for v, q in zip(box, (W, H, W, H))]
    x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(W, max(x1, x0 + 1)), min(H, max(y1, y0 + 1))
    return bool(M[y0:y1, x0:x1].any())


def ket_luan(V, band, A, anh_tinh, nam):
    """danh sách mô hình (q_n2p_vision ket_qua) → (vật (a), thời đại có năm, nghi vấn không năm, đóng băng, đổi vùng). Luật = NC-N2P kiem_n2p.ket_luan."""
    L1, L2, L2b, L4, VUNG = [], [], [], [], []
    hop = lambda x: x.get('toa_do') if isinstance(x.get('toa_do'), list) and len(x.get('toa_do')) == 4 else [0, 0, 1, 1]
    for mh, rr in sorted((V or {}).items()):
        j = rr.get('json') or {}
        for x in j.get('them') or []:
            if (x.get('do_tin') or 0) < TIN: continue
            b = hop(x); it = dict(mh=mh, loai=x.get('loai'), mo_ta=x.get('mo_ta'), toa_do=b, dai_a=_in(b, band) or _in(b, A))
            if x.get('loai') in LOAI_A: L1.append(dict(it, kieu='THÊM vật lớp (a)'))
            if x.get('thoi_dai_sai'):
                ny = x.get('nam_xuat_hien'); co_nam = isinstance(ny, (int, float)) and ny > float(nam)
                (L2 if (co_nam or (x.get('loai') in LOAI_HIEN_DAI and float(nam) < 1900)) else L2b).append(dict(it, ly_do=x.get('ly_do_thoi_dai'), nam=ny))
            if anh_tinh and x.get('loai') in LOAI_DONG: L4.append(it)
        for x in j.get('bot_doi') or []:
            if (x.get('do_tin') or 0) < TIN or x.get('loai') not in LOAI_A: continue
            b = hop(x); L1.append(dict(mh=mh, loai=x.get('loai'), mo_ta=x.get('mo_ta'), toa_do=b, dai_a=_in(b, band) or _in(b, A), kieu='BỚT/ĐỔI vật lớp (a)'))
        for x in j.get('doi_loai_vung') or []:
            if (x.get('do_tin') or 0) >= TIN: VUNG.append(dict(mh=mh, mo_ta=x.get('mo_ta'), toa_do=x.get('toa_do')))
    return L1, L2, L2b, L4, VUNG


def _trung(b1, b2):
    """hai hộp chuẩn hoá chồng nhau (hoặc tâm hộp này nằm trong hộp kia nở 0,02)"""
    if not b1 or not b2: return False
    return not (b1[2] < b2[0] - 0.02 or b2[2] < b1[0] - 0.02 or b1[3] < b2[1] - 0.02 or b2[3] < b1[1] - 0.02)


def qtd_moi(Qg, Qr, W=1920, H=1080):
    """q_thoi_dai (O2): nghi vấn trên khung ghép không trùng nghi vấn nào của render (đối chứng: lỗi sẵn có của render là việc của O2, không của N2+)"""
    nb = lambda x: [x['toa_do_px'][0] / W, x['toa_do_px'][1] / H, x['toa_do_px'][2] / W, x['toa_do_px'][3] / H] if x.get('toa_do_px') else None
    rr = [nb(y) for y in (Qr or {}).get('nghi_van') or []]
    return [x for x in (Qg or {}).get('nghi_van') or [] if not any(_trung(nb(x), y) for y in rr if y)]


def kiem_tam(t, ep_dir='.', vision=False, cache=None, out=None, noi='', t4=False, ppm=None):
    """một tấm (mục n2p.tam) → dict(do, V, ket luận, qtd, loi_chay). ppm: ngưỡng px/m nhà đo được của tập (1.17.6, tấm be_mat_nha_ai)"""
    from checks.ll import q_n2p_vision as QV
    rp, gp, mp = _p(ep_dir, t.get('render')), _p(ep_dir, t.get('ghep')), _p(ep_dir, t.get('mat_na'))
    nam = t.get('nam'); tid = str(t.get('id') or os.path.basename(gp or '?'))
    if not (rp and gp and mp and nam is not None): return dict(id=tid, loi_chay=f'tấm {tid}: thiếu render/ghep/mat_na/nam')
    TRU, TRU_GHI = None, None
    if t.get('be_mat_nha_ai'):   # 1.17.6 (KN-2): vùng nhà đo được nở 1 px do BE-MAT-NHA (a)(b) kiểm — loại khỏi (i)(a)(c); (a) còn lại giữ 0/255
        from checks.ll import q_k1176 as K76
        TRU, nd = K76.vung_bmn(t, ep_dir, ppm if ppm is not None else K76.PPM_MAC_DINH)
        TRU_GHI = f'{nd} nhà đo được (≥ {ppm if ppm is not None else K76.PPM_MAC_DINH:g} px/m) loại khỏi (a)' if TRU is not None else f'không tính được vùng BMN ({nd}) — (a) đo đủ'
    D = do_tam(rp, gp, mp, t.get('lop_a') or LOP_A, t.get('bang'), TRU)
    if TRU_GHI: D['i']['bmn'] = TRU_GHI
    SONG, VONG = None, None
    sg = t.get('song') or {}
    if sg or t.get('khop_mau_cuc_bo'):
        import cv2
        from checks.ll import q_k1175 as K75
        R_, G_ = cv2.imread(rp), cv2.imread(gp); Ab = K75.bao_ve(D['_A'])
        if sg:   # 1.17.5 (A3): lớp sống ghép bằng cộng hiệu render có/không — ngoài vùng bảo vệ ghép == clip(nền + (có − không))
            fs = {k: _p(ep_dir, sg.get(k)) for k in ('render_co', 'render_khong', 'nen')}
            if not all(fs.values()): SONG = dict(thieu='song: cần render_co, render_khong, nen')
            else:
                Rc, Rk, Pn = (cv2.imread(fs[k]) for k in ('render_co', 'render_khong', 'nen'))
                if any(x is None or x.shape != G_.shape for x in (Rc, Rk, Pn)): SONG = dict(thieu='song: ảnh thiếu hoặc khác cỡ ghép')
                else: mx, cnt = K75.kiem_song(G_, Pn, Rc, Rk, Ab); SONG = dict(max=mx, diem=cnt)
        if t.get('khop_mau_cuc_bo'):   # 1.17.5 (A4, cần K1175-D3): vòng bảo vệ = render-khớp + một độ lệch màu/vật
            res, off, k = K75.kiem_vong(G_, R_, D['_A'], Ab); VONG = dict(du=res, lech=off, vong=k)
    gv = _p(ep_dir, sg.get('nen')) if sg.get('nen') else gp   # (iv): lớp sống từ render không phải vật AI thêm → mô hình soi tấm nền (chưa cộng lớp sống)
    V = QV.soi(rp, gv, nam, t.get('noi', noi), t.get('t4', t4), out=out, tag=tid, api=vision, cache=cache)
    L1, L2, L2b, L4, VUNG = ket_luan(V.get('ket_qua') or {}, D['_band'], D['_A'], bool(t.get('anh_tinh', True)), nam)
    L1b = []
    if TRU is not None:   # 1.17.6 (KN-2): vật (a) mô hình báo có TÂM hộp trong vùng nhà đo được BMN → (c) người đọc (BE-MAT-NHA (c)/(w) kiểm vùng này)
        H_, W_ = TRU.shape; tam_ = lambda b: TRU[min(H_ - 1, max(0, int((b[1] + b[3]) / 2 * H_))), min(W_ - 1, max(0, int((b[0] + b[2]) / 2 * W_)))]
        L1b = [x for x in L1 if tam_(x['toa_do'])]; L1 = [x for x in L1 if not tam_(x['toa_do'])]
    Q = None
    if vision or (cache or {}).get('qtd', {}).get(tid):
        Q = (cache or {}).setdefault('qtd', {}).get(tid)
        if Q is None and vision:
            from checks.ll import q_thoi_dai as QT
            qc = (cache or {}).setdefault('o2', {}); od = os.path.join(out or '/var/tmp/n2p-qtd', 'qtd')
            Qg = QT.soi_khung(gp, nam, od, f'{tid}-ghep', t.get('noi', noi), True, qc); Qr = QT.soi_khung(rp, nam, od, f'{tid}-render', t.get('noi', noi), True, qc)
            Q = dict(ghep=Qg, render=Qr, moi=qtd_moi(Qg, Qr), loi='; '.join(x for x in (Qg.get('loi'), Qr.get('loi')) if x) or None,
                     chi_phi_usd=round(float(Qg.get('cost_usd') or 0) + float(Qr.get('cost_usd') or 0), 4))
            if cache is not None and not Q['loi']: cache['qtd'][tid] = Q
    return dict(id=tid, shot=t.get('shot'), nam=nam, anh_tinh=bool(t.get('anh_tinh', True)), do={k: v for k, v in D.items() if not k.startswith('_')},
                V=V, L1=L1, L1b=L1b, L2=L2, L2b=L2b, L4=L4, VUNG=VUNG, Q=Q, SONG=SONG, VONG=VONG)


def tong_tam(KT):
    """các tấm → hàng N2P-1…4"""
    out = {}
    m = lambda x: f"{x['mh']}: {x.get('loai')} «{str(x.get('mo_ta') or '')[:70]}» @{[round(v, 3) for v in x['toa_do']]}" + (' dải (a)' if x.get('dai_a') else '')
    L, T = {k: [] for k in ROWS[:4]}, {k: [] for k in ROWS[:4]}; M = {k: {} for k in ROWS[:4]}; near = {k: [] for k in ROWS[:4]}
    nv0, cum, t9, kn = 0, 0, [], 0
    for k in KT:
        w = f"tấm {k['id']}" + (f" ({k['shot']})" if k.get('shot') else '')
        if k.get('loi_chay'):
            for q in ROWS[:4]: T[q].append(('(a) ' if q == 'N2P-1' else '') + k['loi_chay'])
            continue
        i = k['do']['i']; iii = k['do']['iii']; vl = (k['V'] or {}).get('loi')
        if i['max_trong_a'] > 0: L['N2P-1'].append(f"(a) {w}: lớp (a) sau ghép lệch tối đa {i['max_trong_a']}/255 ở {i['diem_lech_trong_a']} điểm (cần 0)")
        L['N2P-1'] += [f'(b) {w}: {x["kieu"]} — {m(x)}' for x in k['L1']]
        L['N2P-1'] += [f'(c) {w}: {x["kieu"]} trong vùng nhà đo được BMN (BE-MAT-NHA kiểm; người đọc) — {m(x)}' for x in k.get('L1b') or []]
        if i['dai20_cum_dE30']:
            cum += i['dai20_cum_dE30']; L['N2P-1'].append(f"(c) {w}: {i['dai20_cum_dE30']} cụm ΔE ≥ {CUM_DE:g} trong dải {DAI_PX} px quanh (a) (người đọc tờ so): "
                                                         + ', '.join(f"{c['hop']} {c['px']} px" for c in i['dai20_cum_lon'][:4]))
        sg, vg = k.get('SONG'), k.get('VONG')
        if sg is not None:
            if sg.get('thieu'): T['N2P-1'].append(f"(e) {w}: {sg['thieu']}")
            elif sg['max'] > 1: L['N2P-1'].append(f"(e) {w}: lớp sống ≠ clip(nền + (render có − render không)) — sai lớn nhất {sg['max']}/255 ở {sg['diem']} điểm (dán nguyên/lệch khung/sai cường độ)")
        if vg is not None and (vg['du'] > 1 or vg['lech'] > K75_VONG_MAX):
            L['N2P-1'].append(f"(d) {w}: vòng bảo vệ không phải render-khớp + một độ lệch/vật — phần dư {vg['du']:.0f}/255, độ lệch {vg['lech']:.0f} (trần {K75_VONG_MAX})")
        L['N2P-2'] += [f"(a) {w}: lỗi thời đại — {m(x)} — năm {x.get('nam')} · {str(x.get('ly_do') or '')[:80]}" for x in k['L2']]
        nv0 += len(k['L2b'])
        if k.get('Q') is not None:
            if k['Q'].get('loi'): T['N2P-2'].append(f"(b) {w}: q_thoi_dai: {k['Q']['loi']}")
            L['N2P-2'] += [f"(b) {w}: q_thoi_dai nghi vấn mới (không có ở render): [{x.get('muc')}] {str(x.get('mo_ta'))[:70]} @px {x.get('toa_do_px')}" for x in k['Q']['moi']]
        c9 = iii.get('t9c')
        if c9 is not None and c9.get('ap') is False: kn += 1   # 1.17.6 (KN-1): tấm không nước → T9c KHÔNG ÁP, phép khác vẫn chạy
        for nm, v in (('đất→nước', iii['t9b_dat_thanh_nuoc_pct']), ('nước→đất', iii['t9b_nuoc_thanh_dat_pct'])):
            if c9 is not None and nm == 'nước→đất': continue   # 1.17.5: chiều nước→đất đo bằng T9c (đường bờ + đối chứng render); T9b chỉ in
            t9.append(v); near['N2P-3'] += sat(f'{w} T9b {nm} %', v, T9B_MAX)
            if v > T9B_MAX: L['N2P-3'].append(f'(a) {w}: T9b {nm} {v} % > {T9B_MAX:g} %')
        if c9 is not None and c9.get('ap') is not False:
            L['N2P-3'] += [f"(c) {w}: bờ lấn ({x['kieu']}) sâu {x['sau_px']} px @1080" + (f", dài {x['dai_px']} px, x {x['x0']}–{x['x1']}" if 'x0' in x else f", hộp {x['hop']}") for x in c9['lan'][:8]]
            if c9['giua_pct'] > K75_GIUA: L['N2P-3'].append(f"(d) {w}: khác nước (đối chứng render) không bám bờ {c9['giua_pct']} % > {K75_GIUA:g} %")
            near['N2P-3'] += sat(f'{w} T9c giữa nước %', c9['giua_pct'], K75_GIUA)
        L['N2P-3'] += [f"(b) {w}: {x['mh']} báo đổi loại vùng «{str(x.get('mo_ta') or '')[:70]}»" for x in k['VUNG']]
        L['N2P-4'] += [f'(a) {w}: vật chuyển động trên tấm tĩnh — {m(x)}' for x in k['L4']]
        if vl:
            for q in ('N2P-1', 'N2P-2', 'N2P-3', 'N2P-4'): T[q].append(('(b) ' if q == 'N2P-1' else '') + f'{w}: mô hình nhìn — {vl}')
    n = sum(1 for k in KT if not k.get('loi_chay'))
    out['N2P-1'] = r(L['N2P-1'], T['N2P-1'], val=f"{n} tấm · max lệch (a) {max([k['do']['i']['max_trong_a'] for k in KT if not k.get('loi_chay')] or [0])}/255 · vật (a) mô hình {sum(len(k.get('L1') or []) for k in KT)} · cụm dải 20 px {cum}")
    out['N2P-2'] = r(L['N2P-2'], T['N2P-2'], val=f"{n} tấm · lỗi có năm {sum(len(k.get('L2') or []) for k in KT)} · nghi vấn không năm {nv0} (người đọc) · q_thoi_dai mới "
                                                  + str(sum(len(k['Q']['moi']) for k in KT if k.get('Q'))) + ' · giới hạn: cờ ~20 px không bảo đảm')
    c9s = [k['do']['iii']['t9c'] for k in KT if not k.get('loi_chay') and k['do']['iii'].get('t9c') is not None and k['do']['iii']['t9c'].get('ap') is not False]
    out['N2P-3'] = r(L['N2P-3'], T['N2P-3'], val=f"{n} tấm · T9b lớn nhất {max(t9 or [0]):.2f} % · mô hình báo {sum(len(k.get('VUNG') or []) for k in KT)}"
                     + (f" · T9c (1.17.5): đoạn bờ lấn {sum(c['so_doan_lan'] for c in c9s)}, sâu nhất {max([c['sau_lon_nhat_px'] for c in c9s] or [0])} px, giữa nước ≤ {max([c['giua_pct'] for c in c9s] or [0])} %"
                        + f"; T9b nước→đất (chỉ in) {max([k['do']['iii']['t9b_nuoc_thanh_dat_pct'] for k in KT if not k.get('loi_chay')] or [0]):.2f} %" if c9s else '')
                     + (f" · T9c KHÔNG ÁP ở {kn} tấm không nước (1.17.6 KN-1)" if kn else ''), sat_nguong=near['N2P-3'])
    if kn and kn == n and out['N2P-3']['ok']: out['N2P-3']['ket_qua'] = 'KHÔNG ÁP'   # mọi tấm không nước, T9b đất→nước + mô hình 0 lỗi
    out['N2P-4'] = r(L['N2P-4'], T['N2P-4'], val=f"{n} tấm ({sum(1 for k in KT if k.get('anh_tinh'))} tĩnh) · vật chuyển động {sum(len(k.get('L4') or []) for k in KT)}")
    for q in ROWS[:4]:
        out[q]['muc'] = {c: [x for x in out[q]['loi'] if x.startswith(f'({c})')] for c in 'abcde'}
    return out


# ================================================================ (v) video: nhấp nháy + chuyển tấm
def _frames(mp4, W=480, H=270):
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', mp4, '-map', '0:v:0', '-vf', f'scale={W}:{H}:flags=area', '-pix_fmt', 'bgr24', '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def _fps(mp4):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', mp4], capture_output=True, text=True).stdout.strip()
    a, _, b = o.partition('/'); return float(a) / float(b or 1)


def do_video(ghep, render, mat_na, chuyen=(), lop_a=LOP_A, bang=None):
    """→ dict(buoc_max ΔE/khung, buoc_tai s, nhap_ghep, nhap_render) trên lớp (c) = ngoài (a) của mặt nạ khung đầu (máy cố định)"""
    import cv2, numpy as np
    G = _frames(ghep); Rr = _frames(render); n = min(len(G), len(Rr)); fps = _fps(ghep)
    L, names = idmap(mat_na, (G.shape[2], G.shape[1]), bang); C = ~lop(L, names, lop_a)
    C = cv2.erode(C.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    lab = [(_lab(f))[C] for f in G[:n]]; dE = [float(np.sqrt(((lab[i + 1] - lab[i]) ** 2).sum(-1)).mean()) for i in range(n - 1)]
    gg = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)[C] for f in G[:n]]; gr = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)[C] for f in Rr[:n]]
    win = [(float(c.get('t', 0)) - 0.5, float(c.get('t', 0)) + float(c.get('dur') or 0) + 0.5) for c in chuyen or []]
    ngoai = [i for i in range(n - 1) if not any(a <= (i + 0.5) / fps <= b for a, b in win)]
    fl = lambda F: float(np.mean([np.abs(F[i + 1] - F[i]).mean() for i in ngoai])) if ngoai else 0.0
    i_max = int(np.argmax(dE)) if dE else 0
    return dict(khung=n, fps=round(fps, 3), buoc_max=round(max(dE or [0]), 3), buoc_tai_s=round((i_max + 1) / fps, 3), buoc_trung_vi=round(statistics.median(dE), 4) if dE else 0,
                nhap_ghep=round(fl(gg), 4), nhap_render=round(fl(gr), 4), lop_c_pct=round(float(C.mean() * 100), 1))


def n2p5(E, LS, ep_dir='.', vids=None):
    """(v) — vids: số đo đã có {shot: do_video} (selftest) hoặc None (đo từ n2p.video)"""
    N = E.get('n2p') or {}; V = list(N.get('video') or []); loi, th, near, rows = [], [], [], []
    shots_nen = [s for s in LS or [] if s.get('ai_nen')]
    if not shots_nen and not V: return na('không shot tấm nền (log ai_nen) và không khai n2p.video')
    by = {str(v.get('shot')): v for v in V}
    for s in shots_nen:
        sid = str(s.get('shot')); v = by.get(sid) or {}
        ch = v.get('chuyen_tam') if v.get('chuyen_tam') is not None else (s['ai_nen'].get('chuyen_tam') if isinstance(s['ai_nen'], dict) else None)
        for c in ch or []:
            if str(c.get('kieu') or '') != 'hoa': loi.append(f"(a) {sid} @{c.get('t')} s: chuyển tấm kiểu {c.get('kieu')!r} (chỉ hoà ≥ {HOA_MIN:g} s)")
            elif float(c.get('dur') or 0) < HOA_MIN - 1e-6: loi.append(f"(a) {sid} @{c.get('t')} s: hoà {float(c.get('dur') or 0):.2f} s < {HOA_MIN:g} s")
            else: near += sat(f'{sid} hoà s', float(c['dur']), HOA_MIN)
        d = (vids or {}).get(sid)
        if d is None and v.get('ghep') and v.get('render') and v.get('mat_na'):
            try: d = do_video(_p(ep_dir, v['ghep']), _p(ep_dir, v['render']), _p(ep_dir, v['mat_na']), ch or [], v.get('lop_a') or LOP_A, v.get('bang'))
            except Exception as e: th.append(f'{sid}: đo video lỗi: {type(e).__name__}: {e}'); continue   # noqa: BLE001
        if d is None: th.append(f'{sid}: shot tấm nền chưa có video đo (n2p.video: ghep + render đối chứng + mat_na)'); continue
        lim = max(NHAP_K * d['nhap_render'], SAN_NHAP)
        rows.append(f"{sid}: bước {d['buoc_max']} ΔE/khung @{d['buoc_tai_s']} s · nhấp nháy {d['nhap_ghep']} (đối chứng {d['nhap_render']}, trần {lim:.4f})")
        if d['buoc_max'] > BUOC_MAX: loi.append(f"(b) {sid}: bước nhảy {d['buoc_max']} ΔE/khung @{d['buoc_tai_s']} s > {BUOC_MAX:g} (chuyển tấm không hoà / tấm nhảy)")
        near += sat(f'{sid} bước ΔE/khung', d['buoc_max'], BUOC_MAX)
        if d['nhap_ghep'] > lim + 1e-9: loi.append(f"(c) {sid}: nhấp nháy {d['nhap_ghep']} mức xám/khung > {lim:.4f} (= max({NHAP_K:g} × đối chứng {d['nhap_render']}, sàn {SAN_NHAP:g}))")
        near += sat(f'{sid} nhấp nháy', d['nhap_ghep'], round(lim, 4))
    for sid in by:
        if sid not in {str(s.get('shot')) for s in shots_nen}: th.append(f'{sid}: n2p.video khai nhưng log shot không có ai_nen')
    return r(loi, th, val=f"{len(shots_nen)} shot tấm nền · " + (' · '.join(rows[:6]) or 'chưa đo'), sat_nguong=near, chi_tiet=rows,
             muc={c: [x for x in loi if x.startswith(f'({c})')] for c in 'abc'})


# ================================================================ (vi) trần §15(d)
def _dur(s):
    if isinstance(s.get('dur'), (int, float)): return float(s['dur'])
    if isinstance(s.get('t1'), (int, float)) and isinstance(s.get('t0'), (int, float)): return float(s['t1']) - float(s['t0'])
    return 0.0


def n2p6(E, LS, tong_s=None):
    """1.17.4 (Q2, chủ dự án 23/10/2026 21:45): (b) trần minh hoạ 20 % BỎ cho tập từ T4 (mọi tập vào N2P đều từ T4) — chỉ ghi %; giới hạn thay thế:
    GEMINI-NGAN-SACH (ngân sách Gemini của tập), (c) tổng AI ≤ 70 % (giữ), GOC-CAO-60 (q_k1174)."""
    if not LS: return r(thieu=['không có log shot (`log_shot`) — không đọc được ai_nen / minh_hoa'], val='—')
    T = float(tong_s) if tong_s else sum(_dur(s) for s in LS)
    nen = [s for s in LS if s.get('ai_nen')]; mh = [s for s in LS if s.get('minh_hoa')]
    ai = [s for s in LS if s.get('ai_nen') or s.get('minh_hoa') or s.get('ai_image') or s.get('ai_texture')]
    pn, pm, pt = (100 * sum(_dur(s) for s in x) / T if T else 0.0 for x in (nen, mh, ai))
    loi, near = [], []
    if pn > TRAN_NEN + 1e-9: loi.append(f'(a) tấm nền N2+ {pn:.1f} % > {TRAN_NEN:g} % thời lượng ({len(nen)} shot)')
    if pt > TRAN_TONG + 1e-9: loi.append(f'(c) tổng khung có AI {pt:.1f} % > {TRAN_TONG:g} % ({len(ai)} shot)')
    loi += [f"(d) {s.get('shot')}: vừa ai_nen vừa minh_hoa (chồng shot — mỗi shot một loại)" for s in LS if s.get('ai_nen') and s.get('minh_hoa')]
    near += sat('tấm nền %', round(pn, 2), TRAN_NEN) + sat('tổng AI %', round(pt, 2), TRAN_TONG)
    return r(loi, val=f'{T:.1f} s · tấm nền {pn:.1f} % ({len(nen)}) · minh hoạ {pm:.1f} % ({len(mh)}; không trần cứng từ 1.17.4 — Q2) · tổng AI {pt:.1f} % ({len(ai)})', sat_nguong=near,
             muc={c: [x for x in loi if x.startswith(f'({c})')] for c in 'abcd'}, pct=dict(nen=round(pn, 2), minh_hoa=round(pm, 2), tong=round(pt, 2)))


# ================================================================ cả bộ
def check(E, TL=None, ep_dir='.', LS=None, vision=False, out=None, KT=None, vids=None):
    """→ {N2P-1…6: hàng}. KT: kết quả kiem_tam đã có (selftest); không có → chạy kiem_tam trên n2p.tam."""
    if not ap_n2p(E): return {k: na('tập trước T4 (không khai kenh2_tu_t4 / n2p): giữ hành vi 1.16.1') for k in ROWS}
    N = E.get('n2p') or {}; out = out or E.get('out'); cp = os.path.join(out, 'n2p-vision-cache.json') if out else None
    cache = json.load(open(cp)) if cp and os.path.exists(cp) else {}
    res = {}
    tam = list(N.get('tam') or [])
    from checks.ll import q_k1176 as K76
    ppm = K76.ppm_min(E)[0]
    if KT is None and tam:
        KT = []
        for t in tam:
            try: KT.append(kiem_tam(t, ep_dir, vision, cache, out, N.get('noi', ''), bool(N.get('t4')), ppm))
            except Exception as e: KT.append(dict(id=str(t.get('id')), loi_chay=f"tấm {t.get('id')}: {type(e).__name__}: {e}"))   # noqa: BLE001
        if cp and vision:
            os.makedirs(out, exist_ok=True); json.dump(cache, open(cp, 'w'), ensure_ascii=False, indent=1)
    if KT: res.update(tong_tam(KT))
    else:
        nen = [s for s in LS or [] if s.get('ai_nen')]
        for k in ROWS[:4]:
            res[k] = (r(thieu=[('(a) ' if k == 'N2P-1' else '') + f"{len(nen)} shot ai_nen nhưng chưa khai tấm kiểm (n2p.tam)"], val='—') if nen
                      else na('không có tấm nền AI (n2p.tam / log ai_nen)'))
    res['N2P-5'] = n2p5(E, LS, ep_dir, vids)
    res['N2P-6'] = n2p6(E, LS, (TL or {}).get('tong_s'))
    cong = 'animatic' if E.get('animatic') else 'G2'
    return {k: dict(v, cong=cong) for k, v in res.items()}


def _main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    if g('render'):
        t = dict(id=g('tag') or 'khung', render=g('render'), ghep=g('ghep'), mat_na=g('mat-na'), nam=int(g('nam')), anh_tinh=(g('anh-tinh') or '1') != '0')
        cache, out = {}, g('out') or '/var/tmp/n2p-kiem'
        cp = os.path.join(out, 'n2p-vision-cache.json')
        if os.path.exists(cp): cache = json.load(open(cp))
        K = kiem_tam(t, '.', '--vision' in a, cache, out, g('noi') or '', '--t4' in a)
        if '--vision' in a: os.makedirs(out, exist_ok=True); json.dump(cache, open(cp, 'w'), ensure_ascii=False, indent=1)
        R = tong_tam([K])
    else:
        E = base.load(a[0]); ep_dir = os.path.dirname(os.path.abspath(a[0])); TL = json.load(open(g('tl'))) if g('tl') else None
        lp = _p(ep_dir, E.get('log_shot')); LS = json.load(open(lp)) if lp and os.path.exists(lp) else None
        LS = LS.get('shots') if isinstance(LS, dict) else LS
        R = check(E, TL, ep_dir, LS, '--vision' in a)
    for k, v in R.items():
        print(f"{k}: {v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')} · {v['val']}" + ''.join(f'\n  {x}' for x in (v['loi'] + (v.get('thieu') or []))[:20]))
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1, default=str)
    sys.exit(0 if all(v['ok'] for v in R.values()) else 1)


if __name__ == '__main__':
    _main()
