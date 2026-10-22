#!/opt/cine/bin/python -I
"""NC-N2P · tổng hợp số đo video Omni đã ghép (bộ đo NC-V2V/V2V3 + 3 khung mẫu kiem_n2p + q_thoi_dai) → bảng Markdown + JSON.
  tong_hop_video.py <thư mục omni> <ra.json>"""
import glob, json, os, sys
O = sys.argv[1]; rows = []
for g in sorted(glob.glob(f'{O}/do/*-ghep.json')):
    tag = os.path.basename(g)[:-10]
    if tag.endswith('doichung'): continue
    k = tag.split('-')[0]; G = json.load(open(g))
    v2 = f'{O}/do/{tag}-v2v.json'; t3 = f'{O}/do/{tag}-them3.json'; dc2 = f'{O}/do/{k}-doichung-v2v.json'; dc3 = f'{O}/do/{k}-doichung-them3.json'
    if not os.path.exists(v2): continue
    V = json.load(open(v2)); T = json.load(open(t3)); DV = json.load(open(dc2)) if os.path.exists(dc2) else None; DT = json.load(open(dc3)) if os.path.exists(dc3) else None
    fr = []
    for f in sorted(glob.glob(f'{O}/kiem/{tag}-*-kiem.json')):
        K = json.load(open(f)); tq = os.path.basename(f)[:-10]; q = f'{O}/qtd/{tq}.json'; qn = None
        if os.path.exists(q): qn = sum(len(x.get('nghi_van', [])) for x in json.load(open(q)).get('khung', []))
        fr.append(dict(khung=tq, vat_a=len(K['i_lop_a']['vat_lop_a']), vat_a_ca_hai=len({x['loai'] for x in K['i_lop_a']['vat_lop_a'] if x['mh'] == 'gpt'} & {x['loai'] for x in K['i_lop_a']['vat_lop_a'] if x['mh'] == 'claude'}),
                       loai_a=sorted({x['loai'] for x in K['i_lop_a']['vat_lop_a']}), thoi_dai=len(K['ii_thoi_dai']['loi']), nghi_van=len(K['ii_thoi_dai'].get('nghi_van_khong_nam', [])), qtd=qn,
                       t9b=[K['iii_doi_vung'].get('t9b_dat_thanh_nuoc_pct'), K['iii_doi_vung'].get('t9b_nuoc_thanh_dat_pct')], vung_mh=len(K['iii_doi_vung']['mo_hinh_bao'])))
    r = dict(tag=tag, max_trong_a_truoc_ma_hoa=G['max_trong_a_moi_khung'], nhap_nhay_ti_so=V['nhap_nhay']['ti_so'], nhap_nhay_dc=DV['nhap_nhay']['ti_so'] if DV else None,
             T7_dom_sang_ben=T['dom_sang_moi']['ben_1s'], T7_mau_lua=T['dom_sang_moi']['ben_1s_mau_lua'], T7_dc=DT['dom_sang_moi']['ben_1s'] if DT else None,
             T8_vat_moi_ben=T['vat_moi_vung_trong']['ben_1s'], T8_dc=DT['vat_moi_vung_trong']['ben_1s'] if DT else None,
             T9=[T['doi_loai_vung']['dat_thanh_nuoc_pct'], T['doi_loai_vung']['nuoc_thanh_dat_pct']], T9_dc=[DT['doi_loai_vung']['dat_thanh_nuoc_pct'], DT['doi_loai_vung']['nuoc_thanh_dat_pct']] if DT else None,
             lua_moi_pct_max=V['lua_moi']['pct_max'], may_dich_px=V['may']['can_khung_dich_tb_px'], khung=fr)
    r['dat'] = (r['max_trong_a_truoc_ma_hoa'] == 0 and all(x['vat_a'] == 0 and x['thoi_dai'] == 0 and x['vung_mh'] == 0 and max(x['t9b']) <= 2 for x in fr)
                and r['T9'][0] <= max(2, (r['T9_dc'] or [0, 0])[0] + 2) and r['T9'][1] <= max(2, (r['T9_dc'] or [0, 0])[1] + 2) and r['T7_mau_lua'] == 0 and r['nhap_nhay_ti_so'] <= 1.5 * max(1e-6, r['nhap_nhay_dc'] or 1))
    rows.append(r)
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print('| Biến thể | (i) ghép: max lệch trong (a) trước mã hoá | (i) vật lớp (a) THÊM/ĐỔI (3 khung; gpt ∪ claude) | (ii) lỗi thời đại có năm · nghi vấn · q_thoi_dai | (iii) T9 cả clip đất→nước · nước→đất % (đối chứng) | (iii) T9b 3 khung max % · mô hình báo | T7 đốm sáng bền ≥ 1 s (màu lửa) · đc | T8 vật mới bền · đc | Nhấp nháy ÷ nguồn (đc) | Máy kết luận |')
print('|---|---|---|---|---|---|---|---|---|---|')
for r in rows:
    fr = r['khung']
    print(f"| {r['tag']} | {r['max_trong_a_truoc_ma_hoa']} | {sum(x['vat_a'] for x in fr)} ({', '.join(sorted({l for x in fr for l in x['loai_a']}))}) | {sum(x['thoi_dai'] for x in fr)} · {sum(x['nghi_van'] for x in fr)} · {sum(x['qtd'] or 0 for x in fr)} | "
          f"{r['T9'][0]} · {r['T9'][1]} ({r['T9_dc'][0]} · {r['T9_dc'][1]}) | {max(max(x['t9b']) for x in fr):.2f} · {sum(x['vung_mh'] for x in fr)} | {r['T7_dom_sang_ben']} ({r['T7_mau_lua']}) · {r['T7_dc']} | {r['T8_vat_moi_ben']} · {r['T8_dc']} | "
          f"{r['nhap_nhay_ti_so']} ({r['nhap_nhay_dc']}) | {'ĐẠT' if r['dat'] else 'LOẠI'} |")
