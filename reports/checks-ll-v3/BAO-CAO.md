# Phiên K — xét và khoá luật chất lượng Q26–Q31 (checks LL v3)

Ngày 07/10/2026 · Phiên K (kiểm định độc lập) · Nhánh `checks/ll-v3` (gốc: đỉnh `ccr-5219a838-ftr84s`, 80a66c7).
Chủ dự án duyệt lệnh khoá 07/10/2026, rồi **duyệt kết quả và ra phán quyết 4 câu hỏi cùng ngày**. Mục 1–11 ghi bản 1.7.0 trình duyệt và giữ nguyên để đối chiếu; mục 12 là bản 1.7.1.
Mục 13 là bản 1.8.0 (sửa Q27, Q31, thêm Q26b sau tập 7); số Q26b ở mục 13 đo theo luật quãng cũ, đã được thay bằng mục 14.
**Bản trình duyệt hiện tại là 1.8.1 (mục 14): chủ dự án duyệt 4 quyết định 09/10/2026, sửa quãng liên tục Q26b. K DỪNG, chờ chủ dự án duyệt merge.**

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

## 11. Việc đang chờ chủ dự án (bản 1.7.0, đã xử lý: xem mục 12)
1. Duyệt kết quả khoá checks LL v3 (LOCK `0b180104…`).
2. Trả lời Q-L27, Q-L30, Q-L31, Q-L6v2.
3. Sau khi duyệt: phiên P merge `checks/ll-v3` (P là phiên duy nhất merge vào `main`).

## 12. Sau phán quyết của chủ dự án (07/10/2026) — bản 1.7.1
- **Bản khoá:** VERSION **1.7.1**, LOCK `TREE_SHA256 e3fcd2e686ac92eb15cab0bf93e54aa31165acd8e129d500f4affeb58cc03240`. Tính lại: KHỚP.
- **Tự kiểm:** **109/109** ca đúng kỳ vọng (`do/selftest.txt`). So với bản 1.7.0: thêm 14 ca, bỏ 4 ca tông màu tuyệt đối, sửa kỳ vọng 2 ca.

| Phán quyết | Sửa trong luật | Kiểm bằng |
|---|---|---|
| **Q-L27 = B** (30 + 30) | `N27 = 30`; đề bài Q27 nêu 60 ảnh F01–F60 (SHA đề bài đổi); lấy mẫu phân tầng đều, hạt giống = SHA video mới, trộn như cũ | Ca: đủ 30 + 30, mỗi tầng 1/30 thời lượng đúng một khung; dựng lại ra cùng bộ. **Chạy thật 6 subagent Sonnet** trên đề bài mới (bảng dưới) |
| **Q-L30 = B** | Bỏ khoảng màu tuyệt đối. Hồi 3 phải có b* trung bình (CIELAB, cảnh toàn khung, L* > 15) thấp hơn hẳn mọi hồi khác; thiếu hồi nào để đo thì TRƯỢT; chênh trong ±5 % thì nêu sát ngưỡng | Tập 6 v2: b* 26,1 / 9,5 / **7,9** / 18,2 → ĐẠT (cách hồi 2: 17 %). Ca: hồi 2 lạnh hơn, hồi 3 bằng hồi 2, thiếu hồi 3 → TRƯỢT; 9,2 so với 9,5 → nêu sát ngưỡng |
| **Q-L31 = A có điều kiện** | Vòng tính theo từng tập. `q31-set` chuyển lần xem trước sang `<thư mục>-lich-su/vong-NN`; chỉ vòng chấm đủ 3 người được đếm; manifest ghi số vòng, bộ chấm đối chiếu với sổ lịch sử. Vòng 1: chặn ≥ 2/3. Từ vòng 2: chặn 3/3; điểm 2/3 cần giải trình ≥ 20 ký tự trong `giai-trinh.json` (theo T## hoặc m:ss.s), chép vào báo cáo G2 | Ca: tập 6 v2 vòng 2 chỉ còn 3 điểm chặn (T03, T05, T10); 2/3 chưa giải trình, giải trình quá ngắn → TRƯỢT; đủ giải trình → ĐẠT; sổ lịch sử bỏ vòng chấm dở. **Chạy thật:** dựng bộ hai lần trên cùng thư mục → manifest vòng 1 rồi vòng 2; xoá sổ lịch sử → bộ chấm báo "vòng 2 khác lịch sử" |
| **Q-L6v2 = B** | `scripts/ll/qc.py` gọi Q26–Q31 từ **tập 7** (`_epn >= 7`); tập ≤ 6 ghi "không áp" | Q14, Q16 (đề nghị đã chấp nhận) vẫn áp như bản khoá |

**Q27 chạy thật, bản 30 + 30** (câu trả lời ở `mu/v2-q27b`, `mu/v1-q27b` và `checks/ll/fixtures/ep06/q27b-*.json`):
| | Tập mới | Tập 1 | Chênh | Sai số chuẩn | Tương quan giữa người chấm | Kết luận |
|---|---|---|---|---|---|---|
| Tập 6 v2 | 4,98 | 5,13 | −0,15 | 0,26 | 0,63–0,70 | TRƯỢT (**sát ngưỡng ±5 %**) |
| Tập 6 v1 | 4,34 | 4,92 | −0,58 | 0,20 | 0,14–0,45 | TRƯỢT |

- So với bản 10 + 10, sai số chuẩn giảm từ 0,63 xuống 0,20–0,26, và ba người chấm bớt trùng nhau (0,98 → 0,14–0,70). Luật vẫn phân biệt được: v1 kém rõ ràng hơn v2.
- Tập 6 v2 kém tập 1 0,15 điểm, trong khoảng một sai số chuẩn; ở mẫu khác có thể ĐẠT. Theo Q-L6v2 = B, kết quả này không chặn tập 6.
- Điểm tập 1 khác nhau giữa hai lần chấm (5,13 và 4,92) vì mỗi video mới rút một bộ khung tập 1 khác. So sánh luôn dùng điểm tập 1 của chính lần chấm đó.

**Hạn chế ghi thêm**
- Q30 màu: thước tương đối, chưa có ngưỡng tuyệt đối. **Hiệu chuẩn lại sau tập 7–8** (khi có ≥ 3 tập theo kịch bản màu).
- Q31 vòng: sổ lịch sử nằm trong thư mục ra của P. Xoá cả sổ lẫn bộ hiện tại để "làm lại vòng 1" là không phát hiện được bằng máy; báo cáo G2 phải ghi mọi lần xem mù (đã có trong RULES-LL.md).

**Chỉ số trong ±5 % quanh ngưỡng (bổ sung):** Q27 tập 6 v2 bản 30 + 30, 4,98 so với 5,13 (cách 2,9 %).

**Việc đang chờ chủ dự án**
1. Duyệt bản khoá 1.7.1 (LOCK `e3fcd2e6…`).
2. Sau khi duyệt, phiên P merge `checks/ll-v3` vào `main`. Phiên P cần biết: qc áp Q26–Q31 từ tập 7, đề bài Q27 là 60 ảnh, Q31 có sổ vòng (không xoá `q31-lich-su/`).
3. Hiệu chuẩn lại Q30 màu sau tập 7–8 (K mở lại khi có dữ liệu).

## 13. Sửa sau tập 7 (09/10/2026) — bản 1.8.0
Lệnh chủ dự án 09/10/2026, sau khi đọc `reports/m3/TAP7-G2.md`, `reports/m3/ep07/Q27-Q31.md` (nhánh `claude/eager-babbage-6cc4l6`, df6da4d). Nhánh K: `claude/checks-ll-v3-tap-7-b3kbii`, gốc `main` b9acad1. K không sửa nội dung tập.

- **Bản khoá:** VERSION **1.8.0**, LOCK `TREE_SHA256 848ee170beb253fab25e1eaf6b3d4f53fe4c8f80d0ca6f7561229eb49fe6b1d9`. Tính lại bằng `checks/lock.py --verify`: KHỚP.
- **Tự kiểm:** `checks/ll/selftest_ll.py` **152/152** (109 ca cũ + 43 ca mới, `do/selftest.txt`); `checks/selftest/run_selftest.py` (bộ máy L1) **142/142** ca + kiểm đầu-cuối `run.py` (sạch ĐẠT, bẩn TRƯỢT): TẤT CẢ KHỚP (18,6 phút).
- **Tệp đã sửa:** `checks/ll/q_blind.py` (Q27, Q31), `checks/ll/q_setting.py` (mới, Q26b), `checks/ll/RULES-LL.md`, `checks/ll/selftest_ll.py`, `checks/ll/fixtures/ep06/` (tệp lời, xem 13.5), `checks/ll/fixtures/ep07/` (mới), `checks/cinecheck/__init__.py` (VERSION), `checks/LOCK`; `scripts/ll/qc.py` (chỉ phần gọi luật).

### 13.1 Q27 — chỉ chấm bản cuối 1080p, ngưỡng có sai số
| | Trước (1.7.1) | Bây giờ (1.8.0) |
|---|---|---|
| Bản được chấm | bất kỳ video nào | **chỉ bản cuối 1920×1080**. `q27-set` từ chối bản nháp; `q27-score` trên nháp: TRƯỢT |
| Đối chứng tập 1 | 3 bản xem m23 **1280×720** (`screening/`) | **master m23 1920×1080**, SHA `9c382538…0113942` (đúng SHA trong `M2-3-MASTER-SHORTS.md` và nhánh `release-ll-ep01-v1`). Ngoài repo, lấy bằng `q_blind.py ref-fetch` (kiểm SHA) |
| ĐẠT | tập mới ≥ tập 1 | **d ≥ −SE**, d = tập mới − tập 1, **SE = 0,27** |
| Sát ngưỡng | ±5 % | **\|d\| ≤ SE: "SÁT NGƯỠNG"**, bắt buộc `reports/m3/ep<N+1>/PLAN.md` có mục tiêu đề chứa "Cải thiện hình", nội dung ≥ 40 ký tự; thiếu: TRƯỢT |
| Bộ ảnh luật cũ | — | manifest không ghi đối chứng 1080p: TRƯỢT, phải dựng lại |

**SE đo trên dữ liệu đã có** (`do/q27-se.txt`; 6 lần chấm 30 + 30 hợp lệ, 18 câu trả lời Sonnet thật):

| Lần chấm | Tập mới | Tập 1 | Chênh | SE (người × khung) | SE (chỉ khung) |
|---|---|---|---|---|---|
| Tập 6 v1 | 4,34 | 4,92 | −0,58 | 0,23 | 0,20 |
| Tập 6 v2 | 4,98 | 5,13 | −0,15 | 0,27 | 0,26 |
| Tập 7 nháp lần 2 | 5,11 | 4,90 | +0,21 | 0,28 | 0,22 |
| Tập 7 nháp lần 3 | 5,54 | 5,42 | +0,12 | 0,33 | 0,23 |
| Tập 7 nháp lần 4b | 5,14 | 5,24 | −0,09 | 0,23 | 0,19 |
| Tập 7 chính thức | 5,68 | 5,64 | +0,04 | 0,28 | 0,23 |

- **Cách đo:** mỗi lần chấm, bootstrap hai tầng (lấy lại 3 người chấm có hoàn lại × lấy lại khung trong từng bộ, 4 000 lượt), lấy độ lệch chuẩn của chênh; gộp 6 lần bằng căn trung bình bình phương: **0,273 → khoá 0,27**. Hàm `se27()` trong luật; selftest tính lại từ fixtures và so với số khoá.
- **Khác số "≈ 0,36" trong lệnh:** 0,36 là **dự báo** của K ở bản 1.7.0 (0,63 × √(10/30), mục 8), chưa đo. Số đo thật trên 6 lần là 0,27 (dải 0,23–0,33). Theo "số đo thật thắng số tự khai", K khoá 0,27. Ngưỡng **chặt hơn** 0,36 một chút.
- **Cách đo khác đã xét:** độ lệch chuẩn điểm tập 1 qua 6 lần × √2 = 0,41. Không dùng, vì nó gồm dao động chung của cả lần chấm (cùng người chấm, cùng ngữ cảnh), phần này triệt tiêu khi lấy chênh. Chỉ tính phương sai do rút khung thì được 0,22, thấp vì bỏ qua người chấm.
- **Suy lại bộ new/ref từ hạt giống** (`sets_from_seed`): khớp đúng bộ đã lưu của tập 6 v1, v2; đọc lại tập 7 chính thức ra đúng 5,68 / 5,64 như G2. Dữ liệu tập 7 đóng băng ở `checks/ll/fixtures/ep07/`.
- **Chạy thật đầu-cuối** trên master tập 7 (`ec203d63…`, tải lại từ `release-ll-ep07-v1`, SHA khớp G2): `q27-set` dựng 60 ảnh với đối chứng 1080p trong 19 s; bản xem 1280×720 bị từ chối; `q27-score` với điểm thử bắt được ảnh bị thay, thiếu mục PLAN, và ĐẠT khi PLAN có mục. Đây là thử cơ chế, **không phải lần chấm Q27**; K không gọi subagent.

**Tập 7 theo luật mới:** d = +0,04, trong ±0,27 → **ĐẠT, SÁT NGƯỠNG**. `reports/m3/ep08/PLAN.md` trên `main` hiện **chưa có mục "Cải thiện hình"** (selftest ghi lại: TRƯỢT). P cần thêm mục này trước G2 tập 8. Hướng sửa đã có trong G2 tập 7: nội thất 3D khối thô, tối; thẻ giấy dựng dở. Lưu ý: lần chấm chính thức tập 7 so với tập 1 **720p**. Bản 1.8.0 so với 1080p, nên chạy lại qc tập 7 trên 1.8.0 sẽ báo "bộ ảnh luật cũ" ở Q27. K không chạy lại; G2 tập 7 giữ kết quả 1.7.1.

### 13.2 Q31 — luật chuyển sổ vòng nháp sang bản cuối
- **Dấu vân** ghi trong manifest khi `q31-set`:
  - **lời** = SHA chữ lời từng đoạn (theo căn chữ);
  - **cấu trúc** = SHA của thứ tự đoạn; mỗi đoạn gồm chuỗi shot theo mẫu, cảnh đinh (cả hai nửa diptych), ảnh tư liệu, kiểu vào;
  - không tính thời điểm, máy quay và chi tiết vẽ trong cảnh đinh: lượt sửa ánh sáng/nội thất không đổi dấu vân (selftest).
- **Đếm vòng:** vòng tính theo tập như cũ. Khi chuyển từ nháp sang **bản cuối (1920×1080)**, sổ nháp chỉ được chuyển nếu bản cuối có **cùng dấu vân lời và cấu trúc với nháp cuối cùng đã chấm**. Khác, hoặc nháp không có dấu vân, thì bản cuối **đếm lại từ vòng 1**. Giữa các vòng nháp với nhau và giữa các vòng bản cuối với nhau vẫn đếm tiếp.
- **Chuyển sổ:** `q31-set <cuối>/blind/q31 … --tu-nhap <nháp>/blind/q31` **chép** (không chuyển, không xoá) mọi vòng nháp sang `<cuối>/blind/q31-lich-su/`, chạy lại không chép trùng. Thay cho việc P chép tay như ở tập 7.
- **Không bao giờ xoá `q31-lich-su/`:** manifest ghi SHA manifest của mọi vòng trong sổ. `q31-score` kiểm từng vòng; thiếu hoặc bị sửa: TRƯỢT. Bộ chấm tính lại số vòng từ sổ; khác manifest: TRƯỢT. Dấu vân timeline khác manifest: TRƯỢT.
- **Chạy thật đầu-cuối** trên master tập 7 với sổ vòng nháp thật (vòng 1–4, `reports/m3/ep07/blind/`) và câu trả lời thật vòng 5:
  - ảnh dựng lại **trùng SHA 37/37** với bộ G2 gốc;
  - (A) sổ nháp luật cũ, không dấu vân → bản cuối **vòng 1** → TRƯỢT (T05, T09, T15 2/3 chặn);
  - (B) sổ nháp có dấu vân cùng lời/cấu trúc → **vòng 5** → ĐẠT (3 điểm 2/3 có giải trình);
  - (B′) xoá `vong-02` → TRƯỢT ("sổ vòng thiếu", "vòng 5 khác sổ vòng").
- **Tập 7 theo luật mới:** nháp v6 (vòng 4) và bản cuối **cùng lời, cùng cấu trúc**. Từ 6e771e5 (trước vòng 4) tới df6da4d, `episode.yaml`, `scripts/ll/ll.py`, `scripts/ll/lib/` và `reports/m3/ep07/vo/` **không đổi**; chỉ `design/ll-hero/ep07.js` (nội thất, ánh sáng) đổi. Timeline là hàm của các tệp không đổi đó. Vậy cách P chuyển sổ ở tập 7 (vòng 5) **đúng luật mới về nội dung**. Sổ nháp tập 7 dựng theo 1.7.1 nên không có dấu vân; máy chỉ xác nhận được từ tập 8.

### 13.3 Q26b — đa dạng bối cảnh (mới; áp từ tập 8)
- **Nhãn bối cảnh** cho mỗi shot của timeline (`checks/ll/q_setting.py`):
  - `plate` → cảnh đinh `heroes.<khoá>.hero`: mọi góc máy của một cảnh 3D là **một** bối cảnh;
  - `diptych` → hai nửa, mỗi nửa 1/2 thời lượng;
  - cảnh 2D toàn khung → `2d/<mẫu>`;
  - thẻ số, chữ, trích dẫn, isotype, bản đồ, ảnh tư liệu, thẻ kết → trung tính.
- **Chặn khi:** (a) một bối cảnh > 25 % thời lượng phim; (b) liên tục > 90 s; (c) nửa sau < 3 bối cảnh.
- **Chi tiết K định, nêu để duyệt:**
  - Quãng liên tục đi qua shot trung tính, dứt khi gặp bối cảnh khác hoặc khi chuỗi trung tính dài > 8 s (lấy trần Q15).
  - Ở nửa sau, một bối cảnh phải hiện ≥ 3 s mới được đếm, để chớp một shot ngắn cho đủ số không tính.

**Kết quả** (`do/q26b-*.txt`, có bảng nhãn từng shot):
| | Bối cảnh | Lớn nhất | Liên tục dài nhất | Nửa sau | Kết luận |
|---|---|---|---|---|---|
| **Tập 7 bản cuối** (timeline dựng lại, 14 825 khung = master, 0 ký tự ElevenLabs) | 6 | **ep07/tower 29,1 %** | **ep07/tower 117,0 s (6:02,8–7:59,8)** | 5 | **TRƯỢT** (a), (b) |
| **Tập 6 v2** | 10 | ep06/drafts 17,3 % | ep06/drafts 27,1 s | 7 | **ĐẠT** |

- **Tập 7:** `ep07/tower` là "văn phòng tầng cao hôm nay, đêm" (chú thích trong `ep07.js`), tức **văn phòng đêm**, đúng dự kiến.
  - Tổng 179,8 s qua 3 góc máy (tower_in, tower_code, tower_floor) và 3 diptych.
  - Quãng 5:28,8–5:51,0 bị thẻ trích dẫn 11,9 s cắt (> 8 s); nếu thẻ ngắn hơn 8 s, quãng liên tục là 150,9 s từ 5:28,8 (selftest).
  - Khoảng "chán" 8:00–9:20 người xem Q31 nêu nằm trong phần văn phòng đêm sau cái thang; luật bắt từ tỷ lệ tổng (a).
- **Sát ngưỡng (±5 %):** tập 7 `ep07/pool` (phòng tính toán) **24,99 %**, ngưỡng 25 %.
- **Đối chiếu tập 2–5 (chỉ tham khảo, luật không áp):**
  - Tập 2: TRƯỢT (c), nửa sau 2 bối cảnh.
  - Tập 3: ĐẠT, nửa sau đúng 3.
  - Tập 4: TRƯỢT (a), `2d/office` 37,3 %.
  - Tập 5: TRƯỢT (a), `2d/desk` 33,8 %.
  - Các tập dạng thẻ giấy (trung tính 33–80 %) ít bối cảnh. Luật bắt đúng loại lặp nơi chốn mà chủ dự án chê; không ảnh hưởng tập đã phát hành.
- **qc:** `scripts/ll/qc.py` chạy Q26b **từ tập 8**; tập 7 ghi "không áp". Áp ngược cho tập 7 thì G2 tập 7 TRƯỢT. Chủ dự án quyết (mục 13.7).

### 13.4 Selftest mới (43 ca)
| Luật | Số ca | Nội dung chính |
|---|---|---|
| Q27 | 16 | suy lại bộ từ hạt giống (2); SE khoá = SE đo lại; đọc lại tập 7 = 5,68/5,64; tập 7 sát ngưỡng: không PLAN / PLAN tập 8 trên main / PLAN có mục / mục rỗng / không có mục; +1 điểm → ĐẠT rõ; nháp 4b sát ngưỡng ĐẠT; tập 6 v2 sát ngưỡng ĐẠT; tập 6 v1 TRƯỢT dù có PLAN; lần 4 không hợp lệ; bản xem 720p là nháp; đối chứng là master 1080p |
| Q31 | 17 | dấu vân: sửa nội thất không đổi, đổi cảnh đinh / bỏ ảnh tư liệu / đổi một chữ lời → đổi; đếm vòng: cùng dấu vân → 5, đổi cấu trúc → 1, đổi lời → 1, nháp luật cũ → 1, nháp đổi giữa các vòng vẫn đếm, cuối → cuối đếm tiếp, nháp → cuối đổi → cuối; tập 7 vòng 5 thật ĐẠT, vòng 1 chặn đúng 3 điểm; sổ nguyên / bị sửa / bị xoá; `--tu-nhap` chép đủ, không trùng, nguồn còn |
| Q26b | 10 | tập 7 TRƯỢT đúng hai lý do; tập 7 pool sát ngưỡng; tập 6 v2 ĐẠT; nhãn góc máy, diptych, trung tính; thẻ > 8 s cắt quãng; thẻ < 8 s nối quãng; nửa sau còn 1 bối cảnh; chớp 1,5 s không tính; đoạn 06–08 cùng cảnh 114 s |

(Tổng 43: Q27 16 + Q31 17 + Q26b 10. Một ca Q27 cũ đổi kỳ vọng: "tập 6 v2 10 + 10 nếu mọi khung tập mới +1 điểm" có chênh +0,25 nằm trong SE, không có PLAN → TRƯỢT.)

### 13.5 Sửa dữ liệu tự kiểm (lỗi K tìm thấy)
- Trên `main`, selftest 1.7.1 chỉ được **107/109**. Hai ca Q28 trượt vì "lặng trước số neo ở 00: 0,49 s".
- **Nguyên nhân:**
  - fixture `timeline-v2.json.gz` trỏ tới `reports/m3/ep06/vo/`;
  - P thu lại lời tập 6 v2 (TAP6-SUA-LOI) và nhánh lô 6–8 merge vào `main` sau khi K khoá, nên tệp lời không còn khớp timeline đóng băng.
- **Sửa:** chép đúng bản lời K đã dùng (từ `checks/ll-v3`) vào `checks/ll/fixtures/ep06/vo/` (13 MB) và trỏ timeline vào đó. Selftest không còn phụ thuộc tệp P có thể sửa.
- Tập 2–5 vẫn trỏ `reports/m3/ep0N/vo/`, hiện vẫn khớp; nếu P thu lại lời các tập đó, cần đóng băng tương tự.

### 13.6 Hạn chế
- **SE** đo trên 6 lần, 4 lần trong số đó cùng một tập (tập 7). Lần 4b dùng lại R2, R3 của lần 4. K đề nghị đo lại sau tập 8–9.
- **Q27 sát ngưỡng → PLAN:** máy chỉ kiểm được mục có tồn tại và có nội dung, không kiểm được chất lượng của mục. Tập sau làm đúng mục đó hay không do G1/G2 tập sau và chủ dự án xét.
- **Dấu vân cấu trúc** không tính thời điểm cắt. P dời điểm cắt trong đoạn mà không đổi chuỗi shot thì sổ vẫn được chuyển. Dải T## của Q31 nằm ở ranh giới đoạn, nên dời cắt bên trong đoạn ít ảnh hưởng tới điểm đứt mạch.
- **Q26b** dựa vào khai báo `heroes.<khoá>.hero`. Hai cảnh đinh khác tên mà dựng cùng một nơi (đổi tên để lách) thì máy không thấy; Q26 (khung nhìn) và người xem Q31 vẫn là lưới thứ hai.

### 13.7 Việc đang chờ chủ dự án
1. **Duyệt bản khoá 1.8.0** (LOCK `848ee170…`). Sau khi duyệt, phiên P merge nhánh `claude/checks-ll-v3-tap-7-b3kbii` vào `main`.
2. **SE = 0,27 (đo thật)** thay cho 0,36 (dự báo): xác nhận, hoặc chỉ định 0,36. Đổi chỉ là một dòng `SE27` cùng một ca selftest, rồi khoá lại.
3. **Q26b áp từ tập 8** (đề nghị của K), hay áp ngược tập 7. Áp ngược thì G2 tập 7 TRƯỢT: văn phòng đêm 29,1 % và 117 s.
4. Hai chi tiết đo Q26b do K định: chuỗi trung tính > 8 s cắt quãng liên tục; ≥ 3 s mới tính ở nửa sau. Duyệt hoặc chỉnh.
5. **P cần biết:**
   - Q27 chỉ chạy trên bản cuối (`q_blind.py ref-fetch` một lần mỗi máy);
   - tập 7 Q27 sát ngưỡng → thêm mục **"Cải thiện hình"** vào `reports/m3/ep08/PLAN.md`;
   - Q31 chuyển sổ bằng `--tu-nhap`;
   - không bao giờ xoá `q31-lich-su/`.

## 14. Sau quyết định của chủ dự án (09/10/2026) — bản 1.8.1
### 14.1 Bốn quyết định
1. **SE Q27 = 0,27** (đo thật từ 6 lần chấm). Q27 ĐẠT khi điểm tập mới ≥ tập 1 − 0,27. Chênh trong ±0,27 thì ghi SÁT NGƯỠNG và PLAN tập sau bắt buộc có mục "Cải thiện hình". Luật 1.8.0 đã đúng như vậy, không phải sửa mã.
2. **Q26b áp từ tập 8.** Không áp ngược tập 7 (đã đăng); kết quả tập 7 chỉ ghi nhận là điểm yếu. `scripts/ll/qc.py` đã gọi Q26b từ tập 8, không đổi.
3. **Giữ ngưỡng ≥ 3 s** cho mỗi bối cảnh ở nửa sau. Không đổi.
4. **Sửa luật quãng liên tục của Q26b** (mục 14.2). Vì định nghĩa đo đổi, K nâng VERSION từ 1.8.0 lên **1.8.1**.

### 14.2 Luật quãng liên tục mới (`checks/ll/q_setting.py`, `RULES-LL.md`)
- Shot trung tính (ảnh tư liệu, isotype, trích dẫn, thẻ số…):
  - không làm dứt quãng;
  - không tính vào độ dài quãng.
- Quãng của bối cảnh X chỉ dứt khi các shot có bối cảnh khác X cộng dồn **≥ 8 s**, tính từ lần X xuất hiện gần nhất. X xuất hiện lại thì bộ đếm về 0.
- Diptych có X ở một nửa vẫn tính là có X.
- **Độ dài quãng** = từ đầu shot X đầu tiên tới cuối shot X cuối cùng, trừ các shot trung tính nằm trong quãng.
  - Shot bối cảnh khác ngắn hơn 8 s nằm giữa quãng vẫn được tính, vì luật chỉ loại trừ shot trung tính.
- Đã bỏ `NEUTRAL_GAP`; thay bằng `OTHER_BREAK = 8.0`.

### 14.3 Số theo luật mới, đối chiếu với người rà
(`do/q26b-ep07-final.*`, `do/q26b-ep06-v2.*`, chạy lại và ghi đè)

| | Quãng | Số K (trừ trung tính) | Trung tính trong quãng | Khoảng đầu–cuối | Số người rà | Kết luận |
|---|---|---|---|---|---|---|
| Tập 7 `ep07/tower` (văn phòng đêm) | 5:28,8–7:59,8 | **139,1 s** | 11,9 s (thẻ trích dẫn 5:51) | 150,9 s | ≈ 151 s | TRƯỢT (> 90 s) |
| Tập 7 `ep07/pool` (phòng tính toán) | 0:51,2–2:56,2 | **104,3 s** | 20,7 s (ảnh tư liệu 4,3 + 7,1 s, isotype 9,4 s) | 125,0 s | ≈ 125 s | TRƯỢT (> 90 s) |
| Tập 6 v2 quãng dài nhất | `ep06/drafts` 4:22,0–4:49,1 | **27,1 s** | 0 | 27,1 s | ≈ 28 s | ĐẠT |

**Giải trình chênh ≥ 1 s:**
- **Tập 7:** số người rà bằng đúng *khoảng đầu–cuối* của quãng, tức là vẫn tính thẻ trung tính vào độ dài: 150,9 s và 125,0 s. Quyết định 4 ghi rõ thẻ trung tính "không được tính vào thời lượng quãng", nên K trừ phần đó ra: tower còn 139,1 s (−11,9 s), pool còn 104,3 s (−20,7 s). Ranh giới quãng hai bên trùng nhau, và kết luận giống nhau: cả hai TRƯỢT.
- **Tập 6 v2:** chênh 0,9 s, dưới 1 s. Số ≈ 28 s của người rà có lẽ là khoảng 0:46,8–1:14,8 của `ep06/linotype` (28,0 s). Trong khoảng đó có 16,0 s trung tính, nên theo luật mới quãng này chỉ dài 12,0 s. Quãng dài nhất thật là `ep06/drafts` 27,1 s.
- Nếu chủ dự án muốn tính thẻ trung tính vào độ dài (như người rà), chỉ cần đổi một dòng. Khi đó số sẽ là 150,9 / 125,0 / 28,0 s, kết luận không đổi.

**Tập 7 đầy đủ** (ghi nhận điểm yếu, không áp):
- `ep07/tower` 29,1 % thời lượng (> 25 %);
- tower liên tục 139,1 s; pool liên tục 104,3 s;
- nửa sau có 5 bối cảnh;
- pool chiếm 24,99 %, sát ngưỡng 25 %.

**Tập 6 v2:** ĐẠT. 10 bối cảnh, lớn nhất `ep06/drafts` 17,3 %, quãng dài nhất 27,1 s, nửa sau 7 bối cảnh.

### 14.4 Selftest
- **LL v3: 160/160** ca đúng kỳ vọng (`do/selftest.txt`); 1.8.0 có 152 ca.
  - Thêm 8 ca:
    - Ca 1: thẻ 12 s chen giữa → một quãng 100 s;
    - Ca 2: bối cảnh khác 5 s chen giữa → liền, 105 s;
    - Ca 3: bối cảnh khác 8 s chen giữa → dứt quãng;
    - Ca 4: 4 s + 4 s → dứt quãng;
    - Ca 5: tập 7 pool 0:51–2:56 qua ảnh tư liệu và isotype → 104,3 s, bắt lỗi;
    - thẻ trung tính không cộng vào bộ đếm (4 s + thẻ 6 s + 3,9 s → liền);
    - diptych có X đặt bộ đếm về 0;
    - quãng 100 s qua thẻ 12 s bị bắt.
  - Sửa 3 ca cũ:
    - "thẻ 11,9 s dứt quãng" → thẻ không dứt quãng, 139,1 s;
    - "thẻ ngắn hơn 8 s" → thay thẻ bằng cảnh văn phòng, quãng 150,9 s;
    - ca tổng tập 7 → 3 lỗi (tower 29,1 %, tower 139,1 s, pool 104,3 s).
- **cinecheck (L1, có ASR): 142/142** ca, **0 ca trượt**, kèm kiểm đầu-cuối `run.py` (sạch ĐẠT, bẩn TRƯỢT): TẤT CẢ KHỚP.
  - Lần chạy duy nhất: bắt đầu ≈ 03:38:06 UTC, kết thúc 03:56:42 UTC (18 phút 36,6 giây). Kết quả ở `reports/checks-selftest/selftest.md`.
  - Bản 1.8.1 không sửa mã L1 (`checks/cinecheck/` chỉ đổi chuỗi VERSION), nên K không chạy lại lần hai.
  - Ghi chú: trong lúc chờ, K để ba vòng chờ `pgrep` tự khớp với chính dòng lệnh của mình, nên tưởng selftest còn chạy. K đã dừng các vòng đó; không có lần chạy thứ hai nào.

### 14.5 Bản khoá
- VERSION **1.8.1**, LOCK `TREE_SHA256 208121b48826b80a2170d5fab2e8cb9d092b37cf011de8f0da956e7d0dd98af7`. `checks/lock.py --verify`: KHỚP.
- **Tự kiểm độc lập:** một đoạn Python riêng (`python3 -I`, không nạp mã trong `checks/`) tính lại theo ALGO ghi trong LOCK, trên 155 tệp, ra **cùng** `208121b4…`.
  - Lưu ý cho lần kiểm sau: ALGO sắp theo từng thành phần đường dẫn. Dùng `sort` của shell (so cả chuỗi) sẽ đổi chỗ `ll/fixtures/ep03-v1-4833ac1.yaml` và ra SHA khác.
- Lý do nâng 1.8.1: đổi định nghĩa đo Q26b (b). Q27, Q31 giữ nguyên như 1.8.0.

### 14.6 Việc đang chờ chủ dự án
1. **Duyệt bản khoá 1.8.1** (LOCK `208121b4…`).
2. **Thứ tự merge** (đề xuất của người rà, K đồng ý): `claude/eager-babbage-6cc4l6` (tập 7) vào `main` trước, sau đó nhánh K `claude/checks-ll-v3-tap-7-b3kbii`. Phiên P merge.
3. **Việc của P sau merge:** thêm mục **"Cải thiện hình"** vào `reports/m3/ep08/PLAN.md`, vì Q27 tập 7 sát ngưỡng (+0,04). Gợi ý: đưa vào mục này cả điểm yếu Q26b của tập 7 (văn phòng đêm 29,1 %, 139 s).
