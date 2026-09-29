# NHÁP characters v1.5: Ida mặt 'bl' (MPFB2). CHƯA DUYỆT, CHƯA KHOÁ SHA

P soạn theo quyết định A′ (AUTHORSHIP "Cửa mặt Ida", 29/09/2026). Chủ dự án đã nhận **tỷ lệ đầu MPFB và tai MPFB**.
`bible/characters.md` v1.4 và `design/cong3/model-sheet/ida.json` **không đổi** cho tới khi chủ dự án duyệt nháp này. Các dòng dưới đây sẽ **thay** các dòng tương ứng của v1.4 nếu được duyệt.

| Hạng mục | v1.4 (A-α, đang khoá) | Nháp v1.5 ('bl') | Nguồn |
|---|---|---|---|
| Cách dựng | Thân 3D, tay 3D, mặt vẽ tay trên texture phủ đầu 3D (C′) | Thân, áo, tay giữ như v1.4. **Đầu, cổ, tóc, tai từ lưới người MPFB2** (tài sản lõi CC0, RIGHTS W4-MPFB-A), dựng trong Blender bằng script (`design/cong3/v2/char3d/blender/build_ida_l2.py`), xuất glb, render trong three.js (`IDA_STYLE='bl'`) | Quyết định d / A′ |
| Mặt | A-α tròn–mềm cách điệu, nét nhăn vẽ | Người nữ MPFB khoảng 74 tuổi (age 0,877), `head-age-incr` 0,75, 33 target chi tiết (mũi dài hơi khoằm, mắt to, dái tai dài, gò má cao, môi mỏng, cằm nhỏ); nếp tuổi bằng khối (3 nếp trán, chân chim, rãnh mũi–má, rãnh khoé miệng, nếp môi trên, nếp cổ); da loang hai tầng, đốm tuổi, độ nhám theo vùng 0,45–0,85 | W4 lượt 2–3 |
| Tai | tai A-α, khuyên treo dái tai | **tai MPFB liền lưới**; hoa tai treo ở điểm thấp nhất của dái tai (target `ear-lobe-incr`) | Chủ dự án nhận tai MPFB |
| Tỷ lệ đầu | mắt ở 0,575 H | **tỷ lệ mặt MPFB** (mắt khoảng 0,50 H); phần đầu nhìn thấy dài hơn A-α (thân/đầu ở 0° giảm 15,3 %) | Chủ dự án nhận tỷ lệ đầu MPFB |
| Khăn | quấn thấp ở chân cổ | **khăn cao 4 vòng** | Duyệt ngày 28/09 |
| Mũ | mũ phớt #262a33, ngồi thấp ôm đầu | giữ #262a33; miệng mũ theo khối tóc 'bl' (rx 0,3798, rz 0,4254 H; tâm z −0,026); **bản lề mũ mới** (ngả 0,26 rad khi đẩy mũ; A-i 0,36) | Duyệt ngày 28/09 |
| Tóc | #e2dfda + shader tóc bạc | giữ màu; búi = lõi + 40 lọn quấn; chân tóc dày, hạ ở trán và thái dương | W4 lượt 3 |
| Biểu cảm, khẩu hình | preset vẽ | shape key 16 kênh cùng tên `CHANNELS` của facerig.js + 6 khẩu hình `vis_*` + 4 preset; corrective `corr_mouth`, `corr_smile_lip`; nguồn: expression unit CC0 của MPFB | W4 lượt 2–3 |

**c3_views 'bl' (tỷ lệ bộ phận / đầu nhìn thấy; đo như B1; số thô `reports/m2/cong5/w4/L3_c3_bl.json`):**

| Bộ phận | 0° | 45° | −45° | 90° | −90° | 135° | −135° | 180° |
|---|---|---|---|---|---|---|---|---|
| thân | **2,272** | 2,219 | 2,216 | 2,033 | 2,069 | 2,381 | 2,353 | 2,130 |
| cánh tay trên | **1,336** | 1,428 | 1,418 | — | 1,404 | 1,482 | 1,474 | 1,355 |
| cẳng tay | **0,831** | 0,882 | 1,257 | — | 1,005 | 0,837 | 1,101 | 1,025 |
| cẳng chân (bỏ) | 0,245 | 0,272 | 0,273 | — | 0,271 | 0,275 | 0,275 | 0,245 |
| thân so với v1.4 | −15,3 % | −3,1 % | −2,1 % | −0,05 % | +0,4 % | −6,9 % | −6,9 % | −22,6 % |

**Tác động tới Cas (chủ dự án cần quyết):** đầu 'bl' vẫn dài 1 H nên chiều cao và quan hệ cao thấp Ida–Cas không đổi. Nhưng ở khung hai người, đầu Ida trông to hơn tương đối (khoảng 13–18 % ở chính diện và sau lưng). Hai hướng:
- (i) chấp nhận và ghi vào v1.5;
- (ii) cho Cas đi cùng quy trình MPFB ở Cổng 6.

**Khi duyệt:** ghi v1.5 vào `bible/characters.md`, cập nhật `ida.json` (c3_views, face, hat), thêm tài sản vào `assets/LIBRARY.json`, khoá lại `design/cong3/LOCK-THIET-KE.sha256`, đổi mặc định `IDA_STYLE` sang 'bl', rồi chạy luật C3 trên layout.
