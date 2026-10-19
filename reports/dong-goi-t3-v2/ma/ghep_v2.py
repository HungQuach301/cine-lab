#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 v2 · ghép 8 ứng viên thumbnail V1…V8 (1280×720 + 3840×2160 + 360×202 + 168×94) từ: khung dựng V7B 4K (dựng thuần), ảnh [F] AI tăng cường
(gpt-image sửa từ khung gốc, đã ghép lại điểm ảnh gốc cho cờ — rào chắn Kinh thánh §11.3), ảnh thực [E] có giấy phép (Flickr CC BY 2.0, nguon-anh.json).
Chữ đặt bằng mã (Inter Display, RIGHTS K2-F1) — AI không vẽ chữ. Hai cỡ tên nơi: S = 8 % chiều cao, M = 11,5 % (vòng 1). Lề an toàn 5 %, tránh góc dưới phải.
Dùng: ghep_v2.py <thư mục khung 4K> <thư mục AI> <thư mục ảnh thực> <out>"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
R4, AI, PH, O = map(Path, sys.argv[1:5]); O.mkdir(parents=True, exist_ok=True)
W, H = 3840, 2160; M = int(W * 0.05); FD = "/usr/share/fonts/opentype/inter/"
def F(w, px): return ImageFont.truetype(FD + {"b": "InterDisplay-Black.otf", "x": "InterDisplay-ExtraBold.otf"}[w], px)
GOLD, INK, WHITE = (242, 193, 78), (24, 27, 33), (250, 248, 242)
CO = json.loads((AI / "co-px.json").read_text())   # vị trí cờ (px ở 2560×1440) chiếu từ toạ độ cảnh
def lift(im, g):
    a = np.asarray(im).astype(np.float32) / 255; a = np.clip((a ** g[0]) * g[1], 0, 1); return Image.fromarray((a * 255).astype(np.uint8))
def render(name, g=None):
    im = Image.open(R4 / name / "00000.jpg").convert("RGB").resize((W, H), Image.LANCZOS); return lift(im, g) if g else im
def ai(name, protect=None):
    """ảnh AI 2560×1440 → 4K; ghép lại điểm ảnh GỐC (khung vào) quanh mỗi cờ (bán kính 30 px @2560, mép mềm)"""
    a = Image.open(AI / f"{name}-ai.jpg").convert("RGB"); g = Image.open(AI / f"{name}-vao.png").convert("RGB").resize(a.size)
    if protect:
        m = Image.new("L", a.size, 0); d = ImageDraw.Draw(m)
        for x, y in protect.values():
            if 0 <= x < a.size[0] and 0 <= y < a.size[1]: d.ellipse([x - 30, y - 34, x + 30, y + 26], fill=255)
        a = Image.composite(g, a, m.filter(ImageFilter.GaussianBlur(4)))
    return a.resize((W, H), Image.LANCZOS)
def photo(fn, x0, x1, y0):   # cắt ảnh thực đúng 16:9 (không kéo méo): bề ngang x0..x1 (tỷ lệ), mép trên y0 (tỷ lệ), cao = ngang × 9/16
    p = Image.open(PH / fn).convert("RGB"); w, h = p.size; cw = int((x1 - x0) * w); ch = int(cw * 9 / 16); y = min(int(y0 * h), h - ch)
    assert ch <= h, "khung cắt cao hơn ảnh"; return p.crop((int(x0 * w), y, int(x0 * w) + cw, y + ch)).resize((W, H), Image.LANCZOS)
def diag(a, b, x_top=0.58, x_bot=0.42, seam=10):
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon([(0, 0), (int(W * x_top), 0), (int(W * x_bot), H), (0, H)], fill=255)
    out = Image.composite(a, b, m.filter(ImageFilter.GaussianBlur(3))); ImageDraw.Draw(out).line([(int(W * x_top), 0), (int(W * x_bot), H)], fill=(245, 240, 228), width=seam); return out
def grad_bottom(im, h=0.38, a=0.45):
    g = np.linspace(0, 1, int(H * h)) ** 1.6 * a; arr = np.asarray(im).astype(np.float32); arr[H - len(g):] *= (1 - g)[:, None, None]; return Image.fromarray(arr.astype(np.uint8))
DO = {}
def lum(c):
    c = np.asarray(c, np.float32) / 255; c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4); return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]
def text(im, name, s, font, xy, fill, anchor, box=None):
    d = ImageDraw.Draw(im); bb = d.textbbox(xy, s, font=font, anchor=anchor)
    if box:
        pad = box["pad"]; ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle([bb[0] - pad, bb[1] - pad * 0.7, bb[2] + pad, bb[3] + pad * 0.7], radius=18, fill=INK + (225,))
        im.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"))
    else:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 6, xy[1] + 8), s, font=font, fill=(0, 0, 0, 210), anchor=anchor)
        im.paste(Image.alpha_composite(im.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(14))).convert("RGB"))
    a = np.asarray(im)[max(0, bb[1]):bb[3], max(0, bb[0]):bb[2]]; lb = float(np.median(lum(a.reshape(-1, 3))))
    ImageDraw.Draw(im).text(xy, s, font=font, fill=fill, anchor=anchor); lt = float(lum(np.array(fill)))
    DO.setdefault(name, []).append({"chu": s, "cao_ti_le": round((bb[3] - bb[1]) / H, 3), "tuong_phan_wcag": round((max(lt, lb) + 0.05) / (min(lt, lb) + 0.05), 2)})
SIZE = {"S": 240, "M": 330}   # px chữ ở 4K → cao chữ ≈ 8 % / 11,5 % khung
def chu(im, name, band, size):
    text(im, name, band, F("x", 210), (W // 2, M + 40), GOLD, "mt", box={"pad": 50})
    text(im, name, "GIBRALTAR", F("b", SIZE[size]), (M + 20, H - M - 40), WHITE, "ls")
def save(im, name):
    im.save(O / f"{name}-3840x2160.png", optimize=True)
    for w, h in ((1280, 720), (360, 202), (168, 94)): im.resize((w, h), Image.LANCZOS).save(O / f"{name}-{w}x{h}.png", optimize=True)
NIGHT = (0.85, 1.12)
C = {}
# V1 [F] toàn khung đêm 13/9/1782 (điểm N12, máy 45 m cách 1,7 km, fov 26) — chữ S
im = grad_bottom(ai("F1-N12", CO["F1-N12"])); chu(im, "V1", "1704 → 2026", "S"); save(im, "V1"); C["V1"] = "[F] F1-N12 · chữ S"
# V2 [F] cận (N2r, máy 25 m cách ≈ 450 m tới pin nổi gần nhất, fov 46) — chữ M
im = grad_bottom(ai("F2-N2r", CO["F2-N2r"])); chu(im, "V2", "1704 → 2026", "M"); save(im, "V2"); C["V2"] = "[F] F2-N2r · chữ M"
# V3 [F] chia chéo cùng điểm máy N12: 1782 cháy ↔ 2026 phố đèn — chữ S
im = grad_bottom(diag(ai("F1-N12", CO["F1-N12"]), ai("F3-N12-2026"))); chu(im, "V3", "1782 → 2026", "S"); save(im, "V3"); C["V3"] = "[F] F1 ↔ F3 cùng điểm máy · chữ S"
# V4 [E] dựng thuần V7B 1782 (N12) ↔ ảnh thực bình minh 2008 (axmiller, CC BY 2.0) — chữ S, dải năm 'TODAY' (ảnh không phải 2026)
im = grad_bottom(diag(render("N12", NIGHT), photo("a3d5740d.jpg", 0.0, 1.0, 0.10))); chu(im, "V4", "1782 → TODAY", "S"); save(im, "V4"); C["V4"] = "[E] dựng N12 ↔ ảnh a3d5740d · chữ S"
# V5 [E] dựng thuần V7B cận (N2r) ↔ ảnh thực chiều từ La Línea 2008 (BY-YOUR-⌘, CC BY 2.0; cắt bỏ người ở mép trái) — chữ M
im = grad_bottom(diag(render("N2r", NIGHT), photo("1cc4493e.jpg", 0.0, 1.0, 0.02))); chu(im, "V5", "1782 → TODAY", "M"); save(im, "V5"); C["V5"] = "[E] dựng N2r ↔ ảnh 1cc4493e · chữ M"
# V6 ĐỐI CHỨNG dựng thuần V7B (N12, chỉ chỉnh tông toàn khung) — chữ S
im = grad_bottom(render("N12", NIGHT)); chu(im, "V6", "1704 → 2026", "S"); save(im, "V6"); C["V6"] = "dựng thuần V7B N12 · chữ S"
# V7 [F] chia chéo: F2 cận 1782 ↔ điểm D 2026 đêm DỰNG THUẦN V7B (đường băng có đèn) — chữ M. F4 (AI của khung D) bị LOẠI: AI thêm chi tiết kiến trúc (§11.3)
im = grad_bottom(diag(ai("F2-N2r", CO["F2-N2r"]), render("D2026n", NIGHT))); chu(im, "V7", "1782 → 2026", "M"); save(im, "V7"); C["V7"] = "[F] F2 ↔ dựng V7B D 2026 (đường băng) · chữ M"
# V8 = V1 với chữ M (thử cỡ chữ cùng ảnh)
im = grad_bottom(ai("F1-N12", CO["F1-N12"])); chu(im, "V8", "1704 → 2026", "M"); save(im, "V8"); C["V8"] = "[F] F1-N12 · chữ M (cặp thử cỡ với V1)"
(O / "do-chu.json").write_text(json.dumps(DO, indent=1, ensure_ascii=False)); (O / "mo-ta.json").write_text(json.dumps(C, indent=1, ensure_ascii=False)); print(json.dumps(DO, ensure_ascii=False)[:800])
