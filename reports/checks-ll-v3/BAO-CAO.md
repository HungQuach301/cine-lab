# Phiên K — xét và khoá luật chất lượng Q26–Q31 (checks LL v3)

Ngày 07/10/2026 · Phiên K (kiểm định độc lập) · Nhánh `checks/ll-v3` (gốc: đỉnh `ccr-5219a838-ftr84s`, 80a66c7).
Chủ dự án duyệt lệnh khoá 07/10/2026. **K DỪNG ở đây: luật đã khoá, chờ chủ dự án duyệt kết quả và 4 câu hỏi ở mục 8.**

## 1. Kết quả chính
- **Bản khoá:** VERSION **1.7.0**, LOCK `TREE_SHA256 0b180104d6b7cad9e5ab942011f86c02557fb07388bb52260b42c1efdbe22915`.
  Tính lại bằng `checks/lock.py --verify`: KHỚP.
- **Tự kiểm:** `checks/ll/selftest_ll.py` cho **97/97** ca đúng kỳ vọng. Gồm 52 ca cũ (tập 2–5, không đổi) và 45 ca mới trên dữ liệu thật tập 1, tập 6 v1, tập 6 v2 (`reports/checks-ll-v3/do/selftest.txt`).
- **Hiệu chuẩn Q26 (đúng yêu cầu):** tập 1 **ĐẠT**; tập 6 v1 **TRƯỢT**; tập 6 v2 kết luận theo thước mới là **ĐẠT**.
- **Tập 6 v2 theo bản khoá:**
  - ĐẠT: Q14, Q16, Q26, Q29.
  - TRƯỢT: Q27, Q28, Q30, Q31 (chi tiết ở mục 7). Áp ngay hay từ tập 7 là câu hỏi Q-L6v2.
- **Đề nghị của P:** Q14 (tựa chồng lên cảnh đinh) và Q16 (5 mẫu toàn khung) đều **CHẤP NHẬN**. Q16 tập 6 v2 giảm từ 75,6 % xuống 7,2 %.
- **Tệp đã sửa:**
  - `checks/` (luật, đề bài, fixtures, LOCK);
  - `scripts/ll/qc.py` (chỉ phần gọi luật);
  - `checks-appeal.md` (phán quyết);
  - thư mục báo cáo này.

## 2. Q26 — đa dạng hình
### 2.1 Thước của P có 3 lỗi đo (chạy lại trên `screening/`, cùng tệp chủ dự án xem)
| | Tập 1 m23 | Tập 6 v1 | Tập 6 v2 |
|---|---|---|---|
| Thước P: khung nhìn / lớn nhất / chuỗi | 50 / **21,1 %** / 4 → TRƯỢT | 15 / 46,3 % / 5 → TRƯỢT | 67 / 4,9 % / **5** → TRƯỢT |

1. **Gộp mọi cảnh tối thành một bố cục.** Ở ngưỡng 24/255 trên xám thô, mọi cảnh tối đều chênh nhau dưới 24.
   - Chuỗi "5 cảnh liền" của v2 ở 6:07,8 là 5 cảnh khác hẳn nhau: Linotype cao, tường bản nháp, bảng tin việc, khung đôi, khay chữ.
   - Ở tập 6 v1, phố đêm và ảnh tư liệu cũng bị gộp vào cụm "bàn làm việc".
2. **Kết quả phụ thuộc thứ tự và pha lấy mẫu.** Mỗi cụm so với mẫu đầu tiên của nó, nên lời giải đổi theo thứ tự mẫu.
   - Đổi pha lấy mẫu 0,5 s làm tỷ lệ lớn nhất của tập 1 dao động **14,4–21,6 %**.
   - Con số "18 %" của tập 1 trong chẩn đoán gốc là một pha may.
   - Trên bản xem 3 phần, chính thước P cho tập 1 **TRƯỢT** (21,1 %).
3. **Ranh giới cảnh dò bằng `scdet` bỏ sót gần hết các chuyển thẻ giấy** (lướt, lật) của tập 1: có "cảnh" dài 184 s.

### 2.2 Định nghĩa khoá
Hai chỉ số khung nhìn giữ nguyên ngưỡng (≥ 40, ≤ 20 %) và đặc trưng của P (32×18 xám thô, chênh < 12/255). Sửa ba điểm:
- **Gom cụm liên kết đầy đủ:** mọi cặp mẫu trong một khung nhìn đều chênh < 12/255. Không phụ thuộc thứ tự mẫu. Cài đặt tự viết, đối chiếu với scipy cho phân hoạch giống hệt.
- **Lấy mẫu ổn định:** lưới 0,5 s chia thành 6 pha (mỗi pha 1 mẫu/3 s, đúng mật độ chủ dự án định). Kết quả lấy pha **xấu nhất**.
- **Cảnh liền cùng bố cục:**
  - Ranh giới cảnh = mọi đầu shot trong timeline (nhà máy LL). Tập không có timeline thì dò chuyển cảnh toàn khung.
  - Bộ dò được đối chiếu với ranh giới thật: v2 bắt 50/59 điểm cắt, đúng 50/54 lần dò; v1 bắt 24/30, đúng 24/29.
  - Hai cảnh liền nhau **cùng bố cục** khi khung đại diện thuộc **cùng khung nhìn**, sau khi trừ độ sáng trung bình và nâng tương phản khung tối lên sàn 40.
  - Hệ quả: cảnh tối khác nhau không còn bị gộp, còn cắt nhảy về cùng một hình vẫn bị bắt dù sáng tối khác nhau (selftest: hình tối đi 4 lần vẫn bị bắt).
- **Vì sao "cùng bố cục" = "cùng khung nhìn" mà không dùng ngưỡng lỏng hơn:**
  - Tập 1 có nhiều thẻ giấy khác nội dung (biểu đồ đường, trích dẫn, cột, sơ đồ) đặt trên cùng khuôn tờ giấy; chúng chênh nhau 8–20/255 (hình `hinh/q26-tap1-the-giay-lien-nhau.jpg`).
  - Ngưỡng lỏng (20–24) sẽ coi chúng là cùng bố cục, khi đó tập 1 TRƯỢT với chuỗi 7.
  - Chủ dự án đã định tập 1 là chuẩn đạt, nên "cùng bố cục" phải nghĩa là **cắt sang cùng một hình**, không phải "cùng khuôn giấy". Tỷ lệ thẻ giấy đã có Q16 giữ.
- **Các phương án K đã thử và bỏ:**
  - Chuẩn hoá z, lọc dải, bản đồ cạnh, SSIM, tỷ lệ ô khác nhau: với cả 5 cách, tập 1 gộp ≥ 70 % (mép tờ giấy và vân giấy cố định chiếm hết cấu trúc ảnh).
  - Nâng tương phản cho cả chỉ số khung nhìn: làm v1 lọt (cảnh bàn tối bị tách thành nhiều khung nhìn).

### 2.3 Kết quả (bản khoá, chạy trên `screening/*.mp4`)
| | Khung nhìn (6 pha) | Lớn nhất (6 pha) | Cảnh liền cùng bố cục | Kết luận |
|---|---|---|---|---|
| Tập 1 m23 (không timeline, dò trên hình) | **64** (64–72) | **11,9 %** (7,0–11,9) | 2 | **ĐẠT** |
| Tập 6 v1 (timeline dựng lại, 11 758 khung khớp master) | **19** (19–24) | **43,3 %** (39,6–43,3) | 2 | **TRƯỢT** |
| Tập 6 v2 (timeline) | **70** (70–79) | **5,5 %** (4,2–5,5) | 2 | **ĐẠT** |
| Tập 6 v2 (dò trên hình, đối chứng) | 70 | 5,5 % | 2 | ĐẠT |

- Tập 6 v1: cụm lớn nhất là cảnh bàn làm việc (hình `hinh/q26-thuoc-P-cum-lon-nhat-tap6v1.jpg`). Bản khoá đo 43,3 %, P đo 46 %; chênh lệch do bản khoá không còn gộp nhầm phố đêm và ảnh tư liệu.
- Số liệu từng pha: `do/q26-*.json`; số của thước P: `do/q26-thuoc-P-*.txt`.

## 3. Q27 và Q31 — xem mù bằng subagent (K cố định)
| | Q27 chấm hình | Q31 xem liền mạch |
|---|---|---|
| Đề bài | `checks/ll/blind/Q27-R1..3.txt`: nhà quay phim / chỉ đạo mỹ thuật / người xem YouTube. Cùng thang beauty, detail, light 1–10; trả JSON | `Q31-R1..3.txt`: người xem lần đầu / dựng phim / biên tập truyện. Trả lời câu hỏi của phim, điểm 1–10, danh sách `break` / `boring` theo `T##` hoặc `R##.k` |
| Mẫu | 10 khung tập mới + 10 khung tập 1 m23 (SHA khoá), **phân tầng đều** theo thời lượng; hạt giống = SHA-256 video mới; trộn | 6 khung quanh mỗi điểm chuyển đoạn + lời ±2,5 s; dải tổng quan 1 khung/4 s, 8 khung/dải, độn khung đen |
| Người chấm | 3 subagent **Sonnet** mới, độc lập, chỉ nhận đề bài | như Q27 |
| Ngưỡng | trung bình tập mới ≥ tập 1 (chủ dự án) | TRƯỢT khi có điểm **đứt mạch** được ≥ 2 người khác nhau cùng nêu (cùng T## hoặc cách ≤ 4 s) |
| Chống sửa | Bộ chấm kiểm SHA đề bài, mô hình, đủ 3 người, đủ điểm. Bộ chấm **dựng lại 20 ảnh và so SHA**. Không có tệp khoá giải mã | Kiểm SHA đề bài và SHA từng dải ảnh so với manifest; số dải phải khớp timeline |

**P không được sửa đề bài:**
- Đề bài nằm trong `checks/` nên khoá SHA cùng luật.
- P chỉ thay `{DIR}` (lệnh `q*-set` tự điền) và phải ghi `prompt_sha256` vào mỗi câu trả lời.
- Bộ ảnh phải nằm ngoài repo; lệnh `q*-set` từ chối thư mục nằm trong repo.

**Chạy thật trên đề bài khoá (9 subagent Sonnet, câu trả lời lưu ở `mu/` và `checks/ll/fixtures/ep06/`):**
| | Kết quả | Kết luận |
|---|---|---|
| Q27 tập 6 v2 | tập mới **4,83**, tập 1 **5,58** (R1 4,77/5,53 · R2 4,90/5,50 · R3 4,83/5,70) | TRƯỢT |
| Q27 tập 6 v1 | tập mới **3,84**, tập 1 **5,48** | TRƯỢT |
| Q31 tập 6 v2 | điểm liền mạch 7 / 6 / 7. 8 điểm đồng thuận ≥ 2/3, trong đó **7 điểm đứt mạch**: T01, T03, T05, T07, T09, T10, T12. Cả 3/3 cùng nêu: T03, T05, T10 | TRƯỢT |

**Phát hiện quan trọng về Q27:**
- Ba người chấm Sonnet cho điểm từng khung tương quan **0,98** với nhau. Ba vai khác nhau không tạo ra ba ý kiến độc lập.
- Vì thế phương sai thật nằm ở **việc rút khung nào**. Với 10 + 10 khung, sai số chuẩn của chênh lệch ≈ **0,63 điểm**.
- Lần P chấm tập 6 v2 (+0,37) và lần K chấm (−0,74) đều nằm trong vùng nhiễu này. Đề nghị tăng số khung ở câu Q-L27.

**Q31:** P đã sửa một phần theo lần xem trước (T02, T04 không còn đồng thuận). Các điểm còn lại là cắt cứng giữa hai cảnh tối khác nơi, cùng lời không khớp hình ("the work did not vanish" trên tường tối).

## 4. Q28–Q30 — kiểm định nghĩa đo
| Mục | Thước P (`scripts/ll/cont.py`) | Lỗ / điểm yếu tìm thấy | Bản khoá |
|---|---|---|---|
| Q28 lặp nhạc | các khoảng nguồn cùng bài chồng ≤ 60 s; cờ `loop` | dựa hoàn toàn vào mix.json tự khai | thêm: cue không được dài hơn bài (ffprobe); độ dài đoạn bài = độ dài cue |
| Q28 cue theo hồi | hồi 2, 3 một bài; kết = bài đầu tiên | "nhạc hiệu kênh" = bất kỳ bài nào đặt đầu tiên | nhạc hiệu xác định bằng SHA (RIGHTS LL-MUS-1 Reawakening); mở **và** kết đều phải là nhạc hiệu |
| Q28 âm thanh nghề | mỗi `plate` có SFX trong [đầu − 1,5 s, cuối] | `diptych` (hai cảnh đinh) không được kiểm; quyền theo tên tệp | `diptych` tính là cảnh đinh; SFX phải có **SHA-256 trong RIGHTS.md** (3 tệp có SHA nhưng thiếu tên tệp trong RIGHTS: gas-hiss, paper-flip, paper-slide) |
| Q28 lặng trước số neo | căn chữ ElevenLabs; chỉ các lần khớp | số neo không khớp cụm `say` thì **bỏ qua im lặng** (ĐẠT); "eighty-six" có gạch nối dễ trượt khớp; P đo 3 lần đọc trong khi có 4 | mọi số neo phải tìm thấy; đo trên **âm thật** của tệp lời (khung 10 ms < −50 dBFS), mọi lần đọc. Tập 6 v2: 0,76 / 0,69 / 0,69 / 0,70 s (căn chữ: 0,76 / 0,78 / 0,83 / 0,76). Ngưỡng −60…−40 dBFS cho cùng kết quả ±0,03 s |
| Q28 loudness | mix.json | số tự khai | đo ebur128 trên master; không có master thì dùng mix.json và ghi rõ |
| Q28 ASR | asr.json của P (tên riêng khớp 3 chữ đầu hoặc giống ≥ 0,6) | công cụ của P; khớp lỏng | ASR độc lập của K (faster-whisper small.en, tất định) trên từng tệp lời. Số so **chặt** theo giá trị, tên riêng giống ≥ 0,75. Tập 6 v2: 13/13 đoạn đủ từ khoá |
| Q29 hình–lời | shot vật chất chạm cửa sổ ±1 s | vòng lặp kiểm số neo **rỗng** (`pass`); hình chạm 0,05 s ở đuôi fade vẫn tính; `map` (thẻ giấy) tính là vật chất | kiểm cả mọi lần đọc số neo; hình phải hiện ≥ 0,5 s trong cửa sổ; đoạn có lời phải khai `nouns`; bỏ `map` khỏi hình vật chất. Tập 6 v2: 59/59 |
| Q30 chuyển hồi | chỉ cần một phía khai match/jcut/lcut | hai phía có thể khai mâu thuẫn | hai phía phải khai **cùng** một kiểu; J-cut và L-cut phải có SFX kéo qua ≥ 0,3 s |
| Q30 ngọn đèn | danh sách tên cảnh có đèn **viết trong mã của P** | đèn có hiện hay không tuỳ góc máy | danh sách (cảnh, góc máy) **K xem tận mắt**; cảnh mới: `heroes.<khoá>.lamp: true`. Tập 6 v2: khay chữ cận (`cellar` b) ở 01→02 không thấy đèn (hình `hinh/q30-den-chuyen-hoi-tap6v2.jpg`) |
| Q30 tông màu | ≥ 60 % thời lượng cảnh đinh có nhãn `grade` đúng (tự khai) | không đo màu | đo **tông trung bình trên điểm ảnh** cảnh toàn khung mỗi hồi (CIELAB, L* > 15). Ấm: h 20–80°, C ≥ 15. Sepia: h 45–95°, C 4–15. Lạnh: h 180–300°, C ≥ 3 |

**Đo màu thật tập 6 v2:**
| Hồi | Khai | h | C | Đánh giá |
|---|---|---|---|---|
| 1 | ấm | 59° | 30,4 | ấm |
| 2 | sepia | 72° | 10,0 | sepia |
| 3 | **lạnh** | **61°** | **9,0** | **sepia, ngả vàng** |
| 4 | ấm | 50° | 23,8 | ấm |

Hồi 3 có cả cảnh ấm (khay chữ cam, phòng Linotype, mặt phố gạch đỏ); chỉ tường bản nháp là xanh tối (hình `hinh/q30-canh-dinh-theo-hoi-tap6v2.jpg`).

## 5. Đề nghị của P (checks-appeal.md)
- **Q16 — CHẤP NHẬN.** K xem khung thật tập 6 v2 (hình `hinh/q16-mau-tap6v2.jpg`).
  - `plate`, `diptych`, `filmstrip`, `jobboard` là cảnh toàn khung.
  - `pasteup` là tấm bảng dàn trang (đạo cụ thời kỳ, đặt nghiêng trên bàn tối), không phải thẻ dữ liệu: chấp nhận, có ghi chú.
  - Tập 6 v2: bản khoá cũ 75,6 % → bản mới 7,2 % (thước P: 12,9–15,2 %). Tập 2–5 không đổi.
  - Q14 "hình trước 0:15" dùng cùng tập cảnh toàn khung. Tập 6 v2 vẫn ĐẠT nhờ chú thích.
- **Q14 — CHẤP NHẬN.**
  - Tựa phim = `text` + `lamp` như cũ, hoặc `plate` có `p.title`.
  - Khi có log render, chuỗi tựa phải hiện trong log của đoạn trong khoảng shot (selftest: khai title mà log không có chữ → TRƯỢT).
  - Ngưỡng 0:20 giữ nguyên.
  - Lưu ý: `title` trong đặc tả là tiêu đề YouTube, khác chữ tựa trên hình ("THE HAND THAT DREW IT"), nên luật đọc `p.title`.

## 6. Selftest và dữ liệu thật
- Dữ liệu đóng băng trong `checks/ll/fixtures/ep06/` (1,1 MB):
  - mẫu Q26 (32×18, 2 khung/s) của tập 1 m23, 6 v1, 6 v2;
  - timeline tập 6 v1 và v2, dựng lại bằng `ll.prep` từ giọng đã lưu, đã chặn gọi ElevenLabs: **0 ký tự**;
  - mix.json tập 6 v2, dựng lại bằng `mix.py`: −14,0 LUFS / −1,6 dBTP, đúng số P báo;
  - câu trả lời thật của 9 subagent.
- 45 ca mới, mỗi luật có ca BẮT lỗi thật và ca SẠCH. Ví dụ:
  - cắt nhảy 3 cảnh cùng hình;
  - cue dài hơn bài; dùng lại 90 s cùng đoạn bài;
  - lời chưa chèn lặng trước số neo;
  - đoạn chỉ còn thẻ số;
  - hai phía chuyển hồi khai khác nhau; bỏ tiếng J-cut;
  - người chấm thiếu khung; chỉ 2 người chấm;
  - đề bài bị sửa (SHA khác);
  - hai người nêu cùng chỗ bằng hai cách ghi (T05 và R05.1).
- **Chạy tích hợp qua `scripts/ll/qc.py`** trên thư mục ra dựng lại của tập 6 v2 (`do/qc-tich-hop-ep06-v2.md`): các dòng Q26–Q31 ra đúng như bảng trên. Dòng LOCK KHÔNG KHỚP ở lần chạy đó vì chạy trước khi khoá lại; sau khi khoá: KHỚP.

## 7. Tập 6 v2 theo bản khoá (để P biết sửa ở đâu)
| Mục | Kết quả | Việc cần làm |
|---|---|---|
| Q26 | ĐẠT 70 / 5,5 % / 2 | — |
| Q27 | TRƯỢT 4,83 so với 5,58 | Kết luận phụ thuộc mẫu; xem Q-L27 |
| Q28 | TRƯỢT | Shot `diptych` ở 2:43,2 (đoạn 05) và 6:24,4 (đoạn 10) không có âm thanh nghề. Còn lại ĐẠT: 4 cue, nhạc hiệu mở/kết, lặng 0,69–0,76 s, −14,0 LUFS / −1,6 dBTP, ASR 13/13 |
| Q29 | ĐẠT 59/59 | — |
| Q30 | TRƯỢT | (1) 01→02: shot trước điểm cắt là khay chữ cận (`case_line`), không thấy đèn; (2) hồi 3 đo h 61°, C 9: không lạnh (xem Q-L30) |
| Q31 | TRƯỢT | 7 điểm đứt mạch ≥ 2/3 (xem Q-L31) |

## 8. Câu hỏi cho chủ dự án
K đã khoá đúng chữ CHUAN-KENH §11.2; chọn khác thì K sửa và khoá lại. Chi tiết trong `checks-appeal.md`.

1. **Q-L27. Số khung chấm mù.**
   - **A (đang khoá):** 10 + 10 khung.
   - **B (khuyến nghị):** 30 + 30 khung. Sai số ≈ 0,36 thay vì 0,63; ba người chấm vẫn ổn (đọc 60 ảnh, dưới 1 phút).
   - Ưu của B: kết luận ổn định, không phụ thuộc may rủi của mẫu. Nhược: gấp 3 lượt đọc ảnh mỗi lần chấm. Rủi ro của A: tập đạt hay trượt do mẫu, không do chất lượng.
2. **Q-L30. Tông màu theo hồi.**
   - **A (khuyến nghị, đang khoá):** đo trên điểm ảnh, ngưỡng tuyệt đối. Tập 6 v2 TRƯỢT; P phải grade lại các cảnh đinh hồi 3.
   - **B:** đo trên điểm ảnh, chỉ đòi hồi 3 lạnh nhất trong 4 hồi. Tập 6 v2 ĐẠT.
   - **C:** đếm nhãn như P.
   - A đúng chữ "tông màu trung bình"; B nhẹ cho xưởng nhưng chấp nhận hồi "lạnh" vẫn ngả vàng.
3. **Q-L31. Điểm đồng thuận.**
   - **A (khuyến nghị, đang khoá):** chặn điểm đứt mạch ≥ 2/3.
   - **B:** chỉ chặn điểm 3/3; điểm 2/3 phải có phản hồi trong báo cáo G2.
   - **C:** chặn cả điểm "chán".
   - Rủi ro của A: người xem mù gần như luôn tìm thấy vài chỗ cắt cứng, nên có thể phải lặp nhiều vòng. Nếu sau một vòng sửa vẫn còn điểm 2/3, K đề nghị chuyển sang B.
4. **Q-L6v2. Áp v3 cho tập 6 v2 đang chờ G2?**
   - **A (khuyến nghị):** áp; P sửa Q28 và đèn (sửa nhỏ), màu hồi 3 theo Q-L30, rồi chạy lại Q27 và Q31.
   - **B:** phát hành tập 6 v2 theo luật làm việc của P, áp v3 từ tập 7.

## 9. Hạn chế đã biết
- **Q27/Q31 là luật dựa trên trung thực của P:**
  - P gọi subagent, nên K không chứng minh được câu trả lời đến từ đúng đề bài; chỉ chứng minh được ảnh, đề bài và định dạng khớp.
  - Mỗi lần dựng lại video sinh một bộ mẫu mới, nên về lý thuyết có thể "rút lại" mẫu Q27. RULES-LL.md buộc báo cáo G2 ghi **mọi** lần chấm.
  - Đề nghị chủ dự án hoặc K kiểm toán ngẫu nhiên bằng cách tự chạy lại.
- **Q26 khi không có timeline:** dùng bộ dò trên hình (độ chính xác 83–93 % so với ranh giới thật). Mọi tập dựng bằng nhà máy LL đều có timeline.
- **Q30 kiểu chuyển "match":** chưa đo được trên hình, chỉ dựa vào khai báo; người xem Q31 xem dải T## ở mọi điểm chuyển.
- **Danh sách cảnh có đèn:** K mới xem các cảnh tập 6. Cảnh mới dựa vào khai báo `lamp: true` cho tới lần K mở sau.
- **Ngưỡng màu Q30 chưa hiệu chuẩn chéo:** mới đo trên một tập có kịch bản màu (tập 6 v2). Các khoảng h/C lấy theo vùng màu CIELAB thông dụng, không chỉnh theo dữ liệu.

## 10. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
- **Q14 tập 6 v2:** tựa ở 19,8 s, trần 20 s (cách 1 %).
- **Q15 tập 6 v2:** quãng dài nhất 7,8 s, trần 8 s (cách 2,5 %).
- **Q26:**
  - Chuỗi cảnh liền cùng bố cục bằng đúng ngưỡng 2 ở cả tập 1, tập 6 v1, tập 6 v2 (số nguyên, không có biên).
  - Khung nhìn và tỷ lệ lớn nhất không có chỉ số nào sát ngưỡng.
- **Q28, Q29, Q30:** không có chỉ số nào trong ±5 %. Lặng gần nhất là 0,69 s so với sàn 0,5 s.

## 11. Việc đang chờ chủ dự án
1. Duyệt kết quả khoá checks LL v3 (LOCK `0b180104…`).
2. Trả lời Q-L27, Q-L30, Q-L31, Q-L6v2.
3. Sau khi duyệt: phiên P merge `checks/ll-v3` (P là phiên duy nhất merge vào `main`).
