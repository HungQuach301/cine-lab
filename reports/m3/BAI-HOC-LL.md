# BÀI HỌC — Last Lamplighters (tập 1 → lô 3–5)

> **NGUYÊN TẮC TỐI CAO (chủ dự án, 06/10/2026).** Chất lượng — nội dung, hình ảnh, âm thanh, mọi yếu tố và **sự liền mạch giữa chúng** — là ưu tiên hàng đầu, **không bao giờ được hy sinh**. Tốc độ, token, giảm chạm, mở rộng chỉ được tối ưu khi không làm giảm chất lượng. **Trần token là trần mềm:** vượt để giữ chất lượng thì làm và báo cáo, không dừng hỏi. Nguyên tắc này đứng trên mọi mục khác (kể cả §8 "Nguyên tắc tốc độ").

**Bài học gốc của lô 6–8 (chủ dự án, 06/10/2026):** tối ưu token và nhịp đã kéo chất lượng xuống — đa dạng hình tập 1: 52 khung nhìn → tập 6: 19, khung lặp nhiều nhất 18 % → 46 %; hình làm nền cho phụ đề; người thắp đèn chỉ ở đầu/kết; nhạc một bản đều; ít âm thanh nghề; cắt cứng; màu không theo hồi. qc chỉ đo "có đổi", không đo đa dạng, độ đẹp hay liền mạch → thêm Q26–Q31 (CHUAN-KENH §11).

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
| 31 | Kiểm mù: chi phí chủ yếu là **nạp ngữ cảnh subagent**, không phải đọc lời | tập 3: 3 subagent = 141 nghìn; tập 4: 1 subagent 3 vai = 47,3 nghìn | mỗi subagent ≈ 45 nghìn chi phí nền | **1 subagent Sonnet, 3 vai, trần ~50 nghìn/tập; chỉ đưa lời kịch bản (một tệp), không đưa repo** (chủ dự án, 05/10) |
| 32 | Chỉ viết thành script khi một việc đã làm tay từ 3 lần | — | tránh tự động hoá sớm | luật thư viện (chủ dự án, 05/10); `scripts/ll/lib/README.md` |
| 33 | Test thư viện trước mỗi lần build | 13 mẫu, lệch lặp lại < 0,3 mức xám; check bắt 4 đặc tả sai; build dừng mã 3 khi render lỗi | sửa lib làm hỏng mẫu khác mà không biết | `scripts/ll/tests/run.sh`, gọi đầu `build.sh` (TESTS=0 để bỏ) |
| 34 | Mỗi tập một PLAN ≤ 1 trang + mẫu lệnh | — | PLAN gốc 120 dòng lịch sử | `playbook/prompts/`, `playbook/PLAN-TAP-MAU.md`; lịch sử ở `reports/archive/` |
| 35 | Phim quá nhiều thẻ giấy, ít đổi hình, mở đầu chậm | tập 3: giấy 75 %, quãng tĩnh dài nhất 21 s, tựa 0:52; tập 4 (trước sửa): giấy 80 %, 3,1 số/phút, tựa 0:46 | mẫu kênh dựa vào thẻ số; cảnh truyện chỉ ở mở/kết | CHUAN-KENH §9, qc Q14–Q18 (`rhythm.py`), chặn trước render; tập 4 sau sửa: giấy 32 %, 1,75 số/phút, tựa 0:18,6 |
| 36 | Thẻ chữ thuần thay được bằng cảnh + chú thích đè (`cap`) | tập 4: 7 thẻ text/bars → cảnh | — | dùng `cap` trước khi thêm thẻ giấy; thẻ số vào ngay trước số (≤ 1,5 s) |
| 37 | Số phụ đọc trong lời, không lên hình | tập 4: 27 → 15 số trên hình | — | 3 số neo (`anchors`) + số đi kèm |
| 38 | Hoãn tiến trình nền khi phiên/máy khởi động lại | tập 4 lượt 1 mất giữa render | tiến trình `&` không được harness theo dõi | chạy build bằng công cụ nền của harness, không dùng `&` |
| 39 | Băm đoạn lỗi (thư mục `lib/preview` lọt vào danh sách tệp) → băm rỗng → `build.sh` "giữ" trung gian CŨ của đặc tả trước | tập 4: đoạn 00–05 suýt ghép từ bản trước luật nhịp | băm đọc mọi mục trong `lib/` | băm chỉ đọc `lib/*.js`; băm rỗng = lỗi, không bao giờ "giữ" |
| 40 | Nhãn mặc định của mẫu lọt sang tập khác | tập 4: màn hình phòng đánh máy hiện "AUTOMATED VOICE" (nhãn của tập 2) ở 4 đoạn; P thấy khi rà khung tổng quan | `rows.screenLabel` mặc định theo tập 2 | luôn khai `screenLabel` khi dùng `screen`; rà `khung-g2.jpg` trước G2 |
| 41 | `pkill -f`/`pgrep -f` theo chuỗi lệnh giết luôn shell của P (lần 2) | tập 4 | chuỗi tìm nằm trong chính lệnh shell | dừng tiến trình bằng PID lấy từ `ps` có lọc `grep -v $$`, hoặc để tiến trình chạy hết |
| 42 | Chú thích `//` chèn bằng sed/replace vào giữa dòng JS nuốt phần còn lại của dòng | 2 lần (core.js, shot.js) — thư viện hỏng, render lỗi | dòng mã dài một dòng | chỉ dùng `/* … */` khi chèn chú thích giữa dòng; test thư viện bắt được (đã chặn build mã 5) |
| 43 | Test dùng tệp kết quả cũ có thể báo ĐẠT giả | khung `--only` và log `iso-cap` của lần trước | không xoá đầu ra trước khi chạy | xoá đầu ra trước mỗi lần test |
| 44 | Mẫu cảnh không có chuyển động nền liên tục → giữ khung 2–12 khung khi máy quay giảm tốc tới dừng | tập 5 lượt 1: Q1 = 221 (mẫu v2: archive, desk, sign, inspect, isotype) | máy quay easing → vận tốc ≈ 0 ở cuối, cảnh tĩnh tuyệt đối | mọi mẫu cảnh gọi `alive()` (bụi trong ánh đèn + hạt phim đổi mỗi khung); qc Q1 bắt |
| 45 | True peak phần bản xem vượt dù master đạt | tập 5 phần 1: +0,4 dBTP (master −1,5) | mã hoá lại AAC 2 lượt + cắt đoạn | bản xem: volume −1,2 dB + alimiter 0,82 |
| 46 | Mẫu "sơn dần" ghi chữ khi chưa hiện → đo tương phản 1:1 | tập 5 Short S3 khung 0 | chữ vẽ trong vùng cắt rộng 0 vẫn được ghi log | không gọi text khi alpha = 0 |
| 47 | Nhãn khoảng trắng (' ') vẫn được vẽ và đo tương phản | tập 5 đoạn 01, 06: Q5 = 1,01 | dùng ' ' để ẩn nhãn thời kỳ | qc bỏ chuỗi rỗng; mẫu desk không vẽ nhãn rỗng (áp ở lượt chạm thư viện tới) |
| 48 | Nhãn góc trên của mẫu cảnh trùng dòng hook của Shorts (9:16) | tập 5 S2: 'nhãn 1966' dưới hook, Q5 = 1,03 | toạ độ nhãn theo 16:9 | Shorts: không dùng nhãn góc trên; bản vá thư viện chờ: đặt nhãn dưới vùng hook khi 9:16 |
| 49 | Ken Burns phủ kín khung cắt mất chủ thể ảnh tư liệu (xe tai nạn bị dải chú thích che) | tập 5 đoạn 10: P thấy khi chọn khung thumbnail | căn giữa ảnh theo khung | `archive.focus` = điểm chính của ảnh, đặt trên dải chú thích; rà một khung mỗi ảnh trước khi build |
| 50 | Dòng nguồn ảnh tư liệu bị dải chú thích che/thay | tập 5 | chỉ một dòng nguồn | ảnh tư liệu: nguồn ảnh bên phải, nguồn số bên trái, cùng trên dải |
| 51 | Chú thích riêng của mẫu (sign.caption) nằm dưới dải `cap` ở 9:16 | tập 5 S3: Q5 = 1,83 | hai lớp chữ cùng vùng đáy | dùng một lớp: khi có `cap`, bỏ caption của mẫu |
| 52 | Dòng nguồn ghép nhiều nguồn tràn mép phải khung 16:9 | tập 5 đoạn 07 isotype: P thấy trên khung tổng quan, qc không bắt | nhãn `short` dài (mã USDL) + không thu cỡ theo bề ngang | giữ `short` ≤ 30 ký tự; hàng chờ: text tự thu cỡ + qc hộp chữ vượt khung |
| 53 | Mô tả YouTube nêu mốc năm/số ngoài lời phim ("1950s and 60s") | tập 5: Q13 trượt khi mô tả mới sinh | viết mô tả theo trí nhớ nội dung | mô tả chỉ dùng năm/số có trong lời hoặc `numbers`; chạy qc sau khi sinh mô tả |
| 54 | Câu chú thích mang nguồn của cả cảnh, không phải nguồn của nó ("1966…" ghi BLS OOH 2025–35) | tập 5 đoạn 00: Claude rà độc lập thấy sau G2 | dòng nguồn gộp theo số của shot; câu không có `num` mượn dòng chung | mỗi câu khai `num` hoặc `src: [...]` (`src: []` = không cần nguồn); `ll.py` ghi `capsrc`; qc **Q21** chặn câu có số/năm/cơ quan chưa khai và dòng nguồn thiếu nguồn của câu |
| 55 | Shorts 9:16: dòng nguồn và chú thích dài tràn hai mép; hộp ước tính đặt theo toạ độ 16:9 | tập 5 S1–S3: qc **Q22** mới bắt 10 chỗ (G2 đã duyệt mà không thấy) | nhãn nguồn dài; mẫu đặt vị trí cố định theo 16:9 | nhãn `short9` cho Shorts; thư viện tự thu cỡ chữ phủ trên khung (≥ MINPX); `inspect` có bố cục 9:16; Q22 đọc hộp chữ trong log render |
| 56 | Số token "ước" trong báo cáo G2 thấp hơn thực tế nhiều lần | tổng kết lô 3–5: log phiên cho 1,2–2,8 triệu đầu vào mới mỗi tập so với ước 0,24–0,3 triệu | ước theo cảm giác, chỉ gần với token sinh ra | đo bằng trường `usage` trong log phiên (khử trùng theo mã tin nhắn), báo cả sinh ra / đầu vào mới / đọc cache |
| 57 | Luật mới quét lại tập cũ tìm ra lỗi cùng loại ngoài chỗ được giao sửa | Q21 tập 5: 5 đoạn thiếu dòng nguồn ngoài đoạn mở đầu | lỗi hệ thống, không phải lỗi một chỗ | khi thêm luật qc, chạy trên mọi tập đang mở; nêu rõ phạm vi mở rộng trong báo cáo |

## Lô 6–8 (G1)
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| 58 | Đo nhịp Q14–Q19 và Q21 được ngay ở G1 trên timeline ước (lời giả lập 2,214 từ/s) | thử trên tập 5: tựa ước 19,2 s / thật 19,8 s; giấy 14,3 / 15,5 %; số 1,29 / 1,29 phút⁻¹. Lô 6–8: bắt 3 tựa > 20 s, 14 quãng > 8 s, 1 thẻ trống, 18 câu chưa khai nguồn trước khi viết xong | `rhythm.py` chỉ chạy sau `prep` (cần lời thật) | đo trên timeline ước trước G1; đề xuất gộp vào `ll.py est` (LO-6-8-G1 §6.8) |
| 59 | Mốc `@từ` với số đọc nhiều chữ và từ có gạch nối | "@twohundredsixteen" không khớp ("two hundred sixteen" là 3 từ); "paste-up" → "pasteup"; "platform's" ≠ "platform"; "@today" khớp "today" ở câu trước | `norm()` tách theo khoảng trắng, bỏ dấu gạch, giữ dấu nháy | neo vào từ cuối của số ("@sixteen"); dùng `#n`; chạy `ll.py est` sau mỗi lần sửa lời |
| 60 | Kiểm nguồn trước khi chọn đề tài loại sớm thẻ yếu | 5 thẻ: 1 thẻ thiếu nguồn thứ hai (drafters: bls.gov chặn), 1 thẻ trượt điểm 1 (người học việc không phải nhiệm vụ bị tự động hoá) | — | `topics/queue.md`: 5 tiêu chí × 0–2 điểm (chủ dự án, lệnh lô 6–8) |
| 61 | LoC JSON tìm kiếm không có trường quyền; trang `loc.gov/item/…` (HTML) trả 403 | — | — | lọc theo bộ (FSA/OWI, USN&WR), đọc `rights_advisory` qua `loc.gov/item/<id>/?fo=json` |
| 62 | Câu/thẻ ghép hai số khác nguồn, khác loại hoặc khác cơ sở phân loại lọt qua mọi luật cũ | checks LL v2 (Q23) quét 4 tập đã đăng: tập 2 thẻ so sánh đoạn 11 (−16,1 % đếm 1930–40 ↔ −5,3 % dự báo 2025–35); tập 4 hook Short S1 "134,000 to 3.9 million" (1900, phân loại 1950 → 1970) | Q13 chỉ kiểm từng số truy được về `numbers`, không kiểm cặp số | Q23 khoá (LL v2); không sửa video đã đăng (Q-L23b = A, chủ dự án 06/10); áp từ tập 6 |
| 63 | "?" không phải nhãn dự báo; Q20 cần phép đo độc lập với cờ `hit` | — | cờ `hit` do render tự khai, chỉ xét dải chú thích | Q13 bỏ "?" (Q-L13 = A); `render.js` ghi `zones` vào mỗi mục `text` của log từ tập 6 (Q-L20 = A); khai `basis` cho số theo phân loại nghề, `say` đúng như lời |
| 64 | Đoạn "minh bạch về AI" trong lời phim không hợp kênh | tập 6 đoạn 11 (bản nháp G1) | P đề xuất theo cảnh báo "nhạy cảm cao" của SERIES | CHUAN-KENH §10: lời không nói trực diện về việc phim làm bằng AI, không khẳng định sai về cách làm phim; câu hỏi đặt về nghề (chủ dự án, G1 lô 6–8) |
| 65 | Đợt dự báo mới có thể đổi chiều câu chuyện | graphic designers: +2,1 % (2024–34) → −1,7 % (2025–35) | P dùng đợt có toàn văn trên FRASER vì bls.gov chặn P | giao Claude (Cowork) đọc đợt mới nhất **trước** khi viết lời, không đợi G1; thẻ so sánh dùng đợt mới nhất (CHUAN-KENH §10) |
| 66 | ASR dừng build ngay đoạn đầu: faster-whisper 1.2.1 gọi `av.open(..., metadata_errors=…)` mà PyAV 19.0.1 không nhận | tập 6 lượt 1: build mã 4 sau 0 đoạn render; 0 ký tự ElevenLabs thừa (cache theo băm) | `verify.sh` chỉ kiểm import, không giải mã thật | `asr.py` tự giải mã mp3 bằng ffmpeg (float32 16 kHz) rồi đưa mảng cho faster-whisper; hàng chờ: `verify.sh` thêm một lần nhận dạng thử |
| 67 | Cổng luật nhịp trong `build.sh` không chặn: `rhythm.py | tee` trả mã của `tee` (pipefail tắt) | tập 6: Q15 TRƯỢT 8,4 s mà build vẫn render; P tưởng build đã dừng và chạy lượt thứ hai → 2 build ghi chồng một thư mục (x264 2 lượt hỏng tệp thống kê, judder đọc tệp dở) | lỗi có từ khi thêm cổng (tập 4); trước nay nhịp đều đạt nên không lộ | đọc mã qua `PIPESTATUS[0]`; **trước khi chạy build mới, kiểm không còn tiến trình build/render (`ps`)**; hai build chồng nhau thì xoá trung gian, dựng lại sạch |
| 68 | Chữ đè chữ không có luật qc: dòng nguồn số (trái) đè dòng ghi ảnh (phải) ở `archive`; `caption` của mẫu `sign` chồng dải `cap` | tập 6 lượt 1: 02/0, 10/0 (nguồn đè ghi ảnh); 04/0, 07/1, 09/1 (`sign`); qc Q20/Q22 ĐẠT vì chỉ đo chữ–hình và chữ–mép khung | nhãn `short` dài; viết đặc tả quên BAI-HOC #51 | `short` ≤ 30 ký tự cho nguồn đi cùng ảnh tư liệu, ghi ảnh gọn; mẫu `sign` có `cap` thì đưa câu của `caption` vào `cap`; rà `khung-g2` trước qc; hàng chờ: luật P đo hộp chữ giao hộp chữ trong log render |
| 69 | True peak của phần bản xem vẫn vượt dù có giới hạn 0,82 | tập 6 p1: −0,0 dBTP (master −1,6) tại một âm bật "t" của lời; mẫu −0,34 dB sau AAC 720p | AAC vọt ≈ 1,4 dB trên quá độ nhọn | bản xem: `alimiter` 0,75; bộ dò click theo bước nhảy mẫu báo nhầm âm bật tự nhiên — không dùng |
| 70 | Cảnh đinh 3D xoá hết khi một lần dựng lỗi | tập 6 v2: sửa 1 dòng `ep06.js` (chú thích `//` chèn giữa dòng, cắt mất mảng khung máy) → dấu của cả 14 cảnh đổi → `rm -rf` từng thư mục rồi lỗi → mất toàn bộ khung cũ (~2,5 giờ dựng) | dấu băm cả thư mục mã cảnh; build xoá trước khi dựng | `build.sh` dựng vào `<dir>.new`, chỉ thay khi thành công. Sửa mã cảnh: chạy thử `hero.js --only 0` trước khi build |
| 71 | Thước Q26 'cùng bố cục' (xám 32×18, ngưỡng 24) gộp mọi cảnh tối | tập 6 v2: phố đêm, phòng tối, phòng tráng ảnh đỏ cùng một 'bố cục'; tập 1 cũng trượt (chuỗi 4–5) | so độ sáng trung bình, không so cấu trúc | Báo cả hai số; đề nghị K định nghĩa khi khoá (`checks-appeal.md`). Nội dung: tránh ≥ 3 cảnh tối liền nhau |
| 72 | scdet bỏ sót fade nên gộp nhiều shot thành một 'cảnh' | tập 1: ngưỡng 10 → 15 điểm cắt, ngưỡng 4 → 52 | fade, dissolve không tạo bước nhảy khung | `diversity.py`: có timeline thì lấy ranh giới shot thật |
| 73 | Bộ xem mù tự tạo 'lỗi' giả | Q31 tập 6 v2: 3/3 người xem báo '24 s cuối đứng yên' (dải cuối độn bằng khung lặp), 'lời rơi vào thẻ tựa' (cửa sổ lời ±6 s) | công cụ, không phải phim | `blind_set.py`: độn khung đen, lời ±2,5 s. Luôn kiểm điểm mù trên khung thật trước khi sửa |
| 74 | Thẻ trích dẫn sáng ở cuối đoạn cắt cứng sang cảnh tối | Q31 3/3 (T03, T05, T09) | thẻ giấy kem giữa thế giới cảnh tối | Trích dẫn ngắn: chú thích trên cảnh vật chất. Thẻ trích dẫn chỉ giữa đoạn, có chuyển lật hoặc trượt |
| 75 | Dòng hook và số lớn Shorts đè vùng sáng của cảnh 3D | Q5 S1 1,63; S2 3,02 | cảnh đinh có cửa sổ, tờ giấy sáng sau chữ | `shot.js`: dải tối sau hook; dải chú thích 9:16 đậm từ trên số lớn |
| 76 | Lỗi #70 lặp lại thêm 2 lần: chú thích chèn giữa dòng nuốt mã (`cont.py` mất `: nohero.append`, `ep06.js` mất lệnh đặt vị trí người thắp đèn) | lần 3 không gây lỗi cú pháp: người thắp đèn đứng ở gốc toạ độ, không ai thấy; chỉ lộ khi xem trước khung | sửa bằng `str.replace` chèn chú thích vào giữa dòng nhiều lệnh | `tests/comment_guard.py` + `node --check` mã cảnh đinh trong `tests/run.sh` (chạy đầu mỗi build). Không chèn chú thích vào giữa dòng; đặt ở cuối dòng sau khi đã kiểm |
| 77 | Bóng người tối trên mặt tiền tối thì biến mất | Q31: 2/3 thấy 'phố trống, không có người thắp đèn' ở đoạn 12; khung thật xác nhận | không có ánh viền hay nguồn sáng trên nhân vật | nhân vật chính trong cảnh đêm phải có nguồn sáng riêng (ngọn lửa mồi ở đầu sào) |
| 78 | Bàn làm việc 2D phẳng là cảnh yếu nhất cạnh cảnh đinh 3D | Q27 lần 2: khung bàn làm việc 3–5/10 ở cả 3 người chấm; Q31: T03 'đổi phong cách' 2/3 | thư viện 2D cũ đặt cạnh 3D mới | tập 7 trở đi: thay bàn làm việc 2D bằng cảnh đinh 3D nội thất |
| 79 | Khoá YAML `off:` bị đọc thành boolean `false` → khung bắt đầu cảnh đinh bị bỏ qua lặng lẽ | tập 6 v2: mọi shot cảnh đinh đều chạy từ khung 0 qua 4 lần dựng; chỉ lộ khi xem khung đoạn 06→07 (tường nhỏ lại thay vì đẩy vào) | YAML 1.1: off/on/yes/no không ngoặc là boolean | Đặc tả dùng `frame0`; `ll.py load` chặn mọi khoá boolean. Mọi tham số mới: kiểm giá trị trong timeline.json trước khi dựng |

## Tập 7 (G1 v2)
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| 80 | Trục kể đặt vào "máy thay thế người" làm lệch thông điệp kênh | tập 7 v1: móc câu và kết đặt vào "−19 %" và "máy lấy tên nghề" | khung kể cũ xưa ↔ nay theo cặp số | CHUAN-KENH §12 (chủ dự án, 08/10/2026): trọng tâm là sự biến đổi của nghề quá khứ → hiện tại → tương lai; thay thế thật nói đúng nguồn nhưng không làm trung tâm; tương lai chỉ bằng nguồn hoặc câu hỏi mở; kiểm mù hỏi "thông điệp chính người xem rút ra" |
| 81 | bls.gov chặn curl của P (403) nhưng WebFetch đọc được | tập 7: đọc được OOH software developers và computer programmers 2025–35 | đường mạng khác | thử WebFetch trước khi giao Claude (Cowork); WebFetch trả lời qua mô hình tóm tắt nên chỉ nhận trích ngắn nguyên văn, số khớp bảng; ghi "P đọc qua WebFetch" và nhờ Claude đối chiếu khi số mới vào lời |
| 82 | Wikimedia Commons trả 429 liên tục cho proxy của phiên (API và upload.wikimedia.org) | tập 7: 5 tệp Work With Sounds không tải được sau ~1 giờ thử lại | giới hạn theo IP dùng chung | tìm bản sao hợp lệ: Europeana API (`wskey=api2demo`) → "Sounds of Changes" (cùng bản ghi WWS, CC BY 4.0); radio aporee trên Internet Archive (Public Domain Mark). Ghi RIGHTS cả nguồn gốc và bản sao |
| 83 | Dấu băm cảnh đinh tính trên toàn bộ `design/ll-hero/*.js` → sửa một dòng là dựng lại cả 21 cảnh | tập 7: 3 lần dựng lại toàn bộ cảnh nháp (~55 phút/lần ở 960×540 SPP1) | thiết kế an toàn (không giữ cảnh cũ sai) | gom mọi sửa mã cảnh vào một lần; trước khi render đoạn, rà tờ khung 4 mốc/cảnh của mọi cảnh đinh (sau khi dựng cảnh, trước render đoạn) |
| 84 | Cây sào người thắp đèn lật ngược khi giơ tay (lửa mồi chạm đất) | nháp tập 7 lượt 1: đoạn 01, 16 | góc tay −2,4 rad quay cả sào qua vai | góc tổng (tay + sào) quyết định hướng sào: giữ sào gần thẳng, nghiêng đầu sào bằng `pole.rotation.x`; xem trước khung lúc thắp đèn |
| 85 | Mốc `@từ#n` đếm mọi lần xuất hiện trong đoạn, kể cả "first" trong "first American satellite" | đoạn 06 tập 7: `@first#2` rơi vào sai câu | — | khi một từ lặp ≥ 2 lần trong đoạn, in giờ từng lần (align) trước khi chọn `#n` |
| 86 | ASR tham lam (beam 1) nghe "one point seven two million" thành "1.7-2 million" | Q28f TRƯỢT đoạn 12 dù `asr.py` (beam 5) ĐẠT | Bill ngắt nhịp giữa hai chữ số | kiểm thêm bằng beam 1 sau thu giọng; lời khoá thì đổi nhịp đọc (`speed: 0.97`), không đổi chữ |
| 87 | Thẻ/biển chờ số (biển gạch trống, cột laptop chưa mọc) bị chấm mù thấp nhất và bị coi là đứt mạch | Q27 nháp: 3,3–4,1/10; Q31: T08 3/3 | hình không gắn lời trong vài giây đầu | số đặt trên cảnh vật chất đã đẹp (chú thích số trên cảnh 3D) hoặc isotype vào ngay trước số; tránh `sign` khi số đến muộn |
| 88 | Bản nháp 960×540: cảnh đinh nửa khổ, SPP 1, `MW=960` khi ghép | 0,3 s/khung cảnh đinh (so 2,9 s ở 1080p SPP4); cả tập ≈ 2,5 giờ máy | — | chạy Q14–Q31 và chấm mù trên nháp trước khi render 1080p một lần; Q27 trên nháp thiệt cho tập mới (độ phân giải thấp), báo kèm khi so |
| 89 | Q27 dao động mạnh giữa các lượt chấm cùng loại bản | nháp tập 7: lần 2 5,11/4,90 · lần 3 5,54/5,42 · lần 4b 5,14/5,24 | 30 + 30 khung, 3 người chấm; sai số K đo ±0,36 | (điều phối 08/10) Q27 trên nháp chỉ để CHẨN ĐOÁN khung điểm thấp; chỉ chấm chính thức một lần trên 1080p; trượt trong sai số thì ghi G2 cho chủ dự án quyết, không chấm lặp |
| 90 | Người chấm mù có thể trả thiếu hoặc thừa mục (F59–F60 thiếu; F61 = 0 thừa) | tập 7: lần 4 R1 thiếu 2 khung → bộ chấm loại cả lượt; lần 3 R3 thừa F61 → bộ chấm chấp nhận | — | lưu nguyên văn, chạy lại riêng người chấm đó bằng subagent mới, ghi cả lượt bị loại vào G2 |
| 91 | Lời đổi nơi chốn (Langley → JPL California) trên cùng cảnh bàn tính bị coi là đứt mạch 2/3 | Q31 vòng 2 T06 | hình không đổi khi lời đổi địa điểm | cảnh riêng có dấu hiệu nơi chốn nhìn ra ngay (ban ngày, nắng, hàng cọ) + phụ đề nơi chốn ở chữ đầu → vòng 3–4 không ai nêu |
| 92 | Khung chia đôi (diptych) không nhãn: người xem không biết hai nửa là hai thời kỳ/hai chức danh | Q31 vòng 3 T11, T13 (2/3) | — | `p.labels` cho diptych ("Langley, 1940s" · "today"; "computer programmers" · "software developers") → vòng 4 không ai nêu |
| 93 | Cắt 3D cách điệu ↔ ảnh lưu trữ luôn bị 2/3 người xem nêu "đổi chất liệu", kể cả khi có hoà 1,4 s | Q31 vòng 2–4 T04 | dải mẫu cách 1 s không bắt pha hoà | giữ ảnh tư liệu (quyết định của chủ dự án), mở đoạn bằng cảnh 3D nối tiếp rồi hoà; giải trình trong `giai-trinh.json` |
| 94 | Job nền bị ngắt ở 2 giờ xoá phần dở của cảnh đinh đang dựng | 1080p tập 7: mất 655/938 khung tower_code (~40 phút) | `build.sh` xoá `$dir.new` khi chạy lại | `hero.js --resume` + `pending` stamp (08/10): dựng tiếp từ khung cuối; khung tất định nên trùng byte. Lưu ý: prep chạy lại có thể đổi `dur` cảnh 0,1 s → stamp mới → dựng lại |
| 95 | `asr.py` gọi `ll.tts` không kèm `speed` → chữ ký cache lệch với prep → đoạn có `speed` (12) bị thu lại 2 lần mỗi build bản cuối (1,0 rồi 0,97), mỗi lần một bản đọc khác, thời lượng đổi (56,67 → 55,88 → 54,17 s), stamp cảnh đinh đổi theo | 1080p tập 7 lượt 1–2: 2 × 2 lần thu đoạn 12 (702 ký tự/lần), tower_code dựng lại 2 lần | bản nháp chạy `ASR=0` nên không lộ | sửa `asr.py` truyền `speed` (08/10); khôi phục bản thu đã kiểm trên nháp (git); prep kiểm lại: `el_sent` 0, đoạn 12 = 56,67 s như nháp. Bài học: chạy prep bản cuối (có ASR) MỘT lần riêng và kiểm `el_sent` = 0 trước khi render cảnh đinh |
