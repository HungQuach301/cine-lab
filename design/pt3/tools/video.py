"""PT3 · video thử 540p (960×540 H.264, 24 fps, không LFS): mỗi nhánh × cú một tệp + nhãn nhánh góc trên-trái.
Khung có vân AI mang dòng bắt buộc "Surface detail AI-assisted · layout, landmarks & flags from sources" (dưới-trái); khung A: "No AI imagery".
Ghi log khung: ai_texture true/false.  video.py <ra.mp4> <log.jsonl> <nhãn:thư mục>"""
import sys, os, glob, json, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont
OUT, LOG = sys.argv[1], sys.argv[2]; BR = [a.split(':', 1) for a in sys.argv[3:]]
FB = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 22); FS = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf', 15)
frames = sorted(set.intersection(*[set(os.path.basename(p) for p in glob.glob(os.path.join(d, '[0-9][0-9][0-9][0-9].png'))) for _, d in BR]))
n = len(BR); H = 540; W = 960
with tempfile.TemporaryDirectory() as td, open(LOG, 'w') as lg:
    for k, f in enumerate(frames):
        S = Image.new('RGB', (W, H * n))
        for i, (lab, d) in enumerate(BR):
            im = Image.open(os.path.join(d, f)).convert('RGB').resize((W, H), Image.LANCZOS); dr = ImageDraw.Draw(im); ai = lab != 'A'
            dr.rectangle((0, 0, 92, 32), fill=(0, 0, 0)); dr.text((10, 4), lab, font=FB, fill=(255, 255, 255))
            txt = 'Surface detail AI-assisted · layout, landmarks & flags from sources' if ai else 'No AI imagery'
            tw = dr.textlength(txt, font=FS); dr.rectangle((0, H - 26, tw + 16, H), fill=(0, 0, 0)); dr.text((8, H - 23), txt, font=FS, fill=(235, 235, 235))
            S.paste(im, (0, i * H)); lg.write(json.dumps({'khung': f[:4], 'nhanh': lab, 'ai_texture': ai}) + '\n')
        S.save(os.path.join(td, f'{k:04d}.png'))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '24', '-i', os.path.join(td, '%04d.png'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '22',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], check=True)
print(OUT, len(frames), 'khung', round(os.path.getsize(OUT) / 1e6, 2), 'MB')
