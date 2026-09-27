"""Cổng 5 — ghép hình LAYOUT theo bảng ORDER (order_w1.js + order_w2.js qua film.js). Mọi shot 'new'.
Nguồn: các video nhóm render_film.js --only của từng gói, tìm trong /var/tmp/cine-out/{W1,W2,P}/**/timing_*.json (bản mới hơn của cùng shot thắng).
Chạy: /opt/cine/bin/python design/cong5/layout/assemble.py  → /var/tmp/cine-out/final/video.mp4 (x264 crf 14, trung gian) + motion/ (gộp) + assemble.json
"""
import glob, json, os, shutil, subprocess
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
A = os.path.join(REPO, 'design/cong5/layout'); V2 = '/var/tmp/cine-out/final'; os.makedirs(V2, exist_ok=True); W, H, FPS = 960, 540, 24
FB = W * H * 3
EV = json.loads(subprocess.run(['node', os.path.join(A, 'render_film.js'), '--events', '--out', '/tmp'], capture_output=True, text=True, check=True).stdout)
src = {}
for tj in sorted([f for d in ('W1', 'W2', 'P') for f in glob.glob(f'/var/tmp/cine-out/{d}/**/timing_*.json', recursive=True) if '/probe' not in f], key=os.path.getmtime):   # bản render mới hơn của cùng shot thắng
    T = json.load(open(tj)); k = 0
    for s in T['summary']: src[s['id']] = (T['mp4'], k, s['frames'], os.path.dirname(tj)); k += s['frames']

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
    mp4, k, m, d = src[sid]; assert m == n, (sid, m, n); it = frames(mp4, k, n)
    shutil.copyfile(os.path.join(d, 'motion', f'{sid}.json'), os.path.join(md, f'{sid}.json'))
    for b in it: enc.stdin.write(b)
    log.append({'id': sid, 'src': s, 'film_frames': [f0, f1], 'from': src[sid][0], 'from_frame': k})
enc.stdin.close(); enc.wait()
json.dump({'frames': round(EV['FILM_S'] * FPS), 'shots': log}, open(os.path.join(V2, 'assemble.json'), 'w'), indent=1)
print(json.dumps({'mp4': out, 'frames': round(EV['FILM_S'] * FPS)}))
