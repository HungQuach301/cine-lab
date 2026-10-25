# Khiếu nại luật kiểm (phiên xưởng ghi; chủ dự án phán quyết ở cuối mốc)
| Thời điểm | Mã luật | Lý do cho rằng luật đo sai | Bằng chứng | Phán quyết |
|---|---|---|---|---|

| 2026-09-27 (P, table read Cổng 2) | J1 | Từ ghép "goodnight": ASR viết "Good night", bị tính 1 thay + 1 chèn. Câu do chủ dự án chốt nguyên văn. Đề nghị coi biến thể ghép/tách là cùng một từ (goodnight = good night). Đã gặp ở M0 | `reports/m1/cong2/tableread/checks/` (J1 TRƯỢT: 94,87% từ, WER 10,26%). P không sửa thoại hay audio để lách | **Chủ dự án CHẤP NHẬN** (chat 27/09/2026). **Đã sửa ở checks v1.2** (LOCK 0196187b7af0…): J1 chuẩn hoá từ ghép/tách theo bảng COMPOUND (goodnight = good night…), áp cho cả kịch bản và bản nghe; ngưỡng không đổi. Selftest: SẠCH trên chính table read này; "good" thay cho "goodnight" vẫn TRƯỢT |
| 2026-09-27 (P, table read Cổng 2) | J1 | Chèn "you" trong đoạn im lặng số tuyệt đối (30,0–32,06 s, audio toàn 0): Whisper bịa chữ. Đề nghị bỏ đoạn ASR nằm trong vùng RMS < −60 dBFS hoặc bật VAD trước khi tính chèn. Bản mix thật có room tone nên có thể tự hết | `reports/m1/cong2/tableread/checks/` (J1 TRƯỢT: 94,87% từ, WER 10,26%). P không sửa thoại hay audio để lách | **Chủ dự án CHẤP NHẬN** (chat 27/09/2026). **Đã sửa ở checks v1.2** (LOCK 0196187b7af0…): chữ ASR nằm hoàn toàn trong im lặng số (RMS 50 ms < −60 dBFS) bị bỏ trước khi tính chèn, liệt kê trong báo cáo (bản này: "you" 56,8–58,2 s theo mốc chữ). Bản mix có room tone trên −60 dBFS thì không được bỏ. Selftest: xoá "Warm" thành 0 tuyệt đối vẫn TRƯỢT (thiếu từ thật) |
| 2026-09-27 (P, table read Cổng 2) | J1 | "warm" (L5, bắt đầu 139,5 s) bị tính mất. ASR riêng trên `lines/L5.mp3` nghe đủ "Warm" (p 0,84). Trong bản ghép, từ này rơi ở ranh giới đoạn giải mã 139,84 s. Đề nghị kiểm cách cắt đoạn, hoặc đánh giá chéo từng câu | `reports/m1/cong2/tableread/checks/` (J1 TRƯỢT: 94,87% từ, WER 10,26%). P không sửa thoại hay audio để lách | **Chủ dự án CHẤP NHẬN** (chat 27/09/2026). **Đã sửa ở checks v1.2** (LOCK 0196187b7af0…): J1 kiểm theo từng câu (cửa sổ theo căn kịch bản, ASR riêng từng câu); "warm" nay nghe đúng (câu 5, cửa sổ 137,53–144,34 s). Chữ ngoài mọi câu vẫn tính chèn. Selftest: kịch bản thiếu một câu có thật trong audio vẫn TRƯỢT |
| 2026-09-27 (P, Cổng 3 v3) | J1, J1b | Clip thiết kế không có luồng âm (khung phong cách, chưa làm âm) và `X.script.txt` rỗng (không lời) bị **TRƯỢT** "Không có luồng âm", trong khi M3 cùng điều kiện cho "—" (không áp). Không có từ bắt buộc nào để nghe; không có câu thoại nào để đo SII. Đề nghị: không có luồng âm + kịch bản rỗng → "—" (hoặc THIẾU nếu có kịch bản), thống nhất với M3. P **không** chèn luồng âm im lặng để qua luật | `design/cong3/v2/out/check/*/`: 9/9 file TRƯỢT J1 và J1b với ghi chú "Không có luồng âm"; M3 của cùng file: "—" | **Chủ dự án CHẤP NHẬN** (chat 27/09/2026). **Đã sửa ở checks v1.4** (LOCK 289c6916363f…): file không có luồng âm → kịch bản rỗng: J1, J1b = "—" như M3 (J1b không cần stem); kịch bản có lời hoặc không có kịch bản: THIẾU (không bao giờ ĐẠT). Chạy thử 8 file A2+: J1, J1b TRƯỢT → "—" 8/8. Selftest: "—" ×3 (J1, J1b, run.py không có thư mục stem); THIẾU ×2; có âm nhưng thiếu từ vẫn TRƯỢT |
| 2026-09-27 (P, Cổng 3 v3) | C3 (tài liệu, không phải ngưỡng) | RUN.md 3.6 không mô tả lược đồ model sheet (độ dài bộ phận nằm ở đâu). Sheet của phim lồng độ dài trong `parts{}`; máy đọc ở cấp gốc (như sheet M0) và **dừng với "LỖI ĐO: KeyError: 'torso'"** thay vì báo sai định dạng. Đề nghị K: ghi lược đồ vào RUN.md 3.6, và trả thông báo rõ (THIẾU/sai định dạng) thay vì lỗi Python. P đã thêm bản sao khoá cấp gốc vào sheet (cùng giá trị) | `design/cong3/v2/out/check-lan1/*/`: C3 "LỖI ĐO KeyError: 'torso'" ở 9/9 file | **Chủ dự án CHẤP NHẬN** (chat 27/09/2026). **Đã sửa ở checks v1.4** (LOCK 289c6916363f…): lược đồ ghi ở RUN.md 3.6.1. Độ dài lấy ở cấp gốc; thiếu thì lấy `parts{}` (một nguồn cho mọi bộ phận, không trộn); thêm bảng `c3_views` (góc 0° phải khớp cấp gốc). Sai định dạng (sheet, parts.json, views) → THIẾU với "Sai định dạng (RUN.md mục 3.6): …" nêu đúng trường, không lộ lỗi Python. Selftest: sheet chỉ có `parts{}` → ĐẠT; thiếu torso (trước: KeyError), khoá góc 'front', views thiếu trường → THIẾU, thông báo rõ |
| 2026-09-27 (P, Cổng 3 đợt vá A2+; chủ dự án chọn B-i) | C3 | C3 đo độ dài 2D của mặt nạ NHÌN THẤY, nên đổi theo **tư thế** (tay gập), **góc nhìn** (nghiêng, sau lưng), **che khuất** (váy, áo len) và **cỡ đầu** — dù nhân vật dựng đúng model sheet. Bằng chứng: (1) cùng lưới 3D, tư thế đứng thẳng, máy trực giao, thân Ida đo được 2,584 (0°) / 2,332 (45°) / 2,153 (−90°) — lệch 17 % chỉ vì góc; (2) 8 file A2+ đều TRƯỢT với độ lệch khớp tư thế/góc (cận mặt tay gập: cẳng tay +55,9 %; cảnh 5 rộng đầu 13 px: +166 %; walk nghiêng: thân −13…−16 %); (3) **walk_cas (góc và tư thế gần sheet): mọi bộ phận −6,8…+4,1 %, đa số "đạt"** — nhân vật khớp sheet. Đề nghị (v1.4): chỉ tính C3 ở khung có tư thế và góc gần sheet (ví dụ thân thẳng, góc lệch ≤ 30°, không che khuất > x %), hoặc cho model sheet nhiều góc (`c3_views`) và so với góc gần nhất; khung ngoài miền → "—" có ghi lý do, không phải TRƯỢT. P không nộp chọn lọc để lách | `design/cong3/v2/out/a2p/check/*/` (8 file); `reports/m1/cong3-a2p/B1_so-do-moi-goc.json`; `reports/m1/CONG-3-VA-A2PLUS.md` mục 5 | **Chủ dự án CHẤP NHẬN, chọn B-i** (chat 27/09/2026). **Đã sửa ở checks v1.4** (LOCK 289c6916363f…): C3 chỉ so ở mẫu đo được, với số của góc `c3_views` gần nhất. Đo được khi góc 3D cách góc gần nhất ≤ 30°, co ngắn do tư thế ≤ 2%, bị vật ngoài thân che ≤ 10%, phối cảnh lệch đầu ≤ 2%, không chạm mép khung. Góc và tư thế lấy từ `views` xuất từ render (RUN.md 3.6.2), kiểm toán render lại cả `views`. Mẫu không đo được được đếm, liệt kê; tỷ lệ đo được báo theo từng shot. Shot có nhân vật mà 0 mẫu đo được → **CẦN NGƯỜI XEM** (mã thoát 5), không ĐẠT. Chạy thử 8 file (mặt nạ thật, `views` K tính từ page.js): TRƯỢT 8/8 → CẦN NGƯỜI XEM 5, TRƯỢT 3. walk_cas: đùi +9,2…+11,4% so với −90°. walk: thân +2,2…+3,9% không chứng minh được. c_s5_wide: độ khớp biên 1,06 (v1.3). Chi tiết: `reports/checks-v1.4/dryrun/KET-QUA-CHAY-THU.md`. Selftest: (a) tay gập → ĐẠT (không views: TRƯỢT); (b) tay +20% ở 0° → TRƯỢT; (c) toàn góc lệch → CẦN NGƯỜI XEM. **P cần:** xuất `views` (tham chiếu `reports/checks-v1.4/dryrun/k_views.js`) và `views.json` khi kiểm toán. **Quyết định của chủ dự án về v1.4:** Q-C3v = A: P đo thêm các góc −45°, ±135°, 180° vào `c3_views` và xuất `views`. Q-C3w = A: P render tư thế turnaround ở góc −75° để kiểm đùi Cas (+9,2…+11,4% so với −90° ở walk_cas) trước khi quyết. Q-C3r = B: shot CẦN NGƯỜI XEM do phiên kiểm liên tục (agent cine-continuity) lập tờ so sánh shot với model sheet trước; chủ dự án chỉ duyệt các shot bị đánh dấu. Q-C3p = A: giữ ngưỡng phối cảnh 2%. Không đổi luật hay LOCK (vẫn 289c6916…) |
| 2026-09-28 (P, Cổng 5 layout) | P0 | **Báo nhầm: mặt nhân vật đọc thành chữ.** Trên `design/cong5/layout/out/layout.mp4`, vùng duy nhất bị tính "chữ không matte" là khung 2775 (s42a), hộp [469, 196, 494, 208] đọc "56", độ tin 0,84 (sát ngưỡng 0,8). Hộp nằm đúng trên **hai mắt và lông mày của Cas** (mặt 3D, không có chữ nào trong hình; luật thế giới mục 6 cấm chữ đọc được). Bộ lọc độ đặc nét loại cửa sổ nhưng không loại cặp mắt tròn tối trên nền da. Đề nghị K: (a) loại vùng nằm trong mặt nạ nhân vật (`X.parts/` đã có mặt nạ đầu, mỗi 12 khung) hoặc (b) nâng độ tin cho chuỗi toàn số ≤ 2 ký tự, hoặc (c) cho P khai vùng loại trừ có kiểm lại bằng người xem. P không sửa hình để lách luật | `reports/m2/cong5/khieu-nai/P0_khung2775_s42a.jpg`; `reports/checks/layout-cong5/layout.checks.md` mục P0 | **Chủ dự án CHẤP NHẬN** (chat 29/09/2026). **Đã sửa ở checks v1.5** (LOCK 8d55b6ad…): K chọn (a) có điều kiện — vùng chữ không matte được miễn khi chuỗi ≤ 3 ký tự, khung có mặt nạ nhân vật trong `X.parts/` (mặt nạ C3 hoặc `silhouettes` mới, bóng mọi nhân vật, RUN.md 3.6.3), mặt nạ chạm hộp chữ, mặt nạ khớp cạnh ảnh ngay quanh hộp (độ khớp biên cục bộ ≥ 1,5), và xoá nhân vật khỏi khung rồi đọc lại thì hết chữ (phản chứng). Không chọn (b) (nâng độ tin cho chuỗi số: không phân biệt được mắt với số thật) và (c) (vùng loại trừ khai tay). Khung này: hộp "56" nằm 100% trên đầu Cas, độ khớp cục bộ 2,32, đọc lại sau khi xoá: rỗng → miễn. Selftest: khung thật (khớp từng điểm ảnh bản gốc) không mặt nạ → TRƯỢT, có bóng → ĐẠT; "BAKERY"/"CAFE" in trên áo Cas → TRƯỢT; "56" trên tường → TRƯỢT; "56" chạm mép đầu Cas → TRƯỢT; mặt nạ giả che "56" → TRƯỢT. **P cần:** xuất `silhouettes` cho các khung P0 lấy mẫu (công cụ tham chiếu `reports/checks-v1.5/dryrun/k_sil.js`). Chi tiết: `reports/checks-v1.5/BAO-CAO.md` |
| 2026-09-28 (P, Cổng 5 v2 layout) | P0 | **Báo nhầm lần 2 cùng loại:** trên `layout.mp4` v2 bản cuối (SHA `78e662d1…`), vùng duy nhất bị tính "chữ không matte" là khung 1980 (s33), hộp [351, 288, 616, 452] đọc "MA", độ tin 0,86 (ngưỡng 0,8). Hộp bao **hai nhân vật đứng trong hốc cửa** (Ida và Cas, dáng thẳng đứng) — không có chữ nào trong hình. Cùng gốc với khiếu nại 2026-09-28 (mắt Cas đọc "56"). Đề nghị như trên (loại vùng thuộc mặt nạ nhân vật trong `X.parts/`) | `reports/m2/cong5/khieu-nai/P0_khung1980_s33.jpg`; `reports/checks/layout-cong5/layout.checks.md` mục P0 | **Chủ dự án CHẤP NHẬN** (chat 29/09/2026). **Đã sửa ở checks v1.5** (LOCK 8d55b6ad…): cùng cách sửa với khiếu nại "56" ở trên. Khung này: hộp "MA" 266 × 165 px, phần lớn là tường giữa hai người (mặt nạ hai nhân vật phủ 16% hộp), nên K không đo "phần lớn" bằng diện tích mà bằng phản chứng: xoá Ida và Cas thì máy không còn đọc ra chữ (độ tin 0); độ khớp biên cục bộ 1,61 (ngưỡng 1,5) → miễn. Selftest: khung thật không mặt nạ → TRƯỢT, có bóng → ĐẠT. **Chủ dự án cần xác nhận** cách hiểu "phần lớn trong mặt nạ" = phản chứng (Q-P0c trong báo cáo). Chi tiết: `reports/checks-v1.5/BAO-CAO.md` **Chủ dự án xác nhận Q-P0c (chat 29/09/2026).** |
| 2026-09-29 (P, Cổng 6 W2; chủ dự án giao: C3 phải đo cả Cas) | C3 (một nhân vật mỗi thư mục `parts`) | **Không phải luật đo sai, mà luật chỉ đọc MỘT nhân vật mỗi lần chạy.** RUN.md 3.6: "`parts.json` có một `model_sheet`; một thư mục parts cho mỗi lần chạy (v1 kiểm một nhân vật mỗi file; báo P nếu shot có nhiều nhân vật chính)". Phim có hai nhân vật chính (Ida, Cas) ở 21 shot (đo trên layout-v16: `reports/checks/layout-v16-c3-cas/`, Cas đo được 141/565 mẫu, lệch lớn nhất 19,11 %, 7 shot cần người xem); từ Cổng 3 tới layout-v16, C3 chỉ đo Ida, Cas chưa từng được đo. P **không sửa checks/**, làm theo đúng câu "một thư mục parts cho mỗi lần chạy": `export_c3.js --who cas` xuất mặt nạ Cas (model_sheet cas.json, trục đầu 'doc') vào `<X>.cas.parts`, rồi chạy `audit.py issue` và `run.py --only C3` trên `<X>.cas.mp4`. Tệp này là **liên kết cứng** tới `<X>.mp4`: `audit.py` giải liên kết mềm về tệp gốc nên ghi đè `<X>.audit`. **Đề nghị K chọn một:** (a) xác nhận cách hai lượt này hợp lệ, kể cả liên kết cứng và `--only C3` cho lượt Cas; hoặc (b) cho `parts.json` khai nhiều nhân vật (ví dụ `characters: {ida: {model_sheet, frames, views}, cas: {…}}`), C3 báo theo từng nhân vật, kiểm toán chọn khung của từng nhân vật; hoặc (c) `audit.py`/`run.py` nhận `--audit` như `--parts` | Chạy thử 2 shot có cả hai nhân vật (s41 + s42a, cắt từ layout-v16, khung 2688–2771): `reports/checks/c3thu-s41-s42a-c3-ida/` (Ida: TRƯỢT như v16, thân −8,74 % ở 90°, s41 cần người xem) và `reports/checks/c3thu-s41-s42a-c3-cas/` (Cas: 0 mẫu trượt chắc, 4 đạt, 12 không chứng minh được vì đầu Cas chỉ cao 15–44 px; kiểm toán ĐẠT). Mã: `design/cong5/layout/export_c3.js` (`--who`, `--offset`), `scripts/p/c3_hai_nv.sh` | Chờ K / chủ dự án |


## Yêu cầu mới, 2026-10 (P gửi 04/10/2026 theo quyết định chủ dự án; chờ K phán quyết và khoá bản checks mới)

Nguồn: `reports/m3/YEU-CAU-K-NHAP.md`. Bảy mục:

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

### 2. Profile luật cho Shorts 9:16
**Hiện trạng:** `run.py --profile shot|youtube|archive`. Profile `youtube` kiểm N3 khung 16:9 và SAR 1:1, M1 −14 LUFS ±1, true peak ≤ −1 dBTP.

**Nhu cầu:** Shorts 1080×1920, 24 fps, < 60 s, có chữ trên màn hình và phụ đề cháy (`KE-HOACH-TAP-THU.md` §6).

**Câu hỏi cho K**
1. Thêm profile `shorts`, với các điểm khác profile youtube:
   - N3: khung 9:16, 1080×1920, SAR 1:1; codec và bitrate theo khuyến nghị YouTube Shorts;
   - thời lượng < 60 s (luật mới hoặc thuộc N3);
   - M1: giữ −14 LUFS?
   - P0/P1/G4: vùng an toàn chữ cho giao diện Shorts (lề trên, dưới, phải bị nút che). Có cần luật vùng an toàn mới không?
2. Shorts cắt từ master 16:9: C3 và H1b chạy trên bản cắt hay chỉ trên master?

### 3. Luật đo judder (thêm 01/10/2026, theo CHUAN-KENH-LL §5.2; gửi ở M2.3)
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

### 4. Luật phát hiện máy xuyên hình học (thêm 01/10/2026 sau animatic v3; gửi ở M2.3)
**Hiện trạng**
- Ở animatic v3, lỗi trôi máy cộng dồn làm máy xuyên vào khối nhà: đoạn 01 7,7–9,9 s; đoạn 04 khoảng 14 s. Đồng hồ quảng trường trôi khỏi khung 3,5 s.
- **Judder không bắt được** lỗi này vì khung vẫn thay đổi liên tục. P chỉ phát hiện khi xem khung bằng mắt.

**Câu hỏi cho K**
1. Có thêm luật tự động không? Ví dụ một trong hai cách:
   - xuất kèm độ sâu từ driver render, rồi đo tỷ lệ điểm ảnh có độ sâu sát mặt phẳng gần (> x % khung) trong ≥ 3 khung liền;
   - đo tỷ lệ khung một màu phẳng (> 60 % diện tích) ngoài vùng chuyển cảnh.
2. Có thêm luật "chủ thể bắt buộc ra khỏi khung" không? Ví dụ đồng hồ, đèn hoặc nhân vật khai trong bảng shot mà không còn trong khung.

**P đề xuất** (K quyết): luật độ sâu cho cảnh three.js; driver xuất kèm độ sâu thu nhỏ.

### 5. Kiểm chéo số HSUS từ bản quét (thêm 04/10/2026)
**Hiện trạng**
- Đoạn 08, 09, khối 10–13 và đoạn 14 dùng 24 giá trị từ HSUS Series D 233–682, tr. 140–145 [32]. PDF là ảnh quét, không có lớp chữ.
- P đọc từng hàng bằng mắt trên ảnh dựng ở 220–400 dpi. Chưa có người thứ hai đọc lại.

**Yêu cầu K:** K đọc độc lập 24 giá trị (thang máy 1900–1970 theo hai phân loại 1950/1960/1970; trực tổng đài; tốc ký–đánh máy–thư ký) từ bản quét và đối chiếu với bảng §6.1 kịch bản v3.1. Lệch giá trị nào thì báo P sửa hình trước G2.

### 6. Kiểm lại số BLS 2025–35 (thêm 04/10/2026)
**Hiện trạng**
- Số BLS Table 1.5 và USDL-26-1422 được đọc toàn văn ngày 01/10/2026 qua Wayback (bls.gov trả 403 từ máy này).
- Các số trên hình: −34,4 %, −27,6 %, −26,0 %, −25,5 %, −21,4 %, −4,0 %; nhóm tăng +41,0 / +36,5 / +34,6 %.

**Yêu cầu K:** K kiểm lại từng số trên bảng gốc (đường dẫn trực tiếp hoặc Wayback) và ghi ngày đọc.

### 7. Luật nguồn số: không dùng Wikipedia làm nguồn chính (thêm 04/10/2026, CHUAN-KENH §7)
**Hiện trạng:** số "1820s · 40 000 đèn · 215 dặm" từng dựa trên Wikipedia và hai trang web. Claude (rà độc lập) phát hiện; ở M2.2 phim đã bỏ số này.

**Đề xuất cho K:** mỗi số trên hình hoặc trong lời dẫn phải có ít nhất một nguồn chính là sách, báo cáo, bài học thuật hoặc văn bản gốc đọc được toàn văn, có ghi trang. Wikipedia, trang tổng hợp hoặc blog chỉ được dùng để dẫn đường. K quyết cách kiểm (danh sách nguồn có trường `loai_nguon` và `trang`).


### 8. Bộ kiểm nhà máy `scripts/ll/qc.sh` — đề nghị K xét khoá thành luật (thêm 04/10/2026, Mốc B)
**Hiện trạng:** P viết bộ kiểm một lệnh cho các tập dựng bằng thư viện `scripts/ll/lib/` (báo cáo `reports/m3/MOC-B-NHA-MAY.md` §3). Đây là luật làm việc của P, **không** nằm trong `checks/`, P không sửa `checks/`. Mục kiểm và ngưỡng ghi ở đầu `scripts/ll/qc.py`:
- Q1 judder 2–12 khung (framemd5) = 0; Q2 khung gần trùng kẹp giữa chuyển động (|chênh| ≤ 0,1 mức xám, trung vị 6 khung hai bên > 0,5) = 0;
- Q3 máy xuyên hình học: log khoảng cách máy–lớp gần của cảnh 2.5D ≤ 0,05 → lỗi; khung có > 85 % ô 16×16 phẳng ngoài vùng mờ (trừ thẻ kết) → nghi;
- Q4 −14 ± 1 LUFS, TP ≤ −1 dBTP (master, Shorts; 3 phần bản xem ±2 LU để đối chiếu);
- Q5 tương phản ≥ 4,5:1 **đo trên điểm ảnh thật** (nền = trung vị viền hộp chữ; chữ = phân vị 5 %/95 % trong hộp) ở mỗi 12 khung; Q6 chữ hoa ≥ 18 px (16:9) / 30 px (9:16) ở mọi khung mẫu, kể cả khi tấm giấy thu nhỏ;
- Q7 shot có số dự báo phải hiện chữ PROJECTION, có số thực tế phải hiện ACTUAL; Q8 nguồn đọc toàn văn, không Wikipedia/Wikimedia làm nguồn chính, số trên hình có cụm đọc trong lời đoạn;
- Q9 số khung trung gian = timeline, master = tổng; Q10 mỗi phần bản xem ≤ 90 MB, Short ≤ 60 s; Q11 không quá 3 s liền không có nội dung mới khi lời đang nói (cảnh truyện toàn khung miễn).

**Đề nghị K:**
1. Xét khoá Q1–Q11 (hoặc phần K chọn) vào `checks/` như luật kênh Last Lamplighters cho tập nhà máy; gộp với yêu cầu 2 (Shorts), 3 (judder), 4 (máy xuyên), 7 (nguồn) ở trên.
2. Xác nhận cách đo Q5 trên điểm ảnh (khác cách đo theo màu khai báo ở tập 1).
3. Q3 bản ảnh (khung phẳng) là heuristic, có thể báo nhầm với cảnh nền đơn sắc: K chọn ngưỡng hoặc bỏ.

### 8b. Bổ sung mục 8 (05/10/2026, khi dựng tập 2)
- **Q11 bản dài đổi định nghĩa** cho đúng luật kênh §5.1 ("không khung đồ hoạ nào **đứng trống** quá 3 s khi lời dẫn đang nói", lỗi L1 tập 1): đếm khung chưa có dữ liệu hay chữ gắn lời (chỉ tựa/trục/nguồn/biểu tượng). Bản cũ "không có nội dung mới > 3 s" chặt hơn luật, báo cả lúc biểu đồ đã đủ số; nay chỉ áp cho **Shorts** (yêu cầu Mốc B). Đề nghị K xác nhận hai định nghĩa.
- Q5 có thêm dữ kiện: góc tối của ánh rọi B3 làm chữ nhỏ ở mép giấy xuống 4,1–4,4:1; P giảm độ tối góc ≈ 17 % và đặt nhãn trục trên nền giấy.

### 8c. Thêm Q12 — thumbnail trong lề an toàn (05/10/2026, theo G2 tập 2)
- G2 tập 2: thumbnail T1 bị cắt chữ S của "OPERATORS" ở mép phải. Chủ dự án giao thêm mục qc.
- **Q12:** ảnh 1280×720; mọi hộp chữ (gồm nền chữ) nằm trong lề an toàn 5 % mỗi cạnh (64 px ngang, 36 px dọc), không chạm. Hộp lấy từ `.boxes.json` do `scripts/ll/thumb.py` ghi; thiếu tệp này thì TRƯỢT.
- Đề nghị K xét khoá cùng Q1–Q11.

## Phán quyết K — checks LL v2 (06/10/2026; chủ dự án duyệt lệnh khoá 06/10)
Bản khoá: `checks/ll/` (luật `checks/ll/RULES-LL.md`), VERSION 1.6.0, LOCK ghi ở `checks/LOCK`. Báo cáo: `reports/checks-ll-v2/BAO-CAO.md`.
qc.py gọi luật khoá cho Q7, Q12–Q25 và thêm dòng LOCK. Phần còn lại của mục 8 (Q1–Q6, Q8–Q11) **chưa khoá ở bản này**: vẫn là luật làm việc của P.

| Mã | Đề nghị của P | Phán quyết K | Sửa khi khoá |
|---|---|---|---|
| Q7 | Nhãn ACTUAL/PROJECTION có mặt | **CHẤP NHẬN, siết thêm** | Bản cũ chỉ đòi nhãn có mặt nên không bắt được lỗi tập 2 S2 (ACTUAL hiện trên −5,3 % dự báo, vì thẻ có số actual khác). Nay TRƯỢT cả khi hiện nhãn của loại không có trong shot, hoặc `kind` khai khác loại của `num` |
| Q12 | Thumbnail trong lề 5 % | **CHẤP NHẬN** | Không đổi ngưỡng. Hạn chế: hộp chữ do `thumb.py` tự khai, K chưa đo trên điểm ảnh (ghi trong báo cáo) |
| Q13 | Số trên bề mặt phát hành truy về `numbers` | **CHẤP NHẬN, sửa 3 điểm** | (1) thêm kiểm dấu; (2) đọc "135k"; (3) **bỏ "?"** khỏi danh sách dấu hiệu dự báo (câu hỏi không phải nhãn dự báo). Câu hỏi Q-L13 ở dưới |
| Q14–Q18 | Luật nhịp | **CHẤP NHẬN nguyên ngưỡng** | Bản khoá dùng hàm nền riêng (`checks/ll/base.py`), không phụ thuộc `ll.py`. Chạy lại: tập 3 trượt cả 5 mục như tổng kết lô 3–5; tập 4 và 5 đạt |
| Q19 | Hồ sơ quyền tư liệu | **CHẤP NHẬN, vá 1 lỗ** | Danh sách trắng cũ nhận `loc.gov.evil.com`; nay tên miền phải kết thúc ở `.gov` |
| Q20 | Chữ không đè hình (cờ `hit`) | **CHẤP NHẬN có điều kiện** | Cờ `hit` do render tự khai và chỉ xét dải chú thích. K thêm phép đo độc lập: khi log có `zones` thì mọi hộp chữ không được giao vùng hình. Từ tập 6, đoạn có isotype phải ghi `zones` (Q-L20) |
| Q21 | Dòng nguồn khớp `src` | **CHẤP NHẬN, siết thêm** | Không tin riêng `capsrc` do ll.py ghi: nguồn cần có cộng thêm nguồn của `num` và `src` khai trong đặc tả |
| Q22 | Chữ tràn khung, gồm Shorts 9:16 | **CHẤP NHẬN** | Không có log render thì TRƯỢT (trước đây ĐẠT vì không có gì để đo) |
| Q23 (mới, chủ dự án giao) | Câu ghép nhiều số | **KHOÁ** | Định nghĩa ở RULES-LL.md. Chạy trên 4 tập đã đăng bắt được 2 chỗ: tập 2 thẻ so sánh đoạn 11 (−16,1 % đếm 1930–40 ↔ −5,3 % dự báo 2025–35, cùng dạng lỗi +87 % ↔ −13 %) và tập 4 hook Short S1 "134,000 to 3.9 million" (1900, phân loại 1950 → 1970). Tập 3 và tập 5: 0 |
| Q24 (mới) | Nhãn phân loại khớp số (bài học HSUS 135 nghìn) | **KHOÁ** | |
| Q25 (mới) | Thẻ khoảng số không đếm qua số trung gian (bài học 50–80 %) | **KHOÁ** | |

**Câu hỏi cho chủ dự án** (K đã khoá theo phương án khuyến nghị; nếu chọn khác, K sửa và khoá lại):
- **Q-L23a. "Cùng một đối tượng" nghĩa là gì?** **A (khuyến nghị, đang khoá):** cùng họ nguồn (cùng cơ quan phát hành) và cùng loại, cùng kỳ. Ví dụ được phép: "giám định viên −5 %, mọi nghề +3,5 % (BLS 2025–35)". Ưu: giữ được phép so với mức chung, khớp bài học #17 (cùng nguồn, cùng kỳ). Nhược: hai nghề khác nhau vẫn đứng chung một câu. **B:** đúng một nghề trong mỗi câu/thẻ. Ưu: chặt nhất. Nhược: tập 5 lời 07 sẽ TRƯỢT; mất phép so với mức chung.
- **Q-L23b. Hai chỗ tìm thấy ở tập đã đăng.** **A (khuyến nghị):** không sửa video đã đăng; ghi vào BAI-HOC; luật áp từ tập 6. **B:** sửa chữ hook Short S1 tập 4 (phải render lại Short) và mô tả liên quan.
- **Q-L20. Bắt buộc ghi `zones` từ tập 6?** **A (khuyến nghị):** có. P thêm `zones` vào log render (render.js, `LL.zones`). Ưu: đo độc lập, bắt được cả chữ không thuộc dải chú thích. Nhược: P sửa thư viện một lần. **B:** chỉ dựa cờ `hit`.
- **Q-L13. Bỏ "?" khỏi dấu hiệu dự báo?** **A (khuyến nghị, đang khoá):** bỏ. Bốn tập đã đăng vẫn ĐẠT. **B:** giữ như P.

**Chủ dự án DUYỆT checks LL v2 (chat 06/10/2026):** VERSION 1.6.0, LOCK `0973478b6493722f3812862238c0d31752ef8062102711299e8adefc13b63908`. Claude tính lại LOCK: KHỚP; selftest 52/52.
- **Q-L23a = A:** "cùng đối tượng" là cùng họ nguồn (cùng cơ quan phát hành), cùng loại, cùng kỳ. Đúng như bản đã khoá, không đổi luật.
- **Q-L23b = A:** không sửa video đã đăng (thẻ so sánh đoạn 11 tập 2; hook Short S1 tập 4). P ghi hai chỗ này vào BAI-HOC. Q23 áp từ tập 6.
- **Q-L20 = A:** từ tập 6, P ghi `zones` vào log render (render.js, `LL.zones`) cho đoạn có isotype. Thiếu thì Q20 TRƯỢT (đã có trong bản khoá).
- **Q-L13 = A:** bỏ "?" khỏi dấu hiệu dự báo. Đúng như bản đã khoá.
Không đổi `checks/`, không đổi LOCK. Phiên K kết thúc.

## Yêu cầu khoá — Q26–Q31 (P chuyển lời chủ dự án, 06/10/2026)
Chủ dự án giao: các luật chất lượng mới Q26–Q31 (định nghĩa ở `reports/m3/CHUAN-KENH-LL.md` §11.2) là luật tự động, **Chặn**, và **gửi K khoá ở lần mở tới**.
- Từ nay đến khi K khoá, P chạy các luật này như **luật làm việc của P** trong `scripts/ll/` (`diversity.py` cho Q26, các công cụ còn lại ghi trong `scripts/ll/README.md`) và báo số đo ở mỗi báo cáo G2.
- P không sửa `checks/`.

## Khiếu nại P — Q16 bản khoá không nhận các mẫu toàn khung mới (06/10/2026, tập 6 v2)
- **Hiện tượng:** qc tập 6 v2, Q16 (bản khoá) báo **79,3 %** thẻ giấy (trần 40 %). Thước nhịp của P (`scripts/ll/rhythm.py`, tập FULL đã cập nhật) đo **12,9–15,2 %** trên cùng timeline.
- **Nguyên nhân P suy ra từ đầu ra (P không đọc mã `checks/`):** danh sách mẫu toàn khung trong bản khoá có trước tập 6 v2, nên chưa có các mẫu mới chủ dự án yêu cầu ở CHUAN-KENH §11.3. Đó là `plate` (cảnh đinh 3D), `jobboard`, `filmstrip`, `pasteup`, `diptych` (lib/v3.js). Các mẫu này vẽ cảnh toàn khung, không phải thẻ giấy.
- **Đề nghị K:** thêm 5 mẫu trên vào tập cảnh toàn khung của Q16, khoá lại, chạy lại trên tập 6 v2 và các tập đã đăng (không đổi ngưỡng).
- **Ghi chú cho K về Q26 (luật làm việc của P):**
  - Định nghĩa "cùng bố cục" của P (cụm xám 32×18, ngưỡng 24/255) gộp mọi cảnh tối (phố đêm, phòng tối, phòng tráng ảnh) thành một bố cục, dù cấu trúc khác nhau.
  - Điểm cắt dò bằng scdet bỏ sót fade. Khi có timeline, P lấy ranh giới shot thật.
  - Đề nghị K chọn định nghĩa bố cục khi khoá, ví dụ chuẩn hoá độ sáng từng khung trước khi so. Tập 1 cũng trượt điều kiện này (chuỗi 4).
- **Đề nghị Q14 (tập 6 v2, Q31):** cả 3 người xem mù đều thấy cú nhảy từ cảnh tối sang thẻ tựa giấy kem ở 0:19,8 là cứng. Bản khoá chỉ nhận tựa là shot `text` có `lamp`. Đề nghị K cho phép thêm dạng tựa chồng lên cảnh đinh (ví dụ shot `plate` có `title`), ngưỡng 0:20 giữ nguyên. Cho tới khi K khoá, P giữ thẻ tựa giấy.
- **Chủ dự án quyết (07/10/2026):** Q26 "cảnh liền cùng bố cục" theo phương án A. K định nghĩa lại thước khi khoá: chuẩn hoá độ sáng từng khung, hoặc dựa ranh giới shot thật. Gửi K **cùng lúc** với đề nghị Q14 (tựa chồng lên cảnh đinh) và Q16 (5 mẫu toàn khung) ở trên.

## Phán quyết K — checks LL v3 (07/10/2026; chủ dự án duyệt lệnh khoá 07/10)
Bản khoá: `checks/ll/` (luật `checks/ll/RULES-LL.md`), VERSION 1.7.0, LOCK ở `checks/LOCK`. Báo cáo: `reports/checks-ll-v3/BAO-CAO.md`.
qc.py gọi luật khoá Q26–Q31 (áp từ tập 6) và truyền log render cho Q14. Từ bản này **P không sửa định nghĩa Q26–Q31** (`scripts/ll/diversity.py`, `cont.py`, `blind_set.py` chỉ còn là công cụ nháp của P) và **không sửa đề bài Q27/Q31**.

| Mã | Luật làm việc của P | Phán quyết K | Sửa khi khoá |
|---|---|---|---|
| Q26 | khung nhìn, tỷ lệ lớn nhất, cảnh liền cùng bố cục | **KHOÁ, sửa định nghĩa** | (1) Gom cụm liên kết đầy đủ thay cho "so với mẫu đầu cụm" (phụ thuộc thứ tự); (2) 6 pha lấy mẫu, lấy pha xấu nhất (thước P: tập 1 dao động 14,4–21,6 % chỉ vì pha); (3) cảnh liền cùng bố cục = cắt sang **cùng khung nhìn** sau khi chuẩn hoá sáng/tương phản, ranh giới shot lấy từ timeline. Ngưỡng giữ nguyên. Tập 1 ĐẠT (64 / 11,9 % / 2), tập 6 v1 TRƯỢT (19 / 43,3 %), tập 6 v2 ĐẠT (70 / 5,5 % / 2; chuỗi 5 của P là 5 cảnh tối khác nhau) |
| Q27 | 3 subagent chấm 10 + 10 khung | **KHOÁ** | Đề bài khoá (`checks/ll/blind/Q27-R*.txt`), lấy mẫu phân tầng, hạt giống = SHA video mới, tập 1 khoá SHA, không có tệp khoá giải mã, bộ chấm dựng lại ảnh để so SHA. Ngưỡng như chủ dự án. Câu hỏi Q-L27 ở dưới |
| Q28 | cont.py Q28 | **KHOÁ, siết 5 điểm** | (1) số neo phải tìm thấy (P bỏ qua im lặng khi không khớp cụm `say`); (2) đo lặng trên **âm thật** của tệp lời, mọi lần đọc (tập 6 v2: 4 lần, P đo 3); (3) nhạc hiệu kênh xác định bằng SHA (RIGHTS LL-MUS-1), cue không được dài hơn bài; (4) `diptych` là cảnh đinh; SFX phải có SHA trong RIGHTS; (5) ASR độc lập của K trên tệp lời, số so chặt theo giá trị |
| Q29 | cont.py Q29 | **KHOÁ, siết 3 điểm** | Số neo được kiểm (P có vòng lặp rỗng); hình phải hiện ≥ 0,5 s trong cửa sổ ±1 s; đoạn có lời phải khai `map.nouns`. Bản đồ (`map`) không còn là hình vật chất |
| Q30 | cont.py Q30 | **KHOÁ, siết 3 điểm** | (1) hai phía điểm chuyển hồi phải khai cùng một kiểu; (2) đèn theo cảnh + góc máy K đã xem tận mắt (P: theo tên cảnh), cảnh mới khai `lamp: true`; (3) **tông màu đo trên điểm ảnh** (P đếm nhãn `grade` tự khai). Câu hỏi Q-L30 ở dưới |
| Q31 | 3 subagent xem liền mạch | **KHOÁ** | Đề bài khoá, định dạng trả lời JSON, gom điểm (cùng T## hoặc ≤ 4 s), TRƯỢT khi có điểm **đứt mạch** được ≥ 2/3 người cùng nêu. Câu hỏi Q-L31 ở dưới |
| Q14 (đề nghị P) | cho tựa chồng lên cảnh đinh | **CHẤP NHẬN** | `plate` có `p.title`; chuỗi tựa phải hiện trong log render của đoạn trong khoảng shot. Ngưỡng 0:20 giữ nguyên. Q14 "hình < 0:15" dùng cùng tập cảnh toàn khung với Q16 |
| Q16 (khiếu nại P) | thêm 5 mẫu toàn khung | **CHẤP NHẬN** | K xem khung thật tập 6 v2: `plate`, `diptych`, `filmstrip`, `jobboard` là cảnh toàn khung; `pasteup` là đạo cụ thời kỳ đặt trên bàn (không phải thẻ dữ liệu), chấp nhận. Tập 6 v2: 75,6 % → 7,2 %. Tập 2–5 không đổi |

**Câu hỏi cho chủ dự án** (K đã khoá đúng chữ CHUAN-KENH §11.2; nếu chọn khác, K sửa và khoá lại):
- **Q-L27. Số khung chấm mù.** Ba người chấm Sonnet tương quan 0,98, nên phương sai nằm ở việc rút khung nào: với 10 + 10 khung, sai số chuẩn của chênh lệch ≈ 0,63 điểm. Tập 6 v2: lần P chấm +0,37 (ĐẠT), lần K chấm −0,74 (TRƯỢT); cả hai nằm trong nhiễu. **A (đang khoá):** 10 + 10 như chủ dự án định. **B (khuyến nghị):** 30 + 30 (sai số ≈ 0,36), cùng đề bài, 3 người chấm. Ưu: kết luận ổn định. Nhược: mỗi lần chấm đọc 60 ảnh (thời gian người chấm ≈ ×3, vẫn dưới 1 phút).
- **Q-L30. Tông màu theo hồi.** Đo thật tập 6 v2: hồi 3 khai "lạnh" có h = 61°, C = 9 (sepia, ngả vàng); nhãn `grade` cho 69 %. **A (khuyến nghị, đang khoá):** đo trên điểm ảnh, ngưỡng tuyệt đối (lạnh: h 180–300°). Tập 6 v2 TRƯỢT, P phải grade lại các cảnh đinh hồi 3. **B:** đo trên điểm ảnh, chỉ đòi thứ tự tương đối (hồi 3 có b* thấp nhất trong 4 hồi). Tập 6 v2 ĐẠT. **C:** giữ cách P (đếm nhãn).
- **Q-L31. Điểm đồng thuận.** Tập 6 v2 (bản G2 lần 2): 7 điểm đứt mạch ≥ 2/3, trong đó 3 điểm cả 3/3 cùng nêu (T03, T05, T10). **A (khuyến nghị, đang khoá):** TRƯỢT khi còn điểm đứt mạch ≥ 2/3; điểm "chán" chỉ liệt kê. **B:** chỉ chặn điểm 3/3; điểm 2/3 phải có phản hồi trong báo cáo G2. **C:** chặn cả điểm "chán" ≥ 2/3.
- **Q-L6v2. Áp v3 cho tập 6 v2 đang chờ G2?** Theo bản khoá, tập 6 v2 TRƯỢT Q27, Q28 (2 shot diptych không có âm thanh nghề), Q30 (đèn ở 01→02, màu hồi 3), Q31. **A (khuyến nghị):** áp; P sửa rồi chạy lại qc (Q28 và đèn là sửa nhỏ; màu hồi 3 tuỳ Q-L30). **B:** phát hành tập 6 v2 theo luật làm việc của P, áp v3 từ tập 7.

**Chủ dự án DUYỆT checks LL v3 (chat 07/10/2026):** LOCK `0b180104…` KHỚP; selftest 97/97. Phán quyết, K đã sửa luật và khoá lại (VERSION 1.7.1, LOCK ghi ở `checks/LOCK` và `reports/checks-ll-v3/BAO-CAO.md` mục 12):
- **Q-L27 = B:** 30 khung tập mới + 30 khung tập 1, phân tầng đều, cùng cách trộn (hạt giống = SHA video mới). Đề bài Q27 đổi sang 60 ảnh F01–F60. Chạy thật trên đề bài mới (6 subagent Sonnet): tập 6 v2 4,98 so với 5,13 (TRƯỢT, chênh −0,15, sai số chuẩn 0,26, **sát ngưỡng ±5 %**); tập 6 v1 4,34 so với 4,92 (TRƯỢT, −0,58, sai số chuẩn 0,20). Ba người chấm bớt trùng nhau: tương quan 0,14–0,70 (bản 10 + 10: 0,98).
- **Q-L30 = B:** tông đo trên điểm ảnh; chỉ đòi hồi 3 (hôm nay) có b* trung bình thấp nhất trong 4 hồi; thiếu hồi để đo thì TRƯỢT. Tập 6 v2: b* hồi 3 = 7,9 < 9,5 (ĐẠT). **Hạn chế:** chưa có ngưỡng tuyệt đối; hiệu chuẩn lại sau tập 7–8.
- **Q-L31 = A có điều kiện:** vòng 1 chặn điểm đứt mạch ≥ 2/3. Từ vòng 2 chỉ chặn điểm 3/3; điểm 2/3 phải có giải trình (≥ 20 ký tự) trong `<out>/blind/q31/giai-trinh.json`, chép vào báo cáo G2. **Vòng tính theo từng tập:** `q31-set` chuyển lần xem trước của tập sang `q31-lich-su/vong-NN`; chỉ vòng chấm đủ 3 người được đếm; manifest ghi số vòng và bộ chấm đối chiếu với sổ lịch sử.
- **Q-L6v2 = B:** tập 6 v2 phát hành theo luật làm việc của P; qc chỉ gọi Q26–Q31 từ tập 7. Q14 (tựa trên cảnh đinh) và Q16 (5 mẫu toàn khung) đã chấp nhận vẫn áp như bản khoá.

**Chủ dự án DUYỆT checks LL v3 1.7.1 (chat 07/10/2026):** LOCK `e3fcd2e686ac92eb15cab0bf93e54aa31165acd8e129d500f4affeb58cc03240`. Claude tính lại: KHỚP; selftest 109/109. Không đổi `checks/`, không đổi LOCK. Phiên K kết thúc.
- Việc mở: **hiệu chuẩn lại Q30 (tông màu theo hồi) sau tập 7–8, ở một phiên K mới**.

## Khiếu nại P — Q28f (ASR độc lập) đọc sai số khi lời viết bằng chữ khác cách ASR viết (09/10/2026, tập 8)
P không đọc mã `checks/`; chỉ mô tả hiện tượng đo được trên bản nháp tập 8 (`ll-ep08-nhap`), qc 1.8.1.
- **Đoạn 06:** lời "some twenty million dollars"; faster-whisper small.en (beam 1, P chạy lại) viết "some $20 million". Q28f báo "thiếu 20000000.0". Giọng đọc đúng (P nghe lại bằng beam 5: "twenty million dollars").
- **Đoạn 13:** lời "three and a half percent"; ASR viết "3.5%". Q28f báo "thiếu 3.0", tức bộ chấm đọc giá trị lời là 3 (bỏ "and a half"), trong khi ASR nghe đúng 3,5.
- Cùng loại lỗi P vừa sửa trong `scripts/ll/asr.py` (luật làm việc của P): "and a half" = +0,5; năm đứng liền số ("nineteen sixty six twelve years") không ghép thành một số; ngày thứ tự sau tên tháng ("January seventh" = 7).
- **Đề nghị K:** (1) "$20 million" / "20 million" = 20 000 000; (2) "N and a half" = N,5; (3) không ghép số liền sau năm; (4) ngày thứ tự. Lời đã khoá (G1 v2), P không đổi chữ để né thước.
- Đến khi K sửa, G2 tập 8 ghi Q28 TRƯỢT riêng mục (f) với giải trình này; các mục khác của Q28 P sửa trong bản cuối.

## 10/10/2026 — Q27 chấm lại theo SHA master hiện tại (phiên P tập 8)
- **Hiện tượng:** Q27 chính thức tập 8 chấm trên master SHA `688b4fab…` (manifest `blind/q27/manifest.json` ghi SHA này): `q27-score` lúc đó cho 5,13 vs 5,44 (−0,31). Sau lượt sửa T12 (Q31), master đổi thành `a1202dbd…`; `qc.sh` chạy lại cùng R1–R3.json lại cho **5,31 vs 5,25 (+0,06)**.
- **Nguyên nhân (theo hành vi và thông báo lỗi khi chạy):** bước chấm điểm dựng lại phép gán khung F01–F60 ↔ tập mới/tập 1 từ SHA video đang có, không lấy từ `seed`/SHA lưu trong manifest, và không báo khi SHA lệch manifest. Khung người chấm đã xem thuộc master cũ, nên số mới gán sai khung.
- **Đề nghị K:** (1) chấm theo `seed`/phép gán lưu trong manifest; (2) nếu SHA video hiện tại khác manifest thì báo rõ "bộ chấm thuộc bản khác" thay vì tính lại; (3) luật ghi rõ sửa sau Q27 có cần chấm lại hay không.
- **P ghi trong G2:** kết quả chính thức là −0,31 (TRƯỢT nhẹ, lỗi nhỏ chấp nhận); số +0,06 của QC cuối nêu kèm, không dùng.

## Phán quyết K — checks LL v3 1.9.0 (11/10/2026; chủ dự án duyệt hướng sửa trong lệnh mở phiên K)
Báo cáo: `reports/checks-ll-v3/BAO-CAO.md` mục 15.
- **Q28f (khiếu nại 09/10): CHẤP NHẬN.** Bộ đọc số của K viết lại, dùng **cùng một bộ** cho lời khoá và văn bản ASR: "$20 million" = "20 million" = "twenty million dollars" = 20 000 000; "N and a half" = N,5; "%" = "percent"; năm đọc chữ không ghép với số liền sau; ngày thứ tự chỉ đọc sau tên tháng. Không nới: "two million" ≠ "twenty million", "3%" ≠ "three and a half percent" vẫn TRƯỢT. ASR thật của K (beam 5) trên tập 8: đoạn 06, 13 **ĐẠT**; tập 6 v2, tập 7 không đổi (ĐẠT trước và sau). Bộ cũ còn một lỗi K tự thấy: "two and three" bị cộng thành 5 (đã sửa: chỉ "and" sau hundred/thousand… mới nối số).
- **Q27 (khiếu nại 10/10): CHẤP NHẬN (1), (2); trả lời (3).** (1) `q27-score` gán khung theo **hạt giống ghi trong manifest** của lần chấm; (2) video hiện tại khác SHA trong manifest → báo "bộ chấm thuộc bản khác", in số của bản trong manifest, kết quả TRƯỢT; (3) **mọi lần đổi master sau Q27 phải chấm lại** (qua API: ≈ $0,8, ≈ 2 phút). Selftest tái hiện đúng số sai −0,11 (master phát hành `d22d7d6e…`) và số đúng −0,31 trên cùng câu trả lời. Kết quả chính thức tập 8 giữ **−0,31** (chấm trên `688b4fab…`).
- **Người chấm mù qua Claude API** (Q27, Q31, G1): `q_blind.py q27-run | q31-run | g1-run` thay subagent; mô hình ghim `claude-sonnet-5-5`; fail closed; chi phí ghi vào manifest. Từ 1.9.0 qc **không nhận** trả lời subagent.
- **Hiệu chuẩn Q27 API so với subagent: chênh > SE ở tập 7 (+0,55, +0,44) và tập 8 lần 2 (+0,34)** → K trình phương án cho chủ dự án (BAO-CAO mục 15.4). Bản khoá 1.9.0 đang theo phương án A (API, SE giữ 0,27); chọn khác thì K sửa và khoá lại.
- **Chủ dự án duyệt 1.9.0 (11/10/2026)** và chọn **Q27 = phương án A + đặt lại mốc**: API, 3 người chấm, SE 0,27. Từ tập 9, chấm kèm tập 8 bản phát hành (`d22d7d6e…`) so với tập 1; báo tập mới − tập 1 (ngưỡng), tập 8 − tập 1, tập mới − tập 8. K sửa mã và khoá **1.9.1** (LOCK `f777e0ca…`; BAO-CAO mục 16).

## Khiếu nại V — Q34(c) không tính số đặt trên cột 3D của bản đồ (12/10/2026, phiên V kênh 2, nhánh k2-visual)
Phiên V không đọc mã `checks/`; chỉ đọc `checks/ll/RULES-LL.md` và chạy `q_types.py` trên shot mẫu A (`channel-k2/k2v-mau/A-map-washington-brussels.yaml`, checks 1.10.1).
- **Hiện tượng:** shot `type: map` (`design/k2v/map.js`) đặt hai số neo (`t50`, `eu50`) lên **cột 3D nhô theo pháp tuyến địa cầu**, nhãn bám đỉnh cột. Q34 báo "(c) số neo hiện bằng chart3d/scene3d 0/2 = 0 % < 60 %".
- **Vì sao nêu:** Q34(c) đo "số đặt trong cảnh 3D thay vì thẻ phẳng" (bài học Steel: thẻ trên nền mờ). Cột số liệu trên bản đồ là đúng ý đó (số gắn với nơi chốn, vật thể 3D có tỷ lệ), nhưng bị đếm như thể không phải 3D. Nếu giữ, tập nào đặt số lên bản đồ sẽ phải vẽ lại cùng số đó bằng chart3d chỉ để qua thước (trái luật cứng "không thêm phần tử chỉ để vượt ngưỡng").
- **Đề nghị K:** tính `map` là hình 3D cho Q34(c) **khi** số neo bám vật thể 3D của bản đồ (shot `map` có `opt.cols` hoặc nhãn số bám neo `col:*`); số chỉ in chữ trên bản đồ phẳng thì vẫn không tính. Module xuất sẵn tên neo `col:<id>` trong `anchors.json` để đo.
- **Ghi thêm (không phải khiếu nại):** Q34(a), (b) trên shot mẫu trượt vì shot mẫu không có lời (không `.align.json`); Q32(b) trên mẫu C trượt vì shot mẫu 9,5 s toàn ảnh/văn bản (100 %). Cả ba là bản chất của shot mẫu, sẽ đo lại trong tập thật.

## Khiếu nại P — qc.py áp luật nhịp LL (Q14–Q18) cho tập kênh 2 vì mã tập "k2c-t1-06" (14/10/2026, phiên P kênh 2, nhánh k2c-t1-06)
Phiên P không đọc mã `checks/`; chỉ chạy `scripts/ll/qc.py` và đọc `checks/ll/RULES-LL.md`.
- **Hiện tượng:** trên K2G-01 (`k2g-ep01`) bảng QC ghi "Q14–18 · không áp (tập ≤ 3)". Trên K2C-T1-06 (`id: k2c-t1-06`) cùng bộ qc lại áp Q14, Q15, Q17 và đánh TRƯỢT (Q14 "tựa None · trả lời ở None"; Q15 quãng 17,2 s; Q17 "anchors không đúng 3 số"). Dấu hiệu: số tập được suy từ đuôi "06" của mã, nên tập kênh 2 bị coi là "LL tập 6".
- **Vì sao nêu:** kênh 2 không theo luật nhịp LL (K2G-01 G2 §5.1). Q17 ("anchors đúng 3 số") còn mâu thuẫn với Q34 của kênh 2 (anchors = mọi số neo, đo tỷ lệ hiện bằng 3D). Thay `anchors` để qua Q17 sẽ làm sai Q34.
- **Đề nghị K:** nhận diện tập kênh 2 (đường dẫn `channel-k2/` hoặc khoá kênh trong đặc tả) và đánh Q14–Q18 "không áp", như K2G-01; hoặc quy định rõ phần nào của Q14–Q18 áp cho kênh 2.
- **Phiên P không đổi gì** để vượt các mục này (không đổi id, không đổi anchors); báo cáo G2 ghi rõ ba mục TRƯỢT và lý do.

## Phán quyết K — checks 1.11.0 (15/10/2026; chủ dự án duyệt L6 và các quyết định 14–15/10 trong lệnh mở phiên K)
Báo cáo: `checks/K-1.11-BAO-CAO.md`. Nhánh `checks/v1.11` (chưa merge; P merge sau T2 G2, cùng `am-thanh`).
- **Khiếu nại P 14/10 — Q14–Q18 áp nhầm cho kênh 2 (k2c-t1-06): CHẤP NHẬN.**
  - **Nguyên nhân thật** (K đọc mã `scripts/ll/qc.py`): qc gọi Q14–Q18 khi đặc tả có `hook` **hoặc** `anchors`. Kênh 2 khai `anchors` cho Q34, nên T1 bị đo; K2G-01 không khai `anchors` nên ghi "không áp (tập ≤ 3)". Số tập suy từ mã (`ep(\d+)`) không khớp "k2c-t1-06", nên **không** phải nguyên nhân.
  - **Sửa ở luật khoá** (`checks/ll/q_rhythm.py`, không cần sửa `qc.py`): tập kênh 2 (đặc tả dưới `channel-k2/` hoặc mã tập bắt đầu bằng `k2`) → Q14–Q18 trả "không áp (kênh 2 …)", ĐẠT. Kênh 2 đo nhịp bằng **Q37** (nhịp thị giác, Kinh thánh §4) và số neo bằng **Q34**; Q17 "đúng 3 số neo" không áp.
  - Selftest (`selftest_k2.py`): T1 thật → 5/5 "không áp"; cùng dữ liệu T1 đội lốt tập LL → vẫn đo như LL (Q14, Q15, Q17 TRƯỢT — tái hiện đúng hiện tượng khiếu nại). LL tập 2–8: `selftest_ll.py` không đổi.
  - **Ảnh hưởng T1 G2:** ba mục Q14, Q15, Q17 TRƯỢT trong `g2/qc-v1.md` là áp nhầm, không phải lỗi của tập. Không cần làm lại gì.
- **Ghi thêm cho P (không phải khiếu nại):** `scripts/k2/rhythm.py` @T2 đọc `p.frame0`, nhưng `scripts/ll/ll.py` load() đổi tên `frame0` → `off`; trên đặc tả đã giải (est.py T2) mọi cảnh dùng lại bị coi là bắt đầu ở khung 0. Đo 15/10 trên T2: 5 biến cố khai lệch mốc thật (đoạn 01: 65,59 s, 67,97 s; đoạn 06: 37,77 s, 45,05 s, 54,97 s). Q37 của K đọc `off` khi thiếu `frame0`. Đề xuất P sửa `rhythm.py`/`est.py` ở T3.

## Phán quyết K — checks 1.11.1 (15/10/2026; chủ dự án duyệt O1, O2-B, O3, O4, O6)
- **Q-K111-3 (Q34(d) và văn bản gốc) → O2-B.** Thêm loại shot `record` (văn bản gốc: Federal Register, luật, thư, hợp đồng). Điều kiện:
  - ≤ 12 s mỗi shot;
  - bắt buộc có dòng tô hiện trong shot (`p.hl` hoặc `opt.hl` của cảnh);
  - phải dẫn nguồn; nguồn là luật thì khai `loai`/`hieu_luc`.
  - Trần 3 s của Q34(d) giữ cho ảnh chụp báo hiện đại.
- **Q-K111-2 ("Facts as of" trong câu miễn trừ) → O3 = B.** Được một lần, trong 0:00–0:15, khi khai `mien_tru: true`. Ngoài câu miễn trừ giữ luật 1.11.0.
- **Q-K111-1 (D5) → O4.** Giữ cách hiểu đã khoá: năm/ngày hiện trên khung thì miễn ACTUAL. `RULES-LL.md` ghi "duyệt 15/10".
- **T2 vẫn ghim 1.10.2:** 5 shot `document` của T2 vẫn trượt Q34(d) cho tới khi chủ dự án cho T2 áp riêng Q34(e), hoặc T2 rút các shot đó ≤ 3 s. Chi tiết: `checks/K-1.11-BAO-CAO.md` mục 1.11.1.

## Phán quyết K — checks 1.17.3 (23/10/2026; khiếu nại BAN-CUOI-T3 A1–A6, `reports/ban-cuoi-t3/checks-appeal.md`)
Báo cáo: `reports/k1173/K1173-BAO-CAO.md`; bảng quyết định chờ chủ dự án: `reports/k1173/QUYET-DINH-TREO.md`. Nhánh `checks-1-17-3` (không merge). Tái hiện trên đầu vào thật bản cuối T3 (`channel-k2/k2c-t3-01/cuoi` @origin/main 9852adf5 + master `k2-t3-v1-master.mp4` SHA `5b9f0bcc…`) trong thư mục tạm; `channel-k2/` không sửa. T3 đã phát hành (23/10 10:45 "không sửa thêm") — mọi "cách khai đúng" dưới đây là cho T4 trở đi.
- **A1 TL-3 sập khi `trong_pct` là danh sách — LỖI LUẬT, sửa.** Căn cứ: K117 §2.3 / RULES-LL 1.17 tự định nghĩa `trong_pct` = "số TB shot hoặc `[[t, %], …]`"; EO-DAT-R2 đọc được, TL-3 ép `float()`. Sửa: TL-3 lấy **trung bình theo thời gian** khi là danh sách (mẫu giữ tới mẫu sau); kiểu lạ → THIẾU, không sập. T3: 43 shot 3D, 0 lỗi (trống TB ≤ 60 %).
- **A2 Q37 (a) không đọc mốc trong `heroes.<k>.opt` — LỖI LUẬT, sửa (chỉ tập từ T3).** Căn cứ: Q37 (a) "biến cố khai phải khớp mốc thật của đặc tả"; cảnh `tl/*` đặt mốc ở `opt.time` và năm thế giới của lớp vật (Kinh thánh §13.6 TL-1 "trong shot, thời gian chạy (nhà mọc/cháy/sập, công trình có ngày đầu/cuối, tàu, ngày–đêm, khói)"), bộ đọc mốc 1.11 chỉ biết lớp bản đồ T1/T2. Sửa: mốc `opt.time[].t`, `smoke[].t`, mọi năm thế giới (wY/w/on/off/full/day/hoist/path, `nc.bakes`) quy về giây cảnh qua **bản sao độc lập `tl7.timeline`** (trùng tl7.js chạy bằng node: lệch 0 trên 147 điểm năm + 12 crossing), thẻ chương `p.the_chuong.at`. T3: (a) **207 → 69**. **69 còn lại là LỖI KHAI**: beat do thước xưởng `scripts/k2tl/cuoi_bien_co.py` tính (nội suy tuyến tính + `dy()` bỏ múi giờ LMT) lệch giờ trình dựng (vd. N2_7 "khói xuất hiện" khai 2,04/3,08/4,13/5,17 s, trình dựng 0,64/1,69/2,73/3,78 s — lệch 1,39 s), hoặc beat mô tả trạng thái ở 0,5/1,0 s không ứng mốc nào. Khai đúng cho T4: lấy giờ biến cố từ chính đường cong của trình dựng (tl7.timeline/crossings, hoặc `q_nhip.tl_moc_canh` của K), không tự nội suy; trạng thái có sẵn từ đầu shot không phải beat.
- **A3 EO-DAT-R3 (b) không tính cắt góc — LỖI LUẬT, sửa.** Căn cứ: Kinh thánh §14.7 R3 "Shot > 15 s chia 2–3 góc, **mỗi góc** có biến cố thấy được ≤ 6 s" — đầu mỗi góc là ranh như đầu shot (luật đã tính đầu/cuối shot); cắt góc R3 đã được nhận ở TL-1 (V2-D7, K1172-D2). Sửa: `goc_may[].t0|t` (> 0) là ranh; mốc quy về lưới khung (round(t·24)/24) — video không hiện biến cố giữa hai khung. T3: (b) 5 → **0**; **N5_1 đúng ngưỡng 6,00 s** (144 khung; ±5 %). Đề xuất K1173-D2.
- **EO-DAT-R3 (a) N4.5 (27,2 s), N5.6 (20 s) một góc — LỖI PHIM theo chữ R3; luật giữ, KHÔNG tự cho đạt.** Chủ dự án 23/10 10:45 "không muốn sửa thêm" là quyết định không sửa phim, chưa phải duyệt ngoại lệ R3. 1.17.3 thêm **đường ngoại lệ có khai**: log shot `r3_ngoai_le: {ly_do, authorship: "YYYY-MM-DD HH:MM"}` chỉ được nhận khi AUTHORSHIP.md có dòng cùng ngày giờ nêu id shot và "R3". Hiện chưa có dòng → (a) vẫn TRƯỢT. Chờ chủ dự án: K1173-D1.
- **A4 PP-1 đếm cả tiêu đề "How this film was made" — LỖI PHIM/KHAI, giữ luật.** Căn cứ: K116-D8 (duyệt 19/10 18:48) "'≈ 8 s' = 7–9 s, ≤ 3 từ/s" và lệnh "7–9 s mỗi thẻ, ≤ 3 từ/s" đo tốc độ đọc **mỗi thẻ**; tiêu đề là chữ trên thẻ người xem phải đọc (§12.1 (b) gọi thẻ bằng chính tiêu đề). PP1 = 31 từ / 9 s = 3,44 từ/s → (e) **Cảnh báo** (không chặn). Khai đúng cho T4: ≤ 27 từ cả tiêu đề cho thẻ 9 s, ≤ 24 từ cho thẻ 8 s. Xác nhận: K1173-D3.
- **A5 Q33 N1_6 ×3 — LỖI LUẬT, sửa.** Căn cứ: §13.6 TL-1 "mỗi phần phim quay lại cùng điểm máy ở **năm khác**". Miễn 1.17 so khoảng [min, max] của `nam` log; N1_6 khai [1704,8; 2026,79] nhưng đường cong `opt.time` NHẢY (1705,3 → 1727,15 → 1735,4 → 2026,78 trong 0,05 s) — năm 1782 và 1900–1930 không hề hiện. Sửa: năm của miễn = **các khoảng năm hiện trên hình** đọc từ `opt.time` (bản sao tl7; hai mốc cách ≤ 3 khung = bước năm, tách khoảng, khung giữa bước bỏ); đoạn không có `opt.time` → năm log như 1.17. T3: N1_6 hiện 1704,8–1705,3 · 1727,15–1727,45 · 1730–1735,4 · 2026,78–2026,79 → N2_10 (1782), N3_4 (1900–1930) miễn → Q33/Q33-K2/Q33 (1.13) **ĐẠT** (xem bảng so ở báo cáo).
- **A6 SACH-1 thẻ chương + thẻ PP "ngoài danh sách", chữ PP2 — LỖI LUẬT một phần, sửa; tên vai log là LỖI KHAI.** Căn cứ: §13.3 "Thẻ chương (ngoại lệ của §12.1)"; §12.1 (b) đưa "chỗ nào là ước tính" lên thẻ "How this film was made" (chữ "illustrative" ở thẻ PP2 là đúng chỗ). Luật chỉ nhận theo tên vai (`the_chuong`, `the_phuong_phap` — K117 §3), trong khi CHUONG-1 và PP-1 cùng lượt đã nhận đúng thẻ theo đặc tả. Sửa: chữ trong khoảng giờ đoạn thẻ PP được bỏ qua ở SACH-1 (PP-1 xét nội dung); chữ trùng nguyên văn `p.the_chuong` trong [at, at + dur] ± 1 bước mẫu được bỏ qua (CHUONG-1 xét dạng/thời lượng); ngoài hai khoảng đó vẫn lỗi như cũ. Khai đúng cho T4: log render ghi vai `the_chuong` cho thẻ chương và `the_phuong_phap` cho chữ thẻ PP. Xác nhận: K1173-D5.
- Selftest `checks/ll/selftest_k1173.py` 42/42 (mỗi luật đổi ≥ 1 ca đạt + ≥ 1 ca trượt); selftest cũ k112…k1172, k2, ll giữ nguyên kỳ vọng. LOCK 1.17.2 `aca05e60…` → **1.17.3 `d99af8f2…`** (`--verify` KHỚP). Trên bản cuối T3: Q33-K2, Q33 (1.13), SACH-1 TRƯỢT → ĐẠT; TL-3 CẢNH BÁO → ĐẠT; EO-DAT-R3 7 → 2 (chỉ (a)); Q37 209 → 71.

## Phán quyết K — checks 1.17.4 · D11 phép (iii) bộ kiểm N2P (23/10/2026; chủ dự án duyệt Q7 23/10 21:45, PHIEU-G1 TIEN-KY-T4 D11)
Báo cáo: `reports/k1174/K1174-BAO-CAO.md` §1; số đo + script tái hiện: `reports/k1174/do/d11-t6-iii.json`, `reports/k1174/do/d11_tai_hien.py`. Nhánh `checks-1-17-4` (không merge).
- **Khiếu nại (TIEN-KY-T4, T6):** N2P-3 (a) T9b "nước → đất" trượt 0/3 lượt (lượt 2: 2,42 % > 2 %); phiên tiền kỳ cho rằng do dải "biển" giả ở chân trời ngoài hộp địa hình + mặt nạ JPEG; đề nghị chỉ đo trong vùng địa hình đã dựng, mặt nạ PNG.
- **Tái hiện:** ghép lại cả 3 lượt từ đầu vào gốc trong git (`channel-k2/k2c-t4-02/ai/goc/T6-*`) bằng `scripts/k2ldn/t6_ghep.py` nguyên bản → SHA ảnh ghép **trùng từng bit** sổ kiểm (l1b `cb59edc0…`, l2 `5cc3a4b6…`, l3 `d5de5127…`); `q_n2p.do_tam` (1.17.3) cho đúng số tiền kỳ: l2 T9b nước→đất **2,42 %**, đất→nước 0,01 %.
- **Kiểm giả thuyết của khiếu nại bằng số đo:**
  - Dải "biển" chân trời (thành phần nước riêng, y 273–328, 60 947 điểm mẫu số): đóng góp **0 điểm** vào tử số lượt 2 (lượt 1: 4 403 / 258 471 điểm = 1,7 % của lỗi). Bỏ dải này (đo chỉ trong vùng địa hình hợp lệ) → lượt 2 **2,67 %** (tăng, vì dải chỉ làm to mẫu số). Đo với render thô (không khớp màu) → cũng 2,67 %.
  - Mặt nạ JPEG: chỉ ảnh hưởng (i); (iii) lượt 1 JPEG ↔ 1b PNG **trùng 42,24 %**; mặt nạ lượt 2 vốn là PNG.
  - Nguồn thật của 15 781 điểm lượt 2 (đều ở sông chính): **sát bờ bắc ≤ 40 px: 1,49 %** — AI vẽ bãi/bến lấn ra sông 8–40 px so đường bờ của mặt nạ (đường bờ là lớp dữ kiện hình học §15 (a)), cụm lớn nhất x 666–715, y 694–735 (bến nhô/inlet) và x 157–233, y 717–780; **giữa nước 0,93 %** — vệt phản chiếu nhà dọc (x 520–600, y 700–1000) và loé nhạt dưới ngưỡng loé (lý do mất "màu nước": 85 % nhạt S < 40, 15 % lệch sắc).
- **Phán quyết: LỖI ẢNH — giữ luật, giữ ngưỡng 2 %.** Theo đúng cách sửa khiếu nại đề nghị (vùng hợp lệ, PNG), phần đo hợp lệ **vẫn vượt (2,67 %)**; giả thuyết "dải biển giả" bị số đo bác. Ảnh sai ở: (1) đường bờ bắc dịch vào sông (1,49 % sát bờ — lỗi hình học lớp (a), không phụ thuộc cách đo màu); (2) mặt sông giữa có phản chiếu/nhạt màu đọc như mất nước (0,93 %). Lượt 1: cả sông chính nhạt xám (S trung vị 25) — 42,24 %; lượt 3: bãi cát trong phố thành nước (đất→nước 20,63 %, 2 mô hình cùng báo) — đều LỖI ẢNH.
- **Không sửa luật trong 1.17.4.** Phần (2) có thể là báo nhầm của thước màu với phản chiếu đúng vật lý (mặt nước là lớp nền, AI tự do về bề mặt) — nhưng chưa có khung đáp án phân biệt "phản chiếu" với "bãi lấn"; nới bằng suy đoán là trái "không nới nếu phần đo hợp lệ vẫn vượt". Đề xuất cho chủ dự án: **K1174-D1** (báo cáo §9): một phiên K riêng dựng bộ khung đáp án (bãi/bờ lấn chèn + phản chiếu thật) rồi mới quyết có miễn phản chiếu hay không; tới lúc đó phía dựng: giữ đường bờ của render (ghép lại dải bờ ± 8–40 px từ render như lớp (a)), lệnh không xin "reflections", hoặc kiểm từng tấm trước khi dùng.
- **Cách khai cho T4 (không đổi):** `n2p.tam[]` {render, ghep (PNG), mat_na (PNG)}; `render` = render đã khớp màu dùng làm tham chiếu (i). Thêm (tuỳ chọn, không đổi kết quả): `reports/k1174/do/d11_tai_hien.py` in vị trí điểm lỗi theo khoảng cách bờ để phía dựng sửa đúng chỗ.

## Khiếu nại cho K-1.17.5 (ghi 24/10/2026 01:15 UTC, TRƯỚC khi phán; nguồn: lệnh mở phiên K-1.17.5 — chủ dự án 24/10/2026 06:21 "1. Chọn phương án A+B theo khuyến nghị", K1174-D1 = A duyệt 24/10)
- **A1 (K1174-D1 = A):** phép (iii) N2P-3 tính phản chiếu thật trên mặt nước như "nước→đất". Yêu cầu: dựng khung đáp án phân biệt phản chiếu thật với bãi/bờ lấn, rồi quyết miễn phản chiếu trong (iii).
- **A2 (LOOK-T4-V2 §11 (2)):** T9b dùng định nghĩa "màu nước" HSV tuyệt đối → AI đổi nước sang xám/ô-liu bị tính "nước→đất" dù vẫn là nước (Gemini 19–69 %). Yêu cầu: đo đường bờ/hình học thay vì chỉ sắc, nhưng vẫn bắt bờ lấn 8–40 px như D11.
- **A3 (PHIEU-LOOK-V2 V3):** phép (i)/(iv) cho lớp sống (khói bếp) ghép bằng CỘNG HIỆU render có/không khói — khói không thuộc lớp (a) nên không qua (i) 0/255; mô hình nhìn báo khói là vật chuyển động.
- **A4 (PHIEU-LOOK-V2 V4 (b)):** khớp màu cục bộ trong vòng bảo vệ vật nhỏ lớp (a) (< 60 px, nở 3 px) — quầng 1–2 px quanh nhà xa làm (iv) trượt.
- **A5 (mới, phương án B):** phép kiểm "BE-MAT-NHA" cho ảnh AI phủ bề mặt nhà thường không tên (hình khối, lớp (a) còn lại 0/255, lỗi thời đại vật liệu, ổn định theo thời gian, hai cách dùng ảnh tĩnh/chiếu 3D).

## Phán quyết K — checks 1.17.5 · A1–A5 (24/10/2026; báo cáo `reports/k1175/K1175-BAO-CAO.md`; nhánh `checks-1-17-5`, không merge)
Khung đáp án (tiêu chí đặt TRƯỚC khi đo, chọn tham số ở nửa A — T6 lượt 1/2 + cảnh Blender máy P1 hạt 1 — rồi KIỂM ở nửa B — T6 lượt 3 + cảnh Blender máy TRUNG hạt 2): (1) bắt 100 % bờ lấn ≥ 8 px @1080; (2) 0 báo nhầm ở nước đổi sắc (xám/ô-liu/nâu/nhạt) giữ bờ và ở phản chiếu VẬT LÝ có trong render (Cycles); (3) T6 lượt 2 thật (D11) vẫn trượt. Mặt nạ ID look2 KHÔNG có trong git (ở /var/tmp phiên LOOK) → ảnh look2 chỉ đo chỉ báo bằng mặt nạ suy từ render, không dùng để phán.
- **A2 (đổi sắc nước) — LỖI LUẬT, sửa (1.17.5).** T9b "màu nước HSV tuyệt đối" tính nước ô-liu là đất (đối chứng: T6 render + nước ô-liu, bờ giữ: T9b nước→đất 91,1 %). Thay chiều nước→đất bằng **T9c** (đối chứng render: tấm ≈ T(render), T affine Lab khớp bền trên vùng nước; đo độ sâu khác-nước theo cửa sổ từ đường bờ). τ0 chọn ở nửa A = 6 (5: hỏng ca âm Blender; 7–8: sót bến gỗ tối 8 px). Nửa A: bờ lấn ≥ 8 px 15/15 (2D) + 18/18 (Blender), ca âm 4/4 + 6/6 đạt; **nửa B (kiểm): 15/15 + 14/14 bắt, 4/4 + 6/6 âm đạt.** T6 lượt 1/2/3 thật vẫn TRƯỢT (l2: bờ bắc lấn, đoạn sâu 22 px — đúng D11). Gemini M1-trung-gem-l1 (T9b 80,5 %, mặt nạ suy): T9c ĐẠT.
- **A1 (phản chiếu) — MỘT PHẦN.** (1) Phản chiếu có trong RENDER 3D (vật lý) được giữ tự động nhờ đối chứng render: Blender phản chiếu vật lý ở 3 độ nhám × 4 sắc nước: 11/11 ca đạt, bờ lấn trước dãy nhà có phản chiếu vẫn bắt. (2) Phản chiếu do AI TỰ VẼ (render không có) **KHÔNG được miễn**: đã thử phân biệt bằng hình học trục gương + vật cao + pha màu α + tương quan — luật 0 lọt bờ lấn chỉ miễn ≈ 48 % dải phản chiếu tổng hợp và 0 % phản chiếu vật lý (phần dư màu 0,6–0,9); không đạt độ nhạy 100 % → không nới. Muốn có phản chiếu: dựng trong 3D.
- **A3 (lớp sống cộng hiệu) — LỖI LUẬT, sửa (1.17.5).** Luật cũ không có phép cho lớp sống. Thêm N2P-1 (e): ghép == clip(nền + (render có − render không)) ≤ 1/255 ngoài vùng bảo vệ (đúng 0; dán nguyên kiểu T6 8–72; lệch 6 px 38–50; nửa cường độ 18–22 → trượt), và (iv) soi tấm nền. Ca (iv) của M1-rong-oai-l3h không tái hiện được trong phiên (tấm ghép ở /var/tmp phiên LOOK); số LOOK: biến thể nhà xa lớp (c) 0 báo (iv) → nguyên nhân (iv) là quầng (A4), không phải khói.
- **A4 (khớp màu cục bộ vòng bảo vệ) — KHÔNG phải lỗi mã K; cần chủ dự án sửa chữ Kinh thánh §15 (a).** (i) của K chỉ đo TRONG mặt nạ (a) (không đo vòng nở 1/3 px) — ràng buộc vòng = render là chữ Kinh thánh. K thêm phép kiểm được (d) cho trường hợp chủ dự án cho phép (K1175-D3): vòng = render-khớp + một độ lệch/vật (phần dư ≤ 1/255, |độ lệch| ≤ 40); T6: (i) giữ 0/255, phần dư 1. Không tái hiện được quầng M1-rong (thiếu mặt nạ look2); trên T6 chênh tông cục bộ không giảm sau khớp (ΔE vòng↔AI 8,1–9,4 trước/sau) → lợi ích chưa có số đo trong phiên.
- **A5 (BE-MAT-NHA) — luật MỚI, một phần đạt yêu cầu.** (b) khoá 0/255, (c) thời đại (v2: 5/5 vật hiện đại vẽ thêm bị cả hai mô hình + q_thoi_dai bắt; 0 báo trên 2 ảnh AI thật sạch), (d) quỹ đạo sáng/nhấp nháy, (e) khung 0 chiếu 3D: đạt tiêu chí ở cả hai nửa. **(a) hình khối KHÔNG đạt yêu cầu "bắt 100 % nhà dời ≥ 2 m hoặc đổi mái":** ở 1,4–4,8 px/m (máy P1/TRUNG), điểm bắt 100 % (nửa TRUNG, ≥ 3 px/m, ≥ 40 điểm cạnh) báo nhầm 3,4 % nhà chỉ đổi bề mặt; điểm 0 báo nhầm (đỡ cạnh < 0,20) chỉ bắt xoá nhà (3/3) — dời 0/11, đổi mái 0/9. → (a) Chặn chỉ phần thô; phần còn lại Cảnh báo người đọc; nhà không đo được phải giữ render (b). Quyết định cách đi tiếp: K1175-D5.

## Khiếu nại cho K-1.17.6 (ghi 24/10/2026 08:34 UTC, TRƯỚC khi phán; nguồn nguyên văn: `origin/ccr-ce664665-996oyl` @353d0f0c `reports/thu-b-t4/khieu-nai-K.md` — phiên THU-B-T4; lệnh mở phiên K-1.17.6 kèm căn cứ chủ dự án 24/10 12:52 và 15:25, giờ Asia/Saigon)

### Khiếu nại cho phiên K (THU-B-T4 → P chuyển vào `checks-appeal.md`; phiên xưởng không sửa `checks/`, không đọc mã `checks/`)

> Căn cứ: chạy `checks/ll/k2check.py` 1.17.5 (LOCK `c7630b4a…` KHỚP) trên các tấm BE-MAT-NHA của vòng thử. Bằng chứng: `channel-k2/k2c-t4-02/thu-b/kiem/*/k2check.md` (nguyên văn đầu ra + stderr).
> Ghi chú minh bạch: dòng mã trích dưới đây là **traceback Python in ra khi chạy** `q_n2p.py` (không mở tệp mã để đọc).

#### KN-1 · N2P-1/2/3/4/5/6 "không chạy được: 'so_doan_lan'" khi khung KHÔNG có nước
- Hiện tượng: tấm M4-trung (2026, mặt phố Fleet St) và B3-p4-1938 (Ludgate Hill) — khung không có điểm nước nào trong mặt nạ lớp. Cả 6 hàng N2P đều "không chạy được: 'so_doan_lan'" (Chặn ở G2). Chạy riêng `q_n2p.py episode.yaml --tl timeline.json` ra traceback: `q_n2p.py, line 276, in tong_tam … sum(c['so_doan_lan'] for c in c9s) … KeyError: 'so_doan_lan'`.
- Tách theo nguyên nhân (BAI-HOC-K2 K48): cùng cách khai, tấm M1-trung (CÓ sông) chạy đủ N2P-3 (T9c: 0 đoạn bờ lấn, giữa nước 0 %). Lỗi chỉ xuất hiện khi một tấm không có nước → bản tóm tắt T9c gộp kết quả không có khoá `so_doan_lan`.
- Đề nghị: T9c trả `so_doan_lan = 0, sau_lon_nhat_px = 0, giua_pct = 0` (hoặc "KHÔNG ÁP — không có nước") cho khung không nước; thêm 1 ca selftest khung không nước.

#### KN-2 · N2P-1 (i) tính vùng nhà ĐO ĐƯỢC của tấm `be_mat_nha_ai` là lớp (a) → mọi tấm BMN trượt N2P-1 (a)
- Hiện tượng: M1-trung lượt 1/2 — N2P-1 (a) "lớp (a) sau ghép lệch tối đa 192/255 (l1), 218/255 (l2) ở 566 433 / 566 426 điểm". Số điểm này trùng vùng AI được phép của BE-MAT-NHA: vùng ghép AI = nhà đo được nở 1 px = **27,67 % khung = 573 766 điểm** (`tam/M1-trung/l*/ghep.json`); 566 433 = số điểm trong vùng đó có giá trị khác render (phần còn lại trùng ngẫu nhiên).
- Đo của phiên (ngoài k2check): trong mặt nạ (a) TRỪ lớp `nha_thuong` (215, 215, 215): max |ghép − render| = **0/255** ở cả 3 khung; BE-MAT-NHA (b) của chính k2check: **0/255** ở mọi tấm.
- Thử khai `lop_a` (danh sách lớp (a) không gồm `nha_thuong`, trường có trong RULES 1.17.0): KHÔNG đổi kết quả (`kiem/M1-l1-lopa/`). Phiên không thử thêm cách khai nào khác (không đoán).
- Đề nghị: với tấm `be_mat_nha_ai: true`, N2P-1 (i) loại vùng "nhà đo được nở 1 px" khỏi mặt nạ (a) (vùng đó do BE-MAT-NHA (a)(b) kiểm), giữ (i) cho mọi điểm (a) còn lại — đúng chữ RULES 1.17.5 "BE-MAT-NHA (b) mọi điểm ngoài nhà đo được (nở 1 px) = render 0/255".

#### KN-3 · Mô hình nhìn Claude "không đọc đủ ảnh" ngẫu nhiên → (c) THIẾU (Chặn)
- Số lần: B3 lượt 1 (lần chạy 2: đọc 6/10 ảnh), M4-trung lượt 1 và 2, M1-trung lượt 2 — cùng một lời gọi, có lần đọc đủ 10/10 (B3 lượt 2, M1 lượt 1). Chi phí mỗi lần ≈ $0,04–0,07.
- Đúng thiết kế fail-closed (K-1.17.5 §5.2). Đề nghị: tự gọi lại 1 lần khi thiếu ảnh (như Q27/Q31 "sau 1 lần gọi lại"), ghi cả hai lần vào `n2p-cost.jsonl`.

#### KN-4 (ghi nhận, không phải lỗi mã) · (a) hình khối KHÔNG bắt vật AI vẽ thêm TRONG bóng nhà
- B3 lượt 1: k2check (a) 0 Chặn, 0 (w); nhưng gpt-6.1-sol báo 10 (w) "thêm ống khói/chụp ống, đổi đầu hồi" và ô phóng (`tam/B3-p4-1938/l1/soi-a.jpg`) thấy ống khói AI vẽ thêm. Đỡ cạnh hình học (biên nhà ∪ mặt phẳng) không giảm khi AI THÊM chi tiết bên trong bóng nhà. Hiện chỉ mô hình nhìn (w) + người đọc bắt được. Đề nghị K xét phép "cạnh màu MỚI không có ở render và pass bóng" trong lòng nhà (như (c) cụm ΔE của N2P-1) — chỉ báo.

#### KN-5 · (d) quỹ đạo sáng theo nhà báo lỗi cả khi dựng lại ánh sáng ĐÚNG (chiếu theo tỉ số bóng)
- Cách (ii-b) "chiếu theo tỉ số bóng render" (máy cố định): trong nhà đo được C(t) = tấm × R(t)/R(0) từng điểm ảnh (sRGB tuyến tính) — đúng bằng chiếu albedo AI đã khử sáng (tấm/bóng(0)) rồi nhân bóng(t); nhấp nháy 0 về lý thuyết.
- k2check (video không mất, crf 0 yuv444p): B3-p4-1938 lượt 2 — nhấp nháy ĐẠT, (e) ĐẠT, nhưng (d) **7,2 % nhà** có e_h > 0,10 (trần 2 %). Phiên tính lại e_h trên khung PNG theo đúng chữ RULES 1.17.5 (d): **11/153 nhà = 7,2 %** (trùng k2check). Tách nguyên nhân (`tam/B3-p4-1938/l2/phan-tich-d.json`): nhà lệch có độ quét bóng trong nhà sd(ln q) trung vị **0,47** (nhà không lệch 0,26) và độ đổi albedo AI sd(ln I/R0) **0,48** (0,38) — tức lệch xảy ra khi đường bóng quét QUA một nhà mà AI đã phân bố lại độ sáng bề mặt (cửa tối/tường sáng ở chỗ khác render): trung bình theo nhà của ảnh đúng vật lý vẫn khác quỹ đạo của render.
- Đề nghị: đo (d) theo TỪNG ĐIỂM ẢNH (ln(C(t)/C(0)) − ln(R(t)/R(0)), trung vị theo nhà) thay cho tỉ số trung bình theo nhà, hoặc giữ thước hiện tại nhưng chuẩn hoá theo độ quét bóng; thêm ca selftest "albedo phân bố lại + bóng quét" (khử sáng đúng phải đạt).

#### KN-6 · (e) khung 0 chiếu 3D so video 640×360 với tấm 1080p → sai số phóng/thu chiếm ngân sách ΔE
- B3-p4-1938 lượt 2, chiếu 3D (ii-a) sau 3 vòng hiệu chỉnh ở 640×360: khung 0 video (PNG trước mã hoá) so tấm thu INTER_AREA về 640×360 — trong nhà đo được ΔE76 TB **2,19 / p95 6,48** (`tam/B3-p4-1938/l2/khung0-360-de.json`); trên cả lớp nhà thường 2,32 / 7,21.
- k2check (video không mất crf 0 yuv444p), `tam` = tấm 1080p: (e) **TRƯỢT 4,6 / 12,6**; cùng video, `tam` = tấm thu về 640×360 (INTER_AREA): (e) **ĐẠT** (`kiem/B3-l2-tam640/`). Cách (ii-b) tỉ số bóng (khung 0 = tấm thu về 640×360 từng điểm): (e) ĐẠT cả hai.
- Đề nghị: RULES ghi rõ (e) so ở độ phân giải VIDEO (thu `tam` bằng INTER_AREA) hoặc bắt buộc video kiểm cùng độ phân giải tấm; selftest có ca video 640×360 + tấm 1080p.

#### Yêu cầu kèm theo của lệnh K-1.17.6 (không phải khiếu nại; căn cứ chủ dự án, Asia/Saigon)
- 24/10 12:52 "Duyệt cách kết hợp tư liệu theo khuyến nghị": trần tư liệu + khắc + thẻ của T4 = 15 % (thay 10 %); tư liệu chỉ chồng lên shot 3D, không chồng/ghép liền với clip Omni; mỗi lần ≤ 10 s → TU-LIEU-10 thành tham số theo tập `tu_lieu_tran_pct` + phép mới "không trùng/không ghép liền clip M-d" và "mỗi lần ≤ 10 s".
- 24/10 15:25 trả lời phiếu THU-B "theo khuyến nghị": B chỉ ở nhà ≥ 4 px/m (cách tỉ số bóng khi máy cố định, chiếu 3D khi máy di chuyển; D 3D không vân nướng; nâng vật liệu 3D toà 2026 có tên) → BE-MAT-NHA (a) đọc `be_mat_nha_px_m_min` (mặc định 2; T4 khai 4).

## Phán quyết K — checks 1.17.6 · KN-1…KN-6 + tư liệu T4 + B ≥ 4 px/m (24/10/2026; báo cáo `reports/k1176/K1176-BAO-CAO.md`; nhánh `checks-1-17-6`, không merge)
Tái hiện bằng tấm thật của THU-B (`origin/ccr-ce664665-996oyl` @353d0f0c, `git archive`, không sửa); video kiểm không mất tái tạo bằng đúng mã THU-B (dữ liệu nền `ldn2.bin` bd776509… trùng): B3 và M1 trùng SHA `video-sha.json` 3/4 video (render, ảnh tĩnh, tỉ số bóng), chiếu 3D và M4 khác SHA nhưng 1.17.5 trên bản tái tạo cho ĐÚNG từng số của THU-B. Tiêu chí đặt TRƯỚC khi đo (theo lệnh): KN-1 không lỗi chạy + khung không nước KHÔNG ÁP (iii); KN-2 (a) còn bắt mọi điểm (a) ngoài vùng nhà đo được; KN-3 gọi lại 1 lần, sổ ghi cả hai; KN-4 100 % ống khói thêm ở báo nhầm thấp mới đề xuất Chặn; KN-5 dựng lại ánh sáng đúng ĐẠT, dán tĩnh + nhiễu mỗi khung TRƯỢT; KN-6 (e) so ở độ phân giải video.
- **KN-1 — LỖI MÃ, sửa.** `q_k1175.t9c` trả sớm (không lớp nước / nước < 0,2 % khung — B3 có 213 px nước) thiếu khoá `so_doan_lan` → `q_n2p.tong_tam` KeyError, cả 6 hàng N2P "không chạy được". Sửa: T9c trả đủ khoá + `ap: False`; tấm không nước → T9c KHÔNG ÁP, T9b đất→nước + mô hình (b) vẫn chạy; mọi tấm không nước, 0 lỗi → N2P-3 KHÔNG ÁP. Tái hiện: 1.17.5 KeyError trên `kiem/M4-l12`, `kiem/B3-l2`; 1.17.6: N2P-1…6 chạy.
- **KN-2 — LỖI LUẬT (1.17.5 không định nghĩa quan hệ N2P-1 ↔ BE-MAT-NHA), sửa.** Lớp `nha_thuong` (215) rơi vào màu gần nhất `nha` (235) của bảng N2P → (a). 1.17.6: tấm `be_mat_nha_ai` trừ vùng nhà đo được nở 1 px (cùng định nghĩa + cùng ngưỡng px/m với BE-MAT-NHA) khỏi (i)(a) và dải 20 px (i)(c). M1 l2 / B3 l2 / M4 l2: (a) 218 / 224 / 183 → **0/255** (557 / 153 / 14 nhà đo được, khớp prep.json THU-B). Đạt/trượt (selftest): AI lấn công trình có tên hoặc nhà không đo được → (a) vẫn trượt.
- **KN-3 — chấp nhận (cải tiến vận hành), sửa.** Tần suất Claude đọc thiếu ảnh: 4/14 lần ở THU-B; phiên này 0/2 lần gọi thật (M4 l1, B3 l1, $0,20). Gọi lại MỘT lần khi thiếu ảnh (BMN (c) và N2+), mỗi lần một dòng `n2p-cost.jsonl`; thiếu cả hai → THIẾU. Đường gọi lại kiểm bằng selftest (mô hình giả lập).
- **KN-4 — ghi nhận, thêm phép CHỈ BÁO (w); KHÔNG đề xuất Chặn.** Đáp án lập bằng mắt trước khi đo: B3 l1 20 ống khói + 2 đầu hồi đổi thành mái; l2 0. Ống khói AI vẽ ĐÈ lên nhiều mã nhà (3D phía sau là tường nhà xa) nên mọi thước theo nhà/mặt phẳng hụt (≤ 4/20). Thước chọn: cạnh màu mới không được cạnh render/pass bóng cùng hướng giải thích → bắt **15/20** ống khói l1; 2 đầu hồi chỉ "trùng hộp" nhờ cửa sổ bên trong (không bắt được đường mái mới); báo nhầm 23 cụm ở l2 sạch (đa số cửa sổ AI lệch cửa sổ render). Lưới 96 điểm vận hành: không điểm nào 100 %. → (w) người đọc + mô hình nhìn `hinh_khoi` + lời nhắc bmn-v2b.
- **KN-5 — LỖI LUẬT, sửa (một phần ảnh).** (d) đo theo điểm ảnh (trung vị theo nhà của ln C(t)/C(0) − ln R(t)/R(0)), sàn Y ≥ 0,01 (lượng tử 8 bit khi nắng tắt — chọn trên M1, ghi rõ). Tỉ số bóng (ii-b): B3 7,2 % → **0 %**, M4 7,1 → **0 %**, M1 32,1 → **1,6 %** (ĐẠT); nhấp nháy tỉ số bóng B3/M4 đạt, M1 0,0119 sát trần (thước nhấp nháy chưa có sàn Y — K1176-D6). Ảnh tĩnh vẫn TRƯỢT (85,5 / 99,8 / 64,3 %). **Chiếu 3D trong trình dựng (ii-a) vẫn TRƯỢT — LỖI ẢNH (giữ):** B3 9,4 %, M4 7,1 %, M1 26 %; soi nhà B3 35893 (2 396 điểm lõi): C(t)/C(0) = 1,53 so render 1,27 — tường sáng lên nhiều hơn render khi nắng đổi (bản dựng ii-a không tái tạo đúng ánh sáng, không phải lỗi thước).
- **KN-6 — LỖI LUẬT, sửa.** (e) so ở độ phân giải video (khung 0 đọc cỡ gốc; tấm thu INTER_AREA; mặt nạ NEAREST). Chiếu 3D: B3 4,6/12,6 → **ĐẠT**, M4 4,8/14,7 → ĐẠT, M1 4,9/12,9 → ĐẠT (số ở báo cáo §KN-6).
- **B ≥ 4 px/m (15:25) — luật mới:** `be_mat_nha_px_m_min` (mặc định 2, < 2 không nhận); T4 khai 4 → nhà 2–4 px/m phải = render ((b)).
- **Tư liệu T4 (12:52) — luật mới/đổi:** TU-LIEU-10 đọc `tu_lieu_tran_pct` (mặc định 10, > 15 không nhận) + (b) mỗi lần ≤ 10 s; TU-LIEU-OMNI (a) không trùng clip M-d, (b) không ghép liền (≥ 1 shot 3D hoặc ≥ 1 s 3D). P ghi ngoại lệ T4 vào Kinh thánh §19 (c).

## Khiếu nại cho K-1.17.7 (ghi 25/10/2026 02:35 UTC, TRƯỚC khi phán; nguồn nguyên văn: `reports/animatic-t4/ANIMATIC-T4-BAO-CAO.md` §9.3 (sha256 `9111538d…`) và `reports/animatic-t4/PHIEU-XEM.md` C11, C13 (sha256 `74d3fb08…`) — phiên ANIMATIC-T4, trên origin/main @2a49e3ca; lệnh mở phiên K-1.17.7 kèm căn cứ chủ dự án 25/10 06:56, 09:08, 09:15, giờ Asia/Saigon)

### Câu hỏi cho K (ANIMATIC-T4 §9.3, nguyên văn)
- **A1.** K1174 §5 nói `log_may` = log.json `render_ldn.js` (ghi [E, N, h]) nhưng MAY-19 đọc hệ cảnh → xin ghi rõ hệ toạ độ trong RULES-LL (hoặc MAY-19 dùng `goc_toa_do` để đổi).
- **A2.** MAY-19 (c) H5-07b KHOP "lệch 62 139 px": tự chiếu điểm neo [532118, 181150, 111] qua ma trận máy → **0 px** giữa hai nửa a/b và với khung đầu M03; xin xem cách (c) chọn khung so khi `khop_voi` là shot DAY.
- **A3.** K-LAI-1 (≤ 20 % `ai_image`) mâu thuẫn Q2/1.17.4 (bỏ trần 20 % M-d từ T4) ở đúng dải Q1 20–23 %.
- **A4.** Q37 (a): lớp chồng mờ vào 0,4–0,5 s → biến cố đo trễ > 0,3 s so với mốc khai; phiên không dịch mốc để khớp thước.
- **A5.** N2P-1…5 báo "chưa khai `n2p.tam`" dù log shot có `n2p: {tam: [{tag, kiem, ghep, v, khoang_s}]}` — xin khuôn đúng.

### PHIEU-XEM C13 (nguyên văn)
**C13 — (thông tin, cần K trả lời) cách khai log máy và KHOP H5-07b.** (1) K1174 §5 nói `log_may` = log.json của `render_ldn.js` (ghi `cam.p` theo [E, N, h]), nhưng MAY-19 đọc `cam.p` theo hệ cảnh y-lên (như log T3) → phiên ghi thêm `cam` hệ cảnh, giữ `cam_en` gốc (cùng số liệu, đổi trục). (2) H5-07b KHOP báo lệch 62 139 px; tự chiếu điểm neo qua ma trận máy: 0 px giữa hai nửa và với khung đầu M03 — đề nghị K xem cách MAY-19 (c) chọn khung so khi `khop_voi` là shot DAY.

### PHIEU-XEM C11 (nguyên văn; chủ dự án 25/10 06:56 "C11, C13 theo khuyến nghị")
**C11 — K-LAI-1 = 20,4 % > 20 % (k2check 1.17.4, Chặn P2-2).** Q1 (chủ dự án) duyệt M-d 20–23 % và 1.17.4 (Q2) bỏ trần 20 % ở MINH-HOA, nhưng K-LAI-1 vẫn tính `ai_image` ≤ 20 % trên cùng 23 đoạn — hai luật mâu thuẫn ở đúng dải Q1 (số nằm trong ±5 % quanh ngưỡng: 20,36 %).
- (a) Đề nghị K sửa K-LAI-1 theo Q2 (minh hoạ M-d tính ở MINH-HOA/N2P-6, không trần 20 %). Ưu: giữ đúng tỷ lệ chủ dự án duyệt. Nhược: chờ một vòng K. Rủi ro: không.
- (b) Rút 1 clip M-d ≈ 3 s về 3D → 19,9 %. Nhược: dưới Q1 20 %; **thêm/bớt chỉ để vượt chỉ số — trái luật cứng**.
- **Khuyến nghị (a)**; phiên không tự cắt.

### Ghi thêm cho K (PHIEU-XEM C14, nguyên văn dòng cuối)
- Ghi thêm cho K: Q37 (a) không nhận 12 mốc lớp chồng đã khai (thẻ nhân vật, bộ đếm, tư liệu) — lớp chồng mờ vào 0,4–0,5 s nên biến cố đo trên video trễ > 0,3 s so với mốc khai; phiên không dịch mốc khai để khớp thước.

### Yêu cầu kèm theo của lệnh K-1.17.7 (không phải khiếu nại; căn cứ chủ dự án, Asia/Saigon, nguyên văn)
- 25/10 09:08 "Vấn đề tôi concern nhất là chỉ phí bị đội nhiều, còn các vấn đề khác đều có thể nới để tăng chất lượng và độ chân thực của hình ảnh / Người xem cũng không phải là người chuyên về khảo cổ hay gì để có thể nhận ra những dự khác biệt nhỏ trong những frame hình ngắn".
- 25/10 09:15 "Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị".
- 25/10 06:56 C11, C13 theo khuyến nghị.
- Việc theo lệnh: GOC-CAO tham số + 5 chốt cấu trúc; TU-LIEU trần 20 % + lớp THAT; K-LAI-1 theo Q2 từ T4; TL-1 (c) miễn ranh M-d/tư liệu; nhân vật có tên trong M-d (mặt ≤ 1/8 khung); kiểm 2 mức `muc_kiem`; câu "công trình mốc" trong q_thoi_dai; K1176-D6 sàn Y cho nhấp nháy BMN (d).

## Phán quyết K — checks 1.17.7 · A1–A5 + C11 + C13 (ANIMATIC-T4) + gói "50 % tiết kiệm" (25/10/2026; báo cáo `reports/k1177/K1177-BAO-CAO.md`; nhánh thật `claude/k1177-animatic-checks-nfbsbr` — harness buộc, lệnh ghi `checks-1-17-7`; LOCK 513c9442 → 3a53574c; không merge)
Tái hiện trên dữ liệu thật của ANIMATIC-T4 trong `main` (`channel-k2/k2c-t4-02/animatic/`: log shot, 58 log máy, 23 clip M-d, kiểm 2 tầng); video = nối 3 bản xem (SHA `4263d29d…`, 730,146 s) vì animatic gốc ở ngoài git. Tiêu chí đặt TRƯỚC khi đo: A2 — khung KHOP phải khớp ≤ 0,5 px với ÍT NHẤT một khung của shot tham chiếu khi cùng máy thật (đo lại bằng ma trận máy), và lệch thật vẫn bắt; A4 — tách "thước (a) sai" với "đặc tả thiếu mốc"; luật mới — mỗi luật ≥ 1 ca đạt + ≥ 1 ca trượt, tập không khai giữ hành vi 1.17.6.
- **A1 (= C13 (1)) — LUẬT THIẾU CHỮ, sửa.** MAY-19 đọc `cam.p`/`tieu_diem`/`diem_neo` theo hệ cảnh y lên (x = E − E0, y = h, z = −(N − N0)) nhưng RULES/K1174 §5 chỉ nói "log.json render_ldn.js". Phiên ANIMATIC khai đúng hướng (thêm `cam` hệ cảnh, giữ `cam_en`) nhưng `diem_neo` vẫn ghi [E, N, h] trong trường hệ cảnh — lỗi ẩn gây ra A2. 1.17.7: RULES ghi rõ hệ; nhận log `toa_do: EN` hoặc chỉ `cam_en`; trường mới `diem_neo_en`; toạ độ > 100 km trong trường hệ cảnh → đổi theo `goc_toa_do` + (w).
- **A2 (= C13 (2)) — LỖI LUẬT (2 lớp), sửa.** (i) điểm neo [532118, 181150, 111] đọc như hệ cảnh = điểm cách ≈ 560 km → phép 7 điểm chỉ còn đo hướng nhìn: H5-07b "lệch 62 139 px" (trượt giả) và H2-12 "0,08 px" (đạt giả); (ii) (c) chỉ so khung CUỐI shot `khop_voi` — sai khi shot tham chiếu di chuyển (M03 DAY, H1-03 TRUOT). Đo lại với neo đúng hệ: H5-07b ↔ khung đầu M03 **0,00 px** (khung cuối 36,0 px); H2-12 ↔ đầu/cuối H1-03 51,9 / 51,7 px, ↔ khung 202/403 **0,128 px**; H3-06, H4-08 0,00 px. 1.17.7: so khung ĐẦU shot KHOP với khung GẦN NHẤT của shot tham chiếu (ghim được bằng `khop_khung`), in khung khớp. MAY-19 (c) T4: 1 → **0**; ca lệch thật (máy dời 5 m) vẫn trượt (selftest).
- **A3 (= C11) — LỖI LUẬT (mâu thuẫn Q2), sửa theo C11 (a) chủ dự án duyệt 06:56.** Từ T4: K-LAI-1 không tính đoạn minh hoạ M-d (đã tính ở MINH-HOA/N2P-6, tổng AI ≤ 70 %); `ai_image` ngoài M-d vẫn ≤ 20 %. T4 v1: K-LAI-1 TRƯỢT 20,4 % → **ĐẠT** (0 % ngoài M-d, M-d 148,67 s in kèm). T3: không đổi.
- **A4 (= ghi chú C14) — KHÔNG phải lỗi thước; chẩn đoán của phiên chưa đúng; bổ sung khuôn.** Q37 (a) đối chiếu beats khai với mốc của ĐẶC TẢ (spec_times), không với biến cố đo trên video — độ trễ mờ vào 0,4–0,5 s không tham gia (a). 12 mốc (thẻ nhân vật, bộ đếm, tư liệu) do `ghep.py` đặt nhưng KHÔNG có trong đặc tả `shots[].p` → (a) đúng định nghĩa (chống tự khai biến cố). 1.17.7: đặc tả nhận `p.lop_chong: [{at, k, s, mo_vao_s?}]` — mốc `at` và `at + mo_vao_s`; phía dựng ghi lớp chồng vào đặc tả (ghép đọc từ đó). Beats tự do vẫn không nhận.
- **A5 — KHAI SAI KHUÔN (luật rõ ở RULES 1.17.0), không đổi luật; sửa thông báo.** k2check đọc tấm kiểm ở episode.yaml `n2p: {tam: [{id, shot, render, ghep, mat_na, nam, …}]}` (ảnh PNG render đối chứng + ghép + mặt nạ lớp để đo (i)–(iv)); `n2p.tam` của log shot là KẾT QUẢ kiểm của phiên ({tag, kiem, ghep, v, khoang_s}) — không đo lại được. Thông báo THIẾU nay nêu khuôn đúng khi thấy khuôn log.
- **Gói "50 % tiết kiệm" + P1–P10 (09:15) — luật mới/đổi (chi tiết RULES-LL §1.17.7):** GOC-CAO (`goc_cao_min_pct` 50–100, mặc định 60) + 5 chốt cấu trúc (mở/kết chương góc cao; P1 mỗi hồi cùng khung; ≤ 2 liền {thấp, cận, M-d, THAT}; chương ≥ `goc_cao_chuong_min_pct`; TL-1 `tl1_muc_tieu_pct`) · TU-LIEU trần tới 20 % + lớp THAT + TU-LIEU-THAT (giấy phép footage hiện đại có SHA) · TL-1 (c) miễn ranh M-d/tư liệu/ảnh thật · NHAN-VAT-TEN (YuNet ≤ 1/8; chân dung + duyệt) · KIEM-2-MUC (day_du/nen; bắt buộc day_du khi có nhân vật/công trình có tên/chân trời City) · q_thoi_dai lớp công trình mốc (H2-13 bắt 3/3, khung đúng 0/3) · BE-MAT-NHA sàn Y nhấp nháy (K1176-D6) `be_mat_nha_y_san_nhap`.
