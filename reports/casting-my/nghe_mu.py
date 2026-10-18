#!/opt/cine/bin/python
"""CASTING-MỸ · gói nghe mù: nghe_mu.py <ma> … (các giọng ĐẠT máy kiểm + đối chứng DC-G1)
→ nghe-mu/M1.mp3 … Mn.mp3 (thứ tự ngẫu nhiên bằng secrets, Fisher–Yates), khoa-ten.json (M ↔ mã nội bộ; KHÔNG mở trước khi chấm).

Cùng MỘT chuỗi cho mọi tệp (công bằng, gần với tiếng trong phim):
 0. nguồn ứng viên mới = WAV nối 2 đoạn (kiem.py) → MP3 112 kb/s (thế hệ 1, như bản G1 trong gói casting);
    nguồn đối chứng DC-G1 = 0–90,40 s của casting-giong/nghe-mu/G1.mp3 (MP3 112 kb/s thế hệ 1). ⇒ mọi tệp phát hành đều là thế hệ 2, 112 kb/s, cùng dung lượng/giây.
 1. mono, float; gain tuyến tính về −20 LUFS (để bộ nén tác động như nhau dù TTS ra to nhỏ khác nhau — giọng B-kenton ra −30 LUFS, đỉnh/độ to ≈ 25 dB).
 2. chuỗi giọng của kênh (scripts/audio/master.py vo_chain): highpass 70 Hz, deesser, acompressor −24 dB 2,5:1.
 3. gain g (chia đôi tới −14,0 ± 0,1 LUFS), lên stereo không suy hao (pan), giới hạn đỉnh trên tín hiệu nâng mẫu 192 kHz (trần −2 dBFS) → MP3 112 kb/s;
    đo lại ebur128 trên chính tệp phát hành (đạt: −15,0…−13,8 LUFS, ≤ −1 dBTP).
Lần đầu (bỏ): chuỗi casting cũ (gain + alimiter, ứng viên 112 kb/s, đối chứng 192 kb/s) làm một giọng bị nén ≈ 10 dB và lộ tệp đối chứng qua dung lượng."""
import json, os, secrets, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import my_lib as M
K, L = M.K, M.L
sys.path.insert(0, str(K.R / 'scripts/audio')); import lib as AL
H = M.H; os.makedirs(f'{H}/nghe-mu', exist_ok=True)
VO = 'highpass=f=70,deesser=i=0.35:m=0.5:f=0.5:s=o,acompressor=threshold=-24dB:ratio=2.5:attack=5:release=120:knee=6'
TRAN = 10 ** (-2.0 / 20)


def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)


def lufs_mono(p):
    return float(AL.integrated(AL.dec(p, 1)))


ma = sys.argv[1:]; thu_tu = ma[:]
for i in range(len(thu_tu) - 1, 0, -1):
    j = secrets.randbelow(i + 1); thu_tu[i], thu_tu[j] = thu_tu[j], thu_tu[i]
khoa = {}
for i, m in enumerate(thu_tu, 1):
    g = f'M{i}'; meta = json.load(open(f'{L.OUT}/{m}.json')); out = f'{H}/nghe-mu/{g}.mp3'; gen1 = f'{L.OUT}/{m}-gen1.mp3'; pre = f'{L.OUT}/{m}-vo.wav'
    if m == 'DC-G1': ff('-i', meta['nguon'], '-t', '90.40', '-c', 'copy', gen1)
    else: ff('-i', f'{L.OUT}/{m}-noi.wav', '-ac', '1', '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '112k', gen1)
    g0 = -20.0 - lufs_mono(gen1)
    ff('-i', gen1, '-af', f'aformat=sample_fmts=fltp:channel_layouts=mono,volume={g0:.3f}dB,{VO}', '-c:a', 'pcm_f32le', pre)
    lo, hi = -10.0, 20.0
    for _ in range(14):
        gain = (lo + hi) / 2
        ff('-i', pre, '-af', f'volume={gain:.3f}dB,pan=stereo|c0=c0|c1=c0,aresample=192000,alimiter=limit={TRAN:.5f}:attack=1:release=60:level=disabled,aresample=44100',
           '-c:a', 'libmp3lame', '-b:a', '112k', '-map_metadata', '-1', out)
        E = AL.ebur128(out)
        if abs(E['I'] + 14) <= 0.1: break
        lo, hi = (gain, hi) if E['I'] < -14 else (lo, gain)
    assert E['TP'] <= -1.0 and -15.0 <= E['I'] <= -13.8, (g, E)
    khoa[g] = dict(ma=m, voice_id=meta['voice_id'], gain_truoc_dB=round(g0, 2), gain_dB=round(gain, 2), kbps=112, I=E['I'], TP=E['TP'], LRA=E['LRA'],
                   giay=round(K.dur(out), 2), sha256=AL.sha256(out), mb=round(os.path.getsize(out) / 1e6, 2))
    print(g, khoa[g]['I'], khoa[g]['TP'], khoa[g]['LRA'], khoa[g]['mb'], flush=True)
json.dump(dict(ghi='KHOÁ TÊN — chỉ mở SAU khi chủ dự án đã chấm xong. Thứ tự M do secrets.randbelow (Fisher–Yates) sinh, không chọn tay.', chuoi=VO, G=khoa),
          open(f'{H}/khoa-ten.json', 'w'), ensure_ascii=False, indent=1)
