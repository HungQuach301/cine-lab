# RÀ CONTINUITY — Cổng 6 · W2 vòng 1 · cảnh 4–6 (s25 → s48, 59,0–140,5 s)

Người rà: agent continuity (chỉ báo lỗi, không sửa). Ngày 29/09/2026. Nhánh P (đã merge W2). Không đọc mã trong `checks/`.
Căn cứ: `bible/characters.md` (v1.5.1/v1.6), `bible/world-rules.md` (v0.5), `design/cong3/model-sheet/ida.json`, `cas.json` (trường mô tả), `shots/layout/continuity/canh-4.md`, `canh-5.md`, `canh-6.md`, `shots/layout/LAYOUT-W2.md`, `reports/m2/cong6/w2/BAO-CAO-W2-V1.md`, PLAN.md mục "Việc cho Cổng 6 (từ Cổng 5)".
Hình: thumbs a/b/c `/var/tmp/cine-out/W2/thumbs/`, bảng khung `reports/m2/cong6/w2/bang-khung_*.jpg`, khung trích bằng ffmpeg từ các mp4 hiện hành (BAO-CAO mục 8). Ảnh bằng chứng tự trích ở `/tmp/claude-0/cont-w2/` (tạm, không commit).
Quy ước: "khung" = khung toàn cục 24 fps (giây phim × 24); "n" = chỉ số khung trong tệp mp4 đã ghi.

> Ghi chú đường dẫn: lệnh giao yêu cầu nộp `shots/layout/continuity/RA-W2-V1.md`; cấu hình phiên này chỉ cho phép ghi `reports/continuity.md` và cấm sửa tệp khác, nên báo cáo nằm ở đây. P chép sang nếu cần.
> Không có ảnh mốc s24c (`/var/tmp/cine-out/P/full/thumbs/` không có s24c) nên chỗ nối W1 → s25 **chưa kiểm được**.

## 1. Bảng lỗi

| Mã | Shot | Khung / giây | Mô tả | Mức | Bằng chứng |
|---|---|---|---|---|---|
| N1 | s40 | n36 → n37 `video_s40.mp4` (108,90 → 108,94 s, ≈ khung 2614–2615); lửa tắt n43 (109,19 s, ≈ khung 2621) | Mặt Ida **đã biến mất khỏi hình 6 khung (0,25 s) trước khi L11 tắt**: từ 108,94 s chỉ còn gáy, tai, búi; kính lồng còn sáng tới n42 (109,15 s) và tối từ n43. Hai nhịp "quay mặt đi" và "lửa tắt" tách rời, không trùng khung như quyết định cố định "mặt chìm tối đúng 109,20". Ngoài ra sau 109,2 s gáy và tóc bạc vẫn sáng đều dưới điện trắng: hình đọc "bà quay đi", không đọc "chìm vào bóng tối" (báo cáo W2 §2 đã nêu lý do: điện phẳng không đổ bóng). | **chặn** (quyết định cố định của chủ dự án; P có thể hạ mức nếu chủ dự án chấp nhận lệch 6 khung) | `reports/m2/cong6/w2/ra-continuity/s40_tung_khung.jpg`, `s40_quanh_109_2.jpg`; `reports/m2/cong6/w2/bang-khung_s40.jpg` (108,90 / 109,40) |
| N2 | s40w → s41 | s40w cuối 111,96 s (khung 2687) → s41 đầu 112,00 s (khung 2688) | **Nhảy vị trí và đạo cụ qua cắt WS → WS**: cuối s40w Cas đứng TRƯỚC Ida, quay lưng về máy, Ida ở sau-PHẢI cậu; đầu s41 Ida TRÁI, Cas PHẢI đứng song song, cách nhau rõ. Đèn lồng: cuối s40w ở tay bà sát bên phải/dưới Cas (111,79 s bên phải Cas, 111,96 s đốm sáng thấp bên trái Cas) → đầu s41 ở hông/sau lưng bà phía cột đèn (trái khung), rồi 112,5 s mới ra trước giữa hai người. Hai máy cùng phía đường Ida–Cas (không vượt trục về hình học) nhưng ở s40w đường này gần song song trục ống kính nên thứ tự trái–phải trên hình lật. | nên sửa | `reports/m2/cong6/w2/ra-continuity/noi_s40w_s41.jpg` |
| N3 | s40w | 110,9–111,5 s (khung 2662–2676) | **Dáng xuống thang đọc như ngả/rơi khỏi thang**: thân bà lệch hẳn ra ngoài mặt thang về phía Cas, hai tay duỗi thẳng ngang, thân nghiêng ≈ 45° (111,17 s); 111,25 s thân bà chồng lên người Cas (không xác định được xuyên lưới trên hình 960 px). G10 "bà xuống thang trong shot" có, nhưng không đọc là bước xuống từng bậc. | nên sửa | `reports/m2/cong6/w2/ra-continuity/s40w_xuong_thang.jpg`, `noi_s40w_s41.jpg` (111,25; 111,54) |
| N4 | s39 → s38 | s39 cuối 105,97 s (khung 2543) → s38 106,00 s (khung 2544) | **Ánh mắt không khớp (cùng nhìn TRÁI khung)**: s39 bà nhìn nghiêng xuống về TRÁI khung (mặt hướng lồng đèn, +z); s38 Cas ngước lên về TRÁI khung. Theo s37w (WS, cùng phía máy), Cas ở PHẢI-dưới, sau lưng bà — nên ở s39 hướng nhìn của bà đi ra xa Cas, không phải "bà nhìn xuống, cậu nhìn lên" như continuity canh-5 mô tả. Liên quan trực tiếp tới Đ6 (phía máy PA1) đang chờ chủ dự án. | nên sửa (chờ Đ6) | `reports/m2/cong6/w2/ra-continuity/N_s39_s38_anh_mat.jpg`; thumbs `s37w_c`, `s39_c`, `s38_a` |
| N5 | s42b → s42 | s42b cuối 117,46 s (khung 2819) → s42 117,50 s (khung 2820) | **Ida "hiện ra" ở miệng vòm qua cắt**: s42 mở với bà đứng yên ở miệng vòm (1,25; 5,25 hệ hốc). Máy s42b (0,9; 1,25; 8,2) nhìn vào hốc đi qua đúng chỗ đó (tính: sâu 2,9 m, lệch phải 0,63 m trong nửa khung 1,63 m — bà phải chiếm góc dưới-phải khung), nhưng suốt s42b không có bà. Không có nhịp bà bước tới. | nên sửa | thumbs `s42b_a/b/c`, `s42_a`; `reports/m2/cong6/w2/ra-continuity/noi_s42a_s42b_s42.jpg` |
| N6 | s32 → s33 (G11) | s33 n0–n16 (80,00–80,67 s, khung 1920–1936) | **Không thấy nhịp đứng dậy**: s33 khung đầu bà đã đứng đủ cao (đỉnh mũ cùng mức ở 80,00 / 80,29 / 80,67 s), chân như đang bước. Continuity ghi "0–0,6 s đứng dậy từ tư thế quỳ" và báo cáo ghi G11 "đã có" — trên hình không có. Cắt s32 → s33 đã là cắt nén địa điểm (tường → hốc 12 m) nên nhảy quỳ → đứng không phải sai vật lý, nhưng G11 chưa đạt như mô tả. | nên sửa | `reports/m2/cong6/w2/ra-continuity/s33_dau.jpg`, `noi_s32_s35.jpg` |
| N7 | s30 (và s27) | s30 72,0–72,7 s (khung 1728–1745); s27 64,0 s | **Đèn lồng ở hông không thấy sáng**: s30 bà quay phải, hông TRÁI hướng về máy, nhưng không có kính đèn sáng ở hông (72,4 s chỉ thấy một khối tối sau hông); 72,8 s đèn mới hiện, sáng, trong tay. s27 (WS) cũng không thấy điểm ấm ở hông bà. Trái N6 cảnh 4 ("cháy liên tục… ở thắt lưng kính đèn sáng"). So sánh: s35, s40w đèn hông sáng rõ. | nên sửa | `reports/m2/cong6/w2/ra-continuity/z_s30_start.jpg`, `den_hong.jpg` |
| N8 | s37b | 96,4–98,8 s (khung 2314–2371), rõ ở 97,9 và 98,7 s | **Tay trên van còn đọc như "mẩu"**: tay trái bị mép dưới–trái khung cắt, chỉ còn một mảng da phẳng mép răng cưa sau thân van đồng, không thấy ngón. s36 (1,55–2,0 s), s37, s39: tay đọc rõ là bàn tay đang nắm (đạt). | nên sửa | `reports/m2/cong6/w2/ra-continuity/s37b_tay_van.jpg` (so `s36c_s37_tay.jpg`) |
| N9 | s47 | 133,5–135,5 s (khung 3204–3251) | **Cách vác thang lệch model sheet**: thang gần thẳng đứng sau lưng, bậc thang cắt ngang mũ và gáy bà (đọc như thang xuyên đầu). Model sheet `ida.json` props.ladder: "vai phải, nghiêng 28° so với phương ngang, đầu chúc về trước"; silhouette_keys: "vác chéo vai phải, đầu thang chúc về trước — nhận ra từ xa". | nên sửa | thumbs `s47_a/b/c`; `reports/m2/cong6/w2/ra-continuity/canh6_zoom.jpg` (hàng dưới) |
| N10 | s45 (B1) | 127,0–128,0 s (khung 3048–3072) | **Đồng hồ không thấy trong 1 s đầu**: hai bàn tay khép che kín đồng hồ, chỉ thấy tay; từ ≈ 128,5 s mới thấy một đĩa tối ở lòng tay. B1 "làm rõ đồng hồ trong tay" mới đạt nửa sau shot. Tay trái xoè cứng như vuốt ở 127,0–128,0 s. | nên sửa | `reports/m2/cong6/w2/bang-khung_s45.jpg` |
| N11 | s26 | 62,0–64,0 s (khung 1488–1535) | Mặt Ida gần chính diện, mắt nhìn gần ống kính; continuity ghi "nhìn **phải khung** (về Cas)" — trên hình không đọc hướng về Cas. Là MS, không thuộc cao trào PA1, nhưng nằm trong nhóm "khung chính diện bị gọi búp bê" (characters v1.5). | ghi nhận | `reports/m2/cong6/w2/ra-continuity/s26_mat.jpg`, `z_s26b.jpg` |
| N12 | s36 → s37 | cắt 93,0 s (khung 2232) | Đổi góc 60° → 90° (chỉ 30°) với cỡ MCU → MCU: sát ngưỡng quy tắc 30°, có nguy cơ đọc như cắt nhảy. | ghi nhận | thumbs `s36_c`, `s37_a` |
| N13 | s35 | cuối shot ≈ 90,5–91,0 s (khung ≈ 2172–2183) | Một mảng bóng tối lớn hình vòm trên tường bên phải L11 (bóng của bà/thang sát ngọn lửa, hợp quang học) — đọc như vật lạ, không nối sang s37w. | ghi nhận | thumb `s35_c`; `reports/m2/cong6/w2/ra-continuity/zoom_misc.jpg` (ô cuối) |
| N14 | s40 / tài liệu | — | Số đo tự khai lệch nhau: `canh-5.md` bảng Cổng 6 "cúi 34° + quay mặt 38°", BAO-CAO §2 "cúi 30°, quay mặt 72°, thân 14°". Cần một số. | ghi nhận | hai tệp nêu |
| N15 | s42a → s42b | 115,46 → 115,50 s (khung 2771–2772) | Đèn lồng Cas ở s42b (0–1,45 s) nằm thấp hơn (ngang hông, dưới hai bàn tay) so với s42a (áp bụng–ngực). Cùng `casHug` nhưng đọc là cầm thấp. | ghi nhận | `reports/m2/cong6/w2/ra-continuity/noi_s42a_s42b_s42.jpg` |
| N16 | s40w | 110,6–110,9 s (khung 2654–2662) | Mũ #262a33 dưới điện ra đen xanh, chìm vào lòng vòm tối phía sau → vài khung tưởng mất mũ. Không phải lỗi dữ liệu. | ghi nhận | `reports/m2/cong6/w2/ra-continuity/s40w_mu.jpg` |
| N17 | s37b, s39 (CU) | toàn shot | Tóc bạc trên đỉnh đầu (mũ đẩy ra sau) có vân sọc đều, dễ đọc thành mũ len xám dưới mũ phớt; búi đọc như cuộn len. | ghi nhận (Cổng 7/kiểm mù) | `reports/m2/cong6/w2/bang-khung_s37b.jpg`, `bang-khung_s39.jpg` |
| N18 | s45c | 132,0–133,5 s | Vạch và kim đồng hồ quảng trường ra hồng nâu do quầng sáng; world-rules: "12 vạch đen, hai kim đen". Giờ đúng 10:00. | ghi nhận | thumbs `s45c_a/b/c` |
| N19 | s48 | 135,5–138 s | Bóng chim chạm sát bóng đầu (dính mép phải), chưa tách rõ như continuity ghi "chim tách khỏi bóng đầu". | ghi nhận | thumbs `s48_a/b` |
| N20 | s40 | 107,4 s | Băng mũ có một nút tròn nhỏ bên hông (thấy rõ ở s40). Model sheet cấm nơ, không nói nút; kiểm lại có trong tài sản khoá hay không. | ghi nhận | `reports/m2/cong6/w2/bang-khung_s40.jpg` |

**Tổng: chặn 1 · nên sửa 9 · ghi nhận 10.**

## 2. Các mục rà theo lệnh

### 2.1 Liên tục qua cắt (thứ tự dựng)
| Nối | Kết quả |
|---|---|
| s24c → s25 | chưa kiểm (không có ảnh s24c) |
| s25 → s26 → s27 → s28 → s29 | Khớp: Cas quay vào tường, chim bóng tan ở s27 (cột sân bật), s28 không còn bóng, s29 hạ tay → quay trái khung về Ida. N11 (s26 ánh mắt). |
| s29 → s30 → s31 → s32 | Khớp vị trí Ida TRÁI / Cas PHẢI; quỳ, đèn trong tay, mũ hat_back 0. N7 (đèn hông s30). |
| s32 → s33 → s34 → s35 | Đèn xuống nền hốc (cắt nén) khớp; Ida trái, Cas phải. N6 (G11). |
| s35 → s36 → s37 → s37b → s37w | Đèn hông trái sáng, bà trên thang; mũ đẩy ở s36 và giữ 0,35; nền tối trước P5 (99,2), trắng sau. N12. |
| s37w → s39 → s38 → s40 → s40w | L11 cháy tới 109,2 rồi kính tối đục (s40 n43, s40w, s41). N1, N4. |
| s40w → s41 → s42a | N2, N3. s41 → s42a khớp (Ida trái không đèn, Cas phải ôm đèn sáng). |
| s42a → s42b → s42 | Đèn đặt xuống nền đúng chỗ mở s42; Cas quay ra vòm. N5, N15. |
| s42 → s43 → s44 → s45 → s46 → s45c → s47 → s48 | Mũ kéo lại cuối s42, cảnh 6 giữ 0; không đèn lồng trên người Ida; giờ chỉ tiến. N9, N10, N18, N19. |

### 2.2 Đạo cụ, trạng thái
- **Đèn lồng:** hông trái (s25–s30 đầu; N7 không thấy sáng) → tay (s30–s32) → nền hốc (s33–s34) → hông trái sáng (s35–s40w) → tay phải (s40w cuối, N2) → Cas (s41–s42) → bậu cửa (s44, s48). Ida không còn đèn ở cảnh 6: **đạt**.
- **L11:** sáng tới 109,19 s; tối đục từ 109,20 (s40 n43), s40w, s41: **đạt**. **P5:** tắt ở cảnh 4 và s33–s37b; bật trong s37w (99,2): **đạt** (khớp nền tối s37/s37b, nền trắng s39/s38/s40).
- **Thang:** tựa L11 suốt cảnh 4–5 (s27, s35, s37w, s40w, s41, s42a); ngõ: tựa vách phải s44 (G13), vác ở s47 (N9).
- **Đồng hồ và giờ trên mặt số:** s45 chỉ thấy vỏ (N10); s46 9:53 → ≈ 9:59 → 10:00 (a/b/c), kim chỉ tiến; s45c 10:00:00 → 10:00:01. **Chỉ tiến: đạt.**
- **Mũ (G2):** xem mục 3.

### 2.3 Trục 180° và hướng màn hình
- Cảnh 4: Ida TRÁI, Cas PHẢI ở s27, s30, s31, s32: **đạt**; s29 Cas nhìn trái khung: **đạt**.
- Cảnh 5 (Đ6): Ida nhìn TRÁI khung ở s36, s37, s37b, s39, s40 và s37w/s40w: **đạt về hướng**; nhưng hệ quả ánh mắt với Cas ở s39 → s38 hỏng (N4). s33, s34, s41, s42a, s42: Ida TRÁI, Cas PHẢI: **đạt**; s40w cuối lật thứ tự (N2).
- **s42a ánh mắt xuống Cas:** bà cúi rõ, mặt và mắt hướng xuống về phía đèn trong tay Cas (113,5–115,46 s): **đạt** (`bang-khung_s42a.jpg`).
- Cảnh 6: s45 cuối nhìn phải khung về miệng ngõ → s47 đi ra miệng ngõ: **đạt**.

### 2.4 PA1 s36–s39
| Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|
| Không cận mặt chính diện ở cao trào | **Đạt**: s36 3/4 ≈ 60°, s37/s37b/s39 nghiêng hoàn toàn | thumbs s36–s39, bảng khung s37b, s39 |
| Van đồng không lộ "mẩu tay" | **Đạt ở s36, s37, s39; chưa đạt ở s37b** (N8) | `s36c_s37_tay.jpg`, `s37b_tay_van.jpg` |
| Câu cuối L4 bắt đầu trên hình Ida, cắt sang Cas 106,0 | **Đạt theo hình và bảng thời gian**: "Just…" nằm trong s39 (nhãn 102,60), "ones" ở khung cuối s39 105,97; s38 t0 = 106,0 (`timing_s39.json`, `timing_…s38…json`). Chưa nghe được tiếng (mp4 không tiếng). | `bang-khung_s39.jpg` |

### 2.5 s40 — mặt chìm tối lúc L11 tắt (109,2)
**Chưa đạt** — N1 (mặt đã quay khỏi hình từ 108,94 s, sớm 6 khung; sau 109,2 gáy vẫn sáng).

## 3. Bảng G / B1

| Mục | Yêu cầu | Kết quả | Bằng chứng |
|---|---|---|---|
| G2 | Mũ không nhảy s39 → s40; hat_back 0,35 liên tục s36 (1,05 s) → s42 (2,2 s); kéo lại cuối s42; cảnh 6 = 0 | **Đạt** | s36_a (0) / s36_c (đẩy); s37b, s39 lộ tóc trán; s40 107,4 vành ngả, tóc lộ trước vành; s42_a → s42_c kéo xuống; s44–s47 mũ thẳng |
| G5 | s44 tay đặt ngực | **Đạt** | `reports/m2/cong6/w2/ra-continuity/canh6_zoom.jpg` (s44) |
| G6 | s45 tay trái không tách đồng hồ | **Đạt** (tay trái đỡ dưới); dáng tay xoè cứng (N10) | `bang-khung_s45.jpg` |
| G10 | Ida xuống thang trong s40w, lối xuống không vướng Cas | **Đạt một phần**: có xuống trong shot, Cas ở cạnh phía đông; dáng đọc như rơi, chồng hình với Cas (N3), cuối shot lật vị trí sang s41 (N2) | `s40w_xuong_thang.jpg`, `noi_s40w_s41.jpg` |
| G11 | s32 → s33 quỳ → đứng (0–0,6 s) | **Chưa đạt trên hình** (N6) | `s33_dau.jpg` |
| G13 | Thang trong ngõ s44 trước khi vác s47 | **Đạt** (thang tựa vách phải s44; s45 ngoài khung; s47 vác) — cách vác lệch model sheet (N9) | thumbs s44, s47 |
| B1 cảnh 6 | s45 rõ hướng mặt, hướng đầu, đồng hồ trong tay; giữ s45 → s46 → s45c | **Đạt một phần**: hướng mặt (cúi nhìn tay → quay phải về miệng ngõ) rõ; đồng hồ khuất 0–1,0 s (N10); thứ tự s45 → s46 → s45c giữ, giờ chỉ tiến | `bang-khung_s45.jpg`, thumbs s46, s45c |

## 4. Tờ so nhân vật với model sheet (bằng mắt, thay C3 ở shot máy không đo được)

Chuẩn: Ida `ida.json` (6,27 H; mũ phớt #262a33 không nơ; khăn #8e5c5a cao 4 vòng, một đuôi trước ngực; áo khoác dài #3f5552 cổ bẻ thấp; váy #4a3a44; tóc bạc, búi 1,3×; hoa tai; đèn hông trái; thang vai phải 28°). Cas `cas.json` (5,0 H; mũ len kem #d6c9ae quả bông #a8483a; áo len #8a4a3c cổ lật cao, gấu 2,17 H; quần #3a3d48 ống thẳng; tai vểnh; tay MPFB).

| Shot | Ai | Tỷ lệ đầu/thân/tay | Trang phục | Lệch thấy được |
|---|---|---|---|---|
| s25, s28 | Cas (sau lưng) | Không đo được (sau lưng, tay giơ) | Mũ quả bông, áo len đỏ, quần tối: đúng | — |
| s26 | Ida MS | Đầu/vai hợp lý | Mũ không nơ, khăn 4 vòng + đuôi trước ngực, hoa tai, áo xanh: đúng. Khăn ra đỏ cam bão hoà dưới lửa khí (so #8e5c5a) — do ánh sáng | N11 |
| s27, s35, s37w, s40w, s41 | Hai người WS | Nhỏ (< 60 px), không đánh giá được | Nhận ra được mũ phớt / mũ quả bông | — |
| s29 | Cas MCU | Đầu–cổ–vai đúng tỷ lệ MPFB | **Cổ lật cao rõ**, tai vểnh, tóc gáy nâu: đúng | — |
| s30, s32 | Hai người MS | Cas 5 H hợp lý; Ida quỳ | Quần Cas ống thẳng, gấu áo len qua cạp: đúng; áo Ida ra vàng xanh dưới đèn lồng (ánh sáng) | — |
| s31 | Ida MCU | — | Mũ, tóc bạc thái dương, khăn 4 vòng: đúng | — |
| s33, s34 | Hai người (bóng) | Bóng ×1,94 / ×1,36 như continuity | Mũ phớt, mũ quả bông in trên bóng: đúng | — |
| s36, s37, s37b, s39 | Ida CU nghiêng | Đầu MPFB, tai, búi 1,3×: đúng | Hoa tai, khăn 4 vòng: đúng; tóc đỉnh đầu đọc như len (N17) | N8, N17 |
| s38 | Cas MS cao | Đầu to hơn do máy hất xuống (phối cảnh), không phải lệch sheet | Cổ lật cao, quần ống thẳng: đúng | — |
| s40 | Ida CU insert | — | Mũ ngả, tóc bạc, khăn: đúng; nút trên băng mũ (N20) | N20 |
| s42a | Hai người MS toàn thân | Ida ≈ 6,3 H, thẳng lưng; Cas ≈ 5 H, đầu ≈ 1/5 chiều cao: khớp sheet | Váy dài lộ dưới vạt áo, gấu cách đất: đúng; Cas quần ống thẳng, gấu cách mắt cá: đúng | — |
| s42b, s42 | Cas (ngược sáng) | Bóng người tối, mũ quả bông in rõ | — | N15 |
| s44, s47 | Ida WS | Toàn thân đúng khối chữ A | Mũ, khăn, áo dài: đúng; thang vác sai kiểu (N9) | N9 |
| s45 | Ida MS | Tay MPFB 1,15× hơi to so với đầu ở khung 127,0 (phối cảnh máy thấp gần tay) | Mũ, khăn, hoa tai, búi: đúng | N10 |
| s48 | Cas (sau lưng) | Tay giơ cao, không đo được | Mũ quả bông, áo len: đúng | N19 |

Không thấy lệch tỷ lệ đầu/thân/tay rõ ràng so với sheet ở shot nào; C3 bằng máy vẫn cần P chạy (BAO-CAO R6).

## 5. Việc đang chờ
- **Chủ dự án:** chấp nhận hay yêu cầu sửa N1 (lệch 6 khung ở mốc cố định 109,2); Đ6 (phía máy PA1) quyết định cách sửa N4.
- **P:** chép báo cáo sang `shots/layout/continuity/RA-W2-V1.md` nếu cần; giao W2 vòng 2 các mục nên sửa; lấy ảnh s24c để kiểm chỗ nối W1 → s25; kiểm tiếng câu cuối L4 trên bản ghép.
