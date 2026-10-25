#!/opt/cine/bin/python
"""Luật 1.17.6 (phiên K-1.17.6, 24/10/2026) — CHỈ tập kênh 2 từ T4 (`kenh2_tu_t4: true` hoặc khối `n2p:`). T3 và trước: KHÔNG ÁP (không hồi tố).
Căn cứ: khiếu nại THU-B-T4 KN-1…KN-6 (checks-appeal.md, mục K-1.17.6; nguồn `reports/thu-b-t4/khieu-nai-K.md` @353d0f0c); chủ dự án
24/10/2026 12:52 "Duyệt cách kết hợp tư liệu theo khuyến nghị" (T4: trần tư liệu + khắc + thẻ 15 %; tư liệu chỉ chồng shot 3D, không chồng/ghép
liền clip Omni; mỗi lần ≤ 10 s) và 15:25 (phiếu THU-B "theo khuyến nghị": B chỉ ở nhà ≥ 4 px/m). Số đo, tiêu chí đặt trước: reports/k1176/.

KN-1 (N2P-3): tấm KHÔNG NƯỚC (mặt nạ không có lớp nước hoặc nước < 0,2 % khung) → T9c "KHÔNG ÁP" (q_k1175.t9c trả đủ khoá, `ap: False`);
     các phép khác vẫn chạy. Mọi tấm không nước và không lỗi khác → hàng N2P-3 "KHÔNG ÁP".
KN-2 (N2P-1 (i)): tấm `be_mat_nha_ai: true` → mặt nạ (a) của (i)(a) và dải 20 px của (i)(c) TRỪ vùng "nhà đo được nở 1 px" (vung_bmn — cùng định
     nghĩa BE-MAT-NHA (a)(b)); mọi điểm (a) còn lại (kể cả nhà thường KHÔNG đo được) giữ 0/255.
KN-3 (mô hình nhìn): Claude không đọc đủ ảnh → tự gọi lại MỘT lần (goi_claude_du); cả hai lần ghi vào <out>/n2p-cost.jsonl (`lan`, `goi_lai`).
KN-4 (BE-MAT-NHA (w)): canh_moi — cạnh màu MỚI trong lòng nhà đo được không có ở render và pass bóng (ống khói/đầu hồi AI vẽ thêm). CHỈ BÁO.
KN-5 (BE-MAT-NHA (d)): quỹ đạo sáng đo THEO ĐIỂM ẢNH: e_h = max_t |trung vị_{p ∈ lõi nhà h} [ln(C_p(t)/C_p(0)) − ln(R_p(t)/R_p(0))]| (quy_dao_px).
KN-6 (BE-MAT-NHA (e)): khung 0 so ở ĐỘ PHÂN GIẢI VIDEO (tấm thu INTER_AREA, mặt nạ thu NEAREST về cỡ video).
B ≥ 4 px/m (15:25): BE-MAT-NHA (a) đọc `be_mat_nha_px_m_min` của tập (mặc định 2; < 2 không nhận) — nhà dưới ngưỡng không đo được → (b) = render.
TU-LIEU (12:52): TU-LIEU-10 đọc `tu_lieu_tran_pct` (mặc định 10; > 15 không nhận — trần cao nhất chủ dự án đã duyệt), thêm (b) mỗi lần ≤ 10 s;
     hàng mới TU-LIEU-OMNI: (a) tư liệu (lớp TL/KHAC/THE/MAP) không trùng thời gian clip M-d (`minh_hoa`); (b) không ghép liền: giữa lần tư liệu và
     clip M-d có ≥ 1 shot 3D hoặc ≥ 1 s 3D (hoà qua 3D).
1.17.7 (chủ dự án 25/10/2026 09:15, gói "50 % tiết kiệm"): `tu_lieu_tran_pct` nhận tới 20 (T4 khai 20; > 20 không nhận); lớp mới THAT (ảnh chụp /
     footage thật) tính vào tư liệu ở TU-LIEU-10 (a)(b) và TU-LIEU-OMNI (không tính AI, không tính góc cao — q_k1177). Tập không khai: như 1.17.6.
"""
import json, os, sys, time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

PPM_MAC_DINH, PPM_SAN = 2.0, 2.0          # be_mat_nha_px_m_min: mặc định 2 (1.17.5); không nhận < 2
TU_LIEU_MAC_DINH, TU_LIEU_TRAN_DUYET = 10.0, 20.0   # tu_lieu_tran_pct: mặc định 10 (§19 c); cao nhất chủ dự án duyệt 20 (T4, 25/10 09:15; trước: 15, 24/10 12:52)
TU_LIEU_LAN_S = 10.0                       # mỗi lần tư liệu ≤ 10 s
GHEP_LIEN_S = 1.0                          # khoảng 3D tối thiểu giữa tư liệu và clip M-d khi không có shot 3D xen giữa
LOP_TU_LIEU = ('TL', 'KHAC', 'THE', 'MAP', 'THAT')   # 1.17.7: + THAT (ảnh chụp/footage thật)
LOP_TRAN = ('TL', 'KHAC', 'THE', 'THAT')            # lớp tính vào trần tư liệu (a); MAP tính ở BAN-DO-12
D_LOI_MIN_PX = 4                           # (d) nhà cần ≥ 4 điểm lõi ở độ phân giải video mới tính quỹ đạo


def ap_1176(E): return bool(E.get('kenh2_tu_t4') or E.get('n2p'))


def _num(x): return isinstance(x, (int, float)) and not isinstance(x, bool)


# ================================================================ ngưỡng B ≥ 4 px/m (15:25)
def ppm_min(E):
    """→ (ngưỡng px/m của BE-MAT-NHA (a), lỗi khai | None). Khai ở gốc episode.yaml hoặc trong khối n2p."""
    v = E.get('be_mat_nha_px_m_min', (E.get('n2p') or {}).get('be_mat_nha_px_m_min'))
    if v is None: return PPM_MAC_DINH, None
    if not _num(v): return PPM_MAC_DINH, f'be_mat_nha_px_m_min {v!r} không phải số — dùng {PPM_MAC_DINH:g}'
    if float(v) < PPM_SAN: return PPM_SAN, f'be_mat_nha_px_m_min {v:g} < {PPM_SAN:g} (sàn đo được của thước (a)) — dùng {PPM_SAN:g}'
    return float(v), None


# ================================================================ KN-2: nhà đo được (cùng định nghĩa q_k1175.hinh_khoi)
def nha_do(R, B, I, PID, nha, p):
    """→ set mã nhà ĐO ĐƯỢC: px_m ≥ PPM_MIN, ≥ A_MIN px (quy 1080p), ≥ N_MIN điểm cạnh hình học thấy được ở render (Lab) VÀ pass bóng (L*)."""
    import numpy as np
    from checks.ll import q_k1175 as K75
    H = I.shape[0]; s = H / 1080.0
    gR = K75._grad(R, p['SIG'] * s, True); gB = K75._grad(B, p['SIG'] * s) if B is not None else gR
    GE = (K75._bien(I) | (K75._bien(PID) if PID is not None else False)) & (gR >= p['T_VIS']) & (gB >= p['T_VIS'])
    ids, cnt = np.unique(I.ravel(), return_counts=True); nc = dict(zip(*np.unique(I[GE], return_counts=True)))
    out = set()
    for h, a in zip(ids.tolist(), cnt.tolist()):
        if h == 0: continue
        ppm = float((nha.get(h) or {}).get('px_m') or 0)
        if a < p['A_MIN'] * s * s or ppm < p['PPM_MIN']: continue
        if nc.get(h, 0) < p['N_MIN'] * s: continue
        out.add(int(h))
    return out


def chuan_bi_bmn(t, ep_dir='.'):
    """đọc tấm be_mat_nha_ai → dict(R, G, B, L, names, I, PID, nha) như q_k1175.kiem_bmn; thiếu tệp → None"""
    import cv2
    from checks.ll import q_k1175 as K75, q_n2p as N
    f = {k: K75._p(ep_dir, t.get(k)) for k in ('render', 'ghep', 'mat_na', 'mat_na_nha', 'mat_na_mat', 'bong', 'nha')}
    if any(not f[k] or not os.path.exists(f[k]) for k in ('render', 'ghep', 'mat_na', 'mat_na_nha', 'bong', 'nha')): return None
    R, G, B = cv2.imread(f['render']), cv2.imread(f['ghep']), cv2.imread(f['bong']); H, W = R.shape[:2]
    if G is None or B is None or G.shape != R.shape or B.shape != R.shape: return None
    L, names = N.idmap(f['mat_na'], (W, H), dict({'nha_thuong': K75.NHA_THUONG}, **(t.get('bang') or {})))
    I = K75._ma(f['mat_na_nha'], (W, H)); I[L != names.index('nha_thuong')] = 0
    PID = K75._ma(f['mat_na_mat'], (W, H)) if f['mat_na_mat'] and os.path.exists(f['mat_na_mat']) else None
    if PID is not None: PID[I == 0] = 0
    nha = {int(x['id']): x for x in json.load(open(f['nha']))}
    return dict(R=R, G=G, B=B, L=L, names=names, I=I, PID=PID, nha=nha, f=f)


def vung_bmn(t, ep_dir='.', ppm=PPM_MAC_DINH):
    """KN-2 → (mặt nạ nhà đo được nở 1 px (3×3, như BE-MAT-NHA (b)), số nhà đo được) | (None, lý do)"""
    import cv2, numpy as np
    from checks.ll import q_k1175 as K75
    D = chuan_bi_bmn(t, ep_dir)
    if D is None: return None, 'thiếu tệp be_mat_nha (render/ghep/mat_na/mat_na_nha/bong/nha) hoặc khác cỡ'
    do = nha_do(D['R'], D['B'], D['I'], D['PID'], D['nha'], dict(K75.BMN, PPM_MIN=ppm))
    return cv2.dilate(np.isin(D['I'], list(do)).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0, len(do)


# ================================================================ KN-4: (w) cạnh màu mới trong lòng nhà (ống khói/đầu hồi AI vẽ thêm) — CHỈ BÁO
CM = dict(SIG=1.0, NB=12, T_A=8.0, T_O=5.0, RAD=2, L_M=1.0, A_M=0.5, IN_TOP=8)   # điểm vận hành chọn trên B3 l1/l2 (reports/k1176 §KN-4)


def _gxy(b, sig, mau=True):
    """độ lớn gradient (kênh Lab mạnh nhất, mờ σ) + hướng 0–180° của kênh đó"""
    import cv2, numpy as np
    x = cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32), (0, 0), sig)
    G = np.zeros(x.shape[:2], np.float32); GX = np.zeros_like(G); GY = np.zeros_like(G)
    for c in (range(3) if mau else (0,)):
        sx = cv2.Sobel(x[..., c], cv2.CV_32F, 1, 0, ksize=3) / 8; sy = cv2.Sobel(x[..., c], cv2.CV_32F, 0, 1, ksize=3) / 8; m = np.sqrt(sx * sx + sy * sy)
        u = m > G; GX[u] = sx[u]; GY[u] = sy[u]; G = np.maximum(G, m)
    return G, np.degrees(np.arctan2(GY, GX)) % 180


def canh_moi(R, G, B, I, do, nha, p=None):
    """KN-4 → danh sách thành phần [{hop, px, m, nha, ppm}] sắp theo độ dài cạnh (m). Điểm cạnh MỚI = cạnh màu ảnh ghép ≥ T_A (ΔE/px, mờ σ 1)
    KHÔNG được giải thích bởi cạnh render (Lab) hay pass bóng (L*) ≥ T_O CÙNG HƯỚNG (±1 ngăn 15°) trong RAD px, trong lòng nhà đo được (co 1 px).
    Thành phần (đóng 3×3) giữ khi cạnh dài ≥ L_M m và ≥ A_M·px_m điểm. Không theo mã nhà: ống khói AI vẽ đè lên nhiều nhà ở xa (3D phía sau)."""
    import cv2, numpy as np
    p = dict(CM, **(p or {})); s = I.shape[0] / 1080.0; NB = p['NB']; sig = p['SIG'] * s
    M = np.isin(I, list(do)); Mi = cv2.erode(M.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    gA, tA = _gxy(G, sig); bA = (tA / (180 / NB)).astype(int) % NB
    ER = [np.zeros(I.shape, bool) for _ in range(NB)]
    for g, t in (_gxy(R, sig), _gxy(B, sig, False)):
        b = (t / (180 / NB)).astype(int) % NB
        for k in range(NB): ER[k] |= (g >= p['T_O']) & (b == k)
    ker = np.ones((2 * p['RAD'] + 1,) * 2, np.uint8); expl = np.zeros(I.shape, bool)
    for k in range(NB): expl |= (bA == k) & (cv2.dilate((ER[k] | ER[(k - 1) % NB] | ER[(k + 1) % NB]).astype(np.uint8), ker) > 0)
    new = cv2.morphologyEx(((gA >= p['T_A']) & ~expl & Mi).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)) > 0
    PPM = np.zeros(I.shape, np.float32)
    for h in do: PPM[I == h] = float((nha.get(h) or {}).get('px_m') or 0)
    n, cc, st, _ = cv2.connectedComponentsWithStats(new.astype(np.uint8), 8); out = []
    for i in range(1, n):
        x, y, w, h, a = (int(v) for v in st[i]); mm = cc == i; pp = PPM[mm]; pp = pp[pp > 0]
        if not len(pp): continue
        ppm = float(np.median(pp))
        if max(w, h) >= p['L_M'] * ppm and a >= p['A_M'] * ppm:
            out.append(dict(hop=[x, y, x + w, y + h], px=a, m=round(a / ppm, 1), ppm=round(ppm, 2), nha=int(np.bincount(I[mm]).argmax())))
    return sorted(out, key=lambda z: -z['m'])


# ================================================================ KN-5: (d) quỹ đạo sáng theo điểm ảnh
def _Y(f):
    import numpy as np
    x = f.astype(np.float32) / 255; x = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
    return 0.0722 * x[..., 0] + 0.7152 * x[..., 1] + 0.2126 * x[..., 2]


def loi_nha(IID):
    """điểm LÕI của mỗi nhà: cùng mã với 4 điểm kề (bỏ mép — khử răng cưa/viền ghép)"""
    import numpy as np
    c = IID > 0; P = np.pad(IID, 1, mode='edge')
    for dy, dx in ((0, 1), (2, 1), (1, 0), (1, 2)): c &= P[dy:dy + IID.shape[0], dx:dx + IID.shape[1]] == IID
    return c


Y_SAN = 0.01                               # (d) sàn độ sáng Y tuyến tính (≈ sRGB 25/255): dưới sàn ở khung t hoặc 0 → điểm bỏ ở khung đó (lượng tử 8 bit)


def quy_dao_px(Cs, Rs, IID, eps=1e-3, y_san=None):
    """(d) KN-5 → dict(e_h {id: e}, n_loi {id: điểm lõi}, bo_nho [id]). Mỗi điểm lõi: d_p(t) = ln((C_p(t)+ε)/(C_p(0)+ε)) − ln((R_p(t)+ε)/(R_p(0)+ε))
    (độ sáng tuyến tính Y); m_h(t) = trung vị d_p(t) trên lõi nhà h; e_h = max_t |m_h(t)|. Dựng lại ánh sáng đúng (C = albedo AI × bóng(t)) → d ≡ 0
    bất kể AI phân bố lại độ sáng bề mặt; dán ảnh tĩnh → d = −ln(R(t)/R(0)) (trượt khi nắng đổi)."""
    import numpy as np
    core = loi_nha(IID); idv = IID[core]; o = np.argsort(idv, kind='stable'); ids, st, ct = np.unique(idv[o], return_index=True, return_counts=True)
    ys = Y_SAN if y_san is None else y_san
    keep = ct >= D_LOI_MIN_PX; yc0 = _Y(Cs[0])[core][o]; yr0 = _Y(Rs[0])[core][o]; lc0 = np.log(yc0 + eps); lr0 = np.log(yr0 + eps)
    M = np.zeros((len(Cs), len(ids)), np.float64)
    for t in range(1, len(Cs)):
        yc, yr = _Y(Cs[t])[core][o], _Y(Rs[t])[core][o]
        d = (np.log(yc + eps) - lc0) - (np.log(yr + eps) - lr0)
        ok = np.minimum(np.minimum(yc, yc0), np.minimum(yr, yr0)) >= ys   # bỏ điểm dưới sàn ở khung này (lượng tử 8 bit vô nghĩa)
        for j in np.nonzero(keep)[0]:
            seg = slice(st[j], st[j] + ct[j]); v = d[seg][ok[seg]]
            if len(v) >= D_LOI_MIN_PX: M[t, j] = np.median(v)
    e = np.abs(M).max(0)
    return dict(e_h={int(h): round(float(v), 4) for h, v, k in zip(ids, e, keep) if k}, n_loi={int(h): int(c) for h, c in zip(ids, ct)},
                bo_nho=[int(h) for h, k in zip(ids, keep) if not k])


Y_SAN_NHAP_MAC_DINH = 0.0                  # 1.17.7 (K1176-D6): sàn Y của thước nhấp nháy (d) theo tập — mặc định 0 (như 1.17.6); T4 khai 0,01 (= sàn (d))


def y_san_nhap(E):
    """`be_mat_nha_y_san_nhap` (gốc episode.yaml hoặc khối n2p): số 0–0,05; khác → mặc định 0 (như 1.17.6)"""
    v = E.get('be_mat_nha_y_san_nhap', (E.get('n2p') or {}).get('be_mat_nha_y_san_nhap'))
    return float(v) if _num(v) and 0 <= float(v) <= 0.05 else Y_SAN_NHAP_MAC_DINH


def nhap_nhay_san(Cs, Rs, IID, y_san):
    """(d) nhấp nháy bề mặt CÓ SÀN Y (K1176-D6): ε_t = ln Y(ghép_t) − ln Y(render_t) (mờ σ 1) trên lõi vùng nhà (xói 3×3); cặp (t, t+1) chỉ lấy
    điểm có Y ≥ y_san ở ghép và render cả hai khung (lượng tử 8 bit gần đen vô nghĩa); TB |ε_{t+1} − ε_t| rồi TB theo cặp. y_san = 0 → đúng
    thước 1.17.5/1.17.6 (q_k1175.quy_dao)."""
    import cv2, numpy as np
    M = cv2.erode((IID > 0).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    Yc = [_Y(c) for c in Cs]; Yr = [_Y(r) for r in Rs]
    eps = [cv2.GaussianBlur(np.log(yc + 1e-3) - np.log(yr + 1e-3), (0, 0), 1.0) for yc, yr in zip(Yc, Yr)]
    v = []
    for i in range(len(eps) - 1):
        ok = M & (np.minimum(np.minimum(Yc[i], Yc[i + 1]), np.minimum(Yr[i], Yr[i + 1])) >= y_san)
        if ok.any(): v.append(float(np.abs(eps[i + 1] - eps[i])[ok].mean()))
    return round(float(np.mean(v)), 4) if v else 0.0


def quy_dao_tb(Cs, Rs, IID):
    """thước 1.17.5 (TB độ sáng mỗi nhà) — chỉ để in so sánh trong báo cáo/selftest (không tính lỗi từ 1.17.6)"""
    from checks.ll import q_k1175 as K75
    return K75.quy_dao(Cs, Rs, IID)['e_h']


def frames_video(mp4, maxW=None, n=None):
    """khung BGR ở độ phân giải GỐC của video (thu INTER_AREA nếu rộng hơn maxW; n khung đầu nếu khai) → (mảng [n, H, W, 3], (W, H))"""
    import subprocess, numpy as np
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', mp4], capture_output=True, text=True, check=True).stdout
    w, h = [int(x) for x in o.strip().split(',')[:2]]
    if maxW and w > maxW: h, w = int(round(h * maxW / w)), maxW
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', mp4, '-map', '0:v:0'] + (['-frames:v', str(n)] if n else []) + ['-vf', f'scale={w}:{h}:flags=area', '-pix_fmt', 'bgr24', '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3), (w, h)


# ================================================================ KN-6: (e) khung 0 ở độ phân giải video
def khung0_de(C0, tam_bgr, I_video):
    """C0: khung 0 video (cỡ gốc); tấm đã duyệt thu INTER_AREA về cỡ video; ΔE76 trên vùng nhà đo được (mặt nạ cỡ video) → (TB, p95)"""
    import cv2, numpy as np
    from checks.ll import q_k1175 as K75
    T0 = cv2.resize(tam_bgr, (C0.shape[1], C0.shape[0]), interpolation=cv2.INTER_AREA)
    dE = np.sqrt(((K75._lab(C0) - K75._lab(T0)) ** 2).sum(-1))[I_video > 0]
    return (float(dE.mean()), float(np.percentile(dE, 95))) if dE.size else (0.0, 0.0)


# ================================================================ KN-3: gọi lại Claude 1 lần khi không đọc đủ ảnh
def goi_claude_du(QV, pr, td, need, tag, out=None):
    """→ (txt, meta) như QV.call_claude; meta['loi'] = 'không đọc đủ ảnh…' chỉ khi CẢ HAI lần thiếu. Mỗi lần một dòng n2p-cost.jsonl (call_claude ghi)
    + dòng ghi chú lần/gọi lại. meta['lan'] = số lần gọi, meta['usd'] = tổng hai lần."""
    usd, lan = 0.0, 0
    for lan in (1, 2):
        txt, meta = QV.call_claude(pr, td, f'{tag}' if lan == 1 else f'{tag}-goi-lai', out)
        usd += float(meta.get('usd') or 0)
        miss = [os.path.basename(x) for x in need if x not in (meta.get('reads') or [])]
        thieu_anh = not meta.get('loi') and bool(miss)   # chỉ gọi lại khi THIẾU ẢNH (lỗi API/mô hình khác: fail-closed như cũ)
        if thieu_anh: meta['loi'] = f'không đọc đủ ảnh: thiếu {", ".join(miss)}' + (' (cả lần gọi lại)' if lan == 2 else '')
        QV._log(out, dict(tag=f'{tag}', lan=lan, ghi='K-1.17.6 KN-3', doc_du=not miss, so_anh_doc=len(meta.get('reads') or []), so_anh_can=len(need),
                          goi_lai=(lan == 1 and thieu_anh), date_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
        if not thieu_anh: break
    meta['lan'] = lan; meta['usd'] = round(usd, 6); meta.pop('reads', None)
    return txt, meta


# ================================================================ TU-LIEU (12:52)
def tran_tu_lieu(E):
    """→ (trần % tư liệu + khắc + thẻ của tập, lỗi khai | None)"""
    v = E.get('tu_lieu_tran_pct')
    if v is None: return TU_LIEU_MAC_DINH, None
    if not _num(v): return TU_LIEU_MAC_DINH, f'(k) tu_lieu_tran_pct {v!r} không phải số — dùng {TU_LIEU_MAC_DINH:g} %'
    if float(v) > TU_LIEU_TRAN_DUYET + 1e-9:
        return TU_LIEU_MAC_DINH, f'(k) tu_lieu_tran_pct {v:g} > {TU_LIEU_TRAN_DUYET:g} % (trần cao nhất chủ dự án duyệt, T4 25/10/2026 09:15) — dùng {TU_LIEU_MAC_DINH:g} %'
    return float(v), None


def _t01(s):
    from checks.ll import q_k1174 as K
    t0 = s.get('t0') if _num(s.get('t0')) else None; d = K._dur(s)
    if t0 is None: return None, None
    return float(t0), float(s.get('t1')) if _num(s.get('t1')) else float(t0) + d


def lan_tu_lieu(LS):
    """→ danh sách lần tư liệu [{shot, i, t0, t1, s, lop, co_gio}]. Trường log shot `tu_lieu_lan: [{t0, t1, lop?}]` (giây tuyệt đối trong phim) cho
    giờ thật từng lần; không có → một lần mỗi shot, dài = tổng lớp TL + KHAC + THE + MAP, VỊ TRÍ CHƯA BIẾT (xét như phủ cả shot khi đo trùng/ghép liền)."""
    from checks.ll import q_k1174 as K
    out = []
    for i, s in enumerate(LS or []):
        a, b = _t01(s)
        if isinstance(s.get('tu_lieu_lan'), list) and s['tu_lieu_lan']:
            for x in s['tu_lieu_lan']:
                if _num(x.get('t0')) and _num(x.get('t1')):
                    out.append(dict(shot=str(s.get('shot')), i=i, t0=float(x['t0']), t1=float(x['t1']), s=float(x['t1']) - float(x['t0']), lop=x.get('lop'), co_gio=True))
            continue
        v = K._lop(s, *LOP_TU_LIEU)
        if v > 0: out.append(dict(shot=str(s.get('shot')), i=i, t0=a, t1=b, s=v, lop='+'.join(k for k in LOP_TU_LIEU if K._lop(s, k) > 0), co_gio=False))
    return out


def tu_lieu_10(E, TL, LS, cong='G2'):
    """TU-LIEU-10 (1.17.6): (a) TL + KHAC + THE ≤ tu_lieu_tran_pct % thời lượng (mặc định 10); (b) mỗi lần tư liệu ≤ 10 s; (k) khai sai trần → Chặn."""
    from checks.ll import q_k1174 as K
    if LS is None: return K.r(thieu=['không có log shot'], val='—', cong=cong)
    tran, lk = tran_tu_lieu(E)
    T = K._tong(E, TL, LS); tot = sum(K._lop(s, *LOP_TRAN) for s in LS); p = 100 * tot / T if T else 0.0
    M = {'a': [], 'b': [], 'k': [lk] if lk else []}
    if p > tran + 1e-9: M['a'].append(f'(a) tư liệu + tranh khắc + thẻ' + (' + ảnh/footage thật' if any(K._lop(s, 'THAT') for s in LS) else '') + f' {tot:.1f} s = {p:.2f} % > {tran:g} %')
    for x in lan_tu_lieu(LS):
        if x['s'] > TU_LIEU_LAN_S + 1e-9: M['b'].append(f"(b) {x['shot']}: một lần tư liệu ({x['lop']}) {x['s']:.1f} s > {TU_LIEU_LAN_S:g} s" + ('' if x['co_gio'] else ' (không khai tu_lieu_lan — tính cả lớp của shot)'))
    return K.r(sum(M.values(), []), val=f'{tot:.1f} s / {T:.1f} s = {p:.2f} % / trần {tran:g} %' + (' (khai tu_lieu_tran_pct)' if E.get('tu_lieu_tran_pct') is not None and not lk else ' (mặc định)')
               + f' (TL {sum(K._lop(s, "TL") for s in LS):g} · KHAC {sum(K._lop(s, "KHAC") for s in LS):g} · THE {sum(K._lop(s, "THE") for s in LS):g}'
               + (f' · THAT {sum(K._lop(s, "THAT") for s in LS):g}' if any(K._lop(s, 'THAT') for s in LS) else '') + ' s) · lần dài nhất '
               + f"{max([x['s'] for x in lan_tu_lieu(LS)] or [0]):.1f} s", sat_nguong=K.sat('tư liệu + khắc + thẻ %', round(p, 2), tran), muc=M, cong=cong, pct=round(p, 2), tran=tran)


def tu_lieu_omni(E, TL, LS, cong='G2'):
    """TU-LIEU-OMNI (1.17.6): (a) lần tư liệu không trùng thời gian clip M-d (`minh_hoa`); (b) không ghép liền — giữa lần tư liệu và clip M-d
    (theo giờ phim) phải có ≥ 1 shot 3D (không tư liệu, không M-d) HOẶC ≥ GHEP_LIEN_S s 3D (hoà qua 3D: phần shot 3D không có tư liệu).
    Lần không khai giờ (`tu_lieu_lan`) xét như phủ cả shot của nó (phần 3D còn lại trong shot không được tính)."""
    from checks.ll import q_k1174 as K
    if LS is None: return K.r(thieu=['không có log shot'], val='—', cong=cong)
    gio = [_t01(s) for s in LS]
    if any(a is None for a, _ in gio): return K.r(thieu=['log shot thiếu t0 (hoặc t1/dur) — không xếp được giờ phim'], val='—', cong=cong)
    md = [(j, s) for j, s in enumerate(LS) if s.get('minh_hoa')]; LT = lan_tu_lieu(LS); M = {'a': [], 'b': []}
    if not md or not LT: return K.r(val=f'{len(LT)} lần tư liệu · {len(md)} clip M-d — không có cặp để xét', cong=cong, muc=M)
    # khoảng KHÔNG phải 3D sạch: clip M-d + mọi lần tư liệu (lần không khai giờ phủ cả shot)
    ban = [gio[j] for j, _ in md] + [((x['t0'], x['t1']) if x['co_gio'] else gio[x['i']]) for x in LT]

    def sach3d(lo, hi):   # số giây 3D không tư liệu, không M-d trong (lo, hi)
        if hi <= lo: return 0.0
        iv = sorted((max(lo, a), min(hi, b)) for a, b in ban if b > lo and a < hi); phu, cur = 0.0, lo
        for a, b in iv:
            if b <= cur: continue
            phu += b - max(a, cur); cur = b
        return (hi - lo) - phu
    bo_trung = 0
    for x in LT:
        a, b = (x['t0'], x['t1']) if x['co_gio'] else gio[x['i']]
        # 1.17.8 (khiếu nại ANIMATIC-T4-V2 §8): (b) chỉ xét clip M-d GẦN NHẤT mỗi phía — clip xa hơn đã có clip M-d gần hơn chắn giữa (không đếm trùng)
        tr = [gio[j][1] for j, _ in md if gio[j][1] <= a + 1e-6]; sa = [gio[j][0] for j, _ in md if gio[j][0] >= b - 1e-6]
        gan = ({j for j, _ in md if tr and abs(gio[j][1] - max(tr)) < 1e-6} | {j for j, _ in md if sa and abs(gio[j][0] - min(sa)) < 1e-6})
        for j, s in md:
            c, d = gio[j]
            if j == x['i'] or (a < d - 1e-6 and c < b - 1e-6):
                M['a'].append(f"(a) {x['shot']}: tư liệu ({x['lop']}) {a:.1f}–{b:.1f} s trùng clip M-d {s.get('shot')} {c:.1f}–{d:.1f} s — tư liệu chỉ chồng lên shot 3D"); continue
            if j not in gan: bo_trung += 1; continue
            lo, hi = (b, c) if b <= c else (d, a)
            xen = [z for k, z in enumerate(LS) if lo - 1e-6 <= gio[k][0] and gio[k][1] <= hi + 1e-6 and not z.get('minh_hoa') and K._lop(z, *LOP_TU_LIEU) <= 0
                   and not z.get('tu_lieu_lan') and gio[k][1] - gio[k][0] > 1e-6]
            g3 = sach3d(lo, hi)
            if not xen and g3 < GHEP_LIEN_S - 1e-6:
                M['b'].append(f"(b) {x['shot']} ({a:.1f}–{b:.1f} s) ↔ clip M-d {s.get('shot')} ({c:.1f}–{d:.1f} s): ghép liền — không shot 3D xen giữa, 3D sạch {g3:.2f} s < {GHEP_LIEN_S:g} s"
                              + ('' if x['co_gio'] else ' (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)'))
    return K.r(sum(M.values(), []), val=f'{len(LT)} lần tư liệu · {len(md)} clip M-d · trùng {len(M["a"])} · ghép liền {len(M["b"])}'
               + (f' · 1.17.8: bỏ {bo_trung} cặp với clip M-d không gần nhất' if bo_trung else ''), muc=M, cong=cong)


def check_tu_lieu(E, TL=None, ep_dir='.', LS=None):
    """→ {TU-LIEU-10, TU-LIEU-OMNI} cho tập từ T4 (thay TU-LIEU-10 của q_k1174)"""
    from checks.ll import q_k1174 as K
    cong = 'animatic' if E.get('animatic') else 'G2'
    if not ap_1176(E): return {k: K.na('tập trước T4 — không hồi tố') for k in ('TU-LIEU-10', 'TU-LIEU-OMNI')}
    if not LS and E.get('log_shot'):
        try: LS = K.K6._load(K.K6._p(ep_dir, E['log_shot']))
        except Exception: LS = None   # noqa: BLE001
    LS = K.chuan_ls(LS); out = {}
    for k, fn in (('TU-LIEU-10', tu_lieu_10), ('TU-LIEU-OMNI', tu_lieu_omni)):
        try: out[k] = fn(E, TL, LS, cong)
        except Exception as e: out[k] = K.r(thieu=[f'không chạy được: {type(e).__name__}: {e}'], val='—', cong=cong)   # noqa: BLE001
    return out
