#!/opt/cine/bin/python
"""LOOK-T4 · bảng số đo 24 khung THEO NHÃN MÙ (reports/look-t4/do/<hàng>-<X|Y|Z>.json) → markdown (in ra) + reports/look-t4/do/tong.json;
tổng hợp theo biến thể A/B/C (cần khoá) → reports/look-t4/khoa-do.json (MỞ SAU KHI CHỌN MÙ). Đánh dấu chỉ số trong ±5 % quanh ngưỡng
(bão hoà trung vị ≥ 0,40 — BIBLE §14.4; trời + sương 8–20 % — LOOK-2 T3; nước ≤ 33,3 % — §11.4).
  look_bang.py"""
import json, os, glob
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(REPO, 'reports/look-t4/do'); rows = []
ORDER = ['M1-rong', 'M1-trung', 'M2-ngay', 'M2-dem', 'M3-rong', 'M3-trung', 'M4-rong', 'M4-trung']
def gan(v, ng, kieu):
    return abs(v - ng) <= 0.05 * ng
out = ['| Khung | Cột (mù) | Bão hoà TV (cả khung / giữa) | Colorfulness | Chi tiết | Nước % | Trời % | Sương % | Trời+sương % | Tiêu điểm (x %, y %) · cách giao 1/3 · tương phản | ±5 % ngưỡng |', '|---|---|---|---|---|---|---|---|---|---|---|']
tong = {}
for k in ORDER:
    for v in 'XYZ':
        f = os.path.join(D, f'{k}-{v}.json')
        if not os.path.exists(f): continue
        d = json.load(open(f)); t = d.get('tieu_diem', {}); tong[f'{k}-{v}'] = d
        near = []
        if gan(d['bao_hoa_tv'], 0.40, ''): near.append('bão hoà')
        if gan(d.get('troi_suong_pct', 0), 20, '') or gan(d.get('troi_suong_pct', 0), 8, ''): near.append('trời+sương')
        if gan(d.get('nuoc_pct', 0), 33.3, ''): near.append('nước')
        out.append(f"| {k} | {v} | {d['bao_hoa_tv']:.3f} / {d['bao_hoa_tv_giua']:.3f} | {d['colorfulness']} | {d['chi_tiet']} | {d.get('nuoc_pct')} | {d.get('troi_pct')} | {d.get('suong_pct')} | {d.get('troi_suong_pct')} | "
                   f"{t.get('x_pct')}, {t.get('y_pct')} · {t.get('cach_giao_diem_1_3_pct_cheo')} · {t.get('tuong_phan_cuc_bo_so_khung')} | {', '.join(near) or '—'} |")
json.dump(tong, open(os.path.join(D, 'tong.json'), 'w'), ensure_ascii=False, indent=1)
import statistics as st
KH = json.load(open(os.path.join(REPO, 'reports/look-t4/khoa.json')))['hang']; agg = {}
for v in 'ABC':
    rows = {k: tong[f'{k}-{lab}'] for k in ORDER for lab in 'XYZ' if KH[k][lab] == v and f'{k}-{lab}' in tong}
    ngay = [d['bao_hoa_tv'] for k, d in rows.items() if k in ('M1-rong', 'M1-trung', 'M2-ngay', 'M4-rong', 'M4-trung')]
    agg[v] = {'bao_hoa_tv_trung_vi_8': round(st.median([d['bao_hoa_tv'] for d in rows.values()]), 3), 'bao_hoa_tv_trung_vi_5_khung_ngay': round(st.median(ngay), 3),
              'colorfulness_trung_vi': round(st.median([d['colorfulness'] for d in rows.values()]), 1), 'theo_khung': {k: d['bao_hoa_tv'] for k, d in rows.items()}}
json.dump({'ghi_chu': 'MỞ SAU KHI CHỌN MÙ — số đo tổng hợp theo biến thể', 'bien_the': agg}, open(os.path.join(REPO, 'reports/look-t4/khoa-do.json'), 'w'), ensure_ascii=False, indent=1)
allv = [d['bao_hoa_tv'] for d in tong.values()]
out.append(f'\nPhạm vi bão hoà TV trên 24 ô: {min(allv):.3f} – {max(allv):.3f} (ngưỡng §14.4: 0,40). Tổng hợp theo biến thể: `khoa-do.json` (mở sau khi chọn).')
print('\n'.join(out))
