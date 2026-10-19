#!/opt/cine/bin/python
"""KL42 · GC-C′ (đề xuất, CHỜ chủ dự án duyệt): isthmus 'iss-muss' → 'issmus'. Lý do (thay.json, kiem-tap.json): với 'iss-muss', 3/3 câu có isthmus ở bản thu
cả tập chỉ NGHI ("Isesmus"/"Icesmus"); thu lại seed 19102027 còn tệ hơn ("ice muss", "ice moss", "I.S. Musse" — đọc thành chữ cái). Thử 3 alias trên cùng 3 câu,
seed 19102026: 'isthmus' (không alias) 3/3 ĐÚNG, 'issmus' 3/3 ĐÚNG, 'iss-mus' 1/3. Chọn 'issmus': giữ ý gốc của từ điển (không đọc âm "th"), chữ thường, không gạch.
Sửa tu-dien.json + PLS + preview; thay dòng PLS trong LOI-KHOA.sha256. loi-khoa.txt không đổi."""
import hashlib, json, re
from pathlib import Path
from xml.sax.saxutils import escape
H = Path(__file__).resolve().parent; R = H.parents[1]; EP = R / 'channel-k2/k2c-t3-01'; PA = EP / 'khoa-loi/phat-am'
PLS, TD, PV, SH = PA / 'gibraltar-eric.pls', PA / 'tu-dien.json', PA / 'loi-khoa.tts-preview.txt', EP / 'LOI-KHOA.sha256'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
LOI_SHA = '51d1c7735a106efdefc3f466ad77ea03cabdade4d38e7d513cc0e5227d6e431c'; assert sha(EP / 'loi-khoa.txt') == LOI_SHA
truoc = sha(PLS); assert truoc == '8242b87b12a42334a946bc4850db4079f44722b57a8c0670d0bbb815de59397e'
td = json.loads(TD.read_text()); m = [x for x in td['muc'] if x['viet'] == 'isthmus'][0]; assert m['doc'] == 'iss-muss'
m['doc'] = 'issmus'; m['ghi_chu'] += " · GC-C′ KL42 19/10/2026 (CHỜ DUYỆT): 'iss-muss' bị đọc 'ice-muss'/'I.S.' → 'issmus' (3/3 câu ĐÚNG cả hai cách nghe)"
TD.write_text(json.dumps(td, ensure_ascii=False, indent=1) + '\n')
s = PLS.read_text(); old = '    <grapheme>isthmus</grapheme>\n    <alias>iss-muss</alias>'; assert s.count(old) == 1
s = s.replace(old, '    <grapheme>isthmus</grapheme>\n    <alias>issmus</alias>').replace('+ GC-C chữ thường hết (reports/kl42/sua_pls_gcc.py) 19/10/2026.',
                                                                                    '+ GC-C chữ thường hết (reports/kl42/sua_pls_gcc.py) + GC-C′ isthmus (reports/kl42/sua_pls_isthmus.py, chờ duyệt) 19/10/2026.')
PLS.write_text(s); sau = sha(PLS)
D = [(x['viet'], x['doc']) for x in td['muc']]; tts = (EP / 'loi-khoa.txt').read_text()
for g, a in sorted(D, key=lambda x: -len(x[0])): tts = re.sub(r'(?<![\w-])' + re.escape(g) + r'(?![\w])', a, tts)
PV.write_text(tts)
L = SH.read_text().splitlines(keepends=True); n = 0
for i, l in enumerate(L):
    if not l.startswith('#') and l.rstrip().endswith('  khoa-loi/phat-am/gibraltar-eric.pls'): L[i] = f'# cũ (GC-C, KL42 trước GC-C′): {l}'; L.insert(i + 1, f'{sau}  khoa-loi/phat-am/gibraltar-eric.pls\n'); n += 1; break
assert n == 1; SH.write_text(''.join(L))
out = dict(viet='isthmus', truoc='iss-muss', sau='issmus', pls_sha_truoc=truoc, pls_sha_sau=sau, preview_ky_tu=len(tts))
json.dump(out, open(H / 'sua-pls-isthmus.json', 'w'), ensure_ascii=False, indent=1); print(out)
