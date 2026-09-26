"""M0 bước 3 — kiểm đủ từ bằng faster-whisper (chạy cục bộ, CPU).
Luật tạm (bản P, KHÔNG thay luật J1 của phiên K): mọi từ nội dung trong câu sạch phải xuất hiện trong bản ASR; kèm WER.
Chạy: /opt/cine/bin/python reports/m0/voice/asr_check.py [model=small.en]"""
import json, os, re, sys, time
from faster_whisper import WhisperModel

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, '..', 'raw')
MODEL = sys.argv[1] if len(sys.argv) > 1 else 'small.en'
meta = json.load(open(os.path.join(RAW, 'voice-takes.json')))
STOP = {'the', 'a', 'an', 'then', 'now', 'just', 'we', 'you', 'how', 'that', 's', 'll', 'one'}

def norm(s):
    s = s.lower().replace('’', "'")
    s = re.sub(r"\[[^\]]*\]", ' ', s)          # bỏ thẻ âm thanh nếu model đọc thành lời
    s = s.replace("that's", 'that is').replace("you'll", 'you will').replace("don't", 'do not')
    return re.findall(r"[a-z]+", s)

def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r != h)); prev, d[j] = d[j], cur
    return d[len(hyp)] / max(1, len(ref))

items = []
for t in meta['takes']:
    if t.get('files'):
        items += [(f['file'], t['text_clean']) for f in t['files']]
    elif t.get('file') and t.get('http') == 200:
        items.append((t['file'], t['text_clean']))

t0 = time.time(); m = WhisperModel(MODEL, device='cpu', compute_type='int8'); load_s = time.time() - t0
res = []
for fn, clean in items:
    a = time.time()
    segs, info = m.transcribe(os.path.join(HERE, fn), language='en', beam_size=5, word_timestamps=True)
    segs = list(segs); hyp = ' '.join(s.text.strip() for s in segs)
    ref_w, hyp_w = norm(clean), norm(hyp)
    need = [w for w in ref_w if w not in STOP]
    missing = [w for w in dict.fromkeys(need) if w not in hyp_w]
    extra = [w for w in dict.fromkeys(hyp_w) if w not in ref_w]
    r = {'file': fn, 'duration_s': round(info.duration, 2), 'asr': hyp, 'wer': round(wer(ref_w, hyp_w), 3),
         'required_words': len(set(need)), 'missing': missing, 'extra_words': extra,
         'all_required_present': not missing, 'asr_s': round(time.time() - a, 2)}
    res.append(r); print(json.dumps(r, ensure_ascii=False))
json.dump({'model': MODEL, 'load_s': round(load_s, 2), 'results': res},
          open(os.path.join(RAW, 'voice-asr.json'), 'w'), indent=1, ensure_ascii=False)
