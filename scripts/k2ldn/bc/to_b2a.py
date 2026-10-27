#!/opt/cine/bin/python
"""BAN-CUOI-T4-B2a · tờ so / tờ khung (JPG ≤ 2 MB) + số đo nhanh (độ sáng TB, % điểm cháy trắng).
  to_b2a.py luoi <ra.jpg> <số cột> <rộng ô> <ảnh>[::nhãn] …        lưới ảnh có nhãn; giảm chất lượng tới ≤ 2 MB
  to_b2a.py do <ảnh> …                                             in JSON: sang_tb (0–255, luma Rec.709), chay_trang_pct (mọi kênh ≥ 250), sang_p99
  to_b2a.py trang <thư mục khung> <n>                              soi cháy trắng n khung đầu (bài học H1-13a/c): % điểm ≥ 250 mỗi khung + vùng sáng nhất"""
import json, os, sys
import cv2, numpy as np


def nhan(im, s):
    if not s: return im
    cv2.rectangle(im, (0, 0), (min(im.shape[1], 14 + 11 * len(s)), 26), (0, 0, 0), -1)
    cv2.putText(im, s, (6, 19), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA); return im


def luoi(ra, cot, w, items):
    o = []
    for it in items:
        p, _, s = it.partition('::'); im = cv2.imread(p) if p != '-' else None
        if im is None: im = np.zeros((int(w * 9 / 16), w, 3), np.uint8)
        im = cv2.resize(im, (w, int(round(im.shape[0] * w / im.shape[1]))), interpolation=cv2.INTER_AREA); o.append(nhan(im, s))
    h = max(i.shape[0] for i in o); o = [cv2.copyMakeBorder(i, 0, h - i.shape[0], 0, 0, cv2.BORDER_CONSTANT) for i in o]
    while len(o) % cot: o.append(np.zeros_like(o[0]))
    G = np.vstack([np.hstack(o[r * cot:(r + 1) * cot]) for r in range(len(o) // cot)])
    for q in (90, 85, 80, 75, 70, 60, 50):
        cv2.imwrite(ra, G, [cv2.IMWRITE_JPEG_QUALITY, q])
        if os.path.getsize(ra) <= 2_000_000: break
    print(ra, G.shape[1], 'x', G.shape[0], 'q', q, round(os.path.getsize(ra) / 1e6, 2), 'MB')


def do(p):
    im = cv2.imread(p).astype(np.float64); Y = 0.0722 * im[..., 0] + 0.7152 * im[..., 1] + 0.2126 * im[..., 2]
    return dict(anh=p, sang_tb=round(float(Y.mean()), 2), sang_p99=round(float(np.percentile(Y, 99)), 1), chay_trang_pct=round(float((im.min(-1) >= 250).mean() * 100), 3))


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'luoi': luoi(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5:])
    elif c == 'do': print(json.dumps([do(p) for p in sys.argv[2:]], ensure_ascii=False))
    elif c == 'trang':
        d, n = sys.argv[2], int(sys.argv[3]); fs = sorted(f for f in os.listdir(d) if f.endswith('.jpg'))[:n]
        print(json.dumps([do(f'{d}/{f}') for f in fs], ensure_ascii=False))
