# CHECKPOINT — KHEP-T3 (23/10/2026)

Nhánh làm việc: `k2c-t3-khep` (từ origin/main @9852adf5). Nhánh bộ khung `ccr-e05d9102-klug8w` không dùng (lệnh chủ dự án nêu rõ nhánh).

## Trạng thái
- 06:19 UTC bắt đầu; hook preflight (pre-commit, pre-push) đã cài trước lần đẩy đầu.
- Master T3 tải qua media.githubusercontent.com: SHA-256 `5b9f0bcc…7b682` KHỚP.
- Giọng master `T3-loi-G1-v42-14LUFS.wav` + nhạc kéo LFS được.
- Bộ đệm cảnh `cuoi_cache.sh` đang chạy (lần 1 lỗi: thiếu ref `origin/v5a` cho LUT A → `git fetch origin v5a`, chạy lại).
- Kế tiếp: nướng lightmap b1704, b1900, b1940, b2026 (đúng `anim_nuong.sh`) → dựng 3 điểm máy dọc 1080×1920 → ghép.
- Đoạn Cycles chọn: master 347,0–351,3 s (N2.9), cắt 608×1080 tại x = 760, phóng 1,776× lên 1080×1920.

## Lệnh bổ sung đã áp
- (chưa có)

## Tệp ngoài git
| Tệp | Tái tạo |
|---|---|
| `/var/tmp/cine-out/k2tl-cache/` | `bash scripts/k2tl/cuoi_cache.sh` (cần `git fetch origin v5a`) |
| lightmap | `NUONG_META=reports/khep-t3/do bash scripts/k2tl/anim_nuong.sh b1704 b1900 b1940 b2026` |
| master T3 | `https://media.githubusercontent.com/media/HungQuach301/cine-lab/release-k2-t3-g2/k2-t3-v1-master.mp4` (SHA `5b9f0bcc…`) |
