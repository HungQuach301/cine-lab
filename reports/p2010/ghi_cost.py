#!/usr/bin/env python3
"""P-2010 · thêm dòng COST-LEDGER.csv (20 cột) cho NHẠC-T3, ĐÓNG-GÓI v1/v2, V7-PILOT, V7B, NC-V2V lượt 1/2, NC-CPU, NC-GPU, P-2010.
Số lấy từ báo cáo từng phiên (đường dẫn ở cột nguon). Kiểm mọi dòng đúng 20 cột."""
import csv, io, os, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); P = os.path.join(R, 'COST-LEDGER.csv')
s = open(P, encoding='utf-8').read(); H = next(csv.reader(io.StringIO(s))); assert len(H) == 20
if 'NC-GPU,' in s: sys.exit('DỪNG: đã có dòng NC-GPU')
P2010_GIO = sys.argv[1] if len(sys.argv) > 1 else '1.5'
G = 'ghi sổ bởi P-2010'
rows = [
 ['NHAC-T3', 'Nhạc T3: cue sheet A (MacLeod) / B (+8 bản Scott Buckley CC BY 4.0), trộn thử, gói nghe mù 4 cặp', 'R&D', '2026-10-19', '', '', '', '', '0', '', 'không gọi API', '0', '0', '0.9', '', '0', '', '',
  'reports/nhac-t3/NHAC-T3-BAO-CAO.md dòng 22–24 (nhánh nhac-t3 @af4208ed)', f'YouTube 0; OpenAI 0; ElevenLabs 0; mua nhạc 0 (CC BY 4.0); Claude API 0, 0 subagent; giờ máy báo cáo không ghi — 0,9 h là ước theo thời gian thực 14:00–14:55 UTC; {G}'],
 ['DONG-GOI-T3', 'Đóng gói T3 v1: tiêu đề, thumbnail, kiểm cầu YouTube', 'Đóng gói', '2026-10-19', '', '', '', '', '0.959', '', 'claude-sonnet-5-5 (10 lệnh)', '0', '0', '0.7', '', '0', '', '',
  'reports/dong-goi-t3/DONG-GOI-T3-BAO-CAO.md dòng 232–236 (nhánh dong-goi-t3 @7b983213)', f'YouTube Data API 1 947 đơn vị (mốc 2 000: −2,65 %, trong ±5 %; lượt 1 1 121 lỗi + lượt 2 724 + kiểm cầu 101 + thử 1); OpenAI 0; ElevenLabs 0; Claude API $0,959 (cost.jsonl 0,9593; token vào 604 234, ra 43 255); giờ máy ≈ 0,7 h (ước từ log); {G}'],
 ['DONG-GOI-T3-V2', 'Đóng gói T3 v2: thumbnail V4/V5 ghép ảnh Flickr CC BY 2.0 + 4 ảnh gpt-image', 'Đóng gói', '2026-10-19', '', '', '', '', '0.486', '', 'claude-sonnet-5-5 (9 lệnh); gpt-image-2.5-sunburst-2026-09-08', '0', '0', '0.8', '', '0', '', '',
  'reports/dong-goi-t3-v2/DONG-GOI-V2-BAO-CAO.md dòng 157–161 (nhánh dong-goi-t3-v2 @76abba56)', f'OpenAI $0,303 (4 ảnh × ≈ $0,076; 3 lệnh lỗi 400/502/502 tính $0; goi-api.jsonl 0,3034); YouTube 0; ElevenLabs 0; Claude API $0,486 (cost.jsonl 0,4862; token vào 550 973, ra 6 585); giờ máy ≈ 0,8 h (ước); báo cáo ghi kết thúc 16:50 UTC nhưng commit cuối 15:56; {G}'],
 ['V7-PILOT', 'V7P: bản thử ngữ pháp hình timelapse TL-1…TL-6 + chấm xem câm', 'R&D', '2026-10-19', '', '', '', '', '0.230', '', 'claude (3 lượt chấm xem câm)', '0', '0', '4.3', '', '0', '', '',
  'reports/v7p/V7P-BAO-CAO.md dòng 209–212 (nhánh ccr-f96ee5b5-2ec2i5 = v7-pilot @71932a3f; vào main qua V7B)', f'OpenAI 0; ElevenLabs 0; YouTube 0; Claude API $0,230 (cost.jsonl 0,2301); giờ máy ≈ 4,3 h; phiên chưa có dòng sổ — P-2010 bổ sung; {G}'],
 ['V7B', 'V7B: bản dựng timelapse T3 (nối V7P) + xem câm', 'R&D', '2026-10-19', '', '', '', '', '0.657', '', 'claude -p (9 lệnh)', '0', '0', '5.5', '', '0', '', '',
  'reports/v7b/V7B-BAO-CAO.md dòng 18, 249–256, 272–274 (nhánh ccr-ef2b66f0-9639kq @317dcf51)', f'OpenAI 0; ElevenLabs 0; YouTube 0; Claude API $0,657 theo báo cáo (xem-cam/cost.jsonl 9 dòng cộng 0,655 — lệch $0,002); giờ máy ≈ 5,5 h đồng hồ bận máy; {G}'],
 ['NC-V2V-1', 'NC-V2V lượt 1: thử Gemini Omni video→video — khoá không hợp lệ', 'R&D', '2026-10-19', '', '', '', '', '0', '', 'không gọi API Claude', '0', '0', '0', '', '0', '', '',
  'reports/nc-v2v/NC-V2V-BAO-CAO.md dòng 312–322 (nhánh nc-v2v @811b8ff8)', f'Gemini $0 (2 lệnh GET trả 400 API_KEY_INVALID, 16:33–16:34 UTC); OpenAI 0; ElevenLabs 0; YouTube 0; giờ máy ≈ 0; {G}'],
 ['NC-V2V-2', 'NC-V2V lượt 2: Gemini Omni video→video, bộ đo bịa T1–T6, chấm mù', 'R&D', '2026-10-19', '', '', '', '', '0.262', '', 'claude sonnet + haiku (chấm mù); gpt-6.1-sol; Gemini Omni', '0', '0', '2.2', '', '0', '', '',
  'reports/nc-v2v/NC-V2V-BAO-CAO.md dòng 15, 20, 241–245, 299 (nhánh nc-v2v @2c1d1e12)', f'Gemini $17,00 theo sổ phiên (so-ai.jsonl 21 lệnh: 16×200, 1×502, 4×402; cộng 16,9993) — vượt mốc theo dõi $15 (+13 %), trả trước cạn (HTTP 402); hoá đơn Google ₫453.145 (chủ dự án cung cấp trong lệnh P-2010; không có trong repo; cả hoá đơn thuộc lượt 2 vì lượt 1 $0); OpenAI $0,046 (ước; 11 711 token vào, 2 205 ra); Claude API $0,262 (R1 sonnet 0,243 + R3 haiku 0,019); ElevenLabs 0; YouTube 0; giờ máy CPU ≈ 2,2 h; {G}'],
 ['NC-CPU', 'NC-CPU: so cách A (three.js + nướng) / B (Cycles CPU) / C (Eevee llvmpipe), chấm mù 18', 'R&D', '2026-10-19', '', '', '', '', '1.10', '', 'claude-sonnet (18 lượt)', '0', '0', '7.2', '', '0', '', '',
  'reports/nc-cpu/NC-CPU-BAO-CAO.md dòng 16, 186–190 (nhánh claude/clever-franklin-daez5k = nc-cpu @718dec9e)', f'OpenAI 0; ElevenLabs 0; YouTube 0; không thuê GPU; Claude API $1,10 (cost.jsonl 19 dòng 1,1004); giờ máy CPU ≈ 7,2 h; {G}'],
 ['NC-GPU', 'NC-GPU: Cycles GPU RTX 5090 thuê (RunPod) cho cú lặn/cận đêm, chấm mù G0/G1/G2', 'R&D', '2026-10-20', '', '', '', '', '1.036', '', 'claude-sonnet (18 lượt)', '0', '0', '2.7', '', '0', '', '',
  'reports/nc-gpu/NC-GPU-BAO-CAO.md dòng 20, 52–54, 227–232 (nhánh claude/eloquent-dijkstra-kemr8j @4fe45ec3)', f'RunPod $10,98 thật (số dư 25,00 → 14,02; 8 pod RTX 5090 SECURE $1,19/h, 10,70 h; giá × giờ = $12,74 — RunPod tính theo giây, số dư cập nhật trễ); mốc theo dõi $12 (−8,5 %); ≈ 2,3 h pod (≈ $2,7) lãng phí do lỗi vận hành (BAI-HOC #115); Claude API $1,036 (cost.jsonl 1,0359); OpenAI 0; Gemini 0; ElevenLabs 0; YouTube 0; giờ máy CPU ≈ 2,7 h + 10,70 h GPU pod; {G}'],
 ['P-2010', 'Merge 5 nhánh (V7B, NHẠC-T3, ĐÓNG-GÓI v2, NC-V2V, NC-GPU+NC-CPU) vào main, Kinh thánh §14 (N1/N2, G0), sổ, tra nguồn thực vật 1782, tìm master giọng KL42', 'P', '2026-10-20', '', '', '', '', '0', '0', 'không gọi API', '0', '0', P2010_GIO, '', '0', '', '',
  'reports/p2010/P2010-BAO-CAO.md', 'YouTube 0; OpenAI 0; Gemini 0; Claude API 0 (3 subagent đọc repo trong phiên, không gọi API riêng); ElevenLabs 0 ký tự (2 lệnh GET subscription + 1 GET history bị 401 thiếu quyền speech_history_read); GET archive.org 5 tệp djvu (SHA khớp đăng ký T3b) + api.polyhaven.com/info 3 lệnh + polyhaven.com/license; giờ máy = thời gian thực (mốc theo dõi 2 h); ghi sổ bởi P-2010'],
]
buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n')
for r in rows:
    assert len(r) == 20, (r[0], len(r)); w.writerow(r)
out = s.rstrip('\n') + '\n' + buf.getvalue()
for i, r in enumerate(csv.reader(io.StringIO(out))):
    assert len(r) == 20, (i + 1, len(r))
open(P, 'w', encoding='utf-8').write(out); print('thêm', len(rows), 'dòng; mọi dòng sổ 20 cột')
