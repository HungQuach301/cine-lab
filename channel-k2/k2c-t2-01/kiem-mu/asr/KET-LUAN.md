# ASR hai cách nghe — K2C-T2-01, lời KHOÁ v3.3 (15/10/2026)
Giọng: ElevenLabs Eric `cjVigY5qzO86Huf0OWal`, `eleven_multilingual_v2` (stability 0,5, similarity 0,75), chuỗi gửi = `loi-khoa.txt` (SHA 9bf318c2…, kiểm trong `make_spec.py`).
Đoạn 05 (2 361 ký tự) thu thành 2 phần (1 173 + 1 188 ký tự, tách ở ranh giới câu, gửi kèm previous_text/next_text) vì proxy cắt yêu cầu sau ~30 s (`scripts/k2/prep.py` tts_k2).
Cách A: faster-whisper small.en CÓ hotwords tên riêng (như `scripts/ll/asr.py`). Cách B: medium.en KHÔNG hotwords. Toàn văn: `<đoạn>-A.txt`, `<đoạn>-B.txt`; số liệu: `asr2.json`.

| Đoạn | Công cụ báo thiếu | Nghe thật (trích toàn văn) | Kết luận |
|---|---|---|---|
| 00 | A: 0.04 | A "zero point oh four percent" · B "0.04%" | đọc đúng (bộ phân tích không hiểu "oh") |
| 01 | A: 747 · B: 15.5, 22 | A "seven forty seven ships", "a hundred and twenty two days", "four days and fifteen and a half hours" · B "747 ships", "122 days", "15 and a half hours" | đọc đúng |
| 02, 03, 06 | — | — | đúng |
| 04 | A, B: 500 · B: 7 | A "a five hundred one banknote" · B "a 501 banknote" (won ≡ one, đồng âm) · B "$107" | đọc đúng "five hundred won" |
| 05 | B: 5 000 000 000 | A "five billion dollars" · B "$5 billion" | đọc đúng |
Tên riêng: cả hai cách nghe đều có Kaiser, Owens, Carver, Wesley Jones, Mike Lee, McClintock, Chung Ju-yung, Livanos, Park Chung Hee, Munseob Lee, Hanwha, JoongAng (B: "Jungang"), Military Times. "Peary": A viết "perry", B viết "Peary" — không xác định được âm từ chữ; giữ (không thu lại).
**Không thu lại đoạn nào.** Ký tự ElevenLabs gửi phiên G2: 9 728 (bộ đếm tài khoản 105 498 → 113 556, gồm ~214 ký tự của lần kết nối bị ngắt ở đoạn 03).
