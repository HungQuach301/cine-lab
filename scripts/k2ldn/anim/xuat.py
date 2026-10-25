#!/opt/cine/bin/python
"""ANIMATIC-T4 · việc 8 — XUẤT: (1) animatic đủ = hinh.mp4 + am-nhap.wav (H.264 crf 20 + AAC 160 k, ngoài git, SHA trong xuat.json);
(2) bản xem chia 3 phần ≤ 5 MB/phần (H.264 2 lượt theo bitrate đích + AAC 48 k mono) vào git reports/animatic-t4/xem/;
(3) tờ khung 1 khung/shot (giữa shot) có mã shot + mốc giờ → reports/animatic-t4/to-khung.jpg (+ tờ chia 2 nếu > 2 MB)."""
import hashlib, json, os, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; RP = REPO / 'reports/animatic-t4'; OUT = Path(os.environ.get('ANIM_OUT', '/var/tmp/anim/out'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def mm(t): return f'{int(t // 60)}:{t % 60:04.1f}'
def run(c): subprocess.run(c, check=True)


def main():
    B = json.loads((EP / 'BANG-SHOT-v2.json').read_text()); T = B['tong']['thoi_luong_s']; hinh, am = OUT / 'hinh.mp4', OUT / 'am-nhap.wav'
    du = OUT / 'k2c-t4-02-animatic-640.mp4'
    run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(hinh), '-i', str(am), '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '20', '-preset', 'slow', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '160k', '-t', f'{T:.3f}', '-movflags', '+faststart', str(du)])
    xem = RP / 'xem'; xem.mkdir(parents=True, exist_ok=True)
    # chia 3 phần theo ranh shot gần 1/3 và 2/3
    t0s = [r['t0'] for r in B['shot']]; cuts = [0.0] + [min(t0s, key=lambda x: abs(x - T * k / 3)) for k in (1, 2)] + [T]; parts = []
    for i in range(3):
        a, b = cuts[i], cuts[i + 1]; d = b - a; vb = int((4.75 * 8e6 / d - 48e3) * 0.97); p = xem / f'k2c-t4-02-animatic-xem-{i + 1}.mp4'
        for ps in (1, 2):
            run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{d:.3f}', '-i', str(du), '-c:v', 'libx264', '-b:v', str(vb), '-pass', str(ps), '-passlogfile', str(OUT / f'p{i}'),
                 '-preset', 'slow', '-pix_fmt', 'yuv420p'] + (['-an', '-f', 'mp4', '/dev/null'] if ps == 1 else ['-c:a', 'aac', '-b:a', '48k', '-ac', '1', '-movflags', '+faststart', str(p)]))
        parts.append({'tep': str(p.relative_to(REPO)), 'tu_s': round(a, 3), 'den_s': round(b, 3), 'bytes': p.stat().st_size, 'sha256': sha(p), 'video_bps': vb})
    # tờ khung
    sh = B['shot']; cols = 6; w, h = 320, 180; rows = (len(sh) + cols - 1) // cols; S = Image.new('RGB', (cols * w, rows * (h + 20)), (20, 20, 22)); g = ImageDraw.Draw(S)
    F = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 12)
    for i, r in enumerate(sh):
        t = (r['t0'] + r['t1']) / 2; fp = OUT / f'tk_{i:03d}.jpg'
        run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-ss', f'{t:.3f}', '-i', str(hinh), '-frames:v', '1', '-vf', f'scale={w}:{h}', str(fp)])
        x, y = (i % cols) * w, (i // cols) * (h + 20); S.paste(Image.open(fp), (x, y + 20))
        g.text((x + 4, y + 3), f"{r['ma']}  {mm(r['t0'])}–{mm(r['t1'])}  {r['cu_may']}  (@{mm(t)})", fill=(255, 225, 110), font=F)
    tk = RP / 'to-khung.jpg'; S.save(tk, quality=80)
    rec = {'animatic': {'tep': str(du), 'sha256': sha(du), 'bytes': du.stat().st_size, 'giay': T, 'ngoai_git': True,
                        'tai_tao': 'scripts/k2ldn/anim/du_lieu.sh → dung.sh (tệp máy animatic/may) → md (omni/chon + clip) → tn_tl.sh → am.py → ghep.py → xuat.py'},
           'hinh': {'sha256': sha(hinh)}, 'am': {'sha256': sha(am)}, 'xem': parts, 'to_khung': {'tep': str(tk.relative_to(REPO)), 'bytes': tk.stat().st_size}}
    (RP / 'xuat.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1)); print(json.dumps(rec, ensure_ascii=False)[:1200])


if __name__ == '__main__': main()
