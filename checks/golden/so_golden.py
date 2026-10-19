#!/opt/cine/bin/python
"""Khung vàng tham chiếu theo TRÌNH DỰNG V6 (phiên K-1.16, 19/10/2026; P10C-5). Ảnh tham chiếu mới khoá SHA trong checks/LOCK.

Lý do: tham chiếu cũ là khung master đã phát hành (LFS) dựng bằng trình dựng trước V6. V6 (Kinh thánh §12.5: mức dựng T3) đổi bóng đổ, SSAO,
chỉnh màu, và bộ công cụ hiện hành vẽ dòng nguồn 38 px (t1) → SSIM rơi về 0,945 / 0,931 / 0,908, t1 lệch cục bộ 22/144 ô dù không có lỗi hồi quy.
Từ 1.16 hồi quy đo so với khung do chính trình dựng V6 dựng (tham_chieu/<ca>.png = moi.png của lượt golden.py ghi trong GOLDEN-V6.json).

  so_golden.py <thư mục ra của scripts/common/golden.py run>      → so <ra>/<ca>/moi.png với tham_chieu/<ca>.png; in bảng; ghi <ra>/golden-v6.json

Số đo và ngưỡng: BẢN SAO ĐỘC LẬP của scripts/common/golden.py (pHash 64 bit DCT, SSIM xám σ 1,5, MAD, % điểm ảnh lệch > 24, ô lưới 16×9 > 3 %);
KHỚP khi Hamming ≤ 6, SSIM ≥ 0,90, không ô lệch. Mã thoát 0 khi mọi ca KHỚP.
"""
import hashlib, json, os, sys

import numpy as np
from PIL import Image
from scipy.fft import dctn
from scipy.ndimage import gaussian_filter

D = os.path.dirname(os.path.abspath(__file__))
PH_MAX, SSIM_MIN = 6, 0.90


def phash(im):
    a = np.asarray(im.convert('L').resize((32, 32), Image.LANCZOS), dtype=np.float64)
    d = dctn(a, norm='ortho')[:8, :8].flatten(); return d > np.median(d[1:])


def ssim(a, b):
    a = a.astype(np.float64); b = b.astype(np.float64); C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2; g = lambda x: gaussian_filter(x, 1.5)
    ma, mb = g(a), g(b); va, vb, cab = g(a * a) - ma * ma, g(b * b) - mb * mb, g(a * b) - ma * mb
    return float((((2 * ma * mb + C1) * (2 * cab + C2)) / ((ma * ma + mb * mb + C1) * (va + vb + C2))).mean())


def compare(new, ref):
    if new.size != ref.size: new = new.resize(ref.size, Image.LANCZOS)
    A, B = np.asarray(new.convert('RGB'), dtype=np.int16), np.asarray(ref.convert('RGB'), dtype=np.int16)
    Dm = np.abs(A - B).max(axis=2); ham = int((phash(new) != phash(ref)).sum()); s = ssim(np.asarray(new.convert('L')), np.asarray(ref.convert('L')))
    gh, gw = Dm.shape[0] // 9, Dm.shape[1] // 16
    cells = [(cx, cy) for cy in range(9) for cx in range(16) if (Dm[cy * gh:(cy + 1) * gh, cx * gw:(cx + 1) * gw] > 24).mean() > 0.03]
    ok = ham <= PH_MAX and s >= SSIM_MIN
    return dict(phash_hamming=ham, ssim=round(s, 4), mad=round(float(np.abs(A - B).mean()), 2), px_gt24_pct=round(100 * float((Dm > 24).mean()), 2),
                o_lech=len(cells), ket_qua='KHỚP' if ok and not cells else 'LỆCH CỤC BỘ' if ok else 'LỆCH')


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    out = sys.argv[1]; G = json.load(open(os.path.join(D, 'GOLDEN-V6.json'))); res = []
    for ca, c in G['ca'].items():
        ref = os.path.join(D, 'tham_chieu', f'{ca}.png'); moi = os.path.join(out, ca, 'moi.png')
        if sha(ref) != c['sha256_moi']: sys.exit(f'{ca}: tham chiếu không khớp SHA trong GOLDEN-V6.json')
        if not os.path.exists(moi): res.append(dict(ca=ca, ket_qua='THIẾU', loi=f'không có {moi}')); continue
        m = compare(Image.open(moi).convert('RGB'), Image.open(ref).convert('RGB')); res.append(dict(ca=ca, **m))
        print(f"{ca:6} {m['ket_qua']:12} pHash {m['phash_hamming']}/64 · SSIM {m['ssim']} · MAD {m['mad']} · >24: {m['px_gt24_pct']} % · ô lệch {m['o_lech']}/144")
    json.dump(dict(nguong=dict(phash_max=PH_MAX, ssim_min=SSIM_MIN), ca=res), open(os.path.join(out, 'golden-v6.json'), 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if all(r['ket_qua'] == 'KHỚP' for r in res) else 1)


if __name__ == '__main__':
    main()
