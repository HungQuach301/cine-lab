#!/opt/cine/bin/python
"""P-2010b · việc 1 bước 2: chữ lịch sử ElevenLabs ↔ chữ KL42 đã gửi. Tách phần như thu.py (≤ 1 900 ký tự, ranh giới đoạn) trên loi-khoa.txt
(kl_lib.doan_v42 kiểm nối lại đúng loi-khoa.txt), alias theo từ điển TẠI LÚC THU (commit trước 4cd2d941 — lúc thu chương, isthmus còn `iss-muss`);
câu thay: chữ `gui` trong thay.json. → kiem-chu.json"""
import json, os, re, sys
from pathlib import Path
H = Path(__file__).resolve().parent; R = H.parents[1]
os.environ.setdefault('KL_OUT', '/var/tmp/cine-out/p2010b/kl'); sys.path.insert(0, str(R / 'reports/kl42'))
import kl_lib as K  # noqa: E402
import thu  # noqa: E402
TD_THU = json.loads(Path('/var/tmp/cine-out/p2010b/tu-dien-truoc-isthmus.json').read_text())['muc']


def alias(t, td):
    for d in sorted(td, key=lambda x: -len(x['viet'])): t = re.sub(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', d['doc'], t)
    return t


K.TD = TD_THU; LS = {m['ten']: m for m in json.loads((H / 'lich-su-tai.json').read_text())['muc']}
res = []
for cid, ss in K.doan_v42():
    for i, p in enumerate(thu.phan(ss)):
        ten = f"{cid.replace(' ', '-')}-p{i}"; g = ' '.join(alias(t, TD_THU) for _, t in p)
        res.append(dict(ten=ten, shot=[s for s, _ in p], ky_tu=len(g), khop=LS[ten]['text'] == g))
for t in [t for t in json.loads((R / 'reports/kl42/thay.json').read_text()) if t['chon']]:
    ten = f"01-thay-{t['shot']}-{t['i']}"; res.append(dict(ten=ten, ky_tu=len(t['gui']), khop=LS[ten]['text'] == t['gui'], khoa=t['khoa']))
json.dump(res, open(H / 'kiem-chu.json', 'w'), ensure_ascii=False, indent=1)
for r in res: print(r['ten'], r['ky_tu'], 'KHỚP' if r['khop'] else 'LỆCH')
print('loi-khoa.txt: kl_lib.doan_v42 nối lại đúng (assert)')
