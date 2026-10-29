#!/opt/cine/bin/python
"""NV-2 · lọc dữ liệu quét theo định nghĩa đo (bản sao sửa từ scripts/nc-viral/loc.py).
  loc.py <raw.json> <cand.json> <kenh.json>
- Kênh mới: channels.snippet.publishedAt ≤ 90 ngày trước videos.snippet.publishedAt (cột ch_age; nhóm ≤ 30 ngày tách riêng).
- Tuổi video tính tới lúc lấy số liệu (`_fetched`, lượt đầu không có thì dùng measured_at).
- M1: A = tuổi ≤ 7 ngày và ≥ 1 000 000; B = 7 < tuổi ≤ 30 và ≥ 1 000 000 × (tuổi/7)^0,5 (ước).
- M2: như M1 với 300 000; bảng M2 không gồm video đã đạt M1.
- cand.json: mọi video của kênh ≤ 90 ngày (có cột m1/m2); kenh.json: mọi kênh ≤ 90 ngày tuổi (tính tới lúc đo) trong mẫu.
"""
import datetime as dt, json, re, sys
raw = json.load(open(sys.argv[1]))
NOW = dt.datetime.fromisoformat(raw['measured_at'])
P = lambda s: dt.datetime.fromisoformat(s.replace('Z', '+00:00'))


def dur(s):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s or ''); d, h, mi, se = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def nhom(s):
    return 'Shorts' if s <= 180 else '3–10 phút' if s <= 600 else '10–20 phút' if s <= 1200 else '> 20 phút'


def hang(age, views, base):
    if age <= 7 and views >= base: return 'A'
    if 7 < age <= 30 and views >= base * (age / 7) ** 0.5: return 'B'
    return None


rows = []
for vid, v in raw['videos'].items():
    c = raw['channels'].get(v['snippet']['channelId'])
    if not c: continue
    vp, cp = P(v['snippet']['publishedAt']), P(c['snippet']['publishedAt'])
    t = P(v['_fetched']) if v.get('_fetched') else NOW
    ch_age = (vp - cp).total_seconds() / 86400
    if ch_age > 90 or ch_age < -1: continue
    age = (t - vp).total_seconds() / 86400
    st = v['statistics']; views = int(st.get('viewCount', 0)); subs = c['statistics'].get('subscriberCount')
    m1, m2 = hang(age, views, 1e6), hang(age, views, 3e5)
    d = dur(v['contentDetails'].get('duration'))
    rows.append(dict(id=vid, m1=m1, m2=m2, title=v['snippet']['title'], ch=c['snippet']['title'], cid=c['id'], ch_created=c['snippet']['publishedAt'],
        pub=v['snippet']['publishedAt'], age=round(age, 2), ch_age=round(ch_age, 1), views=views, vpd=round(views / max(age, 0.5)),
        need_m2=round(3e5 * max(age / 7, 1) ** 0.5), need_m1=round(1e6 * max(age / 7, 1) ** 0.5),
        likes=st.get('likeCount'), comments=st.get('commentCount'), dur=d, nhom=nhom(d),
        nvid=c['statistics'].get('videoCount'), subs=subs, hidden_subs=c['statistics'].get('hiddenSubscriberCount'),
        v_per_sub=round(views / int(subs), 1) if subs and int(subs) > 0 else None,
        country=c['snippet'].get('country'), lang=v['snippet'].get('defaultAudioLanguage') or v['snippet'].get('defaultLanguage'),
        cat=v['snippet'].get('categoryId'), handle=c['snippet'].get('customUrl'), mfk=v['status'].get('madeForKids'),
        hits=raw['hits'].get(vid, []), tags=v['snippet'].get('tags', [])[:15],
        desc=v['snippet'].get('description', ''), ch_desc=c['snippet'].get('description', '')))
rows.sort(key=lambda r: -r['vpd'])
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)

kenh = []
for cid, c in raw['channels'].items():
    cage = (NOW - P(c['snippet']['publishedAt'])).total_seconds() / 86400
    if cage > 90: continue
    subs = int(c['statistics'].get('subscriberCount') or 0)
    vs = [v for v in raw['videos'].values() if v['snippet']['channelId'] == cid]
    kenh.append(dict(cid=cid, ch=c['snippet']['title'], handle=c['snippet'].get('customUrl'), created=c['snippet']['publishedAt'], age=round(cage, 1),
        subs=subs, subs_per_day=round(subs / max(cage, 1)), nvid=c['statistics'].get('videoCount'), views=c['statistics'].get('viewCount'),
        country=c['snippet'].get('country'), ch_desc=c['snippet'].get('description', ''),
        sample=[dict(id=v['id'], title=v['snippet']['title'], views=int(v['statistics'].get('viewCount', 0)),
                     dur=dur(v['contentDetails'].get('duration'))) for v in vs]))
kenh.sort(key=lambda k: -k['subs_per_day'])
json.dump(kenh, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
for r in rows:
    if r['m2']:
        print(r['m1'] or '-', r['m2'], r['id'], r['nhom'], r['views'], r['age'], r['ch_age'], r['subs'], r['nvid'], r['country'], r['lang'], r['cat'], '|', r['ch'][:25], '|', r['title'][:80])
print('video kênh ≤90 ngày:', len(rows), '· M2:', sum(1 for r in rows if r['m2']), '· M1:', sum(1 for r in rows if r['m1']), '· kênh ≤90 ngày (tuổi lúc đo):', len(kenh))
