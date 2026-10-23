# Luật kênh 2 (checks 1.17.2) — k2c-t3-anim — TRƯỢT

| Mục | Kiểm | Kết quả | Cấp (1.12.1) | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) |
|---|---|---|---|---|---|---|
| Q26b | Đa dạng bối cảnh (1.16: cảnh tl/* theo vùng) | **ĐẠT** |  | 38 bối cảnh · lớn nhất tl/t3tl · C-lai 5.4 % · liên tục dài nhất tl/t3tl · D-cong-thap → F-hang-rao 31.5 s · nửa sau 18 · trung tính 0.0 % | ≤ 25 % · ≤ 90 s · nửa sau ≥ 3 |  |
| Q32 | Footage/ảnh nguồn ngoài | **ĐẠT** |  | không dùng footage ngoài | ≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5× |  |
| Q33 | Lặp cảnh (1.17: miễn cùng điểm máy năm khác — TL-1) | **ĐẠT** |  | 43 góc máy · 43 lần xuất hiện · nhiều nhất tl/t3tl · anim_C1 1 lần · 0 góc > 2 · chưa đo pHash (không có master) · miễn năm khác (1.17, TL-1) 0 | ≤ 2 lần |  |
| Q34 | Loại shot | **ĐẠT** |  | 45/45 shot có type · scene3d 97.9 % · card 2.1 % · số neo 3D 100 %, chỉ card 0 % (0 số) · địa danh 0 · nhân vật 0 | type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document ≤ 3 s · record ≤ 12 s + dòng tô + nguồn |  |
| Q35 | Nhãn loại số (D5) | **ĐẠT** |  | mô hình đặc tả · 96 khung xét · ACTUAL nhiều nhất 0/khung · lỗi a 0 · b 0 · c 0 · d 0 | ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL |  |
| Q36 | Chữ trên màn hình | **ĐẠT** |  | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực (+ 1 lần trong câu miễn trừ 0:00–0:15) |  |
| Q37 | Nhịp thị giác (1.16: miễn khung neo/im lặng ≤ 10 s) | **TRƯỢT** |  | 761.0 s · biến cố khai 146 (gộp 146) · TB 5.21 s · dài nhất 12.71 s · khung tĩnh: không đo (không có master) · miễn khung neo/im lặng (1.16): 0 khoảng, dài nhất trước miễn 12.71 s | TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s |  |
| A1–A13 | Âm thanh (tập cũ — chỉ báo) | **CHỈ BÁO** |  | CHỈ BÁO · A1 không có master · A2 không có master · A5 không có master · A7 không có master · A4 KHÔNG ÁP (không có lời — 1.16) · A8 KHÔNG ÁP (không có lời — 1.16) | docs/AUDIO-THUOC-DO.md |  |
| ML1 | Mạch truyện | **ĐẠT** | Chặn (b), (c) · Cảnh báo (a) ở T3 (Chặn từ T4) — lỗi Chặn 0, Cảnh báo 0 | 41/45 shot gắn (0 suy từ mốc @từ) · timelapse 761.0 s, trôi 4.2 % | mỗi shot gắn câu/claim · timelapse trôi ≤ 15 % |  |
| ML2 | Lời lặp ý | **ĐẠT** | Chặn có giải trình (người quyết; không vào mã thoát tự động) — lỗi Chặn 0, Cảnh báo 0 | 0 câu · 0 cặp ứng viên (chấm 0) · 0 lặp ý · không khai tóm tắt | n-gram/IDF + chấm ngữ nghĩa ghim mô hình; ngoài tóm tắt cuối |  |
| ML3 | Lời mời đăng ký | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 câu mời: không có · 0 luận điểm chính khai | 60 s cuối hoặc ±5 s ranh chương · không trong 20 s trước luận điểm chính |  |
| FT1 | Chỉ báo footage/ảnh | **ĐẠT** | Cảnh báo (20 % footage đã Chặn ở Q32 b2) — lỗi Chặn 0, Cảnh báo 0 | 0 shot footage/ảnh · tính 0.0 s = 0.0 % (miễn ảnh nhỏ 0.0 s) · khai lý do: 0/0 | ≤ 20 % (trần) · mỗi shot có lý do · ảnh ≤ 1/3 khung ≤ 6 s không tính |  |
| NHIP-K2 | Nhịp kênh 2 (Q14–Q18 không áp → Q37) | **TRƯỢT** | Chặn (như Q37) — lỗi Chặn 88, Cảnh báo 0 | Q37: 761.0 s · biến cố khai 146 (gộp 146) · TB 5.21 s · dài nhất 12.71 s · khung tĩnh: không đo (không có master) · miễn khung neo/im lặng (1.16): 0 khoảng, dài nhất trước miễn 12.71 s | TB ≤ 3,5 s · dài nhất ≤ 6 s |  |
| Q26b-K2 | Đa dạng loại cảnh + vùng | **CẢNH BÁO** | Chặn (c), (d), (e) (như Q26b) · Cảnh báo (a), (b) — lỗi Chặn 0, Cảnh báo 3 | loại: 3d 97.9 %, the_so 2.1 % · 37 vùng, lớn nhất C-lai 5.4 % · nửa sau 18 vùng · không vùng 2.1 % | ≥ 3 loại/nửa · loại ≤ 70 % · vùng ≤ 25 %, ≤ 90 s, nửa sau ≥ 3 |  |
| Q33-K2 | Lặp cảnh (vùng, góc) + pHash L/ΔE | **TRƯỢT** | Chặn (như Q33) — lỗi Chặn 1, Cảnh báo 0 | 43 khoá (vùng, góc) · 43 lần xuất hiện · nhiều nhất tl/t3tl · anim_C1 1 · 0 khoá > 2 | ≤ 2 lần (miễn: khác chương + khác năm/lớp; 1.17: năm log shot không chồng — TL-1) |  |
| Q32b-K2 | Trần clip/ảnh | **ĐẠT** | Chặn (như Q32b) — lỗi Chặn 0, Cảnh báo 0 | 0 clip/ảnh ·  | footage ≤ 8 s · ảnh có máy/chú thích đổi ≤ 12 s · ảnh tĩnh ≤ 8 s |  |
| NC-H1 | Thành phố có nhà | **TRƯỢT** | Chặn (a), (b) (đúng lỗi chủ dự án nêu ở T2) — lỗi Chặn 2, Cảnh báo 0 | 18 shot thành phố (234.8 s; khai 18, suy 0) · có lớp nhà khai 16 · không lớp nhà 2 · không đo fabric 16 | fabric trung vị ≥ 25 % · không khung < 15 % (trừ ≤ 3 s cuối reveal) |  |
| NC-H2 | Địa cầu | **CẢNH BÁO** | Chặn (a), (b) — lỗi Chặn 0, Cảnh báo 1 | 0 lần · 0.0 s (0.0 % phim) · map/globe 0.0 s · bản đồ nổi tầm cao 0.0 s · dài nhất 0 s | AGL > 50 km: ≤ 1 lần/tập · ≤ 3 s/lần |  |
| NC-H3 | Tầm mặc định | **CẢNH BÁO** | Cảnh báo — lỗi Chặn 0, Cảnh báo 1 | 3D địa lý 0.0 s · AGL ≤ 60 km 0.0 % · ≤ 3 km 0.0 % · có thành phố: có | AGL ≤ 60 km ≥ 70 % 3D · có thành phố: AGL ≤ 3 km ≥ 40 % |  |
| NC-H4 | Nơi có tên | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 shot bản đồ · chip nơi 0 · nhãn địa danh 0 · thiếu 0 (nguồn: đặc tả, không log chữ) | mọi shot bản đồ: chip nơi hoặc nhãn địa danh |  |
| NC-H5 | Đúng thời kỳ | **ĐẠT** | Chặn (a) · Cảnh báo (b) — lỗi Chặn 0, Cảnh báo 0 | tập không có bộ đếm năm (cảnh tl/* có opt.year/counter, hoặc p.counter) | năm xây ≤ bộ đếm (nam_khung) · ghost có nguồn + nguồn trong mô tả (§12.1: không nhãn trên hình) |  |
| Q7/Q8-K2 | Nhãn/loại số nhận estimate (khiếu nại TT5 i) | **ĐẠT** | Chặn (thay Q7/Q8 cho kênh 2, như Q35) — lỗi Chặn 0, Cảnh báo 0 | Q7 nhận ESTIMATE: 0 lỗi (không log: chỉ kiểm kind khai) · Q8 loại số: 0 lỗi | kind ∈ actual/projection/estimate (kênh 2) · đủ nhãn, không thừa nhãn |  |
| Q33 (1.13) | Lặp cảnh — pHash bỏ lớp chữ cố định | **ĐẠT** | Chặn (thay Q33 cho kênh 2) — lỗi Chặn 0, Cảnh báo 0 | 43 góc máy · 43 lần xuất hiện · nhiều nhất tl/t3tl · anim_C1 1 lần · 0 góc > 2 · chưa đo pHash (không có master) · miễn năm khác (1.17, TL-1) 0 | ≤ 2 lần · pHash L vùng nội dung y 18–72 %, θ 16 · 1.17: miễn cùng điểm máy năm khác (TL-1) |  |
| Q36 (1.13) | Chữ — câu miễn trừ nhận theo chữ | **ĐẠT** | Chặn (thay Q36 cho kênh 2) — lỗi Chặn 0, Cảnh báo 0 | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | "This video explains… Facts as of" 1 lần trong 0:00–0:15 không đòi nguồn luật |  |
| Q37 (1.13) | Nhịp — khung tĩnh theo khung neo | **TRƯỢT** | Chặn (thay Q37 cho kênh 2) — lỗi Chặn 88, Cảnh báo 0 | 761.0 s · biến cố khai 146 (gộp 146) · TB 5.21 s · dài nhất 12.71 s · khung tĩnh: không đo (không có master) · miễn khung neo/im lặng (1.16): 0 khoảng, dài nhất trước miễn 12.71 s | khung tĩnh (mọi khung khác khung đầu quãng < 2,0/255) ≤ 6 s |  |
| BD-1…BD-8 | Bản đồ chiến lược / inset / ranh | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | không có shot strategic, lớp ranh, tuyến hay inset |  |  |
| K-R1…K-R9 | ĐỎ-K | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập không khai rui_ro: do-k |  |  |
| K-LAI-1 | LAI: thời lượng khung AI | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 28.40 s AI / 761.00 s (timeline) = 3.7 % · nguồn: log shot (4 đoạn minh hoạ + 0 shot ai_image), không có log khung | ai_image/ai_texture ≤ 20 % thời lượng (log khung; không có → đoạn khai trong log shot, 1.17.2) |  |
| K-LAI-2 | LAI: công bố AI (§12.1) | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 2, Cảnh báo 0 | thẻ phương pháp có (1.17.2: không đòi câu AI) · mô tả không · log chữ không · cờ AI: log shot | cờ ai_* mọi khung (hoặc mọi shot log) · shot khai khớp log · mô tả "AI use = Yes" · KHÔNG nhãn trên hình (1.17.2: bỏ "thẻ PP nói AI") |  |
| K-LAI-3 | LAI: kiểm dữ kiện từng tấm C | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 4, Cảnh báo 0 | minh hoạ: 4 đoạn · kiểm ĐẠT 0 · thiếu tệp kiểm 4 | mỗi tấm C: loi_chac_cuoi 0 · nghi vấn đã xử lý · ngoại lệ có duyệt · không chấm mù |  |
| K-LAI-4 | LAI: vùng bảo vệ = A | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | sai khác TB < 1/255 trên mặt nạ bao_ve (PNG) |  |
| K-LAI-5 | LAI: một tấm, ban ngày, đêm ≤ 1,5× A | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | ≤ 1 tấm/khung neo × mốc · ≤ 2 lần sinh lại · chỉ lượt ngày · đêm ≤ 1,5× A |  |
| K-LAI-6 | LAI: sổ gọi API | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | — | model, prompt, % mặt nạ, usage, $, C2PA, giờ |  |
| K-LAI-B | LAI: bão hoà khung (P2-3) | **ĐẠT** | Cảnh báo (P2-3) — lỗi Chặn 0, Cảnh báo 0 | 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | bão hoà trung vị ≤ 0,40 mỗi khung LAI |  |
| K-LAI-3V | LAI: nghi vấn còn ghi của vân (1.16) | **ĐẠT** | Chặn ở cổng G2 (bản phát hành) · Cảnh báo ở animatic (K116-D5) — lỗi Chặn 0, Cảnh báo 0 | không có khung ai_texture | tệp vân dùng không còn nghi vấn chưa xử lý (Chặn ở G2 · Cảnh báo ở animatic — K116-D5) |  |
| O2 | Máy soi lỗi thời đại (lưới lọc thứ hai) | **CẢNH BÁO** | Cảnh báo (lưới lọc thứ hai — không thay kiểm nguồn) — lỗi Chặn 0, Cảnh báo 1 | — | 1 khung/5 s + khung neo · cờ/quân phục/tàu/đèn/xe/vật hiện đại/chữ/kiến trúc theo năm · không thay kiểm nguồn |  |
| SACH-1 | Khung sạch §12.1 + TL-4 | **TRƯỢT** | Chặn (a)–(f) (K116-D1; (e) chữ bản đồ Chặn theo K116-D3: ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ) — lỗi Chặn 1, Cảnh báo 0 | 45 shot · tấm số/trích 0 · tư liệu đứng riêng 0 · không log chữ | chỉ bộ đếm · chip nơi ≤ 3 s · thẻ chương · thẻ phương pháp · bản đồ ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ (K116-D3); không tấm số/trích, không tư liệu đứng riêng (phủ ≤ 3 s) |  |
| CHUONG-1 | Thẻ chương §13.3 | **ĐẠT** | Chặn (a)–(e) · Cảnh báo (f) vị trí/mờ (K116-D1) — lỗi Chặn 0, Cảnh báo 0 | 5 thẻ (đặc tả) · dài nhất 3.00 s · 0:44.2 1704 — The Rock changes hands; 2:53.5 1779 — The Great Siege; 6:23.0 1783 — The neutral ground; 7:52.0 1939 — A runway on the sand | ≤ 8/tập · "năm — ≤ 6 từ" · ≤ 3 s · không trong móc · trung tính | thẻ '1704 — The Rock chan' s 3.0 (ngưỡng 3.0); thẻ '1779 — The Great Sie' s 3.0 (ngưỡng 3.0); thẻ '1783 — The neutral g' s 3.0 (ngưỡng 3.0); thẻ '1939 — A runway on t' s 3.0 (ngưỡng 3.0); thẻ '1969 — The gate clos' s 3.0 (ngưỡng 3.0) |
| PP-1 | Thẻ phương pháp (D6) | **CẢNH BÁO** | Chặn (a)–(d) · Cảnh báo (e) tốc độ đọc ≤ 3 từ/s (K116-D1, D8: ≈ 8 s = 7–9 s) — lỗi Chặn 0, Cảnh báo 2 | 2 thẻ · PP1 8.0 s, PP2 8.0 s · 58 từ | 2 thẻ × 7–9 s, cuối phim · nguồn/bản đồ + chỗ ước tính (1.17.2: không đòi câu AI) · ≤ 3 từ/s |  |
| TL-1 | Xương sống timelapse §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; mục tiêu §13.6, hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 38 | thân phim 745.0 s · góc cao + tl 709.0 s (95.2 %) · đặc tả ≤ 3.54 cắt/phút (cận trên) · video 67 cắt = 5.40/phút (thô) − 0 cắt góc R3 (so_goc/goc_may) = 5.40/phút tính trần · đặc tả 44 ranh = 3.54/phút · khớp ±0.5 s 42 (chỉ video 25: 0:04.5, 0:15.4, 0:23.4, 0:23.8, 1:48.0, 2:11.2…; chỉ đặc tả 2 — cùng góc máy đổi năm/giờ hoặc chưa cắt) · trôi góc cao trung vị 0.18 %/s (39 shot) · ngưỡng hiệu chỉnh sau V7-PILOT | góc cao + thời gian chạy ≥ 75 % · ≤ 5 cắt/phút (video: đổi cấu trúc; đối chiếu đặc tả ±0,5 s; 1.17.2: cắt góc R3 so_goc/goc_may không tính trần) · trôi ≤ 2 %/s · 6–8 điểm máy (hiệu chỉnh sau V7-PILOT) |  |
| TL-2 | Lướt thấp §13.6 | **ĐẠT** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 0 | lướt thấp 4 shot · 36.0 s = 4.8 % · ngưỡng hiệu chỉnh sau V7-PILOT | lướt thấp ≤ 10 % · có vai, phố/người (hiệu chỉnh sau V7-PILOT) |  |
| TL-3 | Không shot trống §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 1 | 43 shot 3D · không đổi 0 · trống 0 · thiếu trong_pct 43 | mỗi shot 3D: thời gian chạy hoặc biến cố · trống ≤ 60 % (hiệu chỉnh sau V7-PILOT) |  |
| NHIP-NGHIA | Nhịp → vật mang nghĩa §13.2 | **ĐẠT** | Chặn (K116-D1; §13.2) — lỗi Chặn 0, Cảnh báo 0 | 71/71 nhịp chính có vật mang nghĩa = 100.0 % | ≥ 90 % nhịp chính |  |
| XEM-CAM | Cổng XEM CÂM §13.4 | **TRƯỢT** | Chặn (K116-D1, D2; §13.4 bắt buộc từ T3) — lỗi Chặn 1, Cảnh báo 0 | — | 8 câu · 3 AI + chủ dự án · tắt tiếng · chủ dự án ≥ 6/8 VÀ TB AI ≥ 6/8 (K116-D2) |  |
| PC-1 | Thước phục chế §12.3 | **ĐẠT** | Cảnh báo (K116-D1; thước tạm, hiệu chuẩn trên ≥ 10 ảnh) — lỗi Chặn 0, Cảnh báo 0 | tập không khai phuc_che: (không dùng ảnh phục chế) | Δ cạnh mới so bicubic ≤ 1,0 điểm % · PSNR ≥ bicubic |  |
| MINH-HOA | Minh hoạ AI §14.1 (c) / §15 M-d | **TRƯỢT** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.1 (c) N2 / §15 M-d) — lỗi Chặn 4, Cảnh báo 0 | 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4) · 28.4 s = 3.7 % · lỗi kẹp 0 · AGL 0 · sổ AI 4 · nhãn: không bắt buộc (1.17.2) (đoạn khai mâu thuẫn ai_image: false: C4/M1 — K-LAI-2 (b)) | theo đoạn khai: ≤ 20 % · kẹp giữa 2 khung 3D · máy ≤ 40 m AGL · sổ AI mỗi đoạn (1.17.2: không nhãn bắt buộc) |  |
| EO-DAT-R1 | Eo đất R1 — chủ thể | **ĐẠT** | Chỉ báo ở mọi cổng — chủ dự án chấm bằng mắt (1.17.2, V2-D2 duyệt 22/10 11:09); in pixel thô + vùng nở 1,5 % bề ngang (§14.7 R1 "≥ 15–20 %") — lỗi Chặn 0, Cảnh báo 0 | không shot khai chu_the_eo_dat | chu_the_eo_dat: chủ thể ≥ 15 % khung · 15–20 % (§14.7) — CHỈ BÁO mọi cổng, in pixel thô + vùng nở 1.5 % (1.17.2) |  |
| EO-DAT-R2 | Eo đất R2 — cỏ/cát trống | **TRƯỢT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R2: trống > 50 % ≤ 6 s liên tục, ≤ 10 % thời lượng chương) — lỗi Chặn 18, Cảnh báo 0 | 18 shot eo đất · đo 0 · trống liên tục dài nhất 0.0 s · — | trống (> 50 %) liên tục ≤ 6 s · mỗi chương ≤ 10 % thời lượng chương (§14.7) |  |
| EO-DAT-R3 | Eo đất R3 — góc + biến cố | **TRƯỢT** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.7 R3) — lỗi Chặn 24, Cảnh báo 0 | 12/18 shot eo đất > 15 s · khoảng biến cố dài nhất: N1_6 9.0 s, C1 11.5 s, N2_10 10.2 s, N2_11 13.5 s, N3_1 13.8 s, N3_4 15.0 s, N4_1 21.2 s, N4_2 25.4 s | shot eo đất > 15 s: ≥ 2 góc · biến cố cách ≤ 6 s |  |
| EO-DAT-R4 | Eo đất R4 — câu lời không vật | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R4 + TL-4; lệnh K-1.17.1) — lỗi Chặn 0, Cảnh báo 0 | không shot khai loi_khong_vat_eo_dat | loi_khong_vat_eo_dat: noi ∈ pho/lau_dai/cang hoặc bản đồ phủ ≤ 3 s (§14.7, TL-4) |  |
| CONG-BO-1 | Công bố AI ở gói phát hành (1.17.2) | **CẢNH BÁO** | Chặn ở gói phát hành (`cong: phat_hanh` | `phat_hanh.goi: true`) · chỉ báo (Cảnh báo) ở mọi cổng trước — §14.1 (f), YouTube "AI use" — lỗi Chặn 0, Cảnh báo 2 | áp vì: 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4) · 4 shot log ai_image (H1, N1_4, C3, C5) · mô tả không khai · youtube_altered_content None | khung AI hoặc giọng tổng hợp → mô tả YouTube có câu "AI"/"synthetic" · phat_hanh.youtube_altered_content: true (Chặn ở gói phát hành) |  |
| N2P-1…6 | Luật N2+ (§15, từ T4) | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập trước T4 (không khai kenh2_tu_t4 / n2p) |  |  |
| LOCK | checks/ khớp LOCK (1.17.2) | **ĐẠT** |  | KHỚP |  |  |

## Âm thanh A1–A13
| Mục | Kiểm | Loại | Kết quả | Giá trị | Ngưỡng |
|---|---|---|---|---|---|
| A1 | Loudness tích hợp | chặn | BÁO | không có master |  |
| A2 | Đỉnh thật sau AAC | chặn | BÁO | không có master |  |
| A3 | LRA | báo | — | không có master | báo |
| A4 | Lời trên nhạc (SMR) | chặn | — | KHÔNG ÁP (không có lời — 1.16) | p10 ≥ 15 · min ≥ 12 |
| A5 | Lặng bất thường | chặn | BÁO | không có master |  |
| A6 | Tỉ lệ lặng | báo | — | không có master | báo |
| A7 | Chạm trần | chặn | BÁO | không có master |  |
| A8 | Chồng lời | chặn | — | KHÔNG ÁP (không có lời — 1.16) | 0 |
| A9 | ASR hai cách nghe | chặn | — | KHÔNG ÁP (không có lời — 1.16) | 100 % đoạn |
| A10 | Quãng không lời > 8 s không khai khoảnh khắc nhạc | báo | — | KHÔNG ÁP (không có lời — 1.16) | > 8 s (báo) |
| A11 | Giao nhạc | chặn | — | không đo (mix.json không phải chuỗi mới) | ≤ 1 ô nhịp · không lặp |
| A12 | Loudnorm tuyến tính | chặn | — | không đo (mix.json không phải chuỗi mới) | linear |
| A13 | Đồng bộ tiếng | báo | — | KHÔNG ÁP (không có lời — 1.16) | báo |

## Chi tiết lỗi
### Q37
- (a) H1 3.41s loi "To walk in from Spain, you c": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1 6.67s loi "Since July 2026, this gate h": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2 3.23s loi "Historians on both sides cou": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H3 5.67s loi "So why, today, is the fight ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_1 6.50s loi "That summer, their fleet sai": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_1 10.79s loi "Its commanders, Admiral Geor": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 0.89s loi "This plan, printed in 1705, ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 10.50s loi "Inside, Governor Diego de Sa": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 19.28s loi "He refused to surrender.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 21.39s loi "The fleet answered with some": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_3 9.50s loi "British accounts put the def": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_4 5.13s loi "By a British account, almost": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_5 16.55s loi "The treaty names the town, c": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_5 25.49s loi "Britain said in 2015 that Gi": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_6 6.07s loi "Spain tried again in 1727.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_6 9.20s loi "Neither siege took it.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 6.38s loi "On the twenty-first of June ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 12.47s loi "Spain had joined France in i": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 16.05s loi "By October, British intellig": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 4.95s loi "Based at Algeciras, its boat": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C3 11.14s loi "The food had to come by sea.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C4 7.99s loi "Scurvy spread, until a Danis": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C5 10.07s loi "The townspeople fled south.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_6 3.87s loi "A British officer blamed "re": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_6 8.46s loi "By British tallies, the two ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_10 4.01s loi "By early July, Sergeant Ince": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_10 13.79s loi "A Spanish historian wrote it": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 8.71s loi "On the eighth of September, ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 8.68s loi "The Duc de Crillon led the s": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 12.14s loi "Their answer to red-hot shot": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 18.85s loi "A French account says he'd a": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 23.11s loi "It was refused.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 0.57s loi "The thirteenth of September ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 4.32s loi "That morning, the batteries ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 9.25s loi "At ten twenty-five, by the S": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 17.24s loi "By the next afternoon, all t": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 21.50s loi "Over two thousand attackers ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 3.57s loi "The blockade never forced a ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 15.62s loi "Spanish historian Montero pu": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 24.33s loi "The garrison's records count": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 30.69s loi "Gibraltar stayed British.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 5.07s loi "Which leaves a question the ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 11.06s loi "Between the walls and the Sp": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 24.11s loi "With Spain's consent, the Br": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_2 0.55s loi "After that, the edge kept mo": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_2 3.30s loi "A Spanish historian describe": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_3 5.15s loi "In 1870, it became La Línea ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) KC1910 2.50s loi "We'll come back to it.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 13.42s loi "The fence went up in 1909; S": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 22.00s loi "Behind the fence: a garrison": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_5 0.69s loi "And from 1934, a grass airst": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_5 5.13s loi "Subscribe if you'd like the ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 4.26s loi "In March 1939, Spain protest": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 10.78s loi "That November, Spain's forei": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 4.21s loi "Then Britain pushed it out i": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 20.88s loi "Gibraltar counts about fifty": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_4 6.05s loi "June: Spain turns "non-belli": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_4 11.35s loi "By 1942, the invasion of Nor": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 11.25s loi "On the night of the seventh ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 21.40s loi "The invasion fleets, from Br": không khớp mốc nào trong đặc tả (±0.3 s)
- … 28 mục nữa
### NHIP-K2
- (a) H1 3.41s loi "To walk in from Spain, you c": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1 6.67s loi "Since July 2026, this gate h": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2 3.23s loi "Historians on both sides cou": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H3 5.67s loi "So why, today, is the fight ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_1 6.50s loi "That summer, their fleet sai": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_1 10.79s loi "Its commanders, Admiral Geor": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 0.89s loi "This plan, printed in 1705, ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 10.50s loi "Inside, Governor Diego de Sa": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 19.28s loi "He refused to surrender.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 21.39s loi "The fleet answered with some": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_3 9.50s loi "British accounts put the def": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_4 5.13s loi "By a British account, almost": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_5 16.55s loi "The treaty names the town, c": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_5 25.49s loi "Britain said in 2015 that Gi": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_6 6.07s loi "Spain tried again in 1727.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_6 9.20s loi "Neither siege took it.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 6.38s loi "On the twenty-first of June ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 12.47s loi "Spain had joined France in i": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 16.05s loi "By October, British intellig": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 4.95s loi "Based at Algeciras, its boat": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C3 11.14s loi "The food had to come by sea.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C4 7.99s loi "Scurvy spread, until a Danis": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C5 10.07s loi "The townspeople fled south.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_6 3.87s loi "A British officer blamed "re": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_6 8.46s loi "By British tallies, the two ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_10 4.01s loi "By early July, Sergeant Ince": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_10 13.79s loi "A Spanish historian wrote it": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 8.71s loi "On the eighth of September, ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 8.68s loi "The Duc de Crillon led the s": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 12.14s loi "Their answer to red-hot shot": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 18.85s loi "A French account says he'd a": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 23.11s loi "It was refused.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 0.57s loi "The thirteenth of September ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 4.32s loi "That morning, the batteries ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 9.25s loi "At ten twenty-five, by the S": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 17.24s loi "By the next afternoon, all t": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 21.50s loi "Over two thousand attackers ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 3.57s loi "The blockade never forced a ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 15.62s loi "Spanish historian Montero pu": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 24.33s loi "The garrison's records count": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 30.69s loi "Gibraltar stayed British.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 5.07s loi "Which leaves a question the ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 11.06s loi "Between the walls and the Sp": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 24.11s loi "With Spain's consent, the Br": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_2 0.55s loi "After that, the edge kept mo": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_2 3.30s loi "A Spanish historian describe": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_3 5.15s loi "In 1870, it became La Línea ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) KC1910 2.50s loi "We'll come back to it.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 13.42s loi "The fence went up in 1909; S": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 22.00s loi "Behind the fence: a garrison": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_5 0.69s loi "And from 1934, a grass airst": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_5 5.13s loi "Subscribe if you'd like the ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 4.26s loi "In March 1939, Spain protest": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 10.78s loi "That November, Spain's forei": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 4.21s loi "Then Britain pushed it out i": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 20.88s loi "Gibraltar counts about fifty": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_4 6.05s loi "June: Spain turns "non-belli": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_4 11.35s loi "By 1942, the invasion of Nor": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 11.25s loi "On the night of the seventh ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 21.40s loi "The invasion fleets, from Br": không khớp mốc nào trong đặc tả (±0.3 s)
- … 28 mục nữa
### Q26b-K2
- (a) nửa đầu: 1 loại cảnh ≥ 3 s (3d) < 3
- (a) nửa sau: 2 loại cảnh ≥ 3 s (3d, the_so) < 3
- (b) loại 3d chiếm 97.9 % > 70 %
### Q33-K2
- không có master: pHash không đo (chỉ đếm lần khai)
### NC-H1
- (a) C3/0 anim_C3 @3:27.6 (khai noi: thanh_pho): cảnh tl/t3tl không có lớp nhà/đường (fabric 0 % theo đặc tả) < 25 %
- (a) C5/0 anim_C5 @3:55.2 (khai noi: thanh_pho): cảnh tl/t3tl không có lớp nhà/đường (fabric 0 % theo đặc tả) < 25 %
### NC-H2
- không có shot bản đồ/địa cầu có máy quay đọc được
### NC-H3
- không có thời lượng 3D địa lý
### Q37 (1.13)
- (a) H1 3.41s loi "To walk in from Spain, you c": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1 6.67s loi "Since July 2026, this gate h": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2 3.23s loi "Historians on both sides cou": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H3 5.67s loi "So why, today, is the fight ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_1 6.50s loi "That summer, their fleet sai": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_1 10.79s loi "Its commanders, Admiral Geor": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 0.89s loi "This plan, printed in 1705, ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 10.50s loi "Inside, Governor Diego de Sa": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 19.28s loi "He refused to surrender.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 21.39s loi "The fleet answered with some": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_3 9.50s loi "British accounts put the def": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_4 5.13s loi "By a British account, almost": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_5 16.55s loi "The treaty names the town, c": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_5 25.49s loi "Britain said in 2015 that Gi": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_6 6.07s loi "Spain tried again in 1727.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_6 9.20s loi "Neither siege took it.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 6.38s loi "On the twenty-first of June ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 12.47s loi "Spain had joined France in i": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 16.05s loi "By October, British intellig": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 4.95s loi "Based at Algeciras, its boat": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C3 11.14s loi "The food had to come by sea.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C4 7.99s loi "Scurvy spread, until a Danis": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C5 10.07s loi "The townspeople fled south.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_6 3.87s loi "A British officer blamed "re": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_6 8.46s loi "By British tallies, the two ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_10 4.01s loi "By early July, Sergeant Ince": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_10 13.79s loi "A Spanish historian wrote it": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 8.71s loi "On the eighth of September, ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 8.68s loi "The Duc de Crillon led the s": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 12.14s loi "Their answer to red-hot shot": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 18.85s loi "A French account says he'd a": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 23.11s loi "It was refused.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 0.57s loi "The thirteenth of September ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 4.32s loi "That morning, the batteries ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 9.25s loi "At ten twenty-five, by the S": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 17.24s loi "By the next afternoon, all t": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 21.50s loi "Over two thousand attackers ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 3.57s loi "The blockade never forced a ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 15.62s loi "Spanish historian Montero pu": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 24.33s loi "The garrison's records count": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 30.69s loi "Gibraltar stayed British.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 5.07s loi "Which leaves a question the ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 11.06s loi "Between the walls and the Sp": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 24.11s loi "With Spain's consent, the Br": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_2 0.55s loi "After that, the edge kept mo": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_2 3.30s loi "A Spanish historian describe": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_3 5.15s loi "In 1870, it became La Línea ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) KC1910 2.50s loi "We'll come back to it.": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 13.42s loi "The fence went up in 1909; S": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 22.00s loi "Behind the fence: a garrison": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_5 0.69s loi "And from 1934, a grass airst": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_5 5.13s loi "Subscribe if you'd like the ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 4.26s loi "In March 1939, Spain protest": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 10.78s loi "That November, Spain's forei": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 4.21s loi "Then Britain pushed it out i": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 20.88s loi "Gibraltar counts about fifty": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_4 6.05s loi "June: Spain turns "non-belli": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_4 11.35s loi "By 1942, the invasion of Nor": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 11.25s loi "On the night of the seventh ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 21.40s loi "The invasion fleets, from Br": không khớp mốc nào trong đặc tả (±0.3 s)
- … 28 mục nữa
### K-LAI-2
- (b) đoạn minh hoạ khai trong log shot nhưng shot ghi ai_image: false: C4/M1 — sửa log (bỏ mục đoạn, hoặc ai_image: true)
- (d) không khai phat_hanh.mo_ta (mô tả + bình luận ghim)
### K-LAI-3
- H1/M5: không có tệp kiểm (mục đoạn `kiem` hoặc lai.kiem_minh_hoa.M5)
- N1_4/M3: không có tệp kiểm (mục đoạn `kiem` hoặc lai.kiem_minh_hoa.M3)
- C3/M2: không có tệp kiểm (mục đoạn `kiem` hoặc lai.kiem_minh_hoa.M2)
- C5/M4: không có tệp kiểm (mục đoạn `kiem` hoặc lai.kiem_minh_hoa.M4)
### K-LAI-6
- 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4): không có sổ AI (tệp so_ai: của episode.yaml hoặc lai.goi_api)
### O2
- chưa soi: khai khối o2: {nam | nam_theo} và chạy --o2 <master> --o2-api (Claude API, có chi phí)
### SACH-1
- (c) không có log chữ (--logs k2.js) — không đo được chữ thực hiện trên hình; (d) chip nơi chưa đo
### PP-1
- (e) thẻ PP1: 29 từ / 8.0 s = 3.6 từ/s > 3 (khó đọc trên điện thoại)
- (e) thẻ PP2: 29 từ / 8.0 s = 3.6 từ/s > 3 (khó đọc trên điện thoại)
### TL-1
- (c) video: 67 cắt đo / 12.42 phút = 5.40 cắt/phút − 0 cắt góc R3 (so_goc/goc_may) = 5.40/phút tính trần > 5 (đặc tả 44 ranh = 3.54/phút; khớp ±0.5 s 42)
- (d) shot C1 góc cao trôi 2.50 % khung/s > 2 (trung vị 19 cửa sổ 1 s)
- (d) shot C3 góc cao trôi 2.12 % khung/s > 2 (trung vị 11 cửa sổ 1 s)
- (d) shot C4 góc cao trôi 4.58 % khung/s > 2 (trung vị 8 cửa sổ 1 s)
- (d) shot C5 góc cao trôi 3.10 % khung/s > 2 (trung vị 9 cửa sổ 1 s)
- (d) shot N2_11 góc cao trôi 6.93 % khung/s > 2 (trung vị 24 cửa sổ 1 s)
- (d) shot N5_2 góc cao trôi 5.95 % khung/s > 2 (trung vị 11 cửa sổ 1 s)
- (d) shot N5_5 góc cao trôi 3.10 % khung/s > 2 (trung vị 18 cửa sổ 1 s)
- (e) 34 điểm máy cao (cần 6–8)
- (f) điểm máy D7-lai → WCA-than → D7-lai: chỉ ở năm 2026-10-19 15:00 — phải quay lại ở năm khác
- (f) điểm máy K2: chỉ ở năm 2026-10-19 23:53 — phải quay lại ở năm khác
- (f) điểm máy D7h-lai: chỉ ở năm 1938.6 — phải quay lại ở năm khác
- (f) điểm máy K-co: chỉ ở năm 1704-08-04 08:30 — phải quay lại ở năm khác
- (f) điểm máy B-thap → K-co → E-bac: chỉ ở năm 1713-07-13 09:00 — phải quay lại ở năm khác
- (f) điểm máy A2-thap → L-linea: chỉ ở năm 1704.8 — phải quay lại ở năm khác
- (f) điểm máy L-linea → T-trai-bac: chỉ ở năm 1779-06-20 09:00 — phải quay lại ở năm khác
- (f) điểm máy E (V7B-a): chỉ ở năm 1779-07-12 16:00 — phải quay lại ở năm khác
- (f) điểm máy Ca2-lai: chỉ ở năm 1780-01-14 10:00 — phải quay lại ở năm khác
- (f) điểm máy Bm-thap → M1 → Bm-thap: chỉ ở năm 1780-01-16 12:00 — phải quay lại ở năm khác
- (f) điểm máy Cc2-lai → M4: chỉ ở năm 1781-04-12 09:20 — phải quay lại ở năm khác
- (f) điểm máy D-vach-thap → E-vach: chỉ ở năm 1782-05-25 12:00 — phải quay lại ở năm khác
- (f) điểm máy D-bac-thap: chỉ ở năm 1782-09-08 06:30 — phải quay lại ở năm khác
- (f) điểm máy B-cao-lai: chỉ ở năm 1782-09-11 07:00 — phải quay lại ở năm khác
- (f) điểm máy B-lan: chỉ ở năm 1782-09-13 06:45 — phải quay lại ở năm khác
- (f) điểm máy D-bac-thap → W-cong-su → T-trai-bac: chỉ ở năm 1782-10-01 12:00 — phải quay lại ở năm khác
- (f) điểm máy SF-thap → SB-thap: chỉ ở năm 1783.6 — phải quay lại ở năm khác
- (f) điểm máy B-thap: chỉ ở năm 1810.3 — phải quay lại ở năm khác
- (f) điểm máy H-thap → F-hang-rao: chỉ ở năm 1900.0 — phải quay lại ở năm khác
- (f) điểm máy D2-thap: chỉ ở năm 1933.5 — phải quay lại ở năm khác
- (f) điểm máy D-thap-dong → D-thap-tay: chỉ ở năm 1939.2 — phải quay lại ở năm khác
- (f) điểm máy W-vinh-thap → D-vach-thap: chỉ ở năm 1941.6 — phải quay lại ở năm khác
- (f) điểm máy Bb-lai: chỉ ở năm 1940-05-20 12:00 — phải quay lại ở năm khác
- (f) điểm máy D-duongbang: chỉ ở năm 1942.3 — phải quay lại ở năm khác
- (f) điểm máy D-cong: chỉ ở năm 1946.0 — phải quay lại ở năm khác
- (f) điểm máy D → H: chỉ ở năm 2026-10-19 08:10 — phải quay lại ở năm khác
- (f) điểm máy D-cong-thap → F-hang-rao: chỉ ở năm 2026-07-14 10:00 — phải quay lại ở năm khác
- (f) điểm máy B-lui: chỉ ở năm 2026-10-18 16:00 — phải quay lại ở năm khác
- (f) điểm máy D7-lai-nguoc: chỉ ở năm 1730.0 — phải quay lại ở năm khác
### TL-3
- (b) 43 shot 3D không có trong_pct (đầu: shot H1: không có trong_pct)
### XEM-CAM
- không khai `xem_cam:` trong episode.yaml — cổng XEM CÂM bắt buộc từ T3 (§13.4); K không tự chấm
### MINH-HOA
- (e) H1/M5 @0:04.5–0:10.5: sổ AI không có dòng cho đoạn (so_ai của đoạn/shot, hoặc tệp so_ai: có shot/doan/ma = M5 hoặc tag = luot)
- (e) N1_4/M3 @1:48.0–1:56.0: sổ AI không có dòng cho đoạn (so_ai của đoạn/shot, hoặc tệp so_ai: có shot/doan/ma = M3 hoặc tag = luot)
- (e) C3/M2 @3:27.6–3:35.6: sổ AI không có dòng cho đoạn (so_ai của đoạn/shot, hoặc tệp so_ai: có shot/doan/ma = M2 hoặc tag = luot)
- (e) C5/M4 @4:01.3–4:07.7: sổ AI không có dòng cho đoạn (so_ai của đoạn/shot, hoặc tệp so_ai: có shot/doan/ma = M4 hoặc tag = luot)
### EO-DAT-R2
- H1: thiếu `trong_pct`
- H3: thiếu `trong_pct`
- N1_4: thiếu `trong_pct`
- N1_6: thiếu `trong_pct`
- C1: thiếu `trong_pct`
- N2_10: thiếu `trong_pct`
- N2_7: thiếu `trong_pct`
- N2_11: thiếu `trong_pct`
- N3_1: thiếu `trong_pct`
- N3_4: thiếu `trong_pct`
- N3_5: thiếu `trong_pct`
- N4_1: thiếu `trong_pct`
- N4_2: thiếu `trong_pct`
- N4_5: thiếu `trong_pct`
- N5_1: thiếu `trong_pct`
- N5_2: thiếu `trong_pct`
- N5_4: thiếu `trong_pct`
- N5_6: thiếu `trong_pct`
### EO-DAT-R3
- (b) N1_6 @2:27.6 (25.5 s): khoảng không biến cố dài nhất 9.0 s > 6 s (6 biến cố log)
- (b) C1 @2:53.1 (22.5 s): khoảng không biến cố dài nhất 11.5 s > 6 s (4 biến cố log)
- (b) N2_10 @4:30.2 (18.4 s): khoảng không biến cố dài nhất 10.2 s > 6 s (2 biến cố log)
- (b) N2_11 @5:55.0 (27.6 s): khoảng không biến cố dài nhất 13.5 s > 6 s (3 biến cố log)
- (b) N3_1 @6:22.6 (27.2 s): khoảng không biến cố dài nhất 13.8 s > 6 s (4 biến cố log)
- (b) N3_4 @7:15.3 (27.0 s): khoảng không biến cố dài nhất 15.0 s > 6 s (3 biến cố log)
- (b) N4_1 @7:51.6 (25.5 s): khoảng không biến cố dài nhất 21.2 s > 6 s (3 biến cố log)
- (b) N4_2 @8:17.1 (28.4 s): khoảng không biến cố dài nhất 25.4 s > 6 s (2 biến cố log)
- (b) N4_5 @9:18.6 (27.2 s): khoảng không biến cố dài nhất 10.8 s > 6 s (3 biến cố log)
- (b) N5_1 @9:45.8 (23.8 s): khoảng không biến cố dài nhất 16.8 s > 6 s (3 biến cố log)
- (b) N5_4 @11:06.1 (31.5 s): khoảng không biến cố dài nhất 16.3 s > 6 s (3 biến cố log)
- (b) N5_6 @12:05.0 (20.0 s): khoảng không biến cố dài nhất 6.7 s > 6 s (5 biến cố log)
- (a) N1_6 @2:27.6 (25.5 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) C1 @2:53.1 (22.5 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N2_10 @4:30.2 (18.4 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N2_11 @5:55.0 (27.6 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N3_1 @6:22.6 (27.2 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N3_4 @7:15.3 (27.0 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N4_1 @7:51.6 (25.5 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N4_2 @8:17.1 (28.4 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N4_5 @9:18.6 (27.2 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N5_1 @9:45.8 (23.8 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N5_4 @11:06.1 (31.5 s): thiếu `so_goc` (hoặc `goc_may`)
- (a) N5_6 @12:05.0 (20.0 s): thiếu `so_goc` (hoặc `goc_may`)
### CONG-BO-1
- (a) không khai phat_hanh.mo_ta (mô tả + bình luận ghim) — cần câu công bố có "AI" hoặc "synthetic" trong mô tả YouTube của gói phát hành
- (b) đặc tả gói không khai phat_hanh.youtube_altered_content (cần true — "AI use" = Yes ở YouTube Studio)
