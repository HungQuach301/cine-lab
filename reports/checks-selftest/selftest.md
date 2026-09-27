# Test tự chứng minh — luật L1 (phiên K)

| Mã | Mẫu | Kỳ vọng | Kết quả | Khớp | Số đo |
|---|---|---|---|---|---|
| N1 | 24 fps CFR (testsrc2) | PASS | PASS | ✔ | r_frame_rate=24.0 (== 24.0); avg_frame_rate=24.0 (== 24.0); bước PTS lệch khỏi 1/24 s > 0,5 ms=0 (<= 0); PTS trùng (lặp khung)=0 (<= 0); khoảng hở PTS (rơi khung)=0 (<= 0) |
| N1 | rơi khung 10 (PTS hở) | FAIL | FAIL | ✔ | r_frame_rate=24.0 (== 24.0); avg_frame_rate=23.5 (== 24.0); bước PTS lệch khỏi 1/24 s > 0,5 ms=1 (<= 0); PTS trùng (lặp khung)=0 (<= 0); khoảng hở PTS (rơi khung)=1 (<= 0) |
| N1 | 25 fps | FAIL | FAIL | ✔ | r_frame_rate=25.0 (== 24.0); avg_frame_rate=25.0 (== 24.0); bước PTS lệch khỏi 1/24 s > 0,5 ms=49 (<= 0); PTS trùng (lặp khung)=0 (<= 0); khoảng hở PTS (rơi khung)=0 (<= 0) |
| N2 | BT.709 đủ nhãn, dải limited | PASS | PASS | ✔ | color_primaries=bt709 (== bt709); color_transfer=bt709 (== bt709); color_space=bt709 (== bt709); color_range=tv (== tv); luma ngoài dải limited=0.0 (<= 0.5) |
| N2 | không có nhãn màu | FAIL | FAIL | ✔ | color_primaries=(không có) (== bt709); color_transfer=(không có) (== bt709); color_space=(không có) (== bt709); color_range=(không có) (== tv); luma ngoài dải limited=0.0 (<= 0.5) |
| N2 | nhãn tv nhưng luma 0/255 (full range) | FAIL | FAIL | ✔ | color_primaries=bt709 (== bt709); color_transfer=bt709 (== bt709); color_space=bt709 (== bt709); color_range=tv (== tv); luma ngoài dải limited=100.0 (<= 0.5) |
| N3 | YouTube: H.264 High 14 Mbps, AAC 384k 48 kHz | PASS | PASS | ✔ | tỷ lệ khung=1.7778 (== 1.7778); SAR=1:1 (== 1:1); codec/profile hình=h264/High (== h264/High | hevc/Main(10)); pix_fmt=yuv420p (== yuv420p | yuv420p10le); kích thước=1920x1080 (== 1920x1080 | 3840x2160); bitrate hình đo từ gói=14.0154 (>= 12.0); codec âm=aac/LC (== aac/LC); tần số lấy mẫu âm=48000 (== 48000); số kênh âm=2 (== 2) |
| N3 | YouTube: 3 Mbps, AAC 128k 44,1 kHz | FAIL | FAIL | ✔ | tỷ lệ khung=1.7778 (== 1.7778); SAR=1:1 (== 1:1); codec/profile hình=h264/High (== h264/High | hevc/Main(10)); pix_fmt=yuv420p (== yuv420p | yuv420p10le); kích thước=1920x1080 (== 1920x1080 | 3840x2160); bitrate hình đo từ gói=3.0424 (>= 12.0); codec âm=aac/LC (== aac/LC); tần số lấy mẫu âm=44100 (== 48000); số kênh âm=2 (== 2) |
| N3 | Lưu trữ: ProRes 422 HQ + PCM 24 bit | PASS | PASS | ✔ | tỷ lệ khung=1.7778 (== 1.7778); SAR=1:1 (== 1:1); codec/profile hình=prores/HQ (== prores HQ/4444/4444XQ | dnxhr HQ/HQX/444 | ffv1); chiều cao=1080 (>= 1080); codec âm=pcm_s24le (== pcm_*); độ sâu bit âm=24 (>= 24); tần số lấy mẫu âm=48000 (>= 48000) |
| N3 | Lưu trữ: H.264 + AAC | FAIL | FAIL | ✔ | tỷ lệ khung=1.7778 (== 1.7778); SAR=1:1 (== 1:1); codec/profile hình=h264/High (== prores HQ/4444/4444XQ | dnxhr HQ/HQX/444 | ffv1); chiều cao=1080 (>= 1080); codec âm=aac (== pcm_*); độ sâu bit âm=0 (>= 24); tần số lấy mẫu âm=48000 (>= 48000) |
| P1 | tiêu đề + phụ đề tách rời | PASS | PASS | ✔ | điểm ảnh nét chữ va chạm=0 (<= 0); độ khớp matte–render thấp nhất=100.0 (>= 90.0) |
| P1 | phụ đề đè lên tiêu đề | FAIL | FAIL | ✔ | điểm ảnh nét chữ va chạm=63828 (<= 0); độ khớp matte–render thấp nhất=100.0 (>= 90.0) |
| P1 | matte khai lệch vị trí so với render | FAIL | FAIL | ✔ | điểm ảnh nét chữ va chạm=0 (<= 0); độ khớp matte–render thấp nhất=0.0 (>= 90.0) |
| G4 | chữ sáng trên nền tối (~14:1) | PASS | PASS | ✔ | tương phản chữ/nền (P10) thấp nhất=14.8213 (>= 4.5); độ khớp matte–render thấp nhất=100.0 (>= 90.0) |
| G4 | chữ xám trên nền xám (~1,4:1) | FAIL | FAIL | ✔ | tương phản chữ/nền (P10) thấp nhất=1.514 (>= 4.5); độ khớp matte–render thấp nhất=100.0 (>= 90.0) |
| G3 | gradient 8 bit không dither (bậc thang) | FAIL | FAIL | ✔ | diện tích banding lớn nhất=45.2083 (<= 0.2) |
| G3 | cùng gradient có dither/grain | PASS | PASS | ✔ | diện tích banding lớn nhất=0.0 (<= 0.2) |
| G3 | mảng phẳng phong cách hoá, biên cứng | PASS | PASS | ✔ | diện tích banding lớn nhất=0.0 (<= 0.2) |
| M1 | −14 LUFS, đỉnh giới hạn −1,6 dBFS | PASS | PASS | ✔ | integrated loudness=-14.0 (in (-15.0, -13.0)); true peak=-3.8 (<= -1.0) |
| M1 | −8 LUFS, cắt đỉnh tại 0 dBFS | FAIL | FAIL | ✔ | integrated loudness=-8.2 (in (-15.0, -13.0)); true peak=-0.4 (<= -1.0) |
| M3 | stereo tương quan cao | PASS | PASS | ✔ | cửa sổ tương quan < −0,3=0.0 (<= 1.0); mất mát mono tích phân (BS.1770)=-0.0623 (>= -3.0); mất mát mono cửa sổ 3 s tệ nhất=-0.0406 (>= -6.0) |
| M3 | kênh phải đảo pha | FAIL | FAIL | ✔ | cửa sổ tương quan < −0,3=100.0 (<= 1.0); mất mát mono tích phân (BS.1770)=-18.4637 (>= -3.0); mất mát mono cửa sổ 3 s tệ nhất=-22.0417 (>= -6.0) |
| J1 | lời + nhạc nền thấp 22 dB | PASS | PASS | ✔ | từ bắt buộc nghe đúng=100.0 (>= 100.0); WER=0.0 (<= 5.0) |
| J1 | nhạc/ồn lấn át lời 1,7–4,2 s | FAIL | FAIL | ✔ | từ bắt buộc nghe đúng=94.4444 (>= 100.0); WER=5.5556 (<= 5.0) |
| H1 | easing, cung, quay chậm 4 s; kim đồng hồ 'mechanical' | PASS | PASS | ✔ | đoạn tuyến tính ở bộ phận nhân vật=0 (<= 0); kênh 'mechanical' thiếu lý do=0 (<= 0); kênh có lớp không hợp lệ=0 (<= 0) |
| H1 | cánh tay nội suy tuyến tính 20 khung | FAIL | FAIL | ✔ | đoạn tuyến tính ở bộ phận nhân vật=1 (<= 0); kênh 'mechanical' thiếu lý do=0 (<= 0); kênh có lớp không hợp lệ=0 (<= 0) |
| O3 | tài sản khớp SHA thư viện | PASS | PASS | ✔ | tài sản không có trong thư viện=0 (<= 0); tài sản lệch SHA so với thư viện=0 (<= 0); tài sản thư viện thiếu file trên đĩa=0 (<= 0); file media lạ trong thư mục làm việc=0 (<= 0) |
| O3 | tài sản bị sửa sau khoá + vẽ lại ngoài thư viện | FAIL | FAIL | ✔ | tài sản không có trong thư viện=1 (<= 0); tài sản lệch SHA so với thư viện=1 (<= 0); tài sản thư viện thiếu file trên đĩa=0 (<= 0); file media lạ trong thư mục làm việc=1 (<= 0) |

## Luật được chứng minh (có mẫu TRƯỢT và mẫu SẠCH, mọi ca khớp)

- N1: ĐẠT
- N2: ĐẠT
- N3: ĐẠT
- P1: ĐẠT
- G4: ĐẠT
- G3: ĐẠT
- M1: ĐẠT
- M3: ĐẠT
- J1: ĐẠT
- H1: ĐẠT
- O3: ĐẠT

## Chạy đầu–cuối bằng lệnh duy nhất (run.py, profile youtube)

- Mẫu sạch: ĐẠT (exit 0); LOCK khớp: True
- Mẫu bẩn (rơi khung, thiếu nhãn màu; --only N1,N2): exit 1 (kỳ vọng 1 khi LOCK khớp, 3 khi chưa khoá)
- Khớp kỳ vọng: ✔
- Trạng thái: {'N1': 'PASS', 'N2': 'PASS', 'N3': 'PASS', 'P1': 'PASS', 'G4': 'PASS', 'G3': 'PASS', 'M1': 'PASS', 'M3': 'PASS', 'J1': 'PASS', 'H1': 'PASS', 'O3': 'PASS'}
- Sát ngưỡng ±5%: [{'code': 'M1', 'metric': 'integrated loudness', 'value': -14.4, 'threshold': [-15.0, -13.0]}]
