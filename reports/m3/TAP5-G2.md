# TẬP 5 — CỔNG G2: bản cuối · 06/10/2026

**P DỪNG ở G2, chờ chủ dự án duyệt bản cuối, Shorts và thumbnail.**
- Tiêu đề đã chốt ở G1 (phương án A): "In 1966, Computers Couldn't Judge an Insurance Claim. Now Software Prices the Wreck".
- So sánh theo phương án 5B (định tính); thẻ cuối "Next: The Hand That Drew It".
- Đây là **tập đầu tiên dựng bằng Thư viện HÌNH v2** (quyết định G2 tập 4, 06/10/2026) và tập thứ hai áp luật nhịp Q14–Q18.
- Dựng bằng nhà máy: `reports/m3/ep05/episode.yaml` (v4), `scripts/ll/build.sh`, kiểm bằng `scripts/ll/qc.sh`.
- Mọi số dưới đây là số đo thật trên tệp.

## 1. Bàn giao
| Tệp | Thông số | Dung lượng | SHA-256 |
|---|---|---|---|
| Master (Git LFS, nhánh **`release-ll-ep05-v1`**, commit `@REL@`): `ll-ep05-v1-master-1080p.mp4` | 1920×1080, 24 fps, **8:32,5** (12 301 khung) | @MSZ@ MB | `@MSHA@` |
| `screening/ll-ep05-v1-p1.mp4` | phần 1, 720p | @P1@ | `@P1S@` |
| `screening/ll-ep05-v1-p2.mp4` | phần 2 | @P2@ | `@P2S@` |
| `screening/ll-ep05-v1-p3.mp4` | phần 3 | @P3@ | `@P3S@` |
| Shorts S1/S2/S3 (LFS, cùng nhánh) | 1080×1920; 25,1 / 27,0 / 23,3 s | @SSZ@ | `SHA256SUMS.txt` của nhánh |
| Thumbnail T1, T2 · mô tả (14 chương) · text Shorts · phụ đề `.srt` | cùng nhánh và `reports/m3/ep05/phat-hanh/` | | |

- **Kiểm sau khi đẩy:** @VERIFY@
- Khung tổng quan (33 shot): `reports/m3/ep05/khung-g2.jpg`. Bảng khán giả (tự sinh): `reports/m3/ep05/KHAN-GIA.md`.

## 2. Kết quả `qc.sh` lượt cuối: **@QCRES@** (bảng đầy đủ: `reports/m3/ep05/qc-g2.md`)
| Mục | Giá trị |
|---|---|
| Q1–Q3 judder, khung gần trùng, máy xuyên hình | 0 · 0 · 0 |
| Q4 loudness / true peak | @Q4@ |
| Q5 tương phản thấp nhất | @Q5@ |
| Q6 cỡ chữ hoa tối thiểu | 30,7 px (Short S1, nhãn "PROJECTION") |
| Q7–Q13 | ĐẠT (0 lỗi; 12 301/12 301 khung; phần ≤ 90 MB; T1/T2 lề 5 %; số trên tiêu đề, thumbnail, mô tả, Shorts truy được về `numbers`) |
| **Q14 móc câu** | câu hỏi "Who decides what a damaged car is worth?" và hình giám định xe trước 0:15; **tựa ở 0:19,8**; trả lời ở đoạn 11 ("The line is moving") |
| **Q15 đổi hình** | quãng dài nhất **7,9 s**, trung bình **2,8 s** |
| **Q16 thẻ giấy** | **15,5 %** (trần 55 %) |
| **Q17 mật độ số** | **11 số / 8,5 phút = 1,29/phút**. Neo: two-thirds (1963) · −5 % (2025–35) · −9 % (2025–35) |
| **Q18 thẻ trống** | 0 |
| **Q19 hồ sơ quyền tư liệu** | ĐẠT: 4 ảnh LoC, 84,5 s = **16,5 %** (trần 20 %), cả 4 có dòng RIGHTS |
| **Q20 chữ đè hình** (mới, từ test va chạm isotype) | 0 khung |

**Chỉ số trong ±5 % quanh ngưỡng:**
- Q14: tựa ở 19,8 s (ngưỡng 20 s, cách 1 %);
- Q15: quãng dài nhất 7,9 s (ngưỡng 8 s, cách 1,3 %);
- Q6: cỡ chữ Short 30,7 px (ngưỡng 30 px).
- Tỷ lệ STORY/HISTORY/TODAY 19,5 / 37,5 / 43,0 %: cả ba trong ±5 điểm, không mục nào sát biên.

### 2.1 So với tập 4 (cùng `rhythm.py`, timeline thật)
| | Tập 4 (HÌNH v1 + luật nhịp) | Tập 5 (HÌNH v2 + luật nhịp) |
|---|---|---|
| Thời lượng | 8:34,7 | 8:32,5 |
| Tựa phim | 0:18,6 | 0:19,8 |
| Quãng không đổi hình dài nhất / TB | 8,0 s / 3,0 s | **7,9 s / 2,8 s** |
| Thẻ giấy (Q16) | 32,1 % | **15,5 %** |
| Mật độ số (Q17) | 15 số, 1,75/phút | **11 số, 1,29/phút** |
| Thẻ trống > 1,5 s (Q18) | 0 | 0 |
| Tư liệu phạm vi công cộng | 0 | 84,5 s (16,5 %) |
| Q5 tương phản thấp nhất | 5,79:1 | @Q5S@ |

- Thẻ giấy giảm một nửa: cảnh `desk` (1963 → 1988 → 2025 trên cùng một bàn), `inspect`, `isotype`, `sign` và tư liệu LoC thay phần lớn thẻ trích dẫn. Còn 6 thẻ trích dẫn BLS, giữ vì lời trích nguyên văn là chứng cứ chính của tập.
- Tựa muộn hơn tập 4 1,2 s, vẫn trong ngưỡng.

**Lỗi bắt được trong lúc sản xuất (đã sửa trước khi giao):**
1. **Q1 judder 221 quãng** ở cảnh tĩnh v2. Đã thêm `alive()` (bụi + hạt phim mỗi khung) vào thư viện.
2. **Q4:** true peak phần bản xem +0,4 dBTP. Đã hạ bản xem 1,2 dB và thêm `alimiter` trong `build.sh`.
3. **Q5** (4 lần):
   - chữ biển hiệu vẽ khi chưa sơn (a = 0);
   - nhãn rỗng của `desk`;
   - nhãn thời kỳ S2 nằm dưới chữ hook;
   - chú thích biển hiệu S3 dưới dải cap: tương phản 1,83:1, đã chuyển vào dải cap.
4. **Q13:** số "193" (NAIC) trong Shorts chưa có trong `numbers`. Đã thêm `naic_n`.
5. **Tư liệu:** Ken Burns cắt mất chiếc xe trong ảnh tai nạn 1936. Đã thêm tham số `focus`. Dòng nguồn ảnh bị dải cap che, đã đặt sang phải trên dải.
6. **Phụ đề đè hàng isotype 1950** (lỗi lát cắt v2 chủ dự án chỉ ra):
   - isotype giữ chỗ dải chú thích khi có cap;
   - test va chạm chữ–hình trong `scripts/ll/tests`;
   - qc Q20 đọc cờ va chạm từ log render.
7. **Test thư viện chặn build đúng:** một chú thích `//` chèn giữa dòng làm hỏng `shot.js`. Build dừng ở bước test (mã 5), đã sửa trước khi render.
8. **P tự phát hiện khi rà khung tổng quan:** dòng nguồn ở cảnh isotype đoạn 07 tràn mép phải ("…Handbook (2025–35): Claims" bị cắt). Đã rút gọn nhãn nguồn EP thành "BLS Employment Projections" và render lại đoạn 07. qc hiện chưa đo được lỗi này: xem hàng chờ 1.

## 3. Nội dung, tỷ lệ, kiểm mù
- **Thời lượng 8:32,5. Tỷ lệ 19,5 / 37,5 / 43,0 %.**
- **Kiểm mù** (1 subagent Sonnet, 3 vai, 50,7 nghìn token, chỉ nhận lời phim, trước khi thu giọng). Điểm có ≥ 2/3 vai cùng nêu đã sửa:
  - đoạn 03 gọn lại, bỏ thẻ 17 hãng;
  - đoạn 00 nói rõ "drafts the estimate";
  - đoạn 06 thêm "for decades";
  - đoạn 10 kết "the final call still sits with people".
- **ASR:** mọi đoạn và 3 Shorts ĐẠT ở lần thu đầu, không thu lại.

## 4. HÌNH v2 trên tập 5
| Mẫu | Số shot | Thời lượng | Dùng cho |
|---|---|---|---|
| `desk` (đổi thời kỳ 1963 → 1988 → 2025, nhân vật vô danh khăn đỏ) | 10 | 173,3 s | sợi chỉ của cả tập: cùng một bàn bồi thường qua ba thời kỳ |
| `inspect` (giám định viên + xe móp; 1988 máy ảnh, 2025 điện thoại + "AUTOMATED ESTIMATE") | 4 | 91,4 s | móc câu, đoạn 05b, 08, 10 |
| `archive` (tư liệu LoC, Ken Burns + tông B3) | 4 | 84,5 s | văn phòng bảo hiểm 1941/1943, phòng máy IBM 1967, tai nạn xe 1936 |
| `isotype` (hàng hình người) | 2 | 21,9 s | nhân viên đơn vị máy tính 1954–63; giám định viên 2025 ↔ 2035 |
| `sign` (số sơn trên biển) | 2 | 18,2 s | +31,5 % (1954–63) · 88 % (NAIC 2022) |
| `quote` · `street` · `text` · `endcard` | 6 · 3 · 1 · 1 | 76,5 · 37,6 · 3,0 · 6,1 s | trích dẫn BLS nguyên văn; cầu nối người thắp đèn |
- **Đạo cụ:** bàn bồi thường, xe móp, máy ảnh, hồ sơ bồi thường (đóng dấu), điện thoại, màn hình terminal 1988, laptop 2025.
- **Tư liệu phạm vi công cộng:** chỉ từ danh sách trắng (loc.gov, "No known restrictions on publication"). 4 dòng RIGHTS: `LOC-8d27894`, `LOC-8c01946`, `LOC-8b28380`, `LOC-89395`. Mỗi ảnh có chuyển động máy, tông B3 và dòng nguồn trên hình. Mô tả YouTube ghi nguồn ảnh.

## 5. Token, ElevenLabs, giờ máy, đĩa
| Phần | Token | Nguồn số |
|---|---|---|
| Kiểm mù (1 subagent, 3 vai) | 50,7 nghìn | harness |
| P: HÌNH v2 cho tập 5 (inspect, đạo cụ, focus, Q20), đặc tả v4, thu giọng, 8 lượt build/qc, phát hành, báo cáo | ≈ 0,25 triệu | ước |
| **Tổng tập 5** | **≈ 0,3 triệu / trần 0,5 triệu (≈ 60 %)** | ước |
- **ElevenLabs:** bộ đếm tài khoản 27 538 → **33 386** (+5 848 ký tự, gồm lời phim và 3 Shorts; không thu lại lần nào).
- **Giờ máy:** 8 lượt build (phần lớn chỉ dựng lại đoạn/Short hỏng nhờ băm đoạn), 8 lượt qc.
- **Đĩa:** @DISK@. Trung gian `/var/tmp/cine-out/ll-ep05` giữ đến khi G2 duyệt.

## 6. Hàng chờ nhỏ (không chặn G2)
1. **Chữ tràn khung chưa có qc.** Lỗi mục 2.8 do P thấy bằng mắt. Đề xuất:
   - `srcLine`/`text` tự thu cỡ khi vượt bề ngang an toàn (đặt sàn cỡ chữ);
   - test thư viện + qc đo hộp chữ vượt khung.
   - Sửa thư viện làm đổi băm, nên mọi đoạn của tập sau đều render lại; làm ở lượt chạm thư viện tới.
2. Thẻ trích dẫn (`quote`) còn 6 thẻ. Có thể thay 1–2 thẻ bằng cảnh `desk` + chú thích nếu chủ dự án muốn giảm thêm thẻ giấy. Không làm khi chưa có quyết định, vì lời trích nguyên văn là chứng cứ.
3. Hàng chờ từ tập 4 (tư thế tay ở mẫu `rows`) chưa đụng tới, vì tập 5 không dùng `rows`.

## 7. Chờ chủ dự án — CỔNG G2 tập 5
1. **Duyệt bản cuối:** xem `screening/ll-ep05-v1-p1/p2/p3.mp4`. Master trên nhánh `release-ll-ep05-v1`, SHA `@MSHORT@`.
2. **Duyệt 3 Shorts:**
   - S1 "Software that drafts the estimate for a wrecked car";
   - S2 "1966: the computer couldn't judge. 2026?";
   - S3 "88% of auto insurers — use, plan, or explore AI".
3. **Chọn thumbnail:**
   - T1: giám định viên chụp xe móp (cảnh `inspect`, v2) + tiêu đề A;
   - T2: biển hiệu "−9 %" + "BLS PROJECTION".
   - P đề xuất T1, thử A/B với T2.
4. **Hàng chờ 1:** duyệt hướng thêm kiểm chữ tràn khung (thư viện + qc) cho tập sau.
5. **Sau G2:** P chuẩn bị G3 như tập 4 (hướng dẫn đăng, Altered content = No, RIGHTS tư liệu đã có, xoá trung gian).
