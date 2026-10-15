#!/opt/cine/bin/python
"""DÙNG CHUNG · LUT màu kênh 2 (Mốc D4, phiên V5a 15/10/2026). Chỉ áp OFFLINE lên khung để so sánh — CHƯA gắn vào render (để V5b sau T2 G2).

  lut.py make   [--out assets/k2/lut]                       # sinh các LUT ứng viên .cube (33³) từ công thức dưới đây
  lut.py frames --out <thư mục> [--src t1|<video>] [--at s1,s2,…]   # trích 12 khung 1080p (mặc định từ master T1 trong LFS, không tải cả tệp)
  lut.py apply  <lut.cube> <vào.png> <ra.png>              # ffmpeg lut3d (tetrahedral)
  lut.py study  --frames <thư mục> [--luts a.cube,b.cube] --out <thư mục>   # áp mọi LUT lên mọi khung → study.json + tờ so sánh
  lut.py --self-test

Bảng màu đích ("bảng màu Kinh thánh"): nhận diện kênh `channel-k2/NHAN-DIEN.md` §2 (mực, chữ, thép, cam, lục lam, hổ phách; trùng
`design/k2v/common.js` C) + cặp SEPIA quá khứ của Kinh thánh §4 (mực nâu/giấy của `design/k2v/relief.js`). Số đo (CIEDE2000, D65):
  ΔE_trung_thanh   ΔE00(LUT(p), p) của từng màu nhận diện — chữ/đồ hoạ đã vẽ đúng bảng màu KHÔNG được đổi (đích ≤ 2, nhận ra ≥ 3)
  ΔE_bang_mau      trung bình có trọng số (theo diện tích) của ΔE00 từ 8 màu chủ đạo của khung (k-means Lab) tới màu gần nhất của bảng
  ΔE_dich          ΔE00 trung bình từng điểm ảnh trước/sau (độ mạnh của LUT)
  tương phản chữ   WCAG #EEF1F4 trên #0F1722 sau LUT (≥ 7:1 như NHAN-DIEN)
"""
import json, os, subprocess, sys, tempfile
import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
N = 33
PALETTE = {   # NHAN-DIEN.md §2 + design/k2v/common.js (C) · sepia: design/k2v/relief.js (close.ink/paper)
    'ink': '#0F1722', 'ink2': '#16212F', 'text': '#EEF1F4', 'steel': '#9AA7B5', 'dim': '#B9C3CE',
    'orange': '#F08A4B', 'teal': '#3CC2B0', 'amber': '#F2C14E', 'sepia_ink': '#2A1C10', 'sepia_paper': '#F1E4C6'}
IDENTITY = ['ink', 'ink2', 'text', 'steel', 'dim', 'orange', 'teal', 'amber']   # màu đồ hoạ của kênh: phải giữ nguyên
# 12 mốc trên master T1 (k2c-t1-06, 15:41) rải đủ loại shot: cảnh 3D, bản đồ, biểu đồ, ảnh lưu trữ, văn bản, footage Pexels (178,5 · 340 · 509 s), thẻ
T1_AT = [8.0, 44.0, 95.0, 178.5, 190.0, 340.0, 470.0, 509.0, 515.0, 600.0, 830.0, 900.0]
T1_REF = dict(lfs_branch='release-k2c-t1-06-v1', lfs_path='k2c-t1-06-v1-master.mp4')


# ---------- màu ----------
def hex2rgb(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float) / 255


def srgb2lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin2srgb(c): c = np.clip(c, 0, 1); return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def rgb2lab(rgb):
    """sRGB 0..1 (…×3) → CIELAB D65."""
    l = srgb2lin(np.asarray(rgb, float))
    M = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = l @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def de2000(a, b):
    """CIEDE2000 giữa hai mảng Lab (…×3). Sharma, Wu & Dalal (2005)."""
    L1, a1, b1 = a[..., 0], a[..., 1], a[..., 2]; L2, a2, b2 = b[..., 0], b[..., 1], b[..., 2]
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2); Cm = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cm ** 7 / (Cm ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2; C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p, h2p = np.degrees(np.arctan2(b1, a1p)) % 360, np.degrees(np.arctan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dh = h2p - h1p; dh = np.where(C1p * C2p == 0, 0, np.where(dh > 180, dh - 360, np.where(dh < -180, dh + 360, dh)))
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dh / 2))
    Lpm, Cpm = (L1 + L2) / 2, (C1p + C2p) / 2
    hs = h1p + h2p
    hpm = np.where(C1p * C2p == 0, hs, np.where(np.abs(h1p - h2p) <= 180, hs / 2, np.where(hs < 360, (hs + 360) / 2, (hs - 360) / 2)))
    T = 1 - 0.17 * np.cos(np.radians(hpm - 30)) + 0.24 * np.cos(np.radians(2 * hpm)) + 0.32 * np.cos(np.radians(3 * hpm + 6)) - 0.20 * np.cos(np.radians(4 * hpm - 63))
    dth = 30 * np.exp(-(((hpm - 275) / 25) ** 2)); Rc = 2 * np.sqrt(Cpm ** 7 / (Cpm ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lpm - 50) ** 2 / np.sqrt(20 + (Lpm - 50) ** 2); Sc = 1 + 0.045 * Cpm; Sh = 1 + 0.015 * Cpm * T
    Rt = -np.sin(np.radians(2 * dth)) * Rc
    return np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def wcag(c1, c2):
    y = lambda c: float(srgb2lin(np.asarray(c, float)) @ np.array([0.2126, 0.7152, 0.0722]))
    a, b = sorted((y(c1), y(c2)), reverse=True); return (a + 0.05) / (b + 0.05)


# ---------- công thức LUT ứng viên (trên sRGB 0..1, mảng …×3) ----------
def _luma(c): return c @ np.array([0.2126, 0.7152, 0.0722])


def _sat(c, k):
    y = _luma(c)[..., None]; return y + (c - y) * k


def _hue_w(c, centers, width=28):
    """trọng số 0..1 theo khoảng cách sắc độ HSV tới các tâm (độ), nhân độ bão hoà — để bảo vệ màu nhấn."""
    mx, mn = c.max(-1), c.min(-1); d = mx - mn + 1e-9; r, g, b = c[..., 0], c[..., 1], c[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = np.where(mx > 0, d / (mx + 1e-9), 0)
    w = np.zeros_like(h)
    for c0 in centers:
        dd = np.abs((h - c0 + 180) % 360 - 180); w = np.maximum(w, np.clip(1 - dd / width, 0, 1))
    return (w * np.clip(s * 1.6, 0, 1))[..., None]


def _curve(c, s):
    """S nhẹ quanh 0,5 trên giá trị gamma (s = độ mạnh 0..1)."""
    sm = c * c * (3 - 2 * c); return c + (sm - c) * s


def _split(c, shadow, high, ks, kh):
    """ám bóng tối về `shadow`, vùng sáng về `high` (chênh so với xám cùng độ sáng), theo độ sáng."""
    y = _luma(c)[..., None]
    sh = hex2rgb(shadow); sh = sh - _luma(sh); hi = hex2rgb(high); hi = hi - _luma(hi)
    return c + sh * ks * (1 - y) ** 2 + hi * kh * y ** 2


ACCENT_HUES = [22, 42, 172]   # cam #F08A4B, hổ phách #F2C14E, lục lam #3CC2B0


def lut_thep_lanh(c):
    """A — THÉP LẠNH: bóng tối ám mực xanh đen của kênh, vùng sáng trắng lạnh #EEF1F4, giảm bão hoà màu nền 12 %, giữ màu nhấn, S nhẹ."""
    w = _hue_w(c, ACCENT_HUES)
    x = _split(c, '#0F1722', '#EEF1F4', 1.6, 0.6)
    x = w * c + (1 - w) * _sat(x, 0.88)
    return _curve(np.clip(x, 0, 1), 0.18)


def lut_trung_tinh(c):
    """B — TRUNG TÍNH: chỉnh nhẹ — S 10 %, bóng tối ám mực 0,8, không đổi bão hoà; an toàn nhất cho ảnh lưu trữ/footage."""
    x = _split(c, '#0F1722', '#EEF1F4', 0.8, 0.3)
    return _curve(np.clip(x, 0, 1), 0.10)


def lut_cam_lam(c):
    """C — CAM–LỤC LAM: tách tông mạnh: bóng tối về lục lam đậm, vùng sáng về hổ phách, +8 % bão hoà, S 22 % (kiểu "phim bom tấn")."""
    x = _split(c, '#1E5A60', '#F2C14E', 1.4, 0.55)
    x = _sat(x, 1.08)
    return _curve(np.clip(x, 0, 1), 0.22)


CANDIDATES = {'k2-a-thep-lanh': (lut_thep_lanh, True), 'k2-b-trung-tinh': (lut_trung_tinh, True), 'k2-c-cam-lam': (lut_cam_lam, False)}


def lock_palette(grid, fn, keys=IDENTITY, sigma=0.09):
    """khoá màu nhận diện: cộng hiệu chỉnh Gauss (RBF trong RGB) để LUT(p) = p tại từng màu nhận diện, giảm dần ra xa (σ RGB)."""
    P = np.array([hex2rgb(PALETTE[k]) for k in keys]); R = P - fn(P)        # sai lệch tại màu bảng
    K = np.exp(-((P[:, None, :] - P[None, :, :]) ** 2).sum(-1) / (2 * sigma ** 2))
    W = np.linalg.solve(K + 1e-6 * np.eye(len(P)), R)                       # nội suy đúng tại các điểm bảng
    out = fn(grid); d = ((grid[..., None, :] - P) ** 2).sum(-1)
    return np.clip(out + np.exp(-d / (2 * sigma ** 2)) @ W, 0, 1)


def build(name):
    fn, lock = CANDIDATES[name]
    v = np.linspace(0, 1, N); b, g, r = np.meshgrid(v, v, v, indexing='ij')   # .cube: R chạy nhanh nhất
    grid = np.stack([r, g, b], -1).reshape(-1, 3)
    return (lock_palette(grid, fn) if lock else np.clip(fn(grid), 0, 1)), lock


def write_cube(path, name, rgb, lock):
    fn = CANDIDATES[name][0]
    with open(path, 'w') as f:
        f.write(f'# cine-lab kênh 2 — LUT ứng viên {name} (scripts/common/lut.py, V5a 15/10/2026). Tự tạo, không dựa LUT của bên thứ ba.\n')
        f.write(f'# {(fn.__doc__ or "đồng nhất").strip()}\n# khoá màu nhận diện NHAN-DIEN §2: {"có" if lock else "không"}. Áp offline bằng ffmpeg lut3d; CHƯA gắn vào render.\n')
        f.write(f'TITLE "{name}"\nLUT_3D_SIZE {N}\nDOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n')
        for x in rgb: f.write(f'{x[0]:.6f} {x[1]:.6f} {x[2]:.6f}\n')


def read_cube(path):
    n, rows = None, []
    for l in open(path):
        l = l.strip()
        if l.startswith('LUT_3D_SIZE'): n = int(l.split()[1])
        elif l and (l[0].isdigit() or l[0] in '-.'): rows.append([float(x) for x in l.split()])
    return n, np.array(rows)


def cube_eval(path, rgb):
    """nội suy ba tuyến tính LUT .cube tại các màu sRGB (để đo trung thành bảng màu không cần ffmpeg)."""
    n, T = read_cube(path); T = T.reshape(n, n, n, 3)   # [b][g][r]
    p = np.clip(np.asarray(rgb, float), 0, 1) * (n - 1); i0 = np.floor(p).astype(int).clip(0, n - 2); f = p - i0
    out = 0
    for dr in (0, 1):
        for dg in (0, 1):
            for db in (0, 1):
                w = (f[..., 0] if dr else 1 - f[..., 0]) * (f[..., 1] if dg else 1 - f[..., 1]) * (f[..., 2] if db else 1 - f[..., 2])
                out = out + w[..., None] * T[i0[..., 2] + db, i0[..., 1] + dg, i0[..., 0] + dr]
    return out


# ---------- khung, áp, đo ----------
def frames(out, src='t1', ats=None):
    os.makedirs(out, exist_ok=True); ats = ats or T1_AT
    if src == 't1':
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import golden
        src, oid = golden.lfs_href(T1_REF['lfs_branch'], T1_REF['lfs_path']); label = f"LFS {T1_REF['lfs_branch']}:{T1_REF['lfs_path']} oid {oid[:12]}"
    else:
        label = src
    meta = []
    for i, t in enumerate(ats, 1):
        p = os.path.join(out, f'f{i:02d}.png')
        r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', p], capture_output=True, text=True, timeout=300)
        if r.returncode: raise SystemExit(f'không trích được khung {t}s: {r.stderr[-200:]}')
        meta.append(dict(f=os.path.basename(p), t=t))
    json.dump(dict(nguon=label, khung=meta), open(os.path.join(out, 'frames.json'), 'w'), ensure_ascii=False, indent=1)
    return meta


def apply(cube, src, dst):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', f"lut3d=file='{cube}':interp=tetrahedral", '-frames:v', '1', dst],
                       capture_output=True, text=True, timeout=300)
    if r.returncode: raise SystemExit(f'ffmpeg lut3d lỗi: {r.stderr[-300:]}')


def load(p, w=480):
    from PIL import Image
    im = Image.open(p).convert('RGB'); im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    return np.asarray(im, float) / 255


def palette_de(img, k=8):
    """8 màu chủ đạo (k-means Lab, cv2) → ΔE00 tới màu bảng gần nhất, trọng số diện tích."""
    import cv2
    lab = rgb2lab(img.reshape(-1, 3)).astype(np.float32)
    _, lbl, cen = cv2.kmeans(lab, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.2), 3, cv2.KMEANS_PP_CENTERS)
    cv2.setRNGSeed(0)
    wts = np.bincount(lbl.ravel(), minlength=k) / len(lbl)
    P = rgb2lab(np.array([hex2rgb(v) for v in PALETTE.values()]))
    d = de2000(cen[:, None, :].astype(float), P[None, :, :]).min(1)
    return float((d * wts).sum())


def fidelity(cube):
    P = np.array([hex2rgb(PALETTE[k]) for k in IDENTITY]); Q = cube_eval(cube, P)
    de = de2000(rgb2lab(P), rgb2lab(Q))
    t, i = Q[IDENTITY.index('text')], Q[IDENTITY.index('ink')]
    return {k: round(float(v), 2) for k, v in zip(IDENTITY, de)}, round(wcag(t, i), 2)


def study(fdir, luts, out):
    import cv2
    cv2.setRNGSeed(0)
    os.makedirs(out, exist_ok=True); fm = json.load(open(os.path.join(fdir, 'frames.json')))
    res = dict(nguon=fm['nguon'], bang_mau=PALETTE, luts={}, khung=[])
    for c in luts:
        fid, cr = fidelity(c); SP = np.array([hex2rgb(PALETTE[k]) for k in ('sepia_ink', 'sepia_paper')])
        sep = de2000(rgb2lab(SP), rgb2lab(cube_eval(c, SP)))   # cặp sepia quá khứ: không khoá, chỉ báo LUT kéo giấy/mực đi bao xa
        res['luts'][os.path.basename(c)] = dict(de_trung_thanh=fid, de_trung_thanh_max=max(fid.values()), tuong_phan_chu=cr,
                                                de_sepia=dict(sepia_ink=round(float(sep[0]), 2), sepia_paper=round(float(sep[1]), 2)))
    for k in fm['khung']:
        src = os.path.join(fdir, k['f']); a = load(src); row = dict(f=k['f'], t=k['t'], goc=dict(de_bang_mau=round(palette_de(a), 2)))
        for c in luts:
            n = os.path.splitext(os.path.basename(c))[0]; dst = os.path.join(out, f"{os.path.splitext(k['f'])[0]}-{n}.png"); apply(c, src, dst)
            b = load(dst)
            row[n] = dict(de_bang_mau=round(palette_de(b), 2), de_dich=round(float(de2000(rgb2lab(a), rgb2lab(b)).mean()), 2))
        res['khung'].append(row)
    for c in luts:
        n = os.path.splitext(os.path.basename(c))[0]; L = res['luts'][os.path.basename(c)]
        L['de_bang_mau_tb'] = round(float(np.mean([r[n]['de_bang_mau'] for r in res['khung']])), 2)
        L['de_dich_tb'] = round(float(np.mean([r[n]['de_dich'] for r in res['khung']])), 2)
        L['khung_gan_hon'] = sum(r[n]['de_bang_mau'] < r['goc']['de_bang_mau'] for r in res['khung'])
    res['goc_de_bang_mau_tb'] = round(float(np.mean([r['goc']['de_bang_mau'] for r in res['khung']])), 2)
    json.dump(res, open(os.path.join(out, 'study.json'), 'w'), ensure_ascii=False, indent=1)
    sheet(fdir, out, luts, res); return res


def sheet(fdir, out, luts, res, w=400):
    """tờ so sánh: mỗi hàng một khung — GỐC | từng LUT, nhãn ΔE bảng màu / ΔE dịch dưới mỗi ô; thêm ô mẫu bảng màu qua LUT."""
    from PIL import Image, ImageDraw, ImageFont
    try: ft = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 15); fb = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 17)
    except OSError: ft = fb = ImageFont.load_default()
    names = [os.path.splitext(os.path.basename(c))[0] for c in luts]; cols = ['GỐC (T1 phát hành)'] + names
    h = round(w * 9 / 16); lab = 24; head = 36; sw = 46
    W, H = w * len(cols), head + (h + lab) * len(res['khung']) + sw + lab
    S = Image.new('RGB', (W, H), (15, 23, 34)); d = ImageDraw.Draw(S)
    for j, c in enumerate(cols): d.text((j * w + 8, 9), c, fill=(238, 241, 244), font=fb)
    for i, r in enumerate(res['khung']):
        y = head + i * (h + lab)
        for j, c in enumerate(cols):
            p = os.path.join(fdir, r['f']) if j == 0 else os.path.join(out, f"{os.path.splitext(r['f'])[0]}-{c}.png")
            S.paste(Image.open(p).convert('RGB').resize((w - 4, h - 2), Image.LANCZOS), (j * w + 2, y))
            m = r['goc'] if j == 0 else r[c]
            txt = f"{r['f']} @{r['t']:.0f}s · ΔE bảng {m['de_bang_mau']}" + (f" · ΔE dịch {m['de_dich']}" if j else '')
            d.text((j * w + 6, y + h + 3), txt, fill=(185, 195, 206), font=ft)
    y = head + len(res['khung']) * (h + lab)
    P = np.array([hex2rgb(PALETTE[k]) for k in IDENTITY])
    for j, c in enumerate(cols):
        Q = P if j == 0 else cube_eval(luts[j - 1], P)
        for k, q in enumerate(Q):
            x0 = j * w + 4 + k * ((w - 8) // len(IDENTITY)); d.rectangle([x0, y, x0 + (w - 8) // len(IDENTITY) - 3, y + sw - 4], fill=tuple(int(v * 255 + 0.5) for v in q))
        f = res['luts'].get(os.path.basename(luts[j - 1])) if j else None
        d.text((j * w + 6, y + sw + 2), 'bảng màu nhận diện (gốc)' if not j else f"qua LUT · ΔE trung thành max {f['de_trung_thanh_max']} · chữ/nền {f['tuong_phan_chu']}:1",
               fill=(185, 195, 206), font=ft)
    p = os.path.join(out, 'LUT-SO-SANH.jpg'); S.save(p, quality=88); return p


def self_test():
    ok = 0; n = 0
    # CIEDE2000: ca chuẩn của Sharma 2005 (cặp 1, 7, 17, 25)
    for L1, L2, want in [((50, 2.6772, -79.7751), (50, 0, -82.7485), 2.0425), ((50, 0, 0), (50, -1, 2), 2.3669),
                         ((50, 2.5, 0), (73, 25, -18), 27.1492), ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644)]:
        n += 1; got = float(de2000(np.array(L1, float), np.array(L2, float))); ok += abs(got - want) < 1e-3
        print(('ĐẠT ' if abs(got - want) < 1e-3 else 'SAI ') + f'ΔE00 {got:.4f} (chuẩn {want})')
    with tempfile.TemporaryDirectory() as d:
        for name in CANDIDATES:
            rgb, lock = build(name); p = os.path.join(d, name + '.cube'); write_cube(p, name, rgb, lock)
            fid, cr = fidelity(p)
            if lock:
                n += 1; good = max(fid.values()) <= 1.0; ok += good; print(('ĐẠT ' if good else 'SAI ') + f'{name} khoá bảng màu: ΔE max {max(fid.values())}')
        # LUT đồng nhất → ΔE 0 qua ffmpeg
        v = np.linspace(0, 1, N); b, g, r = np.meshgrid(v, v, v, indexing='ij'); I = np.stack([r, g, b], -1).reshape(-1, 3)
        CANDIDATES['_id'] = (lambda c: c, False); p = os.path.join(d, 'id.cube'); write_cube(p, '_id', I, False); del CANDIDATES['_id']
        from PIL import Image
        src = os.path.join(d, 's.png'); Image.fromarray((np.random.default_rng(1).random((90, 160, 3)) * 255).astype(np.uint8)).save(src)
        dst = os.path.join(d, 'o.png'); apply(p, src, dst)
        diff = np.abs(np.asarray(Image.open(src), int) - np.asarray(Image.open(dst), int)).max()
        n += 1; ok += diff <= 1; print(('ĐẠT ' if diff <= 1 else 'SAI ') + f'LUT đồng nhất qua ffmpeg lut3d: lệch tối đa {diff} mức')
    print(f'self-test: {ok}/{n}'); return ok == n


def main():
    a = sys.argv[1:]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    if not a: print(__doc__); sys.exit(2)
    if a[0] == '--self-test': sys.exit(0 if self_test() else 1)
    if a[0] == 'make':
        out = opt('--out', os.path.join(REPO, 'assets/k2/lut')); os.makedirs(out, exist_ok=True)
        for name in CANDIDATES:
            rgb, lock = build(name); p = os.path.join(out, name + '.cube'); write_cube(p, name, rgb, lock); fid, cr = fidelity(p)
            print(f'{p}: ΔE trung thành max {max(fid.values())}, chữ/nền {cr}:1')
    elif a[0] == 'frames':
        ats = [float(x) for x in opt('--at').split(',')] if opt('--at') else None; m = frames(opt('--out'), opt('--src', 't1'), ats); print(f'{len(m)} khung → {opt("--out")}')
    elif a[0] == 'apply': apply(a[1], a[2], a[3])
    elif a[0] == 'study':
        luts = opt('--luts', ','.join(os.path.join(REPO, 'assets/k2/lut', n + '.cube') for n in CANDIDATES)).split(',')
        r = study(opt('--frames'), luts, opt('--out'))
        print(json.dumps(dict(goc=r['goc_de_bang_mau_tb'], luts=r['luts']), ensure_ascii=False, indent=1))
    else: print(__doc__); sys.exit(2)


if __name__ == '__main__':
    main()
