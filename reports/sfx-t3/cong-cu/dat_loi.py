"""SFX-T3 · dựng stem lời G1 trên TRỤC PHIM (761 s) cho đoạn [t0, t1) từ MASTER FLAC LFS (channel-k2/k2c-t3-01/am-thanh/master/
T3-loi-G1-v42-14LUFS.flac, SHA 852b9e41…) theo channel-k2/k2c-t3-01/animatic/anim-loi.json (mỗi dòng: [bd_stem, kt_stem] → bd_phim).
Khác NHẠC-T3 (dựng từ 2 MP3 xem 96 kb/s): ở đây dùng master FLAC thật, nên SMR đo được là số trên master giọng.
Khoảng lời (speech) lấy từ reports/kl42/nhip-that.json → cau[].bd_phim/kt_phim (trùng mốc anim-loi: 0b 6,669 = 6,669 …).
Trả (vo mono float32 48 kHz, speech [(a,b)] giây tương đối t0)."""
import json, os, subprocess, numpy as np
SR = 48000
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
FLAC = os.path.join(ROOT, 'channel-k2/k2c-t3-01/am-thanh/master/T3-loi-G1-v42-14LUFS.flac')
ANIM = os.path.join(ROOT, 'channel-k2/k2c-t3-01/animatic/anim-loi.json')
NHIP = os.path.join(ROOT, 'reports/kl42/nhip-that.json')
_cache = {}
def stem():
    if 'x' not in _cache:
        r = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', FLAC, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True)
        _cache['x'] = np.frombuffer(r.stdout, np.float32)
    return _cache['x']
def dung(t0, t1, pad=0.12):
    a1 = stem(); A = json.load(open(ANIM)); N = int(round((t1 - t0) * SR)); vo = np.zeros(N, np.float32)
    for d in A['dong']:
        a, b = max(0.0, d['bd_stem'] - pad), d['kt_stem'] + pad; off = d['bd_phim'] - d['bd_stem']; fa, fb = a + off, b + off
        if fb <= t0 or fa >= t1: continue
        x = a1[int(a * SR):int(b * SR)].copy(); n = len(x); r = int(0.01 * SR)
        x[:r] *= np.linspace(0, 1, r); x[-r:] *= np.linspace(1, 0, r)
        i = int(round((fa - t0) * SR)); j0 = max(0, -i); i = max(0, i); m = min(n - j0, N - i)
        if m > 0: vo[i:i + m] += x[j0:j0 + m]
    sp = []
    for s in json.load(open(NHIP))['shot']:
        for c in s.get('cau', []):
            ca, cb = max(c['bd_phim'], t0) - t0, min(c['kt_phim'], t1) - t0
            if cb > ca: sp.append((round(ca, 3), round(cb, 3)))
    return vo, sorted(sp)
