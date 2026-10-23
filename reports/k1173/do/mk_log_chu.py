"""LOG CHỮ TỔNG HỢP từ đặc tả bản cuối T3 (log render thật ở <out>/sec đã mất cùng container dựng). Tái tạo đúng các vai mà k2check-1.17.2-cap-l3 báo:
thẻ chương vai `chuong` (log render ghi vậy), chữ thẻ PP vai rỗng, bộ đếm năm vai `year`. Mẫu mỗi 12 khung. CHỈ để tái hiện khiếu nại A6."""
import json, sys, yaml
E = yaml.safe_load(open(sys.argv[1])); TL = json.load(open(sys.argv[2])); out = {}
SP = {s['id']: (s['t0'], s['t1']) for s in TL['segments']}
T = TL['tong_s']; n = int(round(T * 24))
for f in range(0, n, 12): out.setdefault(f, []).append(dict(role='year', s='1704', alpha=1))
for s in E['segments']:
    a, b = SP[s['id']]
    for sh in s.get('shots') or []:
        p = sh.get('p') or {}; c = p.get('the_chuong')
        if isinstance(c, dict):
            t0 = a + float(sh.get('at') or 0) + float(c['at']); t1 = t0 + float(c['dur'])
            for f in range(0, n, 12):
                if t0 <= f / 24 < t1: out.setdefault(f, []).append(dict(role='chuong', s=c['s'], alpha=1))
        cd = p.get('card') or {}
        if sh.get('type') == 'card' and cd:
            for f in range(0, n, 12):
                if a <= f / 24 < b:
                    out.setdefault(f, []).append(dict(role='', s=cd['title'], alpha=1))
                    for it in cd.get('items') or []:
                        if f / 24 >= a + float(it.get('at') or 0): out[f].append(dict(role='', s=it['s'], alpha=1))
json.dump([dict(f=f, items=v) for f, v in sorted(out.items())], open(sys.argv[3], 'w'), ensure_ascii=False)
print(len(out), 'khung mẫu')
