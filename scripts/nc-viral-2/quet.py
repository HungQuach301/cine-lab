#!/opt/cine/bin/python
"""NC-VIRAL-2 (NV-2) · quét YouTube Data API v3, ngách gần Moving Parts (lịch sử, bản đồ/địa lý, timelapse, 3D giải thích,
"how it was built", "then and now", tài liệu), video đăng ≤ 30 ngày trước thời điểm đo. Bản sao sửa từ scripts/nc-viral/quet.py.

  quet.py <raw.json>                               # lượt đầu
  quet.py <raw.json> --tiep <raw_cu.json> <probe.json>   # chạy tiếp: giữ kết quả cũ, bỏ truy vấn đã 200 trong sổ,
                                                          # dùng probe.json (search 'history' gọi tay) cho truy vấn 'history'
Lượt đầu gặp 429 rateLimitExceeded (giới hạn nhịp, KHÔNG phải quotaExceeded) ở 79/84 search.list do gọi cách 0,2 s.
Sửa: giãn 20 s giữa hai search.list (lượt 6 s vẫn 429 sau 3 lệnh); 429 → chờ 65 s thử lại ĐÚNG 1 lần, lặp 429 thì dừng. 429 ghi units = 0 (Google từ chối
trước khi xử lý), kèm cột units_neu_tinh_429 = chi phí danh nghĩa làm trần trên.
Khác NC-VIRAL: truy vấn theo từ khoá ngách (q), cửa sổ 30 ngày; gọi videos.list + channels.list XEN sau mỗi search.list
(id mới) để nếu quota hết giữa chừng thì mọi truy vấn đã chạy vẫn có đủ số liệu. Khoá API do proxy gắn cho www.googleapis.com —
script KHÔNG đọc/ghi khoá. Trần mềm 8 800 đơn vị (hạn mức phiên 9 000; phần còn lại cho playlistItems.list).
403 quotaExceeded → dừng ngay, ghi phần đã có, không thử lại.
"""
import datetime as dt, json, os, sys, time, urllib.parse, urllib.request, urllib.error

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'reports', 'nc-viral-2')
LED = os.path.join(OUT, 'so-quota.jsonl')
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
BASE = 'https://www.googleapis.com/youtube/v3/'
CAP = 8800
COST = {'search': 100, 'videos': 1, 'channels': 1}
_L = [json.loads(l) for l in open(LED)] if os.path.exists(LED) else []
used = sum(x['units'] for x in _L); upper = sum(x.get('units_neu_tinh_429', x['units']) for x in _L)
DONE = {x['tag'] for x in _L if x['endpoint'] == 'search.list' and x['http'] == 200}
NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
qlog = open(LED, 'a')


class QuotaStop(Exception): pass


def call(ep, params, tag, retry=True):
    global used, upper
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
    reason = ((body.get('error') or {}).get('errors') or [{}])[0].get('reason') if status != 200 else None
    u = 0 if status == 429 else COST[ep]
    used += u; upper += COST[ep]
    qlog.write(json.dumps({'t': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'endpoint': ep + '.list',
                           'tag': tag, 'units': u, 'cum': used, 'http': status, 'reason': reason,
                           'n': len(body.get('items', [])), 'usd': 0.0, 'units_neu_tinh_429': COST[ep], 'cum_tran_tren': upper},
                          ensure_ascii=False) + '\n'); qlog.flush()
    if status == 403 and reason in ('quotaExceeded', 'dailyLimitExceeded'): raise QuotaStop(reason)
    if status == 429:
        if not retry: raise QuotaStop('429 lặp lại sau 1 lần chờ')
        time.sleep(65); return call(ep, params, tag, retry=False)
    return body if status == 200 else None


def S(q=None, tag=None, **kw):
    return dict(q=q, tag=tag or '/'.join([q or '(rỗng)'] + [f'{k}={v}' for k, v in kw.items()]), **kw)


# Thứ tự = ưu tiên (nếu quota hết giữa chừng, phần đầu là phần quan trọng nhất).
PLAN = [
    # A · lõi ngách, mọi độ dài
    S('history'), S('how it was built'), S('3D timelapse'), S('map', videoDuration='medium'), S('history documentary', videoDuration='long'),
    S('evolution of'), S('city timelapse'), S('history', videoDuration='short'), S('engineering explained'), S('then and now'),
    S('ancient history'), S('medieval history'), S('empire history'), S('war history'), S('construction timelapse'),
    S('geography'), S('borders map'), S('why does exist'), S('3D animation explained'), S('archaeology'), S('lost city'), S('documentary'),
    # B · video dài (medium 4–20 phút, long > 20 phút)
    S('history', videoDuration='medium'), S('history', videoDuration='long'), S('ancient history', videoDuration='medium'),
    S('ancient history', videoDuration='long'), S('how it was built', videoDuration='medium'), S('documentary', videoDuration='medium'),
    S('geography', videoDuration='medium'), S('engineering explained', videoDuration='medium'), S('war history', videoDuration='medium'),
    S('war history', videoDuration='long'), S('archaeology', videoDuration='medium'), S('evolution of', videoDuration='medium'),
    S('lost city', videoDuration='medium'), S('medieval history', videoDuration='medium'), S('empire history', videoDuration='medium'),
    S('why does exist', videoDuration='medium'), S('3D animation explained', videoDuration='medium'), S('then and now', videoDuration='medium'),
    # C · theo danh mục (27 Education, 28 Science & Tech, 19 Travel & Events, 1 Film & Animation, 22 People & Blogs)
    S('history', videoCategoryId='27'), S('history', videoCategoryId='1'), S('history', videoCategoryId='22'), S('history', videoCategoryId='19'),
    S('history', videoCategoryId='28'), S('timelapse', videoCategoryId='1'), S('timelapse', videoCategoryId='19'), S('timelapse', videoCategoryId='28'),
    S('explained', videoCategoryId='27'), S('explained', videoCategoryId='28'), S('3D animation', videoCategoryId='1'), S('3D animation', videoCategoryId='27'),
    S(None, videoCategoryId='27', regionCode='US'), S(None, videoCategoryId='27', regionCode='GB'), S(None, videoCategoryId='27', regionCode='IN'),
    S(None, videoCategoryId='27', regionCode='BR'), S(None, videoCategoryId='27', regionCode='ID'), S(None, videoCategoryId='27', regionCode='DE'),
    S(None, videoCategoryId='28', regionCode='US'), S(None, videoCategoryId='28', regionCode='IN'),
    # D · ngoài tiếng Anh
    S('historia', relevanceLanguage='es'), S('documental historia', relevanceLanguage='es'), S('cómo se construyó', relevanceLanguage='es'),
    S('história', relevanceLanguage='pt'), S('como foi construído', relevanceLanguage='pt'), S('documentário história', relevanceLanguage='pt'),
    S('इतिहास', relevanceLanguage='hi'), S('history in hindi', relevanceLanguage='hi'), S('sejarah', relevanceLanguage='id'),
    S('sejarah dunia', relevanceLanguage='id'),
    # E · regionCode
    S('history', regionCode='GB'), S('history', regionCode='IN'), S('history', regionCode='BR'), S('history', regionCode='ID'),
    S('history', regionCode='DE'), S('timelapse', regionCode='US'),
    # F · Shorts
    S('3D timelapse', videoDuration='short'), S('map animation', videoDuration='short'), S('then and now', videoDuration='short'),
    S('ancient city', videoDuration='short'), S('evolution of', videoDuration='short'), S('how it was built', videoDuration='short'),
    S('history facts', videoDuration='short'), S('geography', videoDuration='short'),
]


def main():
    global NOW
    after = (NOW - dt.timedelta(days=30)).isoformat().replace('+00:00', 'Z')
    hits, videos, channels, stop = {}, {}, {}, None
    probe = None
    if '--tiep' in sys.argv:
        old = json.load(open(sys.argv[sys.argv.index('--tiep') + 1])); probe = json.load(open(sys.argv[sys.argv.index('--tiep') + 2]))
        NOW = dt.datetime.fromisoformat(old['measured_at']); after = old['published_after']   # giữ mốc đo của lượt đầu
        hits, videos, channels = old['hits'], old['videos'], old['channels']
    try:
        for p in PLAN:
            p = dict(p); tag = p.pop('tag')
            if tag in DONE or any(tag in h for h in hits.values()): continue
            if tag == 'history' and probe: b = probe
            else:
                b = call('search', dict(part='snippet', type='video', order='viewCount', maxResults=50, publishedAfter=after, **p), tag)
                time.sleep(20)
            new = []
            for it in (b or {}).get('items', []):
                vid = it['id'].get('videoId')
                if not vid: continue
                if vid not in hits and vid not in videos: new.append(vid)
                hits.setdefault(vid, []).append(tag)
            if new:
                b = call('videos', dict(part='snippet,statistics,contentDetails,status,topicDetails', id=','.join(new), maxResults=50), f'videos<{tag}>')
                for v in (b or {}).get('items', []): v['_fetched'] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'); videos[v['id']] = v
                nc = sorted({videos[v]['snippet']['channelId'] for v in new if v in videos} - set(channels))
                if nc:
                    b = call('channels', dict(part='snippet,statistics,contentDetails,brandingSettings', id=','.join(nc), maxResults=50), f'channels<{tag}>')
                    for c in (b or {}).get('items', []): channels[c['id']] = c
    except QuotaStop as e:
        stop = str(e)
    json.dump({'measured_at': NOW.isoformat(), 'published_after': after, 'units_used': used, 'stopped': stop, 'plan_size': len(PLAN),
               'units_upper': upper, 'search_with_hits': len({x for h in hits.values() for x in h}),
               'plan': [p['tag'] for p in PLAN], 'hits': hits, 'videos': videos, 'channels': channels},
              open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
    print(f'đo {NOW.isoformat()} · đơn vị {used} · id {len(hits)} · video {len(videos)} · kênh {len(channels)} · dừng={stop}')


if __name__ == '__main__': main()
