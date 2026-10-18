"""T3 khoá lời · từ script-v4-KHOA.md sinh (1) loi-khoa.txt = văn bản đọc cuối (khuôn T2: giữ đầu chương [NN PART], mỗi shot một đoạn, bỏ mã shot/claim,
chữ trên hình, tấm im lặng và shot không lời); (2) từ điển phát âm cho Eric · eleven_multilingual_v2 — model này CHỈ nhận luật alias (phoneme bị bỏ qua,
tài liệu ElevenLabs "Pronunciation dictionaries", đọc 18/10/2026) → PLS chỉ có <alias>; IPA để tham khảo trong JSON; PLS phân biệt hoa/thường;
(3) loi-khoa.tts-preview.txt = lời sau khi áp alias (chỉ để kiểm + đếm ký tự; KHÔNG gửi đi); (4) LOI-KHOA.sha256 (khuôn T2, sha256sum).
KHÔNG gọi ElevenLabs. Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/khoa-loi/lam_loi_khoa.py"""
import hashlib, json, re, sys
from pathlib import Path
from xml.sax.saxutils import escape
HERE = Path(__file__).resolve().parent; EP = HERE.parent; PA = HERE / 'phat-am'
sys.path.insert(0, str(EP / 'g1')); from kiem_loi import year, parse  # noqa: E402  (cùng bộ đọc năm với kiểm chữ G1)

md = (EP / 'script-v4-KHOA.md').read_text()
L, ch = [], None
for line in md.splitlines():
    m = re.match(r'^(\[\d\d \w+\])', line)
    if m: L += ['', m.group(1)]; continue
    m = re.match(r'^‹[^›]+›\s*(.*)', line)
    if m:
        t = re.sub(r'\s*\{[^}]*\}', '', m.group(1)).replace('‹Our read› ', '').replace('[IM LẶNG]', '').strip()
        if t: L += ['', t]
txt = '\n'.join(L).strip() + '\n'
assert '{' not in txt and '‹' not in txt and 'TRÊN HÌNH' not in txt
(EP / 'loi-khoa.txt').write_text(txt)

# --- từ điển: (chữ viết, alias đọc, IPA tham khảo, loại, ghi chú) ---
D = [('18 October 2026', 'the eighteenth of October, twenty twenty-six', '', 'ngày', 'ngày khoá lời (5i) đọc kiểu Anh')]
for y in sorted(set(re.findall(r'\b(1[0-9]{3}|20[0-9]{2})\b', txt))):
    D.append((y, year(int(y)), '', 'năm', 'năm đọc kiểu Anh (bộ đọc g1/kiem_loi.year)'))
D += [
 ('La Línea de la Concepción', 'La LEE-neh-ah deh la Kon-sep-SYON', 'la ˈlinea ðe la konsepˈsjon', 'địa danh TBN', 'giọng Andalucía (seseo) — cách người địa phương đọc'),
 ("La Línea's", "La LEE-neh-ah's", 'la ˈlinea', 'địa danh TBN', 'sở hữu cách'),
 ('La Línea', 'La LEE-neh-ah', 'la ˈlinea', 'địa danh TBN', '3 âm tiết: lí-ne-a'),
 ('San Roque', 'San ROH-keh', 'san ˈroke', 'địa danh TBN', 'không đọc kiểu Anh "roke"'),
 ('Algeciras', 'Al-heh-SEE-rahs', 'alxeˈsiɾas', 'địa danh TBN', 'giọng Andalucía (seseo); chuẩn Castilla: al-xe-θi-ɾas'),
 ('Cádiz', 'KAH-deeth', 'ˈkaðiθ', 'địa danh TBN', 'chỉ có trên hình ở bản khoá — dự phòng nếu lời đổi'),
 ('Tangier', 'tan-JEER', 'tænˈdʒɪə', 'địa danh', 'cách đọc Anh chuẩn'),
 ('Utrecht', 'YOO-trekt', 'ˈjuːtrɛkt', 'địa danh', 'cách đọc Anh chuẩn'),
 ('Diego de Salinas', 'dee-AY-go deh sah-LEE-nahs', 'ˈdjeɣo ðe saˈlinas', 'tên người', 'thống đốc Tây Ban Nha 1704'),
 ('Hesse-Darmstadt', 'Hessa Darm-shtat', 'ˈhɛsə ˈdarmʃtat', 'tên người', 'hoàng tử Georg von Hessen-Darmstadt'),
 ('Rooke', 'Rook', 'rʊk', 'tên người', 'Đô đốc George Rooke — đọc "rook"'),
 ('Duc de Crillon', 'Dook duh Kree-YOHN', 'dyk də kʁijɔ̃', 'tên người', 'Louis des Balbes de Berton de Crillon'),
 ("d'Arçon", 'dar-SOHN', 'daʁsɔ̃', 'tên người', 'kỹ sư Pháp, ç = s'),
 ('Montero', 'mon-TEH-roh', 'monˈteɾo', 'tên người', 'sử gia Tây Ban Nha 1860'),
 ('Eliott', 'EL-ee-ut', 'ˈɛliət', 'tên người', 'tướng George Augustus Eliott (một chữ l, hai chữ t)'),
 ("Ince's", "Inss's", 'ɪns', 'tên người', 'Trung sĩ Henry Ince — một âm tiết'),
 ('fait accompli', 'fayt a-kom-PLEE', 'fɛt‿akɔ̃pli', 'cụm từ', 'tiếng Pháp trong lời Anh'),
 ('isthmus', 'ISS-muss', 'ˈɪsməs', 'từ thường', 'không đọc âm "th"'),
]
seen = set()
for g, *_ in D: assert g not in seen, g; seen.add(g)
miss = [g for g, *_ in D if g not in txt and g != 'Cádiz']
assert not miss, ('mục từ điển không có trong lời', miss)
pls = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<lexicon version="1.0" xmlns="http://www.w3.org/2005/01/pronunciation-lexicon" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
       '  xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"',
       '  alphabet="ipa" xml:lang="en-GB">',
       '  <!-- K2C-T3-01 Gibraltar · giọng Eric · eleven_multilingual_v2 (chỉ alias). Sinh bằng khoa-loi/lam_loi_khoa.py từ lời khoá 18/10/2026. -->']
for g, a, *_ in sorted(D, key=lambda x: -len(x[0])):   # cụm dài trước (La Línea de la Concepción trước La Línea)
    pls += ['  <lexeme>', f'    <grapheme>{escape(g)}</grapheme>', f'    <alias>{escape(a)}</alias>', '  </lexeme>']
pls.append('</lexicon>')
(PA / 'gibraltar-eric.pls').write_text('\n'.join(pls) + '\n')
(PA / 'tu-dien.json').write_text(json.dumps({'voice': 'Eric', 'model': 'eleven_multilingual_v2', 'luat': 'alias (model không nhận phoneme)', 'muc': [dict(viet=g, doc=a, ipa=i, loai=k, ghi_chu=n) for g, a, i, k, n in D]}, ensure_ascii=False, indent=1) + '\n')
tts = txt
for g, a, *_ in sorted(D, key=lambda x: -len(x[0])): tts = re.sub(r'(?<![\w-])' + re.escape(g) + r'(?![\w])', a, tts)
(PA / 'loi-khoa.tts-preview.txt').write_text(tts)
body = '\n'.join(l for l in txt.splitlines() if l and not l.startswith('['))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
(EP / 'LOI-KHOA.sha256').write_text(''.join(f'{sha(EP / n)}  {n}\n' for n in ('script-v4-KHOA.md', 'loi-khoa.txt')) + f'{sha(PA / "gibraltar-eric.pls")}  khoa-loi/phat-am/gibraltar-eric.pls\n')
print(f'loi-khoa.txt: {len(body.split())} từ viết, {len(body)} ký tự (ElevenLabs tính ký tự lời đọc ≈ {len(body)}); từ điển {len(D)} mục; tts-preview {len(tts)} ký tự')
print((EP / 'LOI-KHOA.sha256').read_text())
