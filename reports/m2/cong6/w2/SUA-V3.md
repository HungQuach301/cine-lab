# W2 — LƯỢT SỬA NHỎ v3 (chủ dự án 30/09/2026)

Nhánh `cong6-w2-v3` (từ `cong6-w2-v2` @25547c1). Chỉ sửa `design/cong5/layout/shots_w2.js`. Không sửa `sets_end.js`, mã dùng chung, tài sản khoá, bible, checks.
Bảng khung 0,5 s trước/sau: `reports/m2/cong6/w2/sua-v3/{s27,s37b,s39,s45}_{truoc,sau}.jpg` ("trước" cắt từ mp4 v2, "sau" từ mp4 v3).

| Việc | Nguyên nhân / đo | Sửa |
|---|---|---|
| **a. s27** cột điện cùng mé L11 (trái luật v0.6) | Cột sân (sets_end `wallPost`, hệ tường (6,8; 2,2)) dùng chung với s23 (W1) → không dời ở `sets_end.js`. | Chỉ trong s27 (móc `onBuild` của `wallShot`, các shot cảnh 4 khác không gọi): ẩn thân cột, bóng đèn, quầng, loá (mọi vật ≤ 1,6 m quanh đầu đèn + nhóm cột); **chính PointLight của cột** dời sang mé đối diện — vỉa hè nam z_w 12,2 (hàng cột POST_Z), (7,2; 6,2; 12,2), ngoài khung phải-sau máy; bỏ giới hạn tầm, cường độ × 2,7 (độ rọi lên tường nhà kho quanh Cas cách 12–13 m ≈ như vũng cũ cách 4–5 m). Cùng nhịp bật 64,4 s, cùng màu; không thêm nguồn thứ hai. Kết quả: cột không có trong khung; từ 64,4 s trắng lạnh tràn từ mé đối diện phủ mặt tường, lấn át quầng vàng L11 (bảng `s27_sau`). |
| **b. s39** miệng chỉ có hàm, "rách" | Hàm mở tới 0,86 (viseme A × 1,15) cộng nét nghẹn frown 0,7 + chinRaise 0,5 + press + shape key sửa `corr_mouth` (frown × press/chinRaise) → môi dưới bị kéo hai hướng. | `richLip`: hàm trần 0,35; phần mở còn lại chuyển sang môi (pucker +0,2·j, wide +0,15·j, lowerLipIn nhẹ khi mở lớn), má (cheekRaise +0,25·j), cằm (chinRaise theo âm khép MBP/FV), mày trong nhích theo; khi đang nói frown/chinRaise/press giảm tới 60 % theo độ mở. Biên độ khẩu hình 1,15 → 1,0. |
| **c. s45** quay đầu giật, tay "móng vuốt" | Quay cổ đồng thời 42° ngang + 42° dọc (30° → −12°) trong 1,05 s (easeIO) → mắt thấy ≈ 90°. Ngón curl 0,2–0,3, xoè 0,05. | Cổ dọc chỉ 30° → 6° (thêm 40° ngang, thân 18°); quay 0,55–2,0 s bằng smoothstep (đỉnh ≤ 43°/s); mắt dẫn trước 0,45–0,8 s. Ngón thả lỏng: phải curl 0,45 xoè 0,14; trái curl 0,42 xoè 0,12. |
| **d. s37b** vệt "ria" trên môi trên | Khung 1920: dải tối là vùng nhân trung dưới mũi **tự che sáng** (mặt da quay xuống, key L11 cao phía trước); tắt bóng L11 (`shadow: 0`) không đổi → không phải bóng đổ, không phải shape key. | Chỉ s37b: dội từ khăn/áo lên cằm của facelight W3 (nguồn có thật) under 0,04 → 0,16 × key. Vùng dưới mũi sáng lên, hết dải tối; bóng vành mũ giữ. |

**Lệch 0 px (shot không đổi):** gốc probe tạo TRƯỚC khi sửa (`/var/tmp/cine-out/W2/lech3/goc`), so sau khi sửa (`…/lech3/sau`): s02, s23, s24c (W1) + mọi shot W2 trừ s27, s37b, s39, s45 (26 shot) — **87 ảnh; lệch 0**.

**MP4 mới** (`/var/tmp/cine-out/W2/`, 960×540, không tiếng, kèm `timing_*.json`): s27 → `video_s27.mp4`; s37b, s39 → `video_s37b-s39.mp4`; s45 → `video_s45.mp4`. Mọi shot khác giữ mp4 hiện hành của vòng 2 (BAO-CAO-W2-V2 §6).

**Ghi chú:** s25, s26, s28–s32 vẫn nhận ánh từ vị trí cột cũ (cùng mé L11, cột ngoài khung các shot đó) — không tự sửa lan rộng; nếu cần đồng bộ hướng ánh cả cảnh 4 thì là việc riêng (P/W1 cùng xử lý với s23).

**Token, thời gian:** bộ đếm công cụ ≈ 40 nghìn cho lượt v3 (hạn 150 nghìn). Thời gian thật 05:51 → ≈ 06:40 UTC 30/09/2026 (≈ 50 phút, phần lớn là render + dò lệch).
