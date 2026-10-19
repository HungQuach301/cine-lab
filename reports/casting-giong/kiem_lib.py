"""CASTING-GIỌNG · máy kiểm: ASR (faster-whisper, 2 cách nghe như BAI-HOC #86), tỷ lệ từ đúng, tên/số, F0, tốc độ, loudness."""
import difflib, re, subprocess, sys
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / 'scripts/ll')); sys.path.insert(0, str(R / 'scripts/audio'))
import asr as A          # nums_of, year_heard (đọc, không sửa)
_M = {}
NGHE = (('medium.en', 5), ('small.en', 1))


def model(name):
    if name not in _M:
        from faster_whisper import WhisperModel
        _M[name] = WhisperModel(name, device='cpu', compute_type='int8', cpu_threads=4)
    return _M[name]


def transcribe(mp3, name, beam):
    segs, _ = model(name).transcribe(A.pcm16k(mp3), language='en', beam_size=beam, vad_filter=False, word_timestamps=True)
    segs = list(segs); return ' '.join(s.text.strip() for s in segs), [w for s in segs for w in (s.words or [])]


U = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
T = '_ _ twenty thirty forty fifty sixty seventy eighty ninety'.split()
ORD = {'1': 'first', '2': 'second', '3': 'third', '5': 'fifth', '8': 'eighth', '9': 'ninth', '12': 'twelfth'}


def w99(n): return U[n] if n < 20 else T[n // 10] + ('' if n % 10 == 0 else ' ' + U[n % 10])


def w(n):
    n = int(n); out = []
    for s, nm in ((1_000_000, 'million'), (1000, 'thousand')):
        if n >= s: out += [w(n // s), nm]; n %= s
    if n >= 100: out += [U[n // 100], 'hundred']; n %= 100
    if n or not out: out.append(w99(n))
    return ' '.join(out)


def year(y):
    a, b = divmod(int(y), 100)
    if 2000 <= int(y) <= 2009: return w(int(y))
    return w99(a) + ' ' + ('hundred' if b == 0 else ('oh ' + U[b] if b < 10 else w99(b)))


def norm(t):
    t = t.lower().replace('£', ' £').replace('’', "'").replace('metres', 'meters').replace('18 october', '18th of october')
    t = re.sub(r'\ba (hundred|thousand)\b', r'one \1', t)
    t = re.sub(r'£\s?([\d,]+)', lambda m: m.group(1) + ' pounds', t)
    t = re.sub(r'\b(\d{1,2})[:.](\d\d)\b', lambda m: w(int(m.group(1))) + ' ' + w99(int(m.group(2))), t)
    t = re.sub(r'\b(\d+)(st|nd|rd|th)\b', lambda m: (w(int(m.group(1))) + ' ').rsplit(' ', 2)[0] + ' ' + ORD.get(str(int(m.group(1)) % 100 if int(m.group(1)) % 100 in (1, 2, 3, 5, 8, 9, 12) else -1), (w(int(m.group(1))) + 'th').replace('yth', 'ieth')).split()[-1] if int(m.group(1)) >= 20 and int(m.group(1)) % 10 else ORD.get(m.group(1), (w(int(m.group(1))) + 'th').replace('yth', 'ieth')), t)
    t = re.sub(r'\b(1[0-9]{3}|20[0-9]{2})\b', lambda m: year(m.group(1)), t)
    t = re.sub(r'\b\d[\d,]*\b', lambda m: w(int(m.group(0).replace(',', ''))), t)
    t = t.replace('%', ' percent').replace('-', ' ')
    ws = re.findall(r"[a-z]+(?:'[a-z]+)?", t)
    num = set(U) | set(T) | {'hundred', 'thousand', 'million'}
    ws = [x for i, x in enumerate(ws) if not (x == 'and' and 0 < i < len(ws) - 1 and ws[i - 1] in num and ws[i + 1] in num)]   # "three hundred and fifty-seven" = "357"
    return [{'oh': 'oh', 'o': 'oh'}.get(x, x) for x in ws]


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp); d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (r[i - 1] != h[j - 1]))
    sm = difflib.SequenceMatcher(None, r, h, autojunk=False)
    diff = [(' '.join(r[a:b]), ' '.join(h[c:e])) for op, a, b, c, e in sm.get_opcodes() if op != 'equal']
    return dict(tu_dung=round(1 - d[len(h)] / len(r), 4), loi=d[len(h)], so_tu=len(r), cho_lech=diff)


def name_ok(name, hyp, alias=None):
    def n(s): return re.sub(r'[^a-z0-9 ]', ' ', s.lower().replace('-', ' ').replace("'s", ' ')).split()
    H = n(hyp); best = 0.0
    for cand in [name] + ([alias] if alias else []):
        a = ' '.join(n(cand)); k0 = len(a.split())
        for k in (k0 - 1, k0, k0 + 1):
            if k < 1: continue
            for i in range(0, max(1, len(H) - k + 1)): best = max(best, difflib.SequenceMatcher(None, a, ' '.join(H[i:i + k])).ratio())
    return round(best, 3)


def num_ok(v, hyp):
    if ' ' + w(v) + ' ' in ' ' + ' '.join(norm(hyp)) + ' ': return True   # "10.25" ↔ ten twenty-five; "150" ↔ (a hundred and) fifty
    return any(abs(v - x) < 1e-6 for x in A.nums_of(hyp)) or A.year_heard(v, hyp) or (1000 <= v < 1800 and year(v) in ' '.join(norm(hyp)))


def f0(mp3):
    import librosa
    y = A.pcm16k(mp3); f, vf, _ = librosa.pyin(y, fmin=50, fmax=300, sr=16000, frame_length=1024, hop_length=320)
    f = f[vf & ~np.isnan(f)]; return round(float(np.median(f)), 1), round(float(np.percentile(f, 10)), 1), round(float(np.percentile(f, 90)), 1)


def dur(mp3):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3], capture_output=True, text=True).stdout)


def speech_span(words):
    return (words[-1].end - words[0].start) if words else 0.0
