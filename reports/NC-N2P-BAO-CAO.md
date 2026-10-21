Nhánh thật: `nc-n2p` (tạo từ origin/main @bc7e96d1 theo lệnh; harness gợi ý nhánh `ccr-7b29f52b-ixkuxi` nhưng làm theo lệnh chủ dự án). Không merge. Chỉ tạo/sửa `reports/nc-n2p/**` và tệp này (≈ 18 MB, không LFS, video ≤ 2,3 MB/tệp). Không sửa `design/`, `scripts/`, `checks/`, `docs/`, `channel-*/`, sổ, `main` hay nhánh khác; mã V7C/NC-V2V/NC-V2V3 chỉ được GỌI (worktree tạm `/var/tmp/n2p-wt` @ V7C 47a0f55a và bản sao tạm của `do_them3.py` từ origin/nc-v2v3).

# NC-N2P — Nghiên cứu + thử luật AI "N2+" cho T4 London 1666: BÁO CÁO

> Phiên nghiên cứu 21/10/2026 04:20–08:00 UTC. Chỉ nghiên cứu + thử nhỏ, không dựng phim; T3 giữ N1/N2. Mọi số là số đo thật trong phiên (tệp ở `reports/nc-n2p/`), trừ chỗ ghi **(ước)**. Khoá do proxy gắn (OpenAI, Gemini `x-goog-api-key`); mã không đọc/in/ghi khoá. User-Agent `CineLab-research (+https://github.com/HungQuach301/cine-lab)`; không đưa email vào header/URL/payload/prompt. Chỉ gửi lên API khung/clip do ta dựng (máy V7B/V7C, cách A NC-CPU) và chữ lệnh; không gửi khung đối thủ. Preflight: ĐẠT ở mọi commit (lock.py KHỚP).

## §0. Tóm tắt + bảng quyết định đề xuất

**Kết luận một dòng:** N2+ dùng được cho **ảnh tĩnh làm tấm nền timelapse** (OpenAI sửa ảnh KHÔNG mặt nạ → ghép lại lớp (a) theo mặt nạ ID → khớp màu → bộ kiểm 2 mô hình + máy), **không dùng được cho video Omni** (0/8 lượt qua cổng: Omni đổi máy, đổi đất↔nước, bịa lửa/nhà/tàu ngay cả khi lệnh cấm; ghép lớp (a) không cứu được vì vùng (c) đã sai hình học).

| Việc | Kết quả đo |
|---|---|
| 1. Luật N2+ T4 | `reports/nc-n2p/LUAT-N2P-T4.md`: (a) 27 mục ranh cháy theo ngày + công trình có tên + mốc tồn tại (Monument 1671–1677, St Paul's Wren 6/1675 → 26/10/1708 → 25/12/1711, tháp tây Westminster Abbey 1740s, Globe dỡ 1644–45, Old St Paul's KHÔNG có chóp từ 1561…); (b) 41 vật minh hoạ (18 đứng yên / 20 chuyển động / 3 điều kiện nền) — **câu trích khớp nguyên văn 27/27 và 41/41 bằng máy**, đọc lượt 2 bằng gpt-6.1-sol + P phân xử; (c) danh sách CẤM 33 dòng; (d) trần đề xuất; (e) chính sách YouTube đọc lại 21/10/2026. Thêm 3 điều luật từ số đo: **B1 (c) tự do bề mặt, KHÔNG tự do hình học**; B2 vật gắn ranh lửa thuộc (a); B3 người luôn là "chuyển động" trên tấm tĩnh. |
| 2. Bộ kiểm N2+ + kiểm có đáp án | `ma/kiem_n2p.py` (máy + 2 mô hình nhìn + q_thoi_dai.py của K). Khung thử chèn cố ý 3 lỗi thời đại + 2 vật lớp (a) + 1 người: **gpt-6.1-sol 6/6, claude-sonnet-5-5 6/6, hợp 6/6; q_thoi_dai.py 3/3 lỗi thời đại**; đối chứng render↔render: **0 báo** ở cả hai mô hình. |
| 3. O1 ảnh tĩnh (OpenAI) | Lượt 1 **gửi mặt nạ**: gpt-image VẼ LẠI HÌNH HỌC (núi đổi dáng, đồng bằng thành biển, T9b 8,7–24,3 %) → **0/6**. Lượt 2 **không mặt nạ**: giữ hình học (T9b ≤ 1,6 %) → **2/6 qua**; lượt 3 (sửa lệnh, bỏ chữ "terraces" đã gợi AI xây tường đá) → **5/6 qua sau ≤ 2 lần làm lại**; 1/6 trượt (thêm gia súc trên tấm tĩnh). Lớp (a) sau ghép lệch **0/255** ở mọi ảnh. Khớp màu làm lệch nền↔vật render giảm từ ΔE ≈ 9–16 xuống **3,2–7,1**. Thử timelapse 12 s máy cố định 2 mốc: nhấp nháy ngoài hoà **0,006 mức xám/khung**, bước nhảy chuyển tấm **0,54 ΔE (hoà 2 s)** so với **11,8 ΔE (cắt cứng)**. |
| 4. Omni (Gemini) | Bước 0 QUA (`gemini-omni-1.1-flash`; `gemini-omni-flash-preview` tắt 22/10/2026). 8 lượt có đầu ra (c1 ×3, c4B ×3, c2 ×2) + 1 lượt c4A cho thử nối: **0/8 qua**; làm lại 1 lần/clip (lệnh "RESTYLE ONLY") ở c1, c4B không hết lỗi → dừng ở 1 (lý do §4.3). Đường nối c4 sau ghép **ΔE 14,7 = 21,5 × nền** (Omni thô 16,8 = 47,7 ×). C2PA `trainedAlgorithmicMedia` + SynthID 9/9 tệp ra. |
| 5. Ước T4 ≈ 12 phút | O1 ≈ 84 tấm (ước) × ≈ 2,8 lượt/tấm đạt × ≈ $0,33/lượt ≈ **$78 ± 30** + ≈ 4 h người đọc tờ so; mặt nạ ID mọi khung O1 ≈ **22 h CPU** ở 1080p (đo 9,2 s/khung) — cần lượt mặt nạ 1 lần dựng (việc kỹ thuật cho G0). Omni: **0 %** thời lượng. |
| Chi phí thật | OpenAI **$5,77** (ảnh $2,07 + chữ/nhìn $3,71; vượt mốc $5 — lợi ích dưới) · Gemini **$9,92** (dưới mốc $12) · Claude **$8,37** (nhìn $6,95 + q_thoi_dai $1,42; vượt mốc $8 — lợi ích dưới) · RunPod/Runway/ElevenLabs/YouTube 0. Không chạm chặn an toàn. |

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| **N2P-D1** | **Duyệt N2+ cho T4 ở dạng "tấm nền AI tĩnh + lớp (a) và lớp sống từ render"** cho shot timelapse máy cố định (TL-1): OpenAI sửa ảnh KHÔNG mặt nạ → ghép (a) (bảo vệ = mặt nạ (a) nở 1 px, vật nhỏ nở 3 px, viền mềm 3 px) → khớp màu Reinhard trên lớp (c) → bộ kiểm → người đọc tờ so | Ảnh "thật" hơn rõ (tờ so); lớp (a) giữ 0/255; vật chuyển động vẫn từ render nên không đóng băng; nhấp nháy ≈ 0; ≈ $0,9/tấm đạt | Mỗi tấm chỉ đúng cho một (điểm máy × mốc × trạng thái sáng); 1/6 trượt sau 2 lần làm lại; mặt nạ mọi khung tốn CPU | Thêm bước "tấm AI" + "ghép" vào G0 (§5) | AI vẽ tường/lối mòn/đá ngầm (đã gặp) → luật B1 + lệnh cấm cụ thể + bộ kiểm |
| **N2P-D2** | **Không dùng Omni (video→video) ở T4 (0 % thời lượng)** | Tránh dữ kiện bịa (lửa, nhà, tàu, đổi máy) trong phim lịch sử | Mất "chuyển động thật" kiểu video AI | Không | Đối thủ dùng video AI → bù bằng D1 |
| **N2P-D3** | Thêm vào luật N2+: **B1** (c) chỉ tự do bề mặt — đường bờ, chân trời, dáng núi, mặt nước là dữ kiện địa lý; **B2** vật/biến cố gắn ranh lửa theo ngày là (a); **B3** người luôn "chuyển động" trên tấm tĩnh | Khớp đúng 3 kiểu lỗi đo được | Thêm điều luật | Kinh thánh §15 (nháp §6.3) | — |
| **N2P-D4** | Giao phiên K đưa bộ kiểm vào `checks/`: `kiem_n2p.py` + `vision_kiem.py` (2 mô hình, đề bài cố định, `cam_thoi_dai.json`) + T9b + `cham_dap_an.py` + khung thử có đáp án | Đã có đáp án 6/6 mỗi mô hình, đối chứng 0 báo | Mô hình báo dư (gắn "thời đại sai" cho vật bịa không lỗi thời đại; báo "lối mòn" là công trình) → cần người đọc | `checks/` (K) | Thứ tự ngẫu nhiên của mô hình: số vật báo thay đổi giữa các lần chạy |
| **N2P-D5** | Trần T4: O1 ≤ 50 % thời lượng, Omni 0 %, tổng AI ≤ 50 %; chuyển tấm chỉ bằng hoà ≥ 2 s | Có số đo | Thấp hơn mức "nền N1 cả tập" (M4) | §14.1 d/g | — |
| N2P-D6 | Nếu muốn thử video tiếp (chỉ tài liệu): **NVIDIA Cosmos-Transfer2.5** (có kênh điều khiển PHÂN VÙNG — đúng thứ Omni/Wan thiếu, NC-V2V3 §1b; cần chủ dự án chấp nhận giấy phép NVIDIA trên HF + token riêng cho pod). Không đề xuất Veo 3.1 (tài liệu Gemini 19/10/2026: preview tắt 22/10/2026, không có sửa video tải lên/mặt nạ) | Đóng câu hỏi "mô hình khác" | Cơ chế lỗi (vùng AI vẽ được = vùng có thể đổi hình học) không phụ thuộc mô hình | Chỉ nghiên cứu, GPU thuê | Tốn tiền cho câu hỏi gần như đã có đáp án |
| N2P-D7 | Bài học (phiên P ghi BAI-HOC): (a) gpt-image **có mặt nạ** vẽ lại hình học, **không mặt nạ** giữ hình học; (b) chữ trong lệnh ("terraces", "plots") gợi AI xây vật lớp (a); (c) mặt nạ V7C xếp cây instanced vào "nước"; mặt nạ "trại" gồm cả nền đất trại → mảng phẳng lộ khi ghép; (d) `omni.py` NC-V2V nhận nhầm VIDEO VÀO làm đầu ra khi tương tác treo `in_progress` 1 h (c2-manh lần 1); (e) T9 gốc báo nhầm loé nắng → T9b | Tránh lặp | — | BAI-HOC | — |

**Xem nhanh:** `reports/nc-n2p/to-so/to-so-o1-*.png` (render | AI | AI+ghép; hàng dưới = lượt có mặt nạ), `clip/so-timelapse.mp4`, `clip/so-c1.mp4`, `clip/so-c4B.mp4`, `clip/so-c2.mp4`, `clip/so-c4-noi.mp4` (render | Omni | Omni+ghép), `kiem/dap-an/khung-thu-dap-an.jpg`.

## §1. Luật N2+ cho T4 London 1666 — `reports/nc-n2p/LUAT-N2P-T4.md`

- **(a) lớp dữ kiện:** 27 mục, 4 nhóm: ranh cháy theo ngày (a01–a16; nguồn chính: *A True and Exact Relation … 1666*, EEBO-TCP A63370 — danh sách điểm dừng lửa đêm 4→5/9 và đám cháy lại ở Inner Temple đêm 5/9; Pepys; Evelyn), công trình có tên + trạng thái theo ngày (St Paul's, Royal Exchange, Tower, London Bridge + khoảng trống 1633, All Hallows Barking, Clothworkers' Hall, Guildhall…), **mốc tồn tại CẤM** trong khung 1666 (Monument, St Paul's của Wren, tháp tây Westminster Abbey, Globe, Royal Exchange 1669/1844) có URL + ngày đọc, gió/thời tiết, chữ/số. Lịch Julius: 2/9/1666 J. = 12/9 G. — dùng ngày Gregory khi tính mặt trời/trăng. **Vị trí chỉ từ bậc 1** (Hollar 1666, Ogilby & Morgan 1676); ranh nội suy giữa hai nơi có tên = bậc 5.
- **(b) vật minh hoạ:** 18 ĐỨNG YÊN (lều/chòi ngoài thành, đống đồ, thùng đường vỡ, hố chôn đồ, đồ chất trong nhà thờ/Westminster Hall, gạch đá vụn, móc kéo nhà…), 20 CHUYỂN ĐỘNG (sà lan, thuyền, đồ trôi sông, xe, người khiêng, bồ câu, lính…), 3 điều kiện nền (trăng sáng 2/9, gió đông, trời màu lửa). Mỗi mục có câu trích nguyên văn + mục ngày + dòng + SHA tệp. Gutenberg không có số trang in → vị trí = mục ngày + dòng (như NC-AI §7.2).
- **(c) CẤM:** 11 nhóm chung (trước 1850) + 12 riêng 1666 + 10 loại AI đã bịa — đưa nguyên văn vào đề bài bộ soi.
- **(d), (e):** §5 và §6 của tệp luật; tóm tắt ở §5 và §6.2 dưới.

## §2. Bộ kiểm N2+ (`reports/nc-n2p/ma/`) + kiểm có đáp án

| Phép | Cách đo | Ngưỡng |
|---|---|---|
| (i) lớp (a) sau ghép | max \|ghép − render\| trong mặt nạ (a); dải 20 px quanh (a): cụm ΔE ≥ 30 ≥ 80 px (cho người đọc); hai mô hình liệt kê vật THÊM/BỚT/ĐỔI loại (a) (cờ, công trình, công sự, tàu lớn, chữ, đèn, lửa lớn) — ở bất kỳ đâu = LỖI, ghi "dải (a)" | 0/255; 0 vật |
| (ii) lỗi thời đại | 2 mô hình nhìn khác nhau (gpt-6.1-sol Responses; claude-sonnet-5-5 `claude -p`), cùng đề bài + 5 ảnh trước/sau (toàn khung + 4 ô phóng 1,5×) + danh sách CẤM; LỖI khi mô hình nêu năm xuất hiện > năm khung (hoặc máy bay/xe máy ở cảnh < 1900); không kèm năm → "nghi vấn" cho người; + `checks/ll/q_thoi_dai.py` (K) | 0 |
| (iii) đổi loại vùng | T9 NC-V2V3 (màu nước HSV theo mặt nạ) + **T9b** (bỏ loé nắng V ≥ 0,85 & S ≤ 0,25 và dải 8 px quanh bờ) + mô hình báo đổi đất↔nước | ≤ 2 % mỗi chiều; 0 báo |
| (iv) đóng băng (ảnh tĩnh) | vật THÊM loại chuyển động (người, động vật, chim, thuyền nhỏ, xe chạy, khói, lửa trại, máy bay, xe máy) | 0 |
| (v) nhấp nháy + đường nối | `do_v2v.py` (NC-V2V T1–T6) + `do_them3.py` (NC-V2V3 T7–T9) gọi nguyên mã, đối chứng = đường ghép áp lên chính nguồn; `noi.py` cho đường nối | ≤ 1,5 × đối chứng |

**Kiểm có đáp án** (`kiem/dap-an/`): khung thử = render cổng "cang" (cách A) + 6 vật chèn bằng gpt-image, chỉ dán trong hộp và ngoài lớp (a): L1 máy bay, L2 ô tô, L3 cột điện cao thế (thời đại); L4 tàu chiến 3 cột buồm trên vùng nước trống, L5 cột cờ đỏ trắng trong dải 20 px quanh công sự (lớp a); L6 người đi trên bãi cỏ (đóng băng).

| | L1 | L2 | L3 | L4 | L5 | L6 | Bắt | Báo trên đối chứng sạch |
|---|---|---|---|---|---|---|---|---|
| gpt-6.1-sol | ✓ | ✓ | ✓* | ✓ | ✓ (dải a) | ✓ | **6/6** | 0 |
| claude-sonnet-5-5 | ✓ | ✓ | ✓ | ✓ | ✓ (dải a) | ✓ | **6/6** | 0 |
| q_thoi_dai.py (K) | ✓ | ✓ | ✓ | — | — | — | 3/3 thời đại | — |

\* L3 với gpt: mô hình báo cột điện nhưng KHÔNG kèm năm → theo luật cuối là "nghi vấn"; hộp L2/L3 chồng nhau nên bộ chấm tính trúng nhờ báo ô tô (năm 1886). Theo luật chặt: gpt 2/3 thời đại có năm + 1 nghi vấn; claude 3/3. Thêm: gpt tự phát hiện **cờ Union kiểu 1801** trên tàu AI chèn (lỗi thời đại thật do AI tạo, không nằm trong đáp án). Chi phí một khung: gpt ≈ $0,04–0,07, claude ≈ $0,13–0,15, q_thoi_dai ≈ $0,04.

**Giới hạn đã đo của bộ kiểm:** (1) mô hình gắn "thời đại sai" cho vật bịa nhưng đúng thời kỳ (vd. thùng gỗ, đá ven bờ) → đã sửa luật (cần năm); (2) với cảnh 2026, danh sách CẤM "trước 1850" làm claude gắn ô tô là lỗi → nay chỉ đưa danh sách đó khi năm < 1850; (3) số vật báo khác nhau giữa các lần chạy (tl-moc2: lượt đầu báo "mất cờ", lượt sau với mã ghép bảo vệ vật nhỏ thì báo "lối mòn bị xoá"); (4) q_thoi_dai.py báo nhầm cờ Union 1707 của render là 1801 (giới hạn đã biết của K: cờ ~20 px). ⇒ bộ kiểm là lưới lọc; người đọc tờ so vẫn bắt buộc (§11.3).

## §3. Kết quả O1 — ảnh tĩnh (OpenAI `gpt-image-2.5-sunburst-2026-09-08`, `POST /v1/images/edits`, 2560×1440, quality high)

**Khung:** 3 khung cổng cách A có sẵn (`reports/nc-cpu/khung/A/cong-{cang,vay-ham,toan-canh}.jpg`; năm 1780 / 1779 / 1781). Mặt nạ ID dựng lại bằng `design/k2v/v7c/do_bocuc.js` + `idmask_v7c.js` cùng máy (1920×1080, khớp hình học với ảnh A — `o1/mat-na/`). Lệnh nguyên văn: `o1/lenh/*.txt`; sổ AI mọi lệnh: `so-ai.jsonl` (model gửi/nhận, ngày, lệnh nguyên văn, SHA vào/ra, % mặt nạ được sửa, usage, $, C2PA đọc từ tệp — **27/27 tệp ra có C2PA `trainedAlgorithmicMedia`**; gốc mẫu `o1/openai-goc-vay-ham-vua-l2.jpg`).

| Khung · mức | Lượt 1 (gửi mặt nạ) T9b đất→nước / nước→đất % | Lượt 2 (không mặt nạ) | Lượt 3 (lệnh sửa) | Kết luận máy + mô hình | Lệch viền nền↔vật (ΔE trung vị) |
|---|---|---|---|---|---|
| cang · vừa | 8,69 / 3,69 → LOẠI | gpt báo vịnh nhỏ cắt vào bờ → LOẠI | **ĐẠT** | ĐẠT ở lần 3 | 5,07 |
| cang · mạnh | 23,37 / 2,85 → LOẠI | tường đá ruộng bậc thang (a) + đá lấn biển → LOẠI | gia súc trên tấm tĩnh (iv, gpt) → LOẠI | **LOẠI sau 2 lần làm lại** | 3,19 |
| vay-ham · vừa | 24,27 / 18,75 → LOẠI | **ĐẠT** (4 nghi vấn không năm: thùng, chòi củi) | — | ĐẠT ở lần 2 | 6,43 |
| vay-ham · mạnh | 17,45 / 6,71 → LOẠI | **ĐẠT** | — | ĐẠT ở lần 2 | 6,44 |
| toan-canh · vừa | 14,64 / 10,54 → LOẠI | tường đá (a, 5) + đá ngầm thành đảo (iii) → LOẠI | **ĐẠT** | ĐẠT ở lần 3 | 3,62 |
| toan-canh · mạnh | 16,44 / 13,17 → LOẠI | tường đá + lối mòn (a, 9) → LOẠI | **ĐẠT** | ĐẠT ở lần 3 | 5,10 |

(Bảng đầy đủ: `kiem/o1/BANG-O1.txt`, JSON từng ảnh `kiem/o1/*-kiem.json`, trả lời nguyên văn mô hình `*.raw.txt`; tờ so `to-so/to-so-o1-*.png`.) Lớp (a) sau ghép: **max lệch 0/255 ở 20/20 ảnh**. Tỷ lệ điểm ảnh do AI (vùng (c)): cang 89 %, vay-ham 80 %, toan-canh 76 %.

**Đọc kết quả:**
- **Mặt nạ làm hỏng:** với mặt nạ, gpt-image vẽ lại cả khung với máy/địa lý khác (núi Rock thành vách cao, đồng bằng eo đất thành biển) — đúng kiểu lỗi "đổi loại vùng" NC-V2V3 §4b. Không mặt nạ thì giữ hình học tốt (T9b ≤ 1,6 % ở 14/14 ảnh lượt 2–3 (gồm 4 tấm timelapse)). Vì ta ghép lại (a) nên không cần mặt nạ để bảo vệ (a).
- **Lệnh gợi vật:** chữ "terraced garden plots", "dry-stone terraces" trong lệnh lượt 2 làm AI xây tường đá (lớp a) ở 3/6 ảnh; lượt 3 bỏ chữ đó + cấm cụ thể → hết tường. ⇒ danh mục (b) cho lệnh phải là vật đứng yên CỤ THỂ từ bảng §3 luật, không danh từ địa hình nhân tạo.
- **Đóng băng:** AI thêm xe có ngựa (tl-moc1 lượt 2) và gia súc (cang-mạnh lượt 3) dù lệnh cấm động vật → (iv) bắt được.
- **Màu:** AI đổi giờ/ánh sáng (vàng chiều) dù lệnh giữ; khớp màu Reinhard một bộ hệ số trên lớp (c) đưa lệch viền về 3,2–7,1 ΔE (trước 9–16).

### §3.1 Thử timelapse 12 s ở một điểm máy cố định qua 2 mốc — `clip/so-timelapse.mp4`, `tl/do-timelapse.json`

- Cảnh: C1-a V7B (trại vây hãm 1779), máy cố định tại khoá đầu ([−1200, 215, 3560] → [−1300, 0, 2900], fov 44), giây 6–18 (21/6 → ≈ 9/1779, trại mọc dần). 288 khung 1280×720 + mặt nạ ID từng khung.
- Tấm nền AI: mốc 1 = khung 168 (1/7/1779, chưa có trại), mốc 2 = khung 408 (18/9/1779, trại 18 % khung); lượt 3 (lượt 2 trượt: xe ngựa; lối mòn). Bộ kiểm tấm lượt 3: (ii)(iii)(iv) ĐẠT; (i) gpt báo "lối mòn của render bị xoá" (1 mục/tấm) → **LOẠI theo máy**; P đọc: lối mòn nằm ở lớp "đất bằng" của mặt nạ (không phải đường chính) — **chủ dự án quyết** lối mòn là (a) hay (c) (§9).
- Ghép: nền = hoà mờ tấm 1 → tấm 2 trong khung 264–312 (2 s); lớp (a) + mọi vật chuyển động (người, đơn vị, chim, cờ) từ render từng khung.

| Đo | Hoà 2 s | Cắt cứng (so) |
|---|---|---|
| Nhấp nháy vùng tĩnh lớp (c), ngoài cửa sổ hoà (TB \|Δ xám\|/khung; render = 0,000) | **0,006** | 0,006 |
| Bước nhảy chuyển tấm: max ΔE khung kề trên lớp (c) (trung vị cả clip) | **0,54** (0,009) — 60 × | **11,83** (0,007) — 1 817 × |
| Khớp ánh sáng nền ↔ vật render: ΔE vòng ngoài vật (trung vị · p90 max) | 4,76 · 14,15 | 4,83 · 14,15 |

- **Thấy trên clip:** nền phẳng của trại (mặt nạ "trại" gồm cả nền đất trại) hiện thành mảng vàng phẳng trên đất AI có vân → phải tách "lều" khỏi "nền trại" trong mặt nạ trước khi dùng (BAI-HOC D7c). Nước AI xanh lam đậm hơn render.

## §4. Kết quả Omni — Gemini `gemini-omni-1.1-flash` (Interactions API, chạy nền)

**Bước 0** (21/10/2026 04:25 UTC): `GET /v1beta/models` → 200; có `gemini-omni-1.1-flash` và `gemini-omni-flash-preview` (theo trang giá, bản preview **tắt 22/10/2026**) → chọn 1.1. Tài liệu đọc 21/10/2026: <https://ai.google.dev/gemini-api/docs/omni> (sửa/nối video tải lên ≤ 10 s; 720p mặc định, 1080p/4K là phóng; *"Editing or extending uploaded videos is not currently available for users in the European Economic Area"* (cả Thuỵ Sĩ, Anh); *"All generated videos include SynthID watermarking, which is invisible to viewers"*; không có mặt nạ/sửa theo vùng), <https://ai.google.dev/gemini-api/docs/pricing> (*Last updated 2026-10-19 UTC*: vào $1,50/1M; ra video $17,50/1M, *"calculated at a rate of 5,792 tokens per second of 720p video"*; không ghi giá 1080p/4K).

**Điều khoản đầu ra** (<https://ai.google.dev/gemini-api/terms>, *Last updated 2026-04-28 UTC*, đọc 21/10/2026): *"Google won't claim ownership over that content."*; *"You acknowledge that Google may generate the same or similar content for others and that we reserve all rights to do so."*; *"You're responsible for your use of generated content…"*; dịch vụ trả tiền: *"Google doesn't use your prompts … or responses to improve our products"*. Không có câu cấm dùng thương mại; dịch vụ dành cho *"professional or business purposes"*. ⇒ được dùng thương mại, không độc quyền đầu ra.

**Clip nguồn** dựng lại bằng mã có sẵn (tệp NC-V2V đã mất theo container): opt `reports/nc-v2v/clips-opt.json`, `do_bocuc.js` V7C (tắt `opt.nc` = V7B bit-giống), 1280×720 spp 1, mỗi khung kèm mặt nạ ID: c1 (H2 giây 11–21, 13/9/1782 sáng → đêm), c4B (C1-a giây 10–20, trại 1779), c2 (H3 máy D 2026), c4A (C1-a giây 0–10, cho thử nối). SHA nguồn: `omni/c2pa-dau-ra.json` (ra) và sổ `so-ai-gemini.jsonl` (vào). Lệnh nguyên văn `omni/lenh/*.txt` (vừa/mạnh theo N2+: thêm đời sống thời kỳ, cấm lửa/nhà/tàu lớn/cờ/chữ mới, cấm đổi đất↔nước).

| Biến thể | (i) max lệch (a) trước mã hoá | (i) vật lớp (a) THÊM/ĐỔI (3 khung; gpt ∪ claude) | (ii) thời đại có năm · nghi vấn · q_thoi_dai | (iii) T9 cả clip đất→nước · nước→đất % (đối chứng) | (iii) T9b 3 khung max % · mô hình báo | T7 đốm sáng bền ≥ 1 s (màu lửa) · đc | T8 vật mới bền · đc | Nhấp nháy ÷ nguồn (đc) | Máy |
|---|---|---|---|---|---|---|---|---|---|
| c1-vừa | 0 | 44 (công trình, lửa lớn, tàu) | 0 · 83 · 2 | 11,15 · 4,72 (1,29 · 0,98) | 31,20 · 26 | 11 (10) · 0 | 2 · 0 | 4,70 (1,84) | LOẠI |
| c1-mạnh | 0 | 46 (cờ, công trình, lửa lớn, tàu) | 0 · 56 · 0 | 44,6 · 6,11 | 55,87 · 27 | 45 (28) · 0 | 27 · 0 | 5,05 (1,84) | LOẠI |
| c1-vừa làm lại 1 | 0 | 36 (công trình, lửa lớn, tàu) | 0 · 57 · 1 | 24,22 · 5,44 | 26,45 · 14 | 84 (45) · 0 | 34 · 0 | 5,84 (1,84) | LOẠI |
| c4B-vừa | 0 | 114 (cờ, công sự, công trình, tàu) | 0 · 80 · 0 | 17,82 · 36,21 (0,01 · 0,18) | 23,91 · 23 | 88 (50) · 1 | 38 · 0 | 1,96 (2,05) | LOẠI |
| c4B-mạnh | 0 | 74 (chữ, cờ, công sự, công trình, tàu) | 0 · 96 · 0 | 3,9 · 74,25 | 52,93 · 20 | 86 (59) · 1 | 55 · 0 | 12,8 (2,05) | LOẠI |
| c4B-vừa làm lại 1 | 0 | 56 (công sự, công trình, tàu) | 0 · 28 · 0 | 1,74 · 31,42 | 9,49 · 1 | 97 (67) · 1 | 22 · 0 | 2,47 (2,05) | LOẠI |
| c2-vừa (2026) | 0 | 12 (công trình, đèn, tàu) | 0 · 15 · 0 | 6,22 · 3,79 (0,34 · 0,27) | 1,98 · 10 | 6 (0) · 3 | 11 · 0 | 1,62 (1,99) | LOẠI |
| c2-mạnh (2026) | 0 | 52 (công trình, đèn, lửa lớn, tàu) | 0 · 35 · 0 | 7,55 · 7,61 | 3,78 · 8 | 27 (5) · 3 | 10 · 0 | 2,07 (1,99) | LOẠI |

(`omni/BANG-OMNI.md`, `omni/tong-hop.json`, số thô `omni/do/`, khung mẫu `omni/kiem/`. "max lệch (a)" đo trước mã hoá H.264; khung mẫu sau mã hoá lệch 33–55/255 do nén, không do AI. T1/T2 của `do_v2v.py` trên bản ghép bị méo do căn ECC theo nền AI đã đổi — không dùng.)

### §4.1 Đọc khung (P) — `clip/so-c1.mp4`, `so-c4B.mp4`, `so-c2.mp4`
- **c1:** Omni thêm **lửa cháy trong phố, cột khói, nổ trên mặt nước** ở cả 3 lượt (kể cả lượt "RESTYLE ONLY … do not add any fire"); sau ghép, lửa trên mái bị thay bằng render nhưng **quầng lửa trên quảng trường/bãi cỏ (lớp c) và trên mặt nước vẫn còn**; c1-mạnh còn đổi đêm thành ngày ở một đoạn và dựng nhà đá mới ở tiền cảnh.
- **c4B:** vừa/mạnh **đổi góc máy** (mạnh dựng hẳn một cảnh mới: núi Rock gần, trại lều trắng kiểu khác, ngựa, tàu buồm) → bản ghép là hai hình học chồng nhau; làm lại 1 giữ máy gần đúng nhưng **thay hai dãy trại bằng trang trại có nhà gỗ, hàng rào**, nước→đất 31 %.
- **c2 (2026):** ít lỗi nhất nhưng vẫn thêm cột đèn, vạch qua đường, tàu nhỏ ở xa, xoá lối bậc trên sườn Rock (lớp a) → LOẠI.
- Lỗi thời đại có năm: **0** ở mọi lượt (Omni bịa vật đúng thời kỳ, không lỗi thời đại) → điều kiện "làm lại khi bắt được lỗi thời đại" của lệnh **không kích hoạt**; phiên vẫn làm lại 1 lần cho c1 và c4B vì lỗi (i)/(iii) nặng hơn, không làm lần 2 vì lần 1 không giảm loại lỗi (c1: 44 → 36 vật (a), T7 lửa tăng 10 → 45; c4B: T9 nước→đất 36 → 31 %). **Tỷ lệ làm lại đo được: 8/8 lượt LOẠI (100 %); 2/2 lượt làm lại LOẠI.**

### §4.2 Thử nối 20 s (c4A + c4B, cùng lệnh làm lại 1) — `clip/so-c4-noi.mp4`, `omni/do/noi-*.json`

| | ΔE tại nối (khung 239 → 240) | Nguồn cùng chỗ | ΔE nền trung vị | Tỉ số nối/nền | Chi tiết B/A (nguồn) |
|---|---|---|---|---|---|
| Omni thô | 16,84 | 1,31 | 0,35 | **47,7** | 0,795 (1,007) |
| Omni + ghép (a) + khớp màu | 14,69 | 1,31 | 0,68 | **21,5** | 0,836 (1,007) |

Ghép lớp (a) + khớp màu giảm bước nhảy ≈ 13 % nhưng nối **vẫn thấy rõ** (> 3 × nền). Cùng hướng NC-V2V (28–65 × nền).

### §4.3 Sự cố và C2PA/SynthID
- **c2-mạnh lần 1:** tương tác treo `in_progress` 3 611 s; `omni.py` (NC-V2V) lấy video cuối trong `steps` = **chính video vào** (SHA trùng `c2-nguon.mp4`) và ghi như đầu ra. GET sau đó: *"There was a problem processing your request. You will not be charged."* → bỏ, ghi dòng hiệu chỉnh trong sổ; gọi lại lần 2 thành công ($1,10). Đề nghị sửa `omni.py`: chỉ nhận video ở bước `model_output` và dừng khi quá 10 phút.
- **9/9 tệp ra Omni có manifest C2PA `trainedAlgorithmicMedia` + chuỗi SynthID trong manifest** (`omni/c2pa-dau-ra.json`). Mã hoá lại (ghép) làm mất C2PA; SynthID theo tài liệu nằm trong điểm ảnh.

## §5. Ước T4 London 1666 (≈ 12 phút = 720 s) — mọi số dưới là **(ước)** từ số đo phiên này

| Khoản | Cách tính | Kết quả |
|---|---|---|
| Phần thời lượng mỗi cách | O1 (tấm nền AI + render) cho shot TL-1 máy cao cố định: ≤ 50 % (≈ 360 s, D5); Omni: 0 %; phần còn lại: cách A/Cycles như G0 | O1 ≈ 360 s; Omni 0 s |
| Số tấm O1 | 7 điểm máy × ≈ 6 mốc dùng/điểm (1/9 trước cháy; 2/9 ngày, đêm; 3/9; 4/9; 5/9; 7/9 phế tích; chọn theo lời) × ≈ 2 trạng thái sáng (ngày / đêm lửa — đêm lấy từ lượt chiếu sáng A, §11.3) | **≈ 84 tấm** |
| Lượt/tấm đạt | đo: 14 lượt (không mặt nạ) → 5 đạt trên 8 mục tiêu (5/6 ảnh O1 + 0/2 tấm timelapse chờ quyết "lối mòn") → **≈ 2,8 lượt/tấm đạt**; nếu chủ dự án coi lối mòn là (c): ≈ 2,0 | ≈ 170–235 lượt |
| Chi phí/lượt | ảnh $0,077 + gpt $0,04–0,07 + claude $0,13–0,15 + q_thoi_dai $0,04 | ≈ $0,30–0,33 |
| **Chi phí O1** | 170–235 × $0,33 | **≈ $56–78** (+ dư 30 % làm lại do người đọc ⇒ ≈ $75–100) |
| Giờ người | đọc tờ so ≈ 3 phút/tấm (84 tấm) + duyệt lối mòn/vật bậc 5 | ≈ 4–5 h |
| Giờ máy — mặt nạ ID | mọi khung O1 phải có mặt nạ để ghép (a) + vật chuyển động: 360 s × 24 = 8 640 khung × **9,2 s/khung** (đo 1080p, mặt nạ không kèm màu) | **≈ 22 h CPU** (≈ 11 h đồng hồ 2 làn) |
| Giờ máy — tấm + ghép + kiểm | dựng khung nguồn của tấm (cách A 1080p ≈ 15–25 s) + ghép ≈ 0,3 s/khung + API chạy song song (≈ 35 s ảnh + ≈ 50 s kiểm/lượt) | ≈ 1 h CPU + ≈ 3–5 h đồng hồ API |
| Omni (nếu vẫn ép dùng 10 %, 72 s) | 7–8 đoạn × $1,10 × ≥ 5 lượt (0 % đạt — không hội tụ) | ≥ $40, không bảo đảm đoạn nào đạt — **không đề xuất** |

**Tác động tới đường dựng G0 (§14.2):** thêm 4 bước sau "dựng cách A": (1) **lượt mặt nạ ID mọi khung** shot O1 — chi phí lớn nhất; nên viết lượt ID **một lần dựng** (MRT/ID theo vật) thay ~10 lượt hiện nay (việc kỹ thuật, chưa đo — ước giảm ≥ 5×); tách "lều" khỏi "nền trại", "cây" khỏi "nước" trong mặt nạ; (2) **tấm AI** cho mỗi (điểm máy × mốc × trạng thái sáng) từ khung cách A 1080p; (3) **ghép** (bảo vệ (a), khớp màu, hoà tấm ≥ 2 s); (4) **bộ kiểm** + người đọc tờ so trước G2. Vùng (c) của shot O1 vẫn phải dựng (ánh sáng/đổ bóng cho vật (a)) nhưng có thể ở mức nháp.

## §6. Đề xuất

### §6.1 Bảng cách × chỉ số (KHÔNG chấm "đẹp" — chủ dự án xem tờ so/clip)

| Cách | (i) lớp (a) sau ghép | Lỗi thời đại (có năm) | Đổi vùng (T9b) | Đóng băng | Nhấp nháy / nối | Tỷ lệ làm lại | Chi phí đo |
|---|---|---|---|---|---|---|---|
| O1 có mặt nạ (lượt 1) | 0/255; | 0 | **8,7–24,3 %** → 6/6 LOẠI | — | — | 6/6 | $0,077/ảnh |
| **O1 không mặt nạ + ghép + khớp màu** | 0/255; vật (a) mới: tường đá/lối mòn ở 3/6 lượt 2 → 0/4 lượt 3 | 0 | ≤ 1,6 % | 2 lần (xe ngựa, gia súc) | timelapse: 0,006 xám/khung; chuyển tấm hoà 0,54 ΔE | **4/6 cần làm lại; 5/6 đạt sau ≤ 2 lần** | ≈ $0,33/lượt kể cả kiểm |
| Omni + ghép | 0/255 nhưng 12–114 vật (a) bịa/đổi ở vùng (c) mỗi biến thể | 0 | 2–56 % | (video) | nhấp nháy 1,6–12,8 × nguồn; nối 21,5 × nền | **8/8 LOẠI, làm lại không hội tụ** | $1,10/10 s + ≈ $0,6 kiểm |

### §6.2 Nếu Omni trượt — mô hình thử tiếp (chỉ tài liệu)
- **NVIDIA Cosmos-Transfer2.5** (điều khiển độ sâu + cạnh + **phân vùng**): là loại duy nhất trong các bản đã xem có kênh "đây là nước/đất" — lỗi chung của Omni, Wan VACE (NC-V2V3) và gpt-image có mặt nạ. Điều kiện: chủ dự án chấp nhận NVIDIA Open Model License trên HF + token đọc riêng cho pod (NC-V2V3 §1b, V2V3-D4). Kỳ vọng thấp vì vùng AI được vẽ vẫn có thể bịa vật (NC-V2V3 B2).
- Không đề xuất Veo 3.1 (preview tắt 22/10/2026 theo <https://ai.google.dev/gemini-api/docs/video>, *Last updated 2026-10-19 UTC*; trang không có sửa video tải lên hay mặt nạ).
- Đường thay thế đã đo được ở phiên này: **video = tấm nền AI tĩnh + lớp sống render** (§3.1) — không cần mô hình video.

### §6.3 Nháp Kinh thánh §15 "N2+" (nguyên văn đề xuất)

> **§15. Luật AI N2+ (áp từ T4; chủ dự án duyệt …/10/2026).**
> (a) Ba lớp. **LỚP DỮ KIỆN CÂU CHUYỆN — khoá:** vật mang câu chuyện/nhịp kể (cờ, công trình có tên, ranh giới/ranh đám cháy theo ngày, tàu/vật được lời nhắc tới, đường sá chính, năm/ngày, chữ, số) **và hình học địa lý** (đường bờ, chân trời, dáng núi/đồi có tên, vị trí mặt nước); vật/biến cố gắn trực tiếp với ranh lửa của ngày đó (lửa lớn, cột khói, nổ nhà chặn lửa). AI không được thêm/xoá/đổi; ghép lại điểm ảnh render theo mặt nạ ID (sai khác < 1/255; vùng bảo vệ = mặt nạ nở 1 px, vật < 60 px nở 3 px; viền mềm ≤ 3 px); cấm đổi loại vùng (đất ↔ nước). **LỚP CHI TIẾT MINH HOẠ — AI được thêm/đổi:** người, đám đông, lều, lửa trại, khói, đồ đạc, thuyền nhỏ, xe, gia súc, cây, quần áo phơi… nếu đúng thời kỳ (bảng vật của tập, nguồn bậc 2–5 §12.2), không trái hoàn cảnh có nguồn, không lỗi thời đại, không chữ; trên **ảnh tĩnh** chỉ vật đứng yên trong khoảng thời gian của tấm, **người và động vật luôn tính là chuyển động**. **LỚP NỀN — AI tự do về bề mặt** (vân đất, nước, trời, sương, ánh sáng), không tự do về hình học.
> (b) Cách dùng: **ảnh tĩnh** sửa KHÔNG gửi mặt nạ (mặt nạ làm mô hình vẽ lại hình học) rồi ghép lớp (a) + khớp màu về render trên lớp nền; lệnh chỉ nêu vật đứng yên cụ thể từ bảng vật, cấm tên vật lớp (a) (tường, ruộng bậc thang, lối, cầu, nhà…). **Video AI (video→video) không dùng** cho tới khi một mô hình qua cổng (c) với tỷ lệ làm lại ≤ 3 lượt/đoạn. Vật chuyển động và lớp dữ kiện luôn từ render từng khung; chuyển giữa hai tấm nền chỉ bằng hoà ≥ 2 s.
> (c) Cổng kiểm bắt buộc mọi khung N2+: (i) lớp (a) 0/255 + 0 vật (a) thêm/bớt/đổi; (ii) 0 lỗi thời đại có năm ở hai mô hình nhìn khác nhau + q_thoi_dai; (iii) đổi loại vùng T9b ≤ 2 % mỗi chiều và 0 báo của mô hình; (iv) 0 vật chuyển động trên tấm tĩnh; (v) nhấp nháy ≤ 1,5 × đối chứng, chuyển tấm ≤ 1 ΔE/khung; + người đọc tờ so. Bộ kiểm có khung thử đáp án; đổi mô hình/đề bài thì chạy lại đáp án.
> (d) Trần T4: tấm nền N2+ ≤ 50 % thời lượng, chỉ shot timelapse máy cố định; video AI 0 %; tổng khung có AI (N1 + N2 + N2+) ≤ 50 %; nâng ở tập sau khi bình luận chê AI ≤ 2 % (§11.3).
> (e) Công bố: bật "AI use = Yes" trên YouTube; thẻ phương pháp + mô tả ghi "illustrative detail (people, goods, boats, carts, textures) is AI-generated; the fire's extent by day, named buildings, dates and the river are from sources"; danh sách nguồn lớp (a) và (b) trong mô tả/bình luận ghim; sổ AI ghi mọi lệnh (model, lệnh nguyên văn, SHA vào/ra, % điểm ảnh AI, giá, C2PA/SynthID).

### §6.4 Việc gắn vào
- **Tiền kỳ T4:** chốt ranh từng ngày trên bậc 1 (Hollar 1666 / Ogilby & Morgan 1676) cho 15 điểm dừng (a11) và các nơi có tên theo ngày; bậc 3–4 trang phục 1660s (NC-AI §7.4: cổng bậc 3 London đang yếu) trước khi viết lệnh vật (b); chọn 6–8 điểm máy TL-1 và lập bảng (điểm × mốc × trạng thái sáng) để đếm tấm thật.
- **Phiên K:** đưa `kiem_n2p.py`, `vision_kiem.py`, `cam_thoi_dai.json`, T9b, `cham_dap_an.py` + khung thử đáp án vào `checks/` (bổ sung V2V-D4, V2V3-D2); quyết "lối mòn/đường phụ" thuộc (a) hay (c); sửa giới hạn cờ nhỏ của q_thoi_dai.
- **Phiên P:** ghi BAI-HOC theo N2P-D7; RIGHTS/AUTHORSHIP cho nguồn văn bản T4 (Gutenberg #4167, #42081 — PD Mỹ; EEBO-TCP A63370 — CC0) và các đầu ra AI (OpenAI, Gemini) nếu dùng; lượt mặt nạ ID một lần dựng vào G0.

## §7. Nguồn (URL + ngày đọc 21/10/2026)

| Nguồn | URL | Dùng cho | SHA-256 tệp (nếu tải) |
|---|---|---|---|
| Pepys, Diary vol. 45 (Braybrooke), Gutenberg #4167 | https://www.gutenberg.org/cache/epub/4167/pg4167.txt | (a), (b) bậc 2 | `8a7ec38ef2de9aff782077ac6e6127c2b83ecc78e4be22288f68ba43d4a3f918` (khớp NC-AI) |
| Evelyn, Diary vol. 2 (Bray), Gutenberg #42081 | https://www.gutenberg.org/cache/epub/42081/pg42081.txt | (a), (b) bậc 2 | `912a1791a66b5199d34101866d536c701ecf46e8bc4c1fe643e79492dbfd51cb` (khớp NC-AI) |
| *A True and Exact Relation … Fires … 1666* (EEBO-TCP A63370, EarlyPrint) | https://distantreader.org/stacks/earlyprint/txt/A63370.txt | ranh cháy theo ngày, chóp St Paul's 1561, cháy cầu 1633 | `1bf5c146dc3c80e4f4682042c2b002341bbf2ab1e493978511584ed3114162c8` |
| Wikipedia: Great Fire of London; Old St Paul's; St Paul's Cathedral; Westminster Abbey; Old London Bridge; Royal Exchange; Guildhall; Globe Theatre | en.wikipedia.org/wiki/… (đường dẫn đầy đủ trong `nguon/danh-muc-a.json`) | mốc tồn tại (thứ cấp) | — |
| The Monument — History | https://www.themonument.org.uk/history | Monument 1671–1677 | — |
| London Gazette số 85 (bản chép bên thứ ba) | https://freepages.rootsweb.com/~dutillieul/genealogy/ZOtherPapers/LGSept31666.html (403) — danh sách điểm dừng trùng A63370 | đối chiếu | chưa đối chiếu bản quét |
| YouTube — disclosing altered or synthetic content | https://support.google.com/youtube/answer/14328491 | (e) | — |
| YouTube — YPP policies (inauthentic content, mục 15/7/2025) | https://support.google.com/youtube/answer/1311392 | (e) | — |
| Gemini Omni docs; pricing (Last updated 2026-10-19); terms (Last updated 2026-04-28); video (Veo) | https://ai.google.dev/gemini-api/docs/omni · /pricing · /terms · /docs/video | §4, §6.2 | — |
| OpenAI pricing | https://developers.openai.com/api/docs/pricing (gpt-image-2.5: chữ vào $5, ảnh vào $8, ảnh ra $30/1M; gpt-6.1-sol $2/$10) | giá | — |
| OpenAI Services Agreement | https://openai.com/policies/services-agreement/ — **403 trong phiên**; quyền đầu ra lấy theo ghi chép PT3/ĐÓNG-GÓI v2 (§4.1), chưa đọc lại | quyền đầu ra O1 | — |

## §8. Chi phí thật

| Khoản | Mốc / chặn | Thật | Ghi chú |
|---|---|---|---|
| OpenAI ảnh (`so-ai.jsonl`) | — | **$2,065** | 27 ảnh × ≈ $0,077 + 1 lỗi 400 (`input_fidelity` không hỗ trợ) $0 |
| OpenAI chữ/nhìn (`cost.jsonl`, gpt-6.1-sol) | — | **$3,708** | 2 lượt đọc nguồn + 51 lượt kiểm khung |
| **OpenAI tổng** | $5 / $20 | **$5,77** | **Vượt mốc theo dõi $5 — lợi ích: mô hình nhìn thứ hai cho MỌI khung (đáp án 6/6, bắt tường đá/gia súc mà claude bỏ sót).** |
| **Gemini** (`so-ai-gemini.jsonl`) | $12 / $18 | **$9,92** | 9 lượt có tính tiền × $1,10; c2-mạnh lần 1 lỗi "will not be charged". Số Google thực tính chưa xem được (AI Studio không truy cập từ phiên) — đề nghị chủ dự án đối chiếu |
| Claude nhìn (`cost.jsonl`, claude-sonnet-5-5) | — | $6,946 | 49 lượt |
| Claude q_thoi_dai.py (K) | — | $1,422 | 39 khung |
| **Claude tổng** | $8 / $25 | **$8,37** | **Vượt mốc $8 — lợi ích: q_thoi_dai chạy trên mọi khung kiểm để đối chiếu luật của K.** Token phiên chính không đo được từ container |
| RunPod / Runway / ElevenLabs / YouTube | 0 | 0 | |
| Giờ máy CPU | — | ≈ 3,5 h đồng hồ (4 vCPU gần đầy): bộ đệm 0,1 · 1 248 khung nguồn + mặt nạ (10,6–12,8 s/khung/làn, 2 làn) ≈ 2,3 · ghép/đo video ≈ 0,6 · khác 0,5 | |

Chặn an toàn: không chạm (OpenAI $20, Gemini $18, Claude $25); không lỗi lặp ≥ 3. Dừng tiến trình theo PID nhóm (`kill -- -PGID`), không `pkill -f`.

## §9. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)

| Mục | Chỉ số | Giá trị | Ngưỡng | Lệch |
|---|---|---|---|---|
| c2-vừa khung mẫu | T9b đất→nước (max 3 khung) | 1,98 % | ≤ 2 % | −1,0 % (vẫn LOẠI do (i)) |
| toan-canh-mạnh lượt 2 | T9 gốc nước→đất | 1,94 % | ≤ 2 % | −3,0 % (LOẠI do (i)) |
| c4B-vừa | nhấp nháy ÷ nguồn | 1,96 | so đối chứng 2,05 × 1,5 = 3,08 | ngoài ±5 %; ghi vì đối chứng cao (cảnh gần tĩnh) |

Không chỉ số nào ở trên đổi kết luận. Sàn đo cần biết: T9 gốc báo nhầm loé nắng (cang lượt 2: 3,97 % gốc → 0,98 % T9b, tờ so xác nhận chỉ là loé nắng + dải bọt sóng).

## §10. Việc chờ chủ dự án
1. **Xem** `reports/nc-n2p/to-so/to-so-o1-*.png`, `clip/so-timelapse.mp4` (O1) và `clip/so-c1.mp4`, `so-c4B.mp4`, `so-c4-noi.mp4` (Omni) — không chấm "đẹp" trong báo cáo này.
2. **Quyết N2P-D1…D7**; đề xuất chính: **D1 + D2 + D3 + D5** (O1 tấm nền cho timelapse; không Omni; thêm B1–B3; trần 50 %).
3. **Quyết "lối mòn / đường phụ"** thuộc lớp (a) hay (c) (2 tấm timelapse chỉ trượt vì mục này).
4. **Duyệt nháp Kinh thánh §15 N2+** (§6.3) — ghi AUTHORSHIP quyết định sáng tạo.
5. **Gemini billing:** đối chiếu sổ $9,92 với AI Studio (trả trước ≈ $21–23 sau VAT; còn ≈ $11–13 theo sổ).
6. Phiên K: bộ kiểm vào `checks/` (D4). Phiên P: BAI-HOC (D7), RIGHTS nguồn T4, merge nhánh khi duyệt (phiên này **không** merge).

## Tệp
| Tệp | Nội dung |
|---|---|
| `reports/nc-n2p/LUAT-N2P-T4.md` | Luật N2+ T4: danh mục (a)/(b), CẤM, trần, YouTube |
| `reports/nc-n2p/nguon/` | tệp nguồn PD + SHA, `danh-muc-{a,b}.json` + `.kiem.json` (khớp nguyên văn) + `.luot2*.json` (đọc lượt 2) |
| `reports/nc-n2p/ma/` | `kiem_trich.py`, `luot2_gpt.py`, `n2p_lib.py` (mặt nạ, ghép, khớp màu, sổ), `oai_edit.py`, `vision_kiem.py`, `kiem_n2p.py`, `cam_thoi_dai.json`, `chen_loi.py`, `cham_dap_an.py`, `timelapse.py`, `ghep_video.py`, `omni_goi.py`, `do_video.sh`, `kiem_video.sh`, `tong_hop_video.py`, `luoi.sh`, `to_so_o1.py`, `dung_cache.sh`, `dung_clip.sh`, `chay_*.sh`, `nguon-clip.json` |
| `reports/nc-n2p/o1/` | mặt nạ ID + mặt nạ sửa 3 khung, lệnh nguyên văn, 1 ảnh gốc OpenAI có C2PA |
| `reports/nc-n2p/kiem/` | `dap-an/` (khung thử + đáp án + kết quả 2 mô hình + q_thoi_dai), `o1/` (mọi kết quả kiểm O1 + `BANG-O1.txt`) |
| `reports/nc-n2p/omni/` | lệnh, `BANG-OMNI.md`, `tong-hop.json`, `do/` (NC-V2V/V2V3 + nối), `kiem/`, `qtd/`, `c2pa-dau-ra.json` |
| `reports/nc-n2p/tl/` | lệnh tấm + `do-timelapse.json` |
| `reports/nc-n2p/so-ai.jsonl`, `so-ai-gemini.jsonl`, `cost.jsonl` | sổ AI (K-LAI) và chi phí |
| ngoài git (mất theo container) | `/var/tmp/n2p/**` (ảnh AI, clip nguồn, Omni ra — SHA trong sổ), `/var/tmp/cine-out/k2tl-cache`, worktree `/var/tmp/n2p-wt` |

**DỪNG — chờ chủ dự án.**
