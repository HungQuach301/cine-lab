# CHECKPOINT tập 8 — phiên P (cập nhật ở mỗi mốc lớn)

**Cập nhật:** 10/10/2026 03:40 · nhánh `ccr-a261f349-6rkunc` · checks LL v3 1.8.1 (LOCK KHỚP)

## Bước hiện tại: **XONG G2 có điều kiện — chờ G3** (10/10/2026)
- Sửa T01 (đoạn 00 → 01) xong; `render.js` nới cửa sổ nạp khung (BAI-HOC #108), dựng lại 17 đoạn; Q31 vòng 3 [7, 8, 8]: T01 hết, T11 3/3 mới (chỉ ghi).
- Nhánh phát hành `release-ll-ep08-v1` @ `67bfc2e`: 9 tệp (chỉ Short S2), tải ngược 9/9 SHA OK; master `d22d7d6e640dc6f0…`.
- Báo cáo: `reports/m3/TAP8-G2.md` mục 9. Bàn giao tập 9: `reports/m3/ep08/BAN-GIAO-P.md`.
- Chờ: G3 (chủ dự án đăng); khiếu nại Q28f, Q27 (phiên K); đề tài tập 9.

## Job nền và cách dựng tiếp
- Cảnh đinh: runner tách rời (10:49) `P=2 SPP=4 setsid nohup bash scripts/ll/heroes_par.sh reports/m3/ep08/episode.yaml >> /var/tmp/cine-out/ll-ep08/heroes-par2.log 2>&1 &` + 3 cảnh mồ côi của lượt 09:46 (st_screen, lib_end, vrs_screen; tự xếp vào chỗ khi xong). Lỗi: `hero-<khoá>.err`. Mỗi cảnh đang dựng có `<dir>.new/pid`; chạy lại runner sẽ bỏ qua cảnh có pid còn sống.
  - Bị ngắt: **trước khi chạy lại, kiểm không còn `scripts/ll/hero.js` nào chạy** (`pgrep -f scripts/ll/hero.js`, dừng theo PID). Chạy lại đúng lệnh trên: cảnh có `<dir>.new/pending` trùng stamp sẽ `--resume`, cảnh có `stamp` trùng được giữ.
- Đoạn + ghép: `SPP=4 J=3 bash scripts/ll/build.sh reports/m3/ep08/episode.yaml render mix ghep shorts` (cảnh đinh đã dựng được giữ theo stamp). Không chạy hai build chồng nhau (BAI-HOC #67).
- QC: `bash scripts/ll/qc.sh reports/m3/ep08/episode.yaml`; mù: `checks/ll/q_blind.py q27-set / q31-set` (RULES-LL).

## Lỗi đã gom và đã sửa ở lượt sửa (commit đã đẩy)
- `booth_in`: máy quay ở x 14,0 nằm sau vách sau buồng (13,8) → khung 2–245 bị che (01:40–01:55 nháp, nửa phải 2 diptych). Sửa: máy x 13,55 → 13,45 (trong buồng).
- `lib_bridge` (cầu 09): lia 180° qua bầu trời trống ~5 s → thêm khoá máy lia ngang dọc phố.
- Q5 biển số ≈28,000 nền gạch tương phản 4,0 → nền vữa. Q28d lặng đặt nhầm giữa "two | hundred", "two | percent" → trước "@two". Q29 3 mốc (thẻ cột → chú thích số trên cảnh đinh). Q30 hai chuyển hồi 01→02, 14→15 → J-cut.
- **Còn mở:** Q28f (ASR độc lập của K) đọc "$20 million" và "3.5%" lệch cách viết lời → khiếu nại `checks-appeal.md` (09/10). Lời khoá, không đổi chữ.

## Tệp ngoài git quan trọng
- `/var/tmp/cine-out/hero/ll-ep08-*` — khung cảnh đinh (dựng lại bằng lệnh trên; mất thì dựng lại toàn bộ, ~9–10 giờ).
- `/var/tmp/cine-out/ll-ep08/` — timeline.json, heroes.json, sec/, mix, master (dựng lại: `build.sh … prep` rồi các bước trên; prep không gọi ElevenLabs vì giọng đã cache trong `reports/m3/ep08/vo/`).
- `/var/tmp/cine-out/ll-ep08-nhap/` — nháp (master 960×540, qc.md, el-counter.log). Đặc tả nháp: `reports/m3/ep08/episode-nhap.yaml` (sinh tự động).
- Bộ đếm ElevenLabs: `/var/tmp/cine-out/ll-ep08*/el-counter.log` (62 953 sau prep bản cuối; tính/gửi ≈ 0,44 ổn định).

## Chi phí đến mốc này (đo)
- ElevenLabs: +6 143 ký tự bộ đếm (56 810 → 62 953); log gửi 13 970.
- Giờ máy: cảnh đinh nháp 71 phút, render nháp 86 phút, cảnh đinh 1080p ≈ 12,7 giờ, build + dựng lại ≈ 2,8 giờ (chi tiết TAP8-G2 §6).
- Subagent: 6 lượt đọc mù G1, Q27 3 lượt, Q31 6 lượt (2 vòng). Credits ước tính ≈ $72 (TAP8-G2 §6).
