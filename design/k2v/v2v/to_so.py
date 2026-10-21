#!/opt/cine/bin/python -I
"""NC-V2V · TỜ SO trước–sau (PNG): hàng = thời điểm, cột = nguồn V7B + các biến thể Omni; hàng cuối = bản đồ CẠNH MỚI (đỏ: cạnh ra cách mọi cạnh nguồn > 3 px,
sau căn ECC như do_v2v.py) + LỬA MỚI (vàng) ở giữa clip. Không chữ trong khung ngoài nhãn cột/hàng ở dải trên.
  to_so.py --src nguồn.mp4 --out a.mp4 b.mp4 c.mp4 --nhan nguồn a b c --khung 48 192 --png ra.png"""
import argparse, importlib.util, os
import cv2, numpy as np
sp = importlib.util.spec_from_file_location('d', os.path.join(os.path.dirname(__file__), 'do_v2v.py')); d = importlib.util.module_from_spec(sp); sp.loader.exec_module(d)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--src'); ap.add_argument('--out', nargs='+'); ap.add_argument('--nhan', nargs='+'); ap.add_argument('--khung', nargs='+', type=int); ap.add_argument('--png')
    a = ap.parse_args(); S = d.frames(a.src); O = [d.frames(x) for x in a.out]; cw, ch = 480, 270; bar = 34
    rows = []
    def lab(img, t):
        img = img.copy(); cv2.rectangle(img, (0, 0), (img.shape[1], bar), (20, 20, 20), -1); cv2.putText(img, t, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (240, 240, 240), 1, cv2.LINE_AA); return img
    for f in a.khung:
        cells = [cv2.resize(S[f], (cw, ch), interpolation=cv2.INTER_AREA)] + [cv2.resize(o[f], (cw, ch), interpolation=cv2.INTER_AREA) for o in O]
        rows.append(np.hstack([np.vstack([lab(np.zeros((bar, cw, 3), np.uint8), f'{n} - {f / 24:.1f} s'), c]) for n, c in zip(a.nhan, cells)]))
    f = a.khung[len(a.khung) // 2] if len(a.khung) > 1 else a.khung[0]; f = (a.khung[0] + a.khung[-1]) // 2
    cells = [cv2.resize(S[f], (cw, ch)) // 3]
    gs = cv2.cvtColor(S[f], cv2.COLOR_BGR2GRAY); Es = d.canny(gs); near = cv2.dilate(Es.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    for o in O:
        al, _ = d.align(S[f], o[f]); Eo = d.canny(cv2.cvtColor(al, cv2.COLOR_BGR2GRAY)); nE = Eo & ~near
        h = cv2.cvtColor(al, cv2.COLOR_BGR2HSV); hs = cv2.cvtColor(S[f], cv2.COLOR_BGR2HSV)
        fire = lambda q: (q[..., 0] >= 3) & (q[..., 0] <= 20) & (q[..., 1] >= 115) & (q[..., 2] >= 160)
        nf = fire(h) & ~(cv2.dilate(fire(hs).astype(np.uint8), np.ones((13, 13), np.uint8)) > 0)
        v = (cv2.cvtColor(gs, cv2.COLOR_GRAY2BGR) // 4).copy(); v[nE] = (40, 40, 255); v[nf] = (0, 230, 255)
        cells.append(cv2.resize(v, (cw, ch), interpolation=cv2.INTER_NEAREST))
    names = ['nguon (toi)'] + [f'{n}: canh moi=do, lua moi=vang' for n in a.nhan[1:]]   # nhãn ASCII (phông Hershey của OpenCV không có dấu)
    rows.append(np.hstack([np.vstack([lab(np.zeros((bar, cw, 3), np.uint8), f'{n} - {f / 24:.1f} s'), c]) for n, c in zip(names, cells)]))
    cv2.imwrite(a.png, np.vstack(rows), [cv2.IMWRITE_PNG_COMPRESSION, 9]); print(a.png)


if __name__ == '__main__': main()
