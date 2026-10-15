#!/opt/cine/bin/python
"""K2C-T2-01 · ASR HAI CÁCH NGHE (G2, lệnh chủ dự án 15/10): mỗi đoạn lời đã thu → (A) faster-whisper small.en CÓ hotwords tên riêng (cách của scripts/ll/asr.py),
(B) medium.en KHÔNG hotwords (nghe độc lập, không gợi ý). So từ khoá của asr.py (số theo giá trị, tên riêng) cho cả hai; ghi toàn văn nghe được.
  asr2.py [--only 00,04] → kiem-mu/asr/<đoạn>-{A,B}.txt + kiem-mu/asr/asr2.json"""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'scripts/k2')); import prep  # noqa: E402
sys.path.insert(0, os.path.join(REPO, 'scripts/ll')); import ll, asr  # noqa: E402
from faster_whisper import WhisperModel
E = ll.load(os.path.join(H, 'episode.yaml')); only = (sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None)
M = {'A': (WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=4), True), 'B': (WhisperModel('medium.en', device='cpu', compute_type='int8', cpu_threads=4), False)}
out = {}; od = os.path.join(H, 'kiem-mu', 'asr')
for sg in E['segments']:
    if only and sg['id'] not in only: continue
    mp3 = os.path.join(REPO, E['vo_dir'], f"{E['id']}-{sg['id']}.mp3"); names, vals = asr.keywords(E, sg); r = {}
    for k, (m, hw) in M.items():
        segs, _ = m.transcribe(asr.pcm16k(mp3), language='en', beam_size=5, vad_filter=False, hotwords=(' '.join(names) or None) if hw else None)
        txt = ' '.join(s.text.strip() for s in segs); open(os.path.join(od, f"{sg['id']}-{k}.txt"), 'w').write(txt + '\n')
        heard = set(ll.norm(w) for w in txt.split()); hv = asr.nums_of(txt)   # cùng phép so của scripts/ll/asr.py check_one
        r[k] = dict(thieu_so=[v for v in vals if not any(abs(v - h) < 1e-6 for h in hv) and not asr.year_heard(v, txt)],
                    thieu_ten=[n for n in names if not any(asr.near(n, h) for h in heard)])
    out[sg['id']] = r; print(sg['id'], json.dumps(r, ensure_ascii=False), flush=True)
json.dump(out, open(os.path.join(od, 'asr2.json' if not only else f"asr2-{'-'.join(only)}.json"), 'w'), ensure_ascii=False, indent=1)
