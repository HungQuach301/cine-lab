"""G1b-T3 · VIỆC 7 — PHỤC CHẾ ẢNH CHỤP 1940s CÓ ĐÁP ÁN (Kinh thánh §12.3). Chỉ ảnh chụp (NARA 342-FH), không bản khắc/tranh.
Công cụ (giấy phép mã + trọng số: reports/g1b-t3/phuc-che/giay-phep/): Swin2SR classical ×2 (Apache-2.0), Real-ESRGAN x2plus (BSD-3); mốc so: bicubic.
KIỂM: mỗi ảnh 8 ô 512×512 (hạt 20261018, độ lệch chuẩn > 20) = đáp án → thu nhỏ ×0,5 (INTER_AREA) → phục chế ×2 → so đáp án:
 PSNR, SSIM, và CẠNH MỚI = tỉ lệ điểm cạnh Canny (60/150) của bản phục chế KHÔNG có cạnh đáp án trong 2 px. Cạnh mới > 5 % → LOẠI công cụ cho ảnh đó.
Qua kiểm → phục chế BẢN GỐC ở ×1 (mô hình ×2 rồi thu về cỡ gốc INTER_AREA = khử nhiễu/làm nét, không phóng; ≤ ×2 theo luật).
  <venv>/python -I phuc_che.py kiem <goc_dir> <ra_dir> <weights_dir> · phuc <goc_dir> <ra_dir> <weights_dir> <ten_anh> <cong_cu> [x0,y0,x1,y1]"""
import sys, os, json, time, hashlib
import numpy as np, cv2, torch, torch.nn as nn, torch.nn.functional as F
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim
torch.set_num_threads(2)

# ---------- Real-ESRGAN RRDBNet (kiến trúc theo bài báo ESRGAN / mã BSD-3 của xinntao, viết lại tối giản để nạp trọng số) ----------
class RDB(nn.Module):
    def __init__(s, f=64, g=32):
        super().__init__(); s.conv1 = nn.Conv2d(f, g, 3, 1, 1); s.conv2 = nn.Conv2d(f + g, g, 3, 1, 1); s.conv3 = nn.Conv2d(f + 2 * g, g, 3, 1, 1); s.conv4 = nn.Conv2d(f + 3 * g, g, 3, 1, 1); s.conv5 = nn.Conv2d(f + 4 * g, f, 3, 1, 1); s.l = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        x1 = s.l(s.conv1(x)); x2 = s.l(s.conv2(torch.cat((x, x1), 1))); x3 = s.l(s.conv3(torch.cat((x, x1, x2), 1))); x4 = s.l(s.conv4(torch.cat((x, x1, x2, x3), 1))); x5 = s.conv5(torch.cat((x, x1, x2, x3, x4), 1)); return x5 * 0.2 + x
class RRDB(nn.Module):
    def __init__(s, f=64, g=32): super().__init__(); s.rdb1 = RDB(f, g); s.rdb2 = RDB(f, g); s.rdb3 = RDB(f, g)
    def forward(s, x): return s.rdb3(s.rdb2(s.rdb1(x))) * 0.2 + x
class RRDBNet(nn.Module):
    def __init__(s, scale=2, f=64, nb=23, g=32):
        super().__init__(); s.scale = scale; cin = 3 * (4 if scale == 2 else 1)
        s.conv_first = nn.Conv2d(cin, f, 3, 1, 1); s.body = nn.Sequential(*[RRDB(f, g) for _ in range(nb)]); s.conv_body = nn.Conv2d(f, f, 3, 1, 1)
        s.conv_up1 = nn.Conv2d(f, f, 3, 1, 1); s.conv_up2 = nn.Conv2d(f, f, 3, 1, 1); s.conv_hr = nn.Conv2d(f, f, 3, 1, 1); s.conv_last = nn.Conv2d(f, 3, 3, 1, 1); s.l = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        if s.scale == 2: x = F.pixel_unshuffle(x, 2)
        fe = s.conv_first(x); fe = fe + s.conv_body(s.body(fe))
        fe = s.l(s.conv_up1(F.interpolate(fe, scale_factor=2, mode='nearest'))); fe = s.l(s.conv_up2(F.interpolate(fe, scale_factor=2, mode='nearest')))
        return s.conv_last(s.l(s.conv_hr(fe)))

def load_tools(W):
    T = {}
    net = RRDBNet(2); sd = torch.load(os.path.join(W, 'RealESRGAN_x2plus.pth'), map_location='cpu', weights_only=True); net.load_state_dict(sd.get('params_ema', sd.get('params', sd)), strict=True); net.eval()
    def esr(g):   # g: uint8 xám HxW → uint8 xám 2H×2W
        x = torch.from_numpy(np.repeat(g[None, None].astype(np.float32) / 255, 3, 1))
        with torch.no_grad(): y = net(x)[0].clamp(0, 1).mean(0).numpy()
        return (y * 255).round().astype(np.uint8)
    T['realesrgan_x2plus'] = esr
    from transformers import Swin2SRForImageSuperResolution, Swin2SRConfig
    from safetensors.torch import load_file
    cfg = Swin2SRConfig.from_json_file(os.path.join(W, 'swin2sr-x2-config.json')); m = Swin2SRForImageSuperResolution(cfg); m.load_state_dict(load_file(os.path.join(W, 'swin2sr-x2-model.safetensors')), strict=True); m.eval()
    def swin(g):
        h, w = g.shape; ph, pw = (-h) % 8, (-w) % 8; gp = np.pad(g, ((0, ph), (0, pw)), mode='reflect')
        x = torch.from_numpy(np.repeat(gp[None, None].astype(np.float32) / 255, 3, 1))
        with torch.no_grad(): y = m(pixel_values=x).reconstruction[0].clamp(0, 1).mean(0).numpy()
        return (y[:2 * h, :2 * w] * 255).round().astype(np.uint8)
    T['swin2sr_x2'] = swin
    T['bicubic'] = lambda g: cv2.resize(g, (g.shape[1] * 2, g.shape[0] * 2), interpolation=cv2.INTER_CUBIC)
    return T

def edges(g): return cv2.Canny(g, 60, 150) > 0
def new_edge(a, ref):
    ea = edges(a); er = cv2.dilate(edges(ref).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    return float((ea & ~er).sum() / max(1, ea.sum())), int(ea.sum())

def kiem(goc, out, W):
    T = load_tools(W); R = {}; os.makedirs(out, exist_ok=True); sheets = []
    for fn in sorted(os.listdir(goc)):
        if not fn.endswith('.jpg'): continue
        im = cv2.imread(os.path.join(goc, fn), cv2.IMREAD_GRAYSCALE); H, Wd = im.shape; rng = np.random.default_rng(20261018); tiles = []
        while len(tiles) < 8:
            y, x = int(rng.integers(0, H - 512)), int(rng.integers(0, Wd - 512)); t = im[y:y + 512, x:x + 512]
            if t.std() > 20: tiles.append((x, y, t))
        r = {'sha256': hashlib.sha256(open(os.path.join(goc, fn), 'rb').read()).hexdigest(), 'px': [Wd, H], 'o': [[x, y] for x, y, _ in tiles], 'cong_cu': {}}
        rows = []
        for name, f in T.items():
            P, S, N, s_t = [], [], [], 0.0
            outs = []
            for x, y, t in tiles:
                lo = cv2.resize(t, (256, 256), interpolation=cv2.INTER_AREA); t0 = time.time(); sr = f(lo); s_t += time.time() - t0
                P.append(psnr(t, sr)); S.append(ssim(t, sr)); N.append(new_edge(sr, t)[0]); outs.append(sr)
            ne = float(np.mean(N))
            r['cong_cu'][name] = {'psnr': round(float(np.mean(P)), 2), 'ssim': round(float(np.mean(S)), 4), 'canh_moi_pt': round(100 * ne, 2), 'canh_moi_max_o_pt': round(100 * float(np.max(N)), 2),
                                  'dat': bool(ne <= 0.05) if name != 'bicubic' else None, 's_moi_o': round(s_t / len(tiles), 2)}
            rows.append(outs)
        # tờ so: 2 ô đầu — gốc | bicubic | swin2sr | realesrgan (cắt 256×256 giữa ô, phóng ×1)
        for k in range(2):
            c = lambda a: a[128:384, 128:384]
            sheets.append(np.hstack([c(tiles[k][2])] + [c(rows[list(T).index(n)][k]) for n in ('bicubic', 'swin2sr_x2', 'realesrgan_x2plus')]))
        R[fn] = r; print(fn, {n: (v['psnr'], v['ssim'], v['canh_moi_pt'], v['dat']) for n, v in r['cong_cu'].items()}, flush=True)
    sh = np.vstack(sheets); cv2.putText(sh, 'goc | bicubic | Swin2SR x2 | Real-ESRGAN x2plus  (dap an: thu nho x0.5 -> x2)', (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, 255, 1)
    cv2.imwrite(os.path.join(out, 'to-so-kiem-dap-an.jpg'), sh, [cv2.IMWRITE_JPEG_QUALITY, 88])
    json.dump(R, open(os.path.join(out, 'kiem.json'), 'w'), indent=1)

def phuc(goc, out, W, fn, tool, box=None):
    T = load_tools(W); f = T[tool]; im = cv2.imread(os.path.join(goc, fn), cv2.IMREAD_GRAYSCALE)
    if box: x0, y0, x1, y1 = map(int, box.split(',')); im = im[y0:y1, x0:x1]   # vùng (CPU dùng chung: cả ảnh ≈ 3–4 h)
    H, Wd = im.shape
    acc = np.zeros((H, Wd), np.float32); wt = np.zeros((H, Wd), np.float32); TS, OV = 384, 32; t0 = time.time()
    win = np.outer(np.hanning(TS + 2)[1:-1], np.hanning(TS + 2)[1:-1]).astype(np.float32) + 1e-3
    ys = list(range(0, H - TS, TS - OV)) + [H - TS]; xs = list(range(0, Wd - TS, TS - OV)) + [Wd - TS]
    for y in ys:
        for x in xs:
            t = im[y:y + TS, x:x + TS]; sr = f(t); back = cv2.resize(sr, (TS, TS), interpolation=cv2.INTER_AREA).astype(np.float32)
            acc[y:y + TS, x:x + TS] += back * win; wt[y:y + TS, x:x + TS] += win
    res = np.clip(acc / wt, 0, 255).round().astype(np.uint8)
    ne, _ = new_edge(res, im)   # cạnh mới của bản ×1 so chính bản gốc (kiểm lần hai, trên toàn ảnh)
    os.makedirs(out, exist_ok=True); p = os.path.join(out, fn.replace('.jpg', f'_{tool}_x1' + (f'_vung{box.replace(",", "-")}' if box else '') + '.png')); cv2.imwrite(p.replace('.png', '_goc.png'), im); cv2.imwrite(p, res)
    info = {'anh': fn, 'vung': box, 'cong_cu': tool, 'giay': round(time.time() - t0, 1), 'canh_moi_toan_anh_pt': round(100 * ne, 2), 'psnr_vs_goc': round(float(psnr(im, res)), 2), 'ra': p, 'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest(), 'byte': os.path.getsize(p)}
    print(json.dumps(info)); return info

if __name__ == '__main__':
    if sys.argv[1] == 'kiem': kiem(*sys.argv[2:5])
    else: phuc(*sys.argv[2:8])
