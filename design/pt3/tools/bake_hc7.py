"""PT3 · HC7 bước 3 — NƯỚNG vân: ảnh AI của từng khúc → atlas của đúng toà (dải mặt tường) / bản ghép 'top'.
  1. kiểm trôi: tỉ lệ điểm ảnh gần đen MỚI trong vùng mặt nạ (AI thu nhỏ/dời mặt tường) > 1 % → loại khúc (dùng lần thử 2 nếu có và đạt);
  2. đều sáng + neo màu (phép toán): out × G(in)/G(out) với G = làm mờ Gauss chuẩn hoá trong mặt nạ, σ = 1 m → giữ chi tiết AI < ~1 m,
     bỏ bóng/nắng/lệch màu tầm lớn mà AI có thể nướng vào, màu tầm lớn = màu A (bảng màu thời kỳ do người đặt);
  3. ghép CỨNG theo mặt nạ (ngoài mặt nạ = albedo A), khúc chồng nhau hoà tuyến tính trên đoạn chồng;
  4. đo: đường nối (khúc, góc nhà, vòng kín), lệch màu AI thô so với A (ΔE76) từng toà, mức chỉnh đều sáng.
  /opt/cine/bin/python -I bake_hc7.py <thư mục ai_in/site> <thư mục ảnh AI> <ra atlas> <ra đo.json>"""
import sys, os, json, glob
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import exr
DI, DA, OUT, DJ = sys.argv[1:5]; os.makedirs(OUT, exist_ok=True)
man = json.load(open(os.path.join(DI, 'chunks.json'))); site = man['site']
TRY_ORDER = ['-thu2', '']
LOAI_MAT = json.load(open(os.environ['PT3_LOAI'])) if os.environ.get('PT3_LOAI') else {}   # khúc bị loại khi rà mắt (kiểm dữ kiện) → giữ A   # ưu tiên lần thử 2 nếu có (lần 1 trượt kiểm trôi), rồi lần 1

def lab(rgb_lin):
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]); xyz = rgb_lin @ M.T / np.array([0.9505, 1.0, 1.089])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116); return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)

def nblur(x, m, s):
    d = gaussian_filter(m, s) + 1e-6; return np.stack([gaussian_filter(x[..., c] * m, s) / d for c in range(x.shape[-1])], -1)

def seam(img, x, m, w=40):
    """tỉ số |chênh qua cột x| / TB |chênh giữa hai cột kề| bên trong ±w (≈ 1 = liền, > 1,5 = lộ) trên hàng thuộc mặt nạ."""
    if x < w + 1 or x > img.shape[1] - w - 1: return None
    rows = (m[:, x - 1] > 0.5) & (m[:, x] > 0.5)
    if rows.sum() < 20: return None
    L = img[rows].mean(-1); a = np.abs(L[:, x] - L[:, x - 1]).mean()
    inner = np.concatenate([np.abs(np.diff(L[:, x - w:x - 1], axis=1)).ravel(), np.abs(np.diff(L[:, x + 1:x + w], axis=1)).ravel()]).mean()
    return round(float(a / (inner + 1e-6)), 3)

def load_ai(name):
    for t in TRY_ORDER:
        p = os.path.join(DA, name + t + '.jpg')
        if os.path.exists(p): yield t, p

RES = {'site': site, 'khuc': [], 'toa': {}, 'top': {}}
def bake(A, M, chunks, ppm, key, ox='x0', oy=None):
    H, W = A.shape[:2]; base = A[..., :3].astype(np.float32); al = A[..., 3].astype(np.float32); Mm = ((M > 0.5) & (al > 0.5)).astype(np.float32)
    num = np.zeros((H, W, 3), np.float32); den = np.zeros((H, W), np.float32); raw_acc = np.zeros((H, W, 3), np.float32); s = ppm * 1.0
    # trọng số hoà: mỗi điểm thuộc khúc có TÂM gần nhất trong các khúc phủ nó; mép mềm bằng làm mờ Gauss nhãn (σ 10 px tường / 16 px sàn)
    lab_ = np.full((H, W), -1, np.int32); best = np.full((H, W), 1e9, np.float32); yy, xx = np.mgrid[0:H, 0:W]
    for i, c in enumerate(chunks):
        x0, x1 = c['x0'], c['x1']; y0, y1 = c.get('y0', 0), c.get('y1', H); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        d = np.abs(xx[y0:y1, x0:x1] - cx) if oy is None else np.maximum(np.abs(xx[y0:y1, x0:x1] - cx) / (x1 - x0), np.abs(yy[y0:y1, x0:x1] - cy) / (y1 - y0))
        sub = best[y0:y1, x0:x1]; upd = d < sub; sub[upd] = d[upd]; lab_[y0:y1, x0:x1][upd] = i
    sg = 10 if oy is None else 16; WGT = {}
    for i, c in enumerate(chunks):
        x0, x1 = c['x0'], c['x1']; y0, y1 = c.get('y0', 0), c.get('y1', H); cov = np.zeros((H, W), np.float32); cov[y0:y1, x0:x1] = 1
        WGT[c['name']] = gaussian_filter((lab_ == i).astype(np.float32), sg) * cov
    for c in chunks:
        x0, x1 = c['x0'], c['x1']; y0, y1 = c.get('y0', 0), c.get('y1', H)
        inp = base[y0:y1, x0:x1]; mk = Mm[y0:y1, x0:x1]; rec = {'khuc': c['name'], 'mask_frac': c['mask_frac']}
        chosen = None
        for t, p in load_ai(c['name']):
            out = exr.srgb2lin(np.asarray(Image.open(p).convert('RGB').resize((x1 - x0, y1 - y0), Image.LANCZOS), np.float32) / 255.0)
            sel = mk > 0.5
            def corr(o):   # tương quan cấu trúc tầm thấp (σ = 1 m) của độ sáng vào/ra trong mặt nạ — AI bịa bố cục mới → thấp
                a_ = gaussian_filter(inp.mean(-1), ppm)[sel]; b_ = gaussian_filter(o.mean(-1), ppm)[sel]
                return float(np.corrcoef(a_, b_)[0, 1]) if a_.std() > 1e-4 and b_.std() > 1e-4 else float('nan')
            def dark(o): return float(((o.mean(-1) < 0.004) & sel).sum() / max(1, sel.sum()))
            den_new = dark(out); r_ = {'lan': t or '-thu1', 'den_moi_trong_mat_na': round(den_new, 4), 'tuong_quan_cau_truc': round(corr(out), 3)}
            if c['name'] in LOAI_MAT: r_['loai_kiem_du_kien'] = LOAI_MAT[c['name']]; rec.setdefault('lan', []).append(r_); continue
            if den_new > 0.01:   # nắn khung: hộp bao hàng/cột "không đen" của ảnh ra → hộp bao vùng có bề mặt của ảnh vào (phép toán, tất định)
                ok_in = al[y0:y1, x0:x1] > 0.5; ok_out = out.mean(-1) >= 0.004
                ri = np.where(ok_in.mean(1) > 0.5)[0]; ro = np.where(ok_out.mean(1) > 0.5)[0]; ci = np.where(ok_in.mean(0) > 0.5)[0]; co_ = np.where(ok_out.mean(0) > 0.5)[0]
                if len(ri) and len(ro) and len(ci) and len(co_):
                    crop = out[ro[0]:ro[-1] + 1, co_[0]:co_[-1] + 1]
                    rs = np.asarray(Image.fromarray((exr.lin2srgb(crop) * 255 + 0.5).astype(np.uint8)).resize((ci[-1] - ci[0] + 1, ri[-1] - ri[0] + 1), Image.LANCZOS), np.float32) / 255
                    out2 = out.copy(); out2[ri[0]:ri[-1] + 1, ci[0]:ci[-1] + 1] = exr.srgb2lin(rs)
                    r_['nan_khung'] = {'hang_ra': [int(ro[0]), int(ro[-1])], 'hang_vao': [int(ri[0]), int(ri[-1])], 'cot_ra': [int(co_[0]), int(co_[-1])], 'cot_vao': [int(ci[0]), int(ci[-1])],
                                       'ti_le_doc': round((ri[-1] - ri[0] + 1) / (ro[-1] - ro[0] + 1), 3)}
                    sy = (ri[-1] - ri[0] + 1) / (ro[-1] - ro[0] + 1); sx = (ci[-1] - ci[0] + 1) / (co_[-1] - co_[0] + 1)
                    d2 = dark(out2); r_['den_sau_nan'] = round(d2, 4); r_['nan_khung']['ti_le_ngang'] = round(sx, 3)
                    if d2 <= 0.01 and 0.85 <= sy <= 1.2 and 0.85 <= sx <= 1.2: out = out2; den_new = d2   # chỉ nắn khi AI co/dãn ≤ 15–20 %
            vá = None
            if 0.01 < den_new <= 0.05:   # vá cục bộ: điểm gần đen trong mặt nạ (nới 3 px) loại khỏi mặt nạ → giữ A / khúc kề tại đó
                from scipy.ndimage import binary_dilation
                vá = binary_dilation((out.mean(-1) < 0.004) & sel, iterations=3); r_['va_cuc_bo_pct'] = round(100 * float(vá.sum()) / max(1, sel.sum()), 2)
            r_['dat'] = den_new <= 0.01 or vá is not None; rec.setdefault('lan', []).append(r_)
            if r_['dat']: chosen = (t, out, vá); break
        if chosen is None: rec['ket_qua'] = 'LOẠI (trôi) — giữ A'; RES['khuc'].append(rec); continue
        t, out, vá = chosen; rec['dung'] = t or '-thu1'
        if vá is not None: mk = mk * (~vá)
        Bi, Bo = nblur(inp, mk, s), nblur(out, mk, s); ratio = np.clip(Bi / (Bo + 1e-5), 0.4, 2.5); fixed = out * ratio
        lr = np.abs(np.log(ratio[mk > 0.5])); rec['chinh_deu_sang_med_log'] = round(float(np.median(lr)), 3); rec['chinh_p95_log'] = round(float(np.percentile(lr, 95)), 3)
        li, lo = lab(inp[mk > 0.5].mean(0)), lab(out[mk > 0.5].mean(0)); rec['dE_AI_tho_vs_A'] = round(float(np.linalg.norm(li - lo)), 2)
        rec['dE_sau_neo_vs_A'] = round(float(np.linalg.norm(li - lab(fixed[mk > 0.5].mean(0)))), 2)
        wgt = WGT[c['name']][y0:y1, x0:x1]
        w = wgt * mk; num[y0:y1, x0:x1] += fixed * w[..., None]; den[y0:y1, x0:x1] += w; raw_acc[y0:y1, x0:x1] = np.where(mk[..., None] > 0.5, out, raw_acc[y0:y1, x0:x1])
        rec['ket_qua'] = 'dùng'; RES['khuc'].append(rec)
    atlas = np.where(den[..., None] > 1e-4, num / np.maximum(den, 1e-4)[..., None], base)
    Image.fromarray((exr.lin2srgb(atlas) * 255 + 0.5).astype(np.uint8)).save(os.path.join(OUT, key + '.png'))
    cover = float(((den > 1e-4) & (Mm > 0.5)).sum() / max(1, (Mm > 0.5).sum()))
    return atlas, Mm, cover, raw_acc

mani = {'elev': {}, 'top': None}
for bid, info in man['strips'].items():
    z = np.load(os.path.join(DI, f'strip_b{bid}.npz')); A = z['A'].astype(np.float32); M = z['M'].astype(np.float32)
    ch = [c for c in man['chunks'] if c['kind'] == 'elev' and str(c.get('bid')) == bid and 'bo_qua' not in c]
    atlas, Mm, cover, raw = bake(A, M, ch, info['ppm'], f'b{bid}')
    T = {'phu_mat_na': round(cover, 4), 'so_khuc': len(ch), 'W': info['W'], 'H': info['H']}
    xs = sorted({c['x1'] for c in ch[:-1]} if len(ch) > 1 else set())
    T['noi_khuc'] = [seam(exr.lin2srgb(atlas), int((c['x1'] + ch[i + 1]['x0']) / 2), Mm) for i, c in enumerate(sorted(ch, key=lambda c: c['x0'])[:-1])]
    T['noi_goc_lien_ke'] = [seam(exr.lin2srgb(atlas), j['x'], Mm) for j in info['joins'] if j['lien_ke']]
    T['noi_goc_A'] = [seam(exr.lin2srgb(A[..., :3]), j['x'], Mm) for j in info['joins'] if j['lien_ke']]
    gs = sorted(info['groups'].values(), key=lambda g: g['x0'])
    if len(gs) > 1:   # vòng kín: cột cuối dải vs cột đầu dải (chỉ có nghĩa khi hai cạnh đầu/cuối kề nhau trên đa giác)
        e, s0 = exr.lin2srgb(atlas)[:, -1].mean(-1), exr.lin2srgb(atlas)[:, 0].mean(-1); rows = (Mm[:, -1] > 0.5) & (Mm[:, 0] > 0.5)
        T['noi_vong_chenh_TB'] = round(float(np.abs(e[rows] - s0[rows]).mean()), 4) if rows.sum() > 20 else None
    li = lab(A[..., :3][Mm > 0.5].mean(0)); T['mau_A_lab'] = [round(float(v), 1) for v in li]
    T['mau_AI_tho_lab'] = [round(float(v), 1) for v in lab(raw[Mm > 0.5].mean(0))] if (raw[Mm > 0.5].sum() > 0) else None
    T['mau_HC7_lab'] = [round(float(v), 1) for v in lab(atlas[Mm > 0.5].mean(0))]
    RES['toa'][bid] = T
    mani['elev'][bid] = {'file': f'b{bid}.png', 'W': info['W'], 'H': info['H'], 'ppm': info['ppm'], 'zmin': info['zmin'], 'groups': {g: {'x0': v['x0']} for g, v in info['groups'].items()}}
z = np.load(os.path.join(DI, 'top.npz')); A = z['A'].astype(np.float32); M = z['M'].astype(np.float32)
ch = [c for c in man['chunks'] if c['kind'] == 'top' and 'bo_qua' not in c]
atlas, Mm, cover, raw = bake(A, M, ch, man['top']['ppm'], 'top', oy=True)
RES['top'] = {'phu_mat_na': round(cover, 4), 'so_khuc': len(ch), 'W': man['top']['W'], 'H': man['top']['H']}
n_top = sum(1 for r in RES['khuc'] if r['khuc'] in [c['name'] for c in ch] and r.get('ket_qua') == 'dùng')
mani['top'] = {'file': 'top.png', 'rect': man['top']['rect'], 'W': man['top']['W'], 'H': man['top']['H']} if n_top else None   # không ô nào đạt → mái/sàn giữ vật liệu A gốc (không dùng ảnh A thu nhỏ)
json.dump(mani, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
k = [r for r in RES['khuc'] if r.get('ket_qua') == 'dùng']
RES['tom_tat'] = {'khuc_dung': len(k), 'khuc_loai': sum(1 for r in RES['khuc'] if r.get('ket_qua', '').startswith('LOẠI')),
                  'dE_AI_tho_TB': round(float(np.mean([r['dE_AI_tho_vs_A'] for r in k])), 2) if k else None, 'dE_AI_tho_max': max([r['dE_AI_tho_vs_A'] for r in k], default=None),
                  'dE_sau_neo_TB': round(float(np.mean([r['dE_sau_neo_vs_A'] for r in k])), 2) if k else None,
                  'chinh_deu_sang_med_log_TB': round(float(np.mean([r['chinh_deu_sang_med_log'] for r in k])), 3) if k else None}
json.dump(RES, open(DJ, 'w'), indent=1, ensure_ascii=False); print(json.dumps(RES['tom_tat'], ensure_ascii=False))
