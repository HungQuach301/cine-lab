#!/opt/cine/bin/python
"""Last Lamplighters · nhà máy — dựng âm thanh một tập hoặc một Short từ timeline của ll.py (tổng quát hoá scripts/p/mix_ep01.py).

  mix.py <timeline.json> <ra.wav> [--short ID]

- Lời Bill nguyên bản (lọc thấp 70 Hz, nén nhẹ 3:1; không atempo), chuẩn −17 LUFS vùng có lời.
- Nhạc: danh sách music [{file, from: id đoạn, xfade}] — lặp có giao 4 s, giao 3 s khi đổi bài; hạ 12 dB khi có lời; vào 1,5 s, ra 3 s.
  Short: dùng bài đầu, cùng luật hạ nhạc.
- SFX: cue trong timeline (mẫu tự sinh: lật/trượt giấy khi chuyển thẻ, đèn khí xì khi đèn bừng) + cue khai tay.
- Master: −14 LUFS tích hợp, true peak ≤ −1 dBTP (limiter trên tín hiệu nâng mẫu ×4). Ghi <ra>.json số đo.
"""
import json, os, subprocess, sys
import numpy as np
import pyloudnorm as pyln

SR = 48000
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda p: p if os.path.isabs(p) else os.path.join(REPO, p)
tl_p, out_p = sys.argv[1:3]; SHORT = sys.argv[sys.argv.index('--short') + 1] if '--short' in sys.argv else None
TL = json.load(open(tl_p))
SEGS = [s for s in TL['shorts'] if s['id'] == SHORT] if SHORT else TL['segments']
DUR = SEGS[0]['t1'] if SHORT else TL['tong_s']
N = int(round(DUR * SR)); t = np.arange(N) / SR


def dec(p, ch, af=None, ss=None, dur=None):
    cmd = ['ffmpeg', '-v', 'error', '-nostdin'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(dur)] if dur is not None else [])
    cmd += ['-i', P(p)] + (['-af', af] if af else []) + ['-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, ch).astype(np.float64)


lufs = lambda x: pyln.Meter(SR).integrated_loudness(x)


def put(dst, src, at):
    k = int(round(at * SR)); m = min(len(src), len(dst) - k)
    if m > 0 and k >= 0: dst[k:k + m] += src[:m]


vo = np.zeros(N); seg = []
for d in SEGS:
    if not d.get('vo_file'): continue
    x = dec(d['vo_file'], 1, 'highpass=f=70,acompressor=threshold=-26dB:ratio=3:attack=6:release=160:knee=4')[:, 0]
    put(vo, x, d['t0'] + d['vo_offset'])
    seg += [[d['t0'] + a, d['t0'] + b] for a, b in d['speech']]
seg.sort(); mseg = []
for a, b in seg:
    if mseg and a - mseg[-1][1] < 0.55: mseg[-1][1] = max(mseg[-1][1], b)
    else: mseg.append([a, b])

# nhạc
mus = np.zeros((N, 2)); M = TL.get('music') or []
if M:
    starts = [0.0] if SHORT else [next((s['t0'] for s in SEGS if s['id'] == m.get('from')), 0.0) for m in M]
    for i, m in enumerate(M[:1] if SHORT else M):
        a0, a1 = starts[i], (starts[i + 1] if i + 1 < len(starts) else DUR) + (m.get('xfade', 3) if i + 1 < len(starts) else 0)
        src = dec(m['file'], 2); need = int((a1 - a0) * SR); XF = int(4 * SR); bed = src.copy()
        while len(bed) < need:
            w = np.linspace(0, 1, XF)[:, None]; bed = np.concatenate([bed[:-XF], bed[-XF:] * (1 - w) + src[:XF] * w, src[XF:]])
        bed = bed[:need].copy(); X3 = int(min(3, (a1 - a0) / 2) * SR)
        if i > 0: bed[:X3] *= np.linspace(0, 1, X3)[:, None]
        if i + 1 < len(starts): bed[-X3:] *= np.linspace(1, 0, X3)[:, None]
        put(mus, bed, a0)
    q = mus[:int(min(N, 240 * SR))]; mus *= 10 ** ((-24.0 - lufs(q)) / 20)
DUCK = -12.0; env = np.zeros(N)
for a, b in mseg:
    i0, i1 = max(0, int((a - 0.6) * SR)), min(N, int((b + 0.6) * SR)); tt = t[i0:i1]
    u = np.clip(np.minimum((tt - (a - 0.2)) / 0.2, ((b + 0.25) - tt) / 0.25), 0, 1); u = u * u * (3 - 2 * u)
    env[i0:i1] = np.minimum(env[i0:i1], DUCK * u)
fade = np.clip(t / 1.5, 0, 1) * np.clip((DUR - t) / (1.2 if SHORT else 3.0), 0, 1)
mus_st = mus * (10 ** (env / 20))[:, None] * fade[:, None]

vo_st = np.stack([vo, vo], 1); mask = np.zeros(N, bool)
for a, b in mseg: mask[int(a * SR):int(b * SR)] = True
if mask.any(): vo_st *= 10 ** ((-17.0 - lufs(vo_st[mask])) / 20)

sfx = np.zeros((N, 2)); log = []
for d in SEGS:
    for c in d.get('sfx', []):
        s = dec(c['file'], 2, ss=c.get('src_ss', 0), dur=c.get('dur')); n = len(s)
        if not n: continue
        fl = max(1, min(n // 2, int(c.get('fade_ms', 8) / 1000 * SR))); w = np.ones(n); w[:fl] = np.linspace(0, 1, fl); w[-fl:] = np.linspace(1, 0, fl)
        put(sfx, s * w[:, None] * 10 ** (c.get('gain_db', 0) / 20), c['at_abs']); log.append(c)

mix = (vo_st + mus_st + sfx * 10 ** (-6 / 20)).astype(np.float32)
raw = out_p.replace('.wav', '.pre.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_f32le', raw], input=mix.tobytes(), check=True)


def meas(p):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', p, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = r[r.rfind('Summary:'):]; g = lambda k: float(s.split(k)[1].split()[0]); return dict(I=g('I:'), LRA=g('LRA:'), TP=g('Peak:'))


m0 = meas(raw); gain = -14.0 - m0['I']
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', f'volume={gain:.3f}dB,aresample=192000,alimiter=limit=0.83:attack=1:release=60:level=disabled,aresample=48000',
                '-c:a', 'pcm_s24le', out_p], check=True)
os.remove(raw); m1 = meas(out_p)
rec = dict(tong_s=DUR, so_khoang_loi=len(mseg), pre=m0, gain_db=round(gain, 2), master=m1, duck_db=DUCK, so_sfx=len(log), khoang_loi=mseg)
json.dump(rec, open(out_p.replace('.wav', '.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: rec[k] for k in ('tong_s', 'so_khoang_loi', 'master', 'so_sfx')}, ensure_ascii=False))
