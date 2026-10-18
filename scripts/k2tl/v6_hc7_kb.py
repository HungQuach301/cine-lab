#!/opt/cine/bin/python
"""V6 · bước 4 (Q-PT3-1, Q-PT3-5) — nạp vân HC7 King's Bastion của PT3 vào máy dựng three.js/llvmpipe (design/k2v/tl/fort.js).
Đầu vào CHỈ là dữ liệu PT3 đã kiểm dữ kiện (không gọi API): sổ khúc reports/pt3/do/khuc-kb.json (dải 8000: 16 719 × 696 px, 80 px/m, z −5,5 … +3,2 m),
sổ nướng reports/pt3/do/nuong-kb.json (lần thử dùng + nắn khung), ảnh AI reports/pt3/ai/kb_b8000_c*.jpg (9 khúc tường, 0 lỗi chắc — reports/pt3/ai/kiem-du-kien.json).
Cách nướng (như bake_hc7.py PT3, rút gọn cho hình học khác): mỗi khúc đổi cỡ về (x1−x0) × 696 → nắn khung đúng hộp PT3 đã ghi → ghép dải, hoà tuyến tính trên đoạn chồng 160 px
→ CHỈ GIỮ CHI TIẾT < ~1 m: D = I / G_σ(I), σ = 1 m (80 px) — màu/độ sáng tầm lớn do vật liệu đá của máy dựng quyết (tương đương "neo màu σ 1 m về A" của PT3);
mã hoá D·0,5 (D trong 0,25–1,95) → JPEG 40 px/m (8 360 × 348). Sàn pháo (4 ô 'top') KHÔNG dùng: hệ toạ độ ô sàn PT3 không ghi phép nắn sang hình học k2v (ghi báo cáo).
  v6_hc7_kb.py <ra.jpg> <ra.json>"""
import json, os, sys, hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT, OJ = sys.argv[1:3]
K = json.load(open(f'{REPO}/reports/pt3/do/khuc-kb.json')); N = {x['khuc']: x for x in json.load(open(f'{REPO}/reports/pt3/do/nuong-kb.json'))['khuc']}
S = K['strips']['8000']; W, H, ppm = S['W'], S['H'], S['ppm']
s2l = lambda a: np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4); l2s = lambda a: np.where(a <= 0.0031308, a * 12.92, 1.055 * np.power(np.maximum(a, 0), 1 / 2.4) - 0.055)
acc = np.zeros((H, W, 3), np.float32); wsum = np.zeros((H, W), np.float32); used = []
for c in [c for c in K['chunks'] if c['kind'] == 'elev']:
    n = N[c['name']]; assert n['ket_qua'] == 'dùng', c['name']
    t = n['dung']; p = f"{REPO}/reports/pt3/ai/{c['name']}{'' if t == '-thu1' else t}.jpg"
    x0, x1 = c['x0'], min(c['x1'], W); w = x1 - x0
    img = s2l(np.asarray(Image.open(p).convert('RGB').resize((c['x1'] - c['x0'], H), Image.LANCZOS), np.float32) / 255)[:, :w]
    nk = next((l.get('nan_khung') for l in n['lan'] if l['lan'] == t and l.get('nan_khung')), None)
    if nk and 0.85 <= nk['ti_le_doc'] <= 1.2:   # nắn khung như PT3: hộp ra → hộp vào
        ro, ri, co, ci = nk['hang_ra'], nk['hang_vao'], nk['cot_ra'], nk['cot_vao']; crop = img[ro[0]:ro[1] + 1, co[0]:min(co[1] + 1, w)]
        rs = s2l(np.asarray(Image.fromarray((l2s(crop) * 255 + 0.5).clip(0, 255).astype(np.uint8)).resize((min(ci[1] + 1, w) - ci[0], ri[1] - ri[0] + 1), Image.LANCZOS), np.float32) / 255)
        img = img.copy(); img[ri[0]:ri[1] + 1, ci[0]:ci[0] + rs.shape[1]] = rs
    # trọng số hoà: tam giác trên đoạn chồng
    wx = np.ones(w, np.float32); ov = 160
    if x0 > 0: wx[:ov] = np.linspace(0, 1, ov)
    if x1 < W: wx[-ov:] = np.minimum(wx[-ov:], np.linspace(1, 0, ov))
    acc[:, x0:x1] += img * wx[None, :, None]; wsum[:, x0:x1] += wx[None, :]
    used.append({'khuc': c['name'], 'lan': t, 'tep': os.path.basename(p), 'x0': x0, 'x1': x1, 'nan_khung': nk, 'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest()})
I = acc / np.maximum(wsum, 1e-6)[..., None]; cov = float((wsum > 0).mean())
ok = (I.mean(-1) > 0.008).astype(np.float32)   # vùng ngoài mặt nạ PT3 (AI để đen / giữ A) → không chi tiết AI (D = 1)
den = gaussian_filter(ok, ppm) + 1e-6; G = np.stack([gaussian_filter(I[..., k] * ok, ppm) / den for k in range(3)], -1)
D = np.where(ok[..., None] > 0.5, np.clip(I / np.maximum(G, 1e-4), 0.25, 1.95), 1.0); st_ok = float(ok.mean())
small = Image.fromarray((np.clip(D * 0.5, 0, 1) * 255 + 0.5).astype(np.uint8)).resize((W // 2, H // 2), Image.LANCZOS)
small.save(OUT, quality=90)
st = {'nguon': 'PT3 HC7 King\'s Bastion (reports/pt3) — 9 khúc tường, 0 lỗi chắc (kiem-du-kien.json)', 'dai_px': [W, H], 'ppm_goc': ppm, 'ppm_ra': ppm / 2, 'z_m': [S['zmin'], S['zmax']],
      'chu_vi_m': round(W / ppm, 2), 'phu': round(cov, 4), 'vung_co_AI': round(st_ok, 4), 'D_tb': [round(float(x), 4) for x in D.reshape(-1, 3).mean(0)], 'D_p05_p95': [round(float(np.percentile(D, 5)), 3), round(float(np.percentile(D, 95)), 3)],
      'khuc': used, 'ra': os.path.basename(OUT), 'ra_sha256': hashlib.sha256(open(OUT, 'rb').read()).hexdigest(), 'san_phao': 'không dùng (không có phép nắn toạ độ ô sàn PT3 → k2v)'}
json.dump(st, open(OJ, 'w'), ensure_ascii=False, indent=1); print(json.dumps({k: v for k, v in st.items() if k != 'khuc'}, ensure_ascii=False))
