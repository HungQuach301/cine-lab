#!/opt/cine/bin/python
"""GIỌNG-CHỐT · xuất MP3 nghe: toc-do/G1-moc-speed-1.00|1.03|1.06-A|B.mp3 (móc 0a–0e, v2; lượt A không seed, lượt B cùng seed) + bản kéo nhịp tham khảo và model/X.mp3, model/Y.mp3 (pin 2k–2n, v2 / v4; gán X/Y
ngẫu nhiên bằng secrets → khoa-model.json, KHÔNG mở trước khi nghe). Cùng MỘT chuỗi cho mọi tệp (như casting-my/nghe_mu.py):
mono float → gain về −20 LUFS → chuỗi giọng kênh (highpass 70 Hz, deesser, nén −24 dB 2,5:1) → gain chia đôi tới −14,0 ± 0,1 LUFS → stereo
→ giới hạn đỉnh trên tín hiệu 192 kHz (trần −2 dBFS) → MP3 112 kb/s; đo ebur128 trên chính tệp phát hành (đạt −15,0…−13,8 LUFS, ≤ −1 dBTP)."""
import json, os, secrets, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gc_lib as G
K, L = G.K, G.L
sys.path.insert(0, str(K.R / 'scripts/audio')); import lib as AL
VO = 'highpass=f=70,deesser=i=0.35:m=0.5:f=0.5:s=o,acompressor=threshold=-24dB:ratio=2.5:attack=5:release=120:knee=6'
TRAN = 10 ** (-2.0 / 20); IDX = json.load(open(f'{L.OUT}/thu.json'))


def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)


def xuat(src, out):
    os.makedirs(os.path.dirname(out), exist_ok=True); pre = f'{L.OUT}/{os.path.basename(out)}.vo.wav'
    g0 = -20.0 - float(AL.integrated(AL.dec(src, 1)))
    ff('-i', src, '-af', f'aformat=sample_fmts=fltp:channel_layouts=mono,volume={g0:.3f}dB,{VO}', '-c:a', 'pcm_f32le', pre)
    lo, hi = -10.0, 20.0
    for _ in range(14):
        gain = (lo + hi) / 2
        ff('-i', pre, '-af', f'volume={gain:.3f}dB,pan=stereo|c0=c0|c1=c0,aresample=192000,alimiter=limit={TRAN:.5f}:attack=1:release=60:level=disabled,aresample=44100',
           '-c:a', 'libmp3lame', '-b:a', '112k', '-map_metadata', '-1', out)
        E = AL.ebur128(out)
        if abs(E['I'] + 14) <= 0.1: break
        lo, hi = (gain, hi) if E['I'] < -14 else (lo, gain)
    assert E['TP'] <= -1.0 and -15.0 <= E['I'] <= -13.8, (out, E)
    r = dict(I=E['I'], TP=E['TP'], LRA=E['LRA'], gain_truoc_dB=round(g0, 2), gain_dB=round(gain, 2), giay=round(K.dur(out), 2), sha256=AL.sha256(out), mb=round(os.path.getsize(out) / 1e6, 2))
    print(out, r, flush=True); return r


tom = {}
for s in ('1.00', '1.03', '1.06'):
    for luot, pre in (('A', 'moc'), ('B', 'mocb')): tom[f'toc-do/G1-moc-speed-{s}-{luot}.mp3'] = xuat(IDX[f'{pre}-{s}']['tep'], f'{G.H}/toc-do/G1-moc-speed-{s}-{luot}.mp3')
# tham khảo thêm (0 ký tự): lượt A speed 1,00 kéo nhịp ×1,03 sau thu bằng rubberband (giữ cao độ) — cách nén thời lượng không phụ thuộc lượt thu
keo = f'{L.OUT}/moc-1.00-keo-1.03.wav'
ff('-i', IDX['moc-1.00']['tep'], '-af', 'aformat=channel_layouts=mono,rubberband=tempo=1.03:pitch=1:transients=smooth:detector=soft:phase=laminar:window=standard:smoothing=on:formant=preserved:pitchq=quality:channels=together', '-c:a', 'pcm_f32le', keo)
tom['toc-do/G1-moc-speed-1.00-A-keo-x1.03.mp3'] = xuat(keo, f'{G.H}/toc-do/G1-moc-speed-1.00-A-keo-x1.03.mp3')
tom['phat-am/G1-bang-41-muc.mp3'] = xuat(IDX['bang']['tep'], f'{G.H}/phat-am/G1-bang-41-muc.mp3')   # để tai người: Cádiz, La Línea, isthmus…
KM = f'{G.H}/khoa-model.json'
if os.path.exists(KM): ab = [json.load(open(KM))['G'][x]['ban'] for x in 'XY']   # giữ gán X/Y đã sinh
else: ab = ['pin-v2', 'pin-v4']; j = secrets.randbelow(2); ab = ab if j == 0 else ab[::-1]
khoa = {}
for name, tag in zip('XY', ab):
    khoa[name] = dict(ban=tag, model=IDX[tag]['model'], settings=IDX[tag]['settings'], **xuat(IDX[tag]['tep'], f'{G.H}/model/{name}.mp3'))
json.dump(dict(ghi='KHOÁ MODEL — chỉ mở SAU khi chủ dự án đã nghe X/Y. Gán X/Y bằng secrets.randbelow(2), không chọn tay.', G=khoa), open(f'{G.H}/khoa-model.json', 'w'), ensure_ascii=False, indent=1)
json.dump(dict(chuoi=VO, tran_dBFS=-2.0, tep=tom, model={k: {kk: vv for kk, vv in v.items() if kk not in ('ban', 'model', 'settings')} for k, v in khoa.items()}),
          open(f'{G.H}/xuat.json', 'w'), ensure_ascii=False, indent=1)
