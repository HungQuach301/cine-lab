#!/opt/cine/bin/python
"""K2C-T2-01 · gói phát hành theo docs/CHUAN-KENH-K2.md §1–2 (khuôn k2c-t1-06/make_release.py):
mô tả ≤ 5 000 ký tự Unicode (miễn trừ, "Facts as of", chương theo timeline THẬT, ghi chú số liệu, ghi công ngắn + nhạc/SFX CC BY lấy NGUYÊN VĂN cột "Ghi công"
của RIGHTS.md cho đúng các tệp có trong đặc tả, câu dẫn bình luận ghim); bình luận ghim ≤ 10 000 ký tự (mọi URL + ngày truy cập, bản ghi ảnh/tài liệu/footage,
giấy phép); 3 tiêu đề (J5: chính = tiêu đề 1); .en.srt; SHA256SUMS phủ master, Short, .srt, mô tả, bình luận ghim (+ tiêu đề, brief, ảnh nền).
Năm/số trong mô tả chỉ lấy từ lời khoá hoặc claims (BAI-HOC-LL #53). Không làm thumbnail (chủ dự án tự làm theo PACKAGING-BRIEF, Test & Compare: T-B mặc định — J5).
  make_release.py <timeline.json> <thư mục out (master, shorts/)> <thư mục phat-hanh> [--v v1]"""
import csv, hashlib, json, os, re, shutil, sys, yaml
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(f'{H}/../..')
tl_p, O, D = sys.argv[1:4]; V = sys.argv[sys.argv.index('--v') + 1] if '--v' in sys.argv else 'v1'; os.makedirs(D, exist_ok=True)
TL = json.load(open(tl_p)); E = yaml.safe_load(open(f'{H}/episode.yaml'))
CH = {'00': 'Three ships a day', '01': 'Richmond, 1940: the order comes first', '02': 'The Jones Act and the end of a subsidy',
      '03': '"It\'s the wages" and what the record says', '04': 'Ulsan, 1972: an empty beach', '05': 'Today: a petition, a finding, a fee and a pause', '06': 'What to watch'}
mmss = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
TITLES = ["Why America Builds So Few Ships (It's Not Just Wages)",              # CHÍNH (J5, chủ dự án 15/10)
          "In 1943, America Launched 3 Ships a Day. Why Does It Build So Few Now?",
          "From Richmond to Ulsan: Why America Builds So Few Ships"]


def rights_credit():
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
src_lines = [f"- {s['short']}: {s['url']} (accessed {s['accessed']})" for s in E['sources'].values()]
item_lines = [f"- {r['clip_id']}: {r['url_trang']} — {r['giay_phep'].split(' (licenses')[0]}" for r in SF]
item_lines += ["- Aerial imagery: USDA FSA NAIP 2022 via USGS The National Map (USGSNAIPPlus), public domain",
               "- Terrain: USGS 3DEP; SRTM / GMTED2010 (USGS) via AWS Terrain Tiles; Canada: Open Government Licence – Canada; Natural Earth (public domain); NASA Blue Marble",
               "- Federal Register / USTR page images: works of the U.S. Government"]
desc = f"""In 1943, at the peak, America launched three cargo ships a day. In a 2026 report, Congress's researchers put America's share of world shipbuilding tonnage at 0.04 percent. So why does America build so few ships? You'll often hear: wages. The record says something narrower.

This video explains how the system works. It isn't financial or investment advice. Facts as of 15 October 2026. Fees, investments, contracts and bills mentioned here can change after that date.
Lines marked "our read" are the channel's interpretation. Company stories marked "by the company's account" come from the company's own history; the banknote story is a newspaper column's account (lore), not a record.

CHAPTERS
""" + '\n'.join(f"{mmss(s['t0'])} {CH[s['id']]}" for s in TL['segments']) + """

SOURCES
All """ + str(len(src_lines)) + """ sources (with links and access dates) and the item page of every archival photo, film and document are listed in the pinned comment.

NOTES ON THE NUMBERS
- 0.04 percent is a share of world shipbuilding tonnage (CRS, 2026); "around five a year" counts ships (CRS, 2023). Different measures, different eras.
- "About four times the global price" is one consulting firm's estimate for one ship type (cited by CRS, 2019).
- Output per person for South Korea is in current dollars (World Bank), not adjusted for inflation.

CREDITS
Narration: synthetic voice (ElevenLabs). Maps, 3D objects and animation are our own; no logos or real people depicted in them.
Archival photos: Library of Congress (FSA/OWI; National Photo Company) — no known restrictions. Film: United News newsreel (1944), U.S. National Archives.
Aerial imagery: U.S. Department of Agriculture, Farm Service Agency (NAIP 2022), via USGS The National Map. Terrain: 3DEP, GMTED2010 and SRTM terrain data courtesy of the U.S. Geological Survey; Canada terrain data contains information licensed under the Open Government Licence – Canada; Natural Earth; NASA Blue Marble.
Music by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0 — https://creativecommons.org/licenses/by/4.0/
""" + '\n'.join(f'  {m}' for m in mus) + """
Sound effects: Work With Sounds / Sounds of Changes (via Europeana), CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/
""" + '\n'.join(f'  {s}' for s in sfx) + """
Fonts: Inter (SIL Open Font License 1.1).

Next: why one country makes almost all the world's shipping containers.
"""
assert len(desc) <= 5000, f'mô tả {len(desc)} ký tự > 5000'
open(f'{D}/description.en.txt', 'w').write(desc)
pin = ("SOURCES (accessed dates in brackets)\n" + '\n'.join(src_lines) + "\n\nPHOTOS, FILM, IMAGERY AND DOCUMENTS (item pages and licences)\n" + '\n'.join(item_lines) + "\n")
assert len(pin) <= 10000, f'bình luận ghim {len(pin)} ký tự > 10000'
open(f'{D}/nguon-binh-luan-ghim.en.txt', 'w').write(pin)
open(f'{D}/titles.txt', 'w').write(f'CHÍNH (J5): {TITLES[0]} ({len(TITLES[0])} ký tự)\nPHƯƠNG ÁN 2: {TITLES[1]} ({len(TITLES[1])} ký tự)\nPHƯƠNG ÁN 3: {TITLES[2]} ({len(TITLES[2])} ký tự)\nThumbnail mặc định Test & Compare: T-B (J5)\n')
srt = f"{O}/{TL['id']}.en.srt"
if os.path.exists(srt): shutil.copy(srt, f'{D}/{TL["id"]}.en.srt')
files = [f for f in [f'{O}/{TL["id"]}-{V}-master.mp4'] + [f'{O}/shorts/{TL["id"]}-short-{s["id"]}.mp4' for s in TL['shorts']] + [f'{D}/{n}' for n in (f'{TL["id"]}.en.srt', 'description.en.txt', 'nguon-binh-luan-ghim.en.txt', 'titles.txt', 'PACKAGING-BRIEF.md', 'nen-1.jpg', 'nen-2.jpg', 'nen-3.jpg')] if os.path.exists(f)]
with open(f'{D}/SHA256SUMS.txt', 'w') as fh:
    for f in files: fh.write(hashlib.sha256(open(f, 'rb').read()).hexdigest() + '  ' + os.path.basename(f) + '\n')
print(json.dumps(dict(files=[os.path.basename(f) for f in files], mo_ta=len(desc), ghim=len(pin), chapters=len(TL['segments']), music=len(mus), sfx=len(sfx)), ensure_ascii=False))
