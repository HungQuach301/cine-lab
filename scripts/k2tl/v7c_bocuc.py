#!/opt/cine/bin/python
"""V7C (việc 2) · ĐO BỐ CỤC từng shot bằng mặt nạ ID (design/k2v/v7c/do_bocuc.js + idmask_v7c.js) — cùng thước cho V7B (trước) và V7C (sau).
  v7c_bocuc.py run <episode.yaml> <nhãn> [--root <cây mã>] [--every 12] [--shots H1,C4]   → reports/v7c/do/bocuc-<nhãn>/<shot>.json
  v7c_bocuc.py bang <nhãn> [<nhãn 2>]                                                     → bảng markdown (stdout) + reports/v7c/do/bocuc-<nhãn>.json
Số đo mỗi khung mẫu (mặc định 2 khung/s): % khung từng loại; NỘI DUNG = phố (nền đô thị) + nhà + trại + công sự + tàu + cờ + pin nổi + lửa + người + khác;
TRỐNG = nước + đất bằng tự nhiên + sườn (> 30 m) — vách/dốc Rock ('da') và trời tách riêng; TIÊU ĐIỂM (tieu-diem.json): bề ngang hộp bao ≥ 8 %, tâm ở 1/3 giữa hoặc giao điểm 1/3;
máy: AGL, góc nhìn xuống, tiêu cự (fov dọc → tiêu cự tương đương 35 mm). Góc cao (V7B-D1) = AGL ≥ 120 m HOẶC nhìn xuống ≥ 15°; AGL < 50 m = lướt thấp."""
import json, math, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]; OUT = ROOT / 'reports/v7c/do'
TD = json.loads((ROOT / 'design/k2v/v7c/tieu-diem.json').read_text())['vat']
# V7B: tiêu điểm + loại shot (đặc tả V7B không khai — gán theo vai truyện của câu lời)
V7B_TD = {'H1': [('bien_gioi', None)], 'H2': [('lau_dai', [0, 10.5]), ('pin_noi', [10.5, 21])], 'H3': [('duong_bang', None)], 'C1': [('trai', None)], 'C2': [('chan_thuyen', None)],
          'C3': [('hai_rau', [0, 3.9]), ('line_wall', [3.9, 99])], 'C4': [('old_mole', None)], 'C5': [('doan_darby', [0, 4.0]), ('pho_bi_ban', [4.0, 99])]}
V7B_LOAI = {'H1': 'pho', 'H2': 'vinh', 'H3': 'pho', 'C1': 'trai', 'C2': 'vinh', 'C3': 'pho', 'C4': 'vinh', 'C5': 'vinh'}
NGUONG = {'pho': 50.0, 'vinh': 40.0, 'trai': 40.0}

def td_of(opt):
    out = []
    for k, t in (opt.get('td') or V7B_TD.get(opt['shot'], [])):
        d = dict(TD[k]); d['k'] = k
        if t: d['t'] = t
        out.append(d)
    return out

def run(ep, nhan, root, every, only):
    import yaml
    E = yaml.safe_load(open(ep)); d = OUT / f'bocuc-{nhan}'; d.mkdir(parents=True, exist_ok=True)
    for key, h in E['heroes'].items():
        o = h['opt']; sh = o['shot']
        if only and sh not in only: continue
        cmd = ['node', str(ROOT / 'design/k2v/v7c/do_bocuc.js'), '--root', root, '--opt', json.dumps(o), '--every', str(every), '--td', json.dumps(td_of(o)), '--out', str(d / f'{sh}.json')]
        if os.environ.get('V7C_PNG'): cmd += ['--png', f"{os.environ['V7C_PNG']}/{nhan}-{sh}"]
        r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, K2TL_CACHE=os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache')))
        print(sh, r.stdout.strip()[-300:], r.stderr.strip()[-300:] if r.returncode else '', flush=True)
        if r.returncode == 0:
            j = json.loads((d / f'{sh}.json').read_text()); j['loai'] = o.get('loai') or V7B_LOAI.get(sh, 'pho'); j['dur'] = h['dur']; j['key'] = key
            (d / f'{sh}.json').write_text(json.dumps(j))

def tom(nhan):
    d = OUT / f'bocuc-{nhan}'; rows = []
    for p in sorted(d.glob('*.json')):
        j = json.loads(p.read_text()); F = j['frames']; n = len(F); loai = j.get('loai', 'pho'); ng = NGUONG[loai]
        avg = lambda f: sum(f(r) for r in F) / n
        td_ok = [any(x.get('dat') for x in r['td']) for r in F]; td_w = [max([x.get('rong_pct', 0) for x in r['td'] if x.get('thay')] or [0]) for r in F]
        cao = [r['agl'] >= 120 or r['xuong'] >= 15 for r in F]; thap = [r['agl'] < 50 for r in F]
        fl = lambda r: 12.0 / math.tan(math.radians(r['fov']) / 2)   # tiêu cự tương đương 35 mm theo fov dọc (khung 24 mm)
        rows.append(dict(shot=p.stem, loai=loai, nguong=ng, n=n, dur=j.get('dur'), noi_dung=round(avg(lambda r: r['noi_dung']), 1), noi_dung_min=round(min(r['noi_dung'] for r in F), 1),
                         dat_noi_dung_pct=round(100 * sum(r['noi_dung'] >= ng for r in F) / n), trong=round(avg(lambda r: r['trong']), 1), dat_trong_pct=round(100 * sum(r['trong'] <= 100 / 3 for r in F) / n),
                         troi=round(avg(lambda r: r['pct']['troi']), 1), nuoc=round(avg(lambda r: r['pct']['nuoc']), 1), da=round(avg(lambda r: r['pct']['da']), 1),
                         khoi=round(avg(lambda r: sum(r['pct'][k] for k in ('nha', 'trai', 'congsu', 'tau', 'pin', 'nguoi', 'co'))), 1),
                         td_dat_pct=round(100 * sum(td_ok) / n), td_rong=round(sum(td_w) / n, 1), agl=round(avg(lambda r: r['agl'])), agl_min=round(min(r['agl'] for r in F)), xuong=round(avg(lambda r: r['xuong']), 1),
                         fov=round(avg(lambda r: r['fov']), 1), tieu_cu_mm=round(avg(fl)), cao_pct=round(100 * sum(cao) / n), thap_pct=round(100 * sum(thap) / n)))
    (OUT / f'bocuc-{nhan}.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    return rows

def bang(nhans):
    R = {n: {r['shot']: r for r in tom(n)} for n in nhans}
    print('| Shot | Loại (ngưỡng) | ' + ' | '.join(f'{n}: nội dung % (min) · khung đạt · trống % · tiêu điểm đạt (rộng %) · AGL · nhìn xuống · tiêu cự' for n in nhans) + ' |')
    print('|---|---|' + '---|' * len(nhans))
    shots = sorted(set().union(*[set(x) for x in R.values()]), key=lambda s: ('H' not in s, s))
    for s in shots:
        cells = []
        for n in nhans:
            r = R[n].get(s)
            cells.append('—' if not r else f"{r['noi_dung']} ({r['noi_dung_min']}) · {r['dat_noi_dung_pct']} % · {r['trong']} · {r['td_dat_pct']} % ({r['td_rong']}) · {r['agl']} m · {r['xuong']}° · {r['tieu_cu_mm']} mm")
        r0 = next(R[n][s] for n in nhans if s in R[n]); print(f"| {s} | {r0['loai']} (≥ {r0['nguong']:.0f}) | " + ' | '.join(cells) + ' |')

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'run':
        root = a[a.index('--root') + 1] if '--root' in a else str(ROOT); ev = int(a[a.index('--every') + 1]) if '--every' in a else 12
        only = a[a.index('--shots') + 1].split(',') if '--shots' in a else None
        run(a[1], a[2], root, ev, only)
    else: bang(a[1:])
