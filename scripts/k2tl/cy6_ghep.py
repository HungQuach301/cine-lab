#!/opt/cine/bin/python
"""V6 bước 7 · GHÉP bản TỐT NHẤT: albedo k2v (không chiếu sáng) × ÁNH SÁNG Cycles (Combined / DiffCol trên vật liệu xám → bức xạ tới, gồm nắng mềm, trời, GI, AO thật)
→ sương FogExp2 theo độ sâu Z (đúng công thức three: 1 − exp(−(ρ·z)²), màu sương của cảnh) → điểm ảnh không có hình học (nước, trời) lấy lượt k2v không khói
→ khói k2v (nhân alpha, che theo độ sâu) phủ lên → HDR tuyến tính (RGBA float32, hàng từ dưới lên) cho export6.js grade (cùng tone/grade/hạt của k2v).
  cy6_ghep.py <thư mục xuất> <cycles.exr> <ra.f32> [--irr-png <ảnh chẩn đoán>]"""
import sys, json, os
import numpy as np
import OpenEXR, Imath

D, EXR, OUT = sys.argv[1:4]
M = json.load(open(os.path.join(D, 'manifest.json'))); W, H = M['passes']['W'], M['passes']['H']
rd = lambda n: np.fromfile(os.path.join(D, n + '.f32'), np.float32).reshape(H, W, 4)[::-1]   # → hàng từ trên xuống
alb, nos, smk = rd('albedo'), rd('nosmoke'), rd('smoke')
f = OpenEXR.InputFile(EXR); hd = f.header(); dw = hd['dataWindow']; ew, eh = dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1; assert (ew, eh) == (W, H), (ew, eh)
chans = list(hd['channels'].keys()); FT = Imath.PixelType(Imath.PixelType.FLOAT)
def ch(name): k = [c for c in chans if c.endswith(name)]; assert k, (name, chans); return np.frombuffer(f.channel(k[0], FT), np.float32).reshape(H, W)
def rgb(layer): return np.stack([ch(f'{layer}.R'), ch(f'{layer}.G'), ch(f'{layer}.B')], -1)
comb = rgb('Combined'); alpha = ch('Combined.A')
f = OpenEXR.InputFile(EXR[:-4] + '-aux.exr'); chans = list(f.header()['channels'].keys())   # lượt phụ cy6.py: R = albedo GI, G = Z/1000 (nhân alpha)
xa = ch('Combined.A'); dcol = np.repeat(ch('Combined.R')[..., None], 3, -1); Z = ch('Combined.G') * 1000 / np.maximum(xa, 1e-3); Z[xa < 1e-3] = 1e6
irr = comb / np.maximum(dcol, 1e-4); irr[dcol.max(-1) < 1e-4] = 0
lit = alb[..., :3] * irr
fog = M.get('fog')
if fog:
    fz = 1 - np.exp(-(fog['density'] * np.minimum(Z, 1e6)) ** 2); lit = lit * (1 - fz[..., None]) + np.array(fog['color'], np.float32) * fz[..., None]
a = np.clip(alpha, 0, 1)[..., None]
out = lit * a + nos[..., :3] * (1 - a)
out = smk[..., :3] + out * (1 - np.clip(smk[..., 3:4], 0, 1))
o4 = np.concatenate([out, np.ones((H, W, 1), np.float32)], -1)[::-1].astype(np.float32)
o4.tofile(OUT)
st = {'hinh_hoc_pct': round(float((alpha > 0.5).mean() * 100), 2), 'irr_tb': [round(float(x), 4) for x in irr[alpha > 0.5].mean(0)] if (alpha > 0.5).any() else None,
      'khoi_pct': round(float((smk[..., 3] > 0.05).mean() * 100), 2)}
if '--irr-png' in sys.argv:
    from PIL import Image
    p = sys.argv[sys.argv.index('--irr-png') + 1]; im = np.clip((irr / (irr.max() * 0.5 + 1e-6)) ** (1 / 2.2), 0, 1); Image.fromarray((im * 255).astype(np.uint8)).save(p)
print(json.dumps(st))
