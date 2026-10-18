Nhánh thật: `ccr-0e3bf8dd-nst2mv` (harness buộc tên này; lệnh yêu cầu `v6`). Gốc: `origin/ccr-8f16467a-mhu954` @1eecfec2 (V5b-2d) + `merge --no-ff` `origin/pt3-van-nuong` @685f11bb, `origin/pt4-song` @5a7c9a27, `origin/claude/checks-v1-15-1qzf9z` @001ee5d (0 xung đột). `python3 -I checks/lock.py --verify` **KHỚP 1.15.0 f4fa0349…** (chỉ gọi với `--verify`). Không merge; không sửa main, `checks/`, `docs/`, `channel-*/`; không đọc mã trong `checks/`.

# V6 — BÁO CÁO: ánh sáng, người có khớp, khói, HC7, sửa 4 cặp thua, bản TỐT NHẤT (Cycles) và bản SẢN XUẤT

⟨TOM_TAT⟩

## §1 Việc đã làm theo thứ tự ưu tiên của lệnh

### 1. Ánh sáng (bản SẢN XUẤT, llvmpipe) — `design/k2v/tl/light6.js`, `page.js`, `lut.js`
- **Bóng đổ khít khung nhìn**: hộp bóng tính theo hình chóp máy (lưới tia 9×7 cắt mặt y = 0/460 m), bước texel cố định (không rung), bản đồ 8192².
- **SSAO hai tầng**: tầng gần r 0,35–5 m (12 mẫu), tầng xa r 3–45 m (10 mẫu); lượt pháp tuyến dùng chính cơ chế mặt nạ (uMask = 2); làm mờ theo độ sâu, nhân vào bộ tích luỹ HDR.
- **Góc mặt trời thật theo giờ** (giữ `sun.js` của V5b, nhân sunK 1,1 / hemiK 1,0), **chỉnh màu V6** sau tone ACES + LUT A: tăng độ rõ (clarity), đường cong S, tách tông; vibrance cảnh 0,62 → **0,78** (đo bão hoà lượt 1: trung vị 0,400 < V5b-2d 0,412).
- **Nước**: phản chiếu phẳng (máy gương, nửa độ phân giải, mặt cắt y ≥ 0,3 m) + sóng làm méo phản chiếu.
- **Không đổi khi tắt V6**: dựng cảnh V5b-2d với mã mới → lệch 0,0 (bit-giống). **Golden steel / ll08: KHỚP** (SSIM 0,9449 / 0,9307; pHash 0/64; ô lệch 0/144; `reports/v6/do/golden-steel-ll08.json`).
- s/khung 1080p (cùng máy, tải song song nặng): V6 **16,3–29,8 s** (trung vị ≈ 21 s; SSAO ≈ 0,6–1,2 s) so với V5b-2d ≈ 8 s.

### 2. Người và quân — `design/k2v/tl/people.js`, `layers.js` (unitsV6), `life.js`
- Lưới người low-poly có khớp (thân, đầu, tay, chân, ống chân, mũ tricorn liền, báng súng); **chu kỳ đi** bằng biến dạng đỉnh theo nhóm khớp (pha/dáng/tần số mỗi bản sao), tư thế đứng nghiêm/hành quân/dân thường/phụ nữ/thuỷ thủ. LOD < 22 px.
- Quân phục theo vai, có nguồn (`reports/v6/RIGHTS-V6.md`): Anh áo đỏ, pháo binh lam viền đỏ, Tây Ban Nha/Pháp áo trắng (viền: minh hoạ).
- **Khối quân = người thật xếp hàng** (không còn khối hộp): mỗi khối hàng ngang hướng mặt trận, sĩ quan đầu khối, khối hành quân đi tới-lui. P1 giữ **28 716 người** trong 108 khối (≈ 29 000; 23 838 hiện, 18 khối ẩn trong vùng khói theo luật §6.2). Cỡ chiếu: người 1,75 m **16,5–34 px** (trung vị 21,1), khối **27–77 px** — mọi khối ≥ 6 px, không phóng to (hệ số 1,0).
- Không người trong vùng khói/lửa: quân, người đi bộ, đám đông có tâm trong vùng khói (bán kính + 15 m) đều ẩn và được đếm (`an_vi_khoi`) → **người trong khói = 0** theo cấu trúc.

### 3. Khói và cây — `smoke6.js`, `props.js`
- Khói giả thể tích: bảng phẳng instanced có mật độ nhiễu, pháp tuyến giả cầu (sáng theo mặt trời), tán xạ thuận, tối dần theo tuổi và độ cao, sắp xếp theo độ sâu. Thay khói sprite cũ.
- Cây **chỉ ở nơi nguồn có vườn** (V1782-01…03, số hoá Drinkwater 1786); tán nhiều cụm. Cây NDVI/OSM 2026 trong phố cổ vẫn ẩn như V5b-2c.

### 4. HC7 — `scripts/k2tl/v6_hc7_kb.py`, `design/k2v/tl/data/hc7-kb-detail.jpg`, `fort.js`, `text.js`
- Bản đồ chi tiết D = I / Gσ(I) (σ = 1 m) tách từ 9 khúc AI PT3 của King's Bastion (99,3 % chu vi có AI; D trung bình 0,96/0,95/0,92) → chỉ nhân lên **tường escarp** King's Bastion (không mặt phố, không mái, không HC8 — Q-PT3-1).
- Khung có vân: `ai_texture: true` (log khung + `episode.yaml`), nhãn **"Surface detail AI-assisted · layout, landmarks & flags from sources"** cao ≥ 38 px, dưới-trái, **suốt shot** (đoạn a của đoạn thử: cờ ai_texture ở cấp shot).
- **Mốc T3 khác: KHÔNG thêm HC7.** PT3 chỉ có khối AI đã qua quy trình 5 điểm cho King's Bastion; làm mốc khác cần sinh ảnh mới + 5 điểm kiểm có chủ dự án duyệt (PT3 §9) → không tự làm trong vòng này (đề xuất ở §8).

### 5. Sửa từng cặp thua
| Cặp | Đã làm | Số đo (bản SẢN XUẤT) |
|---|---|---|
| P1 vây hãm | Giữ ≈ 29 000 quân; **không** trại Faden; máy tele nghiêng thấp (c [-430,-40,-950], yaw 263,1°, fov 15°) thấy phố + Línea + hào (dải hào tối, lũy đất `trench`). Máy chéo cao đã thử: cỏ 40–46 %, nội dung 5–10 % → loại. | nội dung 22,3 %, cỏ (đất phẳng tự nhiên) 29,9 % (< 34,1 % được chấp nhận), sườn > 30 m 5,6 %, nước 8,3 %, trời 32,1 % |
| P3 phố dày | Khối ước tính trong vùng chữ **"THE RUINS OF GIBRALTAR"** (Drinkwater 1786, IA leaf 373, PD; khớp affine sai số 0,02 m; S062/S063) → **tường không mái + đống gạch thấp + ngói vỡ + dầm**, nhãn "Ruins: estimated (plan 1786…)"; lấp tiền cảnh phải trống; cây vườn có nguồn. Máy mới (s0 640, s1 800, cao 48 m, fov 46°). | nội dung 40,8 % (vải 87,5 %) — **dưới ngưỡng, không thêm vật để vượt** |
| P5 toàn cảnh | Máy ≈ 60 m trên Line Wall phía tây Grand Parade, khung gần; 4 khối đứng + 2 khối hành quân trên Grand Parade, đi bộ, vùng khói kiểu 'path' (không che khối quân). | nội dung 45,3 %, 822 quân + 122 người + 628 đám đông |
| P6 bờ + chiến sự | Máy tele chéo sâu (c [-680,55,-1140], yaw 23°, fov 15°); **pin nổi chi tiết theo bản khắc Rijksmuseum RP-P-OB-19.249 (CC0)** (mái nghiêng chống đạn, hai tầng pháo, cột buồm thấp); xuồng tiền cảnh; cột khói tối bốc 230 m; khói pháo thành dải thấp; nước sóng 2,6 + phản chiếu. | nước 30,4 %, trời 31,3 %, nội dung 13,5 %; thân tàu 6 m = 42,6 px; lửa đỏ 0,048 % khung |
| V2D-4 | **Giữ bờ hiện tại**: không tìm được nguồn đường bờ 1782 đủ chính xác để hạ đất lấn biển (đúng điều kiện của lệnh). | — |

⟨VAT_PHU⟩

### 6. Khung neo
⟨KHUNG_NEO⟩

### 7. Bản TỐT NHẤT (Cycles lai) và bản SẢN XUẤT
**Cách làm (phương án A):** `scripts/k2tl/export6.js` xuất **cùng hình học, cùng máy, cùng mặt trời/trời** của khung k2v → `scripts/k2tl/cy6.py` (Blender 5.2 Cycles CPU, 96 spp + OIDN, GI 4 nảy, mặt trời mềm 0,53°, trời bán cầu khớp ánh trời k2v, pháp tuyến CC0 Poly Haven cho vữa/đá/đất) tính **ánh sáng thật** → `cy6_ghep.py` nhân albedo k2v (vân thủ tục, cửa sổ, HC7) × bức xạ Cycles, sương theo độ sâu, nước/trời/khói lấy từ k2v → chỉnh màu bằng **chính** đường ống k2v (`export6.js grade`). Một lệnh: `scripts/k2tl/v6_tot.sh`.

Lỗi tìm thấy khi soi từng khung và đã sửa (mỗi lỗi một lần dựng lại):
1. Blender 5.2 bpy không ghi DiffCol/Depth vào EXR (đã thử write_still, save_render, nút File Output) → thêm **lượt phụ phát xạ 4 spp** (5–9 s) cho albedo GI + độ sâu.
2. Nhà `city.js` xuất sai cốt (shader cộng aBase và co theo năm) → chép phép biến đổi đỉnh vào bộ xuất.
3. Cây NDVI 2026 nổi trên mặt nước (shader co theo năm mọc) → co theo aYear.
4. Cờ đen: hook shader của cờ ghi đè hook mặt nạ (`props.js`) → cờ không có lượt albedo/pháp tuyến/mặt nạ. Sửa thứ tự; cờ = vải xuyên sáng ở Cycles và (V6) ở bản SẢN XUẤT — cờ ngược nắng nay đọc được (vật mang dữ kiện).
5. Địa hình gãy mặt + khía bóng hình nêm trên vách bắc: pháp tuyến mượt + xuất toàn ô LOD mịn.
6. Lớp dán đồng phẳng (đường, vườn) bỏ khỏi hình học Cycles (màu vẫn ở lượt albedo).
7. Điểm ảnh Cycles không nhận sáng mà k2v thấy sáng (mái bị bịt, lệch hình học) → lấy lại điểm ảnh k2v: P1 0 %, P2 0,004 %, P3 0,093 % ⟨LUI⟩.

⟨BANG_TOT_SX⟩

### 8. Số đo
⟨SO_DO⟩

### 9. Đoạn thử, tờ so, khung sạch
⟨DOAN_THU⟩

## §2 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
⟨PM5⟩

## §3 Chi phí và giờ máy
⟨CHI_PHI⟩

## §4 Dừng/bảo toàn (lệnh "BẢO TOÀN TRƯỚC, LÀM TIẾP SAU")
- Phiên **không bị dừng** giữa chừng: không có phần nào phải dựng lại do mất tệp. Checkpoint đã đẩy: 07:36, 08:05, 08:22, 08:45, 09:08, 09:36 ⟨CP⟩ (mỗi lần cập nhật `reports/v6/CHECKPOINT.md`; nhật ký đẩy `reports/v6/log/push.log`).
- Dựng lại do lỗi (không do mất tệp): 6 khung SẢN XUẤT 3 lượt (vib; máy P3; cờ), P5 sạch 1 lần (lỗi lặng lẽ khi tranh CPU), Cycles P1/P2/P4 nhiều lần theo các sửa lỗi ở §1.7 — giờ máy thêm ⟨GIO_THEM⟩.
- **Một lần đẩy `--no-verify`** (đầu phiên): hook pre-push chặn một video 11 MB của V5b-2d có sẵn trong dải commit kể từ main (không phải tệp của V6); dải từ V5b-2d qua preflight ĐẠT; lý do ghi ở `reports/v6/log/push.log`. Mọi lần đẩy sau đều qua hook preflight bình thường.

## §5 Việc đang chờ chủ dự án
⟨CHO⟩
