# BÀI HỌC — Last Lamplighters (tập 1 → lô 3–5)

Mọi phiên P đọc tệp này khi khởi động, thay cho việc đọc lại báo cáo cũ (chủ dự án, 05/10/2026).
- Mỗi dòng gồm: bài học · số đo · nguyên nhân · luật hiện hành (nằm ở đâu).
- Thêm dòng mới ở cuối mỗi mốc. Không xoá dòng cũ; luật đổi thì sửa cột cuối.

## Hình và đồ hoạ
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| 1 | Khung đồ hoạ đứng trống khi lời đang nói | tập 1 lỗi L1; tập 2 lượt đầu 43 quãng → 8 → 0 | hình neo vào từ quá muộn, chỉ có tựa/trục | CHUAN-KENH §5.1 (≤ 3 s); `beats` neo vào từ; `ll.py est` báo trước; qc Q11 |
| 2 | Số trên hình và lời đọc phải khớp | tập 1 lỗi L2 | đổi phân loại số giữa chừng | `say` trong `numbers` (ll.py check); đổi phân loại thì ngắt đường + ghi chú |
| 3 | Nhãn đè ô thu nhỏ/mép biểu đồ; hai đợt dự báo trên một khung | tập 1 L3, L4 | bố cục thủ công | §5.1; hai đợt dự báo ở hai khung riêng, ghi đợt |
| 4 | Nhãn ACTUAL/PROJECTION sai loại | tập 2: Short S2 gắn ACTUAL cho −5,3 % | `bignum` không đọc loại từ số | `bignum` lấy `kind` từ `nums`; qc Q7 |
| 5 | Tương phản chữ < 4,5:1 ở góc tối/màn hình phát sáng | tập 2: nhãn "0"; tập 3: "ATM" 4,15:1 | quầng sáng cộng màu dưới chữ | nền chữ tối hơn, chữ đậm, quầng ≤ 0,2; qc Q5 |
| 6 | Câu trích dài tràn khung 9:16 | tập 3 S3: Q5 = 1:1 | thẻ trích không tự xuống dòng đủ cho Shorts | Shorts: trích ≤ ~12 từ mỗi thẻ, tách nhiều thẻ, nguyên văn có "…" |
| 7 | Chữ đứng > 3 s trong Shorts | tập 2 S1 3,04 s; tập 3 vòng 1: 7 quãng | ít `beats` hơn bản dài | Shorts: một `beat`/dòng mới mỗi ≤ 2,5 s lời; qc Q11 |
| 8 | Khoảng số bị đếm qua số trung gian | tập 2 thẻ 50–80 % | `bignum` đếm mọi giá trị | `range` hiện thẳng (lib) |
| 9 | Thumbnail cắt chữ | tập 2 T1 mất chữ "S" | không có lề an toàn | `thumb.py` lề 5 %; qc Q12 |
| 10 | Mốc `@từ` khớp lần xuất hiện đầu tiên | tập 2 "@many"; tập 4 "@tasks" | từ lặp trong lời | dùng `#2` hoặc từ khác; `ll.py est` giải thử mốc |

## Nguồn số liệu
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| 11 | bls.gov chặn P (403), Wayback bị chặn | mọi tập | chính sách mạng | liệt kê bảng/URL để Claude (Cowork) đọc; đánh dấu CHỜ XÁC MINH; nhãn "đã xác minh (Claude)" |
| 12 | FRASER đọc được (MLR, BLS Bulletin, OOH cũ); URL kiểu `bls_<số>_<năm>.pdf` | Bulletin 1468, 1276, 2350 tải được; OOH 1976 (1875) 404 | — | ưu tiên FRASER; KHÔNG đoán URL quá 1 lần |
| 13 | HSUS 1975 là ảnh quét, không có lớp chữ | gói tập 3–4 đọc bằng mắt | không có OCR | cắt ảnh hàng 300 dpi để Claude đối chiếu ("đã đối chiếu (Claude)"); nên cài tesseract |
| 14 | Gói tra nguồn Sonnet vượt trần | lô 3–5: 4 gói ≈ 100–120 nghìn mỗi gói; vòng bổ sung 124,5 / 80 nghìn | đọc trọn PDF dài; đoán URL | **P tải và lọc (`grep`) trước, chỉ giao đoạn trích (~10 nghìn token/nguồn)** (chủ dự án, 05/10) |
| 15 | Một subagent tốn ≈ 45 nghìn token chi phí nền dù việc rất nhỏ | kiểm mù tập 3: 3 × 47 nghìn = 141 nghìn (trần 25 nghìn) | lời nhắc hệ thống + công cụ của subagent | việc nhỏ: gộp vào 1 subagent hoặc P tự làm; trần dưới ~50 nghìn không giao được 3 subagent |
| 16 | Chuỗi số không có toàn văn thì không kể bằng số | tellers 1980–2010; typists 1970–88 | — | nói thẳng trong lời ("our record runs thin"); không độn |
| 17 | So sánh phải cùng cơ chế, cùng kỳ | tập 3: thẻ +87 % (1960–70, trước ATM) bị chủ dự án bỏ | chọn thập kỷ theo dữ liệu có sẵn, không theo cơ chế | ưu tiên thẻ cùng nguồn, cùng kỳ; nếu không có thì so định tính (tập 5) |

## Giọng, âm thanh, thời lượng
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| 18 | Tốc độ đọc thật của Bill | 2,214 từ/s (tập 2: 1 062 từ / 479,6 s) | G1 tập 2 ước 2,55 từ/s nên thiếu 1:26 | `ll.py est` (BILL_WPS); ước 8:51 → thật 8:35 ở tập 3 (ước dư ≈ 3 %) |
| 19 | ASR báo sai tên riêng hiếm | tập 3: "Bessen" → "Besson", 4 đoạn thu lại 2 lần thừa (≈ 3 000 ký tự) | whisper viết sai tên ít gặp | `asr.py`: hotwords + so gần đúng ≥ 0,75; năm đọc bằng chữ được chấp nhận |
| 20 | Loudness | mọi tập −14,0 LUFS / ≤ −1,3 dBTP | — | `mix.py`; qc Q4 |

## Nhà máy, đĩa, máy
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| 21 | Đĩa đầy giữa phiên | tập 1: 5 worktree + FFV1 | trung gian không nén | CHUAN-KENH §6; dừng khi < 3 GB |
| 22 | `build.sh` ghép trên trung gian cũ khi render lỗi | tập 2 | không kiểm mã lỗi | dừng hẳn (exit 3) |
| 23 | Sửa `lib/` làm render lại TẤT CẢ đoạn | tập 3: lượt sửa nhãn ATM render lại 16 đoạn (≈ 40 phút) | băm đoạn gồm cả `lib/*.js` | gom sửa thư viện vào một lượt; sửa lời/đặc tả không chạm lib thì chỉ đoạn đổi được render lại |
| 24 | `pkill -f` theo đường dẫn giết cả lệnh shell của P | tập 3 | mẫu khớp chính dòng lệnh | dừng tiến trình bằng PID |
| 25 | Không sửa `build.sh` khi nó đang chạy | — | bash đọc script dần | sửa sau khi lượt chạy xong |
| 26 | Giờ máy | tập 2 ≈ 5 giờ máy; tập 3 lượt trọn ≈ 77 phút đồng hồ | mã hoá bản xem "slow" | — |

## Quy trình
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| 27 | 3 cổng là đủ | tập 2: 3 lần chủ dự án chạm | — | CHUAN-KENH §7 |
| 28 | Sonnet làm tốt tra nguồn, trượt Q11 khi dựng shot | tập 2: Opus 64,5 nghìn ĐẠT, Sonnet 60,0 nghìn TRƯỢT | — | Sonnet tra nguồn, Opus dựng shot |
| 29 | Kiểm mù bắt được chỗ lời hiểu sai | tập 3: 3/3 nêu "hopeful" quá đà, 3/3 nêu đoạn 02 dày số | P đọc quen nên không thấy | kiểm mù trước khi thu giọng; sửa điểm ≥ 2/3 |
| 30 | Bản xem tổng quan lấy khung ở 70 % shot có thể rơi vào lúc chưa hiện số | tập 3 khung-g2 đoạn 04 | số neo muộn trong shot dài | xem khung cuối shot khi rà; cân nhắc neo số sớm hơn |
