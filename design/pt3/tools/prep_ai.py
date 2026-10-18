"""PT3 · HC7 bước 1 — ghép DẢI mặt tường mỗi toà (các nhóm 'elev' theo thứ tự cạnh: góc nhà liền nhau trong dải) + bản ghép 'top',
rồi chia thành KHÚC cho lệnh sửa ảnh (tỉ lệ ≤ 3:1, cạnh ≤ 2560 px, bội 16, chồng 2 m). Mỗi khúc: ảnh vào (albedo A, sRGB, lỗ cửa = đen)
+ mặt nạ PNG (alpha 0 = được sửa = CHỈ điểm ảnh thuộc mặt tường/mái/sàn của nhóm; còn lại giữ).
  /opt/cine/bin/python -I prep_ai.py <site> <thư mục elev> <thư mục top> <groups.json> <ra thư mục>"""
import sys, os, json, math
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import exr
site, DE, DT, GJ, OUT = sys.argv[1:6]; os.makedirs(OUT, exist_ok=True)
req = json.load(open(GJ)); meta = json.load(open(os.path.join(DE, 'meta.json'))); G = meta['groups']
CFG = {'street': {'H_api': 1024, 'W_max': 2560, 'ov_m': 2.0, 'tile_m': 64.0, 'tile_ov_m': 12.0},
       'kb': {'H_api': 768, 'W_max': 2304, 'ov_m': 2.0, 'tile_m': 70.0, 'tile_ov_m': 10.0}}[site]
OPEN = 0.012   # màu lỗ cửa/nền trong ảnh vào (tuyến tính ≈ sRGB 28)

def r16(x): return max(16, int(round(x / 16.0)) * 16)

def strip(bid, gl):
    gl = sorted(gl, key=lambda g: G[g]['order']); ppm = req['ppm']
    zmin = min(G[g]['z0'] for g in gl); zmax = max(G[g]['z1'] for g in gl); Hs = int(round((zmax - zmin) * ppm))
    ims = []; x = 0; groups = {}; joins = []
    for k, g in enumerate(gl):
        a = exr.read(os.path.join(DE, f'elev_b{bid}_g{g}_alb.exr')); m = exr.read(os.path.join(DE, f'elev_b{bid}_g{g}_mask.exr'), 'R')[..., 0]
        h, w = a.shape[:2]; top = int(round((zmax - G[g]['z1']) * ppm)); top = max(0, min(top, Hs - h))
        A = np.zeros((Hs, w, 4), np.float32); M = np.zeros((Hs, w), np.float32); A[top:top + h] = a; M[top:top + h] = m
        ims.append((A, M)); groups[str(g)] = {'x0': x, 'w': w, 'order': G[g]['order'], 'L': G[g]['L']}
        if k: joins.append({'x': x, 'g_a': gl[k - 1], 'g_b': g, 'lien_ke': G[g]['order'] == G[gl[k - 1]]['order'] + 1})
        x += w
    A = np.concatenate([i[0] for i in ims], 1); M = np.concatenate([i[1] for i in ims], 1)
    return A, M, {'bid': int(bid), 'W': int(A.shape[1]), 'H': int(Hs), 'ppm': ppm, 'zmin': zmin, 'zmax': zmax, 'groups': groups, 'joins': joins}

def to_api(A, M, Wa, Ha, name, kind):
    rgb = A[..., :3].copy(); al = A[..., 3]
    rgb[al < 0.5] = OPEN
    im = Image.fromarray((exr.lin2srgb(rgb) * 255 + 0.5).astype(np.uint8)).resize((Wa, Ha), Image.LANCZOS)
    mk = (M > 0.5).astype(np.uint8); mk = np.array(Image.fromarray(mk * 255).resize((Wa, Ha), Image.NEAREST)) > 127
    mask = np.zeros((Ha, Wa, 4), np.uint8); mask[..., :3] = 255; mask[..., 3] = np.where(mk, 0, 255)   # alpha 0 = vùng được sửa
    im.save(os.path.join(OUT, name + '.png')); Image.fromarray(mask, 'RGBA').save(os.path.join(OUT, name + '_mask.png'))
    return {'name': name, 'kind': kind, 'W_api': Wa, 'H_api': Ha, 'mask_frac': round(float(mk.mean()), 4)}

chunks = []; strips = {}
for bid, gl in req['elev'].items():
    A, M, info = strip(bid, gl); np.savez_compressed(os.path.join(OUT, f'strip_b{bid}.npz'), A=A.astype(np.float16), M=M.astype(np.float16)); strips[bid] = info
    Hs, Ws = A.shape[:2]; Ha = CFG['H_api']; sc = Ha / Hs; Wmax_px = int(CFG['W_max'] / sc); ov = int(CFG['ov_m'] * info['ppm'])
    n = 1 if Ws <= Wmax_px else math.ceil((Ws - ov) / (Wmax_px - ov)); step = (Ws - ov) / n if n > 1 else Ws
    for k in range(n):
        x0 = int(round(k * step)) if n > 1 else 0; x1 = min(Ws, int(round(x0 + step + ov))) if n > 1 else Ws
        Wa = r16((x1 - x0) * sc); Wa = max(Wa, r16(655360 / Ha + 8)) if Wa * Ha < 655360 else Wa
        if Wa > Ha * 3: Wa = r16(Ha * 3 - 8)
        c = to_api(A[:, x0:x1], M[:, x0:x1], Wa, Ha, f'{site}_b{bid}_c{k}', 'elev'); c.update(bid=int(bid), x0=x0, x1=x1, H=Hs)
        if c['mask_frac'] < 0.02: c['bo_qua'] = 'mặt nạ < 2 % — không gọi'
        chunks.append(c)
# bản ghép 'top'
T = req['top']; x0m, y0m, x1m, y1m = T['rect']; ppm = T['ppm']
At = exr.read(os.path.join(DT, 'top_alb.exr')); Mt = exr.read(os.path.join(DT, 'top_mask.exr'), 'R')[..., 0]
np.savez_compressed(os.path.join(OUT, 'top.npz'), A=At.astype(np.float16), M=Mt.astype(np.float16))
Ht, Wt = At.shape[:2]; tm = int(CFG['tile_m'] * ppm); to = int(CFG['tile_ov_m'] * ppm)
def spans(N):
    if N <= tm: return [(0, N)]
    n = math.ceil((N - to) / (tm - to)); st = (N - tm) / (n - 1); return [(int(round(i * st)), int(round(i * st)) + tm) for i in range(n)]
for (ya, yb) in spans(Ht):
    for (xa, xb) in spans(Wt):
        Wa, Ha = r16(xb - xa), r16(yb - ya)
        if Wa * Ha < 655360: s_ = math.sqrt(655360 / (Wa * Ha)) * 1.02; Wa, Ha = r16(Wa * s_), r16(Ha * s_)
        c = to_api(At[ya:yb, xa:xb], Mt[ya:yb, xa:xb], Wa, Ha, f'{site}_top_y{ya}_x{xa}', 'top'); c.update(x0=xa, x1=xb, y0=ya, y1=yb)
        if c['mask_frac'] < 0.02: c['bo_qua'] = 'mặt nạ < 2 % — không gọi'
        chunks.append(c)
man = {'site': site, 'strips': strips, 'top': {'rect': T['rect'], 'ppm': ppm, 'W': Wt, 'H': Ht}, 'chunks': chunks}
json.dump(man, open(os.path.join(OUT, 'chunks.json'), 'w'), indent=1, ensure_ascii=False)
print(site, 'dải', len(strips), 'khúc elev', sum(1 for c in chunks if c['kind'] == 'elev' and 'bo_qua' not in c), 'khúc top', sum(1 for c in chunks if c['kind'] == 'top' and 'bo_qua' not in c),
      'bỏ qua', sum(1 for c in chunks if 'bo_qua' in c))
