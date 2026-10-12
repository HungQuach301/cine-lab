#!/opt/cine/bin/python
"""KÊNH 2 · rà thư viện góc máy: dựng khung đầu và cuối của mỗi preset (480×270, SPP1) cho một bộ cảnh → tờ khung có nhãn tên preset.
Dùng opt (trừ cam) của một shot Steel làm bối cảnh đại diện. Preset hỏng (lộ mép cảnh, xuyên vật thể, trống) → đánh 'loai: true' trong cams.yaml.
  cams_sheet.py <k2g01/port> [--ep channel-k2/k2g-ep01/ep-src.yaml] [--out channel-k2/k2v-mau/cams]
  cams_sheet.py map/globe --module --ep channel-k2/k2v-mau/A-map-washington-brussels.yaml --key a_pair --extra '{"focus": "brussels"}' [--dur 8]
      (preset module k2v: opt.preset = tên preset, nội dung lấy từ đặc tả mẫu)"""
import json, os, subprocess, sys, yaml
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
a = sys.argv; arg = lambda k, d=None: a[a.index('--' + k) + 1] if '--' + k in a else d
scene = a[1]; L = yaml.safe_load(open(os.path.join(REPO, 'scripts/k2/cams.yaml')))[scene]
E = yaml.safe_load(open(os.path.join(REPO, arg('ep', 'channel-k2/k2g-ep01/ep-src.yaml'))))
rep = next(({k: v for k, v in (h.get('opt') or {}).items() if k != 'cam'} for kk, h in E['heroes'].items() if h['hero'] == scene and not h.get('size') and (not arg('key') or kk == arg('key'))), {})
rep.update(json.loads(arg('extra', '{}')))
def noat(v):   # mốc "@từ" → -1 (có sẵn từ đầu), giữ cấu trúc
    if isinstance(v, str) and '@' in v: return -1
    if isinstance(v, list): return [noat(x) for x in v]
    if isinstance(v, dict): return {k: noat(x) for k, x in v.items()}
    return v
rep = noat(rep)
out = os.path.join(REPO, arg('out', 'channel-k2/k2v-mau/cams')); tmp = '/var/tmp/cine-out/cams-sheet/' + scene.replace('/', '-'); os.makedirs(out, exist_ok=True)
tiles = []
for name, P in L.items():
    if P.get('module') and '--module' not in a: continue
    d = os.path.join(tmp, name); o = dict(rep, preset=name) if P.get('module') else dict(rep, cam=P['cam'])
    if not os.path.exists(os.path.join(d, 'meta.json')):
        r = subprocess.run(['node', os.path.join(REPO, 'scripts/k2/hero.js'), '--hero', scene, '--dur', arg('dur', '4'), '--w', '480', '--h', '270', '--spp', '1', '--only', f"0,{int(float(arg('dur', '4')) * 24) - 1}", '--opt', json.dumps(o), '--out', d], capture_output=True, text=True)
        if r.returncode: print(name, 'LỖI', r.stderr[-500:]); continue
    lab = os.path.join(tmp, name + '.jpg')
    last = f"{int(float(arg('dur', '4')) * 24) - 1:05d}.jpg"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(d, '00000.jpg'), '-i', os.path.join(d, last), '-filter_complex',
                    f"[0][1]hstack,drawbox=x=0:y=0:w=iw:h=34:color=black@0.7:t=fill,drawtext=fontfile=/usr/share/fonts/opentype/inter/Inter-SemiBold.otf:text='{name}':x=10:y=7:fontsize=22:fontcolor=white", lab], check=True)
    tiles.append(lab)
cols = 2; rows = (len(tiles) + cols - 1) // cols
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + sum([['-i', t] for t in tiles], []) + ['-filter_complex', ''.join(f'[{i}]' for i in range(len(tiles))) + f'xstack=inputs={len(tiles)}:layout=' +
               '|'.join(f'{(i % cols) * 960}_{(i // cols) * 270}' for i in range(len(tiles))) + f':fill=black', os.path.join(out, scene.split('/')[1] + '.jpg')] if len(tiles) > 1 else ['-i', tiles[0], os.path.join(out, scene.split('/')[1] + '.jpg')], check=True)
print(os.path.join(out, scene.split('/')[1] + '.jpg'), len(tiles), 'preset')
