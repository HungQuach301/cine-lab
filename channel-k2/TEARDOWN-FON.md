# TEARDOWN-FON — công thức kênh "địa lý/công trình × kinh tế" cho kênh 2 Moving Parts (Mốc A: Đóng gói)

> Phiên Teardown, 15/10/2026 (lệnh chủ dự án duyệt 15/10). Nhánh `teardown-fon` từ `origin/main`. Chỉ ghi tệp này và `channel-k2/teardown/*.json`; không sửa mã, `checks/`, `design/`, tệp tập.
> **Mục tiêu:** học CÔNG THỨC, không sao chép. Không tải video. Thumbnail của kênh khác chỉ xem tạm ở `/var/tmp/cine-out/teardown-thumbs` (ngoài git, không commit). Không chép câu chữ của họ vào sản phẩm: tiêu đề của họ chỉ xuất hiện ở đây như dữ liệu phân tích.
> Mọi lượt xem/thích/bình luận là **số công khai YouTube Data API đọc ngày 15/10/2026 (UTC)**. Mọi chỉ số tính thêm (lượt xem/ngày, tỷ lệ, trọng số) là **tự tính, không phải chỉ số YouTube**.
> Không đọc lại phần việc đã có: tôi dùng `DONG-GOI.md` và `PACKAGING-BRIEF.md` của T2 (nhánh `origin/k2c-t2`) làm nền và chỉ đo phần chúng chưa đo (toàn bộ video + bình luận của 2 đối thủ, kênh TRẺ cùng dạng, công thức tiêu đề/thumbnail/độ dài, đề tài mới).

## 0. Tóm tắt cho chủ dự án
1. **Công thức thắng là "câu hỏi giàu–nghèo về một NƠI ai cũng biết, gói trong một cặp tương phản".** 3/5 video dài của FoN vượt 100 nghìn trong 2 tuần; 3 video thắng đều là *nơi* + *giàu/nghèo* + *nghịch lý* (Mỹ ↔ Mỹ Latin 1,38 triệu; Anh ↔ Ireland 226 nghìn; Thuỵ Sĩ "lẽ ra phải nghèo" 124 nghìn). GoDocs thắng khi đề tài là **công trình nổi tiếng trên mặt đất** (Palm Jumeirah 2,35 triệu; Suez 2,26 triệu; Burj Khalifa 1,69 triệu) và thua hẳn khi ra ngoài mặt đất (thiên thạch 3,4 nghìn; siêu núi lửa 2,8 nghìn; máy bay trắng 2,2 nghìn).
2. **Độ dài KHÔNG phải đòn bẩy.** Trong cùng kênh, tương quan thứ hạng giữa độ dài và lượt xem ≈ 0 (FoN ρ = 0,00; GoDocs 0,19, p = 0,24; Geography Effect −0,01; Uncover History −0,12). Kênh thắng dài 9,5 phút (FoN), 15,7 phút (GoDocs), 13,5 phút (Geography Effect), 29 phút (Uncover History). → Đề xuất §10: bỏ khung cứng 9–11 phút, đổi thành **dải 10–14 phút theo số chương**.
3. **Đề tài và thời điểm mới là đòn bẩy.** 8 kênh trẻ do search.list trả về (333 video dài) chỉ có **2 video ≥ 100 nghìn**, cả hai của cùng một kênh và cùng một **tin thảm hoạ vừa xảy ra**. Hai kênh trẻ thành công nhất cùng ngách — **Geography Effect** (lập 02/2026, 24/68 video dài ≥ 100 nghìn) và **Uncover History** (lập 05/2026, 23/104) — đăng ~2–5 video dài/tuần với đề tài neo vào tin đầu tư/hạ tầng hoặc lịch sử tiền–đế quốc.
4. **Khán giả FoN tranh luận, khán giả GoDocs trầm trồ.** Bình luận FoN: tranh luận nguyên nhân + sửa sai chiếm phần lớn trọng số (Mỹ Latin: tranh luận 920, sửa sai 185, ý kiến khác 2 407 so với khen 101), khen gần như chỉ về **hình động bản đồ**; một bình luận nặng (66) chê **giọng nghe như AI và phụ đề ép**. Bình luận GoDocs: khen chung + "cơ chế kỹ thuật thật thú vị", hỏi công cụ AI/lồng tiếng, sửa sai tiền đề (Palm "không bê tông" sai; đảo đang lún). Đây là khoảng trống đúng cho lợi thế "receipts" của mình.
5. **Gói của mình:** T2 (đóng tàu) khớp công thức tốt nhất (câu hỏi + "It's Not Just Wages", thumbnail bản đồ/đối lập quá khứ–hiện tại). Steel và T1 thiếu **nơi chốn trên tiêu đề và thumbnail**, dài 17 và 15,6 phút. Chi tiết §7.
6. **10 đề tài mới** (§8) đã loại mọi đề tài của 4 kênh: FoN, GoDocs, Geography Effect, Uncover History. **Ba Lan, Argentina, dầu Na Uy–Venezuela, kênh Erie** bị loại vì hai kênh trẻ vừa làm trong 3 tháng. Đề tài đầu bảng: **Gibraltar** (hàng rào biên giới gỡ 15/07/2026), **Nauru** (+ Ma-rốc thành chuỗi phosphate), **hiệp ước sông Colorado** (quyết định 21/08/2026).
7. **Chi phí:** YouTube Data API **255/300 đơn vị**; Claude API **$0,0514** (Haiku 5.5 ghim, 12 lượt); ElevenLabs 0. Chi tiết §1.

## 1. Cách đo và chi phí
| Bước | Lệnh | Đơn vị |
|---|---|---|
| Preflight (`verify.sh`: 9 PASS, 4 FAIL không liên quan việc này — three.js, tifffile, k2v node_modules, Freesound) + 1 lệnh thử `channels.list` | `channels` | 1 |
| Tìm 2 kênh bằng handle (`@FortuneOfNations` → "Fortune of Nations Animated"; `@GoDocumentaries` → "GoDocs") | `channels forHandle` | 2 |
| Toàn bộ video (13 + 42) | `playlistItems` 2 + `videos` 2 | 4 |
| 100 bình luận hàng đầu (`order=relevance`) × 3 video lớn nhất mỗi kênh (thực thu 522: video Thuỵ Sĩ chỉ có 45 bình luận gốc, Suez 77) | `commentThreads` | 6 |
| Tìm kênh trẻ cùng dạng: 2 câu (`order=viewCount`, `publishedAfter=2026-04-15`, US, en, 4–20 phút) + đọc 26 kênh | `search` 2 + `channels` 1 | 201 |
| Toàn bộ video 8 kênh trẻ từ mẫu search + 2 kênh trẻ thành công (Geography Effect, Uncover History) + 1 lượt `forHandle` không ra kênh | `playlistItems`/`videos`/`channels` | 32 |
| Cung đề tài: lượt xem 106 video cùng đề tài (mã tìm bằng WebSearch giới hạn youtube.com, không tốn quota) | `videos` | 3 + 1 kiểm kênh = 4 |
| **Tổng** | | **255 / 300** |

- **Claude API: $0,0514** (trần $3). Gắn nhãn 522 bình luận bằng `claude -p --model claude-haiku-5-5 --tools ""`; sổ `cost.jsonl` ghi model thực chạy = `claude-haiku-5-5` ở cả 12 lượt. Tổng hợp và viết báo cáo do phiên này (Opus) làm, không qua API trả tiền.
- **ElevenLabs:** 0. **WebSearch:** ~30 lượt để tra neo thời sự và tìm mã video cùng đề tài (không thuộc quota YouTube).
- **Không ghi `COST-LEDGER.csv`** vì lệnh giới hạn tệp được ghi; số trên để P chép vào sổ.
- Số thô (mô tả, bình luận nguyên văn, ảnh) ở `/var/tmp/cine-out/teardown-data/` và `teardown-thumbs/`, **ngoài git**. Trong repo chỉ có số đo, đặc điểm cấu trúc và ý diễn đạt lại (`channel-k2/teardown/`).
- **Tệp JSON:** `doi-thu-video.json` (55 video, chỉ số + đặc điểm mô tả, không lưu nguyên văn) · `binh-luan-tom-tat.json` · `thumbnail-mo-ta.json` · `kenh-tre-so-sanh.json` · `cung-de-tai.json` · `de-tai-10.json`. `channel-k2/.gitignore` chặn `*.json`; tôi không sửa `.gitignore` (ngoài phạm vi) mà thêm 6 tệp bằng `git add -f` theo đúng lệnh giao. Các tệp chỉ chứa số đo, đặc điểm cấu trúc, tiêu đề/tag (siêu dữ liệu công khai) và ý diễn đạt lại — không có mô tả, bình luận nguyên văn hay ảnh của kênh khác.

## 2. Hai đối thủ: số liệu
### 2.1 Fortune of Nations Animated (lập 30/09/2026; 8 950 người đăng ký; 1,74 triệu lượt; 13 video)
| Ngày | Dài | Lượt xem | Thích/1k | BL/1k | Lượt/ngày | Dạng tiêu đề (mô tả, không chép) |
|---|---|---|---|---|---|---|
| 02/10 | 9:32 | 124 124 | 13,5 | 1,0 | 10 174 | "X lẽ ra phải nghèo. Đây là lý do nó không nghèo" — nghịch lý khẳng định |
| 05/10 | 9:35 | 225 713 | 11,6 | 2,6 | 24 534 | "Vì sao sự suy yếu của A làm B giàu lên" — tổng bằng không giữa hai láng giềng |
| 07/10 | 9:41 | **1 377 805** | 5,1 | 1,4 | **191 362** | "Vì sao A giàu mà B không bao giờ giàu?" — cặp tương phản lục địa |
| 11/10 | 10:21 | 12 108 | 9,0 | 1,2 | 3 784 | "X lớn hơn [nơi Mỹ quen thuộc]… vậy sao mọi người sống ở đây?" — so tầm cỡ |
| 13/10 | 9:09 | 28 619 | 14,8 | 2,4 | 23 849 | "Vì sao A thống nhất còn B thì không?" — cặp tương phản (lặp mẫu 07/10) |
- **8 Short** (52 s–1:36): 1 359–4 208 lượt, tiêu đề có 2–3 emoji. Short không kéo được kênh trong 2 tuần đầu.
- **Nhịp:** 5 video dài trong 11 ngày (~3,2/tuần) + 8 Short.
- **Mô tả:** 2 200–2 900 ký tự; dòng đầu nhắc lại câu hỏi của tiêu đề + một sự thật móc (năm, con số); 2–3 đoạn dày từ khoá; **9–17 chương** (tên chương gợi tò mò); khối **SOURCES** cấp cơ quan (IMF, cơ quan thống kê, hiệp ước, toà án) hoặc "nguồn có link ở bình luận ghim"; "Watch next"; ghi công dữ liệu bản đồ (AWS Terrain Tiles, Natural Earth, OSM) và nhạc (Kevin MacLeod CC BY — kênh ta không dùng được cho phim bán nếu điều khoản không hợp RIGHTS); 16–23 tag là cụm từ tìm kiếm ("why is X so rich", "X vs Y economy").
- **Giọng/lời:** khán giả nhận ra giọng AI (bình luận trọng số 66); kết bằng "scorecard" (bảng điểm) — Kinh thánh đã có.

### 2.2 GoDocs (kênh lập 03/2024, video công khai đầu tiên 19/05/2026; 41 300 người đăng ký; 15,4 triệu lượt; 42 video)
- **42 video dài, 0 Short**; trung vị 15,3 phút; **20/42 ≥ 100 nghìn** (48 %); trung vị 74 nghìn; ~2 video/tuần.
- **Thắng:** công trình/địa danh trên mặt đất ai cũng biết + câu hỏi "vì sao nó chưa lún/sập", "làm sao xây được": Palm Jumeirah 2,35 triệu (19 phút), Suez 2,26 triệu (11 phút), Burj Khalifa 1,69 triệu, Kola 1,07 triệu, Vạn lý trường thành xanh 1,08 triệu, Hà Lan 626 nghìn, Kim tự tháp 635 nghìn, Ả Rập Xê Út không sông 721 nghìn (4 ngày tuổi, 206 nghìn/ngày).
- **Thua:** không gian/khái niệm trừu tượng: thiên thạch 3,4 nghìn, siêu núi lửa 2,8 nghìn, máy bay vì sao trắng 2,2 nghìn, phi hành gia 5,7 nghìn, máy bay tàng hình 12,7 nghìn.
- **Tương tác thấp:** thích 1,4–7,7/1 000 lượt ở các video ≥ 379 nghìn (FoN: 5–15), bình luận 0,05–0,25/1 000 (Panama 379 nghìn lượt, 546 thích, 20 bình luận). Bình luận khen bản lồng tiếng Thái/Ả Rập → nhiều khán giả không nói tiếng Anh, xem thụ động. Tôi **không kết luận** nguồn lượt xem (đề xuất, quảng bá trả phí hay khác): API không cho biết.
- **Mô tả:** 500–1 600 ký tự, 3 đoạn kể chuyện, **không chương, không nguồn** (1/42 có nguồn), 15–28 tag. Đây là điểm yếu mà khán giả bắt được (sửa sai tiền đề; hỏi "dùng AI gì").

## 3. Bình luận: khán giả khen gì, hỏi gì, đòi gì
Mẫu: 522 bình luận (100 + 100 + 45 FoN; 100 + 77 + 100 GoDocs), Haiku gắn nhãn 522/522. Trọng số = 1 + thích + phản hồi. Ý dưới đây là **diễn đạt lại**, không phải nguyên văn.

| | FoN (3 video) | GoDocs (3 video) |
|---|---|---|
| **Khen** | hình động bản đồ (62/101 trọng số khen ở video Mỹ Latin), câu móc mở đầu (22 ở Thuỵ Sĩ: mở bằng nạn đói 1817 rồi tới ngân hàng); khen rất ít so với tranh luận | khen chung "kỹ thuật thật kỳ diệu" (Palm: khen 494/805 trọng số), cơ chế nền móng/đất; khen lồng tiếng Thái, Ả Rập; vài người khen "dùng AI đúng chỗ" |
| **Hỏi** | đảo của Ireland có bền không khi phụ thuộc tập đoàn đa quốc gia (51); lương hưu các nước giàu khác nhau ra sao (78); làm bản đồ bằng phần mềm gì | vì sao không dùng đá/bê tông thay cát (34); thuỷ triều có ảnh hưởng không; ai là kiến trúc sư; **dùng công cụ AI nào, prompt nào** (≥ 6 câu ở Suez) |
| **Sửa sai / tranh luận** | nguyên nhân bị bỏ sót: giáo dục, quyền sở hữu, Chile/Argentina giàu quanh 1900, Venezuela từng đứng thứ tư; tranh cãi "nạn đói hay Great Hunger"; "Ireland chưa từng rời EU"; ý kiến tôn giáo/văn hoá/IQ (trọng số lớn, dễ biến thành bãi chiến) | "không bê tông" là sai (cọc bê tông cốt thép); đảo đang lún vài mm/năm; Burj "không có hệ thống thoát nước thải"; kỹ thuật cọc đã có từ thời Sinan; dán nhầm vị trí (Palm ghi Qatar) |
| **Đòi đề tài** | Singapore, Hồng Kông, Trung Đông, Tây Ban Nha, "nước tiếp theo" | thêm nội dung cho kỹ sư; thêm ảnh thật bên cạnh tranh minh hoạ; số liệu đất nạo vét ở Suez |
| **Một ý vàng cho kênh 2** | — | ở video Suez: "kênh đào đem về hàng tỷ mà người dân vẫn thuộc nhóm nghèo nhất vùng" (15) — đúng câu hỏi kênh 2 trả lời, GoDocs không trả lời |

**Bài học:**
1. Khán giả kinh tế–địa lý **đến để cãi nhau về nguyên nhân**. Video có một nguyên nhân đơn giản sẽ bị "nguyên nhân bị bỏ sót" áp đảo. Đoạn "the honest part" + bảng điểm nhiều nhân tố của Kinh thánh là đúng hướng; nên **nêu trước 2–3 nguyên nhân phổ biến mà khán giả sẽ đưa ra** và trả lời bằng số.
2. **Sai một tiền đề là mất uy tín công khai** (Palm "không bê tông"; "Ireland rời EU"). Quy trình claims + kiểm mù hiện hành chặn được — giữ nguyên.
3. **Giọng AI bị nhận ra và bị trừ điểm.** Kênh 2 dùng ElevenLabs: giữ chuẩn giọng hiện hành, ưu tiên nhịp đọc tự nhiên; đừng ép phụ đề cháy cứng (khán giả FoN chê).
4. Câu hỏi "dùng AI gì" ở GoDocs cho thấy khán giả **nhìn ra hình AI**. Hình tự dựng 3D + hồ sơ thật của mình là khác biệt rõ.
5. Bình luận tôn giáo/sắc tộc/IQ xuất hiện ngay ở video Mỹ Latin → luật lọc bình luận của `QUAN-TRI-RUI-RO` §1.2 cần bật từ video đầu.

## 4. Thumbnail (mô tả bằng lời; chi tiết `teardown/thumbnail-mo-ta.json`)
**FoN — một ngữ pháp duy nhất, lặp lại:**
- Nền: **bản đồ nổi thật** (địa hình có bóng), biển xanh lam.
- Chủ thể: **1–2 vùng tô màu bão hoà, viền trắng, phát sáng** (xanh lá neon ↔ nâu đất; đỏ ↔ vàng). Cặp tương phản dùng **vạch đỏ dọc** chia đôi khung.
- Chữ: **hộp đen chữ trắng hoặc đỏ, in hoa, đậm, 1–2 từ** ("WHY?", "[SỰ KIỆN] WINNER") hoặc **con số + 1 từ** ("$3 TRILLION", "109M PEOPLE"), góc trên-trái hoặc đè giữa vạch chia.
- Biểu tượng: 0–3 (mũi tên trắng cong chỉ dòng chảy; biểu tượng tròn gạch chéo "không dầu/không biển/không khoáng sản").
- Video lớn nhất (1,38 triệu) = **ít yếu tố nhất**: hai lục địa, một vạch, một từ.

**GoDocs — không chữ, minh hoạ (dáng AI), cho thấy cái ẩn:**
- **Mặt cắt lộ cơ chế dưới vật nổi tiếng** (đảo cắt lộ lớp đá; khối địa tầng; toà tháp trên nền cát nứt), **đối lập quá khứ–hiện tại** (người cổ đại nhìn tàu container), **trước/sau chia đôi** (sa mạc → rừng, mũi tên đỏ), **nhân vật truyện tranh vật lộn** với vật khổng lồ.
- Video yếu: không gian, ẩn dụ (nhiệt kế băng trên núi lửa), dấu hỏi phát sáng — **không có vật nổi tiếng trên mặt đất**.

**Kênh trẻ thua:** dùng gần y ngữ pháp GoDocs (mặt cắt đường hầm, cầu kính giữa núi) nhưng chỉ 5–13 nghìn → **thumbnail không cứu được đề tài không ai tìm**. Kênh thắng duy nhất trong mẫu thua (1,82 triệu): diorama 3D thung lũng + vòng tròn đỏ + mũi tên + **con số khổng lồ có dấu hỏi** — neo vào thảm hoạ vừa xảy ra.

## 5. So kênh trẻ cùng dạng (< 12 tháng, cùng thước)
| Kênh | Lập / video dài đầu | Video dài | Dài/tuần | ≥ 100 nghìn | Trung vị lượt | Trung vị dài (phút): thắng / còn lại | Thích/1k | Kiểu tiêu đề thắng |
|---|---|---|---|---|---|---|---|---|
| Fortune of Nations (đối thủ) | 09/2026 | 5 | 3,2 | **3/5 (60 %)** | 124 124 | 9,6 / 9,8 | 6,7 | Vì sao A giàu mà B không? / suy yếu của A làm B giàu |
| GoDocs (đối thủ) | 05/2026 | 42 | 2,0 | **20/42 (48 %)** | 74 196 | 15,7 / 14,9 | 5,0 | Vì sao [công trình nổi tiếng] chưa lún/sập? |
| **Geography Effect** | 02/2026 | 68 | 2,0 | **24/68 (35 %)** | 38 520 | 13,5 / 11,9 | 9,8 | "Why [nơi] [nghịch lý]" · "[nơi] Shouldn't Exist — Here's Why It Does" · "Why [suy yếu của A] Is Making [B] Rich" · "[$ tỷ] Bet on [nơi]" |
| **Uncover History** | 05/2026 | 104 | 5,1 | **23/104 (22 %)** ⚠ | 23 493 | 28,9 / 30,0 | 20,4 | "[Chủ thể] did [hành động + năm/số] — So why/how [cú lật]?" |
| DT Civil Core | 06/2026 | 106 | 6,2 | 2/106 | 722 | 17,1 / 17,2 | 2,9 | tin thảm hoạ mới: "[số] in [thời gian] — How Did [sự kiện]?" |
| The Built Mind | 05/2026 | 26 | 1,3 | 0 | 305 | — / 9,9 | 14,4 | (tốt nhất 40 nghìn: "What It's Like Inside…") |
| Beyond Manufacturing | 07/2026 | 25 | 2,2 | 0 | 1 073 | — / 17,0 | 5,2 | (12,7 nghìn: "How [nơi] Is Building the IMPOSSIBLE…") |
| Stories Of USA | 04/2026 | 32 | 2,8 | 0 | 618 | — / 9,5 | 7,0 | (8,7 nghìn: "They Built This… No One Talks About It!") |
| Mega Build World | 07/2026 | 53 | 4,8 | 0 | 304 | — / 6,7 | 4,4 | (5,0 nghìn: "Inside [nơi]'s [công trình] \| How Engineers…") |
| FactVerse | 04/2026 | 47 | 2,0 | 0 | 17 | — / 8,7 | 11,9 | — |
| The Why of Where | 06/2026 | 26 | 1,7 | 0 | 66 | — / 12,6 | 9,8 | — |
| The Useful Brief | 09/2026 | 18 | 7,9 | 0 | 96 | — / 8,4 | 17,2 | — |

⚠ **Chỉ số nằm trong ±5 % quanh ngưỡng 100 nghìn:** 5 video Uncover History (95 236–104 296 lượt) → tỷ lệ của kênh này dao động 21–23/104 tuỳ ngày đo.
**Giới hạn mẫu:** 4 kênh thắng (2 đối thủ + Geography Effect + Uncover History) là chọn có chủ đích; 8 kênh còn lại là những kênh trẻ mà 2 câu search.list trả về (search `order=viewCount` + `publishedAfter` chỉ trả 13 kết quả mỗi câu, thiên về kênh nhỏ). Vì vậy **không dùng bảng này để ước xác suất thành công**; chỉ dùng để thấy cái gì phân biệt kênh thắng và kênh thua.

**Điều phân biệt kênh thắng với kênh thua (đọc từ bảng):**
1. **Đề tài là NƠI có tên + tiền** (Geography Effect: Canada, Slab City, Ba Lan, Argentina, nhà máy chip Arizona; FoN: Mỹ–Mỹ Latin) hoặc **công trình nổi tiếng** (GoDocs). Kênh thua đi dạng liệt kê/giật gân ("5 Insane…", "IMPOSSIBLE", "Secret") và đề tài rời rạc.
2. **Neo tin đầu tư/hạ tầng lớn có con số đô la** là mạch riêng của Geography Effect: nhà máy chip $265 tỷ (407 nghìn), Micron $100 tỷ (245 nghìn), Meta $200 tỷ ở Louisiana (181 nghìn), khởi động lại nhà máy hạt nhân (231 nghìn). Đúng lăng kính "hạ tầng" của Kinh thánh.
3. **Nhịp đăng ≥ 2 video dài/tuần** ở mọi kênh thắng; nhưng nhịp cao không đủ (Mega Build World 4,8/tuần, 0 video ≥ 100 nghìn).
4. **Độ dài không quyết định** (mục 0, ý 2). Nhóm 15–20 phút có trung vị cao nhất ở Geography Effect (134 nghìn, n = 12) và GoDocs (374 nghìn, n = 20), nhưng n nhỏ và lẫn đề tài.
5. **Cảnh báo:** Uncover History thắng bằng khung "ngân hàng/gia tộc đứng sau chiến tranh" ("Rothschild…", "Bankers Who Funded Hitler…"). Đây chính là vùng ĐỎ/VÀNG của `QUAN-TRI-RUI-RO` §1.2. **Không học phần này.**

## 6. CÔNG THỨC (tổng hợp từ §2–§5)
| Yếu tố | Công thức thắng | Bằng chứng |
|---|---|---|
| **Đề tài** | Một NƠI có tên mà khán giả Mỹ/quốc tế biết (nước, thành phố, công trình) + câu hỏi giàu/nghèo hoặc "vì sao nó tồn tại/không sập" + một **cặp tương phản** (hai nước, hai bờ, quá khứ ↔ hiện tại) | FoN 3/3 video thắng; GoDocs 20/42; Geography Effect 24/68 |
| **Thời điểm** | Neo vào tin mới có con số (hiệp ước, khoản đầu tư $ tỷ, quyết định chính phủ) nhưng câu chuyện sống lâu | Geography Effect (chip, Micron, Meta), DT Civil Core (thảm hoạ — kênh 2 không đi đường này) |
| **Tiêu đề** | ≤ 60 ký tự; mở bằng "Why"; có tên nơi; có nghịch lý hoặc cặp đối lập; không emoji ở video dài; không từ giật gân ("INSANE", "IMPOSSIBLE", "Secret") | FoN, Geography Effect; kênh thua dùng từ giật gân |
| **Thumbnail** | (a) **Bản đồ nổi + 1–2 vùng tô bão hoà phát sáng + hộp đen 1–2 từ hoặc số + từ** (FoN), hoặc (b) **không chữ, mặt cắt/đối lập lộ cơ chế dưới vật nổi tiếng** (GoDocs). Một ý, ≤ 3 biểu tượng, tương phản cực mạnh | §4 |
| **Độ dài** | 9–16 phút; không có hiệu ứng độ dài trong kênh; chọn theo số chương thật | §5 |
| **Nhịp** | ≥ 2 video dài/tuần ở kênh thắng; Short không kéo kênh mới | §2.1, §5 |
| **Mô tả** | Dòng 1 = câu hỏi tiêu đề + một sự thật móc; 9–17 chương tên gợi tò mò; nguồn cấp cơ quan; "Watch next"; tag = cụm tìm kiếm "why is X so rich", "X vs Y economy" | FoN |
| **Lời/hình (theo bình luận)** | Móc bằng một cảnh lịch sử cụ thể (năm + chuyện người); bản đồ chuyển động mượt; trả lời trước các nguyên nhân khán giả sẽ cãi; không sai tiền đề; giọng tự nhiên | §3 |
| **Khác biệt mình giữ (đối thủ thiếu)** | nguồn có link + "as of"; hồ sơ thật; "the honest part"; nhân vật người thật; hình tự dựng không dáng AI; câu hỏi "tiền chảy về ai" mà GoDocs bỏ trống | §2.2, §3 |

## 7. Đối chiếu gói Steel, T1, T2 với công thức
| Tiêu chí | **Steel (K2G-01)** "Is American Steel Dying? What 1950 vs 2025 Really Shows" | **T1 (K2C-T1-06)** "Why Did America Almost Stop Building Small Buildings Like This?" | **T2 (K2C-T2-01)** "Why America Builds So Few Ships (It's Not Just Wages)" |
|---|---|---|---|
| Nơi có tên trên tiêu đề | Có (America) — rộng | Có (America) — rộng, chủ thể là "loại nhà" | Có (America); tiêu đề 3 có Richmond → Ulsan |
| Mở bằng "Why" / nghịch lý | **Thiếu**: câu có/không ("Is…Dying?") — dạng tin tức, yếu hơn "Why" | Có "Why"; "Like This" dựa vào thumbnail (khó đọc ở tìm kiếm) | **Có**: "Why" + ngoặc lật ngược "It's Not Just Wages" — khớp mẫu "It's Not What You Think" của kênh thắng |
| Cặp tương phản | Có (1950 ↔ 2025) — thời gian, không nơi | **Thiếu** | Có trong lời và tiêu đề 2/3 (1943 ↔ nay; Mỹ ↔ Hàn) — **chưa lên tiêu đề chính** |
| Độ dài tiêu đề | 55 ✓ | 63 (hơi dài) | 54 ✓ |
| Thumbnail | Hai cọc thỏi thép + "1950 VS 2025" trên bảng kỹ thuật — **không bản đồ, không nơi** | Toà gạch góc phố chạng vạng + "1% OF NEW HOMES" — **không bản đồ**, đọc như kiến trúc | **T-A** bản đồ nổi + 2 hộp số (đúng ngữ pháp FoN); **T-B** đối lập quá khứ–hiện tại không chữ (đúng ngữ pháp GoDocs Suez) ✓ |
| Độ dài | ~17:04 (14 chương) | ~15:40 | ~10–11 phút (7 chương, chương cuối 9:53) |
| Mô tả | Dòng 1 là câu miễn trừ (không móc) | — | Dòng 1 là móc số (1943, CRS 2026) ✓; miễn trừ ở đoạn 2 |
| Nhân vật | Carnegie (lịch sử) | yếu | Kaiser, Jones, Chung ✓ |
| Neo thời sự | thuế 232, CBAM ✓ | dữ liệu 2025 | hạn phí cảng 09/11/2026 ✓ |
| Hồ sơ/nguồn | ✓ mạnh (22 nguồn) | ✓ | ✓ |
| **Thiếu chính** | đổi sang "Why…" + nơi; thumbnail bản đồ (Pittsburgh ↔ thế giới) | nơi cụ thể (một thành phố có tên) + cặp tương phản; thumbnail bản đồ/đối lập | tiêu đề chính chưa có cặp nơi; thử tiêu đề 3 trong Test & Compare vòng 2 |

**Kết luận:** T2 là gói đầu tiên khớp 9/10 tiêu chí (1 tiêu chí một phần: cặp tương phản chưa lên tiêu đề chính); giữ kế hoạch Test & Compare của T2. Với Steel/T1 (đã phát hành hoặc sắp phát hành), nếu kênh cho đổi tiêu đề/thumbnail, đề xuất thử một phương án "Why + nơi + tương phản" (chủ dự án quyết; tôi không sửa tệp tập).
**Xung đột luật cần chủ dự án/K xem:** `QUAN-TRI-RUI-RO` §4 mục 5 bắt câu miễn trừ ở **dòng đầu mô tả** khi chạm tài chính; công thức thắng dùng dòng đầu làm móc (YouTube hiện ~2 dòng ở trang xem/tìm kiếm). T2 đã đặt miễn trừ ở đoạn 2 — cần xác nhận cách này hợp luật hay xin sửa luật thành "trong 3 dòng đầu".

## 8. Mười đề tài kênh 2 theo Kinh thánh
Cách lọc: Kinh thánh §2 (cầu + neo thời sự + nghịch lý một câu + nhân vật có hồ sơ + mức rủi ro) và loại trừ **mọi đề tài** của FoN (13), GoDocs (42), Geography Effect (72), Uncover History (104), danh sách loại của `DONG-GOI.md` T2 và hàng đợi `HANG-DOI.md`. **Cầu sơ bộ** = lượt xem các video cùng đề tài tìm qua web (`teardown/cung-de-tai.json`), **chưa phải hồ sơ cầu** theo `LUAT-CHON-DE-TAI.md` (mỗi đề tài cần search.list ở G1). Neo tra bằng web ngày 15/10/2026, **phải xác minh bằng nguồn gốc trước khi khoá lời**. Chi tiết đầy đủ (nguồn số, cảnh 3D): `teardown/de-tai-10.json`.

| # | Đề tài (tên làm việc) | Nghịch lý một câu | Neo thời sự | Nhân vật có hồ sơ | Cầu sơ bộ | Rủi ro |
|---|---|---|---|---|---|---|
| 1 | **Gibraltar ↔ La Línea** — *The Fence Came Down: How a Rock With No Farmland Got Rich* | 6,8 km², không đất nông nghiệp, không sông, tự báo GDP/người thuộc nhóm cao nhất thế giới; thị trấn Tây Ban Nha bên kia hàng rào thất nghiệp thuộc nhóm cao nhất nước | Hiệp ước Anh–EU ký 14/07/2026, hàng rào gỡ 15/07/2026; ~15 000 người qua lại/ngày | George Rooke (1704, chân dung tài sản công); công nhân qua biên giới (A-lite) | **Cầu-bền CÓ**: 4,06 triệu (2021, góc "vì sao Anh giữ"); 470 nghìn (08/2026) | **VÀNG nhẹ** (tranh chấp chủ quyền; "thiên đường thuế" nói bằng luật/thuế suất; số GDP/người là số chính quyền tự công bố) |
| 2 | **Nauru** — *What a Country Sells When the Ground Runs Out* | Một hòn đảo từng thuộc nhóm giàu nhất thế giới tính theo đầu người đã đào gần hết chính mình; giờ sống bằng cách cho thuê vị trí, quốc tịch, chủ quyền | Hiệp ước với Australia (12/2024: 100 triệu AUD/5 năm); MoU nhận người bị trục xuất (08/2025); quốc tịch đầu tư (2025) — **neo 2024–25, cần tin 2026** | Albert Ellis (phát hiện phosphate 1900); Hammer DeRoburt (kiểm quyền ảnh) | **Cầu-bền CÓ**: 5,26 triệu (2022); 2026 gần như không có cung | **VÀNG** (chính sách xử lý người tị nạn ngoài khơi của Australia) |
| 3 | **Hiệp ước sông Colorado 1922** — *The 1922 Deal That Divided More Water Than the River Has* | Bảy bang chia sông theo những năm ướt nhất; một thế kỷ sau liên bang phải tự đặt luật, mỗi lần 2 năm | Record of Decision 21/08/2026 (hướng dẫn 2027–28, khung 2 năm/lần, các bang không thoả thuận); tuyết thấp kỷ lục 2025–26 | **Herbert Hoover** (chủ trì 1922; ảnh LoC) | Cầu-tìm: nhiều video 2026 cỡ 17–25 nghìn; kề Geography Effect (Las Vegas 48 nghìn, Phoenix 93 nghìn) | **XANH**; rủi ro bị xem là trùng Geography Effect: trung bình |
| 4 | **Zambia: hai đường sắt, một vành đai đồng** — *Two Railways, One Copper Belt* | Nước không giáp biển ngồi trên mỏ đồng lớn; 1970s Trung Quốc xây đường ra biển, 50 năm sau Mỹ trả tiền cho đường thứ hai | Lobito: gói 753 triệu USD đoạn Angola (07/2026); TAZARA: nhượng quyền 30 năm 1,4 tỷ USD (09/2025), cải tạo tới 2028 | Kenneth Kaunda, Julius Nyerere (ảnh chuyến thăm Nhà Trắng — kiểm) | Cầu-ngách: WSJ 294 nghìn (2024); dạng dài 2026 trống | **VÀNG** (Mỹ–Trung; nợ Zambia) |
| 5 | **Đường sắt cao tốc Tây Ban Nha** — *Spain Built Europe's Biggest Fast-Train Network. Competition Made It Pay.* | Mạng dài nhất EU, có tuyến vắng tới mức đóng cửa; rồi đối thủ vào, khách gấp đôi, giá giảm ~40 % | CNMC: 44,5 triệu khách 2025 (+12 %), gấp đôi 2019. **Không làm trục vụ tai nạn Adamuz 01/2026** | Felipe González (AVE 1992; kiểm giấy phép ảnh) | Cầu-ngách: 323 nghìn (2023); khán giả FoN đòi "Tây Ban Nha" | **XANH** (VÀNG nếu buộc nhắc tai nạn) |
| 6 | **Ma-rốc và phosphate** — *The Country Sitting on Most of the World's Fertilizer* | Giữ ~7/10 trữ lượng đá phosphate thế giới mà vẫn là nền kinh tế thu nhập trung bình thấp | Trung Quốc hạn chế xuất phosphate (tới ít nhất 08/2026); Mỹ ngừng thuế phosphate Ma-rốc 29/06/2026 (nguồn thứ cấp); phụ thuộc lưu huỳnh vùng Vịnh khi Hormuz gián đoạn | Hubert Lyautey (OCP lập 1920); thợ mỏ Khouribga (A-lite) | Cầu-bền dạng ngắn: 1,72 triệu (2019, 3,6 phút); tiếng Anh dạng dài 2026 trống | **VÀNG cao** (Tây Sahara; chiến sự Hormuz — không làm trục) |
| 7 | **Djibouti** — *The Country That Rents Out Its Coastline* | Gần như không có đất canh tác, sống bằng một dải bờ biển và những láng giềng không có biển | Ethiopia tìm lối ra biển; Saudi nhận khung nhượng quyền cảng Tadjourah (11/2025); gián đoạn Biển Đỏ | Menelik II (đường sắt 1917; ảnh tài sản công) | Cầu-ngách: 159 nghìn (tiếng Pháp, 2024), 133 nghìn và 109 nghìn (2023) | **VÀNG** (căn cứ quân sự; chỉ nói hợp đồng/tiền có nguồn; số tiền thuê lệch 25–125 triệu USD → đưa vào "the honest part") |
| 8 | **Lithium: Chile ↔ Bolivia** — *Chile Sells Lithium. Bolivia Has More. Why Does It Sell So Little?* | Nước báo tài nguyên lithium lớn nhất thế giới nằm cạnh một nước sản xuất hàng đầu, mà 15 năm gần như không bán được | NovaAndino Litio (Codelco–SQM) hoàn tất 27/12/2025; chính phủ Paz (01/2026) giữ nhưng rà soát hợp đồng 2024 | Simón Patiño ("vua thiếc"; ảnh đầu TK20) | **Cầu yếu**: 62 nghìn (2024) → phải đo search.list trước | **VÀNG**; kề FoN (Potosí) — khác tài nguyên, khác thời kỳ |
| 9 | **Cảng Hambantota** — *The Port Sri Lanka "Lost" to China: What the Records Show* | Biểu tượng "bẫy nợ" của thế giới không bị tịch thu vì nợ, theo hồ sơ vay và thuê — vậy vì sao Sri Lanka giao nó đi? | Nhà máy lọc dầu Sinopec 3,7 tỷ USD: 01/2026 đồng ý trần 20 % thị trường nội địa, chưa ký thoả thuận triển khai (cần tin mới) | **Yếu**: chủ thể là cơ quan; chính khách còn sống | Cầu-ngách: 86 nghìn (2023) | **VÀNG** (địa chính trị; vùng phỉ báng) |
| 10 | **Thâm Quyến ↔ Hồng Kông** — *The Border Town That Outgrew Hong Kong* | Năm 1979 là một huyện biên giới; nay kinh tế lớn hơn Hồng Kông, nhưng người Hồng Kông vẫn giàu hơn nhiều tính theo đầu người | GDP Thâm Quyến 2025: 3,873 nghìn tỷ NDT (+5,5 %); HK 2025 +3,5 %; ngân sách HK 2026–27: 30 tỷ HKD cho Northern Metropolis | Đặng Tiểu Bình (ảnh chính phủ Mỹ 1979 — kiểm) | **Chưa thấy cầu** (≤ 15 nghìn) | **VÀNG** (chính trị TQ/HK) |

- **Chuỗi gợi ý:** #2 Nauru → #6 Ma-rốc (phosphate: một nơi đào cạn, một nơi giữ 7/10) — câu dẫn ở màn kết đúng Kinh thánh §3.
- **Thứ tự đề xuất:** 1 → 3 → 2 → 5 → 4 → 6 (xen XANH giữa các VÀNG; `LUAT-CHON-DE-TAI`: không quá 2 VÀNG liền nhau). #8–#10 chỉ làm sau khi có hồ sơ cầu đo bằng search.list.
- **Lệch tỷ lệ trụ:** 10 đề tài nghiêng về *quốc gia/lãnh thổ + hạ tầng* (Kinh thánh mới), ít *thành phố Mỹ* (trụ T1 cũ). Đây là chủ ý theo Kinh thánh §1 ("quốc gia, thành phố hay ngành"); nếu `HANG-DOI.md` vẫn áp tỷ lệ T1 ≈ 60 %, cần chủ dự án quyết hàng đợi nào hiệu lực.
- **Đã loại trong phiên** (vì đối thủ trẻ vừa làm): Ba Lan, Argentina, dầu Na Uy–Venezuela, kênh Erie/New York, Singapore; Liberia–Firestone (không neo 2026, chủ thể là một công ty).
- **Chưa kiểm:** kho 10 kênh lớn của T2 (Wendover, RealLifeLore, PolyMatter…) — số thô của phiên T2 không có trong container này. Trước G1 mỗi đề tài cần tra lại kho đó (rẻ: `playlistItems`).
- **Bối cảnh lớn cần chủ dự án biết:** eo Hormuz gần như đóng với tàu thương mại (tin 30/09–12/10/2026; Brent ~$104). Mọi đề tài chạm dầu/vận tải biển sẽ đông kênh làm; đây là chiến sự đang diễn ra → **không làm trục tập** (vùng sai sự thật và cập nhật liên tục), chỉ dùng làm bối cảnh có "as of".

## 9. Mẫu brief thumbnail mới (thay mục 2 của `toolkit/market/brief.py` khi K/Nền tảng cập nhật)
```
THUMBNAIL BRIEF — <mã tập>
Ngữ pháp chọn: [A] BẢN ĐỒ TƯƠNG PHẢN  |  [B] CƠ CHẾ LỘ RA (không chữ)   (chọn 1; Test & Compare chạy A vs B)

[A] BẢN ĐỒ TƯƠNG PHẢN
- Nền: bản đồ nổi thật của chính tập (render relief của mình), bảng màu tự nhiên; tầm vùng đủ nhận ra hình dạng nơi chốn ở 168×94 px.
- Chủ thể: 1–2 vùng tô màu bão hoà theo MÃ MÀU CỐ ĐỊNH của tập (phía A / phía B), viền trắng, quầng sáng ≤ 0,2.
- Tương phản: vạch chia (dọc) HOẶC mũi tên dòng chảy (tiền/hàng/người) giữa hai vùng — chọn 1.
- Chữ: 1 hộp, nền tối đặc, chữ in hoa đậm ≥ 4,5:1, TỐI ĐA 2 từ HOẶC 1 con số + 1 từ; số phải có trong claims-allowed của tập.
- Biểu tượng: ≤ 2 sticker vật 3D của bộ k2v (ví dụ: tàu, tháp cẩu, hàng xu), đặt đúng chỗ trên bản đồ.
[B] CƠ CHẾ LỘ RA
- Một vật/nơi nổi tiếng của tập, render 3D tự dựng hoặc ảnh tài sản công đã kiểm giấy phép.
- Một mặt cắt / đối lập quá khứ (sepia) ↔ hiện tại (tự nhiên) / trước–sau, cho thấy CƠ CHẾ mà tiêu đề hỏi.
- Không chữ. Không mặt người làm tiêu điểm. Không hình dáng AI tả thực về nơi có thật (nếu có → bật nhãn AI theo QUAN-TRI-RUI-RO §2).

Chung (kiểm đọc, không chặn):
- Tiêu đề kèm: "Why …" + tên nơi + nghịch lý/cặp tương phản, ≤ 60 ký tự, không emoji, không từ cấm (§1.2: secret, hidden, who really controls…).
- Thumbnail không lặp chữ của tiêu đề; tiêu đề hỏi, thumbnail cho thấy.
- Lề an toàn 5 %; tránh góc dưới-phải ~18 % × 12 %; đọc được ở 168×94.
- Không logo công ty, không cờ làm điểm nhấn, không bạch tuộc/con rối/tay khổng lồ.
- Mọi hình và số trên thumbnail có trong video (QUAN-TRI-RUI-RO §4 mục 2).
- Ghi: ảnh nền (tệp/khung), nguồn ảnh tài sản công (ID LoC/NARA), mã màu hai phía.
- Test & Compare: 3 bản = A, B, và A với chữ khác (số ↔ từ); ghi kết quả vào SO-LIEU-7-NGAY.md của tập.
```

## 10. Đề xuất chỉnh khuôn độ dài (Kinh thánh §3: "9–11 phút")
- **Đề xuất:** đổi thành **"10–14 phút, theo số chương thật (7–10 chương × 75–100 s)"**; trần cứng 16 phút; không độn để đạt độ dài.
- **Lý do:** (1) không thấy hiệu ứng độ dài trong cùng kênh ở cả 4 kênh thắng (§0 ý 2); (2) kênh thắng trẻ nhất có trung vị bản thắng 13,5 phút (Geography Effect), GoDocs 15,7 phút; (3) FoN thắng ở 9,5 phút nên 10 phút không là cản trở; (4) 10–14 phút cho chỗ cho "the honest part" + trả lời trước các nguyên nhân khán giả sẽ cãi (§3) mà không kéo dài như Steel (17 phút) hay T1 (15,6 phút); (5) ≥ 8 phút giữ quảng cáo giữa video.
- **Ưu:** khớp dữ liệu, cho phép tập có nhân vật ở mỗi chương; giảm áp lực cắt thông tin nguồn.
- **Nhược:** dài hơn khung 9–11 → tăng chữ lời (~150 từ/phút: 1 500–2 100 từ), tăng giờ render và ký tự ElevenLabs ~20–30 %.
- **Tác động:** bảng hình theo câu, `est.py` ngân sách, CHUAN-KENH-K2 (K sửa luật); T2 (~10,5 phút) vẫn hợp.
- **Rủi ro:** giữ chân giảm nếu nhịp chậm — đo bằng đường giữ chân T2 và tập kế; nếu giữ chân < T1 tại mốc 30 s/50 %, quay về 9–11.
- **Phép thử:** tập sau T2 làm ở ~12–13 phút; so CTR/thời gian xem trung bình/giữ chân 7 ngày với T2 (Kinh thánh §8).

## 11. Giới hạn và điều chưa làm
- Mẫu kênh trẻ không ngẫu nhiên (§5). Kết luận "độ dài không phải đòn bẩy" dựa trên tương quan trong kênh (n = 5, 42, 68, 104), không phải thí nghiệm.
- API không cho CTR, thời gian xem, nguồn lượt xem của kênh khác → không kết luận vì sao GoDocs có tương tác thấp.
- Cầu của 10 đề tài là **sơ bộ** (cung + lượt xem video cùng đề tài); chưa có search.list theo câu hỏi khán giả.
- Neo thời sự tra bằng WebSearch (tóm tắt thứ cấp). Các mục ghi "cần xác minh": số GDP/người Gibraltar, thuế phosphate Mỹ 29/06/2026, nhánh Zambia của Lobito, Sinopec Hambantota sau 01/2026, tin 2026 về Nauru.
- Chưa đọc mô tả/chương của Geography Effect và Uncover History (chỉ tiêu đề + số), để giữ quota.

## 12. Việc đang chờ chủ dự án
1. **Duyệt TEARDOWN-FON** (nhánh `teardown-fon`, chưa merge — P merge).
2. **Chọn đề tài** cho tập kế từ §8 (đề xuất #1 Gibraltar hoặc #3 Colorado nếu cần XANH sau T2 VÀNG); cho phép đo hồ sơ cầu bằng search.list ở G1.
3. **Quyết khuôn độ dài** §10 (giữ 9–11 hay đổi 10–14 phút) → K đưa vào luật.
4. **Quyết vị trí câu miễn trừ** trong mô tả (§7: dòng đầu theo luật hiện hành vs dòng 3).
5. **Mẫu brief thumbnail** §9: duyệt để phiên Nền tảng/K đưa vào `brief.py`.
6. Quyết hàng đợi hiệu lực (`HANG-DOI.md` tỷ lệ T1 ≈ 60 % vs Kinh thánh "nơi chốn") — §8.
