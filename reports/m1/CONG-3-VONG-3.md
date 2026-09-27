# CỔNG 3 — THIẾT KẾ · vòng 3 (chốt thiết kế) · "Last Round"

Phiên P, 27/09/2026. Nhánh `claude/cine-lab-m1-cong3-v3`. `bash scripts/env/verify.sh`: **10 PASS, 0 FAIL**. `checks/lock.py --verify`: **KHỚP** `144b3cff…0294`. Không sửa `checks/`, không đọc mã trong `checks/` (chỉ đọc `RUN.md`, `RULES.md`).
Mọi số dưới đây là **đo thật**. Thời gian đo **tuần tự trên máy rỗi**, 1920×1080. Đây là **đề xuất của Claude, chưa duyệt**.

## 0. Tóm tắt
- **Cửa thử C′ ĐẠT** cả 4 tiêu chí: không lộ đường nối, mặt không trượt, biểu cảm đọc được ở 0°/4°/15°, 4,70 s/khung (sau 7A). Không lùi về A.
- **L1, L2 đã sửa** bằng DOF hậu kỳ theo độ sâu, nhân đĩa tròn 64 mẫu. Crop 200% trước/sau nằm trong `reports/m1/cong3-v3/L1-L2/`.
- **L3 đã sửa** nhờ C′: bỏ rãnh khoé miệng và nếp nhăn khắc vào hình học, thay bằng nét vẽ trên texture; da mờ (Lambert).
- **L4 / 5B ĐẠT ngay lần 1**: subagent mù trả lời bóng là **"a bird spreading its wings"**.
- **Cảnh 5 trung cảnh**: người chiếm 0,80–0,94 chiều cao khung; đầu tách khỏi nền bóng nhờ viền từ đèn lồng phía sau.
- **7A: mọi khung ≤ 5 s** (2,31–4,70 s; hai clip đi bộ có trung vị 3,59 và 3,77 s).
- **C2 = 85% (chưa đạt 90%)**, nằm trong vùng ±5% quanh ngưỡng. Chấm chặt: 70%. Chim bóng đã đọc đúng; vẫn trượt "hơ tay trên thang".
- **Luật máy: 9/9 file TRƯỢT.** Cụ thể:
  - Lỗi thật của mình: C3 (bộ xuất mặt nạ lỗi alpha; tỷ lệ render lệch model sheet), G3b ở 4 khung tĩnh (grain gần như đứng yên trong file mã hoá), H1b ở 2 clip đi bộ (track bàn tay).
  - Lỗi luật, đã khiếu nại: J1/J1b ("không có luồng âm").
- 7 khung phong cách phủ color script, cộng 1 clip đi bộ cho mỗi nhân vật.

## 1. Kết quả theo bước
| Bước | Việc | Kết quả đo | Đạt? |
|---|---|---|---|
| 1 | Cửa thử C′: mặt vẽ tay trên texture chiếu trước, phủ đầu 3D (`v2/char3d/facepaint.js`) | Xem mục 2 | **ĐẠT** |
| 2 | 2A, 3B, 4A cho Ida và Cas; model sheet, `bible/characters.md` | Tay Ida 1,15×, Cas 1,30×; búi 1,3×; váy, khăn, tóc gáy Cas; **không nơ mũ**; giữ mũ len Cas. Ghi vào `model-sheet/*.json` (trường `scale`, `bun_scale`, `scarf`, `skirt`, `hair`, `face`) và bảng tỷ lệ trong `characters.md`. `characters.md` v1.0 **KHOÁ**, SHA-256 `0db8b4cd…af658f5` | Xong |
| 3 | L1, L2 | DOF hậu kỳ `shared/dof.js`: 0,21–0,24 s/khung. Cửa sổ nhoè thành khối bo tròn, mịn, không còn ô. Ngón tay gần máy nhoè liền, không còn 8 lớp | Xong |
| 4 | Chim bóng 5B + kiểm mù | Lần 1: **"a bird spreading its wings"** (mục 4) | **ĐẠT** (1/3 lần) |
| 5 | Cảnh 5 trung cảnh | Cao người/khung: **Cas 0,80, Ida 0,935** (≥ 1/3). Đầu Cas trên nền bóng: sáng hơn nền **1,93×** (trung vị), viền p90 **5,51×**. Đầu Ida trên vách sáng: tối hơn nền **2,6:1**, viền má sáng. Nguồn: đèn lồng dưới đất sau lưng (có trong truyện) + dội vách bên | **ĐẠT** |
| 6 | 7A tối ưu ≤ 5 s | Bảng mục 3 | **ĐẠT** |
| 7 | C2 kiểm mù | **8,5/10 = 85%**; chặt 70% (mục 5) | **CHƯA ĐẠT** (ngưỡng 90%) |
| 8 | 5–8 khung phong cách + clip đi bộ | 7 khung + 2 clip (mục 6) | Xong |
| 9 | `checks/run.py --profile shot` + `audit.py issue` | 9/9 **TRƯỢT** (mục 7) | **TRƯỢT** |

## 2. Cửa thử C′ (bước 1)
Ảnh: `reports/m1/cong3-v3/cprime/t0|t4|t15/a_close_ida.png`, ghép 200% `cprime/face_3angles_200.png`.

| Tiêu chí | Đo / quan sát | Kết quả |
|---|---|---|
| Không lộ đường nối | Nền texture trắng (= không đổi màu da), nét tan về trắng ở rìa; nửa sau đầu gán về một điểm trắng. Xem 200% ở cả 3 góc: không thấy mép | Đạt |
| Mặt không trượt khi quay | Texture gắn vào UV của **chính lưới đầu**, nên trượt bằng 0 theo cấu tạo. Ở 0°, 4°, 15°, nét mi luôn nằm đúng trên nhãn cầu, khe môi đúng trên môi | Đạt |
| Biểu cảm đọc được ở 3 góc | Mi trên đậm, mí nặng, khoé miệng trễ, nếp mũi–má đọc được ở cả 3 góc. *P tự chấm, chưa có người chấm độc lập* | Đạt (tự chấm) |
| ≤ 5 s/khung | C′ không tốn thêm: 9,70 s so với 9,92 s của vòng 2, cùng thiết lập cũ. Sau 7A: **4,70 s** | Đạt |

Sửa L3 kèm theo: bỏ rãnh khoé miệng (khắc sâu 0,003 H ở Ida, 0,007 H ở Cas) và toàn bộ nếp nhăn khắc vào lưới; chuyển thành nét vẽ. Chất da vẫn là Lambert, không bóng. Vệt sẫm ở má là bóng thật của khối gò má (vòng 2 cũng có), không do texture.

## 3. Thời gian render (bước 6, thiết lập sản xuất v3)
Thiết lập v3: **3 mẫu** (vòng 2: 8), bóng **PCF** (vòng 2: PCFSoft), bản đồ bóng 1024 (cận mặt vòng 2: 2048), **DOF hậu kỳ** thay rung khẩu độ.
Căn cứ: đo cận mặt thì một mẫu tốn ≈ 0,9–0,98 s. Trong đó tra bóng mỗi điểm ảnh ≈ 0,4 s, còn vẽ bản đồ bóng chỉ ≈ 0,1 s. Khi DOF không còn cần nhiều mẫu, 3 mẫu cho ảnh gần trùng 8 mẫu: sai khác trung bình **0,63 mã 8 bit**, p99 7 mã ở vùng nhoè. Crop so sánh: `L1-L2/7A_8mau-trai_3mau-phai_200pct.png`.

| Khung | s/khung (render + lớp vẽ + DOF + pass cuối) | Vòng 2 |
|---|---|---|
| s1 mở đầu | 3,07 | — |
| a cận mặt Ida | **4,70** (một lần đo khác cùng thiết lập: 4,84, **trong ±5% quanh 5 s**) | 9,92 |
| b chim bóng | 2,74 | 5,13 |
| c cảnh 5 rộng | 2,61 | 4,12 |
| c cảnh 5 trung | 3,28 | — |
| d cảnh 6 ngõ | 2,98 | — |
| e kết | 2,31 | — |
| walk Ida (48 khung) | trung vị 3,77, lớn nhất 4,02 | 7,36 |
| walk Cas (48 khung) | trung vị 3,59, lớn nhất 3,96 | — |

Chi phí từng chặng ở khung a: tích luỹ 3 mẫu 2,76 s; lớp vẽ 1,27 s; DOF 0,21 s; phần còn lại là pass cuối và readPixels.

## 4. Chim bóng 5B: kiểm mù (bước 4), nguyên văn
Crop `reports/m1/cong3-v3/bird/lan1_crop_bong.png`, lấy từ `design/cong3/v2/out/b_cas_bird.png`. Subagent **mới, không ngữ cảnh**, chỉ được mở một file tên trung tính. Câu hỏi: "bóng này là hình gì?"

> Cái em thấy đầu tiên là bóng một con chim đang dang rộng hai cánh, giống đại bàng hay phượng hoàng, với phần đầu nhô lên ở giữa. Phần thân dưới dài và cong, khá giống bóng tay (cổ tay, cánh tay) làm trò bóng hình. Góc dưới bên phải có thêm một khối tròn tối.

Tư thế: góc khớp **giải ngược bằng số** (IK, theo đúng quy ước Euler của `cast.js`) từ hướng mong muốn:
- cánh tay trên vươn về phía tường;
- cẳng tay dựng, bắt chéo ở cổ tay;
- ngón xoè ngang (cánh); hai ngón cái chập giữa (đầu).

Đèn khí dời từ x −1,0 sang −2,2 m (vẫn cao 3,3 m) để bóng chim tách khỏi bóng đầu; máy quay lùi để thấy trọn Cas và chim. Luật thế giới giữ nguyên: đèn khí, bóng rìa tương đối sắc, hơi thấp trên tường.

## 5. C2 kiểm mù (bước 7), nguyên văn
Câu lệnh giống hệt vòng 2. 10 ảnh đánh số, không nhãn, thứ tự trộn cố định; khoá ở `design/cong3/v2/out/c2/blind-key.json`, bảng `design/cong3/v2/out/C2-silhouettes-v3.png`.
```
01 | adult, woman (long skirt, hat, hair in bun), likely middle-aged or older | standing on a ladder, reaching up to the street lamp to light or tend it | high
02 | adult, woman (long dress, hat, bun), older-looking | walking while carrying a lantern held out in front | high
03 | child (small, hair bun or topknot, trousers), gender unclear | bending over to look closely at something cupped in their hands, with a lantern on the ground by their feet | medium
04 | child (topknot/bun, trousers), gender unclear | holding an upright ladder and looking up along it | medium
05 | adult, woman (hat, bun, long skirt) | kneeling or crouching down with one hand reaching forward, a bag or box beside her | low
06 | child (topknot/bun), gender unclear | squatting next to a lantern with both hands reaching out toward it, maybe to pick it up or warm their hands | medium
07 | child (small figure seen from the front, standing), gender unclear | raising both hands above their head to make a hand-shadow puppet (bird-like) that throws a large shadow on the wall | low
08 | adult, woman (hat, bun, long skirt) | walking with a ladder carried over her shoulder | high
09 | adult, woman (hat, bun, long skirt), older-looking | standing and leaning back to look up, one hand raised (waving or gesturing upward) | medium
10 | adult, woman (hat, bun, long skirt) | using a long pole to reach up and light or adjust a street lamp | high
```

Chấm theo khoá (bảng chi tiết: `design/cong3/v2/out/c2/C2-KIEM-MU-v3.md`):
- **Đúng hoàn toàn (7/10):** 02, 04, 05, 07, 08, 09, 10. Riêng 07 (chim bóng) vòng 2 bị đọc sai.
- **½ điểm (3/10):**
  - 01 hơ tay trên thang: đọc là "thắp/chăm đèn", như vòng 2;
  - 03 Cas nhìn đèn lồng: đọc là "nhìn vật trong tay";
  - 06 Cas hơ tay: đọc là "nhặt HOẶC hơ tay".
- **Tổng 85%** (vòng 2: 85%), **thấp hơn ngưỡng 90% 5 điểm**, nằm trong vùng ±5% quanh ngưỡng. Chấm chặt: 70%.
- Ida: 5/5 "adult woman". Cas: 4/4 "child", nhưng vẫn "topknot/bun" và giới tính không rõ, do quả bông của mũ len (giữ theo 4A).
- Ô 05: đèn lồng bị đọc thành "túi/hộp". Em vẫn tính 1 điểm vì hành động quỳ đúng.

## 6. Khung phong cách và clip (bước 8)
| Nhịp color script | Khung | File |
|---|---|---|
| Mở đầu (cảnh 1): tím chạng vạng + hổ phách | toàn cảnh thành phố, Ida rất nhỏ | `design/cong3/v2/out/s1_opening.png` (+ `.mp4` 1 s) |
| Giữa (cảnh 1/3): hơ tay ở đèn | cận mặt Ida (C′, DOF mới) | `design/cong3/v2/out/a_close_ida.png` |
| Giữa (cảnh 4): bức tường | Cas làm chim bóng 5B | `design/cong3/v2/out/b_cas_bird.png` |
| Cảnh 5 rộng: hốc tối ấm giữa phố trắng | giữ khung vòng 2 (6B) | `design/cong3/v2/out/c_s5_wide.png` |
| Cảnh 5 trung (6B) | qua vai, hai người và hai bóng | `design/cong3/v2/out/c_s5_medium.png` |
| Cảnh 6 ngõ khuất | ngõ tối, vệt hổ phách từ cửa sổ nhà Cas, miệng ngõ trắng | `design/cong3/v2/out/d_s6_alley.png` |
| Kết: phố trắng, một ô vàng | toàn cảnh phố điện, ô cửa nhà Cas, Ida ở miệng ngõ | `design/cong3/v2/out/e_ending.png` |
| Clip đi bộ Ida (48 khung) | vác thang qua 2 cột đèn | `design/cong3/v2/out/walk.mp4`, `walk_000|024|047.png` |
| Clip đi bộ Cas (48 khung) | nhịp trẻ con: chu kỳ 0,95 s, bước 0,42 m, vung hai tay | `design/cong3/v2/out/walk_cas.mp4`, `walk_cas_000|024|047.png` |

Bối cảnh cảnh 6 (`v2/s6.js`) là dựng mới:
- đèn lồng trên bậu cửa sổ nhà Cas chiếu qua khẩu độ ô cửa (SpotLight có bóng);
- ánh điện chỉ lọt vào miệng ngõ, giảm theo độ sâu;
- nguồn cao nên bóng Ida ngắn, nhạt, đúng luật thế giới 3.4–3.5;
- ô vàng ở khung kết chính là phòng góc đó.

Khung mở đầu dùng lại bối cảnh hướng C, chỉ thay nhân vật.

## 7. Luật máy (bước 9), nguyên văn kết luận
Kiểm toán C3: `audit.py issue` phát cho cả 9 file (hạt giống từ hệ điều hành; khung được chọn ghi trong `X.audit/request.json`). Mặt nạ được render lại đúng các khung đó bằng đúng lệnh, và `render.log` được ghi.

Các file đi kèm xuất từ chính trang render (`shared/export_sidecars.js`):
- mặt nạ bộ phận **7680×4320 (4×)**;
- `motion.json` (góc khớp bake + track màn hình);
- `text` rỗng, `script` rỗng, stem im lặng;
- `assets.json`, và `assets/LIBRARY.json` rỗng (phim chưa dùng tài sản ngoài: mọi kết cấu sinh bằng mã).

**Lần 1** (báo cáo giữ ở `design/cong3/v2/out/check-lan1/`): 9/9 **TRƯỢT**.
- C3: **LỖI ĐO "KeyError: 'torso'"** (lược đồ sheet), 9/9 file.
- O3: 59 file media của vòng 2 nằm ngoài `out/`.
- H1b: track cổ chân ra ngoài khung hoặc nằm trên vùng trơn.

Sửa sau lần 1, **chỉ ở file đi kèm và cách xếp thư mục, không đụng phim**:
- dời đầu ra vòng 2 vào `v2/out/v2/` và `v2/out/v2-dev/`;
- thêm khoá tương thích C3 vào sheet (cùng giá trị);
- đặt track trên vùng có chi tiết theo RUN.md 3.4 (đầu, lòng bàn tay), bỏ track toàn `null`;
- với 2 clip đi bộ, lần 3 thêm `null` khi bị che.

**Kết quả cuối** (khung tĩnh: lần 2; clip đi bộ: lần 3; báo cáo ở `design/cong3/v2/out/check/`):

| File | Kết luận | N1 | N2 | P0 | P1 | G4 | G3 | G3b | J1 | J1b | H1 | H1b | C3 | O3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s1_opening | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | TRƯỢT | TRƯỢT | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| a_close_ida | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | TRƯỢT | TRƯỢT | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| b_cas_bird | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | TRƯỢT (0,624) | TRƯỢT | TRƯỢT | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| c_s5_wide | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | TRƯỢT (0,669) | TRƯỢT | TRƯỢT | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| c_s5_medium | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | TRƯỢT (0,536) | TRƯỢT | TRƯỢT | ĐẠT | ĐẠT (95,7%) | TRƯỢT | ĐẠT |
| d_s6_alley | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | TRƯỢT | TRƯỢT | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| e_ending | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | TRƯỢT (0,687) | TRƯỢT | TRƯỢT | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| walk | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (0,208) | TRƯỢT | TRƯỢT | ĐẠT | TRƯỢT (46,7%) | TRƯỢT | ĐẠT |
| walk_cas | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (0,222) | TRƯỢT | TRƯỢT | ĐẠT | TRƯỢT (74,5%) | TRƯỢT | ĐẠT |

Máy báo **không có chỉ số nào nằm trong ±5% quanh ngưỡng**. Các chỉ số sát ngưỡng P tự nêu:
- G3b c_s5_medium 0,536 (ngưỡng 0,5; lệch +7%);
- H1b c_s5_medium 95,7% (ngưỡng 90%; lệch +6%);
- C2 85% (ngưỡng 90%);
- thời gian khung a: 4,70–4,84 s (ngưỡng 5 s).

Nguyên nhân từng luật trượt:
- **C3 (lỗi của P, 9/9):**
  1. Bộ xuất ghi PNG RGBA với **alpha 255 toàn ảnh**, nên máy đọc "xám hoặc alpha ≥ 128" và coi cả khung là bộ phận (đầu "cao 1920 px").
  2. `page.js` bị sửa **sau** khi ghi `render.log`, nên SHA file cảnh không khớp.

  Mặt nạ đã khoá theo yêu cầu kiểm toán, nên P **không sửa và không phát lại**; bộ xuất đã sửa cho lần nộp sau. Chẩn đoán trên bản sao ngoài hồ sơ, với mặt nạ đúng định dạng, cho thấy **tỷ lệ render lệch model sheet thật**:
  - Ida: thân +8–10%, cánh tay trên +24%;
  - Cas: thân +13–15%, cánh tay trên −25%, cẳng tay +14%, đùi +12%;
  - đầu cao 43–46 px, mặt nạ 4× là đúng quy định.

  Đây là quyết định B dưới đây.
- **G3b (4 khung tĩnh):** tương quan grain giữa hai khung kề vượt 0,5. P tự đo lại trên file giao:
  - sau khi bỏ thành phần tĩnh theo thời gian, tương quan vẫn là 0,43–0,44 ở `c_s5_wide`, `e_ending`, tức grain gần như **đứng yên thật trong file mã hoá** (có khả năng x264 chép khối trong shot đứng máy);
  - ở `b`, `c_s5_medium`, phần lớn do kết cấu tĩnh (0,145–0,149 sau khi bỏ).

  Luật bắt đúng. **Không khiếu nại.** Sửa ở khâu mã hoá shot tĩnh; P tự làm được, không cần quyết định sáng tạo.
- **H1b (2 clip đi bộ):** track đầu khớp 97,9–100%; track lòng bàn tay phía gần máy khớp 46,7% (Ida) và 74,5% (Cas). Bàn tay nhỏ (khoảng 7 px ở độ phân giải đo) và nhoè chuyển động khoảng 15 px/khung, nhưng **chưa chứng minh** đó là nguyên nhân. P **dừng**, không đổi track thêm để khỏi thành lách luật.
- **J1, J1b (9/9):** "Không có luồng âm", trong khi M3 cùng điều kiện cho "—". **Đã khiếu nại** trong `checks-appeal.md`. P không chèn luồng âm im lặng.

Khiếu nại mới trong `checks-appeal.md` (chờ chủ dự án phán quyết): J1/J1b không nhất quán với M3; C3 thiếu mô tả lược đồ sheet và báo LỖI ĐO thay vì thông báo định dạng.

## 8. Việc khác
- AUTHORSHIP: đã ghi nguyên văn quyết định Cổng 3 vòng 2 (C′, 2A, 3B, 4A, 5B, 6B, 7A, duyệt characters.md, L1–L4).
- Đã xoá 6 file `.rgb` nháp: `design/cong3/dir-A|dir-B|dir-C/out/{s1_opening,s5_shadows}.rgb`, cùng thư mục tạm `/tmp/claude-0/v2raw`; `.rgb` của vòng này cũng đã xoá sau khi mã hoá.
- Hạ tầng mới:
  - `shared/dof.js` (DOF hậu kỳ);
  - `shared/export_sidecars.js` (file đi kèm cho checks);
  - `v2/s6.js` (cảnh 6 và kết), `v2/s1.js` (mở đầu với nhân vật tiêm);
  - `v2/char3d/facepaint.js` (C′);
  - `walkPose` cho trẻ con (`shared/anim.js`);
  - `sheet_page.js`: khung silhouette chim bao trọn bóng.
- Lỗi của P trong vòng này, đã sửa và ghi lại để tránh lặp:
  1. Hai lần chú thích `//` nuốt mã ở cuối dòng (`scene.add`, `n += on`). Từ nay chạy `node --check` sau mỗi lần sửa.
  2. Mặt nạ RGBA sai alpha.
  3. Sửa file cảnh sau khi ghi `render.log`.
- Mọi vòng chờ đều chờ theo PID (`kill -0`), có hạn giờ.

## 9. Quyết định cho chủ dự án
**A. "Chốt thiết kế và sang Cổng 4 (animatic) chưa?"**
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A1. Chốt ngay, sang Cổng 4**; C2 và luật máy làm song song đầu Cổng 4 | Không mất nhịp; hình và người đã đủ tốt để làm animatic | Vào Cổng 4 khi C2 85% và C3 chưa đo được | Animatic dùng thiết kế hiện tại | Nếu B chọn "sửa lưới" thì phải cập nhật tài sản sau animatic |
| **A2. Chốt hình ảnh, nhưng làm một bước nhỏ "chuẩn C3" trước khi dựng animatic** (quyết định B + mã hoá shot tĩnh + xuất mặt nạ đúng) | Vào Cổng 4 với luật máy đo được thật | Thêm một bước ngắn | Animatic đi trên model sheet đã khớp | Thấp |
| A3. Thêm vòng 4 Cổng 3 để lên C2 ≥ 90% (sửa tư thế "hơ tay trên thang", "nhìn đèn lồng") | C2 qua ngưỡng trước khi khoá | Tốn thêm một vòng render | Trễ Cổng 4 | Hai tư thế này đọc bằng ngữ cảnh động tốt hơn silhouette tĩnh; sửa bằng tĩnh có thể thành gượng |

**Khuyến nghị: A2.**

**B. Tỷ lệ bộ phận render lệch model sheet (C3)**
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **B1. Đo lại model sheet theo nhân vật 3D đã duyệt** (quy trình đo cố định, ghi vào sheet, khoá lại) | Giữ đúng hình chủ dự án đã thấy và duyệt | Sheet đổi số | C3 đo được từ Cổng 4 | Thấp |
| B2. Sửa lưới cho khớp số sheet cũ | Giữ số cũ | Đổi dáng đã duyệt (tay Ida ngắn lại, tay Cas dài ra…) | Phải duyệt lại hình | Có thể mất cái chủ dự án đã thích |
| B3. Khiếu nại C3 (đo theo khung xương thay vì mặt nạ) | Không đụng phim | Không có căn cứ luật sai | Chờ K | Bị bác |

**Khuyến nghị: B1.**

**C. C2 85%**
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **C1. Giữ tư thế; ở animatic kể "hơ tay" bằng nhịp đếm ba và ánh trên mặt**, chấm lại C2 trên khung animatic | Diễn xuất tự nhiên | C2 tĩnh vẫn 85% tới lúc đó | Không tốn vòng thiết kế | C2 animatic vẫn có thể < 90% |
| C2. Sửa tư thế tĩnh cho rõ hơn (tay khum quanh kính đèn, mặt ngửa vào lửa) và đổi dáng mũ Cas | Dễ qua 90% | Mũ Cas trái 4A; tư thế dễ gượng | Mở lại 4A | Trái quyết định đã chốt |

**Khuyến nghị: C1.**

## 10. Việc đang chờ chủ dự án
1. Trả lời A, B, C.
2. Duyệt các yếu tố sáng tạo mới do Claude đề xuất, rồi ghi vào AUTHORSHIP:
   - bố cục trung cảnh 5 (qua vai);
   - bố cục cảnh 6 (ngõ, cửa sổ tầng 2);
   - bố cục khung kết (ô vàng là phòng góc nhà Cas);
   - dáng đi của Cas.
3. Phán quyết 2 khiếu nại mới trong `checks-appeal.md` (J1/J1b; tài liệu C3).
