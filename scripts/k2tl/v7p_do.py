#!/opt/cine/bin/python
"""V7-PILOT · TỰ ĐO (việc 5 — ghi số, KHÔNG tự chấm đạt): % thời lượng góc cao có thời gian chạy / lướt thấp / khung neo; cắt/phút, shot TB;
khung "trống" (mặt nạ nội dung: đất tự nhiên phẳng không vật thể > 60 % khung — render.js --maskonly, lượt riêng, 1 khung/2 s); giây có tấm chữ; trôi máy (% khung/s) và
năm/s lớn nhất mỗi shot (meta cảnh); AGL. Ra reports/v7p/do/do-v7p.json.
Dùng: /opt/cine/bin/python -I scripts/k2tl/v7p_do.py [--mask]   (--mask: chạy lượt mặt nạ, ≈ 3 s/khung)"""
import json, os, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]; EPD = ROOT / 'channel-k2/k2c-t3-01/v7p'; OUT = ROOT / 'reports/v7p/do'; OUT.mkdir(parents=True, exist_ok=True)
E = yaml.safe_load((EPD / 'episode.yaml').read_text()); LOG = json.loads((EPD / 'log-shot.json').read_text())
HERO = Path('/var/tmp/cine-out/hero'); env = dict(os.environ, K2TL_CACHE=os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache'))

def main():
    T = sum(L['dur'] for L in LOG); n = len(LOG)
    hi = sum(L['dur'] for L in LOG if L['loai'].startswith('timelapse') and not L['luot_thap'] and not L['khung_neo'])
    low = sum(L['dur'] for L in LOG if L['luot_thap']); neo = sum(L['dur'] for L in LOG if L['khung_neo'])
    shots = []
    for L in LOG:
        k = f"v7p_{L['shot']}"; m = {}
        for p in HERO.glob(f'k2c-t3-v7p-{k}-d/meta.json'): m = json.loads(p.read_text())
        sm = m.get('scene_meta') or {}; fm = m.get('frames_meta') or {}
        agl = [v['agl_m'] for v in fm.values() if v.get('agl_m') is not None]
        shots.append(dict(shot=L['shot'], diem=L['diem_may'], dur=L['dur'], drift_pct_s=sm.get('drift_pct_s'), year_rate_max=sm.get('year_rate_max'), nam=sm.get('nam'),
                          agl_m=[min(agl), max(agl)] if agl else None, s_khung_540=m.get('s_per_frame'), leu=sm.get('leu')))
    chu = [dict(shot=L['shot'], loai='thẻ chương', s=L['chuong'], giay=3.0) for L in LOG if L.get('chuong')]
    res = dict(tong_s=round(T, 2), so_shot=n, cat_phut=round(n / (T / 60), 2), shot_tb_s=round(T / n, 2), ty_le_pct=dict(goc_cao_thoi_gian_chay=round(100 * hi / T, 1), luot_thap=round(100 * low / T, 1), khung_neo=round(100 * neo / T, 1)),
               tam_chu=dict(tam_so=0, tam_tu_lieu=0, cau_trich=0, the_chuong=chu, giay_co_tam_chu=round(sum(c['giay'] for c in chu), 1), ghi='bộ đếm năm/ngày (chữ chính, suốt tập) không tính là tấm chữ'), shots=shots)
    if '--mask' in sys.argv:
        rows = []
        for L in LOG:
            k = f"v7p_{L['shot']}"; o = E['heroes'][k]['opt']; N = int(round(L['dur'] * 24)); fr = list(range(12, N, 48)); f = OUT / f'mask-{L["shot"]}.json'
            subprocess.run(['node', str(ROOT / 'scripts/k2tl/render.js'), '--scene', 't3tl', '--pack', 'gib', '--w', '960', '--h', '540', '--opt', json.dumps(o, separators=(',', ':')), '--maskonly', str(f), '--only', ','.join(map(str, fr))],
                           env=env, capture_output=True, text=True)
            for r in json.loads(f.read_text()) if f.exists() else []:
                rows.append(dict(shot=L['shot'], f=r['f'], t=round(L['t0'] + r['f'] / 24, 2), dat_phang_tu_nhien_pct=r.get('flat_nat_pct'), nuoc_pct=r.get('water_pct'), troi_pct=r.get('sky_pct'), noi_dung_pct=r.get('content_pct')))
        trong = [r for r in rows if (r['dat_phang_tu_nhien_pct'] or 0) > 60]
        res['khung_trong'] = dict(dinh_nghia='đất tự nhiên phẳng không vật thể > 60 % diện tích khung (mặt nạ nội dung render.js, lượt riêng)', mau=len(rows), so_khung_trong=len(trong), danh_sach=trong,
                                  dat_phang_max=max((r['dat_phang_tu_nhien_pct'] or 0) for r in rows) if rows else None, chi_tiet=rows)
    (OUT / 'do-v7p.json').write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n'); print(json.dumps({k: v for k, v in res.items() if k not in ('shots', 'khung_trong')}, ensure_ascii=False))
    if 'khung_trong' in res: print('khung trống', res['khung_trong']['so_khung_trong'], '/', res['khung_trong']['mau'], 'max', res['khung_trong']['dat_phang_max'])

if __name__ == '__main__': main()
