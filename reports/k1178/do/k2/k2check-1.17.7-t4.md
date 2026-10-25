# Luật kênh 2 (checks 1.17.7) — k2c-t4-02-anim3 — TRƯỢT

| Mục | Kiểm | Kết quả | Cấp (1.12.1) | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) |
|---|---|---|---|---|---|---|
| Q26b | Đa dạng bối cảnh (1.16: cảnh tl/* theo vùng) | **TRƯỢT** |  | 1 bối cảnh · lớn nhất the 2.1 % · liên tục dài nhất the 16.0 s · nửa sau 0 · trung tính 97.9 % | ≤ 25 % · ≤ 90 s · nửa sau ≥ 3 |  |
| Q32 | Footage/ảnh nguồn ngoài | **ĐẠT** |  | không dùng footage ngoài | ≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5× |  |
| Q33 | Lặp cảnh | **ĐẠT** |  | 0 góc máy · 0 lần xuất hiện · nhiều nhất — 0 lần · 0 góc > 2 · chưa đo pHash (không có master) | ≤ 2 lần |  |
| Q34 | Loại shot | **TRƯỢT** |  | 65/97 shot có type · scene3d 74.2 % · card 2.1 % · số neo 3D 100 %, chỉ card 0 % (0 số) · địa danh 0 · nhân vật 0 | type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document ≤ 3 s · record ≤ 12 s + dòng tô + nguồn |  |
| Q35 | Nhãn loại số (D5) | **ĐẠT** |  | mô hình đặc tả · 196 khung xét · ACTUAL nhiều nhất 0/khung · lỗi a 0 · b 0 · c 0 · d 0 | ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL |  |
| Q36 | Chữ trên màn hình | **ĐẠT** |  | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực (+ 1 lần trong câu miễn trừ 0:00–0:15) |  |
| Q37 | Nhịp thị giác (1.16: miễn khung neo/im lặng ≤ 10 s; 1.17.4: + thẻ PP cuối phim) | **TRƯỢT** |  | 770.9 s · biến cố khai 134 + đo video 1621 (gộp 1468) · TB 0.53 s · dài nhất 20.21 s · khung tĩnh (khung liền < 0.6/255) dài nhất 10.38 s (từ 4:29.1) · miễn khung neo/im lặng (1.16): 2 khoảng, dài nhất trước miễn 20.21 s · biến cố đo trên video (1.17.4, q_bcv): 1621 | TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s |  |
| A1–A13 | Âm thanh (tập cũ — chỉ báo) | **CHỈ BÁO** |  | CHỈ BÁO · A1 -15.2 LUFS · A2 -2.9 dBTP · A5 0 đoạn · A7 0 · A4 không có stem (--vo/--bed) và mix.json không có smr · A8 0 | docs/AUDIO-THUOC-DO.md | A1 I = -15.2 LUFS (ngưỡng -15 / -13.8) |
| ML1 | Mạch truyện | **CẢNH BÁO** | Chặn (b), (c) · Cảnh báo (a) ở T3 (Chặn từ T4) — lỗi Chặn 0, Cảnh báo 2 | 92/97 shot gắn (0 suy từ mốc @từ) · timelapse 572.3 s, trôi 4.0 % | mỗi shot gắn câu/claim · timelapse trôi ≤ 15 % |  |
| ML2 | Lời lặp ý | **ĐẠT** | Chặn có giải trình (người quyết; không vào mã thoát tự động) — lỗi Chặn 0, Cảnh báo 0 | 0 câu · 0 cặp ứng viên (chấm 0) · 0 lặp ý · không khai tóm tắt | n-gram/IDF + chấm ngữ nghĩa ghim mô hình; ngoài tóm tắt cuối |  |
| ML3 | Lời mời đăng ký | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 câu mời: không có · 0 luận điểm chính khai | 60 s cuối hoặc ±5 s ranh chương · không trong 20 s trước luận điểm chính |  |
| FT1 | Chỉ báo footage/ảnh | **ĐẠT** | Cảnh báo (20 % footage đã Chặn ở Q32 b2) — lỗi Chặn 0, Cảnh báo 0 | 0 shot footage/ảnh · tính 0.0 s = 0.0 % (miễn ảnh nhỏ 0.0 s) · khai lý do: 0/0 | ≤ 20 % (trần) · mỗi shot có lý do · ảnh ≤ 1/3 khung ≤ 6 s không tính |  |
| NHIP-K2 | Nhịp kênh 2 (Q14–Q18 không áp → Q37) | **TRƯỢT** | Chặn (như Q37) — lỗi Chặn 2, Cảnh báo 0 | Q37: 770.9 s · biến cố khai 134 + đo video 1621 (gộp 1468) · TB 0.53 s · dài nhất 20.21 s · khung tĩnh (khung liền < 0.6/255) dài nhất 10.38 s (từ 4:29.1) · miễn khung neo/im lặng (1.16): 2 khoảng, dài nhất trước miễn 20.21 s · biến cố đo trên video (1.17.4, q_bcv): 1621 | TB ≤ 3,5 s · dài nhất ≤ 6 s |  |
| Q26b-K2 | Đa dạng loại cảnh + vùng | **TRƯỢT** | Chặn (c), (d), (e) (như Q26b) · Cảnh báo (a), (b) — lỗi Chặn 1, Cảnh báo 3 | loại: 3d 74.2 %, khac 23.7 %, the_so 2.1 % · 0 vùng, lớn nhất — · nửa sau 0 vùng · không vùng 100.0 % | ≥ 3 loại/nửa · loại ≤ 70 % · vùng ≤ 25 %, ≤ 90 s, nửa sau ≥ 3 |  |
| Q33-K2 | Lặp cảnh (vùng, góc) + pHash L/ΔE | **ĐẠT** | Chặn (như Q33) — lỗi Chặn 0, Cảnh báo 0 | 0 khoá (vùng, góc) · 0 lần xuất hiện · nhiều nhất — 0 · 0 khoá > 2 | ≤ 2 lần (miễn: khác chương + khác năm/lớp) |  |
| Q32b-K2 | Trần clip/ảnh | **ĐẠT** | Chặn (như Q32b) — lỗi Chặn 0, Cảnh báo 0 | 0 clip/ảnh ·  | footage ≤ 8 s · ảnh có máy/chú thích đổi ≤ 12 s · ảnh tĩnh ≤ 8 s |  |
| NC-H1 | Thành phố có nhà | **ĐẠT** | Chặn (a), (b) (đúng lỗi chủ dự án nêu ở T2) — lỗi Chặn 0, Cảnh báo 0 | 0 shot thành phố (0.0 s; khai 0, suy 0) · có lớp nhà khai 0 · không lớp nhà 0 · không đo fabric 0 | fabric trung vị ≥ 25 % · không khung < 15 % (trừ ≤ 3 s cuối reveal) |  |
| NC-H2 | Địa cầu | **CẢNH BÁO** | Chặn (a), (b) — lỗi Chặn 0, Cảnh báo 1 | 0 lần · 0.0 s (0.0 % phim) · map/globe 0.0 s · bản đồ nổi tầm cao 0.0 s · dài nhất 0 s | AGL > 50 km: ≤ 1 lần/tập · ≤ 3 s/lần |  |
| NC-H3 | Tầm mặc định | **CẢNH BÁO** | Cảnh báo — lỗi Chặn 0, Cảnh báo 1 | 3D địa lý 0.0 s · AGL ≤ 60 km 0.0 % · ≤ 3 km 0.0 % · có thành phố: không | AGL ≤ 60 km ≥ 70 % 3D · có thành phố: AGL ≤ 3 km ≥ 40 % |  |
| NC-H4 | Nơi có tên | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 shot bản đồ · chip nơi 0 · nhãn địa danh 0 · thiếu 0 (nguồn: đặc tả, không log chữ) | mọi shot bản đồ: chip nơi hoặc nhãn địa danh |  |
| NC-H5 | Đúng thời kỳ | **ĐẠT** | Chặn (a) · Cảnh báo (b) — lỗi Chặn 0, Cảnh báo 0 | tập không có bộ đếm năm (cảnh tl/* có opt.year/counter, hoặc p.counter) | năm xây ≤ bộ đếm (nam_khung) · ghost có nguồn + nguồn trong mô tả (§12.1: không nhãn trên hình) |  |
| Q7/Q8-K2 | Nhãn/loại số nhận estimate (khiếu nại TT5 i) | **ĐẠT** | Chặn (thay Q7/Q8 cho kênh 2, như Q35) — lỗi Chặn 0, Cảnh báo 0 | Q7 nhận ESTIMATE: 0 lỗi (không log: chỉ kiểm kind khai) · Q8 loại số: 0 lỗi | kind ∈ actual/projection/estimate (kênh 2) · đủ nhãn, không thừa nhãn |  |
| Q33 (1.13) | Lặp cảnh — pHash bỏ lớp chữ cố định | **ĐẠT** | Chặn (thay Q33 cho kênh 2) — lỗi Chặn 0, Cảnh báo 0 | 0 góc máy · 0 lần xuất hiện · nhiều nhất — 0 lần · 0 góc > 2 · chưa đo pHash (không có master) | ≤ 2 lần · pHash L vùng nội dung y 18–72 %, θ 16 |  |
| Q36 (1.13) | Chữ — câu miễn trừ nhận theo chữ | **ĐẠT** | Chặn (thay Q36 cho kênh 2) — lỗi Chặn 0, Cảnh báo 0 | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | "This video explains… Facts as of" 1 lần trong 0:00–0:15 không đòi nguồn luật |  |
| Q37 (1.13) | Nhịp — khung tĩnh theo khung neo | **TRƯỢT** | Chặn (thay Q37 cho kênh 2) — lỗi Chặn 3, Cảnh báo 0 | 770.9 s · biến cố khai 134 + đo video 1621 (gộp 1468) · TB 0.53 s · dài nhất 20.21 s · khung tĩnh (neo, < 2.0/255) dài nhất 8.92 s (từ 12:35.0) · trôi chậm (thước cũ > 6 s, không tĩnh): 8 quãng, dài nhất 10.38 s từ 4:29.1 · miễn khung neo/im lặng (1.16): 2 khoảng, dài nhất trước miễn 20.21 s · biến cố đo trên video (1.17.4, q_bcv): 1621 | khung tĩnh (mọi khung khác khung đầu quãng < 2,0/255) ≤ 6 s | khung tĩnh 5.96 s từ 11:22.0 (ngưỡng 6.0); khung tĩnh 5.96 s từ 11:28.0 (ngưỡng 6.0) |
| BIEN-CO-V | Biến cố thấy được ĐO trên video (K117-D8) | **CẢNH BÁO** | Chặn (b), (c), (h) ở G2 khi thước đạt hiệu chuẩn (q_bcv.HIEU_CHUAN + (h) trên tập) · Cảnh báo ở animatic hoặc khi chưa hiệu chuẩn — K117-D8 — lỗi Chặn 0, Cảnh báo 1 | 770.9 s · biến cố đo 1621 (gộp 1454; cắt 271) · TB 0.53 s · dài nhất 20.25 s · miễn 2 khoảng (the_pp) · ranh shot bắt 95/96 (99.0 %) · hiệu chuẩn T3: ĐẠT (T3 5b9f0bcc…: θ 8, k 2; R cắt 100/100 %, R beat 90,8/98,2 %, Δt TV 0,05/0,04 s, báo nhầm 0) | TB khoảng biến cố đo ≤ 3,5 s · dài nhất ≤ 6 s (miễn khung neo/im lặng/thẻ PP ≤ 10 s) · bắt ≥ 95 % ranh shot |  |
| BD-1…BD-8 | Bản đồ chiến lược / inset / ranh | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | không có shot strategic, lớp ranh, tuyến hay inset |  |  |
| K-R1…K-R9 | ĐỎ-K | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập không khai rui_ro: do-k |  |  |
| K-LAI-1 | LAI: thời lượng khung AI | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 1.17.7 (Q2/C11): minh hoạ M-d 159.87 s (20.7 %) tính ở MINH-HOA/N2P-6 (tổng AI ≤ 70 %), không tính trần 20 % · AI ngoài M-d 0.00 s / 770.87 s (timeline) = 0.0 % · nguồn: log shot (0 shot ai_image ngoài M-d) | ai_image/ai_texture NGOÀI minh hoạ M-d ≤ 20 % thời lượng (1.17.7, tập từ T4: M-d tính ở MINH-HOA/N2P-6 — Q2/C11) |  |
| K-LAI-2 | LAI: công bố AI (§12.1) | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | thẻ phương pháp có (1.17.2: không đòi câu AI) · mô tả không · log chữ không · cờ AI: log shot | cờ ai_* mọi khung (hoặc mọi shot log) · shot khai khớp log · mô tả "AI use = Yes" · KHÔNG nhãn trên hình (1.17.2: bỏ "thẻ PP nói AI") |  |
| K-LAI-3 | LAI: kiểm dữ kiện từng tấm C | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 2, Cảnh báo 0 | minh hoạ: 27 đoạn · kiểm ĐẠT 25 · thiếu tệp kiểm 2 | mỗi tấm C: loi_chac_cuoi 0 · nghi vấn đã xử lý · ngoại lệ có duyệt · không chấm mù |  |
| K-LAI-4 | LAI: vùng bảo vệ = A | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 27 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | sai khác TB < 1/255 trên mặt nạ bao_ve (PNG) |  |
| K-LAI-5 | LAI: một tấm, ban ngày, đêm ≤ 1,5× A | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 27 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | ≤ 1 tấm/khung neo × mốc · ≤ 2 lần sinh lại · chỉ lượt ngày · đêm ≤ 1,5× A |  |
| K-LAI-6 | LAI: sổ gọi API | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 88 lệnh AI · $5.6741 · C2PA 84/84 | model, prompt, % mặt nạ, usage, $, C2PA, giờ |  |
| K-LAI-B | LAI: bão hoà khung (P2-3) | **ĐẠT** | Cảnh báo (P2-3) — lỗi Chặn 0, Cảnh báo 0 | 27 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | bão hoà trung vị ≤ 0,40 mỗi khung LAI |  |
| K-LAI-3V | LAI: nghi vấn còn ghi của vân (1.16) | **ĐẠT** | Chặn ở cổng G2 (bản phát hành) · Cảnh báo ở animatic (K116-D5) — lỗi Chặn 0, Cảnh báo 0 | không có khung ai_texture | tệp vân dùng không còn nghi vấn chưa xử lý (Chặn ở G2 · Cảnh báo ở animatic — K116-D5) |  |
| O2 | Máy soi lỗi thời đại (lưới lọc thứ hai) | **CẢNH BÁO** | Cảnh báo (lưới lọc thứ hai — không thay kiểm nguồn) — lỗi Chặn 0, Cảnh báo 1 | — | 1 khung/5 s + khung neo · cờ/quân phục/tàu/đèn/xe/vật hiện đại/chữ/kiến trúc theo năm · không thay kiểm nguồn |  |
| SACH-1 | Khung sạch §12.1 + TL-4 | **TRƯỢT** | Chặn (a)–(f) (K116-D1; (e) chữ bản đồ Chặn theo K116-D3: ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ) — lỗi Chặn 1, Cảnh báo 0 | 97 shot · tấm số/trích 0 · tư liệu đứng riêng 0 · không log chữ | chỉ bộ đếm · chip nơi ≤ 3 s · thẻ chương · thẻ phương pháp · bản đồ ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ (K116-D3); không tấm số/trích, không tư liệu đứng riêng (phủ ≤ 3 s) |  |
| CHUONG-1 | Thẻ chương §13.3 | **ĐẠT** | Chặn (a)–(e) · Cảnh báo (f) vị trí/mờ (K116-D1) — lỗi Chặn 0, Cảnh báo 0 | 5 thẻ (đặc tả) · dài nhất 3.00 s · 1:08.5 1666 — The Great Fire; 5:17.0 1666 — Rebuilding on the old s; 8:09.0 1711 — The dome rules the skyl; 9:19.5 1940 — The second great fire | ≤ 8/tập · "năm — ≤ 6 từ" · ≤ 3 s · không trong móc · trung tính | thẻ '1666 — The Great Fir' s 3.0 (ngưỡng 3.0); thẻ '1666 — Rebuilding on' s 3.0 (ngưỡng 3.0); thẻ '1711 — The dome rule' s 3.0 (ngưỡng 3.0); thẻ '1940 — The second gr' s 3.0 (ngưỡng 3.0); thẻ '1946 — Second rebuil' s 3.0 (ngưỡng 3.0) |
| PP-1 | Thẻ phương pháp (D6) | **CẢNH BÁO** | Chặn (a)–(d) · Cảnh báo (e) tốc độ đọc ≤ 3 từ/s (K116-D1, D8: ≈ 8 s = 7–9 s) — lỗi Chặn 0, Cảnh báo 1 | 2 thẻ · PP1 9.0 s, PP2 7.0 s · 53 từ | 2 thẻ × 7–9 s, cuối phim · nguồn/bản đồ + chỗ ước tính (1.17.2: không đòi câu AI) · ≤ 3 từ/s | thẻ PP1 s (cận trên) 9.0 (ngưỡng 9.0); thẻ PP2 s (cận dưới) 7.0 (ngưỡng 7.0) |
| TL-1 | Xương sống timelapse §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; mục tiêu §13.6, hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 13 | thân phim 754.9 s · góc cao + tl 513.6 s (68.0 %) · đặc tả ≤ 7.63 cắt/phút (cận trên) · video 99 cắt = 7.79/phút (thô) − 0 cắt góc R3 (so_goc/goc_may) − 59 ranh vào/ra M-d/tư liệu/ảnh thật (1.17.7; trước miễn 7.79/phút) = 3.10/phút tính trần · đặc tả 96 ranh = 7.63/phút · khớp ±0.5 s 92 (chỉ video 7: 0:56.2, 1:02.8, 7:28.0, 7:34.1, 8:26.8, 8:29.2…; chỉ đặc tả 4 — cùng góc máy đổi năm/giờ hoặc chưa cắt) · trôi góc cao trung vị 0.36 %/s (54 shot) · ngưỡng hiệu chỉnh sau V7-PILOT | góc cao + thời gian chạy ≥ 75 % (1.17.7: `tl1_muc_tieu_pct` theo tập) · ≤ 5 cắt/phút (video: đổi cấu trúc; đối chiếu đặc tả ±0,5 s; 1.17.2: cắt góc R3 so_goc/goc_may không tính trần; 1.17.7 từ T4: ranh vào/ra M-d, tư liệu, ảnh thật không tính) · trôi ≤ 2 %/s · 6–8 điểm máy (hiệu chỉnh sau V7-PILOT) | shot H1-18a trôi %/s 2.06 (ngưỡng 2.0) |
| TL-2 | Lướt thấp §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 7 | lướt thấp 7 shot · 58.7 s = 7.8 % · ngưỡng hiệu chỉnh sau V7-PILOT | lướt thấp ≤ 10 % · có vai, phố/người (hiệu chỉnh sau V7-PILOT) |  |
| TL-3 | Không shot trống §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 64 | 63 shot 3D · không đổi 0 · trống 0 · thiếu trong_pct 63 | mỗi shot 3D: thời gian chạy hoặc biến cố · trống ≤ 60 % (hiệu chỉnh sau V7-PILOT) |  |
| NHIP-NGHIA | Nhịp → vật mang nghĩa §13.2 | **ĐẠT** | Chặn (K116-D1; §13.2) — lỗi Chặn 0, Cảnh báo 0 | 92/92 nhịp chính có vật mang nghĩa = 100.0 % | ≥ 90 % nhịp chính |  |
| XEM-CAM | Cổng XEM CÂM §13.4 | **TRƯỢT** | Chặn (K116-D1, D2; §13.4 bắt buộc từ T3) — lỗi Chặn 1, Cảnh báo 0 | — | 8 câu · 3 AI + chủ dự án · tắt tiếng · chủ dự án ≥ 6/8 VÀ TB AI ≥ 6/8 (K116-D2) |  |
| PC-1 | Thước phục chế §12.3 | **ĐẠT** | Cảnh báo (K116-D1; thước tạm, hiệu chuẩn trên ≥ 10 ảnh) — lỗi Chặn 0, Cảnh báo 0 | tập không khai phuc_che: (không dùng ảnh phục chế) | Δ cạnh mới so bicubic ≤ 1,0 điểm % · PSNR ≥ bicubic |  |
| MINH-HOA | Minh hoạ AI §14.1 (c) / §15 M-d | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.1 (c) N2 / §15 M-d) — lỗi Chặn 0, Cảnh báo 39 | 27 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a, H1-05b/H1-05b, H1-06b/H1-06b) · 159.9 s = 20.7 % (từ T4: không trần cứng — Q2; xem GEMINI-NGAN-SACH, N2P-6 (c), GOC-CAO (1.17.7; trước: GOC-CAO-60)) · lỗi kẹp 12 · AGL 0 · sổ AI 27 · nhãn: không bắt buộc (1.17.2) | theo đoạn khai: ≤ 20 % · kẹp giữa 2 khung 3D · máy ≤ 40 m AGL · sổ AI mỗi đoạn (1.17.2: không nhãn bắt buộc) |  |
| EO-DAT-R1 | Eo đất R1 — chủ thể | **ĐẠT** | Chỉ báo ở mọi cổng — chủ dự án chấm bằng mắt (1.17.2, V2-D2 duyệt 22/10 11:09); in pixel thô + vùng nở 1,5 % bề ngang (§14.7 R1 "≥ 15–20 %") — lỗi Chặn 0, Cảnh báo 0 | không shot khai chu_the_eo_dat | chu_the_eo_dat: chủ thể ≥ 15 % khung · 15–20 % (§14.7) — CHỈ BÁO mọi cổng, in pixel thô + vùng nở 1.5 % (1.17.2) |  |
| EO-DAT-R2 | Eo đất R2 — cỏ/cát trống | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R2: trống > 50 % ≤ 6 s liên tục, ≤ 10 % thời lượng chương) — lỗi Chặn 0, Cảnh báo 0 | không shot eo đất (noi: eo_dat) | trống (> 50 %) liên tục ≤ 6 s · mỗi chương ≤ 10 % thời lượng chương (§14.7) |  |
| EO-DAT-R3 | Eo đất R3 — góc + biến cố | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.7 R3) — lỗi Chặn 0, Cảnh báo 0 | không shot eo đất (noi: eo_dat) | shot eo đất > 15 s: ≥ 2 góc · biến cố cách ≤ 6 s |  |
| EO-DAT-R4 | Eo đất R4 — câu lời không vật | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R4 + TL-4; lệnh K-1.17.1) — lỗi Chặn 0, Cảnh báo 0 | không shot khai loi_khong_vat_eo_dat | loi_khong_vat_eo_dat: noi ∈ pho/lau_dai/cang hoặc bản đồ phủ ≤ 3 s (§14.7, TL-4) |  |
| CONG-BO-1 | Công bố AI ở gói phát hành (1.17.2) | **CẢNH BÁO** | Chặn ở gói phát hành (`cong: phat_hanh` | `phat_hanh.goi: true`) · chỉ báo (Cảnh báo) ở mọi cổng trước — §14.1 (f), YouTube "AI use" — lỗi Chặn 0, Cảnh báo 2 | áp vì: 27 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a) · 27 shot log ai_image (H1-01a, H1-01b, H1-02, H1-05a) · 27 shot đặc tả ai_image (H1-01a/0, H1-01b/0, H1-02/0, H1-05a/0) · mô tả không khai · youtube_altered_content None | khung AI hoặc giọng tổng hợp → mô tả YouTube có câu "AI"/"synthetic" · phat_hanh.youtube_altered_content: true (Chặn ở gói phát hành) |  |
| N2P-1 | N2+ (i) lớp (a) sau ghép | **CẢNH BÁO** | Chặn (a), (b), (d) vòng khớp màu cục bộ, (e) lớp sống ở G2 · Cảnh báo ở animatic · (c) cụm dải 20 px luôn Cảnh báo (người đọc tờ so) — §15 (c)(i); (d)(e) 1.17.5 — lỗi Chặn 0, Cảnh báo 3 | 1 tấm · max lệch (a) 42/255 · vật (a) mô hình 0 · cụm dải 20 px 3 | 0/255 trong (a) · 0 vật (a) thêm/bớt/đổi · cụm ΔE ≥ 30 trong dải 20 px → người đọc · (1.17.5) lớp sống cộng hiệu ≤ 1/255 · vòng khớp màu cục bộ · (1.17.6) tấm BMN: trừ nhà đo được nở 1 px |  |
| N2P-2 | N2+ (ii) lỗi thời đại (2 mô hình + O2) | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(ii), K đề xuất — lỗi Chặn 0, Cảnh báo 1 | 1 tấm · lỗi có năm 0 · nghi vấn không năm 0 (người đọc) · q_thoi_dai mới 0 · giới hạn: cờ ~20 px không bảo đảm | 0 lỗi có năm (gpt ∪ claude) · O2 mới so render 0 |  |
| N2P-3 | N2+ (iii) đổi loại vùng T9b | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(iii); 1.17.5: nước→đất = T9c (c) bờ lấn, (d) giữa nước (đối chứng render) — lỗi Chặn 0, Cảnh báo 1 | 1 tấm · T9b lớn nhất 0.01 % · mô hình báo 0 · T9c (1.17.5): đoạn bờ lấn 0, sâu nhất 0.0 px, giữa nước ≤ 0.57 %; T9b nước→đất (chỉ in) 0.79 % | T9b đất→nước ≤ 2 % · (1.17.5) T9c: 0 bờ lấn ≥ 6 px · giữa nước ≤ 2 % · 0 báo mô hình · (1.17.6) khung không nước: T9c KHÔNG ÁP |  |
| N2P-4 | N2+ (iv) đóng băng trên tấm tĩnh | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(iv), K đề xuất — lỗi Chặn 0, Cảnh báo 1 | 1 tấm (1 tĩnh) · vật chuyển động 0 | 0 vật chuyển động trên tấm tĩnh |  |
| N2P-5 | N2+ (v) nhấp nháy + chuyển tấm | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic — §15 (b), (c)(v), K đề xuất — lỗi Chặn 0, Cảnh báo 1 | 1 shot tấm nền · chưa đo | hoà ≥ 2 s · ≤ 1 ΔE/khung · nhấp nháy ≤ 1,5 × đối chứng |  |
| N2P-6 | N2+ (vi) trần §15(d) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §15 (d) trần, K đề xuất — lỗi Chặn 0, Cảnh báo 0 | 770.9 s · tấm nền 0.8 % (1) · minh hoạ 20.7 % (27; không trần cứng từ 1.17.4 — Q2) · tổng AI 21.5 % (28) | tấm nền ≤ 50 % · minh hoạ ≤ 20 % · tổng AI ≤ 70 % · không chồng shot |  |
| MAY-19 | Ngữ pháp máy §19 (a) | **CẢNH BÁO** | Chặn (a)–(g) ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — §19 (a) — lỗi Chặn 0, Cảnh báo 4 | 63 shot cú máy · log khung 63 · tóm tắt 0 · loại/chương HỒI 1:7, HỒI 2:9, HỒI 3:5, HỒI 4:5, HỒI 5:9, MÓC:3 · THAP 5.2 % · lỗi a 2 b 0 c 0 d 1 e 0 f 0 · cảnh báo w 0 | tốc độ theo cú máy (log khung) · N2+ = CODINH · KHOP ≤ 0,5 px · ≥ 4 loại/chương · ≤ 2 liền · THAP ≤ 12 % |  |
| BAN-DO-12 | Bản đồ ≤ 12 % §19 (b) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §19 (b) — lỗi Chặn 0, Cảnh báo 0 | 33.5 s / 770.9 s = 4.34 % | MAP + MAP3D ≤ 12 % · ≤ 10 s/lần |  |
| TU-LIEU-10 | Tư liệu + khắc + thẻ ≤ trần tập §19 (c) | **ĐẠT** | Chặn (a) trần theo tập `tu_lieu_tran_pct` (mặc định 10 %, ≤ 15 %), (b) mỗi lần ≤ 10 s, (k) khai sai trần ở G2 · Cảnh báo ở animatic — §19 (c); 1.17.6 (chủ dự án 24/10 12:52) — lỗi Chặn 0, Cảnh báo 0 | 94.7 s / 770.9 s = 12.28 % / trần 20 % (khai tu_lieu_tran_pct) (TL 8 · KHAC 25 · THE 44 · THAT 17.6667 s) · lần dài nhất 8.0 s | TL + KHAC + THE (+ THAT) ≤ tu_lieu_tran_pct (mặc định 10 %, ≤ 20 % từ 1.17.7) · mỗi lần ≤ 10 s |  |
| AI-TU-LIEU | Không AI lên tư liệu §19 (b)(c) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §19 (b)(c) — lỗi Chặn 0, Cảnh báo 0 | 9 shot có tư liệu · 41 SHA tư liệu · 378 dòng sổ AI đối chiếu | 0 shot tư liệu có AI · 0 dòng sổ AI có SHA tư liệu |  |
| GEMINI-NGAN-SACH | Ngân sách Gemini của tập (Q2 i) | **ĐẠT** | Chặn (a) vượt ngân sách, (u) thiếu giá thật ở G2 · Cảnh báo (k) thiếu khai, (m) vượt mốc theo dõi · Cảnh báo ở animatic — Q2 (i) — lỗi Chặn 0, Cảnh báo 0 | 202 lệnh Gemini · $15.07 / ngân sách $55 (mốc $50) | tổng usd sổ Gemini ≤ ngan_sach_gemini_usd |  |
| GOC-CAO | Góc cao timelapse + 5 chốt cấu trúc (Q2 iii; 1.17.7) | **CẢNH BÁO** | Chặn (p) tỉ lệ ≥ goc_cao_min_pct, (a)–(d) 5 chốt cấu trúc, (k) khai sai ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — Q2 (iii) + gói tiết kiệm — lỗi Chặn 0, Cảnh báo 1 | 498.7 s / 754.9 s = 66.1 % / ngưỡng 50 % (log khung V7B-D1: 63 shot) · cấu trúc: mở/kết 1 lỗi · P1/hồi 0 · liền 0 · chương ≥ 40 %: MÓC 96, HỒI 1 53, HỒI 2 62, HỒI 3 65, HỒI 4 64, HỒI 5 86 | goc cao + tl (V7B-D1 theo log khung, trừ THAT) ≥ goc_cao_min_pct (mặc định 60, ≥ 50) · khi < 60 / khai cấu trúc: chương mở+kết góc cao · P1 mỗi hồi (cùng khung) · ≤ 2 liền {thấp, cận, M-d, THAT} · mỗi chương ≥ goc_cao_chuong_min_pct (40) |  |
| TU-LIEU-OMNI | Tư liệu không chồng/ghép liền clip M-d (1.17.6) | **CẢNH BÁO** | Chặn (a) tư liệu trùng clip M-d, (b) ghép liền clip M-d (< 1 shot / < 1 s 3D) ở G2 · Cảnh báo ở animatic — 1.17.6 (chủ dự án 24/10 12:52) — lỗi Chặn 0, Cảnh báo 18 | 23 lần tư liệu · 27 clip M-d · trùng 0 · ghép liền 18 | không trùng clip M-d · cách ≥ 1 shot 3D hoặc ≥ 1 s 3D |  |
| TU-LIEU-THAT | Ảnh chụp/footage thật (1.17.7) | **ĐẠT** | Chặn (a) THAT có AI, (g) footage hiện đại thiếu giấy phép (tệp + SHA) ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — §19 (c) + gói tiết kiệm — lỗi Chặn 0, Cảnh báo 0 | 4 shot có lớp THAT · 17.7 s (tính vào tư liệu, không tính AI, không tính góc cao) | THAT không AI · không tính góc cao · footage hiện đại có giay_phep {tep, sha256} |  |
| NHAN-VAT-TEN | Nhân vật có tên trong M-d (1.17.7, P2 b) | **CẢNH BÁO** | Chặn (a) cận mặt > 1/8 khung, (k) chân dung tham chiếu, (u) thiếu duyệt chủ dự án, (m) không đo được ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — P2 b — lỗi Chặn 0, Cảnh báo 6 | 3 đoạn M-d có nhân vật có tên · mặt lớn nhất/khung: H1-05a/H1-05a 0.068, H1-15b/H1-15b 0.162, H3-05b/H3-05b 0.070 (trần 1/8 = 0.125; YuNet điểm ≥ 0.75) | chan_dung_tham_chieu (SHA) · duyet_chu_du_an · mặt lớn nhất ≤ 1/8 chiều cao khung (YuNet ≥ 0,75) |  |
| KIEM-2-MUC | Kiểm 2 mức day_du/nen (1.17.7) | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic — kiểm 2 mức day_du / nen (gói tiết kiệm) — lỗi Chặn 0, Cảnh báo 1 | 27 đoạn M-d · day_du 25 · nen 2 · lỗi a 0 b 1 c 0 d 0 k 0 | muc_kiem mỗi đoạn · nhân vật/công trình có tên, chân trời City → day_du · nen: Flash + tờ khung, ≤ 2 lượt · day_du: 2 tầng + q_thoi_dai (lớp mốc khi có mốc), ≤ 3 lượt |  |
| BE-MAT-NHA | AI phủ bề mặt nhà thường (phương án B) | **ĐẠT** | Chặn (a)–(e) ở G2 · Cảnh báo ở animatic · (w) mô hình nhìn không năm/hình khối luôn Cảnh báo — phương án B (AI phủ bề mặt nhà thường) — lỗi Chặn 0, Cảnh báo 0 | không tấm nào khai be_mat_nha_ai: true | (a) hình khối từng nhà đo được (≥ be_mat_nha_px_m_min px/m, mặc định 2) · (b) khoá 0/255 · (c) 0 lỗi thời đại · (d) quỹ đạo sáng theo điểm ảnh/nhấp nháy · (e) khung 0 chiếu 3D ở độ phân giải video · (w) cạnh màu mới |  |
| LOCK | checks/ khớp LOCK (1.17.7) | **ĐẠT** |  | KHỚP |  |  |

## Âm thanh A1–A13
| Mục | Kiểm | Loại | Kết quả | Giá trị | Ngưỡng |
|---|---|---|---|---|---|
| A1 | Loudness tích hợp (master sau AAC) | chặn | BÁO | -15.2 LUFS | -15.0 … -13.8 |
| A2 | Đỉnh thật sau AAC | chặn | ĐẠT | -2.9 dBTP | ≤ -1.0 |
| A3 | Biên độ loudness LRA | báo | BÁO | 8.5 LU | 2–8 (báo) |
| A4 | Lời trên nhạc (SMR) | chặn | BÁO | không có stem (--vo/--bed) và mix.json không có smr | p10 ≥ 15 · min ≥ 12 |
| A5 | Lặng bất thường ≥ 1 s (< −50 LUFS tức thời) | chặn | ĐẠT | 0 đoạn | 0 |
| A6 | Tỉ lệ lặng | báo | ĐẠT | 0.09 % | báo |
| A7 | Chạm trần (≥ 3 mẫu |x| ≥ 0,999) | chặn | ĐẠT | 0 | 0 |
| A8 | Chồng lời | chặn | ĐẠT | 0 | 0 |
| A9 | ASR hai cách nghe | chặn | BÁO | không chạy (--no-asr) | 100 % đoạn |
| A10 | Quãng không lời > 8 s không khai khoảnh khắc nhạc | báo | BÁO | dài nhất 29.3 s · 3 quãng (7:39.4, 9:10.8, 10:32.3) | > 8 s (báo) |
| A11 | Giao nhạc | chặn | — | không đo (mix.json không phải chuỗi mới) | ≤ 1 ô nhịp · không lặp |
| A12 | Loudnorm tuyến tính | chặn | — | không đo (mix.json không phải chuỗi mới) | linear |
| A13 | Đồng bộ tiếng | báo | — | không đo (không có stem lời --vo) | ≤ 5 ms (báo) |

## Chi tiết lỗi
### Q26b
- nửa sau (6:25.4–12:50.9) chỉ có 0 bối cảnh (≥ 3 s): —
### Q34
- (0) H1-01a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-01b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-02/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-05a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-05b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-06b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-07b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-10/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-12/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-11b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-14/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-15m/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-15b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-17a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-17b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-18t/0: type tu_lieu ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-01a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-01b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-03c/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-04b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-07/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-13/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H3-01t/0: type tu_lieu ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H3-02t/0: type tu_lieu ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H3-03t/0: type tu_lieu ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H3-04b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H3-05b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H4-01b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H4-03/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H4-04b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H4-04d/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H4-06t/0: type tu_lieu ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
### Q37
- (c) khoảng dài nhất 20.21 s > 6.0 s (từ video 344.25s (video:o))
- (d) khung tĩnh 10.38 s > 6.0 s (từ 4:29.1)
### ML1
- PP1/0 @12:34.9 (card, 9.0 s): không gắn câu lời hay claim
- PP2/0 @12:43.9 (card, 7.0 s): không gắn câu lời hay claim
### NHIP-K2
- (c) khoảng dài nhất 20.21 s > 6.0 s (từ video 344.25s (video:o))
- (d) khung tĩnh 10.38 s > 6.0 s (từ 4:29.1)
### Q26b-K2
- (a) nửa đầu: 1 loại cảnh ≥ 3 s (3d) < 3
- (a) nửa sau: 2 loại cảnh ≥ 3 s (3d, the_so) < 3
- (b) loại 3d chiếm 74.2 % > 70 %
- (e) nửa sau (6:25.4–12:50.9) 0 vùng ≥ 3 s (—) < 3
### NC-H2
- không có shot bản đồ/địa cầu có máy quay đọc được
### NC-H3
- không có thời lượng 3D địa lý
### Q37 (1.13)
- (c) khoảng dài nhất 20.21 s > 6.0 s (từ video 344.25s (video:o))
- (d) khung tĩnh 8.92 s > 6.0 s (từ 12:35.0)
- (d) khung tĩnh 6.92 s > 6.0 s (từ 12:44.0)
### BIEN-CO-V
- (c) khoảng dài nhất không biến cố ĐO 20.25 s > 6 s (từ 5:44.2)
### K-LAI-2
- (d) không khai phat_hanh.mo_ta (mô tả + bình luận ghim)
### K-LAI-3
- H1-06b/H1-06b: không có tệp kiểm (mục đoạn `kiem` hoặc lai.kiem_minh_hoa.H1-06b)
- H1-15m/H1-15m: không có tệp kiểm (mục đoạn `kiem` hoặc lai.kiem_minh_hoa.H1-15m)
### O2
- chưa soi: khai khối o2: {nam | nam_theo} và chạy --o2 <master> --o2-api (Claude API, có chi phí)
### SACH-1
- (c) không có log chữ (--logs k2.js) — không đo được chữ thực hiện trên hình; (d) chip nơi chưa đo
### PP-1
- (e) thẻ PP2: 24 từ / 7.0 s = 3.4 từ/s > 3 (khó đọc trên điện thoại)
### TL-1
- (d) shot H1-07 góc cao trôi 2.38 % khung/s > 2 (trung vị 8 cửa sổ 1 s)
- (d) shot H1-09 góc cao trôi 3.35 % khung/s > 2 (trung vị 7 cửa sổ 1 s)
- (d) shot H1-18a góc cao trôi 2.06 % khung/s > 2 (trung vị 4 cửa sổ 1 s)
- (d) shot H2-11 góc cao trôi 4.10 % khung/s > 2 (trung vị 4 cửa sổ 1 s)
- (d) shot H5-03 góc cao trôi 4.36 % khung/s > 2 (trung vị 4 cửa sổ 1 s)
- (f) điểm máy P1: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P8: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P2: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P6h: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P5: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P7: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P9: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P3: chỉ ở năm ? — phải quay lại ở năm khác
### TL-2
- (b) shot H1-13a: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H1-13c: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H2-04a: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H2-05s: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H2-10: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H5-02s: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H5-05b: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
### TL-3
- (c) shot M00: không ghi `bac` căn cứ
- (c) shot M01: không ghi `bac` căn cứ
- (c) shot M02: không ghi `bac` căn cứ
- (c) shot M03: không ghi `bac` căn cứ
- (c) shot M04: không ghi `bac` căn cứ
- (c) shot H1-01h: không ghi `bac` căn cứ
- (c) shot H1-02h: không ghi `bac` căn cứ
- (c) shot H1-03: không ghi `bac` căn cứ
- (c) shot H1-04: không ghi `bac` căn cứ
- (c) shot H1-05h: không ghi `bac` căn cứ
- (c) shot H1-06: không ghi `bac` căn cứ
- (c) shot H1-07: không ghi `bac` căn cứ
- (c) shot H1-08b: không ghi `bac` căn cứ
- (c) shot H1-09: không ghi `bac` căn cứ
- (c) shot H1-11: không ghi `bac` căn cứ
- (c) shot H1-13a: không ghi `bac` căn cứ
- (c) shot H1-12x: không ghi `bac` căn cứ
- (c) shot H1-13c: không ghi `bac` căn cứ
- (c) shot H1-15: không ghi `bac` căn cứ
- (c) shot H1-15h: không ghi `bac` căn cứ
- (c) shot H1-16: không ghi `bac` căn cứ
- (c) shot H1-18a: không ghi `bac` căn cứ
- (c) shot H1-18b: không ghi `bac` căn cứ
- (c) shot H2-00: không ghi `bac` căn cứ
- (c) shot H2-02: không ghi `bac` căn cứ
- (c) shot H2-03b: không ghi `bac` căn cứ
- (c) shot H2-04h: không ghi `bac` căn cứ
- (c) shot H2-04a: không ghi `bac` căn cứ
- (c) shot H2-05: không ghi `bac` căn cứ
- (c) shot H2-05s: không ghi `bac` căn cứ
- (c) shot H2-06: không ghi `bac` căn cứ
- (c) shot H2-08: không ghi `bac` căn cứ
- (c) shot H2-09: không ghi `bac` căn cứ
- (c) shot H2-10: không ghi `bac` căn cứ
- (c) shot H2-11: không ghi `bac` căn cứ
- (c) shot H2-12: không ghi `bac` căn cứ
- (c) shot H2-14: không ghi `bac` căn cứ
- (c) shot H3-01: không ghi `bac` căn cứ
- (c) shot H3-02: không ghi `bac` căn cứ
- (c) shot H3-03: không ghi `bac` căn cứ
- (c) shot H3-04a: không ghi `bac` căn cứ
- (c) shot H3-05: không ghi `bac` căn cứ
- (c) shot H3-06: không ghi `bac` căn cứ
- (c) shot H4-01a: không ghi `bac` căn cứ
- (c) shot H4-02: không ghi `bac` căn cứ
- (c) shot H4-04a: không ghi `bac` căn cứ
- (c) shot H4-04c: không ghi `bac` căn cứ
- (c) shot H4-05: không ghi `bac` căn cứ
- (c) shot H4-06: không ghi `bac` căn cứ
- (c) shot H4-07: không ghi `bac` căn cứ
- (c) shot H4-08: không ghi `bac` căn cứ
- (c) shot H5-01: không ghi `bac` căn cứ
- (c) shot H5-02: không ghi `bac` căn cứ
- (c) shot H5-02s: không ghi `bac` căn cứ
- (c) shot H5-03: không ghi `bac` căn cứ
- (c) shot H5-04: không ghi `bac` căn cứ
- (c) shot H5-05a: không ghi `bac` căn cứ
- (c) shot H5-05c: không ghi `bac` căn cứ
- (c) shot H5-05b: không ghi `bac` căn cứ
- (c) shot H5-06: không ghi `bac` căn cứ
- … 4 mục nữa
### XEM-CAM
- không khai `xem_cam:` trong episode.yaml — cổng XEM CÂM bắt buộc từ T3 (§13.4); K không tự chấm
### MINH-HOA
- (c) H1-01a/H1-01a @1:11.0–1:16.0: không kẹp giữa hai khung 3D (trước: H1-01h @2.98 s goc cao; sau: H1-01b @0.02 s trong đoạn minh hoạ khác)
- (c) H1-01b/H1-01b @1:16.0–1:19.8: không kẹp giữa hai khung 3D (trước: H1-01a @4.98 s trong đoạn minh hoạ khác; sau: H1-02h @0.02 s goc cao)
- (c) H1-10/H1-10 @3:12.4–3:19.5: không kẹp giữa hai khung 3D (trước: H1-09 @8.98 s goc cao; sau: H1-12 @0.02 s trong đoạn minh hoạ khác)
- (c) H1-12/H1-12 @3:19.5–3:25.9: không kẹp giữa hai khung 3D (trước: H1-10 @7.06 s trong đoạn minh hoạ khác; sau: H1-11 @0.02 s goc cao)
- (c) H1-15m/H1-15m @4:15.5–4:21.5: không kẹp giữa hai khung 3D (trước: H1-15 @7.98 s goc cao; sau: H1-15b @0.02 s trong đoạn minh hoạ khác)
- (c) H1-15b/H1-15b @4:21.5–4:29.0: không kẹp giữa hai khung 3D (trước: H1-15m @5.98 s trong đoạn minh hoạ khác; sau: H1-15h @0.02 s goc cao)
- (c) H1-17a/H1-17a @4:47.9–4:53.9: không kẹp giữa hai khung 3D (trước: H1-16 @7.23 s goc cao; sau: H1-17b @0.02 s trong đoạn minh hoạ khác)
- (c) H1-17b/H1-17b @4:53.9–5:00.2: không kẹp giữa hai khung 3D (trước: H1-17a @5.98 s trong đoạn minh hoạ khác; sau: H1-18a @0.02 s goc cao)
- (c) H2-01a/H2-01a @5:19.5–5:24.5: không kẹp giữa hai khung 3D (trước: H2-00 @2.98 s goc cao; sau: H2-01b @0.02 s trong đoạn minh hoạ khác)
- (c) H2-01b/H2-01b @5:24.5–5:29.7: không kẹp giữa hai khung 3D (trước: H2-01a @4.98 s trong đoạn minh hoạ khác; sau: H2-02 @0.02 s goc cao)
- (c) H3-04b/H3-04b @8:45.4–8:51.3: không kẹp giữa hai khung 3D (trước: H3-04a @4.98 s goc cao; sau: H3-05b @0.02 s trong đoạn minh hoạ khác)
- (c) H3-05b/H3-05b @8:51.3–8:57.3: không kẹp giữa hai khung 3D (trước: H3-04b @5.94 s trong đoạn minh hoạ khác; sau: H3-05 @0.02 s goc cao)
- (e) H1-01a/H1-01a @1:11.0–1:16.0: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-01b/H1-01b @1:16.0–1:19.8: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-02/H1-02 @1:21.8–1:28.7: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-05a/H1-05a @1:55.2–2:00.2: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-05b/H1-05b @2:02.2–2:05.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-06b/H1-06b @2:25.4–2:29.7: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-07b/H1-07b @2:39.2–2:45.2: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-10/H1-10 @3:12.4–3:19.5: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-12/H1-12 @3:19.5–3:25.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-11b/H1-11b @3:34.3–3:40.3: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-14/H1-14 @4:01.0–4:07.5: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-15m/H1-15m @4:15.5–4:21.5: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-15b/H1-15b @4:21.5–4:29.0: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-17a/H1-17a @4:47.9–4:53.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-17b/H1-17b @4:53.9–5:00.2: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-01a/H2-01a @5:19.5–5:24.5: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-01b/H2-01b @5:24.5–5:29.7: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-03c/H2-03c @6:04.5–6:10.5: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-04b/H2-04b @6:16.5–6:22.2: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-07/H2-07 @6:58.3–7:06.2: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-13/H2-13 @7:56.5–8:02.5: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H3-04b/H3-04b @8:45.4–8:51.3: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H3-05b/H3-05b @8:51.3–8:57.3: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H4-01b/H4-01b @9:25.0–9:31.0: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H4-03/H4-03 @9:41.9–9:49.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H4-04b/H4-04b @9:57.4–10:03.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H4-04d/H4-04d @10:07.9–10:12.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
### CONG-BO-1
- (a) không khai phat_hanh.mo_ta (mô tả + bình luận ghim) — cần câu công bố có "AI" hoặc "synthetic" trong mô tả YouTube của gói phát hành
- (b) đặc tả gói không khai phat_hanh.youtube_altered_content (cần true — "AI use" = Yes ở YouTube Studio)
### N2P-1
- (a) tấm P9-2026-oai-l2 (H5-05a): lớp (a) sau ghép lệch tối đa 42/255 ở 947697 điểm (cần 0)
- (c) tấm P9-2026-oai-l2 (H5-05a): 3 cụm ΔE ≥ 30 trong dải 20 px quanh (a) (người đọc tờ so): [993, 735, 1002, 774] 218 px, [1463, 860, 1482, 870] 140 px, [1515, 884, 1534, 894] 113 px
- (b) tấm P9-2026-oai-l2 (H5-05a): mô hình nhìn — chưa soi: không có trong bộ đệm và không chạy --vision (mô hình nhìn có chi phí ≈ $0,2/khung)
### N2P-2
- tấm P9-2026-oai-l2 (H5-05a): mô hình nhìn — chưa soi: không có trong bộ đệm và không chạy --vision (mô hình nhìn có chi phí ≈ $0,2/khung)
### N2P-3
- tấm P9-2026-oai-l2 (H5-05a): mô hình nhìn — chưa soi: không có trong bộ đệm và không chạy --vision (mô hình nhìn có chi phí ≈ $0,2/khung)
### N2P-4
- tấm P9-2026-oai-l2 (H5-05a): mô hình nhìn — chưa soi: không có trong bộ đệm và không chạy --vision (mô hình nhìn có chi phí ≈ $0,2/khung)
### N2P-5
- H5-05a: shot tấm nền chưa có video đo (n2p.video: ghep + render đối chứng + mat_na)
### MAY-19
- (a) H2-10 THAP: ngửa 4.35…7.34° ngoài 5–15°
- (a) H5-05b THAP: ngửa 3.95…6.94° ngoài 5–15°
- (d) chương MÓC: 3 loại cú máy (DAY, KEO, LAN) < 4
- (g) H1-18t: cu_may 'TL' không thuộc §19 (a) (CODINH, DAY, KEO, CAU, VONG, TRUOT, NGHIENG, THAP, XUONG, LAN, KHOP)
### GOC-CAO
- (a) chương HỒI 1: mở bằng H1-01h (cao) — phải là shot góc cao
### TU-LIEU-OMNI
- (b) H1-06 (125.9–145.4 s) ↔ clip M-d H1-05b (122.2–125.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-06 (125.9–145.4 s) ↔ clip M-d H1-06b (145.4–149.7 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-09 (183.4–192.4 s) ↔ clip M-d H1-10 (192.4–199.5 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-09 (183.4–192.4 s) ↔ clip M-d H1-12 (199.5–205.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-09 (183.4–192.4 s) ↔ clip M-d H1-11b (214.3–220.3 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-11 (205.9–214.3 s) ↔ clip M-d H1-10 (192.4–199.5 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-11 (205.9–214.3 s) ↔ clip M-d H1-12 (199.5–205.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-11 (205.9–214.3 s) ↔ clip M-d H1-11b (214.3–220.3 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-18a (300.2–306.2 s) ↔ clip M-d H1-17a (287.9–293.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-18a (300.2–306.2 s) ↔ clip M-d H1-17b (293.9–300.2 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-18t (306.2–311.2 s) ↔ clip M-d H1-17a (287.9–293.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s
- (b) H1-18t (306.2–311.2 s) ↔ clip M-d H1-17b (293.9–300.2 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s
- (b) H2-02 (329.9–337.9 s) ↔ clip M-d H2-01a (319.5–324.5 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.20 s < 1 s
- (b) H2-02 (329.9–337.9 s) ↔ clip M-d H2-01b (324.5–329.7 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.20 s < 1 s
- (b) H3-05 (537.3–551.0 s) ↔ clip M-d H3-04b (525.4–531.3 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H3-05 (537.3–551.0 s) ↔ clip M-d H3-05b (531.3–537.3 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H4-02 (571.0–581.9 s) ↔ clip M-d H4-01b (565.0–571.0 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H4-02 (571.0–581.9 s) ↔ clip M-d H4-03 (581.9–589.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
### NHAN-VAT-TEN
- (a) H1-15b/H1-15b (Samuel Pepys): mặt cao 0.162 khung > 1/8 ở 1/84 khung đo (đầu tiên khung 124, clip) — cận mặt nhân vật có tên
- (k) H3-05b/H3-05b (Godfrey Allen): chưa khai `chan_dung_tham_chieu: {tep, sha256}`
- (w) H1-15b/H1-15b: 6 hộp điểm 0.6–0.75 cao > 1/8 (lớn nhất 0.197 @khung 118) — người soi: có phải mặt cận?
- (u) H1-05a/H1-05a (Samuel Pepys, Charles II): chưa khai `duyet_chu_du_an` (dòng AUTHORSHIP chủ dự án duyệt nhân vật có tên trong M-d)
- (u) H1-15b/H1-15b (Samuel Pepys): chưa khai `duyet_chu_du_an` (dòng AUTHORSHIP chủ dự án duyệt nhân vật có tên trong M-d)
- (u) H3-05b/H3-05b (Godfrey Allen): chưa khai `duyet_chu_du_an` (dòng AUTHORSHIP chủ dự án duyệt nhân vật có tên trong M-d)
### KIEM-2-MUC
- (b) H1-06b/H1-06b: tầng Flash kết luận 'LOẠI' (cần ĐẠT)
