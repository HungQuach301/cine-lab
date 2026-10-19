#!/opt/cine/bin/python
"""CASTING-GIỌNG · đoạn thử chung cho mọi giọng (18/10/2026).
Lấy nguyên văn shot 0a–0e, 2k–2n, 5e–5i từ script-v4.1-KHOA.md (bỏ mã claim, ‹Our read›, [TRÊN HÌNH]),
kiểm từng câu có nguyên văn trong loi-khoa.txt (SHA 0fdc72ce…), rồi áp 47 luật alias của khoa-loi/phat-am/tu-dien.json
(dài trước, cùng biên từ như lam_loi_khoa.py). Ghi doan-thu.json: 3 đoạn × (chữ khoá, chữ gửi TTS)."""
import hashlib, json, re
from pathlib import Path
R = Path(__file__).resolve().parents[2]; EP = R / 'channel-k2/k2c-t3-01'
loi = (EP / 'loi-khoa.txt').read_text()
assert hashlib.sha256(loi.encode()).hexdigest().startswith('0fdc72ce'), 'lời khoá đổi SHA'
sc = (EP / 'script-v4.1-KHOA.md').read_text()
D = json.loads((EP / 'khoa-loi/phat-am/tu-dien.json').read_text())['muc']
assert len(D) == 47
DOAN = {'1-moc': ['0a', '0b', '0c', '0d', '0e'], '2-pin-noi': ['2k', '2l', '2m', '2n'], '3-ket-so-lieu': ['5e', '5f', '5g', '5h', '5i']}
def shot(c):
    m = re.search(r'^‹' + c + r'› (.+)$', sc, re.M); t = re.sub(r'\s*\{[^}]*\}', '', m.group(1)).replace('‹Our read› ', '').strip()
    assert t in loi, c; return t
def alias(t):
    for d in sorted(D, key=lambda x: -len(x['viet'])): t = re.sub(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', d['doc'], t)
    return t
out = []
for k, cs in DOAN.items():
    khoa = ' '.join(shot(c) for c in cs)
    out.append(dict(doan=k, shot=cs, khoa=khoa, gui=alias(khoa), muc_tu_dien=[d['viet'] for d in D if re.search(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', khoa)]))
json.dump(dict(nguon='script-v4.1-KHOA.md + loi-khoa.txt (sha256 0fdc72ce…)', doan=out, ky_tu_khoa=sum(len(o['khoa']) for o in out), ky_tu_gui=sum(len(o['gui']) for o in out)),
          open(Path(__file__).with_name('doan-thu.json'), 'w'), ensure_ascii=False, indent=1)
for o in out: print(o['doan'], len(o['khoa']), len(o['gui']), o['muc_tu_dien']); print(o['gui']); print()
