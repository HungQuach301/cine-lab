"""PT nhánh C — đo độ trôi hình học A → C BẰNG MÁY (không cảm tính).
Đầu vào: khung A 1920×1080 (không chữ), ảnh C (2048×1152 → LANCZOS 1920×1080), lượt mã toà `id.exr` + lượt khoảng cách `depth.exr` của chính cảnh A.
Chỉ số mỗi ảnh:
 - canny_tinh: IoU bản đồ cạnh Canny (60/150, nở 2 px) A vs C; recall = % cạnh A có cạnh C trong 2 px; precision = % cạnh C có cạnh A trong 2 px (thấp = AI thêm chi tiết)
 - canny_tho: như trên ở 480×270 sau làm mờ (cạnh khối lớn: mép nhà, mái, chân trời) — đây là số "trôi hình khối"; ssim_canh_tho = SSIM hai bản đồ cạnh thô đã làm mờ σ=2
 - khoi_nha: mặt nạ "không phải trời" (A: khoảng cách < 20 km; C: phân vùng trời bằng loang từ mép trên theo màu + độ dốc thấp) → IoU; chân trời: lệch TB |hàng mép trời| theo cột (px)
 - mỗi toà (mã 1..8999, ≥ 3 000 px): % vùng thành trời ở C (> 50 % = BIẾN MẤT), recall cạnh thô trong vùng (< 0,5 = ĐỔI HÌNH), SSIM xám thô trong vùng;
   XUẤT HIỆN = thành phần liên thông "không phải trời" ở C nằm trong vùng trời của A, ≥ 0,1 % khung.
  python -I drift_c.py <thư mục A> <thư mục C> <thư mục id> <thư mục nền A> <ra.json> <tên…>"""
import sys, os, json, numpy as np, cv2
from PIL import Image
import OpenEXR
DA, DC, DID, DBG, OUT = sys.argv[1:6]; NAMES = sys.argv[6:]

def exr(p):
    a = list(OpenEXR.File(p).channels().values())[0].pixels; return a[..., 0] if a.ndim == 3 else a

def ssim(a, b):
    a = a.astype(np.float64); b = b.astype(np.float64); C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    mu1, mu2 = cv2.GaussianBlur(a, (11, 11), 1.5), cv2.GaussianBlur(b, (11, 11), 1.5)
    s1 = cv2.GaussianBlur(a * a, (11, 11), 1.5) - mu1 ** 2; s2 = cv2.GaussianBlur(b * b, (11, 11), 1.5) - mu2 ** 2; s12 = cv2.GaussianBlur(a * b, (11, 11), 1.5) - mu1 * mu2
    return float((((2 * mu1 * mu2 + C1) * (2 * s12 + C2)) / ((mu1 ** 2 + mu2 ** 2 + C1) * (s1 + s2 + C2))).mean())

def edges(g, lo=60, hi=150): return cv2.Canny(cv2.GaussianBlur(g, (3, 3), 0), lo, hi) > 0

def edge_stats(ea, ec, tol=2):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * tol + 1, 2 * tol + 1))
    da = cv2.dilate(ea.astype(np.uint8), k) > 0; dc = cv2.dilate(ec.astype(np.uint8), k) > 0
    return dict(iou=round(float((da & dc).sum() / max(1, (da | dc).sum())), 3), recall=round(float((ea & dc).sum() / max(1, ea.sum())), 3),
                precision=round(float((ec & da).sum() / max(1, ec.sum())), 3), mat_do_A=round(float(ea.mean()), 4), mat_do_C=round(float(ec.mean()), 4))

def sky_mask(rgb):
    """trời = loang từ hàng trên cùng qua điểm ảnh có độ dốc thấp và màu gần màu trời ở 3 % hàng trên (Lab)."""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32); g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    grad = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    H, W = g.shape; ref = np.median(lab[: max(3, H // 33)].reshape(-1, 3), 0)
    # cho phép trời chuyển dần xuống chân trời: so với màu trung vị của chính hàng (nếu hàng đó phần lớn là trời) hoặc màu tham chiếu
    cand = (grad < 18).astype(np.uint8)
    dist = np.linalg.norm(lab - ref, axis=-1)
    rowmed = np.array([np.median(lab[y][cand[y] > 0], 0) if cand[y].sum() > W * 0.3 else ref for y in range(H)])
    dist2 = np.linalg.norm(lab - rowmed[:, None, :], axis=-1)
    ok = cand & (((dist < 28) | (dist2 < 10)).astype(np.uint8))
    n, lab_cc = cv2.connectedComponents(ok)
    top = set(np.unique(lab_cc[0][ok[0] > 0])) - {0}
    return np.isin(lab_cc, list(top)) if top else np.zeros_like(ok, bool)

def skyline(nonsky):
    H, W = nonsky.shape; rows = np.where(nonsky.any(0), nonsky.argmax(0), H); return rows

res = {}
for name in NAMES:
    ep = int(name.split('-')[0])
    A = np.asarray(Image.open(os.path.join(DA, f'{name}-A-notext.jpg')).convert('RGB'))
    C = np.asarray(Image.open(os.path.join(DC, f'{name}.png')).convert('RGB').resize((A.shape[1], A.shape[0]), Image.LANCZOS))
    ID = np.round(exr(os.path.join(DID, str(ep), 'id.exr'))).astype(int); DEP = exr(os.path.join(DBG, f'{ep}A', 'depth.exr'))
    gA, gC = cv2.cvtColor(A, cv2.COLOR_RGB2GRAY), cv2.cvtColor(C, cv2.COLOR_RGB2GRAY)
    r = {'canny_tinh': edge_stats(edges(gA), edges(gC))}
    sA, sC = cv2.resize(cv2.GaussianBlur(gA, (0, 0), 2), (480, 270), interpolation=cv2.INTER_AREA), cv2.resize(cv2.GaussianBlur(gC, (0, 0), 2), (480, 270), interpolation=cv2.INTER_AREA)
    eA, eC = edges(sA, 30, 80), edges(sC, 30, 80)
    r['canny_tho'] = edge_stats(eA, eC, tol=1)
    r['ssim_canh_tho'] = round(ssim(cv2.GaussianBlur(eA.astype(np.float32) * 255, (0, 0), 2), cv2.GaussianBlur(eC.astype(np.float32) * 255, (0, 0), 2)), 3)
    r['ssim_xam_tho'] = round(ssim(sA, sC), 3)
    skyA = DEP > 20000; skyC = sky_mask(C); skyA_seg = sky_mask(A)
    nsA, nsC = ~skyA, ~skyC
    # cùng bộ phân vùng cho A và C; chỉ tin cột mà phân vùng A khớp độ sâu thật (≤ 3 px)
    lA_true, lA_seg, lC_seg = skyline(nsA).astype(float), skyline(~skyA_seg).astype(float), skyline(nsC).astype(float)
    ok = np.abs(lA_true - lA_seg) <= 3
    r['khoi_nha'] = {'iou_khong_troi_segA_vs_segC': round(float((~skyA_seg & nsC).sum() / max(1, (~skyA_seg | nsC).sum())), 4),
                     'do_tin_phan_vung_A_vs_do_sau': round(float((~skyA_seg & nsA).sum() / max(1, (~skyA_seg | nsA).sum())), 4),
                     'cot_tin_duoc_pct': round(float(ok.mean() * 100), 1),
                     'lech_chan_troi_px_TB': round(float(np.abs(lA_seg - lC_seg)[ok].mean()), 2) if ok.any() else None,
                     'lech_chan_troi_px_p95': round(float(np.percentile(np.abs(lA_seg - lC_seg)[ok], 95)), 1) if ok.any() else None}
    r['dem_toi'] = bool(gA.mean() < 40)
    toa = []; small = lambda m: cv2.resize(m.astype(np.uint8), (480, 270), interpolation=cv2.INTER_NEAREST) > 0
    for b in np.unique(ID):
        if not (1 <= b < 9000): continue
        m = ID == b
        if m.sum() < 800: continue
        ms = small(m); rec = float((eA & ms & (cv2.dilate(eC.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0)).sum() / max(1, (eA & ms).sum()))
        sky_frac = float(((skyC & ~skyA_seg) & m).sum() / m.sum())   # chỉ tính phần A KHÔNG bị phân vùng nhầm là trời
        ys, xs = np.where(ms); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        ss = ssim(sA[y0:y1, x0:x1], sC[y0:y1, x0:x1]) if (y1 - y0 > 12 and x1 - x0 > 12) else None
        st = 'BIẾN MẤT' if sky_frac > 0.5 else ('ĐỔI HÌNH' if rec < 0.5 else 'giữ')
        toa.append({'ma': int(b), 'px': int(m.sum()), 'troi_o_C': round(sky_frac, 3), 'recall_canh_tho': round(rec, 3), 'ssim_xam': None if ss is None else round(ss, 3), 'ket_luan': st})
    r['toa'] = toa
    # xuất hiện: không-trời ở C trong vùng trời của A
    app = (nsC & skyA & skyA_seg).astype(np.uint8); n, cc, stats, _ = cv2.connectedComponentsWithStats(app)   # trời thật ở A (độ sâu) và phân vùng A cũng là trời
    big = [int(s[4]) for s in stats[1:] if s[4] >= 0.001 * app.size]
    r['xuat_hien'] = {'so_vung': len(big), 'px': big[:10], 'tong_pct': round(float(app.mean() * 100), 3)}
    r['dem'] = {k: sum(1 for t in toa if t['ket_luan'] == k) for k in ('giữ', 'ĐỔI HÌNH', 'BIẾN MẤT')}
    res[name] = r
    print(name, 'tinh', r['canny_tinh']['iou'], r['canny_tinh']['recall'], r['canny_tinh']['precision'], '| tho', r['canny_tho']['iou'], r['canny_tho']['recall'], r['ssim_canh_tho'],
          '| khong-troi IoU', r['khoi_nha']['iou_khong_troi_segA_vs_segC'], 'tin', r['khoi_nha']['do_tin_phan_vung_A_vs_do_sau'], r['khoi_nha']['cot_tin_duoc_pct'], 'chan troi', r['khoi_nha']['lech_chan_troi_px_TB'], '| toa', r['dem'], 'xuat hien', r['xuat_hien']['so_vung'])
# nhất quán giữa các tấm C cùng mốc (điểm yếu "nhà đổi hình giữa hai tấm" của đối thủ): so cạnh thô C_i vs C_j trong vùng nhà A, đối chứng A_i vs A_j
cons = {}
for ep in (1782, 1943):
    ns = [n for n in NAMES if n.startswith(str(ep))]
    ID = np.round(exr(os.path.join(DID, str(ep), 'id.exr'))).astype(int); bm = cv2.resize(((ID >= 1) & (ID < 9000)).astype(np.uint8), (480, 270), interpolation=cv2.INTER_NEAREST) > 0
    def ecoarse(p, rs=False):
        im = Image.open(p).convert('L');
        if rs: im = im.resize((1920, 1080), Image.LANCZOS)
        g = np.asarray(im); return edges(cv2.resize(cv2.GaussianBlur(g, (0, 0), 2), (480, 270), interpolation=cv2.INTER_AREA), 30, 80)
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            a_i, a_j = ecoarse(os.path.join(DA, f'{ns[i]}-A-notext.jpg')), ecoarse(os.path.join(DA, f'{ns[j]}-A-notext.jpg'))
            c_i, c_j = ecoarse(os.path.join(DC, f'{ns[i]}.png'), True), ecoarse(os.path.join(DC, f'{ns[j]}.png'), True)
            cons[f'{ns[i]}~{ns[j]}'] = {'A_iou_vung_nha': edge_stats(a_i & bm, a_j & bm, 1)['iou'], 'C_iou_vung_nha': edge_stats(c_i & bm, c_j & bm, 1)['iou']}
res['_nhat_quan_giua_tam'] = cons; print(json.dumps(cons, ensure_ascii=False))
# cùng vật ở 1782 và 1943: Line Wall + đồi bên kia vịnh có ở cả hai mốc (cùng máy) → so đường chân trời đồi giữa C1782 và C1943 (giờ giữa), đối chứng A
def hill_line(rgb, cols):
    ns = ~sky_mask(rgb); return skyline(ns)[cols]
ID = np.round(exr(os.path.join(DID, '1782', 'id.exr'))).astype(int); ID2 = np.round(exr(os.path.join(DID, '1943', 'id.exr'))).astype(int)
cols = np.where(((ID == 9600).any(0)) & ((ID2 == 9600).any(0)) & ~(((ID >= 1) & (ID < 9000)) | ((ID2 >= 1) & (ID2 < 9000))).any(0))[0]
if len(cols) and '1782-giua' in NAMES and '1943-giua' in NAMES:
    la = hill_line(np.asarray(Image.open(os.path.join(DA, '1782-giua-A-notext.jpg')).convert('RGB')), cols).astype(float)
    lb = hill_line(np.asarray(Image.open(os.path.join(DA, '1943-giua-A-notext.jpg')).convert('RGB')), cols).astype(float)
    ca = hill_line(np.asarray(Image.open(os.path.join(DC, '1782-giua.png')).convert('RGB').resize((1920, 1080), Image.LANCZOS)), cols).astype(float)
    cb = hill_line(np.asarray(Image.open(os.path.join(DC, '1943-giua.png')).convert('RGB').resize((1920, 1080), Image.LANCZOS)), cols).astype(float)
    d1 = exr(os.path.join(DBG, '1782A', 'depth.exr')); d2 = exr(os.path.join(DBG, '1943A', 'depth.exr'))
    t1, t2 = skyline(~(d1 > 20000))[cols].astype(float), skyline(~(d2 > 20000))[cols].astype(float)
    okc = (np.abs(la - t1) <= 3) & (np.abs(lb - t2) <= 3)
    la, lb, ca, cb = la[okc], lb[okc], ca[okc], cb[okc]
    res['_cung_vat_hai_moc'] = {'cot_tin_duoc': int(okc.sum()), 'A_that_1782_vs_1943_px_TB': round(float(np.abs(t1 - t2)[okc].mean()), 2) if okc.any() else None,'vat': 'đường đồi bên kia vịnh (mã 9600), cột không bị nhà che ở cả hai mốc', 'so_cot': int(len(cols)),
                                'A1782_vs_A1943_px_TB': round(float(np.abs(la - lb).mean()), 2), 'C1782_vs_C1943_px_TB': round(float(np.abs(ca - cb).mean()), 2),
                                'C1782_vs_A_px_TB': round(float(np.abs(ca - la).mean()), 2), 'C1943_vs_A_px_TB': round(float(np.abs(cb - lb).mean()), 2)}
    print(res['_cung_vat_hai_moc'])
json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False)
