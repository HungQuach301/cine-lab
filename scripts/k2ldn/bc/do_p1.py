#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · việc 2 (C3 c): đo điểm đứng P1 — hiện tại / dời tây 60 m / 80 m (giữ hướng nhìn, fov 36°).
Mái vòm: mask 2 mã công trình St Paul's mới (chỉ số 4–5 = 1708.5/1708.8: tambour + lantern; thiếu → 1–5) → x % tâm theo bề ngang, y % đỉnh.
Lửa (M03): điểm ảnh render (đã LUT) R ≥ 200, G 80–220, B ≤ 120 và R − B ≥ 110 → bề ngang lửa [x5 %, x95 %], % điểm lửa sát mép phải/trái (≤ 3 % bề ngang).
Ra reports/ban-cuoi-t4-a/p1/do-p1.json + to-p1.jpg (3 × 3 ô).   do_p1.py"""
import json, os, subprocess
import cv2, numpy as np
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
R = '/var/tmp/bc/r'; O = os.path.join(REPO, 'reports/ban-cuoi-t4-a/p1'); os.makedirs(O, exist_ok=True)
LUT = os.path.join(REPO, 'channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube')
res = {}; rows = []
for k in ('P1-M03', 'P1-H4-05', 'P1-M01'):
    row = []
    for dx in (0, 60, 80):
        n = f'{k}-w{dx}'; tmp = f'/var/tmp/bc/{n}-lut.png'
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', f'{R}/{n}/00000.png', '-vf', f"lut3d=file='{LUT}':interp=tetrahedral", tmp], check=True)
        im = cv2.imread(tmp); H, W = im.shape[:2]; M2 = cv2.imread(f'{R}/{n}-m2/00000.png')[:, :, ::-1].astype(int)
        base = (M2[..., 1] == 0) & (M2[..., 2] == 200)
        dome = base & np.isin(M2[..., 0], [80, 100])
        if dome.sum() < 30: dome = base & np.isin(M2[..., 0], [20, 40, 60, 80, 100])
        ys, xs = np.nonzero(dome); r = dict(dome_px=int(dome.sum()))
        if len(xs): r.update(dome_x_pct=round(100 * float(xs.mean()) / W, 1), dome_dinh_y_pct=round(100 * float(ys.min()) / H, 1))
        b, g, rr = im[..., 0].astype(int), im[..., 1].astype(int), im[..., 2].astype(int)
        fire = (rr >= 200) & (g >= 80) & (g <= 220) & (b <= 120) & (rr - b >= 110)
        if fire.sum() > 200:
            fy, fx = np.nonzero(fire); m = int(0.03 * W)
            r.update(lua_px_pct=round(100 * float(fire.mean()), 2), lua_x5=round(100 * float(np.percentile(fx, 5)) / W, 1), lua_x95=round(100 * float(np.percentile(fx, 95)) / W, 1),
                     lua_mep_phai_pct=round(100 * float((fx >= W - m).mean()), 2), lua_mep_trai_pct=round(100 * float((fx < m).mean()), 2))
        res[n] = r
        t = cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
        if len(xs): cv2.line(t, (int(xs.mean() * 960 / W), 0), (int(xs.mean() * 960 / W), 539), (0, 255, 255), 1)
        for x in (320, 640): cv2.line(t, (x, 0), (x, 539), (255, 255, 255), 1)
        lb = f"{n}  vom x {r.get('dome_x_pct')}%" + (f"  lua {r['lua_x5']}-{r['lua_x95']}% mep phai {r['lua_mep_phai_pct']}%" if 'lua_x5' in r else '')
        cv2.putText(t, lb, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4, cv2.LINE_AA); cv2.putText(t, lb, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        row.append(t)
    rows.append(np.hstack(row))
json.dump(res, open(f'{O}/do-p1.json', 'w'), ensure_ascii=False, indent=1)
cv2.imwrite(f'{O}/to-p1.jpg', np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85]); print(json.dumps(res, ensure_ascii=False, indent=0))
