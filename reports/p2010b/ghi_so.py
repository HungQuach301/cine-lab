#!/usr/bin/env python3
"""P-2010b · việc 4: RIGHTS (dòng DG3V2-AI đọc thẳng từ reports/dong-goi-t3-v2/ai/goi-api.jsonl; mẫu ghi công "(edited)" duyệt; 8 tệp nhạc nay ở LFS)
+ AUTHORSHIP (4 dòng nguyên văn do chủ dự án đưa trong lệnh P-2010b). Mỗi thay thế kiểm số lần xuất hiện; dòng mới kiểm 10 cột (RIGHTS) / 6 cột (AUTHORSHIP). Chạy một lần."""
import json, os, re, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
rd = lambda p: open(os.path.join(R, p), encoding='utf-8').read()
G = [json.loads(l) for l in open(os.path.join(R, 'reports/dong-goi-t3-v2/ai/goi-api.jsonl'))]
OK = [g for g in G if g.get('http') == 200 and g['anh'] in ('F1-N12', 'F2-N2r', 'F3-N12-2026')]
assert len(OK) == 3 and all(g['c2pa'] and g['model_resp'] == g['model_req'] for g in OK)
LIC = re.search(r'^\| P1810B-AI \|(?:[^|]*\|){4}([^|]*)\|', rd('RIGHTS.md'), re.M).group(1).strip()
LIC = LIC[:LIC.index('Output."') + len('Output."')]   # chỉ câu §4.1 nguyên văn
P = {}
for g in OK: P.setdefault(g['prompt'], []).append(g['anh'])
anh = ' · '.join(f"**{g['anh']}** ({g['date_utc']}; vào `{g['input']['file']}` {g['input']['sha256']} → ra `{g['file']}` {g['sha256']}; {g['size_resp']} JPEG q90; ${g['usd']}; C2PA có: {'+'.join(g['c2pa_segments'])})" for g in OK)
lenh = ' '.join(f"Lệnh nguyên văn ({', '.join(v)}): \"{k}\"" for k, v in P.items())
dong = ('| DG3V2-AI | 3 ảnh AI tăng cường thumbnail T3 (ĐÓNG-GÓI v2 §2, ứng viên V1/V2/V3/V7/V8): ' + anh + '. F2: 3 cờ Union ghép lại điểm ảnh gốc '
        '(elip 60×60 px @2560, `ai/co-px.json`). F4 (D2026n) LOẠI (AI thêm kiến trúc) — không thuộc dòng này. ' + lenh +
        ' Tham số: `POST /v1/images/edits`, quality high, stream + partial_images 1 (3 lệnh lỗi 400/502 trước đó không tạo ảnh, không tính tiền) '
        '| Ảnh sửa bằng AI (OpenAI) từ khung tự dựng V7B | sổ gọi API `reports/dong-goi-t3-v2/ai/goi-api.jsonl` (model, ngày, prompt, SHA vào/ra, C2PA), tờ so `reports/dong-goi-t3-v2/ai/so-*.jpg` '
        f'| sinh bởi `{OK[0]["model_resp"]}` (model trả về đúng bản ghim) theo lệnh phiên ĐÓNG-GÓI-T3 v2, 19/10/2026 | ' + LIC + ' (nguyên văn như dòng P1810B-AI) '
        '| Thumbnail T3 (YouTube) theo Kinh thánh §14.5 (thumbnail từ render của ta, AI tăng cường theo N1) + §14.1 (e) cổng kiểm; bán phim / LHP: chỉ khi thumbnail/poster được chọn và qua cổng; công bố AI theo §14.1 (f). Chọn ứng viên: chờ chủ dự án '
        '| Không bắt buộc (đầu ra thuộc khách hàng); công bố AI trong mô tả (§10.6) | ' + ' / '.join(f"{g['anh']} {g['sha256']}" for g in OK) + ' | 2026-10-20 |')
assert dong.count(' | ') >= 9 and len(dong.split(' | ')) == 10, len(dong.split(' | '))
s = rd('RIGHTS.md'); a = s.index('| DG3V2-PH2 |'); b = s.index('\n', a) + 1
assert '| DG3V2-AI |' not in s
s = s[:b] + dong + '\n' + s[b:]
SUA = [('— chữ "(edited)" theo CC BY 4.0 §3(a)(1)(B), NHAC-T3 §2.2; chờ chủ dự án duyệt mẫu',
        '— chữ "(edited)" theo CC BY 4.0 §3(a)(1)(B), NHAC-T3 §2.2; **chủ dự án duyệt mẫu 20/10 22:34**', 8)]
for t in ('sb_intervention_nomelody', 'sb_signaltonoise_nomelody', 'Katabasis_I', 'Juggernaut', 'sb_neverdying', 'sb_undertow', 'Echoes', 'sb_hiraeth'):
    SUA.append((f'Tệp `{t}.mp3` ngoài git, **chưa vào `assets/`**', f'Tệp `assets/k2/music/{t}.mp3` (LFS từ P-2010b 20/10; SHA khớp, `assets/k2/music/SHA256SUMS`)', 1))
for cu, moi, n in SUA:
    if s.count(cu) != n: sys.exit(f'DỪNG RIGHTS: "{cu[:60]}" {s.count(cu)} lần (cần {n})')
    s = s.replace(cu, moi)
open(os.path.join(R, 'RIGHTS.md'), 'w', encoding='utf-8').write(s)
CD = 'Chủ dự án'
A = [('2026-10-19', 'Kênh 2 K2C-T3-01 — nhạc T3, nguyên văn lệnh chọn (trước 22:24; P-2010b ghi, bổ sung dòng P-2010 "nghe mù 1X–4X")',
      'Nguyên văn: "Tôi chọn 1x,2x,3x,4x". Giờ chính xác: không có trong repo — chủ dự án nêu "trước 22:24" (lệnh P-2010b). Giải mã theo `reports/nhac-t3/nghe-mu/khoa.json`: B, B, B, A (xem dòng P-2010)',
      'Chủ dự án chọn bằng tai, mù, ở cả 4 cặp', 'NHẠC-T3: cue sheet A/B, gói nghe mù', CD),
     ('2026-10-19', 'Luật kiểm 1.16.1 + nhạc miễn phí (22:24; P-2010b ghi, bổ sung dòng P-2010 "ba điểm xác nhận")',
      'Nguyên văn (như chủ dự án chép trong lệnh P-2010b, dấu "…" có sẵn trong lệnh; phần lược không có trong repo): "Đồng ý Xác nhận 3 điểm của K-1.16.1 … Vẫn thiên về phương án nhạc free tránh rủi ro không đáng có"',
      'Chủ dự án quyết cách đọc luật kiểm và chọn hướng rủi ro thấp cho nhạc (chỉ nhạc miễn phí có giấy phép rõ — Kinh thánh §14.6)', 'Phương án: phiên K-1.16.1; NHẠC-T3', CD),
     ('2026-10-19', 'Kênh 2 — duyệt NC-V2V (23:21; P-2010b ghi, bổ sung dòng P-2010)',
      'Nguyên văn: "duyệt phiên thử NC-V2V"', 'Chủ dự án đọc kết quả, quyết hướng nghiên cứu tiếp', 'Phiên NC-V2V: số đo, bộ đo bịa', CD),
     ('2026-10-20', 'Kênh 2 — duyệt 8 điểm báo cáo P-2010 §9 + bật quyền lịch sử ElevenLabs (22:34; P-2010b ghi)',
      'Nguyên văn: "duyệt 8 điểm của phiên P-2010; Đã bật quyền History". Áp ở P-2010b (`reports/p2010b/P2010B-BAO-CAO.md`): (1) lấy lại master giọng KL42 từ lịch sử, 0 ký tự; (2) giữ 0,45 TẠM bậc 5 + hai ràng buộc có nguồn (cọ lùn; tông khô 9/1782) → Kinh thánh §14.4; '
      '(3) câu minh bạch §10.6 theo bản nháp P-2010 §9 mục 3; (4) ba chỗ vênh: §11.3 bão hoà theo §14.4, §11.3 "Được dùng" là ví dụ của N1, bỏ tên làm việc "14 Times" (khuôn §14.5); xác nhận sửa §12.5 Cycles/cú lặn; '
      '(5) mẫu ghi công nhạc có "(edited)" + 8 MP3 vào LFS `assets/k2/music/`; (6) RIGHTS DG3V2-AI; (7) AUTHORSHIP nguyên văn (các dòng trên); (8) giao phiên K V2V-D4 / chờ NC-V2V3 (ngoài phạm vi P-2010b)',
      'Chủ dự án quyết câu công bố AI gửi khán giả (§10.6), ràng buộc look thực vật 1782, khuôn tiêu đề, mẫu ghi công', 'P-2010: phương án, bản nháp §10.6, tra nguồn thực vật; P-2010b: áp dụng', CD)]
s = rd('AUTHORSHIP.md'); assert s.endswith('\n') and 'P-2010b ghi' not in s
add = ''.join('| ' + ' | '.join(r) + ' |\n' for r in A); assert all(len(r) == 6 for r in A)
open(os.path.join(R, 'AUTHORSHIP.md'), 'w', encoding='utf-8').write(s + add)
print('RIGHTS +1 dòng (DG3V2-AI) + 16 sửa; AUTHORSHIP +4')
