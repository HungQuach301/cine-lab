#!/opt/cine/bin/python
"""BAN-CUOI-T4-B2a · k2check 1.17.9 trên thử E của M01 (N2P-E + N2P-1…5) — khuôn kiem_e_bc.py (phiên A) + khai K1179 §4:
tấm `nuoc_ai: true` (KHÔNG khai `duyet_chu_du_an`: tấm chưa được chủ dự án duyệt — K1179-D6 duyệt từng tấm → (u) Chặn là đúng trạng thái thật),
`toa_co_ten[]` có `loai` (thap + dinh_odn_m · lich_su + nguon_lich_su · mai_vom), video `day_2d: {kieu: day, toc_do_pct_s: 1.0}` (đẩy một phép cho cả khung, máy 3D CODINH).
Chỉ CHẠY checks/ll/k2check.py (không đọc mã checks/). Mức G2 (`animatic: false`).
  kiem_e_m01.py a [--vision]          → e/kiem/E-M01-a/   (tấm tĩnh)
  kiem_e_m01.py b [--vision] [--render day|codinh]   → e/kiem/E-M01-b/   (tấm + video đẩy 2D 640×360; render đối chứng: đẩy cùng phép | CODINH không đẩy)"""
import json, os, subprocess, sys, yaml
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BCE = os.path.join(REPO, 'channel-k2/k2c-t4-02/ban-cuoi/e'); VO = '/var/tmp/bc/e-m01'
a = sys.argv[1:]; ph = a[0]; rd = a[a.index('--render') + 1] if '--render' in a else 'day'
d = f'{BCE}/kiem/E-M01-{ph}' + ('' if ph == 'a' or rd == 'day' else f'-{rd}'); os.makedirs(d, exist_ok=True); T = '../../tam/E-M01'
toa = json.load(open(f'{BCE}/tam/E-M01/toa-thap.json'))
khai = []
for t in toa:
    x = dict(ten=t['ten'], mau=t['mau'], loai=t['loai'])
    if t['loai'] == 'thap': x['dinh_odn_m'] = t['dinh_odn_m']
    if t.get('nguon_lich_su'): x['nguon_lich_su'] = t['nguon_lich_su']
    khai.append(x)
tam = dict(id='E-M01-l2-thap-bo_dat', shot='M01', render=f'{T}/render.png', ghep=f'{T}/l2-thap-bo_dat/ghep.png', mat_na=f'{T}/matna-thap.png', nam=2026, anh_tinh=True,
           n2p_toan_khung_hien_dai=True, nam_min=2020, cu_may='CODINH', dem=False, mat_na_ct=f'{T}/mat_na_ct-thap.png', toa_co_ten=khai, noi='London', nuoc_ai=True)
n2p = dict(noi='London', t4=True, tam=[tam])
dur = 17.875 if ph == 'b' else 3.0
if ph == 'b':
    n2p['video'] = [dict(shot='M01', ghep=f'{VO}/M01-E-ghep-640.mp4', render=f'{VO}/M01-E-render-{rd}-640.mp4', mat_na=f'{VO}/matna-640.png', chuyen_tam=[],
                         n2p_toan_khung_hien_dai=True, nam=2026, cu_may='CODINH', day_2d=dict(kieu='day', toc_do_pct_s=1.0))]
ep = dict(id=f'ban-cuoi-t4-b2a-E-M01-{ph}', title='BAN-CUOI-T4-B2a thử E M01 (không phải tập)', brand='MOVING PARTS', channel='k2', khung_sach=True, kenh2_tu_t4=True, animatic=False,
          out=f'/var/tmp/bc/k2c/E-M01-{ph}-{rd}', segments=[dict(id='s0', dur=dur, shots=[dict(id='M01', at=0.0, tpl='scene3d')])], n2p=n2p, log_shot='log-shot.json')
yaml.safe_dump(ep, open(f'{d}/episode.yaml', 'w'), allow_unicode=True, sort_keys=False)
nf = int(round(dur * 24))
json.dump(dict(id=ep['id'], title=None, music=[], segments=[dict(id='s0', dur=dur, t0=0.0, t1=dur, frames=nf, speech=[], sfx=[], shots=[dict(id='M01', at=0.0, tpl='scene3d', t0=0.0, t1=dur)])],
               heroes={}, tong_s=dur, tong_khung=nf), open(f'{d}/timeline.json', 'w'))
json.dump([dict(shot='M01', t0=0.0, t1=dur, dur=dur, chuong='thu-e', goc='cao', tl=True, cu_may='CODINH', lop={'N2P': dur}, ai_nen=True, vung='bankside_city')], open(f'{d}/log-shot.json', 'w'), ensure_ascii=False, indent=1)
cmd = [sys.executable, 'checks/ll/k2check.py', f'{d}/episode.yaml', '--tl', f'{d}/timeline.json', '--no-asr', '--cap'] + (['--n2p-vision'] if '--vision' in a else [])
r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
open(f'{d}/k2check.md', 'w').write(r.stdout + ('\n\n<!-- stderr -->\n' + r.stderr[-3000:] if r.returncode not in (0, 1) else ''))
print('rc', r.returncode); print('\n'.join(l[:1500] for l in r.stdout.splitlines() if 'N2P' in l or 'BE-MAT' in l)[:9000])
