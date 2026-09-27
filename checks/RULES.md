# CINE LAB — BỘ LUẬT L1 v1.3 (phiên K)

Căn cứ: `docs/cine-lab/CINE-LAB-KHUNG-CHAT-LUONG.md` mục 1 và 4; `docs/cine-lab/CINE-LAB-BAI-HOC-BRIEF-D.md`.
Nguyên tắc: đo từ file đã render; mỗi luật có test tự chứng minh; ngưỡng "nội bộ" là đề xuất, hiệu chuẩn sau bài thử.
v1 = toàn bộ 11 luật v0 (giữ nguyên định nghĩa, mọi test v0 vẫn đúng) + 5 luật mới (P0, G3b, J1b, H1b, C3). Rubric người chấm (loại N): `RUBRIC.md`.
v1.1 = v1 + 4 quyết định của chủ dự án (Q-C3, Q-P0, Q-G3b, Q-J1b), xem mục "Thay đổi của v1.1". Không thêm mã luật mới; vẫn 16 luật, đều cấp Chặn.
Định nghĩa máy đọc nằm trong `cinecheck/registry.py`; báo cáo mỗi lần chạy chép lại định nghĩa và ngưỡng.

v1.2 = v1.1 + 3 khiếu nại J1 được chủ dự án chấp nhận (27/09/2026) + Q-C3b (bịt lỗ hổng mặt nạ phóng to). Vẫn 16 luật, đều cấp Chặn; không nới ngưỡng nào.

v1.3 = v1.2 + quyết định của chủ dự án về v1.2: Q-C3c = B (kiểm toán ngẫu nhiên), Q-δ = A (δ = 2; 4× khi đầu < 100 px), Q-J1c = phương án mới (chèn theo stem thoại). Không nới ngưỡng nào.

### Thay đổi của v1.3

| Căn cứ | Luật | Thay đổi | Ngưỡng | Test tự chứng minh (TRƯỢT / SẠCH) |
|---|---|---|---|---|
| Q-J1c | J1 | Có `<video>.stems/dialogue.*`: chữ ASR chỉ được giữ (và tính chèn nếu không khớp kịch bản) khi stem thoại có lời, tức ≥ 1 khung 10 ms > max(đỉnh − 35 dB, −60 dBFS) như J1b, trong [đầu chữ − 0,15 s, cuối chữ + 0,15 s]. Chữ rơi vào lúc stem thoại im bị bỏ và liệt kê. Không có stem: giữ quy tắc −60 dBFS của v1.2 (J1b khi đó báo THIẾU) | không đổi | kịch bản thiếu một câu có trong stem thoại (room tone −55 dBFS) / table read + room tone −55 dBFS trong mix, stem thoại im giữa câu; ca đơn vị: chữ bịa trong room tone bị quy tắc −60 giữ, quy tắc stem bỏ |
| Lỗi phát hiện khi viết selftest Q-J1c | J1 | Ranh giới hai câu kề nhau = tâm đoạn lặng dài nhất (khung 50 ms ≤ min + 10 dB; năng lượng stem thoại nếu có, không thì mix) giữa lúc **bắt đầu** chữ neo cuối câu trước và chữ neo đầu câu sau. Lý do: khi mix có room tone, Whisper kéo mốc **kết thúc** chữ cuối câu 4 ("it") tới 139,84 s, nuốt chữ "Warm" đầu câu 5. Cách cắt ở điểm giữa của v1.2 làm mất lại "Warm", đúng lỗi của khiếu nại số 3 | không đổi | ca room tone trên (trước khi sửa: TRƯỢT, mất "warm"); mọi ca J1 v1.2 vẫn khớp |
| Q-δ = A | C3 | Giữ δ = 2 px. Đầu < 100 px video ở bất kỳ khung mẫu nào thì hệ số mặt nạ đo được phải ≥ 4 | ≥ 4× khi đầu < 100 px | đầu 57 px, mặt nạ 2× / đầu 80 px, mặt nạ 4× |
| Q-C3c = B | C3 | Kiểm toán ngẫu nhiên (`cinecheck/audit.py`, lệnh `checks/audit.py`). Phiên P phát yêu cầu: hạt giống lấy từ `secrets` của hệ điều hành, chọn 1–2 khung trong các khung có mặt nạ đầu, ghi `request.json` kèm SHA video và SHA bộ mặt nạ; lệnh từ chối phát lại. Xưởng render lại từ file cảnh đã khoá, kèm `render.log`. C3 đối chiếu (qua `run.py`) | video và bộ mặt nạ không đổi; log có SCENE (SHA khớp đĩa, thuộc scene_files) và FRAME…CMD cho mỗi khung; đủ mặt nạ render lại cùng cỡ; lệch tỷ lệ ≤ 1·U (δ = 2); khác điểm ảnh ≤ 0,02 × điểm ảnh biên (nội bộ). Chưa có yêu cầu: **THIẾU** | render lại không khớp: mặt nạ nộp là matte 1× phóng to bicubic rồi ngưỡng hoá (loại C3b không bắt được); thân dài hơn 2%; thiếu log; SHA file cảnh sai; thiếu dòng FRAME; thiếu mặt nạ render lại; mặt nạ sửa sau khi phát / render lại khớp, log đủ; chưa có yêu cầu → THIẾU; phát lại bị từ chối |

**Về ngưỡng khác điểm ảnh 0,02 (vượt nguyên văn quyết định):** Quyết định Q-C3c nêu "lệch vượt dải nhiễu". Chỉ riêng tiêu chí đó không bắt được loại phóng to C3b không phát hiện được, vì sai số của loại này nằm trong dải U (đó chính là lý do chọn δ = 2). Phép so điểm ảnh bắt được nó: khảo sát v1.2 cho mặt nạ phóng to ở 4× lệch 5–10% điểm ảnh biên so với render thật, trong khi render lại cùng cách cho gần 0. Vì vậy K đặt thêm ngưỡng 0,02, xem quyết định Q-C3d.

### Thay đổi của v1.2

| Căn cứ | Luật | Thay đổi | Ngưỡng | Test tự chứng minh (TRƯỢT / SẠCH) |
|---|---|---|---|---|
| Khiếu nại J1 số 1 (goodnight) | J1 | Chuẩn hoá từ ghép/tách theo bảng COMPOUND dưới đây, áp cho cả kịch bản và bản nghe. Chỉ các mục trong bảng; không so gần đúng | Không đổi: 100% từ; WER ≤ 5% | "good" thay "goodnight" vẫn lỗi / goodnight = good night, alright = all right, okay = OK; table read nháp 1 |
| Khiếu nại J1 số 2 (chữ bịa trong im lặng) | J1 | Chữ ASR (theo mốc từng chữ) nằm **hoàn toàn** trong im lặng số (mọi khung 50 ms chạm chữ có RMS < −60 dBFS) bị bỏ trước khi căn. Danh sách chữ bị bỏ và vùng im lặng số ≥ 0,5 s ghi vào báo cáo | như trên | xoá "Warm" thành 0 tuyệt đối → thiếu từ, TRƯỢT / chữ bịa trong đoạn 0 bị bỏ, chữ ở vùng có tiếng giữ nguyên |
| Khiếu nại J1 số 3 (mất chữ ở ranh giới đoạn giải mã) | J1 | Kiểm theo từng câu (câu = dòng kịch bản). Lượt 1: ASR toàn file có mốc chữ, căn với kịch bản để lấy mốc câu. Cửa sổ câu = chữ neo đầu/cuối nới tối đa 2 s, không vượt điểm giữa khoảng lặng với câu kề (câu không neo được: cả khoảng giữa hai câu kề). Cửa sổ > 28 s tách tại khoảng lặng lớn nhất. Lượt 2: ASR riêng từng cửa sổ, căn với câu đó. Chữ lượt 1 nằm ngoài mọi cửa sổ (không trong im lặng số) tính là chèn | như trên | kịch bản thiếu câu có thật trong audio (4 chữ chèn ở vùng có tiếng); kịch bản thêm "more" không nói / table read nháp 1: "warm" nghe đúng |
| Q-C3b | C3 | (a) **Biên mờ**: dải xám ở biên (điểm ảnh mức 6–249 / điểm ảnh biên của mặt nạ ngưỡng hoá) ≤ 2,5. Mặt nạ phóng to còn giữ mức xám có dải ≈ s × độ rộng khử răng cưa gốc. (b) **Bậc thang**: kiểm pha lưới của v1.1 (láng giềng gần, phóng to mặt nạ nhị phân). (c) **Loại không phát hiện được bằng ảnh** (matte 1× khử răng cưa, phóng to bằng nhân mượt, rồi ngưỡng hoá): khảo sát v1.2 cho thấy chỉ số "dựng lại từ 1×" của mặt nạ thật (0,067–0,13) và mặt nạ phóng to (0,047–0,078) chồng nhau trên hình đa giác, nên không làm luật Chặn được. Thay vào đó **δ nâng 1 → 2 px mặt nạ** để dải bảo vệ phủ cả sai số của loại này: mặt nạ phóng to không thể cho kết luận "đạt" sai | dải xám ≤ 2,5 (nội bộ); δ = 2 px mặt nạ | 1× AA phóng to 4× và 2× giữ xám (dải 7,3 và 3,7); 1× AA láng giềng gần 4× (pha 1,00) / mặt nạ thật 4× khử răng cưa (dải 0,75); δ = 2 phủ mặt nạ thật (≤ 0,47·U) và mặt nạ phóng to song tuyến/bicubic/Lanczos (≤ 0,78·U) |

**Bảng COMPOUND (J1 v1.2)** — dạng bên trái được đổi thành dạng bên phải ở cả kịch bản và bản nghe, sau khi bỏ dấu câu, dấu nháy, gạch nối (nên "good-night" đã là "good night"):
goodnight, goodbye, goodmorning → good night/bye/morning · alright → all right · okay → ok · anymore, anyone, anybody, anything, anywhere, anyway(s) → any + … · everyone, everybody, everything, everywhere, everyday → every + … · someone, somebody, something, somewhere, sometime(s) → some + … · noone, nobody, nothing, nowhere → no + … · tonight, today, tomorrow → to + … · cannot, maybe, into, onto, outside, inside, upstairs, downstairs → tách · streetlight(s), lamplight, lamplighter, lamppost(s) → tách · mr, mrs, ms, dr, st → mister, missus, miz, doctor, saint.
Thêm mục vào bảng = sửa luật: phiên K làm, chủ dự án duyệt, khoá lại LOCK.

**Hiệu chuẩn lại C3 (v1.2):** khảo sát thêm cỡ đầu (40–146 px, 9 cỡ, ~770 mẫu) cho thấy mặt nạ **thật** có sai số tới 1,21·U(δ = 1): mô hình δ = 1 px của v1.1 che thiếu khi có thêm cỡ đầu (4 cỡ của v1.1 đều ≤ 1). Mặt nạ phóng to ngưỡng hoá tới 1,557·U(δ = 1). δ = 2 px phủ cả hai, còn biên 22%. Hệ quả: dải bảo vệ rộng gấp đôi v1.1. Ở đầu 57 px, mặt nạ 4× chứng minh được lệch tới khoảng ±2% (v1.1: ±2,5%); ca selftest v1.1 "thân +2%" đổi thành "+1,5%".

### Thay đổi của v1.1 (theo quyết định chủ dự án)

| Quyết định | Luật | Thay đổi | Ngưỡng | Test tự chứng minh (TRƯỢT / SẠCH) |
|---|---|---|---|---|
| Q-C3: giữ luật chặt, bắt buộc mặt nạ 2–4× | C3 | Hệ số s = rộng mặt nạ/rộng video = cao mặt nạ/cao video, **đo từ kích thước PNG**, không tin trường `scale` (nếu khai thì phải khớp). Chống phóng to: tập vị trí biên phân biệt quy về pha lưới s; mặt nạ phóng to từ mặt nạ nhị phân thấp hơn có biên dồn vào 1 pha. Nhiễu đo U(s) = √((δ/(s·L_bp))² + (δ/(s·L_đầu))²), L theo px video, δ = 1 px mặt nạ, hiệu chuẩn Monte Carlo ở s = 1, 2, 4 | s ∈ [2, 4]; mọi mặt nạ cùng cỡ; ngang = dọc; pha dồn ≤ 1/k + (1 − 1/k)/2 (k = round(s); s=2: 0,75, s=4: 0,625) với ≥ 40 vị trí (nội bộ) | mặt nạ 1×; 1× phóng to lên 4× (pha 1,00); thật 2× khai 4 / đầu 57 px thân +2% ở 4× (nay đạt, trước trượt); 3×; 2× không khai; mô hình nhiễu phủ 100% ở s = 1, 2, 4 |
| Q-P0: nhãn diegetic | P0, G4, P1 | Phần tử có `"diegetic": true` (đúng kiểu boolean) được miễn đo tương phản G4. Vẫn phải có matte (P0), vẫn qua P1, và vẫn phải khớp matte–render (P1 và G4). **Chống lạm dụng (P0):** chữ máy đọc được trong matte phần tử diegetic được so với (a) từng dòng và từng câu thoại trong `<video>.script.txt` (phụ đề), (b) chữ máy đọc được trong matte phần tử không diegetic (tiêu đề, phụ đề, credit), (c) trường `text` khai cho phần tử không diegetic. Trùng thì TRƯỢT. P0 đọc thêm khung giữa của mỗi phần tử | P0: 0 vùng diegetic trùng. Trùng = giống cả dòng ≥ 0,80, hoặc giống một đoạn liền ≥ 0,85 với ≥ 2 từ và ≥ 50% số từ của dòng (nội bộ) | phụ đề gắn diegetic; tiêu đề lặp lại gắn diegetic; biển hiệu diegetic thiếu matte; G4 không gắn nhãn; nhãn kiểu chuỗi `"true"`; diegetic matte lệch 60 px; P1 phụ đề đè biển hiệu / biển hiệu diegetic + tiêu đề + kịch bản; biển hiệu 1,4:1 gắn diegetic; biển hiệu tách phụ đề |
| Q-G3b: master có grain ≥ 30 Mbps | N3 (dùng số đo G3b) | Profile youtube: nếu σ grain trung vị của một shot bất kỳ (đo như G3b) ≥ 0,8 mã thì ngưỡng bitrate hình đo tăng lên 30 Mbps (1080p; 2160p giữ 45) | ≥ 30 Mbps khi có grain (nội bộ) | grain σ 2,5 ở 14 Mbps (qua ngưỡng cũ 12) / grain σ 2,5 ở 36 Mbps; testsrc 14 Mbps không grain vẫn đạt |
| Q-J1b: giữ Chặn, ngưỡng nội bộ | J1b | Không đổi phép đo. Ghi rõ trong định nghĩa và mọi báo cáo: **ngưỡng nội bộ, chưa hiệu chuẩn**. Kế hoạch hiệu chuẩn ở mục dưới | như v1 | như v1 |

### Kế hoạch hiệu chuẩn J1b (sau bài thử 2–3 phút)

1. **Mẫu.** Lấy từ stem thật của bài thử, gồm mọi câu thoại. Thêm các biến thể: nền tăng +3, +6, +9 dB trên từng câu. Biến thể là bản trộn lại từ stem, không phải bản mix phát hành. Tổng khoảng 60–100 câu, phủ SII câu từ khoảng 0,4 đến 0,95.
2. **Người nghe.** 3–5 người, tiếng Anh thành thạo, không biết kịch bản và không biết câu nào là biến thể. Nghe mù qua tai nghe, ở mức nghe cố định (bản master −14 LUFS). Mỗi câu nghe một lần, chép lại lời; không chép được thì ghi "không rõ".
3. **Đo.** Tỷ lệ từ đúng của mỗi câu, lấy trung vị qua người nghe. Câu "rõ" khi ≥ 90% từ đúng.
4. **Hiệu chuẩn.** Khớp đường logistic giữa SII câu và xác suất "rõ". Ngưỡng câu mới = SII mà tại đó xác suất rõ ≥ 95% (cận dưới khoảng tin 90%). Ngưỡng cửa sổ 0,5 s hiệu chuẩn tương tự trên các câu có một đoạn bị lấn.
5. **Quyết định.** Ngưỡng mới lệch khỏi 0,75 hoặc 0,45 quá 0,05 thì phiên K đề xuất sửa, chủ dự án duyệt, rồi khoá lại LOCK. J1b phân biệt kém (AUC < 0,8) thì đề xuất hạ cấp theo nguyên tắc chống Goodhart số 4.
6. **Ghi lại** vào `reports/checks-calib/J1b/`: stem, danh sách biến thể, phiếu nghe (ẩn danh) và đường khớp.

### Luật giữ nguyên từ v0

| Mã | Mục khung | Định nghĩa đo (tóm tắt) | Ngưỡng | Cấp | Test tự chứng minh (TRƯỢT / SẠCH) |
|---|---|---|---|---|---|
| N1 | 4.N | PTS từng gói hình (ffprobe), r/avg_frame_rate | 24/1; 0 bước lệch > 0,5 ms; 0 trùng; 0 hở | Chặn | rơi khung 10; 25 fps / testsrc 24 fps |
| N2 | 4.N | Nhãn primaries/transfer/matrix/range + tỷ lệ luma ngoài dải limited | đủ bt709 + tv; ngoài dải ≤ 0,5% (nội bộ) | Chặn | không nhãn; nhãn tv nhưng luma 0/255 / đủ nhãn |
| N3 | 4.N | Codec, profile, pix_fmt, kích thước, SAR; bitrate hình đo từ tổng gói | YouTube: H.264 High/HEVC, 1080p ≥ 12 Mbps, 2160p ≥ 45 Mbps (nội bộ), AAC-LC 48 kHz stereo. Lưu trữ: ProRes HQ/4444, DNxHR HQ/HQX/444, FFV1; PCM ≥ 24 bit | Chặn | 3 Mbps + 44,1 kHz; H.264 làm lưu trữ / 14 Mbps; ProRes HQ |
| P1 | 4.P | Matte RGBA từng phần tử chữ; nét = alpha ≥ 0,5 nới 1 px; đếm điểm ảnh thuộc ≥ 2 nét; đối chiếu matte với render | 0 px va chạm; độ khớp matte ≥ 90% | Chặn | phụ đề đè tiêu đề; matte khai lệch 60 px / tách rời |
| G4 | 4.G | Độ chói WCAG: trung vị lõi nét vs vành nền 2–6 px; phân vị 10 tỷ lệ | ≥ 4,5:1 | Chặn | xám trên xám (1,5:1) / sáng trên tối (14,8:1) |
| G3 | 4.G | Điểm trong mảng phẳng 5×5, cửa sổ 95×95 có ≥ 3 mức phẳng, bước ≤ 2 mã, biên độ ≤ 24 mã | diện tích ≤ 0,2% khung (nội bộ) | Chặn | gradient 8 bit không dither (45%) / có grain (0%); mảng phẳng biên cứng (0%) |
| M1 | 4.M | ffmpeg ebur128, peak=true | −15 … −13 LUFS; TP ≤ −1,0 dBTP | Chặn | −8 LUFS cắt đỉnh / −14 LUFS |
| M3 | 4.M | Tương quan cửa sổ 400 ms; mất mát mono BS.1770 tích phân và cửa sổ 3 s | ≤ 1% cửa sổ r < −0,3; ≥ −3 dB; ≥ −6 dB (nội bộ) | Chặn | kênh phải đảo pha / stereo tương quan |
| J1 | 4.J | faster-whisper small.en ghim revision, int8, beam 5, không mồi kịch bản; căn Levenshtein | 100% từ kịch bản; WER ≤ 5% (nội bộ) | Chặn | ồn lấn át lời 2,5 s / nhạc nền −22 dB |
| H1 | 4.H | Tốc độ từng khung từ chuyển động bake; đoạn tốc độ không đổi ±3% ≥ 8 bước sát lần đứng yên, hoặc ≥ 24 bước ở đâu cũng vậy | 0 đoạn ở `character_part` | Chặn | tay nội suy tuyến tính / easing, cung, quay chậm 4 s |
| O3 | 4.O | SHA-256 tính lại từ đĩa so với `assets/LIBRARY.json`; quét file media lạ trong thư mục shot | 0 lệch, 0 ngoài thư viện, 0 file lạ | Chặn | tài sản sửa sau khoá + vẽ lại / khớp |

### Luật mới của v1

| Mã | Mục khung | Định nghĩa đo (tóm tắt) | Ngưỡng | Cấp | Test tự chứng minh (TRƯỢT / SẠCH) |
|---|---|---|---|---|---|
| P0 | 4.P | Máy dò chữ độc lập PP-OCRv4 det + rec (ONNX ghim SHA trong `models/`), 2 khung/giây; chỉ giữ vùng đọc ra chữ Latin độ tin ≥ 0,8 và nét không đặc (độ đặc < 0,85); vùng có matte = ≥ 50% hộp nằm trong nét matte nới | 0 vùng chữ không có matte (nội bộ) | Chặn | phụ đề thiếu matte; chữ không có thư mục chữ / đủ matte trên nền lưới cửa sổ sáng; không chữ trên nền lưới cửa sổ; hồi quy khung M0 bị đọc nhầm "88:18" |
| G3b | 4.G | σ grain = 1,4826·MAD phần dư (luma − Gauss σ 1,5) trên khối 32 px phẳng, luma 40–210; cặp khung kề mỗi 12 khung; shot tách bằng PySceneDetect | σ mỗi shot ≥ 0,8 mã; CV trong shot ≤ 0,20; shot max/min ≤ 1,30; tương quan khung kề ≤ 0,50 (nội bộ) | Chặn | không grain; shot 2 σ 1,1 vs 1,8; grain đứng yên / 2 shot σ 1,8 grain động |
| J1b (ngưỡng nội bộ, chưa hiệu chuẩn) | 4.J, 4.M (M3) | Stem thoại + stem nền (M&E) do mix xuất. (1) Khớp bao năng lượng 100 ms × 7 octave: mix ≈ a²·thoại + b²·nền. (2) Câu = đoạn stem thoại tách bởi lặng ≥ 350 ms. (3) SII rút gọn (tầm quan trọng dải octave ANSI S3.5) mỗi câu và cửa sổ 0,5 s | P95 sai lệch bao ≤ 3 dB; \|a/b\| ≤ 1 dB; SII câu ≥ 0,75; SII cửa sổ ≥ 0,45 (nội bộ) | Chặn | ồn +9 dB 2,5 s (mẫu J1 vẫn cho qua 17/18 từ); stem thoại khai to 6 dB; ồn trong mix không có trong stem / nhạc −22 dB; −14 LUFS + limiter |
| H1b | 4.H | `screen_tracks` (toạ độ khớp nhân vật chiếu qua máy quay) so với luồng quang học DIS trên file render, trung vị đĩa 4 px | mọi nhân vật có track; mỗi track khớp ≥ 90% cặp khung (nội bộ) | Chặn | khai easing nhưng render tuyến tính; thiếu track / track đúng |
| C3 | 4.C | Mặt nạ bộ phận mỗi 12 khung; độ dài PCA; tỷ lệ so model sheet; nhiễu U = √((1 px/L)² + (1 px/L_đầu)²) hiệu chuẩn Monte Carlo; quyết định dải bảo vệ (ISO 14253-1); biên mặt nạ phải nằm trên cạnh ảnh render. **v1.1: thêm hệ số mặt nạ 2–4× (xem trên)** | 0 trượt chắc chắn (\|lệch\| − U > 3%); 0 không chứng minh được (\|lệch\| + U > 3%); độ khớp biên ≥ 1,5 (nội bộ) | Chặn | thân +6%; đầu 57 px (nhiễu vượt biên); mặt nạ lệch 20 px / đúng sheet đầu 146 px; thân +2% đầu 146 px; mô hình nhiễu phủ 100% sai số |

Kết quả test tự chứng minh: `reports/checks-selftest/selftest.md` (v1.3: 96 ca đơn — 81 ca v1.2 giữ kỳ vọng, cộng 15 ca mới (3 J1, 12 C3); chạy đầu–cuối có thêm bước kiểm toán ngẫu nhiên. v1.2: 81 ca đơn — 69 ca v1.1 giữ kỳ vọng, trong đó ca C3 "đầu 57 px, 4×" đổi thân +2% → +1,5% vì δ = 2 và ca hiệu chuẩn nhiễu dùng δ = 2; cộng 12 ca mới (7 J1, 5 C3). v1.1: 69 ca đơn — 51 ca v1 giữ nguyên kỳ vọng, trong đó 4 ca C3 chuyển mặt nạ 1× sang 2× và ca hiệu chuẩn nhiễu mở rộng ra s = 1, 2, 4; cộng 18 ca mới — và chạy đầu–cuối 16 luật qua `run.py`).

## Giới hạn đã biết của v1.3 (mới)

1. **Log render lại là bản khai.** Máy chỉ kiểm được: log có đủ dòng; SHA file cảnh khớp; mặt nạ render lại khớp mặt nạ nộp. Xưởng vẫn có thể ghi lệnh không đúng thật. Muốn chặn tận gốc thì máy phải tự chạy lệnh render (quyết định Q-C3e).
2. **Kiểm toán 1–2 khung là lấy mẫu**: gian lận chỉ ở một phần khung có xác suất bị lọt, ước tính bằng số khung được chọn / số khung mẫu.
3. **Ngưỡng khác điểm ảnh 0,02 giả định render tất định.** Mặt nạ lấy từ pass có nhiễu lấy mẫu (ví dụ Cryptomatte với ít mẫu) có thể lệch nhẹ giữa hai lần render; nếu gặp thì khiếu nại để hiệu chuẩn.
4. **J1 theo stem thoại tin rằng stem thoại chứa đúng và đủ lời thoại.** J1b kiểm tổng stem khớp mix, nhưng không biết lời nằm ở stem nào. Lời không có trong kịch bản mà để ở stem nền (M&E) thì J1 không tính chèn. Tiếng người nền (walla) ở M&E là hợp lệ; lời thoại thật thì không.

## Giới hạn đã biết của v1.2 (mới)

1. **Mặt nạ phóng to từ matte 1× khử răng cưa rồi ngưỡng hoá bằng nhân mượt vẫn không bị phát hiện** (không thể phân biệt đáng tin bằng phân tích ảnh, số đo ở trên). v1.2 làm nó **vô hại về kết luận** (δ = 2 px phủ sai số của nó), nhưng không bắt được việc vi phạm quy trình. Bắt tận gốc cần kiểm nguồn gốc render (quyết định Q-C3c).
2. **J1 im lặng số dùng ngưỡng −60 dBFS**: chữ bịa trong room tone (thường −70…−50 dBFS) trên ngưỡng thì vẫn tính chèn. Bản mix thật có room tone nên ít chữ bịa hơn (theo khiếu nại số 2); nếu vẫn bịa thì khiếu nại lại.
3. **J1 lấy mốc câu từ lượt toàn file**: câu hoàn toàn không neo được thì cửa sổ là cả khoảng giữa hai câu kề (có thể dài). Chữ ở vùng giao ranh cửa sổ kề nhau có thể bị một câu bắt thay câu kia; tổng số từ vẫn đúng nhưng lỗi có thể quy nhầm câu.
4. **Bảng COMPOUND là danh sách đóng**: biến thể ngoài bảng vẫn tính lỗi (chủ ý, để không nới). Gặp trường hợp mới thì khiếu nại.

## Giới hạn đã biết của v1.1 (nêu thẳng để chủ dự án quyết)

1. **Kiểm pha của C3 chỉ bắt mặt nạ phóng to từ mặt nạ nhị phân** (láng giềng gần, song tuyến rồi ngưỡng, bicubic). Nếu phóng to một matte 1× **có khử răng cưa** (mức xám mang thông tin dưới điểm ảnh) rồi ngưỡng, biên có thể trải đều pha và lọt. Loại này có độ chính xác gần với render thật nhưng chưa được chứng minh bằng test. Hình dạng có nhiều cạnh thẳng song song trục khung làm pha dồn hơn; ngưỡng đặt giữa "trải đều" và "phóng to" để chừa biên. *(v1.2: xem giới hạn 1 của v1.2.)*
2. **Mặt nạ 4× nặng**: 1080p → 7680×4320 mỗi bộ phận. C3 đọc mỗi 12 khung; bài thử 2–3 phút mất khoảng vài phút cho C3.
3. **Chống lạm dụng diegetic chỉ so với thoại trong kịch bản và chữ không diegetic.** Nếu tiêu đề phim chỉ xuất hiện dưới dạng diegetic và không có ở đâu khác thì máy không biết đó là tiêu đề. Ngược lại, biển hiệu mà nhân vật đọc to đúng nguyên câu thoại sẽ bị tính là trùng phụ đề và TRƯỢT (quyết định Q-P0b). Chữ diegetic bị méo phối cảnh mạnh có thể không đọc được; khi đó máy không so được, nhưng P0 cũng không bắt thiếu matte.
4. **N3 dùng σ grain của G3b.** Grain bị bộ mã hoá xoá xuống dưới 0,8 mã thì N3 chỉ đòi 12 Mbps, nhưng G3b vẫn trượt vì thiếu grain nên kết luận chung vẫn TRƯỢT.

## Giới hạn đã biết của v1 (nêu thẳng để chủ dự án quyết)

Đã vá từ v0: giới hạn 1 (J1 dễ dãi) → J1b; giới hạn 2 (chữ không matte) → P0; giới hạn 3 (tin dữ liệu bake) → H1b; giới hạn 5 (grain) → G3b.

1. **J1b dùng SII rút gọn**, không tính lan truyền che lấp, ngưỡng nghe và méo mức của ANSI S3.5 đầy đủ; mốc 0,75/0,45 lấy từ cách diễn giải SII, chưa hiệu chuẩn với người nghe phim. J1b tin rằng stem thoại chỉ chứa thoại (tiếng động lẫn vào stem thoại được tính là lời). Tổng stem được kiểm với mix nên stem khai to/thiếu âm đều trượt.
2. **P0 chỉ xác nhận chữ Latin** (phim tiếng Anh). *(v1.1: câu cuối của mục này về G4 cho chữ trong thế giới phim đã được thay bằng nhãn diegetic, Q-P0.)* Lần chạy đầu trên M0 báo nhầm một lưới cửa sổ thành chữ "8818" (độ tin 0,88); đã thêm bộ lọc độ đặc nét và ca hồi quy. Số hoặc chữ vẽ bằng khối đặc (kiểu đồng hồ LED) sẽ bị bỏ qua. Chữ trang trí quá cách điệu có thể lọt máy dò; vùng máy dò nghi nhưng nhận dạng loại được đếm trong báo cáo để người duyệt soi. Chữ trong thế giới phim (biển hiệu) cũng phải có matte, và khi đã có matte thì G4 đòi 4,5:1 (xem quyết định Q-P0).
3. **H1b nối `screen_tracks` với hình render**, nhưng chưa nối kênh rig (`channels`) với `screen_tracks`: bản khai rig giả mà track thật vẫn lọt; cần phép chiếu rig → màn hình (v2). Điểm bị che phải khai `null`; tỷ lệ null nằm trong báo cáo. Luồng quang học yếu trên mảng màu phẳng (đầu nhân vật M0: 91,1%, sát ngưỡng 90%).
4. **C3 đo độ dài 2D**: bộ phận chĩa về phía máy quay bị ngắn đi (phối cảnh) và sẽ trượt oan; v1 chưa có miễn trừ theo góc nhìn. Ở đầu cao ~57 px, nhiễu đo (U 2–2,7%) ăn gần hết biên 3% nên hầu như không chứng minh được: phải render mặt nạ ở `scale` 2–4 (quyết định Q-C3). **v1.1: đã bắt buộc 2–4×**; vấn đề phối cảnh vẫn còn.
5. **G3b giả định grain đều theo độ sáng** trong dải luma 40–210; grain phụ thuộc độ sáng có thể làm lệch tỷ số giữa shot sáng và shot tối. G3b cũng bắt grain bị bộ mã hoá làm dao động theo khung I/P/B (thấy ở mẫu 1080p 14 Mbps trong lúc viết selftest).
6. **O3 tin vào danh sách tài sản và `scene_files`** (như v0).
7. **M3 chỉ đo stereo**; bản 5.1 cần luật riêng (như v0).
8. Ngưỡng "nội bộ" (v0: N2 0,5%, N3 12/45 Mbps, G3 0,2%, M3 −3/−6 dB, J1 WER 5%; v1: P0, G3b, J1b, H1b, C3) chưa hiệu chuẩn với người chấm (nguyên tắc N4 của BAI-HOC).

## Giới hạn đã biết của v0 (bản gốc, giữ để đối chiếu)


1. **J1 dễ dãi hơn tai người.** Ở mẫu TRƯỢT, tiếng ồn lớn hơn lời 9 dB suốt 2,5 giây mà ASR vẫn đoán đúng 17/18 từ nhờ mô hình ngôn ngữ; chỉ trượt 1 từ ("ships" → "shifts"). Nghĩa là J1 bắt được lời mất hẳn, nhưng có thể cho qua lời bị nhạc lấn mà người nghe thật không rõ. Đề xuất bổ sung (quyết định Q2 trong báo cáo).
2. **P1/G4 tin vào matte chữ do render xuất.** Máy đối chiếu matte với khung hình nên matte giả lệch vị trí hay sai màu sẽ trượt; nhưng nếu phiên xưởng **không xuất** matte cho một dòng chữ có trong hình thì v0 không thấy. Cần máy dò chữ độc lập (Q3).
3. **H1 tin vào dữ liệu chuyển động bake.** Chưa đối chiếu với hình render (luồng quang học). Nhãn lớp kênh (`mechanical`, `character_root`) là khai báo; báo cáo liệt kê để người duyệt soi.
4. **O3 tin vào danh sách tài sản và `scene_files`.** SHA tính lại từ đĩa, nhưng việc file cảnh thật sự nạp gì chưa được đọc trực tiếp (bpy trong môi trường hiện FAIL ở `verify.sh`).
5. **G3** đo "không banding", chưa đo phần "grain cố định" trong mục G3 của khung.
6. **M3** chỉ đo stereo. Bản 5.1 (nếu làm DCP) cần luật riêng.
7. Ngưỡng "nội bộ" (N2 0,5%, N3 12/45 Mbps, G3 0,2%, M3 −3/−6 dB, J1 WER 5%) chưa hiệu chuẩn với người chấm (nguyên tắc N4 của BAI-HOC).
