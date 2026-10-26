#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · k2check 1.17.8 trên MỘT tấm E (N2P-E + N2P-1…5) — episode/timeline/log shot tối thiểu theo khuôn THU-B (`thu-b/kiem/*`) + khai K1178 §4.
Chỉ CHẠY checks/ll/k2check.py (không đọc mã checks/). Mức G2 (`animatic: false`) để thấy đúng cấp Chặn.
  kiem_e_bc.py <khung> <tag> <shot> <dem 0|1> [--video <ghep.mp4> <render.mp4> <matna-640.png>] [--vision]"""
import json, os, subprocess, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BCE = os.path.join(REPO, 'channel-k2/k2c-t4-02/ban-cuoi/e')
a = sys.argv[1:]; k, tag, shot, dem = a[0], a[1], a[2], a[3] == '1'
d = f'{BCE}/kiem/{k}-{tag}'; os.makedirs(d, exist_ok=True); T = f'../../tam/{k}'
toa = json.load(open(f'{BCE}/tam/{k}/toa.json'))
tam = dict(id=f'{k}-{tag}', shot=shot, render=f'{T}/render.png', ghep=f'{T}/{tag}/ghep.png', mat_na=f'{T}/matna.png', nam=2026, anh_tinh=True,
           n2p_toan_khung_hien_dai=True, nam_min=2020, cu_may='CODINH', dem=dem, mat_na_ct=f'{T}/mat_na_ct.png',
           toa_co_ten=[dict(ten=t['ten'], mau=t['mau']) for t in toa], noi='London')
n2p = dict(noi='London', t4=True, tam=[tam])
if '--video' in a:
    i = a.index('--video'); g, r, m = a[i + 1:i + 4]
    n2p['video'] = [dict(shot=shot, ghep=g, render=r, mat_na=m, chuyen_tam=[], n2p_toan_khung_hien_dai=True, nam=2026, cu_may='CODINH')]
dur = 3.0
ep = dict(id=f'ban-cuoi-t4-a-E-{k}-{tag}', title='BAN-CUOI-T4-A thử E (không phải tập)', brand='MOVING PARTS', channel='k2', khung_sach=True, kenh2_tu_t4=True, animatic=False,
          out=f'/var/tmp/bc/k2c/{k}-{tag}', segments=[dict(id='s0', dur=dur, shots=[dict(id=shot, at=0.0, tpl='scene3d')])], n2p=n2p, log_shot='log-shot.json')
import yaml
yaml.safe_dump(ep, open(f'{d}/episode.yaml', 'w'), allow_unicode=True, sort_keys=False)
json.dump(dict(id=ep['id'], title=None, music=[], segments=[dict(id='s0', dur=dur, t0=0.0, t1=dur, frames=72, speech=[], sfx=[], shots=[dict(id=shot, at=0.0, tpl='scene3d', t0=0.0, t1=dur)])],
               heroes={}, tong_s=dur, tong_khung=72), open(f'{d}/timeline.json', 'w'))
json.dump([dict(shot=shot, t0=0.0, t1=dur, dur=dur, chuong='thu-e', goc='cao', tl=True, cu_may='CODINH', lop={'N2P': dur}, ai_nen=True, vung='bankside')], open(f'{d}/log-shot.json', 'w'), ensure_ascii=False, indent=1)
cmd = [sys.executable, 'checks/ll/k2check.py', f'{d}/episode.yaml', '--tl', f'{d}/timeline.json', '--no-asr', '--cap'] + (['--n2p-vision'] if '--vision' in a else [])
r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
open(f'{d}/k2check.md', 'w').write(r.stdout + ('\n\n<!-- stderr -->\n' + r.stderr[-3000:] if r.returncode not in (0, 1) else ''))
print('rc', r.returncode); print('\n'.join(l for l in r.stdout.splitlines() if 'N2P' in l or 'BE-MAT' in l)[:4000])
