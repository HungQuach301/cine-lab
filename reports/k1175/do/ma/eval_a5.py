"""A5 (a) trên đáp án Blender: ảnh ghép = render gốc ngoài vùng nhà thường (nở 1 px), ảnh biến thể (bề mặt đổi ± hình khối đổi) trong vùng nhà.
Ra đặc trưng từng nhà (sup0, sup, dich_m, px_m, px) + nhãn đáp án → chọn ngưỡng ở nửa A, kiểm ở nửa B."""
import sys, os, json, glob, cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bmn
S = os.path.dirname(os.path.abspath(__file__)); D = S + '/a5'


def ma(png):
    c = cv2.imread(png); return (c[..., 2].astype(np.int64) << 16) | (c[..., 1].astype(np.int64) << 8) | c[..., 0]


def ghep(R, A, I):
    m = cv2.dilate((I > 0).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0; C = R.copy(); C[m] = A[m]; return C


def bien_doi(cfg, H):
    pos = {}
    for b in cfg.get('bien_doi', []):
        t = b['loai']
        if t == 'doi': pos[b['id']] = f"doi{abs(b.get('dx', 0) or b.get('dy', 0)):g}"
        elif t in ('xoa', 'mai', 'tang'): pos[b['id']] = t + ('-' + b['kieu'] if t == 'mai' else '')
        elif t == 'gop': pos[b['ids'][0]] = 'gop'; pos[b['ids'][1]] = 'gop'
        elif t == 'them': pos[b['gan']] = 'them'
    return pos


P = json.loads(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].startswith('{') else {}
rows = []
for nua in 'AB':
    gd = f'{D}/{nua}-goc'
    if not os.path.exists(gd + '/rgb.png'): continue
    R = cv2.imread(gd + '/rgb.png'); cls = cv2.imread(gd + '/cls.png')[..., ::-1]
    I = ma(gd + '/iid.png'); I[~np.all(cls == (215, 215, 215), -1)] = 0
    PID = ma(gd + '/pid.png'); PID[I == 0] = 0
    J = json.load(open(gd + '/nha.json')); H = {h['id']: h for h in J['nha']}
    BONG = cv2.imread(f'{D}/{nua}-bong/rgb.png') if os.path.exists(f'{D}/{nua}-bong/rgb.png') and '--khong-bong' not in sys.argv else None
    for vd in sorted(glob.glob(f'{D}/{nua}-*/rgb.png')):
        v = os.path.basename(os.path.dirname(vd))
        if v.endswith('-bong'): continue
        cfg = json.load(open(f'{D}/{v}.json')) if os.path.exists(f'{D}/{v}.json') else {}
        A = cv2.imread(vd); C = ghep(R, A, I) if v != f'{nua}-goc' else R
        pos = bien_doi(cfg, H)
        res = bmn.do_nha(R, C, I, H, PID, P, BONG=BONG)
        cen = {h: H[h]['tam_px'] for h in pos if h in H}
        for h, r in res.items():
            if not r.get('do'): continue
            lab = pos.get(h)
            if lab is None:
                near = any(np.hypot(H[h]['tam_px'][0] - c[0], H[h]['tam_px'][1] - c[1]) < 40 for c in cen.values())
                lab = 'gan' if near else 'am'
            rows.append(dict(nua=nua, bt=v, id=h, nhan=lab, **{k: r[k] for k in ('px', 'px_m', 'n_canh', 'sup0', 'sup', 'dich_m', 'dx', 'dy') if k in r}))
        print(nua, v, len(res), file=sys.stderr)
json.dump(rows, open(sys.argv[2] if len(sys.argv) > 2 else S + '/a5-feat.json', 'w'))
