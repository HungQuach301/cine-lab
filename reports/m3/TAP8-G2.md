# TẬP 8 — CỔNG G2: bản cuối "From Headphones to Machine Drafts: How Translators' Work Changed"

**Ngày:** 10/10/2026 · **Phiên P** · **Nhánh:** `ccr-a261f349-6rkunc` · **checks:** LL v3 1.8.1 (LOCK KHỚP)

## 0. Kết luận

- **Bản cuối 1080p đã dựng xong** (10:07,3; 14 576 khung; 24 fps), kèm 3 bản xem, 3 Shorts, thumbnail T1/T2, mô tả, chữ Shorts và `reports/m3/HUONG-DAN-DANG-TAP8.md`.
- **QC máy (Q1–Q26, Q26b, Q28–Q30, LOCK):** ĐẠT mọi mục trừ **Q28 mục (f)** — TRƯỢT do ASR độc lập của K đọc "$20 million" và "3.5%" khác cách viết lời; đã khiếu nại 09/10, **không đổi lời** (chỉ đạo chủ dự án). Bảng đầy đủ: `reports/m3/ep08/qc-g2.md`.
- **Q27 chính thức (một lần, 1080p): TRƯỢT nhẹ** — tập 8 **5,13** vs tập 1 **5,44**, chênh −0,31; SE 0,27 nên vượt sai số 0,04. Theo chỉ đạo 09/10 21:08 đây là **lỗi nhỏ chấp nhận** (Q27 trong/sát ±SE): không dựng lại, đã thêm mục "Cải thiện hình" vào `reports/m3/ep09/PLAN.md`.
- **Q31 bản cuối:** vòng 1 TRƯỢT (3/3 ở T12) → **dùng lượt sửa duy nhất** sửa T12 (dựng lại riêng đoạn 12 + ghép). Vòng 2 **TRƯỢT**: T12 hết, nhưng **T01 (0:22,1) 3/3**. Đã hết lượt sửa nên **không dựng lại**; P đề xuất cách sửa rẻ ở mục 7 để chủ dự án quyết.
- **Lời:** đúng bản khoá G1 v2 (SHA 824df1f0…), chỉ rút câu "Machines had long since…" ở đoạn 05 theo luật tỷ lệ chủ dự án đặt. ASR (P) đạt 17/17 đoạn và 3 Short.
- **Tỷ lệ trục kể** (CHUAN-KENH §2): Mở + Kết 16,1 % (khung 15–20) · Quá khứ + Chuyển giao **44,6 %** (khung 40–45, **sát trần**, đã ≤ 45 sau khi rút câu 05) · Hiện tại + Tương lai 39,3 % (35–40, sát trần).
- **Chi phí ước tính:** khoảng **$70–75** credits (mục 6) — trong ngân sách $100. ElevenLabs +6 143 ký tự bộ đếm.
- **Cần chủ dự án:** mục 7.

## 1. Sản phẩm (ngoài repo, `/var/tmp/cine-out/ll-ep08/`)

| Tệp | Cỡ | Thời lượng | SHA-256 (đầu) |
|---|---|---|---|
| `ll-ep08-v1-master.mp4` (1080p, 24 fps, 14 576 khung) | 900,9 MB | 10:07,3 | `a1202dbdb0cda982…` |
| `ll-ep08-v1-p1/p2/p3.mp4` (bản xem) | 71,2 / 83,4 / 68,4 MB | | `a7a343d7…` · `78045316…` · `3a3abee9…` |
| `shorts/ll-ep08-short-S1/S2/S3.mp4` (9:16) | 23,0 / 24,5 / 22,5 MB | 26,1 / 34,2 / 24,2 s | `a94d174a…` · `e874d6d3…` · `b30e5259…` |

SHA đầy đủ: `reports/m3/ep08/SHA256-v1.txt` (lập 10/10 03:20, sau lần dựng sửa T12 — đúng bản QC cuối và Q31 vòng 2).

Trong repo (`reports/m3/ep08/phat-hanh/`):
- thumbnail **T1** (buồng phiên dịch, tai nghe, đèn cảnh báo; chữ lặp tựa, không số) và **T2** (màn hình duyệt bản nháp máy; `1954: "A FEW YEARS" / IT TOOK MORE THAN FIFTY`), dựng từ khung cảnh đinh 1080p;
- mô tả YouTube: tiêu đề A, 17 chương theo mốc thật, nguồn, ghi công ảnh LoC, nhạc, SFX, "How this film was made";
- chữ cho 3 Shorts (S1 Nuremberg 1945 · S2 1954 "250 words" · S3 post-editing 1966 ↔ nay);
- `make_desc.py`, `make_thumb.py` (dựng lại được).

Thẻ kết: "More from Last Lamplighters" (theo chỉ đạo).

**Chưa đẩy video lên nhánh phát hành** — chờ duyệt G2 (mục 7).

## 2. QC Q1–Q31 trên bản cuối

| Mục | Tập 8 (bản cuối) | Tập 7 (bản cuối) |
|---|---|---|
| Q1 judder / Q2 khung trùng / Q3 xuyên hình | 0 / 0 / 0 | 0 / 0 / 0 |
| Q4 master | −14,0 LUFS / −1,6 dBTP; Shorts −14,0 / −1,6 | −14,0 / −1,5 |
| Q5 tương phản chữ thấp nhất | QC_Q5 | 5,12 |
| **Q6 cỡ chữ hoa nhỏ nhất** | **30,7 px (sát ngưỡng 30)** — dòng nguồn S1 | 30,7 px (sát ngưỡng) |
| Q7, Q8, Q18, Q20–Q25 | 0 lỗi (Q22: QC_Q22) | 0 lỗi |
| Q9 số khung | 14 576 = timeline | 14 825 |
| Q10 bản xem / Shorts | 68–83 MB · 24–34 s | 74–77 MB · 17–34 s |
| Q11 / Q12 / Q13 | 0 / 0 / 0 | 0 / 0 / 0 |
| Q14 móc câu · tựa | câu hỏi và hình < 0:15; tựa 13,3 s; trả lời ở đoạn 14 | móc < 0:15 |
| Q15 đổi hình | dài nhất 6,9 s · TB 2,9 s | 7,6 · 2,8 |
| Q16 thẻ giấy | 1,1 % | 2,9 % |
| Q17 mật độ số | 9 số / 10,1 phút = 0,89/phút · neo w250, frey, it_chg | 0,78/phút |
| Q19 tư liệu | 21,1 s (3,5 %, ≤ 20 %) · ảnh LoC FSA/OWI trong RIGHTS | 51,5 s |
| Q26 đa dạng hình | 101 khung nhìn · lớn nhất 3,9 % · liền cùng bố cục **2 (bằng trần 2)** | 102 · 3,9 % · 1 |
| Q26b đa dạng bối cảnh | 7 bối cảnh · lớn nhất studio 22,2 % (trần 25, cách 2,8 điểm) · liên tục dài nhất 76,0 s (trần 90) · nửa sau 6 | (mới từ tập 8) |
| **Q27 chấm hình mù** | **TRƯỢT 5,13 vs 5,44** (mục 3) | 5,68 vs 5,64 |
| **Q28 âm thanh** | 4 cue · âm nghề 51/51 · lặng trước số neo 0,69 / 0,77 / 0,76 s · **(f) TRƯỢT** (mục 5) | ĐẠT |
| Q29 hình–lời | 81/81 | 89/89 |
| Q30 liền mạch / tông | 3 chuyển hồi · b* 16,7 / 9,9 / 1,5 / 20,4 | 18,5 / 12,3 / 1,8 / 17,2 |
| **Q31 xem liền mạch** | **vòng 2 TRƯỢT** · [7, 7, 8] · 3/3 T01 | vòng 5 ĐẠT [7, 7, 7] |
| LOCK | KHỚP | KHỚP |

QC lần cuối chạy trên bản sau sửa T12 (10/10, `qc-g2.md`). Hai mục trượt ở QC 1080p lần đầu (00:35) đã sửa **trước** khi chấm mù, không tính vào lượt sửa sau chấm mù:
- Q5 3,28 (chú thích số đoạn 11 trên nền sáng) → chuyển vào dải chú thích;
- Q22 chữ Short S2 tràn lề → rút gọn chú thích.

## 3. Mọi lần chấm mù của tập 8

Subagent chấm: Sonnet, đề bài và JSON nguyên văn trong `/var/tmp/cine-out/ll-ep08/blind/` (chép phần JSON vào `reports/m3/ep08/blind-g2/`).

**G1 (kịch bản):** 6 lượt đọc mù (2 vòng × 3) — báo cáo ở `TAP8-G1.md`. Không chấm mù nào trên nháp 960×540 (đúng chỉ đạo).

**Q27 — chính thức, một lần, 1080p** (60 khung, tập hợp chọn theo SHA video):

| Người chấm | Tập 8 | Tập 1 |
|---|---|---|
| R1 | 4,98 | 5,43 |
| R2 | 5,18 | 5,29 |
| R3 | 5,22 | 5,60 |
| **TB** | **5,13** | **5,44** |

- Chênh −0,31 (−5,7 %), SE 0,27 → TRƯỢT, vượt sai số 0,04 (**sát ngưỡng**, nêu tên theo luật ±5 %).
- Chấm trên master **trước** lần sửa T12; lần sửa chỉ thay shot mở đầu đoạn 12 (7:01–7:04), nên kết luận Q27 không đổi. P không chấm lại (chỉ đạo: Q27 chính thức một lần).
- Ý chung 3/3 người chấm (nguyên văn rút gọn):
  - R1: "The best frames are the moody lamplit street scenes and the library exterior. Weaker ones are blank or half-built chart cards and flat low-poly interiors with heavy subtitle banners."
  - R2: "Real 3D night-street scenes … are the strongest … The 3D interiors and paper-card infographics are competent but flat and plain, and several frames are caught mid-transition or half-drawn."
  - R3: "The lamplit street and library frames … are clearly the strongest, while the flat chart cards, blank cards and text-heavy frames score low on detail. Several interior frames are murky…"

**Q31 — bản cuối 1080p:**

| Vòng | Bản | Điểm | Kết quả | Điểm ≥ 2/3 |
|---|---|---|---|---|
| 1 | 1080p trước sửa | [7, 7, 7] | TRƯỢT | **T12 3/3** ("That is translation, the written word" nói trên hình buồng phiên dịch video) |
| 2 | 1080p sau sửa T12 | [7, 7, 8] | **TRƯỢT** | **T01 3/3**; T02, T03, T06, T11 2/3 (đã giải trình 4/4) |

- Lượt sửa duy nhất (T12): đoạn 12 mở bằng `st_screen` (màn hình bản nháp) cho câu "That is translation…", chuyển sang phòng phiên dịch video ở chữ "interpreting" (−0,4 s). Vòng 2 không ai nêu T12.
- **T01** (0:22,1), 3/3 nêu: cắt cứng từ màn hình bàn dịch sang phố thư viện ngay chữ "words between languages?", phụ đề câu hỏi còn trên khung qua điểm cắt. Nguyên văn R3: "The cut falls mid-question. The picture changes from the translator's monitor to the library street while the line 'words between languages?' is still being spoken, so the picture and the sentence end at different moments."
- **Giải trình vòng 2** (nguyên văn `giai-trinh.json`):
  - **T02:** "Chuyển chủ ý của kịch bản khoá: lời 'Inside, volunteers bend over messages' đi từ mặt tiền thư viện vào phòng đọc 3D, rồi đoạn 02 mở bằng câu 'Those volunteers were real. A photograph taken in 1942…' và hoà sang ảnh LoC thật (BAI-HOC #93: cắt 3D ↔ ảnh lưu trữ luôn bị nêu; giữ, hoà 1,4 s, giải trình)."
  - **T03:** "Điểm chuyển 1942 → 1945 do lời dẫn báo trước ('A few years later, a trial changed how interpreters worked'); cảnh phòng xử Nuremberg cố ý trung tính, không người bị xử (chỉ đạo chủ dự án G1 v2). Chuyển ảnh lưu trữ → 3D là chủ ý (BAI-HOC #93)."
  - **T06:** "Nhảy 1954 → 1966 là mốc thời gian của chính câu chuyện; lời nói 'In 1966, twelve years after the demonstration' ngay ở chữ đầu đoạn và có phụ đề năm; phòng 1966 khác hẳn phòng máy 1954 là đúng ý (hai nơi, hai thời)."
  - **T11:** "Khung đôi 1966 | today khép ý 'post-editing: the same word as 1966'; cảnh rộng bàn người dịch hôm nay mở đoạn 11 ('The change shows up in the numbers too') — chuyển từ so sánh sang số liệu của cùng bàn làm việc, có chú thích 'Oxford economists' ngay sau 2 s."
- Điểm "chán" 2/3 ở vòng 2: phòng xử Nuremberg (dải R05), cầu sang đoạn 14 (R16/T14), phố kết dài (R17/T15).
- **Câu hỏi thông điệp:** cả 3 người xem tự nêu đúng trục kể (máy được hứa thay người dịch năm 1954 và 1966; điều gì xảy ra với người làm nghề; phần việc nào còn ở con người và bao lâu). Không ai đọc phim thành "máy thay người".

## 4. Thay đổi so với G1 và nháp

**Lời:** giữ nguyên bản khoá; chỉ rút câu "Machines had long since…" ở đoạn 05 (luật tỷ lệ của chủ dự án: QK + CG 45,4 → 44,6 %). Số và nguồn giữ G1.

**Lượt sửa sau nháp** (một lượt, trước 1080p):
- `booth_in`: máy quay nằm sau vách buồng → che khung 2–245; dời máy vào trong buồng.
- `lib_bridge`: lia 180° qua trời trống ~5 s → khoá máy lia dọc phố.
- Q5 biển số ≈28,000 trên nền gạch → nền vữa. Q28d lặng đặt nhầm giữa "two | hundred" → trước "@two". Q29 3 mốc → chú thích số trên cảnh đinh. Q30 hai chuyển hồi 01→02, 14→15 → J-cut.

**Trên 1080p trước chấm mù:** Q5 (đoạn 11), Q22 (S2) như mục 2.

**Lượt sửa duy nhất sau chấm mù:** T12 (mục 3). Dựng lại đoạn 12 + ghép + Shorts (~54 phút máy), không dựng lại cảnh đinh nào.

**Nhà máy:** `scripts/ll/heroes_par.sh` (dựng cảnh đinh song song, khoá pid, `--resume`); `scripts/ll/asr.py` sửa bộ phân tích số (BAI-HOC #104).

## 5. Chỉ số sát ngưỡng (±5 %), mục trượt và sự cố

**Sát ngưỡng (nêu tên theo luật cứng):**
- Q27: −0,31, vượt SE 0,04.
- Q6: 30,7 px vs 30 (dòng nguồn S1).
- Q26: cảnh liền cùng bố cục 2 = trần 2 (từ 5:16,9, đoạn 09 `lib_bridge`).
- Tỷ lệ trục kể: QK + CG 44,6 % (trần 45); HT + TL 39,3 % (trần 40).
- Q26b: bối cảnh lớn nhất 22,2 % (trần 25) — ngoài ±5 % nhưng gần.

**Q28 mục (f) — TRƯỢT, ghi theo chỉ đạo, không đổi lời:**
- ASR độc lập của K đọc đoạn 06 "twenty million" thành "$20 million" (bộ phân tích K tìm 20 000 000 nhưng chữ ASR viết khác) và đoạn 13 "three and a half percent" thành 3,0.
- Giọng đọc đúng lời khoá (ASR của P đạt cả hai đoạn sau khi sửa bộ phân tích số).
- Khiếu nại đã ghi `checks-appeal.md` (09/10); chờ K sửa thước. Lời khoá, không đổi chữ để né thước.

**Sự cố:**
- ASR P đọc sai số → thu lại thừa khoảng 3 000 ký tự gửi trước khi sửa `asr.py` (BAI-HOC #104).
- Job nền bị dừng ở mốc 30 phút / 2 giờ và một lần container khởi động lại; chuyển sang `setsid nohup`, cảnh đinh dựng tiếp bằng `--resume`, không mất khung đã dựng (BAI-HOC #102).

## 6. Token, giờ máy và chi phí

**Token** (đo từ log phiên, khử trùng theo message id; gồm cả phần trước khi nén ngữ cảnh):

| Mô hình | Đầu vào mới | Đầu ra | Cache tạo | Cache đọc |
|---|---|---|---|---|
| Opus (phiên P) | 686 | 342 107 | 6 323 096 | 150 252 002 |
| Sonnet (subagent, log ghi được 15 lượt) | 72 | 10 747 | 1 067 993 | 982 548 |

- Lượt chấm mù: G1 6 lượt (~51 nghìn token mỗi lượt theo báo của công cụ), Q27 3 lượt (~126 nghìn), Q31 6 lượt (2 vòng × 3, ~71 nghìn). Log subagent trên đĩa không đủ cho mọi lượt; số báo của công cụ cộng lại khoảng 1,1 triệu token.
- So trần mềm 1,5 triệu token/tập (đầu vào mới + cache tạo + đầu ra): Opus ≈ 6,67 triệu, Sonnet ≈ 1,08 triệu → khoảng **5,2 lần trần**. Vượt để giữ chất lượng (NGUYÊN TẮC TỐI CAO); phần lớn là cache đọc/tạo khi đọc log và ảnh khung trong 3 giai đoạn dựng dài.

**Chi phí credits ước tính** (bảng giá API: Opus 5.5 $4 / $20 mỗi triệu token vào/ra, cache đọc $0,20; Sonnet 5.5 $2 / $10, cache đọc $0,20; **giá cache tạo không có trong bảng, P giả định 1,25 × giá vào**: Opus $5, Sonnet $2,5):

| Khoản | Ước tính |
|---|---|
| Opus đầu ra 0,342 M × $20 | $6,8 |
| Opus cache đọc 150,3 M × $0,20 | $30,1 |
| Opus cache tạo 6,32 M × $5 (giả định) | $31,6 |
| Sonnet (theo log) | ≈ $3 |
| **Cộng** | **≈ $72** (dải $70–75 tuỳ giá cache tạo và phần log subagent thiếu) |

Đây là ước tính từ token, không phải số trừ thật trên tài khoản; số thật xem ở trang Usage của chủ dự án.

**Giờ máy** (4 vCPU, SwiftShader):

| Bước | Giờ máy |
|---|---|
| Cảnh đinh nháp 960×540 | 1,2 giờ |
| Render + ghép nháp | 1,4 giờ |
| Cảnh đinh 1080p SPP4 (23 cảnh, 12 761 khung, 3 luồng) | ≈ 12,7 giờ |
| Render đoạn + trộn + ghép + Shorts 1080p | ≈ 1,0 giờ |
| Dựng lại sau QC 1080p (Q5/Q22) và sau T12 | ≈ 1,8 giờ |
| QC (nháp 1 lần, 1080p 3 lần) | QC_GIO |
| **Cộng** | **QC_TONG** |

**ElevenLabs:** bộ đếm 56 810 → 62 953 (**+6 143**), log gửi 13 970 ký tự (tỷ lệ tính/gửi ≈ 0,44, ổn định; BAI-HOC #103). Bộ đếm **không đổi** từ prep bản cuối qua mọi lần dựng 1080p và sửa (`el_sent` = 0).

## 7. Việc chờ chủ dự án

1. **Duyệt G2** bản cuối tập 8, hoặc chỉ đạo sửa.
2. **Q31 T01 3/3 (lỗi nghiêm trọng theo định nghĩa của chủ dự án, nhưng đã hết lượt sửa duy nhất):** chọn một:
   - **(a) Chấp nhận nguyên trạng** (P đề xuất nếu ưu tiên ngân sách): điểm chung 7–8/10, thông điệp đọc đúng 3/3; lỗi nằm ở giây 22.
   - **(b) Giao một lượt sửa nhỏ** (P đề xuất nếu ưu tiên chất lượng): kéo dài đuôi đoạn 00 (`tail` 0,6 → ~1,2 s) để câu hỏi nói xong và phụ đề tắt trước điểm cắt, đổi cắt 00 → 01 thành hoà ~1 s sang phố thư viện, J-cut âm phố 0,8 s. Dùng cảnh đinh đã dựng (`ibm`/`studio`, `lib_*`), không dựng cảnh đinh mới. Dựng lại đoạn 00 + ghép + Shorts ≈ 1 giờ máy; Q31 vòng 3 (3 lượt Sonnet, ~0,2 triệu token, ≈ $1–2); ElevenLabs 0 ký tự. Tổng thời lượng tăng ~0,6 s.
3. **Cho phép tạo nhánh phát hành `release-ll-ep08-v1` (Git LFS):** master, 3 bản xem, 3 Shorts, thumbnail, mô tả, chữ Shorts; P tải ngược và kiểm SHA như tập 7.
4. **Q27 −0,31 (lỗi nhỏ chấp nhận):** xác nhận không sửa tập 8; hướng cải thiện đã vào `ep09/PLAN.md`.
5. **Q28f:** chờ K xét khiếu nại 09/10 (`checks-appeal.md`). P không đổi lời.
6. Chọn đề tài tập 9 (`ep09/PLAN.md` đang chờ).

## 8. Lỗi nhỏ chấp nhận (không dựng lại; đã ghi BAI-HOC hoặc PLAN tập 9)

| Lỗi | Mức | Ghi vào |
|---|---|---|
| Q27 5,13 vs 5,44 (−0,31, vượt SE 0,04): nội thất khối thô, thẻ số phẳng, khung giữa chuyển cảnh | thẩm mỹ, sát ±SE | `ep09/PLAN.md` "Cải thiện hình"; BAI-HOC #97 (đã có) |
| Q31 vòng 2: T02, T03, T06, T11 2/3 | có giải trình 4/4 (mục 3) | BAI-HOC #93 (đã có), #106 |
| Q31 điểm chán 2/3: phòng xử (R05), cầu sang đoạn 14, phố kết dài | nhịp | BAI-HOC #106 |
| Q6 30,7 px, Q26 bố cục liền 2 = trần, tỷ lệ QK+CG 44,6 % | sát ngưỡng, đạt | mục 5 |
| Q28 (f) | thước K (khiếu nại) | `checks-appeal.md`; BAI-HOC #104 |
| T01 3/3 | **nghiêm trọng — chờ chủ dự án** (mục 7.2) | BAI-HOC #105 |
