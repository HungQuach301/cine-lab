# K2C-T1-06 · G2 — báo cáo (phiên P, 14/10/2026)

> Nhánh `k2c-t1-06`. Lệnh: chạy tới G2 theo kế hoạch G1a (giọng → nháp → một lượt sửa → 1080p → QC + chấm mù một lần → gói phát hành), dừng ở G2.
> Quyết định chủ dự án 13/10 22:17 (gói phát hành 1 Short, không thumbnail) đã áp. **DỪNG ở G2, chờ duyệt.**

## Tóm tắt
- **Bản cuối:** 15:41 (941,04 s, 22 585 khung), 1920×1080, 24 fps, −14,0 LUFS / −1,6 dBTP. **1 Short (S1)** 15,25 s, −14,0 LUFS / −2,0 dBTP.
- **Luật K chính thức trên bản cuối (checks 1.10.2, LOCK c598467f… KHỚP):** Q26b · Q32 · Q33 (có pHash trên master) · Q34 đều **ĐẠT**. Kiểm mép chữ 48 px: **0 vi phạm** (12 đoạn + S1).
- **QC nhà máy (`qc.py`):** 26/29 mục đạt. 3 mục trượt (Q14, Q15, Q17) là luật nhịp LL bị áp nhầm cho tập kênh 2 vì mã "…-06" → đã ghi khiếu nại cho K (`checks-appeal.md`), không đổi gì để vượt.
- **Chấm mù một lần trên 1080p:** Q27 tay nghề TB **6,17/10**, 3/3 người chấm xếp **"above"** (trên video faceless thông thường; Steel 5,1 và "similar"). Q31: 0 điểm nối bị đa số coi là gãy; J07 bị 1/3 coi là gãy. Còn 4 điểm hình người chấm cùng chỉ ra, **chưa sửa** (đã dùng lượt sửa; chờ chủ dự án — D2).
- **Chi phí:** API G2 $0,77 (luỹ kế tập **$9,06 / $40**). ElevenLabs: phiên này gửi 7 513 ký tự (thu lại ASR). Giờ máy 1080p ≈ 15,5 giờ đồng hồ.

## 1. Giọng (Eric, `eleven_multilingual_v2`)
- 12 đoạn + 2 Short đã thu, commit ở `k2c-t1-06/vo/` (tệp thường, như K2G-01).
- **Số đọc sai trong TTS:** "4,440" → ~"4,040"; "377,000" → "three to 97,000" (ASR small.en và medium.en cùng nghe). Sửa bằng cách viết bằng chữ **đúng những từ của lời khoá** chỉ trong chuỗi gửi TTS (`make_spec.py` `TTS_SPELL`); script.md giữ chữ số; `say` của c20/c35b đổi theo.
- **ASR (`asr.py`, small.en):** 13/14 đạt. Đoạn 10 bị báo thiếu 25,000 và 100,000 sau 3 lần thu; whisper small.en và medium.en chạy trực tiếp trên cùng tệp đều nghe đúng → **báo nhầm của công cụ**, không thu thêm. Bằng chứng `k2c-t1-06/kiem-mu/asr-doan10-13-10.txt`.

## 2. Nháp 960×540 → QC → một lượt sửa
Chi tiết: `k2c-t1-06/nhap/SUA-NHAP.md` (+ `qc-nhap.md`, `TO-KHUNG-NHAP-1…5.jpg`).
- **Máy bắt:** Q2 (clip Pexels 24p nhồi 29,97 → `decimate`), Q5 (chữ phụ #9AA7B5 → #B8C2CE), Q13 (hook S1 viết bằng chữ đúng cụm `say`), **Q21 38 → 0** (chuỗi nguồn tự do → khoá nguồn thật, credit vào dòng nguồn), Q22/mép (thẻ kết tự co, nhãn S1, thẻ 07), **Q23 10 → 0** (`say` quá ngắn khớp nhầm: "four", "six stories").
- **Mắt thấy trên tờ khung (máy không bắt):** chữ chú thích đè dòng nguồn khi có số lớn; biểu đồ `ch_pew` trống 13 s trong lúc lời giới thiệu Pew (thêm góc `sa_corr`); crane-up cắt đỉnh cột và làm cột 110 trông thấp hơn cột 100 (đổi `front-dolly`); `ch_icc` **mất nhãn số** vì id `yes`/`no` bị YAML đọc thành boolean; khối đen ở mép khung = đầu mút tường studio; `lo_pencil` 11 s chỉ có lô trống (`grow: -1` → NaN); trang CFR không đọc được (góc `detail`).

## 3. Bản 1080p
- Dựng lại toàn bộ (mọi stamp cảnh đinh đổi sau lượt sửa nháp). Cảnh đinh 1080p SPP 4: 12:50 → 00:31 = **11 giờ 41 phút** (3 tiến trình); render lớp chữ 49 phút; mix + ghép 36 phút.
- **QC 1080p + tờ khung → sửa thêm 4 điểm** (máy chỉ bắt luật nhịp; cả 4 là lỗi mắt thấy):
  1. `m_calif0`: California nằm dưới dải chú thích → máy dời về phía nam (dựng lại 1 cảnh, 6 phút).
  2. `sa_fire`: 3 nhãn chồng nhau → trái / trên / phải.
  3. Thẻ "On housing production, the record is mixed": mục 3 đè dòng nguồn 4 nguồn → `px 34, gap 22, top 160`.
  4. Thẻ list có `top` bám trên thay vì căn giữa (dòng nguồn 3 dòng ở đáy thẻ). Đổi `lib/k2.js` → render lại lớp chữ cả 12 đoạn + S1 (89 phút).
- Lỗi nghiêm trọng sau đó: không.

## 4. QC cuối trên bản cuối
### 4.1 Luật K chính thức (checks 1.10.2; đầu ra ở `k2c-t1-06/g2/`)
| Luật | Kết quả |
|---|---|
| LOCK | `checks/lock.py --verify` **KHỚP** c598467f2283b141b8a14382c18dbe23b370522ef2a1afb31856399f7eb4549e (origin/main không có commit mới sau merge 13/10) |
| **Q26b** (`q_setting.py <episode.yaml> --tl <timeline.json>`) | **ĐẠT** · 35 bối cảnh · lớn nhất chart3d/bars 16,5 % (trần 25 %) · liên tục dài nhất 55,5 s (trần 90 s) · nửa sau 11 · trung tính 20,5 % |
| **Q32** | **ĐẠT** · 25 đoạn footage/ảnh có `p.clip` · nguồn ngoài 14,0 % (trần 40 %) · clip dài nhất 7,93 s |
| **Q33** (`--video` master, pHash θ = 14) | **ĐẠT** · 95 góc máy · 0 góc > 2 · pHash thêm 12 lần lặp không khai, không góc nào vượt 2 |
| **Q34** | **ĐẠT** · 103/103 shot có type · scene3d 31,2 % · map 19,9 % · chart3d 21,5 % · photo 10,6 % · document 1,1 % · footage 2,3 % · card 13,4 % · số neo hiện bằng 3D 79 % (ngưỡng 60 %) · 14 địa danh · 3 nhân vật |
| Q21 / Q23 | 0 / 0 |

### 4.2 QC nhà máy (`scripts/ll/qc.py`, `k2c-t1-06/g2/qc-v1.md`)
Đạt: Q1 judder 0 · Q2 0 · Q3 0 · Q4 loudness (master −14,0/−1,6; S1 −14,0/−2,0) · Q5 tương phản thấp nhất 4,85 (ngưỡng 4,5) · Q6 33,4 px · Q7 · Q8 · Q9 22 585/22 585 · Q10 S1 15,25 s · Q11 · Q13 (chạy lại trên gói phát hành cuối: 0) · Q16 · Q18 · Q19–Q25 · Q32 · LOCK.
**Trượt (áp nhầm, xem khiếu nại):** Q14 (tựa/trả lời: luật LL đọc `map.act`), Q15 (quãng đổi hình dài nhất 17,2 s ở bản đồ NYC 13:42; TB 3,1 s), Q17 (2,68 số/phút; "anchors đúng 3 số" mâu thuẫn Q34 kênh 2). Trên K2G-01 cùng bộ qc đánh Q14–18 "không áp".

### 4.3 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
- **Q32 clip PX-20568183** (cần cẩu, đoạn 07): **7,93 s / 8 s** (−0,9 %).
- **Q33 `c_crane`**: **2 lần / tối đa 2** (đúng ngưỡng; hai lần là chủ đích: mở và đóng phim).
- Không có chỉ số nào khác trong ±5 %: Q5 4,85 so 4,5 (+7,8 %); Q26b 16,5 % so 25 %; Q32 14,0 % so 40 %; Q34 79 % so 60 %.

## 5. Chấm mù một lần trên 1080p (`k2c-t1-06/blind_g2.py`, giao thức K2G-01)
3 người chấm (`claude-sonnet-5-5` ghim, thư mục trống, chỉ ảnh/lời): R1 khán giả, R2 đạo diễn motion/3D, R3 biên tập tư liệu. Kênh 2 chưa có tập tham chiếu → chấm tuyệt đối (như K2G-01). Kết quả nguyên văn: `kiem-mu/blind-g2/`.

### 5.1 Q27 — 12 khung ngẫu nhiên (hạt 11)
| | R1 | R2 | R3 | TB |
|---|---|---|---|---|
| Tay nghề TB (12 khung) | 6,08 | 6,00 | 6,42 | **6,17** |
| Đọc được TB | 7,17 | 8,00 | 7,33 | 7,50 |
| Tổng (1–10) | 6 | 6 | 7 | 6,3 |
| So với faceless thường | above | above | above | 3/3 above |
Khung tốt nhất (3/3): F06 (8:01.9, cảnh mặt cắt cầu thang lúc chạng vạng, 8/8/8).
**Cả 3 cùng gắn cờ (chưa sửa):**
- **F04 (7:05.8, `ch_icc` đầu shot):** sàn lưới trống với vài đường kẻ trước khi cột mọc (3/3/3).
- **F05 (7:18.3, `ch_icc` cuối shot):** máy side-track làm cột bị cắt mép trái, nhãn đè cột (5/5/6).
- **F03 (4:45.9, `ch_pew`):** nhãn 13 % mờ (đang hiện dần) chồng lên khối (5/5/5).
- **F09 (9:12.6, thẻ TO RECAP):** thẻ phẳng, nhiều khoảng trống (5/4/5).
Góp ý chung: bớt nhãn ACTUAL lặp; dòng nguồn nhiều nguồn quá dài cho điện thoại; nhãn trên bản đồ Illinois chưa đánh dấu rõ.

### 5.2 Q31 — 11 điểm nối + tổng quan 1 khung/8 s
- Liền mạch 7/6/6 · đa dạng 6/5/6 · hình khớp lời 7/7/7.
- Điểm nối: J04, J08, J10, J11 đa số "smooth"; còn lại "acceptable". **J07 (06→07): R3 coi là gãy** — lời về lời bảo lãnh cá nhân của bên cho vay, hình là bản đồ California rồi footage cần cẩu sáng (nhảy phong cách tối → sáng).
- Cả 3 nêu lạm dụng: cảnh toà góc phố chạng vạng và bản đồ địa cầu; footage Pexels sáng lệch tông với cảnh 3D tối.

### 5.3 Đề xuất sửa (chờ D2; ước giờ máy)
1. `ch_icc`: cột mọc ngay đầu shot hoặc vào shot muộn hơn; đổi side-track → front-dolly (dựng lại 1 cảnh ≈ 20 phút).
2. `ch_pew`: nhãn 13 % `side: up` để không chồng khối (chỉ lớp chữ).
3. J07: thay footage cần cẩu bằng cảnh 3D "costs / rates / rents" hoặc ảnh lưu trữ; thêm hoà tan 0,3 s ở các mối footage ↔ 3D; chỉnh tông footage cho gần cảnh 3D.
4. Thẻ TO RECAP: thêm biểu tượng nhỏ cho từng khoá.
Gộp 1–4: dựng lại 1–2 cảnh + lớp chữ cả phim + ghép ≈ 2–2,5 giờ đồng hồ, chấm mù lại ≈ $0,8.

## 6. Gói phát hành (quyết định 13/10 22:17) — `k2c-t1-06/phat-hanh/`
| Tệp | Ghi chú |
|---|---|
| `k2c-t1-06-v1-master.mp4` | 1,58 GB, **ngoài git** (`/var/tmp/cine-out/k2c-t1-06/`); SHA256 4f2d280bc6494c66cb4c531449d4240fda75b99baa3a13308a56284dcf1e1eb6 |
| `k2c-t1-06-short-S1.mp4` | 17 MB, ngoài git (`…/shorts/`); SHA256 4314fed73d2ca879be34d12cd5fad18e4b180fc1c1cbc555e2c02f934e678d7b |
| `k2c-t1-06.en.srt` | khớp master (từ căn chỉnh lời) |
| `description.en.txt` | **4 637 ký tự** (giới hạn mô tả YouTube 5 000; `make_release.py` chặn khi vượt): miễn trừ, "Facts as of 12 October 2026", 12 chương theo timeline thật, ghi chú số liệu, ghi công đầy đủ — nhạc Kevin MacLeod CC BY 4.0 (5 bài) + 11 SFX Work With Sounds CC BY 4.0 nguyên văn từ RIGHTS.md, ảnh LoC, tài liệu, Pexels, phông; dẫn tới bình luận ghim cho danh sách nguồn |
| `nguon-binh-luan-ghim.en.txt` | 8 284 ký tự (giới hạn bình luận 10 000): **30 nguồn** (URL + ngày truy cập) + 24 trang bản ghi ảnh/tài liệu/footage — đăng làm bình luận ghim. Ghi chú: mô tả K2G-01 dài 5 517 ký tự, vượt giới hạn 5 000 |
| `titles.txt` | CHÍNH "Why Did America Almost Stop Building Small Buildings Like This?" (63) · DỰ PHÒNG Test & Compare "What Happened to America's Small Apartment Buildings?" (53) · phương án 3 (không dùng) |
| `PACKAGING-BRIEF.md` + `nen-1…3.jpg` | ảnh nền 1280×720 lấy từ khung cảnh đinh 1080p **trước lớp chữ** (không chữ); chữ thumbnail gợi ý `1% OF NEW HOMES`; `brief.py` 0 cảnh báo. **Nhà máy không làm thumbnail.** |
| `SHA256SUMS.txt` | master, S1, .srt, mô tả, bình luận ghim |
- **Một Short: S1** — móc câu mạnh hơn: nghịch lý số "one in thirteen homes — but one in a hundred new ones" trong 2 s đầu, dạng câu hỏi, khớp tiêu đề chính và chữ thumbnail. S2 ("Why one staircase stops at three stories") cần bối cảnh mã xây dựng. S2 giữ đặc tả (`shorts_held`) + giọng cache, **không render** (2 cảnh của S2 đã được chặn khỏi lượt dựng 1080p đang chạy bằng cơ chế pid của `heroes_par.sh`, rồi dọn). Ghi AUTHORSHIP.
- Video > 30 MB không gửi qua giao diện và không commit (theo lệnh: shot mẫu/nháp không LFS; release cuối dùng LFS khi chủ dự án cho phép — D3).

## 7. Quyền và nguồn
- **SOURCES-FOOTAGE.csv** chuẩn hoá theo `checks/ll/FOOTAGE.md` (tài liệu, không đọc mã): giấy phép bắt đầu bằng PD; URL + SHA là **tệp gốc đã dùng khi render** (TIFF master LoC, tải lại 16 tệp, khớp SHA ghim); `timecode_dung` từ timeline cuối (`sf_ledger.py`); người/logo đã xem từng ảnh (FSA-01 biển quảng cáo 1930s, FSA-04 biển Coca-Cola nhỏ, HABS-04 logo đã cắt khung).
- **SSZEA** chuyển sang bản quét Internet Archive (`standardstatezon05ball`, cùng ấn phẩm, cùng bản quét): nvlpubs.nist.gov nằm ngoài danh sách nguồn Q32.
- Trang IBC/CFR **dựng lại chữ** (không bản chụp) và tệp dự phòng không dùng → `SOURCES-NGOAI-SO.csv` kèm lý do; RIGHTS.md thêm K2V-DOC-2…5.
- Ảnh Hoover/Sutherland: nguồn trên hình trỏ trang LoC (LCCN 2016888786, 2016877918), không trỏ Wikimedia (Q8).
- Đây là **tập đầu tiên dùng Pexels** (4 clip + 1 ảnh): QUAN-TRI-RUI-RO §6.2 ghi chủ dự án cần mở trang giấy phép Pexels đối chiếu chữ trước tập đầu tiên dùng Pexels (D5).

## 8. Mã dùng chung đã đổi (ảnh hưởng ngoài tập)
- `scripts/k2/hero.js`: footage trích theo số khung (trước đây thiếu 1 khung khi dur × 24 lẻ) + tuỳ chọn `decimate`.
- `scripts/k2/lib/k2.js`: khối chú thích nhường dòng nguồn nhiều dòng; credit nối cuối dòng nguồn; thẻ kết tự co; thẻ list `top` (bám trên); `tags()` 16:9 chặn ở đỉnh dải chú thích; nhãn loại 9:16 trên dải chú thích.
- `design/k2v/common.js`: tường/sàn studio rộng hơn (hết khối đen ở mép khung với mọi biểu đồ k2v).
- `design/ll-hero/k2c106.js`: `lot()` grow âm; preset `pencil` mới, `corridor_side` mới.
- `make_spec.py`: chuẩn hoá nguồn (Q21), khai `p.clip/p.file/p.setting` cho ảnh/trang quét (Q32).

## 9. Chi phí và giờ máy
| Mục | Số đo |
|---|---|
| API (`claude -p`) G2 | chấm mù Q27 $0,41 + Q31 $0,36 = **$0,77**; luỹ kế tập **$9,06 / $40** (sổ `kiem-mu/cost.jsonl`) |
| ElevenLabs | phiên này gửi **7 513** ký tự (thu lại 05, 08 × 3, 10 × 3 khi kiểm ASR); bộ đếm tài khoản sau cùng 93 318 |
| Giờ máy nháp | cảnh 960×540 SPP 2 ≈ 2 giờ 15 phút; lớp chữ + mix + ghép + 2 Short 1 giờ 47 phút |
| Giờ máy 1080p | cảnh SPP 4 **11 giờ 41 phút**; lớp chữ 49 phút; ghép 36 phút; sửa 1080p 65 + 89 phút; S1 2 phút → **≈ 15,5 giờ** (ước G1a 10–13 giờ; vượt vì vật liệu PBR/ánh sáng nặng hơn: 6–7 s/khung/tiến trình) |
| Đĩa | trần phiên ~12 GB trống; đã dọn tệp trung gian nháp, cache pip/uv, mô hình whisper medium.en (small.en giữ), khung dựng thử. Khung cảnh đinh 1080p (8,9 GB) **giữ** để sửa được D2 mà không dựng lại toàn bộ |

## 10. Việc chờ chủ dự án
- **D1.** Xác nhận chọn **S1** làm Short duy nhất (lý do §6).
- **D2.** Bốn điểm hình chấm mù chỉ ra (§5.3: `ch_icc` F04/F05, nhãn 13 % `ch_pew`, J07, thẻ TO RECAP): **sửa một lượt nữa** (≈ 2–2,5 giờ máy + chấm mù lại ≈ $0,8) hay **giữ bản hiện tại**.
- **D3.** Phát hành video: cho phép mở nhánh/thư mục release bằng Git LFS cho master 1,58 GB + S1 (như LL), hay chủ dự án lấy trực tiếp từ container.
- **D4.** Khiếu nại Q14–Q18 áp nhầm cho kênh 2 (`checks-appeal.md`, 14/10) — chờ phiên K.
- **D5.** Đối chiếu trang giấy phép Pexels bằng trình duyệt (tập đầu tiên dùng Pexels; QUAN-TRI-RUI-RO §6.2), ghi AUTHORSHIP.
- **D6** (từ trước). Sau 16/10: chỉ kiểm lại các dòng "as of" nếu chưa đăng.
- Thumbnail: chủ dự án tự làm theo `phat-hanh/PACKAGING-BRIEF.md`.

## 11. Sổ chi phí tập K2C-T1-06 — mốc gốc (chủ dự án yêu cầu 14/10/2026)
| Khoản | Số đo | Nguồn số |
|---|---|---|
| **API (`claude -p`)** | **$9,06** luỹ kế cả tập (trần $40): G1a kiểm mù lời 3 vòng + REVIEWER + tiêu đề; G1b chấm mù trước/sau $0,55; G2 chấm mù Q27 $0,41 + Q31 $0,36 | `k2c-t1-06/kiem-mu/cost.jsonl` (mỗi lượt gọi: model yêu cầu, model chạy, USD) |
| **ElevenLabs (ký tự gửi)** | **≈ 30 360**: bản thu đầu 12 đoạn + 2 Short 15 005 (14 408 + S1 193 + S2 404); thu lại khi kiểm ASR lần 1 7 840; thu lại sau khi viết số bằng chữ + ASR lần 2 7 513. Bộ đếm tài khoản sau cùng: 93 318 | log `prep.py`/`asr.py` (`el_sent`), báo cáo G2 §1 |
| **Giờ máy — mẫu G1b** | 3 shot mẫu 1 879 khung 1080p trong 61 phút; lượt dựng lại sau sửa G1b không đo riêng (không có log thời gian) | TAP-K2C-T1-06-G1b §6 |
| **Giờ máy — nháp 960×540** | cảnh đinh SPP 2 ≈ 2 giờ 15 phút; lớp chữ + mix + ghép + 2 Short 1 giờ 47 phút; ASR ≈ 45 phút → **≈ 4,8 giờ** | `build.log`, log nền |
| **Giờ máy — 1080p** | cảnh đinh SPP 4 11 giờ 41 phút; lớp chữ 49 phút; ghép 36 phút; hai lượt sửa 1080p 65 + 89 phút; S1 2 phút → **≈ 15,5 giờ** | `/var/tmp/cine-out/k2c-t1-06/build.log` |
| **Số lần chủ dự án chạm** | **10**: 3 cổng duyệt (G1a 12/10, G1b có điều kiện 13/10, G2 14/10) + 7 lệnh/xác nhận giữa cổng (lệnh mở G1a 12/10; merge checks 1.10.1 giữa G1a; duyệt mốc V + chỉ đạo G1b 13/10; xác nhận v8.2 + SSZEA 13/10; báo checks 1.10.2 13/10; quyết định gói phát hành 13/10 22:17; rà giấy phép Pexels 14/10) | AUTHORSHIP.md, báo cáo G1a/G1b/G2 |
| Đĩa phiên | trần ~12 GB trống; khung cảnh 1080p 8,9 GB + master 1,58 GB là phần lớn nhất | `df`, `du` |

## 12. Sau duyệt G2 (14/10/2026)
- D1 S1 · D2 giữ bản, 4 điểm → `BAI-HOC-K2.md` K11 · D3 nhánh `release-k2c-t1-06-v1` (Git LFS) · D4 khiếu nại giữ cho K · D5 giấy phép Pexels đã rà → AUTHORSHIP. **Phát hành (14/10/2026):** nhánh mồ côi `release-k2c-t1-06-v1` @ `0aa26ec24e75c420452911b96b233a765574996f` (Git LFS cho 2 mp4; README + 10 tệp gói). Hạn mức LFS: **không đọc được** (cần đăng nhập trang billing; phiên không có `gh`). Push LFS 2/2 (1,6 GB) thành công lần đầu. **Tải ngược:** clone mới nhánh release (con trỏ 135 byte) → `git lfs pull` → `sha256sum -c SHA256SUMS.txt`: **10/10 OK** (master 4f2d280b…, S1 4314fed7…, .srt, mô tả, bình luận ghim, tiêu đề, PACKAGING-BRIEF, nền 1–3). Merge `main`: báo cáo cuối của phiên.
