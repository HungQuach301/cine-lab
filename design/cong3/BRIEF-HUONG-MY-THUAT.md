# Cổng 3 vòng 1 — Giao việc 3 hướng mỹ thuật (phiên P)

Phim: **Last Round**. 2:30, tiếng Anh, 16:9, 24 fps. Kịch bản chốt: `scripts/last-round.fountain`. Luật thế giới (bắt buộc tuân theo, nhất là mục 2–3 về ánh sáng và bóng): `bible/world-rules.md` v0.2.
Công nghệ đã chốt: **2.5D three.js (WebGL, SwiftShader CPU trong Chromium headless) + lớp 2D**. Chống banding bắt buộc; grain cố định.
Mục tiêu chất lượng: **khung hình mẫu ở mức phim ngắn hoạt hình chuyên nghiệp** (style frame là "hợp đồng hình ảnh"), không phải hình thử. Không đạt được thì nói thẳng trong README.

## Việc của mỗi hướng
Dựng **2 khung hình mẫu 1920×1080** ở chất lượng cuối trong thư mục riêng `design/cong3/dir-X/` (X = A, B hoặc C):
1. `s1_opening` — cảnh 1, toàn cảnh cao mở phim lúc **trời xanh cuối chạng vạng** (quyết định 10A): trên mái nhà một thành phố không tên, trời chuyển hồng → tím; đèn khí thắp dần thành những **tâm hổ phách**, giữa chúng là khoảng tối. Ostler Street là phố dốc nhẹ, cong, 11 cột đèn khí; vài ngọn đầu đã sáng, số còn lại chưa. Cột điện kiểu mới (cao ~7 m, tấm kính mờ chữ nhật) đứng xen, **chưa bật**. Quảng trường ở đầu phố có cột đồng hồ điện (mặt tròn ~1,2 m, 12 vạch, không chữ số), **chưa sáng**. Có thể có Ida rất nhỏ (tư thế `walk_ladder`) cạnh ngọn đèn vừa thắp để cho tỷ lệ. Máy quay cao ~30–40 m, chúc xuống 20–30°, nhìn dọc con phố cong.
2. `s5_shadows` — cảnh 5, hình then chốt (quyết định 7A + sửa quang học (a)):
   - **Hốc cửa bốc hàng** hình vòm cắt sâu vào tường nhà kho: rộng ~3,2 m, cao ~4 m, sâu ~4 m. Vách trong trát vôi trắng; trong hốc, ánh điện không chạm tới.
   - **Đèn lồng** (dùng `buildLantern` của `shared/cast.js`) đặt trên nền đá, **cách vách trong ~3 m**, ngay trong miệng vòm. Là nguồn sáng duy nhất trong hốc: đèn điểm có bóng, rung sáng ±4%. Bóng **mềm**: jitter vị trí đèn trong khoảng kính đèn (~12 cm) theo từng mẫu tích luỹ.
   - **Ida** (tư thế `look_shadows`) và **Cas** (tư thế `half_raised`) đứng cạnh nhau, **quay lưng về máy quay**, **cách vách ~1 m**, tức giữa đèn và vách, gần vách hơn. Ida bên trái, Cas bên phải.
   - Trên vách: hai bóng người **vươn cao** (đèn thấp), phóng đại ~1,5×, rìa mềm. Là hai cái bóng duy nhất trong hình.
   - **Ngoài vòm** (mép khung): phố trắng, ánh điện phẳng, tràn đều, **không có bóng đổ dài** (chỉ bóng tiếp xúc rất nhẹ). Tương phản ấm (trong hốc) ↔ lạnh (ngoài phố).
   - Máy quay ngang tầm người lớn (~1,2–1,4 m), sau đèn lồng ~1,5 m, ngoài miệng vòm, nhìn vào hốc. FOV dọc ~35–42°.

Tỷ lệ key : tràn đo tại vách trong phải ≥ 4 : 1 (luật thế giới 3.1–3.4).

## Nền chung BẮT BUỘC dùng (không sửa file trong `shared/` hay `model-sheet/`)
- `shared/cast.js`: `buildCharacter(sheetJson, {material:(role,color,part)=>Material, detail})`, `buildLantern(h, mat)`, `buildLadder(...)`. Tỷ lệ bộ phận và tư thế lấy từ `model-sheet/ida.json`, `model-sheet/cas.json`; **không đổi tỷ lệ** (luật C3). Được đổi vật liệu, mức chi tiết, và thêm chi tiết trang trí gắn vào khớp (nút áo, nếp vải, kết cấu) nếu không làm lệch đường bao bộ phận.
- `shared/post.js`: `createRenderer(W,H)`, `createPipeline(renderer, W, H, {exposure, toneGLSL, gradeGLSL, overlayCanvas, uniforms, uniformDecl})` → `accumulate(scene, camera, n, onSample)` và `finalize(frameIndex)`.
  - **Không đổi GRAIN** (grain cố định cho cả phim; luật G3b đo σ ổn định giữa các shot).
  - Chất liệu riêng (giấy, nét cọ, nét mực) thì đưa vào `gradeGLSL` (hàm `vec3 grade(vec3 c, vec2 uv)`, không gian hiển thị sRGB) hoặc lớp 2D `overlayCanvas`.
  - `onSample(i, n, [jx,jy])` dùng để jitter đèn (bóng mềm) hoặc khẩu độ (DOF thật) theo mẫu.
- `shared/render_still.js`: driver. Trang của bạn là một ES module gán `window.setup(cfg)` (async, `cfg.W`, `cfg.H`), `window.renderFrame(name, samples)` (dựng cảnh `name`, gọi `accumulate`), `window.finalize(f)` (gọi `pipe.finalize(f)`). Mẫu: `model-sheet/sheet_page.js`. Import three từ `../shared/node_modules/three/build/three.module.js` (addons ở `../shared/node_modules/three/examples/jsm/...`).
  ```
  cd design/cong3 && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node shared/render_still.js --page dir-X/scene.js --frame s5_shadows --out dir-X/out --samples 32 --frames 48
  ```
  Ghi `out/<frame>.png`, `out/<frame>.rgb` (48 khung, grain đổi theo khung, để P ghép video kiểm luật), `out/<frame>.timing.json`.

## Ngân sách render (quan trọng cho so sánh)
Ngưỡng Cổng 0 là ≤ 60 s máy cho 1 giây phim, tức **≤ 2,5 s/khung** trên một máy 4 vCPU. Mỗi khung báo **hai** số:
- **Chất lượng cuối** (`--samples 32` hoặc số bạn chọn): thời gian `render_frame_s`.
- **Thiết lập sản xuất** (`--samples 8`): thời gian, kèm nhận xét chất lượng giảm ra sao.

Hướng nào vượt 2,5 s/khung ở thiết lập sản xuất thì ghi rõ vượt bao nhiêu lần và cách hạ.

## Luật cứng
- Không sao chép phong cách, nhân vật, thiết kế của phim tham chiếu (*Ice Merchants, Hair Love, Alike, The Flying Sailor, Sprite Fright*) hay bất kỳ IP có sẵn nào (Laika, Aardman, Ghibli, Pixar…). Ghi trong README bạn đã tránh những gì.
- Không chữ viết đọc được trong hình (biển hiệu, mặt đồng hồ chỉ có vạch).
- Không tải tài sản ngoài (texture, font, model). Mọi thứ sinh bằng mã. Không dùng mạng.
- **Không đọc, không sửa `checks/`.** Không sửa `bible/`, `shared/`, `model-sheet/`, thư mục của hướng khác. Không commit git (P sẽ commit).
- Chỉ ghi trong `design/cong3/dir-X/`.

## Nộp (trong `design/cong3/dir-X/`)
- `scene.js` (và file phụ nếu cần), `out/s1_opening.png`, `out/s5_shadows.png`, `.rgb` 48 khung cho mỗi khung, `.timing.json` (32 và 8 mẫu).
- `README.md` (tiếng Việt, ngắn gọn):
  1. Tên hướng; ngôn ngữ hình khối; chất liệu; bảng màu (mã hex, vai trò từng màu); cách vẽ ánh sáng và bóng; lớp 2D dùng vào việc gì.
  2. Thời gian render mỗi khung (32 và 8 mẫu).
  3. Tự phê bình thẳng thắn: chỗ nào còn "trông như CG rẻ tiền", chỗ nào chưa đúng luật thế giới, còn thiếu gì để đạt mức chuyên nghiệp.
  4. Những gì đã tránh để không giống IP có sẵn.
- Tự xem ảnh (dùng Read trên PNG) và lặp lại tới khi đạt mức tốt nhất bạn làm được trong phạm vi hợp lý.
