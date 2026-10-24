"""nháp BE-MAT-NHA (a): hình khối từng nhà thường — đỡ cạnh hình học (biên mặt nạ ID nhà + biên mặt phẳng) bằng cạnh ảnh AI, dời tốt nhất, cặp vách ngăn"""
import cv2, numpy as np

P = dict(SIG=1.0, T_VIS=3.0, T_AI=3.0, R_DO=1.5, S_M=4.0, PPM_MIN=1.5, A_MIN=120, D_M=1.5, G_MIN=0.10, SUP_MIN=0.45, SEP_MIN=0.30, SEP_L=6)


def lum(b):
    return cv2.cvtColor(b, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32) * (100 / 255)


def grad(b, sig, mau=False):
    """độ lớn gradient (đơn vị L* hoặc ΔE76 mỗi px); mau=True: gradient màu Lab (cạnh giữa hai mặt cùng độ sáng khác sắc vẫn thấy)"""
    x = cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32)
    x = cv2.GaussianBlur(x, (0, 0), sig); ch = range(3) if mau else (0,)
    return np.sqrt(sum((cv2.Sobel(x[..., c], cv2.CV_32F, 1, 0, ksize=3) / 8) ** 2 + (cv2.Sobel(x[..., c], cv2.CV_32F, 0, 1, ksize=3) / 8) ** 2 for c in ch))


def bien(M):
    """biên điểm ảnh của nhãn: điểm có lân cận 4 khác nhãn"""
    b = np.zeros(M.shape, bool)
    b[:-1] |= M[:-1] != M[1:]; b[1:] |= M[1:] != M[:-1]; b[:, :-1] |= M[:, :-1] != M[:, 1:]; b[:, 1:] |= M[:, 1:] != M[:, :-1]
    return b


def do_nha(R, A, IID, nha, PID=None, p=None, chi_id=None, BONG=None):
    """R render · A ảnh đã ghép (bề mặt nhà từ AI) · IID mã nhà (0 = không phải nhà thường) · nha {id: {px_m, lo}} · PID mã mặt phẳng (tuỳ chọn).
    → {id: dict(px, px_m, sup0, sup, dx, dy, dich_m, iou, loi[])}, cặp vách ngăn"""
    p = dict(P, **(p or {})); H, W = IID.shape; s = H / 1080.0
    gR = grad(R, p['SIG'] * s, mau=True); gB = grad(BONG, p['SIG'] * s) if BONG is not None else gR; gA = grad(A, p['SIG'] * s, mau=True)   # cạnh HÌNH HỌC thấy nhờ ánh sáng (pass bóng) ↔ cạnh màu ảnh AI
    EA = gA >= p['T_AI']; DT = cv2.distanceTransform((~EA).astype(np.uint8), cv2.DIST_L2, 3)
    BI = bien(IID); BP = bien(PID) if PID is not None else np.zeros_like(BI)
    GE = (BI | BP) & (gR >= p['T_VIS']) & (gB >= p['T_VIS'])   # cạnh HÌNH HỌC (biên nhà/mặt phẳng) thấy được ở render VÀ do ánh sáng (pass bóng)
    ids, inv, cnt = np.unique(IID.ravel(), return_inverse=True, return_counts=True)
    out = {}
    ys_all, xs_all = np.nonzero(GE)
    gid = IID[ys_all, xs_all]
    # cạnh hình học thuộc nhà h: điểm GE có mã h, hoặc điểm GE kề (≤1 px) mã h (biên phía ngoài)
    Mx = cv2.dilate(IID.astype(np.float32), np.ones((3, 3), np.uint8)).astype(np.int64)   # gần đúng: mã lớn nhất lân cận
    order = np.argsort(gid, kind='stable'); gs = gid[order]
    for k, h in enumerate(ids):
        if h == 0 or (chi_id is not None and h not in chi_id): continue
        info = nha.get(int(h)) or {}; ppm = float(info.get('px_m') or 0)
        a = int(cnt[k])
        if a < p['A_MIN'] * s * s or ppm < p['PPM_MIN']:
            out[int(h)] = dict(px=a, px_m=ppm, do=False); continue
        lo, hi = np.searchsorted(gs, h), np.searchsorted(gs, h, 'right'); sel = order[lo:hi]
        yy, xx = ys_all[sel], xs_all[sel]
        if len(yy) < 8: out[int(h)] = dict(px=a, px_m=ppm, do=False, ly_do='ít cạnh thấy'); continue
        S = int(np.ceil(p['S_M'] * ppm)) + 1
        best = (-1, 0, 0); sup = {}
        for dy in range(-S, S + 1):
            y2 = np.clip(yy + dy, 0, H - 1)
            for dx in range(-S, S + 1):
                x2 = np.clip(xx + dx, 0, W - 1); v = float((DT[y2, x2] <= p['R_DO'] * s).mean()); sup[(dx, dy)] = v
                if v > best[0] + 1e-9 or (abs(v - best[0]) <= 1e-9 and dx * dx + dy * dy < best[1] ** 2 + best[2] ** 2): best = (v, dx, dy)
        s0 = sup[(0, 0)]; v, dx, dy = best; dm = float(np.hypot(dx, dy)) / ppm
        loi = []
        if dm >= p['D_M'] and v - s0 >= p['G_MIN']: loi.append(f'dời {dm:.1f} m ({dx:+d},{dy:+d} px)')
        if s0 < p['SUP_MIN']: loi.append(f'đỡ cạnh {s0:.2f} < {p["SUP_MIN"]}')
        out[int(h)] = dict(px=a, px_m=round(ppm, 3), do=True, n_canh=int(len(yy)), sup0=round(s0, 3), sup=round(v, 3), dx=dx, dy=dy, dich_m=round(dm, 2), loi=loi)
    return out
