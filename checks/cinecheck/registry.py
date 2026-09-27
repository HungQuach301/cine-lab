"""Sổ đăng ký luật: mã, mục trong khung, định nghĩa đo, ngưỡng, cấp.

Nguồn: docs/cine-lab/CINE-LAB-KHUNG-CHAT-LUONG.md mục 4. Ngưỡng ghi "nội bộ" là đề xuất v0,
hiệu chuẩn sau bài thử. Mọi số đo lấy từ file đã render.
"""

CHAN, CHINH, THAM_KHAO = "Chặn", "Chính", "Tham khảo"

RULES = {
    "N1": dict(
        section="4.N — Kỹ thuật file",
        title="24 fps CFR; không rơi hay lặp khung theo PTS",
        level=CHAN,
        measure="ffprobe đọc PTS từng gói hình của luồng video đầu tiên, sắp xếp theo PTS, "
                "tính hiệu PTS kề nhau. Đồng thời đọc r_frame_rate và avg_frame_rate.",
        threshold="r_frame_rate = avg_frame_rate = 24/1; 0 bước PTS lệch khỏi 1/24 s quá 0,5 ms; "
                  "0 PTS trùng; 0 khoảng hở.",
        profiles=("shot", "youtube", "archive"),
    ),
    "N2": dict(
        section="4.N — Kỹ thuật file",
        title="BT.709 đủ 3 trường; dải limited — đo cả nhãn lẫn giá trị điểm ảnh",
        level=CHAN,
        measure="Nhãn: color_primaries, color_transfer, color_space phải là bt709; color_range là tv. "
                "Điểm ảnh: lấy mẫu luma (2 khung/giây, tối đa 240 khung), tính tỷ lệ mẫu nằm ngoài "
                "dải limited (8 bit: <16 hoặc >235; 10 bit: <64 hoặc >940).",
        threshold="Đủ 4 nhãn đúng; tỷ lệ luma ngoài dải ≤ 0,5% (nội bộ).",
        profiles=("shot", "youtube", "archive"),
    ),
    "N3": dict(
        section="4.N — Kỹ thuật file",
        title="Codec và bitrate đúng loại master; khung 16:9, SAR 1:1",
        level=CHAN,
        measure="ffprobe đọc codec, profile, pix_fmt, kích thước, SAR; bitrate hình tính từ tổng "
                "kích thước gói / thời lượng (không dùng số khai trong header). Bitrate âm đo từ gói "
                "chỉ báo tham khảo: AAC dùng ít bit cho đoạn âm đơn giản nên không phản ánh chất lượng.",
        threshold="youtube: H.264 High hoặc HEVC Main/Main10, yuv420p/yuv420p10le, 1920×1080 hoặc "
                  "3840×2160, bitrate hình đo ≥ 12 Mbps (1080p) / ≥ 45 Mbps (2160p) (nội bộ, trên mức "
                  "khuyến nghị YouTube 8/35–45 Mbps); âm AAC-LC 48 kHz 2 kênh (bitrate âm chỉ báo tham khảo). "
                  "archive: ProRes 422 HQ/4444/4444 XQ, DNxHR HQ/HQX/444 hoặc FFV1; âm PCM ≥ 24 bit "
                  "48 kHz; ≥ 1920×1080. Cả hai: tỷ lệ 16:9, SAR 1:1.",
        profiles=("youtube", "archive"),
    ),
    "P1": dict(
        section="4.P — Chữ, tiêu đề, phụ đề",
        title="Không chữ đè chữ, tính theo điểm ảnh nét chữ",
        level=CHAN,
        measure="Mỗi phần tử chữ có matte RGBA xuất từ render (checks/RUN.md mục 3). Nét chữ = "
                "alpha ≥ 0,5, nới 1 px. Ở mọi khung có ≥ 2 phần tử, đếm điểm ảnh thuộc ≥ 2 nét. "
                "Chống khai man: ở lõi nét (alpha ≥ 0,98, co 1 px) màu matte phải khớp màu khung "
                "render (lệch kênh ≤ 24/255) ở ≥ 90% điểm ảnh.",
        threshold="0 điểm ảnh va chạm; độ khớp matte ≥ 90%.",
        profiles=("shot", "youtube", "archive"),
    ),
    "G4": dict(
        section="4.G — Ánh sáng và màu",
        title="Chữ tương phản ≥ 4,5:1 (WCAG AA), đo điểm ảnh",
        level=CHAN,
        measure="Với mỗi phần tử chữ, lấy tối đa 24 khung rải đều. Độ chói tương đối (WCAG, sRGB) "
                "của chữ = trung vị trên lõi nét trong khung render. Nền = vành 2–6 px quanh nét "
                "(trừ nét của mọi phần tử). Tính tỷ lệ tương phản từng điểm nền với chữ; lấy phân "
                "vị 10 (90% điểm nền đạt). Lấy giá trị nhỏ nhất qua các khung.",
        threshold="Phân vị 10 của tỷ lệ tương phản ≥ 4,5 ở mọi phần tử, mọi khung lấy mẫu.",
        profiles=("shot", "youtube", "archive"),
    ),
    "G3": dict(
        section="4.G — Ánh sáng và màu",
        title="Không banding trên gradient",
        level=CHAN,
        measure="Luma ở độ sâu gốc, 2 khung/giây (tối đa 240 khung). Điểm banding = điểm nằm trong "
                "mảng phẳng tuyệt đối 5×5, và trong cửa sổ 95×95 quanh nó: (a) có ≥ 3 mức mảng phẳng "
                "khác nhau (bậc thang), (b) mọi bước nhảy giữa điểm kề ≤ 2 mã (không có cạnh cứng), "
                "(c) biên độ luma ≤ 24 mã. Diện tích banding = tỷ lệ điểm banding trên khung.",
        threshold="Diện tích banding ≤ 0,2% khung ở mọi khung lấy mẫu (nội bộ).",
        profiles=("shot", "youtube", "archive"),
    ),
    "M1": dict(
        section="4.M — Mix và master",
        title="Master YouTube: −14 LUFS ±1; true peak ≤ −1 dBTP",
        level=CHAN,
        measure="ffmpeg ebur128 (ITU-R BS.1770-4, cổng tuyệt đối −70 và tương đối −10 LU), "
                "peak=true (lấy mẫu vượt) trên luồng âm đầu tiên của file.",
        threshold="Integrated trong [−15, −13] LUFS; true peak ≤ −1,0 dBTP.",
        profiles=("youtube",),
    ),
    "M3": dict(
        section="4.M — Mix và master",
        title="Tương quan pha và tương thích mono",
        level=CHAN,
        measure="Giải mã stereo 48 kHz float. Cửa sổ 400 ms không chồng; cửa sổ hoạt động khi RMS "
                "kênh lớn hơn ≥ −50 dBFS. (1) Hệ số tương quan L/R từng cửa sổ. (2) Mất mát khi "
                "gộp mono = độ ồn BS.1770 của (L+R)/2 phát cả 2 kênh trừ độ ồn stereo. (3) Mất "
                "công suất mono/stereo trên cửa sổ trượt 3 s. Phần 'lời rõ trên nhạc' của M3 "
                "được đo bởi J1 (ASR trên bản gộp mono của mix cuối).",
        threshold="≤ 1% cửa sổ hoạt động có tương quan < −0,3; mất mát mono tích phân ≥ −3,0 dB; "
                  "cửa sổ 3 s tệ nhất ≥ −6,0 dB (nội bộ).",
        profiles=("shot", "youtube", "archive"),
    ),
    "J1": dict(
        section="4.J — Giọng",
        title="Mọi từ trong kịch bản nghe rõ trên bản mix cuối",
        level=CHAN,
        measure="faster-whisper small.en (revision ghim, int8, beam 5, nhiệt độ 0, không mồi bằng "
                "kịch bản, không nối ngữ cảnh) chạy trên luồng âm của file, gộp mono 16 kHz. Chuẩn "
                "hoá: chữ thường, bỏ dấu câu và dấu nháy, số → chữ. Căn Levenshtein kịch bản với "
                "bản nghe. Từ bắt buộc = toàn bộ từ trong kịch bản thoại.",
        threshold="100% từ bắt buộc được nghe đúng; WER ≤ 5% (nội bộ).",
        profiles=("shot", "youtube", "archive"),
    ),
    "H1": dict(
        section="4.H — Hoạt hình",
        title="Không chuyển động tuyến tính ở bộ phận nhân vật",
        level=CHAN,
        measure="Dữ liệu chuyển động bake theo từng khung xuất từ phần mềm dựng (không phải khoá "
                "khai báo). Với mỗi kênh lớp 'character_part': tốc độ = chuẩn hiệu giá trị giữa 2 "
                "khung kề; đang chuyển động khi tốc độ > 2% tốc độ lớn nhất của kênh. Đoạn tuyến tính = "
                "chuỗi bước liên tiếp có mọi tốc độ trong ±3% trung bình chuỗi, và (a) dài ≥ 8 bước "
                "và bắt đầu ngay sau hoặc kết thúc ngay trước một lần đứng yên (khởi/dừng không "
                "easing), hoặc (b) dài ≥ 24 bước ở bất kỳ đâu.",
        threshold="0 đoạn tuyến tính ở kênh bộ phận nhân vật. Kênh 'mechanical' được miễn nhưng "
                  "phải có lý do và được liệt kê trong báo cáo.",
        profiles=("shot", "youtube", "archive"),
    ),
    "O3": dict(
        section="4.O — Liên tục và nhất quán",
        title="Mọi tài sản lấy từ thư viện có SHA",
        level=CHAN,
        measure="Tính lại SHA-256 từ đĩa cho mọi tài sản trong danh sách dùng của shot và so với "
                "thư viện assets/LIBRARY.json. Quét thư mục làm việc của shot: mọi file media "
                "(mô hình, ảnh, âm, font) không nằm trong thư viện là tài sản ngoài thư viện "
                "(trừ thư mục render/, out/, cache/, frames/).",
        threshold="0 tài sản lệch SHA; 0 tài sản không có trong thư viện; 0 file media lạ trong "
                  "thư mục làm việc.",
        profiles=("shot", "youtube", "archive"),
    ),
}

ORDER = ["N1", "N2", "N3", "P1", "G4", "G3", "M1", "M3", "J1", "H1", "O3"]
