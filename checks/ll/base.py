"""Hàm nền dùng chung cho luật LL khoá. Bản sao độc lập của các hàm đọc dữ liệu trong scripts/ll/ll.py
(để thay đổi phía P không làm đổi nghĩa luật khoá)."""
import os, re

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FULL = {'street', 'office', 'rows', 'endcard', 'teller', 'isotype', 'stack', 'sign', 'desk', 'archive', 'inspect'}   # cảnh toàn khung
DATA = {'bars', 'line', 'compare', 'bignum'}


def norm(w): return re.sub(r"[^a-z0-9']", '', w.lower())


def words(al):
    out, cur, t0, last = [], '', None, None
    for c, s, e in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if c.isspace():
            if cur: out.append((norm(cur), t0, last, cur)); cur = ''
            continue
        if not cur: t0 = s
        cur += c; last = e
    if cur: out.append((norm(cur), t0, last, cur))
    return out


def nums_in(x, acc, echo=False):
    """Khoá số (`num`) trong một cây tham số; echo=True lấy cả số nhắc lại (vẫn hiện trên hình)."""
    if isinstance(x, dict):
        if 'num' in x and isinstance(x['num'], str) and (echo or not x.get('echo')): acc.append(x['num'])
        for v in x.values(): nums_in(v, acc, echo)
    elif isinstance(x, list):
        for v in x: nums_in(v, acc, echo)
    return acc


def load(path):
    import yaml
    E = yaml.safe_load(open(path)); E.setdefault('out', f"/var/tmp/cine-out/{E['id']}"); return E
