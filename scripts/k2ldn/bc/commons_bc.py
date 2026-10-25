#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · Wikimedia Commons có nhịp: ≤ 1 yêu cầu / 5 s (khoá tệp /var/tmp/bc/commons.last), 429 → chờ (Retry-After hoặc 60 s × lần), UA chuẩn.
  commons_bc.py search "<từ khoá>" [n]           → tên tệp
  commons_bc.py info "File:..."                   → JSON giấy phép/cỡ/URL
  commons_bc.py page "File:..." <ra.txt>          → wikitext trang mô tả (bằng chứng giấy phép)
  commons_bc.py get <url> <ra>                    → tải tệp gốc, in SHA-256"""
import hashlib, json, os, sys, time, urllib.error, urllib.parse, urllib.request
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
API = 'https://commons.wikimedia.org/w/api.php'; LAST = '/var/tmp/bc/commons.last'


def nhip():
    os.makedirs(os.path.dirname(LAST), exist_ok=True)
    try: t = float(open(LAST).read())
    except Exception: t = 0
    w = 5.0 - (time.time() - t)
    if w > 0: time.sleep(w)
    open(LAST, 'w').write(str(time.time()))


def mo(url, n=8):
    for i in range(n):
        nhip()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=120) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                ra = e.headers.get('Retry-After'); w = int(ra) if ra and ra.isdigit() else 60 * (i + 1)
                print(f'[commons] {e.code} → chờ {w} s', file=sys.stderr); time.sleep(min(w, 600)); continue
            raise
    raise RuntimeError('hết lượt thử: ' + url)


def q(**p):
    p['format'] = 'json'; return json.loads(mo(API + '?' + urllib.parse.urlencode(p)))


def info(t):
    d = q(action='query', titles=t, prop='imageinfo', iiprop='url|size|sha1|extmetadata|mime')
    pg = next(iter(d['query']['pages'].values())); ii = pg['imageinfo'][0]; m = ii.get('extmetadata', {})
    g = lambda k: (m.get(k) or {}).get('value')
    return {'title': t, 'url': ii['url'], 'descriptionurl': ii['descriptionurl'], 'w': ii['width'], 'h': ii['height'], 'sha1': ii['sha1'], 'mime': ii['mime'],
            'license': g('LicenseShortName'), 'usage': g('UsageTerms'), 'artist': g('Artist'), 'date': g('DateTimeOriginal'), 'credit': g('Credit'),
            'categories': g('Categories'), 'desc': (g('ImageDescription') or '')[:600]}


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'search':
        d = q(action='query', list='search', srnamespace=6, srlimit=int(sys.argv[3]) if len(sys.argv) > 3 else 20, srsearch=sys.argv[2])
        for r in d['query']['search']: print(r['title'])
    elif c == 'info': print(json.dumps(info(sys.argv[2]), ensure_ascii=False, indent=1))
    elif c == 'page':
        d = q(action='query', titles=sys.argv[2], prop='revisions', rvprop='content|timestamp', rvslots='main')
        pg = next(iter(d['query']['pages'].values())); rv = pg['revisions'][0]
        open(sys.argv[3], 'w').write(rv['slots']['main']['*']); print(rv['timestamp'])
    elif c == 'get':
        b = mo(sys.argv[2]); open(sys.argv[3], 'wb').write(b); print(hashlib.sha256(b).hexdigest(), len(b))
