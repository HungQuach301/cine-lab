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
- **Giai đoạn C (mới nhất):** render đầy đủ 23 shot xong — xem mục 11.
- **Tình trạng (giai đoạn A):** giai đoạn A. Chỉ probe (3 khung/shot, 960×540), **chưa render đầy đủ**. Mặt Ida (W3) và cuối phố (`sets_end.js`, W2) chưa tích hợp.

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
| s22 | 49,5–52,5 | 3,0 | MCU | 85 | faceCam lệch **+45°** (Cổng 6; Cổng 5: −12°), 1,2 m, đặt một lần | **tĩnh** (v2 trôi) | L2; tay phải trên van; L10 bắt lửa ở khung cuối | 3/4, bà nhìn lên lồng |
| s23 | 52,5–55,5 | 3,0 | WS | 28 | **(27,0; 1,5; 3,8) → (4,5; 2,0; −1,5)** (`S23_CAM`, A2) | tĩnh | Ida **vác thang** chạy từ vũng trắng vào góc tối, tới L11, dựng thang, trèo, thắp; Cas đứng ở chân tường chim (casSpot (14,3; −7,15)); P5 và cột sân trước (17,0; −5,9) tắt; mặt vôi 18,5 % | Ida chạy vào chiều sâu, về cuối phố (giữa khung) |
| s24 | 55,5–57,5 | 2,0 | MS hơi cao | 30 | **(11,2; 2,1; 1,8) → (10,5; 1,8; −5,8)** (A2) | tĩnh | đếm ba lần 2; Cas nhỏ ở chân tường chim (casSpot (14,3; −7,15)); bóng Ida + thang trên tường | Ida T, Cas P |
| s24c | 57,5–59,0 | 1,5 | MS | 50 | **3/4 trước Cas, lệch −35° khỏi hướng nhìn về L11, cách 2,1 m** → (14,3; 0,95; −7,15) (A2) | tĩnh | Cas ở chân tường chim; mặt ấm yếu (L11 cách 7,1 m); không có bóng Ida/thang | Cas giữa–trái, nhìn sang T (về Ida) |

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
| s24, s24c | Vị trí Cas đọc từ `endInfo.casSpot` (W2 A2: (14,3; −7,15)). A2: máy s24 (11,2; 2,1; 1,8) 30 mm có cả Ida (T) và Cas (P); máy s24c 3/4 trước, Cas nhìn T | W2 đặt Cas ở phía +x của L11 → từ máy phía nam Cas ở PHẢI Ida (khớp quy ước cảnh 4–5 "Ida trái, Cas phải"). Giai đoạn C dùng casSpot (10,35; −7,15); B1 dời sang (14,3; −7,15) |

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
   - Vài ô cửa vàng. ~~Quầng trắng mờ của các phố đã có điện hắt lên trời ở chân trời~~ — **rút lại**: chủ dự án quyết (world-rules v0.5 @5ec0985) KHÔNG có quầng trắng ở chân trời, kể cả cảnh toàn; trời tối có sao.
   - Sương tối (#0c1024) để lớp xa nhạt dần.
4. **Góc L11 "lùi sau góc nhà"** (luật v0.4): nếu dời tường nhà kho, giữ L11 (x = 8, z = −3,9) và P5 (x = 10,8, z = +3,9) nguyên chỗ.
   - Nếu dãy nhà phố chính phải dừng sớm hơn x = −4, trả `endInfo.houseX0N/houseX0S`.
5. **`endInfo.casSpot = [x, z]`** cho s24 / s24c:
   - chân tường nhà kho (≤ 0,5 m tới tường), **cách L11 ≤ 5 m** để mặt Cas ấm lên vì L11 (kịch bản 0:57 "his face warm in the new amber");
   - khớp với bộ tường cảnh 4 của W2 (L11 cách tường 4,2 m).
   - Ở vị trí mặc định (−1,2; −2,2), cách L11 9,4 m, Cas **không đọc được** trên probe s24.
6. Giữ `endInfo.warehouseWall` (hoặc tương đương) nếu P cần cho C3 / luật máy.

### 5b. Giai đoạn C — kết quả với `sets_end.js` của W2 (nhánh tích hợp ce40df1)
- **Đo mặt vôi s23** (mặt nạ `limeMask`: mặt nhà kho dùng vật liệu vôi → trắng, mọi thứ khác đen nhưng vẫn che; `--nopaint`, ngưỡng độ sáng > 100/255, 3 khung a/b/c):

| Máy s23 | Mặt vôi a / b / c |
|---|---|
| Giai đoạn A (19,5; 1,6; 2,8) → (4,5; 2,5; −2,9), 28 mm | 29,0 % / 29,4 % / 29,4 % — **vượt** ~20 % |
| Thử B–H (6 phương án: xoay trái, chúc, 32–35 mm, lùi máy) | 10,0–30,0 % |
| **Chốt (I): (24,5; 1,5; 3,6) → (4,5; 2,0; −1,8), 28 mm** | **15,4 % / 15,5 % / 15,4 %** |

  - Nguyên nhân vượt ở máy cũ: dãy nhà bắc nay bắt đầu ở x = 15 (houseX0N), phần phải khung là hông nhà kho (tường chim) gần máy.
  - Lùi máy 5 m lên phố: dãy nhà bắc (x ≥ 15) và dãy nam che bớt hông; phố đọc sâu từ vũng trắng (P4, x = 29) vào góc tối; mặt cuối phố + khe phố rẽ ở giữa khung.
  - Đánh đổi: Ida nhỏ hơn ở đầu shot (khoảng 12 m tới máy). Không đổi hình học của W2.
- **Q-W2-3 — cột điện phố chính bật lúc 1:04:** bộ tường chim đặt ở (3,3; 3,9) hệ tường → **thế giới (13,5; −4,2)** (`endInfo.toWorld`, chỉ tịnh tiến (10,2; −8,1)), xoay π/2 + 0,35.
  - Chiếu vào khung: **s23 lọt khung** (u ≈ 0,74, suốt thân tới bóng đèn); **s24 lọt khung** (tiền cảnh phải, sau khi đổi máy); **s24c: sau máy** (không lọt).
  - Đã thêm vào `sets.js` (`wallPost`, không thuộc `POST_X`, `POST_X` không đổi), dựng khi có cuối phố. Bật theo `switchOn` tại `WALL_POST_T`, do `shots_w1.js` gán = `common.WALL_POST_ON` (64,4 s) lúc nạp (tránh vòng import sets ↔ common). **Mọi shot W1 đều trước 64,4 s → cột tắt.**
  - Sau 64,4 s (shot W2 dùng bộ phố: s35–s42a) cột **hiện bóng đèn sáng + loá**, nhưng **PointLight chỉ bật khi `o.wallPostLight = true`** — tôi không tự đổi ánh sáng các shot góc tối của W2. W2/P quyết có bật ánh không (góc L11 phải tối tới s37w).
  - `st.wallPost` (0…1) ghi đè được nếu shot cần.

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

## 11. Giai đoạn C — render đầy đủ (960×540, 24 fps) sau khi tích hợp W2 A + W3 A1 (nhánh tích hợp ce40df1)
- **Merge:** `claude/cine-lab-m2-cong5-layout-24o5fp` @ce40df1 vào worktree (fast-forward, không xung đột).
- **Đổi mã giai đoạn C (trước khi render):**
  - `S23_CAM` lùi 5 m lên phố → mặt vôi s23 **15,5 %** (máy cũ 29,4 %) — mục 5b;
  - s24 dựng lại máy (Ida trái, Cas phải — theo casSpot W2); s24c máy 3/4 trước Cas, Cas nhìn sang trái;
  - cột điện phố chính cạnh góc nhà kho (Q-W2-3) thêm vào `sets.js` (`wallPost`), tắt trước 64,4 s — mục 5b;
  - chế độ đo `limeMask` (chỉ khi `--dbg '{"limeMask":1}'`), `dbg.s23cam` để thử máy; không ảnh hưởng render thường.
- **Không đổi bảng ORDER** (59,0 s, 1 416 khung) trước và sau khi render.

### 11.1 Hàng đợi (nguồn: `/var/tmp/cine-queue/log.tsv`)
| Nhóm | Shot | Khung | Chờ (s) | Chạy (s) | s/khung (render) | s/khung (cả dựng) |
|---|---|---|---|---|---|---|
| canh1 | s01–s08 | 600 | 633,9 | 827,7 | 1,34 | 1,38 |
| canh2 | s09–s14 | 444 | 1 138,0 | 486,8 | 1,05 | 1,10 |
| canh3 | s15–s24c | 372 | 460,5 | 527,6 | 1,36 | 1,42 |
| lam-lai-s08 | s08 | 48 | 0,0 | 76,9 | 1,50 | 1,59 |
| **Tổng** | | 1 416 (+48 làm lại) | 2 232,4 | 1 919,0 | **1,26** (3 nhóm) | 1,30 |

Đầu ra (không commit): `/var/tmp/cine-out/W1/full/` — `video_s01-…-s08.mp4`, `video_s09-…-s14.mp4`, `video_s15-…-s24c.mp4`, **`video_s08.mp4` (bản làm lại, THAY đoạn s08 trong video nhóm 1)**; `timing_*.json` (4 file), `shots/*.timing.json`, `motion/*.json`, `thumbs/`. Tổng video 74 MB.

### 11.2 Duyệt thumbs a/b/c và làm lại
- Duyệt cả 69 khung a/b/c. **1 lần làm lại: s08** — một ô cửa vàng của dãy nhà xa lơ lửng giữa trời (khối nhà đã chìm vào sương tele, cửa sáng thì chưa). Sửa: `o.farLit = 0` cho s08 (không tắt cửa ở shot khác). Đã render lại qua hàng đợi, hết lỗi.
- Không lỗi khác. Ghi nhận không làm lại: s21 khung đầu mới thấy đỉnh mũ (chủ ý, trèo vào khung); s14 tay giơ còn nhỏ (rủi ro Cổng 6).

### 11.3 Quyết định chủ dự án (world-rules v0.5 @5ec0985)
1. Cuối phố = hông nhà kho chữ L của W2: **đã dùng** (s23, s24, s24c).
2. **Không quầng trắng ở chân trời**, kể cả cảnh toàn: shot W1 không có ánh trời do điện. Đo trên thumbs bản cuối (sRGB trung bình vùng trời sát chân trời / mép trên):
   - s10 (toàn cảnh, sau sóng): luma 23,4 (#0e173a) dải sát chân trời, 22,5 mép trên — không quầng;
   - s12: 42,9 (#292755); s19 khung c: 31,1 (#131e4d); s23: 35,4 (#13235b).
   - `nightSky` (sets.js) chỉ là gradient xanh đen → xanh đậm (#2a3354 ở chân trời), không phụ thuộc điện. Quầng sáng thấy ở cuối phố s19/s12 là loá đèn cột quảng trường ở độ cao đèn (nguồn thấy được), không phải trời.
   - Yêu cầu "quầng trắng chân trời" tôi gửi W2 ở giai đoạn A (mục 5 ý 3) đã rút lại.

### 11.4 Rủi ro giai đoạn C
1. Cận mặt Ida (s05, s22; và s03, s11, s13 cỡ MS) render với mặt A1 đã TRƯỢT kiểm mù lần 4 — P sẽ render lại khi A3 xong.
2. s23 Ida nhỏ ở đầu shot (cách máy khoảng 12 m) — đánh đổi để mặt vôi ≤ 20 %.
3. Cột tường chim: sau 64,4 s chỉ bóng đèn + loá bật; PointLight mặc định tắt (`o.wallPostLight`) — W2/P cần quyết cho s35–s42a.
4. `video_s08.mp4` phải thay đoạn s08 trong video nhóm 1 khi ghép (khung 552–599).

### 11.5 Sửa N1 (rà continuity P, `reports/m2/cong5/continuity.md`)
- Lỗi: s23 không dựng Cas (không phải bị cột che); s24 khung đầu có Cas ở casSpot → Cas "hiện ra" ở chỗ nối 1331 → 1332.
- Sửa: thêm Cas đứng yên ở casSpot trong s23, nhìn về L11/Ida. Trên hình: nhỏ, bên phải cột phố chính, trong bóng Ida — không bị che.
- Render lại riêng s23 qua hàng đợi (`lam-lai-s23-N1`): chờ 0,0 s, chạy 118,3 s, 72 khung. `timing_s23.json`, **`video_s23.mp4` thay đoạn s23 (khung 1260–1331) trong video nhóm 3**.
- Ảnh trước/sau: `reports/m2/cong5/w1/N1_s23_truoc-sau.jpg`. Tổng làm lại giai đoạn C: 2 (s08, s23).

## 12. Giai đoạn A2 (quyết định chủ dự án sau Cổng 5, AUTHORSHIP @2591e4d) — sửa + probe, CHƯA render đầy đủ
Nền: merge nhánh tích hợp @633a217 rồi @0f60b36 (W2 A2). Chỉ probe (960×540, 3 khung/shot).

### 12.1 B1 phía phố (s23, s24, s24c)
- Cột phố chính nay do `sets_end.js` (W2) dựng ở **(17,0; −5,9)**, tầm 8,5 m, trả `endInfo.wallPost = {x, z, range, ry, set, group, light}`. `sets.js` **bỏ cột W1 cũ (13,5; −4,2)**, chỉ gọi `wallPost.set(e)` theo `WALL_POST_T` (= 64,4 s) — mọi shot W1 tắt. `o.wallPostLight === false` tắt ánh.
- `casSpot` = **(14,3; −7,15)** (cách L11 ≈ 7,1 m). Dãy bắc bắt đầu x = 18,5. Nếu `sets_end.js` chưa trả `wallPost` thì `shots_w1.js` dùng dự phòng `B1_FALLBACK.casSpot`.

| Shot | Trước (giai đoạn C) | Sau (A2) | Đo / đọc |
|---|---|---|---|
| s23 | máy (24,5; 1,5; 3,6) → (4,5; 2,0; −1,8); Cas (10,35) sau cột | **máy (27,0; 1,5; 3,8) → (4,5; 2,0; −1,5), 28 mm**; Cas ở chân tường, mép phải | mặt vôi (mặt nạ limeMask): máy cũ trên hình mới **22,5 %** → chốt **18,5 / 18,5 / 18,5 %**; thử K 21,1 %, L 13,0 % (Ida quá nhỏ) |
| s24 | (15,5; 2,3; 2,5) → (8,5; 2,1; −5,0), 35 mm — với casSpot mới Cas ra ngoài/khuất | **(11,2; 2,1; 1,8) → (10,5; 1,8; −5,8), 30 mm** | tính chiếu: Ida u 0,22, Cas u 0,82 (tia tới Cas cắt mặt tiền ở x = 13,8 < 18,5 → không bị che); P5 sau máy. Thử (11; 2,3; 4,5) bị P5 che nửa khung — loại |
| s24c | (cx − 0,03; 1,05; cz + 2,1) cố định | **3/4 trước Cas lệch −35° khỏi hướng nhìn về L11, 2,1 m** (tính theo casSpot) | Cas nhìn sang trái; mặt đọc được, ấm yếu hơn (L11 cách 7,1 m; phơi sáng giữ 4,5) |

Ảnh: `reports/m2/cong5/w1/v2_B1_s23-s24c.jpg` (trái: trước; phải: A2).

### 12.2 (c) Tỷ lệ đá lát theo người
- Chiều cao Ida theo khung xương sheet: chân 0,3 + cẳng 1,4 + đùi 1,45 + thân 2,0 + cổ 0,3 + đầu 1,0 = 6,45 H × 0,258 m ≈ **1,66 m** (không tính mũ) → 1/11–1/16 = 0,104–0,151 m.
- `sets.js`: `COBBLE_M = END.cobbleTile` (**2,4 m**, cùng W2 để khớp s38) — viên ngang 0,088–0,136 m (TB 0,112 m ≈ 1/14,8), hàng 0,084 m; `FLAG_M = 3,0 m` — đá phiến vỉa hè 0,34–0,71 m (trước 0,45–0,95 m, đọc "cuội to" cạnh người ở s14). Texture khoá (cobbleTex, flagTex) **không đổi**, chỉ đổi cách trải.
- **Đo trên probe s07** (khung giữa; tự tương quan dải mặt đường ngay trước chân Ida, 111,5 px/m): **trước 16 px ≈ 0,144 m (1/11,6) → sau 14 px ≈ 0,126 m (1/13,2)**. Độ phân giải 1 px ≈ 9 mm nên số đo lệch lên so với TB thiết kế 0,112 m.
- s06, s09w (insert 100–105 mm, lấy nét 0,32–0,42 m): viên đá đúng cỡ nhưng quá SẮC — ngoài đời nền cách 1–2 m nhoè với vòng nhoè ≈ 1/3 khung. Previs không có DOF → thêm `o.groundSoft` (lấy mẫu kết cấu nền 24 px/lần lặp khi dựng, KHÔNG sửa texture khoá) cho riêng s06, s09w = đưa nền ra khỏi nét. Thử đổi góc POV s09w (ngang hơn) thì tay áo che mặt đồng hồ → giữ góc cũ. Cổng 7 thay bằng DOF thật. P/chủ dự án có thể bác cách này — khi đó cần DOF ở `page.js`/pipeline (P).
- Ảnh: `reports/m2/cong5/w1/v2_c_da-lat.jpg` (s14 c, s07 b, s09w b, s06 c).

### 12.3 Đèn lồng (việc nhỏ 1, chủ dự án duyệt)
- Tắt ở s02, s03, s04 đến 1,2 s; bắt lửa ở s04 1,2 s (11,7 s phim); cháy từ đó. Hàm `lanternLit()` (ẩn ngọn lửa, kính tối) — nhịp tay mồi là việc Cổng 6 (ghi ở `shots_w1.json` s03/s04). Ảnh: `v2_den-long_s02-s04.jpg`.
- Máy mới s02, s15: chủ dự án **đã duyệt**.

### 12.4 Shot W1 cần render lại (giai đoạn C2)
**20 shot**: s02, s03, s04, s05, s06, s07, s08, s09w, s10e, s11, s12, s13, s14, s15, s19, s21, s22, s23, s24, s24c.
- Đổi do A2 của W1: s02–s04 (đèn lồng), s06, s09w (nền nhoè), mọi shot thấy mặt phố (đá lát), s23–s24c (B1).
- Không cần render lại: s01, s10 (bộ thành phố khoá), s09 (không thấy mặt phố, không Ida).
- Mọi shot có Ida còn phải render lại vì mặt + tóc trắng của W3 — P nhắn giai đoạn C2.

### 12.5 Rủi ro A2
1. s24, s24c: Cas cách L11 7,1 m → mặt ấm yếu; s24 Cas nhỏ (≈ 90 px cao ở 960×540, đo trên probe). Chỉ nguồn thật (L11, P4 xa). Nếu cần rõ hơn: Cổng 7 thêm ánh cửa sổ ấm có thật ở nhà đầu dãy bắc (đề xuất, chưa làm).
2. s23 mặt vôi 18,5 % (ngưỡng ~20 %): ngoài dải ±5 % (19–21 %) nhưng gần; nếu W2 đổi thêm hông kho phải đo lại.
3. `groundSoft` là giả DOF cục bộ — có thể bị coi là đổi hình texture; phương án thay: DOF thật (P).
4. Cột sân trước: `sets.js` gọi `set(e)` theo WALL_POST_T; shot W2 cảnh 5 gọi thêm `set(1)` sau đó (cùng kết quả sau 64,4 s). `buildStreetSet` trả `wallPostCtl` (không trả `wallPost`) vì `shots_w2.js` dòng 179 coi `st.wallPost` là cột W1 cũ và ẩn nó — đã kiểm `--meta-only` s35, s37w, s41, s45c chạy hết khung, không lỗi.

## 13. Giai đoạn C2 — render đầy đủ 20 shot (mặt A-α W3, sheet v1.4, tóc bạc #e2dfda + shader)
Nền: merge nhánh tích hợp @b378416. P duyệt nền nhoè s06/s09w cho layout (lấy nét thật ở Cổng 7).

### 13.1 Phơi sáng cận mặt s05 (mặt mới)
Đo trên probe khung a/b/c (960×540): "mặt cháy" = tỷ lệ điểm ảnh có kênh ≥ 250 trong khung mặt (x 380–540, y 110–230); nền = độ sáng TB tường trái (x 0–160, y 60–250); tóc = màu TB vùng tóc/búi.

| Cách | Phơi sáng | Mặt cháy | Nền (luma) | Tóc (sRGB, bão hoà) |
|---|---|---|---|---|
| cũ (0,42) | 0,42 | 23,8–24,5 % | 104–106 | #582f1d, 0,66 (đọc nâu/vàng) |
| × 0,4 (W3 đo) | 0,168 | 2,4 % | 55–56 | #2c150e, 0,67 (tối, vẫn cam) |
| facelight 'gas' + `fl.exposure()` | tự tính | 0,0 % | 47–48 | #573c34, 0,39–0,40 |
| **facelight 'gas' + `fl.exposure()` × 1,6 (CHỐT)** | tự tính ×1,6 (khoá ở khung đầu) | **0,5 %** | **69** | **#735449, 0,36 — đọc bạc** |

- Nguồn: chỉ nguồn có thật (dội ấm vôi/đá + viền trời đêm, preset W3 'gas'; nguồn chính L4). Nền không tắt hẳn (luma 69 so với 55 của × 0,4); tóc hết đọc "vàng" (bão hoà 0,66 → 0,36).
- s22 giữ nguyên (theo P).

### 13.2 Render qua hàng đợi (nguồn: `/var/tmp/cine-queue/log.tsv`; 960×540, 24 fps, vào `/var/tmp/cine-out/W1/full/`)
| Nhóm | Shot | Khung | Chờ (s) | Chạy (s) | s/khung render | s/khung cả dựng | timing |
|---|---|---|---|---|---|---|---|
| c2-canh1 | s02–s08 | 504 | 0,0 | 713,8 | 1,37 | 1,42 | `timing_s02-s03-s04-s05-s06-s07-s08.json` |
| c2-canh2 | s09w, s10e, s11–s15 | 336 | 1 061,1 | 426,7 | 1,21 | 1,27 | `timing_s09w-s10e-s11-s12-s13-s14-s15.json` |
| c2-canh3 | s19, s21–s24c | 336 | 0,0 | 491,4 | 1,40 | 1,46 | `timing_s19-s21-s22-s23-s24-s24c.json` |
| **Tổng** | 20 shot | 1 176 | 1 061,1 | 1 631,9 | 1,33 | 1,39 | |

- Lượt c2-canh3 đầu (xếp hàng 06:30:35) bị huỷ khi phiên W1 bị hệ thống dừng lúc đang chờ hàng (kiểm tra an toàn máy chủ không trả kết quả); không có dòng log, không khung nào render. Chạy lại 07:01:44, không phải chờ.
- Video: `video_s02-…-s08.mp4`, `video_s09w-…-s15.mp4`, `video_s19-…-s24c.mp4` (thay các đoạn tương ứng của bản giai đoạn C; s01, s09, s10 giữ bản C).

### 13.3 Duyệt thumbs a/b/c (60 khung) và làm lại
- **0 lần làm lại.** Kiểm: s02–s04 đèn lồng tắt → s04 bắt lửa; s05 tóc bạc, mặt không cháy; s06, s09w nền nhoè (hết "chấm bi"); s14 không bóng dài; s15 một thang; s22 mặt mới không cháy (giữ phơi sáng); s23 Cas ở chân tường, cột sân trước tắt; s24 Ida trái / Cas phải; s24c Cas nhìn trái.
- Ghi nhận (không làm lại): s11 phơi sáng 2,2 dưới L7 làm mũ + mặt rất sáng (đã đề xuất Cổng 7 hạ 1,5–1,7 ở mục 7); s24 Cas nhỏ; s24c mặt Cas ấm yếu.

### 13.4 Rủi ro C2
1. Mặt A-α chỉ kiểm bằng hình ở s05, s22 (cận); các shot rộng hơn chưa đo cháy mặt riêng.
2. s11 (không trong phạm vi sửa C2) còn sáng quá dưới đèn khí gần.
3. Bản cuối gồm nhiều video nhóm của C và C2 — P ghép theo `timing_*.json` mới nhất cho mỗi shot.

## 14. Vòng v3 chốt layout (quyết định chủ dự án @e850c0f)
Nền: merge nhánh tích hợp @e850c0f.

### 14.1 (a) Rà trạng thái ẩn — render THẲNG (trang mới, chỉ khung F) so với NỐI TIẾP (trang mới, F−12 rồi F), F = khung giữa shot
Công cụ: so điểm ảnh RGB thô 960×540 của `renderFrame` + `finalize` (bắt cả phơi sáng, đạo cụ — mặt nạ C3 không có đèn lồng); thêm kiểm mặt nạ C3 `export_c3.js --audit-dir … --scale 1` cho 19 shot có Ida.

| Shot | Lệch (px > 2/255; max) trước sửa | Nguyên nhân | Sửa | Sau sửa |
|---|---|---|---|---|
| s05 | 25 919 px (5,0 %); max 3 | `fl.exposure()` khoá ở KHUNG ĐẦU ĐƯỢC RENDER (bắt đầu giữa shot → giá trị khác) | tính tường minh trạng thái t = 0 (f0) của shot rồi khoá — hàm thuần | 0 |
| s02 | 11 px; max 7 | `util.makeChar().place` gọi `setPose` trước khi đặt hướng gốc → đèn lồng thắt lưng xoay "theo trọng lực" bằng hướng của LẦN ĐẶT TRƯỚC (render thẳng: hướng 0) | `mkChar` cục bộ trong `shots_w1.js`: đặt vị trí + hướng gốc TRƯỚC rồi `place` (22 lời gọi) | 0 |
| s07 | 221 px (0,04 %); max 15 | như s02 | như s02 | 0 |
| s08 | 477 px (0,09 %); max 202 | như s02 | như s02 | 0 (max 1) |
| s23 | 142 px (0,03 %); max 192 | như s02 | như s02 | 0 |
| 18 shot còn lại (s01, s03, s04, s06, s09, s09w, s10e, s10, s11–s15, s19, s21, s22, s24, s24c) | 0 | — | — | 0 |

- **Mặt nạ C3** (thẳng vs nối tiếp, 19 shot có Ida, sau sửa): 0 px lệch ở mọi bộ phận, `views.json` giống hệt (s09w chỉ có đầu).
- **Ảnh hưởng tới bản render đầy đủ đã có** (render luôn bắt đầu từ f0 và nối tiếp): kiểm khung ĐẦU shot, mã cũ vs mới: s02 28 px (max 47), s07 4 px (max 6), s08 307 px (max 118), s23 257 px (max 143); s06, s09w, s15 0 px. s05: mã cũ render từ f0 → F **trùng từng byte** với mã mới (phơi sáng khoá đúng giá trị f0) → **không render lại s05**.
- Render lại: **s02, s07, s08, s23** (khung đầu sai) và **s15** (Ida quay 90° lúc 0,8–1,4 s: đèn lồng trễ một khung ở mã cũ).
- Đề xuất P: sửa gốc trong `util.js` (`ch.place`: đặt `root.position/rotation` trước `setPose`) — lỗi cùng loại có thể ở shot W2 có Ida quay ≠ 0 (s35 là ví dụ đã thấy).

### 14.2 (b) Đồng hồ nhịp 1–2: đọc trên hình từng khung
Móc chỉ đọc `clockAudit()` trong `shots_w1.js` đọc góc kim của vật thể đồng hồ đang render (đồng hồ bỏ túi `watch`, đồng hồ quảng trường) sau `stepFrame(f)` ở mọi khung; không đổi hình.

| Shot | Khung | Giờ đầu → cuối | Kim phút (°) | Kim giờ (°) | Lần lùi |
|---|---|---|---|---|---|
| s06 (bỏ túi) | 384–455 (72) | 7:31:00 → 7:31:03 | 186,000 → 186,296 | 225,5 | 0 |
| s09 (quảng trường) | 600–671 (72) | 8:00:00 → 8:00:02 | 0,000 → 0,196 | 240,0 | 0 |
| s09w (bỏ túi) | 672–719 (48) | 7:53:00 → 7:53:02 | 318,000 → 318,196 | 236,5 | 0 |

- Kim chỉ tiến ở cả ba shot; thumbs a/b/c đọc 7:31 · 8:00 · 7:53. Kim giờ không nhích trong 2–3 s (nhích 0,5°/phút → < 0,03°, không thấy được).
- Ghi vào `continuity/canh-1.md` (s06) và `canh-2.md` (s09, s09w).

## 15. Cổng 6 — DIỄN HOẠT W1 v1 (30/09/2026; AUTHORSHIP "Cổng 6 — diễn hoạt", MỞ W1)
Nhánh `cong6-w1-v1` (từ main `00a4ead`). Báo cáo đầy đủ + số đo: `reports/m2/cong6/w1/BAO-CAO-W1-V1.md`.
- **Không đổi:** id, thứ tự, thời lượng shot (`order_w1.js`), máy các shot trừ s22, mốc sự kiện, `sets.js`, `sets_end.js`, mã dùng chung. Tổng phim 140,5 s.
- **Mã (chỉ `shots_w1.js`):** bản sao trong gói các kỹ thuật W2 — `settle` (đứng tự nhiên), `gripAt`/`gripK` (IK tay MPFB tới một điểm), mặt 16 kênh + 6 viseme (`faceRig`, `lipKeys`, `mouthAt`, `richLip`, `blinkAt`); thêm `breathe` (thở trên thang), `lampGrips` (van = ống khí dưới van, thanh móc thang, thân cột), `topHands`, `climbHands`, `railG`, `shoulderLadderG`, `lanternDoorG`, `watchInPalm`, `casLeanSpot/casLeanPose/casWallHand`, `hideWallPost` (B2). Đo tiếp xúc chỉ khi `--dbg '{"meas":1}'` (bọc `S1`, không đổi hình).
- **s22:** máy lệch **45°** khỏi hướng mặt (đo 42,2–46,5°; Cổng 5: 7,0–11,3°), MCU 85 mm, 1,2 m, tĩnh — bảng mục 2 dòng s22 nay là "faceCam lệch +45° (phía phố)".
- **s23 (B2):** cột điện tường chim ẩn khỏi khung; PointLight dời (17,4; 6,2; 4,1). P5 (10,8; +3,9) giữ.
- **Cas s23/s24/s24c:** dựa lưng tường chim ở (14,3; −7,90) (Cổng 5: casSpot (14,3; −7,15)).
- **Ảnh hưởng tới W2:** không (lệch 0 px 30 shot W2 + s01, s09, s10e, s10). Nối s24c → s25: Cas đổi chỗ 0,75 m qua cắt (xem continuity canh-3).
