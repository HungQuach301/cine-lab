# Chạy thử checks v1.4 trên 8 file Cổng 3 A2+ của P (phiên K)

Nguồn: `design/cong3/v2/out/a2p/*` (video, mặt nạ 4× thật), model sheet `design/cong3/model-sheet/{ida,cas}.json` (B1, có `c3_views`; cùng số với `reports/m1/cong3-a2p/B1_so-do-moi-goc.json`).

- **Trước** = báo cáo v1.3 của P (`design/cong3/v2/out/a2p/check/*`).
- **Sau, không `views`** = v1.4 trên file nguyên trạng (`run.py --only J1,J1b,M3,C3`, có kiểm toán).
- **Sau, có `views`** = v1.4, cùng mặt nạ, thêm `views` do K tính từ chính trang render của P (`k_views.js`; số trong `<file>.views.json`). Chạy bằng `dryrun.py`, không kiểm toán lại (bộ mặt nạ không đổi; kiểm toán mặt nạ v1.3 đạt 8/8). `views` là bản K tính để chạy thử, **không phải bản xuất của P**.

## Kết quả

| File | J1, J1b trước | J1, J1b sau | C3 trước (v1.3) | C3 sau, không views | C3 sau, có views | Mẫu đo được (có views) | Lý do chính |
|---|---|---|---|---|---|---|---|
| a_close_ida | TRƯỢT | — | TRƯỢT | CẦN NGƯỜI XEM (đầu chạm mép khung) | CẦN NGƯỜI XEM | 0/6 | góc −47°: cách 0° 47°, cách −90° 43°; sheet không có −45° |
| b_cas_bird | TRƯỢT | — | TRƯỢT | TRƯỢT | CẦN NGƯỜI XEM | 0/8 | góc 151° (sau lưng): cách 90° 61° |
| c_s5_medium | TRƯỢT | — | TRƯỢT | TRƯỢT | CẦN NGƯỜI XEM | 0/6 | góc 151° |
| c_s5_wide | TRƯỢT | — | TRƯỢT | TRƯỢT | **TRƯỢT** | 0/6 | góc −167°; **độ khớp biên mặt nạ–ảnh 1,06 < 1,5** (đầu 13 px) — chỉ số chống mặt nạ giả, không thuộc khiếu nại |
| d_s6_alley | TRƯỢT | — | TRƯỢT | TRƯỢT | CẦN NGƯỜI XEM | 0/6 | góc 48° (gần 45°) nhưng **đầu ngẩng**: co ngắn 13,5% > 2% |
| e_ending | TRƯỢT | — | TRƯỢT | TRƯỢT | CẦN NGƯỜI XEM | 0/6 | góc −123°, ngẩng 7°: lệch 3D 34° > 30° |
| walk | TRƯỢT | — | TRƯỢT | TRƯỢT | **TRƯỢT** | 4/12 (33%) | thân so với −90°: +0,4 / +1,4 / +2,2 / +3,9% (2 "không chứng minh được"); tay: phối cảnh 2,5–3% → không đo được |
| walk_cas | TRƯỢT | — | TRƯỢT | TRƯỢT | **TRƯỢT** | 12/16 (75%) | **đùi +9,2…+11,4%** so với −90° (trượt chắc chắn); thân +0,7…+5,0%; độ khớp biên 1,473 < 1,5 (như v1.3) |

J1, J1b: 8/8 file không có luồng âm và `X.script.txt` rỗng → "—" (M3 cũng "—"). Trước: TRƯỢT "Không có luồng âm".

## Đọc kết quả

1. **Khiếu nại được giải quyết đúng như chủ dự án quyết:** không còn TRƯỢT oan vì góc nhìn ở 5/8 file. Máy không có mẫu nào so được thì báo CẦN NGƯỜI XEM, không ĐẠT.
2. **Bảng `c3_views` 4 góc phủ ít.** 5/8 file có góc nhìn nằm ngoài ±30° quanh 0°, ±45°… vì sheet thiếu −45°, ±135°, 180°. Thêm 4 góc này thì a_close_ida (−47°), e_ending (−123°), b_cas_bird, c_s5_medium (151°) có thể đo được.
3. **walk_cas: đùi dài hơn số góc −90° khoảng 10%, ổn định ở 3/4 khung.** Số đo khớp số góc 0° (1,191) hơn góc −90° (1,076). Có hai cách giải thích mà máy không phân biệt được:
   - (a) áo len che phần trên đùi nhiều hay ít tuỳ tư thế bước, nên độ dài NHÌN THẤY đổi theo tư thế dù co ngắn xương ≈ 1,000;
   - (b) số góc −90° của sheet B1 có vấn đề.
   Cách kiểm: P render tư thế turnaround ở đúng góc −75° bằng công cụ B1, rồi đo đùi.
4. **walk: thân lệch tăng dần +0,4 → +3,9%** khi góc đi từ −71° về −80°. Không khớp với giả thuyết "lệch do xa góc tham chiếu" (càng gần −90° lẽ ra càng khớp). Có thể do vạt áo khoác theo nhịp bước. Cần P xem.
5. c_s5_wide và walk_cas còn trượt **độ khớp biên** (v1.3, không thuộc khiếu nại): đầu 13 px và 44–46 px thì biên mặt nạ khó khớp cạnh ảnh.

## Số `views` K tính (khung đầu mỗi file)

| File | view_deg | elev_deg | Đầu: co ngắn | Ghi chú |
|---|---|---|---|---|
| a_close_ida | −47,4 | 12,5 | 0,997 | tay trên 0,758, cẳng tay 0,784 (gập về đèn); cẳng tay depth 0,827 (gần máy 17%) |
| b_cas_bird | 150,8 | 8,9 | 0,918 | tay trên 0,714 |
| c_s5_medium | 150,7 | −0,5 | 0,832 | cẳng tay bị che 100% |
| c_s5_wide | −166,8 | 2,0 | 0,826 | |
| d_s6_alley | 48,4 | −0,3 | 0,865 | |
| e_ending | −123,3 | 7,2 | 0,988 | cẳng tay 0,919 |
| walk | −71,4 → −80,1 | ≈ 4 | 1,000 | tay: co ngắn ≥ 0,994, depth 0,968–0,976 |
| walk_cas | −71,3 → −80,0 | ≈ 5,7 | 1,000 | co ngắn ≥ 0,997; cẳng tay depth 0,975 |

Chi tiết từng mẫu: `dryrun.json`.
