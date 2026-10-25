# Luật kênh 2 (checks 1.17.7) — k2c-t3-cuoi — TRƯỢT

| Mục | Kiểm | Kết quả | Cấp (1.12.1) | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) |
|---|---|---|---|---|---|---|
| Q26b | Đa dạng bối cảnh (1.16: cảnh tl/* theo vùng) | **ĐẠT** |  | 39 bối cảnh · lớn nhất tl/t3tl · C-lai 5.4 % · liên tục dài nhất tl/t3tl · D-cong-thap → F-hang-rao 31.5 s · nửa sau 19 · trung tính 0.0 % | ≤ 25 % · ≤ 90 s · nửa sau ≥ 3 |  |
| Q32 | Footage/ảnh nguồn ngoài | **ĐẠT** |  | không dùng footage ngoài | ≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5× |  |
| Q33 | Lặp cảnh (1.17.3: miễn cùng điểm máy năm khác — TL-1, năm hiện theo opt.time) | **ĐẠT** |  | 43 góc máy · 43 lần xuất hiện · nhiều nhất tl/t3tl · anim_C1 1 lần · 0 góc > 2 · pHash xám toàn khung θ=14, thêm 18 lần lặp không khai · miễn năm khác (1.17, TL-1) 18 | ≤ 2 lần |  |
| Q34 | Loại shot | **ĐẠT** |  | 45/45 shot có type · scene3d 97.8 % · card 2.2 % · số neo 3D 100 %, chỉ card 0 % (0 số) · địa danh 0 · nhân vật 0 | type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document ≤ 3 s · record ≤ 12 s + dòng tô + nguồn |  |
| Q35 | Nhãn loại số (D5) | **ĐẠT** |  | mô hình đặc tả · 95 khung xét · ACTUAL nhiều nhất 0/khung · lỗi a 0 · b 0 · c 0 · d 0 | ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL |  |
| Q36 | Chữ trên màn hình | **ĐẠT** |  | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực (+ 1 lần trong câu miễn trừ 0:00–0:15) |  |
| Q37 | Nhịp thị giác (1.16: miễn khung neo/im lặng ≤ 10 s; 1.17.4: + thẻ PP cuối phim) | **TRƯỢT** |  | 762.0 s · biến cố khai 309 (gộp 266) · TB 2.86 s · dài nhất 8.03 s · khung tĩnh (khung liền < 0.6/255) dài nhất 9.46 s (từ 10:09.6) · miễn khung neo/im lặng (1.16): 8 khoảng, dài nhất trước miễn 10.0 s | TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s |  |
| A1–A13 | Âm thanh (tập cũ — chỉ báo) | **CHỈ BÁO** |  | CHỈ BÁO · A1 -14.0 LUFS · A2 -1.4 dBTP · A5 0 đoạn · A7 0 · A4 KHÔNG ÁP (không có lời — 1.16) · A8 KHÔNG ÁP (không có lời — 1.16) | docs/AUDIO-THUOC-DO.md | A1 I = -14.0 LUFS (ngưỡng -15 / -13.8) |
| ML1 | Mạch truyện | **ĐẠT** | Chặn (b), (c) · Cảnh báo (a) ở T3 (Chặn từ T4) — lỗi Chặn 0, Cảnh báo 0 | 41/45 shot gắn (0 suy từ mốc @từ) · timelapse 762.0 s, trôi 4.3 % | mỗi shot gắn câu/claim · timelapse trôi ≤ 15 % |  |
| ML2 | Lời lặp ý | **ĐẠT** | Chặn có giải trình (người quyết; không vào mã thoát tự động) — lỗi Chặn 0, Cảnh báo 0 | 0 câu · 0 cặp ứng viên (chấm 0) · 0 lặp ý · không khai tóm tắt | n-gram/IDF + chấm ngữ nghĩa ghim mô hình; ngoài tóm tắt cuối |  |
| ML3 | Lời mời đăng ký | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 câu mời: không có · 0 luận điểm chính khai | 60 s cuối hoặc ±5 s ranh chương · không trong 20 s trước luận điểm chính |  |
| FT1 | Chỉ báo footage/ảnh | **ĐẠT** | Cảnh báo (20 % footage đã Chặn ở Q32 b2) — lỗi Chặn 0, Cảnh báo 0 | 0 shot footage/ảnh · tính 0.0 s = 0.0 % (miễn ảnh nhỏ 0.0 s) · khai lý do: 0/0 | ≤ 20 % (trần) · mỗi shot có lý do · ảnh ≤ 1/3 khung ≤ 6 s không tính |  |
| NHIP-K2 | Nhịp kênh 2 (Q14–Q18 không áp → Q37) | **TRƯỢT** | Chặn (như Q37) — lỗi Chặn 71, Cảnh báo 0 | Q37: 762.0 s · biến cố khai 309 (gộp 266) · TB 2.86 s · dài nhất 8.03 s · khung tĩnh (khung liền < 0.6/255) dài nhất 9.46 s (từ 10:09.6) · miễn khung neo/im lặng (1.16): 8 khoảng, dài nhất trước miễn 10.0 s | TB ≤ 3,5 s · dài nhất ≤ 6 s |  |
| Q26b-K2 | Đa dạng loại cảnh + vùng | **CẢNH BÁO** | Chặn (c), (d), (e) (như Q26b) · Cảnh báo (a), (b) — lỗi Chặn 0, Cảnh báo 3 | loại: 3d 97.8 %, the_so 2.2 % · 38 vùng, lớn nhất C-lai 5.4 % · nửa sau 19 vùng · không vùng 2.2 % | ≥ 3 loại/nửa · loại ≤ 70 % · vùng ≤ 25 %, ≤ 90 s, nửa sau ≥ 3 |  |
| Q33-K2 | Lặp cảnh (vùng, góc) + pHash L/ΔE | **ĐẠT** | Chặn (như Q33) — lỗi Chặn 0, Cảnh báo 0 | 43 khoá (vùng, góc) · 43 lần xuất hiện · nhiều nhất tl/t3tl · anim_C1 1 · 0 khoá > 2 · pHash L θ=16 + ΔE ≤ 10, thêm 16 lần lặp không khai, miễn 16 | ≤ 2 lần (miễn: khác chương + khác năm/lớp; 1.17.3: năm hiện (opt.time / log shot) không chồng — TL-1) |  |
| Q32b-K2 | Trần clip/ảnh | **ĐẠT** | Chặn (như Q32b) — lỗi Chặn 0, Cảnh báo 0 | 0 clip/ảnh ·  | footage ≤ 8 s · ảnh có máy/chú thích đổi ≤ 12 s · ảnh tĩnh ≤ 8 s |  |
| NC-H1 | Thành phố có nhà | **ĐẠT** | Chặn (a), (b) (đúng lỗi chủ dự án nêu ở T2) — lỗi Chặn 0, Cảnh báo 0 | 18 shot thành phố (234.8 s; khai 18, suy 0) · có lớp nhà khai 18 · không lớp nhà 0 · không đo fabric 18 | fabric trung vị ≥ 25 % · không khung < 15 % (trừ ≤ 3 s cuối reveal) |  |
| NC-H2 | Địa cầu | **CẢNH BÁO** | Chặn (a), (b) — lỗi Chặn 0, Cảnh báo 1 | 0 lần · 0.0 s (0.0 % phim) · map/globe 0.0 s · bản đồ nổi tầm cao 0.0 s · dài nhất 0 s | AGL > 50 km: ≤ 1 lần/tập · ≤ 3 s/lần |  |
| NC-H3 | Tầm mặc định | **CẢNH BÁO** | Cảnh báo — lỗi Chặn 0, Cảnh báo 1 | 3D địa lý 0.0 s · AGL ≤ 60 km 0.0 % · ≤ 3 km 0.0 % · có thành phố: có | AGL ≤ 60 km ≥ 70 % 3D · có thành phố: AGL ≤ 3 km ≥ 40 % |  |
| NC-H4 | Nơi có tên | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 shot bản đồ · chip nơi 0 · nhãn địa danh 0 · thiếu 0 (nguồn: đặc tả, không log chữ) | mọi shot bản đồ: chip nơi hoặc nhãn địa danh |  |
| NC-H5 | Đúng thời kỳ | **ĐẠT** | Chặn (a) · Cảnh báo (b) — lỗi Chặn 0, Cảnh báo 0 | tập không có bộ đếm năm (cảnh tl/* có opt.year/counter, hoặc p.counter) | năm xây ≤ bộ đếm (nam_khung) · ghost có nguồn + nguồn trong mô tả (§12.1: không nhãn trên hình) |  |
| Q7/Q8-K2 | Nhãn/loại số nhận estimate (khiếu nại TT5 i) | **ĐẠT** | Chặn (thay Q7/Q8 cho kênh 2, như Q35) — lỗi Chặn 0, Cảnh báo 0 | Q7 nhận ESTIMATE: 0 lỗi (không log: chỉ kiểm kind khai) · Q8 loại số: 0 lỗi | kind ∈ actual/projection/estimate (kênh 2) · đủ nhãn, không thừa nhãn |  |
| Q33 (1.13) | Lặp cảnh — pHash bỏ lớp chữ cố định | **ĐẠT** | Chặn (thay Q33 cho kênh 2) — lỗi Chặn 0, Cảnh báo 0 | 43 góc máy · 43 lần xuất hiện · nhiều nhất tl/t3tl · anim_C1 1 lần · 0 góc > 2 · pHash L vùng nội dung (bỏ lớp chữ cố định) θ=16, thêm 16 lần lặp không khai · miễn năm khác (1.17, TL-1) 16 | ≤ 2 lần · pHash L vùng nội dung y 18–72 %, θ 16 · 1.17.3: miễn cùng điểm máy năm khác (TL-1, năm hiện theo opt.time) |  |
| Q36 (1.13) | Chữ — câu miễn trừ nhận theo chữ | **ĐẠT** | Chặn (thay Q36 cho kênh 2) — lỗi Chặn 0, Cảnh báo 0 | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | "This video explains… Facts as of" 1 lần trong 0:00–0:15 không đòi nguồn luật |  |
| Q37 (1.13) | Nhịp — khung tĩnh theo khung neo | **TRƯỢT** | Chặn (thay Q37 cho kênh 2) — lỗi Chặn 78, Cảnh báo 0 | 762.0 s · biến cố khai 309 (gộp 266) · TB 2.86 s · dài nhất 8.03 s · khung tĩnh (neo, < 2.0/255) dài nhất 9.58 s (từ 10:32.0) · trôi chậm (thước cũ > 6 s, không tĩnh): 1 quãng, dài nhất 8.17 s từ 8:45.5 · miễn khung neo/im lặng (1.16): 8 khoảng, dài nhất trước miễn 10.0 s | khung tĩnh (mọi khung khác khung đầu quãng < 2,0/255) ≤ 6 s | khung tĩnh 5.92 s từ 12:19.0 (ngưỡng 6.0) |
| BIEN-CO-V | Biến cố thấy được ĐO trên video (K117-D8) | **TRƯỢT** | Chặn (b), (c), (h) ở G2 khi thước đạt hiệu chuẩn (q_bcv.HIEU_CHUAN + (h) trên tập) · Cảnh báo ở animatic hoặc khi chưa hiệu chuẩn — K117-D8 — lỗi Chặn 1, Cảnh báo 0 | 762.0 s · biến cố đo 1987 (gộp 1690; cắt 389) · TB 0.45 s · dài nhất 19.62 s · miễn 31 khoảng (khung_neo, the_pp) · ranh shot bắt 44/44 (100.0 %) · hiệu chuẩn T3: ĐẠT (T3 5b9f0bcc…: θ 8, k 2; R cắt 100/100 %, R beat 90,8/98,2 %, Δt TV 0,05/0,04 s, báo nhầm 0) | TB khoảng biến cố đo ≤ 3,5 s · dài nhất ≤ 6 s (miễn khung neo/im lặng/thẻ PP ≤ 10 s) · bắt ≥ 95 % ranh shot |  |
| BD-1…BD-8 | Bản đồ chiến lược / inset / ranh | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | không có shot strategic, lớp ranh, tuyến hay inset |  |  |
| K-R1…K-R9 | ĐỎ-K | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập không khai rui_ro: do-k |  |  |
| K-LAI-1 | LAI: thời lượng khung AI | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 27.40 s AI / 762.00 s (timeline) = 3.6 % · nguồn: log shot (4 đoạn minh hoạ + 0 shot ai_image), không có log khung | ai_image/ai_texture ≤ 20 % thời lượng (log khung; không có → đoạn khai trong log shot, 1.17.2) |  |
| K-LAI-2 | LAI: công bố AI (§12.1) | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | thẻ phương pháp có (1.17.2: không đòi câu AI) · mô tả không · log chữ không · cờ AI: log shot | cờ ai_* mọi khung (hoặc mọi shot log) · shot khai khớp log · mô tả "AI use = Yes" · KHÔNG nhãn trên hình (1.17.2: bỏ "thẻ PP nói AI") |  |
| K-LAI-3 | LAI: kiểm dữ kiện từng tấm C | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | minh hoạ: 4 đoạn · kiểm ĐẠT 4 · thiếu tệp kiểm 0 | mỗi tấm C: loi_chac_cuoi 0 · nghi vấn đã xử lý · ngoại lệ có duyệt · không chấm mù |  |
| K-LAI-4 | LAI: vùng bảo vệ = A | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | sai khác TB < 1/255 trên mặt nạ bao_ve (PNG) |  |
| K-LAI-5 | LAI: một tấm, ban ngày, đêm ≤ 1,5× A | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | ≤ 1 tấm/khung neo × mốc · ≤ 2 lần sinh lại · chỉ lượt ngày · đêm ≤ 1,5× A |  |
| K-LAI-6 | LAI: sổ gọi API | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 11 lệnh AI · $11.2461 · C2PA 11/11 | model, prompt, % mặt nạ, usage, $, C2PA, giờ |  |
| K-LAI-B | LAI: bão hoà khung (P2-3) | **ĐẠT** | Cảnh báo (P2-3) — lỗi Chặn 0, Cảnh báo 0 | 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | bão hoà trung vị ≤ 0,40 mỗi khung LAI |  |
| K-LAI-3V | LAI: nghi vấn còn ghi của vân (1.16) | **ĐẠT** | Chặn ở cổng G2 (bản phát hành) · Cảnh báo ở animatic (K116-D5) — lỗi Chặn 0, Cảnh báo 0 | không có khung ai_texture | tệp vân dùng không còn nghi vấn chưa xử lý (Chặn ở G2 · Cảnh báo ở animatic — K116-D5) |  |
| O2 | Máy soi lỗi thời đại (lưới lọc thứ hai) | **CẢNH BÁO** | Cảnh báo (lưới lọc thứ hai — không thay kiểm nguồn) — lỗi Chặn 0, Cảnh báo 1 | — | 1 khung/5 s + khung neo · cờ/quân phục/tàu/đèn/xe/vật hiện đại/chữ/kiến trúc theo năm · không thay kiểm nguồn |  |
| SACH-1 | Khung sạch §12.1 + TL-4 | **ĐẠT** | Chặn (a)–(f) (K116-D1; (e) chữ bản đồ Chặn theo K116-D3: ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ) — lỗi Chặn 0, Cảnh báo 0 | 45 shot · tấm số/trích 0 · tư liệu đứng riêng 0 · log chữ 1665 mục hiện · cấm 0 · chip 0 lần, dài nhất 0.00 s · nhãn địa danh 0 shot, dài nhất 0.00 s · lỗi chữ bản đồ/khác 0 · chữ thẻ theo đặc tả (1.17.3): PP 145 mẫu, chương 30 mẫu | chỉ bộ đếm · chip nơi ≤ 3 s · thẻ chương · thẻ phương pháp · bản đồ ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ (K116-D3); không tấm số/trích, không tư liệu đứng riêng (phủ ≤ 3 s) |  |
| CHUONG-1 | Thẻ chương §13.3 | **ĐẠT** | Chặn (a)–(e) · Cảnh báo (f) vị trí/mờ (K116-D1) — lỗi Chặn 0, Cảnh báo 0 | 5 thẻ (đặc tả) · dài nhất 3.00 s · 0:44.2 1704 — The Rock changes hands; 2:53.5 1779 — The Great Siege; 6:23.0 1783 — The neutral ground; 7:52.0 1939 — A runway on the sand | ≤ 8/tập · "năm — ≤ 6 từ" · ≤ 3 s · không trong móc · trung tính | thẻ '1704 — The Rock chan' s 3.0 (ngưỡng 3.0); thẻ '1779 — The Great Sie' s 3.0 (ngưỡng 3.0); thẻ '1783 — The neutral g' s 3.0 (ngưỡng 3.0); thẻ '1939 — A runway on t' s 3.0 (ngưỡng 3.0); thẻ '1969 — The gate clos' s 3.0 (ngưỡng 3.0) |
| PP-1 | Thẻ phương pháp (D6) | **CẢNH BÁO** | Chặn (a)–(d) · Cảnh báo (e) tốc độ đọc ≤ 3 từ/s (K116-D1, D8: ≈ 8 s = 7–9 s) — lỗi Chặn 0, Cảnh báo 1 | 2 thẻ · PP1 9.0 s, PP2 8.0 s · 55 từ | 2 thẻ × 7–9 s, cuối phim · nguồn/bản đồ + chỗ ước tính (1.17.2: không đòi câu AI) · ≤ 3 từ/s | thẻ PP1 s (cận trên) 9.0 (ngưỡng 9.0) |
| TL-1 | Xương sống timelapse §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; mục tiêu §13.6, hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 37 | thân phim 745.0 s · góc cao + tl 709.0 s (95.2 %) · đặc tả ≤ 5.80 cắt/phút (cận trên) · video 75 cắt = 5.96/phút (thô) − 26 cắt góc R3 (so_goc/goc_may) = 3.87/phút tính trần · đặc tả 72 ranh = 5.80/phút · khớp ±0.5 s 69 (chỉ video 6: 0:15.4, 0:23.4, 0:23.8, 3:36.0, 3:36.2, 12:18.4; chỉ đặc tả 3 — cùng góc máy đổi năm/giờ hoặc chưa cắt) · trôi góc cao trung vị 0.16 %/s (39 shot) · ngưỡng hiệu chỉnh sau V7-PILOT | góc cao + thời gian chạy ≥ 75 % (1.17.7: `tl1_muc_tieu_pct` theo tập) · ≤ 5 cắt/phút (video: đổi cấu trúc; đối chiếu đặc tả ±0,5 s; 1.17.2: cắt góc R3 so_goc/goc_may không tính trần; 1.17.7 từ T4: ranh vào/ra M-d, tư liệu, ảnh thật không tính) · trôi ≤ 2 %/s · 6–8 điểm máy (hiệu chỉnh sau V7-PILOT) |  |
| TL-2 | Lướt thấp §13.6 | **ĐẠT** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 0 | lướt thấp 4 shot · 36.0 s = 4.8 % · ngưỡng hiệu chỉnh sau V7-PILOT | lướt thấp ≤ 10 % · có vai, phố/người (hiệu chỉnh sau V7-PILOT) |  |
| TL-3 | Không shot trống §13.6 | **ĐẠT** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 0 | 43 shot 3D · không đổi 0 · trống 0 · thiếu trong_pct 0 | mỗi shot 3D: thời gian chạy hoặc biến cố · trống ≤ 60 % (hiệu chỉnh sau V7-PILOT) |  |
| NHIP-NGHIA | Nhịp → vật mang nghĩa §13.2 | **ĐẠT** | Chặn (K116-D1; §13.2) — lỗi Chặn 0, Cảnh báo 0 | 71/71 nhịp chính có vật mang nghĩa = 100.0 % | ≥ 90 % nhịp chính |  |
| XEM-CAM | Cổng XEM CÂM §13.4 | **TRƯỢT** | Chặn (K116-D1, D2; §13.4 bắt buộc từ T3) — lỗi Chặn 1, Cảnh báo 0 | 8 câu · AI 3 · chủ dự án 0 · R1 8.0/8, R2 6.5/8, R3 8.0/8 · TB AI 7.50/8 | 8 câu · 3 AI + chủ dự án · tắt tiếng · chủ dự án ≥ 6/8 VÀ TB AI ≥ 6/8 (K116-D2) |  |
| PC-1 | Thước phục chế §12.3 | **ĐẠT** | Cảnh báo (K116-D1; thước tạm, hiệu chuẩn trên ≥ 10 ảnh) — lỗi Chặn 0, Cảnh báo 0 | tập không khai phuc_che: (không dùng ảnh phục chế) | Δ cạnh mới so bicubic ≤ 1,0 điểm % · PSNR ≥ bicubic |  |
| MINH-HOA | Minh hoạ AI §14.1 (c) / §15 M-d | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.1 (c) N2 / §15 M-d) — lỗi Chặn 0, Cảnh báo 0 | 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4) · 27.4 s = 3.6 % · lỗi kẹp 0 · AGL 0 · sổ AI 0 · nhãn: không bắt buộc (1.17.2) | theo đoạn khai: ≤ 20 % · kẹp giữa 2 khung 3D · máy ≤ 40 m AGL · sổ AI mỗi đoạn (1.17.2: không nhãn bắt buộc) |  |
| EO-DAT-R1 | Eo đất R1 — chủ thể | **CẢNH BÁO** | Chỉ báo ở mọi cổng — chủ dự án chấm bằng mắt (1.17.2, V2-D2 duyệt 22/10 11:09); in pixel thô + vùng nở 1,5 % bề ngang (§14.7 R1 "≥ 15–20 %") — lỗi Chặn 0, Cảnh báo 12 | 18 shot chu_the_eo_dat · H1: pixel thô trung vị 48.7 % · vùng nở: chưa đo (`chu_the_mat_na` / `chu_the_pct_no`) (khai); H3: pixel thô trung vị 25.1 % · vùng nở: chưa đo (`chu_the_mat_na` / `chu_the_pct_no`) (khai); N1_4: pixel thô trung vị 11.5 % · vùng nở: chưa đo (`chu_the_mat_na` / `chu_the_pct_no`) (khai); N1_6: pixel thô trung vị 2.4 % · vùng nở: chưa đo (`chu_the_mat_na` / `chu_the_pct_no`) (khai); C1: pixel thô trung vị 6.6 % · vùng nở: chưa đo (`chu_the_mat_na` / `chu_the_pct_no`) (khai); N2_10: pixel thô trung vị 5.4 % · vùng nở: chưa đo (`chu_the_mat_na` / `chu_the_pct_no`) (khai) · CHỈ BÁO mọi cổng (V2-D2, chủ dự án chấm bằng mắt) | chu_the_eo_dat: chủ thể ≥ 15 % khung · 15–20 % (§14.7) — CHỈ BÁO mọi cổng, in pixel thô + vùng nở 1.5 % (1.17.2) | N4_2 chủ thể % 14.3 (ngưỡng 15.0) |
| EO-DAT-R2 | Eo đất R2 — cỏ/cát trống | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R2: trống > 50 % ≤ 6 s liên tục, ≤ 10 % thời lượng chương) — lỗi Chặn 0, Cảnh báo 0 | 18 shot eo đất · đo 18 · trống liên tục dài nhất 3.6 s · ch 2: 3.5 % | trống (> 50 %) liên tục ≤ 6 s · mỗi chương ≤ 10 % thời lượng chương (§14.7) |  |
| EO-DAT-R3 | Eo đất R3 — góc + biến cố | **TRƯỢT** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.7 R3) — lỗi Chặn 2, Cảnh báo 0 | 12/18 shot eo đất > 15 s · khoảng biến cố dài nhất (tính ranh góc máy, 1.17.3): N1_6 5.58 s, C1 5.17 s, N2_10 4.21 s, N2_11 5.50 s, N3_1 4.75 s, N3_4 5.50 s, N4_1 4.58 s, N4_2 4.83 s | shot eo đất > 15 s: ≥ 2 góc · biến cố cách ≤ 6 s | N5_1 khoảng biến cố s 6.0 (ngưỡng 6.0); N5_4 khoảng biến cố s 5.87 (ngưỡng 6.0) |
| EO-DAT-R4 | Eo đất R4 — câu lời không vật | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R4 + TL-4; lệnh K-1.17.1) — lỗi Chặn 0, Cảnh báo 0 | không shot khai loi_khong_vat_eo_dat | loi_khong_vat_eo_dat: noi ∈ pho/lau_dai/cang hoặc bản đồ phủ ≤ 3 s (§14.7, TL-4) |  |
| CONG-BO-1 | Công bố AI ở gói phát hành (1.17.2) | **CẢNH BÁO** | Chặn ở gói phát hành (`cong: phat_hanh` | `phat_hanh.goi: true`) · chỉ báo (Cảnh báo) ở mọi cổng trước — §14.1 (f), YouTube "AI use" — lỗi Chặn 0, Cảnh báo 1 | áp vì: 4 đoạn minh hoạ (H1/M5, N1_4/M3, C3/M2, C5/M4) · 4 shot log ai_image (H1, N1_4, C3, C5) · giọng tổng hợp (giong_tong_hop: true) · mô tả không khai · youtube_altered_content True | khung AI hoặc giọng tổng hợp → mô tả YouTube có câu "AI"/"synthetic" · phat_hanh.youtube_altered_content: true (Chặn ở gói phát hành) |  |
| N2P-1…6 | Luật N2+ (§15, từ T4) | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập trước T4 (không khai kenh2_tu_t4 / n2p) |  |  |
| 1.17.4 (T4) | MAY-19 … GOC-CAO-60 | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập trước T4 — không hồi tố (Q2: T3 giữ luật cũ) |  |  |
| 1.17.5 (T4) | BE-MAT-NHA | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập trước T4 — không hồi tố |  |  |
| LOCK | checks/ khớp LOCK (1.17.7) | **TRƯỢT** |  | KHÔNG KHỚP |  |  |

## Âm thanh A1–A13
| Mục | Kiểm | Loại | Kết quả | Giá trị | Ngưỡng |
|---|---|---|---|---|---|
| A1 | Loudness tích hợp (master sau AAC) | chặn | ĐẠT | -14.0 LUFS | -15.0 … -13.8 |
| A2 | Đỉnh thật sau AAC | chặn | ĐẠT | -1.4 dBTP | ≤ -1.0 |
| A3 | Biên độ loudness LRA | báo | ĐẠT | 3.1 LU | 2–8 (báo) |
| A4 | Lời trên nhạc (SMR) | chặn | — | KHÔNG ÁP (không có lời — 1.16) | p10 ≥ 15 · min ≥ 12 |
| A5 | Lặng bất thường ≥ 1 s (< −50 LUFS tức thời) | chặn | ĐẠT | 0 đoạn | 0 |
| A6 | Tỉ lệ lặng | báo | ĐẠT | 0.03 % | báo |
| A7 | Chạm trần (≥ 3 mẫu |x| ≥ 0,999) | chặn | ĐẠT | 0 | 0 |
| A8 | Chồng lời | chặn | — | KHÔNG ÁP (không có lời — 1.16) | 0 |
| A9 | ASR hai cách nghe | chặn | — | KHÔNG ÁP (không có lời — 1.16) | 100 % đoạn |
| A10 | Quãng không lời > 8 s không khai khoảnh khắc nhạc | báo | — | KHÔNG ÁP (không có lời — 1.16) | > 8 s (báo) |
| A11 | Giao nhạc | chặn | — | không đo (mix.json không phải chuỗi mới) | ≤ 1 ô nhịp · không lặp |
| A12 | Loudnorm tuyến tính | chặn | — | không đo (mix.json không phải chuỗi mới) | linear |
| A13 | Đồng bộ tiếng | báo | — | KHÔNG ÁP (không có lời — 1.16) | ≤ 5 ms (báo) |

## Chi tiết lỗi
### Q37
- (a) H1 11.90s ngay_dem "gần nửa đêm biên giới (23:52)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_1 2.00s tau "hạm đội Anh–Hà Lan (Rooke) vào vịnh từ e": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 24.75s ngay_dem "đêm 3/8/1704": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_4 0.50s nguoi "dòng dân rời phố đi bắc dọc eo đất (về S": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_5 9.37s bien_co_tu_dac_ta "tàu tới vị trí/đổi hướng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_6 0.50s lua "vây 1704–05: khói pháo ở chân vách bắc": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 5.65s bien_co_tu_dac_ta "người/thuyền bắt đầu rút": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 17.43s bien_co_tu_dac_ta "nhóm người xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 0.50s tau "hải đội TBN vào hàng chặn (16/7/1779)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 3.56s bien_co_tu_dac_ta "tàu tới vị trí/đổi hướng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 6.50s tau "thuyền châu Phi tới sát hàng chặn": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 9.00s tau "thuyền châu Phi quay về nam": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C5 0.50s tau "12/4/1781: đoàn Darby thả neo": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C5 5.31s bien_co_tu_dac_ta "người/thuyền bắt đầu rút": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_6 0.50s nguoi "14–16/4/1781: lính tụ trước kho thương n": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 1.00s lua "8/9/1782: đạn nung đỏ — tuyến song song ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 2.04s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 3.08s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 4.13s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 5.17s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 10.00s ngay_dem "tối 8/9: lửa còn cháy": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 1.00s tau "hạm đội Pháp–TBN trong vịnh (47 tàu chiế": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 8.40s ngay_dem "hoàng hôn 11/9": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 17.60s ngay_dem "rạng sáng 12/9": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 1.00s tau "13/9/1782 sáng: 10 pin nổi vào vị trí dư": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 5.65s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 9.00s lua "khai hoả": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 21.00s may "lướt 15–17 m dọc hàng pin nổi cháy": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 24.50s may "ngược lên cao": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 0.50s tau "phong toả tiếp tục mùa đông 1782": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 12.63s lua "5/2/1783: phát súng cuối": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 14.13s pha "trại + công sự TBN rút dần 1783": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 3.00s dem_nam "1783 → 1809: dải cát giữa tường và Línea": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 7.24s bien_co_tu_dac_ta "vuon đủ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_2 0.50s dem_nam "1810 → 1860 trên dải trung lập": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_3 0.50s xay "La Línea mọc theo năm xây (Catastro) 184": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 0.50s dem_nam "dải trung lập giữa hai phố 1900": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 7.00s xay "hàng rào 1909 mọc dọc mép (MỐC ĐINH)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 22.57s bien_co_tu_dac_ta "leu đủ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_5 0.50s xay "dải cỏ cắt làm đường bay 1934–36": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 3.32s bien_co_tu_dac_ta "kho xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 22.50s xay "1941: đường băng cắt qua con đường duy n": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 23.71s bien_co_tu_dac_ta "dong đủ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 0.50s xay "đường băng lấn vịnh theo tháng 1941–43": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 3.00s lua "bụi đá nổ ở vách bắc": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 3.94s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 5.92s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 7.89s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_3 0.50s xay "phố 1943 từng nhà (ghost AMS M981) + đườ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_4 6.00s may_bay "1941–42: máy bay tụ dần trên đường băng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 0.50s may_bay "máy bay xếp kín hai bên đường băng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 20.25s tau "đoàn tàu đổ bộ qua eo biển": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_1 21.39s nguoi "1985: rào gỡ, người qua lại trở lại": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_2 0.50s nguoi "người đi bộ băng qua đường băng giờ cao ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_2 8.50s nguoi "dòng người qua cổng sang phía La Línea (": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_3 0.50s nguoi "sáng: dòng người từ La Línea sang Gibral": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_3 5.97s ngay_dem "mặt trời mọc (≈ 08:35)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_3 18.84s nguoi "giờ tan tầm: dòng người về đông lên": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_4 0.50s nguoi "7/2026: kiểm tra thường lệ dừng — người ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_4 13.15s pha "hàng rào cũ gỡ từng đoạn": không khớp mốc nào trong đặc tả (±0.3 s)
- … 11 mục nữa
### NHIP-K2
- (a) H1 11.90s ngay_dem "gần nửa đêm biên giới (23:52)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_1 2.00s tau "hạm đội Anh–Hà Lan (Rooke) vào vịnh từ e": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 24.75s ngay_dem "đêm 3/8/1704": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_4 0.50s nguoi "dòng dân rời phố đi bắc dọc eo đất (về S": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_5 9.37s bien_co_tu_dac_ta "tàu tới vị trí/đổi hướng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_6 0.50s lua "vây 1704–05: khói pháo ở chân vách bắc": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 5.65s bien_co_tu_dac_ta "người/thuyền bắt đầu rút": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 17.43s bien_co_tu_dac_ta "nhóm người xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 0.50s tau "hải đội TBN vào hàng chặn (16/7/1779)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 3.56s bien_co_tu_dac_ta "tàu tới vị trí/đổi hướng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 6.50s tau "thuyền châu Phi tới sát hàng chặn": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 9.00s tau "thuyền châu Phi quay về nam": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C5 0.50s tau "12/4/1781: đoàn Darby thả neo": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C5 5.31s bien_co_tu_dac_ta "người/thuyền bắt đầu rút": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_6 0.50s nguoi "14–16/4/1781: lính tụ trước kho thương n": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 1.00s lua "8/9/1782: đạn nung đỏ — tuyến song song ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 2.04s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 3.08s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 4.13s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 5.17s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 10.00s ngay_dem "tối 8/9: lửa còn cháy": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 1.00s tau "hạm đội Pháp–TBN trong vịnh (47 tàu chiế": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 8.40s ngay_dem "hoàng hôn 11/9": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 17.60s ngay_dem "rạng sáng 12/9": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 1.00s tau "13/9/1782 sáng: 10 pin nổi vào vị trí dư": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 5.65s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 9.00s lua "khai hoả": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 21.00s may "lướt 15–17 m dọc hàng pin nổi cháy": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 24.50s may "ngược lên cao": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 0.50s tau "phong toả tiếp tục mùa đông 1782": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 12.63s lua "5/2/1783: phát súng cuối": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 14.13s pha "trại + công sự TBN rút dần 1783": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 3.00s dem_nam "1783 → 1809: dải cát giữa tường và Línea": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 7.24s bien_co_tu_dac_ta "vuon đủ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_2 0.50s dem_nam "1810 → 1860 trên dải trung lập": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_3 0.50s xay "La Línea mọc theo năm xây (Catastro) 184": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 0.50s dem_nam "dải trung lập giữa hai phố 1900": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 7.00s xay "hàng rào 1909 mọc dọc mép (MỐC ĐINH)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 22.57s bien_co_tu_dac_ta "leu đủ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_5 0.50s xay "dải cỏ cắt làm đường bay 1934–36": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 3.32s bien_co_tu_dac_ta "kho xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 22.50s xay "1941: đường băng cắt qua con đường duy n": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 23.71s bien_co_tu_dac_ta "dong đủ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 0.50s xay "đường băng lấn vịnh theo tháng 1941–43": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 3.00s lua "bụi đá nổ ở vách bắc": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 3.94s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 5.92s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 7.89s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_3 0.50s xay "phố 1943 từng nhà (ghost AMS M981) + đườ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_4 6.00s may_bay "1941–42: máy bay tụ dần trên đường băng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 0.50s may_bay "máy bay xếp kín hai bên đường băng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 20.25s tau "đoàn tàu đổ bộ qua eo biển": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_1 21.39s nguoi "1985: rào gỡ, người qua lại trở lại": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_2 0.50s nguoi "người đi bộ băng qua đường băng giờ cao ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_2 8.50s nguoi "dòng người qua cổng sang phía La Línea (": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_3 0.50s nguoi "sáng: dòng người từ La Línea sang Gibral": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_3 5.97s ngay_dem "mặt trời mọc (≈ 08:35)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_3 18.84s nguoi "giờ tan tầm: dòng người về đông lên": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_4 0.50s nguoi "7/2026: kiểm tra thường lệ dừng — người ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_4 13.15s pha "hàng rào cũ gỡ từng đoạn": không khớp mốc nào trong đặc tả (±0.3 s)
- … 11 mục nữa
### Q26b-K2
- (a) nửa đầu: 1 loại cảnh ≥ 3 s (3d) < 3
- (a) nửa sau: 2 loại cảnh ≥ 3 s (3d, the_so) < 3
- (b) loại 3d chiếm 97.8 % > 70 %
### NC-H2
- không có shot bản đồ/địa cầu có máy quay đọc được
### NC-H3
- không có thời lượng 3D địa lý
### Q37 (1.13)
- (a) H1 11.90s ngay_dem "gần nửa đêm biên giới (23:52)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_1 2.00s tau "hạm đội Anh–Hà Lan (Rooke) vào vịnh từ e": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_2 24.75s ngay_dem "đêm 3/8/1704": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_4 0.50s nguoi "dòng dân rời phố đi bắc dọc eo đất (về S": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_5 9.37s bien_co_tu_dac_ta "tàu tới vị trí/đổi hướng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N1_6 0.50s lua "vây 1704–05: khói pháo ở chân vách bắc": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 5.65s bien_co_tu_dac_ta "người/thuyền bắt đầu rút": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C1 17.43s bien_co_tu_dac_ta "nhóm người xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 0.50s tau "hải đội TBN vào hàng chặn (16/7/1779)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 3.56s bien_co_tu_dac_ta "tàu tới vị trí/đổi hướng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 6.50s tau "thuyền châu Phi tới sát hàng chặn": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C2 9.00s tau "thuyền châu Phi quay về nam": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C5 0.50s tau "12/4/1781: đoàn Darby thả neo": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) C5 5.31s bien_co_tu_dac_ta "người/thuyền bắt đầu rút": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_6 0.50s nguoi "14–16/4/1781: lính tụ trước kho thương n": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 1.00s lua "8/9/1782: đạn nung đỏ — tuyến song song ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 2.04s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 3.08s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 4.13s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 5.17s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_7 10.00s ngay_dem "tối 8/9: lửa còn cháy": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 1.00s tau "hạm đội Pháp–TBN trong vịnh (47 tàu chiế": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 8.40s ngay_dem "hoàng hôn 11/9": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_8 17.60s ngay_dem "rạng sáng 12/9": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 1.00s tau "13/9/1782 sáng: 10 pin nổi vào vị trí dư": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 5.65s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 9.00s lua "khai hoả": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 21.00s may "lướt 15–17 m dọc hàng pin nổi cháy": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_9 24.50s may "ngược lên cao": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 0.50s tau "phong toả tiếp tục mùa đông 1782": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 12.63s lua "5/2/1783: phát súng cuối": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N2_11 14.13s pha "trại + công sự TBN rút dần 1783": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 3.00s dem_nam "1783 → 1809: dải cát giữa tường và Línea": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_1 7.24s bien_co_tu_dac_ta "vuon đủ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_2 0.50s dem_nam "1810 → 1860 trên dải trung lập": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_3 0.50s xay "La Línea mọc theo năm xây (Catastro) 184": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 0.50s dem_nam "dải trung lập giữa hai phố 1900": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 7.00s xay "hàng rào 1909 mọc dọc mép (MỐC ĐINH)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_4 22.57s bien_co_tu_dac_ta "leu đủ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N3_5 0.50s xay "dải cỏ cắt làm đường bay 1934–36": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 3.32s bien_co_tu_dac_ta "kho xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 22.50s xay "1941: đường băng cắt qua con đường duy n": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_1 23.71s bien_co_tu_dac_ta "dong đủ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 0.50s xay "đường băng lấn vịnh theo tháng 1941–43": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 3.00s lua "bụi đá nổ ở vách bắc": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 3.94s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 5.92s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_2 7.89s bien_co_tu_dac_ta "khói xuất hiện": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_3 0.50s xay "phố 1943 từng nhà (ghost AMS M981) + đườ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_4 6.00s may_bay "1941–42: máy bay tụ dần trên đường băng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 0.50s may_bay "máy bay xếp kín hai bên đường băng": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N4_5 20.25s tau "đoàn tàu đổ bộ qua eo biển": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_1 21.39s nguoi "1985: rào gỡ, người qua lại trở lại": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_2 0.50s nguoi "người đi bộ băng qua đường băng giờ cao ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_2 8.50s nguoi "dòng người qua cổng sang phía La Línea (": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_3 0.50s nguoi "sáng: dòng người từ La Línea sang Gibral": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_3 5.97s ngay_dem "mặt trời mọc (≈ 08:35)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_3 18.84s nguoi "giờ tan tầm: dòng người về đông lên": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_4 0.50s nguoi "7/2026: kiểm tra thường lệ dừng — người ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) N5_4 13.15s pha "hàng rào cũ gỡ từng đoạn": không khớp mốc nào trong đặc tả (±0.3 s)
- … 18 mục nữa
### BIEN-CO-V
- (c) khoảng dài nhất không biến cố ĐO 19.62 s > 6 s (từ 1:02.6)
### K-LAI-2
- (d) không khai phat_hanh.mo_ta (mô tả + bình luận ghim)
### O2
- chưa soi: khai khối o2: {nam | nam_theo} và chạy --o2 <master> --o2-api (Claude API, có chi phí)
### PP-1
- (e) thẻ PP1: 31 từ / 9.0 s = 3.4 từ/s > 3 (khó đọc trên điện thoại)
### TL-1
- (d) shot C3 góc cao trôi 2.46 % khung/s > 2 (trung vị 11 cửa sổ 1 s)
- (d) shot C4 góc cao trôi 3.19 % khung/s > 2 (trung vị 8 cửa sổ 1 s)
- (d) shot C5 góc cao trôi 3.71 % khung/s > 2 (trung vị 9 cửa sổ 1 s)
- (d) shot N2_11 góc cao trôi 8.24 % khung/s > 2 (trung vị 22 cửa sổ 1 s)
- (d) shot N5_5 góc cao trôi 3.13 % khung/s > 2 (trung vị 18 cửa sổ 1 s)
- (e) 35 điểm máy cao (cần 6–8)
- (f) điểm máy D7-lai → WCA-than → D7-lai: chỉ ở năm 2026-10-19 15:00 — phải quay lại ở năm khác
- (f) điểm máy K2: chỉ ở năm 2026-10-19 23:53 — phải quay lại ở năm khác
- (f) điểm máy D7h-lai: chỉ ở năm 1938.6 — phải quay lại ở năm khác
- (f) điểm máy K-co: chỉ ở năm 1704-08-04 08:30 — phải quay lại ở năm khác
- (f) điểm máy B-thap → K-co → E-bac: chỉ ở năm 1713-07-13 09:00 — phải quay lại ở năm khác
- (f) điểm máy A2-thap → L-linea: chỉ ở năm 1704.8 — phải quay lại ở năm khác
- (f) điểm máy L-linea → T-trai-bac: chỉ ở năm 1779-06-20 09:00 — phải quay lại ở năm khác
- (f) điểm máy E (V7B-a): chỉ ở năm 1779-07-12 16:00 — phải quay lại ở năm khác
- (f) điểm máy Ca2-lai: chỉ ở năm 1780-01-14 10:00 — phải quay lại ở năm khác
- (f) điểm máy Bm-thap → M1 → Bm-thap: chỉ ở năm 1780-01-18 18:10 — phải quay lại ở năm khác
- (f) điểm máy Cc2-lai → M4: chỉ ở năm 1781-04-12 09:20 — phải quay lại ở năm khác
- (f) điểm máy D-vach-thap → E-vach: chỉ ở năm 1782-05-25 12:00 — phải quay lại ở năm khác
- (f) điểm máy D-bac-thap: chỉ ở năm 1782-09-08 06:30 — phải quay lại ở năm khác
- (f) điểm máy B-cao-lai → Al-pin-thap: chỉ ở năm 1782-09-11 09:00 — phải quay lại ở năm khác
- (f) điểm máy B-lan: chỉ ở năm 1782-09-13 06:45 — phải quay lại ở năm khác
- (f) điểm máy D-bac-thap → W-cong-su → T-trai-bac: chỉ ở năm 1782-10-01 12:00 — phải quay lại ở năm khác
- (f) điểm máy SF-thap → SB-thap: chỉ ở năm 1783.6 — phải quay lại ở năm khác
- (f) điểm máy B-thap: chỉ ở năm 1810.3 — phải quay lại ở năm khác
- (f) điểm máy H-lai: chỉ ở năm 1849.0 — phải quay lại ở năm khác
- (f) điểm máy H-thap → F-hang-rao: chỉ ở năm 1900.0 — phải quay lại ở năm khác
- (f) điểm máy D2-thap: chỉ ở năm 1933.5 — phải quay lại ở năm khác
- (f) điểm máy D-thap-dong → D-thap-tay: chỉ ở năm 1939.2 — phải quay lại ở năm khác
- (f) điểm máy W-vinh-thap → D-vach-thap: chỉ ở năm 1941.6 — phải quay lại ở năm khác
- (f) điểm máy Bb-lai: chỉ ở năm 1940-05-20 12:00 — phải quay lại ở năm khác
- (f) điểm máy D-duongbang: chỉ ở năm 1942.3 — phải quay lại ở năm khác
- (f) điểm máy D-cong-thap → D-cong: chỉ ở năm 1966.0 — phải quay lại ở năm khác
- (f) điểm máy D → H: chỉ ở năm 2026-10-19 08:10 — phải quay lại ở năm khác
- (f) điểm máy H-lai → D-cong-thap → H-lai: chỉ ở năm 2026-10-19 07:30 — phải quay lại ở năm khác
- (f) điểm máy D-cong-thap → F-hang-rao: chỉ ở năm 2026-07-14 10:00 — phải quay lại ở năm khác
- (f) điểm máy B-lui: chỉ ở năm 2026-10-18 16:00 — phải quay lại ở năm khác
- (f) điểm máy D7-lai-nguoc: chỉ ở năm 1730.0 — phải quay lại ở năm khác
### XEM-CAM
- (b) không có kết quả chủ dự án xem tắt tiếng
### EO-DAT-R1
- (a) N1_4 @1:44.5: chủ thể 11.5 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N1_6 @2:27.6: chủ thể 2.4 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) C1 @2:53.1: chủ thể 6.6 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N2_10 @4:30.2: chủ thể 5.4 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N2_7 @4:48.5: chủ thể 10.6 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N2_11 @5:55.0: chủ thể 8.0 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N3_1 @6:22.6: chủ thể 3.7 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N3_4 @7:15.3: chủ thể 11.1 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N3_5 @7:42.3: chủ thể 6.5 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N4_1 @7:51.6: chủ thể 14.1 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N4_2 @8:17.1: chủ thể 14.3 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
- (a) N4_5 @9:18.6: chủ thể 11.3 % khung (pixel thô) < 15 % · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)
### EO-DAT-R3
- (a) N4_5 @9:18.6 (27.2 s): 1 góc máy < 2
- (a) N5_6 @12:05.0 (20.0 s): 1 góc máy < 2
### CONG-BO-1
- (a) không khai phat_hanh.mo_ta (mô tả + bình luận ghim) — cần câu công bố có "AI" hoặc "synthetic" trong mô tả YouTube của gói phát hành
