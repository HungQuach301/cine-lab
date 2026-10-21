#!/opt/cine/bin/python
"""P-2010b · việc 1 bước 7: WER sau chuẩn hoá SỐ hai phía (đọc asr-wer.json, không chạy lại ASR): chữ số → chữ (num2words 0.5.14; số 4 chữ số 1100–2099
đọc kiểu năm, "21st" → ordinal; "1,000" → 1000), rồi cùng chuẩn hoá chữ như asr_wer.py. Ghi thêm danh sách chỗ lệch còn lại theo từng chương.
Cần num2words (cài vào thư mục tạm, PYTHONPATH). → asr-wer.json khoá `chuan_so`"""
import difflib, json, re, sys, unicodedata
from pathlib import Path
from num2words import num2words
H = Path(__file__).resolve().parent; R = H.parents[1]
J = json.loads((H / 'asr-wer.json').read_text()); LK = (R / 'channel-k2/k2c-t3-01/loi-khoa.txt').read_text()
CH = {m.group(1): m.group(2) for m in re.finditer(r'^\[(\d\d \w+)\]\n(.*?)(?=^\[|\Z)', LK, re.S | re.M)}


def norm(t):   # = asr_wer.norm
    t = ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn').replace('%', ' percent')
    t = re.sub(r'(\d),(\d)', r'\1\2', t); t = re.sub(r'[-–—]', ' ', t); t = re.sub(r"[^a-z0-9' ]", ' ', t).replace("'", '')
    return t.split()


def wer(ref, hyp):   # = asr_wer.wer
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        p, d[0] = d[0], i
        for j, h in enumerate(hyp, 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (r != h))
    return d[-1]


def so(t):
    t = re.sub(r'(\d),(\d{3})', r'\1\2', t)
    t = re.sub(r'\b(\d+)(st|nd|rd|th)\b', lambda m: num2words(int(m.group(1)), to='ordinal'), t)
    return re.sub(r'\b\d+(\.\d+)?\b', lambda m: num2words(float(m.group(0))) if m.group(1) else
                  (num2words(int(m.group(0)), to='year') if 1100 <= int(m.group(0)) <= 2099 else num2words(int(m.group(0)))), t)


out = {}
for k, v in J['cach'].items():
    rs = []
    for c in v['chuong']:
        a, b = norm(so(CH[c['chuong']])), norm(so(c['asr'])); e = wer(a, b)
        lech = [f"{' '.join(a[i1:i2])} → {' '.join(b[j1:j2])}" for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if op != 'equal']
        rs.append(dict(chuong=c['chuong'], tu_khoa=len(a), sua=e, wer=round(e / len(a), 4), lech=lech))
    tk, ts = sum(r['tu_khoa'] for r in rs), sum(r['sua'] for r in rs); out[k] = dict(tong_tu=tk, tong_sua=ts, wer=round(ts / tk, 4), chuong=rs)
    print(k, out[k]['wer'], [(r['chuong'], r['wer']) for r in rs])
J['chuan_so'] = out; (H / 'asr-wer.json').write_text(json.dumps(J, ensure_ascii=False, indent=1))
