#!/opt/cine/bin/python -I
"""NC-V2V · áp NGƯỠNG LOẠI (ghi trước khi đọc kết quả tổng, hiệu chuẩn bằng bản đối chứng KHÔNG AI cùng clip: phóng 2 % + dịch + sáng + bão hoà + mờ + nén lại).
  T1 giữ vật: tàu / cờ / pin nổi — tỉ lệ giữ (đầu ra) ÷ tỉ lệ giữ (đối chứng) ≥ 0,90
  T2 hình học: F1 cạnh vùng nhà/công trình ≥ 0,85 và vùng tàu ≥ 0,85 (đối chứng 0,92–1,00)
  T3 bịa vùng trống: % cạnh MỚI ở mỗi vùng trời / nước / đất trống ≤ 5 % (luật giao việc; đối chứng ≤ 0,05 %)
  T4 lửa mới: % khung lớn nhất là điểm cam sáng mới ≤ max(0,05 %, 3 × đối chứng)
  T5 nhấp nháy: chỉ số ra ≤ 1,5 × đối chứng
  T6 máy/thời gian: dịch căn TB ≤ 12 px @640 và tỉ lệ 0,97–1,03; lệch khung |k| ≤ 1 khi đỉnh NCC ≥ 0,01 (không thì 'không xác định')
  danh_gia.py <thư mục do/> <ra.json> <ra.md>"""
import json, sys
from pathlib import Path
D = Path(sys.argv[1]); rows = []; md = ['| Clip-biến thể | T1 giữ tàu / cờ / pin (÷ đối chứng) | T2 F1 nhà · tàu | T3 cạnh mới trời · nước · đất % | T4 lửa mới max % (sàn) | T5 nhấp nháy ÷ đc | T6 dịch px · tỉ lệ · lệch khung | Chi tiết nguồn → ra | Bão hoà nguồn → ra | Kết luận |', '|---|---|---|---|---|---|---|---|---|---|']
for c in ['c1', 'c2', 'c3', 'c4A', 'c4B']:
    dc = json.load(open(D / f'{c}-dc.json'))
    for v in 'abc':
        R = json.load(open(D / f'{c}-{v}-720p.json')); g, dm, m = R['giu'], R['dem'], R['may']; fails = []
        t1 = {}
        for k in ('tau', 'co', 'pin'):
            if dm[k]['truoc']:
                r, r0 = dm[k]['giu'] / dm[k]['truoc'], dc['dem'][k]['giu'] / dc['dem'][k]['truoc']; t1[k] = (round(r, 3), round(r / r0, 3))
                if r / r0 < 0.90: fails.append(f'T1 {k}')
        f_nha, f_tau = g.get('nha', {}).get('f1_canh'), g.get('tau', {}).get('f1_canh')
        if f_nha is not None and f_nha < 0.85: fails.append('T2 nhà')
        if f_tau is not None and f_tau < 0.85: fails.append('T2 tàu')
        cm = {k: R['canh_moi_pct'][k]['tb'] for k in R['canh_moi_pct']}
        for k, x in cm.items():
            if x > 5: fails.append(f'T3 {k}')
        lua, lua0 = R['lua_moi']['pct_max'], dc['lua_moi']['pct_max']; thr = max(0.05, 3 * lua0)
        if lua > thr: fails.append('T4 lửa')
        nn = R['nhap_nhay']['ra'] / dc['nhap_nhay']['ra']
        if nn > 1.5: fails.append('T5 nhấp nháy')
        lag = m['lech_khung_trung_vi'] if (m['lech_do_nhon'] or 0) >= 0.01 else None
        if m['can_khung_dich_tb_px'] > 12 or not (0.97 <= m['can_khung_ti_le_tb'] <= 1.03): fails.append('T6 máy')
        if lag is not None and abs(lag) > 1: fails.append('T6 thời gian')
        rows.append(dict(clip=c, bien_the=v, t1=t1, f1_nha=f_nha, f1_tau=f_tau, canh_moi=cm, lua_max=lua, lua_san=round(thr, 3), nhap_nhay_tren_dc=round(nn, 2), dich=m['can_khung_dich_tb_px'], ti_le=m['can_khung_ti_le_tb'], lech_khung=lag,
                         chi_tiet=(R['look']['nguon']['detail'], R['look']['ra']['detail']), bao_hoa=(R['look']['nguon']['sat_med'], R['look']['ra']['sat_med']), truot=fails, dat=not fails))
        t1s = ' · '.join(f"{k} {a[0]:.2f} ({a[1]:.2f})" for k, a in t1.items()) or '—'
        md.append(f"| {c}-{v} | {t1s} | {f_nha if f_nha is not None else '—'} · {f_tau if f_tau is not None else '—'} | {' · '.join(f'{k} {x}' for k, x in cm.items())} | {lua} ({thr:.3f}) | {nn:.2f} | {m['can_khung_dich_tb_px']} · {m['can_khung_ti_le_tb']} · {lag if lag is not None else 'kxđ'} | {R['look']['nguon']['detail']:.1f} → {R['look']['ra']['detail']:.1f} | {R['look']['nguon']['sat_med']:.2f} → {R['look']['ra']['sat_med']:.2f} | {'ĐẠT' if not fails else 'LOẠI: ' + ', '.join(fails)} |")
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1); Path(sys.argv[3]).write_text('\n'.join(md) + '\n')
print(sum(r['dat'] for r in rows), '/', len(rows), 'đạt'); print('\n'.join(md))
