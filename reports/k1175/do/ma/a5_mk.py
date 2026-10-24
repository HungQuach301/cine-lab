"""A5 — sinh cấu hình biến thể đáp án BE-MAT-NHA từ render gốc (iid.png + nha.json): chọn nhà ĐO ĐƯỢC (thấy ≥ 300 px, px/m ≥ 1,5), cách nhau,
mỗi biến thể HỎNG đổi đồng thời bề mặt (mat_seed khác + bảng màu khác) để thước phải dựa vào hình học, không vào màu."""
import json, sys, cv2, numpy as np
d = sys.argv[1]; nua = sys.argv[2]; J = json.load(open(f'{d}/nha.json')); cfg0 = J['cfg']
iid = cv2.imread(f'{d}/iid.png'); cls = cv2.imread(f'{d}/cls.png')
I = (iid[..., 2].astype(np.int64) << 16) | (iid[..., 1].astype(np.int64) << 8) | iid[..., 0]
I[~np.all(cls[..., ::-1] == (215, 215, 215), -1)] = 0
ids, cnt = np.unique(I, return_counts=True); vis = dict(zip(ids.tolist(), cnt.tolist()))
H = {h['id']: h for h in J['nha']}
ok = [h for h in J['nha'] if vis.get(h['id'], 0) >= 150 and h['px_m'] >= 1.0 and h['lo'] > 0]
rng = np.random.default_rng(int(cfg0['seed']) * 31 + 7)
rng.shuffle(ok)
chosen, used_lo = [], set()
for h in ok:
    if any(np.hypot(h['tam_px'][0] - c['tam_px'][0], h['tam_px'][1] - c['tam_px'][1]) < 50 for c in chosen): continue
    chosen.append(h)
print(len(ok), 'đo được;', len(chosen), 'chọn được (cách ≥ 50 px)', file=sys.stderr)
it = iter(chosen); nxt = lambda: next(it)
# láng giềng cùng lô liền kề (để gộp): nhà cùng lô có x0 khớp x1
def lang_gieng(h):
    c = [g for g in J['nha'] if g['lo'] == h['lo'] and g['id'] != h['id'] and abs(g['tam'][1] - h['tam'][1]) < 2 and abs(abs(g['tam'][0] - h['tam'][0]) - 0.5 * (g['rong'] + h['rong'])) < 0.3]
    return c[0] if c else None
V = {}
mk = lambda: dict(seed=cfg0['seed'], may=cfg0['may'], spp=cfg0.get('spp', 32), mat_seed=int(cfg0['seed']) + 50, bang_mau='khac', chi='rgb', bien_doi=[])
# biến thể ĐẠT (chỉ đổi bề mặt)
V[f'{nua}-bm1'] = dict(mk()); V[f'{nua}-bm2'] = dict(mk(), mat_seed=int(cfg0['seed']) + 77, bang_mau=None)
# dời: 1, 2, 3, 5 m theo x và theo y
for k, (dm, ax) in enumerate([(1, 'x'), (2, 'x'), (2, 'y'), (3, 'x'), (3, 'y'), (5, 'x'), (5, 'y'), (1, 'y')]):
    c = mk(); c['bien_doi'] = [dict(loai='doi', id=nxt()['id'], **({'dx': dm * (1 if j % 2 else -1)} if ax == 'x' else {'dy': dm * (1 if j % 2 else -1)}), m=dm) for j in range(8)]
    V[f'{nua}-doi{dm}{ax}'] = c
c = mk(); c['bien_doi'] = [dict(loai='mai', id=nxt()['id'], kieu='hong') for _ in range(8)]; V[f'{nua}-mai-hong'] = c
c = mk(); c['bien_doi'] = [dict(loai='mai', id=nxt()['id'], kieu='bang') for _ in range(8)]; V[f'{nua}-mai-bang'] = c
c = mk(); bd = []
for _ in range(8):
    h = nxt(); bd.append(dict(loai='mai', id=h['id'], kieu='hoi_ngang' if h['kieu_mai'] != 'hoi_ngang' else 'hoi_doc'))
c['bien_doi'] = bd; V[f'{nua}-mai-xoay'] = c
c = mk(); c['bien_doi'] = [dict(loai='tang', id=nxt()['id'], dh=3.0) for _ in range(8)]; V[f'{nua}-tang'] = c
c = mk(); c['bien_doi'] = [dict(loai='xoa', id=nxt()['id']) for _ in range(8)]; V[f'{nua}-xoa'] = c
c = mk(); bd = []
while len(bd) < 8:
    h = nxt(); g = lang_gieng(h)
    if g: bd.append(dict(loai='gop', ids=[h['id'], g['id']]))
c['bien_doi'] = bd; V[f'{nua}-gop'] = c
c = mk(); bd = []
for _ in range(8):   # thêm nhà CHÈN vào phía sau nhà đo được (lộ phần mái trên mặt nạ nhà trước) — thêm trong vùng nhà
    h = nxt(); x0 = h['tam'][0] - 3; y0 = h['tam'][1] + 0.5 * h['sau'] + 0.5
    bd.append(dict(loai='them', x0=x0, y0=y0, w=6.5, d=8, h=h['cao'] + 4, gan=h['id']))
c['bien_doi'] = bd; V[f'{nua}-them'] = c
for k, v in V.items(): json.dump(v, open(f'{k}.json', 'w'))
json.dump(dict(chon=[h['id'] for h in chosen], vis={str(k): v for k, v in vis.items()}), open(f'{nua}-chon.json', 'w'))
print(len(V), 'cấu hình', file=sys.stderr)
