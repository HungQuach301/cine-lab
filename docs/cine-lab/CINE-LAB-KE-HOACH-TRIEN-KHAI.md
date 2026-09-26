# CINE LAB — PHƯƠNG ÁN TRIỂN KHAI VÀ TỔ CHỨC NHIỀU AGENT SONG SONG (v0.1, 26/09/2026)

Căn cứ: khung `claude/CINE-LAB-KHUNG-CHAT-LUONG.md` (chủ dự án đã đồng ý v0.1); quyết định trong handoff §2. Không có mốc thời gian theo tuần/ngày; mỗi mốc có điểm dừng và chủ dự án duyệt.

## 1. Quyết định mới (26/09/2026)

| # | Nội dung | Quyết định |
|---|---|---|
| 1 | Khung chất lượng v0.1 | **Đồng ý** |
| 2 | Phim tham chiếu | Chủ dự án giao Claude tìm và chọn → danh sách mục 2 |
| 3 | Người chấm | Chủ dự án + một số người bạn |
| 4 | Nhạc | Nguồn miễn phí hoặc tự sinh → phương án mục 3 |
| 5 | Triển khai | Muốn nhiều agent làm song song → mục 4–6 |

## 2. Phim tham chiếu (đã kiểm có bản chính thức xem miễn phí, 26/09/2026)

Cách kiểm: gọi oEmbed YouTube, xác nhận tiêu đề và kênh đăng. Thời lượng lấy từ Wikipedia và báo chí. **Chưa kiểm chặn vùng từ Việt Nam.**

| # | Phim | Năm, tác giả | Thời lượng | Phong cách | Thoại | Giải | Dùng làm chuẩn cho | Link chính thức (kênh đăng) |
|---|---|---|---|---|---|---|---|---|
| R1 | **Ice Merchants** | 2022, João Gonzalez / Cola Animation | ~14' | 2D, bảng màu hẹp | Không | Đề cử Oscar lần 95; giải Cannes Critics' Week; Annie | Bố cục, màu, nhịp, nhạc gánh cảm xúc | youtube.com/watch?v=mhj74ZjfaQ8 (The New Yorker) |
| R2 | **Hair Love** | 2019, Matthew A. Cherry / Sony Pictures Animation | ~7' | 2D | Tiếng Anh (ít) | Oscar lần 92 | Diễn xuất cảm xúc, nét mặt, timing hài | youtube.com/watch?v=kNw8V_Fkw28 (Sony Pictures Animation) |
| R3 | **Alike** | 2015, Daniel Martínez Lara & Rafa Cano Méndez | ~8' | CG phong cách hoá (Blender) | Không | Goya 2016 | Màu như công cụ kể chuyện; diễn xuất không lời | youtube.com/watch?v=kQjtK32mGJQ (Pepe School Land) |
| R4 | **The Flying Sailor** | 2022, Amanda Forbis & Wendy Tilby / NFB | ~8' | Kỹ thuật hỗn hợp | Không | Đề cử Oscar lần 95; giải Sundance | Dựng, thiết kế âm thanh, cao trào | youtube.com/watch?v=4Rj3FG8vFtk (The New Yorker) |
| R5 | **Sprite Fright** | 2021, Blender Studio (Matthew Luhn, Hjalti Hjálmarsson) | ~10'30" | CG phong cách hoá | Tiếng Anh, nhiều nhân vật | — | Thoại tiếng Anh, dàn cảnh nhóm, timing; **giấy phép CC BY 4.0, có công bố file sản xuất**, nên được phân tích sâu | youtube.com/watch?v=_cMxraX_5RE (Blender Studio) |

Dự phòng: *Affairs of the Art* (16', thoại tiếng Anh dày, The New Yorker); *Umbrella* (8', CG không lời); *Spring* (8', Blender Studio, CC). *The Windshield Wiper* (Oscar lần 94) bị loại khỏi bộ chuẩn vì có nội dung người lớn (khoả thân, tình dục), không phù hợp khi mời bạn bè chấm.

Loại sau khi kiểm (không đoán): Kitbull, Purl (bản Pixar đã chuyển riêng tư); Loop, Wind, Out, Bao (chỉ có trên Disney+); Borrowed Time (ngừng phát); Late Afternoon (hạn chế); The Dam Keeper (có phí).

Quy tắc dùng: chỉ xem và phân tích. Không sao chép thiết kế, nhân vật hay nhạc (luật Q3). Riêng Sprite Fright được dùng tài sản theo CC BY 4.0, có ghi công.

## 3. Nhạc và SFX miễn phí hoặc tự sinh

Yêu cầu: dùng được cho **YouTube có kiếm tiền và bán phim**, tức cần quyền dùng ngoài YouTube.

| Phương án | Giấy phép (đã tra) | Ưu | Nhược | Rủi ro | Đánh giá |
|---|---|---|---|---|---|
| **N1. Tự sinh bằng ACE-Step** (mô hình nhạc mã nguồn mở) | Mã nguồn MIT (ACE-Step 1.5), trọng số Apache 2.0 (v1-3.5B) → dùng thương mại được | Toàn quyền; nhạc dài 10 s – 10 phút; chất lượng cao hơn nhạc sinh bằng mã | Cần GPU (≥ 4–6 GB VRAM); **chạy CPU "chậm hơn đáng kể", chưa đo** | Không kiểm được bản sinh ra có giống bài có bản quyền không; nguồn dữ liệu huấn luyện chưa rõ | **Ưu tiên thử ở Cổng 0**: đo tốc độ trên CPU của máy cloud |
| **N2. Nhạc sinh bằng mã** (như bài B–C) | Toàn quyền | Không phụ thuộc bên ngoài; khớp tempo map chính xác | Mắt xích yếu nhất đã biết | Chất lượng không đạt chuẩn điện ảnh | Phương án nền, dùng cho nhạc nền nhẹ và âm hình |
| **N3. Bản thu nhạc cổ điển thuộc phạm vi công cộng** (ví dụ Musopen) | Bản nhạc thuộc phạm vi công cộng; phải kiểm giấy phép từng bản thu | Chất lượng dàn nhạc thật; hợp phim điện ảnh | Không phải nhạc gốc; khó khớp dựng | YouTube Content ID có thể báo nhầm vi phạm (đã có người dùng Musopen phản ánh) | Dùng có chọn lọc |
| **N4. Nhạc CC BY** (ví dụ Kevin MacLeod) | Miễn phí nếu ghi công | Nhiều lựa chọn | Nhạc thư viện đã phổ biến, thiếu bản sắc | Phải ghi công đúng; tránh bản NC/ND | Dự phòng |
| **N5. YouTube Audio Library** | Kiếm tiền trên YouTube được; trang trợ giúp **không nói về dùng ngoài YouTube** | Dễ dùng | Không chắc quyền khi bán phim | Vi phạm khi bán phim | **Không dùng** cho phim đem bán |

SFX: Freesound (chỉ lấy bản **CC0** hoặc CC BY; loại bản NC), tài sản CC BY của Blender Studio, cộng tự tổng hợp bằng mã.
Mọi file nhạc và SFX vào sổ quyền (luật Q1).

**Khuyến nghị:** N1 làm nhạc chính nếu Cổng 0 đo được tốc độ chấp nhận được; N2 làm lớp bổ trợ; N3/N4 dự phòng.

## 4. Người chấm: chủ dự án + bạn bè — điều chỉnh để giữ tính mù

| Vấn đề | Tác động | Cách xử lý |
|---|---|---|
| Chủ dự án biết toàn bộ quy trình | Không thể chấm L3 (khán giả mù) | Chủ dự án chấm **L2** (nghề, theo rubric) và duyệt cổng |
| Bạn bè biết phim do AI làm | Thiên lệch khi so với phim tham chiếu | Chiếu **ngẫu nhiên thứ tự**; không nói phim nào của Cine Lab; hỏi trước "đã xem phim này chưa" để loại người đã biết phim tham chiếu |
| Khán giả đích nói tiếng Anh; bạn bè có thể là người Việt | Lệch đánh giá thoại và hài | Ưu tiên người thạo tiếng Anh; ghi trình độ tiếng Anh của từng người; thoại được chấm riêng |
| Mẫu nhỏ (3–5 người) | Kết quả dao động | Coi kết quả L3 là tín hiệu, không phải kết luận; ghi đủ ý kiến định tính |

Công cụ chấm: một trang web chấm mù (Artifact) — phát phim theo thứ tự ngẫu nhiên, nút "mất tập trung", câu hỏi sau khi xem, lưu kết quả tập trung. Làm ở mốc M1.

## 5. Nhiều agent song song: khả thi đến đâu (đã tra tài liệu Claude Code)

### 5.1 Năng lực có trong tài liệu hiện hành
- **Nhiều phiên cloud song song trên cùng repo:** được. Mỗi phiên là một máy ảo riêng, khoảng **4 vCPU / 16 GB RAM / 30 GB đĩa** (mức "xấp xỉ, có thể thay đổi"). Không công bố giới hạn số phiên đồng thời. Các phiên **dùng chung hạn mức sử dụng** của tài khoản; không tính phí máy ảo riêng.
- **Subagent trong một phiên:** chạy song song hoặc nền; định nghĩa riêng trong `.claude/agents/*.md` (công cụ, model, prompt); có `isolation: worktree` để mỗi agent sửa trên một worktree git riêng.
- **Agent teams:** có, nhưng **thử nghiệm và tắt mặc định** (bật bằng `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Có hộp thư giữa các agent và danh sách việc chung. Không resume được phiên, không lồng team, và tốn token nhiều hơn đáng kể.
- **Môi trường cloud:** allowlist mạng, API credentials, setup script dùng chung cho mọi phiên cùng môi trường.
- Ghi chú đo thật: máy Cowork đang dùng có 2 CPU / 7 GB. Máy của phiên Claude Code cloud theo tài liệu là ~4 vCPU; **phải đo lại ở Cổng 0**.

### 5.2 Việc nào song song được, việc nào không

| Giai đoạn | Song song? | Lý do |
|---|---|---|
| Cổng 1–2: ý tưởng, kịch bản | **Không** (một giọng tác giả) | Truyện cần một tầm nhìn; chủ dự án là tác giả. Chỉ song song việc phụ: sinh 3 phương án logline để chủ dự án chọn, table read, nghiên cứu |
| Cổng 3: thiết kế | **Có, theo luồng** | Nhân vật ∥ thế giới ∥ thử giọng ∥ chủ đề nhạc ∥ phiên K viết luật. Tất cả bám bible đã khoá |
| Cổng 4: animatic | **Hạn chế** | Một agent dựng animatic toàn phim để giữ nhịp; song song phần storyboard theo sequence |
| Cổng 5–7: layout, hoạt hình, render | **Có, lợi ích lớn nhất** | Chia theo sequence/shot; **mỗi phiên cloud là một máy render riêng** → nhiều phiên thành một "render farm" |
| Cổng 8: âm thanh | **Có** | Giọng ∥ SFX ∥ nhạc, bám timing animatic đã khoá |
| Cổng 9–10: hoàn thiện, chiếu thử | **Không** | Một agent tích hợp; chủ dự án duyệt |
| Kiểm định (phiên K) | **Tách riêng, chạy song song** | Phải là **phiên riêng**, không phải subagent của phiên sản xuất, để giữ độc lập |

### 5.3 Kiến trúc đề xuất: "studio" nhiều phiên

- **Chủ dự án:** tác giả, đạo diễn; duyệt cổng; phán quyết khiếu nại.
- **Phiên P — Điều phối (producer).** Một phiên cloud tương tác, giữ PLAN.md, bảng cổng và bảng shot; giao việc; tích hợp; không sửa luật. Bên trong dùng subagent có worktree cho việc nhỏ.
- **Phiên K — Kiểm định.** Phiên riêng, nhánh `checks/`; viết, khoá SHA và chạy luật trên file đã render; ghi kết quả vào `reports/`.
- **Các phiên xưởng W1..Wn (worker):** mỗi phiên nhận một gói việc (một sequence, một luồng thiết kế hoặc âm thanh) trên nhánh riêng. Đầu ra là file cộng manifest, không sửa tài sản của người khác.
- **Nguồn sự thật dùng chung (khoá SHA):** story bible, style bible, model sheet, world bible, thư viện tài sản, shot manifest (shot id, timing, camera, tài sản dùng, trạng thái).
- **Quy tắc tránh xung đột:** mỗi shot/sequence một thư mục; chỉ phiên P merge; render phải xác định (cùng đầu vào → cùng khung hình); mọi thay đổi bible phải qua chủ dự án.

### 5.4 Ưu, nhược, tác động, rủi ro

| | Nội dung |
|---|---|
| **Ưu** | Render song song trên nhiều máy ảo, gỡ nút cổ chai lớn nhất (15 phút = 21.600 khung); các luồng thiết kế và âm thanh chạy cùng lúc; phiên K độc lập thật vì là phiên riêng |
| **Nhược** | Chi phí và hạn mức tăng gần tuyến tính theo số phiên; tốn công điều phối và tích hợp; agent teams còn thử nghiệm |
| **Tác động** | Tổng thời gian giảm chủ yếu ở cổng 5–8; cổng 1–4 không nhanh hơn vì phụ thuộc chủ dự án |
| **Rủi ro** | (1) **Trôi phong cách** giữa các phiên → bible khoá SHA + luật C3/G2/O3 chạy trên từng shot; (2) chủ dự án thành nút cổ chai khi duyệt → gom duyệt theo cổng, không duyệt từng file; (3) xung đột merge → thư mục theo shot, chỉ P merge; (4) chạm trần hạn mức giữa chừng → giới hạn 2–4 phiên xưởng cùng lúc, đo ở M0; (5) Goodhart nhân bản theo số worker → luật do K khoá, worker không đọc mã luật |

**Kết luận:** khả thi. Nên **tăng dần**:
- **M0:** thử 2 phiên xưởng song song cộng phiên K.
- **Bài thử:** 2–3 phiên xưởng.
- **Phim 10–15 phút:** số phiên theo số đo thật.

Không dùng agent teams làm nền móng khi còn thử nghiệm; có thể thử ở M0 để so sánh.

## 6. Kế hoạch theo mốc

### M0 — Hạ tầng và Cổng 0 (năng lực)
1. Chủ dự án tạo repo riêng tư mới `cine-lab` trên GitHub, cấp quyền cho Claude Code.
2. Chủ dự án tạo môi trường cloud `cine-lab-av`:
   - mạng Custom + default list, thêm `api.elevenlabs.io`, `huggingface.co`, `*.huggingface.co`, `*.hf.co`, `freesound.org`;
   - API credential ElevenLabs (gói trả phí thấp nhất có giấy phép thương mại; kiểm giá khi đăng ký);
   - setup script: ffmpeg, faster-whisper, pyloudnorm, bpy trong venv riêng, Chromium headless, có bước thử lại khi `apt-get` lỗi.
3. Phiên P dựng khung repo: `bible/`, `assets/`, `shots/`, `checks/` (của K), `reports/`, `AUTHORSHIP.md`, `RIGHTS.md`, `PLAN.md`, `.claude/agents/` (mục 7).
4. Phiên K v0: viết và khoá luật L1 (kỹ thuật file, chữ theo điểm ảnh, ASR, loudness) kèm test tự chứng minh; chạy trên bài C để chứng minh luật có tác dụng.
5. Đo thật:
   - CPU/RAM của máy cloud;
   - tốc độ render 10 s cho 3 phong cách ứng viên: 2D vector (Canvas/SVG), 2.5D three.js, Blender (Workbench/Grease Pencil, không dùng Cycles);
   - ElevenLabs với 1 cảnh cảm xúc khó;
   - ACE-Step trên CPU (thời gian cho 60 s nhạc);
   - nhân vật dựng ở 2 phiên khác nhau (sai lệch C3);
   - 2 phiên xưởng render song song (tốc độ, xung đột, hạn mức).
6. **Điểm dừng:** báo cáo số đo. Chủ dự án chọn phong cách hình, nguồn nhạc, số phiên song song.

### M1 — Bài thử 2–3 phút: phát triển đến animatic (Cổng 1–4)
1. Chủ dự án đưa ý tưởng. Phiên P sinh 3 phương án logline và chủ đề song song; chủ dự án chọn và sửa, ghi vào AUTHORSHIP.md.
2. Beat sheet → kịch bản → table read bằng ElevenLabs → danh sách sửa. Chủ dự án duyệt.
3. Song song: model sheet, world bible, color script, 5–8 style frame (W1); thử giọng (W2); chủ đề nhạc (W3); K viết luật L2 và rubric kèm ví dụ từ R1–R5.
4. Dựng animatic toàn phim.
5. Làm trang chấm mù; chiếu thử L3 trên animatic với bạn bè.
6. **Điểm dừng Cổng 4:** trượt thì quay lại kịch bản.

### M2 — Bài thử: sản xuất đến chiếu thử (Cổng 5–10)
1. Tách shot manifest; giao sequence cho các phiên xưởng.
2. Layout → hoạt hình rough → duyệt → polish → render song song.
3. K chạy luật trên từng shot; phiên xưởng không sửa luật, khiếu nại ghi file riêng.
4. Âm thanh: giọng cuối, SFX, nhạc, mix; master YouTube và master lưu trữ; phụ đề; credit.
5. Chiếu thử cuối L3, gồm so cặp mù với phim tham chiếu.
6. **Điểm dừng:** báo cáo đủ 3 lớp chất lượng.

### M3 — Hiệu chuẩn khung v1.0 và thiết kế đội cho phim dài
1. Đối chiếu kết quả luật máy với điểm người; hạ cấp luật không phân biệt được tốt/xấu.
2. Hiệu chuẩn ngưỡng nội bộ bằng số đo thật.
3. Đo hiệu quả song song: thời gian, chi phí, lỗi trôi phong cách theo từng cổng.
4. Phát hành khung v1.0 và cấu hình đội (số phiên, vai trò) cho phim 10–15 phút.
5. **Điểm dừng:** chủ dự án duyệt trước khi làm phim đích.

### M4 — Phim 10–15 phút
Lặp Cổng 1–10 theo khung v1.0, song song theo sequence, chiếu thử L3 ở animatic và bản cuối.

## 7. Phụ lục: định nghĩa agent mẫu (`.claude/agents/`) — bản nháp

```markdown
---
name: cine-worker
description: Dựng một gói việc (sequence/shot hoặc luồng thiết kế/âm thanh) theo shot manifest và bible đã khoá. Dùng khi phiên điều phối giao gói việc.
tools: Read, Write, Edit, Bash, Glob, Grep
isolation: worktree
---
Bạn là thành viên xưởng Cine Lab. Chỉ sửa trong thư mục gói việc được giao.
Không sửa bible/, assets/ đã khoá, checks/. Không đọc mã trong checks/.
Mọi tài sản mới phải vào RIGHTS.md. Mọi quyết định sáng tạo cần chủ dự án duyệt thì ghi vào hàng chờ trong PLAN.md.
Khi xong: render, tự chạy lệnh kiểm do K cung cấp (không sửa), ghi báo cáo, commit.
```

```markdown
---
name: cine-continuity
description: Rà liên tục giữa các shot kề nhau theo continuity sheet; chỉ báo lỗi, không sửa.
tools: Read, Bash, Glob, Grep
---
So từng cặp shot kề nhau với continuity sheet và model sheet. Ghi lỗi vào reports/continuity.md kèm khung hình minh chứng.
```

Phiên K **không** định nghĩa là subagent của phiên sản xuất. K chạy như một phiên cloud riêng.

## Nguồn
- Claude Code docs: cloud sessions https://code.claude.com/docs/en/claude-code-on-the-web.md ; cloud environments https://code.claude.com/docs/en/cloud-environments.md ; subagents https://code.claude.com/docs/en/sub-agents.md ; agent teams https://code.claude.com/docs/en/agent-teams.md ; worktrees https://code.claude.com/docs/en/worktrees.md
- ACE-Step 1.5 (MIT): https://github.com/ace-step/ACE-Step-1.5 ; ACE-Step v1-3.5B (Apache 2.0): https://huggingface.co/ACE-Step/ACE-Step-v1-3.5B
- YouTube Audio Library: https://support.google.com/youtube/answer/3376882
- Kevin MacLeod licenses: https://incompetech.com/music/royalty-free/licenses/
- Musopen (Content ID báo nhầm): https://musopen.org/music/4107-goldberg-variations-bwv-988/questions/70/
- Freesound FAQ: https://freesound.org/help/faq/
- Stability AI Community License: https://stability.ai/license
- Phim tham chiếu: Wikipedia các phim; Blender Studio Sprite Fright https://www.blender.org/press/sprite-fright-open-movie/
