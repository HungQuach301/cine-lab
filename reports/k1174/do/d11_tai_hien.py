#!/opt/cine/bin/python
"""K-1.17.4 · D11 — tái hiện phép (iii) N2P-3 trên bản thử T6 tiền kỳ T4 và tách nguồn điểm 'nước → đất'.
Đầu vào gốc trong git: channel-k2/k2c-t4-02/ai/goc/T6-{render-l1l2.jpg, render-l3.jpg, matna-l1l2.png, matna-l3.png, l1-ai.jpg, l2-ai.jpg, l3-ai.jpg}.
Ghép lại bằng scripts/k2ldn/t6_ghep.py (chạy nguyên, không sửa) vào thư mục tạm → so SHA ghép với reports/tien-ky-t4/kiem/T6-l*-ghep.json.
Đo bằng checks/ll/q_n2p.do_tam (luật 1.17.3, T9b) + tách theo: thành phần nước (sông chính / dải 'biển' chân trời ngoài hộp địa hình),
khoảng cách tới bờ mặt nạ, lý do mất 'màu nước' (lệch sắc / nhạt màu), và lượt 'vùng hợp lệ' (bỏ dải chân trời) theo đề xuất của phiên tiền kỳ.
  /opt/cine/bin/python -I reports/k1174/do/d11_tai_hien.py <thư mục tạm> [--json ra.json] [--hinh ra.jpg]"""
import argparse, hashlib, json, os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')); sys.path.insert(0, ROOT)
import cv2, numpy as np, scipy.ndimage as nd  # noqa: E402
from checks.ll import q_n2p as Q  # noqa: E402

ap = argparse.ArgumentParser(); ap.add_argument('tam'); ap.add_argument('--json'); ap.add_argument('--hinh'); a = ap.parse_args()
G0 = os.path.join(ROOT, 'channel-k2/k2c-t4-02/ai/goc'); OUT = os.path.join(a.tam, 'ghep'); os.makedirs(OUT, exist_ok=True)
LUOT = (('T6-l1', 'l1l2'), ('T6-l2', 'l1l2'), ('T6-l3', 'l3'))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
ra = {'dau_vao': {f: sha(os.path.join(G0, f)) for f in sorted(os.listdir(G0)) if f.startswith('T6-')}, 'luot': {}}
for tag, rm in LUOT:
    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts/k2ldn/t6_ghep.py'), '--render', os.path.join(G0, f'T6-render-{rm}.jpg'), '--ai', os.path.join(G0, f'{tag}-ai.jpg'),
                    '--matna', os.path.join(G0, f'T6-matna-{rm}.png'), '--out', OUT, '--tag', tag], check=True, capture_output=True)
    rp, gp, mp = (os.path.join(OUT, f'{tag}-render-khop.png'), os.path.join(OUT, f'{tag}-ghep.png'), os.path.join(G0, f'T6-matna-{rm}.png'))
    so = json.load(open(os.path.join(ROOT, f'reports/tien-ky-t4/kiem/{tag}-ghep.json'))).get('sha_ghep_png')
    so_b = json.load(open(os.path.join(ROOT, 'reports/tien-ky-t4/kiem/T6-l1b-ghep.json'))).get('sha_ghep_png') if tag == 'T6-l1' else None
    d = Q.do_tam(rp, gp, mp); d_tho = Q.do_tam(os.path.join(G0, f'T6-render-{rm}.jpg'), gp, mp)
    R, G = cv2.imread(rp), cv2.imread(gp); L, names = Q.idmap(mp, (R.shape[1], R.shape[0])); Wt = L == names.index('nuoc'); Dm = Q.lop(L, names, Q.DAT)
    br, bg = Q._blue(R), Q._blue(G); hs = cv2.cvtColor(G, cv2.COLOR_BGR2HSV); loe = (hs[..., 2] >= 217) & (hs[..., 1] <= 64)
    edge = cv2.morphologyEx(Wt.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    bo = cv2.dilate(edge.astype(np.uint8), np.ones((17, 17), np.uint8)) > 0
    X = Wt & br & ~bg & ~loe & ~bo; den = int((Wt & br).sum()); dist = cv2.distanceTransform((~edge).astype(np.uint8), cv2.DIST_L2, 5)
    n, cc, st, _ = cv2.connectedComponentsWithStats(Wt.astype(np.uint8), 8); big = 1 + int(np.argmax(st[1:, 4]))
    tp = [dict(hop=[int(st[i, 0]), int(st[i, 1]), int(st[i, 0] + st[i, 2]), int(st[i, 1] + st[i, 3])], loai='sông chính' if i == big else 'dải nước chân trời (ngoài hộp địa hình)',
               mau_so_px=int((Wt & br & (cc == i)).sum()), tu_so_px=int((X & (cc == i)).sum())) for i in range(1, n)]
    hop_le = cc == big; den_h = int((Wt & br & hop_le).sum()); Xh = X & hop_le
    nx, cx, sx, _ = cv2.connectedComponentsWithStats(X.astype(np.uint8), 8); mins = nd.minimum(dist, cx, index=np.arange(1, nx)) if nx > 1 else np.array([]); sz = sx[1:, 4]
    hx = hs[X]; lech = int(((hx[:, 0] < 85) | (hx[:, 0] > 130)).sum()); nhat = int(((hx[:, 0] >= 85) & (hx[:, 0] <= 130) & (hx[:, 1] < 40)).sum())
    cum = sorted([dict(hop=[int(sx[i, 0]), int(sx[i, 1]), int(sx[i, 0] + sx[i, 2]), int(sx[i, 1] + sx[i, 3])], px=int(sx[i, 4]), cach_bo_px=round(float(mins[i - 1]), 1)) for i in range(1, nx)], key=lambda c: -c['px'])[:8]
    dx = dist[X]
    ra['luot'][tag] = dict(
        sha_ghep_png=sha(gp), sha_ghep_so_kiem=so, sha_ghep_l1b_so_kiem=so_b, khop_sha=sha(gp) in (so, so_b),
        iii_luat_1173=d['iii'], iii_render_tho=d_tho['iii'], i_max_trong_a=d['i']['max_trong_a'], thanh_phan_nuoc=tp,
        vung_hop_le_bo_dai_chan_troi=dict(t9b_nuoc_thanh_dat_pct=round(int(Xh.sum()) / max(1, den_h) * 100, 2), mau_so_px=den_h, tu_so_px=int(Xh.sum())),
        theo_khoang_cach_bo_pct={f'{lo}-{hi}px': round(float(((dx >= lo) & (dx < hi)).sum()) / den * 100, 3) for lo, hi in ((8, 16), (16, 24), (24, 40), (40, 80), (80, 4000))},
        dinh_bo_le_40px_pct=round(float(sz[mins <= 40].sum()) / den * 100, 2) if len(sz) else 0, giua_nuoc_pct=round(float(sz[mins > 40].sum()) / den * 100, 2) if len(sz) else 0,
        ly_do_mat_mau_nuoc=dict(lech_sac_H_ngoai_85_130=lech, nhat_S_duoi_40=nhat), cum_lon=cum,
        dat_thanh_nuoc_bo_dai_chan_troi_pct=round(float((Dm & bg & ~br & ~bo).sum()) / max(1, Dm.sum()) * 100, 2))
    if tag == 'T6-l2' and a.hinh:
        V = (G * 0.55).astype(np.uint8); V[X] = (0, 0, 255); c = lambda z: z[640:900, 400:1500]
        cv2.imwrite(a.hinh, np.vstack([c(R), c(G), c(V)]), [cv2.IMWRITE_JPEG_QUALITY, 82])
js = json.dumps(ra, ensure_ascii=False, indent=1)
open(a.json, 'w').write(js) if a.json else print(js)
