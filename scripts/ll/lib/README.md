# Thư viện mẫu Last Lamplighters (`scripts/ll/lib/`)

Mỗi mẫu có: ảnh xem trước (khung test `tests/tpl.yaml`, `preview/<mẫu>.jpg`), tham số chính, tiêu chí nhận và các tập đã dùng.
- Test tự động: `bash scripts/ll/tests/run.sh`. So khung với `tests/ref/`; `--update` ghi lại tham chiếu sau khi sửa mẫu có chủ ý.
- **Luật:** chỉ viết thành script khi một việc đã làm tay từ **3 lần** (chủ dự án, 05/10/2026).

## Mẫu đồ hoạ (`charts.js`)
| Mẫu | Xem trước | Tham số chính | Tiêu chí nhận | Tập đã dùng |
|---|---|---|---|---|
| `text` | ![](preview/text.jpg) | `lines[{s, px, at, serif, color}]`, `beats`, `align`, `lh`, `lamp`, `src` | mỗi dòng neo vào một từ; không đứng > 3 s (Q11) | 1–5 |
| `bars` | ![](preview/bars.jpg) | `bars[{label, num, at, echo}]`, `unit`, `max`, `d`, `kindEach`, `note/noteAt`, `beats` | trục từ 0; nhãn ACTUAL/PROJECTION từng cột (`kindEach`); số dự báo gạch chéo | 1–5 |
| `line` | ![](preview/line.jpg) | `series[{points, labels, ltext, lpos, proj_from, name}]`, `xr`, `xticks`, `ymax`, `yfmt: k`, `marks[{x, label, at}]`, `at`, `dur` | đổi phân loại thì **hai series riêng + `marks`** (không nối); `lpos: below` khi hai nhãn trùng x | 1–4 |
| `bignum` | ![](preview/bignum.jpg) | `num` hoặc `value/text`, `prefix/suffix`, `d`, `caption/capAt`, `icon`, `beats`, `kind` | loại số lấy từ `nums`; khoảng số (`range`, `"50–80…"`) hiện thẳng, không đếm | 1–5 |
| `bignum` (khoảng) | ![](preview/range.jpg) | `value: [a, b]` hoặc `text: "50–80% fewer"` | như trên | 2 |
| `compare` | ![](preview/compare.jpg) | `left/right{title, years, num, at, icon}`, `mid/midAt`, `diff/diffAt` | hai vế cùng đơn vị (ll.py chặn); **chỉ dùng khi cùng cơ chế và cùng kỳ** (BAI-HOC #17) | 2 |
| `quote` | ![](preview/quote.jpg) | `text`, `who`, `where`, `at`, `beats` | nguyên văn; Shorts ≤ ~12 từ mỗi thẻ (BAI-HOC #6) | 1–5 |
| `map` | — | `city`, `year`, `groups` | phố không vượt nước; chỉ cầu có năm ≤ năm bản đồ | 1 |

## Mẫu cảnh (`scenes.js`)
| Mẫu | Xem trước | Tham số chính | Tiêu chí nhận | Tập đã dùng |
|---|---|---|---|---|
| `street` | ![](preview/street.jpg) | `lamps[{x, lit}]`, `lighter{from, to, walk, lights}`, `warm`, `windows`, `cam` | ≥ 3 lớp parallax; người thắp đèn vô danh, không cận mặt | 1–5 |
| `office` | ![](preview/office.jpg) | `light`, `cam` | đèn bật dần theo lời | 2–5 |
| `rows` switchboard | ![](preview/switchboard.jpg) | `rows`, `per`, `dim`, `screen`, `screenLabel`, `cam` | đèn giắc tắt dần; màn hình "AUTOMATED VOICE" | 2 |
| `rows` typing | ![](preview/typing.jpg) | như trên | đèn bàn tắt dần từ trái | 4–5 |
| `rows` teller (`TPL.teller`) | ![](preview/teller.jpg) | `per`, `dim`, `screen` (ATM), `look` (ô giữa ngẩng lên), `customer{at, nervous}` | nhãn ATM ≥ 4,5:1 (nền `#0c1a2b`, chữ đậm, quầng ≤ 0,2) | 3 |
| `endcard` | ![](preview/endcard.jpg) | `line`, `next` | thẻ kết hẹn tập sau | 1–5 |

## Đã trượt — không dùng lại
| Cách làm | Trượt ở | Thay bằng |
|---|---|---|
| Khung đồ hoạ chỉ có tựa/trục khi lời đang nói | tập 1 L1; tập 2: 43 quãng > 3 s | `beats` neo vào từ; `ll.py est` báo trước |
| Một đường nối qua hai cách phân loại nghề | tập 1 L2; tập 3: biểu đồ HSUS D355 (sửa sau G2) | hai `series` + `marks` "classification changes" |
| Hai đợt dự báo trên một khung | tập 1 L4 | hai khung, ghi đợt |
| `bignum` đếm qua số trung gian của khoảng | tập 2 (50–80 %) | `range` |
| Nhãn ACTUAL cứng trong `bignum` | tập 2 Short S2 | `kind` từ `nums` |
| Nhãn "0", PROJECTION ở góc tối | tập 2 (< 4,5:1) | nền giấy + chữ đậm; giảm góc tối ánh rọi |
| Chữ sáng trên màn hình phát sáng + quầng 0,35 | tập 3 "ATM" 4,15:1 | nền tối, quầng 0,2 |
| Câu trích dài trong 9:16 | tập 3 S3 (tương phản 1:1, tràn) | tách thẻ trích ngắn |
| Thẻ `compare` xưa ↔ nay khác kỳ/khác cơ chế | tập 3 (+87 % 1960–70 ↔ −13 %), tập 4 (+69 % ↔ −2 %), tập 5 (bỏ ở G1) | thẻ `bars` cùng nguồn, cùng kỳ; lịch sử làm bối cảnh |
| Mốc `@từ` trùng lần xuất hiện đầu | tập 2 "@many", tập 3 "@fewer", tập 4 "@tasks" | `#2` hoặc từ khác; `ll.py est` |
| Thumbnail không lề | tập 2 T1 cắt chữ | `thumb.py` lề 5 %, qc Q12 |
