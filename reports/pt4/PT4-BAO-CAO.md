Nhánh thật: `pt4-song` (đúng lệnh) — tạo từ `origin/pt2-lai` @ `d0a3b36c`. Harness của phiên chỉ định nhánh làm việc `ccr-ff77de40-rcmt3s`; phiên đẩy `pt4-song` theo lệnh chủ dự án (§0, §12).

# PT4 — Nâng SỰ SỐNG và không khí cho khung neo LAI (P2-1…P2-6) — BÁO CÁO

> Phiên R&D PT4, 18/10/2026, theo lệnh chủ dự án (duyệt P2-1…P2-6 ngày 18/10). **Không merge. DỪNG chờ chủ dự án.**
> Mọi số là số đo thật trong phiên (tệp ở `reports/pt4/`) hoặc ghi rõ **(ước)**. Không email, không khoá API trong repo/báo cáo.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | R&D PT4 | đúng |
| Nhánh | `pt4-song` từ `origin/pt2-lai` (@d0a3b36) | đúng; ghi ở dòng đầu |
| Tệp được sửa | CHỈ `design/pt/**` + `reports/pt4/**`; không `design/pt3/` | mới `design/pt/song/**` (7 tệp); sửa `design/pt/scene/build_scene.py` **chỉ thêm nhánh `PT4=1`** (mặc định ra đúng cảnh PT2 — kiểm: vùng bảo vệ 1782 dựng lại ⊂ mặt nạ PT2, lệch 0,016 % khung); mới `reports/pt4/**`. Không chạm `design/pt3/`, `main`, `scripts/`, `checks/`, `docs/`, `channel-*/` (chỉ đọc) |
| Trần | Claude ≤ $3 · OpenAI ≤ $2 (chỉ tấm C 1943) · YouTube 0 · EL 0 · máy ≤ 6 h | **$2,458** (42 lượt chấm mù) · **$0,0629** (1 lệnh, tấm C 1943 lần 2) · **0** · **0** · **≈ 4,1 h tiến trình** (§7) |
| Preflight | bắt buộc; che email; không in/ghi khoá | `tools/preflight.sh` **ĐẠT** mọi commit; `checks/lock.py --verify` **KHỚP**. Khoá OpenAI do proxy gắn (mã không đọc biến khoá); khoá Claude chỉ qua biến môi trường cho `claude -p` |
| Video / ảnh | 540p ≤ 15 MB, không LFS; ảnh ≤ 30 MB | 2 video 540p **3,7 + 3,3 MB**; ảnh **≈ 17 MB** (§7) |
| Kinh thánh §11.3 (HC1–HC9) | luật | **Không tìm thấy §11.3/HC7–HC9 trong repo** (`docs/BIBLE-KENH2.md` ở mọi nhánh chỉ tới §9). Phiên áp các rào nêu trong lệnh: C chỉ bề mặt, ghép lại lớp dữ kiện A, lớp sống tự dựng, kiểm dữ kiện 0 lỗi, nhãn; người ≥ 10 m, không cận mặt, không người ngã/chết — cộng HC1–HC6 của PT2 |
| Dừng | không dừng hỏi giữa chừng | xong việc; câu hỏi không chặn tự quyết, liệt kê §12 |

## 1. Tóm tắt (đọc 2 phút)
1. **P2-5 — tấm C 1943 lần 2:** một lệnh `gpt-image-2.5-sunburst` `/v1/images/edits` ($0,0629, C2PA có), mặt nạ PT2 + **chặn kiến trúc** (đá viền, sàn ban công, gờ, lan can + dải 0,7 m dưới chúng) + prompt cấm công-xon/gờ/chạm trổ/ống. **W5 (công-xon) hết.** HC4 bắt 2 nghi vấn MỚI: **W6** thanh kim loại trong lòng cửa tầng trệt, **W7** tường thấp + bậc ở cuối quảng trường → cả hai xử lý bằng ghép A. Cuối: **0 lỗi chắc, 0 ngoại lệ chờ duyệt**.
2. **P2-3 — màu LAI riêng:** 1943 LAI bão hoà ngày **0,278–0,329** (PT2 0,478–0,553; mục tiêu ≤ 0,40; mốc đối thủ 0,28), tương phản giữ **0,27** (PT2 0,25–0,26), FIND_EDGES 25,8–32,4 (PT2 28,6–33,4). Thử **"độ sáng C + sắc độ A"**: bão hoà 0,17–0,23 nhưng bóng ngả lam, tường xám tím — **không chọn** (§5.2).
3. **Người:** 2 dáng thân/vai × 21 tư thế (đi 8 pha, đứng thả lỏng, nói, nhìn quanh, chắp tay, việc theo vai, đi mang vật 8 pha) + **cặp khiêng thùng/hòm**; mắt/tóc/lông mày/môi; nhóm 2–4 người quay vào nhau, tổ chữa tường 1782, gác cặp; tốc độ đi riêng; không xếp hàng. Chấm mù: toy_like **6,67 vs 7,56** (vòng 2) — **chưa đạt ≤ 4** (chỉ 1943 chiều = 4). Người vẫn là điểm yếu số 1.
4. **Đồ phố + sự sống có nguồn:** tra TIEN-KY/claims (1782) + ảnh PD Commons/LoC (1943): **không có nguồn** cho quầy/mái che/gà/chó/la/ngựa/đồ phơi tháng 9/1782 hay đồ phố 1943 → **không thêm vật nào** (đúng luật). Khói bếp = khói ống khói sẵn có (theo giờ).
5. **Không khí:** sương/khói phố theo độ sâu (bắt đầu sau 20 m, trần 0,28), tia nắng + bụi trong nắng từ lượt nắng của A, chiều sâu tông; **đêm 1943 không nguồn sáng mới** (vùng bảo vệ đêm sai khác 0,0/255).
6. **Vật bảo vệ của A dựng lại:** lòng nhà đổ nát 1782 (tường sau ám khói theo dải, lỗ + dầm cháy gãy, mảng sàn sót, đá vỡ không đều, đỉnh tường răng cưa), tàu máy 1943 (thân thuôn, thượng tầng, ống khói, cột, cần cẩu, xuồng), hầm trú ẩn (bao cát hình gối) — tất cả là điểm ảnh A.
7. **Chấm mù PT4 vs PT2 LAI cùng khung:** vòng 1 (8 khung): **PT4 thua 6–15** (3 hoà) — lý do lặp: sương làm mất biển/tàu/cờ ("empty haze"). Sửa trần sương → vòng 2 (6 khung ngày): **PT4 thắng 13–5**, craft **6,06 vs 5,61**, chi tiết **6,00 vs 5,50**, ai_look 4,72 vs 4,78.
8. **HC2 giữ:** vùng bảo vệ LAI vs A cùng chỉnh màu sai khác **≤ 0,0007/255** (≤ 0,011 % điểm ảnh — quấn sáng ở mép người) ở 8/8 khung.

## 2. Việc đã làm
### 2.1 Hạ tầng dựng lại (thư mục tạm PT2 không còn)
- Ghost SH bằng `git show` nhánh `claude/sh-ghost-gibraltar-t3-1gkftx` → `/var/tmp/pt/ghost/`; 9 vân Poly Haven tải lại, **SHA 27/27 khớp** `reports/pt/giay-phep/polyhaven-files.json`; MPFB2 clone + fetch đúng commit `3edf9df0…` (SHA base.obj/rig/weights khớp RIGHTS W4-MPFB-A/A3); `OpenEXR` cài vào `/opt/cine` (lần 3 — đề xuất vào `verify.sh` như PT/PT2).
- Nền A 1782 hình học PT2 dựng lại (d2 + mã lớp) để dùng lại tấm C 1782 PT2 lần 2: vùng bảo vệ dựng lại ⊂ mặt nạ PT2 đã gửi AI (chỉ 0,016 % khung ngoài) ⇒ cùng hình học.

### 2.2 P2-5 tấm C 1943 lần 2 — `design/pt/song/gen_c4.py`, sổ `reports/pt4/ai-c/goi-api.jsonl`
- Nền A 1943 PT4 (`PT4=1`, không bao cát như PT2): tàu + hầm dựng lại (§2.6). 1 lệnh `/v1/images/edits` 2048×1152 `quality high`, mặt nạ **43,0 % được sửa** (PT2: 62–66 %): bảo vệ thêm `da_voi`, `vua_go`, `sat` trên toà + dải tường **0,7 m dưới chúng theo khoảng cách từng điểm ảnh** (nơi lần 1 AI vẽ công-xon).
- Prompt (nguyên văn trong sổ) mở đầu: *"STRICT: change nothing outside the transparent mask areas. This is a surface-texture pass only. DO NOT ADD OR CHANGE ANY ARCHITECTURE: no brackets, corbels, consoles or supports under balconies, no cornices, mouldings, carvings, pilasters, window or door surrounds, ledges, pipes, wires, signs or fixtures… Keep each building's existing paint colour, hue and brightness exactly (a muted, sun-faded wartime town, not vivid)…"* + phần PT2.
- Usage: 1 508 token ảnh vào + 436 chữ + 1 522 ra → **$0,0629**, 29,9 s, C2PA `caBX` có.
- **Ghép** (`compose4.py`): vùng bảo vệ PT2 (mã lớp) + `--ma-cua-A` (W6) + `--dat-xa 62` (W7). Thử ghép theo **toàn bộ** mặt nạ đã gửi AI (54 % bảo vệ): để lại **dải tường A phẳng** dưới ban công rất lộ → bỏ; vì AI không vẽ gì trong các dải đó (rà 200 %), ghép theo vùng bảo vệ chuẩn là đủ.

### 2.3 P2-3 chỉnh màu riêng LAI — `live4.py` `GRADE_LAI`
- A-thuần giữ chỉnh màu chung PT (bão hoà ×1,85, tương phản 0,42). LAI: **bão hoà ×1,5, giảm thêm ở điểm ảnh đã đậm màu (×0,8 khi chênh kênh > 0,65)**, tương phản 0,46, ấm 0,025; thêm hạt phim chung cho mọi bản.
- Nguyên nhân 1943 PT2 loang cam đã hết từ gốc: prompt lần 2 giữ màu + "muted" → tấm C tự nó đã nhạt hơn (cùng chỉnh màu chung ×1,85 + không khí: 0,255 thay vì 0,478).
- Biến thể **"độ sáng chi tiết từ C + sắc độ từ A"** (`compose4.py --sac-A`): màu = A_p × (Y_LAI / Y_A) trên vùng được sửa → §5.2.

### 2.4 Người — `design/pt/song/mh_people4.py` (MPFB2 CC0, bộ nạp tự viết như PT2)
- **Dáng thân:** mỗi vai 2 dáng (trung bình; gầy cao *hoặc* chắc thấp luân phiên theo vai; nữ đầy đặn hơn), da 4 tông, tóc 5 màu (bộ binh 1782 dáng 1: tóc rắc bột), dân/thuỷ thủ/thợ dáng 2 không mũ.
- **Mặt/tóc/tay:** tóc = vỏ `helper-hair` của lưới gốc **cắt chỉ giữ phần sọ** (bản đầu dài tới vai phủ mặt như màn che — sửa); nhãn cầu tròng tối + lòng trắng; lông mày + môi tô theo vị trí nhãn cầu/răng; vải bump nhiễu + loang màu nhẹ; da bump lỗ chân lông. SSS da thử rồi bỏ (×3 thời gian dựng, không thấy ở ≥ 10 m). Bỏ SUBSURF (168 người/tờ tràn RAM 15 GB).
- **Tư thế (21 cột/hướng):** đi 8 pha · đứng thả lỏng (dồn trọng tâm, quay đầu ngẫu nhiên) · nói (tay phải ra hiệu, quay đầu 22°) · nhìn quanh (đầu 48°, vai 12°) · chắp tay sau lưng · việc theo vai (1782: bộ binh gác súng dựng, lính/pháo binh chữa tường cầm bay-búa, dân/thuỷ thủ vác bao, dân nữ đỡ giỏ; 1943: lính súng dựng, thuỷ thủ vác túi, RAF/lính chắp tay, thợ cầm dụng cụ) · **đi tay mang vật 8 pha** (thùng/hòm ôm trước bụng, bao trên vai, giỏ).
- **Cặp khiêng:** 2 người (2 dáng) cùng hướng, cách 1,7 m, nhịp bước lệch nửa chu kỳ, thùng (1782) / hòm (1943) treo giữa hai đòn — 1 sprite, 8 hướng × 8 pha.
- Tờ sprite: 8 hướng × 21 tư thế × 3 lượt nắng (d1, d2, d4; d3 dùng d4; đêm = d2 tối + lam), 110 px/m, 8 spp; **13 tờ/mốc** (6 vai × 2 dáng + cặp khiêng). Tăng tốc: đặt tư thế MỘT lần trên người mẫu rồi sao `matrix_basis` cho mọi ô (bản đầu cập nhật cả cảnh mỗi lần xoay xương: O(N²)).
- **Bố trí (`live4.py`):** người đi 60 (1782 hẻm) / 70 (1943) tuyến/mốc, **tốc độ riêng 0,75–1,3×** (nhịp bước theo tốc độ), 30 % người có vai mang vật thì đi tay mang vật, 5 % là cặp khiêng; **nhóm 2–4 người** đứng vòng quanh tâm nhóm, mỗi người quay về tâm (tư thế nói/nhìn/đứng/chắp tay); **tổ chữa tường 1782** sát chân tường, nhìn vào tường (1–3 người làm + 0–1 người đứng xem); **gác** 2 lính súng dựng sát tường cả ngày; **không xếp hàng** (không có đội hình có nguồn). Bóng nắng theo mặt trời từng lượt (PT2) + **bóng tiếp đất** mềm mọi lúc; viền sprite mềm + **quấn sáng** nền vào mép; tông người ±10 %; vệt phơi sáng nhẹ hơn PT2 (bỏ bóng người trong suốt ở khung tĩnh).
- Đã thử và bỏ (rà khung): tổ thợ 1943 (tư thế hai tay giơ trước tường đọc như **bị khám xét** — và không có nguồn chữa tường 1943).

### 2.5 Không khí — `live4.py` `Epoch.khi`
- **Sương/khói phố theo lượt độ sâu:** `1 − exp(−max(d − 20 m, 0) × k)`, k = 0,0024 (+ khói bếp sáng 8,8 h / chiều 18,3 h), nhiễu trôi chậm; màu = màu trời gần chân trời của chính lượt nền; **trần 0,28** (sau chấm mù vòng 1).
- **Tia nắng + bụi:** lượt nắng của A (đất/tường có nắng, ≤ 120 m) + trời → mờ hướng tâm về vị trí mặt trời trên màn hình (9 bước), mạnh khi ngược sáng (hẻm 1782 nhìn tây: chiều có tia nắng cuối hẻm); ~900 hạt bụi trôi chỉ sáng nơi có nắng.
- **Đêm:** sương chỉ nhận màu trời đêm (rất tối); không đèn, không quầng mới; 1943 phong toả giữ nguyên PT2.

### 2.6 Vật bảo vệ của A dựng lại — `build_scene.py` nhánh `PT4=1` (RNG riêng: không đổi chuỗi ngẫu nhiên cảnh)
- **1782 lòng nhà đổ nát** (8 lô RUINS): tường sau chia 6 dải ám khói đậm dần lên trên; lỗ đặt dầm mỗi tầng + dầm cháy còn cắm/gãy chúc (45 %); mảng sàn ván cháy sót (60 %/tầng); đá/gạch vỡ khối 20 mặt xô lệch (≈ 9/m dài lô) dồn chân tường; đỉnh tường răng cưa bằng đá rời so le.
- **1943 tàu máy** (5 chiếc): thân thuôn mũi/đuôi tròn, độ cong boong, đai mớn nước, mạn chắn sóng, 2–3 tầng thượng tầng có dải cửa, đài chỉ huy, ống khói thon 6 đoạn có chóp, cột + xà, cần cẩu (tàu hàng), 2 tháp pháo + nòng (tàu chiến), xuồng cứu sinh. Không cờ, không chữ, màu không có nguồn (xám / thân tối).
- **Hầm trú ẩn:** mái bê tông dày, khung cửa thép, tường chắn bao cát **hình gối** so le 6 hàng (thay hộp vuông). Hình dáng chung, không nguồn chi tiết (3 ảnh hầm 1939 trên Commons nguồn yếu, chưa xem được).

## 3. Nguồn + giấy phép (`reports/pt4/nguon/KET-QUA.md`, wikitext nguyên văn `reports/pt4/nguon/wikitext/`)
| Tài sản | Nguồn | Giấy phép (nguyên văn) | Dùng |
|---|---|---|---|
| Vân nền A (9) | Poly Haven, tải lại 18/10, SHA 27/27 khớp PT | CC0 (như PT) | như PT2 |
| Lưới người, targets, rig, trọng số | MPFB2 commit `3edf9df0…` | CC0 1.0 (`LICENSE.md` mục C; đầu ra mục D) | người PT4 — **vẫn cần dòng RIGHTS W4-MPFB-A5** (PT2 đã đề xuất) |
| Ảnh C 1943 lần 2 | OpenAI `gpt-image-2.5-sunburst` | Services Agreement §4.1/§4.4 như PT/PT2 | **chỉ nghiên cứu** đến khi duyệt |
| Ảnh C 1782 lần 2 | PT2 (dùng lại, `reports/pt2/ai-c/`) | như trên | như trên |
| Font Inter | có sẵn | SIL OFL 1.1 (RIGHTS K2-F1) | nhãn |
| Ảnh tra cứu Gibraltar 1939–45 (12 tệp xem được) | Commons (IWM "The British Army on Gibraltar 1941/1942" GM…, A…; LoC fsa.8e01069) | IWM: `{{PD-Scan|1=PD-UKGov|category=}}`, trường permission ghi "IWM Non Commercial Licence" … "considered expired 50 years after their creation"; LoC: `{{PD-USGov}}`; 3 ảnh hầm Commercial Square 1939: `{{PD-old}}`, tác giả không rõ, nguồn trang Facebook | **chỉ tra cứu, KHÔNG vào phim**; không ghi RIGHTS. Cờ quyền: IWM ghi "Non Commercial" trên trường permission — chủ dự án quyết trước khi dùng |
- **Kết quả tra nguồn đồ phố:** 1782 — TIEN-KY-VAY-HAM/claims chỉ có S062 (12/4/1781 dân bỏ phố chạy về nam), S063 (nhà cháy), "green-market" (1781, đã cháy), lợn quay 1781 (cướp bóc) → **không có quầy/mái che/gia súc/đồ phơi cho hẻm tháng 9/1782**. 1943 — Commons/LoC: **không có ảnh PD phố thị trấn 1939–45** (IWM chỉ cảnh quân sự: hầm, ụ pháo, sân bay, bệnh viện); "Category:Main Street, Gibraltar" chỉ ảnh hiện đại/thế kỷ 19; Commons trả HTTP 429 sau ~40 tải. ⇒ **không thêm vật nào ở cả hai mốc**.
- **Lưu ý vật SẴN CÓ của A không nguồn** (từ PT, PT4 không thêm): 1943 có 40 mái che vải + 102 chậu cây trên ban công (thủ tục mặt tiền PT), 1782 có 1 mái che. Đề xuất xét bỏ khi có quyết định nguồn đồ phố (§9 Q-PT4-3).

## 4. Kiểm dữ kiện (HC4) — `reports/pt4/kiem-du-kien.json`, bằng chứng `reports/pt4/kiem/bang-chung-1943-lan2.jpg`
| # | Tấm | Phát hiện | Loại | Xử lý |
|---|---|---|---|---|
| W5 | 1943 lần 2 | công-xon dưới sàn ban công (lần 1) | — | **hết** (rà 200 % các ban công trong khung) |
| W3 | 1943 lần 2 | gờ chạm trổ mép mái (lần 1) | — | không còn; gờ mái nằm trong vùng bảo vệ |
| **W6** | 1943 lần 2 | lòng cửa tầng trệt toà phải: **thanh kim loại sáng có móc đỉnh** (như ống/khung) — dù prompt cấm "pipes" | **nghi vấn — vật mới** | má cửa lấy từ A (`--ma-cua-A`) → hết; còn viền vữa xám mảnh của A |
| **W7** | 1943 lần 2 | cuối quảng trường (62–100 m): **tường đá thấp nối các cột lan can + bậc thang** | **nghi vấn — kiến trúc mới** | mặt đất > 62 m = A × độ lợi màu khớp đá C có nắng (trung vị tỉ số), hoà 10 m → hết; dải 1,4 % khung mất vân đá lát |
| W1b | 1943 lần 2 | toà phải kem → vàng đất loang (nhẹ hơn lần 1); toà trái giữ hồng | không lỗi (màu A thủ tục) | giữ |
| W2 | 1943 lần 2 | vữa bong, loang ẩm, đá lát mòn | bề mặt | giữ |
| — | 1782 (C PT2) | hình học A mới chỉ thêm ở vùng BẢO VỆ (lòng nhà); 1,31 % vùng sửa có bóng mới → tỉ số A_d2/A_cũ_d2 | — | giữ kết luận PT2 (0 lỗi chắc, 1 sót nhẹ) |
- **Vật cấm trong kết quả:** 0 người, 0 cờ mới, 0 chữ/biển, 0 tàu mới, 0 nguồn sáng mới, 0 cây, 0 vật hiện đại. **Cuối: 0 lỗi chắc, 2 nghi vấn đã xử lý, 0 ngoại lệ chờ duyệt.**
- Bài học: mặt nạ + prompt cấm vẫn **không đủ** — AI chuyển "chi tiết kiến trúc" sang chỗ khác được sửa (lòng cửa, mép mặt đất). Rà 200 % theo ô vẫn bắt buộc; ~40 phút người rà cho tấm này.
- **Người chấm mù lại gán sai cờ:** ở cả 2 vòng, nhiều phiếu ghi "Union Jack post-1801 / St Patrick's cross" cho 1782 — **sai** (cờ do mã vẽ đúng mẫu 1707, như PT2). ⇒ chấm bằng mô hình không thay được kiểm dữ kiện.

## 5. Số đo (`reports/pt4/do/do-khung.json`, `vung-bao-ve.json`) — cách điều phối: 640×360 INTER_AREA, cắt y 60–300
### 5.1 Bảng chính (LAI, khung tĩnh 1080p không chữ; PT2 = khung LAI PT2 đã công bố)
| Khung | PT4 LAI bão hoà / colorfulness / FIND_EDGES / tương phản | PT2 LAI | Vùng bảo vệ LAI vs A (cùng màu) |
|---|---|---|---|
| 1782 sáng | 0,212 / 33,7 / **34,3** / 0,252 | 0,286 / 42,7 / 35,1 / 0,255 | 0,0 · 0 % |
| 1782 trưa | 0,227 / 33,0 / **34,5** / 0,256 | 0,298 / 40,7 / 35,0 / 0,259 | 0,0007 · 0,011 % |
| 1782 chiều | 0,220 / 22,1 / 19,2 / 0,268 | 0,298 / 26,7 / 20,4 / 0,255 | 0,0004 · 0,008 % |
| 1782 đêm | 0,502 / 30,5 / 5,8 / 0,056 | 0,557 / 36,8 / 5,3 / 0,058 | 0,0 · 0 % |
| 1943 sáng | **0,286** / 44,8 / 32,4 / 0,267 | 0,486 / 78,5 / 33,4 / 0,257 | 0,0006 · 0,009 % |
| 1943 trưa | **0,278** / 38,7 / 31,9 / 0,271 | 0,478 / 70,8 / 33,4 / 0,250 | 0,0007 · 0,010 % |
| 1943 chiều | **0,329** / 42,6 / 25,8 / 0,274 | 0,553 / 73,0 / 28,6 / 0,259 | 0,0004 · 0,008 % |
| 1943 đêm | 0,502 / 19,8 / 3,3 / 0,034 | 0,384 / 24,5 / 2,5 / 0,035 | 0,0 · 0 % |
- **P2-3 đạt:** 1943 ngày ≤ 0,40 (tối đa 0,329, −18 % dưới ngưỡng); tương phản không giảm (0,267–0,274 ≥ PT2). Đêm: trung vị bão hoà của khung gần đen (S cao ở điểm ảnh tối) — không phải loang màu; PT2 PNG đo 0,573/0,667.
- FIND_EDGES PT4 thấp hơn PT2 1–10 % — do sương sau 20 m (đo tách: không sương 35,2/33,5 → có sương bản đầu 30,5/28,2 → sương bắt đầu 20 m 34,5/31,9).
- **Đếm (log 540p, mọi khung):** 1782 ngày **19–39 người (TB 31,6)**, đứng 0–23 (TB 14,3), nhóm 0–9 (TB 6,0), mang vật 2–5, cặp khiêng 0–1, đêm 2–3; 1943 ngày **14–46 (TB 38,3)**, đứng TB 11,1, nhóm TB 4,8, mang vật 6–12, cặp khiêng 0–3, đêm 4–5. Vật nền: không thêm (A 1782: 5 thùng, đống gạch vụn, 5 dầm, 2 đống đạn, 1 đèn, 1 pháo, 1 cột cờ; 1943: 3 thùng, 1 xe kéo, 3 đèn, hầm, 1 cột cờ, 5 tàu máy + 1 thuyền buồm).

### 5.2 Biến thể "độ sáng C + sắc độ A" (khung `khung/*-trua-sacA-notext.jpg`)
| | 1782 sáng/trưa/chiều | 1943 sáng/trưa/chiều |
|---|---|---|
| bão hoà | 0,153 / 0,188 / 0,537 | 0,184 / 0,173 / 0,227 |
| FIND_EDGES | 34,1 / 34,3 / 18,9 | 32,6 / 32,0 / 26,0 |
- Chi tiết giữ nguyên (FIND_EDGES ≈ LAI), bão hoà thấp hơn, **nhưng nhìn kém**: bóng trên đá lát ngả lam (sắc độ ánh trời của A), tường xám tím, mép mái loé cam ở 1943 (tỉ số sáng ở mép), 1782 chiều bão hoà 0,537 (tường bóng xanh lam của A). Màu A là bảng màu thủ tục không nguồn ⇒ "sắc độ A" không đúng hơn về dữ kiện. **Không chọn**; chỉnh màu LAI riêng đạt mục tiêu mà giữ màu C.

## 6. Chấm mù (`design/pt/song/blind4.py`, `reports/pt4/kiem-mu/`, `kiem-mu-v2/`)
Giao thức như PT2: `claude -p` ghim **claude-sonnet-5-5** (sổ ghi phục vụ sonnet-5-5 + haiku-5-5 phụ trợ CLI), chỉ Read, thư mục tạm chỉ X/Y, 3 vai nguyên văn `blind_v2.py`, ẩn nhãn, thứ tự X/Y hạt giống 20261019; **PT4 LAI vs PT2 LAI cùng khung neo × cùng giờ khai trước**; hai bản qua cùng bước ffmpeg 1280 px q3 (PT2 từ JPEG đã công bố). Không khung đối thủ.

| | craft | chi tiết | đúng thời kỳ | ai_look | toy_like | Phiếu "tốt hơn" |
|---|---|---|---|---|---|---|
| **Vòng 1** (8 khung) PT4 / PT2 | 5,46 / **5,67** | 5,08 / **5,42** | 5,38 / 5,38 | 4,67 / 4,75 | **5,92** / 6,21 | **PT4 6 – PT2 15 – hoà 3** |
| **Vòng 2** (6 khung ngày, sau trần sương) PT4 / PT2 | **6,06** / 5,61 | **6,00** / 5,50 | 5,17 / 5,06 | 4,72 / 4,78 | **6,67** / 7,56 | **PT4 13 – PT2 5** |
| Vòng 2 — 1782 / 1943 (PT4) | 5,67 / **6,44** | 5,78 / 6,22 | 5,00 / 5,33 | 5,22 / 4,22 | 7,00 / **6,33** | 1782: 4–5; 1943: 9–0 |
- **Vòng 1 thua vì sương:** "Y washes out into an empty haze", "X has a legible harbour with a ship and a flag" — sương không trần làm biển/tàu/cờ cuối khung nhạt mất. Sửa trần sương 0,28 + giảm khói sáng → vòng 2.
- **Vòng 2:** 1943 thắng 9/9 phiếu (chiều toy_like **4** — duy nhất đạt mục tiêu: "haze and silhouetted figures hide the weak character models"); 1782 trưa thua 0/3 ("Y's soldiers form a more coherent marching column, with fewer floating or ghosted figures"), 1782 sáng 1/3, 1782 chiều 3/3.
- **toy_like chưa đạt ≤ 4** (6,67; vòng 1 5,92). Cờ `toy_like` vẫn ở mọi khung ngày. Lưu ý độ ổn định: cùng khung PT2 được chấm toy_like 6,21 (vòng 1) và 7,56 (vòng 2) → biến thiên giữa lượt ≈ ±1 điểm; khác biệt PT4–PT2 trong cùng vòng mới có ý nghĩa.
- Đêm (vòng 1): 2 khung gần như trùng PT2, người chấm hoà/nghiêng PT2 — không chấm lại (trần).

## 7. Giờ máy, chi phí, dung lượng (`reports/pt4/log/gio-may.tsv`)
| Khoản | Trần | Thực tế |
|---|---|---|
| Claude API | $3 | **$2,458** (42 lượt: 24 vòng 1 + 18 vòng 2; `kiem-mu*/cost.jsonl`) |
| OpenAI API | $2 | **$0,0629** (1 lệnh `/v1/images/edits`, `reports/pt4/ai-c/goi-api.jsonl`) |
| YouTube / ElevenLabs | 0 / 0 | 0 / 0 |
| Giờ máy | ≤ 6 h | **≈ 4,1 h tiến trình** (sổ 14 735 s ≈ 4,09 h + ≈ 4 phút lượt thử không ghi sổ), ≈ 3,6 h đồng hồ: sprite 1782 bị cắt ở 30 phút (1 800 s, giữ 20 EXR) + 1 258 s tiếp, sprite 1943 3 177 s (chạy song song nền A 1943 1 986 s — tranh lõi làm cả hai chậm), nền A 1782 995 s + d2 cũ 249 s, thử sprite ≈ 1 000 s, thử ghép/lớp sống ≈ 900 s, sản xuất 2 lượt ≈ 2 600 s |
| Dung lượng | video ≤ 15 MB; ảnh ≤ 30 MB | video **3,7 + 3,3 MB**; ảnh **≈ 17 MB** (tấm C 1943 gốc 4,3 MB bắt buộc lưu) |
- **Dòng COST-LEDGER đề xuất (P ghi):** `PT4-01,khung neo LAI nâng sự sống + không khí (P2-1…P2-6),R&D,2026-10-18,,,,,2.46,3,claude-sonnet-5-5,0,0,≈ 4,1,,0,20,OpenAI $0.063 (gpt-image-2.5-sunburst ×1),reports/pt4/PT4-BAO-CAO.md,YouTube 0; không merge`

## 8. Việc chuyển vào V6 + ước giờ máy
| # | Việc | Ước giờ máy (4 lõi CPU) |
|---|---|---|
| 1 | **Người — vẫn điểm yếu số 1 (toy_like 6,7):** (a) quần áo là lưới riêng có độ dày + nếp theo xương (không tô trên vỏ `helper-tights`); (b) tỉ lệ đầu/vai và tay buông tự nhiên (tay đi hiện vẫn đưa ra trước); (c) mũ có vành/đỉnh đúng mẫu (tricorn hiện là 3 hộp); (d) **ánh sáng sprite theo đúng HDR trời của lượt nền** (hiện ánh trời phẳng 0,35 → bề mặt "nhựa"); (e) dáng thứ 3 + chuyển động phụ (đầu quay khi đi). Kiểm toy_like ≤ 4 ở 6 khung ngày | sprite 13 tờ/mốc × 3 lượt ≈ 45–55 phút/mốc (đo PT4); +25 % nếu thêm dáng 3 |
| 2 | **Mật độ người 1782:** người chấm thích hàng đi có trật tự hơn đám phân tán — chỉ dùng **đội hình hành quân có nguồn** (cần nguồn) hoặc giảm thêm người ở trục hẻm | 0 (tham số) |
| 3 | **Hầm 1943** đọc là "blue box/kiosk hiện đại" (2 phiếu) — cần nguồn hình dáng (3 ảnh 1939 trên Commons nguồn yếu) rồi dựng lại vật liệu ấm | nền A 1943 ≈ 33 phút |
| 4 | **Mặt đất xa 1943 (W7):** dải 62–100 m mịn (A khớp màu) — sinh lại C kèm mặt nạ bảo vệ mặt đất xa thay vì ghép | $0,06 + 1 phút |
| 5 | Nguồn đồ phố: 1782 tháng 9 (nhật ký Drinkwater/Ancell về đời sống phố trong vây), 1943 (Gibraltar National Archives, Gibraltar Heritage Trust, khung newsreel) → danh sách vật nền | 0 máy; giờ người |
| 6 | Vật SẴN CÓ không nguồn của A (40 mái che + 102 chậu cây 1943, 1 mái che 1782): giữ hay bỏ | nền A ≈ 17–33 phút/mốc |
| 7 | Công cụ: `mh_people4.py` (ghi meta sau mỗi dáng, giữ EXR khi bị cắt), `live4.py` (sprite float16 — 2 mốc vừa 15 GB), `compose4.py` (`--nen-cu`, `--sac-A`, `--ma-cua-A`, `--dat-xa`, `--mat-na`), `gen_c4.py`; trình chạy nền **cắt ở 30 phút nếu không đặt thời hạn** (lần 2 trong chuỗi PT) | — |
| 8 | `OpenEXR` vào `/opt/cine` + kiểm trong `verify.sh` (PT, PT2, PT4 đều phải cài lại) | — |
- **Ước cho một tập 10–15 phút (12 khung neo × mốc, ước):** nền A 2–3 h · sprite **dùng chung theo hướng máy ±20°**: 1,5–5 h · tấm C $0,75–1,5 · ghép + 2 lượt sản xuất ≈ 1,5 h · người rà HC4 **≈ 40 phút/tấm** (PT4 đo: 2 nghi vấn mới cần 4 vòng ghép) ⇒ **≈ 5–10 h máy + 8 h người**.

## 9. Quyết định đề xuất
### Q-PT4-1 — Chấp nhận gói "sự sống + không khí + màu LAI" của PT4 làm chuẩn khung neo LAI?
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A. Chấp nhận PT4 (trần sương 0,28, màu LAI riêng) — đề xuất** | thắng PT2 13–5 ở khung ngày; craft +0,45, chi tiết +0,50; 1943 9/9 phiếu; hết loang cam (0,48–0,55 → 0,28–0,33); tương phản giữ; HC2 0/255 | 1782 trưa thua (đám đông kém trật tự hơn); toy_like vẫn 6,7; FIND_EDGES −1…−10 % do sương | mọi khung LAI sau dùng `live4.py` + `GRADE_LAI` | sương/tia nắng là "phong cách": nếu quá tay làm mất mốc dữ kiện (đã thấy ở vòng 1) → giữ trần + kiểm mốc đọc được |
| B. Giữ PT2 + chỉ áp màu LAI riêng | đơn giản | bỏ cải thiện chiều sâu (1943 chiều toy_like 7 → 4 nhờ sương + ngược sáng) | ít | thua đối thủ về không khí |
| C. PT4 nhưng không tia nắng/sương ở 1782 | tránh "rỗng" ở hẻm sáng | mất tia nắng chiều (1782 chiều thắng 3/3) | thêm cờ theo khung | — |

### Q-PT4-2 — Tấm C 1943 lần 2 (thay lần 1 PT2)?
Đề xuất **dùng lần 2**: W5 hết, 0 ngoại lệ chờ duyệt; W6/W7 đã ghép A. Nhược: dải mặt đất xa mịn (1,4 % khung); AI vẫn đổi màu toà phải (kem → vàng đất nhẹ). Rủi ro: cùng loại "kiến trúc mới" có thể xuất hiện ở khung khác ⇒ luật K-LAI-3 (rà 200 %) giữ nguyên.

### Q-PT4-3 — Luật đồ phố khi không có nguồn
Đề xuất ghi vào Kinh thánh (chủ dự án quyết): **"không nguồn → không vật"** áp cả cho vật SẴN CÓ của A (mái che, chậu cây thủ tục) — tức bỏ 40 mái che + 102 chậu cây 1943 trừ khi tìm được ảnh. Ưu: nhất quán dữ kiện; nhược: phố 1943 trống hơn (người chấm đã ghi "no wartime street furniture"); rủi ro: "empty_frame" tăng.

## 10. Chỉ số trong ±5 % quanh ngưỡng
- **toy_like 1943 chiều (vòng 2) = 4,0** = đúng ngưỡng mục tiêu ≤ 4 (0 %) — khung duy nhất đạt.
- **Nhãn phương pháp 38 px** = ngưỡng ≥ 38 px (0 %, kế thừa PT2).
- **Chu kỳ đi 8 khung** = ngưỡng ≥ 8 (0 %) ở tốc độ 1×; người chậm (0,75×) có chu kỳ 10,7 khung.
- **Khoảng cách người tối thiểu 10,0 m** = ngưỡng (luật trong mã).
- **Bão hoà 1943 trưa 0,278** — cách mốc đối thủ 0,28 −0,7 % (mốc so sánh, không phải ngưỡng); ngưỡng ≤ 0,40 còn −18…−30 %.
- Không chỉ số nào khác trong ±5 %: Claude $2,458/$3 (−18 %); OpenAI $0,063/$2; giờ máy ≈ 4,1/6 h (−32 %); ảnh ≈ 17/30 MB; video 7,0/15 MB; vùng bảo vệ ≤ 0,0007/1 (/255).
- **Lệch luật PT2 HC3 "30–80 người/khung ngày":** PT4 TB 31,6 (1782) / 38,3 (1943) nhưng **tối thiểu 19 / 14** ở đầu đoạn (khi tuyến đi chưa vào khung) — PT4 cố ý giảm người (phiếu "cluttered"); chờ chủ dự án quyết ngưỡng.

## 11. Tệp
- **Mã mới** `design/pt/song/`: `mh_people4.py`, `live4.py`, `compose4.py`, `gen_c4.py`, `measure4.py`, `blind4.py`, `README.md`. **Sửa** `design/pt/scene/build_scene.py`: nhánh `PT4=1` (`rock`, `ruin_interior_pt4`, `ship_steam_pt4`, `shelter_pt4`) — mặc định không đổi.
- **Báo cáo** `reports/pt4/`: `pt4-LAI-540p.mp4`, `pt4-A-540p.mp4`, `to-khung-PT2-PT4.jpg`, `to-nguoi-PT2-PT4.jpg`, `khung/` (8 khung LAI không chữ, 4 có chữ, 2 biến thể sắc-độ-A), `ai-c/` (tấm C 1943 lần 2 + mặt nạ + sổ API), `kiem-du-kien.json`, `kiem/`, `do/`, `kiem-mu/`, `kiem-mu-v2/`, `nguon/` (tra ảnh PD), `log/` (log khung, meta nền, meta sprite, sổ giờ máy).
- **Đề xuất ngoài vùng (chưa ghi):** RIGHTS: W4-MPFB-A5 (người đám đông khung neo), dòng ảnh C 1943 lần 2 "chỉ nghiên cứu"; AUTHORSHIP: Q-PT4-1/2/3; COST-LEDGER dòng PT4-01; `verify.sh` kiểm `OpenEXR`; Kinh thánh §11.3 (HC1–HC9) chưa có trong repo — P ghi bản đã duyệt.

## 12. Việc chờ chủ dự án
1. **Q-PT4-1** (gói PT4), **Q-PT4-2** (tấm C 1943 lần 2), **Q-PT4-3** (luật "không nguồn → không vật" cho cả vật sẵn có của A).
2. Ngưỡng người/khung (PT2 HC3 30–80) — PT4 giảm cố ý, tối thiểu 14–19 (§10).
3. Cờ quyền ảnh IWM trên Commons ("IWM Non Commercial Licence" trong trường permission) — chỉ tra cứu, chưa dùng.
4. Ghi các đề xuất ngoài vùng §11; ghi Kinh thánh §11.3 vào repo (phiên không tìm thấy).
5. So với Timelapse Studio trong chat (điều phối) — `reports/pt4/to-khung-PT2-PT4.jpg`, `to-nguoi-PT2-PT4.jpg`, hai video.
6. **Nhánh:** harness chỉ định `ccr-ff77de40-rcmt3s`; phiên đẩy `pt4-song` theo lệnh.
