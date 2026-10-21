Nhánh thật: **`ccr-d189108f-6mcz9k`** (harness buộc tên này; lệnh gọi `k2c-t3-animatic`). Gốc V7C `origin/claude/v7c-layout-density-qg4mng` @`47a0f55a` → `git merge --no-ff origin/main` @`bc7e96d1` (P-2010b): **0 xung đột**. Không merge `main`, không đụng nhánh khác.

# ANIMATIC-T3 — Gibraltar: khoá look + animatic CẢ TẬP. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt

```text
ĐIỀU LỆ                                   | thực tế
Bước 0: main ≥ bc7e96d1 + P-2010b          | origin/main = bc7e96d1, có P2010B-BAO-CAO.md + am-thanh/master/ → làm tiếp
lock.py --verify                           | KHỚP 1.16.1 a3c39873… (đầu phiên, sau merge, trước k2check; chỉ --verify)
LOI-KHOA.sha256                            | 3/3 OK; loi-khoa.txt 51d1c773… không sửa
Vùng sửa                                   | design/k2v/**, scripts/k2tl/**, channel-k2/k2c-t3-01/animatic/**, LOOK-KHOA.md (mới), reports/animatic-t3/**
KHÔNG sửa                                  | checks/, docs/, assets/, am-thanh/**, khoa-loi/**, sổ RIGHTS/AUTHORSHIP/COST-LEDGER, main — đúng
0 AI sinh điểm ảnh                         | đúng (ai_image/ai_texture = false mọi shot; OpenAI $0)
RunPod / ElevenLabs / Gemini / YouTube     | 0 / 0 ký tự / 0 / 0 (prep chạy với proxy chặn → EL bị chặn mạng, kể cả đọc bộ đếm)
Email / khoá                               | 0 email trong diff (preflight mọi commit ĐẠT); UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)"; không in/ghi khoá
Dừng tiến trình                            | theo PGID ghi ra tệp (BAI-HOC #41); không pkill theo chuỗi
Lệnh bổ sung 21/10 16:00                   | CHECKPOINT tự đẩy mỗi 25 phút (anim_ckpt.sh); không sửa design/k2v/tl/*.js sau lệnh; không dừng lượt dựng
```

| Việc | Kết quả |
|---|---|
| 0. LOOK-KHOA.md | 5 quyết định chép nguyên văn + thông số tái lập (cách A, 7 lightmap theo mốc, chỉnh màu, khung lai, đêm lửa) + 10 khung tham chiếu kèm SHA. Commit `db00ee1c` (đẩy ngay). SHA-256 tệp hiện tại `72add9b31ba3445348fe0ee20b5b5a3b722d237683971175f5ec99b39a8d38ec` |
| 1. Bảng shot | **43 shot + 2 thẻ phương pháp = 761,000 s** (thân phim 745,000 s = phương án B, mốc từng câu từ `reports/kl42/nhip-that.json`). `channel-k2/k2c-t3-01/animatic/bang-shot.md` + `episode.yaml` (sinh bởi `mk_ep_anim.py`) |
| 2. Lightmap | Nướng lại **7 mốc** (b1704, b1779, b1781r, b1782 + lửa, b1900, b1940, b2026): **16 190 s ≈ 4,5 h** đồng hồ (chạy chồng với dựng) |
| 3. Đo sớm | lai ngày **2,16** · cận phố **3,44** · đêm lửa **3,10** · neo **3,64** s/khung (960×540, spp 4, máy có nướng song song). Ghi CHECKPOINT trước khi dựng tiếp |
| 4. Animatic | Master 960×540 24 fps **761,000 s**, ngoài git, SHA `fa0f32f2…ef203`. Giọng master G1 LFS (SHA `ba50fba7…` khớp) + nhạc B (KA2026 = cue A8); **−14,0 LUFS · −1,3 dBTP sau AAC · SMR p10 19,7 dB**. 5 thẻ chương, bộ đếm suốt tập, 2 thẻ × 8 s cuối. Cú lặn: clip NC-GPU **giữ chỗ — bản cuối dựng Cycles GPU (G0)** |
| 5. LOOK-4 | Soát 1 khung/2 s (381 khung) trên master; sửa 14 shot qua 4 lượt soi + 1 lượt soát master (§5). **Còn 1 lỗi**: mảng nước xanh nhạt ở vùng đất lấn chưa xây (N4.3, N5.5 giây 714, C4 cận) — cần sửa shader, mã đang khoá |
| 6. Q3 | Có nguồn: **8/8 trích khớp nguyên văn** tệp SHA đăng ký (Drinkwater 1786 tr. 107–109; Ancell 1784 thư 9/9/1780; Spilsbury 27/10/1779 + bảng khẩu phần tr. 121). Hình chỉ dùng vật có nguồn đã có (§6) |
| 7. Xuất | 8 tệp xem theo chương 640×360 (**4,65–4,81 MB**), tờ khung 45 ô (0,87 MB), PHIEU-XEM.md, bản kiểm có phụ đề (ngoài git) |
| 8. Tự đo | §8. XEM CÂM 3 AI (tham khảo): P đọc lại **31/48** (từ khoá 42/48). k2check 1.16.1 `--cap`: TRƯỢT tập — 8 hàng Chặn còn lại (§8.3) |
| Giờ máy / chi phí | ≈ **13,5 h** đồng hồ (mốc 16 h) · Claude API **$0,75** (mốc $10) · OpenAI **$0** (mốc $3) · RunPod/EL/Gemini/YouTube 0 |

**Xem nhanh:** `reports/animatic-t3/PHIEU-XEM.md` → mở `reports/animatic-t3/xem/01-mo-dau.mp4` … `08-ch5b-ket.mp4` theo thứ tự; tờ khung `reports/animatic-t3/to-khung.jpg`.

## §1 LOOK-KHOA
- Tệp: `channel-k2/k2c-t3-01/LOOK-KHOA.md` (commit đầu `db00ee1c`, SHA tệp `72add9b3…38ec`). Phiên P sau ghi Kinh thánh §14.7.
- Giữ nguyên chỉnh màu V7B/V7C/NC-CPU (ACES → LUT `k2-a-thep-lanh` → V6 grade [1,0,35,0,6] → vibrance 0,78). Sương σ = 1/16 km.
- Khung lai V7C không có thông số máy trong git (chỉ ảnh) → LOOK-KHOA ghi thông số theo quy tắc (nhìn xuống 12–25°, trời 8–20 %, AGL 150–450 m, FOV 34–46°) và thông số máy thật từng shot nằm trong bảng shot.
- Hai lưu ý ghi trong LOOK-KHOA (đọc từ chính khung tham chiếu): `lai/cong-vay-ham.png` có lều xếp ô và không có Rock; `nc-cpu/khung/A/cong-toan-canh.jpg` có viền đỏ quanh tàu. Animatic lấy bố cục/độ thật, không lấy các lỗi này.

## §2 Bảng shot (`channel-k2/k2c-t3-01/animatic/bang-shot.md`)
- 43 shot: bảng 42 shot `reports/v7p/diem-may.md` §2 + **KA2026 tách khỏi N5.5** thành khung neo riêng, ghép cặp then/now với KA1782. **N2.10 (hầm Ince) đứng sau KA1782** đúng thứ tự lời v4.2.
- Mỗi dòng có: mã, mốc giây, điểm máy, kiểu khung (lai/chặt/đêm/neo/lai+lặn), nhìn xuống (°), AGL, lightmap, thời gian chạy trong shot, vai, vật mang nghĩa (§13.2), nguồn/bậc. Mã máy (log, đoạn) dùng gạch dưới (`N1_1`), mã người đọc dùng chấm (`N1.1`).
- Kiểu khung theo thời lượng (thân 745 s): lai ≈ 82,5 % có thời gian chạy; khung chặt có vai 8,5 % (cờ 1704, cận người hái rau, vách hầm, H2 cờ); khung neo 6,8 %; đêm lửa (H2T) 0,7 %; cú lặn giữ chỗ 1,5 %.
- **Cú lặn 13/9/1782 đặt ở N2.9** (lời 2m–2n "By the next afternoon all ten batteries were lost…"): 0 → 16,5 s cách A (pin nổi vào vị trí, khai hoả, máy khớp khung đầu clip); 16,5 → 28,0 s clip `reports/nc-gpu/lan/ncg-lan-xem.mp4` (5,5 → 17,0 s: chiều → đêm cháy → trước rạng sáng). Bộ đếm vẽ đè theo đúng giờ clip. Log: `reports/animatic-t3/do/lan-ghep.json` ("giữ chỗ — bản cuối dựng Cycles GPU (G0)").
- 5 thẻ chương (§13.3, ≤ 3 s, ngoài móc): `1704 — The Rock changes hands` · `1779 — The Great Siege` · `1783 — The neutral ground` · `1939 — A runway on the sand` · `1969 — The gate closes`. **Chữ 4 thẻ mới là quyết định sáng tạo chờ chủ dự án duyệt.**
- Vật mới (mã `design/k2v/tl/san_bay.js`, `tl7.js`, `t3tl.js`), tất cả ghi bậc trong log: dải cỏ 1934 (năm: lời 3h; vị trí bậc 5), 650 máy bay khối minh hoạ (số: lời 4i bậc 2; hình/bố trí bậc 5, chờ D3), hàng rào mới 2026 lệch 6 m (lời 5h; vị trí bậc 5), lều trại "tự nhiên" (lệch hàng/xoay/sắc vải — số lều không đổi).
- Chỗ GIỮ CHỖ (chưa có nguồn/khối dựng): mặt cắt hầm M11 (N2.10, N4.2); lớp "mép đất Anh 1810–60" (N3.2); trại/vườn/trường bắn/trường đua 1909–30 (N3.4); vị trí hàng rào mới 2026; mô hình máy bay 1942; bản đồ 1705/1943 phủ khớp (chưa nắn khớp).

## §3 Lightmap (Cycles CPU, 1333 × 2167 texel, 3 m, 24 spp; meta `reports/animatic-t3/do/nuong-*.json`)
| Lightmap | Mốc | Giây đồng hồ (log) | Giây nướng (meta: trời · nảy · nắng · lửa) |
|---|---|---|---|
| b1779 | 15/1/1780 12:00 | 1 435 | 1 270 (377 · 360 · 521) |
| b1782 | 13/9/1782 15:30 + lửa | 2 467 | 2 240 (471 · 309 · 595 · 851) |
| b2026 | 19/10/2026 12:00 | 2 634 | 2 477 (1 065 · 565 · 833) |
| b1704 | 3/8/1704 12:00 | 2 178 | 2 036 (842 · 522 · 657) |
| b1781r | 1/7/1781 12:00 | 2 186 | 2 035 (870 · 500 · 652) |
| b1940 | 1/6/1940 11:00 | 2 651 | 2 491 (980 · 661 · 834) |
| b1900 | 1/6/1910 12:00 | 2 639 | 2 485 (1 015 · 679 · 776) |
| **Tổng** | | **16 190 s ≈ 4,5 h** | |
Hai mốc mới so V7C: b1704, b1900. Mỗi shot nạp các lightmap có cửa sổ năm giao đường thời gian của shot (`nc_for` trong `mk_ep_anim.py`).

## §4 s/khung, giờ máy, ước bản cuối
- Đo (log `heroes-gio.log`, 960×540 spp 4, mỗi tiến trình, máy 4 nhân có nướng/dựng song song): 2,2–4,7 s/khung, TB 12 cảnh cuối ≈ 4,3 (P = 3). Render đoạn (chữ + ghép) 0,26–0,52 s/khung; ghép master 24–25 phút.
- **Giờ máy thật ≈ 13,5 h đồng hồ** (00:20 → 13:50 UTC; gồm khởi động lại container lúc 01:17): bộ đệm + vân 0,2 · soi bố cục 4 lượt 1,5 · nướng 4,5 (chồng) · dựng cảnh đinh 8,3 (48 lượt cảnh = 22,4 h tiến trình, gồm 1 h bỏ do sửa nước LOOK-4) · render đoạn + ghép 2 lượt 1,5 · xuất/đo/k2check 0,6.
- **Ước bản cuối 1080p (G0):** 18 264 khung × ≈ 3,5 s (540p) × ≈ 3,5 (4 lần điểm ảnh, spp 4) ≈ **62 h CPU ± 25 %** cho phần cách A (V7C ước 54 h ± 25 % cho 595 s) + nướng đã có (dùng lại nếu không đổi mã cảnh) + cú lặn/cận đêm Cycles GPU (NC-GPU G0 ≈ 44 h GPU ≈ $52). ≈ 7 gói × ≤ 10 h song song.
- Bài học vận hành: dấu (stamp) cảnh `tl/*` băm **toàn bộ** `design/k2v/tl/*.js` → mọi sửa mã dựng lại mọi cảnh (mất ≈ 1 h ở lượt C1–C4 khi sửa nước). Đã chốt mã trước đợt dựng 02:25.

## §5 LOOK-4 — sửa trên từng shot
Soi bố cục 4 lượt (tắt cách A, 480×270, đầu/giữa/cuối shot) + soát master 1 khung/2 s (381 khung, `reports/animatic-t3/do/` + tờ ngoài git `look4/to-*.jpg`).

| Lỗi LOOK-4 | Shot | Sửa |
|---|---|---|
| Cảnh 2026 mở đầu mất Rock (V7C giây 4) | H1 | máy D7 lùi bắc 650 m, nhìn xuống 14° → Rock nguyên khối 0–12 s |
| Khung nhìn thẳng xuống như bàn cờ (V7C giây 60, 100) | C1 (U1), C4 (Bm2 + cận Old Mole 45°) | C1 → khung lai nhìn bắc 16°; C4 → lai 13° + cận Old Mole xiên 17° |
| Khung chỉ còn mặt nước (V7C giây 68–76) | C2; N2.8 | C2 → máy E của V7B-a (tham chiếu duyệt); N2.8 → gần hơn, 36°, hạm đội trước Rock |
| Lều trắng xếp ô như bàn cờ | C1, N2.11, N5.6 | `campTuNhien`: lều lệch hàng ±2,5 m + gợn dọc dãy, xoay ±26°, 5 sắc vải tối hơn, dải đất giẫm mờ 0,12. **Bớt rõ, chưa hết** khối chữ nhật khi nhìn xa > 700 m (dãy trại theo Faden là khối thật) |
| Rock bị cắt mép khung | N1.5, N1.6, N3.1, N3.5, N4.1, N4.2, N5.1, N5.5 (đầu), N2.10 | xoay/lùi máy; N2.10 lùi để cả khối Rock trong khung |
| Viền xanh nhạt quanh bờ / bọt trắng thành vệt | mọi cảnh có nước (rõ ở C3, C4) | `nc/up.js`: bờ theo thời kỳ (1790/1940/2026) + bỏ điểm "đất" cao độ ≤ 0,2 m khỏi khoảng cách bờ (hết vệt bọt thẳng giữa vịnh theo đê hiện đại); dải nông 38 → 18 m; bọt 0,75 → 0,5 |
| **CÒN**: mảng nước xanh nhạt phẳng ở vùng đất lấn CHƯA xây (địa hình dưới mặt nước hiện qua) | N4.3 (giây 526–532), N5.5 (giây 714), C4 cận (mép trái) | chưa sửa — nằm ở shader địa hình (`terrain.js`/`up.js`), mã khoá theo lệnh 16:00. Đề xuất AT-D1 |

Ngoài LOOK-4, đã sửa theo LOOK-5 (người xem hiểu được): người/Línea/hạm đội quá nhỏ (N1.4, N1.6, N2.7, N2.8), đêm tối sớm làm mất hình (N4.5, N5.3), khung neo tầm mắt ở tư thế G1b chỉ thấy tường/quảng trường trống → KA nâng 60 m (phố đổ nát 9/1782 ↔ phố dày 2026), KB nâng 30 m; KC giữ tầm mắt.

## §6 Q3 "vì sao đói" (V7C 3/6)
Nguồn đã đăng ký SHA (tải lại `archive.org …_djvu.txt`, SHA-256 khớp 3/3: Drinkwater 1786 `7576bb8f…`, Spilsbury `f6c2f3a9…`, Ancell `67d61d0a…`). Kiểm bằng máy `reports/animatic-t3/q3_trich.py` → `q3-trich.json`: **8/8 đoạn khớp nguyên văn** (OCR giữ chính tả, chỉ nối dòng).

- Drinkwater 1786, **tr. 108** (1/1780): *"Few fupplies arriving from Barbary, and t^ere appearing little profpecl of relief from England, famine began to prefent itfelf with its attendant horrors"*; *"thif- tles, dandelion, wild leeks, &c. were for fome time the daily nouriihment of numbers."*
- Drinkwater 1786, **tr. 108–109**: *"Not only bread, but every article neceflary to the fupport of life, was hard to be pro- cured, and only to be purchafed at exorbi- tant prices. Veal, mutton, and beef, fold from two (hillings and fix-pence, to four Shillings per pound … fowls, eighteen {hillings per couple-ducks, a'gui- nea … a fmall cabbage coft one (hil- ling and fix-pence …"* ; tr. 109: *"eggs,, fix-pence each"*.
- Drinkwater 1786, **tr. 107**: bánh mì hạn mức, *"fen- tries were placed at the wickets where it was delivered"*; *"numbers of women, children, and in- firm perfons, returned … frequently without tafting, for fome days"*.
- Ancell 1784, thư 9/9/1780 (trang OCR không đọc được, dấu "( H )"): *"The enemy keeps our port blockaded … much clofer than ever"*; *"We have not received an ox from Barbary fince^June 12th, and every fpecies of provifion is now at a moft extravagant price"*.
- Spilsbury, 27/10/1779 (bản 1908, trang không xác định trong OCR): *"Rice sold at 21 dollars 6 realy per ewt., raised five tines the usual price. Little fresh meat now."*; tr. 121: bảng *"ALLOWANCE OF PROVISIONS FOR ONE MAN IN THE GARRISON OF GIBRALTAR, FROM 7 TO 28 DAYS."*

Áp dụng trong animatic (chỉ vật có nguồn đã có, không thêm vật/chữ mới): giữ thứ tự **C2 thuyền từ châu Phi (Barbary) bị hàng chặn quay lại → C3 cận người hái rau dại** liền nhau (chuỗi nhân quả đúng câu Drinkwater tr. 108). Xem câm AI: Q3 P-đọc **3/6** (cả 3 người đoán "blockade/siege cut off supplies" nhưng rào "not sure") — chưa cải thiện so V7C. Không đưa giá/khẩu phần lên hình (TL-4); nguồn giá để lời/mô tả/bình luận ghim nếu chủ dự án muốn (đề xuất AT-D4).

## §7 Tệp xem (đường dẫn + SHA-256; `reports/animatic-t3/do/sha-xem.txt`)
| Tệp | Nơi | Cỡ | SHA-256 |
|---|---|---|---|
| 01 Mở đầu (0:00–0:43.8) | `reports/animatic-t3/xem/01-mo-dau.mp4` | 4,65 MB | `dfbce5959b49d60da408369543024ddf2bf912aae62f5d7b9b823e4b1fa1cde4` |
| 02 Chương 1 (0:43.8–2:53.1) | `…/xem/02-ch1-rock-1704.mp4` | 4,75 MB | `433c9adb04f33d7cd2b3aaa11382d3ff0498f52abb7415e12fc9a76b0334c34c` |
| 03 Chương 2a (2:53.1–4:22.2) | `…/xem/03-ch2a-vay-ham.mp4` | 4,78 MB | `f9f119b6882ce41e9ee69b0e09d1d2a2f9221d24feec40da36d108154a80dd45` |
| 04 Chương 2b (4:22.2–6:22.6) | `…/xem/04-ch2b-tan-cong-1782.mp4` | 4,80 MB | `d23f0347ffc5f5f4ad398a489f94cbe43833a4932a6f98191dd5b567f03d5c39` |
| 05 Chương 3 (6:22.6–7:51.6) | `…/xem/05-ch3-dat-trung-lap.mp4` | 4,81 MB | `f3f217302827ef9bb36ccd05282b498b6c1f17cd9c2c0cea7af9d22e25296e83` |
| 06 Chương 4 (7:51.6–9:45.8) | `…/xem/06-ch4-duong-bang.mp4` | 4,81 MB | `a071f5ec8b9074b7959b250aae7446b823242b0c172afb5a17831964ea171028` |
| 07 Chương 5a (9:45.8–11:06.1) | `…/xem/07-ch5a-cong.mp4` | 4,79 MB | `4c112f755325c197410804ef05248c91dd83f0c66d09cd21fcea106f03dd5864` |
| 08 Chương 5b + thẻ (11:06.1–12:41.0) | `…/xem/08-ch5b-ket.mp4` | 4,75 MB | `d7635a7bf841e24e614a557091da76852a1bb146df5249d6a008355b0bc37fb4` |
| Tờ khung 45 ô (1 khung/shot, mã + mốc) | `reports/animatic-t3/to-khung.jpg` | 0,87 MB | `522012695ff3fc1bf7a7c7640db27632db59aa81db54096a4748333cb9cd53fb` |
| Phiếu xem | `reports/animatic-t3/PHIEU-XEM.md` | — | — |
| **Master 960×540 liền** (không phụ đề) | ngoài git `/var/tmp/cine-out/k2c-t3-anim/k2c-t3-anim-v1-master.mp4` | 710,4 MB | `fa0f32f20295d1a8cf17ebd20910bab1e92a8b69abe272122c5eaf5ead2ef203` |
| Bản KIỂM có phụ đề 640×360 | ngoài git `/var/tmp/cine-out/k2c-t3-anim/xem/k2c-t3-anim-640-phude-KIEM.mp4` | 47,3 MB | `16ef64d043d8e75f48d59429c5317bd8864a9623c0e733e2383098ce81ef90e3` |
| Tiếng cả tập (WAV) | ngoài git `/var/tmp/cine-out/k2c-t3-anim/mix.wav` | — | `805432b5c7e92bfb007be9e08a8780c40099502e33703fbafc55360d504c4acd` |
Bản xem: có giọng + nhạc, không phụ đề; −14,7…−15,7 LUFS (đã hạ −1,2 dB như BAI-HOC #45), đỉnh ≤ −1,5 dBTP. Lượt xuất đầu dùng `alimiter` để mặc định tự bù mức (−12…−13 LUFS) → đã xuất lại với `level=disabled`.

**Tái tạo master:** `bash scripts/k2tl/v7p_cache.sh` → `v7b_mau_nha.py` → `v7b_faden.py` → `anim_tex.py` → `anim_nuong.sh` → `mk_ep_anim.py` → `K2_DRAFT=1 MW=960 build.sh …/animatic/episode.yaml prep` (chặn mạng) → `P=3 anim_vong.sh` → `anim_lan.py <timeline.json> <log>` → `anim_mix.py …/anim-loi.json <out>/mix.wav` → `build.sh … render` → `build.sh … ghep` → `anim_xuat.py <master>`.

## §8 Số đo (ghi số, KHÔNG tự chấm đạt) — `reports/animatic-t3/do/so-do.json`, `k2check-1.16.1.txt`, `xem-cam/ket-qua.json`
### 8.1 Tự đo
| Chỉ số | Số |
|---|---|
| Thời lượng | 761,000 s (thân 745,000 + thẻ 16,0) |
| Loudness master (sau AAC) | **−14,0 LUFS** · LRA 3,1 · đỉnh thật **−1,3 dBTP** · SMR p10 19,7 dB, min 16,6 |
| Cắt/phút (thân 745 s) | 43 shot = **3,46** · tính cả cú cắt sang cú lặn 3,54 · tính 30 bước năm **5,96** · video (k2check) 50 cắt = 3,95 |
| % góc cao có thời gian chạy | tự đo 82,5 % (khung lai) · 87,1 % gồm khung chặt AGL ≥ 120 m · k2check TL-1 **97,0 %** |
| % lướt thấp | tự đo 8,1 % (khai lướt thấp 9,5 s + khung neo 50,5 s) · k2check TL-2 3,0 % (chỉ 3 shot khai thấp) · cú lặn 1,5 % (không tính TL-2, §14.3) |
| Bão hoà / colorfulness / chi tiết trung vị (640×360, y 60–300, 1 khung/2 s, 381 khung) | **0,400** / 67,6 / 13,63 |
### 8.2 XEM CÂM 3 người AI — CHỈ THAM KHẢO (chủ dự án chấm cuối)
`claude -p` Sonnet 5.5, chỉ Read, 190 khung (1/4 s) không phụ đề không tiếng, 8 câu (`scripts/k2tl/anim_cam.py`). Chi phí $0,75.
| Câu | Từ khoá | **P đọc lại** |
|---|---|---|
| Q1 ai giữ Rock sau 1704 | 6 | **6** |
| Q2 1779 bắt đầu gì | 6 | **6** |
| Q3 vì sao đói | 6 | **3** (đoán phong toả, rào "not sure") |
| Q4 cái gì đến cứu | 6 | **4** |
| Q5 biển 9/1782 | 6 | **5** |
| Q6 cái gì được xây trên eo cát | 6 | **6** |
| Q7 cổng 1969 và sau đó | 2 | **1** |
| Q8 cái gì nối hai phố hôm nay | 4 | **0** |
| **Tổng** | 42/48 | **31/48** · độ rõ 3,0/5 |
Lạc chung 3/3: mở đầu đêm 2026 + bước năm 1309–1943 (móc TL-5, như V7B/V7C); dải 1704–1734 "đất trống chỉ đổi năm"; cận người 1/1780 không rõ là đói; cổng 1969/2026 không thấy người dừng/qua lại (người quá nhỏ ở khung lai).

### 8.3 k2check 1.16.1 `--cap` (LOCK KHỚP) — tập TRƯỢT
| Hàng | Kết quả | Ghi |
|---|---|---|
| NHIP-NGHIA | ĐẠT | sau sửa khai báo `nhip-vat.json` (định dạng V7C, mã đoạn gạch dưới) |
| TL-1 | CẢNH BÁO | góc cao + tl 97,0 %; 3,54 cắt/phút đặc tả, 3,95 video |
| TL-2 | ĐẠT | 3,0 % |
| TL-3 | CẢNH BÁO | thiếu `trong_pct` 43 shot (không đo mặt nạ ID ở animatic) |
| CHUONG-1 | ĐẠT | 5 thẻ, dài nhất 3,00 s |
| PP-1 | CẢNH BÁO | 2 thẻ × 8 s, 58 từ (tốc độ đọc) |
| **Q33 / Q33-K2 / Q33 (1.13)** | TRƯỢT (Chặn 2) | N5_1, N4_1 (cùng vùng D ở năm khác) > 2 lần theo pHash — ngữ pháp TL-1 "quay lại cùng điểm máy ở năm khác" |
| **Q37 / NHIP-K2 / Q37 (1.13)** | TRƯỢT | TB 5,21 s/biến cố, dài nhất 12,7 s — ngữ pháp timelapse (như V7B/V7C) |
| **A1–A13** | TRƯỢT (A11) | `mix.json` không có `nhac[]` (trộn bằng `anim_mix.py`/`tron.py`, không qua `compose.py`); A1, A2, A5, A7, A12 ĐẠT |
| **ML1** | TRƯỢT (Chặn 2) | 41/45 shot gắn câu: KB1943, KA2026 (tấm im lặng) + 2 thẻ phương pháp |
| **NC-H1** | TRƯỢT (16) | "có lớp nhà khai 0" — tên trường khai lớp nhà cho cảnh `tl/*` chưa rõ (như V7C-D5) |
| **SACH-1** | TRƯỢT (1) | "không log chữ" (như V7C) |
| **XEM-CAM** | TRƯỢT | chờ chủ dự án chấm tắt tiếng |
| Q26b-K2, O2 | CẢNH BÁO | |

## §9 Chi phí thật
| Khoản | Mốc / chặn | Thật |
|---|---|---|
| Claude API (`claude -p` xem câm) | $10 / dừng $30 | **$0,752** (6 lượt gọi: 3 người × 2 lần chạy — lần đầu khởi động lỗi đường ống) — `reports/animatic-t3/xem-cam/cost.jsonl`. Token của chính phiên này không có số đo trong container |
| OpenAI | $3 | **$0** |
| RunPod / ElevenLabs / Gemini / YouTube | 0 | 0 / 0 ký tự / 0 / 0 |
| Giờ máy | 16 h | **≈ 13,5 h** |

Chặn an toàn: không lỗi nào lặp ≥ 3 lần. Lỗi vận hành (mỗi lỗi 1 lần, đã sửa): chú thích chèn giữa dòng nuốt mã (BAI-HOC #42, Python, bắt bằng lỗi chạy); `alimiter` tự bù mức; trường khai báo k2check sai đường dẫn/mã; container khởi động lại 01:17 (tiến trình mất, đĩa còn — dựng tiếp `--resume`).

## §10 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
- **Bão hoà trung vị 0,400** — đúng ngưỡng ≥ 0,40 (0 %).
- **Thẻ chương 3,00 s** = trần 3 s (0 %), cả 5 thẻ.
- **Thẻ phương pháp ≈ 3 từ/s** (58 từ / 16 s = 3,6 từ/s tính cả tựa; 24 từ/thẻ không tựa = 3,0 = trần) — như ĐÓNG-GÓI-T3.
- **Q33: 13 góc máy "đúng 2 lần"** = trần ≤ 2 (0 %).
- **Loudness −14,0 LUFS** trong dải −15,0…−13,8 (cách mép trên 0,2 LU, ngoài ±5 % của mục tiêu −14,0 thì 0 %).
- Không thêm phần tử nào để vượt chỉ số; số lều, tàu, người theo nguồn/V7C giữ nguyên.

## §11 Quyết định đề xuất
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| AT-D1 | **Sửa shader địa hình**: vùng đất lấn CHƯA xây (năm < năm xây) tô màu nước sâu, không để lộ địa hình dưới mặt nước | hết mảng xanh nhạt LOOK-4 còn lại (N4.3, N5.5, C4) | đổi mã `tl/*` → dựng lại mọi cảnh (≈ 8 h ở 540p) | mọi cảnh có nước trước 2026 | phải kiểm cả đường băng mọc dần (uRecl) |
| AT-D2 | **Q7/Q8 (cổng, người qua lại) có hình**: thêm 2 khung chặt có vai ở cổng (1969 chắn hạ, người dừng; 2026 dòng người qua) ≤ 4 s mỗi khung trong N5.1/N5.3 | XEM CÂM Q7 1/6, Q8 0/6 — chỗ yếu nhất | +8 s lướt thấp (TL-2 còn dư) | chương 5 | cần nguồn kiểu chắn cổng 1969 (bậc 3–4) |
| AT-D3 | **Thống nhất định nghĩa "góc cao" giữa K và LOOK-2**: K đếm TL-1 97 %, tự đo 82,5 % (khung lai 12–15° ở ranh) | số đo không lệch giữa phiên | phải hỏi K | TL-1 | — |
| AT-D4 | **Q3**: đưa 1 câu giá cả có nguồn (Drinkwater tr. 108 "eggs six-pence each" hoặc "ducks, a guinea") vào **mô tả/bình luận ghim**, không lên hình; hình giữ chuỗi C2 → C3 | có nguồn khớp nguyên văn | XEM CÂM tắt tiếng không đổi | đóng gói | — |
| AT-D5 | **Thẻ phương pháp 2, dòng "AI retouched two street frames…"** sai với bản animatic này (0 AI). Giữ chữ đã duyệt cho bản cuối nếu bản cuối có AI; nếu không → sửa dòng | không khẳng định sai về cách làm (§10.6) | đổi chữ đã duyệt | PP2 | — |
| AT-D6 | **Dấu cảnh `tl/*` chỉ băm mã cảnh dùng tới** (hoặc tách `up.js`) — việc của phiên nền tảng | sửa một lớp không dựng lại cả tập | sửa `scripts/k2/prep.py` (ngoài vùng phiên này) | mọi lượt dựng | băm thiếu → giữ khung cũ sai (BAI-HOC #39) |
| AT-D7 | Bài học (phiên P ghi BAI-HOC): stamp băm cả `design/k2v/tl`; `alimiter` mặc định tự bù mức; mã shot có dấu chấm làm k2check không ghép log; khung neo tầm mắt trong phố Gibraltar dữ liệu OSM chỉ thấy tường | tránh lặp | — | BAI-HOC | — |

## §12 Việc chờ chủ dự án
1. **Xem cả phim** theo `reports/animatic-t3/PHIEU-XEM.md` (8 tệp `reports/animatic-t3/xem/`), ghi nhận xét dạng `<mã shot>: …`.
2. **Chấm XEM CÂM** tắt tiếng (§13.4, cần ≥ 6/8) — 8 câu trong `scripts/k2tl/anim_cam.py`; số AI (tham khảo) ở §8.2.
3. **Duyệt quyết định sáng tạo** (ghi AUTHORSHIP qua phiên P): chữ 4 thẻ chương mới; tách KA2026 thành khung neo riêng; KA/KB nâng 60 m/30 m; N5.2 trôi qua cổng sang La Línea (đổi điểm D → H); cú lặn đặt ở N2.9 16,5–28 s; các vật mới bậc 5 (dải cỏ 1934, máy bay khối, hàng rào mới lệch 6 m, lều "tự nhiên").
4. Quyết AT-D1…AT-D6.
5. Phiên P: ghi LOOK-KHOA vào Kinh thánh §14.7; RIGHTS không có tài sản mới (vân Poly Haven CC0 như NC-CPU, nhạc/giọng đã có dòng); merge nhánh khi duyệt. Nhánh này **không** merge.

**DỪNG — chờ chủ dự án.**
