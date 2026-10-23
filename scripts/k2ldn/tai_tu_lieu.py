#!/opt/cine/bin/python
"""TIEN-KY-T4 · tải tư liệu T4 London + lưu bằng chứng giấy phép.
  tai_tu_lieu.py [id ...]
Gốc tải: $LDN_SRC (mặc định /var/tmp/ldn/tu-lieu, NGOÀI git, tái tạo bằng lệnh này + SHA trong licenses/SHA256-TU-LIEU.txt).
Trong git: channel-k2/k2c-t4-02/licenses/<id>.json (siêu dữ liệu nguyên văn của nơi giữ + URL + ngày tải + SHA)
           channel-k2/k2c-t4-02/tu-lieu/<id>.jpg (bản thu ≤ 2400 px, ≤ 2 MB — đầu vào cho bản thử, tái tạo được)."""
import datetime, hashlib, json, os, re, subprocess, sys, time, urllib.request
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.environ.get('LDN_SRC', '/var/tmp/ldn/tu-lieu'); os.makedirs(SRC, exist_ok=True)
LIC = os.path.join(REPO, 'channel-k2/k2c-t4-02/licenses'); TL = os.path.join(REPO, 'channel-k2/k2c-t4-02/tu-lieu')
os.makedirs(LIC, exist_ok=True); os.makedirs(TL, exist_ok=True)
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
def get(url, accept=None, tries=4):
    h = {'User-Agent': UA}
    if accept: h['Accept'] = accept
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=300) as r: return r.read()
        except Exception as e:
            err = e; time.sleep(6 * (i + 1))
    raise err
def jget(url, accept=None): return json.loads(get(url, accept))

def met(oid):
    d = jget(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}')
    return {'img': [d['primaryImage']] + d.get('additionalImages', []), 'meta': d, 'page': d['objectURL'],
            'license': 'CC0 1.0 (Met Open Access, isPublicDomain=%s)' % d['isPublicDomain'], 'title': d['title'], 'date': d['objectDate'], 'artist': d['artistDisplayName']}
def ycba(obj):
    d = jget(f'https://manifests.collections.yale.edu/ycba/obj/{obj}')
    md = {m['label']['en'][0]: m['value']['en'][0] for m in d['metadata']}
    img = [c['items'][0]['items'][0]['body']['id'] for c in d['items']]
    return {'img': img[:1], 'meta': d, 'page': f'https://collections.britishart.yale.edu/catalog/tms:{obj}',
            'license': 'Copyright Statement: %s; rights %s' % (md.get('Copyright Statement'), d.get('rights')), 'title': md.get('Title'), 'date': d['label']['en'][0], 'artist': md.get('Creator')}
def rijks(num):
    s = jget(f'https://data.rijksmuseum.nl/search/collection?objectNumber={num}', 'application/ld+json')
    oid = s['orderedItems'][0]['id']; d = jget(oid, 'application/ld+json')
    vis = d['shows'][0]['id']; v = get(vis, 'application/ld+json').decode()
    dig = [u for u in re.findall(r'https://id\.rijksmuseum\.nl/\d+', v) if len(u) > 40][0]
    dd = get(dig, 'application/ld+json').decode()
    img = re.findall(r'https://iiif\.micr\.io/[^"/]+/full/max/0/default\.jpg', dd)
    lic = sorted(set(re.findall(r'https?://creativecommons\.org/[^"]+', json.dumps(d))))
    names = [n['content'] for n in d.get('identified_by', []) if n.get('type') == 'Name']
    return {'img': img[:1], 'meta': {'object': d, 'digital': json.loads(dd)}, 'page': f'https://www.rijksmuseum.nl/en/collection/{num}',
            'license': 'Rijksmuseum linked-art: ' + ', '.join(lic), 'title': names[0], 'date': (d.get('produced_by', {}).get('timespan', {}).get('identified_by') or [{}])[0].get('content'), 'artist': None}
def commons(title):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import commons as C
    i = C.info(title)
    return {'img': [i['url'].split('?')[0]], 'meta': i, 'page': i['descriptionurl'], 'license': 'Commons: %s (%s)' % (i['license'], i['usage']), 'title': title, 'date': i['date'], 'artist': i['artist']}
def nga(objid):
    import csv as _csv
    f = os.path.join(SRC, '../src/nga_img.csv')
    if not os.path.exists(f): open(f, 'wb').write(get('https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/published_images.csv'))
    row = [r for r in _csv.reader(open(f, encoding='utf-8', errors='replace')) if len(r) > 11 and r[11] == str(objid) and r[3] == 'primary'][0]
    return {'img': [row[1] + '/full/full/0/default.jpg'], 'meta': {'uuid': row[0], 'iiif': row[1], 'w': row[5], 'h': row[6], 'openaccess': row[8], 'csv': 'https://github.com/NationalGalleryOfArt/opendata data/published_images.csv'},
            'page': f'https://www.nga.gov/artworks/{objid}', 'license': 'NGA Open Access (openaccess=%s; NGA: CC0 for open access images)' % row[8], 'title': 'Sir Christopher Wren (John Smith after Kneller)', 'date': None, 'artist': 'John Smith after Sir Godfrey Kneller'}
def loc(lccn, tif):
    return {'img': [tif], 'meta': jget(f'https://www.loc.gov/pictures/item/{lccn}/?fo=json'), 'page': f'https://www.loc.gov/pictures/item/{lccn}/', 'license': 'LoC: see rights_information in meta', 'title': lccn, 'date': None, 'artist': None}

ITEMS = {
  'met-360649': (met, 360649, 'Hollar, Prospects of London Before and After the Great Fire (17.50.100–.101)', 'thấp'),
  'met-361738': (met, 361738, 'London before the Great Fire (56.581.8)', 'thấp'),
  'met-395057': (met, 395057, "Hollar, Old St Paul's seen from the East (2010.529)", 'thấp'),
  'ycba-266':   (ycba, 266, "The Great Fire of London, with Ludgate and Old St. Paul's (B1976.7.27)", 'thấp'),
  'ycba-40597': (ycba, 40597, 'General View of London during the Great Fire of 1666 (B1977.14.17854)', 'thấp'),
  'rijks-luyken': (rijks, 'RP-P-1896-A-19368-1507', 'Luyken, Grote brand van Londen, 1666', 'thấp'),
  'rijks-charles2': (rijks, 'RP-P-OB-32.684', 'Portret van Karel II', 'thấp'),
  'rijks-doornick': (rijks, 'RP-P-OB-82.345', 'Plattegrond van Londen na de grote brand van 1666 (Doornick)', 'thấp'),
  'rijks-monument': (rijks, 'RP-P-2018-836', "Gezicht op het Monument (na 1676)", 'thấp'),
  'commons-ogilby': (commons, 'File:Ogilby and Morgan Map of London 1677 BL Maps Crace Port 2 61.jpg', 'Ogilby & Morgan, A Large and Accurate Map of the City of London (BL Crace Port. 2.61)', 'vừa'),
  'loc-wren-plan': (loc, ('2004678686', 'https://cdn.loc.gov/master/pnp/cph/3b00000/3b02000/3b02800/3b02873u.tif'), 'A Plan for rebuilding the City of London … Wren (bản khắc 18th c.)', 'thấp'),
  'nga-wren':   (nga, 119667, 'John Smith after Kneller, Sir Christopher Wren (2001.118.55)', 'thấp'),
}
def thu(src, dst):
    subprocess.run(['/opt/cine/bin/python', '-I', '-c', '''
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
im=Image.open(sys.argv[1]); im.seek(0); im=im.convert("RGB"); im.thumbnail((2400,2400), Image.LANCZOS)
q=88
while True:
    im.save(sys.argv[2],"JPEG",quality=q,optimize=True)
    import os
    if os.path.getsize(sys.argv[2])<2_000_000 or q<60: break
    q-=6
''', src, dst], check=True)
def main(ids):
    today = datetime.date.today().isoformat()
    for k in ids or ITEMS:
        fn, arg, desc, risk = ITEMS[k]
        try: r = fn(*arg) if isinstance(arg, tuple) else fn(arg)
        except Exception as e: print('LỖI', k, e); continue
        out = []
        for j, u in enumerate(r['img'][:2]):
            ext = '.tif' if u.lower().endswith(('.tif', '.tiff')) else '.jpg'
            p = os.path.join(SRC, f'{k}-{j}{ext}')
            if not os.path.exists(p):
                b = get(u); open(p, 'wb').write(b); time.sleep(3)
            sha = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            prev = os.path.join(TL, f'{k}-{j}.jpg'); thu(p, prev)
            out.append({'url': u, 'tep': os.path.basename(p), 'bytes': os.path.getsize(p), 'sha256': sha, 'ban_thu_git': os.path.relpath(prev, REPO)})
        rec = {'id': k, 'mo_ta': desc, 'rui_ro': risk, 'trang': r['page'], 'giay_phep': r['license'], 'tieu_de': r['title'], 'nam': r['date'], 'tac_gia': r['artist'],
               'ngay_tai': today, 'anh': out, 'meta_nguyen_van': r['meta']}
        json.dump(rec, open(os.path.join(LIC, f'{k}.json'), 'w'), ensure_ascii=False, indent=1)
        print('OK', k, r['license'][:90], [o['bytes'] for o in out])
    with open(os.path.join(LIC, 'SHA256-TU-LIEU.txt'), 'w') as f:
        for fjs in sorted(os.listdir(LIC)):
            if fjs.endswith('.json'):
                for o in json.load(open(os.path.join(LIC, fjs))).get('anh', []): f.write(f"{o['sha256']}  {o['tep']}  {o['url']}\n")
if __name__ == '__main__': main(sys.argv[1:])
