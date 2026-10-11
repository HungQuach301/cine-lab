# Nhận diện kênh (mốc 1, bước 5)

> Đề xuất, chờ chủ dự án duyệt. Chưa dựng tài sản nào; chưa thêm mục vào `RIGHTS.md` vì chưa dùng tài sản nào trong sản phẩm.
> Nguyên tắc: **khác hẳn Last Lamplighters** (giấy B3, đèn khí ấm, giọng Bill) để hai kênh không ăn khán giả của nhau và không bị xem là cùng một khuôn sản xuất hàng loạt.

## 1. Hình
**Ngôn ngữ hình: "mô hình kỹ thuật sống".** Mỗi ngành là một sa bàn 3D khối giản lược, chiếu sáng như ảnh chụp sản phẩm công nghiệp. Máy quay đi như một kỹ sư dẫn khách: từ toàn cảnh xuống chi tiết cắt lớp. Số liệu nổi trên vật thể chứ không nằm trên tờ giấy.

| Bộ cảnh | Trụ | Dùng lại từ nhà máy LL | Dựng mới |
|---|---|---|---|
| **Nhà máy / xưởng lắp ráp** (thân máy bay, dây chuyền, phòng sạch) | T1 | Bộ đồ nghề `kit.js` (`box/cyl`, `camRig`, `dust`, hậu kỳ). Ý dựng **nhà chứa máy bay và ống hầm gió** của cảnh đinh tập 7 (`ep07.js`, `airfield`): khối nhà xưởng, bóng trên trời chạng vạng | Xưởng lắp thân máy bay theo trạm, cẩu trần, bóng người vô danh theo tỷ lệ; không lặp bố cục cảnh tập 7 |
| **Cảng, cẩu, tàu container** | T1, T2 | `kit.js`, sương theo độ sâu | Cẩu giàn STS, chồng container thủ tục, tàu theo lớp kích thước, đường ray, xe tải |
| **Kho hàng / thị trấn** | T2, T4 | `kit.js`, `figure()` bóng người | Thị trấn sa bàn nhìn từ cao, mái nhà đổi màu theo dữ liệu, dòng xe; trung tâm thương mại bỏ trống |
| **Ngân hàng, mạng thanh toán** | T3 tài chính | `canvasTex` (màn hình, bảng số) | "Đường ống tiền" trong suốt: quầy → POS → ngân hàng phát hành → mạng → ngân hàng thanh toán, gói tin sáng chạy theo ống; két, phòng máy chủ, máy ATM cắt lớp |
| **Bản đồ tuyến thương mại** | T1, T3 | Khung vẽ `lib/map.js` | Quả địa cầu phẳng hoá, tuyến hàng hải, eo biển là điểm nghẽn, nút mạng tài chính |

- **Không** logo, sản phẩm có nhãn hiệu, giao diện app thật, mặt người.
- Đồ hoạ dữ liệu: dùng lại máy dựng `render.js` và mẫu `lib/charts.js` (cột mọc, số đếm, trục từ 0, ACTUAL/PROJECTION), đổi mặt nền giấy B3 thành **bảng kỹ thuật** (lưới mờ, viền mảnh, ánh rọi lạnh).

## 2. Màu
Nền đậm, ánh công nghiệp lạnh, một màu nhấn ấm cho thứ đang được giải thích. Tương phản đo theo WCAG trên nền `#0F1722`:

| Vai trò | Mã | Tương phản với nền | Dùng cho |
|---|---|---|---|
| Nền / bóng | `#0F1722` mực xanh đen | — | Nền, bóng đổ |
| Chữ chính | `#EEF1F4` | 15,9:1 | Chữ, số lớn |
| Thép | `#9AA7B5` | 7,4:1 | Khối máy, trục, chữ phụ |
| **Nhấn: cam an toàn** | `#F08A4B` | 7,2:1 | Thứ đang được giải thích (container, gói tin tiền, dòng phí) |
| Tín hiệu: xanh lục lam | `#3CC2B0` | 8,2:1 | Dữ liệu thực tế thứ hai, dòng chảy "bình thường" |
| Cảnh báo / dự báo | `#F2C14E` hổ phách | 10,7:1 | Dự báo (luôn kèm nét đứt + nhãn PROJECTION) |

- Cam và xanh lục lam có độ sáng gần nhau (tương phản giữa hai màu 1,13:1). Vì vậy **không bao giờ phân biệt hai nhóm chỉ bằng màu**: luôn kèm nhãn, nét hoặc gạch chéo (chuẩn kiểm mù màu LL §5.1 giữ nguyên).
- **Màu theo phần** (thay kịch bản ấm–sepia–lạnh–ấm của LL): móc và kết: nền đậm, nhấn cam mạnh · bối cảnh: thép trung tính · cơ chế: lạnh, nhấn cam dần · giới hạn/tương lai: hổ phách. Cài như một bộ `GRADES` mới trong gói kênh (không sửa `kit.js` của LL).

## 3. Chữ
- **Inter / Inter Display** (OFL-1.1, đã có trong môi trường: gói Debian `fonts-inter`, `/usr/share/doc/fonts-inter/copyright`). Inter Display SemiBold cho tựa và số lớn; Inter Regular/Medium cho nhãn; bật chữ số đều cột (`tnum`) cho số đếm.
- Khác LL (DejaVu Serif/Sans trên giấy). Cỡ tối thiểu và luật chữ của nhà máy (`text()` tự nâng cỡ, ≥ 4,5:1, lề an toàn 5 % thumbnail) giữ nguyên.
- **Việc khi dùng lần đầu:** thêm mục Inter vào `RIGHTS.md` (trích câu OFL, đường dẫn tệp, phạm vi YouTube/bán phim).

## 4. Giọng (ElevenLabs)
Phải khác **Bill** (`pqHfZKP75CvOlQylNhV4`, giọng LL) và khác các giọng đã gắn với dự án khác (`crux-analyst-f1`, "AI-Era Money Defense Narrator V1"). Không chọn giọng có nhãn quảng cáo hoặc mạng xã hội, vì dễ nghe như video hàng loạt. Danh sách lấy từ `GET /v1/voices` ngày 11/10/2026. Tôi **chưa thu mẫu**, để tiết kiệm ký tự cho đến khi chủ dự án chọn ứng viên.

| Ứng viên | voice_id | Nhãn ElevenLabs | Ưu | Nhược / rủi ro |
|---|---|---|---|---|
| **Eric – Smooth, Trustworthy** (đề xuất 1) | `cjVigY5qzO86Huf0OWal` | Mỹ, trung niên, nam, conversational | Giọng Mỹ trung niên, khác xa chất già và chậm của Bill; hợp khán giả Mỹ | Nhãn "trustworthy" có thể gợi chất cố vấn; cần đọc thử đoạn tài chính để chắc không nghe như lời khuyên |
| **Matilda – Knowledgable, Professional** | `XrExE9yKIg1WjnnlVkGX` | Mỹ, trung niên, nữ, informative_educational | Nhãn giáo dục đúng dạng giải thích; tách hẳn khỏi LL | Gần vai "chuyên gia" hơn; có thể trùng cảm giác với giọng nữ phân tích của Crux |
| **River – Relaxed, Neutral, Informative** | `SAz9YHcvj6GT2YYXdXww` | Mỹ, trung niên, trung tính | Trung tính, ít gợi persona nhất | Có thể quá phẳng cho tập 16 phút; cần đo giữ chân |

- **Đề xuất cách chọn:** thu cùng một đoạn móc (khoảng 300 ký tự) bằng 3 giọng, `eleven_multilingual_v2`, tốc độ 1,00, ghi số dư ElevenLabs trước/sau, rồi chủ dự án nghe mù và chọn. Ghi giọng được chọn vào `RIGHTS.md` (giấy phép thương mại gói trả phí, như M3-N1).
- Thiết kế giọng riêng (Voice Design) là phương án dự phòng. Rủi ro Beta Voice Design còn mở từ M1-V3, nên ưu tiên giọng premade.

## 5. Nhạc và âm thanh
- **Nhạc:** nhạc nền điện tử tối giản, xung đều (pulse) theo nhịp máy móc; một motif 4–5 nốt ngắn mở ở móc và trả lại ở kết (đóng vòng). Ba cue theo phần (bối cảnh, cơ chế, kết). Giữ luật dự án: **người làm**, CC0 hoặc CC BY, không AI, không NC/ND, không YouTube Audio Library. Mỗi bản vào `RIGHTS.md` trước khi dùng.
  - Lưu ý môi trường: Freesound trả HTTP 403 ở `scripts/env/verify.sh` phiên này. Nguồn nhạc cần chủ dự án chọn: Freesound qua phiên có mạng mở, thư viện CC0 khác, hoặc đặt nhạc sĩ (tốt nhất cho bán phim).
- **SFX nghề** (luật LL §11 giữ nguyên ý): mỗi bộ cảnh có ≥ 3 âm thanh riêng: cẩu cảng, còi tàu, đinh tán khí nén, tiếng in hoá đơn, tiếng bíp POS, tiếng đếm tiền ATM. Ghi âm do người làm, CC0.
- Trộn âm như nhà máy: lời −17 LUFS, master −14 LUFS, TP ≤ −1 dBTP, nhạc hạ 10–14 dB khi có lời.

## Ưu, nhược, tác động, rủi ro
- **Ưu:** nhận diện tách hẳn LL; tái dùng tối đa lõi (máy dựng, kit 3D, mix, kiểm). Bảng màu đạt tương phản ≥ 7:1 cho mọi màu chữ. Sa bàn 3D có số nổi trên vật thể là thứ video AI hàng loạt (ảnh tĩnh + stock) chưa làm.
- **Nhược:** cần dựng mới 4 bộ cảnh trước tập đầu (nhà máy, cảng, thị trấn, đường ống tiền). Inter là font phổ biến nên ít "chữ ký" hơn font riêng.
- **Tác động:** tập thí điểm (container) cần bộ cảng + bản đồ tuyến trước tiên. Mỗi trụ sau đó có sẵn ít nhất một bộ cảnh.
- **Rủi ro:** SwiftShader dựng cảnh 3D đông vật thể (chồng container hàng nghìn khối) có thể chậm. Đề xuất dùng `InstancedMesh` và đo thời gian dựng trên một cảnh thử trước khi khoá bảng shot. Nguồn nhạc chưa có kênh tải khi Freesound bị chặn.

## Phép thử F1
| Dùng chung lõi LL | Riêng gói kênh |
|---|---|
| `kit.js` (hình học, máy quay, bụi, canvasTex, hậu kỳ), `render.js`, `lib/charts.js`, `mix.py`, luật chữ, kiểm mù màu, luật RIGHTS | Bộ cảnh 3D theo trụ, bảng màu + `GRADES` mới, mặt nền bảng kỹ thuật, Inter, giọng mới, nhạc/SFX mới |
