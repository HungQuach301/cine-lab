#!/opt/cine/bin/python
"""LOOK-T4 · ĐO cú máy clip 8 s (theo §19 đề xuất: quay ≤ 3°/s; tiêu điểm trôi ≤ 1,5 % khung/s) + ghép mp4 640×360 có LUT kênh (biến thể A).
  look_clip.py <thư mục khung (render_look.js)> <ra.mp4> <ra đo.json> --hero E,N,h"""
import json, os, subprocess, sys
import numpy as np
D, MP4, DO = sys.argv[1:4]; hero = [float(v) for v in sys.argv[sys.argv.index('--hero') + 1].split(',')]
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L = json.load(open(os.path.join(D, 'log.json'))); F = sorted(L['frames'], key=lambda r: r['f']); fps = L['shot'].get('fps', 24)
def fwd(r): V = np.array(r['view']).reshape(4, 4).T; return -V[2, :3]          # hướng nhìn (thế giới)
def proj(r):
    V = np.array(r['view']).reshape(4, 4).T; P = np.array(r['proj']).reshape(4, 4).T; p = P @ V @ np.array([hero[0] - 532000, hero[2], -(hero[1] - 180800), 1.0]); n = p[:3] / p[3]
    return np.array([(n[0] + 1) / 2, (1 - n[1]) / 2])
ang = [float(np.degrees(np.arccos(np.clip(fwd(a) @ fwd(b), -1, 1)))) * fps for a, b in zip(F, F[1:])]
pos = [np.array(r['cam']['p']) for r in F]; v = [float(np.linalg.norm(b - a)) * fps for a, b in zip(pos, pos[1:])]
hp = [proj(r) for r in F]; dr = [float(np.linalg.norm(b - a)) * 100 * fps for a, b in zip(hp, hp[1:])]
# phương vị quanh tiêu điểm (cú vòng cung): góc của máy nhìn từ tiêu điểm
az = [float(np.degrees(np.arctan2(p[1] - hero[1], p[0] - hero[0]))) for p in pos]; vaz = [abs(b - a) * fps for a, b in zip(az, az[1:])]
out = {'khung': len(F), 's_khung_dung': L['s_per_frame'], 'quay_huong_nhin_do_s': {'tb': round(np.mean(ang), 2), 'max': round(max(ang), 2)}, 'vong_cung_quanh_tieu_diem_do_s': {'tb': round(np.mean(vaz), 2), 'max': round(max(vaz), 2)},
       'tieu_diem_troi_pct_khung_s': {'tb': round(np.mean(dr), 2), 'max': round(max(dr), 2)}, 'may_m_s': {'tb': round(np.mean(v), 1), 'max': round(max(v), 1)},
       'tieu_diem_dau_cuoi_pct': [[round(x * 100, 1) for x in hp[0]], [round(x * 100, 1) for x in hp[-1]]], 'cu_may': L['shot'].get('cu_may')}
lut = os.path.join(REPO, 'channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube')
for crf in (22, 25, 28, 31):
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-framerate', str(fps), '-i', os.path.join(D, '%05d.jpg'), '-vf', f"lut3d=file='{lut}':interp=tetrahedral",
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', MP4], check=True)
    if os.path.getsize(MP4) <= 5_000_000: break
out['mp4_MB'] = round(os.path.getsize(MP4) / 1e6, 2); out['crf'] = crf
json.dump(out, open(DO, 'w'), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False))
