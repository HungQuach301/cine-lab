# Luật kênh 2 (checks 1.16.0) — k2c-t3-g1b — TRƯỢT

| Mục | Kiểm | Kết quả | Cấp (1.12.1) | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) |
|---|---|---|---|---|---|---|
| Q26b | Đa dạng bối cảnh (1.16: cảnh tl/* theo vùng) | **ĐẠT** |  | 23 bối cảnh · lớn nhất tl/t3s · eo-dat 22.4 % · liên tục dài nhất tl/t3s · eo-dat 63.5 s · nửa sau 14 · trung tính 16.7 % | ≤ 25 % · ≤ 90 s · nửa sau ≥ 3 |  |
| Q32 | Footage/ảnh nguồn ngoài | **ĐẠT** |  | 0 đoạn footage · 0 clip · sổ 0 dòng · nguồn ngoài phim 16.7 % (footage 0.0 s + tư liệu/ảnh/báo 121.5 s) · clip dài nhất 0.00 s · footage thật 0.0 % | ≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5× |  |
| Q33 | Lặp cảnh | **TRƯỢT** |  | 70 góc máy · 70 lần xuất hiện · nhiều nhất tl/t3s · g1b_1g_0 6 lần · 14 góc > 2 · pHash xám toàn khung θ=14, thêm 54 lần lặp không khai | ≤ 2 lần | photo/print · g1b_0c: đúng 2 lần; photo/print · g1b_0f: đúng 2 lần; photo/print · g1b_2b: đúng 2 lần; photo/print · g1b_2h: đúng 2 lần; photo/print · g1b_2l: đúng 2 lần; photo/print · g1b_2p: đúng 2 lần; tl/t3s · g1b_1j_0: đúng 2 lần; tl/t3s · g1b_2g_0: đúng 2 lần; tl/t3s · g1b_3f_0: đúng 2 lần; tl/t3s · g1b_5c_0: đúng 2 lần; tl/t3s · g1b_5h_0: đúng 2 lần; tl/t3s · g1b_5j_1: đúng 2 lần; tl/t3s · g1b_5j_4: đúng 2 lần; tl/t3s · g1b_KC1910_0: đúng 2 lần; tl/t3s · g1b_KC2026_0: đúng 2 lần |
| Q34 | Loại shot | **ĐẠT** |  | 84/84 shot có type · scene3d 64.7 % · photo 16.7 % · card 15.6 % · strategic 3.0 % · số neo 3D 100 %, chỉ card 0 % (0 số) · địa danh 0 · nhân vật 0 | type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document ≤ 3 s · record ≤ 12 s + dòng tô + nguồn |  |
| Q35 | Nhãn loại số (D5) | **ĐẠT** |  | mô hình đặc tả · 218 khung xét · ACTUAL nhiều nhất 0/khung · lỗi a 0 · b 0 · c 0 · d 0 | ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL |  |
| Q36 | Chữ trên màn hình | **ĐẠT** |  | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực (+ 1 lần trong câu miễn trừ 0:00–0:15) |  |
| Q37 | Nhịp thị giác (1.16: miễn khung neo/im lặng ≤ 10 s) | **TRƯỢT** |  | 726.2 s · biến cố khai 194 (gộp 184) · TB 3.95 s · dài nhất 10.0 s · khung tĩnh (khung liền < 0.6/255) dài nhất 3.71 s (từ 0:59.0) · miễn khung neo/im lặng (1.16): 2 khoảng, dài nhất trước miễn 10.0 s | TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s |  |
| A1–A13 | Âm thanh (tập cũ — chỉ báo) | **CHỈ BÁO** |  | CHỈ BÁO · A1 -18.6 LUFS · A2 0.4 dBTP · A5 2 đoạn (5:35.9–5:39.4, 11:17.7–11:21.1) · A7 0 · A4 KHÔNG ÁP (không có lời — 1.16) · A8 KHÔNG ÁP (không có lời — 1.16) | docs/AUDIO-THUOC-DO.md |  |
| ML1 | Mạch truyện | **TRƯỢT** | Chặn (b), (c) · Cảnh báo (a) ở T3 (Chặn từ T4) — lỗi Chặn 84, Cảnh báo 25 | 0/84 shot gắn (0 suy từ mốc @từ) · timelapse 523.2 s, trôi 72.0 % | mỗi shot gắn câu/claim · timelapse trôi ≤ 15 % |  |
| ML2 | Lời lặp ý | **ĐẠT** | Chặn có giải trình (người quyết; không vào mã thoát tự động) — lỗi Chặn 0, Cảnh báo 0 | 0 câu · 0 cặp ứng viên (chấm 0) · 0 lặp ý · không khai tóm tắt | n-gram/IDF + chấm ngữ nghĩa ghim mô hình; ngoài tóm tắt cuối |  |
| ML3 | Lời mời đăng ký | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 câu mời: không có · 0 luận điểm chính khai | 60 s cuối hoặc ±5 s ranh chương · không trong 20 s trước luận điểm chính |  |
| FT1 | Chỉ báo footage/ảnh | **CẢNH BÁO** | Cảnh báo (20 % footage đã Chặn ở Q32 b2) — lỗi Chặn 0, Cảnh báo 15 | 15 shot footage/ảnh · tính 121.5 s = 16.7 % (miễn ảnh nhỏ 0.0 s) · khai lý do: 0/15 | ≤ 20 % (trần) · mỗi shot có lý do · ảnh ≤ 1/3 khung ≤ 6 s không tính |  |
| NHIP-K2 | Nhịp kênh 2 (Q14–Q18 không áp → Q37) | **TRƯỢT** | Chặn (như Q37) — lỗi Chặn 80, Cảnh báo 0 | Q37: 726.2 s · biến cố khai 194 (gộp 184) · TB 3.95 s · dài nhất 10.0 s · khung tĩnh (khung liền < 0.6/255) dài nhất 3.71 s (từ 0:59.0) · miễn khung neo/im lặng (1.16): 2 khoảng, dài nhất trước miễn 10.0 s | TB ≤ 3,5 s · dài nhất ≤ 6 s |  |
| Q26b-K2 | Đa dạng loại cảnh + vùng | **ĐẠT** | Chặn (c), (d), (e) (như Q26b) · Cảnh báo (a), (b) — lỗi Chặn 0, Cảnh báo 0 | loại: 3d 64.7 %, anh 16.7 %, the_so 15.6 %, khac 3.0 % · 37 vùng, lớn nhất eo-dat 22.4 % · nửa sau 22 vùng · không vùng 0.7 % | ≥ 3 loại/nửa · loại ≤ 70 % · vùng ≤ 25 %, ≤ 90 s, nửa sau ≥ 3 | nửa đầu đúng 3 loại cảnh (bằng ngưỡng); nửa sau đúng 3 loại cảnh (bằng ngưỡng) |
| Q33-K2 | Lặp cảnh (vùng, góc) + pHash L/ΔE | **TRƯỢT** | Chặn (như Q33) — lỗi Chặn 7, Cảnh báo 0 | 70 khoá (vùng, góc) · 70 lần xuất hiện · nhiều nhất photo/print · g1b_2k 4 · 7 khoá > 2 · pHash L θ=16 + ΔE ≤ 10, thêm 36 lần lặp không khai, miễn 12 | ≤ 2 lần (miễn: khác chương + khác năm/lớp) | photo/print · g1b_2e: đúng 2 lần; photo/print · g1b_2l: đúng 2 lần; photo/print · g1b_3c: đúng 2 lần; photo/print · g1b_3g: đúng 2 lần; photo/print · g1b_4a: đúng 2 lần; tl/t3s · g1b_5j_0: đúng 2 lần; tl/t3s · g1b_5j_1: đúng 2 lần; tl/t3s · g1b_5j_2: đúng 2 lần; tl/t3s · g1b_5j_3: đúng 2 lần |
| Q32b-K2 | Trần clip/ảnh | **ĐẠT** | Chặn (như Q32b) — lỗi Chặn 0, Cảnh báo 0 | 15 clip/ảnh · ia_historyoflatesie00drin_leaf87_drinkwater1786_plan_bay.jpg 12.0 s/12 s; met_10547.jpg 12.0 s/12 s; rijks_RP-P-OB-83.400_exact_plan_1705.jpg 10.5 s/12 s; yale_2046612_faden_1783_spanish_works.jpg 10.5 s/12 s | footage ≤ 8 s · ảnh có máy/chú thích đổi ≤ 12 s · ảnh tĩnh ≤ 8 s | ia_historyoflatesie00drin_leaf87_drinkwater1786_plan_bay.jpg s 12.0 (ngưỡng 12.0); met_10547.jpg s 12.0 (ngưỡng 12.0) |
| NC-H1 | Thành phố có nhà | **TRƯỢT** | Chặn (a), (b) (đúng lỗi chủ dự án nêu ở T2) — lỗi Chặn 1, Cảnh báo 0 | 27 shot thành phố (236.0 s; khai 27, suy 0) · có lớp nhà khai 26 · không lớp nhà 1 · không đo fabric 26 | fabric trung vị ≥ 25 % · không khung < 15 % (trừ ≤ 3 s cuối reveal) |  |
| NC-H2 | Địa cầu | **CẢNH BÁO** | Chặn (a), (b) — lỗi Chặn 0, Cảnh báo 1 | 0 lần · 0.0 s (0.0 % phim) · map/globe 0.0 s · bản đồ nổi tầm cao 0.0 s · dài nhất 0 s · loại strategic hợp lệ 4 shot (22.0 s) khỏi NC-H2/H3 | AGL > 50 km: ≤ 1 lần/tập · ≤ 3 s/lần |  |
| NC-H3 | Tầm mặc định | **CẢNH BÁO** | Cảnh báo — lỗi Chặn 0, Cảnh báo 1 | 3D địa lý 0.0 s · AGL ≤ 60 km 0.0 % · ≤ 3 km 0.0 % · có thành phố: có · loại strategic hợp lệ 4 shot (22.0 s) khỏi NC-H2/H3 | AGL ≤ 60 km ≥ 70 % 3D · có thành phố: AGL ≤ 3 km ≥ 40 % |  |
| NC-H4 | Nơi có tên | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 4 shot bản đồ · chip nơi 0 · nhãn địa danh 4 · thiếu 0 (nguồn: đặc tả, không log chữ) | mọi shot bản đồ: chip nơi hoặc nhãn địa danh |  |
| NC-H5 | Đúng thời kỳ | **TRƯỢT** | Chặn (a) · Cảnh báo (b) — lỗi Chặn 1, Cảnh báo 3 | bộ đếm có · nam_khung không · ghost 3 (ghost-1704, ghost-1782, ghost-1943) | năm xây ≤ bộ đếm (nam_khung) · ghost có nguồn + nguồn trong mô tả (§12.1: không nhãn trên hình) |  |
| Q7/Q8-K2 | Nhãn/loại số nhận estimate (khiếu nại TT5 i) | **ĐẠT** | Chặn (thay Q7/Q8 cho kênh 2, như Q35) — lỗi Chặn 0, Cảnh báo 0 | Q7 nhận ESTIMATE: 0 lỗi (không log: chỉ kiểm kind khai) · Q8 loại số: 0 lỗi | kind ∈ actual/projection/estimate (kênh 2) · đủ nhãn, không thừa nhãn |  |
| Q33 (1.13) | Lặp cảnh — pHash bỏ lớp chữ cố định | **TRƯỢT** | Chặn (thay Q33 cho kênh 2) — lỗi Chặn 11, Cảnh báo 0 | 70 góc máy · 70 lần xuất hiện · nhiều nhất tl/t3s · g1b_5a_0 5 lần · 11 góc > 2 · pHash L vùng nội dung (bỏ lớp chữ cố định) θ=16, thêm 48 lần lặp không khai | ≤ 2 lần · pHash L vùng nội dung y 18–72 %, θ 16 | photo/print · g1b_2e: đúng 2 lần; photo/print · g1b_2l: đúng 2 lần; photo/print · g1b_3c: đúng 2 lần; photo/print · g1b_3g: đúng 2 lần; photo/print · g1b_4a: đúng 2 lần; tl/t3s · g1b_0b_0: đúng 2 lần; tl/t3s · g1b_1a_0: đúng 2 lần; tl/t3s · g1b_1e_0: đúng 2 lần; tl/t3s · g1b_1g_0: đúng 2 lần; tl/t3s · g1b_1k_0: đúng 2 lần; tl/t3s · g1b_2a_0: đúng 2 lần; tl/t3s · g1b_2g_0: đúng 2 lần; tl/t3s · g1b_2o_0: đúng 2 lần; tl/t3s · g1b_2q_0: đúng 2 lần; tl/t3s · g1b_3f_0: đúng 2 lần; tl/t3s · g1b_4c_0: đúng 2 lần; tl/t3s · g1b_4d_0: đúng 2 lần; tl/t3s · g1b_4g_0: đúng 2 lần; tl/t3s · g1b_5j_0: đúng 2 lần; tl/t3s · g1b_5j_1: đúng 2 lần; tl/t3s · g1b_5j_3: đúng 2 lần; tl/t3s · g1b_KC1910_0: đúng 2 lần; tl/t3s · g1b_KC2026_0: đúng 2 lần |
| Q36 (1.13) | Chữ — câu miễn trừ nhận theo chữ | **ĐẠT** | Chặn (thay Q36 cho kênh 2) — lỗi Chặn 0, Cảnh báo 0 | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | "This video explains… Facts as of" 1 lần trong 0:00–0:15 không đòi nguồn luật |  |
| Q37 (1.13) | Nhịp — khung tĩnh theo khung neo | **TRƯỢT** | Chặn (thay Q37 cho kênh 2) — lỗi Chặn 80, Cảnh báo 0 | 726.2 s · biến cố khai 194 (gộp 184) · TB 3.95 s · dài nhất 10.0 s · khung tĩnh (neo, < 2.0/255) dài nhất 2.08 s (từ 1:41.5) · miễn khung neo/im lặng (1.16): 2 khoảng, dài nhất trước miễn 10.0 s | khung tĩnh (mọi khung khác khung đầu quãng < 2,0/255) ≤ 6 s |  |
| BD-1 | Bản đồ chiến lược: tỷ trọng + định nghĩa | **TRƯỢT** | Chặn — lỗi Chặn 3, Cảnh báo 0 | 4 shot strategic · 22.0 s = 3.0 % phim · dài nhất 7.50 s · nhiều nhất/chương 2 · hợp lệ định nghĩa 4 | ≤ 15 % · ≤ 8 s · ≤ 2/chương · không liền nhau · nghiêng ≤ 30°, 300–5 000 km · mốc thời gian, chú giải ≤ 3 phe, kề 3D nơi chỉ tới |  |
| BD-2 | Bản đồ chiến lược: chuyển động | **CẢNH BÁO** | Cảnh báo (tới khi hiệu chuẩn trên V5b-2c) — lỗi Chặn 0, Cảnh báo 4 | 4 shot strategic · đạt 0 | phần tử chuyển động bắt đầu ≤ 1,5 s, phủ ≥ 60 % |  |
| BD-3 | Ranh lịch sử: nhãn trong dữ liệu, nguồn trong mô tả (§12.1) | **ĐẠT** | Chặn (a) · Cảnh báo (c) năm nhãn ≠ năm lớp (K thêm, chờ duyệt) — lỗi Chặn 0, Cảnh báo 0 | không có lớp bien_gioi_lich_su hiện trong shot nào | manifest nam + nguon · nguồn ranh trong mô tả · KHÔNG hiện "approx. borders" trên hình |  |
| BD-4 | Manifest lớp ranh | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | không có manifest lớp ranh và không shot nào trỏ lớp | nam/nguon/nguon_doi_chieu/lech_tb_px/giay_phep ∈ CC0·PD·CC-BY-4.0; lệch > 4 px → mép mềm/gạch |  |
| BD-5 | Biên hiện đại tranh chấp + lãnh thổ nhỏ | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | không có manifest lớp ranh | ∩ (NE disputed ⊕ 10 km) = ∅ · lãnh thổ < 8 px là điểm |  |
| BD-6 | Tuyến biển không cắt đất | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | không có tuyến | tuyến biển ∩ đất NE 1:10m (trừ 5 km quanh cảng) = ∅ · ≥ 1 claim |  |
| BD-7 | Màu phe cố định (+ B8 bản địa) | **ĐẠT** | Cảnh báo (tới khi hiệu chuẩn trên V5b-2c) — lỗi Chặn 0, Cảnh báo 0 | không có phe tô màu | một faction_id một màu · không cờ/biểu tượng làm fill · bản địa không tô như đất trống |  |
| BD-8 | Inset định vị | **ĐẠT** | Cảnh báo (tới khi hiệu chuẩn trên V5b-2c) — lỗi Chặn 0, Cảnh báo 0 | không có log inset | ≤ 12 % khung · góc trên trái, an toàn 5 % · 2,5–4 s · không giao chữ/LL.occ · không trong liên hoàn/thẻ số/ảnh lưu trữ/2 s sau cắt cứng |  |
| K-R1…K-R9 | ĐỎ-K | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập không khai rui_ro: do-k |  |  |
| K-LAI-1 | LAI: thời lượng khung AI | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | — | ai_image/ai_texture ≤ 20 % thời lượng |  |
| K-LAI-2 | LAI: công bố AI (§12.1) | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | — | cờ ai_* mọi khung · shot khai khớp log · thẻ phương pháp nói AI · mô tả "AI use = Yes" · KHÔNG nhãn trên hình |  |
| K-LAI-3 | LAI: kiểm dữ kiện từng tấm C | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | — | mỗi tấm C: loi_chac_cuoi 0 · nghi vấn đã xử lý · ngoại lệ có duyệt · không chấm mù |  |
| K-LAI-4 | LAI: vùng bảo vệ = A | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | — | sai khác TB < 1/255 trên mặt nạ bao_ve (PNG) |  |
| K-LAI-5 | LAI: một tấm, ban ngày, đêm ≤ 1,5× A | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | — | ≤ 1 tấm/khung neo × mốc · ≤ 2 lần sinh lại · chỉ lượt ngày · đêm ≤ 1,5× A |  |
| K-LAI-6 | LAI: sổ gọi API | **TRƯỢT** | Chặn (P2-2) — lỗi Chặn 1, Cảnh báo 0 | — | model, prompt, % mặt nạ, usage, $, C2PA, giờ |  |
| K-LAI-B | LAI: bão hoà khung (P2-3) | **CẢNH BÁO** | Cảnh báo (P2-3) — lỗi Chặn 0, Cảnh báo 1 | — | bão hoà trung vị ≤ 0,40 mỗi khung LAI |  |
| K-LAI-3V | LAI: nghi vấn còn ghi của vân (1.16) | **CẢNH BÁO** | Cảnh báo (nghi vấn vân; chờ quyết có Chặn như tấm C) — lỗi Chặn 0, Cảnh báo 1 | — | tệp vân dùng không còn nghi vấn chưa xử lý (Cảnh báo) |  |
| O2 | Máy soi lỗi thời đại (lưới lọc thứ hai) | **CẢNH BÁO** | Cảnh báo (lưới lọc thứ hai — không thay kiểm nguồn) — lỗi Chặn 0, Cảnh báo 1 | — | 1 khung/5 s + khung neo · cờ/quân phục/tàu/đèn/xe/vật hiện đại/chữ/kiến trúc theo năm · không thay kiểm nguồn |  |
| SACH-1 | Khung sạch §12.1 + TL-4 | **TRƯỢT** | Chặn (a)–(d), (f) · Cảnh báo (e) chữ bản đồ ngoài danh sách §12.1 (chờ quyết) — lỗi Chặn 56, Cảnh báo 0 | 84 shot · tấm số/trích 40 · tư liệu đứng riêng 15 · không log chữ | chỉ bộ đếm · chip nơi ≤ 3 s · thẻ chương · thẻ phương pháp; không tấm số/trích, không tư liệu đứng riêng (phủ ≤ 3 s) |  |
| CHUONG-1 | Thẻ chương §13.3 | **ĐẠT** | Chặn (a)–(e) · Cảnh báo (f) vị trí/mờ — lỗi Chặn 0, Cảnh báo 0 | 0 thẻ chương (không bắt buộc; ≤ 8/tập) | ≤ 8/tập · "năm — ≤ 6 từ" · ≤ 3 s · không trong móc · trung tính |  |
| PP-1 | Thẻ phương pháp (D6) | **TRƯỢT** | Chặn (a)–(d) · Cảnh báo (e) tốc độ đọc — lỗi Chặn 2, Cảnh báo 1 | 1 thẻ · PP 5.0 s · 69 từ | 2 thẻ × 7–9 s, cuối phim · nguồn/ước tính/AI · ≤ 3 từ/s |  |
| TL-1 | Xương sống timelapse §13.6 | **CẢNH BÁO** | Cảnh báo (mục tiêu §13.6; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 2 | thân phim 721.2 s · góc cao + tl 0.0 s (0.0 %) · đặc tả ≤ 10.48 cắt/phút (cận trên) · video 112 cắt = 9.24/phút · (tham khảo, chưa có goc) trôi máy shot 3D: trung vị 2.73 %/s, ≤ 2 %/s ở 21/50 shot · ngưỡng hiệu chỉnh sau V7-PILOT | góc cao + thời gian chạy ≥ 75 % · ≤ 5 cắt/phút (đặc tả + video) · trôi ≤ 2 %/s · 6–8 điểm máy (hiệu chỉnh sau V7-PILOT) |  |
| TL-2 | Lướt thấp §13.6 | **CẢNH BÁO** | Cảnh báo (hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 1 | — | lướt thấp ≤ 10 % · có vai, phố/người (hiệu chỉnh sau V7-PILOT) |  |
| TL-3 | Không shot trống §13.6 | **CẢNH BÁO** | Cảnh báo (hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 1 | — | mỗi shot 3D: thời gian chạy hoặc biến cố · trống ≤ 60 % (hiệu chỉnh sau V7-PILOT) |  |
| NHIP-NGHIA | Nhịp → vật mang nghĩa §13.2 | **TRƯỢT** | Chặn (§13.2) — lỗi Chặn 1, Cảnh báo 0 | — | ≥ 90 % nhịp chính |  |
| XEM-CAM | Cổng XEM CÂM §13.4 | **TRƯỢT** | Chặn (§13.4 bắt buộc từ T3) — lỗi Chặn 1, Cảnh báo 0 | — | 8 câu · 3 AI + chủ dự án · tắt tiếng · ≥ 6/8 mỗi người |  |
| PC-1 | Thước phục chế §12.3 | **ĐẠT** | Cảnh báo (thước tạm; hiệu chuẩn trên ≥ 10 ảnh) — lỗi Chặn 0, Cảnh báo 0 | tập không khai phuc_che: (không dùng ảnh phục chế) | Δ cạnh mới so bicubic ≤ 1,0 điểm % · PSNR ≥ bicubic |  |
| LOCK | checks/ khớp LOCK (1.16.0) | **TRƯỢT** |  | KHÔNG KHỚP |  |  |

## Âm thanh A1–A13
| Mục | Kiểm | Loại | Kết quả | Giá trị | Ngưỡng |
|---|---|---|---|---|---|
| A1 | Loudness tích hợp (master sau AAC) | chặn | BÁO | -18.6 LUFS | -15.0 … -13.8 |
| A2 | Đỉnh thật sau AAC | chặn | BÁO | 0.4 dBTP | ≤ -1.0 |
| A3 | Biên độ loudness LRA | báo | BÁO | 0.8 LU | 2–8 (báo) |
| A4 | Lời trên nhạc (SMR) | chặn | — | KHÔNG ÁP (không có lời — 1.16) | p10 ≥ 15 · min ≥ 12 |
| A5 | Lặng bất thường ≥ 1 s (< −50 LUFS tức thời) | chặn | BÁO | 2 đoạn (5:35.9–5:39.4, 11:17.7–11:21.1) | 0 |
| A6 | Tỉ lệ lặng | báo | ĐẠT | 0.87 % | báo |
| A7 | Chạm trần (≥ 3 mẫu |x| ≥ 0,999) | chặn | ĐẠT | 0 | 0 |
| A8 | Chồng lời | chặn | — | KHÔNG ÁP (không có lời — 1.16) | 0 |
| A9 | ASR hai cách nghe | chặn | — | KHÔNG ÁP (không có lời — 1.16) | 100 % đoạn |
| A10 | Quãng không lời > 8 s không khai khoảnh khắc nhạc | báo | — | KHÔNG ÁP (không có lời — 1.16) | > 8 s (báo) |
| A11 | Giao nhạc | chặn | — | không đo (mix.json không phải chuỗi mới) | ≤ 1 ô nhịp · không lặp |
| A12 | Loudnorm tuyến tính | chặn | — | không đo (mix.json không phải chuỗi mới) | linear |
| A13 | Đồng bộ tiếng | báo | — | KHÔNG ÁP (không có lời — 1.16) | ≤ 5 ms (báo) |

## Chi tiết lỗi
### Q33
- photo/print · g1b_3g: 3 lần (7:20.2 + pHash: g1b_2h 4:01.2, g1b_2l 4:46.8) > 2
- relief/map · sm1: 3 lần (0:44.5 + pHash: sm3a 8:36.2, sm3b 8:40.9) > 2
- relief/map · sm3a: 3 lần (8:36.2 + pHash: sm1 0:44.5, sm3b 8:40.9) > 2
- relief/map · sm3b: 3 lần (8:40.9 + pHash: sm1 0:44.5, sm3a 8:36.2) > 2
- tl/t3s · g1b_1g_0: 6 lần (1:43.1 + pHash: g1b_1k_0 2:32.1, g1b_2a_0 2:46.6, g1b_4d_0 8:09.2, g1b_5a_0 9:25.2, g1b_5h_0 10:50.7) > 2
- tl/t3s · g1b_1k_0: 6 lần (2:32.1 + pHash: g1b_1g_0 1:43.1, g1b_2o_0 5:26.8, g1b_2q_0 5:47.2, g1b_4d_0 8:09.2, g1b_5a_0 9:25.2) > 2
- tl/t3s · g1b_2a_0: 4 lần (2:46.6 + pHash: g1b_1g_0 1:43.1, g1b_3f_0 7:04.2, g1b_4d_0 8:09.2) > 2
- tl/t3s · g1b_2c_0: 3 lần (3:09.1 + pHash: g1b_1j_0 2:22.1, g1b_5a_0 9:25.2) > 2
- tl/t3s · g1b_2o_0: 3 lần (5:26.8 + pHash: g1b_1k_0 2:32.1, g1b_4d_0 8:09.2) > 2
- tl/t3s · g1b_2q_0: 3 lần (5:47.2 + pHash: g1b_1k_0 2:32.1, g1b_5c_0 9:56.8) > 2
- tl/t3s · g1b_4d_0: 5 lần (8:09.2 + pHash: g1b_1g_0 1:43.1, g1b_1k_0 2:32.1, g1b_2a_0 2:46.6, g1b_2o_0 5:26.8) > 2
- tl/t3s · g1b_5a_0: 5 lần (9:25.2 + pHash: g1b_1g_0 1:43.1, g1b_1k_0 2:32.1, g1b_2c_0 3:09.1, g1b_2g_0 3:48.8) > 2
- tl/t3s · g1b_5j_2: 3 lần (11:22.1 + pHash: g1b_5j_1 11:18.4, g1b_5j_3 11:25.8) > 2
- tl/t3s · g1b_5j_3: 3 lần (11:25.8 + pHash: g1b_5j_2 11:22.1, g1b_5j_4 11:29.5) > 2
### Q37
- (a) 0a 3.50s cut "0a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 0d 2.55s so "Sayer 1862 · García Sanz 2022 ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) SM1: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)
- (a) SM1 4.20s dem "21 July (O.S.) / 1 A": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1d 4.50s cut "1d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1d 9.00s cut "1d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1e 5.00s cut "1e cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1f 1.60s the "up to 500 — British accounts, ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1g 4.50s cut "1g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1g 9.00s cut "1g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1h 4.00s so "Treaty of Utrecht, Article X (": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1i 4.50s cut "1i cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1i 9.00s cut "1i cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1j 5.00s cut "1j cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1k 1.40s so "«bloquear definitivamente la c": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1k 5.00s cut "1k cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1k 10.00s cut "1k cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2a 5.00s cut "2a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2a 9.00s cut "2a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2c 4.40s so "«encaminado principalmente á p": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2c 6.00s cut "2c cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2d 1.50s the "One egg: sixpence": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2d 2.61s so "Garrison diaries (Drinkwater)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) SM2: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)
- (a) 2g 4.50s cut "2g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2g 8.50s cut "2g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2i 1.60s the "258,387 — besiegers": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2i 1.80s so "Drinkwater, 1785": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2j 4.50s cut "2j cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2j 8.50s cut "2j cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2l 7.20s so "«l'expérience que l'inventeur ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 4.40s cut "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 5.90s phase "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 8.70s so "«á las diez y veinte y cinco m": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 10.60s phase "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 12.00s phase "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2n 1.50s the "357 rescued by the British": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2n 2.70s the "Garrison: 16 killed": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2n 2.80s so "British estimate & Montero · B": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2o 4.50s cut "2o cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2o 8.50s cut "2o cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2p 5.10s so "«se formó un boquete tan grand": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2q 5.50s cut "2q cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2r 4.00s so "Peace of Versailles, 3 Septemb": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3a 6.00s cut "3a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3b 5.00s cut "3b cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3b 6.73s so "«con autorización española, fu": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3c 2.80s so "«el progresivo avance de la fr": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3d 5.00s cut "3d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3f 5.50s cut "3f cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3f 10.50s cut "3f cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3h 5.00s cut "3h cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 2.60s cut "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 7.60s phase "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 8.80s phase "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 12.00s phase "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4c 4.50s cut "4c cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4d 5.50s cut "4d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4e 2.55s so "HM Government of Gibraltar, 20": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) SM3: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)
- … 20 mục nữa
### ML1
- 0c/0 @0:12.0 (photo, 3.0 s): không gắn câu lời hay claim
- 0f/0 @0:28.0 (photo, 5.0 s): không gắn câu lời hay claim
- SM1/0 @0:44.5 (strategic, 6.5 s): không gắn câu lời hay claim
- 1b/0 @0:56.0 (photo, 8.0 s): không gắn câu lời hay claim
- 1c/0 @1:04.0 (photo, 10.5 s): không gắn câu lời hay claim
- 1h/0 @1:57.1 (card, 12.0 s): không gắn câu lời hay claim
- 2b/0 @2:58.6 (photo, 10.5 s): không gắn câu lời hay claim
- 2e/0 @3:28.8 (photo, 6.5 s): không gắn câu lời hay claim
- SM2/0 @3:35.2 (strategic, 7.5 s): không gắn câu lời hay claim
- 2h/0 @4:01.2 (photo, 7.0 s): không gắn câu lời hay claim
- KA1782/0 @4:14.2 (scene3d, 8.0 s): không gắn câu lời hay claim
- 2k/0 @4:34.8 (photo, 12.0 s): không gắn câu lời hay claim
- 2l/0 @4:46.8 (photo, 12.0 s): không gắn câu lời hay claim
- 2p/0 @5:39.2 (photo, 8.0 s): không gắn câu lời hay claim
- 2r/0 @5:58.2 (card, 12.0 s): không gắn câu lời hay claim
- 3c/0 @6:32.8 (photo, 8.5 s): không gắn câu lời hay claim
- 3e/0 @6:58.2 (photo, 6.0 s): không gắn câu lời hay claim
- 3g/0 @7:20.2 (photo, 5.0 s): không gắn câu lời hay claim
- 4a/0 @7:34.8 (photo, 10.5 s): không gắn câu lời hay claim
- 4f/0 @8:27.2 (photo, 9.0 s): không gắn câu lời hay claim
- SM3/0 @8:36.2 (strategic, 4.6 s): không gắn câu lời hay claim
- SM3/1 @8:40.9 (strategic, 3.4 s): không gắn câu lời hay claim
- KB1943/0 @8:49.8 (scene3d, 8.0 s): không gắn câu lời hay claim
- 4h/0 @8:57.8 (card, 11.5 s): không gắn câu lời hay claim
- 5g/0 @10:42.7 (card, 8.0 s): không gắn câu lời hay claim
- timelapse trôi 523.2 s = 72.0 % > 15 %
- 0a/0: cau 'Midnight at the Gibraltar frontier.' không khớp đúng một câu trong lời
- 0b/0: cau 'Since July 2026, this gate has had no ro' không khớp đúng một câu trong lời
- 0c/0: cau 'The Rock sits at the western gate of the' không khớp đúng một câu trong lời
- 0d/0: cau 'Historians on both sides count fourteen ' không khớp đúng một câu trong lời
- 0e/0: cau 'This is why everyone fought over it, tol' không khớp đúng một câu trong lời
- 0e/1: cau 'This is why everyone fought over it, tol' không khớp đúng một câu trong lời
- 0e/2: cau 'This is why everyone fought over it, tol' không khớp đúng một câu trong lời
- 0e/3: cau 'This is why everyone fought over it, tol' không khớp đúng một câu trong lời
- 0f/0: cau 'In 1782, ten floating batteries came to ' không khớp đúng một câu trong lời
- 0g/0: cau 'In 1941, a runway was laid across the on' không khớp đúng một câu trong lời
- 0h/0: cau 'So why, today, is the fight over it abou' không khớp đúng một câu trong lời
- SM1/0: cau 'Austria, England and the Dutch backed a ' không khớp đúng một câu trong lời
- 1a/0: cau 'That summer, their fleet sailed into the' không khớp đúng một câu trong lời
- 1b/0: cau 'Its commanders, Admiral George Rooke and' không khớp đúng một câu trong lời
- 1c/0: cau 'This plan, printed in 1705, shows the pr' không khớp đúng một câu trong lời
- 1d/0: cau 'Inside, Governor Diego de Salinas had ba' không khớp đúng một câu trong lời
- 1e/0: cau 'On the fourth of August 1704, by the new' không khớp đúng một câu trong lời
- 1f/0: cau 'British accounts put the defenders at up' không khớp đúng một câu trong lời
- 1g/0: cau 'Townspeople could stay if they swore loy' không khớp đúng một câu trong lời
- 1h/0: cau 'In 1713, the Treaty of Utrecht gave it t' không khớp đúng một câu trong lời
- 1i/0: cau 'The treaty names the town, castle and po' không khớp đúng một câu trong lời
- 1j/0: cau 'Within weeks, Spain and France besieged ' không khớp đúng một câu trong lời
- 1k/0: cau 'So in 1730, Philip the Fifth ordered a s' không khớp đúng một câu trong lời
- 2a/0: cau 'Half a century later came a different qu' không khớp đúng một câu trong lời
- 2b/0: cau 'Spain had joined France in its war with ' không khớp đúng một câu trong lời
- 2c/0: cau 'At sea, from mid-July, a Spanish squadro' không khớp đúng một câu trong lời
- 2d/0: cau 'By January 1780, thistles, dandelions an' không khớp đúng một câu trong lời
- 2e/0: cau 'The governor, General Eliott, could hold' không khớp đúng một câu trong lời
- SM2/0: cau 'To break the blockade, Britain sent thre' không khớp đúng một câu trong lời
- 2f/0: cau 'Scurvy spread, until a Danish ship of le' không khớp đúng một câu trong lời
- 2g/0: cau 'On the twelfth of April 1781, the second' không khớp đúng một câu trong lời
- 2h/0: cau 'Two days later, soldiers broke into the ' không khớp đúng một câu trong lời
- 2i/0: cau 'By British tallies, the two sides fired ' không khớp đúng một câu trong lời
- KA1782/0: cau 'By September 1782, the garrison counted ' không khớp đúng một câu trong lời
- … 49 mục nữa
### FT1
- 0c/0 @0:12.0 (photo, 3.0 s): không khai ly_do_hinh
- 0f/0 @0:28.0 (photo, 5.0 s): không khai ly_do_hinh
- 1b/0 @0:56.0 (photo, 8.0 s): không khai ly_do_hinh
- 1c/0 @1:04.0 (photo, 10.5 s): không khai ly_do_hinh
- 2b/0 @2:58.6 (photo, 10.5 s): không khai ly_do_hinh
- 2e/0 @3:28.8 (photo, 6.5 s): không khai ly_do_hinh
- 2h/0 @4:01.2 (photo, 7.0 s): không khai ly_do_hinh
- 2k/0 @4:34.8 (photo, 12.0 s): không khai ly_do_hinh
- 2l/0 @4:46.8 (photo, 12.0 s): không khai ly_do_hinh
- 2p/0 @5:39.2 (photo, 8.0 s): không khai ly_do_hinh
- 3c/0 @6:32.8 (photo, 8.5 s): không khai ly_do_hinh
- 3e/0 @6:58.2 (photo, 6.0 s): không khai ly_do_hinh
- 3g/0 @7:20.2 (photo, 5.0 s): không khai ly_do_hinh
- 4a/0 @7:34.8 (photo, 10.5 s): không khai ly_do_hinh
- 4f/0 @8:27.2 (photo, 9.0 s): không khai ly_do_hinh
### NHIP-K2
- (a) 0a 3.50s cut "0a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 0d 2.55s so "Sayer 1862 · García Sanz 2022 ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) SM1: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)
- (a) SM1 4.20s dem "21 July (O.S.) / 1 A": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1d 4.50s cut "1d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1d 9.00s cut "1d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1e 5.00s cut "1e cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1f 1.60s the "up to 500 — British accounts, ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1g 4.50s cut "1g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1g 9.00s cut "1g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1h 4.00s so "Treaty of Utrecht, Article X (": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1i 4.50s cut "1i cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1i 9.00s cut "1i cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1j 5.00s cut "1j cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1k 1.40s so "«bloquear definitivamente la c": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1k 5.00s cut "1k cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1k 10.00s cut "1k cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2a 5.00s cut "2a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2a 9.00s cut "2a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2c 4.40s so "«encaminado principalmente á p": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2c 6.00s cut "2c cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2d 1.50s the "One egg: sixpence": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2d 2.61s so "Garrison diaries (Drinkwater)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) SM2: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)
- (a) 2g 4.50s cut "2g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2g 8.50s cut "2g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2i 1.60s the "258,387 — besiegers": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2i 1.80s so "Drinkwater, 1785": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2j 4.50s cut "2j cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2j 8.50s cut "2j cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2l 7.20s so "«l'expérience que l'inventeur ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 4.40s cut "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 5.90s phase "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 8.70s so "«á las diez y veinte y cinco m": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 10.60s phase "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 12.00s phase "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2n 1.50s the "357 rescued by the British": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2n 2.70s the "Garrison: 16 killed": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2n 2.80s so "British estimate & Montero · B": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2o 4.50s cut "2o cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2o 8.50s cut "2o cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2p 5.10s so "«se formó un boquete tan grand": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2q 5.50s cut "2q cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2r 4.00s so "Peace of Versailles, 3 Septemb": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3a 6.00s cut "3a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3b 5.00s cut "3b cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3b 6.73s so "«con autorización española, fu": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3c 2.80s so "«el progresivo avance de la fr": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3d 5.00s cut "3d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3f 5.50s cut "3f cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3f 10.50s cut "3f cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3h 5.00s cut "3h cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 2.60s cut "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 7.60s phase "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 8.80s phase "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 12.00s phase "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4c 4.50s cut "4c cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4d 5.50s cut "4d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4e 2.55s so "HM Government of Gibraltar, 20": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) SM3: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)
- … 20 mục nữa
### Q33-K2
- photo/print · g1b_1c: 3 lần (1:04.0, g1b_2h 4:01.2, g1b_2k 4:34.8) > 2
- photo/print · g1b_2h: 3 lần (g1b_1c 1:04.0, 4:01.2, g1b_3c 6:32.8) > 2
- photo/print · g1b_2k: 4 lần (g1b_1c 1:04.0, 4:34.8, g1b_4a 7:34.8, g1b_4f 8:27.2) > 2
- photo/print · g1b_4f: 3 lần (g1b_2e 3:28.8, g1b_2k 4:34.8, 8:27.2) > 2
- relief/map · sm1: 3 lần (0:44.5, sm3a 8:36.2, sm3b 8:40.9) > 2
- relief/map · sm3a: 3 lần (sm1 0:44.5, 8:36.2, sm3b 8:40.9) > 2
- relief/map · sm3b: 3 lần (sm1 0:44.5, sm3a 8:36.2, 8:40.9) > 2
### NC-H1
- (a) PP/0 g1b_5k_0 @12:01.2 (khai noi: thanh_pho): cảnh tl/t3s không có lớp nhà/đường (fabric 0 % theo đặc tả) < 25 %
### NC-H2
- không có shot bản đồ/địa cầu có máy quay đọc được
### NC-H3
- không có thời lượng 3D địa lý
### NC-H5
- (b) ghost ghost-1704: không có nguồn (ghost.ghost-1704.nguon / log shot nguon)
- (b) ghost ghost-1782: không có nguồn (ghost.ghost-1782.nguon / log shot nguon)
- (b) ghost ghost-1943: không có nguồn (ghost.ghost-1943.nguon / log shot nguon)
- (a) không khai `nam_khung:` trong episode.yaml — năm xây ≤ bộ đếm chưa đo ở cấp tập (bộ timelapse: hàng NC-H5 [bộ])
### Q33 (1.13)
- photo/print · g1b_1c: 3 lần (1:04.0 + pHash: g1b_2h 4:01.2, g1b_2k 4:34.8) > 2
- photo/print · g1b_2h: 3 lần (4:01.2 + pHash: g1b_1c 1:04.0, g1b_3c 6:32.8) > 2
- photo/print · g1b_2k: 4 lần (4:34.8 + pHash: g1b_1c 1:04.0, g1b_4a 7:34.8, g1b_4f 8:27.2) > 2
- photo/print · g1b_4f: 3 lần (8:27.2 + pHash: g1b_2e 3:28.8, g1b_2k 4:34.8) > 2
- relief/map · sm1: 3 lần (0:44.5 + pHash: sm3a 8:36.2, sm3b 8:40.9) > 2
- relief/map · sm3a: 3 lần (8:36.2 + pHash: sm1 0:44.5, sm3b 8:40.9) > 2
- relief/map · sm3b: 3 lần (8:40.9 + pHash: sm1 0:44.5, sm3a 8:36.2) > 2
- tl/t3s · g1b_3d_0: 3 lần (6:41.2 + pHash: g1b_4g_0 8:44.2, g1b_5j_2 11:22.1) > 2
- tl/t3s · g1b_5a_0: 5 lần (9:25.2 + pHash: g1b_1g_0 1:43.1, g1b_1k_0 2:32.1, g1b_2q_0 5:47.2, g1b_5d_0 10:05.2) > 2
- tl/t3s · g1b_5d_0: 3 lần (10:05.2 + pHash: g1b_0b_0 0:06.5, g1b_5a_0 9:25.2) > 2
- tl/t3s · g1b_5j_2: 3 lần (11:22.1 + pHash: g1b_3d_0 6:41.2, g1b_5j_3 11:25.8) > 2
### Q37 (1.13)
- (a) 0a 3.50s cut "0a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 0d 2.55s so "Sayer 1862 · García Sanz 2022 ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) SM1: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)
- (a) SM1 4.20s dem "21 July (O.S.) / 1 A": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1d 4.50s cut "1d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1d 9.00s cut "1d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1e 5.00s cut "1e cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1f 1.60s the "up to 500 — British accounts, ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1g 4.50s cut "1g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1g 9.00s cut "1g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1h 4.00s so "Treaty of Utrecht, Article X (": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1i 4.50s cut "1i cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1i 9.00s cut "1i cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1j 5.00s cut "1j cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1k 1.40s so "«bloquear definitivamente la c": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1k 5.00s cut "1k cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 1k 10.00s cut "1k cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2a 5.00s cut "2a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2a 9.00s cut "2a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2c 4.40s so "«encaminado principalmente á p": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2c 6.00s cut "2c cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2d 1.50s the "One egg: sixpence": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2d 2.61s so "Garrison diaries (Drinkwater)": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) SM2: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)
- (a) 2g 4.50s cut "2g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2g 8.50s cut "2g cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2i 1.60s the "258,387 — besiegers": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2i 1.80s so "Drinkwater, 1785": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2j 4.50s cut "2j cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2j 8.50s cut "2j cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2l 7.20s so "«l'expérience que l'inventeur ": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 4.40s cut "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 5.90s phase "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 8.70s so "«á las diez y veinte y cinco m": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 10.60s phase "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2m 12.00s phase "2m pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2n 1.50s the "357 rescued by the British": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2n 2.70s the "Garrison: 16 killed": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2n 2.80s so "British estimate & Montero · B": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2o 4.50s cut "2o cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2o 8.50s cut "2o cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2p 5.10s so "«se formó un boquete tan grand": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2q 5.50s cut "2q cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 2r 4.00s so "Peace of Versailles, 3 Septemb": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3a 6.00s cut "3a cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3b 5.00s cut "3b cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3b 6.73s so "«con autorización española, fu": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3c 2.80s so "«el progresivo avance de la fr": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3d 5.00s cut "3d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3f 5.50s cut "3f cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3f 10.50s cut "3f cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 3h 5.00s cut "3h cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 2.60s cut "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 7.60s phase "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 8.80s phase "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4b 12.00s phase "4b pha": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4c 4.50s cut "4c cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4d 5.50s cut "4d cú": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) 4e 2.55s so "HM Government of Gibraltar, 20": không khớp mốc nào trong đặc tả (±0.3 s)
- (a) SM3: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)
- … 20 mục nữa
### BD-1
- (d) SM3/0 @8:36.2 và SM3/1 @8:40.9: hai shot strategic liền nhau
- (f) SM2/0 @3:35.2: không shot kề cùng chương là cảnh 3D tại 2/f (kề: 2e/0 @3:28.8 photo photo/print, 2f/0 @3:42.8 scene3d tl/t3s)
- (f) SM3/0 @8:36.2: không shot kề cùng chương là cảnh 3D tại 4/g (kề: 4f/0 @8:27.2 photo photo/print, SM3/1 @8:40.9 strategic relief/map)
### BD-2
- (a) SM1/0 @0:44.5: không có phần tử chuyển động (arrow/blockade/fleet/front/route)
- (a) SM2/0 @3:35.2: không có phần tử chuyển động (arrow/blockade/fleet/front/route)
- (a) SM3/0 @8:36.2: không có phần tử chuyển động (arrow/blockade/fleet/front/route)
- (a) SM3/1 @8:40.9: không có phần tử chuyển động (arrow/blockade/fleet/front/route)
### K-LAI-1
- shot khai AI (KA1782/0, 2m/0, KB1943/0) nhưng episode.yaml không có khối lai:
### K-LAI-2
- shot khai AI (KA1782/0, 2m/0, KB1943/0) nhưng episode.yaml không có khối lai:
### K-LAI-3
- shot khai AI (KA1782/0, 2m/0, KB1943/0) nhưng episode.yaml không có khối lai:
### K-LAI-4
- shot khai AI (KA1782/0, 2m/0, KB1943/0) nhưng episode.yaml không có khối lai:
### K-LAI-5
- shot khai AI (KA1782/0, 2m/0, KB1943/0) nhưng episode.yaml không có khối lai:
### K-LAI-6
- shot khai AI (KA1782/0, 2m/0, KB1943/0) nhưng episode.yaml không có khối lai:
### K-LAI-B
- shot khai AI (KA1782/0, 2m/0, KB1943/0) nhưng episode.yaml không có khối lai:
### K-LAI-3V
- shot khai AI (KA1782/0, 2m/0, KB1943/0) nhưng episode.yaml không có khối lai:
### O2
- chưa soi: khai khối o2: {nam | nam_theo} và chạy --o2 <master> --o2-api (Claude API, có chi phí)
### SACH-1
- (a) 0d/0 @0:15.0: số/câu trích trên hình (p.so: 'Sayer 1862 · García Sanz 2022 · Gibralta') — TL-4: lời + CC mang
- (a) 0d/0 @0:15.0: tấm num đứng riêng ('14') — TL-4
- (a) 0e/0 @0:22.5: số/câu trích trên hình (p.so: '14 sieges · 1309–1783') — TL-4: lời + CC mang
- (a) 1c/0 @1:04.0: số/câu trích trên hình (p.so: '«la preciosa llave del Mediterráneo»') — TL-4: lời + CC mang
- (a) 1d/0 @1:14.5: số/câu trích trên hình (p.so: '«con cien hombres de guarnición … no hab') — TL-4: lời + CC mang
- (a) 1e/0 @1:28.0: số/câu trích trên hình (p.so: '4 August 1704 · English histories: 24 Ju') — TL-4: lời + CC mang
- (a) 1f/0 @1:37.5: tấm list đứng riêng ('Defenders, 1704') — TL-4
- (a) 1g/0 @1:43.1: số/câu trích trên hình (p.so: '«se habia acampado en las haciendas cerc') — TL-4: lời + CC mang
- (a) 1h/0 @1:57.1: số/câu trích trên hình (p.so: 'Treaty of Utrecht, Article X (1713)') — TL-4: lời + CC mang
- (a) 1h/0 @1:57.1: tấm quote đứng riêng ('') — TL-4
- (a) 1k/0 @2:32.1: số/câu trích trên hình (p.so: '«bloquear definitivamente la corresponde') — TL-4: lời + CC mang
- (a) 2b/0 @2:58.6: số/câu trích trên hình (p.so: '«Carlos III declaró la guerra á Inglater') — TL-4: lời + CC mang
- (a) 2c/0 @3:09.1: số/câu trích trên hình (p.so: '«encaminado principalmente á privar a la') — TL-4: lời + CC mang
- (a) 2d/0 @3:21.1: số/câu trích trên hình (p.so: 'Garrison diaries (Drinkwater)') — TL-4: lời + CC mang
- (a) 2d/0 @3:21.1: tấm list đứng riêng ('January 1780') — TL-4
- (a) 2i/0 @4:08.2: số/câu trích trên hình (p.so: 'Drinkwater, 1785') — TL-4: lời + CC mang
- (a) 2i/0 @4:08.2: tấm list đứng riêng ('Rounds fired (from April 1781)') — TL-4
- (a) 2k/0 @4:34.8: số/câu trích trên hình (p.so: '«alegrando la vista los 50 navios que se') — TL-4: lời + CC mang
- (a) 2l/0 @4:46.8: số/câu trích trên hình (p.so: "«l'expérience que l'inventeur avoit dema") — TL-4: lời + CC mang
- (a) 2m/0 @4:58.8: số/câu trích trên hình (p.so: '«á las diez y veinte y cinco minutos de ') — TL-4: lời + CC mang
- (a) 2n/0 @5:18.8: số/câu trích trên hình (p.so: 'British estimate & Montero · British ret') — TL-4: lời + CC mang
- (a) 2n/0 @5:18.8: tấm list đứng riêng ('13–14 September 1782') — TL-4
- (a) 2p/0 @5:39.2: số/câu trích trên hình (p.so: '«se formó un boquete tan grande … que pa') — TL-4: lời + CC mang
- (a) 2r/0 @5:58.2: số/câu trích trên hình (p.so: 'Peace of Versailles, 3 September 1783') — TL-4: lời + CC mang
- (a) 2r/0 @5:58.2: tấm quote đứng riêng ('') — TL-4
- (a) 3b/0 @6:22.2: số/câu trích trên hình (p.so: '«con autorización española, fueran destr') — TL-4: lời + CC mang
- (a) 3c/0 @6:32.8: số/câu trích trên hình (p.so: '«el progresivo avance de la frontera sob') — TL-4: lời + CC mang
- (a) 3f/0 @7:04.2: số/câu trích trên hình (p.so: '«"como acto de cortesía"»') — TL-4: lời + CC mang
- (a) 4b/0 @7:45.2: số/câu trích trên hình (p.so: '«una porción usurpada del territorio nac') — TL-4: lời + CC mang
- (a) 4e/0 @8:19.8: số/câu trích trên hình (p.so: 'HM Government of Gibraltar, 2017') — TL-4: lời + CC mang
- (a) 4e/0 @8:19.8: tấm num đứng riêng ('~55 km') — TL-4
- (a) 4h/0 @8:57.8: số/câu trích trên hình (p.so: 'Spanish government, 4 Mar 1939 (Marquina') — TL-4: lời + CC mang
- (a) 4h/0 @8:57.8: tấm quote đứng riêng ('') — TL-4
- (a) 5b/0 @9:39.2: số/câu trích trên hình (p.so: 'C19 (UK record)') — TL-4: lời + CC mang
- (a) 5b/0 @9:39.2: tấm num đứng riêng ('~4,600') — TL-4
- (a) 5e/0 @10:19.8: số/câu trích trên hình (p.so: 'HM Government of Gibraltar') — TL-4: lời + CC mang
- (a) 5e/0 @10:19.8: tấm num đứng riêng ('£85,000') — TL-4
- (a) 5g/0 @10:42.7: số/câu trích trên hình (p.so: 'UK–EU treaty on Gibraltar, July 2026 (pa') — TL-4: lời + CC mang
- (a) 5g/0 @10:42.7: tấm quote đứng riêng ('') — TL-4
- (a) 5i/0 @11:06.7: tấm list đứng riêng ('As of 18 October 2026') — TL-4
- (b) 0c/0 @0:12.0: tư liệu đứng riêng (photo, 3.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 0f/0 @0:28.0: tư liệu đứng riêng (photo, 5.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 1b/0 @0:56.0: tư liệu đứng riêng (photo, 8.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 1c/0 @1:04.0: tư liệu đứng riêng (photo, 10.5 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 2b/0 @2:58.6: tư liệu đứng riêng (photo, 10.5 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 2e/0 @3:28.8: tư liệu đứng riêng (photo, 6.5 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 2h/0 @4:01.2: tư liệu đứng riêng (photo, 7.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 2k/0 @4:34.8: tư liệu đứng riêng (photo, 12.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 2l/0 @4:46.8: tư liệu đứng riêng (photo, 12.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 2p/0 @5:39.2: tư liệu đứng riêng (photo, 8.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 3c/0 @6:32.8: tư liệu đứng riêng (photo, 8.5 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 3e/0 @6:58.2: tư liệu đứng riêng (photo, 6.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 3g/0 @7:20.2: tư liệu đứng riêng (photo, 5.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 4a/0 @7:34.8: tư liệu đứng riêng (photo, 10.5 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (b) 4f/0 @8:27.2: tư liệu đứng riêng (photo, 9.0 s) — TL-4: chỉ phủ lên địa hình ≤ 3 s
- (c) không có log chữ (--logs k2.js) — không đo được chữ thực hiện trên hình; (d) chip nơi chưa đo
### PP-1
- (a) 1 thẻ phương pháp ≠ 2 (D6: 2 thẻ × ≈ 8 s)
- (b) thẻ PP: 5.00 s ngoài 7–9 s (≈ 8 s)
- (e) thẻ PP: 69 từ / 5.0 s = 13.8 từ/s > 3 (khó đọc trên điện thoại)
### TL-1
- (c) video: 112 cắt đo / 12.02 phút = 9.24 cắt/phút > 5
- (a) không khai `log_shot:` (log shot có goc/tl/vai/trong_pct)
### TL-2
- (a) không khai `log_shot:` (log shot có goc/tl/vai/trong_pct)
### TL-3
- (a) không khai `log_shot:` (log shot có goc/tl/vai/trong_pct)
### NHIP-NGHIA
- không khai `nhip_vat:` trong episode.yaml
### XEM-CAM
- không khai `xem_cam:` trong episode.yaml — cổng XEM CÂM bắt buộc từ T3 (§13.4); K không tự chấm
