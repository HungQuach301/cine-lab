#!/opt/cine/bin/python
"""BAN-CUOI-T3 (việc 9) · TỰ ĐO bản cuối (ghi số, KHÔNG tự chấm đạt) — mở rộng scripts/k2tl/anim_do.py:
  thời lượng · LUFS/LRA/đỉnh thật (ebur128) · bão hoà/colorfulness/chi tiết TRUNG VỊ (1 khung/2 s, 640×360, cắt y 60–300 — cùng công thức anim_do.py)
  · ΔE76 trung bình giữa hai shot kề (Lab trung bình 0,5 s cuối shot trước ↔ 0,5 s đầu shot sau, 320×180) · % minh hoạ AI · % Cycles GPU · cắt/phút (shot / có góc trong shot / có bước năm)
  cuoi_do.py <master.mp4> <ra.json>"""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np
REPO = Path(__file__).resolve().parents[2]; EPD = REPO / 'channel-k2/k2c-t3-01/cuoi'
M, OUT = sys.argv[1], sys.argv[2]
LOG = json.loads((EPD / 'log-shot.json').read_text()); S = [x for x in LOG if 'kieu_khung' in x]; B = json.loads((EPD / 'bang-shot.json').read_text())
r = {}
r['thoi_luong_s'] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', M], capture_output=True, text=True).stdout)
e = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', M, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr.split('Summary:')[-1]
g = lambda k: float(e.split(k)[1].split()[0]); r['lufs'] = g('I:'); r['lra'] = g('LRA:'); r['dinh_that_dbtp'] = g('Peak:')
T = r['thoi_luong_s']; n = len(S); nc = sum(len(x.get('cat_trong_shot') or []) for x in S); nb = sum(x['tl_buoc_n'] for x in S)
r['cat_phut'] = dict(shot=round(n / (T / 60), 2), co_goc_trong_shot=round((n + nc) / (T / 60), 2), co_buoc_nam=round((n + nc + nb) / (T / 60), 2), so_shot=n, so_cat_goc=nc, so_buoc_nam=nb)
mh = sum(m['t1'] - m['t0'] for x in S for m in x.get('minh_hoa') or [] if x.get('ai_image'))
gpu = sum(x['lan']['dur'] for x in S if x.get('lan')) + sum(x['dur'] for x in S if x['ma'] == 'H2T')
r['ty_le'] = dict(minh_hoa_ai_s=round(mh, 2), minh_hoa_ai_pct=round(100 * mh / T, 2), cycles_gpu_s=round(gpu, 2), cycles_gpu_pct=round(100 * gpu / T, 2))
tmp = Path('/var/tmp/cine-out/k2c-t3-cuoi/do-khung'); tmp.mkdir(parents=True, exist_ok=True)
for p in tmp.glob('*.png'): p.unlink()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', M, '-vf', 'fps=0.5,scale=640:360:flags=area', str(tmp / '%05d.png')], check=True)
sat, col, det = [], [], []
for p in sorted(tmp.glob('*.png')):
    im = cv2.imread(str(p))[60:300]; sat.append(float(np.median(cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[..., 1]) / 255))
    b, gg, rr = [im[..., k].astype(np.float64) for k in range(3)]; rg, yb = rr - gg, 0.5 * (rr + gg) - b
    col.append(float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)))
    det.append(float(np.abs(cv2.Laplacian(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float64), cv2.CV_64F, ksize=1)).mean()))
r['mau'] = dict(khung=len(sat), bao_hoa_trung_vi=round(float(np.median(sat)), 3), colorfulness_trung_vi=round(float(np.median(col)), 1), chi_tiet_trung_vi=round(float(np.median(det)), 2),
                cach_do='640×360 INTER_AREA, cắt y 60–300, 1 khung/2 s trên master 1080p (có bộ đếm + thẻ chương)')
def lab_tb(t0, t1):
    fr = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{t1 - t0:.3f}', '-i', M, '-vf', 'scale=320:180:flags=area', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
    a = np.frombuffer(fr, np.uint8).reshape(-1, 180, 320, 3)
    return np.mean([cv2.cvtColor(x, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float64) * [100 / 255, 1, 1] - [0, 128, 128] for x in a], axis=(0, 1))
cap = []
for a, b in zip(B, B[1:]):
    la, lb = lab_tb(max(0, a['t1'] - 0.5), a['t1'] - 0.04), lab_tb(b['t0'] + 0.04, b['t0'] + 0.5); cap.append(dict(tu=a['ma'], toi=b['ma'], dE76=round(float(np.linalg.norm(la - lb)), 2)))
d = [x['dE76'] for x in cap]
r['dE_shot_ke'] = dict(trung_binh=round(float(np.mean(d)), 2), trung_vi=round(float(np.median(d)), 2), lon_nhat=max(cap, key=lambda x: x['dE76']), so_cap=len(cap), cap=cap,
                       cach_do='ΔE76 giữa Lab trung bình (0,5 s cuối shot trước | 0,5 s đầu shot sau), 320×180, trên master đã áp LUT')
json.dump(r, open(OUT, 'w'), ensure_ascii=False, indent=1); print(json.dumps({k: v for k, v in r.items() if k != 'dE_shot_ke'}, ensure_ascii=False, indent=1)); print('dE', r['dE_shot_ke']['trung_binh'], r['dE_shot_ke']['lon_nhat'])
