# Luật kênh 2 (checks 1.13.0) — v5b2b-t — TRƯỢT

| Mục | Kiểm | Kết quả | Cấp (1.12.1) | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) |
|---|---|---|---|---|---|---|
| Q26b | Đa dạng bối cảnh | **TRƯỢT** |  | 2 bối cảnh · lớn nhất tl/vinh1782 69.2 % · liên tục dài nhất tl/vinh1782 18.0 s · nửa sau 2 · trung tính 0.0 % | ≤ 25 % · ≤ 90 s · nửa sau ≥ 3 |  |
| Q32 | Footage/ảnh nguồn ngoài | **ĐẠT** |  | không dùng footage ngoài | ≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5× |  |
| Q33 | Lặp cảnh | **ĐẠT** |  | 2 góc máy · 2 lần xuất hiện · nhiều nhất tl/pho1782 · b_pho 1 lần · 0 góc > 2 · pHash xám toàn khung θ=14, thêm 0 lần lặp không khai | ≤ 2 lần |  |
| Q34 | Loại shot | **ĐẠT** |  | 4/4 shot có type · scene3d 100.0 % · số neo 3D 100 %, chỉ card 0 % (0 số) · địa danh 0 · nhân vật 0 | type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document ≤ 3 s · record ≤ 12 s + dòng tô + nguồn |  |
| Q35 | Nhãn loại số (D5) | **ĐẠT** |  | log render (2 đoạn) · 52 khung xét · ACTUAL nhiều nhất 0/khung · lỗi a 0 · b 0 · c 0 · d 0 | ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL |  |
| Q36 | Chữ trên màn hình | **ĐẠT** |  | 0 dòng nguồn · dài nhất 0 ký tự · log 2 đoạn · lỗi a 0 · b 0 · thiếu 0 | nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực (+ 1 lần trong câu miễn trừ 0:00–0:15) |  |
| Q37 | Nhịp thị giác | **TRƯỢT** |  | 26.0 s · biến cố khai 4 (gộp 4) · TB 6.5 s · dài nhất 8.0 s · khung tĩnh (khung liền < 0.6/255) dài nhất 0.25 s (từ 0:17.4) | TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s |  |
| A1–A13 | Âm thanh (tập cũ — chỉ báo) | **CHỈ BÁO** |  | CHỈ BÁO · A1 -14.1 LUFS · A2 -0.6 dBTP · A5 0 đoạn · A7 0 · A4 không có stem (--vo/--bed) và mix.json không có smr · A8 0 | docs/AUDIO-THUOC-DO.md | A1 I = -14.1 LUFS (ngưỡng -15 / -13.8) |
| ML1 | Mạch truyện | **CHỈ BÁO (TRƯỢT)** | Chặn (b), (c) · Cảnh báo (a) ở T3 (Chặn từ T4) — lỗi Chặn 1, Cảnh báo 0 | 0/4 shot gắn (0 suy từ mốc @từ) · timelapse 26.0 s, trôi 100.0 % | mỗi shot gắn câu/claim · timelapse trôi ≤ 15 % |  |
| ML2 | Lời lặp ý | **CHỈ BÁO (ĐẠT)** | Chặn có giải trình (người quyết; không vào mã thoát tự động) — lỗi Chặn 0, Cảnh báo 0 | 0 câu · 0 cặp ứng viên (chấm 0) · 0 lặp ý · không khai tóm tắt | n-gram/IDF + chấm ngữ nghĩa ghim mô hình; ngoài tóm tắt cuối |  |
| ML3 | Lời mời đăng ký | **CHỈ BÁO (ĐẠT)** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 câu mời: không có · 0 luận điểm chính khai | 60 s cuối hoặc ±5 s ranh chương · không trong 20 s trước luận điểm chính |  |
| FT1 | Chỉ báo footage/ảnh | **CHỈ BÁO (ĐẠT)** | Cảnh báo (20 % footage đã Chặn ở Q32 b2) — lỗi Chặn 0, Cảnh báo 0 | 0 shot footage/ảnh · tính 0.0 s = 0.0 % (miễn ảnh nhỏ 0.0 s) · khai lý do: 0/0 | ≤ 20 % (trần) · mỗi shot có lý do · ảnh ≤ 1/3 khung ≤ 6 s không tính |  |
| NHIP-K2 | Nhịp kênh 2 (Q14–Q18 không áp → Q37) | **CHỈ BÁO (ĐẠT)** | Chặn (như Q37) — lỗi Chặn 0, Cảnh báo 0 | không áp (tập LL: Q14–Q18 như cũ) | TB ≤ 3,5 s · dài nhất ≤ 6 s |  |
| Q26b-K2 | Đa dạng loại cảnh + vùng | **CHỈ BÁO (TRƯỢT)** | Chặn (c), (d), (e) (như Q26b) · Cảnh báo (a), (b) — lỗi Chặn 3, Cảnh báo 3 | loại: 3d 100.0 % · 2 vùng, lớn nhất tl/vinh1782 69.2 % · nửa sau 2 vùng · không vùng 0.0 % | ≥ 3 loại/nửa · loại ≤ 70 % · vùng ≤ 25 %, ≤ 90 s, nửa sau ≥ 3 |  |
| Q33-K2 | Lặp cảnh (vùng, góc) + pHash L/ΔE | **CHỈ BÁO (ĐẠT)** | Chặn (như Q33) — lỗi Chặn 0, Cảnh báo 0 | 2 khoá (vùng, góc) · 2 lần xuất hiện · nhiều nhất tl/pho1782 · b_pho 1 · 0 khoá > 2 · pHash L θ=16 + ΔE ≤ 10, thêm 0 lần lặp không khai, miễn 0 | ≤ 2 lần (miễn: khác chương + khác năm/lớp) |  |
| Q32b-K2 | Trần clip/ảnh | **CHỈ BÁO (ĐẠT)** | Chặn (như Q32b) — lỗi Chặn 0, Cảnh báo 0 | 0 clip/ảnh ·  | footage ≤ 8 s · ảnh có máy/chú thích đổi ≤ 12 s · ảnh tĩnh ≤ 8 s |  |
| TL-Q1 | Timelapse | **CHỈ BÁO (TRƯỢT)** | Chặn (a), (e) · Cảnh báo (b), (c), (d) — lỗi Chặn 1, Cảnh báo 2 | 0 mốc:  | research/timelapse/BAO-CAO.md §6.8 |  |
| TL-Q2 | Timelapse | **CHỈ BÁO (ĐẠT)** | Cảnh báo (1.12.1: AGL theo loại tuyến, HH2) — lỗi Chặn 0, Cảnh báo 0 | [0.0, 4.0]: 4.04 s ≤ 15 m/AGL ≤ 300 m (song: tuyen.loai), lệch TB 0.0 m, max 0.01 m, AGL [96, 100] (AGL của campath (bộ dựng tính từ địa hình)), đích 0.5° (K tính từ hình học tuyến); [18.0, 26.0]: 8.0 s ≤ 15 m/AGL ≤ 120 m (pho: tuyen.loai), lệch TB 0.02 m, max 0.37 m, AGL [65.9, 70] (AGL của campath (bộ dựng tính từ địa hình)), đích 5.6° (K tính từ hình học tuyến) | ≥ 3 s ≤ 15 m · AGL ≤ 120 m phố / ≤ 300 m eo đất, sông, đại lộ |  |
| TL-Q3 | Timelapse | **CHỈ BÁO (THIẾU)** | Chặn — lỗi Chặn 1, Cảnh báo 0 | — | research/timelapse/BAO-CAO.md §6.8 |  |
| TL-Q4 | Timelapse | **CHỈ BÁO (THIẾU)** | Chặn (a), (c) · Cảnh báo (b) — lỗi Chặn 0, Cảnh báo 1 |  | research/timelapse/BAO-CAO.md §6.8 |  |
| TL-Q5 | Timelapse | **CHỈ BÁO (THIẾU)** | Chặn (a), (b), (f) · Cảnh báo (c), (d), (e) — lỗi Chặn 0, Cảnh báo 1 | — | research/timelapse/BAO-CAO.md §6.8 |  |
| TL-Q6 | Timelapse | **CHỈ BÁO (THIẾU)** | Chặn — lỗi Chặn 1, Cảnh báo 0 | — | research/timelapse/BAO-CAO.md §6.8 |  |
| Q35-TL | Timelapse | **CHỈ BÁO (ĐẠT)** | Chặn (như Q35) — lỗi Chặn 0, Cảnh báo 0 | không có số "≈" thiếu ESTIMATE | "≈" bộ đếm chỉ khi dòng phương pháp "≈ = interpolated between counts" trong 6 s đầu |  |
| TL-Q7 | Timelapse | **CHỈ BÁO (ĐẠT)** | Chặn (MM2) — lỗi Chặn 0, Cảnh báo 0 | năm/s max (cửa sổ 0.5 s): bay thấp (AGL ≤ 150 m) 0.00 (từ khung None) · crane/reveal 0.00 (từ khung None) · AGL của campath (bộ dựng tính từ địa hình) | bay thấp (AGL ≤ 150 m) ≤ 10 năm/s · crane/reveal ≤ 20 năm/s |  |
| TL-Q8 | Timelapse | **CHỈ BÁO (ĐẠT)** | Cảnh báo (MM1) — lỗi Chặn 0, Cảnh báo 0 | cú 0–408: bay thấp 273 khung (11.38 s), content trung vị 35.9 %; quãng < 30 %: khung 0–127 (0.0–5.3 s, năm 1783–1783, min 3.9 %) | bay thấp của cú liên hoàn: content_pct trung vị ≥ 30 % |  |
| TL-Q9 | Tiết chế máy (cả tập) | **CHỈ BÁO (ĐẠT)** | Cảnh báo (a)–(d) · Chặn (e) tốc độ góc (JJ1/KK1) — lỗi Chặn 0, Cảnh báo 0 | 1 cú liên hoàn · 0 vertigo · tốc độ góc max 77.2 °/s (do khung 296) · do liên hoàn 0–408: orbit 5.00 s | ≤ 2 liên hoàn, ≤ 1 vertigo/tập · vai mọi pha · orbit 4–6 s · ≤ 90 °/s |  |
| NC-H1 | Thành phố có nhà | **CHỈ BÁO (ĐẠT)** | Chặn (a), (b) (đúng lỗi chủ dự án nêu ở T2) — lỗi Chặn 0, Cảnh báo 0 | 2 shot thành phố (14.4 s; khai 2, suy 0) · có lớp nhà khai 2 · không lớp nhà 0 · không đo fabric 2 | fabric trung vị ≥ 25 % · không khung < 15 % (trừ ≤ 3 s cuối reveal) |  |
| NC-H2 | Địa cầu | **CHỈ BÁO (ĐẠT)** | Chặn (a), (b) — lỗi Chặn 0, Cảnh báo 0 | 0 lần · 0.0 s (0.0 % phim) · map/globe 0.0 s · bản đồ nổi tầm cao 0.0 s · dài nhất 0 s | AGL > 50 km: ≤ 1 lần/tập · ≤ 3 s/lần |  |
| NC-H3 | Tầm mặc định | **CHỈ BÁO (ĐẠT)** | Cảnh báo — lỗi Chặn 0, Cảnh báo 0 | 3D địa lý 14.2 s · AGL ≤ 60 km 100.0 % · ≤ 3 km 100.0 % · có thành phố: có | AGL ≤ 60 km ≥ 70 % 3D · có thành phố: AGL ≤ 3 km ≥ 40 % |  |
| NC-H4 | Nơi có tên | **CHỈ BÁO (ĐẠT)** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 0 shot bản đồ · chip nơi 0 · nhãn địa danh 0 · thiếu 0 (nguồn: đặc tả, không log chữ) | mọi shot bản đồ: chip nơi hoặc nhãn địa danh |  |
| NC-H5 | Đúng thời kỳ | **CHỈ BÁO (KHÔNG ÁP)** | Chặn (a) · Cảnh báo (b) — lỗi Chặn 0, Cảnh báo 0 | không áp (tập không có bộ đếm năm/timelapse) | năm xây ≤ bộ đếm · ghost: nhãn nguồn ≥ 38 px, ≥ 3 s lần đầu |  |
| NC-H1 [do] | Thành phố có nhà (bộ timelapse) | **CHỈ BÁO (ĐẠT)** | Chặn (a), (b) (đúng lỗi chủ dự án nêu ở T2) — lỗi Chặn 0, Cảnh báo 0 | 345/624 khung thành phố (khai noi) · fabric trung vị 40.0 % · min 24.6 % · khung < 15 % (ngoài đuôi reveal) 0 | fabric trung vị ≥ 25 % · không khung < 15 % (trừ ≤ 3 s cuối reveal) |  |
| NC-H2 [do] | Địa cầu (bộ timelapse) | **CHỈ BÁO (ĐẠT)** | Chặn (a), (b) — lỗi Chặn 0, Cảnh báo 0 | 0 lần · AGL cao nhất 0.30 km | AGL > 50 km: ≤ 1 lần/tập · ≤ 3 s/lần |  |
| NC-H3 [do] | Tầm mặc định (bộ timelapse) | **CHỈ BÁO (ĐẠT)** | Cảnh báo — lỗi Chặn 0, Cảnh báo 0 | 3D 26.0 s · AGL ≤ 60 km 100.0 % · ≤ 3 km 100.0 % | AGL ≤ 60 km ≥ 70 % 3D · có thành phố: AGL ≤ 3 km ≥ 40 % |  |
| NC-H4 [do] | Nơi có tên (bộ timelapse) | **CHỈ BÁO (ĐẠT)** | Chặn — lỗi Chặn 0, Cảnh báo 0 | 55 mục chữ nơi/địa danh trong log · role: card, clock, ghost_src, method, src, where, year | mọi shot bản đồ: chip nơi hoặc nhãn địa danh |  |
| NC-H5 [do] | Đúng thời kỳ (bộ timelapse) | **CHỈ BÁO (ĐẠT)** | Chặn (a) · Cảnh báo (b) — lỗi Chặn 0, Cảnh báo 0 | nhãn ghost: "Reconstructed from J. Drinkwater, Plan o" 38.0 px · quãng ≥ 38 px: 0:00.5–0:18.0 (17.50 s), 0:18.5–0:26.0 (7.50 s) · ghost lần đầu: 0:00.0 | năm xây ≤ bộ đếm · ghost: nhãn nguồn ≥ 38 px, ≥ 3 s lần đầu |  |
| Q7/Q8-K2 | Nhãn/loại số nhận estimate (khiếu nại TT5 i) | **CHỈ BÁO (ĐẠT)** | Chặn (thay Q7/Q8 cho kênh 2, như Q35) — lỗi Chặn 0, Cảnh báo 0 | Q7 nhận ESTIMATE: 0 lỗi (log 2 đoạn) · Q8 loại số: 0 lỗi | kind ∈ actual/projection/estimate (kênh 2) · đủ nhãn, không thừa nhãn |  |
| Q33 (1.13) | Lặp cảnh — pHash bỏ lớp chữ cố định | **CHỈ BÁO (ĐẠT)** | Chặn (thay Q33 cho kênh 2) — lỗi Chặn 0, Cảnh báo 0 | 2 góc máy · 2 lần xuất hiện · nhiều nhất tl/pho1782 · b_pho 1 lần · 0 góc > 2 · pHash L vùng nội dung (bỏ lớp chữ cố định) θ=16, thêm 0 lần lặp không khai | ≤ 2 lần · pHash L vùng nội dung y 18–72 %, θ 16 |  |
| Q36 (1.13) | Chữ — câu miễn trừ nhận theo chữ | **CHỈ BÁO (ĐẠT)** | Chặn (thay Q36 cho kênh 2) — lỗi Chặn 0, Cảnh báo 0 | 0 dòng nguồn · dài nhất 0 ký tự · log 2 đoạn · lỗi a 0 · b 0 · thiếu 0 | "This video explains… Facts as of" 1 lần trong 0:00–0:15 không đòi nguồn luật |  |
| Q37 (1.13) | Nhịp — khung tĩnh theo khung neo | **CHỈ BÁO (TRƯỢT)** | Chặn (thay Q37 cho kênh 2) — lỗi Chặn 2, Cảnh báo 0 | 26.0 s · biến cố khai 4 (gộp 4) · TB 6.5 s · dài nhất 8.0 s · khung tĩnh (neo, < 2.0/255) dài nhất 0.25 s (từ 0:17.5) | khung tĩnh (mọi khung khác khung đầu quãng < 2,0/255) ≤ 6 s |  |
| LOCK | checks/ khớp LOCK (1.13.0) | **ĐẠT** |  | KHỚP |  |  |

## Âm thanh A1–A13
| Mục | Kiểm | Loại | Kết quả | Giá trị | Ngưỡng |
|---|---|---|---|---|---|
| A1 | Loudness tích hợp (master sau AAC) | chặn | ĐẠT | -14.1 LUFS | -15.0 … -13.8 |
| A2 | Đỉnh thật sau AAC | chặn | BÁO | -0.6 dBTP | ≤ -1.0 |
| A3 | Biên độ loudness LRA | báo | BÁO | 1.0 LU | 2–8 (báo) |
| A4 | Lời trên nhạc (SMR) | chặn | BÁO | không có stem (--vo/--bed) và mix.json không có smr | p10 ≥ 15 · min ≥ 12 |
| A5 | Lặng bất thường ≥ 1 s (< −50 LUFS tức thời) | chặn | ĐẠT | 0 đoạn | 0 |
| A6 | Tỉ lệ lặng | báo | ĐẠT | 0.00 % | báo |
| A7 | Chạm trần (≥ 3 mẫu |x| ≥ 0,999) | chặn | ĐẠT | 0 | 0 |
| A8 | Chồng lời | chặn | ĐẠT | 0 | 0 |
| A9 | ASR hai cách nghe | chặn | BÁO | không chạy (--no-asr) | 100 % đoạn |
| A10 | Quãng không lời > 8 s không khai khoảnh khắc nhạc | báo | ĐẠT | dài nhất 0.0 s · 0 quãng | > 8 s (báo) |
| A11 | Giao nhạc | chặn | — | không đo (mix.json không phải chuỗi mới) | ≤ 1 ô nhịp · không lặp |
| A12 | Loudnorm tuyến tính | chặn | — | không đo (mix.json không phải chuỗi mới) | linear |
| A13 | Đồng bộ tiếng | báo | — | không đo (không có stem lời --vo) | ≤ 5 ms (báo) |

## Chi tiết lỗi
### Q26b
- tl/vinh1782 chiếm 69.2 % thời lượng (> 25 %)
- tl/pho1782 chiếm 30.8 % thời lượng (> 25 %)
- nửa sau (0:13.0–0:26.0) chỉ có 2 bối cảnh (≥ 3 s): tl/pho1782, tl/vinh1782
### Q37
- (b) khoảng biến cố trung bình 6.5 s > 3.5 s
- (c) khoảng dài nhất 8.0 s > 6.0 s (từ b 18.00s (cut))
### ML1
- timelapse trôi 26.0 s = 100.0 % > 15 %
### Q26b-K2
- (a) nửa đầu: 1 loại cảnh ≥ 3 s (3d) < 3
- (a) nửa sau: 1 loại cảnh ≥ 3 s (3d) < 3
- (b) loại 3d chiếm 100.0 % > 70 %
- (c) vùng tl/vinh1782 chiếm 69.2 % > 25 %
- (c) vùng tl/pho1782 chiếm 30.8 % > 25 %
- (e) nửa sau (0:13.0–0:26.0) 2 vùng ≥ 3 s (tl/pho1782, tl/vinh1782) < 3
### TL-Q1
- (e) 0 mốc đinh < 1 (≥ 1 mỗi 3 phút, phim 26.0 s)
- (c) không có khung không chữ + mặt nạ hero (hero_anh) để đo tương phản cục bộ (1.12.1; nhan_sang sáng trong/ngoài không còn dùng)
- (d) ngân sách chữ không có số thẻ mỗi khung (cards)
### TL-Q3
- không khai reveal
### TL-Q4
- không khai ảnh lịch sử
### TL-Q5
- không có ngân sách chữ mỗi khung
### TL-Q6
- không có bảng năm toà nhà theo lớp (nam_toa)
### Q37 (1.13)
- (b) khoảng biến cố trung bình 6.5 s > 3.5 s
- (c) khoảng dài nhất 8.0 s > 6.0 s (từ b 18.00s (cut))
