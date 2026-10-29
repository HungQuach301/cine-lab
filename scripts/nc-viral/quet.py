#!/opt/cine/bin/python
"""NC-VIRAL · quét YouTube Data API v3 tìm video ≥ 1 triệu lượt/7 ngày của kênh ≤ 30 ngày tuổi (phiên NC-VIRAL 29/10/2026).

  quet.py <raw.json>          # lượt 1: quét, ghi số liệu thô (ngoài repo) + so-quota.jsonl
  quet.py <raw.json> --dai    # lượt 2: lượt 1 ra 0 video dài → quét bổ sung videoDuration=medium/long (lọc bỏ Shorts)
Khoá API do proxy gắn cho www.googleapis.com — script KHÔNG đọc/ghi khoá.
Trần quota mềm 8 800 đơn vị (hạn mức giao 9 000); 403 quotaExceeded → dừng, ghi phần đã có.
"""
import datetime as dt, json, os, sys, time, urllib.parse, urllib.request, urllib.error

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'reports', 'nc-viral')
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
BASE = 'https://www.googleapis.com/youtube/v3/'
CAP = 8950 if '--dai' in sys.argv else 8800
REGIONS = ['US', 'GB', 'IN', 'BR', 'ID', 'MX', 'PH', 'VN', 'DE', 'JP', 'KR', 'FR']
CATS = [None, '22', '24', '20', '23']          # tất cả · People&Blogs · Entertainment · Gaming · Comedy
LANGS = ['es', 'pt', 'hi', 'id', 'ar', 'ru']   # truy vấn rỗng theo relevanceLanguage, không regionCode
COST = {'search': 100, 'videos': 1, 'channels': 1}
used = sum(json.loads(l)['units'] for l in open(os.path.join(OUT, 'so-quota.jsonl'))) if os.path.exists(os.path.join(OUT, 'so-quota.jsonl')) else 0
NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
qlog = open(os.path.join(OUT, 'so-quota.jsonl'), 'a')


class QuotaStop(Exception): pass


def call(ep, params, tag):
    global used
    if used + COST[ep] > CAP: raise QuotaStop(f'chạm trần mềm {CAP}')
    url = BASE + ep + '?' + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    status, body = 0, {}
    try:
        with urllib.request.urlopen(req, timeout=60) as r: status, body = r.status, json.load(r)
    except urllib.error.HTTPError as e:
        status = e.code
        try: body = json.load(e)
        except Exception: body = {}
    used += COST[ep]
    reason = ((body.get('error') or {}).get('errors') or [{}])[0].get('reason') if status != 200 else None
    qlog.write(json.dumps({'t': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'endpoint': ep + '.list',
                           'tag': tag, 'units': COST[ep], 'cum': used, 'http': status, 'reason': reason,
                           'n': len(body.get('items', []))}, ensure_ascii=False) + '\n'); qlog.flush()
    if status == 403 and reason in ('quotaExceeded', 'dailyLimitExceeded'): raise QuotaStop(reason)
    return body if status == 200 else None


def main():
    after21 = (NOW - dt.timedelta(days=21)).isoformat().replace('+00:00', 'Z')
    after7 = (NOW - dt.timedelta(days=7)).isoformat().replace('+00:00', 'Z')
    plan = [dict(regionCode=r, videoCategoryId=c, publishedAfter=after21, tag=f'{r}/{c or "all"}/21d') for r in REGIONS for c in CATS]
    plan += [dict(regionCode=r, publishedAfter=after7, tag=f'{r}/all/7d') for r in REGIONS]
    plan += [dict(relevanceLanguage=l, publishedAfter=after21, tag=f'lang:{l}/21d') for l in LANGS]
    if '--dai' in sys.argv:
        plan = [dict(regionCode=r, videoDuration='medium', publishedAfter=after21, tag=f'{r or "global"}/medium/21d') for r in ['US', 'IN', 'BR', 'ID', 'MX', 'PH', None]]
        plan += [dict(regionCode=r, videoDuration='long', publishedAfter=after21, tag=f'{r or "global"}/long/21d') for r in ['US', 'IN', None]]
    hits, stop = {}, None   # video id -> danh sách truy vấn trúng
    try:
        for p in plan:
            tag = p.pop('tag')
            b = call('search', dict(part='snippet', type='video', order='viewCount', maxResults=50, **p), tag)
            for it in (b or {}).get('items', []):
                vid = it['id'].get('videoId')
                if vid: hits.setdefault(vid, []).append(tag)
            time.sleep(0.2)
        ids = list(hits)
        videos, channels = {}, {}
        for i in range(0, len(ids), 50):
            b = call('videos', dict(part='snippet,statistics,contentDetails,status,topicDetails', id=','.join(ids[i:i + 50]), maxResults=50), f'videos[{i}]')
            for v in (b or {}).get('items', []): videos[v['id']] = v
        cids = sorted({v['snippet']['channelId'] for v in videos.values()})
        for i in range(0, len(cids), 50):
            b = call('channels', dict(part='snippet,statistics,brandingSettings', id=','.join(cids[i:i + 50]), maxResults=50), f'channels[{i}]')
            for c in (b or {}).get('items', []): channels[c['id']] = c
    except QuotaStop as e:
        stop = str(e); videos = locals().get('videos', {}); channels = locals().get('channels', {})
    json.dump({'measured_at': NOW.isoformat(), 'units_used': used, 'stopped': stop, 'plan_size': len(plan),
               'hits': hits, 'videos': videos, 'channels': channels},
              open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
    print(f'đo {NOW.isoformat()} · đơn vị {used} · id {len(hits)} · video {len(videos)} · kênh {len(channels)} · dừng={stop}')


if __name__ == '__main__': main()
