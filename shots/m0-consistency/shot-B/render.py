#!/opt/cine/bin/python
"""M0-W-CONS-B — Shot B: người thắp đèn, nhìn nghiêng quay sang trái, giơ sào thắp đèn.

Bộ dựng độc lập, chỉ đọc model sheet. Mọi kích thước nhân vật = hệ số trong model sheet x H (px).
Các hằng số "DIỄN GIẢI" (INTERP) là chỗ model sheet không quy định; xem README.md.

Chạy:  /opt/cine/bin/python shots/m0-consistency/shot-B/render.py --sheet reports/m0/consistency/model-sheet.json
"""
import argparse
import hashlib
import json
import math
import os

from PIL import Image, ImageDraw

W, HGT = 1920, 1080
SS = 4  # siêu lấy mẫu để khử răng cưa

# ---------------- Thông số bố cục & tư thế (không phải tỷ lệ bộ phận) ----------------
FIGURE_HEIGHT_PX = 820.0      # chiều cao nhân vật = total_height_H (không tính mũ)
GROUND_Y = 1066.0             # đáy bàn chân
FIG_X = 1250.0                # trục thân (vai/hông) theo x
# góc tính bằng độ, 0 = hướng sang phải, 90 = hướng xuống (toạ độ ảnh)
POSE = {
    "near_upper_arm": 180 + 8,    # gần ngang vai, hơi chếch lên, hướng về trái
    "near_forearm": 180 + 80,     # hướng lên, hơi ngả về trước
    "far_upper_arm": 90 - 12,     # buông thõng, hơi ra sau
    "far_forearm": 90 - 6,
    "near_thigh": 90 + 6,         # chân gần: hơi về trước (trái)
    "near_shin": 90 + 5,
    "far_thigh": 90 - 6,          # chân xa: hơi về sau (phải)
    "far_shin": 90 - 5,
    "pole": 180 + 24,             # sào chếch lên phía trước
}

# ---------------- DIỄN GIẢI (chi tiết model sheet không quy định), đơn vị H ----------------
INTERP = {
    "hat_overlap_head": 0.22,     # đáy vành mũ nằm dưới đỉnh đầu 0.22 H
    "hat_brim_thickness": 0.08,   # độ dày vành mũ
    "hat_crown_width_frac": 0.66, # bề rộng chóp mũ / bề rộng vành
    "pole_below_hand": 0.25,      # phần sào thò dưới bàn tay
    "hand_center_beyond_wrist": 0.5,  # tâm bàn tay = đầu mút cẳng tay + 0.5*hand.length
    "heel_behind_ankle": 0.12,    # gót thò ra sau mắt cá
}


def load_sheet(path):
    raw = open(path, "rb").read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def rgb(hexs):
    hexs = hexs.lstrip("#")
    return tuple(int(hexs[i:i + 2], 16) for i in (0, 2, 4))


def shade(c, k):
    return tuple(max(0, min(255, int(round(v * k)))) for v in c)


def unit(deg):
    a = math.radians(deg)
    return math.cos(a), math.sin(a)


def capsule(p0, deg, length, width, n=24):
    """Hình con nhộng; đầu mút bo tròn NẰM TRONG độ dài: tổng chiều dài dọc trục = length.
    p0 là khớp gốc (điểm đầu trục), trả về (đa giác, điểm cuối trục)."""
    ux, uy = unit(deg)
    nx, ny = -uy, ux
    r = width / 2.0
    L = max(length, width)
    a = (p0[0] + ux * r, p0[1] + uy * r)            # tâm cung gốc
    b = (p0[0] + ux * (L - r), p0[1] + uy * (L - r))  # tâm cung mút
    pts = []
    base = math.atan2(uy, ux)
    for i in range(n + 1):  # cung mút: từ +n sang -n qua hướng u
        t = base + math.pi / 2 - math.pi * i / n
        pts.append((b[0] + r * math.cos(t), b[1] + r * math.sin(t)))
    for i in range(n + 1):  # cung gốc
        t = base - math.pi / 2 - math.pi * i / n
        pts.append((a[0] + r * math.cos(t), a[1] + r * math.sin(t)))
    end = (p0[0] + ux * length, p0[1] + uy * length)
    return pts, end


def ellipse_poly(cx, cy, rx, ry, n=96):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def rect_poly(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


class Canvas:
    def __init__(self, bg=(0, 0, 0), mode="RGB"):
        self.img = Image.new(mode, (W * SS, HGT * SS), bg)
        self.d = ImageDraw.Draw(self.img, "RGBA" if mode == "RGB" else None)

    def poly(self, pts, fill):
        self.d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill)

    def line(self, p0, p1, width, fill):
        self.d.line([(p0[0] * SS, p0[1] * SS), (p1[0] * SS, p1[1] * SS)], fill=fill, width=max(1, int(width * SS)))

    def circle(self, c, r, fill):
        self.d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=fill)

    def final(self):
        return self.img.resize((W, HGT), Image.LANCZOS)


def build_figure(S):
    """Tính toàn bộ hình học nhân vật (px). Trả về dict các đa giác/khớp."""
    Hpx = FIGURE_HEIGHT_PX / S["total_height_H"]
    g = lambda part, key="length": S[part][key] * Hpx  # noqa: E731
    F = {"H_px": Hpx}

    # Trục đứng, từ dưới lên: đáy bàn chân -> mắt cá (foot.width) -> hông -> đỉnh thân -> cổ -> đầu
    ankle_y = GROUND_Y - g("foot", "width")
    # hông: đi ngược chuỗi chân gần theo góc tư thế
    tx, ty = unit(POSE["near_thigh"])
    sx, sy = unit(POSE["near_shin"])
    hip_y = ankle_y - (g("thigh") * ty + g("shin") * sy)
    hip = (FIG_X, hip_y)
    torso_top = hip_y - g("torso")
    head_bottom = torso_top - g("neck")
    head_top = head_bottom - g("head")
    F["hip"], F["torso_top"], F["head_top"] = hip, torso_top, head_top

    # Đầu: elip, trục dài dọc = head.length, bề ngang = head.width
    hc = (FIG_X, (head_top + head_bottom) / 2)
    F["head"] = ellipse_poly(hc[0], hc[1], g("head", "width") / 2, g("head") / 2)
    F["head_c"] = hc

    # Cổ: dài neck.length nối đáy đầu với đỉnh thân (vẽ chồng vào 2 bên để không hở)
    nw = g("neck", "width")
    F["neck"] = rect_poly(FIG_X - nw / 2, head_bottom - 0.25 * g("head"), FIG_X + nw / 2, torso_top + 0.05 * g("torso"))

    # Thân: hình thang, đỉnh top_width, đáy bottom_width, cao torso.length
    tw, bw = g("torso", "top_width"), g("torso", "bottom_width")
    F["torso"] = [(FIG_X - tw / 2, torso_top), (FIG_X + tw / 2, torso_top), (FIG_X + bw / 2, hip_y), (FIG_X - bw / 2, hip_y)]

    # Mũ: vành + chóp, tổng cao hat.length, vành rộng hat.width
    brim_bottom = head_top + INTERP["hat_overlap_head"] * Hpx
    hat_top = brim_bottom - g("hat")
    brim_top = brim_bottom - INTERP["hat_brim_thickness"] * Hpx
    hwid = g("hat", "width")
    cw = hwid * INTERP["hat_crown_width_frac"]
    F["hat_brim"] = rect_poly(FIG_X - hwid / 2, brim_top, FIG_X + hwid / 2, brim_bottom)
    F["hat_crown"] = rect_poly(FIG_X - cw / 2, hat_top, FIG_X + cw / 2, brim_top + 1)
    F["hat_band"] = rect_poly(FIG_X - cw / 2, brim_top - 0.07 * Hpx, FIG_X + cw / 2, brim_top)

    # Vai: dưới đỉnh thân shoulder_from_torso_top, nằm trên trục thân (nhìn nghiêng)
    shoulder = (FIG_X, torso_top + S["joints"]["shoulder_from_torso_top"] * Hpx)
    F["shoulder"] = shoulder

    def limb_chain(root, a1, p1, a2, p2):
        poly1, j = capsule(root, a1, g(p1), g(p1, "width"))
        poly2, tip = capsule(j, a2, g(p2), g(p2, "width"))
        return poly1, j, poly2, tip

    for side in ("near", "far"):
        ua, el, fa, wr = limb_chain(shoulder, POSE[f"{side}_upper_arm"], "upper_arm", POSE[f"{side}_forearm"], "forearm")
        F[f"{side}_upper_arm"], F[f"{side}_elbow"], F[f"{side}_forearm"], F[f"{side}_wrist"] = ua, el, fa, wr
        fx, fy = unit(POSE[f"{side}_forearm"])
        k = INTERP["hand_center_beyond_wrist"] * g("hand")
        F[f"{side}_hand_c"] = (wr[0] + fx * k, wr[1] + fy * k)

        th, kn, sh, an = limb_chain(hip, POSE[f"{side}_thigh"], "thigh", POSE[f"{side}_shin"], "shin")
        F[f"{side}_thigh"], F[f"{side}_knee"], F[f"{side}_shin"], F[f"{side}_ankle"] = th, kn, sh, an
        # Bàn chân: cao foot.width dưới mắt cá, dài foot.length, mũi chân hướng trái
        heel = an[0] + INTERP["heel_behind_ankle"] * Hpx
        fh = g("foot", "width")
        F[f"{side}_foot"] = [(heel, an[1]), (heel, an[1] + fh), (heel - g("foot"), an[1] + fh),
                             (heel - g("foot"), an[1] + fh * 0.45), (heel - g("foot") + fh * 0.6, an[1])]

    # Sào: xuyên tâm bàn tay trước
    px, py = unit(POSE["pole"])
    hcn = F["near_hand_c"]
    below = INTERP["pole_below_hand"] * Hpx
    p_bot = (hcn[0] - px * below, hcn[1] - py * below)
    p_top = (p_bot[0] + px * g("pole"), p_bot[1] + py * g("pole"))
    F["pole"] = (p_bot, p_top)
    return F


def draw_background(cv, lamp):
    wall = (40, 30, 34)
    cv.poly(rect_poly(0, 0, W, HGT), wall + (255,))
    # Quầng đèn: các vòng phẳng đồng tâm (flat vector)
    for r, a in ((900, 18), (680, 22), (500, 26), (340, 32), (210, 40)):
        cv.circle(lamp, r, (255, 170, 80, a))
    # Gạch: hàng so le, vạch vữa tối
    bh, bw = 46, 118
    mortar = (22, 16, 20, 255)
    y, row = 0, 0
    while y < 960:
        cv.line((0, y), (W, y), 4, mortar)
        off = (bw // 2) * (row % 2)
        x = -off
        while x < W:
            cv.line((x, y), (x, y + bh), 4, mortar)
            x += bw
        y += bh
        row += 1
    # Vỉa hè
    cv.poly(rect_poly(0, 960, W, HGT), (62, 50, 50, 255))
    cv.poly(rect_poly(0, 960, W, 972), (58, 44, 42, 255))
    for r, a in ((700, 20), (420, 26)):
        cv.poly(ellipse_poly(lamp[0] + 60, 1000, r, 50), (255, 170, 80, a))


def draw_lamp(cv, tip):
    iron = (26, 22, 24, 255)
    # Đèn gắn tường: tay sắt từ mép trên, chụp đèn treo ngay trên đầu sào
    cx, bot = tip[0] - 4, tip[1] - 6
    top = bot - 78
    cv.line((cx, top - 6), (cx, -10), 7, iron)
    cv.line((cx, top - 30), (cx - 120, -10), 6, iron)
    cv.poly([(cx - 30, top), (cx + 30, top), (cx + 22, bot), (cx - 22, bot)], (255, 214, 140, 255))
    cv.poly([(cx - 42, top + 2), (cx, top - 30), (cx + 42, top + 2)], iron)
    cv.poly(rect_poly(cx - 26, bot - 2, cx + 26, bot + 8), iron)
    cv.line((cx - 30, top), (cx - 22, bot), 4, iron)
    cv.line((cx + 30, top), (cx + 22, bot), 4, iron)
    # Ngọn lửa vừa bén
    cv.poly(ellipse_poly(cx, bot - 30, 9, 20), (255, 250, 220, 255))
    return (cx, bot - 40)


def draw_figure(cv, S, F):
    C = {k: rgb(v["color"]) + (255,) for k, v in S.items() if isinstance(v, dict) and "color" in v}
    far = lambda c: shade(c[:3], 0.72) + (255,)  # noqa: E731
    Hpx = F["H_px"]
    # Lớp xa máy quay
    cv.poly(F["far_upper_arm"], far(C["upper_arm"]))
    cv.poly(F["far_forearm"], far(C["forearm"]))
    cv.circle(F["far_elbow"], S["forearm"]["width"] * Hpx / 2, far(C["forearm"]))
    cv.circle(F["far_hand_c"], S["hand"]["length"] * Hpx / 2, far(C["hand"]))
    cv.poly(F["far_thigh"], far(C["thigh"]))
    cv.poly(F["far_shin"], far(C["shin"]))
    cv.circle(F["far_knee"], S["shin"]["width"] * Hpx / 2, far(C["shin"]))
    cv.poly(F["far_foot"], far(C["foot"]))
    # Chân gần
    cv.poly(F["near_thigh"], C["thigh"])
    cv.poly(F["near_shin"], C["shin"])
    cv.circle(F["near_knee"], S["shin"]["width"] * Hpx / 2, C["shin"])
    cv.poly(F["near_foot"], C["foot"])
    # Cổ, thân, đầu, mũ
    cv.poly(F["neck"], C["neck"])
    cv.poly(F["torso"], C["torso"])
    cv.poly(F["head"], C["head"])
    hc = F["head_c"]
    hw = S["head"]["width"] * Hpx / 2
    cv.circle((hc[0] - hw * 0.55, hc[1] - 0.04 * Hpx), 0.045 * Hpx, (30, 22, 26, 255))    # mắt, phía trái
    cv.circle((hc[0] + hw * 0.15, hc[1] + 0.02 * Hpx), 0.09 * Hpx, shade(C["head"][:3], 0.85) + (255,))  # tai
    cv.poly(F["hat_crown"], C["hat"])
    cv.poly(F["hat_band"], (120, 60, 40, 255))
    cv.poly(F["hat_brim"], C["hat"])
    # Sào (giữa thân và tay trước: tay trước nắm lên sào)
    pb, pt = F["pole"]
    cv.line(pb, pt, S["pole"]["width"] * Hpx, C["pole"])
    # Tay gần
    cv.poly(F["near_upper_arm"], C["upper_arm"])
    cv.poly(F["near_forearm"], C["forearm"])
    cv.circle(F["near_elbow"], S["forearm"]["width"] * Hpx / 2, C["forearm"])
    cv.circle(F["near_hand_c"], S["hand"]["length"] * Hpx / 2, C["hand"])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", default=os.path.join(here, "../../../reports/m0/consistency/model-sheet.json"))
    ap.add_argument("--out", default=here)
    a = ap.parse_args()
    S, sha = load_sheet(a.sheet)
    F = build_figure(S)

    cv = Canvas()
    # vị trí đèn phụ thuộc đầu sào: tính trước, vẽ nền rồi đèn
    pt = F["pole"][1]
    draw_background(cv, (pt[0], pt[1] - 50))
    draw_lamp(cv, pt)
    draw_figure(cv, S, F)
    os.makedirs(os.path.join(a.out, "masks"), exist_ok=True)
    cv.final().save(os.path.join(a.out, "frame.png"))

    mask_src = {
        "head": F["head"], "torso": F["torso"],
        "upper_arm": F["near_upper_arm"], "forearm": F["near_forearm"],
        "thigh": F["near_thigh"], "shin": F["near_shin"],
    }
    assert set(mask_src) == set(S["measured_parts"]), "measured_parts không khớp"
    for part, poly in mask_src.items():
        m = Canvas(bg=0, mode="L")
        m.d.polygon([(x * SS, y * SS) for x, y in poly], fill=255)
        m.final().point(lambda v: 255 if v >= 128 else 0).save(os.path.join(a.out, "masks", f"{part}.png"))

    meta = {
        "sheet_path": os.path.relpath(os.path.abspath(a.sheet), os.path.abspath(os.path.join(here, "../../.."))),
        "sheet_sha256": sha,
        "H_px": F["H_px"],
        "figure_height_px_excl_hat": FIGURE_HEIGHT_PX,
        "pose_deg": POSE,
        "interpretation_H": INTERP,
        "joints_px": {k: [round(v[0], 2), round(v[1], 2)] for k, v in F.items()
                      if k in ("shoulder", "hip", "near_elbow", "near_wrist", "near_knee", "near_ankle", "near_hand_c")},
    }
    json.dump(meta, open(os.path.join(a.out, "render-meta.json"), "w"), indent=2, ensure_ascii=False)
    print(f"H = {F['H_px']:.4f} px; sheet sha256 {sha[:12]}; out -> {a.out}")


if __name__ == "__main__":
    main()
