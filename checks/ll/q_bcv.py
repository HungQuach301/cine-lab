#!/opt/cine/bin/python
"""BIEN-CO-V — thước BIẾN CỐ THẤY ĐƯỢC đo trên video (phiên K-1.17.4, 23/10/2026; K117-D8 / K116-D4, chủ dự án duyệt Q7 23/10/2026 21:45).
Căn cứ: Kinh thánh §4 (14/10 18:08) "trung bình ≤ 3,5 s có một biến cố hình mới …; không giữ khung tĩnh > 6 s"; §13.6 TL-1/TL-3 (timelapse: thời
gian chạy trong shot = biến cố); K116-D4 "K đo biến cố thời gian chạy trên video (đổi nội dung trong cửa sổ máy cố định) và cộng vào Q37 —
KHÔNG nhận biến cố tự khai trong log"; K117-D8 (A) duyệt 23/10 17:42 (QUYET-DINH-TREO "theo K").

ĐỊNH NGHĨA (đo, không khai). Video → xám W×H (256×144), làm mờ σ 2 (MO_KHUNG). Mỗi cặp khung liền: chuyển động máy toàn cục = homography (điểm góc
Shi–Tomasi + Lucas–Kanade + RANSAC 2 px); không đủ điểm khớp (< 12 hoặc < 30 % điểm theo) hoặc phần dư sau bù > CAT_DU → CẮT (biến cố, mọi ô
về neo mới). Lưới GX × GY ô (8 × 6). Mỗi ô giữ một KHUNG NEO; mỗi BUOC khung (0,25 s) so khung hiện tại với khung neo của ô đã bù chuyển động
máy (homography gộp neo → hiện tại) và bù sáng toàn khung (g·x + o, bình phương nhỏ nhất trên vùng hợp lệ): phần dư r = |Δ| trung bình trong ô
(mức xám /255). Ô có r ≥ THETA và r ≥ K_CUC_BO × trung vị r các ô (thay đổi CỤC BỘ, không phải trôi/thị sai toàn khung) → ô ĐỔI, neo ô về khung
hiện tại cùng 8 ô kề (một vật đổi trải nhiều ô = một biến cố). Ô ra khỏi vùng nhìn (phần hợp lệ < 50 %, do máy đi) → neo lại, KHÔNG là biến cố (vật mới vào khung do máy không phải biến cố thời gian).
Neo ô quá NEO_MAX (3 s) → neo lại, không biến cố: "thấy được" = đổi cục bộ ≥ THETA trong ≤ 3 s (chặn trôi tích luỹ của bù chuyển động máy).
BIẾN CỐ = thời điểm có ≥ 1 ô đổi (hoặc cắt); gộp các biến cố cách < 0,25 s (như Q37). Đổi liên tục (lửa lan, nhà mọc) cho biến cố lặp theo
tốc độ đổi (mỗi lần ô vượt ngưỡng so với neo của nó).
Bù chuyển động máy chỉ là homography — thị sai mạnh (máy cẩu thấp) còn dư; điều kiện "cục bộ" (≥ K × trung vị) chặn phần lớn dư thị sai.

HIỆU CHUẨN (trên master T3 bản cuối, SHA 5b9f0bcc…; `reports/k1174/do/hieu_chuan_bcv.py`): tham chiếu = ranh shot + ranh góc máy (cắt), beat
khai ĐÃ KHỚP mốc đặc tả (Q37 (a) 1.17.3), quãng khung TĨNH (Q37 1.13, ≥ 2 s) và clip tổng hợp (chỉ máy đi / thêm một vật đổi). Tiêu chí ĐẠT
(HC_*, đặt trước lượt đo đầy đủ): R cắt ≥ 95 %, R beat ≥ 70 %, sai số giờ trung vị ≤ 0,25 s, báo nhầm ≤ 1/phút trong quãng tĩnh và 0 trên clip
chỉ máy đi, bắt 6/6 vật đổi tổng hợp ±0,25 s — trên cả nửa chỉnh lẫn nửa kiểm. Độ chính xác so mốc đặc tả CHỈ BÁO (mốc không phủ đổi liên tục
giữa hai mốc của timelapse). Kết quả ghi ở HIEU_CHUAN (hằng số, kèm SHA master); THETA, K_CUC_BO chọn trên nửa đầu, kiểm trên nửa sau.

Hàng BIEN-CO-V (k2check, tập từ T3 có video): (b) khoảng biến cố ĐO trung bình ≤ 3,5 s; (c) khoảng dài nhất ≤ 6 s, miễn như Q37 1.16 (khung
neo, tấm im lặng ≤ 10 s) + 1.17.4 thẻ phương pháp cuối phim (≤ 2 thẻ × ≤ 10 s — K1173-D6; q_k116.q37_mien); (h) hiệu chuẩn trên CHÍNH tập: R cắt ≥ 95 % so
ranh shot của timeline. Cấp: Cảnh báo ở animatic; Chặn ở G2 khi HIEU_CHUAN đạt VÀ (h) đạt — không thì Cảnh báo (`muc` = 'chua_hieu_chuan').
Q37 / NHIP-K2 / Q37 (1.13) (tập từ T4 — `kenh2_tu_t4`/`n2p`, có video, thước đạt hiệu chuẩn): (b)(c) cộng biến cố ĐO (như I8). Beat tự khai
trong log shot (`su_kien`) KHÔNG được nhận ở đâu.

  q_bcv.py <video.mp4> [--json ra.json]          → danh sách biến cố đo
"""
import json, os, subprocess, sys

W, H, GX, GY, BUOC, FPS = 256, 144, 8, 6, 6, 24
THETA, K_CUC_BO = 8.0, 2.0          # hiệu chuẩn T3 23/10/2026 (chọn trên nửa đầu, kiểm nửa sau — HIEU_CHUAN)
CAT_DU, CAT_MIN_PT, CAT_TY, TRONG_STD = 18.0, 12, 0.30, 3.0
NEO_MAX, MO_DU, MO_KHUNG = 3.0, 1.5, 2.0   # tuổi neo ô ≤ 3 s (dưới ngưỡng TB 3,5 s): đổi CHẬM hơn THETA/3 s không là biến cố thấy được; mờ khung σ 2 (σ 1 → răng cưa khi máy phóng/quay = báo nhầm 14–91/60 s clip tổng hợp), mờ phần dư σ 1,5
MERGE, MEAN_MAX, GAP_MAX, MIEN_MAX = 0.25, 3.5, 6.0, 10.0
TOL = 0.5                           # khớp tham chiếu khi hiệu chuẩn (như TL-1 đối chiếu cắt ±0,5 s)
HC_R_CAT, HC_R_BEAT, HC_DT, HC_FP_PHUT = 95.0, 70.0, 0.25, 1.0
HIEU_CHUAN = dict(dat=True, master_sha='5b9f0bccd88830ab212a6747259ac597328ae87bb964addc953bf1928fd7b682', ngay='2026-10-23', theta=8.0, k=2.0,
                  nua_dau=dict(R_cat=100.0, R_beat=90.8, dt_tv=0.05, bao_nham_tinh=0), nua_sau=dict(R_cat=100.0, R_beat=98.2, dt_tv=0.042, bao_nham_tinh=0, tinh_s=16.1),
                  tong_hop=dict(bao_nham_chi_may=0, bat_vat_doi='6/6'), nguon='reports/k1174/do/hieu-chuan-bcv.json',
                  ghi='ĐẠT (T3 5b9f0bcc…: θ 8, k 2; R cắt 100/100 %, R beat 90,8/98,2 %, Δt TV 0,05/0,04 s, báo nhầm 0)')
# 1.17.8 (K1174-D2 "A, kèm hiệu chuẩn lại trên animatic T4 (log máy thật) trước G2"): hiệu chuẩn lại trên animatic T4 v2 — bản xem 4 phần nối
# (SHA d4b5d486…, 640×360, ≈ 66 kb/s hình) + log máy thật (animatic2/log-may): tập TĨNH THẬT / CHỈ MÁY THẬT lấy từ log máy (năm, lửa, mặt trời không
# đổi), cùng tiêu chí K-1.17.4 §2. KHÔNG lưới (θ, k) nào đạt: ở θ 8, k 2 — R cắt 100/97,9 %, R beat 94,4/100 %, Δt 0,04 s đạt; báo nhầm TĨNH THẬT 0 / 9,9
# phút⁻¹ (nửa sau, 3 trong 18,1 s), CHỈ MÁY THẬT 7,6 / 127,5 phút⁻¹ (TRUOT tầm phố H5-02s, XUONG H2-11: thị sai mạnh — giới hạn (3) K-1.17.4), clip tổng hợp
# chỉ máy 5 báo nhầm, vật đổi 5/6 (khung bản xem phóng 3× — mã hoá thấp). → Tập từ T4: thước CHƯA ĐẠT hiệu chuẩn — BIEN-CO-V chỉ Cảnh báo (cả G2) và
# Q37/NHIP-K2/Q37 (1.13) KHÔNG cộng biến cố đo (cho_q37) tới khi hiệu chuẩn lại đạt trên master/animatic đủ bitrate + xử lý thị sai (reports/k1178 §5).
HIEU_CHUAN_T4 = dict(dat=False, video_sha='d4b5d486e9bcdb9c33b334ea0dc30c66ccc0056db6097dea3e4c8f4e2b94fbb2', ngay='2026-10-25', theta=8.0, k=2.0,
                     nua_dau=dict(R_cat=100.0, R_beat=94.4, dt_tv=0.042, tinh_that_phut=0.0, chi_may_that_phut=7.62),
                     nua_sau=dict(R_cat=97.9, R_beat=100.0, dt_tv=0.043, tinh_that_phut=9.93, chi_may_that_phut=127.5),
                     tong_hop=dict(bao_nham_chi_may=5, bat_vat_doi='5/6'), nguon='reports/k1178/do/hieu-chuan-bcv-t4.json',
                     ghi='KHÔNG ĐẠT (T4 v2 bản xem d4b5d486…, θ 8 k 2: báo nhầm tĩnh thật 9,9/phút, chỉ máy thật 127,5/phút — thị sai TRUOT/XUONG; tổng hợp 5; vật đổi 5/6)')


def hc_tap_nay(E):
    """1.17.8: hiệu chuẩn áp cho tập — từ T4 (kenh2_tu_t4 | n2p) dùng HIEU_CHUAN_T4; tập trước dùng HIEU_CHUAN (T3)"""
    return (HIEU_CHUAN_T4, 'T4 (1.17.8)') if (E or {}).get('kenh2_tu_t4') or (E or {}).get('n2p') else (HIEU_CHUAN, 'T3')


def _frames(mp4, w=None, h=None):
    """→ bộ sinh khung xám uint8 h×w (luồng, không giữ cả phim)"""
    w, h = w or W, h or H
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-nostdin', '-i', mp4, '-map', '0:v:0', '-vf', f'scale={w}:{h}:flags=area,format=gray', '-f', 'rawvideo', '-'],
                         stdout=subprocess.PIPE)
    n = w * h
    try:
        while True:
            b = p.stdout.read(n)
            if len(b) < n: break
            yield b
    finally:
        p.stdout.close(); p.wait()


def do_video(mp4, theta=None, k=None, fps=FPS, ghi_o=False):
    """→ dict(su_kien=[(t, so_o, r_max, loai)], cat=[t], n_khung, thong_so). loai: 'cat' | 'o'. ghi_o: thêm chuỗi r theo bước (hiệu chuẩn)."""
    import cv2, numpy as np
    theta = THETA if theta is None else theta; k = K_CUC_BO if k is None else k
    cw, ch = W // GX, H // GY; ev, cats, prev, Mt, i, trong = [], [], None, np.eye(3), -1, False
    neo, M_neo, ID = {}, {}, np.zeros((GY, GX), np.int64)    # neo[f] = khung chuẩn hoá; M_neo[f] = Mt lúc f; ID[ô] = khung neo của ô
    ones = np.ones((H, W), np.float32); chuoi = []
    for b in _frames(mp4):
        i += 1; cur = cv2.GaussianBlur(np.frombuffer(b, np.uint8).reshape(H, W), (0, 0), MO_KHUNG)
        if float(cur.std()) < TRONG_STD:   # khung trống (đen/mờ dần): không theo, không biến cố; khung có hình đầu tiên sau đó = cắt
            prev = None; trong = True; continue
        cut = prev is None and trong; trong = False
        if prev is not None:
            pt = cv2.goodFeaturesToTrack(prev, 300, 0.01, 6)
            Hm = None
            if pt is not None and len(pt) >= CAT_MIN_PT:
                p1, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, pt, None, winSize=(15, 15), maxLevel=3)
                g = st.ravel() == 1
                if g.sum() >= CAT_MIN_PT:
                    Hm, inl = cv2.findHomography(pt[g], p1[g], cv2.RANSAC, 2.0)
                    if Hm is None or inl.sum() < max(CAT_MIN_PT, CAT_TY * len(pt)): Hm = None
            if Hm is None: cut = True
            else:
                wp = cv2.warpPerspective(prev, Hm, (W, H)).astype(np.float32); vm = cv2.warpPerspective(ones, Hm, (W, H)) > 0.99
                du = float(np.abs(cur.astype(np.float32) - wp)[vm].mean()) if vm.mean() > 0.3 else 99.0
                if du > CAT_DU: cut = True
                else: Mt = Hm @ Mt
        if prev is None or cut:
            t = i / fps
            if cut and t > 0.5: cats.append(round(t, 3)); ev.append((round(t, 3), GX * GY, 99.0, 'cat'))
            Mt = np.eye(3); neo = {i: cur.astype(np.float32)}; M_neo = {i: Mt.copy()}; ID[:] = i; prev = cur; continue
        prev = cur
        if i % BUOC: continue
        cf = cur.astype(np.float32); R = np.full((GY, GX), np.nan, np.float32); V = np.zeros((GY, GX), np.float32)
        for a in np.unique(ID):
            Ha = Mt @ np.linalg.inv(M_neo[int(a)]); A = cv2.warpPerspective(neo[int(a)], Ha, (W, H)); vm = cv2.warpPerspective(ones, Ha, (W, H)) > 0.99
            if vm.sum() > 100:
                x, y = A[vm], cf[vm]; g_, o_ = np.polyfit(x, y, 1) if x.std() > 1e-3 else (1.0, float(y.mean() - x.mean()))
                d = cv2.GaussianBlur(np.abs(cf - (g_ * A + o_)), (0, 0), MO_DU)
            else: d = np.zeros_like(cf)
            for gy, gx in zip(*np.nonzero(ID == a)):
                sl = (slice(gy * ch, (gy + 1) * ch), slice(gx * cw, (gx + 1) * cw)); m = vm[sl]; V[gy, gx] = m.mean()
                if m.mean() >= 0.5: R[gy, gx] = d[sl][m].mean()
        med = float(np.nanmedian(R)) if np.isfinite(R).any() else 0.0
        doi = np.isfinite(R) & (R >= theta) & (R >= k * med)
        roi = V < 0.5
        if ghi_o: chuoi.append((round(i / fps, 3), float(np.nanmax(R)) if np.isfinite(R).any() else 0.0, med))
        if doi.any(): ev.append((round(i / fps, 3), int(doi.sum()), round(float(np.nanmax(R[doi])), 2), 'o'))
        gia = (i - ID) >= NEO_MAX * fps   # neo quá tuổi → neo lại (không biến cố): chặn trôi tích luỹ của bù chuyển động
        ke = cv2.dilate(doi.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)   # một vật đổi trải nhiều ô = MỘT biến cố: neo lại cả ô kề
        ID[ke | roi | gia] = i; neo[i] = cf; M_neo[i] = Mt.copy()
        for f in [f for f in neo if f not in set(ID.ravel().tolist())]: neo.pop(f); M_neo.pop(f)
    return dict(su_kien=ev, cat=cats, n_khung=i + 1, thong_so=dict(theta=theta, k=k, W=W, H=H, GX=GX, GY=GY, BUOC=BUOC), chuoi=chuoi if ghi_o else None)


def gop(ev):
    """gộp biến cố cách < MERGE → [t]"""
    U = []
    for t in sorted(e[0] if isinstance(e, (list, tuple)) else e for e in ev):
        if not U or t - U[-1] >= MERGE: U.append(t)
    return U


def khop(ev, ref, tol=TOL):
    """→ (số ev có ref trong ±tol, số ref có ev trong ±tol, [|Δt| của ref khớp])"""
    import bisect
    E, R = sorted(ev), sorted(ref); dts = []
    def gan(L, x):
        j = bisect.bisect_left(L, x); c = [L[q] for q in (j - 1, j) if 0 <= q < len(L)]
        return min((abs(x - y) for y in c), default=99.0)
    pe = sum(1 for x in E if gan(R, x) <= tol)
    for x in R:
        d = gan(E, x)
        if d <= tol: dts.append(d)
    return pe, len(dts), dts


def tb_dai(ev, total, mien=()):
    """(b) TB khoảng; (c) dài nhất (bỏ khoảng nằm trọn trong một đoạn miễn ≤ MIEN_MAX) → (tb, dài nhất, từ, [miễn])"""
    U = gop(ev)
    G = ([(a, b) for a, b in zip(U, U[1:])] + [(U[-1], total)]) if U else [(0.0, total)]
    if U and U[0] > 0: G = [(0.0, U[0])] + G
    keep, ex = [], []
    for a, b in G:
        m = next((m for m in mien if m[0] - 0.05 <= a and b <= m[1] + 0.05), None)
        if m and b - a <= MIEN_MAX + 1e-6: ex.append((round(b - a, 2), round(a, 2), m[2], m[3]))
        else: keep.append((b - a, a))
    g, at = max(keep) if keep else (0.0, 0.0)
    return (round(total / len(U), 2) if U else None), round(g, 2), round(at, 2), ex


def ranh_shot(TL):
    return sorted({round(float(sg['t0']) + float(sh.get('t0') or 0), 3) for sg in TL.get('segments') or [] for sh in sg.get('shots') or []} - {0.0})


def hang(E, TL, mp4, cong='G2', mien=None, ket=None, tl_ev=()):
    """hàng BIEN-CO-V. ket = kết quả do_video đã có (tránh đo lại). tl_ev: biến cố cảnh tl đo (I8) cộng vào."""
    if not mp4 or not os.path.exists(mp4): return dict(ok=False, ket_qua='THIẾU', loi=[], thieu=['(b) không có video (master/animatic)'], val='—', cong=cong)
    D = ket or do_video(mp4); T = float(TL.get('tong_s') or D['n_khung'] / FPS)
    M = list(mien or [])   # khung neo, tấm im lặng, thẻ PP cuối phim (q_k116.q37_mien — 1.16 + 1.17.4 K1173-D6)
    ev = [e[0] for e in D['su_kien']] + [float(x) for x in tl_ev]
    tb, dn, tu, ex = tb_dai(ev, T, M)
    rs = ranh_shot(TL); _, nr, _ = khop([e[0] for e in D['su_kien']], rs); rcat = 100.0 * nr / len(rs) if rs else 100.0
    loi, near, muc = [], [], {}
    if tb is None or tb > MEAN_MAX: loi.append(f'(b) khoảng biến cố ĐO trung bình {tb} s > {MEAN_MAX:g} s')
    if dn > GAP_MAX: loi.append(f'(c) khoảng dài nhất không biến cố ĐO {dn} s > {GAP_MAX:g} s (từ {int(tu // 60)}:{tu % 60:04.1f})')
    hc_tap = rcat >= HC_R_CAT
    if not hc_tap: loi.append(f'(h) thước trên tập này: bắt {nr}/{len(rs)} ranh shot = {rcat:.1f} % < {HC_R_CAT:g} % — chưa tin để Chặn')
    for v, ng, ten in ((tb or 0, MEAN_MAX, 'TB'), (dn, GAP_MAX, 'dài nhất')):
        if abs(v - ng) <= 0.05 * ng: near.append(f'{ten} {v} s (ngưỡng {ng:g})')
    HC, hc_ten = hc_tap_nay(E)
    dat_hc = bool(HC.get('dat')) and hc_tap
    if not dat_hc: muc = {'chua_hieu_chuan': list(loi)}
    val = (f"{T:.1f} s · biến cố đo {len(D['su_kien'])} (gộp {len(gop(ev))}; cắt {len(D['cat'])}"
           + (f'; + cảnh tl {len(tl_ev)}' if tl_ev else '') + f") · TB {tb} s · dài nhất {dn} s · miễn {len(ex)} khoảng ({', '.join(sorted({x[2] for x in ex}))})"
           + f" · ranh shot bắt {nr}/{len(rs)} ({rcat:.1f} %) · hiệu chuẩn {hc_ten}: {HC.get('ghi')}")
    return dict(ok=not loi, loi=loi, val=val, sat_nguong=near, cong=cong, muc=muc, dat_hieu_chuan=dat_hc, bien_co=sorted(ev), mien=ex, tb=tb, dai_nhat=dn, r_cat=round(rcat, 1))


def cho_q37(E, ket, dat):
    """biến cố đo để cộng vào Q37 (b)(c): chỉ tập từ T4 (kenh2_tu_t4 | n2p) và thước đạt hiệu chuẩn → [(t, 'video', loại, mô tả)]"""
    if not ket or not dat or not (E.get('kenh2_tu_t4') or E.get('n2p')): return []
    return [(t, 'video', 'video:' + lo, f'{n} ô, r {r}') for t, n, r, lo in ket['su_kien']]


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    R = do_video(a[0]); U = gop([e[0] for e in R['su_kien']]); T = R['n_khung'] / FPS
    print(f"{len(R['su_kien'])} biến cố (gộp {len(U)}; cắt {len(R['cat'])}) · TB {T / max(1, len(U)):.2f} s · {T:.1f} s")
    if '--json' in a: json.dump(R, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False)
