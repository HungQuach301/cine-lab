#!/opt/cine/bin/python
"""Q22 chữ tràn khung (chủ dự án duyệt 06/10/2026, G2 tập 5): mọi hộp chữ ở khung mẫu nằm trong khung, cách mép trái/phải ≥ LE px.

Dữ liệu: log render (<đoạn>.mkv.log.json, mục `text`: hộp chữ đã qua phép biến đổi máy quay, ghi ở mọi khung mẫu).
Chữ trang trí (o.deco) và chữ mờ (alpha < 0,95) không vào log nên không bị tính.
Gọi: check(logs) với logs = {tên: log} → danh sách lỗi.  Tự kiểm: python overflow_check.py --self-test
"""
import sys

LE = 8   # px, lề tối thiểu với mép trái/phải


def check(logs):
    bad = []
    for k, L in logs.items():
        W, H = (1080, 1920) if L.get('fmt') == '9x16' else (1920, 1080)
        seen = set()
        for t in L.get('text', []):
            for e in t['items']:
                x0, y0, x1, y1 = e['box']
                if (x0 < LE or x1 > W - LE or y0 < 0 or y1 > H) and e['s'] not in seen:
                    seen.add(e['s']); bad.append(f"{k} f{t['f']} “{e['s']}” hộp {x0}…{x1} (khung {W})")
    return bad


if __name__ == '__main__' and '--self-test' in sys.argv:
    L = {'fmt': '9x16', 'text': [{'f': 0, 'items': [{'s': 'Source: BLS, Occupational Outlook', 'box': [-338, 1769, 1418, 1800]},
                                                    {'s': 'ok', 'box': [100, 10, 900, 40]}]}]}
    r = check({'S1': L}) and len(check({'S1': L})) == 1 and not check({'S1': {'fmt': '16x9', 'text': [{'f': 0, 'items': [{'s': 'a', 'box': [110, 1040, 1700, 1060]}]}]}})
    print('overflow_check tự kiểm', 'ĐẠT' if r else 'TRƯỢT'); sys.exit(0 if r else 1)
