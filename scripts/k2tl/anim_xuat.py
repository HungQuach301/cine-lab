#!/opt/cine/bin/python
"""ANIMATIC-T3 việc 7 · XUẤT CHO CHỦ DỰ ÁN từ master 960×540 (giọng + nhạc, KHÔNG phụ đề):
 (a) bản xem chia theo chương 640×360, mỗi tệp ≤ 5 MB → reports/animatic-t3/xem/NN-<tên>.mp4 (2 lượt bitrate theo độ dài; âm AAC 64 kb/s, alimiter 0,75 như BAI-HOC #45/#69)
 (b) bản kiểm có phụ đề riêng (640×360, ngoài git) — phụ đề CHỈ ở bản kiểm
 (c) tờ khung 1 khung/shot (giữa shot), mã shot + mốc giây → reports/animatic-t3/to-khung.jpg (≤ 4 MB)
 (d) PHIEU-XEM.md: mã shot ↔ tệp xem ↔ mốc giây trong tệp ↔ mốc giây cả phim
  anim_xuat.py <master.mp4> [--buoc a,b,c,d]"""
import json, os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
REPO = Path(__file__).resolve().parents[2]; EPD = REPO / 'channel-k2/k2c-t3-01/animatic'; R = REPO / os.environ.get('ANIM_R', 'reports/animatic-t3'); X = R / 'xem'   # ANIM-V2: ANIM_R=reports/animatic-t3-v2
M = sys.argv[1]; BUOC = (sys.argv[sys.argv.index('--buoc') + 1] if '--buoc' in sys.argv else 'a,b,c,d').split(',')
OUTX = Path('/var/tmp/cine-out/k2c-t3-anim/xem'); OUTX.mkdir(parents=True, exist_ok=True); X.mkdir(parents=True, exist_ok=True)
B = json.loads((EPD / 'bang-shot.json').read_text())
CH = [('01-mo-dau', 0.0, 43.833, 'Mở đầu (móc)'), ('02-ch1-rock-1704', 43.833, 173.083, 'Chương 1 — 1704–1735'), ('03-ch2a-vay-ham', 173.083, 262.167, 'Chương 2a — đại vây hãm 1779–81'),
      ('04-ch2b-tan-cong-1782', 262.167, 382.583, 'Chương 2b — 1782 → hoà ước 1783'), ('05-ch3-dat-trung-lap', 382.583, 471.625, 'Chương 3 — đất trung lập 1783–1938'),
      ('06-ch4-duong-bang', 471.625, 585.833, 'Chương 4 — đường băng 1939–1943'), ('07-ch5a-cong', 585.833, 666.083, 'Chương 5a — cổng 1946–2026'), ('08-ch5b-ket', 666.083, 761.0, 'Chương 5b — hiệp ước 2026 → kết + thẻ phương pháp')]
def sh(c): subprocess.run(c, check=True)
def mm(t): return f'{int(t // 60)}:{t % 60:05.2f}'
if 'a' in BUOC:
    for k, a, b, _ in CH:
        o = X / f'{k}.mp4'; d = b - a; vb = int((4_700_000 * 8 / d - 64_000) / 1000)
        for p in (1, 2):
            sh(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{d:.3f}', '-i', M, '-vf', 'scale=640:360:flags=lanczos,fps=24', '-c:v', 'libx264', '-preset', 'slow', '-b:v', f'{vb}k', '-pass', str(p),
                '-passlogfile', str(OUTX / f'x264-{k}')] + (['-an', '-f', 'mp4', '/dev/null'] if p == 1 else ['-af', 'volume=-1.2dB,alimiter=limit=0.75:level=disabled', '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', str(o)]))
        print(k, o.stat().st_size, flush=True)
if 'b' in BUOC:
    srt = EPD / 'phu-de.srt'; o = OUTX / 'k2c-t3-anim-640-phude-KIEM.mp4'
    sh(['ffmpeg', '-v', 'error', '-y', '-i', M, '-vf', f"scale=640:360:flags=lanczos,subtitles={srt}:force_style='FontName=DejaVu Sans,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=28'",
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '26', '-af', 'volume=-1.2dB,alimiter=limit=0.75:level=disabled', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', str(o)]); print('phude', o)
if 'c' in BUOC:
    W, H = 320, 180; per = 6; rows = (len(B) + per - 1) // per; S = Image.new('RGB', (W * per, (H + 22) * rows), (16, 16, 16)); g = ImageDraw.Draw(S)
    try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
    except Exception: F = None
    for i, b in enumerate(B):
        t = b['t0'] + b['dur'] * 0.5 if not b.get('lan') else b['t0'] + 3.0
        p = OUTX / f"k-{b['ma']}.jpg"; sh(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', M, '-frames:v', '1', '-vf', f'scale={W}:{H}', str(p)])
        x, y = (i % per) * W, (i // per) * (H + 22); S.paste(Image.open(p), (x, y + 22)); g.text((x + 4, y + 4), f"{b['ma']}  {mm(b['t0'])}–{mm(b['t1'])}  (@{mm(t)})", fill=(255, 225, 110), font=F)
    o = R / 'to-khung.jpg'; q = 88
    while True:
        S.save(o, quality=q, optimize=True)
        if o.stat().st_size <= 3_900_000 or q <= 50: break
        q -= 6
    print('to-khung', o.stat().st_size)
if 'd' in BUOC:
    L = ['# PHIẾU XEM — animatic cả tập T3 Gibraltar (960×540 → bản xem 640×360, không phụ đề)', '',
         'Ghi nhận xét theo dạng **`<mã shot>: …`** (ví dụ `N1.4: dòng người khó thấy`). Mốc trong tệp = giây tính từ đầu tệp xem của chương; mốc cả phim = giây trên bản liền 960×540.', '',
         '| Tệp xem | Nội dung | Mốc cả phim |', '|---|---|---|']
    for k, a, b, n in CH: L.append(f'| `{R.relative_to(REPO)}/xem/{k}.mp4` | {n} | {mm(a)} → {mm(b)} |')
    L += ['', '| Mã shot | Tệp xem | Mốc trong tệp | Mốc cả phim | Lời (dòng) | Ghi chú của chủ dự án |', '|---|---|---|---|---|---|']
    for b in B:
        k, a, _, _ = [c for c in CH if c[1] - 1e-3 <= b['t0'] < c[2] - 1e-3][0]
        L.append(f"| **{b['ma']}** | `{k}.mp4` | {mm(b['t0'] - a)} → {mm(b['t1'] - a)} | {mm(b['t0'])} → {mm(b['t1'])} | {', '.join(b['dong']) or 'thẻ'} | |")
    L += ['', 'Ghi chú chung:', '', '- …']
    (R / 'PHIEU-XEM.md').write_text('\n'.join(L) + '\n'); print('PHIEU-XEM')
