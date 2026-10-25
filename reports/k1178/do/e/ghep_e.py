#!/opt/cine/bin/python
"""K-1.17.8 · LUẬT E — ghép đáp án: ảnh AI toàn khung (2560×1440 → 1920×1080, INTER_AREA) + lớp (a)-E từ render (nở 1 px — §15 (a) vùng bảo vệ).
Lớp (a)-E = mặt nạ E: 'nha' 235 (công trình có tên: mái vòm St Paul's, toà tháp có tên, cầu, tường) ∪ 'nuoc' ∪ dải bờ ±8 px @1080 ∪ 'congsu' 'tau' 'lua' 'co' 'pin' 'nguoi'.
Biến đổi tổng hợp (đáp án): xoa_toa (xoá toà có tên: vá bằng trời ảnh AI), doi_toa (dời toà có tên 30 px), thap_bia (dán tháp bịa cao hơn toà có tên gần nhất),
thap_thap (tháp bịa thấp hơn — đối chứng), chu (dán chữ/biển sáng lên mặt nhà thường), thuyen (dán thuyền lên sông).
  ghep_e.py <render.png> <matna-e.png> <ai.jpg> <ra.png> [--bien <kiểu>] [--toa toa.json]"""
import json, sys
import cv2, numpy as np
sys.path.insert(0, __import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__file__), '..', '..', '..', '..')))
from checks.ll import q_n2p as N  # noqa: E402

LOP = ('nha', 'nuoc', 'congsu', 'tau', 'lua', 'co', 'pin', 'nguoi')


def lop_a_e(mp, W=1920, H=1080):
    L, names = N.idmap(mp, (W, H), {'nha_thuong': (215, 215, 215)})
    A = N.lop(L, names, LOP); Wt = L == names.index('nuoc')
    bo = cv2.dilate((cv2.morphologyEx(Wt.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0).astype(np.uint8), np.ones((17, 17), np.uint8)) > 0
    return A | bo, L, names


def main():
    a = sys.argv[1:]; rp, mp, ap, op = a[:4]; g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    R = cv2.imread(rp); AI = cv2.resize(cv2.imread(ap), (R.shape[1], R.shape[0]), interpolation=cv2.INTER_AREA)
    A, L, names = lop_a_e(mp); Ab = cv2.dilate(A.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    G = AI.copy(); G[Ab] = R[Ab]
    bien = g('bien'); toa = json.load(open(g('toa'))) if g('toa') else []
    if bien in ('xoa_toa', 'doi_toa'):
        CT = cv2.imread(g('ct'))[:, :, ::-1].astype(int); t = next(x for x in toa if x['ten'] == g('ten'))
        m = (CT[..., 0] == t['mau'][0]) & (CT[..., 2] == 200)
        m = cv2.dilate(m.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        if bien == 'xoa_toa':
            G = cv2.inpaint(G, m.astype(np.uint8) * 255, 7, cv2.INPAINT_TELEA)
        else:
            dx = 30; M2 = np.roll(m, dx, axis=1); src = np.roll(G, dx, axis=1)
            G = cv2.inpaint(G, m.astype(np.uint8) * 255, 7, cv2.INPAINT_TELEA); G[M2] = src[M2]
    elif bien in ('thap_bia', 'thap_thap'):
        # tháp bịa = toà toa_1 render phóng chiều cao, dán ở x 1180 (giữa toa_2 và toa_3, vùng nhà thường), chân ở y 600
        t = next(x for x in toa if x['ten'] == 'toa_1'); x0, y0, x1, y1 = t['hop']; patch = R[y0:y1, x0:x1]
        k = 1.9 if bien == 'thap_bia' else 0.55; h = int((y1 - y0) * k); P = cv2.resize(patch, (x1 - x0, h), interpolation=cv2.INTER_CUBIC)
        X0, Yb = 1180, 600; G[Yb - h:Yb, X0:X0 + P.shape[1]] = P
    elif bien == 'chu':
        for (x, y, s, c) in ((300, 760, 'HOTEL', (60, 200, 255)), (1500, 700, 'BANK', (255, 255, 255)), (980, 820, 'CAFE 24', (80, 80, 255))):
            cv2.putText(G, s, (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.9, c, 2, cv2.LINE_AA)
    elif bien == 'thuyen':
        ys, xs = np.nonzero(L == names.index('nuoc')); cy, cx = int(np.median(ys)), int(np.median(xs))
        cv2.ellipse(G, (cx, cy), (40, 8), 0, 0, 360, (40, 40, 40), -1); cv2.rectangle(G, (cx - 12, cy - 14), (cx + 12, cy - 4), (230, 230, 230), -1)
    cv2.imwrite(op, G)
    print(op, 'lớp (a)-E', round(float(A.mean() * 100), 2), '% khung')


if __name__ == '__main__':
    main()
