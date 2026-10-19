#!/opt/cine/bin/python
"""KL42 · GC-C (chủ dự án duyệt 19/10/2026): mọi alias còn âm tiết VIẾT HOA → chữ thường hết. Chạy SAU lam_loi_khoa.py (LOI=script-v4.2-KHOA.md):
lam_loi_khoa.py sinh lại PLS/tu-dien.json từ bảng gốc thời Eric (alias VIẾT HOA, chưa có Đ3) → công cụ này lấy tu-dien.json bản Đ3 (GIỌNG-CHỐT, PLS 66ed934a…,
truyền qua đối số), kiểm danh mục 47 mục trùng bản vừa sinh từ lời v4.2, áp GC-C, ghi lại PLS + tu-dien.json + loi-khoa.tts-preview.txt;
thay dòng PLS trong LOI-KHOA.sha256 và giữ các dòng '# cũ' của bản v4. Ghi sua-pls-gcc.json (trước/sau). GC-D (d'Arçon) KHÔNG áp ở đây.
Dùng: sua_pls_gcc.py <tu-dien Đ3> <LOI-KHOA.sha256 bản v4.1>"""
import hashlib, json, re, sys
from pathlib import Path
from xml.sax.saxutils import escape
H = Path(__file__).resolve().parent; R = H.parents[1]; EP = R / 'channel-k2/k2c-t3-01'; PA = EP / 'khoa-loi/phat-am'
PLS, TD, PV, SH = PA / 'gibraltar-eric.pls', PA / 'tu-dien.json', PA / 'loi-khoa.tts-preview.txt', EP / 'LOI-KHOA.sha256'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
LOI_SHA = '51d1c7735a106efdefc3f466ad77ea03cabdade4d38e7d513cc0e5227d6e431c'   # loi-khoa.txt v4.2
assert sha(EP / 'loi-khoa.txt') == LOI_SHA
d3p, sh41 = Path(sys.argv[1]), Path(sys.argv[2])
td = json.loads(d3p.read_text()); moi = json.loads(TD.read_text())
assert [m['viet'] for m in td['muc']] == [m['viet'] for m in moi['muc']], 'danh mục 47 mục đổi theo lời v4.2'
GCC = {'isthmus': 'iss-muss', 'Diego de Salinas': 'dee-ay-go deh sah-lee-nahs', 'Algeciras': 'al-heh-see-rahs', 'San Roque': 'san roh-keh',
       'Tangier': 'tan-jeer', 'Utrecht': 'yoo-trekt', 'Duc de Crillon': 'dook duh kree-yohn', 'La Línea de la Concepción': 'la lee-nay-ah deh la kon-sep-syon',
       'Cádiz': 'kah-deeth'}   # Cádiz: dự phòng (không có trong lời), áp cùng luật
doi = []
for m in td['muc']:
    if m['viet'] in GCC:
        doi.append(dict(viet=m['viet'], truoc=m['doc'], sau=GCC[m['viet']])); m['doc'] = GCC[m['viet']]
        m['ghi_chu'] += ' · GC-C KL42 19/10/2026: alias chữ thường hết (âm tiết VIẾT HOA có thể bị đọc thành chữ cái — ASR M nghe "ISS" in hoa ở GIỌNG-CHỐT)'
assert len(doi) == len(GCC)
hoa = [(m['viet'], m['doc']) for m in td['muc'] if re.search(r'[A-Z]{2}', m['doc'])]
assert not hoa, ('còn âm tiết VIẾT HOA', hoa)
TD.write_text(json.dumps(td, ensure_ascii=False, indent=1) + '\n')
D = [(m['viet'], m['doc']) for m in td['muc']]
pls = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<lexicon version="1.0" xmlns="http://www.w3.org/2005/01/pronunciation-lexicon" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
       '  xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"',
       '  alphabet="ipa" xml:lang="en-GB">',
       '  <!-- K2C-T3-01 Gibraltar · giọng G1 (Voice Design) · eleven_multilingual_v2 (chỉ alias). Sinh bằng khoa-loi/lam_loi_khoa.py từ lời khoá v4.2 19/10/2026; '
       'alias Đ3 (reports/giong-chot/sua_pls.py) + GC-C chữ thường hết (reports/kl42/sua_pls_gcc.py) 19/10/2026. Tên tệp giữ "eric" để không đổi đường dẫn đã khoá. -->']
for g, a in sorted(D, key=lambda x: -len(x[0])):
    pls += ['  <lexeme>', f'    <grapheme>{escape(g)}</grapheme>', f'    <alias>{escape(a)}</alias>', '  </lexeme>']
pls.append('</lexicon>')
sinh = sha(PLS); PLS.write_text('\n'.join(pls) + '\n'); sau = sha(PLS)
tts = (EP / 'loi-khoa.txt').read_text()
for g, a in sorted(D, key=lambda x: -len(x[0])): tts = re.sub(r'(?<![\w-])' + re.escape(g) + r'(?![\w])', a, tts)
PV.write_text(tts)
v4 = [l for l in sh41.read_text().splitlines(keepends=True) if l.startswith('# cũ (v4 ')]
lines = v4 + SH.read_text().splitlines(keepends=True); n = 0
for i, l in enumerate(lines):
    if not l.startswith('#') and l.rstrip().endswith('  khoa-loi/phat-am/gibraltar-eric.pls'): lines[i] = f'{sau}  khoa-loi/phat-am/gibraltar-eric.pls\n'; n += 1
assert n == 1 and len(v4) == 3; SH.write_text(''.join(lines))
assert sha(EP / 'loi-khoa.txt') == LOI_SHA
out = dict(doi=doi, pls_sha_d3_giong_chot='66ed934a5e041e14dee029a89522b7fcba5c83edf3c19741e2dc742179358e29', pls_sha_lam_loi_khoa_sinh_lai=sinh, pls_sha_sau=sau,
           preview_ky_tu=len(tts), loi_khoa_sha=LOI_SHA, so_muc=len(D))
json.dump(out, open(H / 'sua-pls-gcc.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
