#!/opt/cine/bin/python
"""THU-B-T4 · (D2) VÂN NƯỚNG mặt tiền/mái từ ảnh AI (Kinh thánh §11.3 (b) — "vân AI nướng lên mặt tiền… albedo phẳng không bóng nướng").
  fac_thub.py ve      → $THUB/fac/vao-{1666,1667,2026,mai}.png (2560×1440): bản vẽ phẳng của CHÍNH lưới mặt tiền look3 (8 mặt tiền 12 × 13,5 m mỗi tấm, 2 hàng × 4;
                         tầng/khoang/ô cửa theo shader look2: 1666 tầng 2,8 m khoang 2,4 m; gạch 1667/Victoria 3,0–3,6 m; văn phòng 2026 3,8 m khoang 3,0 m) + 3 tấm mái 8 × 13,5 m
                         + lời nhắc (năm bắt buộc) → $THUB/fac/loi-*.txt
  fac_thub.py atlas   → $THUB/fac/fac.png (2560 × 4320: 3 thời kỳ × 2 hàng × 4 mặt tiền), roof.png, fac.json (lưới, trung bình tuyến tính từng thời kỳ để hiệu chuẩn albedo)
Khác "vân vật liệu AI kiểu B" (PT/H-B, thua chấm mù — Kinh thánh §11.3): kiểu B = 9 mẫu vật liệu LÁT LẶP (vữa, gạch, ngói…) sinh tự do, albedo không hiệu chuẩn, lộ nối;
D2 = mặt tiền TRỌN (cửa, tầng, cửa hàng, vệt bẩn theo tầng) sửa từ bản vẽ lưới cửa của chính cảnh 3D (giữ vị trí ô cửa), gán theo nhà (băm mã nhà, 8 biến thể/thời kỳ),
albedo chuẩn hoá theo trung bình hàng atlas rồi nhân độ sáng albedo gốc của nhà (giữ tông/độ sáng đã duyệt); vân CC0 vẫn là lớp vi chi tiết bên dưới (trộn 8 %)."""
import json, os, sys
import numpy as np, cv2
THUB = os.environ.get('THUB', '/var/tmp/ldn/thub'); F = f'{THUB}/fac'; os.makedirs(F, exist_ok=True)
W, H = 2560, 1440; TW, TH = 640, 720; PPM = TW / 12.0          # 53,3 px/m; tấm 12 × 13,5 m
RNG = np.random.default_rng(7)
LOI = {
 '1666': (1666, "This image is a flat texture sheet of eight separate building facades (2 rows of 4 panels), drawn by us as simple shapes from our own 3D city of the year 1666. "
          "Repaint each panel as a realistic, evenly lit, shadow-free, straight-on photographic facade texture of an ordinary London timber-framed town house of the year 1666: "
          "lime-plastered infill, dark oak studs and rails, small leaded casement windows, plain shop openings with timber shutters at street level, weathering and coal soot, "
          "each panel a different house. Keep every window, door and floor line exactly where it is drawn and keep the panel layout and the thin dark gaps between panels. "
          "Fill each panel edge to edge. No sky, no ground, no roof, no perspective, no cast shadows, no people, no text, no signs, no lamps, no plants, no reflections. Nothing from after 1666."),
 '1667': (1900, "This image is a flat texture sheet of eight separate building facades (2 rows of 4 panels), drawn by us as simple shapes from our own 3D city. "
          "Repaint each panel as a realistic, evenly lit, shadow-free, straight-on photographic facade texture of an ordinary London brick building as it stood in the year 1900: "
          "the top row Georgian and later red and brown brick terraced houses with painted timber sash windows and stone sills; the bottom row Victorian commercial buildings in "
          "yellow London stock brick and soot-darkened stone with sash windows and plain shopfronts. Weathering and coal grime, each panel a different building. "
          "Keep every window, door and floor line exactly where it is drawn and keep the panel layout and the thin dark gaps between panels. Fill each panel edge to edge. "
          "No sky, no ground, no roof, no perspective, no cast shadows, no people, no text, no signs, no lamps, no plants, no reflections. Nothing from after 1900."),
 '2026': (2026, "This image is a flat texture sheet of eight separate building facades (2 rows of 4 panels), drawn by us as simple shapes from our own 3D city of the year 2026. "
          "Repaint each panel as a realistic, evenly lit, shadow-free, straight-on photographic facade texture of an ordinary office building in the City of London in 2026: "
          "Portland stone and pale concrete cladding, brick, metal window frames with dark glass, spandrel panels, subtle rain streaks, each panel a different building. "
          "Keep every window and floor line exactly where it is drawn and keep the panel layout and the thin dark gaps between panels. Fill each panel edge to edge. "
          "No sky, no ground, no roof, no perspective, no cast shadows, no people, no text, no logos, no signs, no lamps, no plants, no reflections of other buildings. Nothing from after 2026."),
 'mai': (1666, "This image is a flat texture sheet of three separate roof surfaces seen straight-on from above, drawn by us as simple lines. Repaint them as realistic, evenly lit, "
          "shadow-free photographic roof textures: left panel old hand-made clay roof tiles of London in the year 1666 with moss, lichen and coal soot; middle panel weathered "
          "grey Welsh slate as on London roofs of the 1800s; right panel a flat modern roof of 2026 with grey membrane, seams and gravel patches. Keep the courses exactly where they "
          "are drawn and keep the three panels and the dark gaps between them. Fill each panel edge to edge. No sky, no chimneys, no objects, no people, no text, no perspective, "
          "no cast shadows. Nothing from after 2026 in the right panel and nothing from after 1666 in the left panel."),
}


def rect(im, x0, y0, x1, y1, c): cv2.rectangle(im, (int(x0), int(y0)), (int(x1), int(y1)), c, -1)


def ve_mat(kind, i):
    t = np.zeros((TH, TW, 3), np.uint8); m2y = lambda y: TH - y * PPM; m2x = lambda x: x * PPM
    if kind == '1666':
        wall = [(176, 196, 214), (160, 192, 206), (168, 186, 196), (196, 214, 222)][i % 4]; rect(t, 0, 0, TW, TH, wall)
        st, bay = 2.8, 2.4
        for lv in range(5):
            y0 = lv * st
            for x in np.arange(0, 12.01, 0.78): rect(t, m2x(x), m2y(y0 + st), m2x(x + 0.12), m2y(y0), (34, 50, 75))
            for yy in (y0 + 0.0, y0 + 1.95, y0 + st - 0.18): rect(t, 0, m2y(yy + 0.2), TW, m2y(yy), (34, 50, 75))
            for b in range(5):
                u0 = b * bay
                if lv == 0:
                    if i % 2 == 0: rect(t, m2x(u0 + 0.25), m2y(2.15), m2x(u0 + bay - 0.25), m2y(0.25), (14, 18, 24))
                    else: rect(t, m2x(u0 + 0.5), m2y(1.7), m2x(u0 + 1.5), m2y(0.9), (20, 22, 26))
                else: rect(t, m2x(u0 + 0.35), m2y(y0 + 1.85), m2x(u0 + bay - 0.35), m2y(y0 + 0.85), (30, 26, 22))
    elif kind == '1667':
        vic = i >= 4; wall = [(58, 82, 150), (54, 74, 138), (70, 96, 160), (60, 78, 128)][i % 4] if not vic else [(120, 170, 196), (110, 150, 176), (96, 128, 150), (140, 176, 196)][i % 4]
        rect(t, 0, 0, TW, TH, wall); st, bay = (3.0, 2.3) if not vic else (3.6, 2.6)
        for lv in range(5):
            y0 = lv * st
            for b in range(int(12 / bay) + 1):
                u0 = b * bay
                if lv == 0 and vic: rect(t, m2x(u0 + 0.2), m2y(3.0), m2x(u0 + bay - 0.2), m2y(0.3), (20, 20, 22))
                else:
                    wa, wb = ((0.65, 0.75), (bay - 0.65, 2.45)) if not vic else ((0.70, 0.70), (bay - 0.70, 2.80))
                    rect(t, m2x(u0 + wa[0] - 0.09), m2y(y0 + wb[1] + 0.09), m2x(u0 + wb[0] + 0.09), m2y(y0 + wa[1] - 0.09), (150, 160, 170))
                    rect(t, m2x(u0 + wa[0]), m2y(y0 + wb[1]), m2x(u0 + wb[0]), m2y(y0 + wa[1]), (32, 30, 28))
            if vic: rect(t, 0, m2y(y0 + st), TW, m2y(y0 + st - 0.25), (150, 170, 178))
    else:
        wall = [(176, 186, 190), (160, 170, 176), (130, 150, 170), (190, 196, 200)][i % 4]; rect(t, 0, 0, TW, TH, wall); st, bay = 3.8, 3.0
        for lv in range(4):
            y0 = lv * st
            for b in range(4):
                u0 = b * bay
                if i < 4: rect(t, m2x(u0 + 0.08), m2y(y0 + 3.1), m2x(u0 + bay - 0.08), m2y(y0 + 0.9), (52, 46, 40)); rect(t, m2x(u0 + bay / 2 - 0.05), m2y(y0 + 3.1), m2x(u0 + bay / 2 + 0.05), m2y(y0 + 0.9), (120, 120, 120))
                else: rect(t, m2x(u0 + 0.6), m2y(y0 + 3.0), m2x(u0 + bay - 0.6), m2y(y0 + 0.8), (52, 46, 40))
    return t


def ve():
    for kind in ('1666', '1667', '2026'):
        im = np.zeros((H, W, 3), np.uint8) + 12
        for i in range(8):
            r, c = divmod(i, 4); t = ve_mat(kind, i); im[r * TH + 4:(r + 1) * TH - 4, c * TW + 4:(c + 1) * TW - 4] = t[4:-4, 4:-4]
        cv2.imwrite(f'{F}/vao-{kind}.png', im); open(f'{F}/loi-{kind}.txt', 'w').write(LOI[kind][1])
    im = np.zeros((H, W, 3), np.uint8) + 12; pw = W // 3
    for j, (c0, step) in enumerate((((60, 84, 132), 0.20), ((96, 92, 88), 0.30), ((120, 122, 124), 1.5))):
        x0 = j * pw + 4; x1 = (j + 1) * pw - 4; rect(im, x0, 4, x1, H - 4, c0); pm = (pw - 8) / 8.0
        for y in np.arange(0, 13.5, step): cv2.line(im, (x0, int(4 + y * pm)), (x1, int(4 + y * pm)), tuple(int(v * 0.6) for v in c0), 2)
    cv2.imwrite(f'{F}/vao-mai.png', im); open(f'{F}/loi-mai.txt', 'w').write(LOI['mai'][1]); print('vẽ xong', F)


def s2l(x): x = x / 255.0; return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def atlas():
    rows = []; mean = []
    for kind in ('1666', '1667', '2026'):
        a = cv2.resize(cv2.imread(f'{F}/{kind}-ai.jpg'), (W, H), interpolation=cv2.INTER_LANCZOS4)
        blk = np.zeros((2 * TH, 4 * TW, 3), np.uint8)
        for i in range(8):
            r, c = divmod(i, 4); t = a[r * TH + 6:(r + 1) * TH - 6, c * TW + 6:(c + 1) * TW - 6]; blk[r * TH:(r + 1) * TH, c * TW:(c + 1) * TW] = cv2.resize(t, (TW, TH), interpolation=cv2.INTER_AREA)
        rows.append(blk); mean.append(s2l(blk[..., ::-1].astype(np.float64)).reshape(-1, 3).mean(0).round(4).tolist())
    fac = np.vstack(rows); cv2.imwrite(f'{F}/fac.png', fac)
    a = cv2.resize(cv2.imread(f'{F}/mai-ai.jpg'), (W, H), interpolation=cv2.INTER_LANCZOS4); pw = W // 3
    roof = np.hstack([cv2.resize(a[6:H - 6, j * pw + 6:(j + 1) * pw - 6], (pw, H), interpolation=cv2.INTER_AREA) for j in range(3)])
    cv2.imwrite(f'{F}/roof.png', roof); mean.append(s2l(roof[..., ::-1].astype(np.float64)).reshape(-1, 3).mean(0).round(4).tolist())
    J = {'fac_url': '/data/thub/fac/fac.png', 'roof_url': '/data/thub/fac/roof.png', 'grid': [4, 6, 12.0, 13.5], 'mean': mean}
    json.dump(J, open(f'{F}/fac.json', 'w'), indent=1); print(json.dumps(J))


if __name__ == '__main__':
    ve() if sys.argv[1] == 've' else atlas()
