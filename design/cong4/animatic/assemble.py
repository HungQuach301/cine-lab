"""Cổng 4 v2 — ghép hình ANIMATIC theo bảng ORDER của film.js (nguồn duy nhất).
Shot 'new': lấy từ các video nhóm render_film.js --only (out/v2/video_<…>.mp4, thứ tự + số khung theo timing_<…>.json).
Shot 'v1:<id>': cắt đúng số khung từ bản v1 (out/video.mp4) ở mốc v1 của shot đó.
Chạy: /opt/cine/bin/python design/cong4/animatic/assemble.py  → out/v2/video.mp4 (x264 crf 14, trung gian) + out/v2/motion/ (gộp) + out/v2/assemble.json
"""
import glob, json, os, shutil, subprocess
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
A = os.path.join(REPO, 'design/cong4/animatic'); V2 = os.path.join(A, 'out/v2'); W, H, FPS = 960, 540, 24
FB = W * H * 3
V1_T0 = {'s01': 0.0, 's43': 130.0, 's48': 145.0}   # mốc shot trong bản v1 (film.js v1, 150 s)
EV = json.loads(subprocess.run(['node', os.path.join(A, 'render_film.js'), '--events', '--out', '/tmp'], capture_output=True, text=True, check=True).stdout)
src = {}
for tj in sorted(glob.glob(os.path.join(V2, 'timing_*.json')), key=os.path.getmtime):   # bản render mới hơn của cùng shot thắng
    T = json.load(open(tj)); k = 0
    for s in T['summary']: src[s['id']] = (T['mp4'], k, s['frames']); k += s['frames']

def frames(mp4, start, n):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', mp4, '-vf', f'select=between(n\\,{start}\\,{start + n - 1})', '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    got = 0
    while got < n:
        b = p.stdout.read(FB)
        if len(b) < FB: break
        got += 1; yield b
    p.stdout.close(); p.wait()
    if got != n: raise SystemExit(f'thiếu khung: {mp4} từ {start}: {got}/{n}')

out = os.path.join(V2, 'video.mp4')
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-framerate', '24', '-i', '-',
                        '-vf', 'scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-tune', 'grain',
                        '-g', '48', '-color_range', 'tv', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', '24', out], stdin=subprocess.PIPE)
log, md = [], os.path.join(V2, 'motion'); os.makedirs(md, exist_ok=True)
for sid, dur, s in EV['ORDER']:
    f0, f1 = round(EV['T0'][sid] * FPS), round(EV['T1'][sid] * FPS); n = f1 - f0
    if s == 'new':
        mp4, k, m = src[sid]; assert m == n, (sid, m, n); it = frames(mp4, k, n)
    else:
        v = s.split(':')[1]; k = round(V1_T0[v] * FPS); it = frames(os.path.join(A, 'out/video.mp4'), k, n)
        M = json.load(open(os.path.join(A, 'out/motion', f'{v}.json'))); M['frames'] = M['frames'][:n]; M['first_frame'] = f0
        json.dump(M, open(os.path.join(md, f'{sid}.json'), 'w'))
    for b in it: enc.stdin.write(b)
    log.append({'id': sid, 'src': s, 'film_frames': [f0, f1], 'from': (src[sid][0] if s == 'new' else 'out/video.mp4 (v1)'), 'from_frame': k})
enc.stdin.close(); enc.wait()
json.dump({'frames': round(EV['FILM_S'] * FPS), 'shots': log}, open(os.path.join(V2, 'assemble.json'), 'w'), indent=1)
print(json.dumps({'mp4': out, 'frames': round(EV['FILM_S'] * FPS)}))
