#!/opt/cine/bin/python
"""NC-VIRAL · xuất video-dai.csv, shorts.csv, quet.json (rút gọn: id + số liệu, không mô tả/khoá), so-ai.jsonl; in bảng Markdown.
  xuat.py <raw.json> <cand.json> <raw2.json> <cand2.json> <truoc.json>"""
import csv, datetime as dt, json, os, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'reports', 'nc-viral')
raw1, c1, raw2, c2, tr = (json.load(open(p)) for p in sys.argv[1:6])
# Ngách: phiên tự gán bằng tay từ tiêu đề + mô tả (không gọi Claude API). AI = mô tả video/kênh TỰ NÓI dùng AI.
NICHE = {'ajjH9jQGDJU': 'Trẻ em – truyện nhân vật', '97v-ISQesJo': 'Bán hàng – phụ kiện xe', 'UTQle6WAvSA': 'Hoạt hình hoài niệm kiểu Ghibli',
 'E-Aio5HyWhM': 'Gia đình – em bé', 'YU3KhmHUfTg': 'Bán hàng – đồ trang trí', 'PsP3tUGZv7w': 'Gaming (tiêu đề thể thao lệch mô tả kênh)',
 'CTFJ-OdSP9U': 'Bán hàng – phụ kiện xe', 'UkBpKBU2-2Y': 'Trẻ em – hoạt hình tiếng Ả Rập', 'N4jB87mZGX8': 'Cải tạo/biến đổi đồ vật',
 '-VgwyMQU5U8': 'Nhào lộn/xiếc', 'nxPOSOYQFhw': 'Đoàn tụ cảm xúc', 'DSnY8_a6mJw': 'Quảng cáo sản phẩm', 'rfdCkPDhYtk': 'Mạo hiểm/stunt',
 'MLL8QiDZFi0': 'Truyện kể – phục chế xe', '9OeWy6q-X-A': 'Gia đình – em bé', 'VT0IWbHL4I0': 'Trục vớt/khám phá', 'zJXUkQKqpOg': 'Gia đình – em bé',
 '4c8nW0eASug': 'Truyện ngắn anh chị em', '4J51OQEDReo': 'Drama gia đình', 'vjlmPlVI-Ws': 'Drama xã hội', 'TLF9znXtSFc': 'Giải thích kỹ thuật (3D)',
 'MECqPd3deRo': 'Gia đình – hoạt động', 'DUZfv1I6X5U': 'Nông trại/đời sống quê', 'hRYWcfp6dsg': 'Lịch sử phát minh (giải thích)',
 'VTtaYwY956U': 'Gia đình – em bé', 'CmyNfvNOeic': 'Trồng cây (timelapse)', 'Re5eIR7KJy0': 'Gia đình – em bé', 'kzUe5s-Q1jo': 'Nhạc thiếu nhi',
 'QmHzxSgIXlk': 'Drama xã hội'}
AI = {'-VgwyMQU5U8', 'MLL8QiDZFi0', 'vjlmPlVI-Ws', 'DUZfv1I6X5U', 'VTtaYwY956U', 'Re5eIR7KJy0', 'QmHzxSgIXlk'}
BRAND = {'kzUe5s-Q1jo': 'kênh VEVO (mạng phân phối nhạc), mô tả dẫn về kênh gốc'}
SHOP = {'97v-ISQesJo', 'YU3KhmHUfTg', 'CTFJ-OdSP9U', 'DSnY8_a6mJw'}

def flags(r, v):
    f = []
    if r['id'] in BRAND: f.append('thương hiệu lớn: ' + BRAND[r['id']])
    if r['likes'] is None: f.append('ẩn lượt thích')
    elif int(r['likes']) / r['views'] < 0.002: f.append(f"nghi mua lượt (thích/xem {100*int(r['likes'])/r['views']:.3f} %)")
    if r['comments'] in (None, '0'): f.append('bình luận tắt' + (' (nhãn trẻ em)' if v['status'].get('madeForKids') else ''))
    if r['id'] in SHOP: f.append('kênh bán hàng')
    if r['id'] in AI: f.append('AI (tự khai trong mô tả)')
    return '; '.join(f)

rows = []
for raw, C in ((raw1, c1), (raw2, c2)):
    for r in C:
        v = raw['videos'][r['id']]
        rows.append(dict(hang=r['hang'], tieu_de=r['title'], link=f"https://www.youtube.com/watch?v={r['id']}", kenh=r['ch'],
            link_kenh=f"https://www.youtube.com/channel/{r['cid']}", ngay_tao_kenh=r['ch_created'][:10], ngay_dang=r['pub'][:16].replace('T', ' '),
            kenh_tuoi_luc_dang_ngay=r['ch_age'], tuoi_video_ngay=r['age'], luot_xem=r['views'], xem_moi_ngay=r['vpd'], thich=r['likes'] or '',
            binh_luan=r['comments'] or '', thoi_luong_s=r['dur'], so_video_kenh=r['nvid'], video_truoc_do=tr[r['id']]['before'], dang_ky=r['subs'],
            ngon_ngu=r['lang'] or '', quoc_gia=r['country'] or '', danh_muc=r['cat'], ngach=NICHE[r['id']], co=flags(r, v), _id=r['id'], _src=raw))
def order(L): return sorted(L, key=lambda x: (x['hang'] != 'A', -x['xem_moi_ngay']))
dai, sh = order([r for r in rows if r['thoi_luong_s'] > 180]), order([r for r in rows if r['thoi_luong_s'] <= 180])
cols = [k for k in rows[0] if not k.startswith('_')]
for name, L in (('video-dai.csv', dai), ('shorts.csv', sh)):
    with open(os.path.join(OUT, name), 'w', newline='') as fh:
        w = csv.DictWriter(fh, cols + ['trong_bang_chinh'], extrasaction='ignore'); w.writeheader()
        for i, r in enumerate(L): w.writerow({**r, 'trong_bang_chinh': 'có' if i < 20 else 'phụ lục'})
def slim(raw):
    return {'measured_at': raw['measured_at'], 'units_used_cum': raw['units_used'], 'search_calls': raw['plan_size'], 'hits': raw['hits'],
            'videos': {k: {'channelId': v['snippet']['channelId'], 'publishedAt': v['snippet']['publishedAt'], 'categoryId': v['snippet'].get('categoryId'),
                           'duration': v['contentDetails'].get('duration'), 'statistics': v['statistics'], 'madeForKids': v['status'].get('madeForKids')}
                       for k, v in raw['videos'].items()},
            'channels': {k: {'publishedAt': c['snippet']['publishedAt'], 'country': c['snippet'].get('country'), 'statistics': c['statistics']}
                         for k, c in raw['channels'].items()}}
json.dump({'luot1': slim(raw1), 'luot2_dai': slim(raw2), 'video_truoc_do': tr}, open(os.path.join(OUT, 'quet.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
with open(os.path.join(OUT, 'so-ai.jsonl'), 'w') as fh:
    fh.write(json.dumps({'t': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'), 'viec': 'phân loại ngách/định dạng/AI cho 29 ứng viên',
                         'cach': 'phiên tự gán bằng tay (bảng NICHE trong scripts/nc-viral/xuat.py); không gọi Claude API', 'goi_api': 0, 'usd': 0.0},
                        ensure_ascii=False) + '\n')
def md(L):
    n = lambda x: f"{int(x):,}".replace(',', '\u202f') if x not in ('', None) else 'ẩn'
    out = ['| # | Hạng | Video | Kênh | Kênh tạo | Đăng (UTC) | Tuổi (ngày) | Xem | Xem/ngày | Thích | BL | Dài (s) | Video kênh (trước) | Đăng ký | NN/QG | Ngách | Cờ |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(L, 1):
        t = r['tieu_de'].replace('|', '/'); t = t if len(t) <= 60 else t[:57] + '…'
        out.append(f"| {i} | {r['hang']} | [{t}]({r['link']}) | [{r['kenh'].replace('|', '/')}]({r['link_kenh']}) | {r['ngay_tao_kenh']} | {r['ngay_dang']} | "
                   f"{r['tuoi_video_ngay']} | {n(r['luot_xem'])} | {n(r['xem_moi_ngay'])} | {n(r['thich'])} | {r['binh_luan'] or '—'} | {r['thoi_luong_s']} | "
                   f"{r['so_video_kenh']} ({r['video_truoc_do']}) | {n(r['dang_ky'])} | {r['ngon_ngu'] or '—'}/{r['quoc_gia'] or '—'} | {r['ngach']} | {r['co'] or '—'} |")
    return '\n'.join(out)
open(os.path.join(os.environ.get('SCR', '.'), 'bang.md'), 'w').write('## DAI\n' + md(dai) + '\n\n## SHORTS\n' + md(sh[:20]) + '\n\n## PHU LUC\n' + md(sh[20:]) + '\n')
print(len(dai), len(sh))
