"""PT4 · đo khung tĩnh theo ĐÚNG cách điều phối (như measure2.py PT2): toàn khung → 640×360 INTER_AREA, cắt y 60–300 (cả bề ngang);
bão hoà = trung vị S (HSV /255); colorfulness Hasler–Süsstrunk; chi tiết = TB PIL FIND_EDGES trên độ sáng (bỏ viền 1 px);
thêm độ tương phản (độ lệch chuẩn độ sáng /255) để kiểm "giữ tương phản" khi hạ bão hoà. Vùng bảo vệ LAI vs A-thuần như PT2.
  /opt/cine/bin/python -I measure4.py <ra.json> nhan=<ảnh> [nhan=<ảnh> …] [--bv <bao_ve.png> <ảnh LAI> <ảnh A>]"""
import sys, os, json, numpy as np, cv2
from PIL import Image, ImageFilter
def m3(path):
    im = np.asarray(Image.open(path).convert('RGB')); s = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)[60:300]
    hsv = cv2.cvtColor(s, cv2.COLOR_RGB2HSV); sat = float(np.median(hsv[..., 1]) / 255)
    r, g, b = [s[..., k].astype(np.float64) for k in range(3)]; rg, yb = r - g, 0.5 * (r + g) - b
    col = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    L = np.asarray(Image.fromarray(s).convert('L')); fe = np.asarray(Image.fromarray(L).filter(ImageFilter.FIND_EDGES)).astype(np.float64)[1:-1, 1:-1].mean()
    return {'bao_hoa': round(sat, 3), 'colorfulness': round(col, 1), 'find_edges': round(float(fe), 1), 'tuong_phan': round(float(L.std() / 255), 3)}
out = {}; args = sys.argv[2:]
if '--bv' in args:
    i = args.index('--bv'); bv, la, aa = args[i + 1:i + 4]; args = args[:i] + args[i + 4:]
    prot = cv2.imread(bv, cv2.IMREAD_GRAYSCALE) > 127; a = np.asarray(Image.open(aa).convert('RGB')).astype(np.int64); l = np.asarray(Image.open(la).convert('RGB')).astype(np.int64)
    if a.shape[:2] != prot.shape: prot = cv2.resize(prot.astype(np.uint8), (a.shape[1], a.shape[0]), interpolation=cv2.INTER_NEAREST) > 0
    dd = np.abs(a - l)[prot]; out['vung_bao_ve'] = {'sai_khac_TB_tren_255': round(float(dd.mean()), 4), 'pct_diem_anh_khac_qua_2': round(float((dd.max(-1) > 2).mean() * 100), 3)}
for a in args:
    k, p = a.split('=', 1); out[k] = m3(p)
json.dump(out, open(sys.argv[1], 'w'), indent=1, ensure_ascii=False)
for k, v in out.items(): print(k, json.dumps(v, ensure_ascii=False))
