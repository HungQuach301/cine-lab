#!/opt/cine/bin/python
"""BAN-CUOI-T4-B2a · sinh design/k2v/ldn/bc/look3-b1d.js = bản sao bc/look3-b1.js (KHÔNG sửa) + lớp NGƯỜI/XE L3 của look2d.js (buildDan/danMat/updateDan,
chép nguyên khối từ look2d.js; chỉ hiện khi máy < 95 m) — cho shot bảng v4 "D 3D look2d tầm phố" (H2-04a; sau: H2-05s, H5-02s) để vừa giữ mọi sửa D-A4 của
look3-b1 (niên đại, vật liệu, thuyền…) vừa có người/xe tầm phố. Dữ liệu đoạn phố: $LDN_DATA/look3d/dan.json (anim/dan_du_lieu.py, chép từ look2/).
Kiểm số lần khớp mỗi chỗ chèn = 1.  tao_look3_b1d.py"""
import hashlib, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
L = f'{REPO}/design/k2v/ldn'; src = open(f'{L}/bc/look3-b1.js').read(); d = open(f'{L}/look2d.js').read()
a = d.index('// ---------------------------------------------------------------- ANIMATIC-T4 · L3'); b = d.index('function setTime(f) {'); khoi = d[a:b]
def thay(s, cu, moi):
    assert s.count(cu) == 1, (cu, s.count(cu)); return s.replace(cu, moi)
h = hashlib.sha256(src.encode()).hexdigest()
out = f'// BAN-CUOI-T4-B2a · look3-b1d = BẢN SAO bc/look3-b1.js (sha256 {h}, KHÔNG sửa) + lớp người/xe L3 của look2d.js (sinh bằng scripts/k2ldn/bc/tao_look3_b1d.py).\n' + src
out = thay(out, 'await buildTrees(base); await buildBoats(base); await buildChimneySmoke(base);', 'await buildTrees(base); await buildBoats(base); await buildChimneySmoke(base); await buildDan(base);')
out = thay(out, '\nfunction setTime(f) {', '\n' + khoi + 'function setTime(f) {')
out = thay(out, '  updateBoats(U.uYear.value, night > 0.5, hour >= 0);\n', '  updateBoats(U.uYear.value, night > 0.5, hour >= 0);\n  updateDan(U.uYear.value, f.t || 0, night, hour, h40);\n')
open(f'{L}/bc/look3-b1d.js', 'w').write(out); print('look3-b1d.js', len(out.splitlines()), 'dòng', hashlib.sha256(out.encode()).hexdigest()[:16])
