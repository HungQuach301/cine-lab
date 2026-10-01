#!/usr/bin/env python3
"""Cine Lab · Last Lamplighters · animatic v3 — dựng âm thanh cả tập (tất định), mở rộng từ am_thanh.py của lát cắt M2.2a.

- Lời dẫn Bill nguyên bản theo reports/m3/m2-2b/timeline-v3.json (lọc thấp 70 Hz + nén nhẹ 3:1; KHÔNG atempo, không cắt giữa câu).
  Đoạn 19: tách take ở khoảng lặng giữa hai phần (trường `tach`), lùi phần B thêm `chen_lang_s`, nối bằng fade 20 ms.
- Thoại Ida (C4-D1 L1, L2) theo trường `ida`, chuẩn riêng về −18 LUFS (take gốc nóng hơn lời Bill, gây đỉnh +7 dBTP trước limiter ở bản thử).
- Nhạc: M3-MUS-1 "Immersed" lặp (giao 4 s) tới đoạn 19; M3-MUS-2 "Reawakening" từ đoạn 19 (giao 3 s); hạ 12 dB khi có lời
  (đường bao từ mốc ký tự + thoại), vào 1,5 s, ra 3 s ở cuối.
- SFX: mọi cue trong <thư mục sfx>/*.json (do xưởng ghi, at_abs giây tuyệt đối), fade_ms mặc định 8.
- Master: −14 LUFS tích hợp, true peak ≤ −1 dBTP (limiter trên tín hiệu nâng mẫu ×4).

/opt/cine/bin/python scripts/p/mix_ep01.py <timeline.json> <thư mục sfx> <ra.wav>
Ghi <ra>.json: khoảng lời, mức đo trước/sau, mức hạ nhạc đo thật, danh sách SFX đã đặt.
"""
import glob, json, os, subprocess, sys
import numpy as np

SR = 48000
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
tl_p, sfx_d, out_p = sys.argv[1:4]
TL = json.load(open(tl_p))
DUR = TL['tong_s']
N = int(round(DUR * SR))
t = np.arange(N) / SR


def P(p): return p if os.path.isabs(p) else os.path.join(REPO, p)


def dec(p, ch, af=None, ss=None, dur=None):
    cmd = ['ffmpeg', '-v', 'error', '-nostdin']
    if ss is not None: cmd += ['-ss', str(ss)]
    if dur is not None: cmd += ['-t', str(dur)]
    cmd += ['-i', P(p)] + (['-af', af] if af else []) + ['-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-']
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)
    return a.reshape(-1, ch).astype(np.float64)


def lufs(x):   # x: (n, 2)
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(x)


def put(dst, src, at):
    k = int(round(at * SR)); m = min(len(src), len(dst) - k)
    if m > 0: dst[k:k + m] += src[:m]


VO_AF = 'highpass=f=70,acompressor=threshold=-26dB:ratio=3:attack=6:release=160:knee=4'
vo = np.zeros(N); ida_st = np.zeros((N, 2)); seg = []
def add_seg(a, b):
    seg.append([a, b])

for d in TL['doan']:
    a0 = d['t0'] + d['vo_offset']
    x = dec(d['vo_file'], 1, VO_AF)[:, 0]
    al_p = P(d['vo_file']).replace('.mp3', '.align.json')
    al = json.load(open(al_p))
    cs, ce, chs = al['character_start_times_seconds'], al['character_end_times_seconds'], al['characters']
    shift_from, shift = None, 0.0
    if 'tach' in d:   # đoạn 19: lùi phần B
        cut, shift = d['tach']['cat_tai_giay_trong_take'], d['tach']['chen_lang_s']
        kc = int(cut * SR); fl = int(0.02 * SR)
        A, B = x[:kc].copy(), x[kc:].copy()
        A[-fl:] *= np.linspace(1, 0, fl); B[:fl] *= np.linspace(0, 1, fl)
        put(vo, A, a0); put(vo, B, a0 + cut + shift); shift_from = cut
    else:
        put(vo, x, a0)
    for c, s, e in zip(chs, cs, ce):
        if c.isspace(): continue
        off = shift if (shift_from is not None and s >= shift_from) else 0.0
        add_seg(a0 + s + off, a0 + e + off)
    for il in d.get('ida', []):
        y = dec(il['file'], 1, 'highpass=f=80,acompressor=threshold=-24dB:ratio=4:attack=1:release=120:knee=4')[:, 0]
        y2 = np.stack([y, y], 1); y2 *= 10 ** ((-18.0 - lufs(y2)) / 20)   # thoại Ida chuẩn riêng: −18 LUFS (thấp hơn lời Bill 1 dB)
        put(ida_st, y2, d['t0'] + il['at'])
        add_seg(d['t0'] + il['at'], d['t0'] + il['at'] + len(y) / SR)

seg.sort(); mseg = []
for a, b in seg:
    if mseg and a - mseg[-1][1] < 0.55: mseg[-1][1] = max(mseg[-1][1], b)
    else: mseg.append([a, b])

# nhạc
t19 = [d for d in TL['doan'] if d['n'] == '19'][0]['t0']
imm = dec('reports/m3/m2-2b/music/Immersed.mp3', 2); rea = dec('reports/m3/m2-2b/music/Reawakening.mp3', 2)
XF = int(4 * SR)
bed = imm.copy()
while len(bed) < int((t19 + 3) * SR):
    w = np.linspace(0, 1, XF)[:, None]
    bed = np.concatenate([bed[:-XF], bed[-XF:] * (1 - w) + imm[:XF] * w, imm[XF:]])
bed = bed[:int((t19 + 3) * SR)]
mus = np.zeros((N, 2))
X3 = int(3 * SR); w3 = np.linspace(0, 1, X3)[:, None]
k19 = int((t19 - 0) * SR)
mus[:k19] = bed[:k19]
mus[k19:k19 + X3] = bed[k19:k19 + X3] * (1 - w3)
r = rea[:N - k19]; r = r.copy(); r[:X3] *= w3[:len(r[:X3])]
mus[k19:k19 + len(r)] += r
# chuẩn mức stem nhạc: −24 LUFS ở chỗ lặng (trước đường bao)
mus *= 10 ** ((-24.0 - lufs(mus[: int(min(N, 240 * SR))])) / 20)
DUCK = -12.0
env = np.zeros(N)
for a, b in mseg:
    i0, i1 = max(0, int((a - 0.6) * SR)), min(N, int((b + 0.6) * SR))
    tt = t[i0:i1]
    u = np.clip(np.minimum((tt - (a - 0.2)) / 0.2, ((b + 0.25) - tt) / 0.25), 0, 1); u = u * u * (3 - 2 * u)
    env[i0:i1] = np.minimum(env[i0:i1], DUCK * u)
fade = np.clip(t / 1.5, 0, 1) * np.clip((DUR - t) / 3.0, 0, 1)
mus_st = mus * (10 ** (env / 20))[:, None] * fade[:, None]

# lời: chuẩn về −17 LUFS (vùng có lời)
vo_st = np.stack([vo, vo], 1)
mask = np.zeros(N, bool)
for a, b in mseg: mask[int(a * SR):int(b * SR)] = True
vo_st *= 10 ** ((-17.0 - lufs(vo_st[mask])) / 20)

# SFX
sfx = np.zeros((N, 2)); sfx_log = []
for f in sorted(glob.glob(os.path.join(sfx_d, '*.json'))):
    for c in json.load(open(f)):
        s = dec(c['file'], 2, ss=c.get('src_ss', 0), dur=c.get('dur')); n = len(s)
        if n == 0: continue
        fl = max(1, int(c.get('fade_ms', 8) / 1000 * SR)); w = np.ones(n)
        w[:fl] = np.linspace(0, 1, fl); w[-fl:] = np.linspace(1, 0, fl)
        put(sfx, s * w[:, None] * 10 ** (c.get('gain_db', 0) / 20), c['at_abs'])
        sfx_log.append(dict(json=os.path.basename(f), **c))

mix = (vo_st + ida_st + mus_st + sfx * 10 ** (-6 / 20)).astype(np.float32)
raw = out_p.replace('.wav', '.pre.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_f32le', raw], input=mix.tobytes(), check=True)


def meas(p):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', p, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = r[r.rfind('Summary:'):]; g = lambda k: float(s.split(k)[1].split()[0])
    return dict(I=g('I:'), LRA=g('LRA:'), TP=g('Peak:'))


m0 = meas(raw); gain = -14.0 - m0['I']
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', f'volume={gain:.3f}dB,aresample=192000,alimiter=limit=0.83:attack=1:release=60:level=disabled,aresample=48000',
                '-c:a', 'pcm_s24le', out_p], check=True)
m1 = meas(out_p)
db = lambda x: 10 * np.log10(np.mean(x ** 2) + 1e-20)
inside = env <= DUCK + 0.01; quiet = (env >= -1.0) & (t > 2) & (t < DUR - 3)
duck_meas = db(mus[inside] * (10 ** (env[inside] / 20))[:, None]) - db(mus[inside])
rec = dict(tong_s=DUR, so_khoang_loi=len(mseg), pre=m0, gain_db=round(gain, 2), master=m1, duck_env_db=DUCK,
           duck_do_tren_cung_mau_db=round(duck_meas, 2), sfx=sfx_log, khoang_loi=mseg)
json.dump(rec, open(out_p.replace('.wav', '.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: rec[k] for k in ('tong_s', 'so_khoang_loi', 'pre', 'gain_db', 'master', 'duck_do_tren_cung_mau_db')}, ensure_ascii=False), len(sfx_log), 'sfx')
