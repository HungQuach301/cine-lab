# LAYOUT W1 — Cảnh 1–3 (s01 → s24c · 0:00,00–0:59,00) · Cổng 5, giai đoạn A

- **Phiên:** W1 (xưởng). Nhánh worktree tạo từ `claude/cine-lab-m2-cong5-layout-24o5fp` (085fd31).
- **Mã:**
  - `design/cong5/layout/shots_w1.js`
  - `design/cong5/layout/sets.js` (bộ phố)
  - `order_w1.js` **không đổi**: thời lượng giữ nguyên.
- **Tài liệu:**
  - continuity: `shots/layout/continuity/canh-1.md`, `canh-2.md`, `canh-3.md`;
  - manifest Cổng 6: `shots/layout/shots_w1.json`;
  - ảnh probe: `reports/m2/cong5/w1/` (tờ tổng 23 shot và 9 ảnh trước/sau).
- **Tình trạng:** giai đoạn A. Chỉ probe (3 khung/shot, 960×540), **chưa render đầy đủ**. Mặt Ida (W3) và cuối phố (`sets_end.js`, W2) chưa tích hợp.

## 1. Tóm tắt
- **23 shot, 59,0 s (1 416 khung), không đổi id, không thêm/bỏ shot.** Tổng phim giữ 2:22,5 (142,5 s, đo bằng `render_film.js --events`).
- **Thoại và mốc thoại giữ nguyên văn:**
  - L1 "Evening, old street." ở 12,0 s (s05);
  - L2 "Not yet... not yet." ở 49,5 s (s22).
  - Mốc sự kiện trong `common.js` không đổi.
- **Chiều sâu phố (`sets.js`):**
  - thêm lớp nhà sau trên sườn đồi (bắc cao, nam thấp, dâng dần về đầu dốc 3,5 %);
  - thêm quảng trường có nhà bao ba phía;
  - thêm năm dãy nhà xa xếp bậc theo cung sau quảng trường;
  - thêm sương theo shot.
  - Kết quả: hết nền trống và chân trời phẳng ở s02, s08, s10e, s12, s19 (ảnh trước/sau).
- **Sửa continuity:**
  - s15 hết hai cái thang;
  - s23 Ida chạy vác thang (v2 chạy tay không trong khi thang đã tựa sẵn ở cột);
  - s22 bỏ nhịp xoè tay mâu thuẫn với sào mồi.
- **Sửa quang học theo luật 3.1/3.3:**
  - s13: bóng trên tường tan trong 0,5 s khi trắng tới;
  - s14: không còn bóng dài mờ.
- **Máy tĩnh thật** ở s05, s22 (v2 đặt máy theo đầu mỗi khung nên máy trôi theo diễn xuất).

## 2. Bảng shot cuối
Tiêu cự là mm tương đương full-frame (FOV dọc = 2·atan(12/f)). Vị trí máy là (x; y; z) theo mét, hệ toạ độ bộ phố ở `continuity/canh-1.md`. "→" là điểm nhìn. P = phải màn hình, T = trái.

| id | mốc (s) | dài | cỡ | mm | vị trí máy → điểm nhìn | chuyển máy | dàn dựng | hướng màn hình |
|---|---|---|---|---|---|---|---|---|
| s01 | 0,0–4,0 | 4,0 | EWS | 28 | máy khoá s1 (−14; 39; 34) → (10; 0; −71) | dolly vào 5 %, có gia tốc | thành phố chạng vạng, chấm hổ phách hiện dần | phố Ostler cong xuống dốc giữa khung |
| s02 | 4,0–8,5 | 4,5 | WS | 35 | (103,5; 1,45; 3,6) → (116; 2,6; −1,6) | tĩnh | **mới:** máy chéo lên phố. Ida từ xa tiến về máy, vác thang; L1–L3 đã sáng nối về quảng trường | Ida trôi P → T, lớn dần |
| s03 | 8,5–10,5 | 2,0 | MS thấp | 50 | (103,2; 0,95; −0,2) → (106; 3; −4,3) | tĩnh | lên bậc cuối, mở van, "phụp" 9,2 s | Ida giữa–phải, cột L4 cạnh bà |
| s04 | 10,5–12,0 | 1,5 | WS cao | 28 | (99,5; 5,2; 3,2) → (106,5; 1,2; −4,6) | tĩnh | Ida trên thang, bóng dài trên mặt tiền; phố dựng tới quảng trường | phố lùi về P |
| s05 | 12,0–16,0 | 4,0 | MCU | 85 | đầu Ida + (−1,55; 0,02; 1,35), đặt một lần | **tĩnh** (v2 trôi) | đếm ba ở 12,3 / 12,9 / 13,5; L1 | 3/4 trước-trái, nhìn lồng đèn (P) |
| s06 | 16,0–19,0 | 3,0 | CU insert | 100 | bám đồng hồ, hướng (−0,15; 0,8; 0,6), 0,32 m | bám đồng hồ | 7:31, gõ kính 2 lần | POV chúc |
| s07 | 19,0–23,0 | 4,0 | WS | 35 | (96; 1,4; 4,3) → (93,6; 1,6; −2,6) tới (92,4; 1,4; 4,3) → (90; 1,6; −2,6) | dolly trái 3,6 m, easeIO | **đổi:** lệch máy về T để có khoảng trống phía trước Ida; qua cột L5, bóng quét | Ida P → T |
| s08 | 23,0–25,0 | 2,0 | WS tele | 135 | (58; 1,6; 0,6) → (176; 3,4; 0,2) | tĩnh | Ida đi về máy; hậu cảnh quảng trường có nhà bao và dãy nhà xa trong sương `[40, 330]` | Ida tiền cảnh T–giữa, tiến về máy |
| s09 | 25,0–28,0 | 3,0 | MS thấp | 50 | (169,2; 1,7; −3,4) → (176; **5,7**; 0,5) | tĩnh | đồng hồ bật 8:00, DING; mái nhà quảng trường neo đáy khung | cột giữa khung |
| s09w | 28,0–30,0 | 2,0 | CU insert POV | 105 | từ đồng hồ về mắt + 0,55 m cao, 0,42 m | bám đồng hồ | 7:53 dưới L6 | POV |
| s10e | 30,0–32,0 | 2,0 | MS chèn thấp | 35 | **(163,0; 1,3; 11,6)** → (166,8; 4,4; 6,6) | tĩnh | bóng đèn quảng trường nhấp 2 lần, đứng; đồng hồ hậu cảnh; nhà quảng trường làm nền | đầu cột P–giữa |
| s10 | 32,0–35,0 | 3,0 | EWS | 28 | máy khoá s1 | tĩnh | sóng trắng lan xuống dốc; khối cuối còn hổ phách | sóng từ quảng trường |
| s11 | 35,0–37,0 | 2,0 | MS | 50 | (61,6; 2,5; −1,2) → (64; 2,9; −4,4) | tĩnh | Ida trên thang L7 quay về quảng trường | bà nhìn sang P |
| s12 | 37,0–39,5 | 2,5 | WS qua vai | 35 | (62,3; 3,4; −5,0) → (100; 2,6; −1,0) | tĩnh | P2 (x = 85) bật; phố dựng tới quảng trường, sương `[30, 220]` | trên trục, sóng tiến về máy |
| s13 | 39,5–41,5 | 2,0 | MS thấp nhẹ | 50 | (66,8; 2,0; −1,0) → (64; 2,9; −4,4) | tĩnh | trắng tới 39,55; **bóng tan trong 0,5 s**; bà cúi | 3/4 trước-phải |
| s14 | 41,5–43,5 | 2,0 | MS chúc | 28 | **(65,9; 4,5; −2,3) → (64; 1,4; −4,7)** | tĩnh | **mới:** máy cao phía đầu dốc. Tay trái giơ; không bóng dài | Ida giữa–trên khung, nền đá dưới |
| s15 | 43,5–45,0 | 1,5 | WS | 35 | **(69,5; 1,5; 3,4) → (60; 2,1; −4,0)** | tĩnh | **mới:** nhìn xuôi dốc. Tụt thang, nhấc thang lên vai (1,1 s), quay; đoạn dưới tối (sương `[12, 55]`) | Ida P, quay sang T |
| s19 | 45,0–47,5 | 2,5 | WS | 35 | (41; 1,7; 1,0) → (53; 3; −0,5) | tĩnh | L8 nở, bóng dài; P3 bật, bóng tan; **phố dựng tới quảng trường** | Ida T; trắng đuổi từ P |
| s21 | 47,5–49,5 | 2,0 | MCU tay | 85 | (20,1; 3,1; −2,3) → (22; 3; −4,5) | tĩnh | trèo nhanh (**trong khung từ khung đầu**), tuột sào, chụp lại | 3/4, cột P |
| s22 | 49,5–52,5 | 3,0 | MCU | 85 | faceCam lệch −12°, 1,2 m, đặt một lần | **tĩnh** (v2 trôi) | L2; tay phải trên van; L10 bắt lửa ở khung cuối | 3/4, bà nhìn lên lồng |
| s23 | 52,5–55,5 | 3,0 | WS | 28 | **(19,5; 1,6; 2,8) → (4,5; 2,5; −2,9)** (`S23_CAM`) | tĩnh | Ida **vác thang** chạy tới L11, dựng thang, trèo, thắp; góc tối; P5 tắt | Ida chạy vào chiều sâu về cuối phố |
| s24 | 55,5–57,5 | 2,0 | MS hơi cao | 35 | (14,5; 2,4; 3,0) → (6; 2,2; −2,3) | tĩnh | đếm ba lần 2; Cas ở nền (`casSpot`) | Ida P, Cas T |
| s24c | 57,5–59,0 | 1,5 | MS | 50 | (cx + 1,8; 1,0; cz + 1,0) → (cx; 0,9; cz) | tĩnh | Cas ở chân tường, quay đầu về Ida / L11 | Cas T–giữa, nhìn sang P |

**Trục 180°.** Máy ở phía nam phố ở mọi shot, trừ s12. s12 đặt ngay trên trục nhìn dọc phố lên quảng trường (giống v2, qua vai). Ida đi P → T ở s02, s07, s15. Sóng trắng tới từ P (s12, s19) hoặc từ hậu cảnh.

**Phân bố cỡ cảnh / tiêu cự (F4):**
- EWS 2 · WS 8 · MS 8 · MCU 3 · CU 2;
- tiêu cự 28–135 mm.

## 3. Thay đổi so với animatic v2 và lý do
| Shot | Thay đổi | Lý do |
|---|---|---|
| s02 | Máy chéo lên phố thay vì nhìn thẳng mặt tiền. Ida xuất phát x = 114,5 (v2: 112,5) | v2 là "bức tường mặt tiền", không chiều sâu, Ida chìm tối. Nay đọc được địa lý: đèn đã thắp ở sau lưng bà (P), quảng trường ở đầu dốc |
| s04 | Dựng tới x = 200 | Mép phải khung không còn hết phố |
| s05, s22 | Máy đặt một lần theo tư thế t = 0 | SHOTLIST ghi "tĩnh", nhưng v2 đặt máy theo đầu mỗi khung nên máy trôi theo nhịp tay/đầu (F3) |
| s07 | Điểm nhìn lệch 2,4 m về T | Khoảng trống phía trước hướng đi (lead room). v2 để Ida ở giữa |
| s08 | Sương `[40, 330]` | v2: cột đồng hồ đứng giữa khoảng trời trống, chân trời phẳng. Nay có quảng trường, nhà bao, dãy nhà xa lên đồi |
| s09 | Điểm nhìn hạ 0,6 m | Mái nhà quảng trường neo đáy khung, định vị nơi chốn |
| s10e | Máy dời vào quảng trường (x = 163,0) | Mặt tiền góc quảng trường mới dựng ở x = 162. Vị trí v2 (161,3) nằm sau tường (probe vòng 1 thấy khung cửa sổ che khung) |
| s12 | Dựng tới x = 200, sương `[30, 220]` | Hậu cảnh đầu dốc có quảng trường, không lộ mép bộ |
| s13 | `gasLight` L7: 1 → 0,15 trong 0,5 s sau khi trắng tới | v2: bóng lớn trên tường còn ở cuối shot, trái luật 3.3 |
| s14 | Máy cao phía đầu dốc; L7 không đổ bóng; tay trái giơ cao hơn (tư thế cục bộ `liftHigh`) | v2: bóng dài mờ còn trên đá lát (trái kịch bản "Her long shadow is gone"); đầu Ida bị cắt; lồng đèn che người |
| s15 | Máy nhìn xuôi dốc; thang tựa cột ẩn khi bà nhấc thang (1,1 s); sương gần | v2: hai cái thang cùng lúc; khung chỉ là mặt tiền. Nay thấy nơi bà sắp chạy tới |
| s19 | Dựng tới x = 200 | v2: sau x = 80 là chân trời phẳng |
| s21 | Bắt đầu trèo ở bậc cao hơn | v2: 0,5 s đầu khung không có người |
| s22 | Bỏ nhịp xoè hai tay cuối shot; tay phải giữ van tới khi lửa bắt | Liên tục sào mồi (s21 cầm sào tay phải → s22 sào ở tay trái ngoài khung) |
| s23 | Ida vác thang khi chạy, dựng thang ở 1,1 s; máy cố định `S23_CAM` hơi lệch T | v2: chạy tay không trong khi thang đã tựa sẵn. Máy cố định để W2 dựng cuối phố đúng khung |
| s24, s24c | Vị trí Cas đọc từ `endInfo.casSpot` (W2). Máy s24c bám Cas | Chờ W2 quyết địa lý nhà kho. Mặc định giữ vị trí v2 |

Không đổi: s01, s03, s06, s09w, s10, s11 (chỉ hưởng thay đổi bộ phố).

## 4. Bộ phố `sets.js`: phố dốc, cong, có chiều sâu
**Đã làm (an toàn, không đổi hệ toạ độ):**
- **Giữ nguyên** lòng phố thẳng, phẳng trong đoạn diễn x = 0…160.
  - `LAMP_X`, `LAMP_Z`, `POST_X`, `POST_Z`, `WALK_Z`, `CLOCK` không đổi nghĩa và giá trị.
  - Shot W2 dùng bộ phố vẫn dựng được: `--meta-only` s35, s37w, s45c chạy hết khung, không lỗi (32,3 s). Chưa probe hình các shot W2.
- `buildDepth()` mới, bật mặc định (`o.depth === false` để tắt):
  1. **Sườn đồi, lớp sau.**
     - Phía bắc: 3 dãy khối nhà trên thềm cao +2,6 / +6,4 / +10,5 m.
     - Phía nam: 1 dãy thấp −2,2 m.
     - Mọi nền dâng theo `hillY(x) = 0,035·(x − 80)` (cùng độ dốc 3,5 % của `groundY` trong s1 khoá).
     - Mái hai dốc, ống khói có chụp, ô cửa tối / vàng khoảng 5–12 %.
     - Nhìn lên phố: đường mái lớp sau dâng dần, **đọc được dốc**. Nhìn ngang: mái và ống khói chồng lớp.
  2. **Quảng trường** (x 162…202, z ±20).
     - Nhà mặt tiền chi tiết (`houses()`, cùng kiểu phố) bao ba phía, cộng hai đoạn góc ở x = 162.
     - Vỉa hè đá phiến. Nền đá lát mở rộng 44 × 40 m.
  3. **Năm dãy nhà xa** sau quảng trường (x ≈ 214…310).
     - Xếp bậc lên đồi, uốn theo cung (phố tiếp tục cong về bắc), phía bắc cao hơn.
     - Nhìn lên phố không còn chân trời phẳng.
  4. **`o.fog = [gần, xa]`** theo shot: tele/toàn cảnh cần sương xa hơn để lớp xa còn đọc được.
- Ngưỡng dựng quảng trường, cột điện quảng trường, đồng hồ: `x1 > 165` đổi thành `x1 > 150`.
- `st.gasLight(i)`: hệ số chỉ cho **nguồn sáng** của đèn khí i (ngọn lửa, kính, quầng giữ nguyên). Dùng cho "hổ phách chìm trong trắng" (s13, s14). Mặc định 1.
- **Móc cho W2:**
  - `buildStreetEnd` được gọi **trước** khi dựng hai dãy nhà;
  - `endInfo.houseX0` / `houseX0N` / `houseX0S` cho biết dãy nhà phố chính dừng ở đâu (mặc định −4);
  - `endInfo.casSpot = [x, z]` cho s24 / s24c.

**Không làm (không an toàn trong phạm vi W1):** cong và dốc **thật** của lòng phố trong đoạn diễn.
- Cong thật: dời đèn, cột, đường đi, vị trí nhân vật của cả W1 lẫn W2.
- Dốc thật: mọi `ladderAt`, `place(..., y0)` trong `common.js` và `shots_w2.js` phải theo cao độ.
- Xem đề xuất cho P ở mục 7.

**Ảnh hưởng tới W2:** shot W2 dùng `buildStreetSet` (x −12…30 và 140…200) sẽ có thêm lớp nhà sau và quảng trường. Đây là chủ đích (V3 "tường trống" cũng là thiếu chiều sâu). W2 nên probe lại s37w, s45c.

## 5. V3 — khung s23 (0:52,5) cần gì từ `sets_end.js` (gửi W2)
Máy s23 cố định: `S23_CAM`, pos (19,5; 1,6; 2,8), nhìn (4,5; 2,5; −2,9), 28 mm. FOV dọc 46,4°, ngang 74,6°; tâm khung ngẩng 3,2°.

Vùng thế giới lọt khung (tính từ hình học máy):
- Mặt phẳng x = −5 (tường nhà kho hiện tại, cách 26–51 m): z từ +10 (mép T) tới −37 (mép P), y tới 11,6 (T) … 20 (P) ở mép trên. Tâm khung ở z = −6,5, y = 3,1.
- Mặt phẳng x = −30 (cách khoảng 53 m): z +18 … −79.
- Vị trí trên khung (u ngang 0 = T, v dọc 0 = trên):
  - ngọn L11 (0,61; 0,42);
  - tâm tường nhà kho hiện tại (0,33; 0,38);
  - Cas mặc định (0,42; 0,59);
  - mép dãy nhà bắc x = −4 (0,49; 0,45), mép dãy nhà nam x = −4 (0,16; 0,43);
  - đầu cột góc P5 ra ngoài mép trên (0,16; −0,11): chỉ thân cột tối ở mép trái.

Probe hiện tại: tường vôi 24 × 11 m chắn ngang chiếm khoảng 30 % khung, phần trên–trái là một mảng phẳng không chi tiết (ảnh `s23_truoc-sau.jpg`).

**Yêu cầu (đề xuất, W2 quyết cách làm):**
1. **Phố không cụt.** Sau góc nhà kho, phố **rẽ** (khuyến nghị sang T khung, phía nam +z, vì mép T khung nhìn sâu tới z ≈ +10…+18) hoặc cong tiếp, **dốc xuống**: mặt phố hạ dần sau x < −5.
   - Mắt phải đi được qua góc nhà kho vào chiều sâu ở vùng u ≈ 0,15–0,35, v ≈ 0,4–0,5.
2. **Nhà kho có hình khối đọc được**, không là mặt phẳng trắng.
   - Cần: mái, máng / ống thoát nước, cửa bốc hàng, **hốc vòm sâu khoảng 4 m** (luật 1, cảnh 5), mép chân tường có bậc.
   - Mặt vôi trắng chiếm ≤ khoảng 20 % khung s23, và tối (góc tối: chỉ L11 và ánh xa).
3. **Lớp xa** sau ngã rẽ: 2–3 lớp mái / ống khói hạ dần (xuống dốc).
   - Vài ô cửa vàng; quầng trắng mờ của các phố đã có điện hắt lên trời đêm ở chân trời trái (không hồng; luật v0.4 "Đêm").
   - Sương tối (#0c1024) để lớp xa nhạt dần.
4. **Góc L11 "lùi sau góc nhà"** (luật v0.4): nếu dời tường nhà kho, giữ L11 (x = 8, z = −3,9) và P5 (x = 10,8, z = +3,9) nguyên chỗ.
   - Nếu dãy nhà phố chính phải dừng sớm hơn x = −4, trả `endInfo.houseX0N/houseX0S`.
5. **`endInfo.casSpot = [x, z]`** cho s24 / s24c:
   - chân tường nhà kho (≤ 0,5 m tới tường), **cách L11 ≤ 5 m** để mặt Cas ấm lên vì L11 (kịch bản 0:57 "his face warm in the new amber");
   - khớp với bộ tường cảnh 4 của W2 (L11 cách tường 4,2 m).
   - Ở vị trí mặc định (−1,2; −2,2), cách L11 9,4 m, Cas **không đọc được** trên probe s24.
6. Giữ `endInfo.warehouseWall` (hoặc tương đương) nếu P cần cho C3 / luật máy.

## 6. D2 — mũ Ida #262a33 trên probe (đo thật)
Cách đo: vùng mũ chọn tay trên ảnh probe 960×540, lấy 60 % điểm ảnh tối nhất, trung vị sRGB (`hat.py` trong nhật ký phiên). Albedo sheet v1.3: #262a33 (sắc 222°, bão hoà 0,25).

| Shot (khung giữa) | Nguồn chính trên mũ | Màu thấy | Sắc | Bão hoà |
|---|---|---|---|---|
| s05 | đèn khí L4, sát trên đầu | #57260e | 20° | 0,84 |
| s11 | đèn khí L7, ngay trên mũ (phơi sáng 2,2) | #f7b870 (gần cháy) | 32° | 0,55 |
| s21 | trắng điện | #101118 | 232° | 0,33 |
| s22 | trắng điện | #08070b | 255° | 0,36 |

**Kết luận:**
- D2 đã vào hình: dưới điện, mũ đọc **đen xanh** đúng hướng sheet.
- Dưới đèn khí ở gần, mũ vẫn đọc **nâu cam** (s05) hoặc **gần trắng cam** (s11, cháy sáng vì ngọn lửa cách vành mũ khoảng 0,5 m và phơi sáng 2,2). Đây là vật lý của nguồn hổ phách mạnh, không phải albedo.
- s11 cháy sáng là việc phơi sáng / ánh sáng (Cổng 7). W1 không tự đổi phơi sáng. Đề xuất ở mục 7.

## 7. Đề xuất đổi file chung / bible / sheet (gửi P)
1. **`common.js`: không cần đổi** cho giai đoạn A. Không đổi id, không đổi mốc.
2. **Sheet đạo cụ (P):** quy định chỗ để **sào mồi** khi đi/chạy (đề xuất: móc dọc thang). Hiện sào chỉ thấy ở s21.
3. **Cổng 7 (P):** trắng tràn đang là một `HemisphereLight` toàn cục.
   - Hệ quả: đoạn phố chưa có điện vẫn sáng trắng; s15 phải dùng sương gần để giả "đoạn dưới còn tối".
   - Đề xuất: ánh trắng theo khối (nhiều nguồn rộng có tầm, hoặc mặt nạ theo x) để đúng luật 2 và kịch bản 0:32 "Only the far end… keeps its amber".
4. **Cổng 7:** phơi sáng s11 (2,2) làm mũ / mặt cháy dưới L7. Cân nhắc 1,5–1,7.
5. **Cong / dốc thật cho phố (M3 / Cổng 7, cần P + chủ dự án):** uốn thế giới trong vertex shader (dời z theo (x − x_máy)², hạ y theo dốc) cho mọi vật liệu. Logic toạ độ giữ thẳng, hình ra cong.
   - Rủi ro: vị trí nguồn sáng tính trên CPU không uốn theo, nên ánh ở xa lệch. Chỉ an toàn nếu uốn nhỏ và nguồn gần máy.
   - Không đề xuất cho Cổng 5.
6. **Trạng thái đèn lồng ở cảnh 1** (quyết định sáng tạo, xem mục 8).

## 8. Hàng chờ chủ dự án (P ghi vào PLAN.md; W1 không sửa PLAN.md)
1. **Đèn lồng thắt lưng:** cháy từ s02 (như animatic v2 đã duyệt), hay tắt tới nhịp mồi đèn lồng ở L4 (kịch bản 0:08–0:12 "She tips the flame of her pole into the small tin lantern")?
   - Nếu theo kịch bản: thêm nhịp mồi đèn lồng vào s05 (không đổi thời lượng), và đèn lồng tắt ở s02–s04.
2. **s02 và s15 máy mới** (chéo lên phố / xuôi dốc) thay khung "mặt tiền": xin duyệt như thay đổi bố cục.
3. **Vị trí Cas / tường nhà kho** (theo mục 5): quyết cùng W2.

## 9. Kiểm và số đo
- **Probe:** 6 lượt chạy thành công + 1 lượt hỏng (lỗi cú pháp của tôi, dừng ngay ở shot đầu).

| Lượt | Shot | Khung | Thời gian thật |
|---|---|---|---|
| probe0 (nền v2) | 23 | 69 | 335,2 s |
| probe1 | 15 | 45 | 215,5 s |
| probe2 (toàn bộ sau sửa bộ phố) | 23 | 69 | 381,6 s |
| probe3 | 2 | 6 | 31,6 s |
| probe4 | 2 | 6 | 42,8 s |
| probe5 | 3 | 9 | 44,8 s |
| **Tổng** | 68 | 204 | **1 051,5 s** |

  - Khoảng 3,0–4,6 s/khung trên máy chung 4 vCPU; dựng cảnh 2–4 s/shot.
- **Không** dùng hàng đợi render (không có render nặng). Không render đầy đủ.
- **Luật máy (checks):** không chạy. Giai đoạn A không có lệnh kiểm của K cho gói W1. Chỉ số gần ngưỡng ±5 %: không có số đo nào để nêu.
- **Cú pháp:** `node --input-type=module --check` đạt cho `shots_w1.js`, `sets.js`. `render_film.js --list` in 52 shot; `--events` FILM_S = 142,5.
- **RIGHTS.md:** không có tài sản mới. Mọi hình học và kết cấu thêm vào đều sinh bằng mã (hàm có sẵn của Cổng 3: `houses`, `facadeTex`, `flagTex`, `windowUnit`). Mái hai dốc chép cách dựng `roofGeo` của s1.

## 10. Rủi ro còn lại
1. **s23, s24, s24c phụ thuộc `sets_end.js` (W2):** tường trống, vị trí Cas. Chưa thấy bản W2, nên chưa kiểm được V3 trên hình.
2. **Mặt Ida (W3)** chưa tích hợp. s05, s22 (cận mặt) sẽ đổi khi W3 vào.
3. **Tư thế ngoài sheet** (previs): `liftHigh` (s14), `watchHold`, `watchRaise`, `pole*`, `climb`, đổi đạo cụ tức thì (s15, s23). Cổng 6 phải hoạt hoạ thật các nhịp "nhấc thang", "dựng thang".
   - s14: tay giơ còn khó đọc ở máy cao (probe).
4. **Trắng tràn toàn cục** (mục 7.3). Sương gần ở s15 là giải pháp tạm cho layout.
5. **Lớp nhà sau lặp khối đơn giản** (hộp + mái + ô cửa phẳng). Ở tele s08 đọc được như khối trong sương. Ở Cổng 7 có thể cần thêm chi tiết nếu khung hẹp hơn.
6. **C3 / H1b** (Cổng 4): shot đi bộ s02, s07, s08 vẫn dùng chu kỳ đi cũ. Máy s02 mới làm Ida nhỏ hơn và chéo hơn, nên cần P chạy lại luật máy ở giai đoạn D.
