# Kết quả bộ luật L1 v1 trên media M0 (phiên K)

- Luật: `checks/` nhánh `checks/v1`, LOCK `b86c5d75f14abe5cba7b08c58c95c36e0c1fc49f73af030357f9cc95db7268f8`.
- Media lấy từ `origin/main` (P đã merge M0). Tái lập: `bash reports/checks-v1-m0/run_m0.sh`.
- Mọi báo cáo máy đọc/người đọc nằm trong thư mục con cùng tên.

## 1. Hai file M0 được giao (profile `shot`, không có file đi kèm)

M0 là bài đo tốc độ render: không có âm, không xuất matte chữ, dữ liệu chuyển động, stem hay mặt nạ. Các luật cần file đi kèm báo THIẾU; kết luận vẫn là TRƯỢT vì có luật Chặn trượt.

| Luật | b-3d-mb8 (three.js) | a-2d-mb8 (Canvas 2D) | Ghi chú |
|---|---|---|---|
| N1 | ĐẠT | ĐẠT | 240 khung, 24/1, 0 hở, 0 trùng |
| N2 | ĐẠT (ngoài dải 0,046%) | ĐẠT (0%) | |
| **P0** (mới) | ĐẠT: 0 chữ; 64 vùng nghi bị loại | ĐẠT: 0 chữ; 68 vùng nghi bị loại, 1 khối đặc bị loại | Bản đầu của P0 báo nhầm khung 204 (lưới cửa sổ đọc thành "8818"); đã sửa luật, thêm ca hồi quy |
| G3 | **TRƯỢT** 18,45% khung banding (ngưỡng 0,2%) | **TRƯỢT** 2,32% | Trời và vũng sáng 8 bit không dither |
| **G3b** (mới) | **TRƯỢT**: σ grain 0,013 mã (ngưỡng ≥ 0,8), CV 0,85, tương quan khung kề 0,62 | **TRƯỢT**: σ 0,347, tương quan khung kề 0,86 (phần dư đứng yên, không phải grain) | Cả hai bản không có grain |
| J1, J1b, H1, H1b, C3, P1, G4, O3 | THIẾU | THIẾU | Không có file đi kèm |
| M3 | — (không có âm) | — | |

Lỗi thật bắt được: **banding** (G3) và **không có grain** (G3b) ở cả hai phong cách. Khớp nhận định trong BAO-CAO-M0 mục 7 rằng (b) cần shader có grain/dither.

## 2. Minh hoạ trên hình render thật của M0

| Phép thử | Luật | Kết quả | Ý nghĩa |
|---|---|---|---|
| `SO-SANH-PHONG-CACH.mp4` (nhãn chữ burn-in, không matte) | P0 | **TRƯỢT**: 84 vùng chữ không matte (4 nhãn × 21 khung mẫu), đọc đúng nguyên văn, ví dụ "(a) 2D Canvas - blur 8 mau - 42 s/s" | Đúng lỗ hổng 2 của v0: P1/G4 không thấy chữ không có matte |
| a-2d-mb8 + dữ liệu chuyển động **phiên K dựng lại** từ `scene2d.js` (không phải render xuất) | H1, H1b | ĐẠT. H1b: track ngực khớp 100%, track đầu **91,1% (sát ngưỡng 90%)** | Luồng quang học yếu trên mảng màu phẳng (đầu nhân vật) |
| Cùng file, bản khai **giả** (easing khởi bước 1 s, render thật đi đều) | H1, H1b | H1 **ĐẠT** (bị lừa), H1b **TRƯỢT** 0% cặp khung khớp, lệch trung vị 10 px | H1b bắt được dữ liệu bake không khớp hình |
| Mặt nạ + khung render shot A (đầu 58 px) | C3 | **TRƯỢT – không chứng minh được**: thân lệch −1,09%, U 1,95%, biên trên **3,04% (sát ngưỡng 3%)** | Nhiễu đo ở toàn cảnh ăn gần hết biên 3% |
| Mặt nạ + khung render shot B (đầu 146 px) | C3 | ĐẠT: lệch lớn nhất 0,84%, U ≤ 1,05%; độ khớp biên 4,4 | Cùng thiết kế, đủ độ phân giải thì chứng minh được |

## 3. Chỉ số trong ±5% quanh ngưỡng (luật cứng CLAUDE.md)
- H1b, minh hoạ a-2d dữ liệu đúng: tỷ lệ khớp track đầu 91,1% (ngưỡng ≥ 90%).
- C3, shot A: biên trên |lệch| + U = 3,04% (ngưỡng ≤ 3%).
- Selftest đầu–cuối: M1 −14,5 LUFS (dải −15…−13, sát biên dưới).
