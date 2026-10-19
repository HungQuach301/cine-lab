#!/usr/bin/env python3
"""P-1910 · nháp lời v4.2 cho D11 (G1B §5): dời đoạn hầm mùa hè 1782 (2o–2p) lên trước 2j, bỏ "Before the attack".
Chỉ đọc loi-khoa.txt (không sửa); ghi khoa-loi/loi-v4.2-NHAP.txt + reports/p-1910/nhap-d11.json.
Kiểm: loi-khoa.txt đúng SHA khoá; mỗi đoạn neo xuất hiện đúng 1 lần; nháp là hoán vị đoạn của lời khoá trừ đúng 1 câu đổi."""
import hashlib, json, os, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(R, 'channel-k2/k2c-t3-01/loi-khoa.txt')
OUT = os.path.join(R, 'channel-k2/k2c-t3-01/khoa-loi/loi-v4.2-NHAP.txt')
SHA_KHOA = '0fdc72ce'
WPS = 2.5
raw = open(SRC, 'rb').read()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(SHA_KHOA), sha
paras = raw.decode('utf-8').split('\n\n')

def one(prefix):
    idx = [i for i, p in enumerate(paras) if p.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]

i2j = one('The garrison turned to heat:')
i2o = one('Before the attack, all summer,')
i2p = one('In July they blasted a hole for air.')
assert i2p == i2o + 1 and i2j < i2o
OLD = 'Before the attack, all summer, the garrison had been digging through the north face.'
NEW = 'All summer, the garrison had been digging through the north face.'
assert paras[i2o].count(OLD) == 1
p2o = paras[i2o].replace(OLD, NEW)
new = paras[:i2j] + [p2o, paras[i2p]] + paras[i2j:i2o] + paras[i2p + 1:]
assert len(new) == len(paras)
txt = '\n\n'.join(new)
open(OUT, 'w', encoding='utf-8').write(txt)

def words(t): return len([w for w in t.replace('[', ' [').split() if not (w.startswith('[') or w.endswith(']'))])
def body(t):  # bỏ đầu mục chương [NN NAME]
    return '\n'.join(l for l in t.split('\n') if not l.startswith('['))
CAU = {'nhap': NEW,
       'A': 'That summer, they had been digging through the north face.',
       'B': 'Meanwhile, all summer, the garrison had been digging through the north face.'}
res = {'nguon': 'channel-k2/k2c-t3-01/loi-khoa.txt', 'sha_khoa': sha, 'tu_s': WPS,
       'nhap': 'channel-k2/k2c-t3-01/khoa-loi/loi-v4.2-NHAP.txt',
       'sha_nhap': hashlib.sha256(txt.encode()).hexdigest(),
       'phuong_an': {}}
w0 = words(body(raw.decode()))
res['truoc'] = {'tu': w0, 'giay_uoc': round(w0 / WPS, 1)}
for k, c in CAU.items():
    t = txt.replace(NEW, c); assert t.count(c) == 1
    w = words(body(t))
    res['phuong_an'][k] = {'cau': c, 'tu_cau': len(c.split()), 'tu': w, 'giay_uoc': round(w / WPS, 1),
                           'chenh_tu': w - w0, 'chenh_giay': round((w - w0) / WPS, 1),
                           'tu_doan_2o': len(p2o.replace(NEW, c).split())}
json.dump(res, open(os.path.join(R, 'reports/p-1910/nhap-d11.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
