#!/opt/cine/bin/python -I
"""NC-N2P · kiểm câu trích NGUYÊN VĂN của danh mục (b) và (a) trong tệp nguồn có SHA-256 (§12.3: khớp nguyên văn bằng máy).
  kiem_trich.py <danh-muc.json> [...] → in bảng + ghi <danh-muc>.kiem.json
Khớp = chuỗi trích (gộp mọi khoảng trắng thành một dấu cách) là chuỗi con của tệp (cùng phép gộp). Điền: dòng bắt đầu, SHA-256 tệp,
và kiểm mục ngày: câu trích phải nằm sau dòng đầu mục ngày ghi trong 'muc_ngay' và trước mục ngày kế tiếp (Pepys: '<n>th.' / Evelyn: '<n>th September, 1666.')."""
import hashlib, json, re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]


def norm_map(t):
    """chuỗi gộp khoảng trắng + bảng vị trí → dòng gốc"""
    out, lines, ln, sp = [], [], 1, False
    for ch in t:
        if ch.isspace():
            if not sp: out.append(' '); lines.append(ln); sp = True
            if ch == '\n': ln += 1
        else: out.append(ch); lines.append(ln); sp = False
    return ''.join(out), lines


def day_start(text_lines, muc):
    key = muc.split(' (')[0].strip()
    pat = re.compile(r'^' + re.escape(key) + r'[\s.(,]')
    hits = [i + 1 for i, l in enumerate(text_lines) if pat.match(l)]
    return hits


def main():
    cache = {}
    for f in sys.argv[1:]:
        D = json.load(open(f)); res = []
        for m in D['muc']:
            if 'trich' not in m or m.get('nguon') not in D.get('nguon', {}): res.append({'id': m['id'], 'ket_qua': 'KHÔNG CÓ TRÍCH (nguồn web/bậc khác — xem url)'}); continue
            src = D['nguon'][m['nguon']]; p = REPO / src['tep']
            if p not in cache:
                b = p.read_bytes(); t = b.decode('utf-8', 'replace'); cache[p] = (hashlib.sha256(b).hexdigest(), t, *norm_map(t), t.splitlines())
            sha, t, nt, lines, tl = cache[p]
            q = ' '.join(m['trich'].split()); i = nt.find(q); n = nt.count(q)
            r = {'id': m['id'], 'tep': src['tep'], 'sha256': sha, 'khop': i >= 0, 'so_lan': n, 'dong': lines[i] if i >= 0 else None}
            if i >= 0 and m.get('muc_ngay'):
                st = [h for h in day_start(tl, m['muc_ngay']) if h <= r['dong']]
                r['dong_muc_ngay'] = st[-1] if st else None
                # mục kế tiếp: dòng đầu mục ngày đầu tiên sau dòng mục này
                nxt = re.compile(r'^(\d+(st|nd|rd|th|d)[\s.(]|\d+(st|nd|rd|th|d) [A-Z][a-z]+, 16\d\d)')
                after = [k + 1 for k in range((st[-1] if st else 1), len(tl)) if nxt.match(tl[k])]
                r['trong_muc_ngay'] = bool(st) and (not after or r['dong'] < after[0])
            r['ket_qua'] = 'KHỚP' if r['khop'] and r.get('trong_muc_ngay', True) else ('KHỚP, LỆCH MỤC NGÀY' if r['khop'] else 'KHÔNG KHỚP')
            res.append(r)
        ok = sum(1 for r in res if r['ket_qua'] == 'KHỚP'); tot = sum(1 for r in res if 'tep' in r)
        Path(f).with_suffix('.kiem.json').write_text(json.dumps({'tong': tot, 'khop': ok, 'muc': res}, ensure_ascii=False, indent=1))
        for r in res: print(r['id'], r['ket_qua'], r.get('dong'), r.get('dong_muc_ngay'))
        print(f'{f}: {ok}/{tot} KHỚP')


if __name__ == '__main__': main()
