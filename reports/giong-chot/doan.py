#!/opt/cine/bin/python
"""GIỌNG-CHỐT · chữ gửi: áp từ điển khoá ĐÃ SỬA (tu-dien.json, Đ3) lên chữ khoá → doan.json
 - moc: móc mở đầu 0a–0e; pin: pin nổi 2k–2n (chữ khoá = casting-giong/doan-thu.json, nguyên văn lời khoá SHA 0fdc72ce…)
 - bang: 40 mục bảng phát âm (casting-giong/phat-am-thu.json, chữ khoá) + câu 5i nguyên văn chứa "18 October 2026" (mục 47 duy nhất không có trong móc/pin)."""
import json, re
from pathlib import Path
H = Path(__file__).resolve().parent; R = H.parents[1]
D = json.loads((R / 'channel-k2/k2c-t3-01/khoa-loi/phat-am/tu-dien.json').read_text())['muc']
LOI = (R / 'channel-k2/k2c-t3-01/loi-khoa.txt').read_text()
def alias(t):
    for d in sorted(D, key=lambda x: -len(x['viet'])): t = re.sub(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', d['doc'], t)
    return t
dt = {d['doan']: d for d in json.loads((R / 'reports/casting-giong/doan-thu.json').read_text())['doan']}
pa = json.loads((R / 'reports/casting-giong/phat-am-thu.json').read_text())
c5i = 'As of 18 October 2026, the treaty is in force only provisionally, pending a European Parliament vote indicated for the fourteenth of December.'
assert c5i in LOI
out = {}
for k, src in (('moc', dt['1-moc']), ('pin', dt['2-pin-noi'])):
    assert src['khoa'].replace(' ', '') in LOI.replace('\n', '').replace(' ', '')
    out[k] = dict(shot=src['shot'], khoa=src['khoa'], gui=alias(src['khoa']), muc=src['muc_tu_dien'])
out['bang'] = dict(khoa=pa['khoa'] + ' ' + c5i, gui=alias(pa['khoa'] + ' ' + c5i), muc=pa['muc'] + ['18 October 2026'])
muc_all = set(out['bang']['muc']) | set(out['moc']['muc']) | set(out['pin']['muc'])
assert muc_all == {d['viet'] for d in D}, sorted({d['viet'] for d in D} - muc_all)
json.dump(out, open(H / 'doan.json', 'w'), ensure_ascii=False, indent=1)
for k, v in out.items(): print(k, len(v['khoa']), len(v['gui'])); print('  ', v['gui'])
