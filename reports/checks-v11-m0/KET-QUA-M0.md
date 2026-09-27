# Kết quả bộ luật L1 v1.1 trên media M0 (phiên K)

- Luật: `checks/` trên nhánh `checks/v1.1`, VERSION 1.1.0, LOCK `d97f9b017ea2efd89be98dbecfeeb0e3d57ff44f9cfe26172703da3f1b975c3f`. Mọi báo cáo ghi LOCK khớp.
- Media: toàn bộ 9 file `reports/m0/media/*.mp4` lấy từ `origin/main`, profile `shot`, không có file đi kèm (M0 là bài đo tốc độ render, không xuất sidecar).
- Tái lập: `bash reports/checks-v11-m0/run_m0.sh` (mất 2 phút 28 giây trên 4 vCPU, chạy song song với selftest).
- Báo cáo máy đọc và người đọc nằm trong `media/<tên>/` và `minh-hoa/<phép thử>/`.

## 1. Chín file media M0

Kết luận chung của cả 9 file: **TRƯỢT**, không đổi so với v1.

| File | N1 | N2 | P0 | G3 (banding, ngưỡng ≤ 0,2%) | G3b (σ grain ≥ 0,8; tương quan ≤ 0,5) |
|---|---|---|---|---|---|
| a-2d-mb1 | ĐẠT | ĐẠT | ĐẠT | **TRƯỢT** 2,41% | **TRƯỢT** σ 0,35; tương quan 0,84 |
| a-2d-mb8 | ĐẠT | ĐẠT | ĐẠT | **TRƯỢT** 2,32% | **TRƯỢT** σ 0,35; tương quan 0,86 |
| b-3d-mb1 | ĐẠT | ĐẠT | ĐẠT | **TRƯỢT** 17,23% | **TRƯỢT** σ 0,013; CV 0,80; tương quan 0,60 |
| b-3d-mb8 | ĐẠT | ĐẠT | ĐẠT | **TRƯỢT** 18,45% | **TRƯỢT** σ 0,013; CV 0,85; tương quan 0,62 |
| c-eevee-mb1-1s | ĐẠT | ĐẠT | ĐẠT | **TRƯỢT** 14,82% | **TRƯỢT** σ 0,32; tương quan 0,71 |
| c-eevee-mb8-6f | ĐẠT | ĐẠT | ĐẠT | **TRƯỢT** 16,80% | **TRƯỢT** σ 0,15; CV 0,52 |
| c-wb-mb1 | ĐẠT | ĐẠT | ĐẠT | **TRƯỢT** 0,35% | **TRƯỢT** σ 0,26 |
| c-wb-mb8-1s | ĐẠT | ĐẠT | ĐẠT | **TRƯỢT** 0,61% | **TRƯỢT** σ 0,18 |
| SO-SANH-PHONG-CACH | ĐẠT | ĐẠT | **TRƯỢT**: 84 vùng chữ không matte | **TRƯỢT** 6,51% | **TRƯỢT** σ 0,17 |

- Các luật cần file đi kèm (J1, J1b, H1, H1b, C3, P1, G4, O3) báo THIẾU. N3, M1 không áp cho profile `shot`. M3 không có âm.
- Thay đổi v1.1 không làm đổi kết quả nào trên 9 file:
  - Không file nào có matte chữ, nên không có phần tử diegetic để xét.
  - Không file nào là master YouTube, nên quy tắc bitrate theo grain của N3 không áp.
  - Không file nào có mặt nạ C3.

## 2. Minh hoạ của v1, chạy lại bằng luật v1.1

| Phép thử | Luật | v1 | v1.1 | Ý nghĩa |
|---|---|---|---|---|
| a-2d-mb8 + chuyển động phiên K dựng lại (đúng) | H1, H1b | ĐẠT (91,1%) | ĐẠT (91,1%) | Không đổi |
| a-2d-mb8 + bản khai giả | H1, H1b | H1b TRƯỢT 0% | H1b TRƯỢT 0% | Không đổi |
| Shot A (đầu 58 px), mặt nạ M0 **1×** | C3 | TRƯỢT: không chứng minh được (biên trên 3,04%) | **TRƯỢT: hệ số mặt nạ 1× < 2** (và vẫn biên trên 3,04%) | Q-C3 có hiệu lực |
| Shot B (đầu 146 px), mặt nạ M0 **1×** | C3 | ĐẠT (lệch 0,84%, U ≤ 1,05%) | **TRƯỢT: hệ số mặt nạ 1× < 2**. Tỷ lệ vẫn đạt (biên trên 1,83%) | Q-C3: mặt nạ 1× không còn được chấp nhận, kể cả khi tỷ lệ đúng |

Phiên K không render lại mặt nạ M0 ở 4×, vì việc đó là dựng, thuộc phiên xưởng. Selftest đã chứng minh trên mẫu tổng hợp: cùng cấu hình shot A (đầu 57 px, thân +2%) với mặt nạ 4× thì **chứng minh được ĐẠT** (biên trên 2,52% < 3%, pha biên 0,26 ≈ trải đều 0,25).

## 3. Chỉ số trong ±5% quanh ngưỡng (luật cứng CLAUDE.md)

- G3b, SO-SANH-PHONG-CACH: tương quan khung kề 0,516 (ngưỡng ≤ 0,50).
- G3b, c-eevee-mb1-1s: CV σ theo thời gian 0,197 (ngưỡng ≤ 0,20).
- G3b, c-wb-mb8-1s: CV σ theo thời gian 0,206 (ngưỡng ≤ 0,20).
- C3, shot A: biên trên |lệch| + U = 3,04% (ngưỡng ≤ 3%).
- H1b, a-2d dữ liệu đúng: tỷ lệ khớp track đầu 91,1% (ngưỡng ≥ 90%).
- Selftest v1.1, chạy đầu–cuối:
  - M1 −14,5 LUFS (dải −15…−13).
  - C3 hệ số mặt nạ đo 2,0 (ngưỡng ≥ 2): mẫu cố ý dùng đúng mức tối thiểu. Mọi ca mặt nạ 2× cũng nằm đúng biên này.
- Tham khảo, ngoài vùng ±5%:
  - C3 mặt nạ 4×, đầu 57 px, thân +2%: biên trên 2,52% (ngưỡng ≤ 3%).
  - C3 mặt nạ 3×: pha biên 0,34 (trải đều ≈ 0,33; ngưỡng 0,67). Lần chạy đầu đo 0,59 do lỗi làm tròn số thực ở pha 1/3; đã sửa trước khi khoá LOCK.
  - N3: cùng nội dung có grain σ 2,5 mã RGB, G3b đo σ 1,23 ở 14 Mbps và σ 1,83 ở 36 Mbps (bộ mã ở bitrate thấp xoá bớt grain).
