#!/opt/cine/bin/python
"""K2C-T1-06 · gói phát hành (CHUAN-KENH-LL §13–14 áp cho kênh 2; khuôn k2g-ep01/make_release.py): mô tả (chương theo timeline thật, nguồn, miễn trừ,
"facts as of", ghi công CC BY lấy NGUYÊN VĂN từ cột "Ghi công" của RIGHTS.md cho đúng các tệp nhạc/SFX có trong đặc tả, nguồn ảnh/footage theo SOURCES-FOOTAGE.csv),
.en.srt khớp master, 3 tiêu đề dạng câu hỏi, SHA256SUMS. Không thumbnail hoàn chỉnh (chủ dự án tự tạo theo PACKAGING-BRIEF).
  make_release.py <timeline.json> <thư mục out có master/shorts> <thư mục phat-hanh>"""
import csv, hashlib, json, os, re, shutil, sys, yaml
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(f'{H}/../..')
tl_p, O, D = sys.argv[1:4]; os.makedirs(D, exist_ok=True)
TL = json.load(open(tl_p)); E = yaml.safe_load(open(f'{H}/episode.yaml'))
CH = {'00': 'The question', '01': 'The building on the corner', '02': 'Lock 1: the map (1916–1926)', '03': 'The map today',
      '04': 'Lock 2: the stairwell', '05': 'Is one stair safe? What the record shows', '06': 'Lock 3: the bank line at four homes',
      '07': 'Other forces: costs, rates, rents', '08': 'What the numbers show since the 1970s', '09': 'Myth vs. record: does upzoning work?',
      '10': 'Where the rules are changing', '11': 'The answer'}
mmss = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
TITLES = ["Why Did America Almost Stop Building Small Buildings Like This?",   # CHÍNH (chủ dự án duyệt D3, 12/10/2026; titles.txt)
          "What Happened to America's Small Apartment Buildings?",              # DỰ PHÒNG — YouTube Test & Compare
          "Why Are Duplexes to Fourplexes So Rare Among New US Homes?"]         # phương án 3 (G1a §7; không dùng)


def rights_credit():
    """{đường dẫn tệp: câu ghi công} từ RIGHTS.md (cột 'Ghi công', bỏ tiền tố **Bắt buộc ghi công**:)"""
    out = {}
    for line in open(f'{ROOT}/RIGHTS.md'):
        c = line.split('|')
        if len(c) < 11 or not re.match(r'\s*K2-(MUS|SFX)-\d+', c[1]): continue
        f = re.search(r'`(assets/k2/[^`]+)`', c[2])
        if f: out[f.group(1)] = re.sub(r'^\s*\*\*Bắt buộc ghi công\*\*[^:]*:\s*', '', c[8]).strip()
    return out


RC = rights_credit()
used = sorted(set(re.findall(r'assets/k2/(?:music|sfx)/[\w.-]+\.mp3', open(f'{H}/episode.yaml').read())))
missing = [u for u in used if u not in RC]
assert not missing, f'thiếu ghi công RIGHTS.md: {missing}'
mus = [RC[u] for u in used if '/music/' in u]; sfx = [RC[u] for u in used if '/sfx/' in u]
SF = list(csv.DictReader(open(f'{H}/SOURCES-FOOTAGE.csv')))
loc = sorted({r['clip_id'] for r in SF if r['clip_id'].startswith('LOC-')})
px = [r for r in SF if r['clip_id'].startswith('PX')]
cc = [r['yeu_cau_ghi_cong'] for r in SF if r['giay_phep'].startswith('CC BY')]
src_lines = [f"- {s['short']}: {s['url']} (accessed {s['accessed']})" for s in E['sources'].values()]
desc = f"""This video explains how the system works. It isn't financial or investment advice. Facts as of 12 October 2026.
About one in thirteen American homes sits in a building with two to four apartments. Of the new homes finished in 2025, about one in a hundred did. Three sets of rules shape new ones — the map, the stairwell and the bank line — and building costs, borrowing costs and rents weigh on whether the numbers work. Our read: the record doesn't pin the decline on any single one.

Zoning, building-code and housing-law reforms are ongoing and may have changed since 12 October 2026.
Lines marked "our read" are the channel's interpretation; calculations marked "our calculation" are ours, from the cited figures.

CHAPTERS
""" + '\n'.join(f"{mmss(s['t0'])} {CH[s['id']]}" for s in TL['segments']) + """

SOURCES
""" + '\n'.join(src_lines) + """

NOTES ON THE NUMBERS
- "One in thirteen" (Census ACS 2024, homes in buildings with 2–4 units) and "one in a hundred" (Census completions, 2025) are two different counts; the shares are our calculation.
- Small apartment buildings of five to nineteen units: our sum of two columns of the Census multifamily series (5–9 and 10–19 units).
- Single-family shares pool 1970 through 1974 (our calculation).

CREDITS
Narration: synthetic voice (ElevenLabs). 3D scenes, maps and graphics made for this video; no logos or real people depicted in them.
Maps: NASA Blue Marble: Next Generation imagery (NASA Earth Observatory).
Archival photos: Library of Congress, Prints & Photographs Division (Detroit Publishing Company Collection; Farm Security Administration/Office of War Information Collection; Historic American Buildings Survey) and Harris & Ewing Collection — no known restrictions on publication.
Documents: A Standard State Zoning Enabling Act (U.S. Dept. of Commerce, 1926, via Internet Archive); U.S. Reports, vol. 272 (Library of Congress). Code and regulation excerpts are re-typeset, not facsimiles.
Stock footage and photo: Pexels (""" + ', '.join(sorted(r['clip_id'] for r in px)) + """).
""" + ('\n'.join(cc) + '\n' if cc else '') + """Music by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0 — https://creativecommons.org/licenses/by/4.0/
""" + '\n'.join(f'  {m}' for m in mus) + """
Sound effects: Work With Sounds / Sounds of Changes (via Europeana), CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/
""" + '\n'.join(f'  {s}' for s in sfx) + """
Fonts: Inter (SIL Open Font License 1.1); DejaVu Serif for re-typeset excerpts (Bitstream Vera License).
"""
open(f'{D}/description.en.txt', 'w').write(desc)
open(f'{D}/titles.txt', 'w').write(f'CHÍNH: {TITLES[0]} ({len(TITLES[0])} ký tự)\nDỰ PHÒNG (Test & Compare): {TITLES[1]} ({len(TITLES[1])} ký tự)\nPHƯƠNG ÁN 3 (không dùng): {TITLES[2]} ({len(TITLES[2])} ký tự)\n')
srt = f"{O}/{TL['id']}.en.srt"
if os.path.exists(srt): shutil.copy(srt, f'{D}/{TL["id"]}.en.srt')
files = [f for f in [f'{O}/{TL["id"]}-v1-master.mp4'] + [f'{O}/shorts/{TL["id"]}-short-{s["id"]}.mp4' for s in TL['shorts']] + [f'{D}/{TL["id"]}.en.srt', f'{D}/description.en.txt'] if os.path.exists(f)]
with open(f'{D}/SHA256SUMS.txt', 'w') as fh:
    for f in files: fh.write(hashlib.sha256(open(f, 'rb').read()).hexdigest() + '  ' + os.path.basename(f) + '\n')
print(json.dumps(dict(files=[os.path.basename(f) for f in files], titles=TITLES, chapters=len(TL['segments']), music=len(mus), sfx=len(sfx), loc=len(loc)), ensure_ascii=False))
