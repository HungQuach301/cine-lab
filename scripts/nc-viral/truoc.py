#!/opt/cine/bin/python
"""NC-VIRAL · đếm số video kênh đã đăng TRƯỚC video bùng nổ (playlistItems.list trên danh sách uploads, 1 đơn vị/trang).
  truoc.py <cand.json>... <out.json>   — trần cứng 9 000 đơn vị tính cả sổ so-quota.jsonl."""
import datetime as dt, json, os, sys, urllib.parse, urllib.request, urllib.error
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'reports', 'nc-viral')
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
LED = os.path.join(OUT, 'so-quota.jsonl')
used = sum(json.loads(l)['units'] for l in open(LED))
qlog = open(LED, 'a')
res = {}
for f in sys.argv[1:-1]:
    for c in json.load(open(f)):
        pl, tok, dates = 'UU' + c['cid'][2:], None, []
        while True:
            if used + 1 > 8990: raise SystemExit('chạm trần')
            q = dict(part='contentDetails', playlistId=pl, maxResults=50, pageToken=tok)
            url = 'https://www.googleapis.com/youtube/v3/playlistItems?' + urllib.parse.urlencode({k: v for k, v in q.items() if v})
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r: st, b = r.status, json.load(r)
            except urllib.error.HTTPError as e: st, b = e.code, {}
            used += 1
            qlog.write(json.dumps({'t': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'endpoint': 'playlistItems.list', 'tag': c['id'],
                                   'units': 1, 'cum': used, 'http': st, 'reason': None, 'n': len(b.get('items', []))}) + '\n'); qlog.flush()
            dates += [i['contentDetails'].get('videoPublishedAt') for i in b.get('items', [])]
            tok = b.get('nextPageToken')
            if not tok or st != 200: break
        ds = [d for d in dates if d]
        res[c['id']] = dict(uploads_seen=len(ds), before=sum(1 for d in ds if d < c['pub']), ok=st == 200)
json.dump(res, open(sys.argv[-1], 'w'), indent=1)
print('đơn vị', used, res)
