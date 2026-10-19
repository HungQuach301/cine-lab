#!/opt/cine/bin/python
"""KL42 · tệp nghe so alias isthmus (GC-C′): 4 khối, mỗi khối 3 câu (1i#0, 1i#1, 1k#0), cách nhau 0,8 s; giữa khối 2 s.
Khối 1 = bản thu cả tập (alias 'iss-muss', seed 19102026) · 2 = thu lại 'iss-muss' seed 19102027 · 3 = 'issmus' seed 19102026 (đã dùng trong stem) · 4 = không alias ('isthmus').
→ nghe/isthmus-so-sanh.mp3 (−14 LUFS xấp xỉ, chỉ để nghe)."""
import json, sys
import numpy as np
import kl_lib as K
sys.path.insert(0, str(K.R / 'scripts/audio')); import lib   # noqa: E402
SR = lib.SR; rec = json.loads((K.OUT / 'thu/01.json').read_text()); T = json.loads((K.H / 'thay.json').read_text())
CAU = [('1i', 0), ('1i', 1), ('1k', 0)]
def cat(p, a, b): x = lib.dec(p, 1, sr=SR, dtype=np.float32)[:, 0]; return x[max(0, int((a - 0.08) * SR)):int((b + 0.25) * SR)]
goc = {(d['shot'], j): (p['tep'], c['bd'], c['kt']) for p in rec['phan'] for d in p['doan'] for j, c in enumerate(d['cau'])}
def tl(sh, i, seed, alt): return [(t['tep'], t['bd'], t['kt']) for t in T if t['shot'] == sh and t['i'] == i and t['seed'] == seed and (t.get('alias_thu') or [None, None])[1] == alt][0]
KH = [[goc[c] for c in CAU], [tl(*c, 19102027, None) for c in CAU], [tl(*c, 19102026, 'issmus') for c in CAU], [tl(*c, 19102026, 'isthmus') for c in CAU]]
out = []
for k, kh in enumerate(KH):
    for j, (p, a, b) in enumerate(kh): out += [cat(p, a, b), np.zeros(int(0.8 * SR), np.float32)]
    out.append(np.zeros(int(1.2 * SR), np.float32))
x = np.concatenate(out); g = 10 ** ((-14 - lib.integrated(x[:, None])) / 20); x = np.clip(x * g, -0.85, 0.85)
f = K.H / 'nghe/isthmus-so-sanh.mp3'; lib.write(str(f), x[:, None], codec='libmp3lame', extra=('-b:a', '128k')); print(f, lib.ebur128(str(f)))
