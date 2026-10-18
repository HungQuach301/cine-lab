"""PT3 · đo LẶP VÂN giữa các toà: mỗi khúc tường (mặt nạ ≥ 90 %, tức tường trơn) → xám 384×192 (chuẩn 6 m × 3 m giữa khúc), lọc cao tần (trừ Gauss σ 6 px),
tương quan chéo chuẩn hoá cực đại (mọi dịch, FFT) giữa MỌI cặp khúc khác toà. Cùng thước trên ảnh vào A (vân CC0 lát 2 m — cũng lặp).
  lap_van.py <ai_in/street> <ảnh AI> <ra.json>"""
import sys, os, json, itertools
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
DI, DA, OUT = sys.argv[1:4]; man = json.load(open(os.path.join(DI, 'chunks.json')))
def patch(p, c):
    im = np.asarray(Image.open(p).convert('L'), np.float32); H, W = im.shape; ppm = H / (man['strips'][str(c['bid'])]['H'] / 64.0)
    cx, cy = W // 2, int(H * 0.55); w, h = int(3 * ppm), int(1.5 * ppm); x = im[max(0, cy - h):cy + h, max(0, cx - w):cx + w]
    x = np.asarray(Image.fromarray(x).resize((384, 192), Image.LANCZOS), np.float32); x = x - gaussian_filter(x, 6); return (x - x.mean()) / (x.std() + 1e-6)
def motif(p):   # bố cục vết bẩn tầm lớn: cả khúc → 96×48, trừ trung bình, chuẩn hoá (không dịch)
    im = np.asarray(Image.open(p).convert('L').resize((96, 48), Image.LANCZOS), np.float32); im = gaussian_filter(im, 1.5); return (im - im.mean()) / (im.std() + 1e-6)
def ncc(a, b):
    F = np.fft.fft2(a) * np.conj(np.fft.fft2(b)); return float(np.real(np.fft.ifft2(F)).max() / a.size)
sel = [c for c in man['chunks'] if c['kind'] == 'elev' and c['mask_frac'] > 0.9 and os.path.exists(os.path.join(DA, c['name'] + '-thu2.jpg'))]
P = {c['name']: (c['bid'], patch(os.path.join(DA, c['name'] + '-thu2.jpg'), c), patch(os.path.join(DI, c['name'] + '.png'), c)) for c in sel}
MO = {c['name']: (motif(os.path.join(DA, c['name'] + '-thu2.jpg')), motif(os.path.join(DI, c['name'] + '.png'))) for c in sel}
ai, A, mo, moA = [], [], [], []
for (n1, (b1, a1, i1)), (n2, (b2, a2, i2)) in itertools.combinations(P.items(), 2):
    if b1 == b2: continue
    ai.append((ncc(a1, a2), n1, n2)); A.append(ncc(i1, i2)); mo.append((float((MO[n1][0] * MO[n2][0]).mean()), n1, n2)); moA.append(float((MO[n1][1] * MO[n2][1]).mean()))
ai.sort(reverse=True); r = {'so_khuc': len(P), 'so_cap_khac_toa': len(ai), 'AI_tb': round(float(np.mean([x[0] for x in ai])), 3), 'AI_p90': round(float(np.percentile([x[0] for x in ai], 90)), 3),
     'AI_cap_cao_nhat': [(round(v, 3), a, b) for v, a, b in ai[:5]], 'A_tb': round(float(np.mean(A)), 3), 'A_p90': round(float(np.percentile(A, 90)), 3),
     'AI_cap_tren_0_5_pct': round(100 * float(np.mean([x[0] > 0.5 for x in ai])), 1), 'A_cap_tren_0_5_pct': round(100 * float(np.mean([v > 0.5 for v in A])), 1),
     'bo_cuc_AI_tb': round(float(np.mean([x[0] for x in mo])), 3), 'bo_cuc_AI_p90': round(float(np.percentile([x[0] for x in mo], 90)), 3), 'bo_cuc_A_tb': round(float(np.mean(moA)), 3), 'bo_cuc_A_p90': round(float(np.percentile(moA, 90)), 3),
     'bo_cuc_AI_cap_cao': [(round(v, 3), a, b) for v, a, b in sorted(mo, reverse=True)[:5]]}
json.dump(r, open(OUT, 'w'), indent=1, ensure_ascii=False); print(r)
