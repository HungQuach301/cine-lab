#!/opt/cine/bin/python
"""V7B (việc 3, V7P-D3 phương án b) · NẮN bản Faden 1783 (Yale 2046612, PD; bản xem trước 1600 px trong vay-ham/ref) về hộp ENU để PHỦ lên địa hình ≤ 3 s ở C1
(TL-4: tư liệu chỉ phủ khớp lên địa hình rồi tan vào cảnh). Phép đồng dạng = đúng phép của v7p_eo_dat.py (3 điểm khống chế ghost/gcp-1782-faden-doi-chieu.json, RMS 12,5 m trong vùng;
ngoài vùng ≤ 250 m). Ra: <pack>/layers/faden1783-v7b.png (RGBA; alpha = 0 ngoài tờ bản đồ) + .json (hộp, bước, RMS).
Dùng: /opt/cine/bin/python -I scripts/k2tl/v7b_faden.py [--box -3400,-1700,900,4700 --step 5]"""
import json, os, sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / 'scripts/k2tl')); import geo  # noqa: E402
CACHE = Path(os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache')); PK = CACHE / 'scene/gib/pack'
box = [float(x) for x in (sys.argv[sys.argv.index('--box') + 1] if '--box' in sys.argv else '-3400,-1700,900,4700').split(',')]; step = float(sys.argv[sys.argv.index('--step') + 1]) if '--step' in sys.argv else 5.0
G = json.loads((ROOT / 'channel-k2/k2c-t3-01/ghost/gcp-1782-faden-doi-chieu.json').read_text()); S = 10313 / 1600; OE, ON = geo.utm(-5.3487, 36.1513)
P = np.array([g['px'] for g in G['gcp']], float); U = np.array([[g['utm'][0] - OE, g['utm'][1] - ON] for g in G['gcp']], float)
pz = P[:, 0] - 1j * P[:, 1]; uz = U[:, 0] + 1j * U[:, 1]; A = np.vstack([pz, np.ones(len(P))]).T; (a, b), *_ = np.linalg.lstsq(A, uz, rcond=None)
RMS = float(np.sqrt(np.mean(np.abs(A @ [a, b] - uz) ** 2)))
src = Image.open(ROOT / 'channel-k2/k2c-t3-01/vay-ham/ref/yale_2046612_faden_1783_spanish_works.jpg').convert('RGB'); W, H = src.size; arr = np.asarray(src).astype(np.float32)
sc = 1600 / W   # bản xem trước có thể khác 1600 px: quy về hệ điểm ảnh 1600 của phép đồng dạng
e0, n0, e1, n1 = box; nx, ny = int((e1 - e0) / step), int((n1 - n0) / step)
E, N = np.meshgrid(e0 + (np.arange(nx) + 0.5) * step, n1 - (np.arange(ny) + 0.5) * step)
z = ((E + 1j * N) - b) / a; px = z.real / S / sc; py = -z.imag / S / sc   # nghịch: a·(x·S − i·y·S) + b = E + iN
ok = (px >= 0) & (px < W - 1) & (py >= 0) & (py < H - 1); xi = np.clip(px, 0, W - 2); yi = np.clip(py, 0, H - 2); x0 = xi.astype(int); y0 = yi.astype(int); fx = (xi - x0)[..., None]; fy = (yi - y0)[..., None]
c = arr[y0, x0] * (1 - fx) * (1 - fy) + arr[y0, x0 + 1] * fx * (1 - fy) + arr[y0 + 1, x0] * (1 - fx) * fy + arr[y0 + 1, x0 + 1] * fx * fy
out = np.dstack([c, ok[..., None] * 255.0]).clip(0, 255).astype(np.uint8); (PK / 'layers').mkdir(parents=True, exist_ok=True)
Image.fromarray(out, 'RGBA').save(PK / 'layers/faden1783-v7b.png'); meta = dict(box=box, step=step, px=[nx, ny], rms_m=round(RMS, 1), nguon='Faden 1783 (Yale 2046612, PD) — bản xem trước vay-ham/ref', phep='đồng dạng 3 GCP (ghost/gcp-1782-faden-doi-chieu.json)', phu_pct=round(float(ok.mean() * 100), 1))
(PK / 'layers/faden1783-v7b.json').write_text(json.dumps(meta, ensure_ascii=False)); print(meta, src.size)
