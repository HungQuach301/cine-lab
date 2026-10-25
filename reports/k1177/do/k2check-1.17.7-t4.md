# Luật kênh 2 (checks 1.17.7) — k2c-t4-02-anim — TRƯỢT

| Mục | Kiểm | Kết quả | Cấp (1.12.1) | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) |
|---|---|---|---|---|---|---|
| Q26b | Đa dạng bối cảnh (1.16: cảnh tl/* theo vùng) | **TRƯỢT** |  | 1 bối cảnh · lớn nhất the 2.2 % · liên tục dài nhất the 16.0 s · nửa sau 0 · trung tính 97.8 % | ≤ 25 % · ≤ 90 s · nửa sau ≥ 3 |  |
| Q32 | Footage/ảnh nguồn ngoài | **ĐẠT** |  | không dùng footage ngoài | ≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5× |  |
| Q33 | Lặp cảnh | **ĐẠT** |  | 0 góc máy · 0 lần xuất hiện · nhiều nhất — 0 lần · 0 góc > 2 · chưa đo pHash (không có master) | ≤ 2 lần |  |
| Q34 | Loại shot | **TRƯỢT** |  | 52/75 shot có type · scene3d 77.4 % · card 2.2 % · số neo 3D 100 %, chỉ card 0 % (0 số) · địa danh 0 · nhân vật 0 | type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document ≤ 3 s · record ≤ 12 s + dòng tô + nguồn |  |
| Q35 | Nhãn loại số (D5) | **ĐẠT** |  | mô hình đặc tả · 152 khung xét · ACTUAL nhiều nhất 0/khung · lỗi a 0 · b 0 · c 0 · d 0 | ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL |  |
| Q36 | Chữ trên màn hình | **ĐẠT** |  | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực (+ 1 lần trong câu miễn trừ 0:00–0:15) |  |
| Q37 | Nhịp thị giác (1.16: miễn khung neo/im lặng ≤ 10 s; 1.17.4: + thẻ PP cuối phim) | **TRƯỢT** |  | 730.1 s · biến cố khai 100 + đo video 1706 (gộp 1319) · TB 0.55 s · dài nhất 16.5 s · khung tĩnh (khung liền < 0.6/255) dài nhất 10.42 s (từ 0:00.0) · miễn khung neo/im lặng (1.16): 1 khoảng, dài nhất trước miễn 16.5 s · biến cố đo trên video (1.17.4, q_bcv): 1706 | TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s |  |
| A1–A13 | Âm thanh (tập cũ — chỉ báo) | **CHỈ BÁO** |  | CHỈ BÁO · A1 -14.0 LUFS · A2 2.6 dBTP · A5 0 đoạn · A7 0 · A4 không có stem (--vo/--bed) và mix.json không có smr · A8 0 | docs/AUDIO-THUOC-DO.md | A1 I = -14.0 LUFS (ngưỡng -15 / -13.8) |
| ML1 | Mạch truyện | **CẢNH BÁO** | Chặn (b), (c) · Cảnh báo (a) ở T3 (Chặn từ T4) — lỗi Chặn 0, Cảnh báo 4 | 64/75 shot gắn (0 suy từ mốc @từ) · timelapse 565.4 s, trôi 9.3 % | mỗi shot gắn câu/claim · timelapse trôi ≤ 15 % |  |
| ML2 | Lời lặp ý | **ĐẠT** | Chặn có giải trình (người quyết; không vào mã thoát tự động) — lỗi Chặn 0, Cảnh báo 0 | 0 câu · 0 cặp ứng viên (chấm 0) · 0 lặp ý · không khai tóm tắt | n-gram/IDF + chấm ngữ nghĩa ghim mô hình; ngoài tóm tắt cuối |  |
| ML3 | Lời mời đăng ký | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 câu mời: không có · 0 luận điểm chính khai | 60 s cuối hoặc ±5 s ranh chương · không trong 20 s trước luận điểm chính |  |
| FT1 | Chỉ báo footage/ảnh | **ĐẠT** | Cảnh báo (20 % footage đã Chặn ở Q32 b2) — lỗi Chặn 0, Cảnh báo 0 | 0 shot footage/ảnh · tính 0.0 s = 0.0 % (miễn ảnh nhỏ 0.0 s) · khai lý do: 0/0 | ≤ 20 % (trần) · mỗi shot có lý do · ảnh ≤ 1/3 khung ≤ 6 s không tính |  |
| NHIP-K2 | Nhịp kênh 2 (Q14–Q18 không áp → Q37) | **TRƯỢT** | Chặn (như Q37) — lỗi Chặn 14, Cảnh báo 0 | Q37: 730.1 s · biến cố khai 100 + đo video 1706 (gộp 1319) · TB 0.55 s · dài nhất 16.5 s · khung tĩnh (khung liền < 0.6/255) dài nhất 10.42 s (từ 0:00.0) · miễn khung neo/im lặng (1.16): 1 khoảng, dài nhất trước miễn 16.5 s · biến cố đo trên video (1.17.4, q_bcv): 1706 | TB ≤ 3,5 s · dài nhất ≤ 6 s |  |
| Q26b-K2 | Đa dạng loại cảnh + vùng | **TRƯỢT** | Chặn (c), (d), (e) (như Q26b) · Cảnh báo (a), (b) — lỗi Chặn 1, Cảnh báo 3 | loại: 3d 77.4 %, khac 20.4 %, the_so 2.2 % · 0 vùng, lớn nhất — · nửa sau 0 vùng · không vùng 100.0 % | ≥ 3 loại/nửa · loại ≤ 70 % · vùng ≤ 25 %, ≤ 90 s, nửa sau ≥ 3 |  |
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
| Q37 (1.13) | Nhịp — khung tĩnh theo khung neo | **TRƯỢT** | Chặn (thay Q37 cho kênh 2) — lỗi Chặn 23, Cảnh báo 0 | 730.1 s · biến cố khai 100 + đo video 1706 (gộp 1319) · TB 0.55 s · dài nhất 16.5 s · khung tĩnh (neo, < 2.0/255) dài nhất 10.38 s (từ 9:13.5) · trôi chậm (thước cũ > 6 s, không tĩnh): 10 quãng, dài nhất 10.38 s từ 3:41.4 · miễn khung neo/im lặng (1.16): 1 khoảng, dài nhất trước miễn 16.5 s · biến cố đo trên video (1.17.4, q_bcv): 1706 | khung tĩnh (mọi khung khác khung đầu quãng < 2,0/255) ≤ 6 s | khung tĩnh 5.83 s từ 11:09.0 (ngưỡng 6.0); khung tĩnh 5.83 s từ 11:15.0 (ngưỡng 6.0); khung tĩnh 5.75 s từ 5:53.0 (ngưỡng 6.0); khung tĩnh 5.71 s từ 10:54.0 (ngưỡng 6.0) |
| BIEN-CO-V | Biến cố thấy được ĐO trên video (K117-D8) | **CẢNH BÁO** | Chặn (b), (c), (h) ở G2 khi thước đạt hiệu chuẩn (q_bcv.HIEU_CHUAN + (h) trên tập) · Cảnh báo ở animatic hoặc khi chưa hiệu chuẩn — K117-D8 — lỗi Chặn 0, Cảnh báo 1 | 730.1 s · biến cố đo 1706 (gộp 1305; cắt 524) · TB 0.56 s · dài nhất 16.5 s · miễn 1 khoảng (the_pp) · ranh shot bắt 73/74 (98.6 %) · hiệu chuẩn T3: ĐẠT (T3 5b9f0bcc…: θ 8, k 2; R cắt 100/100 %, R beat 90,8/98,2 %, Δt TV 0,05/0,04 s, báo nhầm 0) | TB khoảng biến cố đo ≤ 3,5 s · dài nhất ≤ 6 s (miễn khung neo/im lặng/thẻ PP ≤ 10 s) · bắt ≥ 95 % ranh shot |  |
| BD-1…BD-8 | Bản đồ chiến lược / inset / ranh | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | không có shot strategic, lớp ranh, tuyến hay inset |  |  |
| K-R1…K-R9 | ĐỎ-K | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập không khai rui_ro: do-k |  |  |
| K-LAI-1 | LAI: thời lượng khung AI | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 1.17.7 (Q2/C11): minh hoạ M-d 148.67 s (20.4 %) tính ở MINH-HOA/N2P-6 (tổng AI ≤ 70 %), không tính trần 20 % · AI ngoài M-d 0.00 s / 730.08 s (timeline) = 0.0 % · nguồn: log shot (0 shot ai_image ngoài M-d) | ai_image/ai_texture NGOÀI minh hoạ M-d ≤ 20 % thời lượng (1.17.7, tập từ T4: M-d tính ở MINH-HOA/N2P-6 — Q2/C11) |  |
| K-LAI-2 | LAI: công bố AI (§12.1) | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | thẻ phương pháp có (1.17.2: không đòi câu AI) · mô tả không · log chữ không · cờ AI: log shot | cờ ai_* mọi khung (hoặc mọi shot log) · shot khai khớp log · mô tả "AI use = Yes" · KHÔNG nhãn trên hình (1.17.2: bỏ "thẻ PP nói AI") |  |
| K-LAI-3 | LAI: kiểm dữ kiện từng tấm C | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | minh hoạ: 23 đoạn · kiểm ĐẠT 23 · thiếu tệp kiểm 0 | mỗi tấm C: loi_chac_cuoi 0 · nghi vấn đã xử lý · ngoại lệ có duyệt · không chấm mù |  |
| K-LAI-4 | LAI: vùng bảo vệ = A | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 23 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | sai khác TB < 1/255 trên mặt nạ bao_ve (PNG) |  |
| K-LAI-5 | LAI: một tấm, ban ngày, đêm ≤ 1,5× A | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 23 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | ≤ 1 tấm/khung neo × mốc · ≤ 2 lần sinh lại · chỉ lượt ngày · đêm ≤ 1,5× A |  |
| K-LAI-6 | LAI: sổ gọi API | **ĐẠT** | Chặn (P2-2) — lỗi Chặn 0, Cảnh báo 0 | 57 lệnh AI · $3.6381 · C2PA 53/53 | model, prompt, % mặt nạ, usage, $, C2PA, giờ |  |
| K-LAI-B | LAI: bão hoà khung (P2-3) | **ĐẠT** | Cảnh báo (P2-3) — lỗi Chặn 0, Cảnh báo 0 | 23 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a): minh hoạ toàn khung (§14.1 (c)) — không có khung A cùng khung / tấm C khung neo để so; kiểm minh hoạ ở K-LAI-3 + MINH-HOA | bão hoà trung vị ≤ 0,40 mỗi khung LAI |  |
| K-LAI-3V | LAI: nghi vấn còn ghi của vân (1.16) | **ĐẠT** | Chặn ở cổng G2 (bản phát hành) · Cảnh báo ở animatic (K116-D5) — lỗi Chặn 0, Cảnh báo 0 | không có khung ai_texture | tệp vân dùng không còn nghi vấn chưa xử lý (Chặn ở G2 · Cảnh báo ở animatic — K116-D5) |  |
| O2 | Máy soi lỗi thời đại (lưới lọc thứ hai) | **CẢNH BÁO** | Cảnh báo (lưới lọc thứ hai — không thay kiểm nguồn) — lỗi Chặn 0, Cảnh báo 1 | — | 1 khung/5 s + khung neo · cờ/quân phục/tàu/đèn/xe/vật hiện đại/chữ/kiến trúc theo năm · không thay kiểm nguồn |  |
| SACH-1 | Khung sạch §12.1 + TL-4 | **TRƯỢT** | Chặn (a)–(f) (K116-D1; (e) chữ bản đồ Chặn theo K116-D3: ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ) — lỗi Chặn 1, Cảnh báo 0 | 75 shot · tấm số/trích 0 · tư liệu đứng riêng 0 · không log chữ | chỉ bộ đếm · chip nơi ≤ 3 s · thẻ chương · thẻ phương pháp · bản đồ ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ (K116-D3); không tấm số/trích, không tư liệu đứng riêng (phủ ≤ 3 s) |  |
| CHUONG-1 | Thẻ chương §13.3 | **ĐẠT** | Chặn (a)–(e) · Cảnh báo (f) vị trí/mờ (K116-D1) — lỗi Chặn 0, Cảnh báo 0 | 5 thẻ (đặc tả) · dài nhất 3.00 s · 0:51.5 1666 — The Great Fire; 4:34.8 1666 — Rebuilding on the old s; 7:20.6 1711 — The dome rules the skyl; 8:28.0 1940 — The second great fire | ≤ 8/tập · "năm — ≤ 6 từ" · ≤ 3 s · không trong móc · trung tính | thẻ '1666 — The Great Fir' s 3.0 (ngưỡng 3.0); thẻ '1666 — Rebuilding on' s 3.0 (ngưỡng 3.0); thẻ '1711 — The dome rule' s 3.0 (ngưỡng 3.0); thẻ '1940 — The second gr' s 3.0 (ngưỡng 3.0); thẻ '1946 — Second rebuil' s 3.0 (ngưỡng 3.0) |
| PP-1 | Thẻ phương pháp (D6) | **CẢNH BÁO** | Chặn (a)–(d) · Cảnh báo (e) tốc độ đọc ≤ 3 từ/s (K116-D1, D8: ≈ 8 s = 7–9 s) — lỗi Chặn 0, Cảnh báo 1 | 2 thẻ · PP1 9.0 s, PP2 7.0 s · 53 từ | 2 thẻ × 7–9 s, cuối phim · nguồn/bản đồ + chỗ ước tính (1.17.2: không đòi câu AI) · ≤ 3 từ/s | thẻ PP1 s (cận trên) 9.0 (ngưỡng 9.0); thẻ PP2 s (cận dưới) 7.0 (ngưỡng 7.0) |
| TL-1 | Xương sống timelapse §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; mục tiêu §13.6, hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 11 | thân phim 714.1 s · góc cao + tl 482.0 s (67.5 %) · đặc tả ≤ 6.22 cắt/phút (cận trên) · video 75 cắt = 6.22/phút (thô) − 0 cắt góc R3 (so_goc/goc_may) − 39 ranh vào/ra M-d/tư liệu/ảnh thật (1.17.7; trước miễn 6.22/phút) = 2.94/phút tính trần · đặc tả 74 ranh = 6.22/phút · khớp ±0.5 s 70 (chỉ video 5: 0:48.1, 4:16.4, 7:37.5, 7:38.8, 7:39.7; chỉ đặc tả 4 — cùng góc máy đổi năm/giờ hoặc chưa cắt) · trôi góc cao trung vị 0.19 %/s (43 shot) · ngưỡng hiệu chỉnh sau V7-PILOT | góc cao + thời gian chạy ≥ 75 % (1.17.7: `tl1_muc_tieu_pct` theo tập) · ≤ 5 cắt/phút (video: đổi cấu trúc; đối chiếu đặc tả ±0,5 s; 1.17.2: cắt góc R3 so_goc/goc_may không tính trần; 1.17.7 từ T4: ranh vào/ra M-d, tư liệu, ảnh thật không tính) · trôi ≤ 2 %/s · 6–8 điểm máy (hiệu chỉnh sau V7-PILOT) | shot H4-07 trôi %/s 2.0 (ngưỡng 2.0) |
| TL-2 | Lướt thấp §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 8 | lướt thấp 7 shot · 83.4 s = 11.7 % · ngưỡng hiệu chỉnh sau V7-PILOT | lướt thấp ≤ 10 % · có vai, phố/người (hiệu chỉnh sau V7-PILOT) |  |
| TL-3 | Không shot trống §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 51 | 50 shot 3D · không đổi 0 · trống 0 · thiếu trong_pct 50 | mỗi shot 3D: thời gian chạy hoặc biến cố · trống ≤ 60 % (hiệu chỉnh sau V7-PILOT) |  |
| NHIP-NGHIA | Nhịp → vật mang nghĩa §13.2 | **ĐẠT** | Chặn (K116-D1; §13.2) — lỗi Chặn 0, Cảnh báo 0 | 64/64 nhịp chính có vật mang nghĩa = 100.0 % | ≥ 90 % nhịp chính |  |
| XEM-CAM | Cổng XEM CÂM §13.4 | **TRƯỢT** | Chặn (K116-D1, D2; §13.4 bắt buộc từ T3) — lỗi Chặn 1, Cảnh báo 0 | 8 câu · AI 3 · chủ dự án 0 · R1 7.5/8, R2 7.5/8, R3 7.5/8 · TB AI 7.50/8 | 8 câu · 3 AI + chủ dự án · tắt tiếng · chủ dự án ≥ 6/8 VÀ TB AI ≥ 6/8 (K116-D2) |  |
| PC-1 | Thước phục chế §12.3 | **ĐẠT** | Cảnh báo (K116-D1; thước tạm, hiệu chuẩn trên ≥ 10 ảnh) — lỗi Chặn 0, Cảnh báo 0 | tập không khai phuc_che: (không dùng ảnh phục chế) | Δ cạnh mới so bicubic ≤ 1,0 điểm % · PSNR ≥ bicubic |  |
| MINH-HOA | Minh hoạ AI §14.1 (c) / §15 M-d | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.1 (c) N2 / §15 M-d) — lỗi Chặn 0, Cảnh báo 35 | 23 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a, H1-05b/H1-05b, H1-08a/H1-08a) · 148.7 s = 20.4 % (từ T4: không trần cứng — Q2; xem GEMINI-NGAN-SACH, N2P-6 (c), GOC-CAO (1.17.7; trước: GOC-CAO-60)) · lỗi kẹp 12 · AGL 0 · sổ AI 23 · nhãn: không bắt buộc (1.17.2) | theo đoạn khai: ≤ 20 % · kẹp giữa 2 khung 3D · máy ≤ 40 m AGL · sổ AI mỗi đoạn (1.17.2: không nhãn bắt buộc) |  |
| EO-DAT-R1 | Eo đất R1 — chủ thể | **ĐẠT** | Chỉ báo ở mọi cổng — chủ dự án chấm bằng mắt (1.17.2, V2-D2 duyệt 22/10 11:09); in pixel thô + vùng nở 1,5 % bề ngang (§14.7 R1 "≥ 15–20 %") — lỗi Chặn 0, Cảnh báo 0 | không shot khai chu_the_eo_dat | chu_the_eo_dat: chủ thể ≥ 15 % khung · 15–20 % (§14.7) — CHỈ BÁO mọi cổng, in pixel thô + vùng nở 1.5 % (1.17.2) |  |
| EO-DAT-R2 | Eo đất R2 — cỏ/cát trống | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R2: trống > 50 % ≤ 6 s liên tục, ≤ 10 % thời lượng chương) — lỗi Chặn 0, Cảnh báo 0 | không shot eo đất (noi: eo_dat) | trống (> 50 %) liên tục ≤ 6 s · mỗi chương ≤ 10 % thời lượng chương (§14.7) |  |
| EO-DAT-R3 | Eo đất R3 — góc + biến cố | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.7 R3) — lỗi Chặn 0, Cảnh báo 0 | không shot eo đất (noi: eo_dat) | shot eo đất > 15 s: ≥ 2 góc · biến cố cách ≤ 6 s |  |
| EO-DAT-R4 | Eo đất R4 — câu lời không vật | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R4 + TL-4; lệnh K-1.17.1) — lỗi Chặn 0, Cảnh báo 0 | không shot khai loi_khong_vat_eo_dat | loi_khong_vat_eo_dat: noi ∈ pho/lau_dai/cang hoặc bản đồ phủ ≤ 3 s (§14.7, TL-4) |  |
| CONG-BO-1 | Công bố AI ở gói phát hành (1.17.2) | **CẢNH BÁO** | Chặn ở gói phát hành (`cong: phat_hanh` | `phat_hanh.goi: true`) · chỉ báo (Cảnh báo) ở mọi cổng trước — §14.1 (f), YouTube "AI use" — lỗi Chặn 0, Cảnh báo 2 | áp vì: 23 đoạn minh hoạ (H1-01a/H1-01a, H1-01b/H1-01b, H1-02/H1-02, H1-05a/H1-05a) · 23 shot log ai_image (H1-01a, H1-01b, H1-02, H1-05a) · 23 shot đặc tả ai_image (H1-01a/0, H1-01b/0, H1-02/0, H1-05a/0) · mô tả không khai · youtube_altered_content None | khung AI hoặc giọng tổng hợp → mô tả YouTube có câu "AI"/"synthetic" · phat_hanh.youtube_altered_content: true (Chặn ở gói phát hành) |  |
| N2P-1 | N2+ (i) lớp (a) sau ghép | **CẢNH BÁO** | Chặn (a), (b), (d) vòng khớp màu cục bộ, (e) lớp sống ở G2 · Cảnh báo ở animatic · (c) cụm dải 20 px luôn Cảnh báo (người đọc tờ so) — §15 (c)(i); (d)(e) 1.17.5 — lỗi Chặn 0, Cảnh báo 1 | — | 0/255 trong (a) · 0 vật (a) thêm/bớt/đổi · cụm ΔE ≥ 30 trong dải 20 px → người đọc · (1.17.5) lớp sống cộng hiệu ≤ 1/255 · vòng khớp màu cục bộ · (1.17.6) tấm BMN: trừ nhà đo được nở 1 px |  |
| N2P-2 | N2+ (ii) lỗi thời đại (2 mô hình + O2) | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(ii), K đề xuất — lỗi Chặn 0, Cảnh báo 1 | — | 0 lỗi có năm (gpt ∪ claude) · O2 mới so render 0 |  |
| N2P-3 | N2+ (iii) đổi loại vùng T9b | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(iii); 1.17.5: nước→đất = T9c (c) bờ lấn, (d) giữa nước (đối chứng render) — lỗi Chặn 0, Cảnh báo 1 | — | T9b đất→nước ≤ 2 % · (1.17.5) T9c: 0 bờ lấn ≥ 6 px · giữa nước ≤ 2 % · 0 báo mô hình · (1.17.6) khung không nước: T9c KHÔNG ÁP |  |
| N2P-4 | N2+ (iv) đóng băng trên tấm tĩnh | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(iv), K đề xuất — lỗi Chặn 0, Cảnh báo 1 | — | 0 vật chuyển động trên tấm tĩnh |  |
| N2P-5 | N2+ (v) nhấp nháy + chuyển tấm | **CẢNH BÁO** | Chặn ở G2 · Cảnh báo ở animatic — §15 (b), (c)(v), K đề xuất — lỗi Chặn 0, Cảnh báo 3 | 3 shot tấm nền · chưa đo | hoà ≥ 2 s · ≤ 1 ΔE/khung · nhấp nháy ≤ 1,5 × đối chứng |  |
| N2P-6 | N2+ (vi) trần §15(d) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §15 (d) trần, K đề xuất — lỗi Chặn 0, Cảnh báo 0 | 730.1 s · tấm nền 6.1 % (3) · minh hoạ 20.4 % (23; không trần cứng từ 1.17.4 — Q2) · tổng AI 26.5 % (26) | tấm nền ≤ 50 % · minh hoạ ≤ 20 % · tổng AI ≤ 70 % · không chồng shot |  |
| MAY-19 | Ngữ pháp máy §19 (a) | **CẢNH BÁO** | Chặn (a)–(g) ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — §19 (a) — lỗi Chặn 0, Cảnh báo 4 | 50 shot cú máy · log khung 50 · tóm tắt 0 · loại/chương HỒI 1:6, HỒI 2:8, HỒI 3:5, HỒI 4:6, HỒI 5:6, MÓC:4 · THAP 9.2 % · lỗi a 0 b 0 c 0 d 0 e 0 f 0 · cảnh báo w 4 | tốc độ theo cú máy (log khung) · N2+ = CODINH · KHOP ≤ 0,5 px · ≥ 4 loại/chương · ≤ 2 liền · THAP ≤ 12 % |  |
| BAN-DO-12 | Bản đồ ≤ 12 % §19 (b) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §19 (b) — lỗi Chặn 0, Cảnh báo 0 | 33.5 s / 730.1 s = 4.58 % | MAP + MAP3D ≤ 12 % · ≤ 10 s/lần |  |
| TU-LIEU-10 | Tư liệu + khắc + thẻ ≤ trần tập §19 (c) | **CẢNH BÁO** | Chặn (a) trần theo tập `tu_lieu_tran_pct` (mặc định 10 %, ≤ 15 %), (b) mỗi lần ≤ 10 s, (k) khai sai trần ở G2 · Cảnh báo ở animatic — §19 (c); 1.17.6 (chủ dự án 24/10 12:52) — lỗi Chặn 0, Cảnh báo 1 | 70.5 s / 730.1 s = 9.66 % / trần 10 % (mặc định) (TL 8 · KHAC 16 · THE 46.5 s) · lần dài nhất 15.0 s | TL + KHAC + THE (+ THAT) ≤ tu_lieu_tran_pct (mặc định 10 %, ≤ 20 % từ 1.17.7) · mỗi lần ≤ 10 s | tư liệu + khắc + thẻ % 9.66 (ngưỡng 10.0) |
| AI-TU-LIEU | Không AI lên tư liệu §19 (b)(c) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §19 (b)(c) — lỗi Chặn 0, Cảnh báo 0 | 7 shot có tư liệu · 17 SHA tư liệu · 219 dòng sổ AI đối chiếu | 0 shot tư liệu có AI · 0 dòng sổ AI có SHA tư liệu |  |
| GEMINI-NGAN-SACH | Ngân sách Gemini của tập (Q2 i) | **ĐẠT** | Chặn (a) vượt ngân sách, (u) thiếu giá thật ở G2 · Cảnh báo (k) thiếu khai, (m) vượt mốc theo dõi · Cảnh báo ở animatic — Q2 (i) — lỗi Chặn 0, Cảnh báo 0 | 105 lệnh Gemini · $8.54 / ngân sách $35 (mốc $30) | tổng usd sổ Gemini ≤ ngan_sach_gemini_usd |  |
| GOC-CAO | Góc cao timelapse + 5 chốt cấu trúc (Q2 iii; 1.17.7) | **ĐẠT** | Chặn (p) tỉ lệ ≥ goc_cao_min_pct, (a)–(d) 5 chốt cấu trúc, (k) khai sai ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — Q2 (iii) + gói tiết kiệm — lỗi Chặn 0, Cảnh báo 0 | 479.5 s / 714.1 s = 67.2 % / ngưỡng 60 % (log khung V7B-D1: 50 shot) · chốt cấu trúc TẮT (ngưỡng 60 %, không khai goc_cao_cau_truc) | goc cao + tl (V7B-D1 theo log khung, trừ THAT) ≥ goc_cao_min_pct (mặc định 60, ≥ 50) · khi < 60 / khai cấu trúc: chương mở+kết góc cao · P1 mỗi hồi (cùng khung) · ≤ 2 liền {thấp, cận, M-d, THAT} · mỗi chương ≥ goc_cao_chuong_min_pct (40) |  |
| TU-LIEU-OMNI | Tư liệu không chồng/ghép liền clip M-d (1.17.6) | **CẢNH BÁO** | Chặn (a) tư liệu trùng clip M-d, (b) ghép liền clip M-d (< 1 shot / < 1 s 3D) ở G2 · Cảnh báo ở animatic — 1.17.6 (chủ dự án 24/10 12:52) — lỗi Chặn 0, Cảnh báo 37 | 18 lần tư liệu · 23 clip M-d · trùng 3 · ghép liền 34 | không trùng clip M-d · cách ≥ 1 shot 3D hoặc ≥ 1 s 3D |  |
| TU-LIEU-THAT | Ảnh chụp/footage thật (1.17.7) | **ĐẠT** | Chặn (a) THAT có AI, (g) footage hiện đại thiếu giấy phép (tệp + SHA) ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — §19 (c) + gói tiết kiệm — lỗi Chặn 0, Cảnh báo 0 | không có shot/lớp ảnh chụp/footage thật (THAT) | THAT không AI · không tính góc cao · footage hiện đại có giay_phep {tep, sha256} |  |
| NHAN-VAT-TEN | Nhân vật có tên trong M-d (1.17.7, P2 b) | **ĐẠT** | Chặn (a) cận mặt > 1/8 khung, (k) chân dung tham chiếu, (u) thiếu duyệt chủ dự án, (m) không đo được ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — P2 b — lỗi Chặn 0, Cảnh báo 0 | không đoạn M-d nào khai nhan_vat_ten | chan_dung_tham_chieu (SHA) · duyet_chu_du_an · mặt lớn nhất ≤ 1/8 chiều cao khung (YuNet ≥ 0,75) |  |
| KIEM-2-MUC | Kiểm 2 mức day_du/nen (1.17.7) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — kiểm 2 mức day_du / nen (gói tiết kiệm) — lỗi Chặn 0, Cảnh báo 0 | tập không khai kiem_2_muc / muc_kiem — giữ kiểm hiện hành (K-LAI-3) | muc_kiem mỗi đoạn · nhân vật/công trình có tên, chân trời City → day_du · nen: Flash + tờ khung, ≤ 2 lượt · day_du: 2 tầng + q_thoi_dai (lớp mốc khi có mốc), ≤ 3 lượt |  |
| BE-MAT-NHA | AI phủ bề mặt nhà thường (phương án B) | **ĐẠT** | Chặn (a)–(e) ở G2 · Cảnh báo ở animatic · (w) mô hình nhìn không năm/hình khối luôn Cảnh báo — phương án B (AI phủ bề mặt nhà thường) — lỗi Chặn 0, Cảnh báo 0 | không tấm nào khai be_mat_nha_ai: true | (a) hình khối từng nhà đo được (≥ be_mat_nha_px_m_min px/m, mặc định 2) · (b) khoá 0/255 · (c) 0 lỗi thời đại · (d) quỹ đạo sáng theo điểm ảnh/nhấp nháy · (e) khung 0 chiếu 3D ở độ phân giải video · (w) cạnh màu mới |  |
| LOCK | checks/ khớp LOCK (1.17.7) | **ĐẠT** |  | KHỚP |  |  |

## Âm thanh A1–A13
| Mục | Kiểm | Loại | Kết quả | Giá trị | Ngưỡng |
|---|---|---|---|---|---|
| A1 | Loudness tích hợp (master sau AAC) | chặn | ĐẠT | -14.0 LUFS | -15.0 … -13.8 |
| A2 | Đỉnh thật sau AAC | chặn | BÁO | 2.6 dBTP | ≤ -1.0 |
| A3 | Biên độ loudness LRA | báo | BÁO | 9.3 LU | 2–8 (báo) |
| A4 | Lời trên nhạc (SMR) | chặn | BÁO | không có stem (--vo/--bed) và mix.json không có smr | p10 ≥ 15 · min ≥ 12 |
| A5 | Lặng bất thường ≥ 1 s (< −50 LUFS tức thời) | chặn | ĐẠT | 0 đoạn | 0 |
| A6 | Tỉ lệ lặng | báo | ĐẠT | 0.00 % | báo |
| A7 | Chạm trần (≥ 3 mẫu |x| ≥ 0,999) | chặn | ĐẠT | 0 | 0 |
| A8 | Chồng lời | chặn | ĐẠT | 0 | 0 |
| A9 | ASR hai cách nghe | chặn | BÁO | không chạy (--no-asr) | 100 % đoạn |
| A10 | Quãng không lời > 8 s không khai khoảnh khắc nhạc | báo | BÁO | dài nhất 34.4 s · 3 quãng (6:45.9, 8:19.3, 9:46.0) | > 8 s (báo) |
| A11 | Giao nhạc | chặn | — | không đo (mix.json không phải chuỗi mới) | ≤ 1 ô nhịp · không lặp |
| A12 | Loudnorm tuyến tính | chặn | — | không đo (mix.json không phải chuỗi mới) | linear |
| A13 | Đồng bộ tiếng | báo | — | không đo (không có stem lời --vo) | ≤ 5 ms (báo) |

## Chi tiết lỗi
### Q26b
- nửa sau (6:05.0–12:10.1) chỉ có 0 bối cảnh (≥ 3 s): —
### Q34
- (0) H1-01a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-01b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-02/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-05a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-05b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-08a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-10/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-12/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-14/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-17a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-17b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H1-19/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-01a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-01b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-03a/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-03c/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-04b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-07/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H2-13/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H3-04b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H4-01b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H4-03/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
- (0) H4-04b/0: type minh_hoa ngoài scene3d/map/chart3d/photo/document/footage/card/record/timelapse/strategic
### Q37
- (a) H1-01b 0.54s the_nhan_vat "Thomas Farriner": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1-03 1.00s tu_lieu "Hollar: London before the Fire (pub. 1666)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1-13 1.00s tu_lieu "The fire at Ludgate, c. 1670": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1-18 3.14s bo_dem "87 churches": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-02 10.98s the_nhan_vat "Robert Hooke": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-06 1.50s tu_lieu "The Monument, engraving": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-06 5.25s bo_dem "202 ft": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-07 3.45s the_nhan_vat "Nicholas Barbon": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-10 4.86s bo_dem "365 ft": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-12 0.50s tu_lieu "Hollar: London before the Fire (pub. 1666)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H4-02 3.50s bo_dem "100,000 incendiaries": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H5-01 4.97s the_nhan_vat "Charles Holden · William Holford": không khớp mốc nào trong đặc tả (±0.3 s)
- (c) khoảng dài nhất 16.5 s > 6.0 s (từ H5-05a 643.12s (cut))
- (d) khung tĩnh 10.42 s > 6.0 s (từ 0:00.0)
### ML1
- H1-19/0 @4:28.2 (minh_hoa, 6.0 s): không gắn câu lời hay claim
- H2-13/0 @7:08.1 (minh_hoa, 6.0 s): không gắn câu lời hay claim
- PP1/0 @11:54.1 (card, 9.0 s): không gắn câu lời hay claim
- PP2/0 @12:03.1 (card, 7.0 s): không gắn câu lời hay claim
### NHIP-K2
- (a) H1-01b 0.54s the_nhan_vat "Thomas Farriner": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1-03 1.00s tu_lieu "Hollar: London before the Fire (pub. 1666)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1-13 1.00s tu_lieu "The fire at Ludgate, c. 1670": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1-18 3.14s bo_dem "87 churches": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-02 10.98s the_nhan_vat "Robert Hooke": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-06 1.50s tu_lieu "The Monument, engraving": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-06 5.25s bo_dem "202 ft": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-07 3.45s the_nhan_vat "Nicholas Barbon": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-10 4.86s bo_dem "365 ft": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-12 0.50s tu_lieu "Hollar: London before the Fire (pub. 1666)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H4-02 3.50s bo_dem "100,000 incendiaries": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H5-01 4.97s the_nhan_vat "Charles Holden · William Holford": không khớp mốc nào trong đặc tả (±0.3 s)
- (c) khoảng dài nhất 16.5 s > 6.0 s (từ H5-05a 643.12s (cut))
- (d) khung tĩnh 10.42 s > 6.0 s (từ 0:00.0)
### Q26b-K2
- (a) nửa đầu: 1 loại cảnh ≥ 3 s (3d) < 3
- (a) nửa sau: 2 loại cảnh ≥ 3 s (3d, the_so) < 3
- (b) loại 3d chiếm 77.4 % > 70 %
- (e) nửa sau (6:05.0–12:10.1) 0 vùng ≥ 3 s (—) < 3
### NC-H2
- không có shot bản đồ/địa cầu có máy quay đọc được
### NC-H3
- không có thời lượng 3D địa lý
### Q37 (1.13)
- (a) H1-01b 0.54s the_nhan_vat "Thomas Farriner": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1-03 1.00s tu_lieu "Hollar: London before the Fire (pub. 1666)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1-13 1.00s tu_lieu "The fire at Ludgate, c. 1670": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H1-18 3.14s bo_dem "87 churches": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-02 10.98s the_nhan_vat "Robert Hooke": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-06 1.50s tu_lieu "The Monument, engraving": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-06 5.25s bo_dem "202 ft": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-07 3.45s the_nhan_vat "Nicholas Barbon": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-10 4.86s bo_dem "365 ft": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H2-12 0.50s tu_lieu "Hollar: London before the Fire (pub. 1666)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H4-02 3.50s bo_dem "100,000 incendiaries": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) H5-01 4.97s the_nhan_vat "Charles Holden · William Holford": không khớp mốc nào trong đặc tả (±0.3 s)
- (c) khoảng dài nhất 16.5 s > 6.0 s (từ H5-05a 643.12s (cut))
- (d) khung tĩnh 10.38 s > 6.0 s (từ 9:13.5)
- (d) khung tĩnh 10.12 s > 6.0 s (từ 10:43.5)
- (d) khung tĩnh 8.92 s > 6.0 s (từ 8:04.0)
- (d) khung tĩnh 8.83 s > 6.0 s (từ 11:00.0)
- (d) khung tĩnh 8.67 s > 6.0 s (từ 11:54.5)
- (d) khung tĩnh 6.71 s > 6.0 s (từ 11:29.5)
- (d) khung tĩnh 6.67 s > 6.0 s (từ 12:03.5)
- (d) khung tĩnh 6.12 s > 6.0 s (từ 0:00.0)
- (d) khung tĩnh 6.12 s > 6.0 s (từ 5:13.0)
- (d) khung tĩnh 6.08 s > 6.0 s (từ 8:13.5)
### BIEN-CO-V
- (c) khoảng dài nhất không biến cố ĐO 16.5 s > 6 s (từ 10:43.2)
### K-LAI-2
- (d) không khai phat_hanh.mo_ta (mô tả + bình luận ghim)
### O2
- chưa soi: khai khối o2: {nam | nam_theo} và chạy --o2 <master> --o2-api (Claude API, có chi phí)
### SACH-1
- (c) không có log chữ (--logs k2.js) — không đo được chữ thực hiện trên hình; (d) chip nơi chưa đo
### PP-1
- (e) thẻ PP2: 24 từ / 7.0 s = 3.4 từ/s > 3 (khó đọc trên điện thoại)
### TL-1
- (a) góc cao có thời gian chạy 482.0 s = 67.5 % < 75 % thân phim (714.1 s)
- (d) shot M03 góc cao trôi 3.76 % khung/s > 2 (trung vị 9 cửa sổ 1 s)
- (d) shot H2-11 góc cao trôi 2.70 % khung/s > 2 (trung vị 4 cửa sổ 1 s)
- (d) shot H5-03 góc cao trôi 3.73 % khung/s > 2 (trung vị 5 cửa sổ 1 s)
- (f) điểm máy P1: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P2: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P5: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P7: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P8: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P3: chỉ ở năm ? — phải quay lại ở năm khác
- (f) điểm máy P9: chỉ ở năm ? — phải quay lại ở năm khác
### TL-2
- (a) lướt thấp 83.4 s = 11.7 % > 10 %
- (b) shot H1-13: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H2-04a: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H2-10: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H3-02: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H3-05: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H4-04a: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
- (b) shot H5-05b: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)
### TL-3
- (c) shot M01: không ghi `bac` căn cứ
- (c) shot M02: không ghi `bac` căn cứ
- (c) shot M03: không ghi `bac` căn cứ
- (c) shot M04: không ghi `bac` căn cứ
- (c) shot H1-03: không ghi `bac` căn cứ
- (c) shot H1-04: không ghi `bac` căn cứ
- (c) shot H1-06: không ghi `bac` căn cứ
- (c) shot H1-07: không ghi `bac` căn cứ
- (c) shot H1-08b: không ghi `bac` căn cứ
- (c) shot H1-09: không ghi `bac` căn cứ
- (c) shot H1-11: không ghi `bac` căn cứ
- (c) shot H1-13: không ghi `bac` căn cứ
- (c) shot H1-15: không ghi `bac` căn cứ
- (c) shot H1-16: không ghi `bac` căn cứ
- (c) shot H1-18: không ghi `bac` căn cứ
- (c) shot H2-02: không ghi `bac` căn cứ
- (c) shot H2-03b: không ghi `bac` căn cứ
- (c) shot H2-04a: không ghi `bac` căn cứ
- (c) shot H2-05: không ghi `bac` căn cứ
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
- (c) shot H5-03: không ghi `bac` căn cứ
- (c) shot H5-04: không ghi `bac` căn cứ
- (c) shot H5-05a: không ghi `bac` căn cứ
- (c) shot H5-05b: không ghi `bac` căn cứ
- (c) shot H5-06: không ghi `bac` căn cứ
- (c) shot H5-07a: không ghi `bac` căn cứ
- (c) shot H5-07b: không ghi `bac` căn cứ
- (c) shot H5-08: không ghi `bac` căn cứ
- (b) 50 shot 3D không có trong_pct (đầu: shot M01: không có trong_pct)
### XEM-CAM
- (b) không có kết quả chủ dự án xem tắt tiếng
### MINH-HOA
- (c) H1-01a/H1-01a @0:51.0–0:57.0: không kẹp giữa hai khung 3D (trước: M04 @11.98 s goc cao; sau: H1-01b @0.02 s trong đoạn minh hoạ khác)
- (c) H1-01b/H1-01b @0:57.0–1:02.8: không kẹp giữa hai khung 3D (trước: H1-01a @5.98 s trong đoạn minh hoạ khác; sau: H1-02 @0.02 s trong đoạn minh hoạ khác)
- (c) H1-02/H1-02 @1:02.8–1:10.8: không kẹp giữa hai khung 3D (trước: H1-01b @5.85 s trong đoạn minh hoạ khác; sau: H1-03 @0.02 s goc cao)
- (c) H1-05a/H1-05a @1:38.2–1:43.7: không kẹp giữa hai khung 3D (trước: H1-04 @10.56 s goc cao; sau: H1-05b @0.02 s trong đoạn minh hoạ khác)
- (c) H1-05b/H1-05b @1:43.7–1:48.9: không kẹp giữa hai khung 3D (trước: H1-05a @5.48 s trong đoạn minh hoạ khác; sau: H1-06 @0.02 s goc cao)
- (c) H1-10/H1-10 @2:45.1–2:52.2: không kẹp giữa hai khung 3D (trước: H1-09 @8.98 s goc cao; sau: H1-12 @0.02 s trong đoạn minh hoạ khác)
- (c) H1-12/H1-12 @2:52.2–2:58.6: không kẹp giữa hai khung 3D (trước: H1-10 @7.06 s trong đoạn minh hoạ khác; sau: H1-11 @0.02 s goc cao)
- (c) H1-17a/H1-17a @3:59.7–4:05.7: không kẹp giữa hai khung 3D (trước: H1-16 @7.23 s goc cao; sau: H1-17b @0.02 s trong đoạn minh hoạ khác)
- (c) H1-17b/H1-17b @4:05.7–4:12.0: không kẹp giữa hai khung 3D (trước: H1-17a @5.98 s trong đoạn minh hoạ khác; sau: H1-18 @0.02 s goc cao)
- (c) H1-19/H1-19 @4:28.2–4:34.2: không kẹp giữa hai khung 3D (trước: H1-18 @16.27 s goc cao; sau: H2-01a @0.02 s trong đoạn minh hoạ khác)
- (c) H2-01a/H2-01a @4:34.2–4:40.8: không kẹp giữa hai khung 3D (trước: H1-19 @5.98 s trong đoạn minh hoạ khác; sau: H2-01b @0.02 s trong đoạn minh hoạ khác)
- (c) H2-01b/H2-01b @4:40.8–4:47.4: không kẹp giữa hai khung 3D (trước: H2-01a @6.48 s trong đoạn minh hoạ khác; sau: H2-02 @0.02 s goc cao)
- (e) H1-01a/H1-01a @0:51.0–0:57.0: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-01b/H1-01b @0:57.0–1:02.8: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-02/H1-02 @1:02.8–1:10.8: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-05a/H1-05a @1:38.2–1:43.7: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-05b/H1-05b @1:43.7–1:48.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-08a/H1-08a @2:17.9–2:23.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-10/H1-10 @2:45.1–2:52.2: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-12/H1-12 @2:52.2–2:58.6: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-14/H1-14 @3:24.9–3:30.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-17a/H1-17a @3:59.7–4:05.7: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-17b/H1-17b @4:05.7–4:12.0: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H1-19/H1-19 @4:28.2–4:34.2: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-01a/H2-01a @4:34.2–4:40.8: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-01b/H2-01b @4:40.8–4:47.4: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-03a/H2-03a @5:02.0–5:10.0: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-03c/H2-03c @5:22.2–5:28.2: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-04b/H2-04b @5:34.2–5:39.9: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-07/H2-07 @6:10.8–6:18.7: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H2-13/H2-13 @7:08.1–7:14.1: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H3-04b/H3-04b @7:52.8–7:59.8: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H4-01b/H4-01b @8:33.5–8:39.5: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H4-03/H4-03 @8:50.4–8:58.4: dòng sổ AI thiếu model / lệnh / SHA đầu ra
- (e) H4-04b/H4-04b @9:06.9–9:13.4: dòng sổ AI thiếu model / lệnh / SHA đầu ra
### CONG-BO-1
- (a) không khai phat_hanh.mo_ta (mô tả + bình luận ghim) — cần câu công bố có "AI" hoặc "synthetic" trong mô tả YouTube của gói phát hành
- (b) đặc tả gói không khai phat_hanh.youtube_altered_content (cần true — "AI use" = Yes ở YouTube Studio)
### N2P-1
- (a) 3 shot ai_nen nhưng chưa khai tấm kiểm (n2p.tam) — log shot M01, H5-04, H5-05a có `n2p.tam` (khuôn log) nhưng k2check đọc episode.yaml `n2p: {tam: [{id, shot, render, ghep, mat_na, nam, anh_tinh?, lop_a?}]}` (PNG render đối chứng + ảnh ghép + mặt nạ lớp — RULES-LL 1.17.0)
### N2P-2
- 3 shot ai_nen nhưng chưa khai tấm kiểm (n2p.tam) — log shot M01, H5-04, H5-05a có `n2p.tam` (khuôn log) nhưng k2check đọc episode.yaml `n2p: {tam: [{id, shot, render, ghep, mat_na, nam, anh_tinh?, lop_a?}]}` (PNG render đối chứng + ảnh ghép + mặt nạ lớp — RULES-LL 1.17.0)
### N2P-3
- 3 shot ai_nen nhưng chưa khai tấm kiểm (n2p.tam) — log shot M01, H5-04, H5-05a có `n2p.tam` (khuôn log) nhưng k2check đọc episode.yaml `n2p: {tam: [{id, shot, render, ghep, mat_na, nam, anh_tinh?, lop_a?}]}` (PNG render đối chứng + ảnh ghép + mặt nạ lớp — RULES-LL 1.17.0)
### N2P-4
- 3 shot ai_nen nhưng chưa khai tấm kiểm (n2p.tam) — log shot M01, H5-04, H5-05a có `n2p.tam` (khuôn log) nhưng k2check đọc episode.yaml `n2p: {tam: [{id, shot, render, ghep, mat_na, nam, anh_tinh?, lop_a?}]}` (PNG render đối chứng + ảnh ghép + mặt nạ lớp — RULES-LL 1.17.0)
### N2P-5
- M01: shot tấm nền chưa có video đo (n2p.video: ghep + render đối chứng + mat_na)
- H5-04: shot tấm nền chưa có video đo (n2p.video: ghep + render đối chứng + mat_na)
- H5-05a: shot tấm nền chưa có video đo (n2p.video: ghep + render đối chứng + mat_na)
### MAY-19
- (w) H2-12 KHOP: diem_neo [532420, 180800, 15] là [E, N, h] (> 100 km khỏi gốc cảnh) — khai `diem_neo_en`; đã đổi theo goc_toa_do
- (w) H3-06 KHOP: diem_neo [532118, 181150, 111] là [E, N, h] (> 100 km khỏi gốc cảnh) — khai `diem_neo_en`; đã đổi theo goc_toa_do
- (w) H4-08 KHOP: diem_neo [532420, 180800, 15] là [E, N, h] (> 100 km khỏi gốc cảnh) — khai `diem_neo_en`; đã đổi theo goc_toa_do
- (w) H5-07b KHOP: diem_neo [532118, 181150, 111] là [E, N, h] (> 100 km khỏi gốc cảnh) — khai `diem_neo_en`; đã đổi theo goc_toa_do
### TU-LIEU-10
- (b) H2-02: một lần tư liệu (TL+THE) 15.0 s > 10 s (không khai tu_lieu_lan — tính cả lớp của shot)
### TU-LIEU-OMNI
- (a) H1-01a: tư liệu (THE) 51.0–57.0 s trùng clip M-d H1-01a 51.0–57.0 s — tư liệu chỉ chồng lên shot 3D
- (a) H1-05a: tư liệu (THE) 98.2–103.7 s trùng clip M-d H1-05a 98.2–103.7 s — tư liệu chỉ chồng lên shot 3D
- (a) H2-07: tư liệu (THE) 370.8–378.7 s trùng clip M-d H2-07 370.8–378.7 s — tư liệu chỉ chồng lên shot 3D
- (b) H1-01a (51.0–57.0 s) ↔ clip M-d H1-01b (57.0–62.8 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-01a (51.0–57.0 s) ↔ clip M-d H1-02 (62.8–70.8 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-03 (70.8–87.6 s) ↔ clip M-d H1-01a (51.0–57.0 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-03 (70.8–87.6 s) ↔ clip M-d H1-01b (57.0–62.8 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-03 (70.8–87.6 s) ↔ clip M-d H1-02 (62.8–70.8 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-05a (98.2–103.7 s) ↔ clip M-d H1-05b (103.7–108.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-06 (108.9–122.4 s) ↔ clip M-d H1-05a (98.2–103.7 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-06 (108.9–122.4 s) ↔ clip M-d H1-05b (103.7–108.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-09 (156.1–165.1 s) ↔ clip M-d H1-10 (165.1–172.2 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-09 (156.1–165.1 s) ↔ clip M-d H1-12 (172.2–178.6 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-09 (156.1–165.1 s) ↔ clip M-d H1-14 (204.9–210.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-11 (178.6–193.0 s) ↔ clip M-d H1-10 (165.1–172.2 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-11 (178.6–193.0 s) ↔ clip M-d H1-12 (172.2–178.6 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-11 (178.6–193.0 s) ↔ clip M-d H1-14 (204.9–210.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-13 (193.0–204.9 s) ↔ clip M-d H1-10 (165.1–172.2 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-13 (193.0–204.9 s) ↔ clip M-d H1-12 (172.2–178.6 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-13 (193.0–204.9 s) ↔ clip M-d H1-14 (204.9–210.9 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-18 (252.0–268.2 s) ↔ clip M-d H1-17a (239.7–245.7 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-18 (252.0–268.2 s) ↔ clip M-d H1-17b (245.7–252.0 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-18 (252.0–268.2 s) ↔ clip M-d H1-19 (268.2–274.2 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-18 (252.0–268.2 s) ↔ clip M-d H2-01a (274.2–280.8 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-18 (252.0–268.2 s) ↔ clip M-d H2-01b (280.8–287.4 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H1-18 (252.0–268.2 s) ↔ clip M-d H2-03a (302.0–310.0 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H2-02 (287.4–302.0 s) ↔ clip M-d H1-17a (239.7–245.7 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H2-02 (287.4–302.0 s) ↔ clip M-d H1-17b (245.7–252.0 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H2-02 (287.4–302.0 s) ↔ clip M-d H1-19 (268.2–274.2 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H2-02 (287.4–302.0 s) ↔ clip M-d H2-01a (274.2–280.8 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H2-02 (287.4–302.0 s) ↔ clip M-d H2-01b (280.8–287.4 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H2-02 (287.4–302.0 s) ↔ clip M-d H2-03a (302.0–310.0 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H2-06 (358.8–370.8 s) ↔ clip M-d H2-07 (370.8–378.7 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H2-12 (416.1–428.1 s) ↔ clip M-d H2-13 (428.1–434.1 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H3-05 (479.8–499.5 s) ↔ clip M-d H3-04b (472.8–479.8 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H4-02 (519.5–530.4 s) ↔ clip M-d H4-01b (513.5–519.5 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
- (b) H4-02 (519.5–530.4 s) ↔ clip M-d H4-03 (530.4–538.4 s): ghép liền — không shot 3D xen giữa, 3D sạch 0.00 s < 1 s (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)
