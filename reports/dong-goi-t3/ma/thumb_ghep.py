#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 2 · ghép thumbnail từ ảnh nền dựng bằng máy V7 (3840×2160, không chữ) — 4 hướng × 2 biến thể.
Chữ: Inter Display (RIGHTS K2-F1). Lề an toàn 5 %; tránh góc dưới phải 18 % × 12 % (YouTube phủ thời lượng). Không cờ, không mũi tên chỉ người, không ảnh AI.
Ra: <out>/<tên>-3840x2160.png, -1280x720.png, -360x202.png, -168x94.png + do-chu.json (tương phản chữ/nền WCAG, cỡ chữ).
Dùng: thumb_ghep.py <thư mục nền 4K: <cảnh>/00000.jpg> <out>"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
R, O = Path(sys.argv[1]), Path(sys.argv[2]); O.mkdir(parents=True, exist_ok=True)
W, H = 3840, 2160; FD = "/usr/share/fonts/opentype/inter/"
def F(w, px): return ImageFont.truetype(FD + {"b": "InterDisplay-Black.otf", "x": "InterDisplay-ExtraBold.otf", "s": "InterDisplay-SemiBold.otf"}[w], px)
GOLD, INK, WHITE = (242, 193, 78), (24, 27, 33), (250, 248, 242)
def nen(name, lift=None):
    im = Image.open(R / name / "00000.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
    if lift:   # chỉ chỉnh tông toàn khung (gamma + độ sáng), không thêm/bớt nội dung
        a = np.asarray(im).astype(np.float32) / 255; a = np.clip((a ** lift[0]) * lift[1], 0, 1); im = Image.fromarray((a * 255).astype(np.uint8))
    return im
def diag(a, b, x_top=0.60, x_bot=0.42, seam=10):
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m); d.polygon([(0, 0), (int(W * x_top), 0), (int(W * x_bot), H), (0, H)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(3)); out = Image.composite(a, b, m); d = ImageDraw.Draw(out)
    d.line([(int(W * x_top), 0), (int(W * x_bot), H)], fill=(245, 240, 228), width=seam); return out
def grad_bottom(im, h=0.42, a=0.55):   # nền tối dần ở đáy để chữ trắng đủ tương phản (không phải dải đặc)
    g = np.linspace(0, 1, int(H * h)) ** 1.6 * a; arr = np.asarray(im).astype(np.float32); y0 = H - len(g)
    arr[y0:] *= (1 - g)[:, None, None]; return Image.fromarray(arr.astype(np.uint8))
def grad_top(im, h=0.28, a=0.45):
    g = np.linspace(1, 0, int(H * h)) ** 1.6 * a; arr = np.asarray(im).astype(np.float32); arr[:len(g)] *= (1 - g)[:, None, None]; return Image.fromarray(arr.astype(np.uint8))
DO = {}
def lum(c):
    c = np.asarray(c, np.float32) / 255; c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4); return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]
def ratio(l1, l2): a, b = max(l1, l2), min(l1, l2); return (a + 0.05) / (b + 0.05)
def text(im, name, s, font, xy, fill, anchor="la", box=None, shadow=True, key=None):
    d = ImageDraw.Draw(im); bb = d.textbbox(xy, s, font=font, anchor=anchor)
    a0 = np.asarray(im)[max(0, bb[1]):bb[3], max(0, bb[0]):bb[2]]; lb0 = float(np.median(lum(a0.reshape(-1, 3))))   # nền gốc (trước hộp/bóng)
    if box:
        pad = box.get("pad", 40); r = [bb[0] - pad, bb[1] - pad * 0.7, bb[2] + pad, bb[3] + pad * 0.7]
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle(r, radius=box.get("rad", 18), fill=box["fill"] + (box.get("a", 235),)); im.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")); d = ImageDraw.Draw(im)
    elif shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 6, xy[1] + 8), s, font=font, fill=(0, 0, 0, 200), anchor=anchor)
        sh = sh.filter(ImageFilter.GaussianBlur(14)); im.paste(Image.alpha_composite(im.convert("RGBA"), sh).convert("RGB")); d = ImageDraw.Draw(im)
    # đo nền ngay dưới chữ TRƯỚC khi vẽ chữ (sau hộp/bóng)
    a = np.asarray(im)[max(0, bb[1]):bb[3], max(0, bb[0]):bb[2]]; lb = float(np.median(lum(a.reshape(-1, 3))))
    d.text(xy, s, font=font, fill=fill, anchor=anchor, stroke_width=0)
    DO.setdefault(name, []).append({"chu": s, "cao_px_720": round((bb[3] - bb[1]) / 3, 1), "cao_ti_le": round((bb[3] - bb[1]) / H, 3), "bbox_720": [round(v / 3) for v in bb],
                                    "tuong_phan_wcag": round(ratio(float(lum(np.array(fill))), lb), 2), "nen_luminance_trung_vi": round(lb, 3),
                                    "tuong_phan_khong_hop_bong": round(ratio(float(lum(np.array(fill))), lb0), 2)})
    return bb
M = int(W * 0.05)   # lề an toàn 5 %
def band(im, name, s):   # dải năm (mã thể loại) — trên, giữa
    return text(im, name, s, F("x", 210), (W // 2, M + 40), GOLD, anchor="mt", box={"fill": INK, "a": 225, "pad": 50})
def place(im, name, s="GIBRALTAR", px=330, xy=None, anchor="ls"):
    return text(im, name, s, F("b", px), xy or (M + 20, H - M - 40), WHITE, anchor=anchor)
def badge(im, name, s="CONTESTED PLACES", xy=None, anchor="ls"):
    return text(im, name, s, F("s", 84), xy or (M + 20, H - M - 40), WHITE, anchor=anchor, box={"fill": INK, "a": 230, "pad": 26, "rad": 10})
def save(im, name):
    im.save(O / f"{name}-3840x2160.png", optimize=True)
    for w, h in ((1280, 720), (360, 202), (168, 94)): im.resize((w, h), Image.LANCZOS).save(O / f"{name}-{w}x{h}.png", optimize=True)
B = {}
# [A] mã thể loại thuần — A1: phố + Rock từ vịnh (điểm B, 2026 ngày); A2: Rock + đường băng + La Línea (điểm D, 2026 ngày) + huy hiệu series (§11.2)
#  chữ tên nơi đặt trên NƯỚC/TRỜI hoặc trên chính Gibraltar — không đè lên La Línea (đất Tây Ban Nha) để tránh đọc thành tuyên bố chủ quyền
im = grad_bottom(grad_top(nen("B_day2026"))); band(im, "A1", "1704 → 2026"); place(im, "A1"); save(im, "A1")
im = grad_top(nen("D_day2026"), h=0.5, a=0.5); band(im, "A2", "1704 → 2026")
place(im, "A2", xy=(W - M - 30, int(H * 0.47)), anchor="rs"); badge(im, "A2", xy=(W - M - 30, int(H * 0.47) + 150), anchor="rt"); save(im, "A2")
# [B] mã thể loại + điểm lệch — B1: chia chéo đêm 13/9/1782 (10 pin nổi cháy, điểm B) ↔ đêm 2026 có đèn phố + đèn mép đường băng (điểm D, như shot H1); B2: toàn khung đêm vây hãm (máy thấp, lửa lớn)
im = diag(nen("NB_night1782", (0.82, 1.18)), nen("D_night2026c", (0.85, 1.15))); im = grad_bottom(im, a=0.35); band(im, "B1", "1782 → 2026"); place(im, "B1"); save(im, "B1")
im = grad_bottom(nen("NB2_night1782", (0.80, 1.20)), a=0.35); band(im, "B2", "1704 → 2026"); place(im, "B2"); save(im, "B2")
# [C] làn câu hỏi — Rock 3D tô nhẹ hai màu phe (§11.1: Anh #b03a2e, TBN #c9a227; eo đất để trung tính, không ranh) + hộp tối ≤ 2 từ
im = nen("D5_tint2026"); text(im, "C1", "WHY BRITISH?", F("b", 230), (W - M - 40, M + 60), WHITE, anchor="rt", box={"fill": INK, "a": 235, "pad": 56}); save(im, "C1")
im = nen("NW4_tint2026"); text(im, "C2", "WHOSE ROCK?", F("b", 230), (M + 40, M + 60), WHITE, anchor="lt", box={"fill": INK, "a": 235, "pad": 56}); save(im, "C2")
# [D] brief B Kinh thánh — không chữ, đối lập cùng điểm máy: D1 điểm B 13/9/1782 ngày (pin nổi vào trận) ↔ 2026; D2 điểm D 1938 (bãi cỏ, chưa đường băng) ↔ 2026
save(diag(nen("B_day1782"), nen("B_day2026")), "D1")
save(diag(nen("D_day1938"), nen("D_day2026")), "D2")
(O / "do-chu.json").write_text(json.dumps(DO, indent=1, ensure_ascii=False)); print(json.dumps(DO, ensure_ascii=False)[:2000])
