# BÀI HỌC — Kênh 2 (cơ chế kinh tế, ngách B/G)

> Mọi phiên P kênh 2 đọc tệp này khi khởi động, cùng `reports/m3/BAI-HOC-LL.md` (phần dùng chung của nhà máy).
> Mỗi dòng: bài học · số đo · nguyên nhân · luật hiện hành (nằm ở đâu). Chủ dự án duyệt ghi 11/10/2026 (G1 K2G-01, D6).

| # | Bài học | Số đo | Nguyên cớ | Luật hiện hành |
|---|---|---|---|---|
| K1 | Nhân giá CBAM (€/t CO₂) với cường độ CO₂ theo tuyến của worldsteel là **trộn cơ sở**: CBAM với thép chỉ tính phát thải **trực tiếp** (quy định (EU) 2023/956, Phụ lục II), còn số worldsteel tính theo phương pháp riêng (có phần gián tiếp) | K2G-01: phép tính "≈ 190 €/t vs ≈ 57 €/t" sống qua v1–v3.3, REVIEWER Opus phát hiện ở lượt 7 | ghép hai số đúng từ hai nguồn mà không đọc định nghĩa phạm vi | Phép tính riêng của kênh phải kiểm **định nghĩa và phạm vi** của từng đầu vào (BAI-HOC LL #62 mở rộng sang luật/giá); khác phạm vi thì bỏ phép tính, chỉ nêu cơ chế (claims C51 → C73) |
| K2 | Sự kiện "đang diễn ra" có thể đổi trong 3 tuần giữa lúc viết lời | Stegra: thông cáo 24/06/2026 "timeline under review" → tin 30/09/2026 cần thêm vốn, đổi CEO; lời v2 ghi "latest public update" đã lỗi thời, phát hiện ở vòng kiểm 2 | tra trạng thái một lần lúc lấy nguồn | Tra lại mọi trạng thái "as of" **ngay trước khi khoá lời** và **ngay trước khi thu giọng** (LUAT-NOI-DUNG-G §5); ghi ngày tra vào `claims.md` |
| K3 | REVIEWER Opus không hội tụ trong một lượt: mỗi lượt sửa câu làm lộ lỗi câu mới | K2G-01: major 13 → 6 → 4 → 3 → 3 → 4 → 1 → 2 → 0 qua 9 lượt; minor không về 0; Opus = $5,37 / $6,12 chi phí AI | sửa từng câu theo danh sách, câu mới lại có quy chủ thể/nhân quả/mốc thời gian chưa chặt | **Tiêu chí dừng: 0 major** (minor áp nếu rẻ, không chạy thêm lượt vì minor). Viết lời từ đầu theo danh sách lỗi hay gặp: nhân quả chỉ khi nguồn nêu; "as of" cho mọi sự kiện mở; quy lời cho đúng chủ thể (văn bản, cơ quan, báo); không tự chấm đạt/trượt chính sách; số khác cơ sở nói rõ |

## K4 · Mốc "@từ" khớp lần xuất hiện ĐẦU TIÊN — kiểm thứ tự shot bằng máy (G2 K2G-01, 12/10/2026)
- **Chuyện xảy ra:** đoạn 08 `@by` khớp "by 2028" thay vì "By our calculation"; đoạn 12 `@question` khớp "security question" thay vì "One question". Shot sau bắt đầu TRƯỚC shot trước → thẻ số neo 131,2 Mt và shot "a toll" không bao giờ hiện; QC nhà máy (Q1–Q25) không bắt được, chỉ lộ khi soát timeline sau QC 1080p. Tốn một lượt dựng lại 2 đoạn.
- **Luật:** `scripts/k2/prep.py` nay dừng hẳn khi có shot `t1 ≤ t0 + 0,3 s`. Khi viết đặc tả, từ phổ biến (by, in, the, question, one, our…) luôn kèm `#n` hoặc chọn từ hiếm.
- **Lưu ý cho LL:** README LL đã ghi bẫy "@many"; nên thêm cùng chặn vào `scripts/ll/ll.py` (đề xuất cho phiên P LL/K, không sửa ở phiên này).

## K5 · Màu canvas trong three.js mới: `THREE.Color` ở hệ tuyến tính (G2 K2G-01)
- Vẽ vân bằng `new THREE.Color(hex).multiplyScalar(k)` rồi lấy `c.r*255` cho ra màu tuyến tính → vân tối gần đen sau khi texture được coi là sRGB. Dùng `'#' + c.getHexString()`. Phát hiện ở nháp 960×540 nhờ soát khung, trước khi dựng 1080p.

## K6 · Bối cảnh tính cả thẻ (chủ dự án duyệt D4, 12/10/2026)
- **Chuyện xảy ra:** luật đa dạng bối cảnh (Q26b kênh 2) tính bối cảnh theo cảnh 3D nền, kể cả nền mờ sau thẻ số → K2G-01 đạt (lớn nhất 21,7 %). Nhưng cả 3/3 người xem mù (Q31) nêu "thẻ tối trên nền mờ" là bối cảnh bị lạm dụng (~ một nửa tấm tổng quan); Q27 tay nghề 5/10.
- **Luật từ tập sau:** "thẻ trên nền mờ" là MỘT bối cảnh riêng, chịu cùng trần (≤ 25 % thời lượng, ≤ 90 s liên tục). Nền mờ không tính cho bối cảnh của cảnh 3D. `scripts/k2/settings.py` sẽ tính thêm hạng mục `card` (phiên P làm ở tập sau); luật khoá do phiên K cập nhật (không sửa `checks/` ở phiên P).

## K7 · Đề xuất nâng hình cho tập sau (chủ dự án ghi nhận D3, 12/10/2026; không làm lại K2G-01)
- **Số đặt trong cảnh 3D rõ nét** bằng nhãn bám vật thể (như đoạn 00, 05 của K2G-01); thẻ trên nền mờ chỉ cho số cần so sánh trên trục (cột, đường).
- **Thay một phần thẻ-trên-nền-mờ bằng footage lưu trữ** theo `QUAN-TRI-RUI-RO.md` §6: nguồn cho phép (LoC, NARA, NASA, Prelinger, Commons kiểm từng file, Pexels/Pixabay), trần ≤ 40 % thời lượng và ≤ 8 s mỗi clip, nhãn năm trên hình, sổ `SOURCES-FOOTAGE.csv`, không commit media, giữ màu gốc cảnh lưu trữ.
- **Thẻ co theo nội dung** (không nửa thẻ trống); mục đầu luôn hiện khi vào thẻ.
- **Phụ đề có nền đậm** (dải đặc, không chỉ gradient) và chữ trắng đủ đậm; kiểm Q5 trên khung trời sáng.
- **Vật liệu PBR và ánh sáng giàu hơn** cho port/mill (Q27 nêu "khối xám phẳng"); bản đồ có nhãn địa danh trên hình.
- **Đo:** Q27 tay nghề ≥ 7/10 và "above" so với faceless thường mới coi là tiến bộ; giữ chấm mù một lần trên 1080p.
- Ưu: tăng điểm hình, giảm cảm giác "slide". Nhược: thêm giờ dựng cảnh và giờ tìm footage. Rủi ro: SwiftShader chậm (4,2 s/khung SPP4); footage sai quyền → luật §6 và sổ CSV.

## K8 · REVIEWER không hội tụ: bỏ câu gây rủi ro thay vì viết thêm (chủ dự án duyệt D7, G1a K2C-T1-06, 12/10/2026)
- **Chuyện xảy ra:** major qua 8 lượt REVIEWER Opus là 13 → 10 → 5 → 5 → 2 → 1 → **4** → 0. Vòng 7 tăng lên 4 vì cả 4 lỗi đều nằm trong câu mới viết ở v7 để sửa minor: câu IBC/Washington mơ hồ và thiếu as-of; câu hỏi "how much of the decline comes from each" ngầm nhân quả; tóm tắt nghiên cứu lệch. Ở v8, chỉ **bỏ** câu (SBCC 16/10, trích MHC 2007, mã NYC, Freddie Mac) → 0 major, lời ngắn hơn 0,6 phút.
- **Luật:** khi một vòng REVIEWER làm tăng major, ưu tiên bỏ câu gây rủi ro (nhất là câu có trạng thái sẽ đổi trước khi thu, câu nhân quả, câu tóm tắt tranh luận) thay vì viết câu mới. Sau 0 major, minor chỉ áp khi là đổi chữ không thêm thông tin, và lượt kiểm chứng sau đó chỉ được sửa bằng đúng chữ REVIEWER đề xuất (bổ sung K3).

## K9 · Trích dẫn lịch sử gây cảm xúc mạnh bị đọc là khung một phía (chủ dự án duyệt D7, G1a K2C-T1-06, 12/10/2026)
- **Chuyện xảy ra:** trích *Euclid* (1926) "very often the apartment house is a mere parasite" có nguồn đúng và quy chủ thể đúng, nhưng 2/3 người đọc mù ở vòng 2 và 3 vẫn thấy nó "gợi khung zoning là phân biệt giai cấp" và nghiêng về phía chống zoning. Ở v4, thay bằng phần lý do Toà liệt kê (chiều cao, khối tích chắn nắng và không khí, xe cộ) cùng nguyên mệnh đề "in a different environment would be… highly desirable, come very near to being nuisances" → không ai nêu nữa.
- **Luật:** với đề tài VÀNG, trích nguồn lịch sử theo **lý do chính nguồn đó nêu**, không chọn câu giàu cảm xúc nhất; trích **trọn mệnh đề** (REVIEWER v4 bắt lỗi cắt mất mệnh đề chính, làm đảo nghĩa). Nếu cần câu mạnh, đặt cạnh lý lẽ của phía bên kia trong cùng shot.

## K10 · Module hình k2v (đổi số từ K8 khi squash vào k2c-t1-06, chủ dự án 13/10) (phiên V, 12/10/2026)
- **`ctx.filter` trên canvas lớn trả về rỗng:** canvas 8192×4096 trong Chromium headless + `filter` → ảnh trắng (đo: điểm ảnh (0,0,0,0) với filter, (100,89,45) không filter). Chỉnh tông bằng lớp phủ, không dùng `ctx.filter` cho canvas > 4096. Lộ ra ở tờ khung nháp đầu (địa cầu không có ảnh vệ tinh).
- **Tiến trình dựng cảnh chết khi tiến trình cha bị dừng:** `hero.js` ghi log qua ống stderr của cha; dừng cha → ống đứt → node chết ở lần ghi log kế tiếp (mất 145/300 khung, dựng tiếp bằng `--resume`). Chạy nền dài: `setsid nohup …` với log ra tệp.
- **"Biến thể rẻ" phải khác góc thật:** preset quay quanh điểm nhìn ±12–25° bị pHash của K (Q33, θ = 14) coi là cùng góc (shot mẫu D: `mid-push` ↔ `orbit-r12-low` lệch 21°; `orbit-l45` ↔ `orbit-r60` lệch 15°). Luật làm việc: `prep.py` gộp góc khai khác nhưng gần (phương vị < 25°, độ cao < 10°, khoảng cách < 1,4×, tiêu cự < 1,3×) — cùng hướng với Q33, chỉ cộng không trừ. Thư viện: rà tờ khung, đếm "họ góc" khác nhau, không chỉ đếm tên preset.
- **Bản đồ phải giữ hướng Bắc:** góc xoay > 60° hoặc nhìn ngược trên sa bàn bản đồ làm mất nhận diện địa lý → loại (chain).
- **Chấm mù cặp số liệu (P2):** cột 3D tỷ lệ thật đẹp hơn (tay nghề 7 vs 5) nhưng 2/3 người chấm vẫn chọn thẻ phẳng vì chữ phụ mờ, đỉnh cột bị cắt, khối 1950 cuối shot không còn nhãn — khớp số đo máy (tương phản 2,8). Chữ trên cảnh 3D cần nền đặc hơn thẻ (0,93) và chữ phụ sáng (#D3DAE2, 32 px).

## K11 · Bốn điểm hình còn lại của K2C-T1-06 — đầu vào phiên V2 (chủ dự án duyệt D2 G2, 14/10/2026: giữ bản phát hành, không sửa thêm)
Nguồn: chấm mù một lần trên 1080p (`k2c-t1-06/kiem-mu/blind-g2/`, Q27 tay nghề 6,17, 3/3 "above"); cả 3 người chấm cùng nêu.
- **Biểu đồ không được có khung "sàn lưới trống" khi lời đã nói (`ch_icc` F04, 7:05.8, 3/3/3 điểm):** cột chỉ mọc ở mốc số nên đầu shot là lưới + vài vạch. Luật cho V2: biểu đồ vào shot không quá ~1 s trước số đầu tiên, hoặc có vật thể/ghi chú giữ khung từ đầu (Q18 của K chỉ đo shot `bars/line/…` của LL, không bắt mẫu chart3d k2v).
- **Máy chạy ngang không được cắt vật thể chính (`ch_icc` F05, side-track, cuối shot cột bị cắt mép trái, nhãn đè cột):** preset side-track chỉ an toàn khi vật thể nằm trọn trong khung ở cả u=0 và u=1. V2 thêm kiểm máy: chiếu hộp bao của mọi cột ở khung đầu/giữa/cuối, lệch khỏi vùng an toàn → đổi preset (đã gặp cùng loại lỗi với crane-up ở nháp: `ch_terner`, `ch_small`, `ch_mpls`).
- **Nhãn đang hiện dần không được nằm đè vật thể (`ch_pew` F03, nhãn 13 % mờ chồng khối):** nhãn `side: right` của cột cao nhất rơi vào khối kế bên. V2: nhãn số đặt theo hướng trống (up/left/right) bằng kiểm va chạm với hộp chiếu của khối, không chỉ với dải chú thích.
- **Mối nối footage sáng ↔ cảnh 3D tối (J07 06→07, 1/3 coi là gãy):** lời về bảo lãnh cá nhân nhưng hình là bản đồ California rồi footage cần cẩu sáng. V2: footage chỉ dùng khi khớp đúng danh từ của lời; mối footage ↔ 3D có hoà tan 0,3–0,5 s hoặc chỉnh tông footage gần cảnh 3D; thiếu footage đúng thì dùng cảnh 3D/ảnh lưu trữ.
- **Thẻ tóm tắt phẳng (TO RECAP, F09, 5/4/5):** thẻ list nhiều chữ, nhiều khoảng trống. V2: thẻ tóm tắt có biểu tượng/hình nhỏ cho từng mục (ba khoá), hoặc thay bằng cảnh 3D ba khoá.
- Ghi thêm (cả 3 người chấm, Q31): lạm dụng toà góc phố chạng vạng và bản đồ địa cầu; nhãn ACTUAL lặp nhiều; dòng nguồn nhiều nguồn dài trên điện thoại.

## K12 · Bộ hình V2: bản đồ nổi + sticker (phiên V2, 14/10/2026; chờ chủ dự án duyệt)
- **Chú thích `//` trong chuỗi GLSL viết một dòng nuốt phần còn lại của `main()`:**
  - Shader lỗi biên dịch. three.js chỉ ghi vào console, nên đã dựng xong 2 lượt nháp toàn khung thiếu địa hình mà không báo.
  - **Luật:** trong chuỗi shader chỉ dùng `/* */` (`test_k2v.py`). `scripts/k2/hero.js` nay dừng có mã lỗi khi gặp "Shader Error".
- **`pkill -f <mẫu>` giết luôn shell đang chạy lệnh** (dòng lệnh của shell chứa mẫu đó). Dừng tiến trình nền bằng PID (`ps … | awk | xargs kill`).
- **Chấm mù V2:**
  - Sticker phẳng bị người chấm "broadcast" gọi là "clip-art dán lên" (2–3/3). Bóng tiếp đất giảm nhưng không hết.
  - Dòng nguồn 30 px bị nêu "nhỏ trên điện thoại" ở mọi cặp (người chấm xem ảnh 1280 px).
  - Hành trình phải thấy **trọn tuyến và nhãn hai đầu mút** ở khung chấm. Khung bám sát vật đi bị chấm "confusing", thua T1 3/3; sau khi mở rộng khung thì thắng 3/3.
  - Chi tiết: `K2V2-BAO-CAO.md` §5.
- **Nhãn né vật phải tính từ MÉP hộp vật, không từ tâm neo:**
  - Khi nhãn bị kẹp vào lề an toàn, nó trượt ngược lại và đè lên vật.
  - Phép kiểm va chạm phải tính cả hộp của chính vật (nhãn "1/10" ở nháp).

## K13–K17 · Bài học K2C-T2-01 "Shipbuilding" (không phát hành, VV1 — P-1710 ghi 17/10/2026)
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| K13 | Phim gần như chỉ có bản đồ | Bản đồ **88,7 %** thời lượng; nửa sau chỉ 2 loại cảnh; bờ Đông 37,8 % phim, liên tục 120,5 s (2:48–4:48) (K-1.12.2 Q26b-K2 TRƯỢT) | Bộ hình k2v mạnh nhất ở bản đồ nổi nên mọi ý đều đổ về bản đồ; không có ngân sách loại cảnh lúc viết đặc tả | Q26b-K2 (checks 1.12.2, CHỈ BÁO tới khi duyệt áp); đặt ngân sách loại cảnh từ G1 |
| K14 | Nơi có thành phố (Richmond, Philadelphia, Ulsan) chỉ hiện địa hình/ảnh hàng không, không có nhà, phố đúng thời kỳ | Chấm mù E2/P2 ghi "map zoomed so far in… no context"; chip nơi dựng phải thêm cho 16 shot bản đồ (SS1) để người xem biết đang ở đâu | Bộ công cụ chưa có lớp nhà/phố theo thời kỳ; dùng DEM + NAIP thay cho thành phố | **VV2** (luật mới, chờ K): nơi có thành phố phải có nhà/phố đúng thời kỳ — `reports/K-HANG-DOI-KHIEU-NAI.md` |
| K15 | Địa cầu và độ cao lớn bị dùng thừa | g05_china: máy 30 → 18 → 22 bán kính Trái Đất; r04_abroad mở xa rồi đẩy vào (G2 §13–§14) | Dùng tầm cao để "đổi cảnh" thay cho nội dung mới | **VV2:** địa cầu/độ cao lớn ≤ 1 lần/tập, ≤ 3 s (chờ K đo) |
| K16 | Vòng sửa theo chấm mù tạo lỗi mới | L4: E2 0/3, P2 7,00 → 6,67, P6 6,67 → 6,00. Ba lỗi đều do chính lượt sửa: nhãn hiện dần chỉ đạt khoảng 20 % ở giây khung, viền vùng thành dải trắng, tấm chữ chừa khoảng trống | Sửa xong chấm ngay, không nhìn khung đúng giây đã khai | **TT3:** luôn **so khung trước khi chấm** (tờ trước ↔ sau, đúng giây đã khai, tự rà từng cặp) |
| K17 | Năm vòng chấm mù không vượt được giới hạn thiết kế | RÀ GU 6,62 → 6,81 → 6,76 → 6,81 → 6,90; phần sửa 6,47 → 6,87 → 6,87 → 6,80 → 6,87; API chấm $15,16. Vẫn thua E2 (hình thức cảnh), P6 (nguồn 640×480, trần 1,45×) | Lỗi nằm ở hình thức cảnh và nguồn, không ở lớp chữ. Vòng sửa lớp chữ chỉ cải thiện biên | Lỗi thiết kế quyết ở G1/tờ khung (đổi hình thức cảnh, nguồn ≥ 720p); không mở thêm vòng chấm mù để vá thiết kế |

## K18–K24 · Vận hành và đo ở SFX-T3, ANIMATIC-T3-V2 (P-2210 ghi 22/10/2026)
| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |
|---|---|---|---|---|
| K18 | Ghi đè lịch sử nhánh của chính phiên để gỡ tệp lỡ đẩy | SFX-T3: commit đầu `699403cb` đẩy trước khi cài hook, có 2 email bên thứ ba → `--amend` + `--force-with-lease` (commit cũ còn truy được theo SHA trên GitHub); ANIMATIC-T3-V2: commit lọt 9 video > 5 MB → amend + force-with-lease (`reports/sfx-t3/SFX-T3-BAO-CAO.md` khối điều lệ; `reports/animatic-t3-v2/ANIM-V2-BAO-CAO.md` §10) | Coi nhánh phiên là "của mình" nên được ghi đè; hook preflight cài sau lần đẩy đầu | **KHÔNG force-push, kể cả nhánh của phiên.** Lỡ đẩy thì commit mới gỡ tệp + báo trong báo cáo (tệp đã đẩy coi như đã lộ). Cài hook preflight (`pre-commit`, `pre-push`) TRƯỚC lần đẩy đầu; môi trường chặn cài hook thì chạy preflight tay trước mọi commit/đẩy |
| K19 | `preflight … \| tail -1 && git commit` không chặn khi preflight trượt | ANIMATIC-T3-V2: preflight báo TRƯỢT, commit vẫn chạy, lọt 9 video (§10) | Mã thoát của ống lệnh là của `tail`, không phải của preflight | Chạy với `set -o pipefail` **và** kiểm chữ "— ĐẠT" ở dòng kết luận trước khi commit (P-2210 dùng cả hai) |
| K20 | PID lấy từ `$!` của `setsid` là tiến trình đã thoát | ANIMATIC-T3-V2: 3 vòng dựng chạy chồng (§10) | `setsid` tách nhóm rồi thoát; tác vụ chờ thấy PID chết nên khởi động thêm vòng | Ghi và dừng theo **PGID**; một vòng dựng một lúc (khoá tệp/kiểm nhóm trước khi khởi động) |
| K21 | OOM khi 3 trình duyệt dựng + Blender nướng | ANIMATIC-T3-V2: cgroup giết chrome khi P = 3 + Blender (§6, §10) | Bộ nhớ container không đủ cho cả hai tải | **P = 2 khi đang nướng**; P = 3 chỉ khi không có Blender chạy |
| K22 | Tệp đầu vào cho bước sau để ở `/var/tmp` mất khi container bị thu hồi | Master v1, lightmap, cảnh đinh của ANIMATIC-T3 mất → V2 nướng lại 7 lightmap ≈ 5,4 h; video gốc Omni chỉ ở `/var/tmp` cho tới lệnh cứu 22/10 (`omni/goc720/`, 4 tệp ≤ 4,9 MB) | Coi `/var/tmp` là bền | Mọi tệp đầu vào cho bước sau (video gốc AI, lightmap…) phải có **bản nén ≤ 5 MB trong git** hoặc **tạo lại được từ lệnh + SHA** ghi trong báo cáo, ngay khi tạo ra |
| K23 | Thước R2 "> 50 % khung" bắt thiếu "eo đất trống" mà chủ dự án thấy | Khung v1 N1.5, N1.6: cỏ 25–45 % + trời ≈ 40 % → không vượt 50 %, thước báo đạt; chủ dự án thấy trống (`ANIM-V2-BAO-CAO.md` §8.1) | Thước đo một ngưỡng diện tích, không đo "có vật để nhìn" | **Mắt chủ dự án là chuẩn**; thước chỉ là số tham khảo (Kinh thánh §14.7: R1 chấm bằng mắt, V2-D2) |
| K24 | Đổi góc làm mất vật mà lời nhắc tới | C4 đổi góc → mất đoàn tàu cứu viện 1780 trên hình; XEM CÂM Q4 "cái gì đến cứu" 4 → 2 (`ANIM-V2-BAO-CAO.md` §8.5) | Sửa góc theo luật bố cục, không đối chiếu câu lời của shot | **Đổi góc phải giữ vật mà lời nhắc tới**; soát tờ so đối chiếu từng câu lời của shot trước khi chốt góc mới |
