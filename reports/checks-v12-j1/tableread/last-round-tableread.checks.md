# Báo cáo kiểm L1 — last-round-tableread.mp4

- Kết luận: **ĐẠT**
- Profile: `shot` · Công cụ: cinecheck 1.2.0 · Thời điểm (UTC): 2026-09-27T04:05:34Z
- LOCK: khớp (`0196187b7af0523e9b2bc23ce68d5d95addd098f42a18de42b8afb8d4e2e76ff`)
- Đếm: ĐẠT 1

| Mã | Luật | Cấp | Kết quả | Số đo chính |
|---|---|---|---|---|
| J1 | Mọi từ trong kịch bản nghe rõ trên bản mix cuối | Chặn | **ĐẠT** | từ bắt buộc nghe đúng = 100 % (ngưỡng >= 100); WER = 0 % (ngưỡng <= 5) |

## Chỉ số nằm trong ±5% quanh ngưỡng
- Không có.

## Chi tiết từng luật

### J1 — Mọi từ trong kịch bản nghe rõ trên bản mix cuối (4.J — Giọng, cấp Chặn): ĐẠT
- Định nghĩa đo: faster-whisper small.en (revision ghim, int8, beam 5, nhiệt độ 0, không mồi bằng kịch bản, không nối ngữ cảnh, có mốc từng chữ) chạy trên luồng âm của file, gộp mono 16 kHz. Chuẩn hoá: chữ thường, bỏ dấu câu, dấu nháy và gạch nối, số → chữ; v1.2: từ ghép/tách theo bảng COMPOUND (goodnight = good night…, RULES.md) cho cả kịch bản và bản nghe. Từ bắt buộc = toàn bộ từ trong kịch bản thoại. v1.2: (1) lượt ASR toàn file, căn Levenshtein với kịch bản để lấy mốc từng câu (câu = dòng kịch bản); cửa sổ câu = mốc chữ đầu/cuối nới tối đa 2 s, không vượt điểm giữa khoảng lặng với câu kề; cửa sổ > 28 s tách tại khoảng lặng lớn nhất. (2) ASR riêng từng cửa sổ câu, căn với câu đó. (3) Chữ ASR nằm hoàn toàn trong im lặng số (mọi khung 50 ms chạm chữ có RMS < −60 dBFS) bị bỏ, liệt kê trong báo cáo. (4) Chữ lượt toàn file nằm ngoài mọi cửa sổ câu (không trong im lặng số) tính là chèn.
- Ngưỡng: 100% từ bắt buộc được nghe đúng; WER ≤ 5% (nội bộ).
- Ghi chú: 5 câu thoại, ASR từng câu (cửa sổ theo căn kịch bản với lượt toàn file). Chữ ASR bị bỏ vì nằm hoàn toàn trong im lặng số (RMS 50 ms < -60 dBFS): 1: 'you' 56.8–58.2 s.
- Ghi chú: Chữ lượt toàn file nằm ngoài mọi câu (tính chèn): 0.
- Ghi chú: Chuẩn hoá ghép/tách theo bảng COMPOUND (RULES.md), áp cho cả kịch bản và bản nghe.
- Bằng chứng: `{"so_tu_kich_ban": 40, "thay": 0, "mat": 0, "chen": 0, "theo_cau": [{"cau": 1, "loi": "Evening, old street.", "cua_so": [7.4, 13.86], "neo": [9.4, 11.86], "nghe": "evening old street", "thay": 0, "mat": 0, "chen": 0, "tu_truot": []}, {"cau": 2, "loi": "Not yet... not yet.", "cua_so": [68.96, 76.5], "neo": [70.96, 74.5], "nghe": "not yet not yet", "thay": 0, "mat": 0, "chen": 0, "tu_truot": []}, {"cau": 3, "loi": "Go on, then.", "cua_so": [101.0, 106.8], "neo": [103.0, 104.8], "nghe": "go on then", "thay": 0, "mat": 0, "chen": 0, "tu_truot": []}, {"cau": 4, "loi": "That's the last one, then. Goodnight, old street. You'll be brighter now. Just... keep a little dark for the ones who ne", "cua_so": [119.76, 137.53], "neo": [121.76, 136.14], "nghe": "thats the last one then good night old street youll be brighter now just keep a little dark for the ones who need it", "thay": 0, "mat": 0, "chen": 0, "tu_truot": []}, {"cau": 5, "loi": "Warm your hands first. Three counts.", "cua_so": [137.53, 144.34], "neo": [138.92, 142.34], "nghe": "warm your hands first three counts", "thay": 0, "mat": 0, "chen": 0, "tu_truot": []}], "chu_bo_vi_im_lang_so": [{"bat_dau": 56.8, "ket_thuc": 58.2, "chu": "you"}], "vung_im_lang_so": [[0.0, 10.0], [12.2, 72.0], [74.9, 104.0], [106.3, 122.0], [136.1, 139.5], [142.7, 165.0]], "ban_nghe_toan_file": "Evening, Old Street  you  Not yet, not yet.  Go on then.  That's the last one then. Good night, old street. You'll be brighter now. Just keep  a little dark f`
