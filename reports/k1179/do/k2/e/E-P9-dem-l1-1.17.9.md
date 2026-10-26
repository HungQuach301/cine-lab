# Luật kênh 2 (checks 1.17.9) — ban-cuoi-t4-a-E-E-P9-dem-l1 — TRƯỢT

| Mục | Kiểm | Kết quả | Cấp (1.12.1) | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) |
|---|---|---|---|---|---|---|
| Q26b | Đa dạng bối cảnh (1.16: cảnh tl/* theo vùng) | **KHÔNG ÁP** |  | 1.17.8 (tập từ T4): thay bằng Q26b-K2 — cùng ngưỡng (c)(d)(e) đo trên vùng; Q26b chỉ đọc bối cảnh qua hero / tl/* (đặc tả ghép không hero → trung tính) | ≤ 25 % · ≤ 90 s · nửa sau ≥ 3 |  |
| Q32 | Footage/ảnh nguồn ngoài | **ĐẠT** |  | không dùng footage ngoài | ≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5× |  |
| Q33 | Lặp cảnh | **ĐẠT** |  | 0 góc máy · 0 lần xuất hiện · nhiều nhất — 0 lần · 0 góc > 2 · chưa đo pHash (không có master) | ≤ 2 lần |  |
| Q34 | Loại shot | **TRƯỢT** |  | 0/1 shot có type ·  · số neo 3D 100 %, chỉ card 0 % (0 số) · địa danh 0 · nhân vật 0 | type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document ≤ 3 s · record ≤ 12 s + dòng tô + nguồn |  |
| Q35 | Nhãn loại số (D5) | **ĐẠT** |  | mô hình đặc tả · 2 khung xét · ACTUAL nhiều nhất 0/khung · lỗi a 0 · b 0 · c 0 · d 0 | ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL |  |
| Q36 | Chữ trên màn hình | **ĐẠT** |  | 0 dòng nguồn · dài nhất 0 ký tự · không có log (cỡ chữ THIẾU) · lỗi a 0 · b 0 · thiếu 0 | nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực (+ 1 lần trong câu miễn trừ 0:00–0:15) |  |
| Q37 | Nhịp thị giác (1.16: miễn khung neo/im lặng ≤ 10 s; 1.17.4: + thẻ PP cuối phim) | **TRƯỢT** |  | 3.0 s · không khai beats · khung tĩnh: không đo (không có master) · tham khảo mốc đặc tả: TB 3.0 s, dài nhất 3.0 s (s0 0.00s (mốc)) | TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s |  |
| A1–A13 | Âm thanh (tập cũ — chỉ báo) | **CHỈ BÁO** |  | CHỈ BÁO · A1 không có master · A2 không có master · A5 không có master · A7 không có master · A4 KHÔNG ÁP (không có lời — 1.16) · A8 KHÔNG ÁP (không có lời — 1.16) | docs/AUDIO-THUOC-DO.md |  |
| ML1 | Mạch truyện | **CẢNH BÁO** | Chặn (b), (c) · Cảnh báo (a) ở T3 (Chặn từ T4) — lỗi Chặn 0, Cảnh báo 1 | 0/1 shot gắn (0 suy từ mốc @từ) · timelapse 0.0 s, trôi 0.0 % | mỗi shot gắn câu/claim · timelapse trôi ≤ 15 % |  |
| ML2 | Lời lặp ý | **ĐẠT** | Chặn có giải trình (người quyết; không vào mã thoát tự động) — lỗi Chặn 0, Cảnh báo 0 | 0 câu · 0 cặp ứng viên (chấm 0) · 0 lặp ý · không khai tóm tắt | n-gram/IDF + chấm ngữ nghĩa ghim mô hình; ngoài tóm tắt cuối |  |
| ML3 | Lời mời đăng ký | **ĐẠT** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 câu mời: không có · 0 luận điểm chính khai | 60 s cuối hoặc ±5 s ranh chương · không trong 20 s trước luận điểm chính |  |
| FT1 | Chỉ báo footage/ảnh | **ĐẠT** | Cảnh báo (20 % footage đã Chặn ở Q32 b2) — lỗi Chặn 0, Cảnh báo 0 | 0 shot footage/ảnh · tính 0.0 s = 0.0 % (miễn ảnh nhỏ 0.0 s) · khai lý do: 0/0 | ≤ 20 % (trần) · mỗi shot có lý do · ảnh ≤ 1/3 khung ≤ 6 s không tính |  |
| NHIP-K2 | Nhịp kênh 2 (Q14–Q18 không áp → Q37) | **ĐẠT** | Chặn (như Q37) — lỗi Chặn 0, Cảnh báo 0 | không áp (tập LL: Q14–Q18 như cũ) | TB ≤ 3,5 s · dài nhất ≤ 6 s |  |
| Q26b-K2 | Đa dạng loại cảnh + vùng | **TRƯỢT** | Chặn (c), (d), (e) (như Q26b) · Cảnh báo (a), (b) — lỗi Chặn 1, Cảnh báo 3 | loại: khac 100.0 % · 0 vùng, lớn nhất — · nửa sau 0 vùng · không vùng 100.0 % | ≥ 3 loại/nửa · loại ≤ 70 % · vùng ≤ 25 %, ≤ 90 s, nửa sau ≥ 3 |  |
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
| Q37 (1.13) | Nhịp — khung tĩnh theo khung neo | **TRƯỢT** | Chặn (thay Q37 cho kênh 2) — lỗi Chặn 1, Cảnh báo 0 | 3.0 s · không khai beats · khung tĩnh: không đo (không có master) · tham khảo mốc đặc tả: TB 3.0 s, dài nhất 3.0 s (s0 0.00s (mốc)) | khung tĩnh (mọi khung khác khung đầu quãng < 2,0/255) ≤ 6 s |  |
| BIEN-CO-V | Biến cố thấy được ĐO trên video (K117-D8) | **CẢNH BÁO** | Chặn (b), (c), (h) ở G2 khi thước đạt hiệu chuẩn (q_bcv.HIEU_CHUAN + (h) trên tập) · Cảnh báo ở animatic hoặc khi chưa hiệu chuẩn — K117-D8 — lỗi Chặn 0, Cảnh báo 1 | — | TB khoảng biến cố đo ≤ 3,5 s · dài nhất ≤ 6 s (miễn khung neo/im lặng/thẻ PP ≤ 10 s) · bắt ≥ 95 % ranh shot |  |
| BD-1…BD-8 | Bản đồ chiến lược / inset / ranh | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | không có shot strategic, lớp ranh, tuyến hay inset |  |  |
| K-R1…K-R9 | ĐỎ-K | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập không khai rui_ro: do-k |  |  |
| K-LAI-1…6 | Khung neo LAI | **ĐẠT** | — — lỗi Chặn 0, Cảnh báo 0 | tập không có khối lai: / shot AI / đoạn AI trong log shot |  |  |
| O2 | Máy soi lỗi thời đại (lưới lọc thứ hai) | **CẢNH BÁO** | Cảnh báo (lưới lọc thứ hai — không thay kiểm nguồn) — lỗi Chặn 0, Cảnh báo 1 | — | 1 khung/5 s + khung neo · cờ/quân phục/tàu/đèn/xe/vật hiện đại/chữ/kiến trúc theo năm · không thay kiểm nguồn |  |
| SACH-1 | Khung sạch §12.1 + TL-4 | **TRƯỢT** | Chặn (a)–(f) (K116-D1; (e) chữ bản đồ Chặn theo K116-D3: ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ) — lỗi Chặn 2, Cảnh báo 0 | 1 shot · tấm số/trích 0 · tư liệu đứng riêng 0 · không log chữ | chỉ bộ đếm · chip nơi ≤ 3 s · thẻ chương · thẻ phương pháp · bản đồ ≤ 2 nhãn địa danh ≤ 3 s, không chú giải chữ (K116-D3); không tấm số/trích, không tư liệu đứng riêng (phủ ≤ 3 s) |  |
| CHUONG-1 | Thẻ chương §13.3 | **ĐẠT** | Chặn (a)–(e) · Cảnh báo (f) vị trí/mờ (K116-D1) — lỗi Chặn 0, Cảnh báo 0 | 0 thẻ chương (không bắt buộc; ≤ 8/tập) | ≤ 8/tập · "năm — ≤ 6 từ" · ≤ 3 s · không trong móc · trung tính |  |
| PP-1 | Thẻ phương pháp (D6) | **TRƯỢT** | Chặn (a)–(d) · Cảnh báo (e) tốc độ đọc ≤ 3 từ/s (K116-D1, D8: ≈ 8 s = 7–9 s) — lỗi Chặn 1, Cảnh báo 0 | 0 thẻ | 2 thẻ × 7–9 s, cuối phim · nguồn/bản đồ + chỗ ước tính (1.17.2: không đòi câu AI) · ≤ 3 từ/s |  |
| TL-1 | Xương sống timelapse §13.6 | **CẢNH BÁO** | Cảnh báo (K116-D1; mục tiêu §13.6, hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 2 | thân phim 3.0 s · góc cao + tl 0.0 s (0.0 %) · đặc tả ≤ 0.00 cắt/phút (cận trên) · ngưỡng hiệu chỉnh sau V7-PILOT | góc cao + thời gian chạy ≥ 75 % (1.17.7: `tl1_muc_tieu_pct` theo tập) · ≤ 5 cắt/phút (video: đổi cấu trúc; đối chiếu đặc tả ±0,5 s; 1.17.2: cắt góc R3 so_goc/goc_may không tính trần; 1.17.7 từ T4: ranh vào/ra M-d, tư liệu, ảnh thật không tính) · trôi ≤ 2 %/s · 6–8 điểm máy (hiệu chỉnh sau V7-PILOT) |  |
| TL-2 | Lướt thấp §13.6 | **ĐẠT** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 0 | lướt thấp 0 shot · 0.0 s = 0.0 % · ngưỡng hiệu chỉnh sau V7-PILOT | lướt thấp ≤ 10 % · có vai, phố/người (hiệu chỉnh sau V7-PILOT) |  |
| TL-3 | Không shot trống §13.6 | **ĐẠT** | Cảnh báo (K116-D1; hiệu chỉnh sau V7-PILOT) — lỗi Chặn 0, Cảnh báo 0 | 0 shot 3D · không đổi 0 · trống 0 · thiếu trong_pct 0 | mỗi shot 3D: thời gian chạy hoặc biến cố · trống ≤ 60 % (hiệu chỉnh sau V7-PILOT) |  |
| NHIP-NGHIA | Nhịp → vật mang nghĩa §13.2 | **TRƯỢT** | Chặn (K116-D1; §13.2) — lỗi Chặn 1, Cảnh báo 0 | — | ≥ 90 % nhịp chính |  |
| XEM-CAM | Cổng XEM CÂM §13.4 | **TRƯỢT** | Chặn (K116-D1, D2; §13.4 bắt buộc từ T3) — lỗi Chặn 1, Cảnh báo 0 | — | 8 câu · 3 AI + chủ dự án · tắt tiếng · chủ dự án ≥ 6/8 VÀ TB AI ≥ 6/8 (K116-D2) |  |
| PC-1 | Thước phục chế §12.3 | **ĐẠT** | Cảnh báo (K116-D1; thước tạm, hiệu chuẩn trên ≥ 10 ảnh) — lỗi Chặn 0, Cảnh báo 0 | tập không khai phuc_che: (không dùng ảnh phục chế) | Δ cạnh mới so bicubic ≤ 1,0 điểm % · PSNR ≥ bicubic |  |
| MINH-HOA | Minh hoạ AI §14.1 (c) / §15 M-d | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.1 (c) N2 / §15 M-d) — lỗi Chặn 0, Cảnh báo 0 | không đoạn minh hoạ khai trong log shot | theo đoạn khai: ≤ 20 % · kẹp giữa 2 khung 3D · máy ≤ 40 m AGL · sổ AI mỗi đoạn (1.17.2: không nhãn bắt buộc) |  |
| EO-DAT-R1 | Eo đất R1 — chủ thể | **ĐẠT** | Chỉ báo ở mọi cổng — chủ dự án chấm bằng mắt (1.17.2, V2-D2 duyệt 22/10 11:09); in pixel thô + vùng nở 1,5 % bề ngang (§14.7 R1 "≥ 15–20 %") — lỗi Chặn 0, Cảnh báo 0 | không shot khai chu_the_eo_dat | chu_the_eo_dat: chủ thể ≥ 15 % khung · 15–20 % (§14.7) — CHỈ BÁO mọi cổng, in pixel thô + vùng nở 1.5 % (1.17.2) |  |
| EO-DAT-R2 | Eo đất R2 — cỏ/cát trống | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R2: trống > 50 % ≤ 6 s liên tục, ≤ 10 % thời lượng chương) — lỗi Chặn 0, Cảnh báo 0 | không shot eo đất (noi: eo_dat) | trống (> 50 %) liên tục ≤ 6 s · mỗi chương ≤ 10 % thời lượng chương (§14.7) |  |
| EO-DAT-R3 | Eo đất R3 — góc + biến cố | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (lệnh K-1.17; §14.7 R3) — lỗi Chặn 0, Cảnh báo 0 | không shot eo đất (noi: eo_dat) | shot eo đất > 15 s: ≥ 2 góc · biến cố cách ≤ 6 s |  |
| EO-DAT-R4 | Eo đất R4 — câu lời không vật | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic (§14.7 R4 + TL-4; lệnh K-1.17.1) — lỗi Chặn 0, Cảnh báo 0 | không shot khai loi_khong_vat_eo_dat | loi_khong_vat_eo_dat: noi ∈ pho/lau_dai/cang hoặc bản đồ phủ ≤ 3 s (§14.7, TL-4) |  |
| CONG-BO-1 | Công bố AI ở gói phát hành (1.17.2) | **ĐẠT** | Chặn ở gói phát hành (`cong: phat_hanh` | `phat_hanh.goi: true`) · chỉ báo (Cảnh báo) ở mọi cổng trước — §14.1 (f), YouTube "AI use" — lỗi Chặn 0, Cảnh báo 0 | tập không có khung AI (đoạn minh hoạ / ai_image) và không khai giọng tổng hợp | khung AI hoặc giọng tổng hợp → mô tả YouTube có câu "AI"/"synthetic" · phat_hanh.youtube_altered_content: true (Chặn ở gói phát hành) |  |
| N2P-1 | N2+ (i) lớp (a) sau ghép | **TRƯỢT** | Chặn (a), (b), (d) vòng khớp màu cục bộ, (e) lớp sống ở G2 · Cảnh báo ở animatic · (c) cụm dải 20 px luôn Cảnh báo (người đọc tờ so) — §15 (c)(i); (d)(e) 1.17.5 — lỗi Chặn 9, Cảnh báo 1 | 1 tấm · max lệch (a) 0/255 · vật (a) mô hình 9 · cụm dải 20 px 54 | 0/255 trong (a) · 0 vật (a) thêm/bớt/đổi · cụm ΔE ≥ 30 trong dải 20 px → người đọc · (1.17.5) lớp sống cộng hiệu ≤ 1/255 · vòng khớp màu cục bộ · (1.17.6) tấm BMN: trừ nhà đo được nở 1 px |  |
| N2P-2 | N2+ (ii) lỗi thời đại (2 mô hình + O2) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(ii), K đề xuất — lỗi Chặn 0, Cảnh báo 0 | 1 tấm · lỗi có năm 0 · nghi vấn không năm 0 (người đọc) · q_thoi_dai mới 0 · giới hạn: cờ ~20 px không bảo đảm | 0 lỗi có năm (gpt ∪ claude) · O2 mới so render 0 |  |
| N2P-3 | N2+ (iii) đổi loại vùng T9b | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(iii); 1.17.5: nước→đất = T9c (c) bờ lấn, (d) giữa nước (đối chứng render) — lỗi Chặn 0, Cảnh báo 0 | 1 tấm · T9b lớn nhất 0.00 % · mô hình báo 0 · T9c (1.17.5): đoạn bờ lấn 0, sâu nhất 0.0 px, giữa nước ≤ 0.0 %; T9b nước→đất (chỉ in) 0.00 % | T9b đất→nước ≤ 2 % · (1.17.5) T9c: 0 bờ lấn ≥ 6 px · giữa nước ≤ 2 % · 0 báo mô hình · (1.17.6) khung không nước: T9c KHÔNG ÁP |  |
| N2P-4 | N2+ (iv) đóng băng trên tấm tĩnh | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §15 (c)(iv), K đề xuất — lỗi Chặn 0, Cảnh báo 0 | 1 tấm (1 tĩnh) · vật chuyển động 0 | 0 vật chuyển động trên tấm tĩnh |  |
| N2P-5 | N2+ (v) nhấp nháy + chuyển tấm | **TRƯỢT** | Chặn ở G2 · Cảnh báo ở animatic — §15 (b), (c)(v), K đề xuất — lỗi Chặn 1, Cảnh báo 0 | 1 shot tấm nền · chưa đo | hoà ≥ 2 s · ≤ 1 ΔE/khung · nhấp nháy ≤ 1,5 × đối chứng |  |
| N2P-6 | N2+ (vi) trần §15(d) | **TRƯỢT** | Chặn ở G2 · Cảnh báo ở animatic — §15 (d) trần, K đề xuất — lỗi Chặn 2, Cảnh báo 0 | 3.0 s · tấm nền 100.0 % (1) · minh hoạ 0.0 % (0; không trần cứng từ 1.17.4 — Q2) · tổng AI 100.0 % (1) | tấm nền ≤ 50 % · minh hoạ ≤ 20 % · tổng AI ≤ 70 % · không chồng shot |  |
| N2P-E | N2+ toàn khung hiện đại — LUẬT E (1.17.8) | **TRƯỢT** | Chặn (k) điều kiện + loại toà có tên (1.17.9 KN-5), (f) toà có tên có mặt, (g) đêm không chữ/biển/logo AI, (h) đẩy/trượt 2D (1.17.9 KN-6), (u) duyệt tấm nước AI (1.17.9 KN-8) ở G2 · Cảnh báo ở animatic · (w) toà bịa cao hơn mốc gần / chữ ban ngày / ngoại lệ mô hình đã duyệt luôn Cảnh báo — 1.17.8; 1.17.9 — lỗi Chặn 1, Cảnh báo 2 | 1 tấm E · E-P9-dem-l1: 151 toà có tên, (f1) 0 lỗi, tháp bịa máy 2 / mô hình 0, đêm (khai `dem`), toà chưa khai loai (KN-5) 151, chữ máy 0 / mô hình 1, (a)-E 13.88 %, nhà thường 29.53 % | tấm n2p_toan_khung_hien_dai: năm ≥ nam_min (≥ 2020) + CODINH · (a)-E 0/255 (sông, bờ, toà có tên, cầu, thuyền, lửa) · (f) mọi toà có tên khai có mặt; toà bịa cao hơn mốc gần → Cảnh báo · (g) đêm: 0 chữ/biển/logo AI |  |
| MAY-19 | Ngữ pháp máy §19 (a) | **TRƯỢT** | Chặn (a)–(g) ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — §19 (a) — lỗi Chặn 2, Cảnh báo 0 | 1 shot cú máy · log khung 0 · tóm tắt 0 · loại/chương thu-e:1 · THAP 0.0 % · lỗi a 0 b 0 c 0 d 1 e 0 f 0 · cảnh báo w 0 | tốc độ theo cú máy (log khung) · N2+ = CODINH · KHOP ≤ 0,5 px · ≥ 4 loại/chương · ≤ 2 liền · THAP ≤ 12 % |  |
| BAN-DO-12 | Bản đồ ≤ 12 % §19 (b) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — §19 (b) — lỗi Chặn 0, Cảnh báo 0 | 0.0 s / 3.0 s = 0.00 % | MAP + MAP3D ≤ 12 % · ≤ 10 s/lần |  |
| TU-LIEU-10 | Tư liệu + khắc + thẻ ≤ trần tập §19 (c) | **ĐẠT** | Chặn (a) trần theo tập `tu_lieu_tran_pct` (mặc định 10 %, ≤ 15 %), (b) mỗi lần ≤ 10 s, (k) khai sai trần ở G2 · Cảnh báo ở animatic — §19 (c); 1.17.6 (chủ dự án 24/10 12:52) — lỗi Chặn 0, Cảnh báo 0 | 0.0 s / 3.0 s = 0.00 % / trần 10 % (mặc định) (TL 0 · KHAC 0 · THE 0 s) · lần dài nhất 0.0 s | TL + KHAC + THE (+ THAT) ≤ tu_lieu_tran_pct (mặc định 10 %, ≤ 20 % từ 1.17.7) · mỗi lần ≤ 10 s |  |
| AI-TU-LIEU | Không AI lên tư liệu §19 (b)(c) | **TRƯỢT** | Chặn ở G2 · Cảnh báo ở animatic — §19 (b)(c) — lỗi Chặn 1, Cảnh báo 0 | 0 shot có tư liệu · 0 SHA tư liệu · 0 dòng sổ AI đối chiếu | 0 shot tư liệu có AI · 0 dòng sổ AI có SHA tư liệu |  |
| GEMINI-NGAN-SACH | Ngân sách Gemini của tập (Q2 i) | **TRƯỢT** | Chặn (a) vượt ngân sách, (u) thiếu giá thật ở G2 · Cảnh báo (k) thiếu khai, (m) vượt mốc theo dõi · Cảnh báo ở animatic — Q2 (i) — lỗi Chặn 1, Cảnh báo 0 | — | tổng usd sổ Gemini ≤ ngan_sach_gemini_usd |  |
| GOC-CAO | Góc cao timelapse + 5 chốt cấu trúc (Q2 iii; 1.17.7) | **ĐẠT** | Chặn (p) tỉ lệ ≥ goc_cao_min_pct, (a)–(d) 5 chốt cấu trúc, (k) khai sai ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — Q2 (iii) + gói tiết kiệm — lỗi Chặn 0, Cảnh báo 0 | 3.0 s / 3.0 s = 100.0 % / ngưỡng 60 % (log khung V7B-D1: 0 shot) · chốt cấu trúc TẮT (ngưỡng 60 %, không khai goc_cao_cau_truc) | goc cao + tl (V7B-D1 theo log khung, trừ THAT) ≥ goc_cao_min_pct (mặc định 60, ≥ 50) · khi < 60 / khai cấu trúc: chương mở+kết góc cao · P1 mỗi hồi (cùng khung) · ≤ 2 liền {thấp, cận, M-d, THAT} · mỗi chương ≥ goc_cao_chuong_min_pct (40) |  |
| TU-LIEU-OMNI | Tư liệu không chồng/ghép liền clip M-d (1.17.6) | **ĐẠT** | Chặn (a) tư liệu trùng clip M-d, (b) ghép liền clip M-d (< 1 shot / < 1 s 3D) ở G2 · Cảnh báo ở animatic — 1.17.6 (chủ dự án 24/10 12:52) — lỗi Chặn 0, Cảnh báo 0 | 0 lần tư liệu · 0 clip M-d — không có cặp để xét | không trùng clip M-d · cách ≥ 1 shot 3D hoặc ≥ 1 s 3D |  |
| TU-LIEU-THAT | Ảnh chụp/footage thật (1.17.7) | **ĐẠT** | Chặn (a) THAT có AI, (g) footage hiện đại thiếu giấy phép (tệp + SHA) ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — §19 (c) + gói tiết kiệm — lỗi Chặn 0, Cảnh báo 0 | không có shot/lớp ảnh chụp/footage thật (THAT) | THAT không AI · không tính góc cao · footage hiện đại có giay_phep {tep, sha256} |  |
| NHAN-VAT-TEN | Nhân vật có tên trong M-d (1.17.7, P2 b) | **ĐẠT** | Chặn (a) cận mặt > 1/8 khung, (k) chân dung tham chiếu (1.17.9 KN-7: miễn khi không có chân dung + nguồn đã tra + YuNet ≤ 1/8 + duyệt; `cat_clip` sai), (u) thiếu duyệt chủ dự án, (m) không đo được ở G2 · Cảnh báo ở animatic · (w) luôn Cảnh báo — P2 b; 1.17.9 KN-4 cửa sổ `cat_clip` — lỗi Chặn 0, Cảnh báo 0 | không đoạn M-d nào khai nhan_vat_ten | chan_dung_tham_chieu (SHA) · duyet_chu_du_an · mặt lớn nhất ≤ 1/8 chiều cao khung (YuNet ≥ 0,75) |  |
| KIEM-2-MUC | Kiểm 2 mức day_du/nen (1.17.7) | **ĐẠT** | Chặn ở G2 · Cảnh báo ở animatic — kiểm 2 mức day_du / nen (gói tiết kiệm) — lỗi Chặn 0, Cảnh báo 0 | tập không khai kiem_2_muc / muc_kiem — giữ kiểm hiện hành (K-LAI-3) | muc_kiem mỗi đoạn · nhân vật/công trình có tên, chân trời City → day_du · nen: Flash + tờ khung, ≤ 2 lượt · day_du: 2 tầng + q_thoi_dai (lớp mốc khi có mốc), ≤ 3 lượt |  |
| BE-MAT-NHA | AI phủ bề mặt nhà thường (phương án B) | **ĐẠT** | Chặn (a)–(e) ở G2 · Cảnh báo ở animatic · (w) mô hình nhìn không năm/hình khối luôn Cảnh báo — phương án B (AI phủ bề mặt nhà thường) — lỗi Chặn 0, Cảnh báo 0 | không tấm nào khai be_mat_nha_ai: true | (a) hình khối từng nhà đo được (≥ be_mat_nha_px_m_min px/m, mặc định 2) · (b) khoá 0/255 · (c) 0 lỗi thời đại · (d) quỹ đạo sáng theo điểm ảnh/nhấp nháy · (e) khung 0 chiếu 3D ở độ phân giải video · (w) cạnh màu mới |  |
| LOCK | checks/ khớp LOCK (1.17.9) | **ĐẠT** |  | KHỚP |  |  |

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
### Q34
- (0) s0/0 @0:00.0: thiếu type
### Q37
- (a) 1/1 đoạn không khai beats (s0)
### ML1
- s0/0 @0:00.0 (None, 3.0 s): không gắn câu lời hay claim
### Q26b-K2
- (a) nửa đầu: 0 loại cảnh ≥ 3 s (—) < 3
- (a) nửa sau: 0 loại cảnh ≥ 3 s (—) < 3
- (b) loại khac chiếm 100.0 % > 70 %
- (e) nửa sau (0:01.5–0:03.0) 0 vùng ≥ 3 s (—) < 3
### NC-H2
- không có shot bản đồ/địa cầu có máy quay đọc được
### NC-H3
- không có thời lượng 3D địa lý
### Q37 (1.13)
- (a) 1/1 đoạn không khai beats (s0)
### BIEN-CO-V
- (b) không có video (master/animatic)
### O2
- chưa soi: khai khối o2: {nam | nam_theo} và chạy --o2 <master> --o2-api (Claude API, có chi phí)
### SACH-1
- (f) s0/0 @0:00.0: shot không bật lọc khung sạch (p.sach)
- (c) không có log chữ — khai `log_chu: <tệp>` ở episode.yaml (khuôn khung [{f, items: [{role, s, …}]}] hoặc, 1.17.8 cho đường ghép Python, khuôn khoảng {fmt: khoang, muc: [{t0, t1, role, s, px1080?, box?}]} giây phim) hoặc --logs k2.js — không đo được chữ trên hình; (d) chip nơi chưa đo
### PP-1
- (a) không có thẻ phương pháp cuối phim (cần 2 thẻ × ≈ 8 s — D6)
### TL-1
- (a) góc cao có thời gian chạy 0.0 s = 0.0 % < 75 % thân phim (3.0 s)
- (c)(d) không có video (master/--tl16-video) — cắt/phút và trôi máy chưa đo (đặc tả: cận trên 0.00 cắt/phút)
### NHIP-NGHIA
- không khai `nhip_vat:` trong episode.yaml
### XEM-CAM
- không khai `xem_cam:` trong episode.yaml — cổng XEM CÂM bắt buộc từ T3 (§13.4); K không tự chấm
### N2P-1
- (b) tấm E-P9-dem-l1 (H5-07a): BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «Named landmark 101 Moorgate: corresponding mass remains aligned, but f» @[0.921, 0.561, 0.947, 0.612] dải (a)
- (b) tấm E-P9-dem-l1 (H5-07a): BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «Named landmark White Collar Factory: skyline height is retained, but t» @[0.743, 0.489, 0.771, 0.535] dải (a)
- (b) tấm E-P9-dem-l1 (H5-07a): BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «Named landmark 21 Moorfields: long building remains in place, but its » @[0.852, 0.553, 0.919, 0.582] dải (a)
- (b) tấm E-P9-dem-l1 (H5-07a): BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «Named landmark Ropemaker Place: facade details differ while the princi» @[0.813, 0.527, 0.829, 0.571] dải (a)
- (b) tấm E-P9-dem-l1 (H5-07a): BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «Building identified by the specific Susleny Coffee box: coarse bright » @[0.237, 0.68, 0.334, 0.754] dải (a)
- (b) tấm E-P9-dem-l1 (H5-07a): BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «Named landmark Dechert: facade and illuminated window pattern are repa» @[0.661, 0.691, 0.739, 0.753] dải (a)
- (b) tấm E-P9-dem-l1 (H5-07a): BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «Named landmark Financial Times: rounded facade is replaced by more det» @[0.607, 0.702, 0.69, 0.8] dải (a)
- (b) tấm E-P9-dem-l1 (H5-07a): BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «Named landmark Intesa Sanpaolo: corresponding right-edge block has cha» @[0.951, 0.66, 0.999, 0.72] dải (a)
- (b) tấm E-P9-dem-l1 (H5-07a): BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «Named landmark The Salvation Army International HQ: corresponding fore» @[0.418, 0.794, 0.455, 0.819] dải (a)
- (c) tấm E-P9-dem-l1 (H5-07a): 54 cụm ΔE ≥ 30 trong dải 20 px quanh (a) (người đọc tờ so): [6, 1032, 155, 1052] 2146 px, [744, 926, 790, 1055] 2003 px, [967, 1042, 1047, 1060] 1003 px, [782, 839, 807, 904] 970 px
### N2P-5
- H5-07a: shot tấm nền chưa có video đo (n2p.video: ghep + render đối chứng + mat_na)
### N2P-6
- (a) tấm nền N2+ 100.0 % > 50 % thời lượng (1 shot)
- (c) tổng khung có AI 100.0 % > 70 % (1 shot)
### N2P-E
- (g) tấm E-P9-dem-l1: gpt: chữ/biển/logo «Small white outlined emblem or sign-like mark on the narrow foreground» @[0.689, 0.92, 0.697, 0.931]
- (w) 7: máy: cụm dựng đứng trên trời render [1081, 477, 1088, 498] đỉnh cao hơn toà có tên gần nhất (Bar Remo, đỉnh y 598) 121 px — nghi toà cao KHÔNG TÊN bịa (người đọc)
- (w) 7: máy: cụm dựng đứng trên trời render [1295, 478, 1302, 502] đỉnh cao hơn toà có tên gần nhất (One New Change, đỉnh y 498) 20 px — nghi toà cao KHÔNG TÊN bịa (người đọc)
### MAY-19
- (d) chương thu-e: 1 loại cú máy (CODINH) < 4
- (g) H5-07a: không có `log_may` (log.json render_ldn.js) — không đo được §19 (a)
### AI-TU-LIEU
- (b) không khai `sha_tu_lieu` (danh sách SHA-256 tư liệu) — không đối chiếu được sổ AI
### GEMINI-NGAN-SACH
- (u) không khai `so_ai_gemini` / `so_ai`

