#!/opt/cine/bin/python
"""K2C-T1-06 · ghép đặc tả tập: ep-src.yaml (hình, nguồn, số) + lời khoá v8.2 NGUYÊN VĂN từ script.md → episode.yaml.
Lời mỗi đoạn = phần văn bản sau nhãn [NN PART] trong script.md, bỏ mã claim {Cnn}, gộp đoạn văn bằng một khoảng trắng (đúng chuỗi gửi ElevenLabs, khoá cache).
Shorts: lời lấy nguyên văn từ các câu của script.md (`vo_from: [đoạn, câu đầu, câu cuối]` trong ep-src.yaml) — không thêm thông tin mới."""
import os, re, sys, yaml
H = os.path.dirname(os.path.abspath(__file__))


def script_vo():
    txt = open(f'{H}/script.md').read(); segs = {}; cur = None; buf = []
    for line in txt.split('\n'):
        m = re.match(r'^\[(\d\d) [A-Z0-9 \-]+\]\s*$', line.strip())
        if m:
            if cur: segs[cur] = buf
            cur, buf = m.group(1), []; continue
        if cur is not None: buf.append(line)
    if cur: segs[cur] = buf
    out = {}
    for k, L in segs.items():
        s = ' '.join(x.strip() for x in L if x.strip() and not x.startswith('>') and not x.startswith('#'))
        s = re.sub(r'\s*\{C\d+\}', '', s); s = re.sub(r'\s+', ' ', s).strip(); out[k] = s
    return out


def sentences(s):
    return [x for x in re.split(r'(?<=[.?!])\s+(?=[A-Z"“])', s) if x]


if __name__ == '__main__':
    VO = script_vo(); src = yaml.safe_load(open(f'{H}/ep-src.yaml'))
    src['heroes'] = yaml.safe_load(open(f'{H}/ep-src-heroes.yaml'))['heroes']
    SG = yaml.safe_load(open(f'{H}/ep-src-segs.yaml')); src['segments'] = SG['segments']; src['shorts'] = SG.get('shorts', [])
    # Cách viết số cho TTS (13/10/2026): ElevenLabs đọc "4,440" thành ~"4,040" và "377,000" sai nhóm (ASR small.en + medium.en, đoạn 05, 08).
    # Viết bằng chữ ĐÚNG những từ của lời khoá v8.2 — không đổi từ nào được nói; script.md giữ chữ số.
    TTS_SPELL = {'4,440': 'four thousand four hundred forty', '377,000': 'three hundred seventy-seven thousand'}
    for s in src['segments']:
        if s.get('vo') == '@script':
            s['vo'] = VO[s['id']]
            for k, v in TTS_SPELL.items(): s['vo'] = s['vo'].replace(k, v)
    assert [s['id'] for s in src['segments']] == sorted(VO), (sorted(VO), [s['id'] for s in src['segments']])
    for sh in src.get('shorts', []):
        f = sh.pop('vo_from', None)
        if f:
            S = sentences(VO[f[0]]); i0 = next(i for i, x in enumerate(S) if x.startswith(f[1])); i1 = next(i for i, x in enumerate(S) if x.startswith(f[2]))
            sh['vo'] = ' '.join(S[i0:i1 + 1])
    # Q32 (FOOTAGE.md §3, 13/10/2026): shot ảnh/trang quét nguồn ngoài khai p.clip (dòng sổ SOURCES-FOOTAGE.csv), p.file (tệp GỐC đã tải, ngoài repo,
    # để K kiểm SHA) và p.setting (nơi theo nội dung hình, nhãn ft/…; cùng nơi cùng nhãn). Trang dựng lại chữ (IBC, CFR) không có tệp nguồn ngoài → không khai.
    sys.path.insert(0, os.path.abspath(f'{H}/../../scripts/k2')); import k2v_assets as KA
    import importlib.util; sp = importlib.util.spec_from_file_location('sfl', f'{H}/sf_ledger.py'); SFL = importlib.util.module_from_spec(sp); sp.loader.exec_module(SFL)
    SETTING = {'LOC-DET-01': 'ft/pittsburgh-fifth-and-wood', 'LOC-DET-02': 'ft/columbus-broad-and-high', 'LOC-DET-03': 'ft/buffalo-delaware-and-north',
               'LOC-DET-04': 'ft/washington-connecticut-ave', 'LOC-DET-05': 'ft/detroit-pasadena-apartments', 'LOC-DET-06': 'ft/nyc-riverside-drive',
               'LOC-DET-12': 'ft/nyc-riverside-drive', 'LOC-DET-08': 'ft/burlington-main-and-st-paul', 'LOC-DET-11': 'ft/detroit-lenox-apartments',
               'LOC-FSA-01': 'ft/durham-corner-store', 'LOC-FSA-03': 'ft/nyc-61st-street-rear', 'LOC-FSA-04': 'ft/washington-corner-store',
               'LOC-HABS-01': 'ft/nyc-st-nicholas-ave', 'LOC-HABS-02': 'ft/tocco-store-north-third-st', 'LOC-HABS-03': 'ft/dade-apartment-building',
               'LOC-HABS-04': 'ft/butte-west-granite', 'WM-HOOVER-1928': 'ft/hoover-portrait-1928', 'WM-SUTHERLAND-1937': 'ft/supreme-court-steps-1937',
               'PXP-7180335': 'ft/bay-ridge-brooklyn', 'DOC-SSZEA': 'ft/page-sszea-1926', 'DOC-EUCLID': 'ft/page-us-reports-272'}
    for s in src['segments']:
        for sh in s['shots']:
            p = sh.get('p') or {}; o = (src['heroes'].get(p.get('hero')) or {}).get('opt', {}); f = o.get('img') or o.get('page')
            if p.get('clip') or not f: continue
            a = SFL.asset_of(f); cid = SFL.clip_of_asset(a)
            if cid: p['clip'] = cid; p['file'] = os.path.join(KA.CACHE, KA.ASSETS[a]['file']); p['setting'] = SETTING[cid]
    # Q21 (13/10/2026, QC nháp): dòng nguồn trên hình phải chứa nguồn của mọi số/câu đang hiện. ll.py chỉ gộp nguồn khi p.src là DANH SÁCH khoá,
    # nên chuỗi tự do được đổi thành khoá: ảnh/footage → bản ghi ảnh (trang LoC/Pexels của đúng tệp, đã đọc đủ bản ghi), bản đồ → MAPC (NASA Blue Marble);
    # "3D illustration" và ghi chú "our calculation" chuyển sang p.credit (góc phải, cùng hàng). Câu chú thích ảnh (nơi chốn, năm) lấy nguồn = bản ghi ảnh.
    import csv as _csv
    LED = {r['clip_id']: r for r in _csv.DictReader(open(f'{H}/SOURCES-FOOTAGE.csv'))}
    LOCITEM = {'WM-HOOVER-1928': 'https://www.loc.gov/pictures/item/2016888786/', 'WM-SUTHERLAND-1937': 'https://www.loc.gov/pictures/item/2016877918/'}
    S = src['sources']; N = src['numbers']
    S['MAPC'] = dict(short='Map: Natural Earth, U.S. Census · Imagery: NASA Earth Observatory', url='https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/base-topography-bathymetry/', read='fulltext', accessed='2026-10-12', onscreen=True)
    PRE = {'Source: Census ACS 2024 (table B25024) · share is our calculation · 3D illustration': (['ACS24'], 'Share: our calculation · 3D illustration'),
           'Sources: Census ACS 2024 (B25024) · Census New Residential Construction · shares are our calculation': (['ACS24', 'NRC'], 'Shares: our calculation'),
           'Sources: Census ACS 2024 · Census New Residential Construction 2025 · shares are our calculation · 3D illustration': (['ACS24', 'NRC'], 'Shares: our calculation · 3D illustration'),
           'Data: Census ACS 2024 (B25127), our calculation · ': (['ACS24'], 'Data: our calculation'),
           'Source: A Standard State Zoning Enabling Act (1926) · ': (['SSZEA'], None), 'Source: Euclid v. Ambler Realty (1926) · ': (['EUCLID'], None)}

    def shot_keys(p):   # nguồn của số (tags/labels/places/cap num) đang hiện trong shot
        ks = set()
        def walk(o):
            if isinstance(o, dict):
                if o.get('num') in N: ks.add(N[o['num']]['src'])
                for v in o.values(): walk(v)
            elif isinstance(o, list): [walk(v) for v in o]
        walk({k: v for k, v in p.items() if k != 'src'}); return ks
    for s in src['segments'] + src['shorts']:
        for sh in s['shots']:
            p = sh.get('p') or {}; x = p.get('src')
            if not isinstance(x, str): continue
            keys, credit = [], None
            i = max(x.find('Photo: '), x.find('Footage: '))
            if i >= 0 and p.get('clip') in LED:
                pre, lab, cid = x[:i], x[i:], p['clip']; k = 'PH-' + cid
                S.setdefault(k, dict(short=lab, url=LOCITEM.get(cid, LED[cid]['url_trang']), read='fulltext', accessed=LED[cid]['ngay_tai_utc'][:10], onscreen=True))
                keys.append(k)
                if pre: kk, credit = PRE[pre]; keys += kk
                for c in p.get('cap') or []:
                    if 'num' not in c and not isinstance(c.get('src'), list): c['src'] = [k]
            elif x.startswith('Map: '): keys = ['MAPC']
            elif x in PRE: keys, credit = PRE[x]
            elif x == '3D illustration':
                ks = shot_keys(p) | {k for c in p.get('cap') or [] if isinstance(c.get('src'), list) for k in c['src']}
                if not ks: continue
                keys, credit = sorted(ks), '3D illustration'
            else: raise SystemExit(f'chuỗi nguồn chưa khai: {x}')
            p['src'] = sorted(set(keys) | shot_keys(p))
            if credit: p['credit'] = credit
    for s in src['segments'] + src['shorts']:   # câu chưa khai nguồn trong shot có danh sách nguồn → nguồn của shot (số/năm/cơ quan trên câu đến từ đúng các nguồn đó)
        for sh in s['shots']:
            p = sh.get('p') or {}
            if isinstance(p.get('src'), list) and p['src']:
                for c in p.get('cap') or []:
                    if 'num' not in c and 'src' not in c: c['src'] = list(p['src'])
    hd = '# TỆP SINH TỰ ĐỘNG bởi make_spec.py từ ep-src.yaml + script.md (lời khoá v8.2). Sửa ep-src.yaml, không sửa tệp này.\n'
    open(f'{H}/episode.yaml', 'w').write(hd + yaml.safe_dump(src, allow_unicode=True, sort_keys=False, width=4000))
    n = sum(len(s['vo'].split()) for s in src['segments'])
    print('episode.yaml', len(src['segments']), 'đoạn,', sum(len(s['shots']) for s in src['segments']), 'shot,', len(src['heroes']), 'cảnh,', n, 'từ lời,', sum(len(s['vo']) for s in src['segments']), 'ký tự')
