# ƯỚC GIỜ MÁY THEO LOOK — thay số trong `reports/tien-ky-t4/UOC-VA-GHIM.md` (LOOK-T4, 23/10/2026)

> Phiên LOOK-T4 không được sửa `reports/tien-ky-t4/**` (ngoài vùng giao) → các dòng lệch > 20 % ghi THAY ở đây; phiên P chép sang UOC-VA-GHIM khi merge. Số đo: `reports/look-t4/LOOK-T4-BAO-CAO.md` §6.

| Dòng UOC-VA-GHIM §2 | Cũ | Mới (đo ở chất lượng look) | Lý do |
|---|---|---|---|
| Nướng ánh sáng (lightmap theo mốc) | 6–8 mốc × ≈ 40 phút ≈ 5 h | 6–8 mốc × ≈ 100 s ≈ **0,2 h** (Cycles CPU, 1 m/texel, 32 spp, hộp 3,2 × 2,3 km) | đo 86–108 s/mốc; không cần GPU |
| Tổng giờ máy container | ≈ 25–30 h | ≈ **20–25 h** | dòng trên |
| Cách A 1080p (P = 2) | ≈ 14 h (8 s/khung) | giữ ≈ 13–14 h (đo 7,28–7,75 s/khung/tiến trình, trung vị, spp 4, hình học cuối) | lệch −9 % < 20 % → không thay |
| Tiền | ≈ $65–85 | không đổi (look không phát sinh chi phí API/GPU) | — |
