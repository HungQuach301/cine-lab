# BÁO CÁO W2 — Cổng 6, DIỄN HOẠT cảnh 4–6 (s25 → s48), VÒNG 1

Phiên xưởng W2 · nhánh `cong6-w2-v1` (từ main `4d1134c`) · 29/09/2026 · căn cứ: lệnh giao của P, AUTHORSHIP "Cổng 6 — diễn hoạt".
Phạm vi đã sửa: `design/cong5/layout/shots_w2.js`, `order_w2.js`; `shots/layout/shots_w2.json`, `LAYOUT-W2.md`, `continuity/canh-4.md`, `canh-5.md`, `canh-6.md`; thư mục này.
**Không** sửa: bible, checks (không đọc mã checks), tài sản khoá, mã dùng chung, `sets2.js`/`sets_end.js` (không cần).

## 0. Tóm tắt
- **PA1 dựng xong** (a): s36 3/4 60°, s37 MCU nghiêng 90° (ngọn L11 gốc trong khung), **s37b mới** CU nghiêng 90° đẩy chậm ("Goodnight"), s39 CU nghiêng 96°. Hết cận mặt chính diện ở cao trào. Câu cuối vẫn bắt đầu trên hình Ida, cắt sang Cas ở 106,0.
- **s40** (b): mặt Ida chìm vào bóng tối đúng **109,20** (cúi + quay mặt khỏi máy dưới vành mũ, kính lồng tối đục cùng khung).
- **Mặt + khẩu hình** (c): L3 (s31) và L4 (s37, s37b, s39) bằng 16 kênh + 6 viseme, mốc đo trên tệp take; hai **nhịp cười buồn** có cười, mắt chùng, dừng một nhịp.
- **Cầm nắm** (d): IK tay MPFB cho thanh thang, van/cần van, vòng quai, ngực, đồng hồ. Phát hiện `reachGrip` (dùng chung) trượt dọc trục với vật ngắn → viết `gripAt` (IK tới một điểm) trong `shots_w2.js`.
- **Đứng tự nhiên + continuity** (e): `settle` (dồn trọng tâm, lệch hông, thở); G2, G5, G6/B1, G10, G13 xong; G11 đã có từ Cổng 5.
- Tổng phim **140,5 s** không đổi; W2 = 30 shot, 81,5 s, 1956 khung. Lệch 0 px ngoài phạm vi (s02, s24c): **0/6 ảnh**.

## 1. Bảng việc a–f
| Việc | Trạng thái | Ghi chú |
|---|---|---|
| a. PA1 s36–s39 (profile 90–96°, L11 gốc, CU "Goodnight" đẩy chậm, câu cuối CU nghiêng, bắt đầu trên Ida) | **Đã làm** | Tách s37 → s37 (93,0–96,4) + s37b (96,4–98,8). Giữ id `s37` cho phần đầu vì `common.js` dùng `DIALOGUE.L4 = T0.s37`. |
| a. Van đồng không lộ "mẩu tay" | **Đã làm** | Tay trái MPFB nắm ống khí ngay dưới thân van (IK điểm), lòng tay che thân van. Ở s39 (máy nâng 0,12 m) bàn tay đọc rõ là bàn tay đang nắm (bảng khung s39). |
| b. s40 mặt chìm tối đúng 109,2 | **Đã làm** | Xem §2. |
| c. Khẩu hình L3–L4 + cười buồn + chớp/nhìn/thở | **Đã làm** | Xem §3. Chủ dự án chấm nhịp cười buồn trên clip có tiếng; P ghép tiếng. |
| d. 12 shot cầm nắm | **Đã làm 11/12, 1 một phần** | s42 (áp tay): cậu ngồi xổm không với tới kính — lòng tay còn cách 18–19 cm (Cổng 5: 35–37 cm). Xem §4. |
| d. s41 Cas đứng gần hơn | **Đã làm** | 1,02 → 0,57 m; bà chìa ngắn (khuỷu gập 42°). |
| d. s42a Ida nhìn xuống Cas | **Đã làm** | cổ 24° + thân 4° + nhãn cầu 0,12 rad; bảng khung s42a. |
| e. Đứng tự nhiên | **Đã làm** | Ida s25–s28, s40w cuối, s41, s42a, s42, s44; Cas s29–s32, s35–s40w, s41, s42a. |
| e. B1 cảnh 6 (s45 hướng mặt, đầu, đồng hồ) | **Đã làm** | Đồng hồ hạ ngang ngực, hai tay giữ; mắt cúi vào mặt số rồi dẫn đầu quay về miệng ngõ. s45 → s46 → s45c giữ. |
| e. G2 mũ s39 → s40 | **Đã làm** | hat_back 0,35 liên tục; máy s40 cùng phía với s39. |
| e. G5 s44 tay đặt ngực | **Đã làm** | IK điểm lên ngực (FK cách 0,38 m). |
| e. G6 s45 tay trái | **Đã làm** | Tay trái đỡ dưới đồng hồ (IK). Không áp ở s46: thử v1 lòng tay chắn trọn máy insert (khung tối) → s46 giữ khung đã duyệt. |
| e. G10 Ida xuống thang trong s40w | **Đã làm** | Cas dời cạnh chân thang phía đông để lối xuống trống (Cổng 5 cậu đứng đúng lối trèo). |
| e. G11 s32 → s33 quỳ → đứng | **Đã có** | s33 0–0,6 s đứng dậy từ Cổng 5 v3; không đổi. |
| e. G13 thang trong ngõ s44 | **Đã làm** | Thang tựa vách cửa sổ (phải khung s44), cả s45. |
| e. Khẩu hình câu cuối L4 ở s39 | **Đã làm** | "Just…" 102,32; "keep a little dark for the ones" 103,86–106,0. |
| e. Nhịp "gập đồng hồ" (nắp) | **Chưa — đề xuất** | §6 (Đ4). |
| f. Giữ sai lệch đã chấp nhận, không sửa tài sản khoá, không thêm nguồn sáng | **Giữ** | Không có shot cận tay Cas mới (s38 MS; s41 WS). Không thêm/bớt đèn nào. |

## 2. s40 — mốc 109,2 s (quyết định cố định)
- Máy phía phố (+x) ngang lồng đèn, 50 mm: cần van ở tiền cảnh, lồng + lửa, mặt bà **nghiêng ≈ 90°** bên phải lồng, chỉ được ngọn lửa rọi (không chính diện).
- 107,7–108,3: tay trái nắm cần van (IK điểm, cách mặt cần −2,3 mm), gạt; 108,32–108,72 buông về tư thế nghỉ.
- **108,75 → 109,20**: cúi 30°, quay mặt 72° khỏi máy, thân xoay 14°; xong **đúng 109,20** = `L11_OFF` — cùng khung lửa tắt và kính lồng chuyển tối đục (`endStreet`). Từ 109,2 trên hình chỉ còn vành mũ, búi tóc, tai (bảng khung `bang-khung_s40.jpg`: 108,90 mặt còn nghiêng một nửa; 109,40 không còn mặt).
- Không đổi đèn: trắng tràn (P5) vẫn phẳng như cũ; "chìm vào bóng tối" dựng bằng diễn + máy (điện phẳng không đổ bóng — luật thế giới — nên không thể làm mặt tối bằng ánh sáng mà không thêm/bớt nguồn).

## 3. Mặt, khẩu hình, cười buồn
- **Mốc thoại** đo trên chính tệp take đã duyệt (`reports/m1/cong2/tableread-d2/lines/L3.mp3`, `L4.mp3`): bao năng lượng −38 dB so với đỉnh + onset librosa + faster-whisper small.en (mốc từ); mix.py cắt đầu tệp 0,000 s nên giây phim = mốc thoại + giây trong tệp.
  L4: "That's the last one, then." 93,09–95,01 · "Goodnight, old street." 96,55–98,06 · "You'll be brighter now." 99,54–100,97 · "Just…" 102,32–102,88 · "keep a little dark for the ones who need it." 103,86–107,07 (cắt sang Cas 106,00 giữa "ones / who"). L3 "Go on, then." 74,04–76,05 (lời 74,05–75,25).
  Lưu ý cho P: bảng W3 cũ ghi "That's the last one, then." 93,0–96,0 — số đo lại ở đây là 93,09–95,01.
- **Khẩu hình**: chuỗi viseme theo từng từ (A/E/O/MBP/FV/L), miệng đi trước tiếng 0,04 s, khép về nghỉ ở khoảng lặng > 0,25 s, biên độ 0,7 (L3 0,65).
- **Cười buồn** (95,0–96,4 và 98,1–98,8): smile 0,8–0,9, cheekRaise 0,3, squint 0,1 (thấp để mắt không híp "cười tươi" và không thành khe ở góc nghiêng — lời chê MAT-IDA-BLENDER-L3), browInnerUp 0,7, browKnit 0,2, lidDrop 0,38–0,45, nhãn cầu cúi 0,22–0,26 rad, cúi đầu 6–7°, chớp chậm (×2,2) ở 95,75. Bảng khung `s37`, `s37b` có nhãn lời.
- **Vế cuối** (s39): nghẹn (frown 0,7, browInnerUp 1,0, chinRaise 0,5, lidDrop 0,3), cúi 12° nhìn xuống Cas; nuốt 103,2–103,6; chớp chậm 103,45 và 105,6.
- Chớp mắt Ida PA1: 91,75 · 92,75 · 95,75 (chậm) · 97,2 · 99,4 · 100,8 · 101,95 · 103,45 (chậm) · 105,35. Cas s38 chớp 106,62; s42a 114,1 và 114,95.
- **Chưa làm**: giọt nước mắt s39 (không có tài sản/shader — đề xuất Đ5).

## 4. Cầm nắm — tâm lòng tay → vật (trước = tư thế FK layout với tay MPFB; sau = IK). Đo mỗi 12 khung bằng `--meta-only` + log.
| Shot | Tay · vật | Trước (m) | Sau (m) | Ghi chú |
|---|---|---|---|---|
| s25, s27, s28 | Cas · chim bóng (không vật) | tâm lòng tay cao 1,216 m, cách tường 0,81 m | 1,241–1,244 m; 0,79–0,80 m | bù 6,4 cm lệch tay MPFB: vai +8°, khuỷu +14° |
| s32 | Cas · chim (birdReach) | — | lòng tay 0,99–1,00 m, cách tường 0,39–0,41 m (giữa đèn 0,6 m và tường) | không bù (hình học đèn–tay giữ) |
| s37w, s38, s40w (đo); s35 3,05–3,6 s cùng hàm | Cas · 2 thanh… 1 thanh thang đông (L 0,74 m, R 1,00 m) | L 0,245–0,259 · R 0,093–0,106 | **−0,0026** cả hai | trụ bán kính 0,018; s40w buông 1,55–1,9 s |
| s36 (1,55–2,0 s), s37, s37b, s39, s37w | Ida · ống khí dưới van | 0,431–0,446 | **−0,0023** | s36 trộn vào nắm |
| s40 | Ida · cần van | 0,466–0,489 | **−0,0023** (tới 108,32) | buông 108,32–108,72 |
| s41 | Cas · vòng quai (2 tay) | 0,34–0,54 (0,25 s) | **−0,0026** từ 0,5 s | trộn 0,35–0,75 s; sau đổi tay đèn theo tay cậu |
| s42a | Cas · vòng quai | 0,056–0,077 | **−0,0026** (IK điểm) | bản `gripRing` Cổng 5: đo tới trục −0,0026 nhưng tới điểm nắm 0,037–0,063 (trượt dọc tiếp tuyến) |
| s42b | Cas · vòng quai | 0,057–0,072 | **−0,0026** tới 1,5 s; 1,75 s: 0,025/0,039 (với xuống nền) | buông 1,75–2,0 s |
| s42 | Cas · mặt kính (hơ tay, 4 cm) | 0,350–0,371 | **0,182–0,190** ở đỉnh nhịp | **chưa đạt**: ngồi xổm không với tới đèn cách 0,55 m (Đ3) |
| s44 | Ida · ngực | 0,381 | **−0,0023** | G5 |
| s45 | Ida · đồng hồ (đỡ dưới) | 0,384–0,388 | 0,008 → 0,030 (khi quay vai) | G6 |
| s48 | Cas · chim cao (không vật) | — | lòng tay cao 1,257 m, z −0,36 | trang thử W4T2 lỗi; nay đo được; không bù |
Giá trị âm −0,0023/−0,0026 = lòng tay úp sát mặt vật (−0,002 × tỉ lệ tay 1,15/1,30, theo thuật toán reachGrip).

## 5. Thời lượng từng shot (khung render thật, 24 fps)
s25 72 · s26 48 · s27 72 · s28 48 · s29 72 · s30 48 · s31 72 · s32 72 · s33 120 · s34 48 · s35 96 · s36 48 · **s37 82 (93,0–96,4)** · **s37b 57 (96,4–98,8)** · s37w 67 · s39 106 · s38 34 · s40 62 · s40w 48 · s41 36 · s42a 48 · s42b 48 · s42 72 · s43 96 · s44 60 · s45 48 · s46 72 · s45c 36 · s47 48 · s48 120 = **1956 khung, 81,5 s**; tổng phim **140,5 s** (không lệch).
Mốc giữ: L3 74,0 · L4 93,0 · P5 99,2 · VALVE 107,7 · **L11_OFF 109,2** · cắt s39 → s38 106,0.

## 6. Đề xuất (P chuyển chủ dự án / P tự xử lý mã dùng chung) — W2 không tự làm
- **Đ1 — `cast3d.reachGrip` (mã dùng chung):** chiếu điểm nắm lên đường trục vô hạn → với vật ngắn tay trượt khỏi vật; giá trị trả về chỉ đo tới đường trục nên báo "chạm" sai (s40: trả −2,3 mm trong khi lòng tay cách cần 0,18 m). Diff đề xuất:
  `const Cp = C0.clone().addScaledVector(A, G.clone().sub(C0).dot(A));` → `const Cp = g.fixed ? C0.clone() : C0.clone().addScaledVector(A, G.clone().sub(C0).dot(A));` và ở cuối trả `g.fixed ? ch.gripPoint(s).distanceTo(C0) - g.radius : …`. Ưu: W1/W2 bỏ bản sao `gripAt`. Nhược: đụng tài sản mã khoá (P quyết).
- **Đ2 — `audio/mix.py` (P):** bảng mức rè điện `LV` chưa có `'s37b'` → 96,4–98,8 rè điện = 0 (lỗ nền). Thêm `'s37b': 0.3`. Nếu có mã khác đọc bảng shot theo id (luật, SHOTLIST) cần thêm s37b.
- **Đ3 — s42 áp tay:** dời đèn lồng từ 0,55 m về 0,38 m trước mặt Cas (s42b + s42 cùng đổi, trong phạm vi W2) để lòng tay chạm được kính. Chờ duyệt vì đổi hình đã duyệt V1 (khung sau lưng).
- **Đ4 — nắp đồng hồ ("gập đồng hồ", bible):** `buildWatch` ở `sets.js` (ngoài phạm vi). Có thể dựng nắp bản lề trong `shots_w2.js`, gập ở s46 2,75–2,9 s; nhưng sẽ rút nhịp giữ 10:00 đã duyệt (2,2–3,0 s). Chủ dự án chọn: (a) gập ở s46 cuối; (b) gập ngoài hình; (c) sửa bible bỏ nhịp.
- **Đ5 — giọt nước mắt s39:** chưa có tài sản; cần quyết có làm không (Cổng 7/8).
- **Đ6 — Hướng máy PA1 phía phố (+x):** W3 thử PA1 ở phía −x (bà nhìn phải khung). W2 chọn +x để giữ trục 180° và hướng màn hình với s37w/s38/s40w (bà nhìn TRÁI khung ở mọi shot cảnh 5). Ghi để chủ dự án xác nhận.

## 7. Rủi ro
- R1: nhịp cười buồn trên khung tĩnh có thể vẫn đọc "cười ấm" (như L3 kiểm mù) — phải chấm trên clip có tiếng (chủ dự án) và kiểm mù bảng khung (P/K).
- R2: s37 MCU tối (phơi sáng theo facelight × 2,2); mặt ≈ 60 px chiều cao ở 960 px. Nếu kiểm mù không đọc được nụ cười ở s37, đổi sang CU như s37b (vòng 2).
- R3: s41 WS 28 mm nhân vật nhỏ — động tác trao đọc được nhưng tay khó thấy (không đổi máy vì ngoài lệnh).
- R4: `settle` nghiêng chậu nhưng không ghim bàn chân: chân đứng dịch ≤ 1 cm (không đo được trên hình 960 px).
- R5: IK nắm cần 4 vòng lặp cập nhật tay MPFB → render chậm: s41 19,3 s/khung, s42b 11,1, s31 9,6, s35 7,3 (máy dùng chung).
- R6: C3 (luật sheet) đo trên tư thế đã IK — chưa chạy (P chạy luật).

## 8. Render và bảng khung
- MP4 (960×540, không tiếng) trong `/var/tmp/cine-out/W2/` — **bản hiện hành theo shot**:
  - cảnh 4: `video_s25-s26-s27-s28-s29-s30-s31-s32.mp4`
  - cảnh 5: `video_s33-s34-s35-s37w-s38-s40w.mp4`; `video_s36-s37-s37b-s39-s40.mp4` (**dùng s36, s37, s37b**; s39, s40 trong tệp này là bản cũ) → `video_s39.mp4`, `video_s40.mp4` (bản hiện hành); `video_s41-s42a-s42b-s42.mp4` (s42a cũ) → `video_s42a.mp4`
  - cảnh 6: `video_s43-s44-s45-s46-s45c-s47-s48.mp4` (s45, s46 cũ) → `video_s45-s46.mp4`
  - `timing_*.json` cạnh mỗi mp4; `shots/<id>.timing.json`, `thumbs/<id>_{a,b,c}.jpg` là bản cuối của mỗi shot.
- Bảng khung mỗi 0,5 s (nhãn giây phim + lời): `reports/m2/cong6/w2/bang-khung_{s36,s37,s37b,s39,s40,s41,s42a,s45,s46}.jpg` (mỗi tệp < 200 KB).
- Lệch 0 px ngoài phạm vi: gốc `/var/tmp/cine-out/W2/lech0/goc`, sau `…/sau` — **6 ảnh; lệch 0**.

## 9. Token, thời gian, chỉ số sát ngưỡng
- Thời gian thật: 12:52 → ≈ 20:35 UTC 29/09/2026 (≈ 7,7 giờ, trong đó container khởi động lại ≈ 13:34 → 16:46 làm mất lượt render đầu; render lại nhóm 16:49 → 19:00 + render lẻ s39, s40, s45–s46, s42a — s42a render lại 2 lần: lần đầu hỏng vì chú thích `//` nuốt nửa dòng mã, `node --check` trên tệp .js không bắt được lỗi mô-đun; sửa ở 5b6… xem git log).
- Token: công cụ báo ≈ 495 nghìn ngữ cảnh tích luỹ khi viết báo cáo (hạn vòng 1 ≈ 900 nghìn).
- Chỉ số sát ngưỡng ±5 %: không chạy luật (P chạy). Tổng phim 140,5 s đúng mốc (ngưỡng ±5 s).

## 10. Việc còn lại / chờ chủ dự án
- Chấm nhịp cười buồn trên clip có tiếng (P ghép tiếng + phụ đề).
- Duyệt Đ3 (dời đèn s42), Đ4 (nắp đồng hồ), Đ5 (nước mắt), Đ6 (phía máy PA1).
- P: Đ1, Đ2; chạy luật + kiểm mù (10 khung) trên bản ghép.
