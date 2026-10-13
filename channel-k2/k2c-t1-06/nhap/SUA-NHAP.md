# K2C-T1-06 · nháp 960×540 → một lượt sửa (13/10/2026, phiên P)

Nháp: master 15:41 (22 585 khung), −14,0 LUFS / −1,6 dBTP, 2 Short. SHA không ghi (nháp, không LFS). QC nhà máy: `qc-nhap.md`. Tờ khung (1 khung giữa mỗi shot): `TO-KHUNG-NHAP-1…5.jpg`.

## A. Lỗi máy bắt (qc.py, edge_check.py, công cụ K)
| Mục | Lỗi | Sửa |
|---|---|---|
| Q2 | 05 f_fire: khung trùng theo chu kỳ 5 (clip Pexels 24p nhồi vào 29,97) | `hero.js` footage `decimate: true` (bộ lọc `decimate=cycle=5` trước `fps=24`); dựng thử 209 khung: 0 khung trùng |
| Q5 | 09 thẻ "Not covered…" màu #9AA7B5 đo 4,14 | mọi chữ phụ #9AA7B5 → #B8C2CE |
| Q10 | 3 phần bản xem 720p > 90 MB | bản cuối không làm 3 phần (PARTS=0, như K2G-01); gói phát hành kênh 2 không cần |
| Q13 | hook S1 "1 in 13 … 1 in 100" không truy về numbers (số khai theo %) | hook viết bằng chữ đúng cụm `say` của c01/c02 ("One in thirteen homes — but one in a hundred new ones. Why?") |
| Q21 (38) | `src` dạng chuỗi tự do (bản đồ, ảnh, footage, dòng gõ tay) → ll.py không gộp nguồn của số/câu | `make_spec.py`: chuỗi → khoá nguồn thật (bản ghi ảnh LoC/Pexels của đúng tệp; MAPC = NASA Blue Marble), "3D illustration"/"our calculation" → `credit` nối cuối dòng nguồn; câu chưa khai nguồn trong shot có danh sách nguồn → nguồn của shot. Còn 0 |
| Q22 + mép 48 px | 07 dòng thẻ dài; S1 nhãn; S2 thẻ kết "THE CORNER BUILDING" tràn 197 px | thẻ kết tự co (`maxW`); nhãn S1 rút gọn chữ (nghĩa giữ); thẻ 07 cỡ chữ riêng |
| Q23 (10) | c26 `say: "four"` khớp mọi chữ "four"; c18/c50 cùng `say: "six stories"` | `say` đúng cụm trong lời ("a line: four"; "them up to six stories"; "buildings up to six stories"); đoạn 10 tách số c26c ("still four"). Còn 0 |
| Q14–Q18 | luật nhịp LL bật vì mã tập "06" bị đọc là "tập 6" | ghi nhận, không sửa: kênh 2 không áp luật nhịp LL (K2G-01 G2 §5.1 "không áp"). Q17 (anchors đúng 3) mâu thuẫn Q34 kênh 2 (anchors = mọi số neo) |

## B. Lỗi mắt thấy trên tờ khung (máy không bắt)
| Shot | Lỗi | Sửa |
|---|---|---|
| dải chú thích có số lớn (01/5, 02/2, 02/8, 09/9) | câu 2 dòng đè dòng nguồn 2 dòng | `caps()` tính chiều cao khối chữ, đẩy cả khối lên cho dòng cuối cách đỉnh dòng nguồn ≥ 18 px |
| `credit` | "Data: our calculation" đè nhãn ACTUAL góc phải | credit nối vào cuối dòng nguồn |
| Short 9:16 | nhãn ACTUAL đè dòng nguồn 2 dòng | nhãn lên trên dải chú thích, giữa khung; nguồn Short dùng nhãn gọn `short9` |
| 07 thẻ TO RECAP | 5 mục tràn đáy thẻ | thẻ list nhận `top`; mục 4 gộp một dòng; px 34, gap 30 |
| 04 ch_pew | biểu đồ trống 13 s trong lúc lời giới thiệu Pew | `sa_plan` giữ qua câu Pew; góc mới `sa_corr` (stairs, `corridor_side`) cho câu "a group that advocates…"; `ch_pew` vào ở "@extra" |
| ch_terner, ch_small, s_hook | crane-up: cột bị cắt đỉnh; phối cảnh làm cột 110 trông thấp hơn cột 100 | `front-dolly` nhìn thẳng, scale vừa khung |
| ch_icc | cột cắt đỉnh, KHÔNG có nhãn số: id `yes`/`no` bị YAML đọc thành boolean → neo `true:top` | id `yea`/`nay`; scale 0,045; đã quét: 0 id boolean khác |
| ch_mpls | cột chồng cắt đỉnh; nhãn 317 đè câu chú thích | `front-dolly`, scale 0,00035; `tags()` 16:9 chặn ở đỉnh dải chú thích |
| ch_study | top-down: một cột lệch mép | `front-dolly` |
| ch_pew, ch_terner (đầu/cuối máy chạy) | khối đen góc bo ở mép khung = đầu mút tường cong studio (±1,5·size) | `design/k2v/common.js`: tường ±6·size, cao 1,5·size; sàn 12·size (ô lưới giữ cỡ) |
| 07 lo_pencil | 11 s chỉ có lô đất trống: `grow: -1` → NaN → toà biến mất | `lot()`: grow số âm = đủ từ đầu; góc `pencil` nhìn từ bãi đỗ (mặt có cửa sổ + mái che) |
| 06 d_cfr | tilt-low: trang nhỏ, thấp, không đọc được | góc `detail` (như d_ibc) |

## C. Đổi mã dùng chung (ảnh hưởng ngoài tập)
- `scripts/k2/hero.js`: footage trích theo số khung (`-t N/24 + 0,1`, trước đây thiếu 1 khung khi dur×24 lẻ) + `decimate`.
- `scripts/k2/lib/k2.js`: `caps()` khối chữ nhường dòng nguồn; credit vào dòng nguồn; thẻ kết `maxW`; thẻ list `top`; `tags()` chặn ở đỉnh dải chú thích (16:9); nhãn loại 9:16 trên dải chú thích.
- `design/k2v/common.js`: tường/sàn studio rộng hơn (mọi biểu đồ k2v). Steel đã phát hành không bị ảnh hưởng (chỉ khi dựng lại).
- `design/ll-hero/k2c106.js`: `lot()` grow âm; preset `pencil` mới, `corridor_side` mới.
- Mọi stamp cảnh đinh đổi → bản 1080p dựng lại toàn bộ (đằng nào cũng dựng lại ở 1080p).

## D. Kiểm lại trên đặc tả sau sửa (timeline nháp)
Q26b ĐẠT (35 bối cảnh, lớn nhất chart3d/bars 16,5 %, liên tục dài nhất 55,5 s) · Q32 ĐẠT (14,0 %; sát ngưỡng: PX-20568183 7,93 s / 8 s) · Q33 ĐẠT (0 góc > 2) · Q34 ĐẠT · Q21 0 · Q23 0 · test_k2v 9/9. Khung sửa được dựng thử từng điểm (lớp chữ bằng `render.js --only`, cảnh 3D bằng `hero.js` 960×540).
