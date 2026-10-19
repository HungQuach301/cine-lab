#!/opt/cine/bin/python
"""V7-PILOT · soi nhanh: dựng vài khung (theo giây cảnh) của các shot timelapse trong v7p/episode.yaml, song song P tiến trình → <out>/<shot>/NNNNN.jpg + tờ khung.
Dùng: /opt/cine/bin/python -I scripts/k2tl/v7p_probe.py --shots H1,H2 --t 0.5,6,12 [--w 960 --h 540 --spp 2 --out /var/tmp/cine-out/v7p/probe --P 3 --sheet tờ.jpg]"""
import argparse, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import yaml
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
a = argparse.ArgumentParser(); a.add_argument('--shots', default=''); a.add_argument('--t', default='mid'); a.add_argument('--w', type=int, default=960); a.add_argument('--h', type=int, default=540)
a.add_argument('--spp', type=int, default=2); a.add_argument('--out', default='/var/tmp/cine-out/v7p/probe'); a.add_argument('--P', type=int, default=3); a.add_argument('--sheet', default=None)
a.add_argument('--ep', default=str(ROOT / 'channel-k2/k2c-t3-01/v7p/episode.yaml')); A = a.parse_args()
E = yaml.safe_load(open(A.ep)); H = E['heroes']; env = dict(os.environ, K2TL_CACHE=os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache'))
keys = [k for k in H if not A.shots or k.split('_', 1)[1] in A.shots.split(',')]
def one(k):
    h = H[k]; d = h['dur']; n = int(round(d * 24)); ts = [d / 2 if x == 'mid' else d - 0.2 if x == 'end' else float(x) for x in A.t.split(',')]
    fr = sorted({min(n - 1, max(0, int(round(t * 24)))) for t in ts if t <= d + 1e-6}); out = Path(A.out) / k; out.mkdir(parents=True, exist_ok=True)
    for f in out.glob('*.jpg'): f.unlink()
    r = subprocess.run(['node', str(ROOT / 'scripts/k2/hero.js'), '--hero', h['hero'], '--variant', 'a', '--dur', str(d), '--w', str(A.w), '--h', str(A.h), '--spp', str(A.spp),
                        '--opt', json.dumps(h['opt'], separators=(',', ':')), '--out', str(out), '--only', ','.join(map(str, fr))], capture_output=True, text=True, env=env)
    err = [l for l in r.stderr.splitlines() if 'pageerror' in l or 'LỖI' in l or 'Error' in l][:3]
    m = json.loads((out / 'meta.json').read_text()) if (out / 'meta.json').exists() else {}
    return k, r.returncode, err, m.get('s_per_frame'), fr
with ThreadPoolExecutor(A.P) as ex: res = list(ex.map(one, keys))
for k, rc, err, spf, fr in res: print(k, 'rc', rc, 's/khung', spf, 'khung', fr, *err)
if A.sheet:
    ims = []
    for k in keys:
        for f in sorted((Path(A.out) / k).glob('*.jpg')): ims.append((f'{k} f{int(f.stem)} ({int(f.stem) / 24:.1f}s)', Image.open(f)))
    w = 640; h = 360; cols = 2; rows = (len(ims) + 1) // 2; S = Image.new('RGB', (cols * w, rows * (h + 16)), 'white'); D = ImageDraw.Draw(S)
    for i, (lab, im) in enumerate(ims): x, y = (i % cols) * w, (i // cols) * (h + 16); S.paste(im.resize((w, h)), (x, y + 16)); D.text((x + 4, y + 2), lab, fill='black')
    S.save(A.sheet, quality=86); print('tờ', A.sheet)
