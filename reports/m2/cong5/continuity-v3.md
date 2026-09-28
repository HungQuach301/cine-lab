# Rà continuity v3 — Cổng 5 v3 (layout) "Last Round" · 52 shot, 3 372 khung (2:20,5)

Người rà: agent continuity (phiên con của P). Chỉ báo lỗi, không sửa file nào ngoài báo cáo này và thư mục ảnh bằng chứng. Không đọc `checks/`. Không commit.

## Đầu vào và cách làm
- Hình: `/var/tmp/cine-out/final/video.mp4` (960×540, 24 fps, 3 372 khung, chưa phụ đề). Mốc shot: `assemble.json` (`film_frames` [f0, f1)). Thứ tự mới đã có trong bản ghép: s37w [2371, 2438) → **s39 [2438, 2544)** → **s38 [2544, 2578)** → s40; s45 [3048, 3096) → **s46 [3096, 3168)** → **s45c [3168, 3204)** → s47.
- Bản có phụ đề: `design/cong5/layout/out/layout.mp4` (+ `layout.script.txt`, `layout.text/elements.json`), bản trên đĩa lúc rà. Lưu ý: bản này và `screening/layout.mp4` **khác HEAD fe0355e** (thay đổi chưa commit trong cây làm việc, 11:40). Đã kiểm: ngoài các khung có phụ đề, hình trùng `video.mp4` (khung 100, 1500, 2000, 3000 và ±1 khung quanh mọi mốc phụ đề: 0 điểm ảnh lệch > 40/255).
- Giải mã **toàn bộ 3 372 khung** của cả hai video (`-fps_mode passthrough`). So từng **cặp shot kề nhau** (51 chỗ cắt) trên khung đầu, giữa, cuối mỗi shot, rồi phóng to vùng cần kiểm. Tiêu chí: đạo cụ, trang phục (mũ #262a33, tóc bạc, khăn, hoa tai), trạng thái đèn L1–L11 / P0–P5 / cột sân trước, nguồn sáng, vị trí, hướng màn hình, trục 180°, hướng nhìn. Đối chiếu `shots/layout/continuity/canh-1…6.md`, `LAYOUT-W1.md` §14, `LAYOUT-W2.md`, `BAO-CAO-W2-A.md` mục "Vòng v4", `bible/characters.md` v1.4, `bible/world-rules.md` v0.5.
- **Kiểm "nhảy" khung đầu (B-i):** với mọi shot, đếm điểm ảnh lệch > 24/255 giữa f0→f1, f1→f2, f2→f3 và ba cặp cuối shot. Nếu khung đầu còn mang trạng thái của shot trước thì f0→f1 phải vọt so với f1→f2.
- **Thoại:** đo mốc lời trên `layout.stems/dialogue.flac` (năng lượng RMS 20 ms, ngưỡng 2 % đỉnh).
- **Đồng hồ:** đọc giờ bằng mắt trên ảnh phóng to ở đầu, giữa, cuối mỗi shot có đồng hồ. Thêm dải khung s46 cách 6 khung (3096 → 3162). Kim phút ở s06, s09, s09w chỉ đi 0,2–0,3° trong shot, dưới độ phân giải 960 px, nên chỉ kiểm được là không có khung nào kim nhảy (lệch khung kề = 0 điểm ảnh > 24 ở s09, s09w; ở s06 chỉ lệch ở f452–455 khi cất đồng hồ).
- Số khung là số khung toàn cục (từ 0). Màu đo trên JPEG trích từ video 4:2:0, chỉ dùng để so tương đối.
- Bằng chứng: `reports/m2/cong5/continuity-v3/*.jpg` (mỗi ảnh ≤ 150 KB, có nhãn shot + khung + giây).

## Bảng lỗi

| # | Mức | Khung (toàn cục) | Shot | Mô tả | Bằng chứng | Gói sửa |
|---|---|---|---|---|---|---|
| N10 | nên sửa (mới) | 2988–3047 → 3048–3095 → 3096–3167 → 3168–3203 | s44 → s45 → s46 → s45c | **Hướng nhìn ở s45 không dẫn tới đồng hồ quảng trường, và nhịp nhìn → insert → POV bị lỏng.** Ở s44, miệng ngõ (phố trắng) là hậu cảnh, Ida quay về phía máy. Ở s45, nền sau lưng bà (phải khung) cũng là miệng ngõ: phố trắng, nhà có cửa sổ, đá lát. Trái khung là tường ngõ ấm. Lúc 1,0–1,6 s bà ngẩng lên về phía máy / trái khung (f3095), tức **quay lưng lại** miệng ngõ. Ở s47 bà đi về miệng ngõ, xa máy. Vì vậy địa lý trên hình đặt đồng hồ quảng trường **sau lưng** bà, trong khi sheet s45 ghi "ngẩng nhìn về miệng ngõ". Thêm vào đó, 3 s insert s46 chen giữa cái ngẩng và s45c. Kết quả: s45c đọc như một cảnh chèn xác nhận giờ thành phố, không phải POV. Ý vẫn đọc được: bà vặn đồng hồ, rồi giờ thành phố khớp, và giờ chỉ tiến. Nhưng mất quan hệ nhân quả "thấy giờ thành phố → vặn đồng hồ". | `N10_s44-s45-s46-s45c_huong-nhin.jpg` | **W2:** ở s45, 1,0–1,6 s cho bà quay đầu về miệng ngõ (sau lưng, phải khung), hoặc đổi máy s45 sang 3/4 sau-phải để miệng ngõ ở trước mặt bà. Không đổi thứ tự (d). Kiểm mù quyết. |
| N11 | nên sửa (mới, sheet) | 2232–2370; 2438–2543; 3048–3095 | s37, s39, s45; bible | **Sheet khác hình sau vòng v4.** (1) `canh-5.md` s37 và s39 ghi "nhìn lên phố (phải khung)". Trên hình, s39 (f2438, f2510, f2543) mắt nhìn xuống, mặt gần chính diện, không nhìn sang phải. s37 (f2370) mặt 3/4 sang phải nhưng mắt nhìn xuống. Hình hiện tại **hợp** với thứ tự mới, vì ở s38 Cas ngước lên. Nên sửa sheet, không sửa hình. (2) `canh-6.md` s45: "ngẩng nhìn về miệng ngõ" (xem N10) và "tay trái đỡ": trên hình tay trái giơ riêng ngang vai (G5/G6). (3) `bible/characters.md` dòng 12: "gập đồng hồ **không gõ** (cảnh 6)", nhưng `canh-6.md` ghi "không có nắp đồng hồ trên hình". Bible khoá, nên ghi cho P / Cổng 6, không sửa ở layout. | `c_s37w-s39-s38-s40_phu-de.jpg`; `N10_…jpg` | W2 (`canh-5`, `canh-6`); P (bible ↔ Cổng 6) |
| N12 | nên sửa (mới) | 3095 → 3096 | s45 → s46 | **Đồng hồ bỏ túi đổi hình dạng qua cắt MS → insert.** s45: vỏ vàng mảnh, có khoen treo, mặt kem vàng. s46 (và s06, s09w): viền dày nâu đỏ, không thấy khoen, mặt cam. Riêng màu mặt có thể do ánh sáng (s45 ánh trắng, s46 ánh cửa sổ ấm), nhưng màu và độ dày viền, cùng cái khoen, thì không. Đây là cắt thẳng giữa hai shot liền nhau của cùng một đạo cụ. Ở s45 đồng hồ còn "dính" trên lòng bàn tay dựng đứng, mặt quay ra máy (G5/G6), nên đọc thành vật khác với đồng hồ nằm trong lòng tay ở insert. | `d_dong-ho_dau-giua-cuoi.jpg` (hàng 2 và hàng 3) | W2 (s45 dùng đúng mô hình đồng hồ của insert) hoặc P chốt mô hình đạo cụ chung cho W1/W2 |
| G1 | ghi nhận (cũ, còn) | 1260–1331 | s23 | Đầu đèn P5 và cột sân trước tắt đúng lịch, nhưng kính vẫn đọc thành đĩa xám sáng trên trời tối (f1296). | — | Cổng 7 |
| G2 | ghi nhận (cũ, còn) | 2578–2639 | s40 | Mũ đọc như đội thẳng dù sheet ghi `hat_back` 0,35. Nay s40 đứng sau s38 (Ida chỉ thấy vạt váy), nên nhảy mũ từ s39 (lộ trán) sang s40 cách nhau 1,4 s thay vì cắt thẳng. Vẫn còn. | `c_s37w-s39-s38-s40_phu-de.jpg` (ô 6) | Cổng 6 |
| G5/G6 | ghi nhận (cũ, còn) | 3018; 3048–3095 | s44, s45 | s44: sheet ghi "tay đặt ngực", hình một tay giơ lên phía cửa sổ. s45: tay trái giơ ngang vai, tách khỏi đồng hồ. Đồng hồ dính trên lòng bàn tay dựng đứng, mặt quay ra máy, và ở f3048–3072 bàn tay che nửa dưới mặt bà. | `N10_…jpg` | Cổng 6 |
| G7 | ghi nhận (cũ, còn) | 864; 918; 972; 2438–2543; 2820 | s11, s12, s13, s39, s42 | Màu mũ Ida nhảy theo nguồn sáng. s39 (render lại ở v4) vẫn nâu đỏ: trung vị điểm tối vùng vành mũ **#311615** (f2438), v2 là #2b140e. s40 f2639 dưới điện là #19181f (đúng D2). s11–s13 không render lại. | `c_…jpg` | Cổng 7 |
| G8 | ghi nhận (cũ, **mở rộng**) | 3168–3203; 636–671 | s45c, s09 | s45c: kim và vạch màu hồng nâu, giờ đúng 10:00. **Mới ghi:** s09 sau khi mặt đồng hồ sáng (f636, f671), kim phút và kim giờ chỉ còn nét nhạt trên mặt loá. Giờ 8:00 đọc rõ ở f600–607 (trước khi sáng), khó đọc sau đó. | `d_dong-ho_dau-giua-cuoi.jpg` (hàng 1, 3) | Cổng 7 |
| G9 | ghi nhận (cũ, còn) | 2381–2687 | s37w, s40w | Quầng loá bóng P5 phủ mảng trời góc trên trái (f2664). | — | Cổng 7 |
| G10 | ghi nhận (cũ, còn) | 2687 → 2688 | s40w → s41 | Ida từ đỉnh thang xuống đất đang trao đèn, qua cắt giữa hai WS. | — | Cổng 6 |
| G11 | ghi nhận (cũ, còn) | 1919 → 1920 | s32 → s33 | Cuối s32 Ida quỳ, đầu s33 bà đã đứng (sheet: "0–0,6 s đứng dậy"). | `OK_C5-N3_s32-s33-s34-s35.jpg` (ô 1–2) | Cổng 6 |
| G12 | ghi nhận (cũ, còn) | 3048–3095 | s45 | Tóc đọc xám bạc tối dưới vành mũ (ánh ngõ yếu từ trên), sáng hơn v2 vì nền s45 nay sáng. | `N10_…jpg` | Cổng 7 |
| G13 | ghi nhận (cũ, còn) | 2988–3047 → 3204 | s44 → s47 | s44 không có thang trong ngõ; s47 bà vác thang. Sheet đã ghi "Cổng 6 cần đặt". | `N10_…jpg` (ô 1, 6) | Cổng 6 |
| G14 | ghi nhận (mới) | 1260–1264; 2578–2581 | s22 → s23; s38 → s40 | **Phụ đề vắt qua cắt.** `sub02` "Not yet... not yet." (1188–1264) còn **5 khung** trên s23 (WS cuối phố). `sub07` (2453–2581) còn **4 khung** trên insert s40. Lời thật L4 hết ở 106,87 s (f2565), sub07 giữ thêm 0,7 s qua hết s38. Quy ước phụ đề điện ảnh: cắt phụ đề trước điểm cắt (hoặc giữ ≥ 12 khung sang shot sau). | `G14_phu-de-vat-qua-cat.jpg` | P (khâu phụ đề: kết thúc sub02 ở 1259, sub07 ở 2577) |
| G16 | ghi nhận (mới — phần còn lại của N8) | 2892–2987 | s43 | Ô hổ phách là **điểm ấm duy nhất** trên toàn cảnh và lớn dần, nhưng **chưa đọc là ô cửa**: lõi hình giọt, sáng ở trên, không có khung chữ nhật, nằm ngay trên một khối sáng giống ống khói (phóng to f2940, f2987). Ở cỡ toàn khung, nó đọc là "một đốm đèn vàng", chưa phải "một ô cửa". | `N8b_s43_o-ho-phach_s43-s44.jpg` | Cổng 7 (hình ô: khung cửa, song, tỉ lệ đứng) |
| G17 | ghi nhận (mới — phần còn lại của N3) | 1980–2039 | s33 | Người và bóng trong hốc vòm: đầu và vành mũ bóng Ida đã ra trái người (f2039). Thân bóng vẫn còn chồng mép thân Ida. Bóng ở s33 thấp và nhạt hơn nhiều so với s34 ngay sau. Theo quyết định (e), việc này dời Cổng 7. | `OK_C5-N3_s32-s33-s34-s35.jpg` (ô 3–5) | Cổng 7 |

Không có lỗi mức **chặn**.

## Kiểm theo danh mục được giao

### 1. B-i — trạng thái ẩn, đèn lồng thắt lưng ở khung đầu shot
| Mục | Kết quả |
|---|---|
| Nhảy khung đầu (52 shot) | **Đạt.** Không shot nào có f0→f1 vọt so với f1→f2. Ví dụ, điểm ảnh lệch > 24/255 (f0→f1 / f1→f2): s02 798 / 800, s07 4 036 / 3 944, s08 195 / 256, s15 2 250 / 2 065, s23 34 / 52, s26 0 / 0, s35 38 / 34, s05 2 710 / 6 145 (đang đếm tay). Các chỗ vọt ở giữa shot đều là sự kiện theo lịch: s13 f949→950 (trắng tới Ida 39,55 s), s19 f1081→1082 (L8 45,05 s), s22 f1258→1259 (L10 52,45 s). |
| s02 (f96) | Đèn lồng **tắt** (bóng người ngược sáng, không có điểm sáng ở hông), f96 ≡ f97. s01 không có Ida. Đạt. |
| s05 (f288) | MCU, hông ngoài khung. Hướng người và phơi sáng f288 ≡ f289. Đạt. |
| s07 (f456) ← s06 | s06 là insert đồng hồ. s07 f456: đèn lồng sáng ở hông trái, phía gần máy (bà đi −x, máy phía nam). Đạt. |
| s08 (f552) ← s07 f551 | f551: đèn treo thẳng ở hông gần máy. f552–553: đèn treo thẳng ở phải khung (bà đi về máy, hông trái ở phải khung). Cùng trạng thái cháy. Đạt. |
| s15 (f1044) ← s14 f1043 | Cả hai: đèn sáng ở hông trái (phải khung). f1044 ≡ f1045. Khi bà quay 0,8–1,4 s, đèn đi theo thân, không trễ khung. Đạt. |
| s23 (f1260) ← s22 f1259 | s22 MCU không thấy hông. s23 f1260–1261: đèn sáng ở trái khung (hông trái khi bà chạy vào chiều sâu). Đạt. |
| s26 (f1488) ← s25 | s25 không có Ida. s26 MS cắt ở thắt lưng, đèn ngoài khung. f1488 ≡ f1489 ≡ f1535 (lệch 0). Đạt. |
| s35 (f2088) ← s34 f2087 | s34: đèn trên nền hốc. s35 f2088–2089: đèn sáng, treo thẳng ở hông, giống f2136 và f2148 (khung P kiểm toán). Đèn nhặt lại ngoài hình, đúng sheet. Đạt. |
| Đèn lồng cảnh 4 (N6) | s24 f1379 sáng. s27, đầu s30: hông trái ở phía khuất máy (không kết luận được từ hình, đúng như sheet). s30: vùng tường sáng tăng liên tục 118,2 → 152,9 (f1748 → f1770, bước 2 khung), không bật cóc. Đạt. |

Bằng chứng: `OK_B-i_den-long_qua-cat.jpg`.

### 2. C-i — s43 máy đẩy chậm, ô cửa hổ phách
- Máy: dolly và zoom liên tục, không giật (lệch khung kề 494 → 1 632 → 2 967 điểm ảnh ở đầu shot, tăng đều). Khung mở đầu f2892 giữ bố cục của s10.
- Ô hổ phách: **một** cụm ấm bão hoà duy nhất trên cả khung, ở f2892, f2916, f2940 (lọc r > 140, r > g > b, bão hoà > 0,45: cụm duy nhất ở ô lưới (y 240, x 520)). Cụm lớn dần: ≈ 5 × 9 px ở f2892 → 8 × 16 px ở f2940 → 8 × 20 px (cả quầng) ở f2987. Tâm cụm trôi từ (0,55; 0,46) sang (0,53; 0,48) khung. Cụm ấm thứ hai ở f2987 (x ≈ 140, y ≈ 460) là mái nhà hồng nhạt bị điện rọi, không phải ô cửa. Mọi ô cửa khác trắng lạnh hoặc xanh xám. Mặt tiền một số nhà gần có màu nâu cam của vật liệu tường, không phải ô sáng.
- **Có đọc là "một ô vàng" không:** đọc được là **một điểm vàng duy nhất**, lớn dần, gần giữa khung. Như vậy đạt phần "toàn cảnh trắng, một [điểm] vàng" và phần chính của N8. **Chưa** đọc là một ô cửa (xem G16).
- **Nối s43 → s44:** s43 kết ở điểm ấm gần giữa khung. s44 f2988 mở ở ngõ tối, vệt hổ phách ô cửa trên tường trái cao, Ida dưới cửa sổ. Mạch "ô cửa ấm → ngõ, người dưới cửa sổ" đọc được. Hướng màn hình: điểm ấm ở giữa-phải (s43) → vệt ấm ở trái-trên (s44). Hai shot khác bộ và khác cỡ, nên không coi là lỗi hướng. **Đạt.**
- Bằng chứng: `N8b_s43_o-ho-phach_s43-s44.jpg`.

### 3. Câu thoại cuối L4 — thứ tự s37w → s39 → s38 → s40
| Mục | Kết quả |
|---|---|
| Mốc lời thật (stem thoại) | Các đoạn L4 sau 90 s: 93,09–94,95 · 96,56–98,02 · 99,54–100,91 · **102,33–102,84 ("Just…")** · **103,86–106,87** ("keep a little dark for the ones who need it."). |
| Lời bắt đầu trên hình ai | **Ida (s39).** "Just…" bắt đầu ở f2455,8, tức 0,74 s sau khi vào s39 (f2438). **Đạt.** |
| Phụ đề `sub07` trong layout.mp4 | Hiện f2453–f2581 (102,21–107,58 s). Khung đầu f2453 nằm trên **s39 (Ida)**, 0,12 s trước lời thật. Phụ đề kéo qua s38 (Cas, f2544–2577) và còn **4 khung trên s40** (f2578–2581): xem G14. Trên hình, phụ đề bắt đầu trên Ida: **đạt.** |
| Cắt s39 → s38 | 106,0 s (f2544), giữa cụm lời liền 103,86–106,87. Theo whisper của W2 là ranh "ones / who". Cas phản ứng trong phần "…who need it." Đọc tự nhiên. |
| s37w → s39 | WS (Ida trên thang ở phải khung, x ≈ 905; Cas dưới chân thang, phải hơn) → CU gần chính diện. Không đổi phía. `hat_back` 0,35, tóc bạc, hoa tai, khăn khớp. Đèn lồng hông sáng ở s37w, ngoài khung ở s39. **Đạt.** |
| s39 → s38 (trục, hướng nhìn) | s39: Ida nhìn xuống, gần chính diện. s38: máy cao gần mắt Ida; vạt váy Ida ở trên-trái khung; Cas ngước lên về trái-trên (về phía máy / Ida). Quan hệ **Ida trái/trên, Cas phải/dưới** giữ đúng như s37w. Hướng nhìn khớp: bà nhìn xuống, cậu nhìn lên. **Đạt.** (Sheet ghi s39 "nhìn phải khung": N11.) |
| s38 → s40 | Insert van, máy phía nam nhìn về bắc, gần trục Ida–Cas, không có Cas nên không vượt trục. Ida ở phải L11, như ở s37w và s40w. Hốc cửa ở trái khung, đúng địa lý khi máy xoay khoảng 90° so với s37w. Ánh trắng phẳng và L11 cháy nhạt khớp s38. **Đạt.** L11 tắt ở **f2621** (1:49,2); P5 bật **f2381** (nhấp f2383–2384, đứng từ f2385): không đổi so với v2. |

Bằng chứng: `c_s37w-s39-s38-s40_phu-de.jpg` (khung trích từ layout.mp4, có phụ đề).

### 4. Đồng hồ — giờ đọc trên hình
| Shot | Đầu | Giữa | Cuối | Ghi chú |
|---|---|---|---|---|
| s06 bỏ túi (384–455) | 7:31 (f384) | 7:31 (f420) | 7:31 (f455) | Kim phút ngay qua số 6, kim giờ giữa 7 và 8. Không có khung nào kim nhảy. |
| s09 quảng trường (600–671) | 8:00 (f600) | 8:00 (f636, kim nhạt) | 8:00 (f671, kim nhạt) | Mặt sáng từ f607. G8 mở rộng. Lệch khung kề 0. |
| s09w bỏ túi (672–719) | 7:53 (f672) | 7:53 (f696) | 7:53 (f719) | Chậm 7 phút so với 8:00. Lệch khung kề 0. |
| s45 bỏ túi, MS (3048–3095) | ≈ 9:53 (f3048) | ≈ 9:53 (f3072) | ≈ 9:53 (f3095) | Hai kim cùng quanh số 10, mặt ≈ 60 px, chưa đọc rõ phút (đúng như sheet). Hình đạo cụ: N12. |
| s46 bỏ túi, insert (3096–3167) | 9:53 (f3096–3102) | ≈ 9:57 (f3132) | 10:00 (f3150–3167) | Dải khung cách 6 khung: kim phút quay **thuận chiều** liên tục 3102 → 3150, rồi đứng. Kim giờ nhích từ sát số 10 tới số 10. |
| s45c quảng trường (3168–3203) | 10:00 (f3168) | 10:00 (f3186) | 10:00 (f3203) | Kim hồng (G8). |

- **Chuỗi người xem thấy:** 7:31 (bỏ túi) → 8:00 (thành phố) → 7:53 (bỏ túi, chậm 7 phút) → … → ≈ 9:53 (bỏ túi) → 9:53 → 10:00 (vặn) → 10:00 (thành phố). Theo từng đồng hồ, giờ **chỉ tiến**. Không có chỗ nào giờ lùi, cả trong shot lẫn giữa các shot. Chỗ 8:00 → 7:53 là hai đồng hồ khác nhau (đồng hồ bà chậm 7 phút), và bố cục insert đã dựng sẵn cho điều đó. **Đạt.**
- **Nhịp nhìn → insert → POV cảnh 6:** đọc được **về ý** (bà vặn đồng hồ, giờ thành phố xác nhận), nhưng **không đọc là POV**. Hướng nhìn ở s45 ngược phía miệng ngõ, và 3 s insert chen giữa cái ngẩng và s45c. Xem **N10**.
- Bằng chứng: `d_dong-ho_dau-giua-cuoi.jpg`.

### 5. Trạng thái các lỗi đang mở ở lần 2
| Mã | Trạng thái | Căn cứ |
|---|---|---|
| **C5** (chặn) ngoài vòm s33 sáng | **Đã đóng** | s33 f1920/1980/2039: tường ngoài vòm trái (48, 46, 52), phải (96→86, 70→65, 63→60), nền ngoài (32–43, 26–31, 30–31). v2 là (217, 217, 221). Tối lạnh, hổ phách từ phải, khớp s35 (tường quanh L11 (143–150, 92–99, 59–64)). s42b/s42 sau P5 vẫn trắng: đúng. |
| **N2** cách cầm đèn s42a → s42b | **Đã đóng** | f2771: ôm sát ngực, đèn áp bụng. f2772: nhìn nghiêng, hai tay trước ngực, đèn ở bụng. f2790–2806: vẫn ôm trước người khi đi. |
| **N3** người/bóng s33 | **Đã cải thiện, phần còn lại dời Cổng 7** theo quyết định (e) → **G17** | f2039: đầu và vành mũ của bóng đã tách khỏi người, thân bóng còn chồng một phần. s34 đạt. |
| **N6** đèn lồng cảnh 4 | **Đã đóng** (P chọn phương án 1) | s30 tăng liên tục 118 → 153, không bật cóc. Sheet `canh-3/canh-4` thống nhất "cháy liên tục". |
| **N7** nhảy hành động s42b → s42 | **Đã đóng** | f2819: Cas ngồi xổm, đèn trên nền, bóng lớn trên vách → f2820 cùng tư thế. |
| **N8** "một ô cửa hổ phách" s43 | **Đóng phần chính** (một điểm vàng duy nhất, nhìn thấy, lớn dần, gần giữa). **Còn hình dạng ô → G16** | Mục 2 ở trên. |
| **N9** sheet số cũ | **Đã đóng** | `canh-3` dòng 15 (1:39,2), "Chỗ hở 3" (14,3; −7,15), s24/s24c khớp hình. `canh-4` bảng toạ độ theo B1, bỏ ống thoát nước s25. `canh-5` 1:20,0–2:00,5, P5 1:39,2, L11 1:49,2, s33 5 s. `canh-6` 2:00,5–2:20,5. `LAYOUT-W1` dòng 62 (máy s24 A2), dòng 89 (ghi rõ "giai đoạn C dùng … B1 dời sang"). `LAYOUT-W2` §1 140,5 s, §5 `houseX0N` 18,5. Các số cũ còn lại (`LAYOUT-W1` §1 dòng 16 "142,5 s", §5b dòng 170) nằm trong mục nhật ký giai đoạn A/C, không phải bảng hiện hành. Sheet mới lệch hình ở v4: N11. |
| G1 | Còn | f1296 |
| G2 | Còn (nay cách một shot, xem bảng) | f2578–2639 |
| G5/G6 | Còn | f3018, f3048–3095 |
| G7 | Còn (s39 #311615) | f2438 |
| G8 | Còn, **mở rộng** sang s09 | f636, f671 |
| G9 | Còn | f2664 |
| G10 | Còn | f2687 → f2688 |
| G11, G12, G13 | Còn (không đổi mã các shot này ở v3, trừ G12 nền sáng hơn) | — |

### 6. Rà lại toàn bộ các cặp kề nhau
- **Cảnh 1** (s01 → s08):
  - Hướng đi phải → trái nhất quán (s02, s07); s08 bà đi về máy.
  - Thang trên vai phải, đầu chúc về trước.
  - Đèn lồng: tắt ở s02–s04 và **cháy từ s04** (lịch 11,7 s).
  - Đèn: L4 bắt lửa trong s03; s07 L1–L5; s08 L6.
  - Trời chạng vạng → đêm ở cắt s08 → s09 (nhảy thời gian theo kịch bản).
  - **Đạt.**
- **Cảnh 2** (s09 → s14):
  - s10e bóng quảng trường bật trong shot. s12 P2 bật. s13 trắng tới Ida ở f949–950. s14 không bóng.
  - Đèn lồng sáng hông trái ở s13, s14.
  - Mũ theo nguồn sáng: G7.
  - **Đạt.**
- **Cảnh 3** (s15 → s24c):
  - s15 xuống thang, thang lên vai phải. s19 L8 f1081, P3 bật.
  - s21 sào tay phải. s22 L10 f1258.
  - s23 P5 và cột sân trước tắt, Cas ở casSpot.
  - s24 Ida trái, Cas phải, bóng lớn Ida + thang. s24c Cas nhìn trái, mũ len có quả bông, không bóng Ida.
  - **Đạt.**
- **Cảnh 4** (s25 → s32):
  - Cột sân trước bật f1546, nhấp, đứng f1556.
  - Chim L11 tan ở s27. s28 không còn chim.
  - s29 Cas quay trái khung. s30 tháo đèn, sáng tăng liên tục.
  - s31 đèn tay phải. s32 chim lớn ấm.
  - Trục Ida trái / Cas phải giữ.
  - **Đạt.**
- **Cảnh 5** (s33 → s42):
  - C5 đã đóng. s34 → s35 đèn từ nền lên hông (ngoài hình, đúng sheet).
  - s36 đẩy mũ. s37–s39 `hat_back` 0,35.
  - P5 f2381, L11 tắt f2621. s40w, s41, s42a kính L11 tối.
  - Trao đèn ở s41. s42a, s42b ôm sát ngực. s42b → s42 ngồi xổm liền mạch.
  - Trục Ida trái / Cas phải ở s37w, s40w, s41, s42a, s42.
  - s42 kéo mũ lại.
  - **Đạt**, trừ G2, G7, G10, G11, G17.
- **Cảnh 6** (s43 → s48):
  - Trời s43 xanh đen, không quầng.
  - Không đèn lồng ở s44, s45, s47. Mũ đội thẳng. Thang vai phải ở s47.
  - s48 Cas có mũ len và quả bông, chim trên bóng đầu, mờ về đen.
  - Lỗi: N10, N12, G5/G6, G13, G16.

## Tổng theo mức
| Mức | Số | Mã |
|---|---|---|
| Chặn | **0** | — |
| Nên sửa | **3** | N10, N11, N12 |
| Ghi nhận | **13** | G1, G2, G5/G6, G7, G8, G9, G10, G11, G12, G13, G14, G16, G17 |

Lỗi lần 2 đã đóng: **C5, N2, N6, N7, N9**. Đóng phần chính: **N8** (phần còn lại → G16). Chuyển Cổng 7 theo quyết định (e): **N3** (→ G17).

Theo gói:
- **W2:** N10 (s45 hướng nhìn), N11 (`canh-5`, `canh-6`), N12 (đồng hồ s45).
- **P:** N11 (bible ↔ "gập đồng hồ", Cổng 6), N12 (nếu chốt mô hình đạo cụ chung), G14 (mốc phụ đề).
- **Cổng 6/7:** các mục G.

## Kết luận
**Layout Cổng 5 v3 không còn lỗi mức CHẶN.** Lỗi chặn duy nhất của lần 2 (C5) đã đóng. Các thay đổi v3/v4 đạt:
- B-i: không còn nhảy khung đầu ở 52 shot, đèn lồng khớp qua cắt.
- Câu cuối L4 bắt đầu trên Ida, cả lời lẫn phụ đề. Trục và hướng nhìn qua s37w → s39 → s38 → s40 đúng.
- Giờ trên hình chỉ tiến ở mọi đồng hồ.
- s43 có một điểm vàng duy nhất lớn dần.

Còn 3 lỗi nên sửa, không chặn: N10 là nhịp nhìn → POV cảnh 6, N11 là sheet, N12 là hình đạo cụ đồng hồ qua cắt s45 → s46.

## Đang chờ chủ dự án / P
1. **N10:** chọn cách sửa hướng nhìn s45 (quay đầu về miệng ngõ, hoặc đổi máy s45), hay chấp nhận s45c là cảnh chèn chứ không phải POV. Kiểm mù quyết.
2. **N12:** chốt mô hình đồng hồ bỏ túi dùng chung cho s45 và các insert.
3. **G14:** chỉnh mốc kết thúc `sub02` và `sub07` cho khỏi vắt qua cắt.
4. `layout.mp4` và `screening/layout.mp4` trong cây làm việc khác HEAD (chưa commit). P xác nhận bản này là bản đóng gói chính thức.
5. P commit báo cáo này và thư mục bằng chứng (agent không commit).
