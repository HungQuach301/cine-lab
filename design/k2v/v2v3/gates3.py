#!/opt/cine/bin/python -I
"""NC-V2V3 · 3 điểm cổng NC-CPU/NC-GPU (design/pt/cpu/gates.json @nc-cpu) có cả A (NC-CPU) và Cycles GPU (NC-GPU) cùng chỗ: hero (H3 10,4 s),
vây hãm (C1a 21,8 s), bờ + chiến sự (H2 13,3 s). Opt shot NGUYÊN BẢN V7B (episode-v7b-a.yaml @317dcf5), cửa sổ 17 khung quanh khung cổng (khung giữa = cổng).
  gates3.py <worktree V7B> <ra.json>"""
import copy, json, sys, yaml
from pathlib import Path
E = yaml.safe_load(open(Path(sys.argv[1]) / 'channel-k2/k2c-t3-01/v7p/episode-v7b-a.yaml'))['heroes']
G = [('hero', 'v7b_H3', 10.4), ('vay-ham', 'v7b_C1a', 21.8), ('bo-chien-su', 'v7b_H2', 13.3)]
C = {k: dict(opt=copy.deepcopy(E[s]['opt']), dur=E[s]['dur'], shot=s, t=t, f=round(t * 24), from_=round(t * 24) - 8, to=round(t * 24) + 9) for k, s, t in G}
json.dump(C, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1); print({k: (v['shot'], v['f'], v['dur']) for k, v in C.items()})
