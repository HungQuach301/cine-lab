Nhánh thật: **`ccr-c8d3a06d-uhtkar`** (harness buộc tên này; nhánh cục bộ `p-2010` cùng SHA, đẩy lên `origin/ccr-c8d3a06d-uhtkar`). Tạo từ `origin/main` @`3176ad1b`. `main` cập nhật fast-forward ở §7.

# PHIÊN P-2010: hợp nhất 5 nhánh (7 phiên), Kinh thánh §14 (luật AI N1/N2, G0), sổ 19–20/10, tra nguồn thực vật 1782, giọng master. BÁO CÁO. DỪNG chờ chủ dự án

```text
ĐIỀU LỆ PHIÊN P-2010                                           | thực tế
Loại phiên:        P (điều phối)                                | đúng
Nhánh:             p-2010 từ origin/main @3176ad1b               | harness buộc ccr-c8d3a06d-uhtkar (dòng đầu); gốc đúng
Merge --no-ff:     (a) V7B → (b) nhac-t3 → (c) dong-goi-t3-v2 →
                   (d) nc-v2v → (e) NC-GPU (gồm nc-cpu)          | 5/5 đúng thứ tự, 0 xung đột; 7b983213 và 718dec9e là tổ tiên
KHÔNG merge:       nc-v2v3                                       | đúng (nhánh có trên origin @974b16d0, không đọc, không merge)
KHÔNG sửa:         checks/, design/, scripts/, loi-khoa.txt      | đúng ngoài phần merge; loi-khoa.txt 51d1c773… trước/sau
lock.py:           chỉ --verify                                  | đúng; mọi lần KHỚP 1.16.1 a3c39873…
Vùng V7C:          design/k2v/**, scripts/k2*, v7p/**, reports/v7c/** | không chạm ngoài merge
Chi phí:           Claude/OpenAI/YouTube 0; ElevenLabs chỉ đọc   | $0 · $0 · 0 đơn vị; ElevenLabs 0 ký tự (bộ đếm 141 009 = số cuối KL42)
Giờ máy:           mốc theo dõi 2 h                              | GIO_MAY (§8)
Preflight:         --staged mỗi commit; --range trước khi đẩy    | --staged ĐẠT 4/4 commit soạn tay; 5 commit merge kiểm bằng --range ngay sau merge: ĐẠT; --range cuối: §6
Email:             che; không vào header/URL/payload/UA           | 0 email trong diff; UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)" ở mọi yêu cầu mạng
Dừng hỏi:          không dừng giữa chừng                          | đúng
```

## 0. Tóm tắt
| Mục | Kết quả |
|---|---|
| Merge | 5/5 `--no-ff`, **0 xung đột**: `3176ad1b` → `42b4d101`, 714 tệp (§1) |
| Sau merge | lock **KHỚP 1.16.1 `a3c39873751805a7a0a5e2b544bc2c28630d78e87725b777d3c7ba1c77cc2d2b`** · selftest k116 **144/144** · k115 **105/105** · k114 **126/126** · `LOI-KHOA.sha256` **3/3 OK** |
| Kinh thánh | SHA-256 `5014eb8e…0618b` → **`9e7492a5a6742a0578dc9c06518e92a8ecc077dd345bfdefb426c1438c5631ad`**; thêm §14 (14.1–14.6); sửa §11.3, §12.2, §12.3, §12.5 + tiêu đề, mỗi chỗ kiểm "đúng 1 lần" (+42 / −5) (§2) |
| Sổ | RIGHTS **+39 dòng** (mọi dòng có giấy phép nguyên văn, kiểm bằng máy) · AUTHORSHIP **+6** · COST-LEDGER **+10** (72 dòng, mọi dòng 20 cột) · Đ5 → **ĐÃ GỬI 19/10 16:57** · BAI-HOC **#111–#117** · HANG-DOI mục 20/10 (§3) |
| Thực vật 1782 | Tải lại 5 nguồn djvu, **SHA khớp đăng ký 5/5**; 15 đoạn, **22/22 trích khớp nguyên văn**. Kết luận: **1782 THƯA HƠN hiện nay** — hướng **bậc 2** (Drinkwater, Ancell, Spilsbury); giá trị 0,45 vẫn **bậc 5 tạm** (§4) |
| Giọng master | **KHÔNG lấy được**: khoá ElevenLabs thiếu quyền `speech_history_read` (HTTP 401); master KL42 ngoài git đã mất. 0 ký tự. Thiếu cả 8 phần chương + 3 câu thu lại; thu lại ước **10 128 ký tự gửi ≈ 4 460 trên bộ đếm** — KHÔNG thu (§5) |
| Kiểm cuối | GOLDEN_TOMTAT (§6) |
| main | `3176ad1b` → **MAIN_SAU** (fast-forward, không force) (§7) |

## 1. Merge
SHA đầu nhánh khớp lệnh 5/5: `origin/ccr-ef2b66f0-9639kq` = `317dcf51`, `origin/nhac-t3` = `af4208ed`, `origin/dong-goi-t3-v2` = `76abba56` (chứa `7b983213` dong-goi-t3), `origin/nc-v2v` = `2c1d1e12`, `origin/claude/eloquent-dijkstra-kemr8j` = `4fe45ec3` (chứa `718dec9e` nc-cpu). Nhật ký: `reports/p2010/merge.log`.

| # | Nhánh @ SHA | SHA trước → sau | Thay đổi (so cha 1) | Xung đột |
|---|---|---|---|---|
| a | `ccr-ef2b66f0-9639kq` @317dcf51 (V7B; gồm V7P `71932a3f`) | `3176ad1b` → **`e05c6b94`** | **123 tệp**, +20 004 / −38: `reports/v7b/` 48, `reports/v7p/` 32, `scripts/k2tl/` 15, `design/k2v/` 14, `channel-k2/k2c-t3-01/` 13, `scripts/k2/` 1 | không |
| b | `nhac-t3` @af4208ed | `e05c6b94` → **`a6aa2b33`** | **35 tệp**, +24 673: `reports/nhac-t3/` | không |
| c | `dong-goi-t3-v2` @76abba56 (gồm dong-goi-t3 @7b983213) | `a6aa2b33` → **`258013b5`** | **158 tệp**, +18 534: `reports/dong-goi-t3-v2/` 74, `reports/dong-goi-t3/` 68, `channel-k2/k2c-t3-01/` 16 | không |
| d | `nc-v2v` @2c1d1e12 | `258013b5` → **`1fb5cc0f`** | **131 tệp**, +10 600: `reports/nc-v2v/` 119, `design/k2v/` 12 | không |
| e | `claude/eloquent-dijkstra-kemr8j` @4fe45ec3 (NC-GPU, gồm nc-cpu @718dec9e) | `1fb5cc0f` → **`42b4d101`** | **267 tệp**, +7 747: `reports/nc-gpu/` 114, `reports/nc-cpu/` 104, `design/pt/` 46, `design/k2v/` 3 | không |

Không nhánh nào đổi `checks/`, `docs/`, RIGHTS, AUTHORSHIP, COST-LEDGER, `loi-khoa.txt` (khớp merge-tree của điều phối).

**Kiểm sau merge (e):** `python3 -I checks/lock.py --verify` → **KHỚP** (LOCK = tính lại = `a3c39873…2d2b`, 1.16.1). Selftest (P chỉ chạy, không đọc mã): `selftest_k116.py` **144/144** (23 nhóm), `selftest_k115.py` **105/105** (15 nhóm), `selftest_k114.py` **126/126**. `sha256sum -c LOI-KHOA.sha256` → `script-v4.2-KHOA.md: OK`, `loi-khoa.txt: OK`, `khoa-loi/phat-am/gibraltar-eric.pls: OK`. `loi-khoa.txt` = `51d1c7735a106efdefc3f466ad77ea03cabdade4d38e7d513cc0e5227d6e431c`. Preflight `--range 3176ad1b..HEAD`: **714 tệp — ĐẠT** (không cần trượt ngoại lệ nào).

## 2. Kinh thánh `docs/BIBLE-KENH2.md`
SHA-256 trước `5014eb8e3793f864b47fef330d14209554f1e1f4971b60cd5a713b2638a0618b` (bản P-1910; script kiểm trước khi sửa), sau **`9e7492a5a6742a0578dc9c06518e92a8ecc077dd345bfdefb426c1438c5631ad`**. Script `reports/p2010/sua_bible.py`: mỗi thay thế kiểm **đúng 1 lần xuất hiện** rồi mới áp; §14 chỉ thêm khi chưa có "## 14.". Bản chép §14: `reports/p2010/s14-ban-chep.md`. Commit `04bc3207`. `git diff`: +42 / −5.

**Tiêu đề**
```diff
-… §12; §13 + sửa 19/10)
+… §12; §13 + sửa 19/10; §14 + sửa 20/10)
```
**§11.3 câu KHÔNG** (câu trái N1/N2)
```diff
-- KHÔNG: AI video sinh từng khung (nhấp nháy, trôi hình; API video OpenAI ngừng 24/9/2026); AI cho cảnh bay trên không tầm cao, bản đồ chiến lược; ước độ sâu bằng AI; vân vật liệu AI kiểu "B" …
+- KHÔNG: AI sinh, xoá hoặc đổi LỚP DỮ KIỆN (§14.1) ở mọi loại cảnh; khung AI (ảnh hay video) chưa qua cổng kiểm §14.1 (e) — nhấp nháy, trôi hình, vật bịa; AI cho bản đồ chiến lược; ước độ sâu bằng AI; (sửa 20/10: AI video và cảnh bay trên không tầm cao được dùng cho LỚP NỀN theo N1/N2 — §14.1); vân vật liệu AI kiểu "B" …
```
**§12.2 phép thử "bỏ AI ra"** → áp cho lớp dữ kiện
```diff
-- AI chỉ được TÌM, ĐỌC, ĐỐI CHIẾU, PHỤC CHẾ, LÀM SỐNG cái đã có nguồn; không sinh dữ kiện (…). Phép thử: bỏ AI ra mà dữ kiện trên hình đổi → không được dùng.
+- Với LỚP DỮ KIỆN (§14.1): AI chỉ được TÌM, ĐỌC, ĐỐI CHIẾU, PHỤC CHẾ, LÀM SỐNG cái đã có nguồn; không sinh dữ kiện (…). Phép thử áp cho lớp dữ kiện: bỏ AI ra mà lớp dữ kiện trên hình đổi → không được dùng. LỚP NỀN: AI được vẽ lại theo N1/N2 (§14.1, sửa 20/10).
```
**§12.3 KHÔNG video AI**
```diff
-… tô màu khi không có nguồn màu; video AI.
+… tô màu khi không có nguồn màu; video AI ngoài N1/N2 (§14.1, sửa 20/10).
```
**§12.5 Cycles** (P thêm để không trái §14.2 — lệnh không nêu chỗ này, chủ dự án xem lại)
```diff
-Cycles chỉ cho khung tĩnh, poster, thumbnail.
+Cycles chỉ cho khung tĩnh, poster, thumbnail (sửa 20/10: và cú lặn/cận cảnh đêm có lửa dựng trọn bằng Cycles GPU — §14.2).
```
**§14 mới** (thêm cuối tệp): "## 14. Bổ sung 19–20/10/2026 (chủ dự án duyệt; nới luật AI tới N2 20/10 21:15, duyệt tất cả khuyến nghị 20/10 21:22)" với 6 tiểu mục chép theo lệnh:
- **14.1 Luật AI mới N1/N2** (a)–(g): hai lớp dữ kiện/nền; N1 ghép mặt nạ ID (< 1/255, viền ≤ 3 px, cấm vật dữ kiện mới, cấm đổi loại vùng); N2 ≤ 20 % minh hoạ, nhãn "Illustration" (ghi là ngoại lệ của §12.1); tổng AI ≤ 20 % ở T3; cổng kiểm bắt buộc (bộ đo NC-V2V T1–T6 + "đốm sáng mới bền ≥ 1 s"; **T7–T9 của NC-V2V3 "khi nhánh đó được duyệt"** vì chưa có trong main); công bố; lộ trình M1–M4 + chọn công cụ theo NC-V2V3.
- **14.2 G0** (NC-D1, NG-D1, NG-D3; NC-D3, NC-D4, NG-D2, NG-D5). **14.3 Cú lặn** (GPU-3) — ghi "bổ sung §13.6". **14.4 Look** (NG-D4, V2V-D2, NC-D5 trỏ tới §4 báo cáo này). **14.5 Đóng gói**. **14.6 Âm thanh**.
- (f) ghi thêm: "câu hiện hành ở §10.6 giữ tới khi chủ dự án duyệt bản viết lại" — P **không** tự viết lại câu tiếng Anh của §10.6; bản nháp đề xuất ở §9 mục 3.

**Chỗ còn vênh, P không sửa (lệnh không giao):**
1. §11.3 "khung lai bão hoà trung vị **≤ 0,40**" ngược chiều §11.4/§14.4 "**≥ 0,40**".
2. §11.3 dòng "Được dùng (a)–(d)" (một tấm/khung neo, vân nướng cho bay cận) hẹp hơn N1; §14.1 đứng trên theo tiêu đề "thay các câu trái ngược".
3. Tên làm việc T3 "Why Gibraltar Was Besieged 14 Times" (HANG-DOI) chạm luật §14.5 (cấm dữ kiện tiêu đề không khớp phần dựng); đã ghi nhắc ở HANG-DOI 20/10.

## 3. Sổ (commit `5a5139a3`)
**RIGHTS.md +39 dòng** trong mục mới "Kênh 2 — nhạc T3 (Scott Buckley), vân CC0 NC-CPU/NC-GPU, tham chiếu NC-V2V, ảnh thumbnail ĐÓNG-GÓI v2 (phiên P-2010 …; 20/10/2026)". Script `reports/p2010/ghi_rights.py` đọc thẳng từ dữ liệu nguồn (không chép tay) và kiểm mỗi dòng 10 cột + cột giấy phép có câu trích ≥ 40 ký tự trong ngoặc kép: **39/39 đạt**.
| Mã | Số dòng | Nguồn dữ liệu | Giấy phép nguyên văn |
|---|---|---|---|
| K2-MUS-6…13 (Intervention NM, Signal to Noise NPM, The Weight of Air – Katabasis I, Juggernaut, Never Dying, Undertow, Echoes, Hiraeth) | 8 | `reports/nhac-t3/nguon-moi.json` (tên, trang, URL tệp, SHA-256, giây, ngày đọc 19/10) | CC BY 4.0 + "This work is licensed under a Creative Commons Attribution 4.0 International License ; meaning it’s free for use in any project (including commercial) as long as I’m credited. For YouTube videos, credits must appear in the video description." Mẫu ghi công: `"<tên>" by Scott Buckley – released under CC-BY 4.0. www.scottbuckley.com.au (edited)` (chữ "(edited)" chờ duyệt). Ghi chú Content ID + cấm phát tán soundtrack (§14.6). Tệp MP3 **chưa vào `assets/`** |
| NCCPU-PH01…18 | 18 | `reports/nc-cpu/RIGHTS-NC.md` (id, tác giả, cỡ, SHA 12 ký tự diff/nor/rough) | Poly Haven: "Our assets are all licensed as CC0, which is effectively Public Domain even in jurisdictions that do not support the Public Domain." — P đọc lại https://polyhaven.com/license ngày 20/10: khớp. `clay_roof_tiles_02` ghi "cùng tài sản P1810-PH05, khác độ phân giải"; `stony_dirt_path` ghi "mở rộng P1810-PH07" |
| NCGPU-PH01…08 (bản 4k) | 8 | `NC-GPU-BAO-CAO.md` dòng 253 | như trên. **SHA bản 4k chưa có trong repo** (`sha.json` ngoài git đã mất) |
| NCV2V-PH1…3 (`marble_cliff_01` Amal Kumar, `coast_sand_01` Rob Tuytel, HDRI `simons_town_harbour` Greg Zaal, Rico Cilliers) | 3 | `reports/nc-v2v/ref/NGUON.md`; tác giả tra `api.polyhaven.com/info` 20/10 | như trên; ghi "ảnh tham chiếu nội bộ, không lên hình" (`aerial_rocks_02` trùng tệp NCCPU-PH05, không ghi lại) |
| DG3V2-PH1 "Gibraltar Sunrise" (axmiller, 2008), DG3V2-PH2 "The Rock of Gibraltar" (BY-YOUR-⌘, 2008) | 2 | `reports/dong-goi-t3-v2/nguon-anh.json` | CC BY 2.0 + nguyên văn deed (json) + link; ghi công đề xuất kèm "cropped, combined with our 3D reconstruction, text added" |

Không ghi: **DG3V2-AI** (3 ảnh gpt-image của ĐÓNG-GÓI v2) — ngoài danh sách lệnh; chờ chủ dự án (§9).

**Đ5:** RIGHTS P1910-G1 "(…, chưa gửi)" → "**ĐÃ GỬI 19/10/2026 16:57** (chủ dự án gửi; P-2010 sửa 20/10, trước ghi "chưa gửi"), **chờ ElevenLabs trả lời**" — quyền phát hành vẫn **CHƯA** tới khi có trả lời. Đính chính thêm ở `reports/k1161/K1161-BAO-CAO.md` §12 mục 6 (giữ câu cũ, thêm dòng đính chính) và tiêu đề `reports/giong-chot/hoi-elevenlabs.md`. Dòng AUTHORSHIP 19/10 12:45 ("thư Đ5 chưa gửi") đúng tại thời điểm đó → giữ.

**AUTHORSHIP.md +6 dòng:** (1) 19/10 nhạc **1X–4X** + miễn phí — mở `khoa.json`: X = B, B, B, A → **B trừ KA2026 = A** (giờ chọn lệnh không ghi); (2) 19/10 22:24 K-1.16.1 **ba điểm xác nhận** = §12 mục 1–3 của K-1.16.1 (nguyên văn lệnh xác nhận không có trong repo); (3) 19/10 22:58 **GPU-3**; (4) 19/10 23:21 **duyệt NC-V2V** (phạm vi nguyên văn không có trong repo); (5) 20/10 21:15 **nới luật tới N2, làm từng phần**; (6) 20/10 21:22 **duyệt tất cả khuyến nghị** (G0, NC-D1…D6, NG-D1…D6, V2V-D1 → N1/N2, V2V-D2, D4, D5, M1–M4). Mỗi dòng có đóng góp biểu đạt của con người.

**COST-LEDGER.csv +10 dòng** (script `ghi_cost.py`, kiểm cả tệp 72 dòng × 20 cột): NHAC-T3 ($0; giờ máy 0,9 h **ước**, báo cáo không ghi) · DONG-GOI-T3 (Claude $0,959; **YouTube 1 947 đơn vị**) · DONG-GOI-T3-V2 (Claude $0,486; OpenAI $0,303) · **V7-PILOT** (Claude $0,230; 4,3 h — phiên chưa có dòng, vào main qua V7B; P bổ sung) · V7B (Claude $0,657; 5,5 h) · NC-V2V-1 ($0) · NC-V2V-2 (**Gemini $17,00**, hoá đơn Google **₫453.145** — số chủ dự án đưa trong lệnh, không có trong repo; Claude $0,262; OpenAI $0,046 ước; 2,2 h) · NC-CPU (Claude $1,10; 7,2 h) · NC-GPU (**RunPod $10,98**; Claude $1,036; 2,7 h CPU + 10,70 h GPU pod) · P-2010. Gemini/RunPod không có cột riêng → ghi `ghi_chu` như dòng cũ.

**BAI-HOC-LL.md** mục mới, dòng **#111–#117**: V2V-D5 (a) gọi API video chạy nền, (b) không `pkill/pgrep -f`, (c) người chấm AI thưởng chi tiết bịa; NC-D6; NG-D6 (a)–(h); "Wan VACE với độ sâu + cạnh đổi loại vùng đất ↔ nước — phải có điều khiển phân vùng" (số đo ở nhánh NC-V2V3, chưa merge — ghi theo lệnh); và #117 (P thêm) tệp lớn ngoài git mất theo container — lần thứ 2 (master giọng KL42, `sha.json` 4k, djvu T3b).

**HANG-DOI.md** mục "CẬP NHẬT 20/10/2026 (phiên P-2010)": T3 → **M1** (V7C bố cục, không AI) → **M2** (thumbnail + móc 30 s + cú lặn, ≈ $5–15) → **dựng cả tập theo G0**; dòng **việc phiên K (V2V-D4)**: bộ đo bịa NC-V2V thành công cụ trong `checks/`, phải xong trước M2.

## 4. Tra nguồn thực vật 1782 (NC-D5) — `reports/p2010/THUC-VAT-1782.md`
- Tệp djvu T3b không còn trong container → tải lại đúng URL đăng ký (`claims-vay-ham.json` `nguon_da_tai`): Drinkwater 1786 `7576bb8f…`, Drinkwater 1785 `d55e8ebf…`, Drinkwater 1905 `9a0c3c3e…`, Spilsbury `f6c2f3a9…`, Ancell `67d61d0a…` — **SHA khớp 5/5**. Tệp ngoài git `/var/tmp/cine-out/p2010/nguon/`.
- 15 đoạn trích (Drinkwater 9, Spilsbury 4, Ancell 2), **22/22 phần trích khớp nguyên văn** (`kiem_trich.py`). Chính:
  - Drinkwater 1786 tr. 49–50: *"The appearance of the rock is barren and forbidding ; as few trees or (hrubs, excepting palmettos, are to be feen on the face of the hill"*; mùa khô *"nothing offers to the eye but fharp uncouth rocks, and dried palmetto bufhes."*
  - Ancell 1784 tr. 40: *"Our barren rock yields but little"*.
  - Trong vây: cắt bụi làm bó cành ở mặt núi và mặt sau (Drinkwater tr. 79, 105, ≈ 111; Spilsbury 27/9/1779 "thorns"); củi khan hiếm (Drinkwater tr. 106, 141; Spilsbury 8/2/1781 "wood sells by the pound"); mặt sau dưới Signal House bị "scalping" (Spilsbury 8/2/1781).
  - Eo đất: vườn rau xanh quanh năm trước 1779, bị bỏ khi TBN dựng công sự (Drinkwater tr. 50); vườn ngoài Land-port bị đốt 10/1780 (Spilsbury).
- Tranh/bản khắc (39/39 SHA khớp `tai-san-vay-ham.json`): hai bản khắc Drinkwater 1786 cùng hướng (sườn không ký hiệu bụi); quạt Met 209515 ngược hướng nhưng địa hình tưởng tượng.
- **Kết luận: 1782 THƯA HƠN hiện nay**; căn cứ hướng **bậc 2** (ba nhân chứng độc lập); tỉ lệ **không có nguồn** → **giữ 0,45 tạm, giá trị bậc 5**. Nguồn còn gợi ý mặt núi có thể thưa hơn 0,45 (gần trơ, chủ yếu cọ lùn) và mốc 9/1782 nên tông khô. Mật độ "hiện nay" làm mốc so cũng chưa có nguồn trong repo.

## 5. Giọng master KL42 G1 v4.2
- **Đích:** 8 phần chương (00 HOOK p0, 01 ROCK p0, 02 SIEGE p0–p1, 03 NEUTRAL p0, 04 RUNWAY p0, 05 GATE p0–p1) + 3 câu thu lại đã chọn (`issmus`: 1i#0, 1i#1, 1k#0; `thay.json` `chon: true`), thu 19/10 06:26–07:05 UTC, G1 `VDLncRBHDjLHBqLhQ1Qt`, `mp3_44100_192`. Master đã biết SHA: WAV `ba50fba75aa956731226f7269adbffb6728853d6d2a7fc95b4eefba8e13b586d`, FLAC `852b9e419b40d16657f3280dfb03ef7c422c50434fa63db57c2ace8e5b29b7de` (733,532 s; KL42 §6) — **ngoài git, không còn** (`/var/tmp/cine-out/kl42` không tồn tại).
- **Lịch sử ElevenLabs:** `GET /v1/history?voice_id=…` → **HTTP 401** `missing_permissions`: *"The API key you used is missing the permission speech_history_read to execute this operation."* (`GET /v1/user/subscription` 200). Công cụ: `reports/p2010/giong_lich_su.py` (chỉ GET; dừng ở lỗi, không ghi tệp kết quả). **Không tải được bản nào → không đối chiếu ±0,05 s, không đưa gì vào LFS.**
- **0 ký tự:** bộ đếm lúc kết thúc **141 009** = đúng số cuối của KL42 (`bo-dem.jsonl`, 19/10 07:14:51 UTC) → không ai tiêu ký tự từ đó tới nay.
- **Đoạn thiếu: tất cả** (8 phần + 3 câu). Trong git chỉ có bản xem MP3 96 kb/s (`reports/kl42/nghe/…-xem-1/2`), không đủ chất lượng master.
- **Ước thu lại (KHÔNG thu):** 9 884 ký tự (8 phần) + 244 (3 câu `issmus`) = **10 128 ký tự gửi ≈ 4 460 trên bộ đếm** (tỉ lệ 0,44, BAI-HOC #103); hạn mức còn 171 534 − 141 009 = 30 525. Thu lại cùng seed không bảo đảm giống bit → SHA master đổi, phải ASR kiểm lại.
- **Cách lấy lại 0 ký tự (đề xuất):** chủ dự án bật quyền **History → Read** (`speech_history_read`) cho khoá API ElevenLabs của môi trường; khi đó tải audio lịch sử (định dạng gốc MP3 44,1 kHz 192 kb/s, bản tốt nhất có vì gói Creator không có PCM), đối chiếu từng phần với `reports/kl42/` và ghép lại bằng `reports/kl42/ghep.py` (cần căn mốc lại vì lịch sử không trả alignment).

## 6. Kiểm cuối
GOLDEN_BANG

## 7. main
MAIN_BANG

## 8. Chỉ số trong ±5 % quanh ngưỡng (và vượt mốc)
| Chỉ số | Số đo | Ngưỡng/mốc | Lệch |
|---|---|---|---|
| YouTube Data API — ĐÓNG-GÓI v1 | 1 947 đơn vị | mốc 2 000 | **−2,65 %** |
| Bão hoà trung vị Cycles sau `--skydif` (NG-D2) | 0,403 | ≥ 0,40 (§11.4/§14.4) | **+0,75 %** (sát nút) |
| Giờ máy P-2010 | GIO_MAY | mốc 2 h | GIO_LECH |
| Ngoài ±5 % nhưng vượt mốc: Gemini NC-V2V-2 $17,00 / mốc $15 (+13 %). RunPod NC-GPU $10,98 / mốc $12 (−8,5 %, dưới mốc). | | | |

Không thêm phần tử nào để vượt ngưỡng.

## 9. Việc chờ chủ dự án
1. **Bật quyền `speech_history_read`** cho khoá ElevenLabs (để lấy lại master giọng 0 ký tự), hoặc duyệt thu lại ≈ 10 128 ký tự gửi (§5). Từ nay master âm thanh vào LFS ngay trong phiên tạo ra (§14.6, BAI-HOC #117).
2. **Hệ số bụi 0,45:** giữ tạm (đề xuất), hay hạ theo hướng bậc 2 (§4); duyệt hai ràng buộc có nguồn (cọ lùn; tông khô 9/1782).
3. **Mô tả §10.6 viết lại theo N1/N2** — bản nháp P đề xuất (chưa vào Kinh thánh): *"Narration: synthetic voice. Visuals: 3D reconstructions built from the cited sources and registers. In some shots AI repaints background surfaces only (terrain, water, sky, vegetation, textures); buildings, street layout, flags, ships, people, lights, text, dates and numbers come from the sources and are never AI-generated. Segments labelled "Illustration" are fully AI-generated and carry no location facts. Historical images: public domain / CC0 / CC BY, credited."*
4. **Ba chỗ vênh Kinh thánh** (§2 cuối): §11.3 bão hoà ≤ 0,40; §11.3 "Được dùng (a)–(d)" so N1; tên làm việc "14 Times" so §14.5. Và xác nhận sửa §12.5 (Cycles cho cú lặn) P thêm ngoài lệnh.
5. **Nhạc:** duyệt mẫu ghi công có "(edited)"; duyệt đưa 8 MP3 Scott Buckley (≈ 110 MB, ngoài git, cần tải lại theo SHA) vào `assets/k2/music/` (LFS?) — RIGHTS đã ghi.
6. **RIGHTS DG3V2-AI** (3 ảnh gpt-image thumbnail ĐÓNG-GÓI v2) chưa ghi — giao P sau hay ghi ngay.
7. **Giờ chọn nhạc 1X–4X** và nguyên văn các lần duyệt 22:24 (K-1.16.1) và 23:21 (NC-V2V) để AUTHORSHIP ghi đủ.
8. **Giao phiên K (V2V-D4)**: bộ đo bịa thành công cụ trong `checks/` trước M2; **NC-V2V3** chờ merge khi xong (chọn Cosmos-Transfer hay Omni có mặt nạ).
9. Thư Đ5: chờ ElevenLabs trả lời — giọng G1 chưa được dùng cho bản phát hành.

## 10. Tệp (`reports/p2010/`)
`P2010-BAO-CAO.md` (tệp này) · `CHECKPOINT.md` · `merge.log` · `sua_bible.py`, `s14-ban-chep.md` · `ghi_rights.py` · `ghi_cost.py` · `THUC-VAT-1782.md`, `kiem_trich.py` · `giong_lich_su.py` · `golden.json`.

**DỪNG — chờ chủ dự án.**
