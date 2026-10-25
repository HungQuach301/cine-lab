"""NC-T4: DIEM-NHAN.json → DIEM-NHAN.md (bảng tóm tắt + chi tiết nguồn). Dùng: python -I xuat_dn.py DIEM-NHAN.json DIEM-NHAN.md"""
import json, sys
d = json.load(open(sys.argv[1])); o = []
o.append('# ĐIỂM NHẤN — K2C-T4-02 London, animatic v2 (NC-T4, 25/10/2026)\n')
o.append(f"> Sinh từ `DIEM-NHAN.json` bằng `scripts/k2ldn/nc/xuat_dn.py`. Câu trích kiểm khớp nguyên văn bằng `scripts/k2ldn/nc/kiem_trich.py` (43/43). Căn cứ: {d['can_cu']}. {d['bac_ghi_chu']}.\n")
o.append('| Mã | Ngày | Nơi | Người | Hành động | Kết luận | Shot | Lớp | Thẻ (≤ 6 từ) | Lời |\n|---|---|---|---|---|---|---|---|---|---|')
for m in d['diem_nhan']:
    o.append(f"| {m['ma']} | {m['ngay']} | {m['noi']} | {m['nguoi']} | {m['hanh_dong']} | **{m['ket_luan']}** | {m['shot']} | {m['lop']} | {m['the']} | {m['loi']} |")
o.append('\n## Chi tiết: hình + nguồn (trích nguyên văn)\n')
for m in d['diem_nhan']:
    o.append(f"### {m['ma']} — {m['ngay']} · {m['noi']}\n- **Hình:** {m['hinh']}")
    for s in m['nguon']:
        u = s.get('url', ''); dong = s.get('dong', '')
        o.append(f"- Nguồn: `{s['tep']}`" + (f" dòng {dong}" if dong and dong != '—' else '') + (f" · <{u}>" if u else '') + f" · đọc {s['ngay_doc']} · bậc **{s['bac']}**")
        for q in s['trich']: o.append(f"  > {q}")
    o.append('')
open(sys.argv[2], 'w').write('\n'.join(o) + '\n')
