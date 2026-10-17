# THƯỚC CHẤM ÂM THANH — phần máy đo và phần tai người

> Phiên Âm thanh soạn 15/10/2026 (Mốc C). **Đề xuất cho phiên K** (chỉ K biến thành luật trong `checks/`); ngưỡng hiệu chuẩn trên số đo thật của 3 tập đã phát hành (Steel, T1, LL ep08 — `reports/AM-THANH-BAO-CAO.md` §2). Công cụ đo: `scripts/audio/measure.py` (một tệp) và báo cáo JSON của `scripts/audio/master.py` / `compose.py` (mỗi lần dựng).
> Kinh thánh §4: "khoảng −14 đến −15 LUFS, đỉnh ≤ −1 dBFS (chờ K đưa vào luật)". Thước này dùng **dBTP** (đỉnh thật, nâng mẫu ×4) — chặt hơn dBFS mẫu, và là cách YouTube/EBU R128 đo.

## 1. Phần MÁY đo được
Đo trên **bản phát hành thật** (master mp4 sau AAC, giải mã lại), trừ A4/A9 đo trên stem.

| # | Chỉ số | Cách đo | Ngưỡng đề xuất | Hiện trạng 3 tập (Steel · T1 · LL08) |
|---|---|---|---|---|
| A1 | Loudness tích hợp | ffmpeg `ebur128` (BS.1770-4, cổng −70/−10) trên luồng âm master | **−15,0 ≤ I ≤ −14,0 LUFS** (dung sai đo ±0,2) | −14,0 · −14,0 · −14,0 — **nằm ĐÚNG mép trên** (±5 % quanh ngưỡng) |
| A2 | Đỉnh thật | `ebur128=peak=true` trên luồng đã giải mã **sau AAC** | **≤ −1,0 dBTP** | −1,6 · −1,6 · −1,6 |
| A3 | Biên độ loudness (LRA) | `ebur128` | cảnh báo khi < 2,0 hoặc > 8,0 LU (không chặn) | 2,3 · 2,1 · 2,8 |
| A4 | Lời trên nhạc (SMR) | stem lời vs phần còn lại; cửa sổ 3 s bước 1 s nằm trọn trong khoảng lời; lọc K | **p10 ≥ 15 dB và min ≥ 12 dB** | p10 18,9 · 18,6 · 17,3; min 16,4 · 14,0 · 13,8 |
| A5 | Khoảng lặng bất thường | loudness tức thời 400 ms < −50 LUFS kéo dài ≥ 1,0 s, bỏ 2 s đầu/cuối | **0 đoạn** | 0 · 0 · 0 |
| A6 | Tỉ lệ lặng | % thời gian tức thời < −50 LUFS | báo cáo (không chặn) | 0,0 · 0,0 · 0,15 % |
| A7 | Chạm trần (cắt) | chuỗi ≥ 3 mẫu liền \|x\| ≥ 0,999 trên tín hiệu giải mã | **0** | 0 · 0 · 0 |
| A8 | Chồng lời | hai đoạn lời phát chồng nhau (từ timeline) | **0** | 0 · 0 · 0 |
| A9 | Đọc đúng (ASR) | `scripts/ll/asr.py` (beam 5) **và** greedy small.en (BAI-HOC-LL #86): mọi số (theo giá trị) + tên riêng của đoạn có trong bản nghe | **100 % đoạn**; câu đánh dấu mơ hồ ASR (vd "won"/"one") chấm tai | (đã chạy ở G2 từng tập) |
| A10 | Quãng không lời | khoảng giữa hai khoảng lời (gộp nghỉ < 0,55 s) | báo khi > 8 s mà không khai "khoảnh khắc nhạc" | dài nhất 1,8 · 1,8 · 4,2 s |
| A11 | Giao nhạc | `compose.py` nhật ký `nhac[]`: điểm giao lệch ranh giới chương; lặp nhạc | \|lệch\| ≤ 1 ô nhịp (≤ 3,4 s ở 72 bpm); **không lặp** (Q28 hiện hành) | — (chuỗi mới) |
| A12 | Loudnorm tuyến tính | `master.py` → `loudness[-1].loudnorm.normalization_type` | **linear** (không nén động ẩn) | — (chuỗi mới) |
| A13 | Đồng bộ tiếng | trễ của luồng âm so với stem lời (tương quan chéo) | ≤ 5 ms | mix.py cũ: **1,0 ms** (độ trễ nhìn trước của `alimiter`) — dưới 1 khung, ghi nhận |

**Cách K có số liệu cho A4 khi chỉ có master:** dựng lại stem bằng `scripts/ll/mix.py <timeline> <x.wav> --stems <dir>` (prep offline như `golden.py`, không gọi ElevenLabs). Đã kiểm 15/10: bản dựng lại khớp master T1 với phần dư −38…−43 dB, Steel −28…−42 dB. Phép "chiếu" lời gốc lên master **không dùng được** (lời qua nén phi tuyến, ra SMR ≈ 3 dB — sai).

**Đề xuất chưa hiệu chuẩn (chỉ báo, chưa chặn):**
- A14 SFX lấn lời: trong 0,5 s quanh mỗi SFX, loudness tức thời của stem SFX ≤ lời − 6 LU.
- A15 Mật độ SFX gắn hình: ≥ 1 biến cố/phút ở chương có bản đồ (Kinh thánh: âm thanh nghề, BAI-HOC-LL "ít âm thanh nghề").

## 2. Phần TAI NGƯỜI — việc của chủ dự án
Máy **không** chấm được những điều sau; ghi điểm vào `AUTHORSHIP.md` khi duyệt G2 (một dòng mỗi mục):
1. **Chất giọng**: ấm, thành thật, hợp phim tài liệu tiếng Anh; nhịp nhấn câu then chốt (mẫu so sánh: `reports/AM-THANH-BAO-CAO.md` §6).
2. **Đọc tên bản ngữ** (tên Hàn, Hy Lạp…): ASR chỉ xác nhận "nghe ra chữ", không xác nhận "đọc đúng âm".
3. **Hợp nhạc**: bài và cường độ có đúng cảm xúc từng chương; chỗ giao bài có "đúng nhịp" với tai (máy chỉ bảo đảm vạch ô nhịp ước).
4. **SFX**: gu, độ to tương đối, có thừa/thiếu so với hình; whoosh/shimmer tổng hợp có "rẻ" không.
5. **Cân bằng tổng**: nhạc dưới lời có bị chìm quá (mất cảm xúc) hay nổi quá (mỏi tai) — SMR chỉ chặn đáy.
6. **A/B** chuỗi mới vs cũ (đoạn 60 s, §8 báo cáo).

## 3. Ghi chú cho K khi viết luật
- Đo A1/A2 trên **luồng âm của master.mp4** (AAC), không trên `mix.wav`: AAC làm đỉnh vọt tới ≈ 1,4 dB ở quá độ nhọn (BAI-HOC-LL #69). `master.py` đã kiểm sau AAC và hạ trần limiter khi cần.
- A1 mép trên: cả 3 tập đều −14,0 LUFS đúng mép ngưỡng −14,0 → nên giữ dung sai đo ±0,2 để không trượt vì làm tròn.
- Bản xem 3 phần 720p của LL (`alimiter 0,75`, −1,2 dB) và Short (AAC 192k) đo theo cùng thước A1/A2 trên tệp phát hành của chúng.
