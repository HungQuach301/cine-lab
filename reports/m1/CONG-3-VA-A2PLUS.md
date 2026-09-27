# CỔNG 3 — ĐỢT VÁ A2+ (chốt thiết kế) · "Last Round"

Phiên P, 27/09/2026. Nhánh `claude/cine-lab-m1-cong3-v3`, **chưa merge vào main**. `scripts/env/verify.sh`: 10 PASS, 0 FAIL. Không sửa `checks/`, không đọc mã trong `checks/`.
Mọi số là đo thật. Thời gian đo tuần tự trên máy rỗi. Đầu ra của đợt vá: `design/cong3/v2/out/a2p/`. Ảnh trước/sau: `reports/m1/cong3-a2p/`.

## 0. Tóm tắt
| Mục | Kết quả |
|---|---|
| V1 khung kết | **Sửa xong**:<br>• mặt tiền vữa/gạch vẽ tay; cửa sổ có khung, song, bậu, lanh tô;<br>• cửa gỗ có bậc; vỉa hè đá phiến có bó vỉa;<br>• cột đèn điện thời kỳ thẳng; mái, ống khói; trời vẽ; sương;<br>• Ida đứng ở miệng ngõ, ngửa nhìn ô vàng |
| V2 mặt đường | **Sửa xong, đã tìm ra nguyên nhân gốc**: UV lấy theo (X, Z) trên mặt phẳng đã xoay nên trục v luôn bằng 0, texture thành sọc "ván gỗ". Đá lát (cobbles) dùng chung cho khung kết, ngõ, khung b và 2 clip đi bộ. Đã thêm một dòng vào luật thế giới |
| V3 ngõ | **Sửa xong**:<br>• trời đêm vẽ, tối đúng tỷ lệ phơi sáng; sương tối làm mái xa tan vào nền, hết "mái lơ lửng";<br>• tường có chất liệu, vách cao bằng mái; ống thoát nước, cửa sau;<br>• cửa sổ nhà Cas có khung và bậu |
| V4 đèn khí | **Sửa xong**: đạo cụ chi tiết (khung 4 trụ, 4 kính hình thang, nắp chóp, van đồng có tay gạt, thanh móc thang, bệ bát giác). Trang bible `bible/props/gas-lamp.md` có ảnh và kích thước. Một xấp xỉ về bóng đổ được ghi rõ (mục 4) |
| V5 mặt Ida | **Một phần**:<br>• tuổi và giới đạt: 3/3 ảnh đọc là "phụ nữ lớn tuổi", 2 ảnh kèm "chưa chắc";<br>• cảm xúc **chưa đạt**: chấm chặt 1/3 (nghẹn lời đúng; trung tính và cười buồn chỉ đúng một nửa);<br>• vệt tối ở má **vẫn còn** trong cận mặt a_close_ida (bóng khối sau gò má, không phải texture) |
| C3 | Chạy được thật: mặt nạ 4× đúng định dạng, **kiểm toán đạt ở 8/8 file**. Kết luận C3: **TRƯỢT 8/8**, vì tỷ lệ phụ thuộc tư thế và góc nhìn. `walk_cas` gần đạt |
| G3b | **Đạt 8/8** sau khi sửa khâu mã hoá (4 khung tĩnh từng trượt, nay tương quan 0,36–0,39) |
| Thời gian | Mọi khung 2,27–4,18 s; hai clip đi bộ có trung vị 3,47 và 3,35 s (ngân sách ≤ 5 s) |

## 1. Quyết định đã ghi
- `AUTHORSHIP.md` mục "Cổng 3 vòng 3", ghi kèm phương án bị loại:
  - A2+ (loại A1, A2 thuần, A3); B1 (loại B2, B3); C1 (loại C2);
  - duyệt ý tưởng 4 yếu tố sáng tạo;
  - chấp nhận 2 khiếu nại;
  - V1–V5.
- `checks-appeal.md`: cột phán quyết của 2 khiếu nại vòng 3 ghi "Chủ dự án CHẤP NHẬN (chat 27/09/2026); K sửa gộp ở lần mở tới." Không mở phiên K.
- `bible/world-rules.md`: "Mặt phố Ostler và quảng trường: đá lát."
- **Khoá (SHA-256):**
  - `bible/characters.md` v1.1: `ab75ca23c5c39d5507717f6a34497c79f3079bd0347a9a70742f3ee5f0eb59ec`
  - `model-sheet/ida.json`: `05227467…b7342c`
  - `model-sheet/cas.json`: `9b2be222…cd758`
  - `bible/props/gas-lamp.md`: `c13911ed…81bfb1`

## 2. V1–V5: số đo và ảnh
| Mã | Việc đã làm | Số đo / kiểm | Ảnh trước/sau |
|---|---|---|---|
| V1 | Bộ phố mới `v2/street.js`:<br>• `facadeTex`: vữa loang, mảng vữa bong lộ gạch (nhạt, thưa), gờ tầng, vệt nước, bẩn chân tường;<br>• `windowUnit`: viền đá, khung gỗ, ray giữa, song 6 ô, bậu, lanh tô; kính vẽ có rèm;<br>• `electricLamp`: bệ bát giác, thân thẳng Ø0,11–0,17, tay treo có giằng, chụp men.<br>Cửa sổ lạnh nhạt #cdd8e3, đúng color script cảnh 6 (#c3ced8), không còn xanh đen. Lớp vẽ giảm lắc nét (wob 3 → 1,2) để cột thẳng. Sương lạnh #a3aec2 (10–95 m) | Render 2,87 s/khung. Ida cao ≈ 24% khung, đứng ở miệng ngõ; ô vàng ở trên trái Ida | `cong3-a2p/V1_khung-ket_truoc-sau.png` |
| V2 | `cobbleTex` (đá granit 0,11–0,17 × 0,10 m, mạch tối, mặt vồng) và `groundPlane` (UV đúng trục). Áp cho khung kết, ngõ, khung b, walk, walk_cas | Kiểm bằng mắt: hết sọc | `V2_duong-da-lat_walk_truoc-sau.png`, `V2_duong-da-lat_ket_200pct.png` |
| V3 | Trời vẽ (`paintedSky`, bảng #121831 → #7d8aa6), trong ngõ ×0,08 để bù phơi sáng ×4; sương #10131f (9–55 m); ánh trời đêm rất yếu (0,12); ánh điện lọt sâu hơn (1,5 m); vách ngõ 7,4 m có gờ | 3,11 s/khung | `V3_ngo_truoc-sau.png` |
| V4 | `shared/props.js` viết lại; trang bible có ảnh (toàn thân và cận lồng) và bảng kích thước | 4,18 s/khung (a_close_ida) | `V4_den-khi_can-mat_truoc-sau.png`, `V4_trang-dao-cu-den-khi.png` |
| V5 | Texture C′ viết lại:<br>• nếp mắt, miệng, trán rõ hơn; môi có hình (mỏng, rộng); mày cong mảnh;<br>• má hồng; tóc bạc ở thái dương; bỏ mảng tím hốc mắt và đốm đồi mồi to;<br>• lớp phát sáng cho catchlight, ánh ướt, nước mắt;<br>• lông mày sợi 3D chuyển động cùng biểu cảm;<br>• gò má hoà mềm, "má hóp" nông lại.<br>Shot kiểm `face_ida`: máy lệch 25° khỏi hướng mặt, đầu ngẩng 12° để mày ra khỏi vành mũ | Mục 3 | `V5_3-bieu-cam.png`, `V5_mat-can_truoc-sau_200pct.png` |

## 3. V5: kiểm mù biểu cảm, nguyên văn
Mỗi lần kiểm dùng 3 subagent **mới, không ngữ cảnh**; mỗi subagent chỉ xem **một** ảnh (tên và thứ tự ảnh đổi mỗi lần). Câu hỏi: "Người này bao nhiêu tuổi, giới tính gì, đang cảm thấy gì?" Toàn văn cả 3 lần nằm ở `reports/m1/cong3-a2p/kiem-mu-mat/lan1–3.md`.

**Lần 3** (sau 2 lần chỉnh, lần cuối được phép):
- **(a) trung tính:** "Ấn tượng đầu tiên: đây là một người phụ nữ lớn tuổi, khoảng 65–75 tuổi. Tôi đoán vậy vì tóc bạc búi phía sau, đeo khuyên tai, mặt có nếp nhăn quanh mắt và miệng. Nét mặt trầm lặng, hơi buồn và man mác: lông mày hơi nhướn lên ở giữa, miệng khép, ánh mắt nhìn xa như đang hồi tưởng hoặc lo âu nhẹ, không thấy vui. / Ghi chú thêm: ánh sáng cam ấm chỉ chiếu lên khuôn mặt, nên cảm xúc đọc được phần lớn nhờ lông mày và ánh mắt, còn miệng gần như trung tính. Vì thế ta có thể đọc là "buồn" hoặc "bình thản đăm chiêu"."
- **(b) cười buồn:** "Ấn tượng đầu tiên: đây là một người phụ nữ lớn tuổi, khoảng 65–75 tuổi (tóc bạc lộ dưới mũ, nếp nhăn sâu từ mũi xuống cằm, có vết chân chim), dù khuôn mặt tròn và nhẵn nên cũng có thể đọc thành một ông già. Bà trông trầm tư, hơi buồn và lo âu một cách lặng lẽ: lông mày nhíu lại, ánh mắt nhìn xuống bàn tay đang giơ ra gần máy quay, môi mím nhẹ như đang kìm cảm xúc hoặc đang ngập ngừng. Ghi chú thêm: phần nửa dưới khuôn mặt khá "chết", đôi mắt hơi trống và nhìn không thật tập trung, nên cảm xúc chủ yếu đến từ lông mày và ánh sáng hơn là từ toàn bộ gương mặt."
- **(c) nghẹn lời:** "Ấn tượng đầu tiên: đây là một người phụ nữ lớn tuổi, khoảng 70–80 tuổi. Tôi nhận ra qua tóc bạc, nếp nhăn sâu ở trán, khoé mắt và quanh miệng. Bà đang lặng người và xúc động: có một giọt nước mắt nhỏ lăn trên má trái, lông mày hơi nhíu, môi mím, ánh mắt nhìn xa xăm. Cảm xúc là buồn và tiếc nhớ, nhưng bà đang cố kìm lại chứ không bật khóc. / Nói thêm: giới tính không hoàn toàn rõ. Mũ và cổ áo khiến khuôn mặt hơi trung tính, nhưng tóc hoa râm búi ra sau tai làm tôi nghiêng về phía nữ. Giọt nước mắt khá mờ, chỉ thấy khi nhìn kỹ."

| Lần | Tuổi/giới (3 ảnh) | Cảm xúc đúng (chặt) | Nhận xét chính của người xem |
|---|---|---|---|
| 1 | "bà cụ" ×1, "phụ nữ… không rõ hẳn" ×1, "không rõ, nghiêng nữ" ×1 | 0–1/3 | mắt "búp bê" thiếu catchlight; cười buồn đọc thành "ngạc nhiên" |
| 2 | tuổi đúng 3/3; giới "nghiêng nữ, chưa chắc" 3/3 | 1/3 (nghẹn lời) | môi đọc thành "chúm như sắp nói 'ô'" |
| 3 | **"phụ nữ lớn tuổi" 3/3** (2 ảnh kèm "chưa chắc") | **1/3** (nghẹn lời); trung tính và cười buồn đúng một nửa | nửa dưới mặt "chết", cảm xúc chủ yếu từ lông mày |

**Kết luận: CHƯA ĐẠT** (cần ≥ 2/3 cảm xúc đúng). Nguyên nhân gốc: C′ vẽ biểu cảm lên một khối đầu **không biến dạng**. Miệng, má và cằm không đổi hình, nên nụ cười không nâng má, mím môi không đổi khối. Mũ phớt vành rộng (thiết kế đã duyệt) che mày và làm giới tính trung tính. Đây là quyết định C bên dưới.

Vệt tối ở má (V5): ở ba khung kiểm biểu cảm không còn đốm đồi mồi hay mảng tím. Nhưng ở a_close_ida (góc nghiêng), **vẫn còn một mảng bóng tối** sau gò má. Đó là bóng khối (mặt quay khỏi đèn) bị grade vùng tối của shot nhuộm tím (`gShadowTint`). Chưa sửa, vì sửa grade phải đổi `page.js`, làm hỏng SHA kiểm toán của cả 8 file. Đề xuất ở quyết định C.

## 4. Đèn khí (V4): ghi chú kỹ thuật
Khi lồng đèn đổ bóng thật, 3 mẫu jitter/khung tạo các khối nêm có bậc trên tường (đo ở walk, ảnh nháp trong phiên). Em đã thử lọc mép bóng (`shadow.radius`), nhưng không có tác dụng với đèn điểm. **Xấp xỉ đang dùng:** phần lồng (trên đáy lồng) không đổ bóng; chỉ cột và bệ đổ bóng. Hệ quả là mất vùng tối mềm phía trên nắp (ngoài đời có). Đã ghi trong trang đạo cụ để xử lý khi tăng mẫu. Kèm theo, em sửa lỗi `addLamp` ghi đè cờ bóng của đạo cụ.

## 5. C3: B1 và kết quả máy
**B1** (`characters.md` v1.1, sheet `c3_views`):
- Đo mặt nạ bộ phận **nhìn thấy** trên lưới 3D đã duyệt, tư thế turnaround, máy trực giao, 4 góc (0°, 45°, 90°, −90°), theo đúng định nghĩa C3 (trục chính PCA). Số ghi vào sheet là góc 0°:

  | Bộ phận | Ida | Cas |
  |---|---|---|
  | thân | 2,584 | 1,669 |
  | cánh tay trên | 1,550 | — |
  | cẳng tay | 0,963 | 0,945 |
  | đùi | — | 1,191 |
  | cẳng chân | — | 1,132 |

- Bỏ khỏi `measured_parts` những bộ phận bị che theo thiết kế:
  - Ida: đùi, cẳng chân (váy dài + áo khoác);
  - Cas: cánh tay trên (áo len rộng; đo được 0,21–0,63 tuỳ góc).
- Khung xương `parts{}` giữ nguyên.
- Tỷ lệ phụ thuộc góc nhìn: thân Ida đo được 2,15–2,58 tuỳ góc.

**Bộ xuất mặt nạ đã sửa**: ngoài bộ phận để alpha = 0. Đã kiểm: số điểm alpha ≥ 128 bằng đúng số điểm xám ≥ 128.

**Kiểm toán**: `audit.py issue` phát cho 8 file mới. Mặt nạ được render lại đúng các khung máy chọn, bằng đúng lệnh, và `render.log` được ghi. Kết quả: SHA file cảnh khớp (True), khác điểm ảnh 0, lệch tỷ lệ 0·U, **8/8**.

**C3: TRƯỢT 8/8** (nguyên văn máy, độ lệch từng bộ phận so với sheet B1):

| File | Đầu (px) | Lệch |
|---|---|---|
| a_close_ida | 372 | thân −43,6% · tay trên −10,6% · cẳng tay +55,9% (tay gập về đèn, phối cảnh) |
| b_cas_bird | 132 | thân +13,6% · cẳng tay −2,5% (không chứng minh được) · đùi −6,8% · cẳng chân −64,6% (nhìn sau lưng, chân khuất) |
| c_s5_wide | **13** | thân +126% · tay +85% · cẳng tay +166% (đầu quá nhỏ) |
| c_s5_medium | 124 | thân +3,1% (không chứng minh được) · tay trên −50,1% · cẳng tay: thiếu mặt nạ |
| d_s6_alley | 48 | thân −9,2% · tay trên −12,8% · cẳng tay +37,1% |
| e_ending | 30 | thân +2,1%, tay trên −2,2% (không chứng minh được) · cẳng tay +20,2% |
| walk | 43–44 | thân −13…−16% · tay trên −6…−8% · cẳng tay +5…+29% (góc nghiêng) |
| walk_cas | 44–46 | **thân −0,2…+4,0% · cẳng tay −0,9…+3,1% · đùi −6,8…+0,7% · cẳng chân −0,5…+4,1% (đa số đạt)**; 1 lần lệch chắc chắn, 6 lần không chứng minh được; độ khớp biên 1,473 (ngưỡng 1,5, **trong ±5%**) |

Kết luận: C3 đo độ dài 2D của mặt nạ nhìn thấy, nên đổi theo tư thế (tay gập), góc nhìn (nghiêng, sau lưng), che khuất và cỡ đầu. Ở đúng góc gần tư thế đo (walk_cas), nhân vật khớp sheet trong khoảng 4%. Đây là giới hạn 4 đã ghi trong RULES.md, không phải lỗi dựng hình. Quyết định B bên dưới.

## 6. Luật máy trên mọi file đã render lại (nguyên văn kết luận)
Báo cáo: `design/cong3/v2/out/a2p/check/<file>/`.

| File | Kết luận | N1 | N2 | P0 | P1 | G4 | G3 | G3b | J1 | J1b | H1 | H1b | C3 | O3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a_close_ida | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (0,039) | chờ K | chờ K | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| b_cas_bird | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (0,391) | chờ K | chờ K | ĐẠT | ĐẠT (95,7%) | TRƯỢT | ĐẠT |
| c_s5_wide | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (0,392) | chờ K | chờ K | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| c_s5_medium | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (0,363) | chờ K | chờ K | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| d_s6_alley | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | chờ K | chờ K | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| e_ending | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (0,385) | chờ K | chờ K | ĐẠT | ĐẠT | TRƯỢT | ĐẠT |
| walk | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (0,187) | chờ K | chờ K | ĐẠT | TRƯỢT (48,9%) | TRƯỢT | ĐẠT |
| walk_cas | **TRƯỢT** | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (0,191) | chờ K | chờ K | ĐẠT | TRƯỢT (76,6%) | TRƯỢT | ĐẠT |

Ghi chú bảng:
- **J1/J1b:** máy in "TRƯỢT: không có luồng âm". P ghi "**chờ K (khiếu nại đã chấp nhận)**", không chèn âm im lặng.
- **H1b ở 2 clip đi bộ:** vẫn do track bàn tay, như vòng 3; chưa xử lý trong đợt này.
- **Chỉ số trong ±5% quanh ngưỡng** (máy liệt kê): C3 hệ số mặt nạ = 4 (ngưỡng ≤ 4); C3 độ khớp biên của walk_cas = 1,473 (ngưỡng 1,5).
- **Không chạy lại:** s1_opening (không đổi; C3 của nó vẫn là kết quả vòng 3 với bộ xuất lỗi, không phát lại yêu cầu kiểm toán). Ba ảnh kiểm biểu cảm `face_ida` là ảnh thử thiết kế, không phải shot, nên không chạy luật.

## 7. G3b: khâu mã hoá
Đo trên `c_s5_wide` (24 khung tĩnh), chạy riêng G3b:

| Mã hoá | Tương quan khung kề | σ | CV | Kết quả |
|---|---|---|---|---|
| Lossless (qp 0) | 0,387 | 1,427 | 0,003 | **ĐẠT** — lỗi không nằm ở render |
| 30 Mbps cũ | 0,674 | — | — | TRƯỢT |
| 30 Mbps + tắt pskip | 0,68 | — | — | TRƯỢT |
| Toàn khung I 30 Mbps | — | — | 0,566 | TRƯỢT (σ dao động) |
| Toàn khung I CRF 14 | 0,257 | — | 0,10 | ĐẠT |
| **CRF 12 + no-fast-pskip + deadzone 0 (chọn)** | 0,392 | 1,545 | 0,014 | **ĐẠT**, ≈ 61 Mbps, sát lossless |

Đã áp cho mọi file của đợt vá (`v2/run_a2p.sh`).

## 8. Thời gian render (s/khung, 1920×1080, 3 mẫu)
| Khung | s/khung |
|---|---|
| a_close_ida | 4,18 |
| b_cas_bird | 2,47 |
| c_s5_wide | 2,27 |
| c_s5_medium | 2,97 |
| d_s6_alley | 3,11 |
| e_ending | 2,87 |
| walk (48 khung) | trung vị 3,47, lớn nhất 3,62 |
| walk_cas (48 khung) | trung vị 3,35, lớn nhất 3,52 |
| face_ida (thử biểu cảm) | 4,60–4,90 (**trong ±5% quanh 5 s**) |

## 9. Quyết định cho chủ dự án
**A. "Khoá thiết kế và sang Cổng 4 (animatic) chưa?"**

| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A1. Khoá, sang Cổng 4**; biểu cảm (C) và C3 (B) làm song song trong Cổng 4 | V1–V4 đã sửa; phố, đạo cụ, nhân vật đủ để dựng animatic; biểu cảm vốn phải chấm trên hình động (C1 đã chọn) | V5 cảm xúc chưa đạt; vệt má ở cận nghiêng còn | Animatic đi ngay | Nếu chọn C2 thì rig mặt đổi giữa Cổng 4 |
| A2. Thêm một đợt vá nhỏ cho biểu cảm (C2 bên dưới) rồi mới khoá | Mặt đạt trước khi khoá | Thêm một đợt dựng rig | Trễ Cổng 4 | Thấp–vừa |

**Khuyến nghị: A1 cộng C2 làm như việc đầu tiên của Cổng 4.**

**B. C3 trượt vì tư thế và góc nhìn**

| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **B-i. Khiếu nại C3 lên K**: chỉ đo ở khung có tư thế và góc gần sheet (thẳng người, góc lệch ≤ 30°), hoặc cho model sheet nhiều góc (dùng `c3_views`) | Luật đo đúng điều nó định đo; walk_cas cho thấy nhân vật khớp ±4% | Chờ K ở lần mở tới | C3 có ý nghĩa ở Cổng 4 | K có thể bác |
| B-ii. Giữ luật, chỉ nộp C3 cho shot có tư thế/góc chuẩn (khai `no_character` hoặc không nộp mặt nạ cho shot khác) | Không đổi luật | Gần như lách luật; mất kiểm tra ở phần lớn shot | — | Cao (trái tinh thần luật) |
| B-iii. Chấp nhận C3 TRƯỢT như giới hạn đã biết (RULES.md giới hạn 4) | Không tốn việc | Luật Chặn luôn đỏ | Kết luận mọi shot có nhân vật là TRƯỢT | Che mất lỗi thật |

**Khuyến nghị: B-i.**

**C. Biểu cảm mặt Ida (V5 chưa đạt)**

| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **C2. Thêm biến dạng hình học cho mặt** (vài "blend shape": khoé miệng, má nâng, mày, mí) dưới lớp texture C′ | Giải đúng nguyên nhân gốc (khối mặt không đổi hình); giữ C′ | Việc rig mặt vừa phải | Cần cho animatic và phim | Vừa |
| C3. Chỉ tăng nét vẽ (giữ khối tĩnh) | Rẻ | Đã thử 2 lần: cảm xúc dừng ở 1/3 | — | Cao (không đạt) |
| C4. Nới vành mũ ở cận mặt (hất ra sau) để lộ mày, trán | Tăng đọc biểu cảm và giới | Đổi dáng mũ đã duyệt | Mở lại thiết kế | Thấp |

**Khuyến nghị: C2** (có thể cộng C4 chỉ cho cận mặt). Vệt má ở cận nghiêng: đề xuất giảm sắc tím vùng tối trên da ở grade cận mặt; làm trong đợt render kế tiếp để khỏi phá kiểm toán hiện tại.

## 10. Việc đang chờ chủ dự án
1. Trả lời A, B, C.
2. Duyệt phần thực thi mới của khung kết và ngõ (bố cục đã duyệt; chất liệu, cửa sổ, cột đèn, trời mới làm), và đạo cụ đèn khí (trang bible).
3. Duyệt merge nhánh `claude/cine-lab-m1-cong3-v3` vào main (P chưa merge).
