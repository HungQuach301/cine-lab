#!/opt/cine/bin/python
"""NV-2 · (1) đếm video kênh đã đăng TRƯỚC video bùng nổ và nhịp đăng; (2) mở rộng mẫu qua danh sách uploads của kênh mới
(không tốn search.list — hạn 100 search/ngày của dự án đã cạn). Bản sao sửa từ scripts/nc-viral/truoc.py.
  truoc.py <raw.json> <cand.json> <kenh.json> <raw_out.json> <truoc.json>
- Kênh xét: mọi kênh trong kenh.json (≤ 90 ngày tuổi lúc đo) ∪ kênh có video trong cand.json.
- playlistItems.list (1 đơn vị/trang) đọc trọn uploads → ngày đăng từng video; videos.list (1 đơn vị/50 id) cho các upload đăng
  ≤ 30 ngày trước đo chưa có trong raw → thêm vào raw với hits = ['uploads'].
- Trần cứng 9 000 đơn vị tính cả sổ; 403 quotaExceeded → dừng, ghi phần đã có.
"""
import datetime as dt, json, os, sys, urllib.parse, urllib.request, urllib.error
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'reports', 'nc-viral-2')
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
LED = os.path.join(OUT, 'so-quota.jsonl')
_L = [json.loads(l) for l in open(LED)]
used = sum(x['units'] for x in _L); upper = sum(x.get('units_neu_tinh_429', x['units']) for x in _L)
qlog = open(LED, 'a')
raw, cand, kenh = (json.load(open(p)) for p in sys.argv[1:4])
NOW = dt.datetime.fromisoformat(raw['measured_at'])
after = raw['published_after']


class Stop(Exception): pass


def get(ep, q, tag):
    global used, upper
    if used + 1 > 8990: raise Stop('chạm trần 9 000')
    url = 'https://www.googleapis.com/youtube/v3/' + ep + '?' + urllib.parse.urlencode({k: v for k, v in q.items() if v})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r: st, b = r.status, json.load(r)
    except urllib.error.HTTPError as e:
        st = e.code
        try: b = json.load(e)
        except Exception: b = {}
    reason = ((b.get('error') or {}).get('errors') or [{}])[0].get('reason') if st != 200 else None
    used += 1; upper += 1
    qlog.write(json.dumps({'t': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'endpoint': ep + '.list', 'tag': tag,
                           'units': 1, 'cum': used, 'http': st, 'reason': reason, 'n': len(b.get('items', [])), 'usd': 0.0,
                           'units_neu_tinh_429': 1, 'cum_tran_tren': upper}, ensure_ascii=False) + '\n'); qlog.flush()
    if st in (403, 429): raise Stop(reason or str(st))
    return b if st == 200 else {}


cids = list(dict.fromkeys([k['cid'] for k in kenh] + [c['cid'] for c in cand]))
uploads, stop = {}, None
try:
    for cid in cids:
        pl = raw['channels'][cid].get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads') or 'UU' + cid[2:]
        tok, items = None, []
        while True:
            b = get('playlistItems', dict(part='contentDetails', playlistId=pl, maxResults=50, pageToken=tok), cid)
            items += [(i['contentDetails']['videoId'], i['contentDetails'].get('videoPublishedAt')) for i in b.get('items', [])]
            tok = b.get('nextPageToken')
            if not tok: break
        uploads[cid] = items
    new = [v for its in uploads.values() for v, d in its if d and d >= after and v not in raw['videos']]
    for i in range(0, len(new), 50):
        b = get('videos', dict(part='snippet,statistics,contentDetails,status,topicDetails', id=','.join(new[i:i + 50]), maxResults=50), f'videos<uploads {i}>')
        for v in b.get('items', []):
            v['_fetched'] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'); raw['videos'][v['id']] = v
            raw['hits'].setdefault(v['id'], []).append('uploads')
except Stop as e:
    stop = str(e)
raw['uploads_stop'] = stop; raw['units_used'] = used; raw['units_upper'] = upper
json.dump(raw, open(sys.argv[4], 'w'), ensure_ascii=False, indent=1)
res = {cid: [[v, d] for v, d in its] for cid, its in uploads.items()}
json.dump({'stop': stop, 'uploads': res}, open(sys.argv[5], 'w'), indent=1)
print('đơn vị', used, 'kênh', len(uploads), '/', len(cids), 'video mới', sum(1 for v in raw['hits'].values() if v == ['uploads']), 'dừng', stop)
