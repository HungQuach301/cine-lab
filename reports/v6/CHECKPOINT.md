# V6 — CHECKPOINT 08:05 UTC 18/10/2026 (nhánh thật: `ccr-0e3bf8dd-nst2mv`; lệnh yêu cầu `v6` — harness buộc tên này)

Nhánh = origin/ccr-8f16467a-mhu954 (V5b-2d @1eecfec2) + merge --no-ff pt3-van-nuong @685f11bb, pt4-song @5a7c9a27, claude/checks-v1-15-1qzf9z @001ee5d (0 xung đột); `checks/lock.py --verify` KHỚP 1.15.0 f4fa0349….

## Đã xong (mã đã đẩy)
1. **Ánh sáng V6** (design/k2v/tl/light6.js): bóng khít khung 8192², SSAO hai tầng qua lượt pháp tuyến uMask 2, chỉnh màu V6. Tắt V6 → khung V5b-2d bit-giống (lệch 0,0).
2. **Người/quân có khớp** (people.js; units/life nhánh V6): chu kỳ đi, tricorn liền, quân phục theo vai, LOD, đội hình + sĩ quan, khối hành quân.
3. **Khói giả thể tích** (smoke6.js) + cây vườn nhiều cụm (props.js).
4. **HC7 King's Bastion** (scripts/k2tl/v6_hc7_kb.py → design/k2v/tl/data/hc7-kb-detail.jpg, fort.js), nhãn vân AI 38 px dưới-trái (text.js, record.js, scripts/k2/lib/k2.js), `ai_texture` theo khung (chỉ pha orbit 5,4–12,6 s).
5. **Cảnh theo cặp** eo6/vinh6/pho6/toan6/bo6 (máy chọn bằng số đo mặt nạ); phố đổ nát vùng "THE RUINS OF GIBRALTAR" (ruins.js, data/ruins-zone-1782.json); pin nổi theo bản khắc (ships6.js); nước phản chiếu + sóng; V2D-5 tách sườn > 30 m.
6. **6 khung cổng bản SẢN XUẤT** đã dựng đủ 1080p + mặt nạ + lượt không lửa P6 (ngoài git); đo lần 1 → reports/v6/do/6-khung-sx.json (bão hoà trung vị 0,400 < V5b-2d 0,412 → đã nâng vib 0,62 → 0,78 trong 5 cảnh, CHƯA dựng lại; pho6 đổi máy).
7. **Bản TỐT NHẤT Cycles chạy thử P4**: xuất 204 vật / 1,01 M tam giác (32 s) → Cycles 96 spp 2 luồng 330 s → ghép → chỉnh màu k2v. Blender 5.2 bpy KHÔNG ghi DiffCol/Depth vào EXR → thêm lượt phụ phát xạ 4 spp (5 s) cho albedo GI + độ sâu (cy6.py, cy6_ghep.py).
8. reports/v6/blind_v6.py (chấm mù 3 bản) viết xong, chưa chạy.

## Đang dở
- TỐT NHẤT: cờ ngược sáng ra đen trong bản Cycles → thêm vải xuyên sáng cho cờ; rồi 5 khung cổng còn lại + 2 khung neo.
- Dựng lại 6 khung SẢN XUẤT (vib 0,78, máy P3 mới) rồi đo lại.
- **Khung neo** (phiên con, design/pt/song/*6.py, reports/v6/khung-neo/): nền A dựng xong, sprite người V6 1782 xong, 1943 đang dựng; tấm C 1943 lần 3 (mặt nạ đất xa) đã sinh 1 lệnh $0,063 + kiểm dữ kiện.

## Chưa làm
Bước 7 chạy Cycles 6+2 khung · đoạn thử 540p qua dây chuyền k2 (reports/v6/doan-thu/episode.yaml đã viết) · k2check 1.15 · đo + chấm mù 3 bản · tờ so · golden steel/ll08 · báo cáo V6.

## Tệp lớn NGOÀI git (mất khi container bị thu hồi)
| Đường dẫn | Cỡ | SHA-256 (16) | Tái tạo |
|---|---|---|---|
| /var/tmp/cine-out/k2tl-cache | 1,1 GB | nguồn thô KHỚP sha256.txt V5b-1 | fetch_sources.py; fetch_osm.py; build_rasters/vectors/scene --ao --far --cls; build_border.py; pack_1782.sh origin/p-1810 (cần pip shapely, imagecodecs; git fetch origin v5a) ≈ 4 phút |
| /var/tmp/cine-out/v6/khung/sach-1/00048.jpg | 0,91 MB | 708dceb589225d0e | bash scripts/k2tl/v6_khung.sh (≈ 25 phút, 6 khung) |
| …/sach-2/00072.jpg | 1,06 MB | e516303e061a8f05 | như trên |
| …/sach-3/00096.jpg | 0,90 MB | 7c6bf9a97b204bd2 | như trên |
| …/sach-4/00192.jpg | 0,99 MB | d7c615c8ed896c79 | như trên |
| …/sach-5/00072.jpg | 1,01 MB | 6866fe306ff1c56a | như trên |
| …/sach-6/00072.jpg | 0,89 MB | 65ce31fa2a82adb4 | như trên |
| /var/tmp/cine-out/v6/cy/x4-cy.exr (+ -aux.exr, x4/ xuất 300 MB) | 42 MB | ba7c58df957178b3 | node scripts/k2tl/export6.js export --scene vinh6 --f 192 --out …/x4; /opt/bpy/bin/python scripts/k2tl/cy6.py -- …/x4 …/x4-cy.exr --spp 96 --threads 2 --cc0 …/cc0 (≈ 6 phút) |
| /var/tmp/cine-out/v6/tot/tot-4.png (thử, cờ đen) | 5,0 MB | 92e719d14bfd808f | cy6_ghep.py + export6.js grade |
| /var/tmp/v6kn/bg, spr1782, spr1943 | 242 + 69 + 167 MB | (nền A + tờ sprite khung neo) | design/pt/README + design/pt/song/mh_people6.py (≈ 1,5–2 h máy) |
| /var/tmp/pt/texA (9 vân Poly Haven), /var/tmp/pt/ghost | 115 MB | SHA khớp reports/pt/giay-phep/polyhaven-files.json | như PT4 §2.1 |
| /var/tmp/cine-out/v6/src/dw/leaf373.jp2 | 1,1 MB | e3a2e3b0181f14f3 | IA historyoflatesie00drin_jp2.zip/…_0373.jp2 (PD) |
| /var/tmp/cine-out/v6/src/rijks/r19249.jpg | 5,1 MB | 3fb24fc6210b9c80 (khớp tệp quyền) | iiif.micr.io/saQvn (CC0) |

## Chi phí lũy kế (thật)
- Claude API: **$0,037** (1 lệnh kiểm đường gọi; reports/v6/log/claude-cost.jsonl) — phiên con chưa chấm mù.
- OpenAI: **$0,063** (1 lệnh tấm C 1943 lần 3; reports/v6/khung-neo/ai-c/goi-api.jsonl).
- YouTube 0 · ElevenLabs 0.
- Giờ máy: đồng hồ tường ≈ 06:00 → 08:05 UTC ≈ 2,1 h (bản 07:36 ghi nhầm mốc đầu 05:37); tải CPU song song (llvmpipe phiên chính + 2 Blender phiên con) ≈ 4 nhân bận phần lớn thời gian.
