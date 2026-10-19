# G1b-T3 · VIỆC 6 — NGƯỜI (V6-4): MPFB, mocap, people.js, chấm mù toy_like

> Phiên con của G1b T3, 18/10/2026. Làm trong worktree `agent-aa9b6924369c24d4b`. Không commit, không push. Số trong báo cáo là số đo thật.
> Tệp lớn ngoài git ở `/var/tmp/cine-out/g1b/nguoi/` (khung trước/sau, ảnh MPFB) và `/var/tmp/g6w/` (tải về, venv, trọng số).

## 0. Tóm tắt
| Việc | Kết quả |
|---|---|
| 6.1 MPFB2 | **TẢI ĐƯỢC** bằng `git clone` qua proxy git ẩn danh (HEAD `3af0cd5a2ffba072e93a34e5f6f494fdc4813ddf`, 13/10/2026). Đường HTTPS (github.com, codeload, api) vẫn trả **403** nguyên văn như V6 (§1). Tài sản CC0; mã GPLv3 (không dùng). Đã dựng **1 người 1782 + 1 người 1943** bằng bộ nạp chỉ đọc dữ liệu. |
| 6.2 Mocap | CMU: **dùng được** ("free for all uses"). 100STYLE: **dùng được**, CC BY 4.0 (phải ghi công). Quaternius UAL: **dùng được**, CC0, nhưng **chưa tải được** (itch.io trả `{"errors":["invalid key"]}` 3 lần). Không nguồn nào có NC/SA/ND. Đã tải 6 clip 100STYLE + 3 clip CMU (SHA §2); bản thử rút hệ số chu kỳ đi. |
| 6.3 people.js | Thêm pháp tuyến mượt, khớp khuỷu, 5 tư thế (nghiêm, nghỉ, khiêng hòm, nói chuyện, cúi làm việc), bước đi bớt "kéo kéo", vân vải và da, che khuất theo độ cao, bóng tiếp đất. API không đổi. |
| 6.4 toy_like | Toàn khung: neo 1782 **8,00** · neo 1943 **7,00** · P4 **8,67 → 8,67** · P5 **8,67 → 8,67**. **Không đạt ≤ 4.** Bản people.js mới **không đổi điểm** (người chấm gọi trước/sau là "same frame"). Bản cắt gần cũng không đổi (P4 cắt 9,0 → 9,0; cảnh kiểm 8,0 → 8,0). **Người MPFB thử: 7,0** so với people.js 9,0 (cùng cận cảnh). |
| Chi phí Claude API | **$0,903** (chấm mù 12 lượt `claude -p` Sonnet: toàn khung $0,516 + cắt gần $0,214 + MPFB $0,173). OpenAI, ElevenLabs: 0. |

**Kết luận chính.** Shader và tư thế không kéo toy_like xuống được. Ở P4/P5, người chỉ cao 22–35 px. Người chấm nêu lý do là cả cảnh: nền cát phẳng, khối nhà hình hộp, đội hình lưới đều, người "peg". Ở cận cảnh, họ nêu "box torsos, stick legs, cone skirts", tức lỗi nằm ở **hình khối**. Đòn bẩy thật là thân người MPFB: bản thử thô (quần áo vẽ lên da, chưa có vải MHCLO) đã hạ điểm từ 9 xuống 7.

## 1. MPFB2 (6.1)
- **Lỗi nguyên văn**, HTTPS qua proxy, 18/10/2026, áp cho `https://github.com/makehumancommunity/mpfb2`, `codeload.github.com/.../zip/refs/heads/master`, `api.github.com/repos/makehumancommunity/mpfb2` và `.../releases/latest`:
  `HTTP/1.1 403 Forbidden` — `{"message":"GitHub access to this repository is not enabled for this session. Use add_repo to request access. If add_repo answers that read access is already available and you need GitHub API or write access, call add_repo again with access:\"push\" to attach the repository with credentials.","documentation_url":"https://docs.anthropic.com/en/docs/claude-code/github-actions"}`
- `raw.githubusercontent.com/.../LICENSE.md` trả **200**. Công cụ `add_repo` báo "read access is already available … anonymous git reads". `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1` **thành công** về `/home/user/makehumancommunity/mpfb2` (108 MB, ngoài repo).
- **Giấy phép, nguyên văn** (`giay-phep/mpfb2-LICENSE.txt`, SHA-256 `5cefb606…ce04d`): mã là GPLv3. Tài sản (base mesh, targets, rigs, poses, textures…) theo câu: "These assets have been released under CC0 1.0 Universal." Đầu ra theo câu: "the MakeHuman team makes no claim whatsoever over output such as … Renderings". Toàn văn CC0 ở `giay-phep/mpfb2-LICENSE.ASSETS.txt` (SHA `f6089cba…6d2c`).
- **Gói da** `makehuman_system_assets_cc0.zip` (files.makehumancommunity.org): SHA-256 `b542127a8e25547c7c29c19f2d1d2adb9a664c80396ecd694095dbc8028a0107`, 280 737 770 byte. Mỗi tài sản ghi "License CC0" (`giay-phep/makehuman-system-assets.txt`). Quần áo trong gói là đồ hiện đại, nên **chỉ dùng da**.
- **Dựng thử** bằng `design/pt/song/mpfb_thu.py` (bộ nạp chỉ đọc dữ liệu, không import mã GPL):
  - Đầu vào: `base.obj` cùng UV; macro male-young (cơ 0,3–0,35); caucasian-male-young; khung xương `rig.default.json` với vị trí khớp tính lại trên lưới đã biến hình; trọng số `weights.default.json` (CC0); tay hạ bằng tư thế xương.
  - Quần áo: vùng theo xương trội, phồng theo pháp tuyến 0,8–2 cm. Vạt áo 1782 và đai 1943 là lưới riêng. Thêm mũ tricorn hoặc Brodie.
  - Cycles 64 spp, 2 luồng, 1200×1000: **119 s**; dựng lưới 1,4 s; cao 1,776 / 1,772 m.
  - Ảnh: `/var/tmp/cine-out/g1b/nguoi/mpfb/mpfb-1782-1943.png`, kèm góc xa `mpfb-xa.png`; xem tờ so `to-so-nguoi.jpg`, hàng cuối.
  - Hạn chế: quần áo vẫn "bó sát như đồ bó"; mép vùng răng cưa; vùng tóc phủ lên chân mày; chưa có MHCLO cho áo khoác, ghệt và giày.

## 2. Dữ liệu chuyển động (6.2) — giấy phép nguyên văn trong `giay-phep/`
| Nguồn | Câu giấy phép (nguyên văn) | Kết luận | Tệp đã tải (ngoài git) · SHA-256 |
|---|---|---|---|
| CMU Graphics Lab | "This dataset of motions is free for all uses." · "The motion capture data may be copied, modified, or redistributed without permission." | **Dùng được** | `70.asf` 44c828dd…e34e · `70_03.amc` (xách vali 19,5 lb) 60030812…5974 · `69.asf` c3019031…605f · `69_69.amc` (đi, nhặt và mang vật) fa2ec067…961d · `02.asf` c9f5ff45…96cf · `02_01.amc` (đi) 1503c481…1492 |
| 100STYLE (Zenodo 8127870) | "For creative or commercial work please credit in an appropriate way. E.g. "The 100STYLE Dataset - Ian Mason". This work is licensed under a Creative Commons Attribution 4.0 International License ." · Zenodo `{'id': 'cc-by-4.0'}` | **Dùng được**, ghi công vào RIGHTS và credit | Đọc từng mục qua HTTP Range, không tải cả 1,47 GB: `Neutral_FW` 2f28800b…59f6 · `Neutral_ID` (đứng) 71aead2e…259f · `March_FW` 52b19fbd…c241 · `ArmsBySide_FW` 75f47b08…42b3 · `LawnMower_FW` d011a9c8…a1d · `Heavyset_FW` 85261977…72af (CRC32 khớp) |
| Quaternius UAL | "License CC0" · "Asset license Creative Commons Zero v1.0 Universal" · "these assets can be used for free without the need for attribution in commercial, educational, and personal projects . All models are under the CC0 License." | **Dùng được**; **chưa tải** | itch.io `/file/17958403` trả `{"errors":["invalid key"]}` 3 lần → dừng theo luật cùng lỗi ≥ 3 lần |

**Chọn clip:**
- Đi: 100STYLE `Neutral_FW`; lính hành quân: `March_FW`.
- Đứng: `Neutral_ID`.
- Khiêng/mang:
  - CMU `70_03` (xách một tay) và `69_69` (nhặt rồi mang).
  - 100STYLE `LawnMower_FW` (hai tay đẩy trước) **không phải khiêng**: gối gần như không dao động, r² 0,12.
  - Còn thiếu clip hai người khiêng cáng hoặc hòm.

**Bản thử** `mocap_gait.py`:
- Cách làm: FK trên BVH, lấy góc trong mặt phẳng dọc, gán pha cục bộ bằng Hilbert, rồi khớp 2 bậc Fourier. Kết quả ở `mocap-gait.json`.
- `Neutral_FW`, chu kỳ 1,385 s:

| Khớp | Biên độ bậc 1 | Bậc 2 | r² |
|---|---|---|---|
| Hông trái | 16,1° | 3,6° | 0,93 |
| Gối | 20,7° | 14,7° | 0,90 |
| Vai | 5,3° | — | 0,55 |
| Khuỷu | 3,8° | — | 0,23 |

- `March_FW`: hông 25,0°, gối 33,2°, khuỷu 58,5° (r² 0,91–0,96).
- people.js hiện dùng hông ±19,5° (0,34 rad). Khớp với đi thường; riêng gối thiếu bậc 2.
- Độ lệch trung bình hông +10,8° nhiều khả năng do trục "lên" lấy theo cổ–hông (thân hơi ngả trước). Cần kiểm thêm trước khi dùng.

**Cách áp lên people.js** (biến dạng đỉnh theo nhóm khớp, không skinning):
1. Mỗi nhóm khớp (hông/gối, vai/khuỷu) đọc góc từ một chuỗi Fourier thay cho `sin(ph)`.
2. Truyền hệ số bằng uniform mảng theo "kiểu đi" (thường, hành quân, khiêng). Mỗi người chọn kiểu qua `aQ.w`, nên chi phí GPU coi như không đổi.
3. Clip không có chu kỳ (nhặt, đặt hòm) phải lấy mẫu thành bảng góc theo thời gian (texture 1D) và phát theo `uT`.
4. Với người MPFB, nên dùng `rig.cmu_mb.json` và `weights.cmu_mb.json` (CC0, khung xương kiểu CMU MotionBuilder) để đổ thẳng BVH CMU lên, không phải đổi đích.

## 3. people.js (6.3) — `design/k2v/tl/people.js`
- **Đã làm:**
  - Pháp tuyến mượt cho lăng trụ và cầu (nắp, hộp, mũ giữ cạnh).
  - Nhóm khớp mới 10/11 (cẳng tay, khuỷu) và 12 (hòm khiêng).
  - Thuộc tính `aQ` (tư thế, hướng đầu, hạt) với 5 tư thế. `pickPose`: lính trong khối giữ nghiêm; dân, thuỷ thủ, kíp pháo và sĩ quan rải tư thế.
  - Hông ±0,34 rad, gối gập cả pha trước, khuỷu chùng.
  - Vân sợi, nếp, bụi gấu và giày; da có loang và hốc mắt; gỗ hòm có vân; che khuất theo độ cao.
  - Bóng tiếp đất: đĩa mờ, không ghi độ sâu. Đĩa bỏ đi ở mọi lượt mặt nạ (`uMask > 0.5`). `export6.js` tự loại đĩa khỏi Cycles (vật liệu trong suốt, `depthWrite` false).
  - Thêm `setPose(i, pose, head)` và `POSES`. API cũ không đổi.
- **Số đo** (`do-truoc-sau.json`, 1080p llvmpipe):

| Mục | Trước | Sau |
|---|---|---|
| Tam giác người chi tiết | 518–734 | 596–776 |
| Tam giác LOD | 244–340 | 256–352 |
| Điểm ảnh đổi > 8 mức xám | — | P4 0,86 % · P5 0,68 % · cảnh kiểm 5,3 % |
| s/khung P4 | 22,6 | 26,3 |
| s/khung P5 | 17,8 | 21,5 |
| s/khung cảnh kiểm | 15,2 | 23,2 |

  - **Lưu ý về s/khung:** số đo lẫn tải của phiên chính đang dựng song song (load 9–10 khi chạy "sau", 1–3 khi chạy "trước"), nên **chưa tách được** phần tăng do people.js. Cần đo lại trên máy rảnh.
- **Kiểm:** `node --check` đạt; 3 cảnh (vinh6, toan6, v6lab) dựng không lỗi shader. Golden steel/ll08 **chưa chạy lại**: các cảnh đó không có người, nhưng phiên chính nên chạy trước khi merge. Mặt nạ người không đổi cơ chế (`maskify` giữ nguyên).
- **Hòm khiêng** là vật nền phụ (Q-PT4-3 lớp b): hòm gỗ đai sắt, không chữ, đúng thời kỳ 1782.

## 4. Chấm mù toy_like (6.4) — `blind_toy.py`, phiếu ở `cham-mu*/`
- **Giao thức:**
  - `claude -p --model claude-sonnet-5-5 --allowedTools Read`, thư mục tạm chỉ chứa ảnh đã đổi tên ngẫu nhiên (1280 px).
  - 3 vai: người xem YouTube lịch sử, hoạ sĩ dựng 3D, sử gia quân sự.
  - Mỗi lượt có 6 ảnh, tên và thứ tự hoán vị theo hạt `20261018-<lượt>-<vai>`; chấm 2 lượt, tổng 6 phiếu cho mỗi ảnh.
  - Thang toy_like 1–10 (thấp = ít giống đồ chơi) và people_craft 1–10.
  - Phiếu ghi model phục vụ gồm cả claude-haiku-5-5, là tác vụ phụ của CLI; model chấm là Sonnet.

| Khung | toy_like TB | people_craft TB | n |
|---|---|---|---|
| Neo 1782 (`1782-trua-LAI-notext.jpg`) | **8,00** | 3,33 | 6 |
| Neo 1943 (`1943-trua-LAI-notext.jpg`) | **7,00** | 4,00 | 6 |
| P4 hero, trước | **8,67** | 3,00 | 6 |
| P4 hero, sau (people.js mới) | **8,67** | 3,00 | 6 |
| P5 toàn cảnh, trước | **8,67** | 2,17 | 6 |
| P5 toàn cảnh, sau | **8,67** | 2,17 | 6 |
| Cắt gần P4, trước → sau (3 phiếu) | 9,0 → 9,0 | 3,0 → 3,0 | 3 |
| Cảnh kiểm v6lab cận, trước → sau | 8,0 → 8,0 | 3,67 → 3,67 | 3 |
| **Người MPFB thử (cận)** so với people.js mới (cận) | **7,0** · 9,0 | 3,67 · 3,0 | 3 |

- **Ghi chú:**
  - Thang V6 là 0–10 trên cả khung; thang ở đây là 1–10 và hỏi riêng về người, nên **không so trực tiếp** với 6,61 hay 5,83 của V6.
  - Mục tiêu ≤ 4 **không đạt** ở mọi khung. Điểm thấp nhất là neo 1943 (7,0) và MPFB thử (7,0).
  - Lý do lặp lại trong phiếu:
    - Khung neo: "waxy / plastic dolls pasted in", "stiff mannequin poses", "clone-like".
    - P4/P5: "tabletop wargame minis", "flat sand", "no contact shadows", "perfect grid blocks".
    - Cận cảnh people.js: "box torsos, stick legs, cone skirts".
  - Có 2/3 phiếu cắt P4 "sau" nhận ra người khiêng hòm và tư thế khác, nhưng không đổi điểm.

## 5. Đề xuất (chờ chủ dự án)
1. **Chuyển người sang thân MPFB** cho khung neo và hero (Cycles/sprite như nguoi6), dùng quần áo MHCLO tự làm theo nguồn quân phục.
   - Ưu: hình khối người thật; bản thô đã hạ toy_like 9 → 7.
   - Nhược: làm quần áo tốn công (áo khoác 1782, battledress 1943).
   - Tác động: khung neo và hero.
   - Rủi ro: thân "bó sát" nếu thiếu vải; tay chân đơn điệu nếu thiếu mocap.
2. **Bản SẢN XUẤT llvmpipe:** lưới MPFB proxy thấp (proxymeshes CC0 trong gói) cho người ≥ 30 px; người < 22 px giữ lưới thô.
3. **Bố cục P4/P5:** người chấm chê đội hình lưới đều, nền phẳng và người quá nhỏ. Đây là việc của cảnh, không phải people.js. Cần phá lưới đội hình, thêm vân nền và máy gần hơn ở shot hero.
4. **Mocap:** áp Fourier `Neutral_FW` và `March_FW` vào shader (rẻ). Ghi 100STYLE vào RIGHTS (CC BY: "The 100STYLE Dataset - Ian Mason"). CMU và Quaternius ghi nguồn tuỳ chọn.
5. **Bóng tiếp đất:** người chấm vẫn ghi "no contact shadows". Có thể tăng độ đậm (0,42 → 0,6) và chạy lại một lượt chấm, chi phí khoảng $0,17.

## 6. Chỉ số trong ±5 % quanh ngưỡng
Không có. toy_like thấp nhất là 7,0, cách ngưỡng 4 tới 75 %.

## 7. Tệp
- Mã: `design/k2v/tl/people.js` (sửa), `design/pt/song/mpfb_thu.py` (mới), `reports/g1b-t3/nguoi/blind_toy.py`, `mocap_gait.py`.
- Số đo: `do-truoc-sau.json`, `mocap-gait.json`, `cham-mu/score.json`, `cham-mu-cat/score.json`, `cham-mu-mpfb/score.json` (kèm phiếu và raw). Ảnh chấm đã xoá; tạo lại bằng `blind_toy.py set`.
- Tờ so: `to-so-nguoi.jpg` gồm 3 hàng: cảnh kiểm trước/sau, P4 cắt trước/sau, MPFB thử.
- Giấy phép: `giay-phep/` gồm CMU, 100STYLE, Quaternius, MPFB2 (2 tệp), MakeHuman system assets.
