#!/opt/cine/bin/python -I
"""NC-V2V3 · tạo job.json cho wf_vace.py (đường dẫn trên pod /w/ctrl/<clip>/…, ra /w/ra/<nhãn>).
  mk_job3.py <clip c1|c2|c4B> <A|B> <nhãn> <tệp ra> [--n 81 --seed 20102026 --steps 20 --sd 1.0 --sc 1.0 --w 1280 --h 720 --cfg 3.5]
A: độ sâu (cường độ sd) + cạnh (sc) toàn khung, không mặt nạ. B: như A nhưng mỗi lớp mang điểm ảnh nguồn ở vùng giữ + mặt nạ (trắng = AI vẽ)."""
import argparse, json, os
ap = argparse.ArgumentParser(); ap.add_argument('clip'); ap.add_argument('mode'); ap.add_argument('lab'); ap.add_argument('out')
for k, d in [('n', 81), ('seed', 20102026), ('steps', 20), ('split', -1), ('w', 1280), ('h', 720)]: ap.add_argument('--' + k, type=int, default=d)
for k, d in [('sd', 1.0), ('sc', 1.0), ('cfg', 3.5), ('shift', 8.0)]: ap.add_argument('--' + k, type=float, default=d)
a = ap.parse_args(); P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prompts3.json'))); ck = a.clip[:2]
C = f'/w/ctrl/{a.clip}'
ctrl = ([{'dir': f'{C}/depth', 'strength': a.sd}, {'dir': f'{C}/canny', 'strength': a.sc}] if a.mode == 'A' else
        [{'dir': f'{C}/bdepth', 'mask_dir': f'{C}/mask', 'strength': a.sd}, {'dir': f'{C}/bcanny', 'mask_dir': f'{C}/mask', 'strength': a.sc}])
ctrl = [c for c in ctrl if c['strength'] > 0]
J = dict(nhan=a.lab, clip=a.clip, che_do=a.mode, w=a.w, h=a.h, n=a.n, start=0, seed=a.seed, steps=a.steps, split=a.split if a.split >= 0 else a.steps // 2, cfg=a.cfg, shift=a.shift,
         sampler='euler', sched='simple', pos=P['chung'] + ' ' + P['clip'][ck], neg=P['neg_c1'] if ck == 'c1' else P['neg'], ctrl=ctrl, out=f'/w/ra/{a.lab}')
json.dump(J, open(a.out, 'w'), ensure_ascii=False, indent=1); print(a.out, a.lab)
