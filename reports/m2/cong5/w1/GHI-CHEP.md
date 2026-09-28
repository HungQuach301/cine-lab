# W1 · Cổng 5 giai đoạn A — ghi chép probe

Báo cáo đầy đủ: `shots/layout/LAYOUT-W1.md`.

**Ảnh trong thư mục** (probe 960×540, thu về 480×270 mỗi ô, jpg):
- `tong-23-shot.jpg`: khung giữa của 23 shot sau layout.
- `<shot>_truoc-sau.jpg`: trái là animatic v2 (probe0), phải là layout W1.
  - Shot: s02, s07, s08, s10e, s14, s15, s19, s23, s24.
  - s10e, s14, s15, s23 lấy khung cuối (c); các shot còn lại lấy khung giữa (b).

**Nơi lưu các lượt probe** (không commit): `/var/tmp/cine-out/W1/probe0` … `probe5` (+ `w2smoke`, chỉ dữ liệu chuyển động).

| Lượt | Shot | Thời gian thật |
|---|---|---|
| probe0 | 23 (nền v2) | 335,2 s |
| probe1 | 15 | 215,5 s |
| probe2 | 23 | 381,6 s |
| probe3 | s14, s22 | 31,6 s |
| probe4 | s14, s22 | 42,8 s |
| probe5 | s05, s14, s22 | 44,8 s |
| w2smoke (`--meta-only`) | s35, s37w, s45c | 32,3 s |

Bản cuối của từng shot: probe2, trừ s05, s14, s22 lấy từ probe5.

## Giai đoạn C
- `tong-23-shot-giai-doan-C.jpg`: khung giữa 23 shot của bản render đầy đủ (s08 là bản làm lại). Ô cuối là mặt nạ mặt vôi s23 với máy giai đoạn A (29 %).
- `s23_mat-voi-chot.jpg`: s23 bản cuối cạnh mặt nạ mặt vôi của máy chốt (15,5 %).
- Thử máy s23 (mặt nạ + hình, không commit): `/var/tmp/cine-out/W1/s23try/{A..I}_{mask,img}`. Probe: `probe6` (máy cũ + cuối phố W2), `probe7` (máy chốt s23, s24, s24c), `lime` (mặt nạ máy cũ).
- Số liệu hàng đợi và làm lại: `shots/layout/LAYOUT-W1.md` mục 11.
