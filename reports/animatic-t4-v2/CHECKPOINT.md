# CHECKPOINT — ANIMATIC-T4-V2 (K2C-T4-02 London, M4 vòng sửa animatic duy nhất, gói "50 % tiết kiệm")

> Nhánh thật: `claude/animatic-t4-v2-revision-hwh8jp` (harness buộc; lệnh ghi `k2c-t4-02-animatic2`). Gốc `origin/main` @2a49e3ca + merge (không squash) `origin/k2c-t4-02-nc` @d2279bbb → merge `af1993ee`.

## Trạng thái
- 25/10 02:30 UTC: khởi động; SHA đỉnh khớp lệnh; verify.sh 10/5 → cài OpenEXR/tifffile/pyshp, npm ci, pyproj 3.8.0 + OSTN15 (SHA 5d6ed64d… KHỚP). Hook pre-commit/pre-push cài. `lock.py --verify` KHỚP 513c9442… (1.17.6).
- Dữ liệu nền 3D đang tái tạo (`du_lieu.sh`, container mới, /var/tmp trống).
- Việc 1: loi-khoa-v3.txt (271c6c25…), LOI-KHOA-v3.sha256, SO-LOI-V2-V3.md. Thu G1 9 câu (868 ký tự chữ khoá; gửi 939 sau alias) + thu lại N2, N3, N6 (394) = **1 333 ký tự gửi** (mốc 1 500). ASR: 8/9 câu 100 % cả hai cách nghe; N6 tên Bazalgette: medium.en đúng, small.en "basil getz" (NGHI). Master giọng v2 tái tạo bit-trùng (b9cec467 OK), lời dựng v2 187e059a… OK.

- 03:30 UTC: bảng v3 105 shot (2 M-d trượt 3/3 → 3D: H2-06b, H2-09x); hàng dựng 3D 65 tệp máy đang chạy (PGID 6286, ≈ 5 s/khung mỗi tiến trình); Omni 2 luồng; SFX CC0 chuông + còi (BigSoundBank); Commons 429 — đang chờ giãn cách.

## Lệnh bổ sung đã áp
- **25/10/2026 10:05 (Asia/Saigon; điều phối, chủ dự án dán vào phiên) — bằng chứng giấy phép tư liệu NC-T4** — nhận ≈ 03:30 UTC. Trạng thái: **ĐÃ ÁP** (03:31–03:55 UTC).
  Nguyên nhân 0/21 tệp: `channel-k2/.gitignore` dòng 2 `*.json` bỏ qua mọi JSON trong channel-k2 (NC-T4 không `git add -f`). Chạy lại `scripts/k2ldn/nc/tai_nc.py` (UA chuẩn) cho đúng 21 mục → `nc/licenses/<id>.json` + `SHA256-NC.txt`, đối chiếu `reports/nc-t4/nhan-vat-anh.json` / `tu-lieu-1940.json`; mục không tải lại được → KHÔNG dùng ở vòng này.
  Kết quả: tải lại **21/21** (Met 2, Rijksmuseum 11, Wellcome 3, LoC 6 — Churchill gồm, không dùng); SHA-256 ảnh gốc **khớp 21/21** với `SHA256-NC.txt` của NC-T4; URL nguồn + SHA khớp `reports/nc-t4/nhan-vat-anh.json` 21/21; JSON lớn nhất 57 KB (≤ 5 MB); email trong siêu dữ liệu đã che (`scrub`). Bản thu nhỏ `nc/anh/*.jpg` giữ bản trong git (Pepys nén lại khác byte, gốc cùng SHA). Ảnh Blitz (Commons) không thuộc 21 mục: bằng chứng ở `animatic2/tu-lieu/giay-phep/`. Mục không tải được: **0**.
