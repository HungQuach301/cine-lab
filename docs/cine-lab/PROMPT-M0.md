# ĐỀ BÀI MỐC M0 — dán vào phiên Claude Code tương ứng

## Phiên 1 — BOOTSTRAP (chạy một lần, trên repo mới)
```
Repo có file cine-lab-bootstrap.zip ở gốc. Giải nén vào gốc repo (giữ nguyên cấu trúc, kể cả .claude/ và .gitignore), xoá file zip, commit với nội dung "bootstrap Cine Lab" và push lên main. Sau đó chạy `bash scripts/env/verify.sh` và báo lại nguyên văn kết quả bằng tiếng Việt. Không làm gì khác.
```

## Phiên P — ĐIỀU PHỐI, mốc M0 (Cổng 0: năng lực và hạ tầng)
```
VAI TRÒ: Phiên P — điều phối Cine Lab. Đọc CLAUDE.md và docs/cine-lab/ (HANDOFF, KHUNG-CHAT-LUONG, KE-HOACH-TRIEN-KHAI mục 6 M0) trước khi làm. Không sửa checks/.

VIỆC (M0 — Cổng 0). Mọi số đo phải là đo thật; lưu script đo và kết quả thô vào reports/m0/.
1. Chạy scripts/env/verify.sh; ghi số vCPU/RAM/đĩa thật.
2. Đo render 10 s (24 fps, 1920×1080) cho 3 phong cách ứng viên, cùng một cảnh mẫu: 1 nhân vật đơn giản đi qua khung, nền 3 lớp chiều sâu, một nguồn sáng ấm:
   (a) 2D vector qua Chromium/Canvas hoặc SVG;
   (b) 2.5D three.js trong Chromium;
   (c) Blender bpy chế độ Workbench hoặc EEVEE nếu chạy được không GPU (không dùng Cycles).
   Báo: giây render / giây phim; có motion blur (siêu lấy mẫu) và không. Ngưỡng dừng: > 60 s/giây.
3. ElevenLabs: sinh 3 take cho một câu cảm xúc khó (lời tạm biệt nói khẽ, nghẹn) bằng 2–3 giọng; thêm 1 giọng trẻ em nếu thư viện có. Chạy faster-whisper kiểm đủ từ. Lưu file cho chủ dự án nghe chấm.
4. ACE-Step: cài trong phiên (không trong setup), sinh 60 s nhạc chủ đề trên CPU. Báo thời gian, RAM đỉnh, và file kết quả. Nếu không chạy được, ghi lỗi nguyên văn.
5. Thử song song: dùng 2 subagent cine-worker (isolation: worktree), mỗi agent render một nửa cảnh mẫu (a). Đo tổng thời gian so với chạy một mình; ghi xung đột nếu có.
6. Thử nhất quán nhân vật: định nghĩa một model sheet nhân vật đơn giản bằng dữ liệu (JSON). Hai subagent dựng 2 shot khác nhau từ cùng model sheet. Đo sai lệch tỷ lệ các bộ phận giữa 2 shot.
7. Viết reports/m0/BAO-CAO-M0.md: bảng số đo; khuyến nghị phong cách (ưu, nhược, tác động, rủi ro); khuyến nghị số phiên song song; việc chờ chủ dự án.
8. Commit, push. DỪNG.
```

## Phiên K — KIỂM ĐỊNH, mốc M0 (phiên riêng, chạy song song với P)
```
VAI TRÒ: Phiên K — viết và khoá luật kiểm của Cine Lab. Bạn KHÔNG dựng phim. Đọc CLAUDE.md, docs/cine-lab/KHUNG-CHAT-LUONG.md (mục 1, 4) và BAI-HOC-BRIEF-D.md.

VIỆC:
1. Tạo nhánh checks/v0 từ main.
2. Trong checks/, viết máy kiểm cho các luật L1 cấp Chặn ở nhóm N (kỹ thuật file), P1 (chữ đè chữ theo điểm ảnh nét chữ), J1 (ASR trên bản mix cuối: 100% từ bắt buộc + WER), M1/M3 (loudness, true peak, tương quan pha, tương thích mono), G3 (banding), G4 (tương phản chữ), H1 (không chuyển động tuyến tính, đo từ dữ liệu chuyển động xuất ra), O3 (tài sản có SHA trong thư viện).
   Mỗi luật có: mã, mục trong khung, định nghĩa đo, ngưỡng, cấp (Chặn/Chính/Tham khảo), và test tự chứng minh (một mẫu nhỏ tự tạo phải TRƯỢT, một mẫu phải SẠCH).
   Đo từ file đã render, không từ bản khai.
3. Viết checks/RUN.md: lệnh duy nhất để phiên xưởng chạy toàn bộ luật trên một file và nhận báo cáo JSON + Markdown.
4. Chạy test tự chứng minh; báo luật nào đạt.
5. Tính SHA-256 toàn thư mục checks/ (trừ LOCK), ghi vào checks/LOCK. Commit, push nhánh checks/v0.
6. Báo lại bằng tiếng Việt: danh sách luật, kết quả test tự chứng minh, SHA khoá. DỪNG.
```
