# CINE LAB — BỘ LUẬT L1 v1 (phiên K)

Căn cứ: `docs/cine-lab/CINE-LAB-KHUNG-CHAT-LUONG.md` mục 1 và 4; `docs/cine-lab/CINE-LAB-BAI-HOC-BRIEF-D.md`.
Nguyên tắc: đo từ file đã render; mỗi luật có test tự chứng minh; ngưỡng "nội bộ" là đề xuất, hiệu chuẩn sau bài thử.
v1 = toàn bộ 11 luật v0 (giữ nguyên định nghĩa, mọi test v0 vẫn đúng) + 5 luật mới (P0, G3b, J1b, H1b, C3). Rubric người chấm (loại N): `RUBRIC.md`.
Định nghĩa máy đọc nằm trong `cinecheck/registry.py`; báo cáo mỗi lần chạy chép lại định nghĩa và ngưỡng.

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
| J1b | 4.J, 4.M (M3) | Stem thoại + stem nền (M&E) do mix xuất. (1) Khớp bao năng lượng 100 ms × 7 octave: mix ≈ a²·thoại + b²·nền. (2) Câu = đoạn stem thoại tách bởi lặng ≥ 350 ms. (3) SII rút gọn (tầm quan trọng dải octave ANSI S3.5) mỗi câu và cửa sổ 0,5 s | P95 sai lệch bao ≤ 3 dB; \|a/b\| ≤ 1 dB; SII câu ≥ 0,75; SII cửa sổ ≥ 0,45 (nội bộ) | Chặn | ồn +9 dB 2,5 s (mẫu J1 vẫn cho qua 17/18 từ); stem thoại khai to 6 dB; ồn trong mix không có trong stem / nhạc −22 dB; −14 LUFS + limiter |
| H1b | 4.H | `screen_tracks` (toạ độ khớp nhân vật chiếu qua máy quay) so với luồng quang học DIS trên file render, trung vị đĩa 4 px | mọi nhân vật có track; mỗi track khớp ≥ 90% cặp khung (nội bộ) | Chặn | khai easing nhưng render tuyến tính; thiếu track / track đúng |
| C3 | 4.C | Mặt nạ bộ phận mỗi 12 khung; độ dài PCA; tỷ lệ so model sheet; nhiễu U = √((1 px/L)² + (1 px/L_đầu)²) hiệu chuẩn Monte Carlo; quyết định dải bảo vệ (ISO 14253-1); biên mặt nạ phải nằm trên cạnh ảnh render | 0 trượt chắc chắn (\|lệch\| − U > 3%); 0 không chứng minh được (\|lệch\| + U > 3%); độ khớp biên ≥ 1,5 (nội bộ) | Chặn | thân +6%; đầu 57 px (nhiễu vượt biên); mặt nạ lệch 20 px / đúng sheet đầu 146 px; thân +2% đầu 146 px; mô hình nhiễu phủ 100% sai số |

Kết quả test tự chứng minh: `reports/checks-selftest/selftest.md` (v1: 51 ca đơn — 28 ca v0 giữ nguyên + 23 ca mới — và chạy đầu–cuối 16 luật qua `run.py`).

## Giới hạn đã biết của v1 (nêu thẳng để chủ dự án quyết)

Đã vá từ v0: giới hạn 1 (J1 dễ dãi) → J1b; giới hạn 2 (chữ không matte) → P0; giới hạn 3 (tin dữ liệu bake) → H1b; giới hạn 5 (grain) → G3b.

1. **J1b dùng SII rút gọn**, không tính lan truyền che lấp, ngưỡng nghe và méo mức của ANSI S3.5 đầy đủ; mốc 0,75/0,45 lấy từ cách diễn giải SII, chưa hiệu chuẩn với người nghe phim. J1b tin rằng stem thoại chỉ chứa thoại (tiếng động lẫn vào stem thoại được tính là lời). Tổng stem được kiểm với mix nên stem khai to/thiếu âm đều trượt.
2. **P0 chỉ xác nhận chữ Latin** (phim tiếng Anh). Lần chạy đầu trên M0 báo nhầm một lưới cửa sổ thành chữ "8818" (độ tin 0,88); đã thêm bộ lọc độ đặc nét và ca hồi quy. Số hoặc chữ vẽ bằng khối đặc (kiểu đồng hồ LED) sẽ bị bỏ qua. Chữ trang trí quá cách điệu có thể lọt máy dò; vùng máy dò nghi nhưng nhận dạng loại được đếm trong báo cáo để người duyệt soi. Chữ trong thế giới phim (biển hiệu) cũng phải có matte, và khi đã có matte thì G4 đòi 4,5:1 (xem quyết định Q-P0).
3. **H1b nối `screen_tracks` với hình render**, nhưng chưa nối kênh rig (`channels`) với `screen_tracks`: bản khai rig giả mà track thật vẫn lọt; cần phép chiếu rig → màn hình (v2). Điểm bị che phải khai `null`; tỷ lệ null nằm trong báo cáo. Luồng quang học yếu trên mảng màu phẳng (đầu nhân vật M0: 91,1%, sát ngưỡng 90%).
4. **C3 đo độ dài 2D**: bộ phận chĩa về phía máy quay bị ngắn đi (phối cảnh) và sẽ trượt oan; v1 chưa có miễn trừ theo góc nhìn. Ở đầu cao ~57 px, nhiễu đo (U 2–2,7%) ăn gần hết biên 3% nên hầu như không chứng minh được: phải render mặt nạ ở `scale` 2–4 (quyết định Q-C3).
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
