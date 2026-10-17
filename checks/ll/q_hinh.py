#!/opt/cine/bin/python
"""BC1 bố cục (EE1), MAU1 màu/chi tiết, KHOP1 đổi trình dựng (GG2) — luật khoá bản 1.12.0 (phiên K, 16/10/2026; chủ dự án duyệt luật 16/10).
Mặc định CHỈ BÁO. Định nghĩa: checks/ll/RULES-LL.md.

  q_hinh.py bc1   <mask.json> [--fps 24] [--moc f0-f1,…] [--hero f0-f1,…]       mặt nạ nội dung theo khung (render.js --maskonly)
  q_hinh.py mau1  <ảnh…> | --dir <thư mục khung không chữ> [--json ra.json]     đo như scripts/k2tl/measure_look.py (bản sao độc lập)
  q_hinh.py khop1 <thư mục khung vàng> <thư mục khung mới> [--json ra.json]     tiêu chí cấu trúc (bản sao độc lập của research/gpu/compare.py)

BC1 (a) quãng liên tục > 2,0 s mà nội dung hình học (`content_pct`) < 30 % diện tích khung, trừ khung mốc đinh → TRƯỢT; mặt nạ phải phủ MỌI khung
    của quãng xét (thiếu khung → THIẾU, không ĐẠT); (b) shot "cận hero": trung vị `hero_pct` trên các khung của shot ≥ 25 % (không có
    `hero_pct` → THIẾU).
MAU1 mỗi shot ≥ 1 khung mẫu KHÔNG CHỮ (render.js override noText), thu về 640×360 INTER_AREA, vùng giữa x/y 15–85 %: bão hoà HSV trung vị ≥ 0,35;
    colorfulness Hasler–Süsstrunk ≥ 35; chi tiết = TB |Laplace 3×3| trên Y ≥ 16; cháy sáng (kênh lớn nhất ≥ 250, CẢ khung) ≤ 1 %.
KHOP1 (a) khung vàng ghi `renderer` (chuỗi trình dựng WebGL, vd "ANGLE (… SwiftShader …)") trong `khung-vang.json` cạnh khung; (b) mọi log dựng
    của một tập cùng MỘT chuỗi renderer (không trộn trình dựng); (c) khung mới so khung vàng cùng tên, đạt CẢ BỐN: tần thấp (Gauss σ 8) lệch
    > 3 mức ≤ 3 % điểm ảnh · dịch màu TB ≤ 1 mức/kênh · PSNR ở ¼ kích thước ≥ 40 dB · SSIM (xám, Gauss 11, σ 1,5) ≥ 0,90. Báo thêm tiêu chí chặt
    (PSNR ≥ 40 dB hoặc lệch > 10/255 ≤ 1 %) để tham khảo.
    1.12.1 (chủ dự án 16–17/10, MM4) — KHAI KHUNG VÀNG (`khung-vang.json` cạnh khung vàng; `khung-moi.json` cạnh khung mới cùng dạng):
      {"renderer": "<UNMASKED_RENDERER thật của lượt dựng>", "gl": "llvmpipe" | "swiftshader" | "gpu",
       "goi_canh": {"ten": "<cảnh/gói>", "sha256": "<băm dữ liệu cảnh: tệp gói hoặc manifest>"}, "ma": "<commit mã dựng>",
       "khung": {"<tên tệp>": "<sha256 tệp>", …}, "phien": "<phiên dựng>", "ngay": "YYYY-MM-DD"}
    (a) TRƯỢT khi: không có `renderer`; `gl` không thuộc 3 lớp hoặc không khớp chuỗi renderer (llvmpipe ↔ /llvmpipe/, swiftshader ↔ /SwiftShader/,
        gpu ↔ không chứa llvmpipe/SwiftShader); thiếu `goi_canh.sha256`; một khung vàng không có SHA trong `khung` hoặc SHA lệch tệp (khung vàng bị thay).
    (b) TRƯỢT khi khung mới/log dựng của một tập có > 1 chuỗi renderer; khung mới không khai renderer → THIẾU. Lớp trình dựng mới ≠ lớp khung
        vàng → "đổi trình dựng": (c) bắt buộc.
    (d) TRƯỢT khi khung mới khai `goi_canh.sha256` khác khung vàng (dữ liệu cảnh khác → lệch hình KHÔNG do trình dựng, không so được);
        khung mới không khai → THIẾU. Khung vàng cũ (1.12.0, chỉ `renderer`) phải khai lại theo mẫu trên.
"""
import glob, hashlib, json, os, re, statistics, sys

import cv2
import numpy as np

BC_MIN, BC_RUN, HERO_MIN = 30.0, 2.0, 25.0
SAT, COL, DET, CLIP = 0.35, 35.0, 16.0, 1.0
LO_PCT, SHIFT, PSNR4, SSIM = 3.0, 1.0, 40.0, 0.90
BOX = (0.15, 0.15, 0.85, 0.85)


def _sat(name, v, thr, up=True):
    return [f'{name} {v} (ngưỡng {thr})'] if thr and abs(v - thr) <= 0.05 * abs(thr) else []


# ---------------------------------------------------------------- BC1
def bc1(M, fps=24, moc=(), hero=(), n=None):
    """M: [{f, content_pct, hero_pct?}]; moc/hero: [(f0, f1)] khung (gồm hai đầu); n: tổng số khung của đoạn (mặc định f lớn nhất + 1)"""
    by = {int(x['f']): x for x in M}; n = n or (max(by) + 1 if by else 0); loi, th = [], []
    inmoc = lambda f: any(a <= f <= b for a, b in moc)
    miss = [f for f in range(n) if f not in by]
    low = sorted(f for f, x in by.items() if x['content_pct'] < BC_MIN and not inmoc(f))
    if miss:
        th.append(f'(a) mặt nạ có {len(by)}/{n} khung — không đo được độ dài quãng liên tục; khung mẫu < {BC_MIN:.0f} % ngoài mốc đinh: '
                  + ', '.join(f"{f} ({by[f]['content_pct']} %)" for f in low[:12]))
    else:
        f = 0
        while f < n:
            if by[f]['content_pct'] < BC_MIN and not inmoc(f):
                g = f
                while g + 1 < n and by[g + 1]['content_pct'] < BC_MIN and not inmoc(g + 1): g += 1
                d = (g - f + 1) / fps
                if d > BC_RUN: loi.append(f'(a) khung {f}–{g} ({f / fps:.2f}–{(g + 1) / fps:.2f} s): nội dung < {BC_MIN:.0f} % liên tục {d:.2f} s > {BC_RUN:.0f} s '
                                          f"(thấp nhất {min(by[k]['content_pct'] for k in range(f, g + 1))} %)")
                f = g + 1
            else: f += 1
    hv = []
    for a, b in hero:
        xs = [by[f].get('hero_pct') for f in range(a, b + 1) if f in by]
        if not xs or any(x is None for x in xs): th.append(f'(b) shot cận hero khung {a}–{b}: mặt nạ không có hero_pct'); continue
        md = statistics.median(xs); hv.append(md)
        if md < HERO_MIN: loi.append(f'(b) shot cận hero khung {a}–{b}: hero trung vị {md:.1f} % < {HERO_MIN:.0f} %')
    cv = [x['content_pct'] for x in by.values()]
    sat = sum((_sat(f"(a) khung {f} nội dung", by[f]['content_pct'], BC_MIN) for f in sorted(by)), [])[:8] + sum((_sat('(b) hero trung vị', round(v, 1), HERO_MIN) for v in hv), [])
    kq = 'THIẾU' if th and not loi else None
    return dict(ok=not loi and not th, ket_qua=kq, loi=loi, thieu=th, sat_nguong=sat,
                val=f"{len(by)}/{n} khung có mặt nạ · nội dung trung vị {statistics.median(cv):.1f} % (min {min(cv)} %) · {len(low)} khung < {BC_MIN:.0f} % ngoài mốc" if cv else 'không có mặt nạ')


# ---------------------------------------------------------------- MAU1
def measure(path, box=BOX):
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    if im is None: raise SystemExit('không đọc được ' + path)
    im = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    clip = float((im.max(-1) >= 250).mean() * 100)
    x0, y0, x1, y1 = int(box[0] * 640), int(box[1] * 360), int(box[2] * 640), int(box[3] * 360); c = im[y0:y1, x0:x1]
    sat = float(np.median(cv2.cvtColor(c, cv2.COLOR_BGR2HSV)[..., 1]) / 255)
    b, g, r = [c[..., k].astype(np.float64) for k in range(3)]; rg, yb = r - g, 0.5 * (r + g) - b
    colorful = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    Y = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY).astype(np.float32); det = float(np.abs(cv2.Laplacian(Y, cv2.CV_32F, ksize=1)).mean())
    return dict(file=os.path.basename(path), sat_med=round(sat, 3), colorful=round(colorful, 1), detail=round(det, 1), clip_pct=round(clip, 2))


def mau1(items, co_chu=False):
    """items: [(shot, đường dẫn ảnh)]; co_chu=True → ảnh có lớp chữ (chỉ tham khảo, không thay được khung không chữ)"""
    rows, loi, sat = [], [], []
    for shot, p in items:
        m = measure(p); m['shot'] = shot; rows.append(m); e = []
        if m['sat_med'] < SAT: e.append(f"bão hoà {m['sat_med']} < {SAT}")
        if m['colorful'] < COL: e.append(f"colorfulness {m['colorful']} < {COL:.0f}")
        if m['detail'] < DET: e.append(f"chi tiết {m['detail']} < {DET:.0f}")
        if m['clip_pct'] > CLIP: e.append(f"cháy sáng {m['clip_pct']} % > {CLIP:.0f} %")
        if e: loi.append(f"shot {shot} ({m['file']}): " + '; '.join(e))
        sat += [f"shot {shot} {x}" for x in _sat('bão hoà', m['sat_med'], SAT) + _sat('colorfulness', m['colorful'], COL) + _sat('chi tiết', m['detail'], DET)]
    md = {k: round(statistics.median(r[k] for r in rows), 3) for k in ('sat_med', 'colorful', 'detail', 'clip_pct')} if rows else {}
    th = ['khung mẫu CÓ CHỮ — MAU1 chấm trên khung không chữ; số dưới đây chỉ tham khảo'] if co_chu else []
    return dict(ok=not loi and not th, ket_qua='THIẾU' if th and not loi else None, loi=loi, thieu=th, sat_nguong=sat, rows=rows, trung_vi=md,
                val=f"{len(rows)} khung · trung vị bão hoà {md.get('sat_med')} · colorfulness {md.get('colorful')} · chi tiết {md.get('detail')} · cháy {md.get('clip_pct')} %" if rows else 'không có khung')


# ---------------------------------------------------------------- KHOP1
def ssim_gray(a, b):
    a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.float64); b = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY).astype(np.float64)
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    m1, m2 = cv2.GaussianBlur(a, (11, 11), 1.5), cv2.GaussianBlur(b, (11, 11), 1.5)
    s1 = cv2.GaussianBlur(a * a, (11, 11), 1.5) - m1 ** 2; s2 = cv2.GaussianBlur(b * b, (11, 11), 1.5) - m2 ** 2; s12 = cv2.GaussianBlur(a * b, (11, 11), 1.5) - m1 * m2
    return float((((2 * m1 * m2 + C1) * (2 * s12 + C2)) / ((m1 ** 2 + m2 ** 2 + C1) * (s1 + s2 + C2))).mean())


def so_khung(a, b):
    """a: khung vàng, b: khung mới (RGB uint8 cùng kích thước) → số đo cấu trúc + chặt"""
    if a.shape != b.shape: return dict(error=f'kích thước khác {a.shape} {b.shape}')
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)); mse = float((d.astype(np.float64) ** 2).mean()); psnr = 99.0 if mse == 0 else 10 * np.log10(255 ** 2 / mse)
    q = lambda x: cv2.resize(x, (x.shape[1] // 4, x.shape[0] // 4), interpolation=cv2.INTER_AREA).astype(np.float64)
    m4 = float(((q(a) - q(b)) ** 2).mean()); psnr4 = 99.0 if m4 == 0 else 10 * np.log10(255 ** 2 / m4)
    sd = b.astype(np.float64) - a; lo = cv2.GaussianBlur(sd, (0, 0), 8); lo_pct = float((np.abs(lo).max(axis=2) > 3).mean() * 100)
    sh = [round(float(x), 2) for x in sd.mean(axis=(0, 1))]; ss = ssim_gray(a, b); pct = float((d.max(axis=2) > 10).mean() * 100)
    ok = lo_pct <= LO_PCT and max(abs(x) for x in sh) <= SHIFT and psnr4 >= PSNR4 and ss >= SSIM
    return dict(psnr=round(psnr, 2), psnr_q4=round(psnr4, 2), lo_pct_gt3=round(lo_pct, 3), shift_rgb=sh, ssim=round(ss, 4), pct_diff_gt10=round(pct, 3),
                dat_cau_truc=bool(ok), dat_chat=bool(psnr >= 40 or pct <= 1.0))


def _rd(p): return cv2.cvtColor(cv2.imread(p, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)


GL_LOP = {'llvmpipe': re.compile(r'llvmpipe', re.I), 'swiftshader': re.compile(r'SwiftShader', re.I)}


def lop_renderer(rs):
    """chuỗi renderer → lớp trình dựng: llvmpipe | swiftshader | gpu"""
    for k, rx in GL_LOP.items():
        if rx.search(rs or ''): return k
    return 'gpu'


def _sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def khai_vang(d, ten='khung-vang.json', kiem_sha=True):
    """đọc + kiểm khai khung vàng (1.12.1) → (khai, lỗi (a), thiếu)"""
    mf = os.path.join(d, ten); G = json.load(open(mf)) if os.path.exists(mf) else {}; loi, th = [], []
    rg = str(G.get('renderer') or '').strip(); gl = G.get('gl')
    if not rg: loi.append(f'(a) {ten} không ghi renderer')
    elif gl not in ('llvmpipe', 'swiftshader', 'gpu'): loi.append(f'(a) {ten}: gl {gl!r} không thuộc llvmpipe/swiftshader/gpu')
    elif lop_renderer(rg) != gl: loi.append(f'(a) {ten}: gl {gl} không khớp renderer {rg[:60]!r} (lớp {lop_renderer(rg)})')
    if not str((G.get('goi_canh') or {}).get('sha256') or '').strip(): loi.append(f'(a) {ten} không ghi goi_canh.sha256 (dữ liệu cảnh của khung)')
    if kiem_sha:
        K = G.get('khung') or {}
        for p in sorted(glob.glob(os.path.join(d, '*.jpg')) + glob.glob(os.path.join(d, '*.png'))):
            n = os.path.basename(p)
            if n not in K: loi.append(f'(a) {ten}: khung vàng {n} không có SHA-256 trong `khung`')
            elif K[n] != _sha(p): loi.append(f'(a) {ten}: khung vàng {n} lệch SHA khai ({K[n][:12]}… ≠ {_sha(p)[:12]}…) — khung vàng bị thay')
    return G, loi, th


def khop1(gold_dir, new_dir, logs=()):
    """gold_dir chứa khung + khung-vang.json (khai 1.12.1); new_dir chứa khung cùng tên + khung-moi.json (renderer, gl, goi_canh);
    logs: các log dựng của tập (JSON có info.renderer hoặc renderer)"""
    G, loi, th = khai_vang(gold_dir); rows = {}
    rg = str(G.get('renderer') or '').strip()
    mn = os.path.join(new_dir, 'khung-moi.json'); NW = json.load(open(mn)) if os.path.exists(mn) else {}
    rn = []
    for p in [mn] + list(logs):
        if os.path.exists(p):
            x = json.load(open(p)); v = x.get('renderer') or (x.get('info') or {}).get('renderer')
            if v: rn.append(v)
    doi = False
    if len(set(rn)) > 1: loi.append(f'(b) trộn trình dựng trong một tập: {sorted(set(rn))}')
    elif not rn: th.append('(b) khung mới/log dựng không ghi renderer')
    elif rg and lop_renderer(rn[0]) != lop_renderer(rg): doi = True
    sv, sn = str((G.get('goi_canh') or {}).get('sha256') or ''), str((NW.get('goi_canh') or {}).get('sha256') or '')
    if not sn: th.append('(d) khung-moi.json không ghi goi_canh.sha256 — không chứng minh được cùng dữ liệu cảnh với khung vàng')
    elif sv and sn != sv: loi.append(f'(d) khung mới dựng từ dữ liệu cảnh khác khung vàng (goi_canh {sn[:12]}… ≠ {sv[:12]}…) — lệch hình không do trình dựng, không so được')
    names = sorted(os.path.basename(p) for p in glob.glob(os.path.join(gold_dir, '*.jpg')) + glob.glob(os.path.join(gold_dir, '*.png')) if os.path.exists(os.path.join(new_dir, os.path.basename(p))))
    if not names: th.append('(c) không có khung chung giữa hai thư mục')
    for n in names:
        r = so_khung(_rd(os.path.join(gold_dir, n)), _rd(os.path.join(new_dir, n))); rows[n] = r
        if r.get('error'): loi.append(f'(c) {n}: {r["error"]}')
        elif not r['dat_cau_truc']:
            loi.append(f"(c) {n}: tần thấp {r['lo_pct_gt3']} % · dịch {r['shift_rgb']} · PSNR¼ {r['psnr_q4']} dB · SSIM {r['ssim']}")
    ok_rows = [r for r in rows.values() if not r.get('error')]
    sat = []
    for n, r in rows.items():
        if r.get('error'): continue
        sat += [f'{n} {x}' for x in _sat('SSIM', r['ssim'], SSIM) + _sat('PSNR¼', r['psnr_q4'], PSNR4) + _sat('tần thấp %', r['lo_pct_gt3'], LO_PCT) + _sat('dịch màu', max(abs(v) for v in r['shift_rgb']), SHIFT)]
    kq = 'THIẾU' if th and not loi else None
    val = (f"{sum(r['dat_cau_truc'] for r in ok_rows)}/{len(ok_rows)} khung đạt cấu trúc ({sum(r['dat_chat'] for r in ok_rows)} đạt chặt) · SSIM min "
           f"{min(r['ssim'] for r in ok_rows)} · PSNR¼ min {min(r['psnr_q4'] for r in ok_rows)} · vàng {G.get('gl') or lop_renderer(rg) if rg else '—'} → mới "
           f"{lop_renderer(rn[0]) if rn else '—'}{' (ĐỔI TRÌNH DỰNG: (c) bắt buộc)' if doi else ''}") if ok_rows else 'không có khung so'
    return dict(ok=not loi and not th, ket_qua=kq, loi=loi, thieu=th, sat_nguong=sat, frames=rows, val=val, doi_trinh_dung=doi)


def khop1_so(rows, renderer_vang=None, renderer_moi=()):
    """KHOP1 trên số đo đã ghi (dict tên → {psnr_q4, lo_pct_gt3, shift_rgb, ssim}) — dùng khi không có khung gốc trong repo"""
    loi, th = [], []
    if not renderer_vang: th.append('(a) khung vàng không ghi renderer')
    if len(set(renderer_moi)) > 1: loi.append(f'(b) trộn trình dựng: {sorted(set(renderer_moi))}')
    n_ok = 0; sat = []
    for n, r in rows.items():
        ok = r['lo_pct_gt3'] <= LO_PCT and max(abs(x) for x in r['shift_rgb']) <= SHIFT and r['psnr_q4'] >= PSNR4 and r['ssim'] >= SSIM; n_ok += ok
        if not ok: loi.append(f"(c) {n}: tần thấp {r['lo_pct_gt3']} % · dịch {r['shift_rgb']} · PSNR¼ {r['psnr_q4']} · SSIM {r['ssim']}")
        sat += [f'{n} {x}' for x in _sat('SSIM', r['ssim'], SSIM) + _sat('PSNR¼', r['psnr_q4'], PSNR4) + _sat('tần thấp %', r['lo_pct_gt3'], LO_PCT) + _sat('dịch màu', max(abs(v) for v in r['shift_rgb']), SHIFT)]
    return dict(ok=not loi and not th, ket_qua='THIẾU' if th and not loi else None, loi=loi, thieu=th, sat_nguong=sat, val=f'{n_ok}/{len(rows)} khung đạt cấu trúc (số đã ghi)')


def _spans(s): return [tuple(int(v) for v in x.split('-')) for x in s.split(',') if x] if s else []


def main():
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    if a[0] == 'bc1': R = bc1(json.load(open(a[1])), int(g('fps') or 24), _spans(g('moc')), _spans(g('hero')))
    elif a[0] == 'mau1':
        fs = sorted(glob.glob(os.path.join(g('dir'), '*.jpg')) + glob.glob(os.path.join(g('dir'), '*.png'))) if g('dir') else [x for x in a[1:] if not x.startswith('--')]
        R = mau1([(os.path.splitext(os.path.basename(p))[0], p) for p in fs], co_chu='--co-chu' in a)
    elif a[0] == 'khop1': R = khop1(a[1], a[2])
    else: sys.exit(__doc__)
    print(f"{a[0].upper()}: {R.get('ket_qua') or ('ĐẠT' if R['ok'] else 'TRƯỢT')} — {R['val']}"); [print('   ', x) for x in R['loi'] + R['thieu'] + R.get('sat_nguong', [])]
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
