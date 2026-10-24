# P-2410: nối thêm dòng sổ (AUTHORSHIP, RIGHTS, COST-LEDGER, BAI-HOC-K2, QUYET-DINH-TREO). Chỉ nối cuối tệp, giữ nguyên byte có sẵn
# (đọc/ghi newline="" — bài học P-2310b: COST-LEDGER có một dòng kết thúc \r). Dùng: python3 -I reports/p2410/ghi_so.py <giờ máy P-2410>
import csv, io, json, os, sys
R = os.path.dirname(os.path.abspath(__file__)) + '/../..'
GIO_P = sys.argv[1]
def noi(p, txt):
    p = os.path.join(R, p); s = open(p, encoding='utf-8', newline='').read()
    if 'P-2410 ghi' in s or 'ghi sổ bởi P-2410' in s:
        sys.exit(f'CHẶN: {p} đã có dòng P-2410')
    assert s.endswith('\n')
    open(p, 'w', encoding='utf-8', newline='').write(s + txt)

# ---------- AUTHORSHIP ----------
A = [
 ('2026-10-23', 'Kênh 2 T4 London — Q1–Q7 trước animatic (21:45; P-2410 ghi)',
  'Nguyên văn: "Duyệt Q1–Q7". Nội dung (theo `checks/ll/RULES-LL.md` 1.17.4 và `reports/k1174/K1174-BAO-CAO.md`): **Q1** ngân sách Gemini T4 mốc $25 / chặn $30 (sau đó nâng ≈ $35 lúc 23:45); **Q2** bỏ trần cứng 20 % minh hoạ M-d ở §15 (d), thay bằng (i) ngân sách Gemini mỗi tập, (ii) tổng khung AI ≤ 70 % (giữ), (iii) góc cao timelapse ≥ 60 %; **Q7** phiên K-1.17.4 làm D11, K117-D8, K1173-D6. Q3–Q6: văn bản đề xuất không có trong repo — P-2410 không ghi nội dung. Văn bản: Kinh thánh §15 (d), §13.6 (24/10/2026)',
  'Chủ dự án đổi cách giới hạn minh hoạ AI (ngân sách tiền thay trần %), giữ trần tổng AI và đặt sàn góc cao', 'Điều phối: đề xuất Q1–Q7', 'Chủ dự án'),
 ('2026-10-23', 'Kênh 2 T4 London — LOOK-T4 chọn mù (23:14; P-2410 ghi)',
  'Nguyên văn: "Tôi chọn 1z 2z 3z 4z 5z 6z 7z 8z". Giải mã `reports/look-t4/khoa.json` (cột Z mỗi hàng): M1-rong A · M1-trung A · M2-ngay C · M2-dem B · M3-rong C · M3-trung A · M4-rong A · M4-trung C (A = cách A + LUT kênh v0,30; B = London sương; C = tranh khắc ấm)',
  'Chủ dự án chấm mù 8 hàng × 3 biến thể trên tờ `reports/look-t4/to-chon-mu.jpg`', 'LOOK-T4: hình học look v2, 3 biến thể, tờ mù, khoá', 'Chủ dự án'),
 ('2026-10-23', 'Kênh 2 T4 London — look hợp nhất + L2–L6 (23:27; P-2410 ghi)',
  'Nguyên văn: "1. xác nhận look hợp nhất Quyết L2–L6 (gồm L5 = bỏ GPU sau khi xem clip M2): “theo khuyến nghị”". Nội dung: look hợp nhất = A chuẩn + ấm kiểu C cho cháy ngày 1666 và toàn cảnh 1940 + khói than dày kiểu B cho đêm cháy 1666; L2 = b (ngưỡng bão hoà theo tập thay ≥ 0,40); L3 = a (người/xe/thuyền nhỏ ở khung trung ≤ 60 m); L4 = a + b (City 1940 khối Victoria–Edward ước lượng + toà có tên); **L5 = bỏ Cycles GPU** (phiếu khuyến nghị (a) giữ GPU cho 3–4 cận đêm; chủ dự án quyết bỏ sau khi xem clip M2); L6 = b (estimated infill chỉ ghi ở thẻ phương pháp). Văn bản: Kinh thánh §14.7 Look T4, §14.2, §11.4, §19 (24/10/2026)',
  'Chủ dự án hợp nhất look theo cảnh (ấm cho ngày cháy/1940, khói than cho đêm cháy) và tự quyết bỏ GPU sau khi xem clip', 'LOOK-T4: phiếu L1–L6, clip 8 s', 'Chủ dự án'),
 ('2026-10-23', 'Kênh 2 T4 London — nhận xét look (23:41; P-2410 ghi)',
  'Nguyên văn: "1. Thành phố vẫn còn trông như “đồ chơi” 2. Khói và lửa cần rõ hơn 3. Các công trình biểu tượng chưa được rõ nét" → mở vòng LOOK-T4-V2',
  'Chủ dự án nêu ba điểm yếu thẩm mỹ của look (độ thật thành phố, lửa/khói, công trình biểu tượng)', '—', 'Chủ dự án'),
 ('2026-10-23', 'Kênh 2 T4 London — mở LOOK-T4-V2 (23:45; P-2410 ghi)',
  'Nguyên văn: "1,2,3,4,5, đồng ý theo khuyến nghị / 6 tôi sẽ tự động nạp". Nội dung: mở LOOK-T4-V2 (công trình biểu tượng, lửa/khói, thử ảnh Gemini làm tấm nền); ngân sách Gemini T4 ≈ $35; mục tiêu tấm nền 35–45 % nếu đạt; GPU lửa chọn sau tờ so; mục 6: chủ dự án tự nạp tiền Gemini',
  'Chủ dự án đặt ngân sách và mục tiêu tỷ lệ tấm nền, tự nạp tài khoản Gemini', 'Điều phối: đề xuất 1–6', 'Chủ dự án'),
 ('2026-10-24', 'Kênh 2 T4 London — hướng sau LOOK-T4-V2 + chọn cột (06:21; P-2410 ghi)',
  'Nguyên văn: "1. Chọn phương án A+B theo khuyến nghị 2. Lấy cột theo khuyến nghị". **A** = dựng animatic T4 bằng look V2 ngay; **B** = thử cho AI phủ BỀ MẶT mái/tường nhà thường (giữ hình khối, vị trí, số nhà; công trình có tên, lửa/khói, sông, bờ vẫn 3D) — K-1.17.5 viết phép kiểm, rồi một vòng thử; đạt thì áp ở bản cuối. **Cột:** M1-rong, M1-trung, M2-ngay, M2-dem, M3-rong, M3-trung, M4-trung = v2-3d; M4-rong = v2-openai (`channel-k2/k2c-t4-02/look/CHON-V2.json`). Văn bản: Kinh thánh §14.7 Look T4, §15 (j)',
  'Chủ dự án chọn cột từng khung trên tờ so (không mù) và mở hướng thử AI phủ bề mặt nhà', 'LOOK-T4-V2: tờ so, khuyến nghị cột và A+B', 'Chủ dự án'),
 ('2026-10-24', 'Kênh 2 T4 London — V1–V7 + K1174-D1…D6 (tin nhắn ngay trước lệnh P-2410; giờ chính xác không có trong lệnh; P-2410 ghi)',
  'Nguyên văn: "Duyệt V1–V7 và K1174-D1…D6 theo khuyến nghị". **V1** = (d) + (b): tấm nền chỉ OpenAI `gpt-image-2.5-sunburst-2026-09-08`, chỉ cảnh 2026 ban ngày; 1666 ngày chờ K-1.17.5; đêm/lửa không dùng tấm nền · **V2** = (a) lửa cách A mới, không GPU · **V3** = (a) khói bếp cộng hiệu, K định cách đo · **V4** = (b) K xét khớp màu cục bộ vòng bảo vệ · **V5** = (b) P1 fov 36° · **V6** = (b) sương σ 1/10 km · **V7** = (b) mục tiêu tấm nền 5–15 % cho animatic. **K1174-D1** = A (phiên K dựng khung đáp án phản chiếu ↔ bãi lấn; luật giữ) · **D2** = A (BIEN-CO-V θ 8/255, k 2, Chặn ở G2) + hiệu chuẩn lại trên animatic T4 · **D3** = A (cách đọc §19 a) · **D4** = A (G2 đòi log máy mỗi khung) · **D5** = A (AI-TU-LIEU khai `sha_tu_lieu`) · **D6** = A (GOC-CAO-60 mẫu số thân phim). Văn bản: Kinh thánh §13.6, §14.2, §14.7, §15 (d), §19',
  'Chủ dự án duyệt phạm vi dùng AI tấm nền, cách dựng lửa, khung xương sống P1 và bộ kiểm T4', 'LOOK-T4-V2: phiếu V1–V7; K-1.17.4: K1174-D1…D6', 'Chủ dự án'),
]
noi('AUTHORSHIP.md', ''.join('| ' + ' | '.join(r) + ' |\n' for r in A))

# ---------- RIGHTS ----------
van = json.load(open(os.path.join(R, 'channel-k2/k2c-t4-02/look/van-cc0.json')))
sha_tl = {l.split()[1]: (l.split()[0], l.split()[2]) for l in open(os.path.join(R, 'channel-k2/k2c-t4-02/licenses/SHA256-TU-LIEU-LOOK.txt')) if l.strip()}
H = '| Mã | Tài sản | Loại | Nguồn/URL | Tác giả | Giấy phép (trích nguyên câu + link) | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 | Ngày thêm |\n|---|---|---|---|---|---|---|---|---|---|\n'
t = ('\n## T4 London — look (LOOK-T4, LOOK-T4-V2; P-2410 ghi 24/10/2026)\n'
     'Nguồn: `channel-k2/k2c-t4-02/RIGHTS-NHAP.md` mục F, `reports/look-t4/LOOK-T4-BAO-CAO.md` §8, `reports/look-t4-v2/LOOK-T4-V2-BAO-CAO.md` §7, `reports/look-t4-v2/NGUON-CONG-TRINH.md`.\n\n'
     '### Vân bề mặt CC0 (Poly Haven, 16 lớp; tải 23/10/2026 bằng `scripts/k2ldn/tai_van.py`; danh sách + URL + SHA: `channel-k2/k2c-t4-02/look/van-cc0.json`)\n' + H)
for l in van['lop']:
    f = {x['tep']: x for x in l['tep']}
    shas = '; '.join(f"{x['tep']} {x['sha256']}" for x in l['tep'])
    t += (f"| T4-VAN-{l['id']} | {l['id']} — {l['vai']} | Vân 1k JPG (diff + nor_gl) | {l['trang']} | {', '.join(l['tac_gia'])} | "
          f"{l['giay_phep']} — https://creativecommons.org/publicdomain/zero/1.0/ | Có / Có / Có | Poly Haven (không bắt buộc) | {shas} | {van['ngay_tai']} |\n")
t += '\n### Tư liệu tham chiếu dựng hình (LOOK-T4, D6 — không lên hình)\n' + H
MET = [('336039', 'Hollar, *Saint Paul\'s, South side (Ecclesiae Cathedralis St. Pauli, A Meridi Prospectus)*, từ Dugdale *The History of St. Paul\'s Cathedral in London* (1658) — tỉ lệ tầng/khoang Old St Paul\'s (bậc 4)', '1991.1336.2', 'Wenceslaus Hollar', 'met-336039-0.jpg'),
       ('336038', 'Hollar, *Saint Paul\'s from the South Showing the Spire* (1657), Dugdale 1658 — đối chiếu (hình trước 1561, có chóp; KHÔNG dựng chóp)', '1991.1336.1', 'Wenceslaus Hollar', 'met-336038-0.jpg'),
       ('757299', 'Dugdale, *The History of St. Paul\'s Cathedral in London, From its Foundation until these Times* (1658), sách — tra bản khắc (2 ảnh trang)', '2017.320.1', 'Sir William Dugdale', 'met-757299-0.jpg')]
for oid, ten, acc, tg, tep in MET:
    s_ = sha_tl[tep][0] + ('; ' + 'met-757299-1.jpg ' + sha_tl['met-757299-1.jpg'][0] if oid == '757299' else '')
    t += (f"| T4-TL-MET-{oid} | {ten} | Bản khắc / sách | The Met {acc} — https://www.metmuseum.org/art/collection/search/{oid} ; ảnh {sha_tl[tep][1]} | {tg} | "
          f"Met API `\"isPublicDomain\": true` (Met Open Access, CC0) — JSON nguyên văn `channel-k2/k2c-t4-02/licenses/met-{oid}.json` | Có / Có / Có (chỉ tham chiếu, không lên hình) | The Metropolitan Museum of Art (CC0) | {s_} | 2026-10-23 |\n")
t += '\n### Dữ kiện kích thước và vị trí (lớp dữ kiện; không dùng hình hay văn bản nguồn trên phim)\n' + H
t += ('| T4-DL-GUT-48491 | *Views of St. Paul\'s Cathedral, London* (trích Gilbertson, Official Guide) — kích thước St Paul\'s: dài 515 ft, ngang cánh 250 ft, mặt tây 180 ft, trống 112 ft, vòm 102 ft, tháp tây 221 ft, tới thập giá 365 ft (bậc 3) | Văn bản (dữ kiện) | Project Gutenberg #48491 — https://www.gutenberg.org/cache/epub/48491/pg48491.txt | (Gilbertson, trích) | Phạm vi công cộng tại Mỹ (ghi chú Gutenberg; LOOK-T4-V2 §7). Chỉ dùng dữ kiện số | Có / Có / Có | — | c2fbc2440a796712bfa9cd43b4f6577e605ad6be15dd6f0ef26a8c10aa78929f (bản .txt, ngoài git) | 2026-10-23 |\n'
          '| T4-DL-GUT-60008 | *London and Its Environs Described*, vol. 5 (Dodsley 1761), mục MONUMENT — thân cột Ø 15 ft cao 120 ft, bệ 40 ft, nón 32 ft, bầu lửa (bậc 3) | Văn bản (dữ kiện) | Project Gutenberg #60008 — https://www.gutenberg.org/cache/epub/60008/pg60008.txt | R. & J. Dodsley (xb. 1761) | Phạm vi công cộng (LOOK-T4-V2 §7). Chỉ dùng dữ kiện số | Có / Có / Có | — | 850d5686956f9e2a13719aa2d37edf09ab17658c0b36e65429e88a6cfd870d15 (bản .txt, ngoài git) | 2026-10-23 |\n'
          '| T4-DL-WIKI-CONG-TRINH | Số liệu từ Wikipedia: St Paul\'s (158 m, 75 m, 37 m, 111 m; lan can ≈ 110 ft; Fletcher 1962), Monument (202 ft), White Tower (36 × 32 m, 27 m, vị trí tháp góc), Old St Paul\'s (586 / 100 / 290 ft, Clifton-Taylor; tháp 204 ft, Hooke 1664), toạ độ 78 nhà thờ giáo xứ City + danh sách 34 nhà thờ không dựng lại (Reynolds 1922) | Dữ kiện số (bậc 3 thứ cấp) | en.wikipedia.org (API `prop=coordinates`, WebFetch; truy cập 23/10/2026) — `channel-k2/k2c-t4-02/mo-hinh/nha-tho-1666.json` | Wikipedia contributors | Văn bản CC BY-SA 4.0 — https://creativecommons.org/licenses/by-sa/4.0/ ; **chỉ dùng số/toạ độ (dữ kiện), không chép văn bản hay ảnh vào phim** | Có / Có / Có (dữ kiện) | — | — | 2026-10-23 |\n'
          '| T4-DL-OSM-CONG-TRINH | OSM relation 3374550 (The Monument to the Great Fire of London; tâm EPSG:27700 ≈ 532923, 180761 — sửa vị trí lệch ≈ 68 m của look v1) và way 369135772 (White Tower; tâm + trục) | Dữ liệu không gian | https://www.openstreetmap.org/relation/3374550 ; https://www.openstreetmap.org/way/369135772 (thuộc bộ T4-DL-OSM) | OpenStreetMap contributors | Open Database License (ODbL) 1.0 — https://opendatacommons.org/licenses/odbl/1-0/ | Có / Có / Có (ghi công) | © OpenStreetMap contributors (ODbL) | — (tải lại được) | 2026-10-23 |\n')
t += ('\n- **Tài sản tự tạo:** LUT `channel-k2/k2c-t4-02/look/mau/look-B-lanh.cube`, `look-C-am.cube` (SHA trong `.sha256`; `scripts/k2ldn/look_lut.py`); LUT kênh `k2c-t3-kenh-v030.cube` (của dự án, T3); lightmap Cycles CPU và hình học `ldn2.bin` (ngoài git, SHA trong báo cáo look); mô hình công trình `scripts/k2ldn/cong_trinh_v2.py` (từ dữ kiện trên, không dùng hình nguồn).\n'
      '- **Ảnh AI thử LOOK-T4-V2** (OpenAI `gpt-image-2.5-sunburst-2026-09-08` 12 ảnh + 2 lỗi HTTP 400 $0; Gemini `gemini-nano-banana-2.1` Batch 12 ảnh; sổ `reports/look-t4-v2/so-ai.jsonl`, C2PA 24/24, SynthID 12/12 Gemini; bản JPG `channel-k2/k2c-t4-02/ai/goc-v2/`): **chỉ là bản thử, chưa vào phim** — không ghi dòng tài sản. Ô M4-rong v2-openai được chọn làm cột look (24/10 06:21); tấm sản xuất làm lại ở fov 36° (V5) và ghi RIGHTS khi vào phim.\n'
      '- LOOK-T4 không dùng AI sinh hình; không nhạc/SFX/giọng/font mới ở hai vòng look.\n')
noi('RIGHTS.md', t)

# ---------- COST-LEDGER ----------
hdr = open(os.path.join(R, 'COST-LEDGER.csv'), encoding='utf-8', newline='').readline().strip().split(',')
rows = [
 dict(phien='LOOK-T4', tap_hoac_moc='K2C-T4-02 London look (M1b): hình học look v2, 4 mốc × 3 biến thể, tờ chọn mù, 4 clip, tranh khắc T3, phiếu L1–L6', cong='look', ngay='2026-10-23',
      claude_api_usd='0', tran_api_usd='5', model_ghim='không gọi API', el_ky_tu_gui='0', el_ky_tu_bo_dem='0', gio_render='5', cham_chu_du_an='1',
      nguon='reports/look-t4/LOOK-T4-BAO-CAO.md §10 (nhánh k2c-t4-02-look @5123bebf)',
      ghi_chu='Claude API $0; OpenAI $0; RunPod $0 (không bật pod; nướng Cycles CPU 86–108 s/mốc); Gemini/ElevenLabs/YouTube 0; tổng API/GPU $0; giờ máy ≈ 5,0 h (10:53 → ≈ 15:50 UTC; mốc 12 h); chủ dự án chọn mù 23/10 23:14; ghi sổ bởi P-2410'),
 dict(phien='K-1.17.4', tap_hoac_moc='Luật 1.17.4: D11 giữ N2P-3, BIEN-CO-V (thước biến cố video), Q37 (c) miễn thẻ PP, Q2 (GEMINI-NGAN-SACH, GOC-CAO-60), §19 (MAY-19, BAN-DO-12, TU-LIEU-10, AI-TU-LIEU); LOCK 1.17.3 d99af8f2 → 1.17.4 08486eb2', cong='K', ngay='2026-10-23',
      claude_api_usd='0', tran_api_usd='3', model_ghim='không gọi API', el_ky_tu_gui='0', el_ky_tu_bo_dem='0', gio_render='2.5', cham_chu_du_an='1',
      nguon='reports/k1174/K1174-BAO-CAO.md §11 (nhánh checks-1-17-4 @f4a3d9ca)',
      ghi_chu='Claude API $0; OpenAI $0; Gemini/ElevenLabs/RunPod/YouTube 0; tải LFS master T3 1,79 GB một lần; selftest k1174 91/91; giờ máy ≈ 2,5 h (15:40 → 18:05 UTC; mốc 5 h); chủ dự án duyệt K1174-D1…D6 24/10; ghi sổ bởi P-2410'),
 dict(phien='LOOK-T4-V2', tap_hoac_moc='K2C-T4-02 London look vòng 2: công trình biểu tượng (St Paul\'s, Monument, White Tower), lửa/khói cách A mới, 24 tấm nền AI thử + cổng (i)–(v), 1 khung Cycles GPU, tờ so, phiếu V1–V7', cong='look', ngay='2026-10-23',
      claude_api_usd='6.02', tran_api_usd='3', model_ghim='claude-sonnet-5-5 (kiểm); gpt-6.1-sol (kiểm); gpt-image-2.5-sunburst-2026-09-08; gemini-nano-banana-2.1', el_ky_tu_gui='0', el_ky_tu_bo_dem='0', gio_render='2.4', cham_chu_du_an='1',
      nguon='reports/look-t4-v2/LOOK-T4-V2-BAO-CAO.md §8 (nhánh k2c-t4-02-look2 @c4079595); sổ AI reports/look-t4-v2/so-ai.jsonl; cost.jsonl',
      ghi_chu='Gemini $0,42 (12 ảnh Batch; mốc $5); OpenAI $2,80 = ảnh $0,914 + kiểm gpt-6.1-sol $1,881 (36 lần; mốc $3, −6,8 %); Claude API $6,02 = kiểm claude-sonnet-5-5 $4,80 (36 lần) + q_thoi_dai.py $1,22 (36 khung) — VƯỢT mốc theo dõi $3 (chặn $15): cổng (i)/(ii)/(iv) bắt buộc §15 (c) cần mô hình nhìn thứ hai, 36 lượt kiểm (24 tấm + 4 ghép lại + 4 l3h + 4 tham khảo); RunPod $0,053 (số dư 21,138 → 21,085; 2 pod 74 s + 117 s, đã xoá); ElevenLabs/YouTube 0; tổng API/GPU ≈ $9,29; giờ máy ≈ 2,4 h (16:50 → ≈ 19:10 UTC; mốc 12 h); chủ dự án chọn cột 24/10 06:21; ghi sổ bởi P-2410'),
 dict(phien='P-2410', tap_hoac_moc='Merge checks-1-17-4 + k2c-t4-02-look2 (gồm k2c-t4-02-look) vào main, CHON-V2.json, Kinh thánh Look T4 + sửa §11.4, §13.6, §14.2, §15 (d)(j), §19, sổ (AUTHORSHIP, RIGHTS, COST-LEDGER, BAI-HOC-K2, QUYET-DINH-TREO), cập nhật main', cong='P', ngay='2026-10-24',
      claude_api_usd='0', tran_api_usd='0', model_ghim='không gọi API', el_ky_tu_gui='0', el_ky_tu_bo_dem='0', gio_render=GIO_P, cham_chu_du_an='0',
      nguon='reports/p2410/P2410-BAO-CAO.md',
      ghi_chu=f'Claude API 0; OpenAI 0; Gemini 0; ElevenLabs 0; RunPod 0; YouTube 0; 0 subagent; selftest 13 bộ × 3 lượt; giờ máy ≈ {GIO_P.replace(".", ",")} h (mốc 2 h); ghi sổ bởi P-2410'),
]
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=hdr, lineterminator='\n')
for r in rows:
    assert set(r) <= set(hdr), set(r) - set(hdr); w.writerow(r)
noi('COST-LEDGER.csv', buf.getvalue())

# ---------- BAI-HOC-K2 ----------
B = [
 ('K40', 'Màu mặt nạ ID ghi qua hàm chuyển màu của trình dựng bị lệch → đo sai lớp', 'LOOK-T4-V2 sự cố 3: mặt nạ mã công trình đọc sai; mọi màu mặt nạ qua `s2l` lệch (đầu ra sau `colorspace_fragment` không mã hoá lại); lỗi có từ `look.js` (đất "bang" đọc thành "suon" ở LOOK-T4, cùng nhóm đất nên không đổi kết luận)', 'mặt nạ đi qua đường màu của ảnh đẹp (chuyển tuyến tính ↔ sRGB)', '**Mặt nạ ghi màu thẳng, bỏ qua mọi chuyển màu; bảng màu cách ≥ 20 mức; đọc lại mặt nạ bằng bảng (đếm điểm ảnh ngoài bảng = 0) trước khi đo** (`design/k2v/ldn/look2.js`)'),
 ('K41', 'Chú thích chèn giữa dòng nuốt phần còn lại của dòng — **lặp BAI-HOC-LL #42/#76**', 'LOOK-T4-V2 sự cố 4: `#` chèn giữa dòng nuốt lệnh `M = …` trong `tam_nen_v2.py` (thấy khi đọc lại, 0 lượt hỏng); LOOK-T4 sự cố 8: 2 lần (Python mất `VICT`, JS lỗi cú pháp); tiền kỳ T4 sự cố #16 — ≥ 4 lần trong 3 phiên T4', 'sửa mã bằng thay chuỗi trên dòng dài, chú thích viết liền sau mã', '**Không chèn chú thích vào giữa dòng; chú thích đặt dòng riêng. Sau mỗi sửa: `python -m py_compile` / `node --check` + đọc lại đúng dòng đã sửa trong `git diff`** (LL #42, #76)'),
 ('K42', 'Ảnh vào tấm nền AI còn vật chuyển động → AI vẽ vật đó lên tấm tĩnh', 'LOOK-T4-V2 sự cố 8: ảnh vào 1666 còn khói bếp → AI vẽ khói lên tấm, (iv) trượt; sửa từ lượt 3 (`chim=false`)', 'dùng nguyên khung đẹp làm ảnh vào', '**Ảnh vào tấm nền dựng riêng KHÔNG có vật chuyển động (khói bếp, lửa, thuyền chạy…)**; vật đó ghép lại từ render từng khung (Kinh thánh §15 (b))'),
 ('K43', 'Vật bán trong suốt dán nguyên điểm ảnh render lên tấm nền kéo theo nền sương → "đốm trắng"', 'LOOK-T4-V2 sự cố 9: khói bếp dán nguyên điểm ảnh; (v) nhấp nháy 3,3–11,9 × đối chứng → cộng HIỆU có/không khói: 0,998–1,008 ×', 'khói không có biên cứng; điểm ảnh render gồm cả nền phía sau', '**Vật bán trong suốt ghép bằng cộng hiệu (render có vật − render không vật)** (V3 = a, 24/10/2026); K-1.17.5 định cách đo (i)/(iv) cho lớp sống'),
 ('K44', 'Lỗi 3D cũ chỉ lộ khi nền đổi tông', 'LOOK-T4-V2 sự cố 10: khói bếp 3D ở xa không áp sương (lỗi có từ look v1) → đốm sáng ở chân trời trên tấm nền; sửa mờ dần 1,5–3 km trong `look2.js`, dựng lại 4 khung 1666 + 2 timelapse', 'vật thêm vào cảnh không đi qua cùng đường khí quyển; trên nền render cùng tông thì không thấy', '**Mọi vật thêm vào cảnh phải qua cùng sương/khí quyển; soát khung có/không vật ở xa (≥ 1,5 km) trước khi dựng hàng loạt**'),
 ('K45', 'Vùng bảo vệ nở 3 px của vật nhỏ tạo quầng khi tông tấm nền lệch render', 'LOOK-T4-V2 sự cố 11: sau khi sửa K42–K44, (iv) 1666 M1-rong vẫn trượt chỉ vì quầng 1–2 px quanh nhà xa; biến thể tham khảo xếp nhà xa ngoài hộp vào lớp (c) đạt (i)–(v)', 'khớp màu render vào tông tấm là toàn cục (Lab, k = 0,7); vòng nở giữ màu render', 'chờ K-1.17.5 xét khớp màu cục bộ vòng bảo vệ (V4 = b, 24/10/2026); tới lúc đó luật nở 3 px giữ nguyên, không tự nới'),
 ('K46', '`pkill -f` / `grep` theo chuỗi có trong chính lệnh shell giết shell — lặp', 'K-1.17.4 §12 (1): 2 lần trong phiên; LOOK-T4 sự cố 4 (`kill $(pgrep -f …)`, exit 144) — lặp LL #24, #41, #112', 'chuỗi tìm nằm trong dòng lệnh của chính shell gọi', '**Lấy PID bằng lệnh riêng (ghi PID/PGID ra tệp khi khởi chạy) rồi mới dừng theo PID/PGID**; không `pkill/pgrep -f` theo chuỗi (LL #112)'),
 ('K47', 'Đẩy WIP bằng stash `checks/` làm hỏng lượt k2check đang chạy', 'K-1.17.4 §12 (2)', 'k2check import module lười; stash đổi tệp giữa lượt chạy', '**Chạy k2check từ bản sao/worktree riêng khi còn thao tác git trên cây đang làm**'),
 ('K48', 'Giả thuyết nguyên nhân lỗi đo phải kiểm bằng tách điểm lỗi theo vùng trước khi xin đổi luật', 'K-1.17.4 §12 (3) / §1: D11 — dải "biển" giả ngoài hộp góp **0 điểm** vào lỗi lượt 2; đo đúng cách khiếu nại đề nghị ra 2,67 % (vẫn vượt 2 %); lỗi thật là bờ lấn sông 8–40 px', 'khiếu nại dựa trên giả thuyết chưa đo', '**Trước khi khiếu nại một phép đo: tách điểm lỗi theo vùng/nguyên nhân và nộp kèm số đó** (`checks-appeal.md`)'),
 ('K49', 'Log máy `render_ldn.js` phải lưu cùng shot', 'K-1.17.4 §12 (4) / §5.1: MAY-19 trên bảng shot T4 v1 = THIẾU log khung ở 50 shot → TRƯỢT ở G2', 'log.json nằm ở `/var/tmp` cùng khung thô, mất theo container (lặp kiểu LL #109, #117)', '**Giữ `log_may` (log.json) của từng shot trong git hoặc kèm SHA + cách tái tạo; G2 đòi log mỗi khung** (K1174-D4 = A, 24/10/2026; Kinh thánh §13.6)'),
 ('K50', 'Tấm nền AI không chữa được phần thuộc lớp (a) — đo trước xem "đồ chơi" nằm ở lớp nào rồi mới chọn công cụ', 'LOOK-T4-V2 §4: tấm nền chỉ thay trời/nước/đất; mái + tường nhà (phần "đồ chơi" lớn nhất theo nhận xét 23/10 23:41) là lớp (a) nên được dán lại từ render; 24 tấm, 1 tấm đạt cổng; ≈ $9,24 AI (ảnh + kiểm) cho vòng thử', 'chọn công cụ (AI tấm nền) trước khi đo điểm yếu thuộc lớp nào', '**Trước vòng sửa look: khoanh vùng điểm yếu theo lớp (a)/(b)/(c) trên mặt nạ ID, rồi mới chọn công cụ (nâng 3D cho lớp (a), AI chỉ cho lớp nền)**; hướng AI phủ bề mặt nhà: Kinh thánh §15 (j) (ĐANG THỬ, 24/10/2026 06:21)'),
]
noi('channel-k2/BAI-HOC-K2.md', '\n## K40–K50 · Look T4 và bộ kiểm 1.17.4 (P-2410 ghi 24/10/2026)\n| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |\n|---|---|---|---|---|\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in B))

# ---------- QUYET-DINH-TREO ----------
Q = ('\n## D. Cập nhật 24/10/2026 (P-2410 ghi)\n\n'
     '**Đã quyết** (nguyên văn + giờ ở `AUTHORSHIP.md`; văn bản ở Kinh thánh `docs/BIBLE-KENH2.md` 24/10/2026):\n\n'
     '| # | Quyết định | Khi nào | Áp ở |\n|---|---|---|---|\n'
     '| K117-D8 | A — Q37 không nhận biến cố tự khai; thước biến cố đo trên video | 23/10 17:42 ("đồng ý theo đề xuất") | K-1.17.4 viết BIEN-CO-V (θ 8/255, k 2); Kinh thánh §13.6 |\n'
     '| K1173-D6 | A — Q37 (c) miễn khối thẻ PP cuối phim (≤ 2 × ≤ 10 s) | 23/10 17:42 | K-1.17.4 (`q37_mien`) |\n'
     '| D11 | LỖI ẢNH — phép (iii) giữ T9b ≤ 2 % (lỗi ở tấm AI: bờ lấn sông) | phán quyết K-1.17.4 (Q7 23/10 21:45) | `checks-appeal.md` "Phán quyết K — checks 1.17.4 · D11"; Kinh thánh §15 (d) |\n'
     '| Q2 | bỏ trần cứng 20 % M-d từ T4; ngân sách Gemini/tập (T4 $35, mốc $30 — 23:45); tổng AI ≤ 70 %; góc cao ≥ 60 % | 23/10 21:45 ("Duyệt Q1–Q7"), 23:45 | 1.17.4 (MINH-HOA, N2P-6, GEMINI-NGAN-SACH, GOC-CAO-60); Kinh thánh §15 (d) |\n'
     '| K1174-D1 | A — phiên K dựng khung đáp án phản chiếu ↔ bãi lấn rồi mới xét miễn; luật giữ | 24/10 ("Duyệt V1–V7 và K1174-D1…D6 theo khuyến nghị") | việc của K-1.17.5 (còn treo bên dưới) |\n'
     '| K1174-D2 | A — duyệt BIEN-CO-V; hiệu chuẩn lại trên animatic T4 (log máy thật) trước G2 | 24/10 | Kinh thánh §13.6 |\n'
     '| K1174-D3…D6 | A — cách đọc §19 (a); log máy mỗi khung ở G2; khai `sha_tu_lieu`; mẫu số GOC-CAO-60 = thân phim | 24/10 | Kinh thánh §13.6 |\n'
     '| V1–V7 | V1 d + b (tấm nền chỉ OpenAI, chỉ 2026 ngày) · V2 a (lửa cách A, không GPU) · V3 a (khói bếp cộng hiệu, K định đo) · V4 b (K xét khớp màu cục bộ vòng bảo vệ) · V5 b (P1 fov 36°) · V6 b (sương σ 1/10 km) · V7 b (tấm nền 5–15 % cho animatic) | 24/10 | Kinh thánh §14.2, §14.7, §15 (d), §19; `channel-k2/k2c-t4-02/look/CHON-V2.json` |\n'
     '| Mục A còn lại (K117-D1, D3, D5, D6; K1171-D2…D4; K1173-D1…D5) | theo khuyến nghị, trừ K1173-D1 = B | 23/10 17:42 | AUTHORSHIP (P-2310b) |\n\n'
     '**Còn treo — giao phiên K-1.17.5** (đang chạy song song, nhánh `checks-1-17-5`; khiếu nại gốc: `reports/look-t4-v2/LOOK-T4-V2-BAO-CAO.md` §11):\n\n'
     '| # | Nội dung | Căn cứ | Chặn gì |\n|---|---|---|---|\n'
     '| K1175-a | Khung đáp án phản chiếu thật ↔ bãi/bờ lấn cho N2P-3 (iii) (K1174-D1 = A) | K1174 §1, §9 | tấm nền có mặt nước |\n'
     '| K1175-b | Phép (iii) T9b với sắc nước: Gemini/OpenAI đổi nước sang xám/ô-liu bị tính "nước→đất" dù vẫn là nước | LOOK-T4-V2 §3, §11 (2) | tấm nền 1666 ngày, công cụ Gemini |\n'
     '| K1175-c | Phép (i)/(iv) cho lớp sống: khói bếp ghép bằng cộng hiệu không thuộc lớp (a) nên không qua (i) 0/255 (V3 = a) | LOOK-T4-V2 §3, V3 | mọi tấm 1666 |\n'
     '| K1175-d | Vòng bảo vệ vật nhỏ (< 60 px, nở 3 px): khớp màu cục bộ (V4 = b) | LOOK-T4-V2 §3, sự cố 11 | tấm 1666 có nhà xa |\n'
     '| K1175-e | Phép kiểm phủ bề mặt nhà thường bằng AI (giữ hình khối, vị trí, số nhà) — điều kiện (1) của Kinh thánh §15 (j) | 24/10 06:21 (B) | vòng thử B, bản cuối T4 |\n'
     '| (sau animatic) | Hiệu chuẩn lại BIEN-CO-V trên animatic T4 (K1174-D2) | K1174 §13 mục 4 | G2 T4 |\n')
noi('reports/k1173/QUYET-DINH-TREO.md', Q)
print('xong')
