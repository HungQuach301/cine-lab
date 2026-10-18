"""Vẽ cảnh tổng hợp 1920×1080 cho selftest O2 (phiên K 1.15): pháo đài đá ven biển, cột cờ, cờ Union mẫu 1707 (Anh–Scotland: chữ thập St George
viền trắng + chéo trắng St Andrew trên nền lam) hoặc mẫu 1801 (thêm chéo đỏ St Patrick so le). Không dùng ảnh/tài sản ngoài; hạt giống cố định."""
import cv2, numpy as np

BLUE, RED, WHITE = (125, 36, 1), (46, 16, 200), (255, 255, 255)   # BGR


def union_flag(mau, h=600):
    """cờ tỉ lệ 1:2, cao h px; mau = 1707 | 1801"""
    w = 2 * h; F = np.zeros((h, w, 3), np.uint8); F[:] = BLUE
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # khoảng cách tới hai đường chéo (đơn vị px), dấu theo phía
    n = np.hypot(h, w)
    d1 = (h * xx - w * yy) / n            # chéo trên-trái → dưới-phải
    d2 = (h * xx + w * yy - w * h) / n    # chéo dưới-trái → trên-phải
    sw = h / 5.0                          # chéo trắng: 1/5 chiều cao (St Andrew + viền)
    F[(np.abs(d1) < sw / 2) | (np.abs(d2) < sw / 2)] = WHITE
    if mau == 1801:
        rw = h / 15.0                     # chéo đỏ St Patrick, so le: so le xoay vòng (góc cán trên: phần trắng rộng nằm trên)
        cx, cy = w / 2, h / 2
        q_tl = (xx < cx) & (yy < cy); q_br = (xx >= cx) & (yy >= cy); q_tr = (xx >= cx) & (yy < cy); q_bl = (xx < cx) & (yy >= cy)
        r1 = ((q_tl & (d1 < 0) & (d1 > -rw)) | (q_br & (d1 > 0) & (d1 < rw)))   # chéo trắng rộng ở phía trên tại góc cán trên
        r2 = ((q_tr & (d2 < 0) & (d2 > -rw)) | (q_bl & (d2 > 0) & (d2 < rw)))
        F[r1 | r2] = RED
    cw = h / 3.0; F[(np.abs(xx - w / 2) < cw / 2) | (np.abs(yy - h / 2) < cw / 2)] = WHITE   # chữ thập trắng (viền)
    rc = h / 5.0; F[(np.abs(xx - w / 2) < rc / 2) | (np.abs(yy - h / 2) < rc / 2)] = RED       # chữ thập đỏ St George
    return F


def canh(mau, co_h=90, seed=1782):
    """cảnh 1920×1080; cờ cao co_h px trên cột ở pháo đài; trả về (ảnh BGR, hộp cờ [x0, y0, x1, y1])"""
    rng = np.random.default_rng(seed); H, W = 1080, 1920
    yy = np.linspace(0, 1, H)[:, None, None]
    im = (np.array([235, 200, 150]) * (1 - yy) + np.array([215, 225, 230]) * yy).astype(np.float32) * np.ones((H, W, 3), np.float32)   # trời
    hz = 620; im[hz:] = np.array([120, 95, 45], np.float32) + rng.normal(0, 6, (H - hz, W, 3))                                           # biển
    # núi đá xa
    pts = np.array([[0, hz], [300, 470], [620, 380], [900, 300], [1180, 360], [1500, 420], [1920, 500], [1920, hz]], np.int32)
    cv2.fillPoly(im, [pts], (150, 160, 165))
    # pháo đài đá: thân + lỗ châu mai
    fx0, fx1, fy = 620, 1500, 560
    im[fy:hz + 40, fx0:fx1] = np.array([140, 165, 180], np.float32) + rng.normal(0, 10, (hz + 40 - fy, fx1 - fx0, 3))
    for x in range(fx0, fx1, 60): im[fy - 30:fy, x:x + 34] = np.array([135, 160, 175], np.float32) + rng.normal(0, 8, (30, 34, 3))
    for y in range(fy + 20, hz + 40, 28): im[y:y + 2, fx0:fx1] *= 0.8                                                                  # mạch đá
    # thuyền buồm nhỏ
    cv2.fillPoly(im, [np.array([[260, 700], [420, 700], [400, 725], [280, 725]], np.int32)], (40, 50, 70))
    cv2.fillPoly(im, [np.array([[335, 700], [335, 600], [395, 690]], np.int32)], (220, 230, 235))
    im = np.clip(im, 0, 255).astype(np.uint8)
    # cột cờ + cờ
    px, ptop = 1120, fy - 30 - int(co_h * 2.6)
    cv2.line(im, (px, fy - 30), (px, ptop), (60, 60, 70), max(3, co_h // 22))
    fl = cv2.resize(union_flag(mau), (2 * co_h, co_h), interpolation=cv2.INTER_AREA)
    x0, y0 = px + 3, ptop + 4; im[y0:y0 + co_h, x0:x0 + 2 * co_h] = fl
    return im, [x0, y0, x0 + 2 * co_h, y0 + co_h]
