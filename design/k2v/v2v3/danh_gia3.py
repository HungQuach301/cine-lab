#!/opt/cine/bin/python -I
"""NC-V2V3 · áp NGƯỠNG LOẠI — T1–T6 Y NGUYÊN design/k2v/v2v/danh_gia.py (NC-V2V; so với bản đối chứng KHÔNG AI cùng cửa sổ) + 2 ngưỡng thêm ghi TRƯỚC khi đọc kết quả chế độ B:
  T7 đốm sáng mới bền ≥ 1 s: số vệt ≤ max(1, đối chứng) VÀ 0 vệt màu lửa
  T8 vật mới bền ≥ 1 s trong vùng trống (thành phần liên thông cạnh mới ≥ 40 px nối qua khung): 0
  ĐẠT = qua T1–T8 VÀ P đọc tờ so không thấy vật bịa (cột 'P' điền tay trong p_doc.json).
  danh_gia3.py <thư mục do/> <ra.json> <ra.md> [p_doc.json]"""
import json, sys, os
from pathlib import Path
D = Path(sys.argv[1]); PD = json.load(open(sys.argv[4])) if len(sys.argv) > 4 and os.path.exists(sys.argv[4]) else {}
rows = []; md = ['| Clip-chế độ | T1 giữ tàu / cờ / pin (÷ đc) | T2 F1 nhà · tàu | T3 cạnh mới trời · nước · đất % | T4 lửa mới max % (sàn) | T5 nhấp nháy ÷ đc | T6 dịch px · tỉ lệ · lệch khung | T7 đốm sáng bền (lửa) · đc | T8 vật mới bền | Chi tiết nguồn → ra | Bão hoà nguồn → ra | Máy | P đọc | Kết luận |', '|' + '---|' * 14]
for c in ['c2', 'c4B', 'c1']:
    if not (D / f'{c}-dc.json').exists(): continue
    dc = json.load(open(D / f'{c}-dc.json')); dct = json.load(open(D / f'{c}-dc-them.json'))
    for v in 'AB':
        if not (D / f'{c}-{v}.json').exists(): continue
        R = json.load(open(D / f'{c}-{v}.json')); X = json.load(open(D / f'{c}-{v}-them.json')); g, dm, m = R['giu'], R['dem'], R['may']; fails = []; t1 = {}
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
        b7, b7l, b70 = X['dom_sang_moi']['ben_1s'], X['dom_sang_moi']['ben_1s_mau_lua'], dct['dom_sang_moi']['ben_1s']
        if b7 > max(1, b70) or b7l > 0: fails.append('T7 đốm sáng bền')
        b8 = X['vat_moi_vung_trong']['ben_1s']
        if b8 > 0: fails.append('T8 vật mới bền')
        p = PD.get(f'{c}-{v}', {}); pok = p.get('dat'); may = not fails
        dat = may and pok is True
        rows.append(dict(clip=c, che_do=v, t1=t1, f1_nha=f_nha, f1_tau=f_tau, canh_moi=cm, lua_max=lua, lua_san=round(thr, 3), nhap_nhay_tren_dc=round(nn, 2), dich=m['can_khung_dich_tb_px'], ti_le=m['can_khung_ti_le_tb'], lech_khung=lag,
                         dom_sang_ben=b7, dom_sang_ben_lua=b7l, dom_sang_ben_dc=b70, vat_moi_ben=b8, chi_tiet=(R['look']['nguon']['detail'], R['look']['ra']['detail']), bao_hoa=(R['look']['nguon']['sat_med'], R['look']['ra']['sat_med']),
                         truot_may=fails, may_dat=may, p_doc=p.get('thay', None), p_dat=pok, dat=dat))
        t1s = ' · '.join(f"{k} {a[0]:.2f} ({a[1]:.2f})" for k, a in t1.items()) or '—'
        md.append(f"| {c}-{v} | {t1s} | {f_nha if f_nha is not None else '—'} · {f_tau if f_tau is not None else '—'} | {' · '.join(f'{k} {x}' for k, x in cm.items())} | {lua} ({thr:.3f}) | {nn:.2f} | {m['can_khung_dich_tb_px']} · {m['can_khung_ti_le_tb']} · {lag if lag is not None else 'kxđ'} | {b7} ({b7l}) · {b70} | {b8} | {R['look']['nguon']['detail']:.1f} → {R['look']['ra']['detail']:.1f} | {R['look']['nguon']['sat_med']:.2f} → {R['look']['ra']['sat_med']:.2f} | {'qua' if may else 'LOẠI: ' + ', '.join(fails)} | {'—' if pok is None else ('không thấy vật bịa' if pok else 'LOẠI: ' + p.get('thay', ''))} | {'**ĐẠT**' if dat else 'LOẠI'} |")
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1); Path(sys.argv[3]).write_text('\n'.join(md) + '\n')
print(sum(r['dat'] for r in rows), '/', len(rows), 'đạt'); print('\n'.join(md))
