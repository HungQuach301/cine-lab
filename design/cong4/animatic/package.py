"""Cổng 4 — đóng gói ANIMATIC: phụ đề tiếng Anh cháy vào hình (kèm matte chữ cho P0/P1/G4), ghép âm tạm, file đi kèm cho checks, gói chiếu mù.
Chạy: /opt/cine/bin/python design/cong4/animatic/package.py <thư mục render (video.mp4, motion/)> <thư mục âm (mix.flac, stems/)>
Ghi:
  design/cong4/animatic/out/animatic.mp4  (+ .script.txt, .text/, .stems/, .motion.json, .assets.json)  ← bản chạy checks
  screening/animatic.mp4                  (bản sao y từng byte của bản trên) + screening/questions.json
"""
import glob, hashlib, json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
W, H, FPS = 960, 540, 24
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FILL = (244, 241, 234)
# Thẻ phụ đề: mốc theo đoạn lời đo trên stem thoại (dialogue.wav): L1 12,13–14,09; L2 60,14–62,89; L3 88,11–88,89;
# L4 110,10–111,85 | 113,56–114,97 | 116,55–117,78 | 119,33–124,05.
CARDS = [(12.0, 14.6, "Evening, old street."), (60.0, 63.2, "Not yet... not yet."), (88.0, 90.0, "Go on, then."),
         (110.0, 112.6, "That's the last one, then."), (113.4, 115.8, "Goodnight, old street."), (116.4, 118.6, "You'll be brighter now."),
         (119.2, 124.6, "Just... keep a little dark for the ones who need it.")]

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def main(rdir, adir):
    HQ = os.environ.get('HQ') == '1'   # bản đối chứng bitrate cao (CRF 14) để đo G3b không bị trần 50 MB — không nộp, không commit
    od = os.path.join(REPO, 'design/cong4/animatic/out' + ('/hq' if HQ else '')); os.makedirs(od, exist_ok=True)
    base = os.path.join(od, 'animatic_hq' if HQ else 'animatic')
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
    # Trần gói chiếu mù < 50 MB (yêu cầu chủ dự án) → mã hoá 2 pass bitrate cố định (mặc định 2 350 kb/s hình + 192 kb/s tiếng ≈ 47,7 MB / 150 s).
    vbr = os.environ.get('VBR', '2350k'); passlog = os.path.join(od, 'x264pass')
    common = ['-filter_complex', ';'.join(chain), '-map', '[vout]', '-t', '150', '-c:v', 'libx264', '-preset', 'slow', '-b:v', vbr, '-tune', 'grain', '-g', '48',
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
    scene_files = [f'design/cong4/animatic/{f}' for f in ['page.js', 'film.js', 'sets.js', 'sets2.js', 'util.js']]
    assets = ['reports/m1/cong2/tableread-d2/lines/L1.mp3', 'reports/m1/cong2/tableread-d2/lines/L2.mp3', 'reports/m1/cong2/tableread-d2/lines/L3.mp3',
              'reports/m1/cong2/tableread-d2/lines/L4.mp3', 'reports/m0/music/theme-dit-1.flac', 'design/cong3/model-sheet/ida.json', 'design/cong3/model-sheet/cas.json']
    json.dump({'workdir': 'design/cong4/animatic', 'scene_files': scene_files, 'assets': assets}, open(base + '.assets.json', 'w'), indent=1)
    # ---- gói chiếu mù ----
    sc = os.path.join(REPO, 'screening'); os.makedirs(sc, exist_ok=True)
    if not HQ: shutil.copyfile(base + '.mp4', os.path.join(sc, 'animatic.mp4'))
    sz = os.path.getsize(base + '.mp4') / 1e6
    print(json.dumps({'mp4': base + '.mp4', 'MB': round(sz, 2), 'sha256': sha(base + '.mp4'), 'screening_same': (not HQ) and sha(base + '.mp4') == sha(os.path.join(sc, 'animatic.mp4')),
                      'channels': len(ch), 'tracks': len(tr), 'cards': len(CARDS)}))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
