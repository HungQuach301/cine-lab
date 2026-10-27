#!/opt/cine/bin/python
"""BAN-CUOI-T4-B1 · tờ so (vi) dạng bản đồ: toà OSM vùng Barbican/London Wall có mặt ở năm cảnh (1973, 1976) theo LUẬT CŨ (phiên A) ↔ LUẬT B1.
Nguồn: $LDN_DATA/vec/osm2026.json + reports/ban-cuoi-t4-b1/sua/nam-toa-b1.json (cu/moi/tien_nhiem). Toà không đổi năm: vẽ xám (năm không đổi giữa hai luật).
Màu: xanh = có mặt cả hai; đỏ = có ở luật cũ, KHÔNG ở B1 (toà sau năm cảnh); vàng = thiếu ở luật cũ, có ở B1 (tháp Barbican…); tím = khối tiền nhiệm hậu chiến (chỉ B1).
  ban_do_nam_b1.py <ra.jpg>"""
import json, os, sys, numpy as np, cv2
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
R = json.load(open(os.path.join(os.environ.get('LDN_DATA', '/var/tmp/ldn'), 'vec/osm2026.json')))['toa']
D = json.load(open(os.path.join(REPO, 'reports/ban-cuoi-t4-b1/sua/nam-toa-b1.json')))
CH = {d['id']: d for d in D if 'moi' in d}; TN = {d['id']: d for d in D if 'tien_nhiem' in d}
X0, Y0, X1, Y1 = 531850, 181350, 532800, 182000; S = 1.0
def px(r): r = np.array(r, float); return np.round(np.c_[(r[:, 0] - X0) * S, (Y1 - r[:, 1]) * S]).astype(np.int32)
F = cv2.FONT_HERSHEY_SIMPLEX; panels = []
for Y in (1973.0, 1976.0):
    for luat in ('cu', 'b1'):
        im = np.full((int((Y1 - Y0) * S) + 40, int((X1 - X0) * S), 3), 24, np.uint8)
        for b in R:
            if b['part'] or len(b['r']) < 3: continue
            c = np.mean(np.array(b['r'], float), 0)
            if not (X0 < c[0] < X1 and Y0 < c[1] < Y1): continue
            d = CH.get(b['id']); t = TN.get(b['id']); col = (90, 90, 90)
            if d:
                a, m = d['cu'] <= Y, d['moi'] <= Y
                col = (80, 170, 80) if (a and m) else (40, 40, 220) if (a and not m) else (40, 210, 230) if (m and not a) else (60, 60, 60)
                if luat == 'cu': col = (80, 170, 80) if a else (60, 60, 60)
                elif not m: col = (60, 60, 60)
                if luat == 'cu' and a and not m: col = (40, 40, 220)
                if luat == 'b1' and m and not a: col = (40, 210, 230)
            if luat == 'b1' and t and t['tien_nhiem'][0] <= Y < t['tien_nhiem'][1]: col = (200, 80, 180)
            cv2.fillPoly(im, [px(b['r'])], col); cv2.polylines(im, [px(b['r'])], True, (20, 20, 20), 1)
        cv2.putText(im, f"{int(Y)} - {'LUAT CU (phien A)' if luat == 'cu' else 'LUAT B1'}", (8, im.shape[0] - 12), F, 0.6, (240, 240, 240), 1, cv2.LINE_AA)
        panels.append(im)
top = np.hstack([panels[0], np.full((panels[0].shape[0], 6, 3), 0, np.uint8), panels[1]]); bot = np.hstack([panels[2], np.full((panels[2].shape[0], 6, 3), 0, np.uint8), panels[3]])
img = np.vstack([top, np.zeros((6, top.shape[1], 3), np.uint8), bot])
leg = np.full((34, img.shape[1], 3), 16, np.uint8)
cv2.putText(leg, 'xanh: co ca hai | do: luat cu co, B1 khong (toa sau nam canh) | vang: B1 them (thap Barbican...) | tim: khoi tien nhiem hau chien (B1) | xam: khong doi/khong co', (8, 22), F, 0.48, (230, 230, 230), 1, cv2.LINE_AA)
cv2.imwrite(sys.argv[1], np.vstack([leg, img]), [cv2.IMWRITE_JPEG_QUALITY, 88]); print(sys.argv[1], img.shape)
