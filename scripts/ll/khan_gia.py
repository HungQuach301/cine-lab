#!/opt/cine/bin/python
"""Last Lamplighters · sinh reports/m3/epNN/KHAN-GIA.md từ timeline (chủ dự án, 05/10/2026, mục B9).
  khan_gia.py <episode.yaml>
Bảng các đoạn theo mốc thời gian thật + ô trống cho số YouTube Studio ở mốc 48 giờ và 7 ngày.
Chủ dự án chỉ gửi ảnh chụp YouTube Studio; Claude điền số vào ô và đọc (đoạn nào rơi người xem, Shorts nào kéo người xem)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import ll
EP = sys.argv[1]; E = ll.load(EP); TL = json.load(open(os.path.join(E['out'], 'timeline.json')))
mm = lambda s: f'{int(s // 60)}:{s % 60:04.1f}'
first = lambda v, n=9: ' '.join((v or '(không lời)').split()[:n]) + ('…' if v and len(v.split()) > n else '')
VO = {s['id']: s.get('vo') for s in E['segments']}
L = [f"# KHÁN GIẢ — {E['id']} · {E.get('title', '')}", '',
     'Tự sinh bởi `scripts/ll/khan_gia.py` khi dựng. Chủ dự án gửi ảnh chụp YouTube Studio (Tổng quan, Mức độ tương tác → Giữ chân người xem, Nguồn lưu lượng, thử nghiệm thumbnail) ở mốc **48 giờ** và **7 ngày**; Claude điền và đọc.', '',
     '## 1. Số chung', '', '| Chỉ số | 48 giờ | 7 ngày |', '|---|---|---|']
L += [f'| {k} |  |  |' for k in ('Lượt xem', 'Số lần hiển thị thumbnail', 'CTR thumbnail (%)', 'Thời lượng xem trung bình', 'Tỷ lệ xem trung bình (%)', 'Người xem giữ lại ở 0:30 (%)', 'Thumbnail thắng A/B (T1/T2)', 'Nguồn lưu lượng chính', 'Người đăng ký mới')]
L += ['', f"## 2. Giữ chân theo đoạn (tổng {mm(TL['tong_s'])}; tỷ lệ {TL.get('ty_le')})", '',
      '| Đoạn | Phần | Từ | Đến | Mở đầu lời | Giữ chân ở đầu đoạn 48 giờ (%) | 7 ngày (%) | Ghi chú (rơi/tăng) |', '|---|---|---|---|---|---|---|---|']
L += [f"| {s['id']} | {s['part']} | {mm(s['t0'])} | {mm(s['t1'])} | {first(VO.get(s['id']))} |  |  |  |" for s in TL['segments']]
L += ['', '## 3. Shorts', '', '| Short | Hook | Dài (s) | Lượt xem 48 giờ | 7 ngày | % xem hết | Lượt sang phim dài |', '|---|---|---|---|---|---|---|']
L += [f"| {s['id']} | {s.get('hook', '')} | {s['t1']:.1f} |  |  |  |  |" for s in TL.get('shorts', [])]
L += ['', '## 4. Đọc số (Claude điền)', '', '- 48 giờ: ', '- 7 ngày: ', '- Bài học đưa vào `reports/m3/BAI-HOC-LL.md`: ', '']
out = os.path.join(os.path.dirname(os.path.abspath(EP)), 'KHAN-GIA.md'); open(out, 'w').write('\n'.join(L)); print(out)
