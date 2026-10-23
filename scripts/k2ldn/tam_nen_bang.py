#!/opt/cine/bin/python
"""LOOK-T4-V2 · bảng tóm tắt cổng kiểm §15 (c) mọi tấm nền: tam_nen_bang.py [thư mục tn] → in bảng Markdown + reports/look-t4-v2/do/tam-nen.json"""
import glob, json, os, sys
V = sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/ldn/v2/tn'; REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); out = {}
print('| Tấm | (i) max/255 · vật (a) | (ii) lỗi thời đại · q_thoi_dai | (iii) T9b đất→nước / nước→đất % — toàn khung | — trong hộp địa hình | mô hình báo đổi vùng | (iv) | (v) nhấp nháy ghép/đối chứng | ĐẠT (i–iv) |')
print('|---|---|---|---|---|---|---|---|---|')
for f in sorted(glob.glob(os.path.join(V, '*', '*', '*-kiem.json'))):
    d = json.load(open(f)); t = d['tag']; i3 = d['iii_doi_vung']; h = i3.get('trong_hop_dia_hinh', {}); q = d['ii_thoi_dai'].get('q_thoi_dai') or {}
    v = os.path.join(os.path.dirname(f), f'{t}-v.json'); vv = json.load(open(v)) if os.path.exists(v) else None
    qs = (q.get('val') or '')[:40]
    vat = '; '.join(f"{x['mh']}:{x['loai']}:{x['mo_ta'][:50]}" for x in d['i_lop_a']['vat_lop_a'])
    row = dict(i=d['i_lop_a']['max_trong_a'], vat=vat, ii=len(d['ii_thoi_dai']['loi']), qtd=qs, iii=(i3['t9b_dat_thanh_nuoc_pct'], i3['t9b_nuoc_thanh_dat_pct']), iii_hop=(h.get('t9b_dat_thanh_nuoc_pct'), h.get('t9b_nuoc_thanh_dat_pct')),
               iii_mh=len(i3['mo_hinh_bao']), iv=len(d['iv_dong_bang']['loi']), iv_vat='; '.join(f"{x['mh']}:{x['loai']}" for x in d['iv_dong_bang']['loi']), v=vv, dat=d['dat_ca'])
    out[t] = row
    print(f"| {t} | {row['i']} · {len(d['i_lop_a']['vat_lop_a'])} ({vat[:90]}) | {row['ii']} · {qs} | {row['iii'][0]} / {row['iii'][1]} | {row['iii_hop'][0]} / {row['iii_hop'][1]} | {row['iii_mh']} | {row['iv']} {row['iv_vat'][:40]} | {(str(vv['nhap_nhay_ghep']) + ' / ' + str(vv['nhap_nhay_doi_chung'])) if vv else '—'} | {'ĐẠT' if row['dat'] else 'TRƯỢT'} |")
os.makedirs(os.path.join(REPO, 'reports/look-t4-v2/do'), exist_ok=True); json.dump(out, open(os.path.join(REPO, 'reports/look-t4-v2/do/tam-nen.json'), 'w'), ensure_ascii=False, indent=1)
