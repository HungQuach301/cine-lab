#!/opt/cine/bin/python
"""V7B (19/10/2026, việc 4 — NHÀ 2026 CÓ VẬT LIỆU) · gắn MÀU + KIỂU cho từng toà hiện đại của gói cảnh gib → pack/buildings-v7b.json (bản ghi gốc + phần tử 8 {w, r, s, nguon}).
Thứ tự ưu tiên nguồn (ghi vào phần tử 8 'nguon' của từng toà, thống kê ở reports/v7b/do/mau-nha.json):
  1. OSM building:colour / roof:colour (thẻ thật của toà — chỉ ≈ 65 toà có; đọc thẳng từ tệp .osm thô, khớp tâm ≤ 15 m)
  2. MÁI: màu Sentinel-2 L2A TCI 15/4/2026 (S2C_30STF_20260415_0, Copernicus, 10 m) — trung vị điểm ảnh trong dấu chân (co 5 m; toà nhỏ: điểm tâm). Ngói (ấm, đỏ hơn lam ≥ 25 %)
     → màu ngói theo điểm ảnh; mái bằng → xám/trắng theo độ sáng điểm ảnh. TCI ≈ phản xạ × 2,5 (sRGB) → chia lại và kẹp về dải vật liệu.
  3. TƯỜNG: kiểu dùng (Catastro 'u' cho La Línea; OSM building=* cho Gibraltar) + số tầng → bảng màu rút từ ảnh CC của Gibraltar (data/mau-nha-v7b.json, k-means trên vùng mặt tiền
     sáng của 4 ảnh Wikimedia Commons 2008–2011 — ảnh 2020s không tải được: Commons trả 429 cho proxy, BAI-HOC #82) — chọn tất định theo băm toà. Bậc 4 (bảng màu vùng, không phải màu toà).
Không đổi hình học, chiều cao, năm. Toà ghost / thời kỳ cũ giữ nguyên (không phần tử 8).
Dùng: /opt/cine/bin/python -I scripts/k2tl/v7b_mau_nha.py [--out-stat reports/v7b/do/mau-nha.json]"""
import json, os, sys, re, hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent)); import geo  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]; CACHE = Path(os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache')); SRC = CACHE / 'scene/gib'; PK = SRC / 'pack'
OUT_STAT = Path(sys.argv[sys.argv.index('--out-stat') + 1]) if '--out-stat' in sys.argv else ROOT / 'reports/v7b/do/mau-nha.json'
PAL = json.loads((ROOT / 'design/k2v/tl/data/mau-nha-v7b.json').read_text())
M = json.loads((SRC / 'meta_rasters.json').read_text()); e0, n0, e1, n1 = M['ext']; ST = M['dsm']['step']; OU = M['origin_utm30']
tci = np.load(SRC / 'r_s2tci.npy').astype(np.float32) / 255.0; H_, W_ = tci.shape[:2]
B = json.loads((PK / 'buildings.json').read_text())
cen = lambda r: (sum(p[0] for p in r) / len(r), sum(p[1] for p in r) / len(r))
hsh = lambda s: int(hashlib.md5(s.encode()).hexdigest()[:8], 16)

# ---- 1. thẻ màu OSM thô
nodes, tagged = {}, []
for f in sorted((CACHE / 'osm/gib').glob('*.osm')):
    txt = f.read_text(errors='ignore')
    for m in re.finditer(r'<node id="(\d+)"[^>]*?lat="([-\d.]+)" lon="([-\d.]+)"', txt): nodes[m.group(1)] = (float(m.group(3)), float(m.group(2)))
    for m in re.finditer(r'<way id="\d+".*?</way>', txt, re.S):
        w = m.group(0); tg = dict(re.findall(r'<tag k="([^"]+)" v="([^"]*)"', w))
        if 'building' in tg and ('building:colour' in tg or 'roof:colour' in tg): tagged.append((re.findall(r'<nd ref="(\d+)"', w), tg))
NAMED = {'white': '#f2f0ea', 'grey': '#9a9a96', 'gray': '#9a9a96', 'red': '#9a3a2a', 'brown': '#6b4a32', 'beige': '#e3d6b4', 'yellow': '#e3c46a', 'cream': '#efe6cf', 'black': '#2a2a2a', 'orange': '#d08a4a', 'pink': '#e0a8a0', 'blue': '#4a6a9a'}
def col(v):
    v = NAMED.get(v.strip().lower(), v.strip());
    if not re.fullmatch(r'#?[0-9a-fA-F]{6}', v): return None
    v = v.lstrip('#'); return [round(int(v[i:i + 2], 16) / 255, 3) for i in (0, 2, 4)]
osm_pts = []
for refs, tg in tagged:
    ll = [nodes[r] for r in refs if r in nodes]
    if len(ll) < 3: continue
    E, N = geo.utm(np.array([p[0] for p in ll]), np.array([p[1] for p in ll])); osm_pts.append((float(np.mean(E) - OU[0]), float(np.mean(N) - OU[1]), col(tg.get('building:colour', '')) if tg.get('building:colour') else None, col(tg.get('roof:colour', '')) if tg.get('roof:colour') else None))
OP = np.array([[p[0], p[1]] for p in osm_pts]) if osm_pts else np.zeros((0, 2))

# ---- kiểu dùng: Catastro (La Línea) + OSM building=* (Gibraltar), khớp theo tâm
C = json.loads((SRC / 'v_catastro.json').read_text()); V = json.loads((SRC / 'v_osm.json').read_text())
from scipy.spatial import cKDTree
def ctr_list(L, key):
    P, U = [], []
    for x in L:
        p = x['p']; P.append(cen(p[:-1] if p[0] == p[-1] else p)); U.append(key(x))
    return cKDTree(np.array(P)), U
kC, uC = ctr_list([c for c in C if isinstance(c.get('p'), list)], lambda c: c.get('u', ''))
kO, uO = ctr_list(V['building'], lambda b: b['t'].get('building', 'yes'))

def s2(ring):
    r = np.array(ring); c0 = np.clip(((r[:, 0] - e0) / ST).astype(int), 0, W_ - 1); r0 = np.clip(((n1 - r[:, 1]) / ST).astype(int), 0, H_ - 1)
    cmin, cmax, rmin, rmax = c0.min(), c0.max(), r0.min(), r0.max(); px = []
    for rr in range(rmin, rmax + 1):
        for cc in range(cmin, cmax + 1):
            e, n = e0 + (cc + 0.5) * ST, n1 - (rr + 0.5) * ST
            ins = False; j = len(ring) - 1
            for i in range(len(ring)):
                if (ring[i][1] > n) != (ring[j][1] > n) and e < (ring[j][0] - ring[i][0]) * (n - ring[i][1]) / (ring[j][1] - ring[i][1]) + ring[i][0]: ins = not ins
                j = i
            if ins: px.append(tci[rr, cc])
    if not px:
        e, n = cen(ring); px = [tci[int(np.clip((n1 - n) / ST, 0, H_ - 1)), int(np.clip((e - e0) / ST, 0, W_ - 1))]]
    return np.median(np.array(px), 0), len(px)

def roof_of(rgb):
    lin = np.clip(rgb, 0, 1) ** 2.2 / 2.5; lin = np.clip(lin, 0, 1); s = lin ** (1 / 2.2)   # TCI ≈ 2,5 × phản xạ → về phản xạ (sRGB)
    r, g, b = s; warm = r > b * 1.40 and r > g * 1.12   # ngói đỏ rõ (ngưỡng chỉnh để nền cát ấm 10 m không bị đếm là ngói)
    if warm:   # ngói: giữ sắc của điểm ảnh, kéo độ sáng về dải ngói nung (0,45–0,75)
        k = np.clip(0.62 / max(r, 1e-3), 0.8, 1.9); t = np.clip(s * k, 0, 1); return [round(float(v), 3) for v in t], 'ngoi'
    L = float(0.299 * r + 0.587 * g + 0.114 * b); L = float(np.clip(0.48 + (L - 0.25) * 1.4, 0.50, 0.92)); tint = (s - s.mean()) * 0.5
    return [round(float(np.clip(L + tint[i], 0, 1)), 3) for i in range(3)], 'bang'

st = dict(tong=0, osm_tuong=0, osm_mai=0, s2_mai=0, s2_ngoi=0, s2_bang=0, tuong_bang_mau={}, s2_px_tb=0.0)
out = []
for i, b in enumerate(B):
    y, gy, h, base, rf, reg, ring = b[:7]
    if gy or y < 1900 or len(ring) < 3: out.append(b); continue
    c = cen(ring); key = f'{reg}:{c[0]:.1f}:{c[1]:.1f}'; R = hsh(key); st['tong'] += 1
    rgb, npx = s2(ring); roof, rk = roof_of(rgb); st['s2_mai'] += 1; st['s2_' + rk] += 1; st['s2_px_tb'] += npx
    if reg == 0: u = uC[kC.query(c)[1]] if kC.query(c)[0] < 20 else ''
    else: u = uO[kO.query(c)[1]] if kO.query(c)[0] < 20 else 'yes'
    if reg == 1: grp = 'gib_thap' if h >= 24 else 'gib_cong_nghiep' if u in ('industrial', 'garages', 'garage', 'warehouse', 'hangar', 'service') else 'gib_moi' if (u in ('commercial', 'office', 'hotel', 'retail', 'hospital', 'university') or y >= 1995) and h >= 12 else 'gib_o'
    else: grp = 'll_cong_nghiep' if ('industrial' in u or 'agric' in u) else 'll_thap' if h >= 18 else 'll_o'
    P = PAL['tuong'][grp]; wall = P[R % len(P)]['rgb']; sty = PAL['kieu'][grp]; ng = {'mai': 'S2 2026 TCI (' + rk + ')', 'tuong': f'bảng màu ảnh CC — nhóm {grp}', 'dung': u or '?'}
    st['tuong_bang_mau'][grp] = st['tuong_bang_mau'].get(grp, 0) + 1
    if len(OP):
        d = np.hypot(OP[:, 0] - c[0], OP[:, 1] - c[1]); j = int(np.argmin(d))
        if d[j] < 15:
            if osm_pts[j][2]: wall = osm_pts[j][2]; ng['tuong'] = 'OSM building:colour'; st['osm_tuong'] += 1
            if osm_pts[j][3]: roof = osm_pts[j][3]; ng['mai'] = 'OSM roof:colour'; st['osm_mai'] += 1
    nb = list(b) + [None] * (8 - len(b)); nb = nb[:8] + [dict(w=wall, r=roof, s=sty, ngoi=rk == 'ngoi', nguon=ng)]; out.append(nb)
st['s2_px_tb'] = round(st['s2_px_tb'] / max(1, st['s2_mai']), 2); st['osm_the_mau'] = len(osm_pts)
(PK / 'buildings-v7b.json').write_text(json.dumps(out, separators=(',', ':')))
OUT_STAT.parent.mkdir(parents=True, exist_ok=True); OUT_STAT.write_text(json.dumps(st, ensure_ascii=False, indent=1) + '\n'); print(json.dumps(st, ensure_ascii=False))
