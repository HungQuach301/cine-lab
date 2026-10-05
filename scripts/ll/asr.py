#!/opt/cine/bin/python
"""Last Lamplighters · kiểm lời Bill bằng ASR (faster-whisper) trước khi render (chủ dự án, 05/10/2026, mục B5).

  asr.py <episode.yaml> [--model small.en]

Mỗi đoạn lời (đoạn + Short): thu (hoặc lấy cache) bằng ll.tts → nghe lại bằng faster-whisper → so TỪ KHOÁ:
  - số: mọi cụm `say` của numbers có trong lời đoạn, và mọi năm/số viết bằng chữ số trong lời;
  - tên riêng / thuật ngữ: từ viết hoa không đứng đầu câu (Bessen, Philadelphia, ATMs…).
Thiếu từ khoá → xoá cache, thu lại đúng đoạn đó (tối đa 2 lần). Ghi <out>/asr.json; mã thoát 1 nếu còn đoạn trượt sau 2 lần.
Số so theo GIÁ TRỊ (chữ ↔ chữ số: "two hundred fifty-three thousand" ↔ "253,000").
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import ll

UNITS = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split())}
TENS = {w: 10 * i for i, w in enumerate('_ _ twenty thirty forty fifty sixty seventy eighty ninety'.split()) if w != '_'}
SCALE = {'hundred': 100, 'thousand': 1e3, 'million': 1e6, 'billion': 1e9}


def nums_of(text):
    """mọi giá trị số trong văn bản (chữ số và số viết bằng chữ)"""
    t = text.lower().replace('-', ' ').replace('—', ' ').replace('–', ' ')
    out = set(float(x.replace(',', '')) for x in re.findall(r'\d[\d,]*(?:\.\d+)?', t))
    W = re.findall(r"[a-z]+|\d[\d,.]*", t)
    i = 0
    while i < len(W):
        if W[i] in UNITS or W[i] in TENS:
            tot, cur, j, dec = 0, 0, i, None
            while j < len(W) and (W[j] in UNITS or W[j] in TENS or W[j] in SCALE or W[j] in ('and', 'point')):
                w = W[j]
                if w == 'point': dec = ''; j += 1; continue
                if dec is not None:
                    if w in UNITS: dec += str(UNITS[w]); j += 1; continue
                    break
                if w in UNITS: cur += UNITS[w]
                elif w in TENS: cur += TENS[w]
                elif w == 'hundred': cur *= 100
                elif w in SCALE: tot += cur * SCALE[w]; cur = 0
                j += 1
            v = tot + cur
            if dec: v = float(f'{int(v)}.{dec}') if v == int(v) else v
            out.add(float(v)); i = j
        else: i += 1
    return out


def keywords(E, sg):
    vo = ' '.join((sg.get('vo') or '').split())
    names = set()
    for sent in re.split(r'(?<=[.!?:—])\s+', vo):
        ws = sent.split()
        for w in ws[1:]:
            c = re.sub(r"[^A-Za-z'’-]", '', w)
            if c[:1].isupper() and len(c) > 2 and c.lower() not in ('the', 'its', 'and'): names.add(ll.norm(c.replace("’", "'")))
    vals = nums_of(vo)
    return sorted(names - {''}), sorted(vals)


def say99(n):
    U = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
    T = '_ _ twenty thirty forty fifty sixty seventy eighty ninety'.split()
    return U[n] if n < 20 else T[n // 10] + ('' if n % 10 == 0 else ' ' + U[n % 10])


def year_heard(y, txt):
    """năm có thể được ASR viết bằng chữ: 'twenty twenty-five', 'nineteen seventies'"""
    t = ' ' + re.sub(r'[^a-z ]', ' ', txt.lower().replace('-', ' ')) + ' '
    if not (1800 <= y <= 2100 and y == int(y)): return False
    y = int(y); a, b = say99(y // 100), y % 100
    cands = [f' {a} {say99(b)} ', f' {a} hundred ' if b == 0 else '', f' {a} oh {say99(b)} ' if b < 10 else '']
    if b % 10 == 0: cands.append(f' {a} {say99(b).replace("ty", "ties")} ')
    return any(c and c in t for c in cands)


def near(a, b):
    """tên riêng hiếm: ASR hay viết khác chữ (Bessen → Besson). Coi là nghe được nếu giống ≥ 0,75 (difflib) sau khi bỏ 's"""
    import difflib
    a, b = a.replace("'s", ''), b.replace("'s", '')
    return a == b or a.rstrip('s') == b.rstrip('s') or difflib.SequenceMatcher(None, a, b).ratio() >= 0.75


def check_one(model, mp3, names, vals):
    segs, _ = model.transcribe(mp3, language='en', beam_size=5, vad_filter=False, hotwords=' '.join(names) or None)
    txt = ' '.join(s.text for s in segs)
    heard = set(ll.norm(w) for w in txt.split()); hv = nums_of(txt)
    miss = [n for n in names if not any(near(n, h) for h in heard)]
    missv = [v for v in vals if not any(abs(v - h) < 1e-6 for h in hv) and not year_heard(v, txt)]
    return txt, miss, missv


def main():
    """--check: chỉ nghe và báo, không thu lại"""
    path = sys.argv[1]; only_check = '--check' in sys.argv; mname = sys.argv[sys.argv.index('--model') + 1] if '--model' in sys.argv else 'small.en'
    from faster_whisper import WhisperModel
    E = ll.load(path); model = WhisperModel(mname, device='cpu', compute_type='int8', cpu_threads=4)
    items = [(f"{E['id']}-{s['id']}", s) for s in E['segments'] if s.get('vo')] + [(f"{E['id']}-short-{s['id']}", s) for s in E.get('shorts', []) if s.get('vo')]
    rep, bad, sent = [], [], 0
    for key, sg in items:
        names, vals = keywords(E, sg)
        for tr in range(3):
            mp3, _, n = ll.tts(E, key, sg['vo'].strip()); sent += n
            txt, miss, missv = check_one(model, mp3, names, vals)
            if not miss and not missv or only_check: break
            if tr < 2 and not only_check:
                d = ll.P(E['vo_dir'])
                for x in ('mp3', 'align.json', 'txt'):
                    f = os.path.join(d, f'{key}.{x}')
                    if os.path.exists(f): os.remove(f)
        r = dict(id=sg['id'], lan_thu=tr + 1, thieu_ten=miss, thieu_so=missv, ok=not miss and not missv)
        rep.append(r); print(json.dumps(r, ensure_ascii=False))
        if not r['ok']: bad.append(sg['id'])
    os.makedirs(E['out'], exist_ok=True)
    json.dump(dict(model=mname, el_sent=sent, doan=rep, truot=bad), open(os.path.join(E['out'], 'asr.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(dict(asr_truot=bad, el_sent=sent), ensure_ascii=False)); sys.exit(1 if bad else 0)


if __name__ == '__main__': main()
