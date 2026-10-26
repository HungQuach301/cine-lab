#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · việc 3 (B) — k2check 1.17.8 BE-MAT-NHA + N2P trên tấm B (AI phủ bề mặt nhà thường ≥ 4 px/m, cách tỉ số bóng máy cố định) — khuôn THU-B `thu-b/kiem/*-tiso`.
Chép tệp tấm từ $THUB/bp/<k>/ vào channel-k2/k2c-t4-02/ban-cuoi/b/tam/<k>/ (PNG ≤ 5 MB); video kiểm không mất NGOÀI git (/var/tmp/bc/), SHA ghi ở video-sha.txt.
Chỉ CHẠY checks/ll/k2check.py.   kiem_b_bc.py <k> <năm> <shot> [--vision] [--luot l2]"""
import hashlib, json, os, shutil, subprocess, sys
import yaml
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
THUB = '/var/tmp/bc/thub'; B = f'{REPO}/channel-k2/k2c-t4-02/ban-cuoi/b'; LUT = f'{REPO}/channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube'
k, nam, shot = sys.argv[1], int(sys.argv[2]), sys.argv[3]; LT = sys.argv[sys.argv.index('--luot') + 1] if '--luot' in sys.argv else 'l1'; S = f'{THUB}/bp/{k}'; T = f'{B}/tam/{k}'; os.makedirs(f'{T}/{LT}', exist_ok=True)
for f in ('render.png', 'matna.png', 'mat_na_nha.png', 'mat_na_mat.png', 'bong.png', 'nha.json', 'nha-chi-tiet.json', 'prep.json', 'px4.json', 'do-duoc.png'): shutil.copy(f'{S}/{f}', f'{T}/{f}')
for f in ('ghep.png', 'ghep.json'): shutil.copy(f'{S}/{LT}/{f}', f'{T}/{LT}/{f}')
# video render đối chứng (không mất, LUT) từ khung timelapse
src = f'/var/tmp/bc/r/tl-{k}-v2'; vr = f'/var/tmp/bc/{k}-tl-render.mp4'; vg = f'{S}/{LT}/tl-chieu_tiso.mp4'
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-framerate', '24', '-i', f'{src}/%05d.png', '-vf', f"lut3d=file='{LUT}':interp=tetrahedral", '-c:v', 'libx264', '-preset', 'slow', '-crf', '0', '-pix_fmt', 'yuv444p', vr], check=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
open(f'{T}/video-sha-{LT}.txt', 'w').write(f'{sha(vg)}  {os.path.basename(vg)} (ngoài git: {vg})\n{sha(vr)}  {os.path.basename(vr)} (ngoài git: {vr})\n')
d = f'{B}/kiem/{k}-{LT}'; os.makedirs(d, exist_ok=True); R = os.path.relpath(T, d)
tam = dict(id=f'{k}-{LT}-tiso', shot=shot, render=f'{R}/render.png', ghep=f'{R}/{LT}/ghep.png', mat_na=f'{R}/matna.png', nam=nam, anh_tinh=True, be_mat_nha_ai=True,
           mat_na_nha=f'{R}/mat_na_nha.png', mat_na_mat=f'{R}/mat_na_mat.png', bong=f'{R}/bong.png', nha=f'{R}/nha.json', nen_ai=False,
           be_mat_nha_video=dict(ghep=vg, render=vr, cach='chieu_3d', tam=f'{R}/{LT}/ghep.png'))
ep = dict(id=f'ban-cuoi-t4-a-B-{k}', title='BAN-CUOI-T4-A thử B (không phải tập)', brand='MOVING PARTS', channel='k2', khung_sach=True, kenh2_tu_t4=True, animatic=False,
          be_mat_nha_px_m_min=4, be_mat_nha_y_san_nhap=0.01, out=f'/var/tmp/bc/k2c/{k}-{LT}', segments=[dict(id='s0', dur=3.0, shots=[dict(id=shot, at=0.0, tpl='scene3d')])],
          n2p=dict(noi='London', t4=True, tam=[tam]), log_shot='log-shot.json')
yaml.safe_dump(ep, open(f'{d}/episode.yaml', 'w'), allow_unicode=True, sort_keys=False)
json.dump(dict(id=ep['id'], title=None, music=[], segments=[dict(id='s0', dur=3.0, t0=0.0, t1=3.0, frames=72, speech=[], sfx=[], shots=[dict(id=shot, at=0.0, tpl='scene3d', t0=0.0, t1=3.0)])], heroes={}, tong_s=3.0, tong_khung=72), open(f'{d}/timeline.json', 'w'))
json.dump([dict(shot=shot, t0=0.0, t1=3.0, dur=3.0, chuong='thu-b', goc='cao', tl=True, cu_may='CODINH', lop={'N2P': 3.0}, ai_nen=False, be_mat_nha_ai=True, vung='thu_b')], open(f'{d}/log-shot.json', 'w'), ensure_ascii=False, indent=1)
r = subprocess.run([sys.executable, 'checks/ll/k2check.py', f'{d}/episode.yaml', '--tl', f'{d}/timeline.json', '--no-asr', '--cap'] + (['--n2p-vision'] if '--vision' in sys.argv else []), cwd=REPO, capture_output=True, text=True)
open(f'{d}/k2check.md', 'w').write(r.stdout + ('\n\n<!-- stderr -->\n' + r.stderr[-3000:] if r.returncode not in (0, 1) else '')); print('rc', r.returncode)
