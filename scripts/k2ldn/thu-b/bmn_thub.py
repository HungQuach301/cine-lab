#!/opt/cine/bin/python
"""THU-B-T4 · (B) AI phủ bề mặt nhà thường — chuẩn bị, ghép, chiếu, timelapse, khai kiểm (K-1.17.5 §7 BE-MAT-NHA; Kinh thánh §15 (j) ĐANG THỬ).
  bmn_thub.py prep <khung>                 → $THUB/bp/<khung>/: render.png (V2 + LUT kênh A = "render-khớp"), vao.jpg (ảnh vào AI; 1666 KHÔNG khói bếp), matna.png (lớp + nha_thuong),
                                             mat_na_nha.png, mat_na_mat.png, bong.png, albedo.png, nha.json [{id, lo, px_m}], do-duoc.png, prep.json (% nhà đo được…)
  bmn_thub.py ghep <khung> <tag> <ai.jpg>  → <tag>/ghep.png (+ nen.png khi có lớp sống), ghep.json — AI CHỈ trong nhà đo được nở 1 px (không lấn lớp (a)/nước); ngoài = render 0/255
  bmn_thub.py proj <khung> <tag> [vòng]    → <tag>/proj.png (albedo đã khử sáng, RGBA; A = nhà đo được) + proj.json (ma trận chiếu VP) — vòng ≥ 1: hiệu chỉnh theo khung 0 đã dựng
  bmn_thub.py tl <khung> <tag>             → <tag>/tl-anh_tinh.mp4, tl-chieu_3d.mp4, tl-render.mp4 (640×360, 3 s, LUT A, x264 crf 10)
Nhà ĐO ĐƯỢC (K-1.17.5 §5.1/§6, cùng định nghĩa): ≥ 2 px/m (1 m ngang chiếu tại tâm nhà, quy 1080p), ≥ 100 px, ≥ 40 điểm cạnh hình học (biên mã nhà ∪ biên mã mặt phẳng)
có gradient ≥ 3 ở cả render (màu Lab, σ 1) và pass bóng (L*, σ 1)."""
import json, os, subprocess, sys
import numpy as np, cv2
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
THUB = os.environ.get('THUB', '/var/tmp/ldn/thub'); RR = f'{THUB}/r'; BP = f'{THUB}/bp'; D = os.environ.get('LDN_DATA', '/var/tmp/ldn')
LUT = os.path.join(REPO, 'channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube')
NAM = {'M1-trung': 1666, 'M4-trung': 2026, 'B3-p4-1938': 1938}
SONG = {'M1-trung'}                       # khung có khói bếp (lớp sống, ghép cộng hiệu render có/không khói)
PAL = {'troi': (40, 80, 200), 'nuoc': (0, 170, 190), 'bang': (200, 170, 90), 'suon': (150, 120, 70), 'nha': (235, 235, 235), 'nha_thuong': (215, 215, 215),
       'tau': (255, 0, 0), 'khac': (128, 128, 128), 'cay': (60, 140, 60)}
NEN_CHO = ('troi', 'bang', 'suon', 'cay')   # vòng nở 1 px của nhà đo được chỉ được lấn vào lớp nền (không lấn lớp (a), không lấn nước)
E0, N0 = 532000.0, 180800.0


def lut(src, dst):
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', src, '-vf', f"lut3d=file='{LUT}':interp=tetrahedral", dst], check=True)


def lop(m, k): return np.all(m == np.array(PAL[k][::-1]), -1)
def dec24(im): im = im.astype(np.int64); return (im[..., 2] << 16) | (im[..., 1] << 8) | im[..., 0]
def enc24(a): a = a.astype(np.int64); return np.stack([a & 255, (a >> 8) & 255, (a >> 16) & 255], -1).astype(np.uint8)
def s2l(x): x = x / 255.0; return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
def l2s(x): x = np.clip(x, 0, 1); return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055) * 255.0


def grad(b, sig, mau=False):
    """như K (reports/k1175/do/ma/bmn.py): độ lớn gradient L* (hoặc ΔE76 Lab khi mau) mỗi px sau mờ Gauss σ"""
    x = cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32)
    x = cv2.GaussianBlur(x, (0, 0), sig); ch = range(3) if mau else (0,)
    return np.sqrt(sum((cv2.Sobel(x[..., c], cv2.CV_32F, 1, 0, ksize=3) / 8) ** 2 + (cv2.Sobel(x[..., c], cv2.CV_32F, 0, 1, ksize=3) / 8) ** 2 for c in ch))


def bien(M):
    b = np.zeros(M.shape, bool)
    b[:-1] |= M[:-1] != M[1:]; b[1:] |= M[1:] != M[:-1]; b[:, :-1] |= M[:, :-1] != M[:, 1:]; b[:, 1:] |= M[:, 1:] != M[:, :-1]
    return b


def cam(logp):
    f = json.load(open(logp))['frames'][0]; V = np.array(f['view']).reshape(4, 4).T; P = np.array(f['proj']).reshape(4, 4).T; return V, P


def chieu(V, P, X, W, H):
    p = (P @ V @ np.c_[X, np.ones(len(X))].T).T; ndc = p[:, :3] / p[:, 3:4]
    return np.c_[(ndc[:, 0] + 1) / 2 * W, (1 - ndc[:, 1]) / 2 * H], p[:, 3]


def prep(k):
    o = f'{BP}/{k}'; os.makedirs(o, exist_ok=True)
    lut(f'{RR}/{k}-v2/00000.png', f'{o}/render.png')
    if k in SONG: lut(f'{RR}/{k}-v2-kk/00000.png', f'{o}/render-khong.png')
    vao = cv2.imread(f'{o}/render-khong.png' if k in SONG else f'{o}/render.png'); cv2.imwrite(f'{o}/vao.jpg', vao, [cv2.IMWRITE_JPEG_QUALITY, 95])
    M1 = cv2.imread(f'{RR}/{k}-m1/00000.png'); IID = dec24(cv2.imread(f'{RR}/{k}-m3/00000.png')); PID = dec24(cv2.imread(f'{RR}/{k}-m4/00000.png'))
    nha = json.load(open(f'{D}/look3b/nha.json')); la = ~np.isin(IID, np.array([int(x) for x in nha], np.int64)) & (IID > 0); n_la = int(la.sum()); IID[la] = 0; PID[la] = 0   # mã không có trong bảng nhà (vài điểm ảnh lẻ) → 0
    cv2.imwrite(f'{o}/matna.png', M1); cv2.imwrite(f'{o}/mat_na_nha.png', enc24(IID)); cv2.imwrite(f'{o}/mat_na_mat.png', enc24(PID))
    cv2.imwrite(f'{o}/bong.png', cv2.imread(f'{RR}/{k}-bong/00000.png')); cv2.imwrite(f'{o}/albedo.png', cv2.imread(f'{RR}/{k}-m6/00000.png'))
    R = cv2.imread(f'{o}/render.png'); BO = cv2.imread(f'{o}/bong.png'); H, W = IID.shape; s = H / 1080.0
    # nhất quán mặt nạ: điểm mã nhà > 0 phải là lớp nha_thuong
    nt = lop(M1, 'nha_thuong'); lech = int(((IID > 0) != nt).sum())
    V, P = cam(f'{RR}/{k}-v2/log.json')
    ids, cnt = np.unique(IID[IID > 0], return_counts=True)
    X = np.array([[nha[str(i)]['E'] - E0, (nha[str(i)]['y0'] + nha[str(i)]['y1']) / 2, -(nha[str(i)]['N'] - N0)] for i in ids])
    right = V[0, :3] / np.linalg.norm(V[0, :3]); right = right - np.array([0, right[1], 0]); right /= np.linalg.norm(right)
    a, w0 = chieu(V, P, X, W, H); b, _ = chieu(V, P, X + right, W, H); ppm = np.hypot(*(b - a).T) / s
    gR = grad(R, 1.0 * s, True); gB = grad(BO, 1.0 * s); GE = (bien(IID) | bien(PID)) & (gR >= 3) & (gB >= 3)
    ec = np.bincount(IID[GE].ravel(), minlength=int(IID.max()) + 1)
    rows = []; meas = []
    for i, c, pm in zip(ids, cnt, ppm):
        e = int(ec[i]); d = bool(pm >= 2.0 and c >= 100 * s * s and e >= 40)
        rows.append({'id': int(i), 'lo': nha[str(i)]['lo'] if not str(nha[str(i)]['lo']).startswith('osm:') else int(str(nha[str(i)]['lo'])[4:]), 'px_m': round(float(pm), 3),
                     'px': int(c), 'n_canh': e, 'do_duoc': d, 'k': nha[str(i)]['k']})
        if d: meas.append(int(i))
    MM = np.isin(IID, np.array(meas, np.int64)); cv2.imwrite(f'{o}/do-duoc.png', (MM * 255).astype(np.uint8))
    json.dump([{kk: r[kk] for kk in ('id', 'lo', 'px_m')} for r in rows], open(f'{o}/nha.json', 'w'))
    json.dump(rows, open(f'{o}/nha-chi-tiet.json', 'w'))
    st = dict(khung=k, nam=NAM[k], nha_thay=len(rows), nha_do_duoc=len(meas), pct_nha_do_duoc=round(100 * len(meas) / max(1, len(rows)), 1),
              px_nha_thuong_pct=round(float((IID > 0).mean() * 100), 2), px_nha_do_duoc_pct=round(float(MM.mean() * 100), 2),
              pct_dien_tich_nha_do_duoc=round(100 * float(MM.sum()) / max(1, float((IID > 0).sum())), 1), lech_ma_nha_vs_lop=lech, ma_la_px=n_la,
              px_m_trung_vi=round(float(np.median(ppm)), 2), px_m_trung_vi_do_duoc=round(float(np.median([r['px_m'] for r in rows if r['do_duoc']] or [0])), 2),
              loai_do_khong_duoc={'px_m<2': sum(1 for r in rows if r['px_m'] < 2), 'px<100': sum(1 for r in rows if r['px'] < 100 * s * s), 'canh<40': sum(1 for r in rows if r['n_canh'] < 40)},
              theo_lop={str(kk): [sum(1 for r in rows if r['k'] == kk), sum(1 for r in rows if r['k'] == kk and r['do_duoc'])] for kk in (1, 3, 4, 10)})
    json.dump(st, open(f'{o}/prep.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(st, ensure_ascii=False))


def vung_ai(o):
    MM = cv2.imread(f'{o}/do-duoc.png', 0) > 127; M1 = cv2.imread(f'{o}/matna.png')
    nen = np.zeros(MM.shape, bool)
    for kk in NEN_CHO: nen |= lop(M1, kk)
    dil = cv2.dilate(MM.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    return MM | (dil & nen)


def ghep(k, tag, ai):
    o = f'{BP}/{k}'; t = f'{o}/{tag}'; os.makedirs(t, exist_ok=True)
    R = cv2.imread(f'{o}/render.png'); H, W = R.shape[:2]; A = cv2.resize(cv2.imread(ai), (W, H), interpolation=cv2.INTER_LANCZOS4)
    MA = vung_ai(o); base = cv2.imread(f'{o}/render-khong.png') if k in SONG else R
    # khớp tông AI VÀO tông render đã duyệt (Lab: trung bình + độ lệch chuẩn trong vùng AI, k = 0,7 — một phép toàn cục, tất định; ngược chiều tấm nền §15 b vì ở đây render là nền)
    lab = lambda x: cv2.cvtColor(x, cv2.COLOR_BGR2LAB).astype(np.float32); Al, Bl = lab(A), lab(base); kk = 0.7
    ma, sa = Al[MA].mean(0), Al[MA].std(0) + 1e-3; mb, sb = Bl[MA].mean(0), Bl[MA].std(0) + 1e-3
    AK = cv2.cvtColor(np.clip((Al - ma) * (1 + kk * (sb / sa - 1)) + ma + kk * (mb - ma), 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    # viền mềm 2 px PHÍA TRONG vùng AI (ngoài vùng vẫn đúng render 0/255)
    al = np.clip(cv2.distanceTransform(MA.astype(np.uint8), cv2.DIST_L2, 3) / 2.0, 0, 1)[..., None]
    NEN = np.where(MA[..., None], np.round(al * AK + (1 - al) * base), base).astype(np.uint8); A = AK
    if k in SONG:
        cv2.imwrite(f'{t}/nen.png', NEN); G = np.clip(NEN.astype(np.int16) + (R.astype(np.int16) - base.astype(np.int16)), 0, 255).astype(np.uint8)
    else: G = NEN
    cv2.imwrite(f'{t}/ghep.png', G); cv2.imwrite(f'{t}/ghep.jpg', G, [cv2.IMWRITE_JPEG_QUALITY, 93]); cv2.imwrite(f'{t}/ai-1080.png', A)
    out = ~MA; b = int(np.abs(G.astype(int) - R.astype(int))[out].max()) if out.any() else 0
    rec = dict(khung=k, tag=tag, ai=os.path.relpath(ai, REPO) if ai.startswith(REPO) else ai, pct_diem_anh_ai=round(float(MA.mean() * 100), 2), b_ngoai_vung_max=b,
               khop_tong=dict(k=kk, mean_ai=ma.round(2).tolist(), mean_render=mb.round(2).tolist(), std_ai=sa.round(2).tolist(), std_render=sb.round(2).tolist()), vien_mem_px=2,
               sha_ghep=__import__('hashlib').sha256(open(f'{t}/ghep.png', 'rb').read()).hexdigest())
    json.dump(rec, open(f'{t}/ghep.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(rec, ensure_ascii=False))


def proj(k, tag, vong=0):
    """albedo đã khử sáng = albedo render × (ảnh ghép / render) (tuyến tính) trong nhà đo được; vòng ≥ 1: × (ghép / khung 0 đã dựng bằng chiếu) — hiệu chỉnh phi tuyến LUT/ánh xạ tông"""
    o = f'{BP}/{k}'; t = f'{o}/{tag}'
    MM = cv2.imread(f'{o}/do-duoc.png', 0) > 127; ALB = s2l(cv2.imread(f'{o}/albedo.png').astype(np.float64))
    base = cv2.imread(f'{t}/nen.png') if k in SONG else cv2.imread(f'{t}/ghep.png')
    R0 = cv2.imread(f'{o}/render-khong.png') if k in SONG else cv2.imread(f'{o}/render.png')
    if vong == 0:
        Q = (s2l(base.astype(np.float64)) + 2e-3) / (s2l(R0.astype(np.float64)) + 2e-3); A = ALB * np.clip(Q, 0.2, 5.0)
    else:
        prev = cv2.imread(f'{t}/proj.png', cv2.IMREAD_UNCHANGED); Ap = s2l(prev[..., :3].astype(np.float64))
        lut(f'{RR}/{k}-bp-{tag}/00000.png', f'{t}/khung0-v{vong - 1}.png'); C0 = cv2.imread(f'{t}/khung0-v{vong - 1}.png')
        if k in SONG: C0 = np.clip(C0.astype(np.int16) - (cv2.imread(f'{o}/render.png').astype(np.int16) - R0.astype(np.int16)), 0, 255).astype(np.uint8)
        Q = (s2l(base.astype(np.float64)) + 2e-3) / (s2l(C0.astype(np.float64)) + 2e-3); A = Ap * np.clip(Q, 0.5, 2.0)
    A = np.clip(A, 0.004, 0.95); out = np.zeros(MM.shape + (4,), np.uint8); out[..., :3] = np.round(l2s(A)).astype(np.uint8); out[..., 3] = MM * 255
    cv2.imwrite(f'{t}/proj.png', out)
    V, P = cam(f'{RR}/{k}-v2/log.json'); VP = P @ V
    json.dump({'vp': VP.T.ravel().tolist(), 'vong': vong, 'ghi_chu': 'VP = proj · view của máy khung V2 (cột trước, như three.js elements)'}, open(f'{t}/proj.json', 'w'))
    print('proj', k, tag, 'vòng', vong)


def mp4(frames_glob, dst, extra_vf=''):
    vf = f"lut3d=file='{LUT}':interp=tetrahedral" + (',' + extra_vf if extra_vf else '')
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-framerate', '24', '-i', frames_glob, '-vf', vf, '-c:v', 'libx264', '-preset', 'slow', '-crf', '10', '-pix_fmt', 'yuv420p', dst], check=True)


def tl(k, tag):
    o = f'{BP}/{k}'; t = f'{o}/{tag}'; tmp = f'{t}/tl-tmp'; os.makedirs(tmp, exist_ok=True)
    mp4(f'{RR}/tl-{k}-v2/%05d.png', f'{t}/tl-render.mp4')
    mp4(f'{RR}/tl-{k}-bp-{tag}/%05d.png', f'{t}/tl-chieu_3d.mp4')
    # (i) ảnh tĩnh: tấm AI dán cố định mọi khung trong nhà đo được (640×360), ngoài = render khung đó (1666: cộng hiệu khói bếp)
    MA = cv2.resize(vung_ai(o).astype(np.uint8), (640, 360), interpolation=cv2.INTER_NEAREST) > 0
    A = cv2.resize(cv2.imread(f'{t}/ai-1080.png'), (640, 360), interpolation=cv2.INTER_AREA)
    n = len([x for x in os.listdir(f'{RR}/tl-{k}-v2') if x.endswith('.png')])
    for i in range(n):
        lut(f'{RR}/tl-{k}-v2/{i:05d}.png', f'{tmp}/r.png'); Rt = cv2.imread(f'{tmp}/r.png')
        if k in SONG:
            lut(f'{RR}/tl-{k}-v2-kk/{i:05d}.png', f'{tmp}/rk.png'); Rk = cv2.imread(f'{tmp}/rk.png')
            G = np.clip(np.where(MA[..., None], A, Rk).astype(np.int16) + Rt.astype(np.int16) - Rk.astype(np.int16), 0, 255).astype(np.uint8)
        else: G = np.where(MA[..., None], A, Rt)
        cv2.imwrite(f'{tmp}/{i:05d}.png', G)
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-framerate', '24', '-i', f'{tmp}/%05d.png', '-c:v', 'libx264', '-preset', 'slow', '-crf', '10', '-pix_fmt', 'yuv420p', f'{t}/tl-anh_tinh.mp4'], check=True)
    subprocess.run(['rm', '-rf', tmp]); print('tl', k, tag, n, 'khung')


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'prep': prep(sys.argv[2])
    elif c == 'ghep': ghep(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == 'proj': proj(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 0)
    elif c == 'tl': tl(sys.argv[2], sys.argv[3])
