#!/opt/cine/bin/python
"""G1b T3 · TỰ SOI 3 shot bản đồ chiến lược (SM1–SM3) sau khi dựng — ghi khoá `soi` vào channel-k2/k2c-t3-01/g1b/sm/log-<SM>.json:
  (a) tuyến biển không cắt đất: mẫu 0,5 km dọc tuyến ĐÃ VẼ, khoảng cách tới đất NE 1:10m (land + minor islands, LAEA EPSG:3035); bỏ đệm 5 km quanh cảng
      (điểm mốc loai 'cang' của routes.geojson); thêm nửa bề ngang nét ở km/px đầu–cuối shot (nét chạm bờ trên hình, không phải cắt đất)
  (b) chú giải ≤ 3 mục mỗi shot · (c) cỡ chữ nhỏ nhất (px @1080; ≥ 30 ↔ ≥ 15 px ở 540p)
  (d) chữ trên hình theo vai từ log lớp chữ (sec/<seg>.log.json nếu có) — không có vai nguồn/bien_gioi/approx
  (e) chuyển động: hiệu khung liên tiếp (xám 160×90) của sec/<seg>.mkv > ngưỡng → thời điểm bắt đầu chuyển động + % khung có chuyển động
Dùng: g1b_soi.py [--g channel-k2/k2c-t3-01/g1b/sm] [--ep /var/tmp/cine-out/g1b/sm/ep] [--raw /var/tmp/cine-out/bd/raw]"""
import argparse, json, math, os, subprocess
import numpy as np
from shapely.geometry import shape, LineString, Point
from shapely.ops import transform, unary_union
from pyproj import Transformer

T = Transformer.from_crs('EPSG:4326', 'EPSG:3035', always_xy=True).transform
FOVK = 2 * math.tan(math.atan(18 / 35))   # bề ngang khung ≈ FOVK × dist (ống 35 mm, cảm biến 36 mm)


def kmpx(cam, t):
    K = sorted(cam, key=lambda k: k['t']); k = K[0]
    for c in K:
        if c['t'] <= t: k = c
    return FOVK * k['dist'] / 1920


def routes_of(S):
    if 'a' in S: return [(r, S[x]['hero_opt']['cam'], x) for x in ('a', 'b') for r in S[x]['hero_opt']['routes']]
    return [(r, S['hero_opt']['cam'], '') for r in S['hero_opt']['routes']]


def shots_of(S):
    return [S[x] for x in ('a', 'b')] if 'a' in S else [S]


def motion(mkv):
    W, H = 160, 90
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mkv, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    d = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2)); thr = 0.15   # mức xám trung bình/khung: > 0,15 = có chuyển động thấy được (nhiễu mã hoá ≈ 0,02–0,05)
    mv = d > thr; first = int(np.argmax(mv)) + 1 if mv.any() else None
    return dict(khung=len(F), nguong_xam=thr, bat_dau_s=round(first / 24, 3) if first else None, phu_pct=round(100 * mv.mean(), 1), hieu_tb=round(float(d.mean()), 3), hieu_min=round(float(d.min()), 3))


def main():
    a = argparse.ArgumentParser(); a.add_argument('--g', default='channel-k2/k2c-t3-01/g1b/sm'); a.add_argument('--ep', default='/var/tmp/cine-out/g1b/sm/ep')
    a.add_argument('--raw', default='/var/tmp/cine-out/bd/raw'); a.add_argument('--routes', default='channel-k2/k2c-t3-01/tuyen/routes.geojson'); A = a.parse_args()
    land = unary_union([shape(f['geometry']) for n in ('ne_10m_land', 'ne_10m_minor_islands') for f in json.load(open(f'{A.raw}/{n}.geojson'))['features']])
    land = transform(T, land.intersection(shape(dict(type='Polygon', coordinates=[[[-30, 25], [25, 25], [25, 62], [-30, 62], [-30, 25]]]))))
    RG = {f['properties']['id']: f['properties'] for f in json.load(open(A.routes))['features']}
    for sm in ('SM1', 'SM2', 'SM3'):
        S = json.load(open(f'{A.g}/spec-{sm}.json')); R = []
        for r, cam, part in routes_of(S):
            pr = RG.get(r['id'], {})
            if r.get('close') or pr.get('mode') != 'sea': continue
            ports = [transform(T, Point(w['lon'], w['lat'])).buffer(5000) for w in (pr.get('waypoints') or []) if isinstance(w, dict) and w.get('loai') == 'cang']
            L = transform(T, LineString(r['pts'])); n = max(2, int(L.length / 500)); step = L.length / 1000 / n
            P = [L.interpolate(i / n, normalized=True) for i in range(n + 1)]; d = [land.distance(p) / 1000 for p in P]
            inport = [any(b.contains(p) for b in ports) for p in P]
            cut = sum(step for x, ip in zip(d, inport) if x == 0 and not ip); cut_port = sum(step for x, ip in zip(d, inport) if x == 0 and ip)
            t0, t1 = r['draw']; k0, k1 = kmpx(cam, t0), kmpx(cam, t1); w = r.get('w', 6)
            R.append(dict(id=r['id'], shot=part or sm, dai_km=round(L.length / 1000, 1), min_bo_km=round(min(x for x, ip in zip(d, inport) if not ip) if not all(inport) else 0, 2),
                          cat_dat_km_ngoai_cang=round(cut, 2), cat_dat_km_trong_dem_cang=round(cut_port, 2), w_px_1080=w,
                          nua_net_km=[round(w * k0 / 2, 2), round(w * k1 / 2, 2)], km_net_cham_bo=round(sum(step for x, ip in zip(d, inport) if not ip and x < w * k1 / 2), 1),
                          dat='ĐẠT' if cut == 0 else 'TRƯỢT'))
        SH = shots_of(S)
        leg = [len(s['p']['legend']['items']) for s in SH]
        px = []
        for s in SH:
            p = s['p']; px += [('legend', 34), ('counter', 72)] + [('point', q.get('px', 32)) for q in p.get('points', [])]
            for q in p.get('places', []): px += [('place:' + q['s'], q.get('px', 36))] + ([('sub:' + q['sub'], q.get('spx', 32))] if q.get('sub') else [])
        mn = min(px, key=lambda x: x[1])
        cam_mv = [dict(dist_dau=s['hero_opt']['cam'][0]['dist'], dist_cuoi=s['hero_opt']['cam'][-1]['dist'], dich_lon=round(abs(s['hero_opt']['cam'][-1]['lon'] - s['hero_opt']['cam'][0]['lon']), 2)) for s in SH]
        seg = sm.lower(); mkv = f'{A.ep}/sec/{seg}.mkv'; mo = motion(mkv) if os.path.exists(mkv) else None
        roles = None; lj = f'{A.ep}/sec/{seg}.mkv.log.json'
        if os.path.exists(lj):
            import re
            BAN = re.compile(r'approx|Map:|Cliopatria|Seshat|Natural Earth|ETOPO|OpenHistorical|Borders:|Relief:|source|illustrat|estimated', re.I)
            items = [it for fr in json.load(open(lj)).get('text', []) for it in fr.get('items', [])]
            chu = {}
            for it in items:
                k = it['s']; c = chu.setdefault(k, dict(vai=it.get('role'), cap_min=it.get('cap'), n=0)); c['n'] += 1
                if it.get('cap') is not None and (c['cap_min'] is None or it['cap'] < c['cap_min']): c['cap_min'] = it['cap']
            caps = [c['cap_min'] for c in chu.values() if c['cap_min'] is not None]
            roles = dict(tep=os.path.basename(lj), so_khung_mau=len(json.load(open(lj)).get('text', [])), chu=chu, cap_min_px1080=min(caps) if caps else None,
                         chu_cam=[k for k in chu if BAN.search(k)], vai_cam=sorted({c['vai'] for c in chu.values() if c['vai'] in ('src', 'bien_gioi', 'credit', 'inset_src', 'method', 'ai_label')}))
        soi = dict(tuyen_bien=R, tuyen_cat_dat='ĐẠT' if all(x['dat'] == 'ĐẠT' for x in R) else 'TRƯỢT', chu_giai_so_muc=leg, chu_giai='ĐẠT' if max(leg) <= 3 else 'TRƯỢT',
                   co_chu_nho_nhat_px1080=dict(vai=mn[0], px=mn[1], px540=mn[1] / 2, dat='ĐẠT' if mn[1] >= 30 else 'TRƯỢT'), may=cam_mv, chuyen_dong=mo, chu_tren_hinh=roles, chu_nguon_tren_hinh=('ĐẠT' if roles and not roles['chu_cam'] and not roles['vai_cam'] else 'TRƯỢT' if roles else 'CHƯA ĐO'),
                   chuyen_dong_dat=('ĐẠT' if mo and mo['bat_dau_s'] is not None and mo['bat_dau_s'] <= 1.5 and mo['phu_pct'] >= 60 else 'TRƯỢT' if mo else 'CHƯA ĐO'))
        lg = f'{A.g}/log-{sm}.json'; Lj = json.load(open(lg)); Lj['soi'] = soi; json.dump(Lj, open(lg, 'w'), ensure_ascii=False, indent=1)
        print(sm, 'tuyến', soi['tuyen_cat_dat'], [(x['id'], x['min_bo_km'], x['cat_dat_km_ngoai_cang']) for x in R], '| chú giải', leg, '| chữ nhỏ nhất', mn, '| chuyển động', mo, '| chữ cấm', roles and (roles['chu_cam'], roles['vai_cam'], roles['cap_min_px1080']))


if __name__ == '__main__':
    main()
