#!/opt/cine/bin/python
"""TIEN-KY-T4 · BẢN THỬ T6 — ghép tấm nền N2+ (§15 b): ảnh AI sửa KHÔNG gửi mặt nạ → ghép lại LỚP (a) từ render theo mặt nạ ID (nở 1 px, vật < 60 px nở 3 px, viền mềm ≤ 3 px)
+ khớp màu RENDER VÀO tông tấm nền (một phép biến đổi Lab toàn cục, tất định — không kéo tấm AI về tông render).
  t6_ghep.py --render r.jpg --ai ai.jpg --matna m.jpg --out <thư mục> --tag T6-l1
Ra: <tag>-render-khop.jpg (render sau khớp màu = tham chiếu lớp (a) cho kiểm (i)), <tag>-ghep.jpg, <tag>-ghep.json (thông số khớp màu, % điểm ảnh AI, lệch (a))."""
import argparse, json, os, sys
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, str(Path(__file__).resolve().parent / 'ai'))
import n2p_lib as L  # noqa: E402
ap = argparse.ArgumentParser(); ap.add_argument('--render', required=True); ap.add_argument('--ai', required=True); ap.add_argument('--matna', required=True)
ap.add_argument('--out', required=True); ap.add_argument('--tag', required=True); a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
R = cv2.imread(a.render); H, W = R.shape[:2]; AI = cv2.resize(cv2.imread(a.ai), (W, H), interpolation=cv2.INTER_AREA)
lab = L.idmap(a.matna, (W, H)); A = L.lop_mask(lab, ['nha'])                  # lớp (a): nhà/công trình/cầu/tường (mặt nạ 'nha')
Ab = L.bao_ve(A, no=1, nho_px=60, no_nho=3)                                      # vùng bảo vệ (luật §15 a)
# khớp màu Reinhard trong Lab: thống kê vùng (a) của render → thống kê CÙNG vùng trên tấm AI (tông AI)
def lab_(x): return cv2.cvtColor(x, cv2.COLOR_BGR2LAB).astype(np.float32)
Rl, Al = lab_(R), lab_(AI); m = Ab
mr, sr = Rl[m].mean(0), Rl[m].std(0) + 1e-3; ma, sa = Al[m].mean(0), Al[m].std(0) + 1e-3
k = np.array([0.7, 0.7, 0.7], np.float32)                                         # nửa đường (giữ phần lớn sắc độ render; k = 1 → khớp hoàn toàn)
Rk = (Rl - mr) * (1 + k * (sa / sr - 1)) + mr + k * (ma - mr)
RK = cv2.cvtColor(np.clip(Rk, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
G, _al = L.ghep(RK, AI, Ab, feather=3, bao=False)
cv2.imwrite(str(out / f'{a.tag}-render-khop.jpg'), RK, [cv2.IMWRITE_JPEG_QUALITY, 95]); cv2.imwrite(str(out / f'{a.tag}-ghep.jpg'), G, [cv2.IMWRITE_JPEG_QUALITY, 95])
cv2.imwrite(str(out / f'{a.tag}-ghep.png'), G); cv2.imwrite(str(out / f'{a.tag}-render-khop.png'), RK)
d = np.abs(G.astype(int) - RK.astype(int)).max(-1)
inner = cv2.erode(Ab.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
rec = {'tag': a.tag, 'khop_mau': {'k': k.tolist(), 'mean_render': mr.tolist(), 'mean_ai': ma.tolist(), 'std_render': sr.tolist(), 'std_ai': sa.tolist()},
       'pct_lop_a': round(float(A.mean() * 100), 2), 'pct_vung_bao_ve': round(float(Ab.mean() * 100), 2), 'pct_diem_anh_ai': round(float((~Ab).mean() * 100), 2),
       'lech_a_max_trong_long_8bit': int(d[inner].max()) if inner.any() else None, 'sha_ghep_png': L.sha_file(out / f'{a.tag}-ghep.png')}
json.dump(rec, open(out / f'{a.tag}-ghep.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(rec, ensure_ascii=False))
