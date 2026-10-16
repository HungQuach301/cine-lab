#!/opt/cine/bin/python
"""K2C-T2-01 · KIỂM ĐIỂM NỐI ÂM sau sua_loi.py (v3.4): mỗi điểm nối → cửa sổ ±6 s của bản thu mới, nghe bằng HAI cách
(A small.en có gợi ý tên, B medium.en không gợi ý) và so với lời khoá trong cửa sổ (tỉ lệ từ sai, WER);
đo khoảng lặng tại điểm nối so với phân bố khoảng nghỉ giữa các câu của chính đoạn đó, và chênh mức âm (dB RMS) 0,4 s cuối câu trước / 0,4 s đầu câu sau
so với phân bố chênh ở các ranh câu tự nhiên của đoạn. Lộ nối khi: WER > 0,10 ở cả hai cách, hoặc khoảng lặng / chênh mức nằm ngoài [min, max] của ranh câu tự nhiên.
  noi_check.py → kiem-mu/asr/noi-v3.4.json"""
import json, os, re, subprocess, sys
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, '..', '..')); VO = os.path.join(H, 'vo'); KEY = 'k2c-t2-01'; SR = 16000
sys.path.insert(0, os.path.join(REPO, 'scripts/ll')); import ll  # noqa: E402
from faster_whisper import WhisperModel
J = json.load(open(f'{VO}/sua-v3.4.json'))
pts = [('03', J['03'][0]['noi_s']), ('04', J['04'][0]['noi_s']), ('06', J['06'][1]['noi_s']), ('06', J['06'][2]['noi_s'][0]), ('06', J['06'][2]['noi_s'][1]), ('02', J['02'][0]['noi_s'])]


def pcm(f):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout, np.float32)


def db(x):
    return float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9))


def wer(ref, hyp):
    r = [ll.norm(w) for w in ref.split() if ll.norm(w)]; h = [ll.norm(w) for w in hyp.split() if ll.norm(w)]
    d = list(range(len(h) + 1))
    for i, a in enumerate(r, 1):
        p, d[0] = d[0], i
        for j, b in enumerate(h, 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (a != b))
    return d[-1] / max(1, len(r))


M = {'A': WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=2), 'B': WhisperModel('medium.en', device='cpu', compute_type='int8', cpu_threads=2)}
out = []
for seg, t in pts:
    x = pcm(f'{VO}/{KEY}-{seg}.mp3'); W = ll.words(json.load(open(f'{VO}/{KEY}-{seg}.align.json'))); dur = len(x) / SR
    # ranh câu tự nhiên của đoạn: khoảng nghỉ và chênh mức
    gaps, jumps = [], []
    for a, b in zip(W, W[1:]):
        if re.search(r'[.?!]["”]?$', a[3]):
            g = b[1] - a[2]; gaps.append(g); jumps.append(db(x[int(b[1] * SR):int((b[1] + 0.4) * SR)]) - db(x[int(max(0, a[2] - 0.4) * SR):int(a[2] * SR)]))
    before = [w for w in W if w[2] <= t]; after = [w for w in W if w[1] >= t]
    g = (after[0][1] - before[-1][2]) if before and after else None
    jmp = (db(x[int(after[0][1] * SR):int((after[0][1] + 0.4) * SR)]) - db(x[int(max(0, before[-1][2] - 0.4) * SR):int(before[-1][2] * SR)])) if before and after else None
    a0, a1 = max(0, t - 6), min(dur, t + 6)
    ref = ' '.join(w[3] for w in W if w[1] >= a0 and w[2] <= a1)
    r = dict(doan=seg, noi_s=t, lang_s=None if g is None else round(float(g), 2), lang_tu_nhien=[round(float(min(gaps)), 2), round(float(np.median(gaps)), 2), round(float(max(gaps)), 2)],
             chenh_db=None if jmp is None else round(jmp, 1), chenh_tu_nhien=[round(min(jumps), 1), round(float(np.median(jumps)), 1), round(max(jumps), 1)], loi=ref)
    for k, m in M.items():
        segs, _ = m.transcribe(x[int(a0 * SR):int(a1 * SR)], language='en', beam_size=5, vad_filter=False)
        hyp = ' '.join(s.text.strip() for s in segs); r[k] = dict(nghe=hyp, wer=round(wer(ref, hyp), 3))
    r['lo_noi'] = bool((r['A']['wer'] > 0.10 and r['B']['wer'] > 0.10) or (g is not None and not (min(gaps) <= g <= max(gaps))) or (jmp is not None and not (min(jumps) <= jmp <= max(jumps))))
    out.append(r); print(json.dumps(r, ensure_ascii=False), flush=True)
json.dump(out, open(os.path.join(H, 'kiem-mu', 'asr', 'noi-v3.4.json'), 'w'), indent=1, ensure_ascii=False)
