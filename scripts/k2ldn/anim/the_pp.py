#!/opt/cine/bin/python
"""ANIMATIC-T4 · việc 4 — chữ NHÁP hai thẻ "How this film was made" (khoa-loi/the-phuong-phap-NHAP.md của GIONG-T4) + dòng L6 (lõi khối 1666 ước lượng) + L4 (City 1940 khối ước lượng)
+ % diện tích lấp: trong ranh vùng cháy 1666 (Doornick, bậc 1), phần đất xây (không phố, không nước) cách tim phố > 15 m (≈ quá một chiều sâu nhà mặt phố) = lõi khối dựng ƯỚC LƯỢNG (bậc 5).
Không nhắc AI (§14.1 c, f; §15 e). Giới hạn K1173-D3: ≤ 27 từ cả tiêu đề / 9 s, ≤ 21 từ / 7 s (≤ 3 từ/s). → channel-k2/k2c-t4-02/animatic/the-phuong-phap.json"""
import json, os
from pathlib import Path
import numpy as np, cv2
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; LD = Path(os.environ.get('LDN_DATA', '/var/tmp/ldn'))
m = json.loads((LD / 'look2/ldn2.json').read_text())['lop_dat']; c = cv2.imread(str(LD / 'look2/cls66.png'), 0)
en = json.loads((EP / 'mo-hinh/ranh-chay-1666-cuoi.json').read_text())['tps']['en']
px = np.array([[(e - m['E0']) / m['buoc'], (m['N1'] - n) / m['buoc']] for e, n in en], np.int32); R = np.zeros_like(c); cv2.fillPoly(R, [px], 1)
pho = (c == 1).astype(np.uint8); dt = cv2.distanceTransform(1 - pho, cv2.DIST_L2, 5) * m['buoc']
dat = (R == 1) & (c != 1) & (c != 6); loi = dat & (dt > 15)
pct = round(100 * loi.sum() / max(1, dat.sum()), 1)
the = [{'giay': 9.0, 'tieu_de': 'How this film was made',
        'dong': ["Streets and buildings are rebuilt in 3D from the 1666 Doornick survey, Hollar's engravings and modern maps. Sources are in the description."]},
       {'giay': 7.0, 'tieu_de': None,
        'dong': [f"Estimated: the fire's daily extent, 1940 damage, 1666 block interiors (about {pct:.0f}% of built area) and 1940 City blocks."]}]
for t in the:
    n = sum(len(x.split()) for x in t['dong']) + (len(t['tieu_de'].split()) if t['tieu_de'] else 0); t['so_tu'] = n; t['tu_moi_giay'] = round(n / t['giay'], 2)
out = {'nhap': True, 'can_cu': 'khoa-loi/the-phuong-phap-NHAP.md + L4, L6 (chủ dự án 23/10/2026 23:27) + K1173-D3', 'pct_loi_khoi_uoc_luong': pct,
       'cach_do': 'ranh vùng cháy cuối 1666 (mo-hinh/ranh-chay-1666-cuoi.json, TPS) ∩ lớp đất 1666 (cls66.png, ô 2 m): đất xây = không phố (lớp 1), không nước (lớp 6); lõi = cách tim phố > 15 m',
       'the': the}
(EP / 'animatic/the-phuong-phap.json').write_text(json.dumps(out, ensure_ascii=False, indent=1)); print(json.dumps(out, ensure_ascii=False)[:900])
