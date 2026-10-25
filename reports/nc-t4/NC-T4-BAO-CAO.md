# NC-T4 — BÁO CÁO NGHIÊN CỨU cho animatic v2 T4 London (K2C-T4-02)

## §0. Nhánh, căn cứ, phạm vi

- **Nhánh thật: `k2c-t4-02-nc`**, tạo từ `origin/main` @df317915. Đã đẩy, KHÔNG merge. Harness gợi ý nhánh `claude/dazzling-cori-gcl9ho`, nhưng phiên đẩy được nhánh chủ dự án yêu cầu nên dùng nhánh đó. SHA đỉnh ghi ở commit cuối "DỪNG chờ chủ dự án".
- Đầu vào chỉ đọc: nhánh ANIMATIC-T4 `origin/ccr-21ab5d6f-7l1yln` @393c3b55, gồm:
  - `BANG-SHOT-v2.json`, git blob dacdd66e;
  - `animatic/log-shot.json`, git blob 556c3475;
  - `PHIEU-XEM.md` và `k2check-1.17.4-animatic.md`;
  - `loi-khoa.txt` trên main.
- Căn cứ: chủ dự án 25/10/2026 06:56 (nhận xét 1–4) và 07:01 (N1–N6 "theo khuyến nghị").
- Phiên NGHIÊN CỨU: không dựng hình, không gọi AI sinh ảnh/video, không thu giọng. Không sửa `checks/`, `docs/`, sổ, `design/`, LOI-NHAP/loi-khoa/BANG-SHOT, main. Không đọc mã trong `checks/`.
- Vận hành:
  - preflight `set -o pipefail` qua `reports/nc-t4/cam_commit.sh`, chỉ commit khi có "— ĐẠT" + "PREFLIGHT ĐẠT"; `lock.py --verify` KHỚP mọi lần;
  - hook pre-commit + pre-push cài lúc 00:12 UTC, trước lần đẩy đầu;
  - không force-push, không amend;
  - email trong trang nguồn đã che (`[email-đã-che]`); một lần preflight CHẶN P1 vì email trong văn bản CC, đã che rồi commit lại;
  - UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`.
- Ba luồng nghiên cứu chạy song song bằng tác tử phụ trong phiên: quyền tư liệu 1940; footage 2026; chân dung + ảnh 1850–1950. Phiên chính kiểm lại từng kết quả: mở JSON giấy phép, grep câu trích trong tệp nguồn đã lưu.

## §1. Việc 1 — Điểm nhấn (15 mục, 1666 → 2026)

`DIEM-NHAN.md` + `DIEM-NHAN.json`. Mỗi mục ghi: ngày, nơi, người, hành động; hình M-d trung/cận hoặc công trình; nguồn (tệp/URL, dòng, ngày đọc, trích nguyên văn, bậc §12.2); kết luận; shot thay; thẻ ≤ 6 từ; lời. **43/43 câu trích khớp nguyên văn** tệp nguồn, kiểm bằng máy (`scripts/k2ldn/nc/kiem_trich.py`).

Kết quả kiểm các ứng viên chủ dự án nêu:

| Ứng viên | Kết luận | Nguồn chính (bậc) |
|---|---|---|
| Pepys báo tin ở Whitehall 2/9/1666 | **GIỮ** | Pepys pg4167 dòng 1103–1112 (2, sơ cấp) |
| Charles II + James chỉ huy chữa cháy, phá nhà | **GIỮ** | Pepys dòng 1168–1170 (sà lan, "pull down houses apace"), 1238–1240; Evelyn 6/9 dòng 1061–1067 ("even laboring in person") (2) |
| Mái chì Old St Paul's chảy 4/9 | **GIỮ** | Evelyn 4/9 dòng 1001–1006; 7/9 dòng 1095–1098 ("six acres … totally melted") (2) |
| Wren trình phương án 11/9 | **SỬA**: "by 11 September 1666" | All Souls catalogue; London Museum ("Just six days after the fire") (TC-CQ) |
| Viên đá đầu tiên St Paul's mới | **SỬA**: chỉ dùng năm 1675 | Thornbury 1878: 21/6/1675 do Wren đặt; St Paul's: Thomas Strong đặt — mâu thuẫn người đặt; Parentalia: 1675 |
| Monument hoàn thành | **GIỮ** 1677 (khởi công 1671) | City of London, themonument.org.uk (TC-CQ) |
| Viên đá cuối đèn lồng 1708 — ai đặt | **GIỮ** 10/1708, Wren con + Edward Strong | St Paul's "Our timeline" (TC-CQ); Parentalia 1750 xác nhận người đặt nhưng ghi hoàn thành 1710, Thornbury cũng ghi 1710 → **lệch, ghi lại** |
| Dỡ nhà trên cầu London | **SỬA** lời: "from 1758" | London Museum: 1758–62; Thornbury: 1757–60 |
| Kè Victoria và Bazalgette | **GIỮ** 2/1864 – 13/7/1870 | Thornbury 1878 (BHO) |
| St Paul's Watch 29/12/1940 | **GIỮ** | St Paul's (28 quả bom; bơm nước, bao cát; Godfrey Allen) |
| Câu Churchill | **BỎ** | không có văn bản sơ cấp/cơ quan (§9) |
| Barbican / London Wall | **GIỮ** | City of London: khởi công 1965, 11 năm; Cripplegate còn 48 cư dân năm 1951 |
| Cụm tháp + tầm nhìn bảo vệ | **GIỮ** | City SPD 2012: Allen đề xuất 1937, áp dụng từ 1938; King Henry's Mound |

Điểm nhấn mới phiên tìm được:
- **DN01:** Evelyn + "Dr. Wren" đề xuất "a noble cupola" cho Old St Paul's ngày 27/8/1666, sáu ngày trước cháy (Evelyn dòng 916–933). Đây là một nhịp truyện mạnh nối mái vòm cũ với mái vòm mới.
- **DN06:** tượng Gresham rơi khỏi hốc mà vẫn nguyên (Evelyn 7/9).

Lỗi nhỏ ở nguồn cơ quan: trang St Paul's "Our timeline" mục Wren ghi "on September 3rd 1666, a fire began". Phiên không dùng câu đó.

## §2. Việc 2 — Nhân vật

Chi tiết: `NHAN-VAT-ANH.md` §1–§2. Tệp ≤ 2,1 MB trong `channel-k2/k2c-t4-02/nc/anh/`; bằng chứng JSON nguyên văn + SHA trong `nc/licenses/`.

| Nhân vật | Bản dùng | Rủi ro |
|---|---|---|
| Charles II | Samuel Cooper, tiểu hoạ vẽ từ người thật (Met 435943, `isPublicDomain: true`) | thấp |
| James, Duke of York | Loggan, bản khắc (Rijksmuseum, PDM), năm rộng 1643–1692 | vừa (năm) |
| Pepys | Wellcome puwvaf8q (PDM), chân dung sau 1685 | vừa |
| Evelyn | Nanteuil, bản khắc (Wellcome, PDM) | thấp |
| Wren | `nga-wren`, đã có từ trước (NGA CC0) | thấp |
| Bazalgette | ảnh c.1862–67 (Rijksmuseum, PDM/CC0), cắt từ trang album, ≈ 800–900 px | thấp |
| Churchill | LoC FSA/OWI, 1943, 856×1024 | thấp quyền / không đúng năm 1940 |

- **Robert Hooke không có chân dung xác thực.** Trích Royal Society: "There are no known portraits of Robert Hooke…". → chỉ thẻ chữ, không dựng mặt.
- Bludworth, Barbon, Godfrey Allen, Holden, Holford, Matthews: không tìm được bản sạch quyền → chỉ thẻ chữ.
- NPG London: 403 Cloudflare (ảnh của NPG là CC BY-NC-ND → không dùng được cho phim bán).
- Cách dùng đề xuất: chân dung chỉ cho **thẻ nhân vật** (≤ 5 s, §17 (3)) và làm **tham chiếu trang phục/dáng** cho ảnh đầu Omni (không đưa mặt). Dựng nhân vật có tên trong M-d còn chờ P2 (§15 (f) đang cấm).

## §3. Việc 3 — Ảnh chụp 1850–1950

`NHAN-VAT-ANH.md` §3: 15 tệp ảnh/bản vẽ City 1850–1930 từ LoC Photochrom ("No known restrictions on publication."), Rijksmuseum (PDM/CC0), Met (CC0), Wellcome (PDM). Phủ được:
- H3-01: St Paul's & Blackfriars của G.W. Wilson; photochrom St Paul's;
- H3-02: London Bridge;
- H3-03: Embankment, kèm bản vẽ thi công 1865;
- phố City: Cheapside, Ludgate 1892, Fleet Street 1895;
- H3-04: chỉ Mansion House.

**Thiếu:** ảnh chụp thi công Embankment thập niên 1860 và ảnh City 1930s sạch quyền. Ảnh Keystone ở LoC chưa đánh giá quyền.

## §4. Việc 4 — Ảnh/phim 1940

Chi tiết: `TU-LIEU-1940.md` + `tu-lieu-1940.json` (21 ứng viên). Phiên chính đã đối chiếu câu trích trong tệp nguồn đã lưu.
- **Ảnh Crown chụp 1940 đã hết bản quyền.** CDPA Sch.1 + Luật 1956 s.39; flowchart TNA: "Copyright expires 50 years after creation".
- **Phim Crown 1940:** CDPA Sch.1 para 7(1): "No copyright subsists in a film, as such, made before 1st June 1957". Khung hình tính như ảnh. Còn nghi vấn quyền lời bình của Quentin Reynolds (mất 1965) → dùng hình câm.
- **"St Paul's Survives" (Herbert Mason): LOẠI.** Mason mất 1964, bản quyền tại Anh còn tới khoảng 2034. Commons xoá năm 2018 "per discussion, copyrighted by Herbert Mason". **Không dựng lại bố cục bằng AI.**
- **Không có ảnh Crown sạch quyền của chính đêm 29–30/12/1940.** Ứng viên rủi ro thấp: IWM D 1301, D 1091, D 4325, D 6418 (St Paul's 1941–42), TR 1693 (màu 1944), bản Commons 550–1300 px. Muốn bản HD phải mua bản sao từ IWM; IWM/TNA thừa nhận Crown copyright hết hạn nhưng đặt điều kiện hợp đồng phi thương mại cho bản số hoá của họ.
- **Phim *London Can Take It!*:** bản Internet Archive là SD, nhãn PD do người tải tự gán. Bản HD qua IWM (COI 943) hoặc BFI; giá niêm yết BFI cho phim tài liệu "£4,320 for the first 60 seconds and £72.00 per second thereafter".

## §5. Việc 5 — Footage London hiện nay

`FOOTAGE-2026.md` + `footage-2026.json`.

| Shot | Ứng viên miễn phí | Giấy phép | Ghi chú |
|---|---|---|---|
| H5-05a | Pexels P1 (Millennium Bridge, 15/05/2026, 4K) | giấy phép Pexels | |
| H5-06 | Commons C2 (drone 2022) | CC BY 3.0 | mang nhãn "License review needed" |
| H5-07 | Commons C1 (timelapse Waterloo Bridge 2016) | CC BY 3.0 | **thiếu 22 Bishopsgate** — không dùng cho "2026" |
| H5-07 | Pixabay X1 (2023, 1080p) | giấy phép Pixabay | |
| (vài giây) | Commons C3 | CC BY 3.0 | giấy phép đã được bot xác nhận |

- **H5-04, H5-05b, H5-08: không có clip miễn phí đạt.**
- CC BY-SA: crop/chỉnh màu gần như chắc chắn tạo "Adapted Material" → phim phải mang BY-SA, không được gắn DRM → **không dùng** cho phim bán.
- Trang giấy phép Pexels/Pixabay: curl 403; WebFetch chỉ trả trích ngắn qua mô hình tóm tắt, **chưa đối chiếu bản gốc** → chủ dự án lưu PDF tay.
- Báo giá (KHÔNG mua): Getty 3 clip, giá ẩn khi chưa đăng nhập, EULA không nói rõ việc bán phim thành phẩm → hỏi Getty bằng văn bản; Storyblocks Business: "Get a Quote" (Individual $21–30/tháng chỉ cho YouTube "1x channel").

## §6. Việc 6 — Mở đầu mới

`MO-DAU.md`. Chẩn đoán: 10 s đầu M01 là **tấm nền AI tĩnh** trên CODINH (k2check: "trôi chậm 9,83 s từ 0:00.0"). Ba phương án:
- **A "Lửa trước"** (khuyến nghị);
- **B** "2026 có máy + chớp lửa";
- **C** "Footage thật trước".

Danh sách 16 shot "đứng" (CODINH > 8 s hoặc khung tĩnh đo > 6 s). Các khung tĩnh đo được nặng nhất:
- H5-05a: 14,04 s;
- H4-04c: 9,21 s;
- H3-05: 8,83 s;
- H5-05b: 8,75 s;
- H5-07b: 7,12 s.

Mỗi shot có cách sửa: rút, cú máy chậm, lớp sống, hoặc chèn điểm nhấn.

## §7. Việc 7 — Bố trí + ước

`bo-tri/ke-hoach-A|B|C.json` → `bo-tri/uoc-A|B|C.json` (script `scripts/k2ldn/nc/bo_tri.py`, đọc `log-shot.json` @393c3b55). Bảng điểm nhấn × shot × lớp ở `DIEM-NHAN.md` (cột Shot/Lớp) và trong `ke-hoach-A.json`.

| Chỉ số (phương án A) | v1 animatic | Sau bố trí A | Ngưỡng | ±5 % |
|---|---|---|---|---|
| Thời lượng | 730,1 s | **760,0 s** (12:40) | ≤ 780 s (13:00) | **CÓ** |
| Omni M-d % | 20,36 | **27,98** | mục tiêu ≈ 28–30 | **CÓ** |
| Góc cao / thân phim % | 67,50 | **61,24** | ≥ 60 | **CÓ** |
| Tổng AI % (M-d + tấm nền) | 24,95 | 30,35 | ≤ 70 | không |
| Tấm nền N2P % | 4,59 | 2,37 | mục tiêu 5–15 (V7) | (đã trượt từ v1) |
| TL + KHAC + THE % | 9,66 | **12,04** | trần cũ 10 | **VƯỢT** → P8 |
| Ảnh/footage thật % | 0 | 1,45 | — | — |
| Tư liệu tổng (đề xuất TU-LIEU-15) | 9,66 | 13,49 | ≤ 15 | không |
| THAP % | 9,21 | 9,17 | ≤ 12 | không |
| Bản đồ % | 4,58 | 4,40 | ≤ 12 | không |
| Cắt/phút (ước) | 6,39 đo | 7,03 | trần TL-1 (c) 5 | (đã trượt từ v1) → P9 |
| M-d mỗi clip | ≤ 8 | ≤ 8 (clip mới 8 s chạm trần) | ≤ 8 | **CÓ** |
| Gemini T4 tổng | $8,54 | **$44,81** | ≤ $55; mốc $45 | **CÓ** (mốc) |

- **Lớp của ảnh/footage thật (đề xuất cho K):** lớp mới **THAT**. Không tính AI. Không tính góc cao khi chiếm toàn khung. Tính chung với TL + KHAC + THE dưới trần **TU-LIEU-15**. Ảnh chồng góc khung (≤ 1/3) giữ góc của shot nền.
- **Gemini:**
  - nháp 360p: 82,2 s (64 s mới + 18,2 s đổi) × $0,035 × 3 lượt = $8,63;
  - bản cuối 720p: 212,7 s × $0,10 × 1,3 = $27,65.
  - Ảnh đầu OpenAI ≈ ≤ $3,1 (ngoài ngân sách Gemini).
- **ElevenLabs:** **868 ký tự** cần thu (6 câu mới + 3 câu sửa thu lại cả câu). Thêm ròng +589 ký tự sau khi bỏ câu Churchill (82 ký tự).
- Phương án B: 754,0 s · M-d 28,20 % · góc cao 60,93 %. Phương án C: 756,0 s · 28,13 % · **60,22 %**.
- Góc cao tính theo điểm máy (cao/thấp) trên `log-shot.json`; bảng v2 tự khai 66,52 %, k2check đo 67,5 %. K đo lại trên video ở vòng sau.

## §8. Việc 8 — Phiếu

`PHIEU-NC-T4.md`: P1 mở đầu; P2 nhân vật có tên trong M-d; P3 tick 15 điểm nhấn; P4 câu Churchill; P5 lời mới từng câu; P6 tư liệu hình; P7 footage; P8 lớp ảnh thật / TU-LIEU-15; P9 nhịp cắt; P10 ngân sách Gemini.

## §9. Nguồn đã đọc (ngày đọc 25/10/2026)

Bản văn bản lưu ở `reports/nc-t4/nguon/web/` (tiền tố `dn-*` là của phiên chính; còn lại của ba luồng). Nguồn PD trong repo: `reports/nc-n2p/nguon/pg4167.txt` (Pepys, SHA 8a7ec38e…), `pg42081.txt` (Evelyn, SHA 912a1791…).

| Nguồn | URL | Trích (rút gọn) |
|---|---|---|
| St Paul's "Our timeline" | https://www.stpauls.co.uk/our-timeline | "In October 1708, the Cathedral was topped out, and the last stone was laid on the lantern…"; "On the 25th December 1711, Parliament declared…"; "28 small explosive devices fell on and around the Cathedral" |
| St Paul's Watch | https://www.stpauls.co.uk/st-pauls-watch-protect-cathedral | "This time, their leader was Surveyor to the Fabric Godfrey Allen." |
| The Monument (City of London) | https://www.themonument.org.uk/history | "construction work commenced in 1671"; "It took six years to finish…"; "completed and opened in 1677" |
| All Souls, Wren drawings | https://library.asc.ox.ac.uk/wren/london_plan_1666.html | "presented to the king by 11 September 1666" |
| London Museum 435888 | https://www.londonmuseum.org.uk/collections/v/object-435888/ | "Just six days after the fire, Wren showed his rebuilding plan to the king." |
| London Museum 99769, 102498 | …/object-99769/, …/object-102498/ | "When the houses were cleared in 1758-62"; "London Bridge after the fire on 11 April 1758" |
| BHO, Old and New London (1878) | british-history.ac.uk node 37716, 37832, vol2 pp9-17 | "The first stone was laid by Wren on the 21st June, 1675"; "commenced in February, 1864"; "not removed till 1757–60" |
| Parentalia (1750), archive.org | https://archive.org/details/gri_33125011157357 | "The higheft or lafl Stone … laid by the Hands of the Surveyor’s Son" (OCR) |
| City of London, Protected Views SPD 2012 | cityoflondon.gov.uk …/planning-spd-protected-views-spd-2012.pdf (SHA cc99c0bf…) | "submitted to the City of London Corporation in 1937"; "implemented from 1938" |
| City of London, Barbican Estate | https://www.cityoflondon.gov.uk/services/barbican-estate/barbican-estate-history | "Construction for the Barbican Estate started in 1965 and took 11 years to complete." |

Nguồn của việc 2–5 (TNA, legislation.gov.uk, IPO, BFI, Internet Archive, Commons, Met, NGA, Rijks, Wellcome, LoC, Royal Society, CC, Pexels/Pixabay, Getty, Storyblocks) ghi đầy đủ URL + trích ở `TU-LIEU-1940.md` §1–§2, `NHAN-VAT-ANH.md`, `FOOTAGE-2026.md` §1–§4.

## §10. Trang không mở được (không vượt rào — đề xuất chủ dự án mở tay)

| Trang | Lỗi |
|---|---|
| historicengland.org.uk (list entry 1079157, 1193901; Blitz Stories St Paul's) | 403 (curl + WebFetch) |
| london.gov.uk LVMF SPG | 403 |
| iwm.org.uk (licensing, copyright, non-commercial licence, terms, film licensing, trang object) | 403 Cloudflare |
| film.iwm.org.uk | 502 |
| images.nationalarchives.gov.uk | 403 |
| npg.org.uk | 403 Cloudflare |
| pexels.com/license, pixabay license-summary/terms | 403 curl (WebFetch chỉ trích ngắn) |
| Pond5, Adobe Stock | 403 |
| Shutterstock | trang rỗng |
| fleetstreetsfinest.com | 403 |
| archive.org/about/terms | trang chỉ có khung JS |
| Commons/Wikipedia API | 429 nhiều lần (đã chờ, thử lại) |
| stpauls.co.uk/history-collections/history | khung JS, không có mốc năm → dùng trang "Our timeline" |

## §11. Chi phí thật

- Claude API gọi trực tiếp: **$0** (mốc $2). Phiên và ba tác tử phụ chạy trong phiên Claude Code; token tác tử phụ ≈ 603 nghìn.
- OpenAI, Gemini, ElevenLabs, RunPod, YouTube: **$0**, 0 lệnh gọi → sổ AI rỗng.
- Giờ máy ≈ 0,9 h (trần 4 h).
- Đĩa: tệp gốc ngoài git `/var/tmp/nc-t4/goc/` 326 MB; SHA trong `nc/licenses/SHA256-NC.txt`; tái tạo bằng `scripts/k2ldn/nc/tai_nc.py`.
- Trong git: `nc/anh` ≈ 20 MB (21 tệp ≤ 2,1 MB).

## §12. Chỉ số nằm trong ±5 % quanh ngưỡng (nêu tên)

- Thời lượng 760,0 s / 780 s.
- Omni 27,98 % / 28 %.
- Góc cao 61,24 % / 60 % (phương án C: 60,22 %).
- Gemini $44,81 / mốc $45.
- M-d mỗi clip 8 s / 8 s.
- Lời mới 9 câu + 1 câu bỏ = 10 / 10 câu.

## §13. Dòng sổ đề xuất (phiên P ghi)

**RIGHTS.md**, sau khi chủ dự án tick P6/P7:
- 21 tệp `nc/anh/*` với nơi giữ, số hiệu, giấy phép nguyên văn, bằng chứng `nc/licenses/<id>.json`, rủi ro (theo `NHAN-VAT-ANH.md`);
- ảnh MoI Crown được chọn (IWM D-số qua Commons, "Crown copyright expired");
- clip footage được chọn: CC BY 3.0 ghi tác giả; Pexels/Pixabay kèm PDF giấy phép do chủ dự án lưu;
- dòng **LOẠI**: Mason "St Paul's Survives" — còn bản quyền, không dựng lại bằng AI;
- văn bản nguồn Parentalia 1750 (archive.org, PD) và City SPD 2012 (dữ kiện).

**AUTHORSHIP.md**, khi chủ dự án duyệt:
- chọn mở đầu (P1);
- quyết định nhân vật có tên (P2) — sửa Kinh thánh §15 (f) nếu (b);
- danh sách điểm nhấn (P3);
- bỏ câu Churchill (P4);
- 9 câu lời mới/sửa (P5) — đóng góp biểu đạt của chủ dự án: chọn và duyệt câu, thứ tự.

**Gửi K (khiếu nại/đề xuất, `checks-appeal.md` do P chuyển):**
- TU-LIEU-15 + lớp THAT (P8);
- miễn ranh M-d/tư liệu ở TL-1 (c) (P9);
- cách tính Q33 với khung P1 lặp ở mở lạnh A.

## §14. Việc đang chờ chủ dự án

1. Phiếu `PHIEU-NC-T4.md` P1–P10.
2. Mở tay và lưu PDF: giấy phép Pexels + Pixabay; trang IWM licensing/non-commercial; Historic England Blitz Stories (nếu muốn thử lại câu Churchill); NPG; LVMF.
3. Xem trực tiếp khung clip Pexels P1, Pixabay X1, Commons C1, C2.
4. Duyệt dùng thẻ Pepys (chân dung sau 1685), James (năm chưa rõ), Churchill (1943).
5. Có xin báo giá stock (Getty bằng văn bản, Storyblocks Business) và báo giá HD *London Can Take It!* (IWM/BFI) không — phiên KHÔNG mua.

Sau khi chủ dự án trả lời, phiên P ghi sổ, sửa bảng shot v3 và giao phiên dựng animatic v2.
