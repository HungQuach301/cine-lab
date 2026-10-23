#!/opt/cine/bin/python
"""LOOK-T4 · ĐO mỗi khung look (thước V6/NC-CPU §5.1 + bổ sung):
  look_do.py <ảnh.jpg> [--mask <mặt nạ ID.png>] [--log <log.json của lượt dựng> --hero E,N,h]   → JSON ra stdout
- bao_hoa_tv: bão hoà HSV trung vị (ảnh thu 640×360, như T3 §14.4 — T3 cắt y 60–300; ở đây đo cả khung và vùng giữa y 60–300).
- colorfulness: Hasler–Süsstrunk (σ_rgyb + 0,3 μ_rgyb).   - chi_tiet: trung vị |Laplace| (thang xám 0–255, 640×360) — NC-CPU: không đo được độ thật, chỉ để theo dõi.
- troi_pct: % điểm ảnh trời theo mặt nạ ID (màu 'troi' 40,80,200).   - suong_pct: % điểm ảnh KHÔNG phải trời có độ lệch chuẩn cục bộ (9×9) < 2,5/255 và gần màu chân trời (ΔE76 < 12) — dải sương.
- tieu_diem: vị trí chiếu của vật tiêu điểm (hero_EN) trên khung (% ngang, % dọc từ trên), khoảng cách tới giao điểm 1/3 gần nhất (% đường chéo),
  tương phản cục bộ quanh tiêu điểm (RMS luma trong hộp 6 % khung so với cả khung)."""
import json, sys
import numpy as np, cv2
a = sys.argv[1:]; IMG = a[0]
def opt(k):
    return a[a.index(k) + 1] if k in a else None
im = cv2.imread(IMG); H, W = im.shape[:2]; sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV).astype(np.float32); S = hsv[..., 1] / 255.0
b, g, r = [sm[..., i].astype(np.float32) for i in range(3)]; rg = r - g; yb = 0.5 * (r + g) - b
cf = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
gray = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY).astype(np.float32); lap = np.abs(cv2.Laplacian(gray, cv2.CV_32F))
out = {'tep': IMG, 'co': [W, H], 'bao_hoa_tv': round(float(np.median(S)), 3), 'bao_hoa_tv_giua': round(float(np.median(S[60:300])), 3), 'colorfulness': round(cf, 1),
       'chi_tiet': round(float(np.median(lap)), 2), 'chay_sang_pct': round(float((gray > 250).mean() * 100), 3)}
mk = opt('--mask')
if mk:
    m = cv2.resize(cv2.imread(mk), (640, 360), interpolation=cv2.INTER_NEAREST).astype(int)
    sky = (np.abs(m[..., 0] - 200) < 30) & (np.abs(m[..., 1] - 80) < 30) & (np.abs(m[..., 2] - 40) < 30)
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).astype(np.float32); hor_rows = []
    for x in range(0, 640, 8):
        col = np.where(sky[:, x])[0]
        if len(col): hor_rows.append(col.max())
    if hor_rows:
        yh = int(np.median(hor_rows)); band = lab[max(0, yh - 4):yh + 1][sky[max(0, yh - 4):yh + 1]]
        hc = band.mean(0) if len(band) else lab[sky].mean(0)
    else: hc = lab.reshape(-1, 3).mean(0)
    mu = cv2.blur(gray, (9, 9)); sd = np.sqrt(np.maximum(cv2.blur(gray * gray, (9, 9)) - mu * mu, 0))
    de = np.linalg.norm((lab - hc) * np.array([100 / 255, 1, 1]), axis=-1)
    fog = (~sky) & (sd < 2.5) & (de < 12)
    out['troi_pct'] = round(float(sky.mean() * 100), 1); out['suong_pct'] = round(float(fog.mean() * 100), 1); out['troi_suong_pct'] = round(float((sky | fog).mean() * 100), 1)
lg = opt('--log'); hero = opt('--hero')
if lg and hero:
    L = json.load(open(lg)); f = L['frames'][0]; V = np.array(f['view']).reshape(4, 4).T; P = np.array(f['proj']).reshape(4, 4).T
    E, N, h = [float(v) for v in hero.split(',')]; p = P @ V @ np.array([E - 532000, h, -(N - 180800), 1.0]); ndc = p[:3] / p[3]
    x, y = (ndc[0] + 1) / 2, (1 - ndc[1]) / 2
    th = [(u, v) for u in (1 / 3, 2 / 3) for v in (1 / 3, 2 / 3)]; dmin = min(np.hypot(x - u, y - v) for u, v in th) / np.hypot(1, 1)
    bx = (int(x * 640), int(y * 360)); r_ = 20; win = gray[max(0, bx[1] - r_):bx[1] + r_, max(0, bx[0] - r_):bx[0] + r_]
    out['tieu_diem'] = {'x_pct': round(x * 100, 1), 'y_pct': round(y * 100, 1), 'trong_khung': bool(0 <= x <= 1 and 0 <= y <= 1 and p[3] > 0),
                        'cach_giao_diem_1_3_pct_cheo': round(float(dmin) * 100, 1), 'tuong_phan_cuc_bo_so_khung': round(float(win.std() / max(gray.std(), 1e-3)), 2) if win.size else None}
print(json.dumps(out, ensure_ascii=False))
