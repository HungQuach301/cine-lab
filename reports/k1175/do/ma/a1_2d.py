"""Khung đáp án 2D cho A1/A2 trên ảnh có sẵn (T6 có mặt nạ; look2 mặt nạ nước suy từ render) — tất định theo hạt."""
import cv2, numpy as np


def mat_na_tu_render(R):
    """look2: mặt nạ ID không có trong git → nước = 'màu nước' HSV của render (định nghĩa T9b, nở/co 2 px), trời = thành phần xanh chạm mép trên."""
    h = cv2.cvtColor(R, cv2.COLOR_BGR2HSV); b = (h[..., 0] >= 85) & (h[..., 0] <= 130) & (h[..., 1] >= 40) & (h[..., 2] >= 30)
    b = cv2.morphologyEx(b.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)); b = cv2.morphologyEx(b, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, cc, st, _ = cv2.connectedComponentsWithStats(b, 4); H, W = b.shape
    L = np.full((H, W), 2, np.uint8)   # 0 troi 1 nuoc 2 bang (đất/nhà gộp — chỉ dùng cho phép (iii))
    for i in range(1, n):
        if st[i, 4] < 0.002 * H * W: continue
        if st[i, 1] == 0: L[cc == i] = 0
        else: L[cc == i] = 1
    # trời không xanh (mây): mọi điểm phía trên đường chân trời (hàng đầu tiên có nước/đất) — lấy theo cột: từ trên xuống tới điểm không sáng/xanh đầu
    return L, ['troi', 'nuoc', 'bang']


def bo_tren(L, names):
    Wt = L == names.index('nuoc'); land = (L != names.index('nuoc')) & (L != names.index('troi'))
    top = Wt & np.vstack([np.zeros((1, Wt.shape[1]), bool), land[:-1]]); return Wt, top


def doi_mau_nuoc(G, Wt, kieu, rng):
    """đổi sắc nước, giữ bờ: xám / ô-liu / nâu / nhạt (kiểu Gemini)"""
    lab = cv2.cvtColor(G, cv2.COLOR_BGR2LAB).astype(np.float32)
    tgt = dict(xam=(0, 0, 0.6), oliu=(-6, 14, 0.7), nau=(6, 14, 0.8), nhat=(0, -4, 1.35))[kieu]
    l, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    l2 = np.clip((l - l[Wt].mean()) * 0.9 + l[Wt].mean() * tgt[2], 0, 255); a2 = 128 + tgt[0] + (a - 128) * 0.25; b2 = 128 + tgt[1] + (b - 128) * 0.25
    out = lab.copy(); out[..., 0][Wt] = l2[Wt]; out[..., 1][Wt] = a2[Wt]; out[..., 2][Wt] = b2[Wt]
    X = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    al = cv2.GaussianBlur(Wt.astype(np.float32), (0, 0), 0.8)[..., None]   # mép mềm 1 px như ảnh AI
    return np.clip(G * (1 - al) + X * al, 0, 255).astype(np.uint8)


def gon_song(G, Wt, rng, amp=6.0):
    n = cv2.resize(rng.normal(0, 1, (G.shape[0] // 6, G.shape[1] // 3)).astype(np.float32), (G.shape[1], G.shape[0]), interpolation=cv2.INTER_CUBIC)
    out = G.astype(np.float32); out[Wt] += (amp * n[Wt])[:, None]; return np.clip(out, 0, 255).astype(np.uint8)


def phan_chieu(G, L, names, top, rng, h_max=60, alpha=(0.65, 0.25), toi=0.8):
    """phản chiếu tổng hợp theo hình học máy cao: trục gương = mặt nước dưới chân vật, cao hơn bờ ≈ 0,55 × (bờ − chân vật) px;
    hàng y dưới bờ phản chiếu hàng 2·trục − y nếu hàng đó là VẬT CAO (nhà/cây/tàu…); đất/bãi phẳng không có ảnh. Gợn ngang ±1,5 px, mờ dần, tối 0,8."""
    H, W = L.shape; Wt = L == names.index('nuoc'); out = G.astype(np.float32); ys, xs = np.nonzero(top)
    ph = rng.uniform(0, 6.28); TALL = [names.index(t) for t in ('nha', 'nha_thuong', 'congsu', 'tau', 'khac', 'cay', 'trai', 'pin', 'lua') if t in names]
    for y, x in zip(ys, xs):
        col = np.isin(L[max(0, y - h_max):y, x], TALL)[::-1]
        if not col.any(): continue
        b = int(np.argmax(col)); axis = y - 0.55 * b
        for j in range(h_max):
            yy = y + j; ym = int(round(2 * axis - yy))
            if yy >= H or ym < 0 or not Wt[yy, x]: break
            if not np.isin(L[ym, x], TALL): break
            dx = int(round(1.5 * np.sin(0.9 * j + 0.05 * x + ph))); xx = min(W - 1, max(0, x + dx))
            a = alpha[0] + (alpha[1] - alpha[0]) * j / h_max
            out[yy, x] = (1 - a) * out[yy, x] + a * toi * G[ym, xx]
    return np.clip(out, 0, 255).astype(np.uint8)


def lan_bo(G, L, names, top, x0, x1, d, rng, kieu='bai'):
    """bờ lấn có kiểm soát: đất mới d px dưới bờ trên đoạn cột [x0, x1], mép răng cưa ±15 %, KHÔNG đối xứng gương:
    bai = vân dải đất 2–10 px trên bờ lấy lệch ngang 23 px, thứ tự hàng xáo; go = bến gỗ tối có ván dọc; bun = bùn (đất ⊕ nước)"""
    H, W = L.shape; Wt = L == names.index('nuoc'); out = G.copy(); gt = np.zeros((H, W), bool)
    ys, xs = np.nonzero(top[:, x0:x1 + 1]); xs = xs + x0
    by = {}
    for y, x in zip(ys, xs): by.setdefault(x, []).append(y)
    nx = x1 - x0 + 1; jit = cv2.resize(rng.uniform(-0.15, 0.15, (1, max(2, nx // 6))).astype(np.float32), (nx, 1), interpolation=cv2.INTER_LINEAR)[0]
    go = np.array([38, 52, 66], np.float32); van = rng.normal(0, 6, W)
    for x in range(x0, x1 + 1):
        if x not in by: continue
        y = min(by[x]); taper = min(1.0, (x - x0 + 1) / 6.0, (x1 - x + 1) / 6.0); dd = int(round(d * (1 + jit[x - x0]) * taper))
        for j in range(dd):
            if y + j >= H or not Wt[y + j, x]: break
            src = G[max(0, y - 2 - ((j * 3) % 9)), min(W - 1, x + 23)].astype(np.float32)
            if kieu == 'go': v = go + van[x] + rng.normal(0, 2)
            elif kieu == 'bun': v = 0.55 * src + 0.45 * G[min(H - 1, y + dd + 6), x].astype(np.float32) + rng.normal(0, 3)
            else: v = src
            out[y + j, x] = np.clip(v, 0, 255).astype(np.uint8); gt[y + j, x] = True
    return out, gt


def chon_doan(top, n, dai, rng, le=60):
    """chọn n đoạn bờ trên không chồng nhau, mỗi đoạn dai px, có bờ ở ≥ 80 % cột"""
    H, W = top.shape; col = top.any(0); out = []; tries = 0
    while len(out) < n and tries < 2000:
        tries += 1; x0 = int(rng.integers(le, W - le - dai))
        if col[x0:x0 + dai].mean() < 0.8 or any(not (x0 + dai + 30 < a or x0 > b + 30) for a, b in out): continue
        ys = [np.nonzero(top[:, x])[0].min() for x in range(x0, x0 + dai) if col[x]]
        if max(ys) - min(ys) > 40: continue
        out.append((x0, x0 + dai))
    return sorted(out)
