"""Timeline TỔNG HỢP từ đặc tả (không phải timeline prep của k2v): đoạn nối tiếp theo dur, shot theo `at` — chỉ để chạy k2check so 1.17.1 ↔ 1.17.2."""
import json, sys, copy, yaml
E = yaml.safe_load(open(sys.argv[1])); out = dict(id=E['id'], title=E.get('title'), music=[], segments=[], heroes=E.get('heroes') or {})
t = 0.0
for s in E['segments']:
    d = float(s['dur']); S = {k: copy.deepcopy(v) for k, v in s.items() if k != 'shots'}; S.update(t0=t, t1=t + d, frames=int(round(d * 24)), speech=[], sfx=[])
    sh = s.get('shots') or []; S['shots'] = []
    for i, x in enumerate(sh):
        a = float(x.get('at') or 0); b = float(sh[i + 1].get('at') or 0) if i + 1 < len(sh) else d
        y = copy.deepcopy(x); y.update(t0=a, t1=b); S['shots'].append(y)
    out['segments'].append(S); t += d
out['tong_s'] = round(t, 4); out['tong_khung'] = int(round(t * 24))
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False)
print(len(out['segments']), out['tong_s'])
