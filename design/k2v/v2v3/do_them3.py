#!/opt/cine/bin/python -I
"""NC-V2V3 · HAI PHÉP ĐO THÊM (bổ sung bộ đo NC-V2V, không thay):
 (a) ĐỐM SÁNG MỚI BỀN ≥ 1 s (bài học NC-V2V §4.1: T4 theo diện tích bỏ sót cột lửa nhỏ ở xa):
     mỗi khung (640×360) điểm SÁNG CỤC BỘ trên đầu ra = V ≥ 0,63 VÀ V − trung vị 15×15 ≥ 40/255; bỏ mọi điểm cách điểm sáng cục bộ / lửa / pin nổi của NGUỒN ≤ 6 px;
     thành phần liên thông ≥ 3 px; nối thành VỆT qua các khung (chồng lấn sau nở 4 px); vệt dài ≥ 24 khung = đốm sáng mới bền (ghi số vệt, cỡ, có màu lửa không).
 (c) ĐỔI LOẠI VÙNG (thêm sau c4B-B, nơi AI biến eo đất thành biển mà T3 cạnh mới không thấy vì mặt nước phẳng không có cạnh):
     'màu nước' = HSV H 85–130 (OpenCV), S ≥ 40, V ≥ 30. ĐẤT→NƯỚC = % điểm lớp đất (mặt nạ ID) màu nước ở đầu ra mà nguồn không; NƯỚC→ĐẤT = % điểm lớp nước nguồn màu nước mà đầu ra không. Trung bình theo khung.
 (b) VẬT MỚI TRONG VÙNG TRỐNG (thành phần liên thông): cạnh ra cách mọi cạnh nguồn > 3 px trong vùng trời/nước/đất cách vật ≥ 6 px (đúng định nghĩa do_v2v.py),
     nở 3 px → thành phần ≥ 40 px; nối thành vệt qua khung; vệt ≥ 24 khung = VẬT MỚI BỀN (ghi hộp bao, vùng, khung đầu) → P đọc tờ so theo danh sách này.
  do_them3.py --src <nguồn.mp4> --out <ra.mp4> --id <thư mục id 1280 hoặc 640, đánh số từ --f0> --f0 0 --json <ra.json>"""
import argparse, glob, json, os, importlib.util
import cv2, numpy as np
sp = importlib.util.spec_from_file_location('d', os.path.join(os.path.dirname(os.path.abspath(__file__)), '../v2v/do_v2v.py')); d = importlib.util.module_from_spec(sp); sp.loader.exec_module(d)
W, H, LOP = d.W, d.H, d.LOP


def bright(bgr):
    v = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[..., 2].astype(np.int16)
    return (v >= 160) & (v - cv2.medianBlur(v.astype(np.uint8), 15).astype(np.int16) >= 40)


def tracks(masks, amin):
    """masks: list bool (H, W) mỗi khung → vệt (đầu, cuối, diện tích max, hộp bao gộp) bằng nối chồng lấn sau nở 4 px."""
    K = np.ones((9, 9), np.uint8); live, done = [], []
    for t, m in enumerate(masks):
        k, cc, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8); comps = []
        for j in range(1, k):
            if st[j, 4] < amin: continue
            comps.append((cv2.dilate((cc == j).astype(np.uint8), K) > 0, st[j]))
        nl = []
        for cm, s in comps:
            hit = None
            for tr in live:
                if (tr['m'] & cm).any(): hit = tr; break
            if hit: hit.update(m=cm, cuoi=t, amax=max(hit['amax'], int(s[4])), box=[min(hit['box'][0], s[0]), min(hit['box'][1], s[1]), max(hit['box'][2], s[0] + s[2]), max(hit['box'][3], s[1] + s[3])]); nl.append(hit)
            else: nl.append(dict(m=cm, dau=t, cuoi=t, amax=int(s[4]), box=[int(s[0]), int(s[1]), int(s[0] + s[2]), int(s[1] + s[3])]))
        done += [tr for tr in live if all(tr is not x for x in nl)]; live = list({id(x): x for x in nl}.values())
    done += live
    return [dict(dau=x['dau'], cuoi=x['cuoi'], dai=x['cuoi'] - x['dau'] + 1, amax=x['amax'], box=[int(v) for v in x['box']]) for x in done]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--src'); ap.add_argument('--out'); ap.add_argument('--id'); ap.add_argument('--f0', type=int, default=0); ap.add_argument('--json'); ap.add_argument('--label', default='')
    a = ap.parse_args(); S, O = d.frames(a.src), d.frames(a.out); n = min(len(S), len(O))
    idx = {int(os.path.basename(p)[:5]): p for p in glob.glob(os.path.join(a.id, '*.png'))}
    mb, mv, firecol, d2n, n2d = [], [], [], [], []
    blue = lambda h: (h[..., 0] >= 85) & (h[..., 0] <= 130) & (h[..., 1] >= 40) & (h[..., 2] >= 30)
    for t in range(n):
        s = S[t]; o, _ = d.align(s, O[t]); L = d.idmap(idx[a.f0 + t])
        srcB = cv2.dilate((bright(s) | np.isin(L, [LOP.index('lua'), LOP.index('pin')])).astype(np.uint8), np.ones((13, 13), np.uint8)) > 0
        b = bright(o) & ~srcB; mb.append(b)
        hs = cv2.cvtColor(o, cv2.COLOR_BGR2HSV); firecol.append((hs[..., 0] <= 25) & (hs[..., 1] >= 90))
        bs, bo = blue(cv2.cvtColor(s, cv2.COLOR_BGR2HSV)), blue(hs); Ld, Ln = L == LOP.index('dat'), L == LOP.index('nuoc')
        if Ld.sum() > 200: d2n.append(float((Ld & bo & ~bs).sum() / Ld.sum() * 100))
        if (Ln & bs).sum() > 200: n2d.append(float((Ln & bs & ~bo).sum() / (Ln & bs).sum() * 100))
        Es, Eo = d.canny(cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)), d.canny(cv2.cvtColor(o, cv2.COLOR_BGR2GRAY))
        objm = np.isin(L, [LOP.index(c) for c in ('nha', 'tau', 'co', 'pin', 'lua', 'nguoi', 'khac')]).astype(np.uint8)
        far = cv2.dilate(objm, np.ones((13, 13), np.uint8)) == 0
        newE = Eo & ~(cv2.dilate(Es.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0) & far & np.isin(L, [0, 1, 2])
        mv.append(cv2.dilate(newE.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0)
    tb, tv = tracks(mb, 3), tracks(mv, 40)
    for x in tb:   # màu lửa: tỉ lệ điểm cam–đỏ trong hộp ở khung giữa vệt
        t = (x['dau'] + x['cuoi']) // 2; x0, y0, x1, y1 = x['box']; x['mau_lua'] = bool(firecol[t][y0:y1, x0:x1][mb[t][y0:y1, x0:x1]].mean() > 0.5) if mb[t][y0:y1, x0:x1].any() else False
    ben_b = [x for x in tb if x['dai'] >= 24]; ben_v = [x for x in tv if x['dai'] >= 24]
    R = dict(label=a.label, n=n, dom_sang_moi=dict(so_vet=len(tb), ben_1s=len(ben_b), ben_1s_mau_lua=sum(x['mau_lua'] for x in ben_b), ds_ben=sorted(ben_b, key=lambda x: -x['amax'])[:20]),
             doi_loai_vung=dict(dat_thanh_nuoc_pct=round(float(np.mean(d2n)), 2) if d2n else None, nuoc_thanh_dat_pct=round(float(np.mean(n2d)), 2) if n2d else None),
             vat_moi_vung_trong=dict(so_vet=len(tv), ben_1s=len(ben_v), ds_ben=sorted(ben_v, key=lambda x: -x['amax'])[:30]))
    json.dump(R, open(a.json, 'w'), ensure_ascii=False, indent=1); print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != 'ds_ben'}) for k, v in R.items()}, ensure_ascii=False))


if __name__ == '__main__': main()
