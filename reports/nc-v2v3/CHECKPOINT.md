# CHECKPOINT NC-V2V3 — 2026-10-20 ~10:45 UTC — đang làm
- Mô hình chính: Wan2.2-VACE-Fun-A14B fp8 (Comfy-Org repackaged, Apache-2.0), ComfyUI v0.42.1 trên RunPod RTX 5090; giấy phép nguyên văn ở `giay-phep/`. Ditto sim2real LoRA bị loại (CC BY-NC-SA 4.0).
- Pod 1 (`v1`, 0,23 h, $0,28 ước) đã TẮT: cài + tải trọng số 184 s (SHA khớp 4/4), thử 17 khung 720p chế độ A: 7,3 s/bước.
- Lỗi đã sửa: lượt mái phố (`v2v3City`) đọc trạng thái nước/trời SAU khi ẩn → khung màu từ khung thứ 2 mất trời/nước; nguồn đang dựng lại (`chay_lan.sh`).
- Tiếp: ctrl3.py → bật pod → 6 biến thể theo thứ tự c2-A, c2-B, c4B-B, c4B-A, c1-B, c1-A → đo → chấm mù → báo cáo.
- Tệp ngoài git: /var/tmp/cine-out/v2v3/ (nguồn, điều khiển, đầu ra), worktree /var/tmp/v7b-wt, bộ đệm /var/tmp/cine-out/k2tl-cache.
