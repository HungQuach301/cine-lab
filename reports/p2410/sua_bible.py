# P-2410: sửa docs/BIBLE-KENH2.md theo quyết định 23/10 21:45 → 24/10/2026. Mỗi chuỗi gốc phải xuất hiện đúng 1 lần.
import hashlib, sys
P = 'docs/BIBLE-KENH2.md'
s = open(P, encoding='utf-8', newline='').read()
print('trước', hashlib.sha256(s.encode()).hexdigest())
E = []
# 0. tiêu đề
E.append(('; §19 + sửa §13.6, §15 — 23/10/2026)',
          '; §19 + sửa §13.6, §15 — 23/10/2026; Look T4 ở §14.7 + sửa §11.4, §13.6, §14.2, §15 (d), §19, thêm §15 (j) — 24/10/2026)'))
# 1. §11.4 ngoại lệ L6
a = '- Phố có nguồn nhưng bản đồ không vẽ hết: lấp khối ước tính trong ranh phố có nguồn, tông hơi khác + dòng "estimated infill", ghi % diện tích lấp. (chữ trên hình: theo §12.1)\n'
E.append((a, a + '- Ngoại lệ T4 (L6): lõi khối nhà 1666 lấp ước lượng ("estimated infill") KHÔNG tô tông khác trên hình; chỉ ghi ở thẻ phương pháp (kèm % diện tích lấp, số đo từ mặt nạ lấp) (duyệt 23/10/2026 23:27, L6 = b "theo khuyến nghị").\n'))
# 2. §13.6 nhịp đo trên video + hàng mới + cách khai
a = '- Từ T4: máy trong shot theo §19 (a) (thay TL-1 "cố định hoặc trôi ≤ 2 %/s"; CODINH vẫn bắt buộc cho shot có tấm nền N2+); bản đồ cổ và tranh khắc theo §19 (b)(c) (thay TL-4) — chủ dự án duyệt 23/10/2026 17:42 (G1 T4, D9).\n'
E.append((a, a +
 '- Từ T4, nhịp đo trên video: biến cố thấy được của TL-3 và Q37 (b)(c) đo trên master/animatic bằng hàng BIEN-CO-V (θ 8/255, k 2; lưới 8 × 6 ô, đổi trong ≤ 3 s sau khi trừ chuyển động máy); biến cố tự khai trong log không được nhận. Cảnh báo ở animatic, Chặn ở G2; hiệu chuẩn lại BIEN-CO-V trên animatic T4 (log máy thật) trước G2 T4 (duyệt 23/10/2026 17:42, K117-D8 = A; 23/10/2026 21:45, Q7; 24/10/2026, K1174-D2 = A).\n'
 '- Hàng kiểm mới từ T4: MAY-19 (§19 a), BAN-DO-12 (§19 b), TU-LIEU-10 (§19 c), AI-TU-LIEU (§19 b–c), GEMINI-NGAN-SACH và GOC-CAO-60 (§15 d). Định nghĩa, trường đọc và ngưỡng: `checks/ll/RULES-LL.md` mục 1.17.4 (LOCK 1.17.4 `08486eb2…`); Kinh thánh không chép luật. Cách đọc §19 (a), log máy mỗi khung ở G2, khai `sha_tu_lieu`, mẫu số góc cao = thân phim trừ thẻ PP: theo K-1.17.4 (duyệt 24/10/2026, K1174-D3…D6 = A).\n'
 '- Cách khai T4 (theo `reports/k1174/K1174-BAO-CAO.md` §5): episode.yaml `kenh2_tu_t4: true`, `animatic: true` ở animatic, `ngan_sach_gemini_usd: 35`, `ngan_sach_gemini_moc_usd: 30`, `so_ai_gemini` (mỗi dòng có `usd` giá thật), `so_ai` / `so_ai_openai`, `sha_tu_lieu: licenses/SHA256-TU-LIEU.txt`, `goc_toa_do`, `log_shot`; log shot mỗi shot khai `cu_may` và giữ `log_may` (log.json của `render_ldn.js`, lưu cùng shot, không để ở `/var/tmp`) (duyệt 23/10/2026 23:45 ngân sách $35; 24/10/2026, K1174-D4 = A).\n'))
# 3. §14.2 T4 không GPU
a = '- Cú lặn/cận cảnh đêm có lửa (10–20 % thời lượng) dựng TRỌN bằng Cycles GPU thuê (RunPod); không ghép A↔B trong một cú máy. Chưa chuyển cả tập sang Cycles (NG-D3).\n'
E.append((a, a + '- T4 không dùng Cycles GPU: lửa/khói mọi khung, kể cả cận đêm, bằng cách A mới (`design/k2v/ldn/look2.js`: lõi lửa, quầng, tàn lửa theo gió, chân khói hắt đỏ, khói ngày đặc tách tầng); dòng trên không áp cho T4 (duyệt 23/10/2026 23:27, L5 "bỏ GPU sau khi xem clip M2"; 24/10/2026, V2 = a).\n'))
# 4. §14.7 Look T4 (sau dòng Màu V2-D1, cuối §14.7)
a = '- Màu (V2-D1; chủ dự án 22/10/2026 11:09): bão hoà ≥ 0,40 đặt ở bước chỉnh màu toàn phim của bản cuối; khớp tông minh hoạ AI vào 3D.\n'
E.append((a, a + '\n**Look T4** (K2C-T4-02 London; chọn mù 23/10/2026 23:14, look hợp nhất 23:27, chọn cột V2 24/10/2026 06:21, V1–V7 24/10/2026):\n'
 '- LOOK-T4-1 Nền: biến thể A = cách A + LUT kênh `k2c-t3-kenh-v030.cube`, cho mọi khung; ấm kiểu C (nắng, trời, sương ấm; LUT A giữ nguyên) cho ngày cháy 1666 và toàn cảnh 1940; khói than dày kiểu B (sương σ 1/6 km + lớp khói than thấp σ 1/4,2 km) cho đêm cháy 1666 (duyệt 23/10/2026 23:27, look hợp nhất sau chọn mù 23:14).\n'
 '- LOOK-T4-2 Lửa/khói: cách A mới `design/k2v/ldn/look2.js` (lõi lửa, quầng, tàn lửa theo gió, chân khói hắt đỏ theo độ cao, khói ngày đặc tách tầng, ánh lửa mặt tiền/mặt sông); không GPU (§14.2) (duyệt 23/10/2026 23:45; 24/10/2026, V2 = a).\n'
 '- LOOK-T4-3 Sương phối cảnh khí quyển σ = 1/10 km (thay 1/16 km của A gốc) cho khung A và ấm kiểu C; đêm cháy 1666 giữ kiểu B (duyệt 24/10/2026, V6 = b).\n'
 '- LOOK-T4-4 Điểm máy xương sống P1 (Bankside) [532330, 180250, 230] nhìn [532420, 180980, 15], **fov 36°** (thay 50°; vòm St Paul\'s 67 px ở 1080p); mọi lần P1 tái xuất đọc lại đúng tham số này (§19 (a) luật 3) (duyệt 24/10/2026, V5 = b).\n'
 '- LOOK-T4-5 Cột chọn và thông số tái lập: `channel-k2/k2c-t4-02/look/CHON-V2.json` (M1-rong, M1-trung, M2-ngay, M2-dem, M3-rong, M3-trung, M4-trung = V2 3D; M4-rong = V2 + tấm nền OpenAI); tệp máy `channel-k2/k2c-t4-02/look/may-v2/`; tờ so `reports/look-t4-v2/to-so-v2.jpg` (duyệt 24/10/2026 06:21).\n'
 '- LOOK-T4-6 Bão hoà: ngưỡng ≥ 0,40 (§14.4) không áp cho T4; ngưỡng theo tập = trung vị của các khung đã chọn, giữ ΔE shot kề; người/xe/thuyền nhỏ thêm ở sản xuất cho khung trung ≤ 60 m (L3 = a); City 1940 = khối Victoria–Edward ước lượng trên cùng lô + toà có tên còn lại, ghi "ước lượng" ở thẻ phương pháp (L4 = a + b) (duyệt 23/10/2026 23:27, L2–L4 "theo khuyến nghị").\n'
 '- LOOK-T4-7 Còn mở: "đồ chơi" chủ yếu nằm ở mái/tường nhà thường (lớp (a) theo số đo LOOK-T4-V2 §4) — xem §15 (j) (duyệt 24/10/2026 06:21, B).\n'))
# 5. §15 (d) viết lại cho T4
a = ('- (d) Trần T4: tấm nền N2+ ≤ 50 % thời lượng (chỉ shot timelapse máy cố định); minh hoạ M-d ≤ 20 %; tổng khung có AI ≤ 70 %; hai loại không chồng nhau trên một shot; chuyển tấm nền chỉ bằng hoà ≥ 2 s. Không dùng AI video→video (sửa video theo video nguồn) cho shot timelapse hoặc shot mang dữ kiện; video AI chỉ cho minh hoạ M-d. T4: tấm nền N2+ lập kế hoạch ≤ 15 % thời lượng tới khi phiên K xét phép (iii) (D11, chủ dự án 23/10/2026 17:42); trần 50 % giữ nguyên làm trần luật.\n')
E.append((a,
 '- (d) Trần từ T4 (viết lại 24/10/2026 theo Q2, D11, V1, V7): tấm nền N2+ ≤ 50 % thời lượng là trần luật (chỉ shot timelapse máy CODINH); minh hoạ M-d **bỏ trần cứng 20 %** (chỉ ghi %), thay bằng **ngân sách Gemini mỗi tập** — T4 $35, mốc theo dõi $30 (hàng GEMINI-NGAN-SACH; $35 thay Q1 $25/$30); tổng khung có AI ≤ 70 %; góc cao timelapse ≥ 60 % thân phim (GOC-CAO-60); hai loại không chồng nhau trên một shot; chuyển tấm nền chỉ bằng hoà ≥ 2 s. Không dùng AI video→video (sửa video theo video nguồn) cho shot timelapse hoặc shot mang dữ kiện; video AI chỉ cho minh hoạ M-d. T3 không hồi tố (giữ §15 (i)) (duyệt 23/10/2026 21:45, Q2; 23/10/2026 23:45).\n'
 '- (d) tiếp — phép (iii) và tấm nền T4: phép (iii) giữ T9b ≤ 2 % mỗi chiều + 0 báo mô hình (D11 = LỖI ẢNH: lỗi ở tấm AI — bờ lấn sông, không nới luật; phản chiếu trên mặt nước chờ khung đáp án của phiên K, K1174-D1 = A). Tấm nền T4 chỉ dùng OpenAI `gpt-image-2.5-sunburst-2026-09-08` và chỉ cho cảnh 2026 ban ngày; cảnh 1666 ban ngày chờ K-1.17.5 (khói bếp ghép bằng cộng hiệu có/không khói, K định cách đo (i)/(iv) — V3 = a; khớp màu cục bộ vòng bảo vệ vật nhỏ — V4 = b); cảnh đêm/lửa không dùng tấm nền. Mục tiêu tấm nền cho animatic 5–15 % thời lượng (thay mục tiêu 35–45 % của 23/10 23:45 và dòng "≤ 15 %" của D11 17:42) tới khi K-1.17.5 xong (duyệt 24/10/2026, V1 = d + b, V3 = a, V4 = b, V7 = b; K1174-D1 = A).\n'))
# 6. §15 (j) phủ bề mặt nhà thường — ĐANG THỬ
a = '- (i) T3 (luật N2 §14.1): được dùng minh hoạ AI theo đúng nguyên tắc (f), ≤ 20 % thời lượng — chủ dự án mở cho vòng sửa T3 ngày 21/10 21:15 (5 đoạn: Rodney dỡ hàng Old Mole 1780, hái rau dại 1780, dân rời phố 8/1704, phố cháy đêm 4/1781, cận chân người qua đường băng 2026).\n'
E.append((a, a + '- (j) **Phủ bề mặt nhà thường bằng AI — ĐANG THỬ, CHƯA ÁP.** Phạm vi thử (T4, phương án B): AI chỉ phủ BỀ MẶT mái/tường của nhà thường; giữ nguyên hình khối, vị trí và số nhà. Công trình có tên, lửa/khói, sông và bờ vẫn từ render 3D (lớp (a)). Điều kiện áp: (1) phiên K-1.17.5 viết phép kiểm hình học/cạnh cho phủ bề mặt nhà; (2) một vòng thử qua phép đó và cổng (c); (3) chủ dự án duyệt kết quả. Đạt đủ ba điều kiện thì áp ở bản cuối; tới lúc đó nhà thường thuộc lớp (a) như (a)(b) ở trên. Animatic T4 dựng bằng look V2 (§14.7 Look T4) không chờ vòng thử này (phương án A) (duyệt 24/10/2026 06:21, "A+B theo khuyến nghị").\n'))
# 7. §19 ghi chú D5 + luật 3
a = '- Lửa/khói T4 (D5): lửa/khói cách A (atlas nướng sẵn) cho cảnh rộng; Cycles GPU chỉ 3–4 cận đêm (≈ 30–40 s); không ghép A↔B trong một cú máy (§14.2); nếu Cycles ngày không sửa được mép thể tích → chỉ A.'
E.append((a, a + '\n- Cập nhật 24/10/2026: T4 không dùng Cycles GPU — lửa/khói mọi khung bằng cách A mới (§14.2, §14.7 Look T4); dòng D5 trên thay bằng dòng này. Luật (3) cho T4: điểm máy xương sống P1 đọc lại từ `channel-k2/k2c-t4-02/look/CHON-V2.json` (fov 36°) (duyệt 23/10/2026 23:27, L5; 24/10/2026, V2 = a, V5 = b).'))
for o, n in E:
    c = s.count(o)
    if c != 1: sys.exit(f'CHẶN: chuỗi gốc xuất hiện {c} lần: {o[:80]}')
    s = s.replace(o, n)
open(P, 'w', encoding='utf-8', newline='').write(s)
print('sau', hashlib.sha256(s.encode()).hexdigest())
