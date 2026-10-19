#!/opt/cine/bin/python
"""GIỌNG-CHỐT · tách tốc độ đọc thành (a) tốc độ phát âm = từ / thời gian có tiếng và (b) tổng ngừng (RMS 20 ms < nền + 8 dB liên tục ≥ 0,2 s, trong khoảng lời).
Tham số speed của ElevenLabs tác động lên (a); (b) thay đổi theo từng lượt thu (stability 0,5). nhip.py → nhip.json"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gc_lib as G
K, L = G.K, G.L
IDX = json.load(open(f'{L.OUT}/thu.json')); KI = json.load(open(f'{G.H}/may-kiem.json'))['ban']
def lang(f, tren_nen=8.0, dmin=0.2, hop=0.01):
    """Quãng ngừng: RMS khung 20 ms (bước 10 ms) < nền (phân vị 5) + 8 dB liên tục ≥ 0,2 s — v2 có nền ≈ −35…−39 dBFS, v4 ≈ −44, nên ngưỡng tuyệt đối không dùng được (ffmpeg silencedetect của máy này không in kết quả)."""
    x = K.A.pcm16k(f).astype('float64'); n = int(0.02 * 16000); h = int(hop * 16000)
    r = 20 * np.log10(np.array([np.sqrt(np.mean(x[i:i + n] ** 2) + 1e-12) for i in range(0, len(x) - n, h)])); q = r < np.percentile(r, 5) + tren_nen
    out, i = [], 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) * hop >= dmin: out.append((i * hop, j * hop + 0.02 - hop))
            i = j
        else: i += 1
    return out
out = {}
for tag, m in IDX.items():
    if tag == 'bang': continue
    f = m['tep']; dur = K.dur(f); S = lang(f)
    a = S[0][1] if S and S[0][0] < 0.05 else 0.0; b = S[-1][0] if S and S[-1][1] > dur - 0.05 else dur      # bỏ lặng đầu/cuối tệp
    ngung = [(x, y) for x, y in S if x >= a - 1e-6 and y <= b + 1e-6 and (x, y) != (0.0, a)]
    ngung = [(x, y) for x, y in ngung if x > a + 1e-3 and y < b - 1e-3]
    tong_ngung = sum(y - x for x, y in ngung); span = b - a; tu = KI[tag]['tu_viet'] if tag in KI else 60
    out[tag] = dict(speed=m['settings'].get('speed'), model=m['model'], span=round(span, 2), ngung_s=round(tong_ngung, 2), so_ngung=len(ngung),
                    co_tieng_s=round(span - tong_ngung, 2), tu=tu, tu_giay=round(tu / span, 3), phat_am_tu_giay=round(tu / (span - tong_ngung), 3))
    print(tag, out[tag])
json.dump(out, open(f'{G.H}/nhip.json', 'w'), ensure_ascii=False, indent=1)
