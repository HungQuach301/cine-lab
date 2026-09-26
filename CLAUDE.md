# CINE LAB — hướng dẫn cho mọi phiên Claude Code trên repo này

## Dự án
Nghiên cứu và sản xuất phim ngắn hoạt hình phong cách hoá **chuẩn điện ảnh cao nhất** bằng Claude Opus 5.5.
- Bài thử năng lực: 2–3 phút. Phim đích: 10–15 phút.
- Tiếng Anh; 16:9; 24 fps. Phát hành trên YouTube và bán phim.
- Tài liệu gốc trong `docs/cine-lab/`. **Đọc trước khi làm:**
  - `CINE-LAB-HANDOFF.md`: quyết định
  - `CINE-LAB-KHUNG-CHAT-LUONG.md`: 11 cổng và tiêu chuẩn
  - `CINE-LAB-KE-HOACH-TRIEN-KHAI.md`: mốc M0–M4 và tổ chức nhiều phiên

## Cách làm việc
- Báo cáo bằng **tiếng Việt**, văn phong chuyên nghiệp. Nội dung phim viết bằng tiếng Anh.
- Kế hoạch theo **mốc và bước nhỏ**, không theo tuần hay ngày. Mỗi đề xuất nêu ưu, nhược, tác động, rủi ro.
- Không đoán: kiểm bằng tài liệu, repo hoặc chạy thật. Số đo thật thắng số tự khai.
- **DỪNG ở cuối mỗi mốc/cổng**: commit, báo cáo, chờ chủ dự án duyệt.
- Luôn nêu việc đang chờ chủ dự án.

## Vai trò (xem KE-HOACH mục 5.3)
- **Chủ dự án** là tác giả – đạo diễn. Mọi quyết định sáng tạo then chốt phải được chủ dự án duyệt và ghi vào `AUTHORSHIP.md`, kèm đóng góp biểu đạt cụ thể của con người.
- **Phiên K (kiểm định)** là phiên riêng. Chỉ K được sửa `checks/`. Luật khoá bằng SHA trong `checks/LOCK`.
- **Phiên P (điều phối)** giữ `PLAN.md`, bảng shot, và là phiên duy nhất merge vào `main`.
- **Phiên xưởng** chỉ sửa trong gói việc được giao. Không sửa `bible/`, tài sản đã khoá, hay `checks/`, và **không đọc mã trong `checks/`**. Khiếu nại về luật ghi vào `checks-appeal.md`.

## Luật cứng
- Không thêm phần tử chỉ để vượt ngưỡng một chỉ số. Mọi chỉ số nằm trong ±5% quanh ngưỡng phải nêu tên trong báo cáo.
- Mọi tài sản (nhạc, SFX, giọng, font, tham chiếu) phải vào `RIGHTS.md` với nguồn, giấy phép, phạm vi dùng. Không dùng nhạc hay SFX có điều khoản NC/ND. Không dùng YouTube Audio Library cho phim đem bán.
- Không sao chép thiết kế, nhân vật hay nhạc của phim tham chiếu hoặc IP có sẵn.
- Không commit khoá API. ElevenLabs được proxy gắn khoá cho `api.elevenlabs.io`.
- File video > 30 MB: không gửi qua giao diện; đẩy lên nhánh git hoặc thư mục `out/` theo quy ước của PLAN.md.

## Môi trường
- Môi trường cloud: `cine-lab-av`. Đầu mỗi phiên chạy `bash scripts/env/verify.sh`.
- Python chính: `/opt/cine/bin/python`. Blender: `/opt/bpy/bin/python`. Chromium: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`.
