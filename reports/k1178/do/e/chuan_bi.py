#!/opt/cine/bin/python
"""K-1.17.8 · LUẬT E — đáp án: dựng mặt nạ E (nhà thường 215 / công trình có tên 235) + mặt nạ mã công trình + bản đêm tổng hợp từ render V2 P9-2026.
Nguồn: origin/claude/animatic-t4-v2-revision-hwh8jp @1a911a01 channel-k2/k2c-t4-02/animatic2/tam-nen/P9-2026/{render,matna}.png (render V2, 1920×1080).
Hộp công trình có tên lập bằng mắt trên render (K, 25/10/2026) — mái vòm St Paul's + 7 toà tháp City nhô khỏi chân trời; tên trong đáp án là
nhãn (toa_1…toa_7), không khẳng định tên OSM.   chuan_bi.py <render.png> <matna.png> <thư mục ra>"""
import json, os, sys
import cv2, numpy as np

HOP = {  # (x0, y0, x1, y1) khung 1920×1080; giao với lớp 'nha' 235 của mặt nạ V2
    'st_pauls': [(760, 495, 845, 700), (588, 612, 962, 775)],
    'toa_1': [(930, 470, 975, 585)], 'toa_2': [(1085, 470, 1133, 578)], 'toa_3': [(1255, 470, 1299, 568)], 'toa_4': [(1385, 495, 1429, 568)],
    'toa_5': [(1508, 490, 1542, 590)], 'toa_6': [(1590, 495, 1633, 600)], 'toa_7': [(1675, 515, 1735, 600)]}


def main():
    rp, mp, out = sys.argv[1:4]; os.makedirs(out, exist_ok=True)
    R = cv2.imread(rp); M = cv2.imread(mp)[:, :, ::-1].copy()
    nha = (M[..., 0] == 235) & (M[..., 1] == 235) & (M[..., 2] == 235)
    ten = np.zeros(nha.shape, np.int32); toa = []
    for i, (k, hs) in enumerate(HOP.items(), 1):
        b = np.zeros_like(nha)
        for x0, y0, x1, y1 in hs: b[y0:y1, x0:x1] = True
        m = b & nha & (ten == 0); ten[m] = i
        ys, xs = np.nonzero(m)
        toa.append(dict(ten=k, ma=i, mau=[i * 20, 0, 200], px=int(m.sum()), dinh_y=int(ys.min()), x_tam=int(xs.mean()), hop=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]))
    E = M.copy(); E[nha & (ten == 0)] = (215, 215, 215)   # nhà thường
    cv2.imwrite(os.path.join(out, 'matna-e.png'), E[:, :, ::-1])
    CT = np.zeros_like(M); 
    for t in toa: CT[ten == t['ma']] = t['mau']
    cv2.imwrite(os.path.join(out, 'matna-ct.png'), CT[:, :, ::-1])
    json.dump(toa, open(os.path.join(out, 'toa.json'), 'w'), ensure_ascii=False, indent=1)
    # bản đêm tổng hợp (KHÔNG phải render đêm V2): giảm sáng + ám lạnh; trời gần đen — dùng làm đầu vào ảnh AI đêm và "render đối chứng" của tấm đêm
    f = R.astype(np.float32) / 255; dem = np.clip(((f ** 2.2) * 0.10) ** (1 / 2.2) * np.array([1.15, 0.95, 0.85]), 0, 1)
    cv2.imwrite(os.path.join(out, 'render-dem.png'), (dem * 255 + 0.5).astype(np.uint8))
    print(json.dumps(toa, ensure_ascii=False))


if __name__ == '__main__':
    main()
