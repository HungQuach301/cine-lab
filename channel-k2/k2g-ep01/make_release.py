#!/opt/cine/bin/python
"""K2G-01 · gói phát hành (CHUAN-KENH-LL §13–14 áp cho kênh 2): mô tả (chương theo timeline thật, nguồn, miễn trừ, "facts as of", ghi công CC BY),
.en.srt khớp master, 3 tiêu đề dạng câu hỏi tìm kiếm, SHA256SUMS. Không thumbnail hoàn chỉnh (chủ dự án tự tạo theo PACKAGING-BRIEF).
  make_release.py <timeline.json> <thư mục out có master/shorts> <thư mục phat-hanh>"""
import hashlib, json, os, shutil, sys, yaml
H = os.path.dirname(os.path.abspath(__file__))
tl_p, O, D = sys.argv[1:4]; os.makedirs(D, exist_ok=True)
TL = json.load(open(tl_p)); E = yaml.safe_load(open(f'{H}/episode.yaml'))
CH = {'00': 'The question', '01': 'Three layers', '02': 'Layer 1: the site at Braddock', '03': 'Four tons of material for one ton of steel',
      '04': 'Owning the coke, and Homestead', '05': '1901: United States Steel', '06': 'Myth vs. record: is U.S. steel dying?',
      '07': 'Layer 2: Section 232 tariffs', '08': 'Overcapacity and the EU quotas', '09': 'The golden share', '10': 'Layer 3: a price on carbon (CBAM)',
      '11': 'Hydrogen steel: what the record shows', '12': 'The mechanism', '13': 'The answer'}
mmss = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
TITLES = ["Is American Steel Dying? What 1950 vs 2025 Really Shows",   # CHÍNH (chủ dự án 12/10, D5)
          "Why Is Steel Guarded Like a Weapon? Who Controls the Path"]   # DỰ PHÒNG Test & Compare
# Loại (D5): "Who Really Controls Steel? Tariffs, a Golden Share, a Carbon Toll" — cụm "who really controls" cấm ở QUAN-TRI-RUI-RO §1.2
src_lines = []
for k, s in E['sources'].items(): src_lines.append(f"- {s['short']}: {s['url']} (accessed {s['accessed']})")
desc = f"""This video explains how the system works. It isn't financial or investment advice. Facts as of 11 October 2026.
Why is steel, a metal America still makes in large amounts, now guarded like a weapon? Three layers, one mechanism: who controls the path from raw material to market, and who sets the tolls along it.

Ongoing events (tariffs, CBAM, Stegra, the Nippon Steel–U.S. Steel terms) may have changed since 11 October 2026.
Lines marked "our read" are the channel's interpretation; calculations marked "our calculation" are ours, from the cited figures.

CHAPTERS
""" + '\n'.join(f"{mmss(s['t0'])} {CH[s['id']]}" for s in TL['segments']) + """

SOURCES
""" + '\n'.join(src_lines) + """

NOTES ON THE NUMBERS
- 1950 U.S. output is USGS "raw steel"; 2025 is worldsteel "crude steel". Shares are our calculations from those figures.
- China's 2025 exports (OECD) and U.S. crude-steel output (worldsteel) are different measures, compared by weight only.
- CO₂ per tonne by route: worldsteel averages (2024 data), its own method. CBAM counts direct emissions under its own rules; we do not multiply the two.
- The 745 Mt excess-capacity figure is an OECD projection for 2028.

CREDITS
Narration: synthetic voice (ElevenLabs). 3D scenes and graphics made for this video; no logos or real people depicted.
Music by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0 — https://creativecommons.org/licenses/by/4.0/
  "Half Mystery", "Beauty Flow", "Tyrant", "Sincerely"
Sound effects: Work With Sounds / Sounds of Changes (via Europeana), CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/
  Recordings by Konrad Gutkowski (ThyssenKrupp Steel Europe, Duisburg: blast furnace tapping, hot rolling, pusher furnace); Technical Museum of Slovenia (Metal Ravne: UHP furnace, scrap, cutting steel);
  Werstas (Port of Rauma gantry crane; Virtsu wind turbine); Museum of Municipal Engineering (Gdańsk DCT terminal; ship "Sołdek" siren); Torsten Nilsson (foghorn, Gislövsläge);
  Helena Tornqvist (Saltsjöbanan train, 1912); Irena Marušič (Trbovlje-Hrastnik mine locomotive); La Fonderie (fire of the forge).
Font: Inter (SIL Open Font License 1.1).
"""
open(f'{D}/description.en.txt', 'w').write(desc)
open(f'{D}/titles.txt', 'w').write(f'CHÍNH: {TITLES[0]} ({len(TITLES[0])} ký tự)\nDỰ PHÒNG (Test & Compare): {TITLES[1]} ({len(TITLES[1])} ký tự)\n'
                                  'LOẠI (chủ dự án 12/10, QUAN-TRI-RUI-RO §1.2): Who Really Controls Steel? Tariffs, a Golden Share, a Carbon Toll\n')
srt = f"{O}/{TL['id']}.en.srt"; shutil.copy(srt, f'{D}/{TL["id"]}.en.srt')
files = [f for f in [f'{O}/{TL["id"]}-v1-master.mp4'] + [f'{O}/shorts/{TL["id"]}-short-{s["id"]}.mp4' for s in TL['shorts']] if os.path.exists(f)] + [f'{D}/{TL["id"]}.en.srt', f'{D}/description.en.txt']
with open(f'{D}/SHA256SUMS.txt', 'w') as fh:
    for f in files: fh.write(hashlib.sha256(open(f, 'rb').read()).hexdigest() + '  ' + os.path.basename(f) + '\n')
print(json.dumps(dict(files=[os.path.basename(f) for f in files], titles=TITLES, chapters=len(TL['segments'])), ensure_ascii=False))
