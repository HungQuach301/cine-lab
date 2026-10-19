#!/opt/cine/bin/python
"""GIỌNG-CHỐT · Đ3: sửa alias trong từ điển khoá (chữ thường, không âm tiết VIẾT HOA) — PLS + tu-dien.json + loi-khoa.tts-preview.txt;
cập nhật CHỈ dòng PLS trong LOI-KHOA.sha256. loi-khoa.txt KHÔNG đổi (kiểm SHA 0fdc72ce… trước và sau). Ghi sua-pls.json (trước/sau)."""
import hashlib, json, re
from pathlib import Path
from xml.sax.saxutils import escape
H = Path(__file__).resolve().parent; R = H.parents[1]; EP = R / 'channel-k2/k2c-t3-01'; PA = EP / 'khoa-loi/phat-am'
PLS, TD, PV, SH = PA / 'gibraltar-eric.pls', PA / 'tu-dien.json', PA / 'loi-khoa.tts-preview.txt', EP / 'LOI-KHOA.sha256'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
LOI_SHA = '0fdc72ce81e33b6f4efc8234a52dafc5410d4448c26c0a0feb3eb01abaa71753'
assert sha(EP / 'loi-khoa.txt') == LOI_SHA
D3 = {'Eliott': 'Elliot', 'fait accompli': 'fet ah-kom-plee', 'La Línea': 'la lee-nay-ah', "La Línea's": "la lee-nay-ah's",
      'La Línea de la Concepción': 'la lee-nay-ah deh la Kon-sep-SYON',   # chỉ phần "La Línea" theo Đ3; "de la Concepción" giữ (G1 đọc đúng ở casting)
      'Montero': 'mon-tair-oh', "d'Arçon": 'dar-sohn'}                    # Cádiz giữ dự phòng (KAH-deeth), để tai người
td = json.loads(TD.read_text()); doi = []
for m in td['muc']:
    if m['viet'] in D3 and m['doc'] != D3[m['viet']]:
        doi.append(dict(viet=m['viet'], truoc=m['doc'], sau=D3[m['viet']])); m['doc'] = D3[m['viet']]
        m['ghi_chu'] += ' · Đ3 GIỌNG-CHỐT 19/10/2026: alias chữ thường (âm tiết VIẾT HOA bị đọc thành chữ cái/viết tắt ở casting)'
assert len(doi) == len(D3), doi
td['voice'] = 'G1 (Voice Design, voice_id VDLncRBHDjLHBqLhQ1Qt — chủ dự án chọn 18/10 và 19/10/2026; trước đó: Eric)'
TD.write_text(json.dumps(td, ensure_ascii=False, indent=1) + '\n')
D = [(m['viet'], m['doc']) for m in td['muc']]
pls = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<lexicon version="1.0" xmlns="http://www.w3.org/2005/01/pronunciation-lexicon" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
       '  xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"',
       '  alphabet="ipa" xml:lang="en-GB">',
       '  <!-- K2C-T3-01 Gibraltar · giọng G1 (Voice Design) · eleven_multilingual_v2 (chỉ alias). Sinh bằng khoa-loi/lam_loi_khoa.py từ lời khoá 18/10/2026; '
       'sửa alias Đ3 (chữ thường) bằng reports/giong-chot/sua_pls.py 19/10/2026. Tên tệp giữ "eric" để không đổi đường dẫn đã khoá. -->']
for g, a in sorted(D, key=lambda x: -len(x[0])):
    pls += ['  <lexeme>', f'    <grapheme>{escape(g)}</grapheme>', f'    <alias>{escape(a)}</alias>', '  </lexeme>']
pls.append('</lexicon>')
truoc = sha(PLS); PLS.write_text('\n'.join(pls) + '\n'); sau = sha(PLS)
tts = (EP / 'loi-khoa.txt').read_text()
for g, a in sorted(D, key=lambda x: -len(x[0])): tts = re.sub(r'(?<![\w-])' + re.escape(g) + r'(?![\w])', a, tts)
pv_truoc = len(PV.read_text()); PV.write_text(tts)
lines = SH.read_text().splitlines(keepends=True); n = 0
for i, l in enumerate(lines):
    if not l.startswith('#') and l.rstrip().endswith('  khoa-loi/phat-am/gibraltar-eric.pls'): lines[i] = f'{sau}  khoa-loi/phat-am/gibraltar-eric.pls\n'; n += 1
assert n == 1; SH.write_text(''.join(lines))
assert sha(EP / 'loi-khoa.txt') == LOI_SHA
out = dict(doi=doi, pls_sha_truoc=truoc, pls_sha_sau=sau, preview_ky_tu_truoc=pv_truoc, preview_ky_tu_sau=len(tts), loi_khoa_sha=LOI_SHA, so_muc=len(D))
json.dump(out, open(H / 'sua-pls.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
