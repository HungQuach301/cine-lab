#!/opt/cine/bin/python
"""K-1.17 · dựng timeline.json TỐI THIỂU từ episode.yaml (segments → t0/t1, shots → at) để chạy lại k2check trên animatic T3
khi timeline thật (/var/tmp/cine-out/k2c-t3-anim, ngoài git) không còn. Không gọi prep.py (prep gọi ElevenLabs).
  tl_tu_dac_ta.py <episode.yaml> <ra timeline.json>"""
import json, sys
import yaml

E = yaml.safe_load(open(sys.argv[1])); t, S = 0.0, []
for s in E['segments']:
    d = float(s['dur']); sh = s.get('shots') or []
    ats = [float(x.get('at') or 0) for x in sh] + [d]
    S.append(dict(id=s['id'], t0=round(t, 6), t1=round(t + d, 6), dur=d, part=s.get('part'),
                  shots=[dict(tpl=x.get('tpl'), t0=ats[i], t1=max(ats[i], ats[i + 1]), type=x.get('type'), p=x.get('p') or {}) for i, x in enumerate(sh)]))
    t += d
json.dump(dict(segments=S, heroes=E.get('heroes') or {}, tong_s=round(t, 6)), open(sys.argv[2], 'w'), ensure_ascii=False)
print('tong_s', round(t, 3), 'đoạn', len(S))
