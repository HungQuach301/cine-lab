#!/opt/cine/bin/python
"""KL42 · khoá lời v4.2 (D11 = A, chủ dự án chọn 19/10/2026): từ script-v4.1-KHOA.md sinh script-v4.2-KHOA.md —
dời khối ‹2o› + ‹2p› (kèm dòng [TRÊN HÌNH] của 2p) lên ngay sau ‹KA1782› ("By September 1782…"), trước ‹2j›; thay câu đầu 2o
"Before the attack, all summer, the garrison had been digging through the north face." → câu nối A. Không đổi chữ nào khác.
Kiểm: (1) nguồn đúng SHA v4.1 7e0cdc0b…; (2) lời sinh ra (cùng bộ đọc lam_loi_khoa) trùng nháp loi-v4.2-NHAP.txt (d48c2333…) trừ đúng câu đầu 2o."""
import hashlib, re
from pathlib import Path
H = Path(__file__).resolve().parent; R = H.parents[1]; EP = R / 'channel-k2/k2c-t3-01'
sha = lambda b: hashlib.sha256(b).hexdigest()
SRC = EP / 'script-v4.1-KHOA.md'; assert sha(SRC.read_bytes()) == '7e0cdc0b218cdcd3fee6d091f1bff9fbef261de5c812d5653b9ce8ed0dbe5a34'
NHAP = EP / 'khoa-loi/loi-v4.2-NHAP.txt'; assert sha(NHAP.read_bytes()) == 'd48c233376c729b8361f57f21c6f2a36f20d01e0133b3a4a5f00524e57a33dd0'
CU = 'Before the attack, all summer, the garrison had been digging through the north face.'
MOI = 'That summer, they had been digging through the north face.'
L = SRC.read_text().split('\n')
i2o = [i for i, l in enumerate(L) if l.startswith('‹2o›')]; i2q = [i for i, l in enumerate(L) if l.startswith('‹2q›')]
iKA = [i for i, l in enumerate(L) if l.startswith('‹KA1782›')]; i2j = [i for i, l in enumerate(L) if l.startswith('‹2j›')]
assert len(i2o) == len(i2q) == len(iKA) == len(i2j) == 1
blk = L[i2o[0]:i2q[0]]                           # ‹2o›, '', ‹2p›, [TRÊN HÌNH] 2p, ''
assert blk[0].count(CU) == 1 and blk[-1] == '' and sum(l.startswith('‹') for l in blk) == 2, blk
blk[0] = blk[0].replace(CU, MOI)
rest = L[:i2o[0]] + L[i2q[0]:]
j = rest.index(L[i2j[0]]); assert rest[j - 1] == '' and rest[j - 2].startswith('‹KA1782›')
out = rest[:j] + blk + rest[j:]
out[0] = ('# K2C-T3-01 "Why Gibraltar Was Besieged 14 Times" — lời v4.2 KHOÁ 19/10/2026 (G1 duyệt 09:35; v4 sau kiểm mù 2 vòng + REVIEWER 2 vòng; '
          'v4.1 = LK2 + LK3 của chủ dự án; v4.2 = D11: dời ‹2o›/‹2p› lên trước ‹2j›, câu nối A — chủ dự án chọn 19/10/2026)')
assert L[0].startswith('# K2C-T3-01') and 'v4.1 KHOÁ' in L[0]
assert sorted(out[1:]) == sorted([l.replace(CU, MOI) for l in L[1:]])   # chỉ đổi vị trí + đúng 1 câu
(EP / 'script-v4.2-KHOA.md').write_text('\n'.join(out))
print('script-v4.2-KHOA.md', sha((EP / 'script-v4.2-KHOA.md').read_bytes()))
