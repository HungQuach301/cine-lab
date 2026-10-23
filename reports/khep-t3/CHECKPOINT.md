# CHECKPOINT — KHEP-T3 (23/10/2026)

Nhánh làm việc: `k2c-t3-khep` (từ origin/main @9852adf5). Nhánh bộ khung `ccr-e05d9102-klug8w` không dùng (lệnh chủ dự án nêu rõ nhánh).

## Trạng thái
- 06:19 UTC bắt đầu; hook preflight (pre-commit, pre-push) đã cài trước lần đẩy đầu.
- Master T3 tải qua media.githubusercontent.com: SHA-256 `5b9f0bcc…7b682` KHỚP.
- Giọng master `T3-loi-G1-v42-14LUFS.wav` + nhạc kéo LFS được.
- Bộ đệm cảnh `cuoi_cache.sh` đang chạy (lần 1 lỗi: thiếu ref `origin/v5a` cho LUT A → `git fetch origin v5a`, chạy lại).
- 06:33 nướng lại (lần 1 hỏng: Blender thiếu `imageio` → `/opt/bpy/bin/python -m pip install imageio`).
- Góc dọc chốt (thử không lightmap, `thu/`): A/E D7 p[470,340,1000]→l[260,0,−350] fov 60; B vịnh p[−2500,1000,1500]→l[−200,0,−1750] fov 58; D Línea p[−200,95,1250]→l[70,60,−600] fov 60.
- Mã: `scripts/k2tl/khep_short.py` (heroes/dung/loi/tron/ghep/do). `loi` xong (10 câu, ASR khớp chữ khoá 10/10); `tron` thử: −14,0 LUFS, −1,4 dBTP sau AAC.
- Sổ: AUTHORSHIP +3 dòng (10:57, 12:49, 13:06), BAI-HOC-K2 K32.
- Kế tiếp (cũ): nướng lightmap b1704, b1900, b1940, b2026 (đúng `anim_nuong.sh`) → dựng 3 điểm máy dọc 1080×1920 → ghép.
- Đoạn Cycles chọn: master 347,0–351,3 s (N2.9), cắt 608×1080 tại x = 760, phóng 1,776× lên 1080×1920.

## Lệnh bổ sung đã áp
- (chưa có)

## Tệp ngoài git
| Tệp | Tái tạo |
|---|---|
| `/var/tmp/cine-out/k2tl-cache/` | `bash scripts/k2tl/cuoi_cache.sh` (cần `git fetch origin v5a`) |
| lightmap | `NUONG_META=reports/khep-t3/do bash scripts/k2tl/anim_nuong.sh b1704 b1900 b1940 b2026` |
| master T3 | `https://media.githubusercontent.com/media/HungQuach301/cine-lab/release-k2-t3-g2/k2-t3-v1-master.mp4` (SHA `5b9f0bcc…`) |

## Trạng thái (07:12 UTC)
- Lightmap b2026 XONG 07:00 (1 646 s; meta khớp bản cuối, p99,5 lệch ≤ 1,1e-5) → `reports/khep-t3/do/nuong-b2026.json`. Đang nướng b1704 → b1940 → b1900.
- Dựng A (101 khung) + E (324 khung) 1080×1920 SPP 4 từ 07:00, ≈ 9 s/khung/luồng; hàng chờ: B sau A (cần b1704), D sau E (cần b1940, b1900). PGID: dung 11389/11479, hàng 14308/14309.
- Sửa lệch ngoài vùng: `cuoi_cache.sh` ghi đè `reports/v7b/do/mau-nha.json` (osm_the_mau 47 → 54 do OSM tải lại hôm nay) → đã `git checkout` trả lại; ghi chênh lệch trong báo cáo.

## Trạng thái (07:58 UTC)
- Dựng xong: A 07:16 (946 s), E 07:37 (2 243 s), B 07:55 (1 166 s). Lightmap b1704 XONG (2 127 s). Đang nướng b1940 → b1900; D tự chạy khi đủ.
