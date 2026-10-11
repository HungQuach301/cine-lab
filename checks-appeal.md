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
