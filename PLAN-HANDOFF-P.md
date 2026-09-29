# BÀN GIAO PHIÊN P (điều phối) — Cine Lab "Last Round", 29/09/2026

Người viết: phiên P cũ (session `01C9bTk1TGhn4Ugfv2mVbC9M`).
Người nhận: phiên P mới. Đọc tài liệu này trước, rồi đến `CLAUDE.md`, `PLAN.md`, `AUTHORSHIP.md` và `reports/m2/CONG-6-KHOA.md`.
**Trạng thái:** không làm việc mới. **W1, W2 CHƯA mở.** Chờ chủ dự án quyết.

---

## 1. Trạng thái hiện tại
| Mục | Giá trị |
|---|---|
| **main** | `3c40f03` (merge Cổng 6 nhân vật). Sau bàn giao, main = commit merge của tài liệu này (SHA báo trong chat) |
| Nhánh P đang dùng | `claude/cine-lab-m2-cong5-layout-24o5fp`. Chỉ P merge vào `main`, và chỉ khi chủ dự án bảo |
| **LOCK checks** | `checks/LOCK` VERSION 1.5.0, SHA `8d55b6ad389dcbd2c40366bb16eed730106edef3ffee6c565e5ce786bd2aa65b`. Kiểm: `/opt/cine/bin/python checks/lock.py --verify` → KHỚP. Chỉ phiên K sửa `checks/` |
| **LOCK-THIẾT-KẾ** | `design/cong3/LOCK-THIET-KE.sha256`, **34 tệp**, SHA của tệp khoá `95d6a347baadd7f5f5bcd41d302794027e6b950de7efd96ebe947a4eed20d3a8`. Kiểm: `sha256sum -c design/cong3/LOCK-THIET-KE.sha256` |
| **bible/characters.md** | **Ida v1.5.1** (mắt, mũ ngồi thấp 0,025 H, tay MPFB). **Cas v1.6** (đầu, thân, áo len cổ lật cao, quần ống thẳng, gấu 2,17 H, tay theo tỷ lệ MPFB; `c3_head_axis: "doc"`). Khoá 29/09/2026 |
| Model sheet | `design/cong3/model-sheet/ida.json` (`_v1_5_1`, c3 trục đầu 'pca' mặc định), `cas.json` (`_v1_6`, `c3_head_axis: "doc"`, `c3_views` theo W4T3) |
| **Mặc định** (`design/cong3/v2/char3d/cast3d.js`) | `IDA_STYLE='bl'` (đầu v1.5.1 `blender/ida_bl_v151.glb`, trỏ từ `bl_head.js`), `CAS_STYLE='bl'` (`cas_bl.glb`), `CAS_BODY='bl'` (`cas_body_bl.json`), `HANDS_STYLE='bl'` (`hands_bl.json`). `'v14'` là bản cũ, bật lại được bằng cờ |
| Layout mới nhất | `design/cong5/layout/out/layout-v16.mp4` (SHA `9a429b22…`, 43 MB) + `.parts` (có `sil/`) + `.audit`; luật ở `reports/checks/layout-v16/` |
| Kết quả luật layout-v16 | P0 ĐẠT; kiểm toán ĐẠT. **C3, H1b, G3b TRƯỢT** (như v15; gốc đã biết). Chi tiết: `reports/m2/CONG-6-KHOA.md` mục 2 |
| `screening/layout.mp4` | Vẫn là bản Cổng 5, chưa thay |

## 2. Lệnh và pipeline (script trong `scripts/p/`; mọi script có chú thích đầu tệp)
| Việc | Lệnh |
|---|---|
| **Layout đủ 52 shot + mặt nạ C3 + bóng nhân vật + kiểm toán + luật v1.5** | `nohup bash scripts/p/layout_full.sh v17 > /var/tmp/cine-out/v17.log 2>&1 &`. Chỉ chạy lại bước sau: `BUOC="mat-na,bong,kiem-toan,luat" bash scripts/p/layout_full.sh v17`. Âm tạm tự trộn khi thiếu (`design/cong5/layout/audio/mix.py`) |
| So C3 theo shot giữa hai bản | `python3 scripts/p/so_sanh_c3.py v16 v17` |
| **Kiểm mù** | `python3 scripts/p/kiem_mu.py` (không đối số → in cách làm). Các bước:<br>1. `doi-chung <dir>`: trích 2 khung đối chứng Sprite Fright 104,5 s và 332 s từ `/var/tmp/hieuchuan/sprite-fright-804p.mp4`; thiếu thì tự tải archive.org, kiểm SHA `85af52d5…`. **Không commit khung đối chứng** (RIGHTS REF-SF-HC).<br>2. `chuan-bi <dir> nhãn=ảnh …`: đặt tên mù 8 hex, ghi `map.tsv`, in prompt nguyên văn.<br>3. Giao mỗi ảnh cho một subagent **mới** (`general-purpose`, chạy nền).<br>4. `nguyen-van <dir> <ra.md> <tasks_dir> agentId=tên …`: lấy nguyên văn.<br>5. `dem <ra.md>`: đếm từ khoá bằng máy |
| Câu hỏi kiểm mù (nguyên văn) | `Mở và xem đúng một file ảnh: <đường dẫn> (dùng công cụ Read). Không mở, không tìm hay đọc bất kỳ file nào khác.` + dòng trống + một trong hai câu: `Trả lời bằng tiếng Việt, như một người xem bình thường: Người này bao nhiêu tuổi, giới tính gì, đang cảm thấy gì? Nêu thêm điều gì người xem có thể thấy lạ trong ảnh (nếu có).` Khung hai người dùng "Những người trong ảnh" thay cho "Người này" |
| Từ khoá đếm máy | `búp bê · mặt nạ · con rối · ma-nơ-canh · tượng sáp · đồ chơi` + nhóm "lệch phong cách" (`lệch phong cách · không ăn nhập · khác phong cách · hai phong cách`) |
| **Dò lệch 0 px** (layout mặc định không đổi) | `bash scripts/p/do_lech_0px.sh <ra> s02,s24c,s37,s42 [bản gốc]`. Bộ chuẩn: s02, s24c, s37, s42 (+ s41, s42a nếu sửa đèn lồng) |
| **Nén clip xem thử** (< 30 MB để gửi qua giao diện) | `bash scripts/p/nen_xem_thu.sh <vào.mp4> <ra.mp4> [MB=28] [từ s] [đến s]` (2 pass như package.py) |
| Khung thử một thời điểm | `bash scripts/p/khung_thu.sh <nhãn> <dir> '{"shot":"s42a","T":114.5,"casStyle":"bl"}' [mẫu] [rộng] [cao]`. Khung nộp: mẫu 3, 1920×1080, `LAN=nang` |
| Ảnh EEVEE 4 góc / cận | `bash scripts/p/eevee_4goc.sh <dir> '<json có "export":1,"exportWho":"cas">' <ra.jpg> [ANG] [DIST] [ZC]` |
| Dựng lại thân Cas | `/opt/bpy/bin/python design/cong3/v2/char3d/blender/build_cas_body_bl.py -- <mpfb2> design/cong3/v2/char3d/blender` (khoảng 2 s). Cần MPFB2 commit `3edf9df0` (`git clone https://github.com/makehumancommunity/mpfb2.git`; RIGHTS W4-MPFB-A…A4). Bản clone cũ nằm ở scratchpad phiên, sẽ mất. Tệp thân đã **khoá**: dựng lại phải khớp SHA hoặc xin duyệt |
| Đo C3 một nhân vật (turnaround) | Cas: `/opt/cine/bin/python design/cong3/v2/char3d/blender/c3_w4t.py <dir> cas v2/char3d/blender/page_turn_w4t.js` (làn nặng, khoảng 170 s). Ida: `… ida v2/char3d/blender/page_c3_bl.js` |
| Hàng đợi | `bash scripts/render/queue.sh <gói> <nhãn> -- <lệnh>`. `LAN=nhanh` cho việc < 60 s. Nhật ký: `/var/tmp/cine-queue/log.tsv` |

## 3. Mẹo và bẫy đã gặp
**Worktree và phiên xưởng**
- **Worktree cô lập của phiên xưởng (cine-worker) tạo từ `main`**, không từ nhánh P. Tài sản chỉ có trên nhánh P thì phiên xưởng **không thấy**. Phải merge vào main trước khi giao gói.
- **Worktree mới thiếu `design/cong3/shared/node_modules`** (three.js, không nằm trong git). Trong worktree của chính gói, liên kết tới repo chính rồi mới render:

  ```
  ln -s /home/user/cine-lab/design/cong3/shared/node_modules design/cong3/shared/node_modules
  ```

  Ghi lệnh này vào lệnh giao gói.
- **Lệnh bị chặn và cách xử lý đúng quy tắc:**
  - Phiên xưởng chạy `git merge --ff-only <nhánh P>` hoặc `git reset --hard <sha>` trong worktree của nó → bộ phân loại chặn ("Modify Shared Resources"). Đọc worktree khác → bị chặn (cô lập). Phiên xưởng **dừng đúng luật** và báo. **P không chạy hộ lệnh đã bị chặn.**
  - Cách đúng: merge tài sản vào main rồi giao lại. Hoặc P tự tạo worktree từ nhánh P (`git worktree add -b <nhánh> <dir> <nhánh P>`) và **tự làm**, ghi rõ trong báo cáo. W4T lượt 2 đã làm như vậy.
  - Lệnh `rm -f $D/*` (glob trên biến) bị chặn → dùng đường dẫn cụ thể.

**Render**
- **Thời gian render toàn phim:** v15 4 325 s; **v16 8 386 s** (+94 %, do da CPU của thân và tay MPFB).
  - Shot có Cas mất khoảng 4,4 s mỗi khung.
  - Mặt nạ C3: v15 556 s → v16 1 085 s. Bóng nhân vật 537 s. Luật 440 s.
  - Toàn pipeline khoảng 3 giờ 7 phút. Chạy nền và chờ bằng `while kill -0 <PID>`, có timeout; hoặc lệnh chờ chạy nền của harness.
- `render_film.js` **không có `--help`**: gọi bừa sẽ render toàn phim vào `out/`.
- Render toàn phim (không `--only`) ghi `timing.json`, nhưng assemble.py chỉ đọc `timing_*.json`, bản mới nhất thắng. Script đã tự đổi tên.
- `still.js` và `export_sil.js` tạo `page-*.html` tạm; chạy bị dừng giữa chừng sẽ sót lại. Tệp này bị .gitignore bỏ qua, xoá được.
- `page_l2.js` (trang thử) chỉ nạp trước glb Cas khi có `"casStyle"`, nên luôn truyền `"casStyle":"bl"`.
- ffmpeg trong vòng `while read` nuốt stdin, nên thêm `-nostdin`.

**Luật và dữ liệu**
- **C3 trên layout hiện chỉ đo Ida.** `export_c3.js` xuất một nhân vật mỗi khung, nên mọi số sheet trong kết quả đều từ ida.json. `c3_views` 'doc' của Cas chưa được luật dùng.
- Mặt nạ C3 xuất RGBA, phải đổi sang L (kênh alpha). **Không** đổi PNG bóng nhân vật.
- **Nhiễu nền kiểm mù:** đối chứng bị gọi bằng từ khoá 2/20 lượt. "0 từ khoá / 3 khung" có khoảng 27 % trượt ngẫu nhiên; 6 khung với ngưỡng 10 % chỉ đạt 53 %.

**Sửa file**
- JSON sheet dùng `indent=2`, `ensure_ascii=False`. Ghi sai indent làm diff phình to.
- Regex đổi dấu thập phân "." → "," từng biến "v1.6" thành "v1,6". Loại trừ số phiên bản.
- Sau `git merge --no-commit`, sửa bằng sed **chưa được stage**. Kiểm `git diff --cached` trước khi commit.
- Sheet cas.json đã ghi gấu áo 2,17 H, nên `build_cas_body_bl.py` đặt `HEM_DROP=0`. Tránh trừ hai lần.

**Kỹ thuật thân MPFB** (chi tiết: `reports/m2/cong6/w4t2/BAO-CAO-W4T2.md` mục 1)
- Làm mượt Taubin nhiều vòng trên lưới MPFB mật độ không đều làm đỉnh trượt, tạo rãnh ở đường giữa lưng. Bước chia lưới Catmull-Clark cũng tạo rãnh. Cách sửa: bắc cầu lại sau chia lưới + lấp cục bộ.
- "Đáy đũng" phải lấy điểm thấp nhất đường giữa **thuộc chậu**: đùi trong chạm nhau thuộc hông, nếu lấy nhầm sẽ ra điểm thấp giả.
- Da gáy MPFB nằm ngoài ống cổ lật nên cổ lật phải nới phía sau.

## 4. Quyết định còn hiệu lực (chi tiết và người duyệt: `AUTHORSHIP.md`, mục "Cổng 6 — nhân vật")
- **Cách chấm kiểm mù (áp từ W1/W2):**
  - **10 khung** mỗi lần kiểm: chủ dự án chốt khi giao bàn giao 29/09/2026, theo đề xuất của P. Kèm 2 khung đối chứng Sprite Fright mỗi lần.
  - Tách cột **HÌNH** (mặt, đầu, thân, quần, áo, tay, vật liệu) và **TƯ THẾ**. Câu nói cả hai tính vào HÌNH.
  - **ĐẠT** khi tỉ lệ khung có từ khoá ở cột HÌNH ≤ **nhiễu nền đo được (hiện 10 %)** và không có lời chê cùng một chỗ lặp ≥ 2 khung.
  - Lời chê trúng chỗ thật vẫn phải sửa. Đối chứng chạy mỗi lần để cập nhật nhiễu nền.
- **Cấm cận mặt chính diện khi chưa sửa mắt:** s22 MCU, s36 MCU, s37 CU, s39 CU, s40 CU insert (PLAN Cổng 6 mục c). Mắt v1.5.1 đã sửa, nhưng phải kiểm lại trên clip trước khi dùng cỡ cận chính diện. s22 cố định xoay 3/4; s40 mặt chìm tối khi L11 tắt (1:49,2).
- **Sai lệch đã chấp nhận ở v1.5.1/v1.6** (kiểm lại trên clip W1/W2):
  - vai áo len Cas phồng tròn;
  - bàn tay Cas thô khi nhìn gần (không có shot cận tay; phát sinh thì sửa riêng shot đó);
  - s41 Cas phải duỗi hết tay mới chạm đèn, nên W2 đặt gần Ida hơn;
  - mép cổ tay áo Ida răng cưa nhẹ (s41);
  - chân/tay có thể còn bị chê ở khung tĩnh.
- Luật cứng trong `CLAUDE.md` giữ nguyên:
  - P không sửa `checks/`, không đọc mã `checks/`;
  - mọi tài sản vào RIGHTS;
  - chỉ số trong ±5 % quanh ngưỡng phải nêu tên;
  - DỪNG ở cuối mỗi mốc.

## 5. Việc tồn
| Việc | Trạng thái | Tài liệu |
|---|---|---|
| **W2** (s25–s48: Cas, hai người, PA1 s36–s39, trao đèn s41, cảnh 6) | **CHƯA MỞ** | `reports/m2/cong6/KE-HOACH-W1-W2.md` |
| **W1** (s01–s24c: Ida) | **Chờ** quyết định mở | như trên |
| Việc chuyển W1/W2 | Tư thế đứng; 12 shot cầm nắm theo tay mới (10 đo được + s42b, s48 chưa đo); khoảng cách s41; Ida nhìn xuống Cas s42a; PA1; s22 3/4; s40; nhịp cười buồn trên clip có tiếng; mắt cận chính diện; van đồng PA1; tồn đọng Cổng 5 (G2, G5/G6, G10, G11, B1 cảnh 6, khẩu hình L4, nắp đồng hồ) | KE-HOACH mục 3 |
| **Bộ xuất C3 chỉ xuất một nhân vật** (Ida) | Chờ chủ dự án quyết: giữ nguyên, sửa `export_c3.js` cho hai nhân vật (việc của P), hay hỏi K | CONG-6-KHOA mục 2, KE-HOACH mục 12a |
| **Cổng 7** | Đèn lồng chiếu sáng xung quanh; bóng tiếp đất; người/bóng X = 2,0 (s32–s34); G1, G7, G8, G9, G12, G16, G17; phơi sáng s11; màu mũ dưới đèn khí; lấy nét s06, s09w; cửa sổ ấm s24c; **grain G3b** | PLAN "Việc dời sang Cổng 7" |
| **Cổng 9** | Danh sách sửa trong PLAN "Việc cho Cổng 9"; đồng hồ Cổng 9 (AUTHORSHIP Cổng 5) | PLAN |
| Luật đang trượt | C3 (gốc: đo 2D, góc nhìn, che khuất; 23 shot cần người xem), H1b (screen track), G3b (layout chưa có khâu grain) | CONG-6-KHOA mục 2 |
| **Khiếu nại** | **Không còn khiếu nại chờ.** Mọi dòng trong `checks-appeal.md` đã có phán quyết (P0 ×2 đã sửa ở checks v1.5). Dòng "Khiếu nại P0 chờ K" trong PLAN đã cũ | `checks-appeal.md` |
| `screening/layout.mp4` | Còn là bản Cổng 5; thay khi có bản đạt sau W1/W2 | — |

## 6. Token thực tế Cổng 5–6 (để ước tính tiếp)
Số là kích thước ngữ cảnh tích luỹ cuối lượt (công cụ báo), không phải tiêu thụ thật. Hạn mức gói Claude P không đo được.

| Gói | Token | Thời gian | Nguồn |
|---|---|---|---|
| Cổng 5 v2 — W1 | 566 777 → 619 458 → 633 600 (3 lượt) | — | CONG-5-V2 |
| Cổng 5 v2 — W2 | 725 063 → 734 766 → 769 975 → 226 069 (sau nén ngữ cảnh) | — | CONG-5-V2 |
| Cổng 5 v2 — W3 (A-α) | 591 241 → 666 367 → 736 843 | — | CONG-5-V2 |
| Cổng 5 v3 — W1 | 688 878 | 56 phút | CONG-5-V3 |
| Cổng 5 v3 — W2 v3/v4; v5 | 393 061; 419 122 | 2 giờ 1 phút; 10 phút | CONG-5-V3 |
| cine-continuity (v2; v3) | 220 781; 222 328 | 18 phút (v3) | CONG-5-V2/V3 |
| Mặt Ida A-i (W3), vòng 1; vòng 2 | 408 nghìn; 572 nghìn | 2 giờ 13 phút; 1 giờ 18 phút | MAT-IDA-AI |
| Mặt Ida Blender L1; L1 + L2 | 251 nghìn; 487 nghìn | 26 phút (L1) | MAT-IDA-BLENDER, -L2 |
| Mặt Ida lượt sửa A′ (W4) | 122 nghìn | — | MAT-IDA-BLENDER-L3 |
| Gói W4 nhân vật Cổng 6 (phiên mới; phiên cũ đã 709 nghìn) | 439 nghìn | 68 phút | CONG-6-W4 |
| W4T thân Cas lượt 1 | 335 066 | 65 phút | CONG-6-THAN |
| W4T lượt 2 — 2 lần giao phiên xưởng hỏng | 20 249 + 20 279 | 2,5 + 28,5 phút | CONG-6-THAN-2 |
| W4T lượt 2 — P tự làm | khoảng 285 nghìn (vượt hạn 150 nghìn) | 65 phút | CONG-6-THAN-2 |
| W4T lượt 3 — P | khoảng 40 nghìn | 25 phút | CONG-6-THAN-3 |
| Khoá + layout-v16 + merge + kế hoạch — P | khoảng 120 nghìn | 3 giờ 14 phút (chủ yếu chờ render) | CONG-6-KHOA |
| **Subagent kiểm mù** | **45 213–50 690 mỗi khung** (trung bình khoảng 48 nghìn; hơn 30 lần đo) | 27–49 s mỗi khung | các báo cáo kiểm mù |

**Ước tính cho W1/W2** (KE-HOACH mục 5):

| Gói | Ước tính |
|---|---|
| W1 | khoảng 1,0 triệu |
| W2 | khoảng 1,3–1,5 triệu |
| P | khoảng 0,4 triệu |
| Kiểm (10 khung + 2 đối chứng ≈ 580 nghìn mỗi lần) | khoảng 1,0–1,4 triệu |
| **Tổng** | **khoảng 3,7–4,3 triệu** |

## 7. Thư mục ngoài git (sẽ mất khi container bị thu hồi)
| Thư mục | Nội dung | Cách tạo lại |
|---|---|---|
| `/var/tmp/cine-out/` | Render trung gian (`P/full`, `W1`, `W2`), `final/`, `audio/` | `scripts/p/layout_full.sh` tạo lại: render + trộn âm |
| `/var/tmp/cine-queue/` | Nhật ký hàng đợi | Queue tự tạo; bản chép Cổng 5: `reports/m2/cong5/queue-log.tsv` |
| `/var/tmp/hieuchuan/` | Video Sprite Fright (tham chiếu, không commit) | `kiem_mu.py doi-chung` tự tải, kiểm SHA |
| Scratchpad phiên (`/tmp/claude-0/…`) | Bản clone MPFB2, ảnh kiểm mù gốc, file tạm | MPFB2: clone lại commit `3edf9df0`. Ảnh mù đã chép vào `reports/m2/cong6/kiem-mu-*` |
