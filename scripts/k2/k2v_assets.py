#!/opt/cine/bin/python
"""KÊNH 2 · tài sản cho module hình k2v (bản đồ, ảnh, văn bản): tải về cache ngoài git, kiểm SHA-256, tạo bản dùng cho cảnh 3D.
Media bên thứ ba KHÔNG commit (QUAN-TRI-RUI-RO §6); dữ liệu bản đồ npm (Natural Earth/Census, tài sản công) nằm ở design/k2v/data.
Mỗi tài sản có một dòng trong ASSETS (nguồn, giấy phép, ghi công, SHA gốc). SHA ghim lần tải đầu (12/10/2026); lệch SHA → dừng.

  k2v_assets.py fetch <id|all>                     tải + kiểm SHA (in đường dẫn cache)
  k2v_assets.py bm-global [--w 8192]               Blue Marble → texture toàn cầu (equirect)
  k2v_assets.py bm-crop --bbox lon0,lat0,lon1,lat1 [--w 4096] [--res 2km|500m]   vùng chi tiết cho cảnh bay xuống (500m: ô gốc)
  k2v_assets.py photo <id> [--h 2400]              ảnh tư liệu → JPG cho cảnh photo (giữ tông gốc, chỉ đổi khổ)
  k2v_assets.py doc <id> --page N --find "cụm 1" --find "cụm 2" [--dpi 220]   trang PDF → PNG + khung highlight (toạ độ chuẩn hoá)
  k2v_assets.py rights                             in bảng giấy phép (markdown) để chép vào RIGHTS.md / SOURCES-FOOTAGE.csv
Cache: $K2V_CACHE (mặc định /var/tmp/cine-out/k2v-cache). Ra: <cache>/<tên>.{jpg,png,json}.
"""
import hashlib, json, os, re, subprocess, sys, urllib.request

CACHE = os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache')
UA = 'Mozilla/5.0 (cine-lab research; https://github.com/HungQuach301/cine-lab)'
BMU = 'https://assets.science.nasa.gov/content/dam/science/esd/eo/images/bmng/bmng-topography-bathymetry/july/world.topo.bathy.200407.3x'
BMI = dict(source='NASA Earth Observatory (Reto Stöckli), https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/base-topography-bathymetry/',
           license='NASA media: "generally are not subject to copyright in the United States"; không hàm ý NASA bảo trợ; không dùng logo NASA (nasa.gov/nasa-brand-center/images-and-media, đọc 12/10/2026). Trang BMNG: "please credit NASA Earth Observatory"',
           credit='NASA Earth Observatory (Blue Marble: Next Generation)', kind='raster bản đồ', commit=False)
ASSETS = {
    'bm-200407': dict(
        url=BMU + '21600x10800.jpg', file='bm/world.topo.bathy.200407.3x21600x10800.jpg', sha256='',
        title='Blue Marble: Next Generation, topography + bathymetry, July 2004 (21600×10800, 2 km/px)', **BMI),
    'bm-200407-B1': dict(
        url=BMU + '21600x21600.B1.jpg', file='bm/world.topo.bathy.200407.3x21600x21600.B1.jpg', sha256='', tile=[-90, 0, 0, 90],
        title='Blue Marble: Next Generation, July 2004, ô B1 (90°W–0°, 0–90°N; 500 m/px)', **BMI),
    'bm-200407-C1': dict(
        url=BMU + '21600x21600.C1.jpg', file='bm/world.topo.bathy.200407.3x21600x21600.C1.jpg', sha256='', tile=[0, 0, 90, 90],
        title='Blue Marble: Next Generation, July 2004, ô C1 (0–90°E, 0–90°N; 500 m/px)', **BMI),
    'loc-carnegie-1913': dict(
        url='https://tile.loc.gov/storage-services/master/pnp/cph/3c00000/3c01000/3c01700/3c01767u.tif',
        file='photo/loc-cph-3c01767u.tif', sha256='',
        title='Andrew Carnegie, three-quarter length portrait, seated, facing slightly left (Theodore C. Marceau, ©1913)',
        source='Library of Congress Prints & Photographs, digital ID cph.3c01767, https://hdl.loc.gov/loc.pnp/cph.3c01767',
        license='Tài sản công tại Mỹ (xuất bản 1913, trước 1931); Commons ghi "free of known restrictions under copyright law" (trang LoC chặn máy 403, đối chiếu qua Commons 12/10/2026)',
        credit='Library of Congress, Prints & Photographs Division (Theodore C. Marceau, 1913)', kind='ảnh tư liệu', commit=False),
    'fr-2026-11314': dict(
        url='https://www.govinfo.gov/content/pkg/FR-2026-06-04/pdf/2026-11314.pdf',
        file='doc/FR-2026-06-04-2026-11314.pdf', sha256='',
        title='Proclamation 11032 of June 1, 2026, Federal Register Vol. 91, No. 107 (4 Jun 2026), FR Doc. 2026-11314',
        source='GovInfo (U.S. Government Publishing Office), https://www.govinfo.gov/content/pkg/FR-2026-06-04/pdf/2026-11314.pdf',
        license='Tác phẩm của Chính phủ Hoa Kỳ, không có bản quyền (17 U.S.C. §105)',
        credit='Federal Register / GovInfo', kind='văn bản', commit=False),
    # K2C-T1-06 (phiên P, G1b 13/10/2026): chân dung Hoover, ảnh Detroit Publishing đã kiểm Rights Advisory, trang U.S. Reports của Euclid
    'loc-hoover-1928': dict(
        url='https://tile.loc.gov/storage-services/master/pnp/hec/34800/34871u.tif',
        file='photo/loc-hec-34871u.tif', sha256='',
        title='Secretary of Commerce Herbert Hoover, Washington, 1928 (Harris & Ewing)',
        source='Library of Congress Prints & Photographs, Harris & Ewing collection, LCCN 2016888786 (qua Wikimedia Commons, kiểm từng tệp 12/10/2026)',
        license='Tài sản công (Harris & Ewing, LoC: "No known restrictions on publication"; Commons: Public domain) — RIGHTS.md bảng tư liệu WM-HOOVER-1928',
        credit='Harris & Ewing, Library of Congress', kind='ảnh tư liệu', commit=False),
    'loc-det-07': dict(
        url='https://tile.loc.gov/storage-services/service/pnp/det/4a10000/4a17000/4a17800/4a17898v.jpg',
        file='photo/loc-det-4a17898v.jpg', sha256='',
        title='Woodward Avenue, Detroit, between 1900 and 1910 (Detroit Publishing Co.)',
        source='Library of Congress, Detroit Publishing Co. collection, https://www.loc.gov/pictures/collection/det/item/2016809637/',
        license='Rights Advisory (JSON loc.gov 13/10/2026): "No known restrictions on publication." — RIGHTS.md bảng tư liệu LOC-DET-07',
        credit='Detroit Publishing Co., Library of Congress', kind='ảnh tư liệu', commit=False),
    'usrep-272-365': dict(
        url='https://tile.loc.gov/storage-services/service/ll/usrep/usrep272/usrep272365/usrep272365.pdf',
        file='doc/usrep272365.pdf', sha256='',
        title='Village of Euclid v. Ambler Realty Co., 272 U.S. 365 (1926), U.S. Reports',
        source='Library of Congress, U.S. Reports collection, https://www.loc.gov/item/usrep272365/',
        license='Phán quyết Toà án Tối cao, tác phẩm Chính phủ Hoa Kỳ (17 U.S.C. §105)',
        credit='U.S. Reports, Library of Congress', kind='văn bản', commit=False),
}
PIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'k2v-assets.sha.json')   # SHA ghim (commit), tài sản ở cache


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def pins():
    return json.load(open(PIN)) if os.path.exists(PIN) else {}


def fetch(k):
    a = ASSETS[k]; p = os.path.join(CACHE, a['file']); os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p):
        req = urllib.request.Request(a['url'], headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=300) as r, open(p + '.part', 'wb') as f:
            while True:
                b = r.read(1 << 20)
                if not b: break
                f.write(b)
        os.replace(p + '.part', p)
    s, P = sha(p), pins()
    if k in P and P[k]['sha256'] != s: raise SystemExit(f'LỖI SHA {k}: {s} ≠ ghim {P[k]["sha256"]} — nguồn đã đổi, kiểm lại giấy phép và nội dung trước khi dùng')
    if k not in P: P[k] = dict(sha256=s, bytes=os.path.getsize(p), url=a['url']); json.dump(P, open(PIN, 'w'), indent=1, ensure_ascii=False); print(f'ghim SHA {k} {s[:16]}…')
    return p


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def bm_open(k='bm-200407'):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    return Image.open(fetch(k))


def bm_global(w=8192):
    out = os.path.join(CACHE, f'bm-global-{w}.jpg')
    if not os.path.exists(out):
        im = bm_open().convert('RGB'); im.resize((w, w // 2), resample=3).save(out, quality=92)
    print(out); return out


def bm_crop(bbox, w=4096, res='2km'):
    """res '2km' = ảnh toàn cầu 21600×10800; '500m' = ô 21600×21600 chứa trọn bbox (A1…D2; hiện ghim B1, C1)."""
    lon0, lat0, lon1, lat1 = bbox
    out = os.path.join(CACHE, 'bm-crop-' + '_'.join(f'{v:g}' for v in bbox) + f'-{w}' + ('' if res == '2km' else '-' + res) + '.jpg')
    if not os.path.exists(out):
        G = [-180, -90, 180, 90]; k = 'bm-200407'
        if res == '500m':
            k = next((k2 for k2, a in ASSETS.items() if a.get('tile') and a['tile'][0] <= lon0 and lon1 <= a['tile'][2] and a['tile'][1] <= lat0 and lat1 <= a['tile'][3]), None)
            if not k: raise SystemExit('bbox không nằm trọn trong ô 500 m đã ghim (B1, C1) — thêm ô vào ASSETS')
            G = ASSETS[k]['tile']
        im = bm_open(k).convert('RGB'); W, H = im.size
        x0, x1 = (lon0 - G[0]) / (G[2] - G[0]) * W, (lon1 - G[0]) / (G[2] - G[0]) * W; y0, y1 = (G[3] - lat1) / (G[3] - G[1]) * H, (G[3] - lat0) / (G[3] - G[1]) * H
        c = im.crop((round(x0), round(y0), round(x1), round(y1))); h = round(w * c.size[1] / c.size[0])
        c.resize((w, h), resample=3).save(out, quality=92)
    print(out); return out


def photo(k, h=2400):
    from PIL import Image
    src = fetch(k); out = os.path.join(CACHE, f'{k}.jpg')
    if not os.path.exists(out):
        im = Image.open(src); im = im.convert('L') if im.mode in ('L', 'I;16', 'I') else im.convert('RGB')
        if im.size[1] > h: im = im.resize((round(im.size[0] * h / im.size[1]), h), resample=3)
        im.save(out, quality=94)
    print(out); return out


def doc(k, page, finds, dpi=220):
    """Trang PDF → PNG; mỗi cụm cần highlight → các khung dòng (chuẩn hoá 0..1 theo trang). Cụm khớp theo chuỗi từ liên tiếp trong -bbox-layout."""
    src = fetch(k); base = os.path.join(CACHE, f'{k}-p{page}')
    if not os.path.exists(base + '.png'):
        subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', str(dpi), '-png', '-singlefile', src, base], check=True)
    x = subprocess.run(['pdftotext', '-f', str(page), '-l', str(page), '-bbox-layout', src, '-'], capture_output=True, text=True, check=True).stdout
    pw, ph = map(float, re.search(r'<page width="([\d.]+)" height="([\d.]+)"', x).groups())
    words = []   # (từ, xMin, yMin, xMax, yMax, chỉ số dòng)
    for li, line in enumerate(re.findall(r'<line [^>]*>(.*?)</line>', x, re.S)):
        for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', line):
            words.append((m.group(5), *map(float, m.group(1, 2, 3, 4)), li))
    norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
    hl = []
    for f in finds:
        toks = [norm(t) for t in f.split() if norm(t)]
        for i in range(len(words)):
            j, k2 = i, 0; got = []
            while k2 < len(toks) and j < len(words):
                w = norm(words[j][0])
                if not w: j += 1; continue
                if toks[k2].startswith(w) and w != toks[k2] and j + 1 < len(words) and toks[k2] == w + norm(words[j + 1][0]):   # từ bị ngắt gạch nối cuối dòng (Alu-/minum)
                    got += [words[j], words[j + 1]]; j += 2; k2 += 1; continue
                if w != toks[k2]: break
                got.append(words[j]); j += 1; k2 += 1
            if k2 == len(toks):
                rows = {}
                for w in got: rows.setdefault(w[5], []).append(w)
                hl.append(dict(find=f, rects=[[round(min(w[1] for w in r) / pw, 4), round(min(w[2] for w in r) / ph, 4), round(max(w[3] for w in r) / pw, 4), round(max(w[4] for w in r) / ph, 4)] for r in rows.values()]))
                break
        else:
            raise SystemExit(f'không tìm thấy cụm "{f}" trên trang {page}')
    meta = dict(img=base + '.png', page=page, aspect=round(pw / ph, 5), hl=hl, sha256_pdf=sha(src))
    json.dump(meta, open(base + '.json', 'w'), indent=1, ensure_ascii=False); print(base + '.json'); return meta


def rights():
    P = pins()
    print('| id | tài sản | nguồn | giấy phép | ghi công | SHA-256 (gốc) | commit |\n|---|---|---|---|---|---|---|')
    for k, a in ASSETS.items():
        print(f"| {k} | {a['title']} | {a['source']} | {a['license']} | {a['credit']} | `{P.get(k, {}).get('sha256', 'chưa tải')}` | {'có' if a['commit'] else 'không (cache ngoài git)'} |")


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'fetch': [print(fetch(k)) for k in (ASSETS if sys.argv[2] == 'all' else [sys.argv[2]])]
    elif c == 'bm-global': bm_global(int(arg('w', 8192)))
    elif c == 'bm-crop': bm_crop([float(v) for v in arg('bbox').split(',')], int(arg('w', 4096)), arg('res', '2km'))
    elif c == 'photo': photo(sys.argv[2], int(arg('h', 2400)))
    elif c == 'doc': doc(sys.argv[2], int(arg('page', 1)), [sys.argv[i + 1] for i, v in enumerate(sys.argv) if v == '--find'], int(arg('dpi', 220)))
    elif c == 'rights': rights()
    else: print(__doc__)
