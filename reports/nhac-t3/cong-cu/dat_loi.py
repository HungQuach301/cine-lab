"""NHẠC-T3 · dựng stem lời trên TRỤC PHIM (phương án B 745,0 s) cho một đoạn [t0, t1) từ 2 MP3 xem của KL42.
Lý do: stem WAV/FLAC của KL42 nằm ngoài git và đã mất theo container; lệnh cho dùng 2 MP3 xem (−14,2 LUFS, chuẩn tuyến tính + alimiter, 96 kb/s).
Mỗi shot: lấy khoảng [bd_stem, kt_stem] (mốc trong stem T3-loi-tho.wav) đặt tại loi_bd_phim (nhip-that.json). Khoảng nối chương 2,0 s giữa các chương
trong stem không dùng. MP3 xem 1 = stem 0 → 392,912 s; MP3 xem 2 = stem 392,912 → hết.
Trả (vo mono float32 48 kHz, speech [(a,b)] theo giây tương đối t0)."""
import json, subprocess, numpy as np
SR = 48000
def dec(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32)
def dung(nhip, xem1, xem2, t0, t1, pad=0.12):
    d = json.load(open(nhip)); a1, a2 = dec(xem1), dec(xem2); cut = 392.912
    def stem(a, b):   # mỗi shot nằm trọn trong một chương → trọn trong một tệp xem
        if b <= cut + 0.2: return a1[int(a * SR):min(int(b * SR), len(a1))]
        return a2[int(max(a - cut, 0) * SR):int((b - cut) * SR)]
    N = int(round((t1 - t0) * SR)); vo = np.zeros(N, np.float32); sp = []
    for s in d['shot']:
        bt = s.get('ban_thu') or {}
        if not s.get('cau') or 'bd_stem' not in bt: continue
        off = s['loi_bd_phim'] - bt['bd_stem']          # stem → phim
        a, b = max(0.0, bt['bd_stem'] - pad), bt['kt_stem'] + pad
        fa, fb = a + off, b + off
        if fb <= t0 or fa >= t1: continue
        x = stem(a, b).copy(); n = len(x); r = int(0.01 * SR)
        x[:r] *= np.linspace(0, 1, r); x[-r:] *= np.linspace(1, 0, r)
        i = int(round((fa - t0) * SR)); j0 = max(0, -i); i = max(0, i); m = min(n - j0, N - i)
        if m > 0: vo[i:i + m] += x[j0:j0 + m]
        for c in s['cau']:
            ca, cb = max(c['bd_phim'], t0) - t0, min(c['kt_phim'], t1) - t0
            if cb > ca: sp.append((round(ca, 3), round(cb, 3)))
    return vo, sorted(sp)
