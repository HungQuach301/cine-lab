#!/opt/cine/bin/python
"""Q21 gán nguồn trên hình (chủ dự án, G2 tập 5, 06/10/2026): dòng nguồn đang hiện phải chứa nguồn của mọi số/câu đang hiện.

Dữ liệu: timeline.json → `capsrc` (ll.py ghi): với mỗi chú thích, tập nguồn thấy trên hình = nguồn dữ liệu của mẫu + nguồn riêng của câu.
Lỗi:
  (a) dòng nguồn hiện cùng câu thiếu nguồn của câu/số đang hiện;
  (b) câu có số, năm hoặc tên cơ quan (BLS, NAIC, Census…) mà không khai `num` hay `src: [...]` (`src: []` = câu không cần nguồn).
Gọi: check(E, TL) → danh sách lỗi.  Tự kiểm: python src_check.py --self-test
"""
import re
import sys

CLAIM = re.compile(r'\d|\b(BLS|NAIC|Census|OOH|NARA|LoC)\b')


def check(E, TL):
    S, CS, bad = E.get('sources', {}), TL.get('capsrc'), []
    if CS is None: return ['timeline thiếu capsrc (chạy lại ll.py prep)']
    for kind in ('segments', 'shorts'):
        for sg in TL.get(kind, []):
            for i, sh in enumerate(sg['shots']):
                p = sh.get('p', {})
                for j, c in enumerate(p.get('cap') or []):
                    info = CS.get(f"{sg['id']}/{i}/{j}")
                    if info is None: bad.append(f"{sg['id']}/{i}/{j}: thiếu capsrc"); continue
                    disp = (c.get('src') or p.get('src') or '').strip()
                    miss = [k for k in info['srcs'] if S.get(k, {}).get('short', k) not in disp]
                    if miss: bad.append(f"{sg['id']} “{c.get('s', '')[:40]}”: dòng nguồn thiếu {', '.join(miss)} (đang ghi “{disp[:50]}”)")
                    if not info['declared'] and CLAIM.search(c.get('s') or ''):
                        bad.append(f"{sg['id']} “{c.get('s', '')[:40]}”: câu có số/năm/cơ quan chưa khai num hoặc src")
    return bad


if __name__ == '__main__' and '--self-test' in sys.argv:
    E = {'sources': {'A': {'short': 'BLS Bulletin 1468 (1966)'}, 'B': {'short': 'BLS OOH (2025–35)'}}}
    shot = lambda caps, src: {'shots': [{'p': {'src': src, 'cap': caps}}]}
    # lỗi tập 5: câu 1966 hiện dưới dòng nguồn OOH
    bad1 = check(E, {'segments': [dict(id='00', **shot([{'s': '1966: judgment cannot be computerized (BLS)'}], 'Source: BLS OOH (2025–35)'))],
                     'capsrc': {'00/0/0': {'srcs': [], 'declared': False}}})
    bad2 = check(E, {'segments': [dict(id='00', **shot([{'s': '1966: judgment…', 'src': 'Source: BLS OOH (2025–35)'}], 'Source: BLS OOH (2025–35)'))],
                     'capsrc': {'00/0/0': {'srcs': ['A'], 'declared': True}}})
    ok = check(E, {'segments': [dict(id='00', **shot([{'s': '1966: judgment…', 'src': 'Source: BLS Bulletin 1468 (1966)'}, {'s': 'Who decides?', 'src': ' '}],
                                                     'Source: BLS OOH (2025–35)'))],
                   'capsrc': {'00/0/0': {'srcs': ['A'], 'declared': True}, '00/0/1': {'srcs': [], 'declared': True}}})
    r = len(bad1) == 1 and len(bad2) == 1 and ok == []
    print('src_check tự kiểm', 'ĐẠT' if r else f'TRƯỢT {bad1} {bad2} {ok}'); sys.exit(0 if r else 1)
