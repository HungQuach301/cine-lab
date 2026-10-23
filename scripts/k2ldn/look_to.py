#!/opt/cine/bin/python
"""LOOK-T4 · TỜ CHỌN MÙ: reports/look-t4/to-chon-mu.jpg — 8 hàng (4 mốc × 2 khung) × 3 cột; thứ tự cột XÁO theo hàng (hạt giống cố định, ghi khoá),
nhãn trung tính X / Y / Z; nhãn hàng chỉ ghi mốc + vai khung (không ghi biến thể). Khoá giải mã: reports/look-t4/khoa.json.
Đầu vào: ô 1080p theo biến thể (đã LUT) $LDN_DATA/look/khung-abc/<hàng>-<A|B|C>.jpg + số đo reports/look-t4/do-abc/ (ngoài git — tên lộ biến thể).
Ra (trong git, MÙ): reports/look-t4/khung/<hàng>-<X|Y|Z>.jpg (≤ 2 MB) + reports/look-t4/do/<hàng>-<X|Y|Z>.json; SHA-256 bản A/B/C ghi trong khoa.json.
  look_to.py"""
import json, os, random, shutil
import numpy as np, cv2
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hashlib
K = os.path.join(os.environ.get('LDN_DATA', '/var/tmp/ldn'), 'look/khung-abc'); MU = os.path.join(REPO, 'reports/look-t4/khung'); os.makedirs(MU, exist_ok=True)
DA = os.path.join(os.environ.get('LDN_DATA', '/var/tmp/ldn'), 'look/do-abc'); DM = os.path.join(REPO, 'reports/look-t4/do'); sha = {}
ROWS = [('M1-rong', '1666 trước cháy · toàn cảnh Bankside'), ('M1-trung', '1666 trước cháy · tháp St Saviour (góc Hollar)'),
        ('M2-ngay', '1666 đang cháy · ngày khói 3/9'), ('M2-dem', '1666 đang cháy · đêm lửa 2/9 từ giữa sông'),
        ('M3-rong', '1940 đêm 29/12 · toàn cảnh Bankside'), ('M3-trung', '1940 đêm 29/12 · mái vòm từ Fleet Street'),
        ('M4-rong', '2026 ngày · toàn cảnh Bankside'), ('M4-trung', '2026 ngày · mái vòm + cụm tháp từ Fleet Street')]
rnd = random.Random(16660902); key = {}
TW, TH, LW, PAD = 800, 450, 300, 14
sheet = np.full((PAD + len(ROWS) * (TH + PAD) + 110, LW + 3 * (TW + PAD) + PAD, 3), 236, np.uint8)
def txt(img, s, xy, sc=0.8, th=2, col=(30, 30, 30)):
    cv2.putText(img, s, xy, cv2.FONT_HERSHEY_SIMPLEX, sc, col, th, cv2.LINE_AA)
for j, lab in enumerate('XYZ'): txt(sheet, lab, (LW + PAD + j * (TW + PAD) + TW // 2 - 12, 44), 1.4, 3)
for i, (k, vai) in enumerate(ROWS):
    order = ['A', 'B', 'C']; rnd.shuffle(order); key[k] = dict(zip('XYZ', order))
    y = 60 + i * (TH + PAD)
    txt(sheet, f'{i + 1}. {k}', (12, y + 40), 0.9, 2)
    words = vai.split(' '); line = ''; yy = y + 80
    for w in words:
        if len(line) + len(w) > 24: txt(sheet, line, (12, yy), 0.6, 1); yy += 26; line = ''
        line += w + ' '
    txt(sheet, line, (12, yy), 0.6, 1)
    for j, lab in enumerate('XYZ'):
        src = os.path.join(K, f'{k}-{key[k][lab]}.jpg'); im = cv2.imread(src)
        shutil.copyfile(src, os.path.join(MU, f'{k}-{lab}.jpg')); sha[f'{k}-{key[k][lab]}'] = hashlib.sha256(open(src, 'rb').read()).hexdigest()
        d = json.load(open(os.path.join(DA, f'{k}-{key[k][lab]}.json'))); d['tep'] = f'reports/look-t4/khung/{k}-{lab}.jpg'; json.dump(d, open(os.path.join(DM, f'{k}-{lab}.json'), 'w'), ensure_ascii=False)
        sheet[y:y + TH, LW + PAD + j * (TW + PAD):LW + PAD + j * (TW + PAD) + TW] = cv2.resize(im, (TW, TH), interpolation=cv2.INTER_AREA)
txt(sheet, 'LOOK-T4 · to chon mu · moi hang chon 1 cot (X/Y/Z) hoac "khong cot nao dat" · ban 1080p tung o: reports/look-t4/khung/<hang>-<X|Y|Z>.jpg', (12, sheet.shape[0] - 20), 0.6, 1)
q = 90
while True:
    cv2.imwrite(os.path.join(REPO, 'reports/look-t4/to-chon-mu.jpg'), sheet, [cv2.IMWRITE_JPEG_QUALITY, q])
    if os.path.getsize(os.path.join(REPO, 'reports/look-t4/to-chon-mu.jpg')) < 4_500_000 or q < 60: break
    q -= 5
json.dump({'hat_giong': 16660902, 'bien_the': {'A': 'T3 kênh (cách A + LUT kênh v0,30)', 'B': 'London sương', 'C': 'tranh khắc ấm'}, 'hang': key, 'sha256_ban_abc': sha}, open(os.path.join(REPO, 'reports/look-t4/khoa.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps(key))
