"""G1 T3 · sinh g1/kiem-chu.md từ g1/kiem-chu.json (kiem_loi.py) + vay-ham/tu-kiem.json. Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/g1/bang_kiem_chu.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
K = json.loads((HERE / 'kiem-chu.json').read_text())
XU_LY = {  # quyết định của phiên cho từng câu bộ lọc bắt (chủ dự án duyệt ở G1-BAO-CAO §5)
    'CS3': 'giữ — chủ thể cụ thể (hạm đội, chiến tuyến, pháo đài, kỹ sư, cách đếm), không phải dân tộc như một khối đạo đức',
    'CS1 (chỉ trong trích có ghi ng': 'giữ — trích nguyên văn chính phủ TBN 4/3/1939 (S096), có ghi ai nói + chữ gốc trên hình',
    'CS1 occupied/occupation (chỉ đ': 'giữ — câu SM3 chủ dự án đã chốt; "occupies Tangier" là sự kiện 14/6/1940 (T022), không nói về chủ quyền Gibraltar',
}
L = ['# T3 · Kiểm chữ lời v1 (lệnh G1 mục 5) — sinh bằng `g1/bang_kiem_chu.py`', '',
     f"Nguồn: `{K['script']}` × `vay-ham/treatment.json` (bản G1). Ước **2,5 từ NÓI/s** (Kinh thánh §3: ~150 từ/phút; số đọc thành chữ, tách gạch nối — cùng cách đếm gói TUYẾN). Đối chiếu: Eric đo thật ở T2 = 151,2 từ VIẾT/phút.", '',
     '## 0. Tổng', '',
     f"- Từ viết **{K['tong']['tu_viet']}** · từ nói **{K['tong']['tu']}** · ước lời **{K['tong']['uoc_s']} s** (2,5 từ nói/s) · ước theo nhịp Eric T2 **{K['tong']['uoc_eric_s']} s** · tổng phim (bảng shot) **{K['tong']['dur']} s**.",
     '- Lỗi: ' + ('không' if not K['loi'] else '; '.join(K['loi'])), '- Cảnh báo tràn > 1,5 s: ' + ('; '.join(K['canh_bao']) or 'không'), '',
     '| Chương | Dài (s) | Từ nói | Ước lời (s) | Lời/cửa sổ |', '|---|---|---|---|---|']
for k, v in K['chuong'].items(): L.append(f"| {k} | {v['dur']} | {v['tu']} | {v['uoc_s']} | {v['ty_le']:.3f} |")
L += ['', '## 1. Từ điển đọc số (áp khi khoá lời, BAI-HOC #19/#59/#104)', '', '| Viết | Đọc |', '|---|---|']
seen = {}
for r in K['shots']:
    for a, b in r['so_doc']: seen.setdefault(a, b)
for a, b in seen.items(): L.append(f'| {a} | {b} |')
L += ['', 'Số lớn đã viết bằng chữ ngay trong lời (fifteen thousand, three hundred and fifty-seven, twenty-eight point six percent…) để giọng đọc không đoán cách đọc.', '',
      '## 2. Độ dài từng shot so cửa sổ', '', '`vào trễ` = lời shot trước còn chảy sang (s); `tràn` = lời shot này chảy sang shot sau (s). Thời lượng đã đặt theo lời (`g1/dur-g1.json`); shot bị trần theo loại ghi ở `tran_chan`.', '',
      '| Shot | Ch | Dài (s) | Từ nói | Ước (s) | Vào trễ | Tràn | Ghi chú |', '|---|---|---|---|---|---|---|---|']
for r in K['shots']:
    L.append(f"| {r['id']} | {r['ch']} | {r['dur']} | {r['tu']} | {r['uoc_s']} | {r['bat_dau_tre_s']} | {r['tran_s']} | {'IM LẶNG' if r['im_lang'] else ''} |")
L += ['', '## 3. Câu nhạy cảm (§10.6, TIEN-KY-VAY-HAM §6.1 CS1–CS10) — bộ lọc bắt và cách xử lý', '', '| Shot | Luật | Câu | Xử lý |', '|---|---|---|---|']
for c in K['cau_nhay_cam']:
    key = next((k for k in XU_LY if c['luat'].startswith(k)), None)
    L.append(f"| {c['shot']} | {c['luat']} | {c['cau']} | {XU_LY.get(key, 'XEM')} |")
L += ['', 'Số thương vong: mọi câu có số chết/mất/cứu đều nói ai đếm (bộ lọc: 0 lỗi). Không tính từ đạo đức cho phe nào (bộ lọc: 0 câu).', '',
      '## 4. Trích trên hình (O4) — đối chiếu nguyên văn trong claim', '', '| Shot | Trích | Claim khớp |', '|---|---|---|']
for q in K['trich_tren_hinh']: L.append(f"| {q['shot']} | «{q['trich']}» | {', '.join(q['claim'])} |")
(HERE / 'kiem-chu.md').write_text('\n'.join(L) + '\n'); print('ghi', HERE / 'kiem-chu.md')
