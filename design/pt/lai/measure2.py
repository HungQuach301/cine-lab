"""PT2 · đo khung tĩnh theo ĐÚNG cách điều phối: thu toàn khung về 640×360 (INTER_AREA), cắt hàng y 60–300 (toàn bộ chiều ngang),
bão hoà = trung vị S (HSV, /255); colorfulness Hasler–Süsstrunk; chi tiết = trung bình PIL FIND_EDGES trên độ sáng (bỏ viền 1 px).
Thêm: % trời, % mặt đất (nền A, lượt mã lớp), vùng bảo vệ LAI vs A-thuần (cùng khung, không chữ): sai khác TB /255 và % điểm ảnh khác.
  /opt/cine/bin/python -I measure2.py <thư mục khung> <ra.json>"""
import sys, os, json, re, numpy as np, cv2
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lai_common as LC
D, OUT = sys.argv[1], sys.argv[2]; BG = '/var/tmp/pt2/bg'
def m3(path):
    im = np.asarray(Image.open(path).convert('RGB')); s = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)[60:300]
    hsv = cv2.cvtColor(s, cv2.COLOR_RGB2HSV); sat = float(np.median(hsv[..., 1]) / 255)
    r, g, b = [s[..., k].astype(np.float64) for k in range(3)]; rg, yb = r - g, 0.5 * (r + g) - b
    col = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    fe = np.asarray(Image.fromarray(s).convert('L').filter(ImageFilter.FIND_EDGES)).astype(np.float64)[1:-1, 1:-1].mean()
    return {'bao_hoa': round(sat, 3), 'colorfulness': round(col, 1), 'find_edges': round(float(fe), 1)}
rows = {}
for f in sorted(os.listdir(D)):
    m = re.match(r'(\d{4})-(\w+)-(LAI|A)-notext\.png$', f)
    if not m: continue
    ep, t, ban = m.groups(); r = rows.setdefault(f'{ep}-{t}', {}); r[ban] = m3(os.path.join(D, f))
    if ban == 'LAI' and os.path.exists(os.path.join(D, f'{ep}-{t}-A-notext.png')):
        prot = cv2.imread(os.path.join(BG, f'{ep}L', 'bao_ve.png'), cv2.IMREAD_GRAYSCALE) > 127   # vùng bảo vệ THỰC dùng khi ghép (mã lớp + vật bị loại ở HC4)
        a = np.asarray(Image.open(os.path.join(D, f'{ep}-{t}-A-notext.png')).convert('RGB')).astype(np.int64)
        l = np.asarray(Image.open(os.path.join(D, f)).convert('RGB')).astype(np.int64)
        if a.shape[:2] != prot.shape: prot = cv2.resize(prot.astype(np.uint8), (a.shape[1], a.shape[0]), interpolation=cv2.INTER_NEAREST) > 0
        dd = np.abs(a - l)[prot]
        r['vung_bao_ve'] = {'sai_khac_TB_tren_255': round(float(dd.mean()), 4), 'pct_diem_anh_khac_qua_2': round(float((dd.max(-1) > 2).mean() * 100), 3),
                            'ghi_chu': 'so trên PNG 8 bit của khung cuối (sau lớp sống + chỉnh màu), không chữ'}
for ep in (1782, 1943):
    t = LC.class_table(os.path.join(BG, f'{ep}A')); rows[f'{ep}-nen'] = {'troi_pct': round(t['troi'] * 100, 2), 'mat_dat_pct': round(t['mat_dat'] * 100, 2)}
json.dump(rows, open(OUT, 'w'), indent=1, ensure_ascii=False)
for k, v in rows.items(): print(k, json.dumps(v, ensure_ascii=False))
