#!/opt/cine/bin/python
"""NV-2 · xuất dai-m1.csv, dai-m2.csv, shorts-m1.csv, shorts-m2.csv, kenh-theo-doi.csv, quet.json (rút gọn: id + số liệu,
không mô tả/khoá), so-ai.jsonl; in bảng Markdown + số kiểm ra $SCR/bang.md. Bản sao sửa từ scripts/nc-viral/xuat.py.
  xuat.py <raw4.json> <cand4.json> <kenh4.json> <truoc.json>
Ngách: phiên tự gán bằng tay theo KÊNH (tiêu đề + mô tả kênh/video), không gọi Claude API. Mức: gần (lõi ngách Moving Parts:
lịch sử, bản đồ/địa lý, timelapse/3D, "how it was built", tài liệu) · vừa (giải thích khoa học/đồ vật, có phần lịch sử) · xa.
AI: chỉ ghi khi mô tả video/kênh TỰ NÓI dùng AI (regex dưới, đã đọc tay từng câu khớp).
"""
import csv, datetime as dt, json, os, re, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'reports', 'nc-viral-2')
raw, cand, kenh, tr = (json.load(open(p)) for p in sys.argv[1:5])
UP = tr['uploads']
NOW = dt.datetime.fromisoformat(raw['measured_at'])
P = lambda s: dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
NICHE = {
    '@trialandeureka': ('gần', 'Lịch sử phát minh/kỹ thuật – hoạt hình giải thích'), '@historymapslore': ('gần', 'Lịch sử – bản đồ trận đánh'),
    '@discoverywithambrose': ('gần', 'Tài liệu khám phá (xác tàu, bí ẩn)'), '@buriedevidence3': ('gần', 'Tài liệu khảo cổ/địa chất'),
    '@whyograph': ('gần', 'Bản đồ – địa chính trị'), '@cityeons': ('gần', '3D timelapse thành phố'),
    '@sincoordenadas-i5v': ('gần', 'Tài liệu địa lý quốc gia (es)'), '@geoevum': ('gần', 'Bản đồ lịch sử – đế quốc'),
    '@its.layers': ('gần', 'How it was built – công trình (kênh tổng hợp)'), '@whyitwasbuilt': ('gần', 'Kỹ thuật – vì sao xây thế'),
    '@nobodycareswhatiswrittenhere': ('gần', '3D timelapse thành phố'), '@floridagilded': ('gần', 'Lịch sử địa phương – dinh thự'),
    '@urbavision': ('gần', '3D timelapse thành phố'), '@thecityclock': ('gần', '3D timelapse thành phố'),
    '@urbisanno': ('gần', '3D timelapse thành phố'), '@kwentongkatotohanan': ('gần', 'Lịch sử/bí ẩn (tiếng Filipino)'),
    '@howitworksin3d': ('gần', 'Giải thích 3D – cách hoạt động'), '@slatescope': ('gần', 'Kỹ thuật công trình'),
    '@buildbreakdown0': ('gần', 'Kỹ thuật cổ đại'), '@thewayitwasmade': ('gần', 'Lịch sử máy móc/siêu dự án'),
    '@buildingshowto': ('gần', 'How it was built – 3D'), '@hownatomy': ('gần', 'Giải thích 3D cắt lớp'),
    '@palimpsest10': ('gần', 'Khảo cổ/lịch sử bí ẩn'), '@history22-q6d': ('gần', 'Lịch sử tổng hợp'),
    '@worlddiscovery-1m': ('gần', 'Khảo cổ/bí ẩn'), '@innerworkings_tv': ('gần', 'Kỹ thuật công trình'),
    '@watchthewhyside': ('vừa', 'Giải thích 3D đồ vật/khoa học (có lịch sử)'), '@onewildstory': ('vừa', 'Khoa học "what if"/tò mò'),
    '@therealpennsylvania': ('vừa', 'Lịch sử/xếp hạng địa phương'), '@themanufacturinglens': ('vừa', 'Nhà máy – sản xuất'),
    '@telugulearningwithanika': ('xa', 'Trẻ em – học tiếng Telugu'), '@smcreate0': ('xa', 'Nhạc Hindi so sánh'),
    '@lovenostalgi': ('xa', 'Meme hoài niệm then vs now'), '@aliwildlife27': ('xa', 'Tài liệu động vật'),
    '@ao3dp': ('xa', 'In 3D hoạt hình'), '@twigbytwigofficial': ('xa', 'Chim làm tổ (macro)'),
    '@cineflexentertainment': ('xa', 'Phim truyện đầy đủ'), '@keyro-blox': ('xa', 'Gaming Roblox'),
    '@cutekittenpuppystories': ('xa', 'Xây nhà mini (kênh đổi chủ đề)'),
}
FAKE = re.compile(r'(?i)(AI-generated illustrations|AI-assisted archival|AI-generated scanning|AI-generated documentary|AI visual reconstruction|AI-assisted biblical documentary)')
WILD = re.compile(r'(?i)(AI-generated wildlife reconstruction|AI-assisted visual recreations|realistic AI wildlife)')
AIDECL = re.compile(r'(?i)(AI voice|Voice: AI|an AI voice|leverage advanced AI tools)')
# Cờ 'AI giả tư liệu thật' chỉ cho kênh dựng cảnh LỊCH SỬ như thật (Apollo, kim tự tháp, khảo cổ); nhà máy/công trình hiện đại → AI tự khai.
HIST = {'@whyitwasbuilt', '@kwentongkatotohanan', '@worlddiscovery-1m'}
NOAI = re.compile(r'(?i)no AI (imagery|images)|\(No AI\)')
REUP = {'@cineflexentertainment': 'nghi đăng lại phim có bản quyền (tiêu đề "Full Hollywood Action Movie")'}


def flags(r, v):
    f = []
    if r['handle'] in REUP: f.append(REUP[r['handle']])
    lk = r['likes']
    if lk is None: f.append('ẩn lượt thích')
    elif r['views'] and int(lk) / r['views'] < 0.002: f.append(f"nghi mua lượt (thích/xem {100 * int(lk) / r['views']:.3f} %)")
    if r['comments'] in (None, '0'): f.append('bình luận tắt' + (' (nhãn trẻ em)' if r['mfk'] else ''))
    elif r['mfk']: f.append('madeForKids')
    txt = r['desc'] + '\n' + r['ch_desc']
    if FAKE.search(txt) and r['handle'] in HIST: f.append('AI giả tư liệu thật (tự khai)')
    elif FAKE.search(txt): f.append('AI tự khai (hình AI dựng như thật, không phải cảnh lịch sử)')
    elif WILD.search(txt): f.append('AI tự khai: tái dựng thiên nhiên như thật')
    elif AIDECL.search(txt): f.append('AI tự khai (giọng/công cụ)')
    if NOAI.search(txt): f.append('tự khai "No AI"')
    return '; '.join(f)


def before(r):
    ds = [d for _, d in UP.get(r['cid'], []) if d]
    return sum(1 for d in ds if d < r['pub'])


def cadence(cid):
    ds = sorted(d for _, d in UP.get(cid, []) if d)
    if not ds: return None
    span = (NOW - P(ds[0])).total_seconds() / 86400
    return round(len(ds) / max(span, 1), 2)


rows = []
for r in cand:
    if not r['m2']: continue
    assert r['handle'] in NICHE, r['handle']
    muc, ngach = NICHE[r['handle']]
    rows.append(dict(muc=('M1' if r['m1'] else 'M2'), hang=r['m1'] or r['m2'], muc_ngach=muc, ngach=ngach, tieu_de=r['title'],
        link=f"https://www.youtube.com/watch?v={r['id']}", kenh=r['ch'], handle=r['handle'], link_kenh=f"https://www.youtube.com/channel/{r['cid']}",
        ngay_tao_kenh=r['ch_created'][:10], ngay_dang=r['pub'][:16].replace('T', ' '), kenh_tuoi_luc_dang_ngay=r['ch_age'],
        nhom_kenh='≤ 30 ngày' if r['ch_age'] <= 30 else '31–90 ngày', tuoi_video_ngay=r['age'], luot_xem=r['views'], xem_moi_ngay=r['vpd'],
        nguong_m1=r['need_m1'], nguong_m2=r['need_m2'], thich=r['likes'] or '', binh_luan=r['comments'] or '', thoi_luong_s=r['dur'],
        nhom_do_dai=r['nhom'], so_video_kenh=r['nvid'], video_truoc_do=before(r), nhip_dang_video_ngay=cadence(r['cid']), dang_ky=r['subs'],
        xem_tren_dang_ky=r['v_per_sub'] or '', ngon_ngu=r['lang'] or '', quoc_gia=r['country'] or '', danh_muc=r['cat'],
        nguon='search' if any(h != 'uploads' for h in r['hits']) else 'uploads kênh', co=flags(r, None), _id=r['id']))


def order(L): return sorted(L, key=lambda x: (x['muc_ngach'] == 'xa', x['hang'] != 'A', -x['xem_moi_ngay']))


T = {}
for dai in (True, False):
    for m in ('M1', 'M2'):
        T[('dai' if dai else 'shorts') + '-' + m.lower()] = order([r for r in rows if (r['thoi_luong_s'] > 180) == dai and r['muc'] == m])
cols = [k for k in rows[0] if not k.startswith('_')]
for name, L in T.items():
    with open(os.path.join(OUT, name + '.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, cols + ['trong_bang_chinh'], extrasaction='ignore'); w.writeheader()
        k = 0
        for r in L:
            tag = 'ngoài ngách (xa)' if r['muc_ngach'] == 'xa' else ('có' if k < 20 else 'phụ lục')
            if r['muc_ngach'] != 'xa': k += 1
            w.writerow({**r, 'trong_bang_chinh': tag})

# Kênh theo dõi: kênh gần/vừa, ≤ 90 ngày tuổi lúc đo, xếp theo đăng ký/ngày tuổi kênh (dù chưa đạt M2).
KT = []
for k in kenh:
    h = k['handle']
    if h not in NICHE or NICHE[h][0] == 'xa': continue
    my = [r for r in cand if r['cid'] == k['cid']]
    best = max(my, key=lambda r: r['views']) if my else None
    sh = sum(1 for r in my if r['dur'] <= 180)
    fl = set()
    for r in my:
        for x in flags(r, None).split('; '):
            if 'AI' in x: fl.add(x)
    KT.append(dict(kenh=k['ch'], handle=h, link_kenh=f"https://www.youtube.com/channel/{k['cid']}", muc_ngach=NICHE[h][0], ngach=NICHE[h][1],
        ngay_tao=k['created'][:10], tuoi_kenh_ngay=k['age'], dang_ky=k['subs'], dang_ky_moi_ngay=k['subs_per_day'], so_video=k['nvid'],
        tong_luot_xem=k['views'], video_30_ngay=len(my), shorts_30_ngay=sh, dai_30_ngay=len(my) - sh, nhip_dang_video_ngay=cadence(k['cid']),
        so_video_m2=sum(1 for r in my if r['m2']), so_video_m1=sum(1 for r in my if r['m1']),
        video_cao_nhat=best['title'] if best else '', link_video_cao_nhat=f"https://www.youtube.com/watch?v={best['id']}" if best else '',
        luot_xem_cao_nhat=best['views'] if best else '', do_dai_video_cao_nhat_s=best['dur'] if best else '', co_ai='; '.join(sorted(fl))))
KT.sort(key=lambda x: -x['dang_ky_moi_ngay'])
KT = KT[:15]
with open(os.path.join(OUT, 'kenh-theo-doi.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, list(KT[0])); w.writeheader(); w.writerows(KT)

ids = {r['_id'] for r in rows}
json.dump({'measured_at': raw['measured_at'], 'published_after': raw['published_after'], 'units_used': raw['units_used'],
           'units_upper_if_429_charged': raw['units_upper'], 'search_stop': raw['stopped'], 'uploads_stop': raw.get('uploads_stop'),
           'plan': raw['plan'], 'search_ok': sorted({h for v in raw['hits'].values() for h in v if h != 'uploads'}),
           'hits': {k: v for k, v in raw['hits'].items()},
           'videos': {k: {'channelId': v['snippet']['channelId'], 'publishedAt': v['snippet']['publishedAt'], 'fetched': v.get('_fetched', raw['measured_at']),
                          'categoryId': v['snippet'].get('categoryId'), 'duration': v['contentDetails'].get('duration'),
                          'statistics': v['statistics'], 'madeForKids': v['status'].get('madeForKids'), 'm2': k in ids}
                      for k, v in raw['videos'].items()},
           'channels': {k: {'publishedAt': c['snippet']['publishedAt'], 'customUrl': c['snippet'].get('customUrl'), 'country': c['snippet'].get('country'),
                            'statistics': c['statistics']} for k, c in raw['channels'].items()},
           'uploads_dates': {k: [d for _, d in v] for k, v in UP.items()}},
          open(os.path.join(OUT, 'quet.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
with open(os.path.join(OUT, 'so-ai.jsonl'), 'w') as fh:
    fh.write(json.dumps({'t': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'viec': 'phân loại ngách (gần/vừa/xa) cho 40 kênh, cờ AI',
                         'cach': 'phiên tự gán bằng tay (bảng NICHE + regex AI trong scripts/nc-viral-2/xuat.py); không gọi Claude API',
                         'goi_api': 0, 'usd': 0.0}, ensure_ascii=False) + '\n')


def n(x): return f"{int(x):,}".replace(',', ' ') if x not in ('', None) else 'ẩn'


def md(L):
    out = ['| # | Hạng | Video | Kênh | Kênh tạo | Tuổi kênh lúc đăng (ngày) | Đăng (UTC) | Tuổi video (ngày) | Xem | Xem/ngày | Thích | BL | Dài (s) · nhóm | Video kênh (trước) | Đăng ký | Xem/ĐK | NN/QG | Ngách | Nguồn | Cờ |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(L, 1):
        t = r['tieu_de'].replace('|', '/'); t = t if len(t) <= 60 else t[:57] + '…'
        out.append(f"| {i} | {r['hang']} | [{t}]({r['link']}) | [{r['kenh'].replace('|', '/').strip()}]({r['link_kenh']}) | {r['ngay_tao_kenh']} | {r['kenh_tuoi_luc_dang_ngay']} | {r['ngay_dang']} | "
                   f"{r['tuoi_video_ngay']} | {n(r['luot_xem'])} | {n(r['xem_moi_ngay'])} | {n(r['thich'])} | {n(r['binh_luan']) if r['binh_luan'] else '—'} | {r['thoi_luong_s']} · {r['nhom_do_dai']} | "
                   f"{r['so_video_kenh']} ({r['video_truoc_do']}) | {n(r['dang_ky'])} | {r['xem_tren_dang_ky']} | {r['ngon_ngu'] or '—'}/{r['quoc_gia'] or '—'} | {r['ngach']} ({r['muc_ngach']}) | {r['nguon']} | {r['co'] or '—'} |")
    return '\n'.join(out)


def mdk(L):
    out = ['| # | Kênh | Ngách | Tạo | Tuổi (ngày) | Đăng ký | ĐK/ngày | Video (30 ngày: Shorts/dài) | Nhịp (video/ngày) | M2 (M1) | Video cao nhất | Cờ AI |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, k in enumerate(L, 1):
        t = k['video_cao_nhat'].replace('|', '/'); t = t if len(t) <= 55 else t[:52] + '…'
        out.append(f"| {i} | [{k['kenh'].strip()}]({k['link_kenh']}) | {k['ngach']} ({k['muc_ngach']}) | {k['ngay_tao']} | {k['tuoi_kenh_ngay']} | {n(k['dang_ky'])} | {n(k['dang_ky_moi_ngay'])} | "
                   f"{k['so_video']} ({k['shorts_30_ngay']}/{k['dai_30_ngay']}) | {k['nhip_dang_video_ngay']} | {k['so_video_m2']} ({k['so_video_m1']}) | [{t}]({k['link_video_cao_nhat']}) — {n(k['luot_xem_cao_nhat'])}, {k['do_dai_video_cao_nhat_s']} s | {k['co_ai'] or '—'} |")
    return '\n'.join(out)


s = []
for name, L in T.items():
    G = [r for r in L if r['muc_ngach'] != 'xa']
    X = [r for r in L if r['muc_ngach'] == 'xa']
    s.append(f'## {name}: ngách {len(G)} (A {sum(r["hang"] == "A" for r in G)}), xa {len(X)}\n' + md(G[:20]) + '\n\nXA: ' +
             '; '.join(f"{r['kenh'].strip()} {n(r['luot_xem'])} ({r['ngach']})" for r in X))
s.append('## KENH\n' + mdk(KT))
# ±5 % quanh ngưỡng
near = []
for r in cand:
    for lab, need in (('M1', r['need_m1']), ('M2', r['need_m2'])):
        if r['age'] <= 30 and abs(r['views'] / need - 1) <= 0.05: near.append(f"{lab}: {r['ch'].strip()} — {r['title'][:50]} — {r['views']} / ngưỡng {need} ({100 * (r['views'] / need - 1):+.1f} %) [{NICHE.get(r['handle'], ('?',))[0]}]")
    if 85.5 <= r['ch_age'] <= 94.5: near.append(f"tuổi kênh 90: {r['ch'].strip()} {r['ch_age']} ngày (M2={r['m2']})")
    if 171 <= r['dur'] <= 189: near.append(f"Shorts 180 s: {r['ch'].strip()} — {r['title'][:40]} {r['dur']} s (M2={r['m2']})")
    if r['m2'] and 28.5 <= r['age'] <= 31.5: near.append(f"cửa sổ 30 ngày: {r['ch'].strip()} — {r['title'][:40]} tuổi {r['age']} (M2={r['m2']})")
for r in rows:
    if r['thich'] and 0.0019 <= int(r['thich']) / r['luot_xem'] <= 0.0021: near.append(f"thích/xem 0,2 %: {r['kenh']} {r['tieu_de'][:40]}")
s.append('## GAN NGUONG\n' + '\n'.join(near))
open(os.path.join(os.environ.get('SCR', '.'), 'bang.md'), 'w').write('\n\n'.join(s) + '\n')
print({k: (len([r for r in v if r['muc_ngach'] != 'xa']), len(v)) for k, v in T.items()}, 'kênh theo dõi', len(KT), 'gần ngưỡng', len(near))
