# Báo cáo kiểm L1 — walk.mp4

- Kết luận: **TRƯỢT**
- Profile: `shot` · Công cụ: cinecheck 1.3.0 · Thời điểm (UTC): 2026-09-27T12:21:49Z
- LOCK: khớp (`144b3cff71dea1eb43ffb9fb55d09e91801872fae16996ca35a27381b4fb0294`)
- Đếm: ĐẠT 9, TRƯỢT 4, — 3

| Mã | Luật | Cấp | Kết quả | Số đo chính |
|---|---|---|---|---|
| N1 | 24 fps CFR; không rơi hay lặp khung theo PTS | Chặn | **ĐẠT** | r_frame_rate = 24 fps (ngưỡng == 24); avg_frame_rate = 24 fps (ngưỡng == 24); bước PTS lệch khỏi 1/24 s > 0,5 ms = 0 bước (ngưỡng <= 0); PTS trùng (lặp khung) = 0 khung (ngưỡng <= 0); khoảng hở PTS (rơi khung) = 0 chỗ (ngưỡng <= 0) |
| N2 | BT.709 đủ 3 trường; dải limited — đo cả nhãn lẫn giá trị điểm ảnh | Chặn | **ĐẠT** | color_primaries = bt709  (ngưỡng == bt709); color_transfer = bt709  (ngưỡng == bt709); color_space = bt709  (ngưỡng == bt709); color_range = tv  (ngưỡng == tv); luma ngoài dải limited = 0.0851 % (ngưỡng <= 0.5) |
| N3 | Codec và bitrate đúng loại master; khung 16:9, SAR 1:1 | Chặn | **—** | Không áp cho profile 'shot'. |
| P0 | Máy dò chữ độc lập: mọi chữ trong hình phải có matte | Chặn | **ĐẠT** | vùng chữ dò được không có matte = 0 vùng·khung (ngưỡng <= 0); chữ gắn diegetic trùng phụ đề/tiêu đề = 0 vùng·khung (ngưỡng <= 0) |
| P1 | Không chữ đè chữ, tính theo điểm ảnh nét chữ | Chặn | **ĐẠT** | elements.json rỗng: không có chữ theo matte xuất ra. Chữ không có matte do luật P0 (máy dò độc lập) bắt. |
| G4 | Chữ tương phản ≥ 4,5:1 (WCAG AA), đo điểm ảnh | Chặn | **ĐẠT** | elements.json rỗng: không có chữ theo matte xuất ra. |
| G3 | Không banding trên gradient | Chặn | **ĐẠT** | diện tích banding lớn nhất = 0 % khung (ngưỡng <= 0.2) |
| G3b | Grain cố định: có grain, ổn định theo thời gian và giữa các shot, chuyển động theo khung | Chặn | **ĐẠT** | σ grain nhỏ nhất theo shot = 1.313 mã 8 bit (ngưỡng >= 0.8); biến thiên σ theo thời gian (CV) lớn nhất trong shot = 0.016  (ngưỡng <= 0.2); σ shot lớn nhất / nhỏ nhất = 1  (ngưỡng <= 1.3); tương quan grain giữa 2 khung kề (trung vị, shot tệ nhất) = 0.187  (ngưỡng <= 0.5) |
| M1 | Master YouTube: −14 LUFS ±1; true peak ≤ −1 dBTP | Chặn | **—** | Không áp cho profile 'shot'. |
| M3 | Tương quan pha và tương thích mono | Chặn | **—** | File không có luồng âm. |
| J1 | Mọi từ trong kịch bản nghe rõ trên bản mix cuối | Chặn | **TRƯỢT** | Không có luồng âm. |
| J1b | Lời rõ trên nhạc theo từng câu, đo từ stem thoại và stem nền | Chặn | **TRƯỢT** | File không có luồng âm. |
| H1 | Không chuyển động tuyến tính ở bộ phận nhân vật | Chặn | **ĐẠT** | đoạn tuyến tính ở bộ phận nhân vật = 0 đoạn (ngưỡng <= 0); kênh 'mechanical' thiếu lý do = 0 kênh (ngưỡng <= 0); kênh có lớp không hợp lệ = 0 kênh (ngưỡng <= 0) |
| H1b | Chuyển động khai báo khớp hình render (luồng quang học ở vùng nhân vật) | Chặn | **TRƯỢT** | nhân vật có kênh bộ phận nhưng không có screen track = 0 nhân vật (ngưỡng <= 0); tỷ lệ cặp khung khớp luồng quang học, track tệ nhất = 48.9 % (ngưỡng >= 90) ✗; track không đo được cặp khung nào (toàn null/ngoài khung) = 0 track (ngưỡng <= 0) |
| C3 | Đúng model: tỷ lệ bộ phận so với model sheet, có tính nhiễu đo | Chặn | **TRƯỢT** | hệ số phân giải mặt nạ/khung đo từ kích thước PNG (nhỏ nhất) = 4 × (ngưỡng >= 2); hệ số phân giải mặt nạ/khung đo từ kích thước PNG (lớn nhất) = 4 × (ngưỡng <= 4) ⚠ sát ngưỡng; mặt nạ cùng kích thước, hệ số ngang = dọc = True  (ngưỡng == True); 'scale' khai báo khớp hệ số đo (bỏ trống được) = True  (ngưỡng == True); vị trí biên phân biệt để kiểm pha lưới = 4933  (ngưỡng >= 40); vị trí biên dồn vào 1 pha lưới (phóng to từ mặt nạ thấp hơn) = 0.254  (ngưỡng <= 0.625); dải xám ở biên mặt nạ (phóng to còn giữ mức xám), lớn nhất = 0 px/px biên (ngưỡng <= 2.5); đầu < 100 px video thì mặt nạ ≥ 4× (Q-δ): hệ số đo khi đầu nhỏ = 4 × (ngưỡng >= 3.98) ⚠ sát ngưỡng; biên trên |lệch| + U lớn nhất = 30.77 % (ngưỡng <= 3) ✗; bộ phận–khung lệch chắc chắn > 3% = 12  (ngưỡng <= 0) ✗; bộ phận–khung không chứng minh được ≤ 3% (nhiễu đo) = 0  (ngưỡng <= 0); khung mẫu (mỗi 12 khung) thiếu mặt nạ = 0  (ngưỡng <= 0); độ khớp biên mặt nạ–cạnh ảnh render thấp nhất = 1.762  (ngưỡng >= 1.5); kiểm toán: video không đổi sau khi phát yêu cầu = True  (ngưỡng == True); kiểm toán: bộ mặt nạ nộp không đổi sau khi phát yêu cầu = True  (ngưỡng == True); kiểm toán: có khung được chọn = 2  (ngưỡng >= 1); kiểm toán: có render.log = True  (ngưỡng == True); kiểm toán: log có dòng SCENE, SHA-256 khớp file cảnh trên đĩa = True  (ngưỡng == True); kiểm toán: khung được chọn không có dòng FRAME … CMD trong log = 0  (ngưỡng <= 0); kiểm toán: mặt nạ render lại thiếu hoặc khác kích thước = 0  (ngưỡng <= 0); kiểm toán: lệch tỷ lệ nộp/render lại, tính theo dải nhiễu U (lớn nhất) = 0 ×U (ngưỡng <= 1); kiểm toán: điểm ảnh khác nhau / điểm ảnh biên (lớn nhất) = 0  (ngưỡng <= 0.02) |
| O3 | Mọi tài sản lấy từ thư viện có SHA | Chặn | **ĐẠT** | tài sản không có trong thư viện = 0  (ngưỡng <= 0); tài sản lệch SHA so với thư viện = 0  (ngưỡng <= 0); tài sản thư viện thiếu file trên đĩa = 0  (ngưỡng <= 0); file media lạ trong thư mục làm việc = 0  (ngưỡng <= 0) |

## Chỉ số nằm trong ±5% quanh ngưỡng
- C3 — hệ số phân giải mặt nạ/khung đo từ kích thước PNG (lớn nhất): 4 (ngưỡng 4)
- C3 — đầu < 100 px video thì mặt nạ ≥ 4× (Q-δ): hệ số đo khi đầu nhỏ: 4 (ngưỡng 3.98)

## Chi tiết từng luật

### N1 — 24 fps CFR; không rơi hay lặp khung theo PTS (4.N — Kỹ thuật file, cấp Chặn): ĐẠT
- Định nghĩa đo: ffprobe đọc PTS từng gói hình của luồng video đầu tiên, sắp xếp theo PTS, tính hiệu PTS kề nhau. Đồng thời đọc r_frame_rate và avg_frame_rate.
- Ngưỡng: r_frame_rate = avg_frame_rate = 24/1; 0 bước PTS lệch khỏi 1/24 s quá 0,5 ms; 0 PTS trùng; 0 khoảng hở.
- Bằng chứng: `{"so_khung": 48}`

### N2 — BT.709 đủ 3 trường; dải limited — đo cả nhãn lẫn giá trị điểm ảnh (4.N — Kỹ thuật file, cấp Chặn): ĐẠT
- Định nghĩa đo: Nhãn: color_primaries, color_transfer, color_space phải là bt709; color_range là tv. Điểm ảnh: lấy mẫu luma (2 khung/giây, tối đa 240 khung), tính tỷ lệ mẫu nằm ngoài dải limited (8 bit: <16 hoặc >235; 10 bit: <64 hoặc >940).
- Ngưỡng: Đủ 4 nhãn đúng; tỷ lệ luma ngoài dải ≤ 0,5% (nội bộ).
- Bằng chứng: `{"khung_lay_mau": 4, "bit_depth": 8}`

### N3 — Codec và bitrate đúng loại master; khung 16:9, SAR 1:1 (4.N — Kỹ thuật file, cấp Chặn): —
- Định nghĩa đo: ffprobe đọc codec, profile, pix_fmt, kích thước, SAR; bitrate hình tính từ tổng kích thước gói / thời lượng (không dùng số khai trong header). Bitrate âm đo từ gói chỉ báo tham khảo: AAC dùng ít bit cho đoạn âm đơn giản nên không phản ánh chất lượng. Profile youtube: dùng chung số đo grain của G3b (σ theo shot) để chọn ngưỡng bitrate.
- Ngưỡng: youtube: H.264 High hoặc HEVC Main/Main10, yuv420p/yuv420p10le, 1920×1080 hoặc 3840×2160, bitrate hình đo ≥ 12 Mbps (1080p) / ≥ 45 Mbps (2160p) (nội bộ, trên mức khuyến nghị YouTube 8/35–45 Mbps); v1.1 (Q-G3b): khi G3b đo thấy grain (σ trung vị của một shot bất kỳ ≥ 0,8 mã) thì bitrate hình đo ≥ 30 Mbps (1080p; 2160p vẫn ≥ 45); âm AAC-LC 48 kHz 2 kênh (bitrate âm chỉ báo tham khảo). archive: ProRes 422 HQ/4444/4444 XQ, DNxHR HQ/HQX/444 hoặc FFV1; âm PCM ≥ 24 bit 48 kHz; ≥ 1920×1080. Cả hai: tỷ lệ 16:9, SAR 1:1.
- Ghi chú: Không áp cho profile 'shot'.

### P0 — Máy dò chữ độc lập: mọi chữ trong hình phải có matte (4.P — Chữ, tiêu đề, phụ đề, cấp Chặn): ĐẠT
- Định nghĩa đo: Lấy mẫu 2 khung/giây (tối đa 240 khung) từ file render. Máy dò PP-OCRv4 det (DB, ONNX ghim SHA trong checks/models/) tìm vùng nghi là chữ (điểm hộp ≥ 0,6); mô hình nhận dạng PP-OCRv4 rec đọc từng vùng, chỉ giữ vùng đọc ra ≥ 2 ký tự Latin/số, chiếm ≥ 60% ký tự, độ tin ≥ 0,8, và độ đặc nét < 0,85 (trung vị diện tích/hộp bao của các thành phần sau ngưỡng Otsu; ký tự đo được 0,4–0,7, ô cửa sổ ≈ 1,0) — loại cửa sổ, lưới, hoa văn. Vùng có matte = ≥ 50% diện tích hộp nằm trong nét matte (alpha ≥ 0,02) của các phần tử đang hiện ở khung đó, nới 0,35 × chiều cao hộp. Không cần matte để chạy: thiếu thư mục chữ thì mọi chữ dò được đều trượt. Ngoài khung lấy mẫu, mỗi phần tử chữ được đọc thêm ở khung giữa khoảng hiện. v1.1 (Q-P0): phần tử 'diegetic': true (chữ trong thế giới phim) được tính là có matte; vùng chữ gán cho phần tử diegetic (phủ nhiều nhất) được chuẩn hoá thành từ như J1 và so với: dòng thoại của <video>.script.txt (phụ đề), chữ đọc được trong matte phần tử không diegetic (tiêu đề, phụ đề, credit), trường 'text' khai cho phần tử không diegetic. Trùng = giống cả dòng ≥ 0,80 (difflib, dòng ≥ 2 từ hoặc ≥ 6 ký tự) hoặc giống một đoạn liền ≥ 0,85 với ≥ 2 từ và ≥ 50% số từ của dòng.
- Ngưỡng: 0 vùng chữ dò được mà không có matte; 0 vùng chữ diegetic trùng phụ đề/tiêu đề (ngưỡng hộp 0,6, độ tin 0,8, độ đặc 0,85, độ phủ 50%, giống 0,80/0,85: nội bộ).
- Ghi chú: Lấy mẫu 5 khung (≈ 2 khung/giây). Vùng máy dò nghi là chữ nhưng nhận dạng không xác nhận chữ Latin (cửa sổ, lưới, hoa văn): 29 (bỏ qua).
- Ghi chú: Không có matte chữ (thiếu <video>.text/ hoặc elements rỗng): mọi chữ dò được đều trượt.
- Bằng chứng: `{"vung_co_matte": 0, "vung_bi_loai": 29, "khung_lay_mau": 5}`

### P1 — Không chữ đè chữ, tính theo điểm ảnh nét chữ (4.P — Chữ, tiêu đề, phụ đề, cấp Chặn): ĐẠT
- Định nghĩa đo: Mỗi phần tử chữ có matte RGBA xuất từ render (checks/RUN.md mục 3). Nét chữ = alpha ≥ 0,5, nới 1 px. Ở mọi khung có ≥ 2 phần tử, đếm điểm ảnh thuộc ≥ 2 nét. Chống khai man: ở lõi nét (alpha ≥ 0,98, co 1 px) màu matte phải khớp màu khung render (lệch kênh ≤ 24/255) ở ≥ 90% điểm ảnh.
- Ngưỡng: 0 điểm ảnh va chạm; độ khớp matte ≥ 90%.
- Ghi chú: elements.json rỗng: không có chữ theo matte xuất ra. Chữ không có matte do luật P0 (máy dò độc lập) bắt.

### G4 — Chữ tương phản ≥ 4,5:1 (WCAG AA), đo điểm ảnh (4.G — Ánh sáng và màu, cấp Chặn): ĐẠT
- Định nghĩa đo: Với mỗi phần tử chữ, lấy tối đa 24 khung rải đều. Độ chói tương đối (WCAG, sRGB) của chữ = trung vị trên lõi nét trong khung render. Nền = vành 2–6 px quanh nét (trừ nét của mọi phần tử). Tính tỷ lệ tương phản từng điểm nền với chữ; lấy phân vị 10 (90% điểm nền đạt). Lấy giá trị nhỏ nhất qua các khung. v1.1 (Q-P0): phần tử 'diegetic': true được miễn đo tương phản nhưng vẫn kiểm độ khớp matte–render như P1.
- Ngưỡng: Phân vị 10 của tỷ lệ tương phản ≥ 4,5 ở mọi phần tử không diegetic, mọi khung lấy mẫu; độ khớp matte–render ≥ 90% ở mọi phần tử.
- Ghi chú: elements.json rỗng: không có chữ theo matte xuất ra.

### G3 — Không banding trên gradient (4.G — Ánh sáng và màu, cấp Chặn): ĐẠT
- Định nghĩa đo: Luma ở độ sâu gốc, 2 khung/giây (tối đa 240 khung). Điểm banding = điểm nằm trong mảng phẳng tuyệt đối 5×5, và trong cửa sổ 95×95 quanh nó: (a) có ≥ 3 mức mảng phẳng khác nhau (bậc thang), (b) mọi bước nhảy giữa điểm kề ≤ 2 mã (không có cạnh cứng), (c) biên độ luma ≤ 24 mã. Diện tích banding = tỷ lệ điểm banding trên khung.
- Ngưỡng: Diện tích banding ≤ 0,2% khung ở mọi khung lấy mẫu (nội bộ).
- Bằng chứng: `{"khung_lay_mau": 4, "bit_depth": 8, "trung_binh_pct": 0.0}`

### G3b — Grain cố định: có grain, ổn định theo thời gian và giữa các shot, chuyển động theo khung (4.G — Ánh sáng và màu, cấp Chặn): ĐẠT
- Định nghĩa đo: Cặp khung kề (n, n+1) mỗi 12 khung (tối đa 240 cặp), luma quy về thang 8 bit. Phần dư = luma − làm mờ Gauss σ=1,5. Khối 32×32 phẳng khi độ lệch chuẩn của ảnh làm mờ σ=2 ≤ 1,5 mã và luma trung bình trong [40, 210]; khung cần ≥ 20 khối phẳng. σ grain của khung = trung vị qua khối của 1,4826·MAD phần dư, đo ở cả khung n và n+1 (bắt grain dao động theo loại khung mã hoá I/P/B). Shot tách bằng PySceneDetect ContentDetector mặc định. Grain đứng yên đo bằng tương quan phần dư khung n với n+1 trên khối phẳng.
- Ngưỡng: Trung vị σ mỗi shot ≥ 0,8 mã 8 bit; CV của σ theo thời gian trong mỗi shot ≤ 0,20; σ shot lớn nhất / nhỏ nhất ≤ 1,30; tương quan khung kề ≤ 0,50 (đều nội bộ).
- Ghi chú: 1 shot (PySceneDetect); 8 khung đo, 0 khung không đủ khối phẳng.
- Bằng chứng: `{"theo_shot": {"0": {"tu_khung": 0, "so_khung_do": 8, "sigma_trung_vi": 1.313, "cv": 0.016, "tuong_quan_khung_ke": 0.187}}, "shot_bat_dau": [0]}`

### M1 — Master YouTube: −14 LUFS ±1; true peak ≤ −1 dBTP (4.M — Mix và master, cấp Chặn): —
- Định nghĩa đo: ffmpeg ebur128 (ITU-R BS.1770-4, cổng tuyệt đối −70 và tương đối −10 LU), peak=true (lấy mẫu vượt) trên luồng âm đầu tiên của file.
- Ngưỡng: Integrated trong [−15, −13] LUFS; true peak ≤ −1,0 dBTP.
- Ghi chú: Không áp cho profile 'shot'.

### M3 — Tương quan pha và tương thích mono (4.M — Mix và master, cấp Chặn): —
- Định nghĩa đo: Giải mã stereo 48 kHz float. Cửa sổ 400 ms không chồng; cửa sổ hoạt động khi RMS kênh lớn hơn ≥ −50 dBFS. (1) Hệ số tương quan L/R từng cửa sổ. (2) Mất mát khi gộp mono = độ ồn BS.1770 của (L+R)/2 phát cả 2 kênh trừ độ ồn stereo. (3) Mất công suất mono/stereo trên cửa sổ trượt 3 s. Phần 'lời rõ trên nhạc' của M3 được đo bởi J1 (ASR trên bản gộp mono của mix cuối).
- Ngưỡng: ≤ 1% cửa sổ hoạt động có tương quan < −0,3; mất mát mono tích phân ≥ −3,0 dB; cửa sổ 3 s tệ nhất ≥ −6,0 dB (nội bộ).
- Ghi chú: File không có luồng âm.

### J1 — Mọi từ trong kịch bản nghe rõ trên bản mix cuối (4.J — Giọng, cấp Chặn): TRƯỢT
- Định nghĩa đo: faster-whisper small.en (revision ghim, int8, beam 5, nhiệt độ 0, không mồi bằng kịch bản, không nối ngữ cảnh, có mốc từng chữ) chạy trên luồng âm của file, gộp mono 16 kHz. Chuẩn hoá: chữ thường, bỏ dấu câu, dấu nháy và gạch nối, số → chữ; v1.2: từ ghép/tách theo bảng COMPOUND (goodnight = good night…, RULES.md) cho cả kịch bản và bản nghe. Từ bắt buộc = toàn bộ từ trong kịch bản thoại. v1.2: (1) lượt ASR toàn file, căn Levenshtein với kịch bản để lấy mốc từng câu (câu = dòng kịch bản); cửa sổ câu = mốc chữ neo đầu/cuối nới tối đa 2 s; v1.3: ranh giới hai câu = tâm đoạn lặng dài nhất (khung 50 ms ≤ min + 10 dB, năng lượng stem thoại nếu có, không thì mix) giữa lúc BẮT ĐẦU chữ neo cuối câu trước và chữ neo đầu câu sau; cửa sổ > 28 s tách tại khoảng lặng lớn nhất. (2) ASR riêng từng cửa sổ câu, căn với câu đó. (3) v1.3 (Q-J1c): có <video>.stems/dialogue.* thì chữ ASR chỉ được giữ khi stem thoại có lời (≥ 1 khung 10 ms > max(đỉnh − 35 dB, −60 dBFS), như J1b) trong [đầu chữ − 0,15 s, cuối chữ + 0,15 s]; không có stem thì chữ nằm hoàn toàn trong im lặng số (mọi khung 50 ms chạm chữ có RMS < −60 dBFS) bị bỏ. Chữ bị bỏ liệt kê trong báo cáo. (4) Chữ lượt toàn file nằm ngoài mọi cửa sổ câu (không trong im lặng số) tính là chèn.
- Ngưỡng: 100% từ bắt buộc được nghe đúng; WER ≤ 5% (nội bộ).
- Ghi chú: Không có luồng âm.

### J1b — Lời rõ trên nhạc theo từng câu, đo từ stem thoại và stem nền (4.J/4.M — Giọng; Mix (M3: lời luôn nghe rõ trên nhạc), cấp Chặn): TRƯỢT
- Định nghĩa đo: Thư mục <video>.stems/: dialogue.* và các stem nền (M&E), xuất từ bản mix. (1) Khớp tổng: tìm lệch thời gian ±100 ms bằng tương quan chéo; bao năng lượng khung 100 ms × 7 dải octave 125 Hz–8 kHz; khớp không âm E_mix ≈ a²·E_thoại + b²·E_nền (sai số tương đối); sai lệch = P95 của |10·log10(dự đoán/E_mix)| trên ô có năng lượng (bền với AAC và limiter nhẹ). (2) Câu = đoạn hoạt động của stem thoại (khung 10 ms > đỉnh − 35 dB và > −60 dBFS), tách khi lặng ≥ 350 ms, dài ≥ 300 ms. (3) Mỗi câu: công suất 6 dải octave 250 Hz–8 kHz của a·thoại và b·nền (mono) trên khoảng câu; SII rút gọn = Σ tầm quan trọng dải (ANSI S3.5, octave) × clip((SNR dải + 15)/30, 0, 1), không tính lan truyền che lấp và ngưỡng nghe. Cửa sổ 0,5 s trượt 50 ms trong câu.
- Ngưỡng: Sai lệch bao P95 ≤ 3 dB; |20·log10(a/b)| ≤ 1 dB; SII rút gọn mỗi câu ≥ 0,75; mọi cửa sổ 0,5 s trong câu ≥ 0,45. Ngưỡng nội bộ, CHƯA HIỆU CHUẨN (Q-J1b: giữ cấp Chặn; mốc 0,75/0,45 lấy theo cách diễn giải SII của ANSI S3.5; hiệu chuẩn sau bài thử với 3–5 người nghe mù, xem RULES.md).
- Ghi chú: File không có luồng âm.

### H1 — Không chuyển động tuyến tính ở bộ phận nhân vật (4.H — Hoạt hình, cấp Chặn): ĐẠT
- Định nghĩa đo: Dữ liệu chuyển động bake theo từng khung xuất từ phần mềm dựng (không phải khoá khai báo). Với mỗi kênh lớp 'character_part': tốc độ = chuẩn hiệu giá trị giữa 2 khung kề; đang chuyển động khi tốc độ > 2% tốc độ lớn nhất của kênh. Đoạn tuyến tính = chuỗi bước liên tiếp có mọi tốc độ trong ±3% trung bình chuỗi, và (a) dài ≥ 8 bước và bắt đầu ngay sau hoặc kết thúc ngay trước một lần đứng yên (khởi/dừng không easing), hoặc (b) dài ≥ 24 bước ở bất kỳ đâu.
- Ngưỡng: 0 đoạn tuyến tính ở kênh bộ phận nhân vật. Kênh 'mechanical' được miễn nhưng phải có lý do và được liệt kê trong báo cáo.
- Bằng chứng: `{"kenh_kiem": 16, "kenh_mien": [{"id": "ida/root.loc", "lop": "character_root", "ly_do": ""}]}`

### H1b — Chuyển động khai báo khớp hình render (luồng quang học ở vùng nhân vật) (4.H — Hoạt hình, cấp Chặn): TRƯỢT
- Định nghĩa đo: <video>.motion.json phải có 'screen_tracks': toạ độ điểm ảnh từng khung của khớp nhân vật, chiếu từ rig bake qua máy quay render (null khi bị che). Luồng quang học DIS (OpenCV, preset medium, tính ở ≤ 1280 px rộng) giữa khung n và n+1 của file render; tại mỗi điểm lấy trung vị luồng trong đĩa bán kính 4 px. Cặp khung khớp khi |luồng − (p(n+1) − p(n))| ≤ max(1,5 px, 25% độ dài dịch chuyển). Tối đa 480 cặp khung rải đều.
- Ngưỡng: Mọi nhân vật có kênh 'character_part' có ≥ 1 screen track; mỗi track khớp ở ≥ 90% cặp khung đo (nội bộ).
- Ghi chú: 3 track, 47 cặp khung đo. Khớp khi |luồng − khai báo| ≤ max(1.5 px, 25% × độ dài dịch chuyển).
- Bằng chứng: `{"theo_track": {"ida/head": {"cap_khung": 47, "khop_pct": 100.0, "epe_trung_vi": 0.16, "lech_lon_nhat": null}, "ida/hand_L": {"cap_khung": 45, "khop_pct": 48.9, "epe_trung_vi": 1.85, "lech_lon_nhat": {"khung": 28, "epe": 8.57, "khai": [1.54, 1.14], "luong": [-5.47, 6.07]}}, "ida/hand_R": {"cap_khung": 47, "khop_pct": 78.7, "epe_trung_vi": 0.3, "lech_lon_nhat": {"khung": 29, "epe": 7.25, "khai": [-7.59, 0.57], "luong": [-2.06, 5.26]}}}}`

### C3 — Đúng model: tỷ lệ bộ phận so với model sheet, có tính nhiễu đo (4.C — Nhân vật, cấp Chặn): TRƯỢT
- Định nghĩa đo: <video>.parts/parts.json: mặt nạ từng bộ phận xuất từ render cho mọi khung chia hết cho 12. v1.1 (Q-C3): mặt nạ bắt buộc ở độ phân giải gấp s = 2–4 lần khung; s đo từ kích thước PNG (rộng/rộng và cao/cao phải bằng nhau, mọi mặt nạ cùng cỡ), trường 'scale' nếu có phải khớp s đo. Chống phóng to mặt nạ thấp hơn: tập vị trí biên phân biệt (x chuyển tiếp ngang, y chuyển tiếp dọc) quy về pha lưới s (k = round(s) ngăn); tỷ lệ dồn vào 1 pha phải ≤ 1/k + (1 − 1/k)/2 (s=2: 0,75; s=3: 0,67; s=4: 0,625) với ≥ 40 vị trí (render thật ≈ 1/k; phóng to từ mặt nạ nhị phân ≈ 1,0). Độ dài = bề dài chiếu lên trục chính PCA của tâm điểm ảnh + 1 px; tỷ lệ = độ dài bộ phận / độ dài đầu; lệch = tỷ lệ / tỷ lệ model sheet − 1. Nhiễu đo U(s) = √((δ/(s·L_bộ phận))² + (δ/(s·L_đầu))²), L theo px video, δ = 2 px mặt nạ (v1.2; v1.1: 1 px); hiệu chuẩn Monte Carlo trong selftest ở s = 1, 2, 4 và phủ cả sai số của mặt nạ phóng to từ matte 1× khử răng cưa rồi ngưỡng hoá (loại không phát hiện được bằng ảnh). v1.3 (Q-δ): đầu < 100 px video ở khung mẫu bất kỳ thì hệ số mặt nạ ≥ 4. v1.3 (Q-C3c) kiểm toán ngẫu nhiên: phiên P chạy checks/audit.py issue (hạt giống từ secrets, 1–2 khung trong khung mẫu, ghi <video>.audit/request.json kèm SHA video và SHA bộ mặt nạ); xưởng render lại mặt nạ các khung đó từ file cảnh đã khoá vào <video>.audit/rerender/ và ghi render.log (SCENE <file> SHA256 <hex>; FRAME <n> CMD <lệnh>). Đối chiếu: video và bộ mặt nạ không đổi sau khi phát; log đủ, SHA file cảnh khớp đĩa (và thuộc scene_files nếu có assets.json); đủ mặt nạ render lại cùng cỡ; lệch tỷ lệ bộ phận/đầu nộp so với render lại ≤ 1·U (δ = 2); điểm ảnh khác nhau / điểm ảnh biên ≤ 0,02. Chưa có yêu cầu = THIẾU. v1.2 (C3b): dải xám ở biên (điểm ảnh mức 6–249 / điểm ảnh biên) ≤ 2,5 — mặt nạ phóng to còn giữ mức xám thì trượt. Quyết định kiểu ISO 14253-1: đạt khi |lệch| + U ≤ 3%; trượt chắc chắn khi |lệch| − U > 3%; giữa hai mức = không chứng minh được. Chống khai man: biên bóng nhân vật (hợp các mặt nạ) phải nằm trên cạnh ảnh render: độ lớn cạnh trên biên / trung vị trên biên dịch ±6 px theo 8 hướng.
- Ngưỡng: Hệ số mặt nạ/khung đo được trong [2, 4], ngang = dọc, khớp số khai; pha biên ≤ 1/k + (1 − 1/k)/2; dải xám biên ≤ 2,5; đầu < 100 px thì ≥ 4×; kiểm toán ngẫu nhiên đạt (lệch ≤ 1·U, khác điểm ảnh ≤ 0,02, log và SHA file cảnh khớp); 0 bộ phận–khung trượt chắc chắn; 0 bộ phận–khung không chứng minh được; 0 khung mẫu thiếu mặt nạ; độ khớp biên ≥ 1,5 (ngưỡng 3% theo khung mục 4.C, nội bộ; 1,5 và ngưỡng pha nội bộ).
- Ghi chú: Model sheet: ida.json. Mặt nạ 7680×4320 px trên khung 1920×1080 → hệ số đo ×4 (khai báo: 4). Đầu cao 42.6–44.2 px video. Lệch lớn nhất 29.27%. 4933 vị trí biên phân biệt; tỷ lệ dồn 1 pha 0.25 (trải đều ≈ 0.25).
- Ghi chú: Kiểm toán ngẫu nhiên: hạt giống 1263884070778839232, khung [12, 36], phát bởi P lúc 2026-09-27T12:14:18Z.
- Bằng chứng: `{"kiem_toan": {"yeu_cau": {"version": 1, "seed": "1263884070778839232", "frames": [12, 36], "candidates": 4, "issued_by": "P", "issued_utc": "2026-09-27T12:14:18Z", "video": "walk.mp4", "video_sha256": "7c9bddfb0d35b8325a0d25d111a4c5331e3c626273eeba532457d3c06f86843c", "parts_sha256": "dbb767c279c4f31ad3eec010705fc3937f9a5323ad1b75a874438fe5caf138e6"}, "log_scene": [{"file": "design/cong3/v2/page.js", "sha_log": "cb2e89e9c313539e51e54cde3c70b421ee024883aadeb9a6b14360efef5eca62", "sha_dia": "cb2e89e9c313539e51e54cde3c70b421ee024883aadeb9a6b14360efef5eca62", "trong_scene_files": true, "khop": true}], "log_lenh": {"12": ["node design/cong3/shared/export_sidecars.js --page v2/page.js --shot walk --video design/cong3/v2/out/a2p/walk.mp4 --parts 12 --scale 4 --args {\"char\":\"3d\"} --audit-dir design/cong3/v2/out/a2p/walk.audit/rerender"], "36": ["node design/cong3/shared/export_sidecars.js --page v2/page.js --shot walk --video design/cong3/v2/out/a2p/walk.mp4 --parts 36 --scale 4 --args {\"char\":\"3d\"} --audit-dir design/cong3/v2/out/a2p/walk.audit/rerender"]}, "doi_chieu": [{"khung": 12, "bo_phan": "head", "khac_diem_anh_tren_bien": 0.0}, {"khung": 12, "bo_phan": "torso", "khac_diem_anh_tren_bien": 0.0}, {"khung": 12, "bo_phan": "upper_arm", "khac_diem_anh_tren_bien": 0.0}, {"khung": 12, "bo_phan": "forearm", "khac_diem_anh_tren_bien": 0.0}, {"khung": 12, "bo_phan": "thigh", "khac_diem_anh_tren_bien": 0.0}, {"khung": 12, "bo_phan": "shin", "khac_diem_anh_tren_bien": 0.0}, {"kh`

### O3 — Mọi tài sản lấy từ thư viện có SHA (4.O — Liên tục và nhất quán, cấp Chặn): ĐẠT
- Định nghĩa đo: Tính lại SHA-256 từ đĩa cho mọi tài sản trong danh sách dùng của shot và so với thư viện assets/LIBRARY.json. Quét thư mục làm việc của shot: mọi file media (mô hình, ảnh, âm, font) không nằm trong thư viện là tài sản ngoài thư viện (trừ thư mục render/, out/, cache/, frames/).
- Ngưỡng: 0 tài sản lệch SHA; 0 tài sản không có trong thư viện; 0 file media lạ trong thư mục làm việc.
- Ghi chú: File cảnh của shot (được miễn quét, v1 sẽ đọc liên kết bên trong): design/cong3/v2/page.js
- Ghi chú: Danh sách tài sản dùng rỗng.
- Bằng chứng: `{"so_tai_san_dung": 0}`
