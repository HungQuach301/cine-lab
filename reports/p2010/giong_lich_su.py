#!/usr/bin/env python3
"""P-2010 · việc 5 bước 1: đọc lịch sử ElevenLabs (CHỈ GET, 0 ký tự) — liệt kê mục giọng G1 ngày 19/10/2026 (UTC) → lich-su-g1-1910.json.
Bộ đếm ký tự đọc trước/sau để chứng minh 0 ký tự."""
import json, urllib.request, urllib.parse, datetime as dt, sys
from pathlib import Path
API = 'https://api.elevenlabs.io'; UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
G1 = 'VDLncRBHDjLHBqLhQ1Qt'; H = Path(__file__).resolve().parent


def get(path):
    req = urllib.request.Request(API + path, method='GET', headers={'Accept': 'application/json', 'User-Agent': UA})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


c0 = get('/v1/user/subscription')['character_count']
a = int(dt.datetime(2026, 10, 19, tzinfo=dt.timezone.utc).timestamp()); b = a + 86400
items, after = [], None
while True:
    q = dict(page_size=1000, voice_id=G1)
    if after: q['start_after_history_item_id'] = after
    r = get('/v1/history?' + urllib.parse.urlencode(q)); items += r['history']
    if not r.get('has_more'): break
    after = r['last_history_item_id']
keep = []
for it in items:
    if not (a <= it['date_unix'] < b): continue
    keep.append(dict(id=it['history_item_id'], luc=dt.datetime.fromtimestamp(it['date_unix'], dt.timezone.utc).isoformat(), model=it.get('model_id'),
                     text=it.get('text'), ky_tu_truoc=it.get('character_count_change_from'), ky_tu_sau=it.get('character_count_change_to'),
                     content_type=it.get('content_type'), settings=it.get('settings'), source=it.get('source'), request_id=it.get('request_id')))
c1 = get('/v1/user/subscription')['character_count']
out = dict(ghi='Lịch sử ElevenLabs giọng G1, 19/10/2026 UTC; chỉ GET', tong_muc_g1=len(items), muc_1910=len(keep), dem_truoc=c0, dem_sau=c1, muc=keep)
(H / 'lich-su-g1-1910.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print('G1 tổng', len(items), '· 19/10', len(keep), '· bộ đếm', c0, '→', c1)
