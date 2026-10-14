#!/opt/cine/bin/python
"""KÊNH 2 · thử cấu hình render nhanh (V2b, lệnh chủ dự án 14/10/2026 bước 6): SPP2 / lưới 1/2 khi máy > 300 km / texture 4096 khi > 500 km,
so với chuẩn SPP4 không LOD trên CÙNG 6 khung 1080p của cuộn mẫu (chỉ lớp cảnh 3D; lớp chữ giống hệt nhau).
Đo: SSIM (ảnh xám, cửa sổ Gauss σ 1,5 — Wang 2004), pHash 64 bit (DCT 32×32 → 8×8, Hamming), s/khung (meta hero.js, 1 tiến trình, chạy tuần tự),
và tờ so cạnh nhau cắt 1:1 vùng nhiều chi tiết.
  lod_test.py <spec.yaml> --out <dir>   → <dir>/lod-test.json, <dir>/lod-test-sheet.jpg"""
import json, os, subprocess, sys, time
import numpy as np, yaml
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.fft import dctn
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep  # noqa: E402

REPO = prep.REPO
# (đoạn, giây trong cảnh) — chọn trước, trải các tầm máy: H 2,5 s (~440 km), H 12,5 s (~520 km), J 6,0 s (~600 km), N 4,2 s (~125 km), S 3,0 s (~650 km), P 2,5 s (ảnh)
PICKS = [('H', 2.5), ('H', 12.5), ('J', 6.0), ('N', 4.2), ('S', 3.0), ('P', 2.5)]
CONFIGS = {'A_spp4': dict(spp=4, lod=False), 'B_spp2': dict(spp=2, lod=False), 'C_spp2_lod': dict(spp=2, lod=True), 'D_spp4_lod': dict(spp=4, lod=True)}
# V3 (E6): --set v3 → chuẩn SPP4 cấu hình V2b; B = V2b (SPP2); E = SPP2 + bóng/mặt nạ viền ½ độ phân giải, viền 12 hướng (fast); F = SPP1 + fast
V3 = {'A_spp4': dict(spp=4, lod=False, fast=False), 'B_spp2_v2b': dict(spp=2, lod=False, fast=False), 'E_spp2_fast': dict(spp=2, lod=False, fast=True), 'F_spp1_fast': dict(spp=1, lod=False, fast=True), 'G_spp2_fast_aa500': dict(spp=2, lod=False, fast=True, spp1Km=500)}


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def ssim(a, b):
    a = a.astype(np.float64); b = b.astype(np.float64); C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2; g = lambda x: gaussian_filter(x, 1.5)
    ma, mb = g(a), g(b); va, vb, cab = g(a * a) - ma * ma, g(b * b) - mb * mb, g(a * b) - ma * mb
    return float((((2 * ma * mb + C1) * (2 * cab + C2)) / ((ma * ma + mb * mb + C1) * (va + vb + C2))).mean())


def phash(im):
    a = np.asarray(im.convert('L').resize((32, 32), Image.LANCZOS), np.float64); d = dctn(a, norm='ortho')[:8, :8].flatten(); return d[1:] > np.median(d[1:])


def main():
    global CONFIGS
    if arg('set') == 'v3': CONFIGS = V3
    E = yaml.safe_load(open(sys.argv[1])); prep.resolve_cams(E); out = arg('out'); os.makedirs(out, exist_ok=True); R = {}
    seg = {s['id']: s for s in E['segments']}
    only = (arg('cfg') or '').split(',')   # --cfg: chỉ dựng lại các cấu hình này; cấu hình khác dùng khung đã có trong --out
    for name, cf in CONFIGS.items():
        R[name] = {}
        for sid in dict.fromkeys(s for s, _ in PICKS):
            sh = seg[sid]['shots'][0]; h = E['heroes'][sh['p']['hero']]; opt = dict(h.get('opt', {}))
            if not cf['lod'] and h['hero'].startswith('relief/'): opt.update(lodMesh=0, lodTex=0)
            if h['hero'].startswith('relief/'): opt['lodMesh'], opt['lodTex'] = (300, 500) if cf['lod'] else (0, 0); opt['fast'] = cf.get('fast', False); opt['spp1Km'] = cf.get('spp1Km', 0)
            fr = [int(round(t * 24)) for s, t in PICKS if s == sid]; d = os.path.join(out, f'{name}-{sid}')
            cmd = ['node', os.path.join(REPO, 'scripts/k2/hero.js'), '--hero', h['hero'], '--dur', str(float(seg[sid]['dur']) + 0.5), '--w', '1920', '--h', '1080', '--spp', str(cf['spp']),
                   '--only', ','.join(map(str, fr)), '--opt', json.dumps(opt), '--out', d]
            t0 = time.time()
            if not (only[0] and name not in only and os.path.exists(os.path.join(d, 'meta.json'))):
                r = subprocess.run(cmd, capture_output=True, text=True)
                if r.returncode: print(r.stderr[-2000:]); sys.exit(f'lỗi {name} {sid}')
            meta = json.load(open(os.path.join(d, 'meta.json')))
            for f in fr: R[name][f'{sid}@{f}'] = dict(file=os.path.join(d, f'{f:05d}.jpg'), s_per_frame=meta['s_per_frame'], wall_s=round(time.time() - t0, 1))
            print(name, sid, meta['s_per_frame'], 's/khung', file=sys.stderr)
    res = {}
    for name in CONFIGS:
        rows = []
        for k, v in R[name].items():
            a = Image.open(R['A_spp4'][k]['file']); b = Image.open(v['file']); ga, gb = np.asarray(a.convert('L')), np.asarray(b.convert('L'))
            rows.append(dict(khung=k, ssim=round(ssim(ga, gb), 4), phash_hamming=int((phash(a) != phash(b)).sum()), s_per_frame=v['s_per_frame']))
        res[name] = dict(khung=rows, ssim_min=min(r['ssim'] for r in rows), ssim_tb=round(sum(r['ssim'] for r in rows) / len(rows), 4), phash_max=max(r['phash_hamming'] for r in rows),
                         s_per_frame_tb=round(sum(r['s_per_frame'] for r in rows) / len(rows), 2))
    json.dump(res, open(os.path.join(out, 'lod-test.json'), 'w'), indent=1, ensure_ascii=False)
    # tờ so: mỗi khung một hàng, cắt 1:1 vùng 640×360 ở tâm ảnh (nhiều chi tiết địa hình/vật), 4 cấu hình cạnh nhau
    keys = list(R['A_spp4']); sheet = Image.new('RGB', (640 * len(CONFIGS), 360 * len(keys)))
    for i, k in enumerate(keys):
        for j, name in enumerate(CONFIGS):
            im = Image.open(R[name][k]['file']); sheet.paste(im.crop((640, 360, 1280, 720)), (j * 640, i * 360))
    sheet.save(os.path.join(out, 'lod-test-sheet.jpg'), quality=88)
    for n, v in res.items(): print(n, 'SSIM tb', v['ssim_tb'], 'min', v['ssim_min'], 'pHash max', v['phash_max'], 's/khung', v['s_per_frame_tb'])


if __name__ == '__main__':
    main()
