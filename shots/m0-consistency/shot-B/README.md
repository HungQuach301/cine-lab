# Shot B — M0-W-CONS-B (thử nhất quán nhân vật, Cổng 0)

Người thắp đèn, trung cảnh (medium-full), 1920×1080, nhìn nghiêng quay sang TRÁI, đứng yên,
tay trước giơ sào thắp ngọn đèn gắn tường; tay sau buông thõng; hai chân hơi dạng.
Phong cách 2D vector phẳng, dựng bằng Python + Pillow (siêu lấy mẫu 4×, không dùng tài sản ngoài).

## Lệnh chạy (từ gốc repo)

```
/opt/cine/bin/python shots/m0-consistency/shot-B/render.py --sheet reports/m0/consistency/model-sheet.json
```

Nếu model sheet chưa được commit vào nhánh này, trỏ `--sheet` tới bản trong checkout chính
(`/home/user/cine-lab/reports/m0/consistency/model-sheet.json`). Bản đã dùng có
SHA-256 `d097fae9604f68bbc766d377a4dcf9144417c80a82f4e30ef17c154c0007fa20` (ghi trong `render-meta.json`).

Đầu ra: `frame.png`, `masks/{head,torso,upper_arm,forearm,thigh,shin}.png` (nhị phân 0/255), `render-meta.json`
(H, tư thế, hằng số diễn giải, toạ độ khớp).

## Thang đo

- Chiều cao nhân vật (không tính mũ) = 820 px = `total_height_H` (5.60 H) → **1 H = 820 / 5.60 = 146.4286 px**.
- Mọi kích thước bộ phận = hệ số trong model sheet × H (đọc từ JSON lúc chạy, không gõ tay).
- Vì hai chân dạng nhẹ (đùi/ống chân nghiêng 5–6°), chiều cao đứng thực tế thấp hơn 820 px vài px; H vẫn giữ 146.4286.

## Diễn giải ở chỗ model sheet mơ hồ

1. **Đầu mút bo tròn tính vào độ dài.** Tay/chân vẽ hình con nhộng (bán kính = width/2); toàn bộ con nhộng,
   kể cả hai nắp tròn, dài đúng `length` dọc trục. Khớp gốc = điểm đầu trục (mép ngoài nắp gốc), đầu mút = mép ngoài nắp mút;
   bộ phận kế tiếp bắt đầu đúng tại điểm đó. Tại khuỷu tay và đầu gối, frame có thêm một hình tròn cùng màu (đường kính = width
   của bộ phận dưới) để che chỗ thắt; hình tròn này KHÔNG nằm trong mặt nạ.
2. **Đầu:** elip, trục dọc = `head.length` (1.00 H), bề ngang = `head.width`. Nhìn nghiêng nhưng vẫn dùng đúng elip đó
   (không thêm mũi nhô ra để không đổi đường bao); mắt và tai vẽ bên trong elip. Mặt nạ đầu = elip, không gồm mũ.
3. **Mũ:** tổng cao `hat.length` (0.55 H), vành rộng `hat.width`, đặt chồng lên đầu: đáy vành nằm dưới đỉnh đầu 0.22 H;
   vành dày 0.08 H; chóp rộng 0.66 × vành. Ba số này là diễn giải (model sheet không quy định). Mũ không tính vào 820 px
   (khớp với `_total_check`, vốn không có mũ).
4. **Cổ:** khoảng hở giữa đáy đầu và đỉnh thân = `neck.length` (0.15 H); hình chữ nhật cổ vẽ lấn vào sau đầu và thân để không hở.
5. **Thân:** hình thang cân, đỉnh `top_width`, đáy `bottom_width`, cao `torso.length`. Trường `width` (1.10) coi là bề rộng
   trung bình, không dùng trực tiếp. Nhìn nghiêng vẫn giữ nguyên bề rộng này (không co theo chiều sâu).
6. **Vai:** trên trục giữa thân, dưới đỉnh thân `shoulder_from_torso_top` (0.12 H); hai tay chung một điểm vai.
   **Hông:** đỉnh đùi tại giữa cạnh đáy thân (`hip_at_torso_bottom`), hai chân chung một điểm hông.
7. **Bàn chân:** `foot.width` (0.20 H) là chiều cao bàn chân dưới mắt cá (đúng theo `_total_check`); `foot.length` là chiều dài
   hướng về phía mặt; gót lùi sau mắt cá 0.12 H (diễn giải).
8. **Bàn tay:** tròn đường kính `hand.length`, tâm nằm trên trục cẳng tay, cách đầu mút cẳng tay 0.5 × `hand.length`.
   Sào dài `pole.length`, xuyên tâm bàn tay trước, thò dưới tay 0.25 H (diễn giải).
9. **Tay/chân "trước":** là phía gần máy quay; mặt nạ lấy tay trước (tay giơ sào) và chân trước (chân bước lên, lệch về trái).
   Tay/chân sau tô tối hơn (×0.72) và nằm sau thân; tay sau buông thõng nên gần như khuất sau thân, chỉ lộ bàn tay.
10. **Tư thế:** cánh tay trên nghiêng 8° lên trên phương ngang, cẳng tay 80° so với phương ngang (hướng lên, hơi về trước);
    đùi ±6°, ống chân ±5° so với phương đứng; sào 24° trên phương ngang (góc thấp để ngọn đèn nằm trong khung với nhân vật cao 820 px).

## Quyền tài sản

Không dùng tài sản ngoài (không font, ảnh, âm thanh); mọi hình vẽ sinh bằng mã trong `render.py`. Không cần mục mới trong `RIGHTS.md`.
