#!/var/tmp/cine-out/segvenv/bin/python
"""KÊNH 2 · TÁCH NGƯỜI KHỎI NỀN chân dung tài sản công (Kinh thánh §4, F2 — chủ dự án duyệt 14/10/2026 22:11; phiên V4).
Chỉ TÁCH NỀN bằng mô hình phân đoạn mã nguồn mở chạy CỤC BỘ (rembg + ONNX Runtime, CPU). Không sinh hình, không sửa điểm ảnh của người:
lớp người = điểm ảnh gốc × mặt nạ alpha. Trọng số mô hình ở cache ngoài git ($K2V_CACHE/models, SHA ghi vào design/k2v/cutouts/<id>.json).

Môi trường: venv riêng /var/tmp/cine-out/segvenv (pip install "rembg[cpu]" — rembg 2.0.85 MIT, onnxruntime MIT, pymatting MIT, scikit-image BSD-3).
Mô hình (rembg releases v0.0.0; giấy phép ghi trong RIGHTS.md K2V4-SEG-*):
  birefnet-portrait  BiRefNet (MIT)          — mặc định cho chân dung: mép tóc/áo mảnh tốt nhất ở phép thử V4
  birefnet-general   BiRefNet (MIT)
  isnet-general-use  IS-Net/DIS (Apache-2.0)
  u2net              U²-Net (Apache-2.0)
  KHÔNG dùng bria-rmbg (CC BY-NC).

  cutout.py try  --img <ảnh> --id <rid> [--models birefnet-portrait,isnet-general-use,u2net]   → $K2V_CACHE/cutout/<rid>/: mặt nạ từng mô hình + tờ so mép 2×
  cutout.py make --img <ảnh> --id <rid> --model <m> [--matting] [--erode px] [--feather px] [--keep-largest]
       → design/k2v/cutouts/<rid>-mask.png (alpha 8 bit, cùng cỡ ảnh, commit) + <rid>-bg.jpg (nền đã lấp chỗ người + mờ, 640 px, commit)
         + <rid>.json (SHA ảnh/mặt nạ/trọng số, mô hình, tham số, số đo mép) + $K2V_CACHE/cutout/<rid>/edge2x.jpg (tờ kiểm mép 2×)
Số đo mép (kiểm "răng cưa"): đường viền alpha = 0,5 so với chính nó làm mượt Gauss σ = 3 px → độ lệch TB/p95 (px); dải mềm (0,05 < α < 0,95) TB (px);
số mảnh rời / lỗ thủng nhỏ. Ngưỡng tự kiểm: lệch p95 ≤ 1,5 px, dải mềm 0,8–6 px; vượt → in CẢNH BÁO để sửa mặt nạ (đổi mô hình / matting / feather).
"""
import hashlib, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CACHE = os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache')
MODELS = os.path.join(CACHE, 'models'); os.environ.setdefault('U2NET_HOME', MODELS)
OUTD = os.path.join(REPO, 'design/k2v/cutouts')
FILES = {'birefnet-portrait': 'BiRefNet-portrait-epoch_150.onnx', 'birefnet-general': 'BiRefNet-general-epoch_244.onnx',
         'isnet-general-use': 'isnet-general-use.onnx', 'u2net': 'u2net.onnx'}
LIC = {'birefnet-portrait': 'MIT (ZhengPeng7/BiRefNet)', 'birefnet-general': 'MIT (ZhengPeng7/BiRefNet)', 'isnet-general-use': 'Apache-2.0 (xuebinqin/DIS)', 'u2net': 'Apache-2.0 (xuebinqin/U-2-Net)'}


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def predict(img, model):
    from rembg import new_session, remove
    s = new_session(model)
    return np.asarray(remove(img, session=s, only_mask=True, post_process_mask=False), np.float32) / 255.0


def clean(a, keep_largest=True):
    """bỏ mảnh rời nhỏ (< 0,2 % diện tích người), lấp lỗ thủng nhỏ bên trong (< 0,1 %) — không đổi mép mảnh chính"""
    b = a > 0.5; lab, n = ndimage.label(b); area = b.sum(); info = dict(manh_roi_bo=0, lo_lap=0)
    if n > 1:
        sz = ndimage.sum(b, lab, range(1, n + 1)); big = np.argmax(sz) + 1
        for i, s in enumerate(sz, 1):
            if i != big and (keep_largest or s < 0.002 * area): a[lab == i] = 0; info['manh_roi_bo'] += 1
    hl, m = ndimage.label(~(a > 0.5))
    if m > 1:
        sz = ndimage.sum(~(a > 0.5), hl, range(1, m + 1)); border = set(np.unique(np.concatenate([hl[0], hl[-1], hl[:, 0], hl[:, -1]])))
        for i, s in enumerate(sz, 1):
            if i not in border and s < 0.001 * area: a[hl == i] = 1; info['lo_lap'] += 1
    return a, info


def edge_metrics(a):
    """độ răng cưa của đường viền α = 0,5 (so với bản làm mượt) + bề dày dải mềm"""
    from skimage import measure
    cs = measure.find_contours(a, 0.5); c = max(cs, key=len); H, W = a.shape; m = 0.03 * min(H, W)   # bỏ dải 3 % sát khung ảnh: mép cắt theo khung, không phải mép người
    sm = np.stack([ndimage.gaussian_filter1d(c[:, k], 3, mode='wrap') for k in (0, 1)], 1); inner = (c[:, 0] > m) & (c[:, 0] < H - 1 - m) & (c[:, 1] > m) & (c[:, 1] < W - 1 - m)
    d = np.hypot(*(c - sm).T)[inner]; yy, xx = np.mgrid[:H, :W]
    soft = (a > 0.05) & (a < 0.95) & (yy > m) & (yy < H - 1 - m) & (xx > m) & (xx < W - 1 - m); per = int(inner.sum())
    return dict(duong_vien_px=int(per), lech_tb_px=round(float(d.mean()), 3), lech_p95_px=round(float(np.percentile(d, 95)), 3), dai_mem_tb_px=round(float(soft.sum() / max(1, per)), 2))


def edge_sheet(img, a, out, n=6, title=''):
    """tờ kiểm mép 2×: n ô 160×160 px gốc (phóng 2×) quanh các điểm viền có độ chi tiết cao nhất (tóc, cổ áo), lớp người trên nền xám–xanh"""
    from skimage import measure
    c = max(measure.find_contours(a, 0.5), key=len); H, W = a.shape
    g = np.hypot(*np.gradient(ndimage.gaussian_filter(np.asarray(img.convert('L'), np.float32), 1.2)))
    score = [g[int(y), int(x)] for y, x in c]; idx = np.argsort(score)[::-1]; picks = []
    for i in idx:
        y, x = c[i]
        if min(y, x, H - 1 - y, W - 1 - x) < 0.03 * min(H, W): continue   # bỏ mép cắt theo khung ảnh (không phải mép người)
        if all(np.hypot(y - py, x - px) > 220 for py, px in picks): picks.append((y, x))
        if len(picks) == n: break
    rgb = np.asarray(img.convert('RGB'), np.float32); bg = np.zeros_like(rgb); bg[..., 0], bg[..., 1], bg[..., 2] = 70, 110, 130
    comp = Image.fromarray((rgb * a[..., None] + bg * (1 - a[..., None])).astype(np.uint8))
    sheet = Image.new('RGB', (n * 330 + 10, 360), (20, 20, 20)); dr = ImageDraw.Draw(sheet); dr.text((10, 4), title, fill=(230, 230, 230))
    for k, (y, x) in enumerate(picks):
        x0, y0 = int(np.clip(x - 80, 0, W - 160)), int(np.clip(y - 80, 0, H - 160))
        sheet.paste(comp.crop((x0, y0, x0 + 160, y0 + 160)).resize((320, 320), Image.NEAREST), (10 + k * 330, 30))
    sheet.save(out, quality=90); return [(round(float(x)), round(float(y))) for y, x in picks]


def matting(img, a):
    """tinh chỉnh dải mép bằng closed-form matting (pymatting) trên trimap lấy từ mặt nạ mô hình; chỉ đổi alpha trong dải ±r px quanh mép"""
    from pymatting import estimate_alpha_cf
    r = int(arg('band', 6)); fg = ndimage.binary_erosion(a > 0.95, iterations=r); bgm = ndimage.binary_erosion(a < 0.05, iterations=r)
    tri = np.full(a.shape, 0.5); tri[fg] = 1; tri[bgm] = 0
    al = estimate_alpha_cf(np.asarray(img.convert('RGB'), np.float64) / 255, tri)
    return np.clip(al, 0, 1).astype(np.float32)


def fill_bg(img, a, w=640):
    """nền cho Ken Burns 2.5D: lấp chỗ người (khuếch tán màu nền vào vùng mặt nạ đã nở) + mờ mạnh; chỉ dùng làm nền mờ/tối phía sau"""
    s = w / img.width; sm = img.convert('RGB').resize((w, round(img.height * s)), Image.LANCZOS); A = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize(sm.size, Image.BILINEAR), np.float32) / 255
    hole = ndimage.binary_dilation(A > 0.03, iterations=max(4, w // 60)); im = np.asarray(sm, np.float32).copy(); known = ~hole
    for _ in range(400):   # khuếch tán lặp (lấp Laplace): màu nền lan vào chỗ trống
        bl = ndimage.uniform_filter(im * known[..., None], (9, 9, 1)); wt = ndimage.uniform_filter(known.astype(np.float32), 9)
        fill = bl / np.maximum(wt, 1e-4)[..., None]; upd = hole & (wt > 0.02); im[upd] = fill[upd]; known = known | upd
        if known.all(): break
    return Image.fromarray(im.astype(np.uint8)).filter(ImageFilter.GaussianBlur(w / 40))


def main():
    cmd = sys.argv[1]; img = Image.open(arg('img')); rid = arg('id'); cd = os.path.join(CACHE, 'cutout', rid); os.makedirs(cd, exist_ok=True)
    if cmd == 'try':
        R = {}
        for m in (arg('models') or 'birefnet-portrait,isnet-general-use,u2net').split(','):
            a = predict(img, m); a, info = clean(a); R[m] = dict(**edge_metrics(a), **info)
            Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(cd, f'{m}-mask.png'))
            edge_sheet(img, a, os.path.join(cd, f'{m}-edge2x.jpg'), title=f'{rid} · {m} · 2x')
        print(json.dumps(R, ensure_ascii=False, indent=1)); json.dump(R, open(os.path.join(cd, 'try.json'), 'w'), indent=1); return
    m = arg('model', 'birefnet-portrait'); a = predict(img, m); a, info = clean(a, '--keep-largest' in sys.argv)
    steps = [f'model:{m}', 'clean']
    if '--matting' in sys.argv: a = np.maximum(matting(img, a) * (a > 0.02), 0) * 1.0; a, _ = clean(a); steps.append('matting-cf')
    if arg('erode'): k = float(arg('erode')); a = np.clip(ndimage.grey_erosion(a, size=(int(2 * k + 1),) * 2), 0, 1); steps.append(f'erode:{k}')
    if arg('feather'): a = ndimage.gaussian_filter(a, float(arg('feather'))); steps.append(f'feather:{arg("feather")}')
    em = edge_metrics(a); os.makedirs(OUTD, exist_ok=True)
    mp = os.path.join(OUTD, f'{rid}-mask.png'); Image.fromarray((np.clip(a, 0, 1) * 255).round().astype(np.uint8)).save(mp, optimize=True)
    bp = os.path.join(OUTD, f'{rid}-bg.jpg'); fill_bg(img, a).save(bp, quality=88)
    picks = edge_sheet(img, a, os.path.join(cd, 'edge2x.jpg'), title=f'{rid} · {" + ".join(steps)} · 2x')
    warn = [w for w, bad in (('lệch p95 > 1,5 px (răng cưa/gợn)', em['lech_p95_px'] > 1.5), ('dải mềm < 0,8 px (mép cứng, dễ răng cưa)', em['dai_mem_tb_px'] < 0.8), ('dải mềm > 6 px (mép nhoè)', em['dai_mem_tb_px'] > 6)) if bad]
    meta = dict(id=rid, img=os.path.relpath(arg('img'), REPO) if arg('img').startswith(REPO) else arg('img'), img_sha256=sha(arg('img')), size=list(img.size),
                mask=os.path.relpath(mp, REPO), mask_sha256=sha(mp), bg=os.path.relpath(bp, REPO), bg_sha256=sha(bp),
                model=m, model_file=FILES.get(m), model_sha256=sha(os.path.join(MODELS, FILES[m])) if m in FILES else None, model_license=LIC.get(m),
                runtime='rembg 2.0.85 + onnxruntime 1.31.0 (CPU, cục bộ)', steps=steps, clean=info, edge=em, edge_points_2x=picks, canh_bao=warn,
                note='Chỉ tách nền: lớp người = điểm ảnh gốc × alpha; không sinh hay vẽ lại điểm ảnh nào. Nền -bg.jpg = nền gốc lấp chỗ người + mờ (chỉ làm nền mờ/tối).')
    json.dump(meta, open(os.path.join(OUTD, f'{rid}.json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    if warn: print('CẢNH BÁO mép:', '; '.join(warn), file=sys.stderr)


if __name__ == '__main__':
    main()
