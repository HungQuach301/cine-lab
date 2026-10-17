"""T3 · gói TUYẾN · tìm câu trích trong tệp nguồn thô (djvu.txt / HTML / JSON Hansard) và định vị dòng + trang in (đầu trang OCR gần nhất).
Chuẩn hoá: chữ thường, ſ→s, bỏ thẻ HTML/thực thể, bỏ mọi ký tự không phải chữ/số. "…" tách câu trích thành mảnh; mỗi mảnh phải có trong tệp."""
import html, json, re
from pathlib import Path

_W = re.compile(r'[^0-9a-zà-ỹ]+')


def norm(s):
    s = html.unescape(s).lower().replace('ſ', 's')
    return _W.sub('', s)


def text_of(path):
    p = Path(path); raw = p.read_text(encoding='utf-8', errors='replace')
    if p.suffix == '.json':   # Hansard: nối mọi chuỗi trong cây JSON
        out = []
        def walk(x):
            if isinstance(x, dict): [walk(v) for v in x.values()]
            elif isinstance(x, list): [walk(v) for v in x]
            elif isinstance(x, str): out.append(x)
        walk(json.loads(raw)); raw = '\n'.join(out)
    if p.suffix in ('.html', '.json'):
        raw = re.sub(r'<[^>]+>', ' ', raw)
    return raw


_PAGE = [re.compile(r'^\s*(\d{1,3})\s+[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\'’ .,;-]{3,}'), re.compile(r'[A-ZÁÉÍÓÚÑ]{3,}[A-ZÁÉÍÓÚÑ\'’ .,;\]\[-]*\s+(\d{1,3})\s*$')]


def locate(path, trich):
    """→ (khớp: bool, mảnh khớp/tổng, dòng đầu, trang in ước hoặc None)"""
    raw = text_of(path); lines = raw.split('\n')
    # chỉ mục: vị trí ký tự chuẩn hoá → số dòng
    buf, idx = [], []
    for i, ln in enumerate(lines):
        n = norm(ln); buf.append(n); idx.extend([i] * len(n))
    full = ''.join(buf)
    frags = [f for f in (norm(x) for x in trich.split('…')) if f]
    hit, first = 0, None
    for f in frags:
        k = full.find(f)
        if k >= 0:
            hit += 1
            if first is None: first = idx[k]
    page = None
    if first is not None and Path(path).suffix == '.txt':
        for j in range(first, max(0, first - 160), -1):
            for rx in _PAGE:
                m = rx.match(lines[j])
                if m:
                    page = int(m.group(1)) + (0 if j < first else 0); break
            if page: break
    return hit == len(frags), f'{hit}/{len(frags)}', (first + 1 if first is not None else None), page
