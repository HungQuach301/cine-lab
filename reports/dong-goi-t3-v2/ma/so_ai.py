#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 v2 · tờ so gốc ↔ AI cho mỗi ảnh [F]: (trái) khung gốc V7B, (giữa) ảnh AI SAU khi ghép lại điểm ảnh gốc cho cờ, (phải) bản đồ chênh |ΔL*|.
Đo bằng máy: số đốm lửa (vùng cam bão hoà) gốc vs AI — số pin nổi cháy phải giữ nguyên; tỷ lệ điểm ảnh đổi > 12 L* theo dải (trời / Rock-phố / nước).
Danh sách phần đổi viết tay sau khi xem cận (báo cáo §2). Dùng: so_ai.py <thư mục AI> <out>"""
import json, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
AI, O = Path(sys.argv[1]), Path(sys.argv[2]); O.mkdir(parents=True, exist_ok=True); CO = json.loads((AI / "co-px.json").read_text())
def fires(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV); h = hsv[..., 0].astype(int) * 2; m = (((h >= 10) & (h <= 50)) & (hsv[..., 1] > 110) & (hsv[..., 2] > 200)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)); n, _, st, _ = cv2.connectedComponentsWithStats(m); return int(sum(1 for s in st[1:] if s[4] >= 150))
out = {}
for n in ["F1-N12", "F2-N2r", "F3-N12-2026", "F4-D2026"]:
    a = Image.open(AI / f"{n}-ai.jpg").convert("RGB"); g = Image.open(AI / f"{n}-vao.png").convert("RGB").resize(a.size)
    if n in CO:
        mk = Image.new("L", a.size, 0); d = ImageDraw.Draw(mk)
        for x, y in CO[n].values():
            if 0 <= x < a.size[0] and 0 <= y < a.size[1]: d.ellipse([x - 30, y - 34, x + 30, y + 26], fill=255)
        a = Image.composite(g, a, mk.filter(ImageFilter.GaussianBlur(4)))
    A = cv2.cvtColor(np.asarray(a), cv2.COLOR_RGB2BGR); G = cv2.cvtColor(np.asarray(g), cv2.COLOR_RGB2BGR)
    La = cv2.cvtColor(A, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32) * 100 / 255; Lg = cv2.cvtColor(G, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32) * 100 / 255; D = np.abs(La - Lg)
    Hh = D.shape[0]; bands = {"tren_40pct": (0, int(.40 * Hh)), "giua_40_65pct": (int(.40 * Hh), int(.65 * Hh)), "duoi_65pct": (int(.65 * Hh), Hh)}
    out[n] = {"dom_lua_goc": fires(G), "dom_lua_ai": fires(A), "ti_le_doi_gt12L": {k: round(float((D[y0:y1] > 12).mean()), 3) for k, (y0, y1) in bands.items()},
              "dL_tb": round(float(D.mean()), 2), "co_ghep_lai_px": CO.get(n, {})}
    hm = cv2.applyColorMap(np.clip(D * 4, 0, 255).astype(np.uint8), cv2.COLORMAP_INFERNO)
    W = 640; H = int(W * Hh / D.shape[1]); S = Image.new("RGB", (3 * W, H + 22), "white"); dr = ImageDraw.Draw(S)
    for i, (im, lab) in enumerate([(g, "goc V7B"), (a, "AI (co: ghep lai goc)"), (Image.fromarray(cv2.cvtColor(hm, cv2.COLOR_BGR2RGB)), "|dL*| x4")]):
        S.paste(im.resize((W, H)), (i * W, 22)); dr.text((i * W + 4, 4), f"{n} - {lab}", fill="black")
    S.save(O / f"so-{n}.jpg", quality=84)
(O / "so-ai.json").write_text(json.dumps(out, indent=1, ensure_ascii=False)); print(json.dumps(out, ensure_ascii=False, indent=0)[:1500])
