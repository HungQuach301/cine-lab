#!/opt/cine/bin/python
"""KL42 · xuất stem lời: chuẩn −14 LUFS, đỉnh thật ≤ −1 dBTP (khuếch đại tuyến tính + alimiter trên tín hiệu nâng mẫu ×4, trần −1,5 dBFS;
đo lại bằng ffmpeg ebur128, bù tuyến tính nếu lệch > 0,1 LU, ≤ 4 vòng). Không nén/EQ (stem lời để V7 trộn; master.py xử lý lời ở bước trộn).
→ $KL_OUT/xuat/T3-loi-G1-v42-14LUFS.{wav,flac} (master, ngoài git) + reports/kl42/nghe/T3-loi-G1-v42-xem.mp3 (bản xem ≤ 5 MB, trong git);
  stem thô (chưa chuẩn) $KL_OUT/stem/T3-loi-tho.wav; số đo + SHA → xuat.json."""
import json, os, subprocess, sys
import kl_lib as K
sys.path.insert(0, str(K.R / 'scripts/audio')); import lib   # noqa: E402
X = K.OUT / 'xuat'; X.mkdir(exist_ok=True); NG = K.H / 'nghe'; NG.mkdir(exist_ok=True)
SRC = K.OUT / 'stem/T3-loi-tho.wav'; WAV = X / 'T3-loi-G1-v42-14LUFS.wav'; FLAC = X / 'T3-loi-G1-v42-14LUFS.flac'; MP3 = NG / 'T3-loi-G1-v42-xem.mp3'
I_T, TP_T, CEIL = -14.0, -1.0, 0.84   # 0.84 ≈ −1,5 dBFS


def ff(src, dst, af, codec='pcm_s24le'):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-af', af, '-ar', '48000', '-ac', '1', '-c:a', codec, str(dst)], check=True)


m0 = lib.ebur128(str(SRC)); g = I_T - m0['I']; vong = []
for k in range(4):
    ff(SRC, WAV, f'volume={g:.3f}dB,aresample=192000,alimiter=limit={CEIL}:attack=1:release=60:level=false,aresample=48000')
    m = lib.ebur128(str(WAV)); vong.append(dict(gain_db=round(g, 3), **m))
    if abs(m['I'] - I_T) <= 0.1 and m['TP'] <= TP_T: break
    g += I_T - m['I']
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(WAV), '-c:a', 'flac', '-compression_level', '8', str(FLAC)], check=True)
dur = K.dur(WAV); br = min(128, int(4.8e6 * 8 / dur / 1000))   # ≤ 4,8 MB
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(WAV), '-ac', '1', '-c:a', 'libmp3lame', '-b:a', f'{br}k', str(MP3)], check=True)
mm = lib.ebur128(str(MP3))
out = dict(nguon_tho=dict(tep=str(SRC), sha256=lib.sha256(str(SRC)), **m0), vong=vong,
           master=dict(wav=str(WAV), wav_sha256=lib.sha256(str(WAV)), flac=str(FLAC), flac_sha256=lib.sha256(str(FLAC)), giay=round(dur, 3), **vong[-1]),
           ban_xem=dict(tep=str(MP3.relative_to(K.R)), sha256=lib.sha256(str(MP3)), kbps=br, mb=round(os.path.getsize(MP3) / 1e6, 2), **mm))
json.dump(out, open(K.H / 'xuat.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
