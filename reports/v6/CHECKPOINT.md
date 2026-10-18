# V6 — CHECKPOINT 13:20 UTC 18/10/2026 (nhánh thật: `ccr-0e3bf8dd-nst2mv`; lệnh yêu cầu `v6` — harness buộc tên này)

Nhánh = origin/ccr-8f16467a-mhu954 (V5b-2d @1eecfec2) + merge --no-ff pt3-van-nuong @685f11bb, pt4-song @5a7c9a27, claude/checks-v1-15-1qzf9z @001ee5d (0 xung đột); `checks/lock.py --verify` KHỚP 1.15.0 f4fa0349….

## Dừng phiên
- **Phiên bị dừng ≈ 10:35 → 13:01 UTC** (tiến trình worker khởi động lại). Commit cuối trước khi dừng: `c01db111` (10:20). **Không mất tệp**: bộ đệm cảnh, khung SX lượt 4, EXR Cycles và khung TỐT NHẤT (đã chỉnh màu lại) ngoài git vẫn còn → **không phải dựng lại phần nào**.
- Phiên con khung neo dừng ≈ cùng lúc do **hết hạn mức tuần của API** (mở lại 13:00 UTC); công việc dở nằm trong worktree `.claude/worktrees/agent-a277c00f732fc405d` + `/var/tmp/v6kn` (4,6 GB, còn).

## Đã xong (đã đẩy)
1. Ánh sáng V6 (light6.js): bóng khít khung 8192², SSAO 2 tầng, chỉnh màu V6; tắt V6 → V5b-2d bit-giống. Golden steel/ll08 **KHỚP**.
2. Người/quân có khớp (people.js), khói giả thể tích (smoke6.js), cây vườn có nguồn, HC7 King's Bastion + nhãn AI.
3. Cảnh theo cặp eo6/vinh6/pho6/toan6/bo6; phố đổ nát vùng "THE RUINS OF GIBRALTAR"; pin nổi theo bản khắc; nước phản chiếu.
4. **6 khung SẢN XUẤT lượt 4** (vib 0,78; cờ xuyên sáng; nền 1782 đất nện không lưới; hemiK 1,2): bão hoà trung vị 0,418 (V5b-2d 0,412), colorful 77,9 (70,0), cạnh 40,8 (27,5), lửa đỏ 0,048 %.
5. **6 khung TỐT NHẤT (Cycles lai)**: Cycles 96 spp 2 luồng 194–619 s/khung; đã chỉnh màu lại theo nền đất nện (dùng lại EXR Cycles — hình học không đổi). 7 lỗi bộ xuất đã sửa (xem báo cáo §1.7).
6. Chấm mù lượt 1 (trước sửa nền): TỐT NHẤT hạng 1 10/18, SX 2/18, V5b-2d 6/18 ($0,95; reports/v6/kiem-mu-l1).
7. Ảnh sạch (reports/v6/khung: tot-*.png, sx-*.jpg) + tờ so 6 khung. RIGHTS-V6.md. Bản nháp báo cáo V6-BAO-CAO.md.

## Đang dở
- Chấm mù lượt 2 XONG (reports/v6/kiem-mu): TỐT NHẤT hạng 1 11/18, SX 1/18, V5b-2d 6/18; P3, P5 vẫn thua 3/3 (lý do bố cục: phế tích / quảng trường trống — theo lệnh; chờ chủ dự án).
- Đoạn thử 540p: cảnh đinh phải dựng lại toàn bộ với mã mới (đã xoá bản dở cũ); chạy P=1 (RAM).
- Khung neo: chờ phiên con (hạn mức API) — sẽ gửi tin nhắn tiếp tục sau 13:00 UTC hoặc tự thu kết quả đã có.

## Chưa làm
k2check 1.15 trên đoạn thử · ước tính chi phí/giờ máy cả tập + đề xuất mức sản xuất · hoàn tất báo cáo · commit cuối "DỪNG chờ chủ dự án".

## Tệp lớn NGOÀI git
| Đường dẫn | Cỡ | SHA-256 (16) | Tái tạo |
|---|---|---|---|
| /var/tmp/cine-out/k2tl-cache | 1,1 GB | nguồn thô KHỚP sha256.txt V5b-1 | fetch_sources.py; fetch_osm.py; build_rasters/vectors/scene; pack_1782.sh (cần pip shapely, imagecodecs; git fetch origin v5a) ≈ 4 phút |
| /var/tmp/cine-out/v6/khung/sach-1…6 (lượt 4) | 0,9–1,1 MB/khung | b9be173f… 419725f3… 2d16144a… cd686a1e… 6b0a6930… 6350e4e2… | bash scripts/k2tl/v6_khung.sh (≈ 25 phút) — bản sao trong git: reports/v6/khung/sx-*.jpg |
| /var/tmp/cine-out/v6/tot/tot-1…6.png | 5 MB/khung | 83a89dbd… 8fccc255… d319e571… ed498e58… 04a60b02… de97780c… | bash scripts/k2tl/v6_tot.sh (≈ 50 phút; REUSE_CY=1 ≈ 15 phút) — bản PNG RGB tối ưu trong git |
| /var/tmp/cine-out/v6/cy/x*-cy.exr (+ -aux.exr) | 42 MB/khung | — | /opt/bpy/bin/python scripts/k2tl/cy6.py -- <xuất> <ra.exr> --spp 96 --threads 2 --cc0 /var/tmp/cine-out/v6/cc0 |
| /var/tmp/cine-out/v6/cc0/{plaster,stone,ground}_nor.jpg | 14 MB | 2d601a46… 962f9ab9… 6e0ee328… | Poly Haven CC0 2k (sao từ /var/tmp/pt/texA) |
| /var/tmp/v6kn (khung neo phiên con) | 4,6 GB | — | design/pt/song/mh_people6.py + design/pt (≈ 2 h máy) |
| /var/tmp/cine-out/v6/src/dw/leaf373.jp2 | 1,1 MB | e3a2e3b0181f14f3 | IA historyoflatesie00drin (PD) |
| /var/tmp/cine-out/v6/src/rijks/r19249.jpg | 5,1 MB | 3fb24fc6210b9c80 | iiif.micr.io/saQvn (CC0) |

## Chi phí lũy kế (thật)
- Claude API: **$2,254** (kiểm đường gọi $0,037 + chấm mù lượt 1 $0,950 + lượt 2 $1,267).
- OpenAI: **$0,063** (1 lệnh tấm C 1943 lần 3 — phiên con).
- YouTube 0 · ElevenLabs 0.
- Giờ máy: đồng hồ tường hoạt động ≈ 06:00 → 10:35 + 13:01 → 13:05 UTC ≈ **4,6 h** (mốc theo dõi 10 h chưa vượt). Không tính 2,4 h phiên dừng.
