#!/opt/cine/bin/python
"""KL42 · xuất stem lời: chuẩn −14 LUFS, đỉnh thật ≤ −1 dBTP (khuếch đại tuyến tính + alimiter trên tín hiệu nâng mẫu ×4, trần −1,5 dBFS;
đo lại bằng ffmpeg ebur128, bù tuyến tính nếu lệch > 0,1 LU, ≤ 4 vòng). Không nén/EQ (stem lời để V7 trộn; master.py xử lý lời ở bước trộn).
→ $KL_OUT/xuat/T3-loi-G1-v42-14LUFS.{wav,flac} (master, ngoài git) + reports/kl42/nghe/T3-loi-G1-v42-xem-{1,2}-*.mp3 (bản xem 2 tệp ≤ 5 MB, trong git);
  stem thô (chưa chuẩn) $KL_OUT/stem/T3-loi-tho.wav; số đo + SHA → xuat.json."""
import json, os, subprocess, sys
import kl_lib as K
sys.path.insert(0, str(K.R / 'scripts/audio')); import lib   # noqa: E402
X = K.OUT / 'xuat'; X.mkdir(exist_ok=True); NG = K.H / 'nghe'; NG.mkdir(exist_ok=True)
SRC = K.OUT / 'stem/T3-loi-tho.wav'; WAV = X / 'T3-loi-G1-v42-14LUFS.wav'; FLAC = X / 'T3-loi-G1-v42-14LUFS.flac'
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
dur = K.dur(WAV); M = json.loads((K.OUT / 'stem/moc.json').read_text()); C = M['chuong']
# bản xem: 2 tệp MP3 96 kb/s (mỗi tệp ≤ 5 MB) — chương 00–02 và 03–05, cắt ở giữa khoảng lặng 2 s giữa chương 02 và 03.
# MP3 làm vọt đỉnh thật (BAI-HOC #69) → đo trên CHÍNH tệp MP3; đỉnh > −1 dBTP thì hạ trần limiter; I lệch > 0,3 LU thì bù tuyến tính (≤ 6 vòng).
cat = C[3]['bd_stem'] - M['gap_chuong'] / 2; PH = [('T3-loi-G1-v42-xem-1-ch00-02.mp3', 0.0, cat), ('T3-loi-G1-v42-xem-2-ch03-05.mp3', cat, dur)]
xem = []
for ten, t0, t1 in PH:
    f = NG / ten; gx, cx, vx = 0.0, CEIL, []
    for k in range(6):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-to', f'{t1:.3f}', '-i', str(WAV), '-af',
                        f'volume={gx:.3f}dB,aresample=192000,alimiter=limit={cx:.3f}:attack=1:release=60:level=false,aresample=48000',
                        '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '96k', str(f)], check=True)
        mm = lib.ebur128(str(f)); vx.append(dict(gain_db=round(gx, 3), tran=round(cx, 3), **mm))
        if mm['TP'] <= TP_T and abs(mm['I'] - I_T) <= 0.3: break
        if mm['TP'] > TP_T: cx *= 10 ** ((TP_T - mm['TP'] - 0.2) / 20)
        if abs(mm['I'] - I_T) > 0.3: gx += I_T - mm['I']
    xem.append(dict(tep=str(f.relative_to(K.R)), sha256=lib.sha256(str(f)), tu=round(t0, 3), den=round(t1, 3), kbps=96, mb=round(os.path.getsize(f) / 1e6, 2), vong=vx, **mm))
for old in NG.glob('T3-loi-G1-v42-xem.mp3'): old.unlink()
out = dict(nguon_tho=dict(tep=str(SRC), sha256=lib.sha256(str(SRC)), **m0), vong=vong,
           master=dict(wav=str(WAV), wav_sha256=lib.sha256(str(WAV)), flac=str(FLAC), flac_sha256=lib.sha256(str(FLAC)), giay=round(dur, 3), **vong[-1]),
           ban_xem=xem)
json.dump(out, open(K.H / 'xuat.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
