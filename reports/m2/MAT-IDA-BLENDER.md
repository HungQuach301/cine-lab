# CỬA MẶT IDA — BLENDER (C chỉnh): DỪNG Ở ĐIỀU KIỆN DỪNG 2, CHƯA KIỂM MÙ

Nhánh: `claude/cine-lab-m2-cong5-layout-24o5fp` (merge W4 @c7196bd). Ngày 28/09/2026.
Quyết định gốc: AUTHORSHIP "Cửa mặt Ida — quyết định".
- **Cổng 6 vẫn khoá.** Layout trên main không đổi. `IDA_STYLE` mặc định vẫn là `'aa'`; W4 không sửa file .js nào.

## 0. Tóm tắt
- W4 (worker mới, worktree riêng) dựng đầu Ida bằng Blender 5.2.2 (`/opt/bpy`), qua một lượt dựng và xuất trọn vẹn (115 s): `ida_bl.glb` 19,5 MB, có shape key.
- **Lần render thử đầu tiên (EEVEE, 4 góc) chưa ra hình đầu dùng được**, nên W4 **dừng đúng điều kiện dừng 2** anh/chị đặt.
- Chưa tích hợp vào three.js, chưa có khung thử nào, **chưa chạy kiểm mù**. Câu hỏi "có hết bị gọi búp bê/mặt nạ không" **chưa có câu trả lời**.
- Chi phí: khoảng 26 phút, **251 nghìn token** (dưới hạn 700 nghìn). Hàng đợi: 1 việc (65,9 s, làn nhanh).

## 1. Lượt dựng 1: được và chưa được
Ảnh: `reports/m2/cong5/w4/BL_thu1_blender_eevee_4goc.jpg` (EEVEE, đèn studio, 4 góc). P tự xem xác nhận nhận định của W4.

| Hạng mục (theo lời chê đã đếm) | Kết quả lượt 1 |
|---|---|
| Tai có cấu trúc, cân hai bên | **Được**: vành, gờ, hố tai, dái dày |
| Lông mày bạc | **Được** |
| Tóc bạc có vân, mép mềm, chân tóc chuyển dần | **Được một phần**: 318 dải thon + 170 sợi tơ; **búi tóc tách rời khỏi đầu** ở góc nghiêng và góc sau |
| Nửa dưới mặt, hàm–cổ | **Hỏng, nặng hơn trước**: môi phồng như đang chu; hàm và cằm có cục lệch, không cân; cổ có u |
| Mắt | **Hỏng**: đọc thành hai hố đen |
| Mũ | Mới là giả lập để xem thử; P thấy **dáng mũ ống cao, chưa phải mũ phớt** theo sheet |
| Nhẹ lưới | Đầu 156 nghìn đỉnh (A-i: 86,7 nghìn), quá nặng |

W4 nhận định (chưa kiểm): cách dựng bằng hàm khoảng cách rồi lấy ra lưới tứ giác dễ ra bề mặt lổn nhổn ở chỗ nhiều khối chồng nhau (hàm, cổ, miệng).

Đã có sẵn, dùng lại được nếu làm tiếp:
- Shape key cho 16 kênh cùng tên `CHANNELS` của facerig.js.
- 6 khẩu hình `vis_A`, `vis_E`, `vis_O`, `vis_MBP`, `vis_FV`, `vis_L`.
- 4 preset neutral, sad_smile, strained, choked.
- Script dựng chạy một lượt 115 s: `design/cong3/v2/char3d/blender/`.

## 2. Việc chưa làm (vì dừng)
- Nạp glb bằng GLTFLoader, cờ `'bl'`, bản lề mũ mới.
- 8 khung thử, bảng so sánh A-α / A-i / 'bl'.
- c3_views cho 'bl'; so hình khối với máy render (EEVEE và three.js).
- Đánh giá đưa vào pipeline.
- Lỗi tay: vẫn còn (ghi nhận từ MAT-IDA-AI, ngoài phạm vi gói).
- Dò 'aa': W4 không sửa .js nên layout không đổi. Đây là suy ra, không phải số đo lại. Lần đo gần nhất là P ở commit c801906, lệch 0 px.

## 3. Quyết định cần chủ dự án
| | **a — W4 làm tiếp cách dựng hiện tại** | **b — Dừng C, trình phương án lùi PA1** | **c — Làm tiếp C nhưng lấy lưới A-i làm nền** |
|---|---|---|---|
| Nội dung | 2–3 lượt chỉnh theo thứ tự: nửa dưới mặt và cổ → mắt → búi, rồi tích hợp 'bl' và làm đủ khung thử. Vẫn 1 vòng kiểm mù | Như quyết định đã ghi: PA1 với A-α hoặc A-i, kèm so sánh; không có 'bl' | Xuất đầu A-i từ three.js sang Blender, dọn topo, subdivision, sửa đúng các lời chê: chân tóc, tai (dùng lại tai và tóc của W4), mày bạc, hàm–cổ. Xuất glb với shape key sẵn có. Vẫn 1 vòng kiểm mù |
| Ưu | Giữ hướng dựng từ đầu, không mang khối cũ | Không tốn thêm; mở Cổng 6 sớm nhất | Nền đã đọc đúng tuổi, giới và cảm xúc (4/4 ở vòng 2); chỉ phải sửa phần bị chê. Tai và tóc của W4 dùng lại được |
| Nhược | Lượt 1 cách đích xa (hàm, cổ, mắt); W4 ước thêm 350–450 nghìn token; bề mặt lổn nhổn có thể do chính cách dựng | Chấp nhận mặt đang bị gọi "búp bê" ở cao trào | Có thể mang theo tỷ lệ "búp bê" của A-i |
| Chi phí ước | 350–450 nghìn token của W4 (tổng khoảng 600–700 nghìn, sát hạn) | 0 | P ước 300–400 nghìn token; cùng các điều kiện dừng |
| Rủi ro | Hết hạn mà chưa ra hình dùng được | Chất lượng cao trào dưới chuẩn | Vẫn trượt tiêu chí 0/4 |

**Khuyến nghị của P: c.**
- Lượt 1 cho thấy dựng từ đầu bằng hàm khoảng cách hỏng đúng ở vùng khó nhất (hàm, cổ, miệng). A-i đã giải được vùng đó ở mức đọc cảm xúc 4/4.
- Cách c dồn hạn còn lại vào đúng các lời chê: chân tóc, tai, mày, hàm–cổ, da. Nếu vẫn trượt, lùi về b như quyết định đã ghi.

Cả ba phương án đều giữ: một vòng kiểm mù, tiêu chí không hạ, Cổng 6 khoá, mặc định 'aa'.

## 4. Thời gian và token
| Việc | Thời gian | Token (ngữ cảnh tích luỹ) | Hàng đợi |
|---|---|---|---|
| W4 lượt 1: đọc tài liệu và mã 10 phút, viết script 8, dựng 2, xem và quyết định dừng 4 | khoảng 26 phút (13:59–14:25 UTC) | 250 828 | 1 việc `probe-aa-truoc` (làn nhanh, chờ 0 s, chạy 65,9 s, gắn QUA-60S); dựng và xem Blender chạy ngoài hàng đợi, dưới 2 phút mỗi lượt |
| P: giao việc, xem ảnh, báo cáo | — | — | — |

Báo cáo gốc của W4: `reports/m2/cong5/w4/BAO-CAO-W4.md`.
