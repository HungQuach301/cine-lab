# Báo cáo kiểm L1 — last-round-tableread-d2.mp4

- Kết luận: **ĐẠT**
- Profile: `shot` · Công cụ: cinecheck 1.2.0 · Thời điểm (UTC): 2026-09-27T04:05:08Z
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
- Ghi chú: 4 câu thoại, ASR từng câu (cửa sổ theo căn kịch bản với lượt toàn file). Chữ ASR bị bỏ vì nằm hoàn toàn trong im lặng số (RMS 50 ms < -60 dBFS): 2: 'Great.' 38.82–40.22 s; 'You' 137.68–139.08 s.
- Ghi chú: Chữ lượt toàn file nằm ngoài mọi câu (tính chèn): 0.
- Ghi chú: Chuẩn hoá ghép/tách theo bảng COMPOUND (RULES.md), áp cho cả kịch bản và bản nghe.
- Bằng chứng: `{"so_tu_kich_ban": 34, "thay": 0, "mat": 0, "chen": 0, "theo_cau": [{"cau": 1, "loi": "Evening, old street.", "cua_so": [9.38, 15.86], "neo": [11.38, 13.86], "nghe": "evening old street", "thay": 0, "mat": 0, "chen": 0, "tu_truot": []}, {"cau": 2, "loi": "Not yet... not yet.", "cua_so": [57.0, 64.52], "neo": [59.0, 62.52], "nghe": "not yet not yet", "thay": 0, "mat": 0, "chen": 0, "tu_truot": []}, {"cau": 3, "loi": "Go on, then.", "cua_so": [85.3, 90.82], "neo": [87.3, 88.82], "nghe": "go on then", "thay": 0, "mat": 0, "chen": 0, "tu_truot": []}, {"cau": 4, "loi": "That's the last one, then. Goodnight, old street. You'll be brighter now. Just... keep a little dark for the ones who ne", "cua_so": [107.74, 126.04], "neo": [109.74, 124.04], "nghe": "thats the last one then good night old street youll be brighter now just keep a little dark for the ones who need it", "thay": 0, "mat": 0, "chen": 0, "tu_truot": []}], "chu_bo_vi_im_lang_so": [{"bat_dau": 38.82, "ket_thuc": 40.22, "chu": "Great."}, {"bat_dau": 137.68, "ket_thuc": 139.08, "chu": "You"}], "vung_im_lang_so": [[0.0, 12.0], [14.2, 60.0], [62.9, 88.0], [90.3, 110.0], [124.1, 150.0]], "ban_nghe_toan_file": "Evening, Old Street  Great.  Not yet, not yet.  Go on then.  That's the last one, then. Good night, old street. You'll be brighter now. Just keep  a little dark for the ones who need it.  You", "doan_toan_file": [[11.38, 13.86, "Evening, Old Street"], [38.82, 40.22, "Great."], [59.0, 62.52, "Not yet, not yet."], [87.3, `
