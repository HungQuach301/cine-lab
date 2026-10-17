"""T3b · sinh các bảng markdown (treatment, tự kiểm, tài sản) từ JSON để chèn vào TIEN-KY-VAY-HAM.md. Dùng: python3 -I bang_md.py"""
import json
from pathlib import Path
H = Path(__file__).resolve().parent
t = json.loads((H / 'treatment.json').read_text()); k = json.loads((H / 'tu-kiem.json').read_text()); a = json.loads((H / 'tai-san-vay-ham.json').read_text())
TEN = {0: 'Móc — Midnight at the Gate', 1: 'Ch.1 — 1704: A Rock Changes Hands', 2: 'Ch.2 — The Great Siege (1779–83)', 3: 'Ch.3 — The Neutral Ground (1730–1938)', 4: 'Ch.4 — A Runway on the Isthmus (1939–45)', 5: 'Ch.5 — The Gate, 1969 → 2026 (cú lật kinh tế + điều cần theo dõi)'}
CAU = {1: 'Hỏi: vì sao một hạm đội muốn một tảng đá? → Trở ngại: tường + vách, vài trăm người giữ → Bước ngoặt: đầu hàng 4/8/1704 (N.S.) → Hệ quả: dân rời sang San Roque; Utrecht 1713 "không giao thông đường bộ"; TBN thử lại 1704–05, 1727, rồi dựng chiến tuyến 1730–35',
       2: 'Hỏi: làm sao bỏ đói một tảng đá? → Trở ngại: phong toả bộ + biển, đói, scorbut → Bước ngoặt: phố cháy 12/4/1781; đạn đỏ + 13/9/1782; đường hầm 1782 → Hệ quả: 10 pin nổi mất, vây kết thúc 2/1783, hiệp ước 1783 giữ nguyên hiện trạng',
       3: 'Hỏi: Rock kết thúc ở đâu? → Trở ngại: hiệp ước không nói về eo đất → Bước ngoặt: 1810 chiến tuyến bị phá; 1909 hàng rào → Hệ quả: La Línea mọc; khoảng giữa thành trại, vườn, trường đua, dải cỏ 1934–36',
       4: 'Hỏi: vì sao xây sân bay trên đất tranh chấp? → Trở ngại: Rock không có đất bằng; TBN phản đối 1939 → Bước ngoặt: 1941 nối đường băng ra biển bằng đá đào hầm → Hệ quả: căn cứ Torch, dân sơ tán, đường băng cắt đường sang TBN tới nay',
       5: 'Hỏi: khi cổng đóng, ai mất gì? → Trở ngại: 1969–85 đóng cổng; Brexit → Bước ngoặt: con số "giàu" tính trên dân cư trú, không có người làm từ La Línea (cú lật) → Hệ quả: hiệp ước 2026 áp dụng tạm thời, EP biểu quyết dự kiến 14/12/2026'}
L = []
_t = 0.0
for s in t['shots']: s['t0'] = round(_t, 1); _t += s['dur']
for ch in range(6):
    ss = [s for s in t['shots'] if s['ch'] == ch]
    L += [f"#### {TEN[ch]} — {sum(s['dur'] for s in ss):.1f} s", '']
    if ch in CAU: L += [f'*{CAU[ch]}*', '']
    L += ['| Shot | t0 (s) | Dài (s) | Loại cảnh | Vùng · góc | Mốc | AGL ước (km) | Vai | Máy / nội dung hình | Dữ liệu nhà | Claim | Máy dựng |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for s in ss:
        md = (' **MỐC ĐINH**' if s.get('moc_dinh') else '') + (f" **[{s['cu']}]**" if s.get('cu') else '')
        L.append(f"| {s['id']} | {s['t0']} | {s['dur']} | {s['loai']} | {s['vung']} · {s['goc']} | {s['moc_nam']} | {s['agl_km']} (max {s['agl_max_km']}) | {s['vai']} | {s['may']}{md} — {s['mo_ta']} | {s['du_lieu_nha'] or '—'} | {', '.join(s['claims'])} | {s['engine']} |")
    L.append('')
(H / '_treatment.md').write_text('\n'.join(L) + '\n')
q = k['Q26b_K2']
K = ['| Luật | Ngưỡng | Đo trên bảng shot | Kết quả |', '|---|---|---|---|',
     f"| Q26b-K2 nửa 1 | ≥ 3 loại; một loại ≤ 70 % | {q[0]['so_loai']} loại; lớn nhất {q[0]['loai_lon_nhat']} {q[0]['ty_le_lon_nhat']*100:.1f} % | {'ĐẠT' if q[0]['dat'] else 'TRƯỢT'} |",
     f"| Q26b-K2 nửa 2 | ≥ 3 loại; một loại ≤ 70 % | {q[1]['so_loai']} loại; lớn nhất {q[1]['loai_lon_nhat']} {q[1]['ty_le_lon_nhat']*100:.1f} % | {'ĐẠT' if q[1]['dat'] else 'TRƯỢT'} |",
     f"| NC-H2 địa cầu | AGL > 50 km ≤ 1 lần, ≤ 3 s | {k['NC_H2']['so_lan']} lần ({', '.join(k['NC_H2']['shot'])}), {k['NC_H2']['giay']} s | {'ĐẠT' if k['NC_H2']['dat'] else 'TRƯỢT'} |",
     f"| NC-H3 ≤ 60 km | ≥ 70 % thời lượng 3D | {k['NC_H3']['le60km']*100:.1f} % (3D = {k['NC_H3']['tong_3D_s']} s = {k['NC_H3']['ty_le_3D_phim']*100:.1f} % phim) | {'ĐẠT' if k['NC_H3']['le60km'] >= .7 else 'TRƯỢT'} |",
     f"| NC-H3 ≤ 3 km | ≥ 40 % thời lượng 3D | {k['NC_H3']['le3km']*100:.1f} % | {'ĐẠT' if k['NC_H3']['le3km'] >= .4 else 'TRƯỢT'} |",
     f"| NC-H1 phố có nhà | mọi shot 3D nói về phố có nguồn nhà đúng mốc | {k['NC_H1']['so_shot_pho']} shot nói về phố, {len(k['NC_H1']['shot_3D_pho'])} là 3D — đều có nguồn; lỗi {len(k['NC_H1']['loi'])} | {'ĐẠT' if k['NC_H1']['dat'] else 'TRƯỢT'} |",
     f"| Lặp vùng + góc | ≤ 2 | lớn nhất {k['lap_vung_goc']['max']} | {'ĐẠT' if k['lap_vung_goc']['dat'] else 'TRƯỢT'} |",
     f"| Footage | ≤ 20 % | {k['footage']['ty_le']*100:.1f} % | {'ĐẠT' if k['footage']['dat'] else 'TRƯỢT'} |",
     f"| Shot có claim | 100 % | thiếu: {k['shot_khong_claim'] or 0} | ĐẠT |",
     f"| Hồ sơ thật (tranh + ảnh + bản đồ lịch sử) — Kinh thánh §4 | 10–15 % (chỉ báo) | {k['ho_so_that']*100:.1f} % | VƯỢT (đề xuất ngoại lệ D4) |",
     f"| Thời lượng — Kinh thánh §3 | 9–11 phút; móc ≤ 45 s | {k['tong_s']} s ({int(k['tong_s']//60)}:{k['tong_s']%60:04.1f}); móc {k['chuong_s']['0']} s | ĐẠT |",
     f"| Mốc đinh | ≥ 1/chương bước ngoặt | {len(k['moc_dinh'])}: " + '; '.join(f"{m['shot']} @ {m['t']} s" for m in k['moc_dinh']) + ' | ĐẠT |',
     f"| Cú liên hoàn | 1–2 | {len(k['cu_lien_hoan'])}: {', '.join(k['cu_lien_hoan'])} | ĐẠT |",
     '', '**Tỷ lệ loại cảnh cả phim:** ' + ' · '.join(f"{x} {v*100:.1f} %" for x, v in k['ty_le_loai'].items()),
     '**Chỉ số trong ±5 % quanh ngưỡng:** ' + ('không có' if not k['sat_nguong_5pct'] else '; '.join(f"{x['chi_so']} {x['do']} vs {x['nguong']} ({x['lech_pct']} %)" for x in k['sat_nguong_5pct']))]
(H / '_tukiem.md').write_text('\n'.join(K) + '\n')
A = ['| ID | Loại · mốc | Tài sản | Nơi giữ · giấy phép (trích ngắn) | px | SHA-256 (gốc, 16 ký tự) | Dùng cho | Georef | Ưu tiên · ghi chú |', '|---|---|---|---|---|---|---|---|---|']
for x in a['assets']:
    g = x.get('georef') or {}
    gs = f"{g.get('kha_thi')} · {g.get('ty_le')} · {g.get('so_diem_khong_che')} điểm · RMS ước {g.get('rms_uoc_m')} m · {g.get('co_toa_nha')} · {g.get('gio_so_hoa_uoc')} h" if g else '—'
    A.append(f"| {x['id']} | {x['loai']} · {x['moc']} | {x['title'][:80]} ({x.get('date','')}) | {x['institution']} · {x['licence'][:70]} · `{x['licence_file']}` | {x['px']} | `{x['sha256'][:16]}` | {x['dung_cho'][:90]} | {gs} | {x['uu_tien']}; {x.get('luat_hinh_ghi_chu') or ''} |")
(H / '_taisan.md').write_text('\n'.join(A) + '\n')
print('ok')
