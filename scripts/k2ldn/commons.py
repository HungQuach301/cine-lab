#!/opt/cine/bin/python
"""Tra Wikimedia Commons (tệp ns 6): commons.py search "<từ khoá>" | info "File:..." (giấy phép, cỡ, URL gốc)."""
import json, sys, time, urllib.parse, urllib.request
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
API = 'https://commons.wikimedia.org/w/api.php'
def q(**p):
    p['format'] = 'json'
    url = API + '?' + urllib.parse.urlencode(p)
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(6 * (i + 1)); err = e
    raise err
def search(s, n=15):
    return [(r['title'], r['size']) for r in q(action='query', list='search', srnamespace=6, srlimit=n, srsearch=s)['query']['search']]
def info(t):
    d = q(action='query', titles=t, prop='imageinfo', iiprop='url|size|sha1|extmetadata|mime')
    pg = next(iter(d['query']['pages'].values()))
    ii = pg['imageinfo'][0]; m = ii.get('extmetadata', {})
    g = lambda k: (m.get(k) or {}).get('value')
    return {'title': t, 'url': ii['url'], 'descriptionurl': ii['descriptionurl'], 'w': ii['width'], 'h': ii['height'], 'sha1': ii['sha1'], 'mime': ii['mime'],
            'license': g('LicenseShortName'), 'usage': g('UsageTerms'), 'artist': g('Artist'), 'date': g('DateTimeOriginal'), 'credit': g('Credit'), 'desc': (g('ImageDescription') or '')[:400]}
if __name__ == '__main__':
    if sys.argv[1] == 'search':
        for t, s in search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 15): print(t)
    else:
        print(json.dumps(info(sys.argv[2]), ensure_ascii=False, indent=1))
