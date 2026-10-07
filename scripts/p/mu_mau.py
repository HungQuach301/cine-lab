#!/opt/cine/bin/python
"""Kiểm mù màu (CHUAN-KENH-LL §5.1) — mô phỏng protanopia, deuteranopia, tritanopia (Machado, Oliveira, Fernandes 2009, mức 1,0,
trên RGB tuyến tính) cho các khung lấy từ video, và đo khoảng cách màu giữa các cặp màu mã hoá nhóm.

1) Ảnh:  /opt/cine/bin/python scripts/p/mu_mau.py anh <video> <ra_thư_mục> <t1,t2,...>
   → mỗi mốc t một ảnh lưới 2×2 (gốc | prot | deut | trit), 960 px rộng mỗi ô.
2) Cặp màu: /opt/cine/bin/python scripts/p/mu_mau.py cap '<tên>=#hex' '<tên>=#hex' ... [--nguong 10]
   → ΔE76 (CIELAB) từng cặp ở mắt thường và 3 dạng mù màu; cặp < ngưỡng phải có mã hoá dư (gạch chéo/nét/nhãn) — in "CẦN MÃ HOÁ DƯ".
"""
import subprocess, sys, os
import numpy as np

M = {  # Machado 2009, severity 1.0
    'prot': np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]]),
    'deut': np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]),
    'trit': np.array([[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]),
}


def lin(c): c = c / 255.0; return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def srgb(l): l = np.clip(l, 0, 1); return np.where(l <= 0.0031308, l * 12.92, 1.055 * l ** (1 / 2.4) - 0.055) * 255.0


def sim(rgb, k):  # rgb: (..., 3) 0..255
    return srgb(lin(rgb.astype(np.float64)) @ M[k].T)


def lab(rgb):
    l = lin(np.asarray(rgb, np.float64))
    X = l @ np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]).T
    X = X / np.array([0.95047, 1.0, 1.08883])
    f = np.where(X > 216 / 24389, np.cbrt(X), (24389 / 27 * X + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def anh(video, out, ts):
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    for tt in ts.split(','):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', tt, '-i', video, '-frames:v', '1', '-vf', 'scale=960:540', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                             capture_output=True, check=True).stdout
        a = np.frombuffer(raw, np.uint8).reshape(540, 960, 3)
        g = Image.new('RGB', (1920, 1080))
        for i, (k, im) in enumerate([('goc', a)] + [(k, sim(a, k).astype(np.uint8)) for k in ('prot', 'deut', 'trit')]):
            g.paste(Image.fromarray(np.ascontiguousarray(im)), ((i % 2) * 960, (i // 2) * 540))
        p = os.path.join(out, f'mu-mau_t{float(tt):07.2f}.jpg'); g.save(p, quality=85); print(p)


def cap(args):
    th = 10.0
    if '--nguong' in args: i = args.index('--nguong'); th = float(args[i + 1]); args = args[:i] + args[i + 2:]
    C = []
    for s in args:
        n, h = s.split('='); h = h.lstrip('#'); C.append((n, np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float64)))
    print(f'{"cặp":44s} {"thường":>7s} {"prot":>7s} {"deut":>7s} {"trit":>7s}')
    bad = 0
    for i in range(len(C)):
        for j in range(i + 1, len(C)):
            (a, ca), (b, cb) = C[i], C[j]
            d = [np.linalg.norm(lab(ca) - lab(cb))] + [np.linalg.norm(lab(sim(ca, k)) - lab(sim(cb, k))) for k in ('prot', 'deut', 'trit')]
            flag = '  CẦN MÃ HOÁ DƯ' if min(d) < th else ''
            bad += bool(flag)
            print(f'{a + " / " + b:44s} ' + ' '.join(f'{x:7.1f}' for x in d) + flag)
    print(f'ngưỡng ΔE76 {th}; {bad} cặp cần mã hoá dư')


if __name__ == '__main__':
    if sys.argv[1] == 'anh': anh(*sys.argv[2:5])
    else: cap(sys.argv[2:])
