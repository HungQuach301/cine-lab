"""Cổng 5 — đóng gói LAYOUT (chép cách đóng gói animatic Cổng 4): phụ đề tiếng Anh cháy vào hình (kèm matte chữ cho P0/P1/G4), ghép âm tạm, file đi kèm cho checks, gói chiếu mù.
Chạy: /opt/cine/bin/python design/cong5/layout/package.py <thư mục render (video.mp4, motion/)> <thư mục âm (mix.flac, stems/)>
Ghi:
  design/cong5/layout/out/layout.mp4  (+ .script.txt, .text/, .stems/, .motion.json, .assets.json)  ← bản chạy checks
  screening/layout.mp4                    (bản sao y từng byte của bản trên) + screening/questions.json
"""
import glob, hashlib, json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
W, H, FPS = 960, 540, 24
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FILL = (244, 241, 234)
# Thẻ phụ đề: mốc tương đối so với đầu câu (đo trên stem thoại v1: L1 +0,13–2,09; L2 +0,14–2,89; L3 +0,11–0,89;
# L4 +0,10–1,85 | +3,56–4,97 | +6,55–7,78 | +9,33–14,05). Đầu câu lấy từ film.js (EVENTS.DIALOGUE) — v2.
EV = json.loads(subprocess.run(['node', os.path.join(REPO, 'design/cong5/layout/render_film.js'), '--events', '--out', '/tmp'], capture_output=True, text=True, check=True).stdout)
D, FILM_S = EV['DIALOGUE'], EV['FILM_S']
CARDS = [(D['L1'] + a, D['L1'] + b, t) for a, b, t in [(0.0, 2.6, "Evening, old street.")]] + [(D['L2'], D['L2'] + 3.2, "Not yet... not yet."), (D['L3'], D['L3'] + 2.0, "Go on, then.")] + \
        [(D['L4'] + a, D['L4'] + b, t) for a, b, t in [(0.0, 2.6, "That's the last one, then."), (3.4, 5.8, "Goodnight, old street."), (6.4, 8.6, "You'll be brighter now."),
                                                     (9.2, 14.6, "Just... keep a little dark for the ones who need it.")]]

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def main(rdir, adir):
    HQ = os.environ.get('HQ') == '1'   # bản đối chứng bitrate cao (CRF 14) để đo G3b không bị trần 50 MB — không nộp, không commit
    od = os.path.join(REPO, 'design/cong5/layout/out' + ('/hq' if HQ else '')); os.makedirs(od, exist_ok=True)
    base = os.path.join(od, 'layout_hq' if HQ else 'layout')
    # ---- phụ đề: ảnh cháy (ruột + viền đen 3 px) và matte (chỉ ruột nét, màu ruột) ----
    tdir = base + '.text'; shutil.rmtree(tdir, ignore_errors=True); os.makedirs(tdir)
    font = ImageFont.truetype(FONT, 30); els = []; burn = []
    for k, (a, b, txt) in enumerate(CARDS, 1):
        full = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(full)
        tw = d.textlength(txt, font=font); x, y = (W - tw) / 2, H - 46 - 30
        # hộp nền tối gần đục sau chữ (phố trắng ở cảnh 3–5 làm viền mảnh không đủ tương phản — G4 đo 1,2:1 ở bản đầu)
        l, t, r, bt = d.textbbox((x, y), txt, font=font); d.rounded_rectangle((l - 14, t - 9, r + 14, bt + 10), radius=6, fill=(12, 12, 14, 228))
        d.text((x, y), txt, font=font, fill=FILL + (255,), stroke_width=2, stroke_fill=(10, 10, 12, 255))
        m = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(m).text((x, y), txt, font=font, fill=FILL + (255,))
        fb = os.path.join(od, f'sub{k:02d}_burn.png'); full.save(fb); burn.append((a, b, fb))
        m.save(os.path.join(tdir, f'sub{k:02d}.png'))
        els.append({'id': f'sub{k:02d}', 'first_frame': int(round(a * FPS)), 'last_frame': int(round(b * FPS)) - 1, 'matte': f'sub{k:02d}.png', 'text': txt})
    json.dump({'elements': els}, open(os.path.join(tdir, 'elements.json'), 'w'), ensure_ascii=False, indent=1)
    # ---- hình + phụ đề + âm → animatic.mp4 ----
    video = os.path.join(rdir, 'video.mp4'); mix = os.path.join(adir, 'mix.flac')
    ins = ['-i', video]; [ins.extend(['-loop', '1', '-framerate', str(FPS), '-i', fb]) for _, _, fb in burn]; ins += ['-i', mix]
    chain, last = [], '[0:v]'
    for k, (a, b, _) in enumerate(burn, 1):
        f0, f1 = int(round(a * FPS)), int(round(b * FPS)) - 1; nxt = f'[v{k}]'
        chain.append(f"{last}[{k}:v]overlay=0:0:enable='between(n,{f0},{f1})':shortest=0:eof_action=pass{nxt}"); last = nxt
    chain.append(f"{last}format=yuv420p[vout]")
    # Trần gói chiếu mù < 50 MB (yêu cầu chủ dự án) → mã hoá 2 pass bitrate cố định (mặc định 2 350 kb/s hình + 192 kb/s tiếng ≈ 45 MB / 142,5 s).
    vbr = os.environ.get('VBR', '2350k'); passlog = os.path.join(od, 'x264pass')
    common = ['-filter_complex', ';'.join(chain), '-map', '[vout]', '-t', str(FILM_S), '-c:v', 'libx264', '-preset', 'slow', '-b:v', vbr, '-tune', 'grain', '-g', '48',
              '-x264-params', 'no-fast-pskip=1:deadzone-inter=0:deadzone-intra=0', '-passlogfile', passlog,
              '-color_range', 'tv', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', '24']
    if HQ:
        common = [('-crf' if c == '-b:v' else c) for c in common]; common[common.index('-crf') + 1] = '14'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, *[c for c in common if c not in ('-passlogfile', passlog)], '-map', f'{len(burn) + 1}:a', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', base + '.mp4'], check=True)
    else:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, *common, '-pass', '1', '-an', '-f', 'null', '-'], check=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, *common, '-pass', '2', '-map', f'{len(burn) + 1}:a', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', base + '.mp4'], check=True)
    for f in glob.glob(passlog + '*'): os.remove(f)
    for _, _, fb in burn: os.remove(fb)
    # ---- file đi kèm cho checks ----
    open(base + '.script.txt', 'w').write('\n'.join(f'IDA: {t}' for _, _, t in CARDS) + '\n')
    sdir = base + '.stems'; shutil.rmtree(sdir, ignore_errors=True); shutil.copytree(os.path.join(adir, 'stems'), sdir)
    # chuyển động bake: kênh theo shot (tên nhân vật trước "/"), track màn hình theo shot
    ch, tr = [], []
    for mf in sorted(glob.glob(os.path.join(rdir, 'motion', 's*.json'))):
        sid = os.path.basename(mf)[:-5]; M = json.load(open(mf)); f0 = M['first_frame']; fr = M['frames']
        keys = set(); [keys.update(x['rot'].keys()) for x in fr]
        for k in sorted(keys):
            name, j = k.split('/', 1); ch.append({'id': f'{name}/{sid}.{j}', 'class': 'character_part', 'first_frame': f0, 'values': [x['rot'].get(k) for x in fr]})
        rk = set(); [rk.update(x['root'].keys()) for x in fr]
        for k in sorted(rk):
            name, j = k.split('/', 1); ch.append({'id': f'{name}/{sid}.{j}', 'class': 'character_root', 'first_frame': f0, 'values': [x['root'].get(k) for x in fr]})
        ch.append({'id': f'camera/{sid}.loc', 'class': 'camera', 'first_frame': f0, 'values': [x['cam'] for x in fr]})
        tk = set(); [tk.update(x['track'].keys()) for x in fr]
        for k in sorted(tk):
            vals = [x['track'].get(k) for x in fr]
            if all(v is None for v in vals): continue   # track không lúc nào thấy (khuất/ngoài khung) — không khai
            name, part = k.split('/', 1); tr.append({'id': f'{name}/{part}@{sid}', 'first_frame': f0, 'values': vals})
    json.dump({'fps': FPS, 'channels': ch, 'screen_tracks': tr}, open(base + '.motion.json', 'w'))
    scene_files = [f'design/cong5/layout/{f}' for f in ['page.js', 'film.js', 'common.js', 'order_w1.js', 'order_w2.js', 'shots_w1.js', 'shots_w2.js', 'sets.js', 'sets2.js', 'sets_end.js', 'util.js'] + (['facelight.js'] if os.path.exists(os.path.join(REPO, 'design/cong5/layout/facelight.js')) else [])]
    assets = ['reports/m1/cong2/tableread-d2/lines/L1.mp3', 'reports/m1/cong2/tableread-d2/lines/L2.mp3', 'reports/m1/cong2/tableread-d2/lines/L3.mp3',
              'reports/m1/cong2/tableread-d2/lines/L4.mp3', 'reports/m0/music/theme-dit-1.flac', 'design/cong3/model-sheet/ida.json', 'design/cong3/model-sheet/cas.json']
    json.dump({'workdir': 'design/cong5/layout', 'scene_files': scene_files, 'assets': assets}, open(base + '.assets.json', 'w'), indent=1)
    # ---- gói chiếu mù ----
    sc = os.path.join(REPO, 'screening'); os.makedirs(sc, exist_ok=True)
    if not HQ: shutil.copyfile(base + '.mp4', os.path.join(sc, 'layout.mp4'))
    sz = os.path.getsize(base + '.mp4') / 1e6
    print(json.dumps({'mp4': base + '.mp4', 'MB': round(sz, 2), 'sha256': sha(base + '.mp4'), 'screening_same': (not HQ) and sha(base + '.mp4') == sha(os.path.join(sc, 'layout.mp4')),
                      'channels': len(ch), 'tracks': len(tr), 'cards': len(CARDS)}))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
