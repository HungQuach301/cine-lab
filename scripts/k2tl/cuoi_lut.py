#!/opt/cine/bin/python
"""BAN-CUOI-T3 (việc 5, §16, V2-D1) · LUT KÊNH (.cube 33³) áp cả phim ở bước ghép — một LUT cho cách A, Cycles GPU, minh hoạ Omni và mọi mốc năm.
Phép biến đổi (miền sRGB, giữ độ sáng Rec.709):
  · VIBRANCE bảo vệ màu đậm: chroma × (1 + v·(1 − s)^1,5), s = bão hoà HSV của điểm ảnh → màu nhạt (cỏ, đá, nước, trời) tăng, màu đã đậm (cờ đỏ/vàng, áo đỏ, mái ngói) gần như giữ:
    s = 0,8 → hệ số 1 + v·0,09; s = 0,4 → 1 + v·0,46.
  · không đổi độ sáng (luma giữ nguyên trừ phần kẹp [0, 1]); không đổi tông (hue) — chỉ kéo dãn quanh luma.
  cuoi_lut.py tao <v> <ra.cube>          → .cube + in SHA-256
  cuoi_lut.py do <thư mục khung> [<ra.json>] [--lut a.cube]   → bão hoà trung vị (640×360, cắt y 60–300 như anim_do.py), sai lệch màu cờ trước/sau trên bảng mẫu cờ"""
import hashlib, json, sys
from pathlib import Path
import numpy as np

def bien_doi(rgb, v):
    mx, mn = rgb.max(-1), rgb.min(-1); s = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
    y = (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2])[..., None]
    k = (1.0 + v * (1.0 - s) ** 1.5)[..., None]; return np.clip(y + (rgb - y) * k, 0.0, 1.0)

def tao(v, out, n=33):
    g = np.linspace(0, 1, n); B, G, R = np.meshgrid(g, g, g, indexing='ij'); rgb = np.stack([R, G, B], -1).reshape(-1, 3)   # .cube: R chạy nhanh nhất
    o = bien_doi(rgb, v); L = [f'TITLE "BAN-CUOI-T3 kenh T3 vibrance v={v}"', f'LUT_3D_SIZE {n}', 'DOMAIN_MIN 0.0 0.0 0.0', 'DOMAIN_MAX 1.0 1.0 1.0']
    L += [f'{a:.6f} {b:.6f} {c:.6f}' for a, b, c in o]; Path(out).write_text('\n'.join(L) + '\n'); return hashlib.sha256(Path(out).read_bytes()).hexdigest()

def ap(im_bgr, v):
    rgb = im_bgr[..., ::-1].astype(np.float64) / 255.0; return (bien_doi(rgb, v)[..., ::-1] * 255 + 0.5).astype(np.uint8)

MAU_CO = {'do_union': (200, 16, 46), 'xanh_union': (1, 33, 105), 'vang_borgona': (241, 191, 0), 'do_borgona': (173, 21, 25), 'trang': (240, 240, 240), 'ao_do': (176, 48, 42), 'mai_ngoi': (178, 92, 58)}

if __name__ == '__main__':
    a = sys.argv
    if a[1] == 'tao': print(tao(float(a[2]), a[3]))
    elif a[1] == 'do':
        import cv2
        v = float(a[a.index('--v') + 1]) if '--v' in a else 0.0; S = []
        for p in sorted(Path(a[2]).glob('*.jpg')) + sorted(Path(a[2]).glob('*.png')):
            im = cv2.resize(cv2.imread(str(p)), (640, 360), interpolation=cv2.INTER_AREA)[60:300]
            if v: im = ap(im, v)
            S.append(float(np.median(cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[..., 1]) / 255))
        co = {k: [int(x) for x in bien_doi(np.array(c, float)[None] / 255, v)[0] * 255 + 0.5] for k, c in MAU_CO.items()}
        r = dict(khung=len(S), bao_hoa_trung_vi=round(float(np.median(S)), 4), v=v, mau_co_sau=co, mau_co_truoc=MAU_CO); print(json.dumps(r, ensure_ascii=False))
        if len(a) > 3 and not a[3].startswith('--'): Path(a[3]).write_text(json.dumps(r, ensure_ascii=False, indent=1))
