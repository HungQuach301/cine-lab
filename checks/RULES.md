# CINE LAB — BỘ LUẬT L1 v0 (phiên K)

Căn cứ: `docs/cine-lab/CINE-LAB-KHUNG-CHAT-LUONG.md` mục 1 và 4; `docs/cine-lab/CINE-LAB-BAI-HOC-BRIEF-D.md`.
Nguyên tắc: đo từ file đã render; mỗi luật có test tự chứng minh; ngưỡng "nội bộ" là đề xuất v0, hiệu chuẩn sau bài thử.
Định nghĩa máy đọc nằm trong `cinecheck/registry.py`; báo cáo mỗi lần chạy chép lại định nghĩa và ngưỡng.

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

## Giới hạn đã biết của v0 (nêu thẳng để chủ dự án quyết)

1. **J1 dễ dãi hơn tai người.** Ở mẫu TRƯỢT, tiếng ồn lớn hơn lời 9 dB suốt 2,5 giây mà ASR vẫn đoán đúng 17/18 từ nhờ mô hình ngôn ngữ; chỉ trượt 1 từ ("ships" → "shifts"). Nghĩa là J1 bắt được lời mất hẳn, nhưng có thể cho qua lời bị nhạc lấn mà người nghe thật không rõ. Đề xuất bổ sung (quyết định Q2 trong báo cáo).
2. **P1/G4 tin vào matte chữ do render xuất.** Máy đối chiếu matte với khung hình nên matte giả lệch vị trí hay sai màu sẽ trượt; nhưng nếu phiên xưởng **không xuất** matte cho một dòng chữ có trong hình thì v0 không thấy. Cần máy dò chữ độc lập (Q3).
3. **H1 tin vào dữ liệu chuyển động bake.** Chưa đối chiếu với hình render (luồng quang học). Nhãn lớp kênh (`mechanical`, `character_root`) là khai báo; báo cáo liệt kê để người duyệt soi.
4. **O3 tin vào danh sách tài sản và `scene_files`.** SHA tính lại từ đĩa, nhưng việc file cảnh thật sự nạp gì chưa được đọc trực tiếp (bpy trong môi trường hiện FAIL ở `verify.sh`).
5. **G3** đo "không banding", chưa đo phần "grain cố định" trong mục G3 của khung.
6. **M3** chỉ đo stereo. Bản 5.1 (nếu làm DCP) cần luật riêng.
7. Ngưỡng "nội bộ" (N2 0,5%, N3 12/45 Mbps, G3 0,2%, M3 −3/−6 dB, J1 WER 5%) chưa hiệu chuẩn với người chấm (nguyên tắc N4 của BAI-HOC).
