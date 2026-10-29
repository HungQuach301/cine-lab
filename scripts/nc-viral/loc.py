#!/opt/cine/bin/python
"""NC-VIRAL · lọc dữ liệu quét theo định nghĩa đo; in ứng viên (kênh ≤ 30 ngày trước video, hạng A/B)."""
import datetime as dt, json, re, sys
raw = json.load(open(sys.argv[1]))
NOW = dt.datetime.fromisoformat(raw['measured_at'])
P = lambda s: dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
def dur(s):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s or ''); d, h, mi, se = (int(x or 0) for x in m.groups()); return d*86400+h*3600+mi*60+se
rows = []
for vid, v in raw['videos'].items():
    c = raw['channels'].get(v['snippet']['channelId'])
    if not c: continue
    vp, cp = P(v['snippet']['publishedAt']), P(c['snippet']['publishedAt'])
    ch_age = (vp - cp).total_seconds() / 86400
    age = (NOW - vp).total_seconds() / 86400
    st = v['statistics']; views = int(st.get('viewCount', 0))
    if ch_age > 30 or ch_age < -1: continue
    if age <= 7 and views >= 1e6: hang = 'A'
    elif 7 < age <= 21 and views >= 1e6 * (age / 7) ** 0.5: hang = 'B'
    else: hang = None
    rows.append(dict(id=vid, hang=hang, title=v['snippet']['title'], ch=c['snippet']['title'], cid=c['id'], ch_created=c['snippet']['publishedAt'],
        pub=v['snippet']['publishedAt'], age=round(age, 2), ch_age=round(ch_age, 1), views=views, vpd=round(views / max(age, 0.5)),
        likes=st.get('likeCount'), comments=st.get('commentCount'), dur=dur(v['contentDetails'].get('duration')),
        nvid=c['statistics'].get('videoCount'), subs=c['statistics'].get('subscriberCount'), country=c['snippet'].get('country'),
        lang=v['snippet'].get('defaultAudioLanguage') or v['snippet'].get('defaultLanguage'), cat=v['snippet'].get('categoryId'),
        handle=c['snippet'].get('customUrl'), hits=len(raw['hits'].get(vid, []))))
rows.sort(key=lambda r: -r['vpd'])
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
for r in rows:
    print(r['hang'], r['id'], r['dur'], r['views'], r['age'], r['ch_age'], r['likes'], r['comments'], r['nvid'], r['subs'], r['country'], r['lang'], r['cat'], r['handle'], '|', r['ch'], '|', r['title'][:70])
print(len(rows), sum(1 for r in rows if r['hang']))
