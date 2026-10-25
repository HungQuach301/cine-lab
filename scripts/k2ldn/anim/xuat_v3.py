#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · việc 7 — XUẤT v3: (1) animatic đủ 640×360 = hinh.mp4 + am-nhap.wav (H.264 crf 20 + AAC 192 k, ngoài git, SHA + lệnh tái tạo trong xuat.json);
(2) bản xem 4 phần ≤ 5 MB/phần vào git reports/animatic-t4-v2/xem/ — F5: âm AAC 128 kb/s (stereo), đỉnh thật ≤ −1 dBTP ĐO TRÊN CHÍNH TỆP XEM (ebur128 peak=true sau giải mã;
nếu > −1,0 thì hạ 0,5 dB + alimiter rồi mã lại, ≤ 4 lần); hình H.264 2 lượt theo bitrate còn lại; (3) tờ khung 1 khung/shot + tờ khung mỗi 10 s (tự soi việc 8)."""
import hashlib, json, os, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; RP = REPO / 'reports/animatic-t4-v2'; OUT = Path(os.environ.get('ANIM_OUT', '/var/tmp/anim/out3'))
A_KBPS, MAXB, PHAN = 132, 4_950_000, 4   # đặt 132 k để tốc độ âm ĐO trên tệp ≥ 128 kb/s (lượt 1 với 128 k: một phần đo 127,97 k)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def mm(t): return f'{int(t // 60)}:{t % 60:04.1f}'
def run(c): subprocess.run(c, check=True)
def do(p, extra=''):
    o = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-i', str(p), '-af', 'ebur128=peak=true' + extra, '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(o.split('I:')[-1].split('LUFS')[0]), float(o.split('Peak:')[-1].split('dBFS')[0])


def main():
    B = json.loads((EP / 'BANG-SHOT-v3.json').read_text()); T = B['tong']['thoi_luong_s']; hinh, am = OUT / 'hinh.mp4', OUT / 'am-nhap.wav'
    du = OUT / 'k2c-t4-02-animatic-v3-640.mp4'
    if not (os.environ.get('XEM_CHI') and du.exists()):   # XEM_CHI=1: giữ animatic đủ đã xuất, chỉ làm lại bản xem
        run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(hinh), '-i', str(am), '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '20', '-preset', 'slow', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-b:a', '192k', '-t', f'{T:.3f}', '-movflags', '+faststart', str(du)])
    I_du, TP_du = do(du)
    xem = RP / 'xem'; xem.mkdir(parents=True, exist_ok=True)
    t0s = [r['t0'] for r in B['shot']]; cuts = [0.0] + [min(t0s, key=lambda x: abs(x - T * k / PHAN)) for k in range(1, PHAN)] + [T]; parts = []
    for i in range(PHAN):
        a, b = cuts[i], cuts[i + 1]; d = b - a; p = xem / f'k2c-t4-02-animatic-v3-xem-{i + 1}.mp4'; gain = -1.2; lan = []
        vb = int((MAXB * 8 / d - A_KBPS * 1000) * 0.96)
        for k in range(5):
            af = f'volume={gain}dB,aresample=192000,alimiter=limit=0.82:level=false:attack=1:release=50,aresample=48000'
            for ps in (1, 2):
                run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{d:.3f}', '-i', str(du), '-c:v', 'libx264', '-b:v', str(vb), '-pass', str(ps), '-passlogfile', str(OUT / f'p{i}'),
                     '-preset', 'slow', '-pix_fmt', 'yuv420p'] + (['-an', '-f', 'mp4', '/dev/null'] if ps == 1 else ['-af', af, '-c:a', 'aac', '-b:a', f'{A_KBPS}k', '-ac', '2', '-movflags', '+faststart', str(p)]))
            I, TP = do(p); lan.append({'gain_dB': gain, 'I_LUFS': I, 'TP_dBTP': TP, 'bytes': p.stat().st_size})
            if p.stat().st_size > 5_000_000: vb = int(vb * 0.93); continue
            if TP <= -1.0: break
            gain -= 0.5
        ab = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=bit_rate', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout.strip() or 0)
        parts.append({'tep': str(p.relative_to(REPO)), 'tu_s': round(a, 3), 'den_s': round(b, 3), 'bytes': p.stat().st_size, 'sha256': sha(p), 'video_bps': vb, 'am_bps_do': ab, 'am_kbps_dat': A_KBPS,
                      'I_LUFS_tren_tep_xem': lan[-1]['I_LUFS'], 'TP_dBTP_tren_tep_xem': lan[-1]['TP_dBTP'], 'lan_ma': lan})
    F = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 12)
    def to(ts, nhan, ra, cols=6, w=320, h=180):
        rows = (len(ts) + cols - 1) // cols; S = Image.new('RGB', (cols * w, rows * (h + 20)), (20, 20, 22)); g = ImageDraw.Draw(S)
        for i, (t, lab) in enumerate(zip(ts, nhan)):
            fp = OUT / f'tk_{i:03d}.jpg'; run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-ss', f'{t:.3f}', '-i', str(hinh), '-frames:v', '1', '-vf', f'scale={w}:{h}', str(fp)])
            x, y = (i % cols) * w, (i // cols) * (h + 20); S.paste(Image.open(fp), (x, y + 20)); g.text((x + 4, y + 3), lab, fill=(255, 225, 110), font=F)
        S.save(ra, quality=78); return ra
    sh = B['shot']; tk = to([(r['t0'] + r['t1']) / 2 for r in sh], [f"{r['ma']}  {mm(r['t0'])}–{mm(r['t1'])}  {r['cu_may']} {r['goc']}" for r in sh], RP / 'to-khung.jpg')
    ts10 = [t + 0.5 for t in range(0, int(T), 10)]
    def ma_at(t): return next(r['ma'] for r in sh if r['t0'] <= t < r['t1'])
    tk10 = to(ts10, [f"@{mm(t)}  {ma_at(t)}" for t in ts10], RP / 'to-khung-10s.jpg', cols=8, w=240, h=135)
    rec = {'animatic': {'tep': str(du), 'sha256': sha(du), 'bytes': du.stat().st_size, 'giay': T, 'ngoai_git': True, 'I_LUFS': I_du, 'TP_dBTP': TP_du,
                        'tai_tao': 'du_lieu.sh (+ nướng 14 mốc) → may_v3.py → dung3.sh (animatic2/may) → md_v3.sh (animatic2/omni/chon + clip; clip v1 theo cột md_clip) → tn.py prep/ghep/tl (P9-2026) → giong/tai_tao.sh → loi_dung.py → loi_v3.py dung → am_v3.py → ghep_v3.py → xuat_v3.py'},
           'hinh': {'sha256': sha(hinh)}, 'am': {'sha256': sha(am)}, 'xem': parts, 'to_khung': {'tep': str(tk.relative_to(REPO)), 'bytes': tk.stat().st_size}, 'to_khung_10s': {'tep': str(tk10.relative_to(REPO)), 'bytes': tk10.stat().st_size}}
    (RP / 'xuat.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1)); print(json.dumps({'du': rec['animatic']['sha256'][:12], 'xem': [(x['bytes'], x['TP_dBTP_tren_tep_xem'], x['am_bps_do']) for x in parts]}, ensure_ascii=False))


if __name__ == '__main__': main()
