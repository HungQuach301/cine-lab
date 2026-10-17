#!/opt/cine/bin/python
"""DÙNG CHUNG · thư viện mô hình/HDRI/vật liệu CC0 cho kênh 2 (Mốc D3, phiên V5a 15/10/2026).

  cc0_fetch.py fetch [--only id1,id2] [--dest assets/k2/cc0]   # tải, kiểm băm nguồn, ghi catalog + giấy phép + .gitattributes LFS
  cc0_fetch.py verify [--dest …]                               # tính lại SHA-256/kích thước mọi tệp so với catalog.json
  cc0_fetch.py list                                            # danh mục dự định (không gọi mạng)

Nguồn (chỉ ba nguồn chủ dự án duyệt): Poly Haven (API api.polyhaven.com, tải dl.polyhaven.org), Quaternius (trang gói quaternius.com →
thư mục Google Drive công khai của tác giả), ambientCG (API v2). Mọi tài sản CC0 1.0.
Mỗi tệp ghi: URL tải, SHA-256, kích thước; mỗi mục: trang nguồn, giấy phép, tệp giấy phép trong <dest>/licenses/ (văn bản lưu nguyên
dạng chữ, ngày tải). Tệp > 1 MB → đánh dấu LFS trong <dest>/.gitattributes. Tổng ≤ 300 MB (vượt → dừng trước khi ghi).
Proxy chặn/không tải được → KHÔNG vòng: ghi URL vào <dest>/BLOCKED-URLS.md để chủ dự án tải tay.
User-Agent theo RUNBOOK §3 (không email).
"""
import datetime as dt, hashlib, html, json, os, re, subprocess, sys, tempfile, zipfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
DEST = os.path.join(REPO, 'assets', 'k2', 'cc0')
UA = 'Mozilla/5.0 (cine-lab research; https://github.com/HungQuach301/cine-lab)'
MAX_TOTAL, LFS_MIN = 300 * 1024 * 1024, 1024 * 1024
CC0 = 'CC0 1.0 Universal (Public Domain Dedication)'
LICENSE_PAGES = {   # tệp trong licenses/ ← trang giấy phép gốc
    'cc0-1.0-legalcode.txt': 'https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt',
    'polyhaven-license.txt': 'https://polyhaven.com/license',
    'ambientcg-license.txt': 'https://docs.ambientcg.com/license/',
    'quaternius-license.txt': 'https://quaternius.com/license.html',
}
QPACK = {   # gói Quaternius: trang gói → thư mục Drive (đọc từ nút Download của trang, 15/10/2026)
    'ships': '1Qf31QTnGfxRzYxx8dHmlVGDT4KmIa0Vy', 'modulartrain': '15UgTB4JZgsSxdBDTTk0Qv1iiCbH9bdMk',
    'zombieapocalypsekit': '1mWP6sCHun7OUMHQeDNZLrXTteXlzWg_t', 'simplebuildings': '1r-FcNFxC6ziN0oI3GqZJdEkdzglFQHQH',
    'buildings': '1uWCsV9QfnAu8u_QbwkYwOfuU3McME7CA',
}
# Danh mục: chủ đề kênh — tàu, cần cẩu, container, nhà máy, nhà ở, biên giới, xe tải, tàu hỏa (+ cảng, bầu trời, vật liệu)
CATALOG = [
    dict(id='ph-overhead-crane', src='polyhaven', asset='overhead_crane', kind='model', chu_de='cần cẩu', ghi='cầu trục bến/xưởng'),
    dict(id='ph-dutch-ship-medium', src='polyhaven', asset='dutch_ship_medium', kind='model', chu_de='tàu', ghi='tàu buồm Hà Lan (cảnh quá khứ, sepia)'),
    dict(id='ph-concrete-road-barrier', src='polyhaven', asset='concrete_road_barrier', kind='model', chu_de='biên giới', ghi='rào bê tông trạm kiểm soát'),
    dict(id='ph-chainlink-fence', src='polyhaven', asset='modular_chainlink_fence', kind='model', chu_de='biên giới', ghi='hàng rào lưới, mô-đun'),
    dict(id='ph-factory-facade', src='polyhaven', asset='modular_factory_facade', kind='model', chu_de='nhà máy', ghi='mặt tiền nhà máy gạch, mô-đun'),
    dict(id='ph-industrial-pipes', src='polyhaven', asset='modular_industrial_pipes_01', kind='model', chu_de='nhà máy', ghi='ống công nghiệp, mô-đun'),
    dict(id='ph-urban-apartments', src='polyhaven', asset='modular_urban_apartments_facade', kind='model', chu_de='nhà ở', ghi='mặt tiền chung cư, mô-đun'),
    dict(id='ph-electricity-poles', src='polyhaven', asset='modular_electricity_poles', kind='model', chu_de='hạ tầng', ghi='cột điện, dây'),
    dict(id='ph-ocean-buoy', src='polyhaven', asset='ocean_buoy', kind='model', chu_de='cảng', ghi='phao luồng'),
    dict(id='ph-hdri-freight-station', src='polyhaven', asset='freight_station', kind='hdri', res='2k', chu_de='tàu hỏa', ghi='HDRI ga hàng có cần cẩu, hoàng hôn'),
    dict(id='ph-hdri-industrial-sunset', src='polyhaven', asset='industrial_sunset_02_puresky', kind='hdri', res='2k', chu_de='nhà máy', ghi='HDRI bầu trời hoàng hôn khu công nghiệp (chỉ trời)'),
    dict(id='ph-hdri-docklands', src='polyhaven', asset='docklands_02', kind='hdri', res='2k', chu_de='cảng', ghi='HDRI khu bến cảng, trời quang'),
    dict(id='q-cruise-ship', src='quaternius', pack='ships', files=['OBJ/CruiseShip.obj', 'OBJ/CruiseShip.mtl'], chu_de='tàu', ghi='tàu lớn low-poly'),
    dict(id='q-boat', src='quaternius', pack='ships', files=['OBJ/Boat.obj', 'OBJ/Boat.mtl'], chu_de='tàu', ghi='tàu nhỏ low-poly'),
    dict(id='q-cargo-train-front', src='quaternius', pack='modulartrain', files=['OBJ/CargoTrain_Front.obj', 'OBJ/CargoTrain_Front.mtl'], chu_de='tàu hỏa', ghi='đầu máy tàu hàng'),
    dict(id='q-cargo-train-container', src='quaternius', pack='modulartrain', files=['OBJ/CargoTrain_Container.obj', 'OBJ/CargoTrain_Container.mtl'], chu_de='container', ghi='toa chở container'),
    dict(id='q-railway-track', src='quaternius', pack='modulartrain', files=['OBJ/RailwayTrack_Straight.obj', 'OBJ/RailwayTrack_Straight.mtl', 'OBJ/RailwayTrack_Curve.obj', 'OBJ/RailwayTrack_Curve.mtl'], chu_de='tàu hỏa', ghi='ray thẳng + cong'),
    dict(id='q-container-red', src='quaternius', pack='zombieapocalypsekit', files=['Environment/glTF/Container_Red.gltf'], chu_de='container', ghi='container 20 ft đỏ (glTF)'),
    dict(id='q-container-green', src='quaternius', pack='zombieapocalypsekit', files=['Environment/glTF/Container_Green.gltf'], chu_de='container', ghi='container 20 ft xanh (glTF)'),
    dict(id='q-truck', src='quaternius', pack='zombieapocalypsekit', files=['Vehicles/glTF/Vehicle_Truck.gltf'], chu_de='xe tải', ghi='xe tải (glTF); dùng bản thường, không dùng bản bọc thép'),
    dict(id='q-house', src='quaternius', pack='simplebuildings', files=['OBJ/House.obj', 'OBJ/House.mtl', 'OBJ/House2.obj', 'OBJ/House2.mtl'], chu_de='nhà ở', ghi='nhà ở thấp tầng low-poly (2 kiểu)'),
    dict(id='q-building-large', src='quaternius', pack='buildings', files=['OBJ/Building1_Large.obj', 'OBJ/Building1_Large.mtl'], chu_de='nhà ở', ghi='toà nhà phố low-poly'),
    dict(id='acg-corrugated-steel', src='ambientcg', asset='CorrugatedSteel009', attr='1K-JPG', chu_de='container', ghi='vật liệu tôn sóng PBR (vỏ container, nhà xưởng)'),
]


class Blocked(Exception):
    pass


def http(url, out=None, timeout=300):
    """tải qua proxy của môi trường (curl dùng HTTPS_PROXY sẵn có); lỗi/chặn → Blocked (không thử đường vòng)."""
    a = ['curl', '-sSL', '--fail', '-A', UA, '--max-time', str(timeout), '-w', '%{http_code}']
    tmp = None
    if out is None:
        fd, tmp = tempfile.mkstemp(); os.close(fd); target = tmp
    else:
        target = out
    r = subprocess.run(a + ['-o', target, url], capture_output=True, text=True)
    if r.returncode:
        if tmp: os.unlink(tmp)
        elif os.path.exists(target): os.unlink(target)
        raise Blocked(f'{url} → curl {r.returncode} HTTP {r.stdout.strip() or "?"} {r.stderr.strip()[:120]}')
    if tmp:
        b = open(tmp, 'rb').read(); os.unlink(tmp); return b
    return None


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()


EMAIL = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}')


def redact(t):
    """ẩn email liên hệ có trên trang nguồn (RUNBOOK §3, preflight P1: không email trong repo); nội dung giấy phép giữ nguyên."""
    return EMAIL.sub('[email đã ẩn]', t)


def html_text(b):
    t = b.decode('utf-8', 'replace')
    t = re.sub(r'(?is)<(script|style|noscript|svg|head)\b.*?</\1>', ' ', t)
    t = re.sub(r'(?i)<br\s*/?>|</(p|div|h\d|li|tr|section)>', '\n', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    lines = [re.sub(r'[ \t ]+', ' ', l).strip() for l in t.splitlines()]
    out, blank = [], 0
    for l in lines:
        blank = blank + 1 if not l else 0
        if blank <= 1: out.append(l)
    return '\n'.join(out).strip() + '\n'


# ---- Google Drive công khai (thư mục tải của Quaternius) ---------------------------------------------------------------
def drive_ls(fid):
    t = http(f'https://drive.google.com/drive/folders/{fid}', timeout=60).decode('utf-8', 'replace')
    rx = re.compile(r'\\x22([A-Za-z0-9_-]{20,})\\x22,\\x5b\\x22' + re.escape(fid) + r'\\x22\\x5d,\\x22(.*?)\\x22,\\x22(.*?)\\x22')
    seen, out = set(), []
    for m in rx.finditer(t):
        if m.group(1) in seen: continue
        seen.add(m.group(1)); out.append((m.group(1), m.group(2), m.group(3).replace('\\/', '/')))
    return out


def drive_find(root, path):
    """id tệp theo đường dẫn tương đối trong thư mục gốc của gói."""
    fid = root
    parts = path.split('/')
    for i, name in enumerate(parts):
        hit = [x for x in drive_ls(fid) if x[1] == name]
        if not hit: raise Blocked(f'không thấy "{path}" trong thư mục Drive {root} (thiếu phần "{name}")')
        fid = hit[0][0]
    return fid


def drive_url(fid): return f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t'


# ---- từng nguồn ---------------------------------------------------------------------------------------------------------
def plan_polyhaven(it):
    info = json.loads(http(f'https://api.polyhaven.com/info/{it["asset"]}', timeout=60))
    files = json.loads(http(f'https://api.polyhaven.com/files/{it["asset"]}', timeout=60))
    page = f'https://polyhaven.com/a/{it["asset"]}'
    if it['kind'] == 'model':
        g = files['gltf']['1k']['gltf']
        L = [(os.path.basename(g['url']), g['url'], g['size'], g.get('md5'))]
        L += [(rel, v['url'], v['size'], v.get('md5')) for rel, v in sorted(g.get('include', {}).items())]
    else:
        h = files['hdri'][it.get('res', '2k')]['hdr']; L = [(os.path.basename(h['url']), h['url'], h['size'], h.get('md5'))]
    authors = ', '.join(info.get('authors', {}).keys())
    return dict(trang=page, tac_gia=authors, ten=info.get('name'), tep_giay_phep='licenses/polyhaven-license.txt', files=L)


def plan_quaternius(it):
    root = QPACK[it['pack']]; page = f'https://quaternius.com/packs/{it["pack"]}.html'
    L = []
    for rel in it['files']:
        fid = drive_find(root, rel); L.append((os.path.basename(rel), drive_url(fid), None, None))
        if rel.endswith('.gltf'):   # glTF có thể kèm .bin/ảnh cùng thư mục
            for x in drive_ls(drive_find(root, os.path.dirname(rel))):
                stem = os.path.splitext(os.path.basename(rel))[0]
                if x[1] != os.path.basename(rel) and x[1].startswith(stem) and not x[1].endswith('.gltf'):
                    L.append((x[1], drive_url(x[0]), None, None))
    try:   # tệp License.txt của gói (có ở hầu hết gói); không có → bằng chứng là trang gói (nút CC0) + trang giấy phép chung
        lic = (drive_url(drive_find(root, 'License.txt')), f'quaternius-{it["pack"]}-License.txt')
    except Blocked:
        lic = None
    return dict(trang=page, tac_gia='Quaternius', ten=it['id'], files=L, pack_license=lic, pack_page=page,
                tep_giay_phep=f'licenses/{lic[1]}' if lic else f'licenses/quaternius-{it["pack"]}-page.txt')


def plan_ambientcg(it):
    d = json.loads(http(f'https://ambientcg.com/api/v2/full_json?id={it["asset"]}&include=downloadData', timeout=60))
    a = d['foundAssets'][0]
    dl = next(x for x in a['downloadFolders']['default']['downloadFiletypeCategories']['zip']['downloads'] if x['attribute'] == it['attr'])
    return dict(trang=f'https://ambientcg.com/view?id={it["asset"]}', tac_gia='ambientCG (Lennart Demes)', ten=a.get('displayName'),
                tep_giay_phep='licenses/ambientcg-license.txt', zip=True, files=[(dl['fileName'], dl['fullDownloadPath'], dl['size'], None)])


PLAN = dict(polyhaven=plan_polyhaven, quaternius=plan_quaternius, ambientcg=plan_ambientcg)


def gitattributes(dest, cat):
    big = sorted(f['path'] for it in cat['items'] for f in it['files'] if f['lfs'])
    L = ['# V5a (15/10/2026): tệp > 1 MB của thư viện CC0 qua LFS (chủ dự án duyệt trong lệnh V5a, việc 5). Sinh bởi scripts/common/cc0_fetch.py.']
    L += [re.sub(r'([ #\[\]*?!])', r'\\\1', p) + ' filter=lfs diff=lfs merge=lfs -text' for p in big]
    open(os.path.join(dest, '.gitattributes'), 'w').write('\n'.join(L) + '\n')


def catalog_md(dest, cat):
    L = ['# Thư viện CC0 kênh 2 (Mốc D3)', '',
         f'Sinh bởi `scripts/common/cc0_fetch.py` ngày {cat["ngay"]}. Mọi mục **{CC0}**; văn bản giấy phép trong `licenses/`. '
         'SHA-256 từng tệp trong `catalog.json`; kiểm lại: `cc0_fetch.py verify`. Tệp > 1 MB qua LFS (`.gitattributes`).', '',
         f'Tổng: **{len(cat["items"])} mục, {sum(len(i["files"]) for i in cat["items"])} tệp, {cat["tong_bytes"] / 1e6:.1f} MB** '
         f'({sum(1 for i in cat["items"] for f in i["files"] if f["lfs"])} tệp LFS).', '',
         '| # | Mục | Chủ đề | Nguồn | Tệp | MB | Giấy phép | Ghi chú |', '|---|---|---|---|---|---|---|---|']
    for n, it in enumerate(cat['items'], 1):
        mb = sum(f['bytes'] for f in it['files']) / 1e6
        L.append(f"| {n} | `{it['id']}` | {it['chu_de']} | [{it['nguon']}]({it['trang']}) | {len(it['files'])} | {mb:.2f} | CC0 1.0 (`{it['tep_giay_phep']}`) | {it['ghi']} |")
    if cat.get('chan'):
        L += ['', f'**Không tải được: {len(cat["chan"])} URL** — xem `BLOCKED-URLS.md`.']
    open(os.path.join(dest, 'CATALOG.md'), 'w').write('\n'.join(L) + '\n')


def fetch(dest, only=None):
    os.makedirs(os.path.join(dest, 'licenses'), exist_ok=True)
    today = dt.date.today().isoformat(); blocked = []
    for fn, url in LICENSE_PAGES.items():
        try:
            b = http(url, timeout=60)
            txt = b.decode('utf-8', 'replace') if fn.endswith('legalcode.txt') else html_text(b)
            open(os.path.join(dest, 'licenses', fn), 'w').write(f'Nguồn: {url}\nTải: {today} (scripts/common/cc0_fetch.py; email trên trang đã ẩn)\n\n{redact(txt)}')
        except Blocked as e: blocked.append(dict(muc=fn, url=url, loi=str(e)))
    old = json.load(open(os.path.join(dest, 'catalog.json'))) if os.path.exists(os.path.join(dest, 'catalog.json')) else {'items': []}
    keep = {i['id']: i for i in old['items']}
    items = [it for it in CATALOG if not only or it['id'] in only]
    plans = {}
    for it in items:   # 1) lập kế hoạch (kích thước) — dừng trước khi ghi nếu vượt trần
        try: plans[it['id']] = PLAN[it['src']](it)
        except Blocked as e: blocked.append(dict(muc=it['id'], url=it.get('asset') or it.get('pack'), loi=str(e)))
    known = sum(s or 0 for p in plans.values() for _, _, s, _ in p['files'])
    if known > MAX_TOTAL: raise SystemExit(f'DỪNG: dự kiến {known / 1e6:.1f} MB > {MAX_TOTAL / 1e6:.0f} MB')
    for it in items:
        p = plans.get(it['id'])
        if not p: keep.pop(it['id'], None); continue
        d = os.path.join(dest, it['src'], it['id']); os.makedirs(d, exist_ok=True); rec = []
        try:
            if p.get('pack_license'):
                u, fn = p['pack_license']; lp = os.path.join(dest, 'licenses', fn); http(u, lp, timeout=60)
                t = open(lp, encoding='utf-8', errors='replace').read()
                if EMAIL.search(t): open(lp, 'w').write(redact(t))
            if p.get('pack_page'):   # trang gói: lưu chữ + liên kết giấy phép (bằng chứng CC0 của chính gói)
                b = http(p['pack_page'], timeout=60); links = sorted(set(re.findall(rb'https?://creativecommons\.org/[^"\'\s<>]+', b)))
                open(os.path.join(dest, 'licenses', f'quaternius-{it["pack"]}-page.txt'), 'w').write(
                    f'Nguồn: {p["pack_page"]}\nTải: {today} (scripts/common/cc0_fetch.py; email trên trang đã ẩn)\nLiên kết giấy phép trên trang: '
                    + (', '.join(x.decode() for x in links) or 'KHÔNG THẤY') + '\n\n' + redact(html_text(b)))
            for rel, url, size, h in p['files']:
                out = os.path.join(d, rel); os.makedirs(os.path.dirname(out), exist_ok=True); http(url, out)
                if size is not None and os.path.getsize(out) != size: raise Blocked(f'{url}: kích thước {os.path.getsize(out)} ≠ API {size}')
                if h and md5(out) != h: raise Blocked(f'{url}: md5 lệch API')
                if p.get('zip'):
                    with zipfile.ZipFile(out) as z:
                        for n in z.namelist():
                            if n.endswith('/') or '..' in n or n.startswith('/'): continue
                            z.extract(n, d)
                            rec.append(dict(path=os.path.relpath(os.path.join(d, n), dest), url=url + f'#{n}'))
                    rec.append(dict(path=None, url=url, sha256_zip=sha(out), bytes_zip=os.path.getsize(out))); os.unlink(out)
                else:
                    rec.append(dict(path=os.path.relpath(out, dest), url=url))
        except Blocked as e:
            blocked.append(dict(muc=it['id'], url=p['trang'], loi=str(e))); keep.pop(it['id'], None); continue
        zipinfo = [r for r in rec if r['path'] is None]
        files = []
        for r in rec:
            if r['path'] is None: continue
            fp = os.path.join(dest, r['path']); b = os.path.getsize(fp)
            files.append(dict(path=r['path'], url=r['url'], sha256=sha(fp), bytes=b, lfs=b > LFS_MIN))
        keep[it['id']] = dict(id=it['id'], chu_de=it['chu_de'], ghi=it['ghi'], nguon={'polyhaven': 'Poly Haven', 'quaternius': 'Quaternius',
                              'ambientcg': 'ambientCG'}[it['src']], trang=p['trang'], tac_gia=p['tac_gia'], ten=p['ten'], giay_phep=CC0,
                              tep_giay_phep=p['tep_giay_phep'], ngay_tai=today, files=files,
                              **({'zip': dict(url=zipinfo[0]['url'], sha256=zipinfo[0]['sha256_zip'], bytes=zipinfo[0]['bytes_zip'])} if zipinfo else {}))
        print(f"tải {it['id']}: {len(files)} tệp, {sum(f['bytes'] for f in files) / 1e6:.2f} MB")
    order = [i['id'] for i in CATALOG]
    cat = dict(ngay=today, cong_cu='scripts/common/cc0_fetch.py', giay_phep=CC0, items=sorted(keep.values(), key=lambda i: order.index(i['id']) if i['id'] in order else 999))
    cat['tong_bytes'] = sum(f['bytes'] for i in cat['items'] for f in i['files']); cat['chan'] = blocked
    if cat['tong_bytes'] > MAX_TOTAL: raise SystemExit(f'DỪNG: tổng {cat["tong_bytes"] / 1e6:.1f} MB > 300 MB')
    json.dump(cat, open(os.path.join(dest, 'catalog.json'), 'w'), ensure_ascii=False, indent=1)
    gitattributes(dest, cat); catalog_md(dest, cat)
    bp = os.path.join(dest, 'BLOCKED-URLS.md')
    if blocked:
        open(bp, 'w').write('# URL không tải được qua proxy — chủ dự án tải tay (KHÔNG vòng qua proxy)\n\n| Mục | URL | Lỗi |\n|---|---|---|\n' +
                            ''.join(f"| {b['muc']} | {b['url']} | {b['loi'].replace('|', '/')} |\n" for b in blocked))
    elif os.path.exists(bp): os.unlink(bp)
    print(f"catalog: {len(cat['items'])} mục, {cat['tong_bytes'] / 1e6:.1f} MB, {len(blocked)} URL chặn")
    return cat


def verify(dest):
    cat = json.load(open(os.path.join(dest, 'catalog.json'))); bad = []
    for it in cat['items']:
        if not os.path.exists(os.path.join(dest, it['tep_giay_phep'])): bad.append(f"{it['id']}: thiếu {it['tep_giay_phep']}")
        for f in it['files']:
            fp = os.path.join(dest, f['path'])
            if not os.path.exists(fp): bad.append(f'thiếu {f["path"]}'); continue
            with open(fp, 'rb') as h: head = h.read(64)
            if head.startswith(b'version https://git-lfs'): bad.append(f'{f["path"]}: còn là con trỏ LFS (chạy git lfs pull)'); continue
            if os.path.getsize(fp) != f['bytes'] or sha(fp) != f['sha256']: bad.append(f'lệch SHA/kích thước: {f["path"]}')
    tot = sum(f['bytes'] for i in cat['items'] for f in i['files'])
    if tot > MAX_TOTAL: bad.append(f'tổng {tot / 1e6:.1f} MB > 300 MB')
    print('\n'.join(bad) or f'verify: {len(cat["items"])} mục, {sum(len(i["files"]) for i in cat["items"])} tệp KHỚP, {tot / 1e6:.1f} MB')
    return not bad


def main():
    a = sys.argv[1:]
    dest = os.path.abspath(a[a.index('--dest') + 1]) if '--dest' in a else DEST
    if not a or a[0] not in ('fetch', 'verify', 'list'): print(__doc__); sys.exit(2)
    if a[0] == 'list':
        for it in CATALOG: print(f"{it['id']:28s} {it['src']:10s} {it['chu_de']:10s} {it['ghi']}")
        sys.exit(0)
    if a[0] == 'verify': sys.exit(0 if verify(dest) else 1)
    only = set(a[a.index('--only') + 1].split(',')) if '--only' in a else None
    cat = fetch(dest, only); sys.exit(1 if cat['chan'] else 0)


if __name__ == '__main__':
    main()
