#!/opt/cine/bin/python
"""ÂM THANH · tiền xử lý lời trước ElevenLabs theo từ điển phát âm (phiên Âm thanh, Mốc C, 15/10/2026).

  phat_am.py apply "<câu>"                 → in bản gửi TTS
  phat_am.py diff <episode.yaml>           → liệt kê mọi đoạn lời sẽ đổi (trước → sau) và mốc "@từ" sẽ gãy
  phat_am.py check <episode.yaml>          → mã thoát 1 nếu lời còn chữ số / viết tắt chưa có trong từ điển

Luật (docs/AUDIO-PHAT-AM.md; từ điển scripts/audio/phat-am.yaml):
  - số có dấu phẩy nghìn và số thập phân → chữ (ElevenLabs đọc sai "4,440": commit 96da659, RUNBOOK §5);
  - năm 4 chữ số → đọc theo cặp ("nineteen forty-three"); thập niên "1970s" → "nineteen seventies";
  - tiền "$5 billion" → "five billion dollars"; "%" → "percent"; số thứ tự "12th" → "twelfth"; ngày "June 12" → "June twelfth";
  - "500-won" → "five-hundred-won"; viết tắt theo từ điển (đánh vần hay đọc như từ); tên riêng theo bảng alias.
Không đổi nghĩa, không đổi dấu câu; chỉ đổi cách viết của cùng chữ nói. Bản gửi phải được dùng cho phụ đề (khớp tiếng).
"""
import os, re, sys
import yaml

D = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phat-am.yaml')))
ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = '_ _ twenty thirty forty fifty sixty seventy eighty ninety'.split()
ORD_IRR = {'one': 'first', 'two': 'second', 'three': 'third', 'five': 'fifth', 'eight': 'eighth', 'nine': 'ninth', 'twelve': 'twelfth'}
MONTHS = 'January February March April May June July August September October November December'.split()


def below_1000(n):
    h, r = divmod(n, 100); out = []
    if h: out.append(ONES[h] + ' hundred')
    if r:
        if r < 20: out.append(ONES[r])
        else: out.append(TENS[r // 10] + ('-' + ONES[r % 10] if r % 10 else ''))
    return ' '.join(out)


def words(n):
    """số nguyên ≥ 0 → chữ tiếng Anh kiểu Mỹ (không 'and')"""
    n = int(n)
    if n == 0: return 'zero'
    out = []
    for v, name in ((10 ** 12, 'trillion'), (10 ** 9, 'billion'), (10 ** 6, 'million'), (1000, 'thousand'), (1, '')):
        q, n = divmod(n, v)
        if q: out.append(below_1000(q) + (' ' + name if name else ''))
    return ' '.join(out)


def ordinal(n):
    w = words(n); head, _, last = w.rpartition(' '); pre = head + ' ' if head else ''
    if '-' in last: a, b = last.rsplit('-', 1); return pre + a + '-' + ORD_IRR.get(b, b + 'th')
    if last in ORD_IRR: return pre + ORD_IRR[last]
    if last.endswith('y'): return pre + last[:-1] + 'ieth'
    return pre + last + 'th'


def year(y):
    y = int(y)
    if 2000 <= y <= 2009: return 'two thousand' + ('' if y == 2000 else ' ' + ONES[y - 2000])
    hi, lo = divmod(y, 100)
    if lo == 0: return words(hi) + ' hundred'
    return words(hi) + ' ' + ('oh-' + ONES[lo] if lo < 10 else words(lo))


def decade(y):
    w = year(y)   # "nineteen seventy" → "nineteen seventies"
    return (w[:-1] + 'ies') if w.endswith('y') else (w + 's')


def num_text(s):
    """'2,710' → chữ; '4.5' → 'four point five'"""
    s = s.replace(',', '')
    if '.' in s:
        a, b = s.split('.'); return words(int(a or 0)) + ' point ' + ' '.join(ONES[int(c)] for c in b)
    return words(int(s))


def apply(t):
    # 1) alias (cụm dài trước), khớp nguyên từ
    for k in sorted(D.get('alias', {}), key=len, reverse=True):
        t = re.sub(r'(?<![\w-])' + re.escape(k) + r'(?![\w-])', D['alias'][k], t)
    # 2) viết tắt
    for k, v in D.get('abbr', {}).items():
        rep = v.get('spell') or v.get('say')
        t = re.sub(r'(?<![\w.])' + re.escape(k) + r'(?![\w])', rep, t)
    # 3) tiền: $5 billion / $4.5 / $100,000
    def money(m):
        sym, n, scale = m.group(1), m.group(2), m.group(3); one, many = D['currency'][sym]
        amt = num_text(n); plural = many if (scale or n.replace(',', '') not in ('1', '1.0')) else one
        return f"{amt}{' ' + scale if scale else ''} {plural}"
    t = re.sub(r'([$€£₩])(\d[\d,]*(?:\.\d+)?)(?:\s+(million|billion|trillion|thousand))?', money, t)
    # 4) phần trăm
    t = re.sub(r'(\d[\d,]*(?:\.\d+)?)\s?%', lambda m: num_text(m.group(1)) + ' percent', t)
    # 5) số-đơn vị nối gạch: 500-won → five-hundred-won
    t = re.sub(r'\b(\d[\d,]*)-(' + '|'.join(D.get('suffix_units', {})) + r')\b', lambda m: num_text(m.group(1)).replace(' ', '-') + '-' + m.group(2), t)
    # 6) thập niên 1970s / năm
    t = re.sub(r"\b(1[5-9]\d0|20\d0)s\b", lambda m: decade(m.group(1)), t)
    lo, hi = D.get('year_range', [1500, 2099]); cn = set(D.get('count_nouns', []))

    def yr(m):
        y = int(m.group(1)); nxt = (m.group(2) or '').strip().lower()
        if lo <= y <= hi and nxt not in cn: return year(y) + (m.group(2) or '')
        return words(y) + (m.group(2) or '')
    t = re.sub(r'(?<![\d,.$])\b(\d{4})\b(?![,.]\d)(\s+[A-Za-z]+)?', yr, t)
    # 7) ngày: "June 12" → "June twelfth"
    t = re.sub(r'\b(' + '|'.join(MONTHS) + r')\s+(\d{1,2})\b(?!,\d)', lambda m: m.group(1) + ' ' + ordinal(int(m.group(2))), t)
    # 8) số thứ tự 12th, 1st, 3rd
    t = re.sub(r'\b(\d+)(st|nd|rd|th)\b', lambda m: ordinal(int(m.group(1))), t)
    # 9) số thường còn lại (có phẩy nghìn, thập phân, số nguyên)
    t = re.sub(r'(?<![\w.])(\d[\d,]*(?:\.\d+)?)(?![\w])', lambda m: num_text(m.group(1).rstrip(',')) + (',' if m.group(1).endswith(',') else ''), t)
    return t


def leftovers(t):
    """chữ số còn sót + cụm IN HOA ≥ 2 ký tự chưa có trong từ điển"""
    known = set(D.get('abbr', {})) | {'I', 'A', 'OK', 'TV'}
    return sorted(set(re.findall(r'\d+', t))), sorted({w for w in re.findall(r'\b[A-Z]{2,}\b', t) if w not in known})


def _episode(path):
    E = yaml.safe_load(open(path)); return [(s['id'], s.get('vo') or '') for s in E.get('segments', []) + E.get('shorts', [])], E


if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == 'apply': print(apply(sys.argv[2])); sys.exit(0)
    segs, E = _episode(sys.argv[2]); bad = 0
    for sid, vo in segs:
        a = apply(vo.strip())
        if cmd == 'diff' and a != vo.strip():
            print(f'== đoạn {sid}'); import difflib
            for w in difflib.ndiff(vo.split(), a.split()):
                if w[0] in '+-': print('  ', w)
        if cmd == 'check':
            d, ab = leftovers(a)
            if d or ab: bad += 1; print(f'đoạn {sid}: còn chữ số {d} · viết tắt chưa có trong từ điển {ab}')
    if cmd == 'diff':   # mốc "@từ" trỏ vào chữ sẽ đổi
        import json
        s = json.dumps(E.get('segments', []), ensure_ascii=False)
        for m in sorted(set(re.findall(r'"@([^"#+\-]+)', s))):
            if re.search(r'\d', m) or m in D.get('alias', {}) or m in D.get('abbr', {}): print(f'MỐC SẼ GÃY: @{m} (lời gửi TTS đổi chữ này)')
    sys.exit(1 if bad else 0)
