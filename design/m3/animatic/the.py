"""Cine Lab · M2.1 — khung tĩnh cho animatic: thẻ dữ liệu theo bộ mẫu B3 (bo_mau.Frame) và thẻ PLACEHOLDER cho tài sản chưa có.
Chữ trong hình bằng tiếng Anh. Số liệu chỉ lấy từ kịch bản V2 / bảng shot (đã duyệt); số chưa chốt thì để placeholder, không bịa.
/opt/cine/bin/python design/m3/animatic/the.py <thư mục ra>   → <id>.png (1920×1080) + tuong-phan.json
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../thu-phong-cach'))
from bo_mau import Frame, NIGHT, PAPER, AMBER, COLD, GREY, INK, AMBER_D, BLUE, MINUS, W, H, src

def title(f, t, sub=None):
    f.text((96, 70), t, 64, PAPER, 'serifb')
    if sub: f.text((96, 160), sub, 34, GREY)

def ill(f, s='Illustrative'): f.text((W - 96, 84), s, 30, GREY, 'sans', 'rs')

def num(o, big, lines, source, color=AMBER, sub=None, seed=401):
    f = Frame(seed); f.text((96, 260), big, 170, color, 'serifb')
    for i, l in enumerate(lines): f.text((100, 520 + i * 60), l, 44, PAPER)
    if sub: f.text((100, 520 + len(lines) * 60 + 20), sub, 34, GREY)
    src(f, source); return f.save(o)

def mapc(o, place, big, lines, source, tag='Illustrative · Not to scale', seed=402, dots=COLD, river=True):
    f = Frame(seed); f.sheet(96, 150, 1000, 800, seed + 7)
    if river: f.line([(110, 760), (330, 700), (560, 780), (800, 720), (1080, 790)], BLUE, 40)
    st = [[(150, 330), (1040, 330)], [(150, 470), (900, 470)], [(260, 230), (360, 690)], [(520, 230), (600, 690)], [(800, 260), (860, 690)], [(150, 600), (980, 620)]]
    for s in st: f.line(s, INK, 8)
    for s in st[:3]:
        for i in range(10): u = (i + 0.5) / 10; f.dot(s[0][0] + (s[1][0] - s[0][0]) * u, s[0][1] + (s[1][1] - s[0][1]) * u, 7, dots, INK)
    f.text((140, 200), place, 54, INK, 'serifb')
    if big: f.text((1170, 300), big, 130, AMBER, 'serifb')
    for i, l in enumerate(lines): f.text((1174, 500 + i * 56), l, 40, PAPER)
    ill(f, tag); src(f, source); return f.save(o)

def t3c(o, head, cols, source, seed=403):
    f = Frame(seed); title(f, head)
    for i, (h, n, lines) in enumerate(cols):
        x = 96 + i * 590; f.sheet(x, 200, 540, 720, seed + i)
        f.text((x + 40, 260), h, 40, INK, 'sansb'); f.text((x + 40, 330), n, 100 if len(n) > 4 else 140, AMBER_D, 'serifb')
        for k, l in enumerate(lines): f.text((x + 40, 540 + k * 52), l, 38, INK)
    src(f, source); return f.save(o)

def bars(o, head, sub, items, source, seed=404):
    """thanh ngang, cùng thang từ 0, nhãn trực tiếp có dấu +/−"""
    f = Frame(seed); title(f, head, sub); vmax = max(abs(v) for _, v, _ in items); x0, wmax = 760, 900
    for i, (lab, v, txt) in enumerate(items):
        y = 270 + i * 130; w = wmax * abs(v) / vmax
        f.text((x0 - 30, y + 30), lab, 40, PAPER, 'sans', 'rm')
        f.rect([x0, y + 4, x0 + 22, y + 56], COLD if v < 0 else AMBER); f.rect([x0, y + 22, x0 + w, y + 38], COLD if v < 0 else AMBER)
        f.text((x0 + w + 24, y + 30), txt, 44, COLD if v < 0 else AMBER, 'serifb', 'lm')
    f.line([(x0, 250), (x0, 270 + len(items) * 130)], PAPER, 3)
    src(f, source); return f.save(o)

def grid(o, big, lines, source, off=False, seed=405):
    f = Frame(seed); f.sheet(1000, 150, 820, 800, seed + 3); cx, cy, s = 1050, 230, 27
    for k in range(270):
        i, j = k % 27, k // 27; x, y = cx + i * s, cy + j * s * 1.5
        if off and k == 200: f.rect([x, y, x + s - 7, y + s * 1.5 - 9], None, INK, 2)
        else: f.rect([x, y, x + s - 7, y + s * 1.5 - 9], BLUE)
    f.text((96, 280), big, 120, AMBER, 'serifb')
    for i, l in enumerate(lines): f.text((100, 480 + i * 58), l, 42, PAPER)
    src(f, source); return f.save(o)

def srcc(o, head, lines, seed=406):
    f = Frame(seed); f.sheet(260, 220, 1400, 620, seed + 1); f.text((330, 300), head, 72, INK, 'serifb')
    for i, l in enumerate(lines): f.text((334, 460 + i * 64), l, 40, BLUE)
    return f.save(o)

def num4(o, rows, source, seed=407):
    f = Frame(seed)
    for i, (n, l) in enumerate(rows): y = 120 + i * 220; f.text((96, y), n, 100, AMBER if i != 3 else COLD, 'serifb'); f.text((1080, y + 62), l, 44, PAPER)
    src(f, source); return f.save(o)

def card(o, big, sub, seed=408):
    f = Frame(seed); f.text((W // 2, 430), big, 96, AMBER, 'serifb', 'mm'); f.text((W // 2, 560), sub, 44, PAPER, 'sans', 'mm'); return f.save(o)

def ph(o, sid, desc, seed=409):
    """PLACEHOLDER rõ ràng: khung đứt, nhãn, mô tả hình (tiếng Anh)"""
    f = Frame(seed)
    for x in range(140, 1780, 60): f.rect([x, 150, x + 30, 156], GREY); f.rect([x, 924, x + 30, 930], GREY)
    for y in range(150, 930, 60): f.rect([140, y, 146, y + 30], GREY); f.rect([1774, y, 1780, y + 30], GREY)
    f.text((W // 2, 300), 'PLACEHOLDER · ' + sid, 56, AMBER, 'sansb', 'mm')
    words, ln, out = desc.split(' '), '', []
    for w_ in words:
        if len(ln) + len(w_) > 46: out.append(ln); ln = w_
        else: ln = (ln + ' ' + w_).strip()
    out.append(ln)
    for i, l in enumerate(out): f.text((W // 2, 460 + i * 70), l, 48, PAPER, 'sans', 'mm')
    f.text((W // 2, 860), 'new asset — not built yet', 34, GREY, 'sans', 'mm'); return f.save(o)

EH, BG, NPR, BLS = 'Source: English Heritage', 'Source: British Gas (2023)', 'Source: NPR (2015)', 'Source: U.S. BLS Employment Projections 2025–35 · U.S. projection'
SPEC = {
 '02-01': lambda o: card(o, 'THE LAST LAMPLIGHTERS', 'Last Lamplighters · episode 1'),
 '02-02': lambda o: mapc(o, 'LONDON', '1807', ['Pall Mall', 'first street lit by gas'], EH, dots=AMBER),
 '02-03': lambda o: ph(o, '02-03', 'Cut-paper crowd silhouettes staring at the first gas lamps, Pall Mall 1807 · Illustrative'),
 '02-04': lambda o: t3c(o, 'London lights up', [('FIRST STREET', '1807', ['Pall Mall', 'lit by gas']), ('FIRST COMPANY', '1812', ['gas company gets', 'royal charter']), ('A BRIDGE', '1813', ['Westminster Bridge', 'glowing'])], 'Sources: English Heritage; Gas Light & Coke Co. charter (1812)'),
 '02-05': lambda o: mapc(o, 'LONDON', '40,000+', ['gas lamps by the 1820s', 'some 215 miles of street'], EH, dots=AMBER),
 '02-06': lambda o: num(o, '40,000', ['gas lamps in London, 1820s', 'hold on to this number'], EH),
 '03-03': lambda o: mapc(o, 'A ROUND', None, [], 'Illustrative route', dots=AMBER, river=False),
 '04-01': lambda o: mapc(o, 'ATLANTIC', '1816', ["Rembrandt Peale's museum,", 'Baltimore: gas as a show'], 'Source: see description', dots=AMBER),
 '04-02': lambda o: ph(o, '04-02', "Facade of Peale's museum, Baltimore, 1816 (new building asset)"),
 '04-03': lambda o: ph(o, '04-03', "Market Street, Baltimore, 7 Feb 1817: America's first public gas street lamp (new facade)"),
 '04-04': lambda o: mapc(o, 'PARIS', 'mid-1800s', ['boulevards', 'run on gas'], 'Source: see description', dots=AMBER),
 '05-03': lambda o: mapc(o, 'PARIS', '1878', ["Avenue de l'Opéra:", '64 electric arc lamps'], 'Source: see description'),
 '05-04': lambda o: mapc(o, 'NEW YORK', '1880', ['electric lights', 'on Broadway'], 'Source: see description'),
 '06-01': lambda o: mapc(o, 'MANHATTAN', 'April 1907', ['lamplighters on strike', 'parts of the city dark'], 'Source: see description', tag='Illustrative', dots=AMBER),
 '06-02': lambda o: ph(o, '06-02', 'Newspaper page redrawn, headline paraphrased, April 1907 · source: Library of Congress'),
 '06-03': lambda o: ph(o, '06-03', 'Police officers climbing lamp posts with matches: cut-paper silhouettes on the street set'),
 '06-04': lambda o: ph(o, '06-04', 'Crowd silhouettes on the street set: the men back at work within a week'),
 '08-01': lambda o: ph(o, '08-01', 'Covent Garden at night: amber gas lamps among white LED lights (new set)'),
 '08-02': lambda o: num(o, '~1,500 ' + '→' + ' ~1,100', ['gas street lamps in London', '2015 ' + '→' + ' 2023'], 'Sources: NPR (2015); British Gas (2023)'),
 '08-03': lambda o: ph(o, '08-03', 'Modern lamplighter silhouette: hi-vis jacket, aluminium ladder, long shot (fictional)'),
 '08-04': lambda o: num(o, '5', ['lamplighters', 'look after them'], BG),
 '08-05': lambda o: ph(o, '08-05', 'Insert: clock mechanism inside a gas lamp, wound every two weeks (new prop)'),
 '08-06': lambda o: ph(o, '08-06', 'Covent Garden set: Westminster LED proposal (2022); Grade II listing (2024)'),
 '08-07': lambda o: t3c(o, 'London, then and now', [('1820s', '40,000', ['gas lamps']), ('2023', '~1,100', ['gas lamps']), ('2023', '5', ['lamplighters'])], 'Sources: English Heritage; British Gas (2023)'),
 '11-01': lambda o: ph(o, '11-01', 'Transition: lamp flames turn into grid squares (new graphic)'),
 '11-02': lambda o: grid(o, '~270', ['occupations', '1950 U.S. Census ' + '→' + ' 2010'], 'Source: J. Bessen (2016), NBER · 271 occupations listed'),
 '11-03': lambda o: grid(o, '1', ['vanished mainly because', 'a machine took over the work:', 'the elevator operator'], 'Source: J. Bessen (2016), NBER', off=True),
 '11-04': lambda o: num(o, '1 of ~270', ['Only 1 of ~270 occupations was', 'eliminated mainly by automation'], 'Source: J. Bessen (2016), NBER · 271 occupations listed'),
 '12-01': lambda o: num(o, MINUS + '34%', ['word processors and typists', 'U.S. projection 2025–35'], BLS, color=COLD),
 '12-02': lambda o: bars(o, 'Fastest-shrinking U.S. jobs', 'Projected change 2025–35 · same scale', [('Word processors, typists', -34, MINUS + '34%'), ('Telephone operators', -28, MINUS + '28%'), ('Switchboard operators', -25, '≈ ' + MINUS + '25%'), ('Data entry keyers', -25, '≈ ' + MINUS + '25%'), ('Telemarketers', -20, '≈ ' + MINUS + '20%')], BLS),
 '12-03': lambda o: num(o, '~3,500', ['telephone operators left (2025)', 'projected ' + MINUS + '28% by 2035'], BLS, color=COLD),
 '12-04': lambda o: srcc(o, 'Forecasts, not verdicts', ['U.S. Bureau of Labor Statistics', 'Employment Projections 2025–35, Table 1.5']),
 '13-01': lambda o: bars(o, 'Where BLS expects AI to cut demand', 'U.S. projection 2023–33 · same scale', [('Customer service reps', -5, MINUS + '5%'), ('Auto damage appraisers', -9, '≈ ' + MINUS + '9%'), ('Software developers', 18, '≈ +18%')], 'Source: U.S. BLS Monthly Labor Review (Feb 2025) · U.S. projection 2023–33'),
 '13-02': lambda o: num(o, '+30% or more', ['nurse practitioners · solar installers', 'data scientists · wind turbine technicians'], BLS),
 '13-03': lambda o: num(o, '~19% below', ['expected employment, ages 22–25,', 'in the most AI-exposed jobs (June 2026)'], 'Source: Stanford Digital Economy Lab (2026)', color=COLD),
 '13-04': lambda o: srcc(o, 'An early signal, not proof', ['Stanford Digital Economy Lab (2026)', 'U.S. BLS Monthly Labor Review (Feb 2025)']),
 '14-01': lambda o: num4(o, [('40,000 → ~1,100', 'gas lamps, London'), ('5', 'lamplighters today'), ('1 of ~270', 'jobs gone mainly to automation'), (MINUS + '34%', 'typists, U.S. projection 2025–35')], 'Sources: English Heritage; British Gas; J. Bessen; U.S. BLS'),
 '14-04': lambda o: card(o, 'Who are the last lamplighters of our time?', 'Last Lamplighters · Every era has its last lamplighters'),
}

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True); rep = {}
    for k, fn in SPEC.items(): rep[k] = fn(f'{out}/{k}.png')
    json.dump(rep, open(f'{out}/tuong-phan.json', 'w'), ensure_ascii=False, indent=1)
    worst = sorted(((t['ratio'], k, t['text']) for k, r in rep.items() for t in r))[:3]; print(len(rep), 'thẻ · tương phản thấp nhất', worst)
