"""V5b-2d · ĐO 6 KHUNG 6 LOẠI CẢNH (sau v5b2d_khung.sh) và so với khung sạch V5b-2c (reports/v5b2c/khung/v0-*.jpg):
  · cách điều phối (measure_dp.py: 640×360, y 60–300, sat/colorful/FIND_EDGES, cháy sáng) trên khung SẠCH và khung CÓ CHỮ (ảnh PNG đổi từ JPG dựng — không nén lại);
  · mặt nạ nội dung (render.js --maskonly: content/fabric/nước/đất tự nhiên/trời %);
  · cỡ px của khối quân/người/tàu ở 1080p: chiếu chiều cao thật (người 1,75 m; tàu: thân 6 m) theo máy của khung (nhật ký --campath) — chỉ vật trong khung nhìn;
  · lửa đỏ %: khác biệt khung bờ+chiến sự có/không lửa (cùng máy), điểm đổi > 30 mức VÀ sắc đỏ–cam (R > G + 35, R > B + 60) — % khung 1080p.
Dùng: v5b2d_do.py --khung <thư mục v5b2d_khung.sh> --cu reports/v5b2c/khung --out <ra.json>"""
import argparse, glob, json, math, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from measure_dp import measure  # noqa: E402

LOAI = {1: ('vay_ham', 'eo1782', 48, 'v0-1-vay-ham.jpg'), 2: ('cang_bo', 'vinh1782', 72, 'v0-2-cang-bo.jpg'), 3: ('pho_day', 'pho1782', 96, 'v0-3-pho-day.jpg'),
        4: ('hero', 'vinh1782', 192, 'v0-4-hero.jpg'), 5: ('toan_canh', 'toan1782', 72, 'v0-5-toan-canh.jpg'), 6: ('bo_chien_su', 'bo1782', 72, 'v0-6-bien-chien-su.jpg')}


def proj_px(cam, pts, h, W=1920, H=1080, box=None):
    """box = (rộng, sâu) m: đo chiều cao HÌNH CHIẾU của khối (hộp rộng × sâu × h, 8 góc) thay vì một người — 'mỗi khối ≥ 6 px cao'."""
    if box:
        out = []
        for q in pts:
            cs = [[q[0] + dx, q[1] + dy, q[2] + dz] for dx in (-box[0] / 2, box[0] / 2) for dz in (-box[1] / 2, box[1] / 2) for dy in (0, h)]
            r = proj_px_raw(cam, cs, W, H)
            if r: out.append(dict(px=max(y for _, y, _ in r) - min(y for _, y, _ in r), d=r[0][2]))
        return out
    return [dict(px=x['px'], d=x['d']) for x in proj_px_pt(cam, pts, h, W, H)]


def proj_px_raw(cam, pts, W, H):
    p = np.array(cam['p'], float); l = np.array(cam['l'], float); f = l - p; f /= np.linalg.norm(f); r = np.cross(f, [0, 1.0, 0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    fy = H / 2 / math.tan(math.radians(cam['fov']) / 2); out = []
    for q in pts:
        v = np.array(q, float) - p; d = v @ f
        if d <= 1: return None
        out.append((W / 2 + fy * (v @ r) / d, H / 2 - fy * (v @ u) / d, float(np.hypot(v[0], v[2]))))
    cx = np.mean([o[0] for o in out]); cy = np.mean([o[1] for o in out])
    return out if (0 <= cx < W and 0 <= cy < H) else None


def proj_px_pt(cam, pts, h, W=1920, H=1080):
    p = np.array([cam['p'][0], cam['p'][1], cam['p'][2]], float); l = np.array([cam['l'][0], cam['l'][1], cam['l'][2]], float)
    f = l - p; f /= np.linalg.norm(f); up = np.array([0, 1.0, 0]); r = np.cross(f, up); r /= np.linalg.norm(r); u = np.cross(r, f)
    fy = H / 2 / math.tan(math.radians(cam['fov']) / 2); fx = fy; out = []
    for q in pts:
        v = np.array([q[0], q[1], q[2]], float) - p; d = v @ f
        if d <= 1: continue
        x, y = W / 2 + fx * (v @ r) / d, H / 2 - fy * (v @ u) / d
        if 0 <= x < W and 0 <= y < H: out.append(dict(px=fy * h / d, d=float(np.hypot(*(v[[0, 2]])))))
    return out


def stat(rows, near=None):
    if near: rows = [r for r in rows if r['d'] <= near]   # chỉ vật đang hiện (units near)
    if not rows: return None
    a = np.array([r['px'] for r in rows]); d = np.array([r['d'] for r in rows])
    return dict(n=len(a), px_min=round(float(a.min()), 1), px_med=round(float(np.median(a)), 1), px_max=round(float(a.max()), 1), n_duoi_6px=int((a < 6).sum()), tam_m=[round(float(d.min())), round(float(d.max()))])


def main():
    A = argparse.ArgumentParser(); A.add_argument('--khung', required=True); A.add_argument('--cu', required=True); A.add_argument('--out', required=True); a = A.parse_args()
    K = a.khung; rep = dict(cach='dieu-phoi measure_dp (640×360, y 60–300) · mặt nạ render.js --maskonly · px chiếu theo campath (1080p)', loai={})
    for k, (ten, sc, f, cu) in LOAI.items():
        R = dict(canh=sc, khung=f)
        sach = glob.glob(f'{K}/sach-{k}/*.jpg')[0]; chu = glob.glob(f'{K}/chu-{k}/*.jpg')[0]
        png = f'{K}/chu-{k}.png'; Image.open(chu).save(png)
        R['v5b2d_sach'] = measure(sach); R['v5b2d_chu_png'] = measure(png); R['v5b2c_sach'] = measure(os.path.join(a.cu, cu))
        for d in (R['v5b2d_sach'], R['v5b2d_chu_png'], R['v5b2c_sach']): d['file'] = os.path.relpath(d['file'], K) if d['file'].startswith(K) else d['file']
        try: M = json.load(open(f'{K}/mask-{k}.json')); M = M[0] if isinstance(M, list) else M; R['mat_na'] = {x: M.get(x) for x in ('content_pct', 'fabric_pct', 'water_pct', 'flat_nat_pct', 'sky_pct', 'dat_doc_pct', 'bo_pct', 'empty_pct', 'content_center_pct')}
        except Exception as e: R['mat_na'] = f'lỗi {e}'
        try:
            L = json.load(open(glob.glob(f'{K}/sach-{k}/log.json')[0])); meta = L['info'].get('scene_meta') or {}
            C = json.load(open(f'{K}/cam-{sc}.json')); fr = (C.get('frames') or C.get('rows') or C)[f] if isinstance(C, dict) else C[f]
            cam = dict(p=fr['pos'], l=fr['look'], fov=fr['fov']) if 'pos' in fr else (fr.get('cam') or fr); dp = (meta.get('doPx') or {}); R['px'] = {}
            if dp.get('quan'): R['px']['quan_1m75'] = stat(proj_px(cam, dp['quan'], 1.75), dp.get('near')); R['px']['khoi_quan'] = stat(proj_px(cam, dp['quan'], 1.75, box=dp.get('khoi', (31, 15))), dp.get('near'))
            if dp.get('dam_dong'): R['px']['dam_dong_1m75'] = stat(proj_px(cam, dp['dam_dong'], 1.75)); R['px']['khoi_dam_dong'] = stat(proj_px(cam, dp['dam_dong'], 1.75, box=(8, 5)))
            if dp.get('tau'): R['px']['tau_than_6m'] = stat(proj_px(cam, [[q[0], 0, q[2]] for q in dp['tau']], 6.0))
            R['scene_meta'] = {x: meta.get(x) for x in ('quan', 'town', 'kb_san', 'kb_phao', 'khoi_dau_nong', 'co', 'khoi', 'vuon', 'chay')}
        except Exception as e: R['px'] = f'lỗi {e}'
        rep['loai'][ten] = R
    # lửa đỏ % (khung 6)
    try:
        A1 = np.asarray(Image.open(glob.glob(f'{K}/sach-6/*.jpg')[0]).convert('RGB')).astype(int); A0 = np.asarray(Image.open(glob.glob(f'{K}/sach-6-khonglua/*.jpg')[0]).convert('RGB')).astype(int)
        dif = np.abs(A1 - A0).max(-1) > 30; red = (A1[..., 0] > A1[..., 1] + 35) & (A1[..., 0] > A1[..., 2] + 60)
        rep['lua_do_pct'] = round(float((dif & red).mean() * 100), 3); rep['lua_doi_pct'] = round(float(dif.mean() * 100), 3)
        rep['do_cam_toan_khung_pct'] = round(float(red.mean() * 100), 2)   # cận trên: mọi điểm đỏ–cam (gồm mái ngói, thân tàu)
    except Exception as e: rep['lua_do_pct'] = f'lỗi {e}'
    for nm in ('v5b2d_sach', 'v5b2d_chu_png', 'v5b2c_sach'):
        rep['trung_vi_' + nm] = {x: round(float(np.median([r[nm][x] for r in rep['loai'].values()])), 3) for x in ('sat_med', 'colorful', 'edges', 'clip_pct')}
    json.dump(rep, open(a.out, 'w'), ensure_ascii=False, indent=1)
    print(f"{'loại':12s} {'sat 2d':>7s} {'sat 2c':>7s} {'col 2d':>7s} {'col 2c':>7s} {'cạnh 2d':>7s} {'cạnh 2c':>7s}  nội dung  nước  đất  trời")
    for t, R in rep['loai'].items():
        m = R['mat_na'] if isinstance(R['mat_na'], dict) else {}
        print(f"{t:12s} {R['v5b2d_sach']['sat_med']:7.3f} {R['v5b2c_sach']['sat_med']:7.3f} {R['v5b2d_sach']['colorful']:7.1f} {R['v5b2c_sach']['colorful']:7.1f} {R['v5b2d_sach']['edges']:7.1f} {R['v5b2c_sach']['edges']:7.1f}  {m.get('content_pct')}  {m.get('water_pct')}  {m.get('flat_nat_pct')}  {m.get('sky_pct')}  px={json.dumps(R.get('px'), ensure_ascii=False)[:200]}")
    print('trung vị', {k: v for k, v in rep.items() if k.startswith('trung_vi')}, 'lửa', rep.get('lua_do_pct'))


if __name__ == '__main__':
    main()
