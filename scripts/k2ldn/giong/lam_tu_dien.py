#!/opt/cine/bin/python
"""GIONG-T4 · từ điển phát âm T4 (G1 · eleven_multilingual_v2 chỉ nhận ALIAS — phoneme bị bỏ qua, như T3 lam_loi_khoa.py).
Luật alias GIỌNG-CHỐT Đ3 + GC-C: chữ thường, không âm tiết VIẾT HOA; chỉ thêm alias khi G1 đọc sai ở lượt nghe thử (reports/giong-t4/phat-am/*.json).
Sinh: khoa-loi/phat-am/tu-dien.json (mục + IPA tham khảo + căn cứ) · khoa-loi/phat-am/london-g1.pls · khoa-loi/phat-am/loi-khoa.tts-preview.txt (chữ gửi sau alias)."""
import json, re, sys
from pathlib import Path
from xml.sax.saxutils import escape
R = Path(__file__).resolve().parents[3]; EP = R / 'channel-k2/k2c-t4-02'; PA = EP / 'khoa-loi/phat-am'; PA.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(R / 'reports/casting-giong')); import kiem_lib as KL   # noqa: E402  (bộ đọc năm, chỉ đọc)
txt = (EP / 'loi-khoa.txt').read_text()
TEN = json.loads((PA / 'ten-chon.json').read_text())   # mục tên chốt sau nghe thử: [{viet, doc, ipa, loai, ghi_chu}]
D = []
TENS = r'(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety) (one|two|three|four|five|six|seven|eight|nine)\b'
gach = lambda w: re.sub(r'\boh (\w+)', r'oh-\1', re.sub(TENS, r'\1-\2', w))   # 'sixteen sixty-six', 'seventeen oh-eight' (như T3)
for y in sorted(set(re.findall(r'\b(1[0-9]{3}|20[0-9]{2})\b(?!s)', txt))):
    D.append(dict(viet=y, doc=gach(KL.year(int(y))), ipa='', loai='năm', ghi_chu='năm đọc kiểu Anh (kiem_lib.year, như T3)'))
for m in re.findall(r'\b(?:mid-)?(?:1[0-9]{3})s\b', txt):
    if any(d['viet'] == m for d in D): continue
    y = int(re.search(r'\d{4}', m).group()); w = KL.year(y)
    w = (w[:-1] + 'ies') if w.endswith('y') else w + 's'
    D.append(dict(viet=m, doc=('mid-' if m.startswith('mid-') else '') + w, ipa='', loai='thập niên', ghi_chu='thập niên đọc kiểu Anh'))
D += TEN
seen = set()
for d in D: assert d['viet'] not in seen, d['viet']; seen.add(d['viet'])
miss = [d['viet'] for d in D if not re.search(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', txt)]
assert not miss, ('mục từ điển không có trong lời', miss)
for d in D: assert not re.search(r'[A-Z]{2,}', d['doc']), ('alias VIẾT HOA (trái Đ3/GC-C)', d)
pls = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<lexicon version="1.0" xmlns="http://www.w3.org/2005/01/pronunciation-lexicon" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
       '  xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"',
       '  alphabet="ipa" xml:lang="en-GB">',
       '  <!-- K2C-T4-02 London · giọng G1 (Voice Design VDLncRBHDjLHBqLhQ1Qt) · eleven_multilingual_v2 (chỉ alias). Sinh bằng scripts/k2ldn/giong/lam_tu_dien.py (GIONG-T4, 24/10/2026); alias theo Đ3/GC-C: chữ thường. -->']
for d in sorted(D, key=lambda x: -len(x['viet'])):
    pls += ['  <lexeme>', f"    <grapheme>{escape(d['viet'])}</grapheme>", f"    <alias>{escape(d['doc'])}</alias>", '  </lexeme>']
(PA / 'london-g1.pls').write_text('\n'.join(pls + ['</lexicon>']) + '\n')
(PA / 'tu-dien.json').write_text(json.dumps(dict(voice='G1 (Voice Design, voice_id VDLncRBHDjLHBqLhQ1Qt)', model='eleven_multilingual_v2', luat='alias (model không nhận phoneme); chữ thường (Đ3/GC-C)', muc=D), ensure_ascii=False, indent=1) + '\n')
tts = txt
for d in sorted(D, key=lambda x: -len(x['viet'])): tts = re.sub(r'(?<![\w-])' + re.escape(d['viet']) + r'(?![\w])', d['doc'], tts)
(PA / 'loi-khoa.tts-preview.txt').write_text(tts)
body = '\n'.join(l for l in tts.splitlines() if l and not l.startswith('['))
print(f'từ điển {len(D)} mục ({len(TEN)} tên); chữ gửi sau alias {len(body)} ký tự')
