#!/opt/cine/bin/python
"""TIEN-KY-T4 · BẢN THỬ T6 (phần chuyển động) — shot timelapse MÁY CỐ ĐỊNH: nền = MỘT tấm N2+ tĩnh; lớp (a) + mọi thứ chuyển động (bóng nắng trên nhà) = render TỪNG KHUNG,
ghép theo mặt nạ ID từng khung; khớp màu render vào tông tấm (thông số Reinhard tính một lần ở khung 0, dùng cho cả shot — không nhấp nháy màu).
  t6_timelapse.py <khung render> <mặt nạ PNG> <tấm AI> <ra> [--k 0.7]
Đo (v): nhấp nháy vùng (c) = TB |Δ xám|/khung (tấm tĩnh → ≈ 0) so đối chứng render; ghi t6-tl.json."""
import json, os, sys
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, str(Path(__file__).resolve().parent / 'ai'))
import n2p_lib as L  # noqa: E402
RD, MD, PLATE, OUT = sys.argv[1:5]; os.makedirs(OUT, exist_ok=True); K = float(sys.argv[sys.argv.index('--k') + 1]) if '--k' in sys.argv else 0.7
fr = sorted(f for f in os.listdir(RD) if f.endswith('.jpg')); R0 = cv2.imread(os.path.join(RD, fr[0])); H, W = R0.shape[:2]
AI = cv2.resize(cv2.imread(PLATE), (W, H), interpolation=cv2.INTER_AREA)
def lab_(x): return cv2.cvtColor(x, cv2.COLOR_BGR2LAB).astype(np.float32)
A0 = L.bao_ve(L.lop_mask(L.idmap(os.path.join(MD, fr[0].replace('.jpg', '.png')), (W, H)), ['nha']), no=1, nho_px=60, no_nho=3)
Rl, Al = lab_(R0), lab_(AI); mr, sr = Rl[A0].mean(0), Rl[A0].std(0) + 1e-3; ma, sa = Al[A0].mean(0), Al[A0].std(0) + 1e-3
fl_g, fl_r, prev_g, prev_r = [], [], None, None
for f in fr:
    R = cv2.imread(os.path.join(RD, f)); A = L.bao_ve(L.lop_mask(L.idmap(os.path.join(MD, f.replace('.jpg', '.png')), (W, H)), ['nha']), no=1, nho_px=60, no_nho=3)
    Rk = cv2.cvtColor(np.clip((lab_(R) - mr) * (1 + K * (sa / sr - 1)) + mr + K * (ma - mr), 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    G, _ = L.ghep(Rk, AI, A, feather=3, bao=False); cv2.imwrite(os.path.join(OUT, f), G, [cv2.IMWRITE_JPEG_QUALITY, 92])
    c = ~A; g = cv2.cvtColor(G, cv2.COLOR_BGR2GRAY).astype(np.float32); r = cv2.cvtColor(R, cv2.COLOR_BGR2GRAY).astype(np.float32)
    if prev_g is not None: fl_g.append(float(np.abs(g - prev_g)[c & prev_c].mean())); fl_r.append(float(np.abs(r - prev_r)[c & prev_c].mean()))
    prev_g, prev_r, prev_c = g, r, c
rec = {'khung': len(fr), 'tam': PLATE, 'k_khop_mau': K, 'nhap_nhay_c_ghep': round(float(np.mean(fl_g)), 4), 'nhap_nhay_c_doi_chung_render': round(float(np.mean(fl_r)), 4)}
json.dump(rec, open(os.path.join(OUT, 't6-tl.json'), 'w'), ensure_ascii=False, indent=1); print(json.dumps(rec, ensure_ascii=False))
