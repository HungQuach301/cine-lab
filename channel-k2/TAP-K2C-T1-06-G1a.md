# K2C-T1-06 "Apartments" — Báo cáo G1a (phiên P kênh 2, 12/10/2026)

> - **Lệnh 12/10:** lời khoá ứng viên + kiểm mù 3 vòng + REVIEWER Opus (0 major) + claims đọc toàn văn; shot list theo yêu cầu mới (type/scene_id/camera_id, places, people, anchors); 3 tiêu đề dạng câu hỏi; ước giờ máy và chi phí.
> - **Không dựng khung mẫu 3D** (chờ bộ công cụ của phiên V được duyệt). Không gọi YouTube Data API. Không liên kết LL.
> - Nhánh `k2c-t1-06`. **Dừng ở G1a, chờ chủ dự án duyệt.**
> - Mức rủi ro: **VÀNG** (zoning; `QUAN-TRI-RUI-RO.md` §1, §7). Mọi chỉ số thị trường ở đây là tự tính, không phải chỉ số YouTube.

## 0. Tóm tắt
- **Lời khoá ứng viên v8.1** (`k2c-t1-06/script.md`):
  - 2 366 từ, ước **15,6 phút** ở tốc độ Eric 151,2 từ/phút (đo ở K2G-01);
  - 12 đoạn, móc dạng câu hỏi;
  - 53 claim, tất cả có nguồn;
  - mốc **as of 12/10/2026** trong lời và trên hình.
- **Nguồn:** 37 nguồn và 63 claim trong `claims.md`, 53 claim được dùng trong lời. Các trích dẫn then chốt đã kiểm lại trên tệp thô bằng `grep` (67 dấu ✔P).
- **Kiểm mù 3 vòng** (3 vai Sonnet, chỉ đưa lời):
  - vòng 1: cả 3 người thấy lời **nghiêng về phía ủng hộ phát triển**;
  - vòng 2 và 3: cả 3 người thấy **không nghiêng phía nào**;
  - cả 3 vòng: 0/3 người thấy lời quy lỗi cho nhóm người, 0/3 thấy giống lời khuyên về tiền thuê hay mua nhà.
- **REVIEWER Opus:** major qua các vòng là 13 → 10 → 5 → 5 → 2 → 1 → 4 → **0** (v8), 0 block. Lượt kiểm chứng v8.1 ra 1 major, đã sửa bằng đúng chữ REVIEWER đề xuất (§4).
- **Shot list** (`shots.yaml` → `SHOTLIST.md`): 90 shot, khai đủ `type`, `scene_id`, `camera_id`, kèm `places:` (11), `people:` (3), `anchors:` (29). Số tự đo (không phải checks/):
  - thẻ 15,2 %;
  - ảnh + tài liệu + footage 5,9 %;
  - số neo hiện bằng chart3d/scene3d 76 %;
  - 0 cặp (scene_id, camera_id) xuất hiện quá 2 lần;
  - 0 clip quá trần độ dài.
- **Footage:**
  - thử tải được ở cả 5 nguồn: LoC Detroit Publishing, HABS, FSA/OWI, Pexels, Pixabay;
  - 4 lượt gọi API (Pexels ảnh/video, Pixabay ảnh/video) đều trả **HTTP 200**;
  - 6 clip/ảnh Pexels đã tải và tính SHA256;
  - 5 mục LoC cần chủ dự án tải hộ hoặc xác nhận quyền (`CAN-TAI-HO.csv`).
- **Chi phí API: $7,74** trên trần $40 (19 lượt ghi sổ). Có thêm 1 lượt REVIEWER bị dừng giữa chừng, không vào sổ (§8).
- **Đang chờ chủ dự án:** §11.

## 1. Chuẩn bị nhánh
- Nhánh `k2c-t1-06` tạo từ `origin/k2g-ep01`, rồi merge `origin/channel-k2` và `origin/main`.
- **Xung đột** khi merge `channel-k2` (thêm/thêm) ở `channel-k2/LUAT-NOI-DUNG-G.md` (§8) và `AUTHORSHIP.md`: giữ cả hai bên. Ở lượt đầu, các dấu xung đột trong `AUTHORSHIP.md` lọt vào một commit; tôi đã gỡ ngay ở commit kế tiếp (`f4eec09`).
- **Giữa phiên** (lệnh chủ dự án): merge `origin/main` @ `2193dbe` (checks **1.10.1**), đọc `reports/checks-ll-v3/BAO-CAO.md` §18. Shot list khai theo §18.4 (type, scene_id, camera_id, places/people/anchors). Phiên này không đọc mã `checks/`.
- **`channel-k2/.gitignore`:**
  - thêm `!*/vo/*.align.json` (BAO-CAO §18.1), để lần đo sau không phải dựng lại căn chữ;
  - thêm kết quả kiểm của tập này (`k2c-t1-06/kiem-mu/*.json`, `cost.jsonl`, `nguon/census-scripts/results.json`);
  - json thị trường của kênh khác vẫn bị bỏ qua (đã kiểm bằng `git check-ignore`).
- `scripts/env/verify.sh`: 10 PASS, 1 FAIL (three.js lệch package-lock ở `design/cong3/shared`). Không ảnh hưởng G1a vì phiên này không dựng 3D.

## 2. Nguồn và claims — `k2c-t1-06/claims.md`
**Cách làm:** 5 subagent nghiên cứu song song, mỗi cụm một nhóm nguồn:
- A: luật zoning và tranh luận;
- B: luật xây dựng và cầu thang;
- C: số liệu Census;
- D: tài chính;
- E: cải cách tính đến 10/2026.

Mỗi subagent tải tệp thô vào scratchpad và ghi sổ có trích nguyên văn (`k2c-t1-06/nguon/A…E-*.md`). Sau đó P tự `grep` lại trên tệp thô các trích dẫn và số đưa vào lời. Bảng `claims.md` ghi rõ claim nào P đã kiểm (✔P).

**Nguồn chính:**
- **Census:**
  - ACS 2024 B25024 và B25127;
  - NRC completions, cập nhật 24/09/2026;
  - Characteristics of New Housing.
- **Luật:**
  - Standard State Zoning Enabling Act (bản 1926);
  - *Euclid v. Ambler*, 272 U.S. 365 (US Reports, LoC);
  - 12 CFR §1282.1;
  - Fannie Mae Selling Guide B2-3-01 và B2-3-04;
  - HUD 4000.1 Update 18;
  - Seattle Building Code 2021, chương 10 (in lại IBC 2021);
  - Oregon HB 2001;
  - RCW 36.70A.635;
  - Texas SB 2835;
  - Colorado HB25-1273.
- **Nghiên cứu và hai phía:**
  - National Zoning Atlas, Colorado 2025;
  - Pew/CBNA 2025, ghi rõ CBNA là tổ chức vận động;
  - IAFC 2024; IAFF và Metro Chiefs; CAL FIRE; nghiên cứu cho Bộ Lao động Minnesota 2025;
  - ICC 2026;
  - Terner 2023 và 2024; Minneapolis Fed 07/10/2026;
  - Freemark 2019; Urban Institute 2023 (chỉ đọc tóm tắt); Auckland 2023;
  - House Bill Report HB 1110 (2023), tóm tắt lời khai cả hai phía;
  - NYC DCP City of Yes.

**Phép tính của kênh, ghi "our calculation" trong lời hoặc trên hình:**
- C01, C02: 7,54 % kho nhà nằm trong toà 2–4 căn, so với 1,07 % nhà hoàn thành năm 2025;
- C03: 23,2 % nhà 2–4 căn có người ở xây trước 1940;
- C36: tỷ trọng 2–4 căn trong nhà mới, 5,91 % (gộp 1970–74) xuống 1,07 % (2025);
- C35: toà 5–19 căn, cộng hai cột Census;
- C63: nhà một căn, 57,1 % lên 67,5 %;
- C53: 81,9 % căn 2–4 có người ở là thuê.

Script tính nằm ở `nguon/census-scripts/`.

**Tra "as of" (claims §1b) — phải tra lại trước khi thu giọng:**
- **SBCC Washington** sẽ biểu quyết quy định một cầu thang tới 6 tầng ngày **16/10/2026**. Từ v7, lời đã bỏ câu này để không lỗi thời.
- **Arlington:** chưa có phán quyết; lời không nhắc.
- **NYC City of Yes:** vụ kiện bị bác 11/2025, chưa thấy phán quyết phúc thẩm. Lời không nhắc vụ kiện (REVIEWER ghi minor).
- **Minneapolis 2040:** vụ kiện bị bác 01/2025.
- **IBC 2027:** chưa phát hành.

**Chỗ còn hổng (đã ghi trong claims):**
- báo cáo đầy đủ của Pew bị 403, chỉ đọc bản tóm tắt;
- nghiên cứu Urban Institute chỉ đọc tóm tắt; phản biện của AEI được ghi trong claims nhưng lời không nêu (chờ quyết §11);
- trang ICC bị reCAPTCHA, nên IBC đọc qua bản in lại của Seattle;
- phán quyết Montana 2026 chỉ đọc qua báo; tập này không dùng.

## 3. Lời khoá ứng viên v8.1 — `k2c-t1-06/script.md`
| Phần (HIEN-CHUONG §2) | Đoạn | Tỷ lệ đo | Đích |
|---|---|---|---|
| Móc (câu hỏi + hai số có nguồn) | 00 | 36 từ ≈ **14,3 s** | ≤ 0:15 |
| Bối cảnh (+ miễn trừ ≤ 30 s, as-of) | 00 (phần sau), 01 | 9,0 % | ~10 % |
| Cơ chế 1–3 (bản đồ, cầu thang, ngân hàng) | 02–06 | 45,2 % | ~55 % |
| Lực ngoài luật + kết quả theo số liệu | 07–08 | 15,0 % | (thuộc phần cơ chế) |
| Hiểu sai / huyền thoại vs hồ sơ | 09 | 16,3 % | ~10 % |
| Giới hạn / nơi cho làm lại (as of) | 10 | 7,6 % | ~10 % |
| Kết (trả lời móc, đóng vòng hình) | 11 | 6,9 % | 5–10 % |

**Lệch quá ±5 điểm % (phải nêu tên):**
- Đoạn 09 chiếm 16,3 % so với đích ~10 %. Lý do: điều kiện VÀNG (5) đòi trình bày các phía với nguồn riêng. Đoạn này gồm lời khai của hai phía, Minneapolis, SB 9, Freemark, Urban Institute và Auckland.
- Cơ chế 1–3 chiếm 45,2 % so với đích ~55 %. Nếu tính cả đoạn 07–08, vốn vẫn là lập luận cơ chế, thì là 60,2 %.

**Nội dung theo chỉ đạo của lệnh:**
- **Móc dạng câu hỏi:** "About one in thirteen American homes sits in a building with two to four apartments. Of the new homes finished in 2025, about one in a hundred did. So why did America almost stop building them?" Ngay sau đó nói rõ đây là hai phép đếm khác cơ sở và là "our calculation".
- **Góc cơ chế:** ba "khoá" là bản đồ (zoning), cầu thang (code) và ngân hàng (vạch 1–4 / 5+ căn, quy định mixed-use), cộng lực ngoài luật (chi phí xây, chi phí vay, giá thuê). Lời nói rõ hồ sơ **không đo được** phần đóng góp của từng yếu tố, và không gán nhân quả khi nguồn không nói.
- **Các phía:**
  - cầu thang: 3 tiếng nói phía cứu hoả, bên ủng hộ một cầu thang (Pew/CBNA), một nghiên cứu mô hình trung lập (Minnesota);
  - zoning: lời khai ủng hộ và băn khoăn từ văn bản lập pháp Washington; nghiên cứu cho kết quả "không thấy tác động" (Minneapolis, SB 9, Freemark) đặt cạnh nghiên cứu "có tăng" (Urban Institute, Auckland).
- **Không khung đảng phái; không nhắm nhà riêng của ai; không chạm vùng Crux.** Không nhắc chủng tộc hay redlining (không cần cho cơ chế đã chọn; Euclid chỉ dùng phần lý do Toà ghi).
- **Thay đổi biên tập lớn trong quá trình kiểm:**
  - Bỏ trích "mere parasite" của Euclid, vì 2/3 người đọc mù ở vòng 2–3 thấy nó gợi khung chống zoning. Thay bằng đoạn Toà liệt kê lý do (chiều cao, khối tích chắn nắng và không khí, xe cộ) cùng vế "in a different environment… highly desirable, come very near to being nuisances".
  - Thêm đoạn 07 "lực ngoài luật" sau khi 3/3 người đọc vòng 1 hỏi về chi phí và lãi suất.
  - Thêm câu phân loại "khoá nào chặn loại nhà nào" (2/3 người đọc vòng 2).
- **Câu miễn trừ:** "This video explains how the system works. It isn't financial or investment advice." Nằm trong 30 s đầu (ước kết thúc ở ~29 s).

## 4. Kiểm mù và REVIEWER (`k2c-t1-06/ai.py`, `claude -p` ghim model, thư mục trống, không subagent)
**Kiểm mù**: R1 người xem phổ thông, R2 người xem nhạy với thiên lệch chính trị, R3 người làm phát triển nhà ở.

| Vòng | Bản | Móc (R1/R2/R3) | Mạch cơ chế | Nghiêng | Tin cậy | Điểm ≥ 2/3 đã sửa |
|---|---|---|---|---|---|---|
| 1 | v1 | 7/7/7 | 8/8/8 | **pro-development 3/3** | 7/7/7 | kết lạc quan quá; thiếu chi phí và lãi suất (3/3); trộn loại nhà (2/3); số liệu dồn ở 03/08/09; thuật ngữ |
| 2 | v2 | 6/7/7 | 6/7/6 | **none 3/3** | 8/8/7 | đoạn 04/06 dày; cần bảng khoá × loại nhà; cú rơi 1986–1990 bỏ lửng; phía ủng hộ một cầu thang nhiều chỗ hơn |
| 3 | v3 | 6/7/7 | 6/6/6 | **none 3/3** | 8/7/7 | mở đầu chậm vì miễn trừ; lịch sử 02 dài; "mere parasite" (2/3) |

Kết thúc trả lời câu hỏi móc: 3/3 ở vòng 1–2; 2/3 ở vòng 3, R3 muốn thêm ví dụ tài chính dự án.

**REVIEWER Opus** (luật kênh + LUAT-G §1–§6 + QUAN-TRI-RUI-RO §1–1.1 + claims):

| Lượt | Bản | Major | Block | Minor | Major chính |
|---|---|---|---|---|---|
| 1 | v1 | 13 | 0 | ~30 | nhân quả 07/10; cắt trích (Sterling Heights, Freddie Mac); thiếu nguồn cho phía ủng hộ; Euclid "only in the fourth"; as-of Arlington, SBCC |
| 2 | v2 | 10 | 0 | ~23 | nhãn calc ở móc; "steepest"; "houses" chưa có nguồn; kết một phía; bỏ Auckland |
| 3 | v3 | 5 | 0 | ~20 | "one state counted in full"; nhãn C63; "near their peak"; tóm tắt nghiên cứu lệch; SBCC |
| 4 | v4 | 5 | 0 | 16 | trích Euclid thiếu mệnh đề chính; xếp hạng "fire-resistant"; ngày "June 2024" suy ra; "similar pattern"; nói rộng về California |
| 5 | v5 | 2 | 0 | 20 | điều kiện thị trường gần đây áp cho 5 thập kỷ; SB 9 thì hiện tại |
| 6 | v6 | 1 | 0 | 14 | "no single lock did it" ngầm cho là nhân quả |
| 7 | v7 | 4 | 0 | 13 | câu IBC/Washington mơ hồ và thiếu as-of; câu hỏi "how much of the decline comes from each" ngầm nhân quả; tóm tắt đoạn 09 lệch |
| 8 | v8 | **0** | 0 | 12 | — |
| kiểm chứng | v8.1 | 1 | 0 | 10 | câu "bank line bites" mất nguồn sau khi bỏ trích MHC → thay bằng đúng chữ REVIEWER đề xuất ("sorts buildings at five homes…") |

- **Đánh giá:** hiện tượng không hội tụ lặp lại đúng như BAI-HOC-K2 K3. Vòng 7 tăng lên 4 major, đều do câu mới viết ở v7. Cách xử lý từ v8: **bỏ câu gây rủi ro, không viết thêm** (bỏ SBCC, MHC, NYC code, Freddie Mac). Kết quả là v8 về 0 major.
- **Minor chưa áp, ghi lại:**
  - nhắc vụ kiện City of Yes;
  - phản biện AEI với nghiên cứu Urban Institute (chờ quyết §11);
  - chú thích chuỗi số trên hình (NRC/CNH, năm gốc);
  - tra lại as-of trước khi thu giọng.
- **REVIEWER gói tiêu đề** (điều kiện VÀNG 3): 0 major, chỉ minor; đã áp (§7).

## 5. Shot list — `k2c-t1-06/shots.yaml` → `SHOTLIST.md` (tính bằng `shotlist.py`)
Số liệu dưới đây là **tự đo của P trên timeline ước**, không phải kết quả checks/. Checks 1.10.1 (`q_types.py`, `q_scene.py`) chạy trên đặc tả `episode.yaml` khi dựng, nên chưa chạy được ở G1a vì chưa có đặc tả dựng hay khung 3D.

| Đo | Kết quả | Luật |
|---|---|---|
| Tổng (ước) | 15,58 phút, 90 shot | 12–16 phút |
| scene3d / chart3d / map | 36,2 % / 24,8 % / 18,0 % | — |
| card (`the`) | **15,2 %**, liên tục dài nhất 29 s | ≤ 25 %, ≤ 90 s |
| photo + document + footage | **5,9 %** (2,5 + 1,2 + 2,2) | ≤ 40 %, ≤ 8 s/clip, document ≤ 3 s |
| Số neo hiện bằng chart3d/scene3d | **22/29 = 76 %** (6 trên map, 1 trên ảnh) | ≥ 60 % |
| Cùng (scene_id, camera_id) > 2 lần | 0 (không cặp nào đúng 2 lần) | ≤ 2 |
| Bối cảnh 3D | corner 14,0 % (liên tục ≤ 49 s); nửa sau có 5 bộ cảnh | ≤ 25 %, ≤ 90 s, nửa sau ≥ 3 |
| Địa danh có shot map | 11/11 | mọi địa danh |
| Người có photo hoặc ly_do | 3/3: Hoover, Sutherland → photo (CAN-TAI-HO); Yonah Freemark → ly_do (người còn sống, không có ảnh có giấy phép đã kiểm) | — |

- **Bộ cảnh 3D dựng riêng (7):**
  - `corner`: toà góc phố, có chế độ cắt lớp;
  - `street`: dãy duplex → walk-up;
  - `tiers`: sa bàn 4 tầng khu kiểu Euclid, ghi "illustration";
  - `lot`: lô nhỏ và ô đỗ xe;
  - `stairs`: mặt cắt sàn 1 vs 2 cầu thang;
  - `bank`: hàng khối 1–4 | 5+;
  - `ends`: sa bàn "hai đầu" 1972/2025.
- **Biểu đồ và bản đồ:** 12 chart3d và 1 bản đồ Mỹ 3D (camera theo nơi, có khung chèn Auckland).
- **Nhịp huyền thoại vs hồ sơ (đoạn 09):** khung đôi COMMON CLAIM ↔ RECORD, nhãn hai bên, nguồn nằm bên RECORD (BAI-HOC #92).
- **Footage chỉ 5,9 %** (trần 40 %). Theo BAI-HOC-K2 K7, thẻ được thay bằng số đặt trong cảnh 3D và chart3d, và thẻ còn 15,2 % (Steel 45 %). Có thể tăng ảnh lưu trữ ở đoạn 01–02 nếu chủ dự án muốn (§11).

## 6. Footage và ảnh nguồn ngoài (QUAN-TRI-RUI-RO §6.6)
**Thử tải mỗi nguồn** (12/10, ~14:35–15:40 UTC, từ container; tệp không commit, nằm ở `/var/tmp/k2-footage/k2c-t1-06/` và scratchpad):

| Nguồn | Kết quả |
|---|---|
| LoC Detroit Publishing (item 2016794835, Connecticut Ave c1904) | HTTP 200 qua tile.loc.gov: r.jpg 63 463 B (SHA 99ad2388…), v.jpg 1024 px 157 513 B. TIFF gốc 159 MB: HEAD 200 |
| LoC HABS (ny0362, 935 St Nicholas Ave, 1979) | HTTP 200: r.jpg 59 277 B (SHA 22332a76…), v.jpg 1024 px |
| LoC FSA/OWI (2017790836, Corner store, Durham, 1940) | HTTP 200: r.jpg 116 846 B (SHA bb17bdc0…), v.jpg 1024 px |
| Pexels CDN | ảnh 2 422 958 B (SHA 38987a81…); video 4 806 474 B (SHA 70516310…) |
| Pixabay CDN | ảnh 335 162 B (SHA 3e16c268…); video 33 627 523 B (SHA d69390a1…) |

- **Chặn:** trang item và trang quyền LoC trả **403/503**. Từ ~15:00 UTC, tìm kiếm LoC trả **trang thử thách Cloudflare** (403). Vì vậy **chưa đọc được "Rights Advisory" từng item** → `CAN-TAI-HO.csv`.
- **Khoá API** (chỉ in tên): `PEXELS_API_KEY`, `PIXABAY_API_KEY`, `PIXABAY_VIDEO_API_KEY`. Gọi thử một lượt mỗi loại, **đều HTTP 200**:
  - Pexels ảnh `/v1/search`;
  - Pexels video `/v1/videos/search`;
  - Pixabay ảnh `/api/`;
  - Pixabay video `/api/videos/`.
  
  Không in khoá ra log (đã `grep` tệp kết quả: 0 lần xuất hiện).
- **Điều khoản API** (đọc qua WebFetch 12/10):
  - **Pexels:** "show a prominent link to Pexels", ghi công nhiếp ảnh gia khi có thể; giới hạn "200 requests per hour and 20,000 requests per month"; cấm sao chép chức năng lõi.
  - **Pixabay:** "requests must be cached for 24 hours", "permanent hotlinking… is not allowed", "download them to your server first", "Systematic mass downloads are not allowed"; 100 lượt/60 s.
  - Phiên này dùng ~30 lượt tìm và lưu kết quả JSON vào scratchpad.
- **Ứng viên** (`k2c-t1-06/footage-ung-vien.csv`, cột theo §6.4 + ghi chú): 6 clip/ảnh Pexels đã tải và có SHA256:
  - NYC rooftops;
  - fire escape;
  - Chattanooga townhouse;
  - cẩu xây dựng (không rõ địa điểm → nhãn "illustrative", không gán nơi chốn);
  - Chicago residential;
  - ảnh Bay Ridge (Brooklyn), toà góc phố có cửa hàng.
  
  Đã xem khung đầu/giữa/cuối: không người nhận diện được, không logo trọng tâm. Ảnh Bay Ridge có biển hiệu nhỏ, chỉ ngẫu nhiên. Thêm 1 ảnh LoC đã tải (FSA Durham) và 4 tài liệu liên bang, dựng lại chữ.
- **Loại khỏi danh sách** (không dùng): clip quay ở Kiev, Nga, Tokyo, London, Việt Nam (tránh gán sai địa điểm, chính sách "Misattributed"); ảnh có biển hiệu nhãn hiệu làm trọng tâm.
- **`k2c-t1-06/CAN-TAI-HO.csv`** (5 dòng):
  - chân dung Hoover;
  - chân dung Sutherland;
  - Detroit Publishing "Corner of Fifth Ave and Wood St, Pittsburgh";
  - FSA Durham: đã có ảnh, chỉ cần xác nhận quyền;
  - HABS 935 St Nicholas: dự phòng.

## 7. Tiêu đề — `k2c-t1-06/titles.txt`
1. **Why Did America Almost Stop Building Small Buildings Like This?** (63 ký tự). Dựa trên ứng viên của chủ dự án: thêm "Did… Almost…?" để đúng số liệu ~1 % và đúng dạng câu hỏi, và đổi "Apartments" thành "Small Buildings" theo REVIEWER (toà lớn tăng lên 57 % căn hộ mới).
2. **What Happened to America's Small Apartment Buildings?** (53)
3. **Why Are Duplexes to Fourplexes So Rare Among New US Homes?** (58)
- **Chữ thumbnail (4 từ):** `1% OF NEW HOMES`. Số có trong video (đoạn 00, 08).
- **Kiểm:** `toolkit/market/brief.py` (gói k2): 0 cảnh báo. REVIEWER Opus: 0 major. Không có cụm cấm §1.2, không có từ thuộc vùng Crux §7.

## 8. Ước giờ máy và chi phí
**Đo thật ở G1a:**

| Hạng mục | Số |
|---|---|
| API (`kiem-mu/cost.jsonl`) | **$7,74**, 19 lượt: 9 Sonnet $0,73; 10 Opus $7,01. Model yêu cầu = model thực chạy ở mọi lượt |
| API ngoài sổ | 1 lượt REVIEWER v7 bị dừng giữa chừng (tôi dừng bằng PID khi phát hiện nó chấm nhầm bản chưa cắt). Không ghi được chi phí; nếu bị tính, tối đa khoảng $0,75 |
| Token phiên P (log phiên, khử trùng theo mã tin nhắn) | sinh 0,18 triệu; ghi cache 0,51 triệu; đọc cache 57,1 triệu (tới lúc đo ~15:40 UTC) |
| Token 5 subagent nghiên cứu | 0,91 triệu (theo thông báo hoàn tất của từng agent); ghi cache 0,90 triệu, đọc cache 37,2 triệu |
| ElevenLabs | 0 ký tự (G1a không thu giọng) |
| YouTube Data API | 0 lượt |

**Ước cho bản đầy đủ** (dựa trên đo thật ở K2G-01; máy 4 vCPU, tối đa 3 tiến trình dựng):

| Hạng mục | Ước |
|---|---|
| Khung 3D 1080p SPP4 | 3D + nền thẻ ≈ 877 s × 24 = 21 050 khung × 5,07 s/khung/tiến trình (Steel: 3 × 11,6 h / 24 723 khung) ≈ 29,6 giờ-tiến trình → **≈ 10 giờ đồng hồ**. Nếu vật liệu PBR và ánh sáng giàu hơn theo K7 làm chậm 30 %, thì ≈ 13 giờ |
| Nháp 960×540 + ghép nháp | ≈ 3 giờ (Steel 1,5 + 1,5) |
| Ghép, trộn, master 1080p + 2 Short | ≈ 2 giờ |
| QC, một lượt sửa, chấm mù | ≈ 2 giờ |
| **Tổng** | **≈ 17–20 giờ đồng hồ** (Steel ≈ 18) |
| ElevenLabs | lời ≈ 14 300 ký tự gửi + Short ≈ 800 → ≈ 15 100 ký tự gửi (bộ đếm tính ≈ 0,44 ký tự/ký tự gửi, BAI-HOC #103) |
| API ở G2 | ≈ $2–3 (Steel G2: $1,79). Tổng tập ≈ $10–11, trần $40 |
| Footage | Pexels/Pixabay $0; tải lại theo `url_tai` khi dựng, kiểm SHA |

## 9. Chỉ số nằm trong ±5 % quanh ngưỡng (luật cứng CLAUDE.md)
- **Thời lượng ước 15,58 phút** so với trần 16 phút: thấp hơn 2,6 %. Nếu Eric đọc chậm hơn 3 % thì vượt trần. Khi đó rút đoạn 09 trước (đang dài hơn đích).
- **Móc ≈ 14,3 s** so với trần 15 s: thấp hơn 4,7 %. "2025" đọc thành "twenty twenty-five" có thể đẩy lên ~14,8 s. Kiểm lại trên bản thu.
- **Câu miễn trừ kết thúc ở ~29 s** so với mốc 30 s.
- Các chỉ số khác không sát ngưỡng: thẻ 15,2 % (trần 25 %), số neo 3D 76 % (sàn 60 %), nguồn ngoài 5,9 % (trần 40 %), tiêu đề dài nhất 63 ký tự (trần 70).

## 10. Sai lệch, rủi ro
- **Sai lệch:**
  - đoạn 09 lệch tỷ lệ (§3);
  - ảnh LoC chưa xác nhận quyền từng item;
  - 1 lượt API ngoài sổ (§8);
  - các dấu xung đột trong `AUTHORSHIP.md` lọt vào một commit merge rồi mới gỡ (§1);
  - shot list đo bằng công cụ của P, chưa chạy checks 1.10.1 (cần `episode.yaml`).
- **Rủi ro:**
  - **as-of thay đổi trước khi thu giọng:** SBCC 16/10, phúc thẩm NYC, IBC 2027 → bảng §1b, tra lại;
  - REVIEWER không hội tụ: mỗi lượt sửa câu có thể làm lộ lỗi mới → chỉ sửa minor đổi chữ, không thêm thông tin;
  - Q27 tay nghề (Steel 5/10) → shot list giảm thẻ và tăng cảnh 3D có số bám vật thể (K7);
  - footage lưu trữ có thể bị Content ID nhận nhầm → sổ SHA.
- **Đề xuất ghi BAI-HOC-K2 (chờ duyệt):**
  - "khi REVIEWER không hội tụ, bỏ câu gây rủi ro thay vì viết thêm" (số đo: vòng 7 lên 4 major vì câu mới; vòng 8 về 0 sau khi chỉ bỏ câu);
  - "trích dẫn gây cảm xúc mạnh trong nguồn lịch sử ('mere parasite') bị người đọc mù coi là khung một phía dù quy chủ thể đúng; thay bằng phần lý do của chính nguồn".

## 11. Việc đang chờ chủ dự án
- **D1. Duyệt đề tài và mức VÀNG ở G1** (điều kiện VÀNG: chủ dự án duyệt G1, ghi vào `AUTHORSHIP.md`).
- **D2. Duyệt lời khoá ứng viên v8.1** (`k2c-t1-06/script.md`, 15,6 phút ước). Kèm hai lựa chọn:
  - (a) thêm một câu về phản biện của AEI với nghiên cứu Urban Institute (REVIEWER minor), hoặc giữ nguyên;
  - (b) thêm câu "a lawsuit against the plan was dismissed in November 2025" cho City of Yes, hoặc giữ nguyên.
- **D3. Chọn tiêu đề** (1, 2 hoặc 3) và duyệt chữ thumbnail `1% OF NEW HOMES`.
- **D4. Tải hộ hoặc xác nhận quyền 5 mục LoC** trong `CAN-TAI-HO.csv`. Nếu không có ảnh Hoover và Sutherland, shot people chuyển sang ly_do và dùng thẻ tên.
- **D5. Shot list:** duyệt 7 bộ cảnh 3D và tỷ lệ (thẻ 15 %, nguồn ngoài 6 %). Có muốn tăng ảnh lưu trữ (Detroit Publishing, HABS) ở đoạn 01–02 không? Dựng khung mẫu chờ bộ công cụ phiên V.
- **D6.** Sau 16/10: cho tra lại SBCC và quyết có đưa câu Washington single-stair trở lại đoạn 10 không.
- **D7.** Ghi 2 bài học đề xuất ở §10 vào BAI-HOC-K2.
