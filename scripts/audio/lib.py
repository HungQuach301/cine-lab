"""ÂM THANH · thư viện chung (phiên Âm thanh, Mốc C, 15/10/2026).

Giải mã/ghi PCM qua ffmpeg, đo loudness theo ITU-R BS.1770-4 / EBU R128 (lọc K tự tính để có đường loudness theo thời gian),
đỉnh thật bằng ffmpeg ebur128 (nâng mẫu ×4), đo hai lượt bằng ffmpeg loudnorm. Không gọi mạng.
"""
import json, os, subprocess
import numpy as np
from scipy.signal import lfilter

SR = 48000
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
P = lambda p: p if os.path.isabs(p) else (os.path.abspath(p) if os.path.exists(p) and not os.path.exists(os.path.join(REPO, p)) else os.path.join(REPO, p))

# Lọc K (BS.1770-4) ở 48 kHz: kệ cao + lọc thông cao RLB
_KB1, _KA1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
_KB2, _KA2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]


def dec(path, ch=2, af=None, ss=None, dur=None, sr=SR, dtype=np.float64):
    """giải mã thành mảng (N, ch) — float64 mặc định; float32 cho tín hiệu dài (tiết kiệm bộ nhớ)"""
    cmd = ['ffmpeg', '-v', 'error', '-nostdin'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(dur)] if dur is not None else [])
    cmd += ['-i', P(path)] + (['-af', af] if af else []) + ['-ac', str(ch), '-ar', str(sr), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, ch).astype(dtype)


def write(path, x, codec='pcm_s24le', sr=SR, extra=()):
    x = np.atleast_2d(x.T).T if x.ndim == 1 else x
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', str(x.shape[1]), '-i', '-', *extra, '-c:a', codec, path],
                   input=np.ascontiguousarray(x, np.float32).tobytes(), check=True)


def kw(x):
    """tín hiệu đã lọc K, (N, ch)"""
    x = x if x.ndim == 2 else x[:, None]
    return lfilter(_KB2, _KA2, lfilter(_KB1, _KA1, x, axis=0), axis=0).astype(x.dtype if x.dtype == np.float32 else np.float64)


def power(x, win, hop, sr=SR, weighted=True):
    """công suất trung bình (tổng kênh) của từng cửa sổ — mảng (n,), tâm cửa sổ ở (i*hop + win/2)/sr"""
    y = kw(x) if weighted else (x if x.ndim == 2 else x[:, None])
    e = (y.astype(np.float64) ** 2).sum(1); del y; c = np.concatenate([[0.0], np.cumsum(e)]); W, H = int(win * sr), int(hop * sr)
    if len(e) < W: return np.array([e.mean() if len(e) else 0.0])
    st = np.arange(0, len(e) - W + 1, H); return (c[st + W] - c[st]) / W


def lu(p):
    return -0.691 + 10 * np.log10(np.maximum(p, 1e-20))


def integrated(x, sr=SR):
    """loudness tích hợp BS.1770-4 (cổng tuyệt đối −70, cổng tương đối −10)"""
    p = power(x, 0.4, 0.1, sr); L = lu(p); g = p[L > -70]
    if not len(g): return -70.0
    rel = lu(g.mean()) - 10; g2 = p[(L > -70) & (L > rel)]
    return float(lu(g2.mean())) if len(g2) else -70.0


def momentary(x, sr=SR):
    """loudness tức thời 400 ms, bước 100 ms → (t_tâm, LUFS)"""
    p = power(x, 0.4, 0.1, sr); return np.arange(len(p)) * 0.1 + 0.2, lu(p)


def ebur128(path):
    """số đo chuẩn của ffmpeg: I (LUFS), LRA (LU), TP (dBTP, nâng mẫu ×4), ngưỡng LRA"""
    r = subprocess.run(['ffmpeg', '-nostats', '-nostdin', '-i', P(path), '-map', '0:a:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = r[r.rfind('Summary:'):]; g = lambda k: float(s.split(k)[1].split()[0])
    return dict(I=g('I:'), LRA=g('LRA:'), TP=g('Peak:'), LRA_low=g('LRA low:'), LRA_high=g('LRA high:'))


def loudnorm_measure(path, I=-14.0, TP=-1.0, LRA=11.0):
    """lượt 1 của ffmpeg loudnorm (chỉ đo)"""
    r = subprocess.run(['ffmpeg', '-nostats', '-nostdin', '-i', P(path), '-map', '0:a:0', '-af', f'loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    return json.loads(r[r.rfind('{'):r.rfind('}') + 1])


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(P(path), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def merge(iv, gap=0.55):
    """gộp các khoảng [a, b] cách nhau < gap giây"""
    out = []
    for a, b in sorted(iv):
        if out and a - out[-1][1] < gap: out[-1][1] = max(out[-1][1], b)
        else: out.append([a, b])
    return out


def speech_from_timeline(TL, short=None):
    """khoảng lời tuyệt đối (giây) từ timeline của ll.py/prep.py"""
    S = [s for s in TL['shorts'] if s['id'] == short] if short else TL['segments']
    return merge([[d['t0'] + a, d['t0'] + b] for d in S for a, b in d.get('speech', [])])
