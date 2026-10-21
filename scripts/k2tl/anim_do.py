#!/opt/cine/bin/python
"""ANIMATIC-T3 việc 8 · TỰ ĐO (ghi số, KHÔNG tự chấm đạt) trên master 960×540 + đặc tả:
  thời lượng (ffprobe) · LUFS/LRA/đỉnh thật (ebur128) · cắt/phút có/không tính bước năm (đặc tả) · % góc cao có thời gian chạy · % lướt thấp (khai + theo khoá máy AGL < 50 m)
  · bão hoà / colorfulness / chi tiết TRUNG VỊ trên khung 1/2 s thu 640×360, cắt y 60–300 (cả bề ngang) — cùng công thức scripts/k2tl/measure_look.py
  anim_do.py <master.mp4> <ra.json>"""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np
REPO = Path(__file__).resolve().parents[2]; EPD = REPO / 'channel-k2/k2c-t3-01/animatic'
M, OUT = sys.argv[1], sys.argv[2]
LOG = json.loads((EPD / 'log-shot.json').read_text()); S = [x for x in LOG if 'kieu_khung' in x]
r = {}
r['thoi_luong_s'] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', M], capture_output=True, text=True).stdout)
e = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', M, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr.split('Summary:')[-1]
g = lambda k: float(e.split(k)[1].split()[0])
r['lufs'] = g('I:'); r['lra'] = g('LRA:'); r['dinh_that_dbtp'] = g('Peak:')
T = 745.0; n = len(S); nb = sum(x['tl_buoc_n'] for x in S); nl = sum(1 for x in S if x.get('lan'))
r['cat_phut'] = dict(shot=round(n / (T / 60), 2), shot_va_cu_lan=round((n + nl) / (T / 60), 2), tinh_buoc_nam=round((n + nl + nb) / (T / 60), 2), so_shot=n, so_buoc_nam=nb, the_pp_ngoai=16.0)
cao = sum(x['dur'] for x in S if x['kieu_khung'] in ('lai', 'lai+lan') and x['goc'] == 'cao')
chat = sum(x['dur'] for x in S if x['kieu_khung'] == 'chat'); neo = sum(x['dur'] for x in S if x.get('khung_neo')); dem = sum(x['dur'] for x in S if x['kieu_khung'] == 'dem')
lan = sum(x['lan']['dur'] for x in S if x.get('lan'))
thap = sum((x['luot_thap'][1] - x['luot_thap'][0]) for x in S if x.get('luot_thap')) + neo
r['goc'] = dict(goc_cao_lai_co_tl_pct=round(100 * (cao - lan) / T, 1), goc_cao_gom_khung_chat_cao_pct=round(100 * (cao - lan + sum(x['dur'] for x in S if x['kieu_khung'] == 'chat' and min(x['agl_m']) >= 120)) / T, 1),
                luot_thap_pct=round(100 * thap / T, 1), khung_neo_pct=round(100 * neo / T, 1), cu_lan_giu_cho_pct=round(100 * lan / T, 1), dem_pct=round(100 * dem / T, 1), khung_chat_pct=round(100 * chat / T, 1),
                ghi='góc cao = kiểu lai (máy ≥ 120 m hoặc nhìn xuống ≥ 12°) có thời gian chạy, trừ đoạn cú lặn giữ chỗ; lướt thấp = khai luot_thap + khung neo (TL-2); cú lặn không tính vào TL-2 (§14.3)')
# màu/chi tiết: 1 khung / 2 s
tmp = Path('/var/tmp/cine-out/k2c-t3-anim/do-khung'); tmp.mkdir(parents=True, exist_ok=True)
for p in tmp.glob('*.png'): p.unlink()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', M, '-vf', 'fps=0.5,scale=640:360:flags=area', str(tmp / '%05d.png')], check=True)
sat, col, det = [], [], []
for p in sorted(tmp.glob('*.png')):
    im = cv2.imread(str(p))[60:300]; hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); sat.append(float(np.median(hsv[..., 1]) / 255))
    b, gg, rr = [im[..., k].astype(np.float64) for k in range(3)]; rg, yb = rr - gg, 0.5 * (rr + gg) - b
    col.append(float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)))
    y = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float64); det.append(float(np.abs(cv2.Laplacian(y, cv2.CV_64F, ksize=1)).mean()))
r['mau'] = dict(khung=len(sat), bao_hoa_trung_vi=round(float(np.median(sat)), 3), colorfulness_trung_vi=round(float(np.median(col)), 1), chi_tiet_trung_vi=round(float(np.median(det)), 2),
                cach_do='640×360 INTER_AREA, cắt y 60–300 cả bề ngang, 1 khung/2 s trên master 960×540 (có bộ đếm + thẻ chương)')
json.dump(r, open(OUT, 'w'), ensure_ascii=False, indent=1); print(json.dumps(r, ensure_ascii=False, indent=1))
