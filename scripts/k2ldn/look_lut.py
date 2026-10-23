#!/opt/cine/bin/python
"""LOOK-T4 · LUT xuất cho 3 biến thể look (áp ở bước xuất bằng ffmpeg lut3d, như T3).
  look_lut.py            → channel-k2/k2c-t4-02/look/mau/look-B-lanh.cube, look-C-am.cube (+ .sha256); A dùng nguyên LUT kênh T3 v0,30 (không chép).
  look_lut.py ap <vào> <ra> <A|B|C>   → áp LUT cho một ảnh (ffmpeg lut3d, nội suy tứ diện), JPG ≤ 2 MB nếu đuôi .jpg
B "London sương": giảm bão hoà ≈ 18 %, bóng tối ngả lạnh (lam xám), điểm trắng hơi lạnh, tương phản trung tính.
C "tranh khắc ấm": tương phản mềm (nâng điểm đen 0,035, cuộn vùng sáng), bảng màu ấm đất (ochre/umber) theo tông tranh sơn thế kỷ 17–18 — chỉ là đường cong màu, KHÔNG lọc nét/giả tranh."""
import hashlib, os, subprocess, sys
import numpy as np
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAU = os.path.join(REPO, 'channel-k2/k2c-t4-02/look/mau'); os.makedirs(MAU, exist_ok=True)
A_LUT = os.path.join(REPO, 'channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube')
def lum(c): return c @ np.array([0.2126, 0.7152, 0.0722])
def lutB(c):
    L = lum(c)[..., None]; c = L + (c - L) * 0.82
    sh = (1 - np.clip(L / 0.45, 0, 1)) ** 2; c = c + sh * np.array([-0.012, 0.000, 0.020])
    c = c * np.array([0.985, 1.0, 1.02]); return np.clip(c, 0, 1)
def lutC(c):
    L = lum(c)[..., None]
    t = 0.035 + (1 - 0.035 - 0.03) * (np.sin((np.clip(c, 0, 1) - 0.5) * np.pi * 0.86) / np.sin(0.5 * np.pi * 0.86) * 0.5 + 0.5)   # tương phản mềm, điểm đen nâng, sáng cuộn
    L2 = lum(t)[..., None]; warm = np.array([1.045, 0.995, 0.90]); t = L2 + (t - L2) * 0.92; t = t * warm
    mid = np.exp(-((L - 0.45) / 0.25) ** 2); t = t + mid * np.array([0.010, 0.004, -0.012]); return np.clip(t, 0, 1)
def write(fn, f, title, n=33):
    g = np.linspace(0, 1, n); out = [f'TITLE "{title}"', f'LUT_3D_SIZE {n}', 'DOMAIN_MIN 0.0 0.0 0.0', 'DOMAIN_MAX 1.0 1.0 1.0']
    for b in g:
        for gg in g:
            for r in g:
                o = f(np.array([r, gg, b])); out.append('%.6f %.6f %.6f' % tuple(o))
    open(fn, 'w').write('\n'.join(out) + '\n'); h = hashlib.sha256(open(fn, 'rb').read()).hexdigest(); open(fn + '.sha256', 'w').write(f'{h}  {os.path.basename(fn)}\n'); return h
def lut_path(v): return A_LUT if v == 'A' else os.path.join(MAU, {'B': 'look-B-lanh.cube', 'C': 'look-C-am.cube'}[v])
def ap(src, dst, v):
    vf = f"lut3d=file='{lut_path(v)}':interp=tetrahedral"
    q = 2
    while True:
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', src, '-vf', vf, '-q:v', str(q), dst], check=True)
        if not dst.endswith('.jpg') or os.path.getsize(dst) <= 2_000_000 or q >= 8: break
        q += 1
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ap': ap(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print('B', write(os.path.join(MAU, 'look-B-lanh.cube'), lutB, 'LOOK-T4 B London suong (lanh, -18% bao hoa)'))
        print('C', write(os.path.join(MAU, 'look-C-am.cube'), lutC, 'LOOK-T4 C tranh khac am (tuong phan mem, am dat)'))
