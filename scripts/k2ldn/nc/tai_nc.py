"""NC-T4 · tải chân dung + ảnh 1850–1950 (nguồn có giấy phép rõ) + lưu bằng chứng.
Chạy: /opt/cine/bin/python -I tai_nc.py [id ...]"""
import datetime, hashlib, json, os, re, subprocess, sys, time, urllib.request, urllib.error
REPO = '/home/user/cine-lab'
GOC = '/var/tmp/nc-t4/goc'
ANH = REPO + '/channel-k2/k2c-t4-02/nc/anh'
LIC = REPO + '/channel-k2/k2c-t4-02/nc/licenses'
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
ACCESSED = '2026-10-25'
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')

def get(url, accept=None):
    h = {'User-Agent': UA}
    if accept: h['Accept'] = accept
    for k in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=600) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and k < 4:
                time.sleep(30 * (k + 1)); continue
            raise
        except Exception:
            if k < 4: time.sleep(10); continue
            raise
def jget(url, accept=None): return json.loads(get(url, accept))
def scrub(o):
    return json.loads(EMAIL.sub('[email-đã-che]', json.dumps(o, ensure_ascii=False)))

def met(oid):
    api = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}'
    d = jget(api)
    return dict(api_url=api, source_url=d['objectURL'], img=d['primaryImage'], meta=d,
                licence_quote=f'"isPublicDomain": {json.dumps(d["isPublicDomain"])}',
                licence='Met Open Access — CC0 1.0 (isPublicDomain=true)',
                title=d['title'], date=d['objectDate'], creator=f"{d['artistDisplayName']} ({d.get('artistBeginDate')}–{d.get('artistEndDate')})",
                holder=f"The Metropolitan Museum of Art, {d['accessionNumber']}")

def rijks(oid):
    api = f'https://id.rijksmuseum.nl/{oid}'
    d = jget(api, 'application/ld+json')
    vis = d['shows'][0]['id']; v = jget(vis, 'application/ld+json')
    dig = [u for u in re.findall(r'https://id\.rijksmuseum\.nl/\d+', json.dumps(v)) if u != vis and len(u) > 30]
    dd = None; img = None
    for u in dig:
        try: x = jget(u, 'application/ld+json')
        except Exception: continue
        m = re.findall(r'https://iiif\.micr\.io/[^"/]+/full/max/0/default\.jpg', json.dumps(x))
        if m: dd, img = x, m[0]; break
    num = [x['content'] for x in d.get('identified_by', []) if x.get('type') == 'Identifier']
    names = [x['content'] for x in d.get('identified_by', []) if x.get('type') == 'Name']
    lic_obj = sorted(set(re.findall(r'https?://creativecommons\.org/[^"]+', json.dumps(d))))
    lic_dig = sorted(set(re.findall(r'https?://creativecommons\.org/[^"]+', json.dumps(dd)))) if dd else []
    pb = d.get('produced_by', {}); tsp = pb.get('timespan', {}); tsp = tsp[0] if isinstance(tsp, list) and tsp else tsp
    date = ((tsp or {}).get('identified_by') or [{}])[0].get('content')
    who = []
    for p in pb.get('part', []) or []:
        for c in p.get('carried_out_by', []) or []: who.append(c.get('id'))
    cre = []
    for w in who[:2]:
        try:
            c = jget(w, 'application/ld+json')
            nm = [x['content'] for x in c.get('identified_by', []) if x.get('type') == 'Name'][:1]
            dob = (((c.get('born') or {}).get('timespan') or {}).get('identified_by') or [{}])[0].get('content') if isinstance(c.get('born'), dict) else None
            dod = (((c.get('died') or {}).get('timespan') or {}).get('identified_by') or [{}])[0].get('content') if isinstance(c.get('died'), dict) else None
            cre.append(f"{nm[0] if nm else w} ({dob}–{dod})")
        except Exception: cre.append(w)
    objnum = [n for n in num if n.startswith(('RP-', 'SK-'))] or num
    return dict(api_url=api, source_url=f'https://www.rijksmuseum.nl/en/collection/{objnum[0]}', img=img,
                meta={'object': d, 'visual_item': v, 'digital_object': dd},
                licence_quote='object: ' + ', '.join(lic_obj) + (' | digital object: ' + ', '.join(lic_dig) if lic_dig else ''),
                licence='Rijksmuseum linked-art: ' + ', '.join(lic_dig or lic_obj),
                title=' / '.join(names[:2]), date=date, creator='; '.join(cre) or 'anoniem/không ghi',
                holder='Rijksmuseum, ' + ', '.join(objnum))

def wellcome(work, iiif_id):
    api = f'https://api.wellcomecollection.org/catalogue/v2/works/{work}?include=notes,contributors,production,items,images,subjects'
    d = jget(api)
    lic = []
    for it in d.get('items', []):
        for l in it.get('locations', []):
            if l.get('license'): lic.append(l['license'])
    imgrec = None
    for im in d.get('images', []):
        x = jget(f"https://api.wellcomecollection.org/catalogue/v2/images/{im['id']}")
        if any(iiif_id in (l.get('url') or '') for l in x.get('locations', [])): imgrec = x
    if imgrec:
        for l in imgrec['locations']:
            if l.get('license'): lic = [l['license']] + lic
    info = f'https://iiif.wellcomecollection.org/image/{iiif_id}/info.json'
    i = jget(info)
    return dict(api_url=api, source_url=f'https://wellcomecollection.org/works/{work}',
                img=f'https://iiif.wellcomecollection.org/image/{iiif_id}/full/max/0/default.jpg',
                meta={'work': d, 'image': imgrec, 'iiif_info': i},
                licence_quote=json.dumps(lic[0], ensure_ascii=False) if lic else '',
                licence=(lic[0]['label'] if lic else '?') + ' (Wellcome Collection)',
                title=d['title'], date='; '.join(p.get('label', '') for p in d.get('production', [])) or None,
                creator='; '.join(c['agent']['label'] for c in d.get('contributors', [])) or None,
                holder=f'Wellcome Collection, {work} / {iiif_id}')

def loc(lccn, maxbytes=70_000_000):
    api = f'https://www.loc.gov/item/{lccn}/?fo=json'
    d = jget(api); it = d['item']
    files = d['resources'][0]['files'][0]
    tif = [f for f in files if f.get('mimetype') == 'image/tiff']
    img = None
    if tif and 2_000_000 <= (tif[0].get('size') or 0) <= maxbytes: img = tif[0]['url']
    elif tif and (tif[0].get('size') or 0) < 2_000_000: img = [f['url'] for f in files if f.get('mimetype') == 'image/jpeg'][-1]
    else:
        m = re.search(r'/service/pnp/([^/]+)/(.+)/([0-9a-z]+)v\.jpg', json.dumps(files))
        jp = [f['url'] for f in files if f.get('mimetype') == 'image/jpeg']
        base = jp[-1]
        mm = re.search(r'service/pnp/(.+)/([0-9a-z]+?)v\.jpg$', base)
        path = mm.group(1).replace('/', ':')
        img = f'https://tile.loc.gov/image-services/iiif/service:pnp:{path}:{mm.group(2)}u/full/pct:50/0/default.jpg'
    r = it.get('rights_information') or it.get('rights')
    rq = r if isinstance(r, str) else ' '.join(r) if isinstance(r, list) else str(r)
    rq = re.sub(r'<[^>]+>', ' ', rq); rq = re.sub(r'\s+', ' ', rq).strip()
    return dict(api_url=api, source_url=f'https://www.loc.gov/item/{lccn}/', img=img, meta=d,
                licence_quote=rq, licence='LoC rights_information', title=it.get('title'),
                date='; '.join(it.get('created_published') or []), creator='; '.join(it.get('contributor_names') or []) or None,
                holder=f'Library of Congress P&P, {lccn}')

ITEMS = {
 # A — chân dung
 'met-435943-charles2-cooper': (met, (435943,), 'A', 'Charles II'),
 'rijks-200221267-james2-loggan': (rijks, (200221267,), 'A', 'James, Duke of York / James II'),
 'wellcome-puwvaf8q-pepys': (wellcome, ('puwvaf8q', 'V0004604'), 'A', 'Samuel Pepys'),
 'wellcome-b6zd76cd-evelyn-nanteuil': (wellcome, ('b6zd76cd', 'V0001805'), 'A', 'John Evelyn'),
 'rijks-200348829-bazalgette': (rijks, (200348829,), 'A', 'Joseph Bazalgette'),
 'loc-2017696565-churchill-1943': (loc, ('2017696565',), 'A', 'Winston Churchill'),
 # B — ảnh 1850–1950
 'loc-2002696930-londonbridge-pc': (loc, ('2002696930',), 'B', 'London Bridge (1831)'),
 'loc-2002696941-embankment-pc': (loc, ('2002696941',), 'B', 'Victoria Embankment'),
 'loc-2002696932-stpauls-pc': (loc, ('2002696932',), 'B', "St Paul's west front"),
 'loc-2002696937-cheapside-pc': (loc, ('2002696937',), 'B', 'Cheapside'),
 'loc-2004678933-stpauls-blackfriars-gww': (loc, ('2004678933', 200_000_000), 'B', "St Paul's & Blackfriars Bridge"),
 'rijks-200323435-theems-stpauls-1892': (rijks, (200323435,), 'B', "Thames + St Paul's"),
 'rijks-200324876-theems-stpauls': (rijks, (200324876,), 'B', "Thames + St Paul's"),
 'rijks-200355251-londonbridge-1900': (rijks, (200355251,), 'B', 'London Bridge'),
 'rijks-200324875-embankment-waterloo': (rijks, (200324875,), 'B', 'Victoria Embankment'),
 'rijks-200337941-ludgate-1892': (rijks, (200337941,), 'B', 'Ludgate Hill'),
 'rijks-200632748-fleetstreet-1895': (rijks, (200632748,), 'B', 'Fleet Street'),
 'rijks-200561138-cheapside-stuart': (rijks, (200561138,), 'B', 'Cheapside'),
 'rijks-200794890-mansionhouse-cheapside': (rijks, (200794890,), 'B', 'Mansion House & Cheapside'),
 'met-288279-stpauls-ryder': (met, (288279,), 'B', "St Paul's"),
 'wellcome-uv3mugch-embankment-1865': (wellcome, ('uv3mugch', 'V0024386'), 'B', 'Embankment construction drawing 1865'),
}

def thu(src, dst):
    subprocess.run(['/opt/cine/bin/python', '-I', '-c', '''
import sys, os
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
im=Image.open(sys.argv[1]); im.seek(0); print("ORIG", im.size[0], im.size[1], flush=True)
im=im.convert("RGB"); im.thumbnail((2400,2400), Image.LANCZOS)
q=88
while True:
    im.save(sys.argv[2],"JPEG",quality=q,optimize=True)
    if os.path.getsize(sys.argv[2])<=5_000_000 or q<60: break
    q-=6
print("OUT", im.size[0], im.size[1], q)
''', src, dst], check=True, capture_output=True, text=True)

def dims(src):
    r = subprocess.run(['/opt/cine/bin/python', '-I', '-c', 'import sys\nfrom PIL import Image\nImage.MAX_IMAGE_PIXELS=None\nim=Image.open(sys.argv[1]);print(im.size[0],im.size[1])', src], capture_output=True, text=True, check=True)
    return [int(x) for x in r.stdout.split()]

def main(ids):
    os.makedirs(GOC, exist_ok=True)
    for k in ids or ITEMS:
        fn, args, grp, subj = ITEMS[k]
        if fn is wellcome and args[1] is None:
            w = jget(f'https://api.wellcomecollection.org/catalogue/v2/works/{args[0]}?include=items')
            u = [l['url'] for it in w['items'] for l in it['locations'] if 'iiif.wellcomecollection.org/image' in (l.get('url') or '')]
            args = (args[0], u[0].split('/image/')[1].split('/')[0])
        try: r = fn(*args)
        except Exception as e: print('LỖI', k, repr(e)); continue
        d = os.path.join(GOC, k); os.makedirs(d, exist_ok=True)
        ext = '.tif' if r['img'].lower().endswith(('.tif', '.tiff')) else '.jpg'
        p = os.path.join(d, 'goc' + ext)
        if not os.path.exists(p):
            try: b = get(r['img'])
            except Exception as e: print('LỖI tải', k, r['img'], repr(e)); continue
            open(p, 'wb').write(b); time.sleep(3)
        sha = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        w0, h0 = dims(p)
        out = os.path.join(ANH, k + '.jpg'); thu(p, out)
        w1, h1 = dims(out)
        rec = {'id': k, 'nhom': grp, 'chu_de': subj, 'source_url': r['source_url'], 'api_url': r['api_url'],
               'accessed': ACCESSED, 'holder': r['holder'], 'title': r['title'], 'date': r['date'], 'creator': r['creator'],
               'licence': r['licence'], 'licence_quote_verbatim': r['licence_quote'],
               'original': {'url': r['img'], 'file': p, 'bytes': os.path.getsize(p), 'sha256': sha, 'px': [w0, h0]},
               'derivative': {'file': os.path.relpath(out, REPO), 'bytes': os.path.getsize(out), 'px': [w1, h1]},
               'raw_metadata_verbatim': r['meta']}
        json.dump(scrub(rec), open(os.path.join(LIC, k + '.json'), 'w'), ensure_ascii=False, indent=1)
        print('OK', k, r['licence'][:60], '|', r['licence_quote'][:80], '|', os.path.getsize(p), w0, h0, '->', w1, h1)
    with open(os.path.join(LIC, 'SHA256-NC.txt'), 'w') as f:
        for fj in sorted(os.listdir(LIC)):
            if fj.endswith('.json'):
                j = json.load(open(os.path.join(LIC, fj)))
                if 'original' in j: f.write(f"{j['original']['sha256']}  {j['id']}{os.path.splitext(j['original']['file'])[1]}  ({j['original']['url']})\n")

if __name__ == '__main__': main(sys.argv[1:])
