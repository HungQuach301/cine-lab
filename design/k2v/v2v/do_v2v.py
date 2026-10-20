#!/opt/cine/bin/python -I
"""NC-V2V · ĐO BẰNG MÁY đầu ra Omni so với clip nguồn do ta dựng (không tin mắt). Mọi số đo ở 640×360 (INTER_AREA), khung theo chỉ số 24 fps.

  do_v2v.py --src <nguồn.mp4> --out <ra.mp4> --id <thư mục mặt nạ id/*.png, 640×360, đánh số theo khung nguồn> --f0 <khung đầu của mặt nạ> --json <ra.json>

Căn khung: mỗi khung, ECC affine trên độ lớn gradient ra → nguồn (thu 1/2), loại nghiệm phi lý, chọn đơn vị/ECC theo NCC gradient; đo trên ảnh ra đã nắn.
(i)  GIỮ DỮ KIỆN — cạnh Canny (ngưỡng theo trung vị, cùng tham số cho nguồn và ra) trong vùng từng loại của mặt nạ ID (nở 2 px):
       F1 cạnh (dung sai 2 px) = 2PR/(P+R), IoU cạnh = |nở(Es) ∩ nở(Eo)| / |nở(Es) ∪ nở(Eo)| trong vùng;
       đếm vật: thành phần liên thông của tàu / cờ / pin nổi (≥ AMIN px); vật GIỮ khi hồi cạnh trong hộp ≥ 0,5 (cờ: thêm ΔE76 TB ≤ 25 vì màu cờ là dữ kiện);
       LỬA MỚI: % khung là điểm cam–vàng sáng cách mọi lửa/pin nổi/điểm cam sáng của nguồn > 6 px, số cụm ≥ 6 px;
       cạnh MỚI trong vùng TRỐNG (trời / nước / đất, cách vật ≥ 6 px): % diện tích vùng có cạnh ra cách mọi cạnh nguồn > 3 px; cụm cạnh mới ≥ 40 px (nở 3) = "vật lạ".
(ii) NHẤP NHÁY — ảnh xám thu 160×90 (khối 4×4, triệt nhiễu nén); vùng tĩnh = điểm có |nguồn_t − nguồn_t−1| < 0,5/255; so TB |ra_t − ra_t−1| với nguồn trên vùng đó (kèm bản đối chứng không AI).
(iv) bão hoà trung vị HSV / colorfulness Hasler–Süsstrunk / chi tiết |Laplace| — đúng công thức scripts/k2tl/measure_look.py (V5b-1b, dùng ở V6), vùng giữa 15–85 %.
(v)  THỜI GIAN / MÁY — luồng quang học Farnebäck toàn khung (trung vị dx, dy mỗi cặp khung) nguồn ↔ ra: RMS sai khác (px/khung), tương quan;
     lệch thời gian = độ dời k ∈ [−12, 12] khung làm cực đại NCC độ lớn gradient (thu 1/4) giữa ra_t đã căn và nguồn_{t+k}, trung vị theo t (kèm độ nhọn đỉnh: gần 0 = không xác định).
"""
import argparse, glob, json, os, sys
import cv2, numpy as np

W, H = 640, 360
NAMES = {(40, 80, 200): 'troi', (0, 170, 190): 'nuoc', (140, 105, 60): 'dat', (235, 235, 235): 'nha', (255, 0, 0): 'tau', (255, 255, 0): 'co', (255, 0, 255): 'pin', (255, 128, 0): 'lua', (0, 255, 0): 'nguoi', (128, 128, 128): 'khac'}
LOP = ['troi', 'nuoc', 'dat', 'nha', 'tau', 'co', 'pin', 'lua', 'nguoi', 'khac']
AMIN = {'tau': 20, 'co': 4, 'pin': 12}


def frames(path):
    cap = cv2.VideoCapture(path); out = []
    while True:
        ok, f = cap.read()
        if not ok: break
        out.append(cv2.resize(f, (W, H), interpolation=cv2.INTER_AREA))
    return out


def idmap(png):
    im = cv2.cvtColor(cv2.imread(png, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    if im.shape[1] != W: im = cv2.resize(im, (W, H), interpolation=cv2.INTER_NEAREST)
    lab = np.full(im.shape[:2], 9, np.uint8)
    for rgb, n in NAMES.items(): lab[np.all(im == rgb, -1)] = LOP.index(n)
    return lab


def canny(g):
    v = np.median(g); return cv2.Canny(cv2.GaussianBlur(g, (3, 3), 0), int(max(10, 0.66 * v * 0.5)), int(min(255, max(30, 1.33 * v * 0.5)))) > 0


def look(bgr):
    x0, y0, x1, y1 = int(.15 * W), int(.15 * H), int(.85 * W), int(.85 * H); c = bgr[y0:y1, x0:x1]
    sat = float(np.median(cv2.cvtColor(c, cv2.COLOR_BGR2HSV)[..., 1]) / 255)
    b, g, r = [c[..., k].astype(np.float64) for k in range(3)]; rg, yb = r - g, 0.5 * (r + g) - b
    col = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    det = float(np.abs(cv2.Laplacian(cv2.cvtColor(c, cv2.COLOR_BGR2GRAY).astype(np.float32), cv2.CV_32F, ksize=1)).mean())
    return sat, col, det


def _gm(bgr, w, h):
    g = cv2.GaussianBlur(cv2.cvtColor(cv2.resize(bgr, (w, h), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 1.2)
    m = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1)); return m / (m.mean() + 1e-6)


def _ncc(a, b):
    a = a - a.mean(); b = b - b.mean(); return float((a * b).sum() / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6))


def align(src, out):
    """căn ra → nguồn: ECC affine trên ĐỘ LỚN GRADIENT (ít nhạy với đổi sáng/màu của Omni), thu 1/2; loại nghiệm phi lý
    (tỉ lệ ngoài 0,85–1,18, cắt xiên > 0,08, dịch > 80 px @640) rồi chọn giữa đơn vị và ECC theo NCC gradient sau nắn."""
    w, h = W // 2, H // 2; gs, go = _gm(src, w, h), _gm(out, w, h); M = np.eye(2, 3, dtype=np.float32); best = (np.eye(2, 3, dtype=np.float32), _ncc(gs, go))
    try:
        _, M = cv2.findTransformECC(gs, go, M, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5), None, 5)
        sx, sy, sh = np.hypot(M[0, 0], M[1, 0]), np.hypot(M[0, 1], M[1, 1]), abs(M[0, 1] + M[1, 0])
        if 0.85 < sx < 1.18 and 0.85 < sy < 1.18 and sh < 0.08 and np.hypot(M[0, 2], M[1, 2]) * 2 < 80:
            sc = _ncc(gs, cv2.warpAffine(go, M, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE))
            if sc > best[1]: best = (M, sc)
    except cv2.error: pass
    M2 = best[0].copy(); M2[:, 2] *= 2
    return cv2.warpAffine(out, M2, (W, H), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE), M2


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--src', required=True); ap.add_argument('--out', required=True); ap.add_argument('--id', required=True)
    ap.add_argument('--f0', type=int, default=0); ap.add_argument('--json', required=True); ap.add_argument('--step', type=int, default=2); ap.add_argument('--label', default='')
    a = ap.parse_args()
    S, O = frames(a.src), frames(a.out); n = min(len(S), len(O))
    ids = sorted(glob.glob(os.path.join(a.id, '*.png')))
    idx = {int(os.path.basename(p)[:5]): p for p in ids}
    K3 = np.ones((3, 3), np.uint8); K5 = np.ones((5, 5), np.uint8)
    per, objs, empty, A = {c: [] for c in ('tau', 'co', 'pin', 'nha', 'lua', 'dat', 'nuoc', 'troi')}, {c: [0, 0] for c in AMIN}, {c: [] for c in ('troi', 'nuoc', 'dat')}, []
    blobs, aff, looks_s, looks_o, fires = [], [], [], [], []
    for t in range(0, n, a.step):
        p = idx.get(a.f0 + t)
        if p is None: continue
        L = idmap(p); s = S[t]; o, M = align(s, O[t]); aff.append(M.ravel().tolist())
        gs, go = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY), cv2.cvtColor(o, cv2.COLOR_BGR2GRAY)
        Es, Eo = canny(gs), canny(go); Ds, Do = cv2.dilate(Es.astype(np.uint8), K5) > 0, cv2.dilate(Eo.astype(np.uint8), K5) > 0
        labS, labO = cv2.cvtColor(s, cv2.COLOR_BGR2LAB).astype(np.float32), cv2.cvtColor(o, cv2.COLOR_BGR2LAB).astype(np.float32)
        labS[..., 0] *= 100 / 255; labO[..., 0] *= 100 / 255; labS[..., 1:] -= 128; labO[..., 1:] -= 128
        dE = np.sqrt(((labS - labO) ** 2).sum(-1))
        for c in per:
            R = cv2.dilate((L == LOP.index(c)).astype(np.uint8), K5) > 0
            if R.sum() < 30: continue
            es, eo = (Es & R).sum(), (Eo & R).sum()
            rec = (Es & Do & R).sum() / es if es else np.nan; pre = (Eo & Ds & R).sum() / eo if eo else np.nan
            f1 = 2 * rec * pre / (rec + pre) if rec + pre > 0 else 0.0
            iou = (Ds & Do & R).sum() / max(1, ((Ds | Do) & R).sum())
            per[c].append((f1, iou, float(dE[L == LOP.index(c)].mean()), int((L == LOP.index(c)).sum())))
        for c, amin in AMIN.items():
            m = (L == LOP.index(c)).astype(np.uint8); k, cc, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
            for j in range(1, k):
                if st[j, 4] < amin: continue
                x, y, w, h = st[j, :4]; pad = 2; X0, Y0, X1, Y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
                es = Es[Y0:Y1, X0:X1].sum(); rec = (Es & Do)[Y0:Y1, X0:X1].sum() / es if es else 1.0; de = float(dE[cc == j].mean())
                objs[c][0] += 1; objs[c][1] += int(rec >= 0.5 and (c != 'co' or de <= 25))   # cờ: màu mang dữ kiện → thêm ΔE ≤ 25; tàu/pin nổi: chỉ hình (ánh sáng được phép đổi)
        objm = np.isin(L, [LOP.index(c) for c in ('nha', 'tau', 'co', 'pin', 'lua', 'nguoi', 'khac')]).astype(np.uint8)
        far = cv2.dilate(objm, np.ones((13, 13), np.uint8)) == 0
        newE = Eo & ~(cv2.dilate(Es.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0)
        for c in empty:
            R = (L == LOP.index(c)) & far; R = cv2.erode(R.astype(np.uint8), K3) > 0
            if R.sum() < 200: continue
            empty[c].append((float((newE & R).sum() / R.sum() * 100), int(R.sum())))
        NB = cv2.dilate((newE & far & np.isin(L, [0, 1, 2])).astype(np.uint8), K3)
        k, _, st, _ = cv2.connectedComponentsWithStats(NB, connectivity=8); blobs.append(int((st[1:, 4] >= 40).sum()) if k > 1 else 0)
        # LỬA/NGUỒN SÁNG MỚI: điểm cam–vàng sáng (HSV: H 5–40°, S ≥ 0,45, V ≥ 0,63) trên đầu ra, cách vùng lửa/pin nổi/lửa-sáng của NGUỒN > 6 px
        hs, ho = cv2.cvtColor(s, cv2.COLOR_BGR2HSV), cv2.cvtColor(o, cv2.COLOR_BGR2HSV)
        fire = lambda h: (h[..., 0] >= 3) & (h[..., 0] <= 20) & (h[..., 1] >= 115) & (h[..., 2] >= 160)
        srcF = cv2.dilate((fire(hs) | np.isin(L, [LOP.index('lua'), LOP.index('pin')])).astype(np.uint8), np.ones((13, 13), np.uint8)) > 0
        nf = fire(ho) & ~srcF; k, _, st, _ = cv2.connectedComponentsWithStats(nf.astype(np.uint8), connectivity=8)
        fires.append((float(nf.mean() * 100), int((st[1:, 4] >= 6).sum()) if k > 1 else 0))
        looks_s.append(look(s)); looks_o.append(look(o))
    # (ii) nhấp nháy + (v) luồng quang học
    fl_s, fl_o, fs_, fo_ = [], [], [], []
    G = lambda im: cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gS = [G(x).astype(np.float32) for x in S[:n]]; gO = [G(x).astype(np.float32) for x in O[:n]]
    lo = lambda g: cv2.resize(g, (160, 90), interpolation=cv2.INTER_AREA)   # thu 160×90: trung bình khối 4×4 → triệt nhiễu nén, giữ nhấp nháy mảng
    lS, lO = [lo(x) for x in gS], [lo(x) for x in gO]
    for t in range(1, n):
        ds, do = np.abs(lS[t] - lS[t - 1]), np.abs(lO[t] - lO[t - 1]); st = ds < 0.5
        if st.sum() > 500: fl_s.append(float(ds[st].mean())); fl_o.append(float(do[st].mean()))
        if t % 2 == 0:
            a1 = cv2.calcOpticalFlowFarneback(gS[t - 1].astype(np.uint8), gS[t].astype(np.uint8), None, 0.5, 3, 21, 3, 5, 1.1, 0)
            a2 = cv2.calcOpticalFlowFarneback(gO[t - 1].astype(np.uint8), gO[t].astype(np.uint8), None, 0.5, 3, 21, 3, 5, 1.1, 0)
            fs_.append(np.median(a1.reshape(-1, 2), 0)); fo_.append(np.median(a2.reshape(-1, 2), 0))
    fs_, fo_ = np.array(fs_), np.array(fo_)
    # lệch thời gian: ra_t nắn theo căn ECC của chính khung t, so tương quan chuẩn hoá (NCC) độ lớn gradient (thu 1/4) với nguồn_{t+k}, k ∈ [−12, 12]
    def gm(g):
        g = cv2.resize(g, (W // 4, H // 4), interpolation=cv2.INTER_AREA); m = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1)); m -= m.mean(); return m / (np.linalg.norm(m) + 1e-6)
    gmS = [gm(x) for x in gS]; lag, peak = [], []
    for t in range(12, n - 12, 6):
        o, _ = align(S[t], O[t]); go = gm(cv2.cvtColor(o, cv2.COLOR_BGR2GRAY).astype(np.float32))
        e = [float((go * gmS[t + k]).sum()) for k in range(-12, 13)]; lag.append(int(np.argmax(e)) - 12); peak.append(max(e) - float(np.median(e)))
    corr = lambda x, y: float(np.corrcoef(x, y)[0, 1]) if len(x) > 2 and np.std(x) > 1e-6 and np.std(y) > 1e-6 else None
    md = lambda v: float(np.nanmedian(v)) if len(v) else None
    R = dict(label=a.label, src=a.src, out=a.out, n_src=len(S), n_out=len(O), step=a.step,
             giu=dict({c: dict(f1_canh=round(md([x[0] for x in v]), 3), iou_canh=round(md([x[1] for x in v]), 3), dE76=round(md([x[2] for x in v]), 1), px_tb=int(np.mean([x[3] for x in v])), n=len(v)) for c, v in per.items() if v}),
             dem=dict({c: dict(truoc=v[0], giu=v[1], ti_le=round(v[1] / v[0], 3) if v[0] else None) for c, v in objs.items()}),
             canh_moi_pct=dict({c: dict(tb=round(float(np.mean([x[0] for x in v])), 2), p90=round(float(np.percentile([x[0] for x in v], 90)), 2), max=round(float(np.max([x[0] for x in v])), 2)) for c, v in empty.items() if v}),
             vat_la_tb=round(float(np.mean(blobs)), 2) if blobs else None, vat_la_max=int(max(blobs)) if blobs else None,
             lua_moi=dict(pct_tb=round(float(np.mean([x[0] for x in fires])), 3), pct_max=round(float(np.max([x[0] for x in fires])), 3), cum_tb=round(float(np.mean([x[1] for x in fires])), 2), cum_max=int(max(x[1] for x in fires))) if fires else None,
             nhap_nhay=dict(nguon=round(float(np.mean(fl_s)), 3) if fl_s else None, ra=round(float(np.mean(fl_o)), 3) if fl_o else None, ti_so=round(float(np.mean(fl_o) / max(1e-3, np.mean(fl_s))), 2) if fl_s else None),
             look=dict(nguon=dict(zip(('sat_med', 'colorful', 'detail'), [round(float(np.median([x[i] for x in looks_s])), 3) for i in range(3)])), ra=dict(zip(('sat_med', 'colorful', 'detail'), [round(float(np.median([x[i] for x in looks_o])), 3) for i in range(3)]))),
             may=dict(luong_nguon_tb=np.round(fs_.mean(0), 3).tolist() if len(fs_) else None, luong_ra_tb=np.round(fo_.mean(0), 3).tolist() if len(fo_) else None,
                      rms_px_khung=round(float(np.sqrt(((fs_ - fo_) ** 2).sum(1).mean())), 3) if len(fs_) else None, corr_dx=corr(fs_[:, 0], fo_[:, 0]) if len(fs_) else None, corr_dy=corr(fs_[:, 1], fo_[:, 1]) if len(fs_) else None,
                      lech_khung_trung_vi=float(np.median(lag)) if lag else None, lech_khung_max=int(np.max(np.abs(lag))) if lag else None, lech_do_nhon=round(float(np.median(peak)), 4) if peak else None,
                      can_khung_dich_tb_px=round(float(np.mean([np.hypot(m[2], m[5]) for m in aff])), 2) if aff else None, can_khung_ti_le_tb=round(float(np.mean([np.hypot(m[0], m[3]) for m in aff])), 4) if aff else None))
    json.dump(R, open(a.json, 'w'), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False))


if __name__ == '__main__': main()
