Nhánh thật: **`claude/p-1910-merge-g1b-giong-chot-49iath`** (harness buộc tên này thay cho `p-1910` của lệnh). Tạo từ `origin/main` @`5253ba2b`. Đã đẩy nhánh này; **không merge vào `main`**.

# PHIÊN P-1910: hợp nhất G1b + GIỌNG-CHỐT, Kinh thánh §13 + sửa 19/10, nháp lời v4.2 (D11), ghi sổ 18–19/10. BÁO CÁO. DỪNG chờ chủ dự án

```text
ĐIỀU LỆ PHIÊN P-1910                                          | thực tế
Loại phiên:        P (điều phối)                               | đúng
Nhánh:             p-1910 từ origin/main @5253ba2b              | harness buộc tên khác (dòng đầu); gốc đúng; main KHÔNG cập nhật
Merge --no-ff:     (a) ccr-6189ede9-lpjwe0 @b9cff40e (G1b) →
                   (b) claude/giong-chot-contested-places-ux4ytb @ccbb1478
                       (GIỌNG-CHỐT, gồm casting-my @3f5dd72b, casting-giong @3b011a0c)
                                                               | 2/2 đúng thứ tự, 0 xung đột; 3f5dd72b, 3b011a0c là tổ tiên của HEAD
Sửa ngoài merge:   docs/BIBLE-KENH2.md, khoa-loi/loi-v4.2-NHAP.txt, AUTHORSHIP, RIGHTS,
                   COST-LEDGER, channel-k2/HANG-DOI.md, reports/ | đúng; KHÔNG sửa checks/, design/, scripts/, loi-khoa.txt
loi-khoa.txt:      giữ SHA 0fdc72ce…                            | 0fdc72ce81e33b6f… trước và sau; sha256sum -c LOI-KHOA.sha256 3/3 OK
lock.py:           chỉ gọi với --verify                         | đúng; mọi lần KHỚP 1.15.0 f4fa0349…
Chi phí:           Claude/OpenAI/ElevenLabs/YouTube 0           | $0 · $0 · 0 ký tự · 0 đơn vị; không gọi API, không WebFetch
Giờ máy:           mốc theo dõi 2 h                             | ≈ 0,4 h thời gian thực; chưa vượt
Preflight:         --staged mỗi commit; --range trước khi đẩy   | --staged ĐẠT ở cả 4 commit P soạn tay; 2 commit merge tạo thẳng bằng `git merge` (không qua --staged) → kiểm bằng --range ngay sau merge (a) và lần cuối; --range: xem §5 (1 mục báo nhầm P4 có sẵn từ G1b)
Email:             che; không vào header/URL/payload/UA          | 0 email trong diff P; không có yêu cầu mạng nào mang email
Dừng hỏi:          không dừng giữa chừng                         | đúng
```

## 0. Tóm tắt
| Mục | Kết quả |
|---|---|
| Merge | 2/2 `--no-ff`, **0 xung đột**. G1b `82141a3a` (125 tệp, +54 924 / −42); GIỌNG-CHỐT `5b4e9187` (92 tệp, +13 313 / −32) (§1) |
| Sau merge | lock **KHỚP 1.15.0 `f4fa0349ca53b05d64e4303554ec168e6445c82d97e662672f70ccf42df80d40`** · selftest k115 **105/105** · k114 **126/126** · `LOI-KHOA.sha256` **3/3 OK** |
| Kinh thánh | SHA-256 `3307185e…a1d24eaaf` → **`5014eb8e3793f864b47fef330d14209554f1e1f4971b60cd5a713b2638a0618b`**; thêm §13 (13.1–13.6), sửa 6 chỗ + tiêu đề, mỗi chỗ kiểm "đúng 1 lần" (§2) |
| Nháp D11 | `channel-k2/k2c-t3-01/khoa-loi/loi-v4.2-NHAP.txt` (SHA `d48c2333…`); 2 câu nối A/B; lời 1 571 → 1 567–1 569 từ, ≈ 628,4 → 626,8–627,6 s ở 2,5 từ/s (§3) |
| Sổ | AUTHORSHIP +8 dòng · RIGHTS +10 dòng · COST-LEDGER +5 dòng (mọi dòng 20 cột) · HANG-DOI mục 19/10 (§4) |
| Kiểm cuối | lock **KHỚP** · k115 105/105 · k114 126/126 · golden steel **KHỚP** (SSIM 0,9449), ll08 **KHỚP** (0,9307), t1 **LỆCH CỤC BỘ** 22/144 (0,9082), trùng P-1810c · preflight `--range` trượt đúng 1 mục báo nhầm P4 có sẵn · 0 email (§5) |

## 1. Merge
SHA đầu nhánh khớp lệnh: `origin/main` = `5253ba2b`, `origin/ccr-6189ede9-lpjwe0` = `b9cff40e`, `origin/claude/giong-chot-contested-places-ux4ytb` = `ccbb1478`.

| # | Nhánh @ SHA | SHA trước → sau | Thay đổi (so cha 1) | Xung đột |
|---|---|---|---|---|
| a | `origin/ccr-6189ede9-lpjwe0` @b9cff40e (G1b) | `5253ba2b` → **`82141a3a`** | **125 tệp**, +54 924 / −42: `reports/g1b-t3/` 81, `channel-k2/k2c-t3-01/` 28 (g1b/, phat-hanh/…), `scripts/k2tl/` 6, `scripts/k2/` 6, `design/k2v/` 4. Không đổi `checks/`, `docs/` | không |
| b | `origin/claude/giong-chot-contested-places-ux4ytb` @ccbb1478 (GIỌNG-CHỐT + casting-my + casting-giong) | `82141a3a` → **`5b4e9187`** | **92 tệp**, +13 313 / −32: `reports/giong-chot/` 38, `reports/casting-giong/` 26, `reports/casting-my/` 22, 2 báo cáo casting, 4 tệp `channel-k2/k2c-t3-01/` (PLS, `tu-dien.json`, `tts-preview`, dòng PLS của `LOI-KHOA.sha256`) | không |
| — | Kinh thánh | `14b7557b` | 2 tệp (`docs/BIBLE-KENH2.md` +27 / −7, `reports/p-1910/sua_bible.py`) | — |
| — | Nháp D11 | `aefe4683` | 3 tệp (`loi-v4.2-NHAP.txt`, `reports/p-1910/nhap_d11.py`, `nhap-d11.json`) | — |
| — | Ghi sổ | `bae6dcca` | 4 sổ + `reports/p-1910/golden.json` | — |
| — | Báo cáo | commit chứa tệp này | `reports/P-1910-BAO-CAO.md` | — |

**Kiểm sau merge (b):**
- `python3 -I checks/lock.py --verify` → **KHỚP**, LOCK = tính lại = `f4fa0349…df80d40` (1.15.0).
- `/opt/cine/bin/python -I checks/ll/selftest_k115.py` → **105/105**, 15 nhóm (8 s). `selftest_k114.py` → **126/126** (8 s). P chỉ chạy, không đọc mã.
- `cd channel-k2/k2c-t3-01 && sha256sum -c LOI-KHOA.sha256` → `script-v4.1-KHOA.md: OK`, `loi-khoa.txt: OK`, `khoa-loi/phat-am/gibraltar-eric.pls: OK` (**3/3**; PLS là bản GIỌNG-CHỐT `66ed934a…`).

**Preflight sau merge (a):** `--range 5253ba2b..HEAD` chặn **1 mục P4**: `reports/g1b-t3/nguoi/giay-phep/mpfb2-LICENSE.txt` dòng 2 là `=======`, gạch chân tiêu đề "LICENSE" trong bản giấy phép MPFB2 nguyên văn, không phải dấu xung đột merge. Đây đúng là mục G1b đã tự báo (G1B §2 mục 8, §6 mục 7). Không phải xung đột merge nên P tiếp tục. P không sửa tệp giấy phép (phải giữ nguyên văn) và không sửa `scripts/` (§5, §8 mục 3).

## 2. Kinh thánh `docs/BIBLE-KENH2.md`
SHA-256 trước `3307185e3e51a78f57088aa74ae575c828fd9d80fe4f04514451a70d1a24eaaf` (bản P-1810c, script kiểm trước khi sửa), sau **`5014eb8e3793f864b47fef330d14209554f1e1f4971b60cd5a713b2638a0618b`**. Script `reports/p-1910/sua_bible.py`: mỗi thay thế kiểm **đúng 1 lần xuất hiện** rồi mới áp; §13 chỉ thêm khi tệp chưa có "## 13.". Ngoài các chỗ dưới đây không câu nào đổi (`git diff`: +27 / −7).

**Tiêu đề:**
```diff
-… 17–18/10/2026 — §11; bổ sung 18/10/2026 tối — §12)
+… 17–18/10/2026 — §11; bổ sung 18/10/2026 tối — §12; §13 + sửa 19/10)
```

**(a) §13 "Hiểu hai đường"**, thêm vào cuối tệp: dòng "## 13. …" + 13.1–13.5 chép nguyên văn từ lệnh; 13.6 "Ngữ pháp hình timelapse (duyệt TL-1…TL-6 ngày 19/10/2026 12:45)" + 6 gạch TL-1…TL-6.
- **Nguồn của 13.6:** `reports/v7p/` **chưa có trên origin** (`git ls-remote` + `git ls-tree origin/main`: không có nhánh hay thư mục v7p), nên P chép từ khối trong lệnh P-1910.
- **Định dạng:** giữa các dòng 13.x P thêm một dòng trống để Markdown không gộp 13.1–13.5 thành một đoạn. Chữ từng dòng giữ nguyên văn.

**(b) §12.1:**
```diff
-- Trên hình CHỈ có: bộ đếm năm/ngày (chữ chính, suốt tập); chip tên nơi khi vào một nơi mới, ≤ 3 s rồi tắt; số liệu hoặc câu trích khi lời đang nói tới, kèm tên nguồn ngắn cỡ nhỏ, ≤ 3 s.
+- Trên hình CHỈ có: bộ đếm năm/ngày (chữ chính, suốt tập); chip tên nơi khi vào một nơi mới, ≤ 3 s rồi tắt; (bỏ — theo §13.6 TL-4).
```
```diff
-… (b) thẻ "How this film was made" 4–5 s ở cuối video (bản đồ/nguồn chính, …
+… (b) thẻ "How this film was made" 2 thẻ × ≈ 8 s cuối phim (D6) (bản đồ/nguồn chính, …
```

**(c) §10.6 (D7):**
```diff
-… built from the cited sources and registers; on marked street frames, surface detail is AI-assisted — …
+… built from the cited sources and registers; on two street frames, surface detail is AI-assisted — …
```

**(d) §4, dòng âm thanh:**
```diff
-… chuỗi MIX=audio mặc định từ T3 (xuất stem); giọng Eric eleven_multilingual_v2; từ điển phát âm áp khi khoá lời.
+… chuỗi MIX=audio mặc định từ T3 (xuất stem); giọng G1 (Voice Design `VDLncRBHDjLHBqLhQ1Qt`, chọn qua nghe mù 18/10 và 19/10) eleven_multilingual_v2, speed 1,03; điều khoản chờ thư Đ5; từ điển phát âm áp khi khoá lời.
```

**(e) §11.6 (dòng 173):**
```diff
-- Video thử: 540p ≤ 15 MB, KHÔNG vào LFS; …
+- Video thử: 540p ≤ 5 MB (§12.5), KHÔNG vào LFS; …
```

**(f) Luật mật độ Q-PT4-4:** con số 30–80 người khung neo **có trong Kinh thánh**, ở §11.2 (dòng 144; "30–80" xuất hiện đúng 1 lần trong tệp). V6 và G1b đều dẫn con số này là "Q-PT4-4". P thêm chú thích D8 ngay sau con số:
```diff
-… khung neo phố ban ngày 30–80 người ở 10–60 m, trang phục và thành phần dân cư theo nguồn …
+… khung neo phố ban ngày 30–80 người ở 10–60 m (1782: theo bảng gác Spilsbury 7/9/1782 + dân thường từ danh-sach-9-1782 — D8), trang phục và thành phần dân cư theo nguồn …
```
`danh-sach-9-1782` là `reports/nc-ai/aib/danh-sach-9-1782.json` / `DANH-SACH-9-1782.md`. D8 cũng ghi ở AUTHORSHIP.

**Câu còn mâu thuẫn với luật mới.** P không sửa vì lệnh không giao; cần chủ dự án quyết (§8 mục 4):
1. **§4 dòng 51:** "Chữ trên màn hình: dòng nguồn ngắn khi có con số: chỉ tên nguồn ngắn, cỡ ≥ 38 px…". Câu này ngược §12.1 (đã bỏ) và §13.6 TL-4: số liệu do lời + CC mang.
2. **§10.5:** "Nhãn chủ chốt hiện đủ… số so sánh". Câu đã có đuôi "(chữ trên hình: theo §12.1)" từ P-1810c, nhưng vẫn nhắc số trên hình. Nay TL-4 cấm tấm số đứng riêng.
3. **§4 dòng 50, nhịp thị giác** (≤ 3,5 s có một biến cố; checks Q37), so với **TL-1** (≤ 5 cắt/phút, shot trung bình ≥ 12 s). Hai luật đo khác nhau: biến cố so với cắt. Nhưng shot timelapse dài 12 s+ với máy cao cố định dễ trượt Q37 "không giữ khung tĩnh > 6 s" nếu thời gian chạy chậm. G1b đã khiếu nại Q37 (`reports/g1b-t3/khieu-nai-K.md`). Nên đưa cho phiên K trước V7-PILOT.
4. **§12.1 dòng 3** còn liệt kê "(nhãn nguồn ghost), §10.5, …" như trước. Không sai, nhưng chưa nhắc §13.3 thẻ chương. §13.3 đã tự ghi "ngoại lệ của §12.1".

## 3. Nháp lời D11 (KHÔNG sửa `loi-khoa.txt`)
- **Tệp:** `channel-k2/k2c-t3-01/khoa-loi/loi-v4.2-NHAP.txt`, SHA-256 `d48c233376c729b8361f57f21c6f2a36f20d01e0133b3a4a5f00524e57a33dd0`.
- **Công cụ:** `reports/p-1910/nhap_d11.py`, số đo ở `reports/p-1910/nhap-d11.json`. Công cụ kiểm `loi-khoa.txt` đúng `0fdc72ce…`, mỗi đoạn neo xuất hiện đúng 1 lần, và số đoạn giữ nguyên.
- **Kiểm độc lập:** so tập dòng đã sắp xếp của hai tệp chỉ khác đúng 1 dòng, là câu bỏ "Before the attack, ".
- **Nội dung nháp:** đoạn hầm mùa hè 1782 (2o, 2p) dời lên ngay trước 2j (8/9/1782), tức sau 2i ("By September 1782…"). Bỏ "Before the attack, " và viết hoa "All summer". Không chữ nào khác đổi.

**Bảng diff dòng** (số dòng theo `loi-khoa.txt` → nháp):
| Dòng khoá | Dòng nháp | Đoạn | Thay đổi |
|---|---|---|---|
| 67 | 67 | 2i "By September 1782, the garrison counted about seven and a half thousand men." | giữ |
| — | **69** | 2o | **chèn**: "All summer, the garrison had been digging through the north face. By early July, Sergeant Ince's thirteen men had cut about eighty-two feet of solid rock." |
| — | **71** | 2p | **chèn**: "In July they blasted a hole for air. A Spanish historian wrote it was big enough for a cannon." (nguyên văn) |
| 69–77 | 73–81 | 2j → 2n (8/9 đạn đỏ … 2 000 tổn thất, 357 được cứu) | giữ nguyên chữ, lùi 4 dòng |
| 79 | — | 2o cũ "**Before the attack,** all summer, the garrison had been digging…" | **bỏ** ở chỗ cũ |
| 81 | — | 2p cũ | **bỏ** ở chỗ cũ |
| 83 → | 83 → | 2q "The blockade never forced a surrender…" trở đi | giữ |

**Hai phương án câu nối** (thay câu đầu 2o trong nháp). Cả hai chỉ dùng dữ kiện đã có trong lời khoá: mùa hè, đào qua vách bắc, đơn vị đồn trú. Không thêm claim.
| | Câu | Từ | Ưu | Nhược |
|---|---|---|---|---|
| **A** | "That summer, they had been digging through the north face." | 10 | "That summer" neo vào "1782" của 2i ngay trước. "They" (= đồn trú ở 2i) tránh lặp "the garrison" 3 đoạn liền (2i, 2o, 2j đều mở bằng "the garrison") | "they" dựa vào chủ ngữ câu trước; nếu sau này 2i đổi thì phải xem lại |
| **B** | "Meanwhile, all summer, the garrison had been digging through the north face." | 12 | Chủ ngữ rõ; "Meanwhile" báo hai mạch song song (bắn phá và đào hầm) | Lặp "the garrison" 3 đoạn liền; "Meanwhile" sau câu đếm quân tháng 9 hơi lỏng về thời gian |
| (nháp) | "All summer, the garrison had been digging through the north face." | 11 | Đúng lệnh "bỏ Before the attack", không thêm chữ | Không có từ nối; lặp "the garrison" |

**P khuyến nghị A**, vì câu ngắn nhất, neo thời gian rõ, và bớt lặp. Chọn câu nào là việc của chủ dự án.

**Số từ và thời lượng ước** (đếm từ lời, không tính đầu mục chương; 2,5 từ/s theo lệnh):
| Bản | Từ | Thời lượng ước | Chênh |
|---|---|---|---|
| Khoá v4.1 (`0fdc72ce…`) | 1 571 | 628,4 s | — |
| Nháp (bỏ "Before the attack") | 1 568 | 627,2 s | −3 từ / −1,2 s |
| Nháp + A | 1 567 | 626,8 s | −4 từ / −1,6 s |
| Nháp + B | 1 569 | 627,6 s | −2 từ / −0,8 s |

- Ở tốc độ thật của G1 (≈ 2,2 từ/s, GIỌNG-CHỐT §3), mỗi phương án cũng chỉ đổi lời < 2 s.
- **Tác động lên bảng shot** (cho V7-PILOT/G1b): GIỌNG-CHỐT §5 cho 2o hấp thụ 5,4 s lời chảy từ chuỗi 2k–2n (+6 s giãn). Sau khi dời, 2o đứng trước 2j, nên phần lời chảy đó phải sang shot giãn được kế tiếp sau 2n. Bảng giãn shot phải tính lại sau khi khoá v4.2.
- Sau khi chủ dự án chọn, phiên khoá lời làm các việc sau: tạo `loi-khoa.txt` mới, `script-v4.2-KHOA.md`, chạy lại `lam_loi_khoa.py`, cập nhật `LOI-KHOA.sha256` và các thẻ ‹2o›/‹2p› trong kịch bản.

## 4. Sổ
| Sổ | Nội dung |
|---|---|
| `AUTHORSHIP.md` | 8 dòng có giờ:<br>• **P10C-1…5** (18/10 23:49). P10C-1 = ngoại lệ video V5b-2d `338cef97…`; P10C-2 = "AI use = Yes". Hai mục này có dấu vết trong repo. **P10C-3…5 chưa có nguyên văn**<br>• **CASTING-MỸ M2 = G1** (19/10 06:07)<br>• **giữ lời T3 + "hiểu hai đường"** (06:25)<br>• **HC-1 kiểu A + HC-2** (06:44) → §13.1–13.5<br>• **GIỌNG-CHỐT**: speed 1,03 (bản 1.03-B), model giữ `eleven_multilingual_v2` (X = v4, Y = v2, khớp `khoa-model.json`; Đ-B) (12:45)<br>• **TL-1…TL-6** bản sửa theo số đo đối thủ (12:45) → §13.6<br>• **D2–D8, D11** theo khuyến nghị (12:45). Ghi rõ D1, D9, D10, D12 không thuộc lượt này<br>• **C2-1…C2-9 vẫn thiếu nguyên văn** |
| `RIGHTS.md` | Khối mới 10 dòng (G1b §6 mục 6 + giọng G1):<br>• **P1910-100STYLE**: CC BY 4.0, ghi công bắt buộc "The 100STYLE Dataset - Ian Mason"<br>• **P1910-CMU**: "free for all uses"<br>• **P1910-MPFB2**: tài sản CC0; mã GPLv3 chỉ chạy làm công cụ<br>• **P1910-CLIO**: mở rộng P1810-CLIO cho SM1, Zenodo 23128623<br>• **P1910-ETOPO**: mở rộng P1810B-ETOPO cho SM1<br>• **P1910-ROOKE**: RP-P-OB-33.529, CC0<br>• **P1910-CAP1704**: RP-P-OB-83.181, CC0<br>• **P1910-LOC1905**: LoC 2020680546, "No known restrictions on publication."<br>• **P1910-MUS-TAM**: Tyrant.mp3, trỏ dòng K2-MUS-3, chỉ animatic nội bộ<br>• **P1910-G1**: Voice Design; **quyền chờ thư Đ5, chưa dùng cho bản phát hành tới khi ElevenLabs trả lời** |
| `COST-LEDGER.csv` | +5 dòng, kiểm bằng `csv`: **mọi dòng đúng 20 cột** (58 dòng):<br>• **P-1810c**: nguyên văn dòng đề xuất §7 của báo cáo P-1810c<br>• **G1B-T3**: Claude **$5,632**, mốc theo dõi 5, giờ máy **9**, 726,2 s<br>• **CASTING-MY**: EL **4 970** gửi, bộ đếm **+2 298**, 0,5 h<br>• **GIONG-CHOT**: EL **4 941** gửi, bộ đếm **+2 171**, 0,33 h<br>• **P-1910**: $0, 0,4 h |
| `channel-k2/HANG-DOI.md` | Mục mới "CẬP NHẬT 19/10/2026 (phiên P-1910: T3)", trên các mục cũ:<br>• **T3 → V7-PILOT** (ngữ pháp timelapse §13.6), rồi dựng cả tập<br>• **giọng G1 chốt**<br>• **lời chờ chọn câu nối D11**; v4.1 còn hiệu lực tới khi khoá v4.2 |
| `reports/p-1910/golden.json` | Số đo golden của phiên (§5) |

**Điểm P tự quyết hoặc chưa kiểm được:**
1. **P10C-3…5:** lệnh chỉ ghi "P10C-1…5 (18/10 23:49)". Repo chỉ có dấu vết của P10C-1 (G1b bước 0) và P10C-2 (`nguon-mo-ta.md`). **P không tự viết lại**, và AUTHORSHIP ghi rõ còn thiếu.
2. **HC-2:** lệnh không nêu riêng nội dung HC-2. AUTHORSHIP ghi HC-1 (kiểu A) và dẫn văn bản có hiệu lực là §13.1–13.5.
3. **RIGHTS 3 ảnh:** SHA đầy đủ của 3 tệp ảnh không có trong repo. G1b chỉ ghi 8 ký tự đầu, và tệp nằm ở `/var/tmp` của container G1b, nay không còn. P ghi phần SHA có sẵn và đánh dấu "SHA đầy đủ chưa ghi". Phiên dựng bản sản xuất cần ghi đủ khi tải lại.
4. **COST-LEDGER, ngày:** dòng G1B-T3 ghi ngày bắt đầu 2026-10-18 (16:55 UTC → 19/10 04:30); dòng CASTING-MY ghi 2026-10-18 (lệnh 23:36). Riêng **casting-giong** (CASTING-GIỌNG) **chưa có dòng** trong COST-LEDGER, và lệnh không giao. Cần ghi ở lần P kế (§8 mục 6).

## 5. Kiểm cuối
| Kiểm | Kết quả |
|---|---|
| `python3 -I checks/lock.py --verify` | **KHỚP**: 1.15.0, `f4fa0349…df80d40`. Chạy sau merge, trong preflight của mỗi commit, và lần cuối trước khi đẩy |
| `selftest_k115.py` / `selftest_k114.py` | **105/105** (15 nhóm) / **126/126**. Chạy sau merge và lần cuối |
| `sha256sum -c LOI-KHOA.sha256` | **3/3 OK** lần cuối. `loi-khoa.txt` = `0fdc72ce81e33b6f4efc8234a52dafc5410d4448c26c0a0feb3eb01abaa71753` |
| golden steel | **KHỚP**: pHash 0/64, SSIM **0,9449**, MAD 2,08, > 24: 0,04 %, 0/144 ô (80,3 s) |
| golden ll08 | **KHỚP**: pHash 0/64, SSIM **0,9307**, MAD 2,25, > 24: 0,01 %, 0/144 ô (149,5 s) |
| golden t1 | **LỆCH CỤC BỘ**: pHash 0/64, SSIM **0,9082**, MAD 4,51, > 24: 1,28 %, **22/144 ô** (59,0 s). `golden.py` trả mã 1 vì ca này |
| `preflight --staged` | **ĐẠT** ở cả 4 commit P (Kinh thánh, nháp D11, sổ, báo cáo) |
| `preflight --range 5b4e9187..HEAD` (riêng phần P) | **ĐẠT**, 10 tệp |
| `preflight --range origin/main..HEAD` | **TRƯỢT 1 mục**, 227 tệp: `CHẶN P4 dấu xung đột merge trong reports/g1b-t3/nguoi/giay-phep/mpfb2-LICENSE.txt`, báo nhầm có sẵn từ G1b (§1). Mục ngoại lệ P10C-1 (video V5b-2d `338cef97…`) **không còn hiện**, vì tệp đó đã nằm trên `origin/main` từ G1b bước 0. Mục P4 này không thuộc ngoại lệ P10C-1, nên **cần quyết** (§8 mục 3) |
| Email trong diff | **0**: không có địa chỉ email nào trong dòng thêm mới, cả phần P lẫn toàn dải `origin/main..HEAD`. Tác giả/người commit chỉ là địa chỉ noreply được phép |

**Golden, số trước / sau** (so `reports/p-1810c/golden.json`): cả 3 ca **trùng từng chữ số** với P-1810c: SSIM 0,9449 / 0,9307 / 0,9082; MAD 2,08 / 2,25 / 4,51; ô lệch 0 / 0 / 22. G1b có sửa `scripts/k2/` (cờ `p.sach`, khung sạch). Số đo cho thấy sửa đổi này không làm đổi khung golden; P không đọc mã để xác nhận cơ chế.

## 6. Chỉ số trong ±5 % quanh ngưỡng
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Golden t1 SSIM | 0,9082 | ≥ 0,90 | **+0,9 %** |
| Golden ll08 SSIM | 0,9307 | ≥ 0,90 | **+3,4 %** |
| Golden steel SSIM | 0,9449 | ≥ 0,90 | **+4,99 %** |
| Giờ máy P-1910 | ≈ 0,4 h | mốc 2 h | −80 % (ngoài ±5 %) |
| Nháp D11: lời ước 2,5 từ/s | 626,8–627,6 s | — (không có ngưỡng ở 2,5 từ/s) | — |

**Chỉ số trong ±5 % có trong sổ vừa ghi** (do phiên gốc tự nêu, P chép lại):
- G1b: bản xem 4,85 MiB so trần 5 MiB (−2,9 %); KB2026 9,5 s so 10 s (−5 %); thẻ phương pháp 5,0 s so "4–5 s" (0 %). Nay D6 đổi thành 2 × ≈ 8 s, nên G1b phải dựng lại thẻ.
- GIỌNG-CHỐT: phim T3 ước 744,1 s so mục tiêu ≤ 745 s (−0,1 %) và so trần 720 s (+3,35 %); loudness −13,9 LUFS, cách cận trên 0,1 LU.
- CASTING-MỸ: EL 4 970 so chặn 5 000 (−0,6 %).

**Ngoài ±5 %, nêu cho rõ:** G1b Claude $5,632 so mốc theo dõi $5 (+12,6 %); GIỌNG-CHỐT EL 4 941 so mốc theo dõi 3 000 (+64,7 %; phiên đã nêu lợi ích). Không phần tử nào được thêm để vượt ngưỡng.

## 7. Chi phí
| Mục | Lệnh | Thực tế |
|---|---|---|
| Claude API (gọi từ script) | 0 | **$0** |
| OpenAI / ElevenLabs / YouTube Data API | 0 | **$0 / 0 ký tự / 0 đơn vị** |
| Web | — | 0 (chỉ `git fetch` origin; pip/npm qua proxy để cài môi trường) |
| Giờ máy | mốc 2 h | **≈ 0,4 h** thời gian thực. Tiến trình: golden 3 ca (289,4 s; lượt đầu 286,1 s lỗi `oid`), selftest k115 + k114 (16 s), verify.sh ×2, pip/npm |
| Token | trần mềm | không đo được trong phiên |

**Môi trường:** đầu phiên `verify.sh` cho **11 PASS / 4 FAIL** (OpenEXR, three.js, tifffile/pyshp, k2v node_modules). P cài lại bằng pip vào `/opt/cine` và `npm ci` trong `design/cong3/shared`, `design/k2v`; các bước này không đổi tệp nào trong git. Sau đó **15 PASS / 0 FAIL**, Freesound cũng PASS. Golden lượt đầu báo LỖI `'oid'` vì container chưa có các nhánh `release-*` cục bộ. Sau `git fetch` 3 nhánh release, chạy lại được.

## 8. Việc chờ chủ dự án
1. **Chọn câu nối D11: A hay B** (§3; P khuyến nghị A). Sau đó phiên khoá lời tạo v4.2 và cập nhật `LOI-KHOA.sha256`.
2. **Claude điều phối rà nhánh rồi ff `main`.** Nhánh là hậu duệ thẳng của `origin/main` `5253ba2b`: `git checkout main && git merge --ff-only origin/claude/p-1910-merge-g1b-giong-chot-49iath && git push origin main`.
3. **Preflight P4 báo nhầm** ở `reports/g1b-t3/nguoi/giay-phep/mpfb2-LICENSE.txt` (dòng `=======` của giấy phép nguyên văn). Hook pre-push sẽ chặn dải này khi ff `main`. Có ba cách:
   - (a) ghi ngoại lệ một lần như P10C-1;
   - (b) phiên Nền tảng cho P4 bỏ qua dòng `=======` khi dòng trên là tiêu đề;
   - (c) đưa tệp ra ngoài git, chỉ ghi URL + SHA.
   
   P đề xuất (a) ngay, rồi (b) cho lâu dài.
4. **Kinh thánh, câu còn mâu thuẫn** (§2 cuối): §4 dòng 51 (dòng nguồn khi có con số), §10.5 (số so sánh trên hình), và quan hệ nhịp Q37 với TL-1. Nên quyết trước V7-PILOT.
5. **Nguyên văn còn thiếu:** P10C-3…5 và C2-1…C2-9.
6. **COST-LEDGER:** thêm dòng casting-giong (CASTING-GIỌNG) ở lần P kế.
7. **Giọng G1:** gửi thư Đ5 (`reports/giong-chot/hoi-elevenlabs.md`). Duyệt Đ-C (alias chữ thường) và Đ-D (d'Arçon). Chưa dùng G1 cho bản phát hành tới khi có trả lời (RIGHTS P1910-G1).
8. **G1b còn treo:**
   - D1/D1b ("midnight"), D9, D10, D12;
   - O2 nghi vấn 3f;
   - khiếu nại K 1.16 (`reports/g1b-t3/khieu-nai-K.md`);
   - SM1 tô màu 1704.
9. **Golden:** SSIM giữ nguyên như P-1810c (t1 0,9082, sát ngưỡng 0,90). Vẫn còn đề nghị của P-1810c §8 mục 6: xem sheet t1 (`/var/tmp/golden-p1910/t1/`, ngoài git) và cân nhắc chụp lại tham chiếu theo trình dựng V6.

**DỪNG — chờ chủ dự án.**
