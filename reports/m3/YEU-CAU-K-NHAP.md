# Yêu cầu gửi phiên K — BẢN NHÁP, CHƯA GỬI (P soạn 01/10/2026)

Căn cứ: AUTHORSHIP 01/10/2026, "P soạn sẵn yêu cầu gửi K (C3 cho nhân vật dạng bóng; profile luật Shorts 9:16), chưa gửi". Kênh Last Lamplighters, tập thử Mốc 2 (`reports/m3/KE-HOACH-TAP-THU.md` §7).
P không đọc mã `checks/`. Mọi mô tả dưới đây dựa trên `checks/RUN.md` và báo cáo luật đã chạy. Khi chủ dự án cho phép, P chuyển nguyên văn mục 1–2 vào `checks-appeal.md`.

## 1. C3 cho nhân vật dạng bóng (silhouette)
**Hiện trạng**
- C3 so tỉ lệ bộ phận (đầu, thân, cánh tay trên, cẳng tay, đùi, ống chân) với model sheet `ida.json` / `cas.json`, đo trên mặt nạ bộ phận.
- Phong cách B3 của kênh mới biến Ida (và Cas) thành **bóng đặc, chỉ một viền sáng mảnh**, không có mặt.
- Lưới, rig và diễn hoạt giữ nguyên Last Round, nên mặt nạ bộ phận vẫn xuất được. Nhưng trên hình, ranh giới giữa các bộ phận trong bóng không thấy được.

**Câu hỏi cho K**
1. Với nhân vật bóng, C3 đo trên mặt nạ hình học (vẫn xuất được) có còn đúng nghĩa không? Hay cần đổi chỉ tiêu sang **đường viền ngoài**: tỉ lệ cao/rộng của bóng, tỉ lệ đầu/thân theo đường viền, độ khớp mép bóng với mặt nạ?
2. Có cần một model sheet riêng cho dạng bóng không, ví dụ `ida-bong.json`: đường viền chuẩn ở 4 góc, tỉ lệ đầu–mũ–thân? Nếu cần, ai lập và khoá: chủ dự án duyệt, K khoá SHA?
3. Viền sáng 1–2 px có ảnh hưởng tới phép đo "độ khớp biên mặt nạ–cạnh ảnh render" (hiện trượt ở mức 0,79–1,0, ngưỡng ≥ 1,5) không?

**P đề xuất** (K quyết): giữ C3 trên mặt nạ hình học để chặn lỗi rig (kéo, lún), và thêm chỉ tiêu đường viền cho dạng bóng. Không hạ ngưỡng.

## 2. Profile luật cho Shorts 9:16
**Hiện trạng:** `run.py --profile shot|youtube|archive`. Profile `youtube` kiểm N3 khung 16:9 và SAR 1:1, M1 −14 LUFS ±1, true peak ≤ −1 dBTP.

**Nhu cầu:** Shorts 1080×1920, 24 fps, < 60 s, có chữ trên màn hình và phụ đề cháy (`KE-HOACH-TAP-THU.md` §6).

**Câu hỏi cho K**
1. Thêm profile `shorts`, với các điểm khác profile youtube:
   - N3: khung 9:16, 1080×1920, SAR 1:1; codec và bitrate theo khuyến nghị YouTube Shorts;
   - thời lượng < 60 s (luật mới hoặc thuộc N3);
   - M1: giữ −14 LUFS?
   - P0/P1/G4: vùng an toàn chữ cho giao diện Shorts (lề trên, dưới, phải bị nút che). Có cần luật vùng an toàn mới không?
2. Shorts cắt từ master 16:9: C3 và H1b chạy trên bản cắt hay chỉ trên master?

## 3. Luật đo judder (thêm 01/10/2026, theo CHUAN-KENH-LL §5.2; gửi ở M2.3)
**Hiện trạng**
- Chủ dự án phát hiện animatic M2.1 giật. Công cụ của P `scripts/p/judder.py` (framemd5 khung giải mã) đo được **799 đoạn đứng hình 2–12 khung, 16,96 % thời lượng**. Số này khớp số đo của Claude (rà độc lập bên ngoài).
- Chuẩn kênh đặt mục tiêu 0. Đứng yên có chủ ý phải dài ≥ 1 s và ghi trong bảng shot.

**Câu hỏi cho K**
1. K có đưa phép đo này vào `checks/` thành luật chính thức không (profile `shot` và `youtube`)? K tự viết hay lấy định nghĩa của `scripts/p/judder.py`:
   - đoạn ≥ 2 khung liên tiếp có framemd5 trùng nhau;
   - đoạn dài 2–12 khung ngoài vùng tĩnh khai báo thì tính là lỗi;
   - đoạn 13–23 khung báo riêng;
   - đoạn ≥ 24 khung coi là cố ý.
2. Đo khớp tuyệt đối (framemd5) hay so gần đúng (ví dụ |chênh| trung bình ≤ 0,5/255 trên ảnh xám thu nhỏ) để bắt khung "gần như đứng" do nén?
3. Vùng tĩnh có chủ ý khai ở đâu (cột trong bảng shot, hay tệp đi kèm video) để luật đọc được?
4. Có thêm chỉ tiêu nhịp cập nhật không (ví dụ không giây nào có < 12 khung mới khi đang chuyển động)?

**P đề xuất** (K quyết): luật mới, mặc định so tuyệt đối; ngưỡng lỗi = 0; vùng tĩnh khai trong bảng shot.

## 4. Luật phát hiện máy xuyên hình học (thêm 01/10/2026 sau animatic v3; gửi ở M2.3)
**Hiện trạng**
- Ở animatic v3, lỗi trôi máy cộng dồn làm máy xuyên vào khối nhà: đoạn 01 7,7–9,9 s; đoạn 04 khoảng 14 s. Đồng hồ quảng trường trôi khỏi khung 3,5 s.
- **Judder không bắt được** lỗi này vì khung vẫn thay đổi liên tục. P chỉ phát hiện khi xem khung bằng mắt.

**Câu hỏi cho K**
1. Có thêm luật tự động không? Ví dụ một trong hai cách:
   - xuất kèm độ sâu từ driver render, rồi đo tỷ lệ điểm ảnh có độ sâu sát mặt phẳng gần (> x % khung) trong ≥ 3 khung liền;
   - đo tỷ lệ khung một màu phẳng (> 60 % diện tích) ngoài vùng chuyển cảnh.
2. Có thêm luật "chủ thể bắt buộc ra khỏi khung" không? Ví dụ đồng hồ, đèn hoặc nhân vật khai trong bảng shot mà không còn trong khung.

**P đề xuất** (K quyết): luật độ sâu cho cảnh three.js; driver xuất kèm độ sâu thu nhỏ.

## 5. Kiểm chéo số HSUS từ bản quét (thêm 04/10/2026)
**Hiện trạng**
- Đoạn 08, 09, khối 10–13 và đoạn 14 dùng 24 giá trị từ HSUS Series D 233–682, tr. 140–145 [32]. PDF là ảnh quét, không có lớp chữ.
- P đọc từng hàng bằng mắt trên ảnh dựng ở 220–400 dpi. Chưa có người thứ hai đọc lại.

**Yêu cầu K:** K đọc độc lập 24 giá trị (thang máy 1900–1970 theo hai phân loại 1950/1960/1970; trực tổng đài; tốc ký–đánh máy–thư ký) từ bản quét và đối chiếu với bảng §6.1 kịch bản v3.1. Lệch giá trị nào thì báo P sửa hình trước G2.

## 6. Kiểm lại số BLS 2025–35 (thêm 04/10/2026)
**Hiện trạng**
- Số BLS Table 1.5 và USDL-26-1422 được đọc toàn văn ngày 01/10/2026 qua Wayback (bls.gov trả 403 từ máy này).
- Các số trên hình: −34,4 %, −27,6 %, −26,0 %, −25,5 %, −21,4 %, −4,0 %; nhóm tăng +41,0 / +36,5 / +34,6 %.

**Yêu cầu K:** K kiểm lại từng số trên bảng gốc (đường dẫn trực tiếp hoặc Wayback) và ghi ngày đọc.

## 7. Luật nguồn số: không dùng Wikipedia làm nguồn chính (thêm 04/10/2026, CHUAN-KENH §7)
**Hiện trạng:** số "1820s · 40 000 đèn · 215 dặm" từng dựa trên Wikipedia và hai trang web. Claude (rà độc lập) phát hiện; ở M2.2 phim đã bỏ số này.

**Đề xuất cho K:** mỗi số trên hình hoặc trong lời dẫn phải có ít nhất một nguồn chính là sách, báo cáo, bài học thuật hoặc văn bản gốc đọc được toàn văn, có ghi trang. Wikipedia, trang tổng hợp hoặc blog chỉ được dùng để dẫn đường. K quyết cách kiểm (danh sách nguồn có trường `loai_nguon` và `trang`).

**Cách gửi khi được phép:** P ghi mục 1–7 vào `checks-appeal.md` (mục "Yêu cầu mới, 2026-10"), chờ K phán quyết và khoá bản checks mới. Trong lúc chờ, M2 chạy luật bằng profile youtube cho master.
