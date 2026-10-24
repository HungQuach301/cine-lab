"""K-1.17.5 · A1/A2 trên ảnh thật: T6 tiền kỳ (mặt nạ trong git; ghép lại bằng t6_ghep.py nguyên bản qua d11_tai_hien.py) + look2 (24 ảnh AI thô;
mặt nạ ID KHÔNG có trong git → mặt nạ nước SUY từ render theo định nghĩa T9b — chỉ báo, không phán). Đo T9b (1.17.4) và T9c (1.17.5).
  /opt/cine/bin/python -I reports/k1175/do/a1_thuc.py <thư mục d11 ghép> <thư mục look2 git archive> --json ra.json"""
import sys, os, json, cv2, numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')); sys.path.insert(0, ROOT)
from checks.ll import q_n2p as Q, q_k1175 as K
d11, l2 = sys.argv[1], sys.argv[2]; out = {}
G0 = os.path.join(ROOT, 'channel-k2/k2c-t4-02/ai/goc')
for tag, rm in (('T6-l1', 'l1l2'), ('T6-l2', 'l1l2'), ('T6-l3', 'l3')):
    R = cv2.imread(f'{d11}/{tag}-render-khop.png'); G = cv2.imread(f'{d11}/{tag}-ghep.png'); mp = f'{G0}/T6-matna-{rm}.png'; L, n = Q.idmap(mp, (1920, 1080))
    old = Q.do_tam(f'{d11}/{tag}-render-khop.png', f'{d11}/{tag}-ghep.png', mp)['iii']; new = K.t9c(R, G, L, n); new.pop('win')
    ctl = K.t9c(R, R, L, n); ctl.pop('win')
    out[tag] = dict(t9b=old, t9c=new, t9c_render_voi_chinh_no=dict(dat=ctl['dat'], so_doan_lan=ctl['so_doan_lan'], giua_pct=ctl['giua_pct']))
sys.path.insert(0, os.path.dirname(__file__))
def mat_na(R):
    h = cv2.cvtColor(R, cv2.COLOR_BGR2HSV); b = (h[..., 0] >= 85) & (h[..., 0] <= 130) & (h[..., 1] >= 40) & (h[..., 2] >= 30)
    b = cv2.morphologyEx(cv2.morphologyEx(b.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n_, cc, st, _ = cv2.connectedComponentsWithStats(b, 4); H, W = b.shape; L = np.full((H, W), 2, np.uint8)
    for i in range(1, n_):
        if st[i, 4] >= 0.002 * H * W: L[cc == i] = 0 if st[i, 1] == 0 else 1
    return L, ['troi', 'nuoc', 'bang']
for k in ('M1-rong', 'M1-trung', 'M4-rong'):
    R = cv2.imread(f'{l2}/reports/look-t4-v2/khung/{k}-v2-3d.jpg'); L, n = mat_na(R)
    for cu in ('oai', 'gem'):
        for lu in (1, 2, 3):
            G = cv2.resize(cv2.imread(f'{l2}/channel-k2/k2c-t4-02/ai/goc-v2/{k}-{cu}-l{lu}-ai.jpg'), (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
            r = K.t9c(R, G, L, n); r.pop('win')
            hb = lambda X: cv2.cvtColor(X, cv2.COLOR_BGR2HSV)
            br, bg = Q._blue(R), Q._blue(G); Wt = L == 1
            out[f'{k}-{cu}-l{lu}'] = dict(mat_na='suy từ render (chỉ báo)', t9b_nuoc_thanh_dat_tho_pct=round(float((Wt & br & ~bg).sum() / max(1, (Wt & br).sum()) * 100), 2),
                                          t9c=dict(dat=r['dat'], so_doan_lan=r['so_doan_lan'], sau_lon_nhat_px=r['sau_lon_nhat_px'], giua_pct=r['giua_pct'], tau=r['tau'], lan=r['lan'][:4]))
json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), ensure_ascii=False, indent=1, default=float)
for k, v in out.items(): print(k, json.dumps(v.get('t9c'), ensure_ascii=False, default=float)[:220], v.get('t9b_nuoc_thanh_dat_tho_pct', v.get('t9b')))
