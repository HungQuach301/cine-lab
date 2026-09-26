#!/opt/cine/bin/python
"""SHOT A (M0-W-CONS-A) - wide, profile facing right, walking lamplighter.

Every body proportion is read from the model sheet (unit H = head height) and
multiplied by H_PX. Only pose angles, placement in frame and background are
authored here. See README.md for interpretation of ambiguous points.

Usage:
  /opt/cine/bin/python shots/m0-consistency/shot-A/render.py [--sheet PATH]
"""
import argparse
import json
import math
import os
import random
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, HGT = 1920, 1080
SS = 8                      # supersampling factor for masks
FS = 4                      # supersampling factor for the colour frame
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- sheet ----
def find_sheet(arg):
    rel = os.path.join("reports", "m0", "consistency", "model-sheet.json")
    cands = []
    if arg:
        cands.append(arg)
    try:
        top = subprocess.check_output(["git", "-C", HERE, "rev-parse", "--show-toplevel"],
                                      text=True).strip()
        cands.append(os.path.join(top, rel))
        common = subprocess.check_output(["git", "-C", HERE, "rev-parse", "--git-common-dir"],
                                         text=True).strip()
        if not os.path.isabs(common):
            common = os.path.join(HERE, common)
        cands.append(os.path.join(os.path.dirname(os.path.abspath(common)), rel))
    except Exception:
        pass
    for c in cands:
        if os.path.isfile(c):
            return c
    raise SystemExit("model-sheet.json not found; pass --sheet PATH")


# ------------------------------------------------------------- geometry ----
def v(a, r=1.0):
    """unit vector for angle a (degrees, 0 = +x right, 90 = down in image)."""
    t = math.radians(a)
    return (r * math.cos(t), r * math.sin(t))


def add(p, q, s=1.0):
    return (p[0] + q[0] * s, p[1] + q[1] * s)


def limb_poly(root, ang, length, width, n=48):
    """Limb: flat end at the root joint, straight sides, semicircular tip.
    Extent along the axis from root joint to tip = length (exactly)."""
    r = width / 2.0
    d = v(ang)
    nrm = (-d[1], d[0])
    cap_c = add(root, d, length - r)
    pts = [add(root, nrm, r)]
    for i in range(n + 1):
        t = math.radians(ang + 90 - 180 * i / n)  # sweep from +nrm through tip to -nrm
        pts.append((cap_c[0] + r * math.cos(t), cap_c[1] + r * math.sin(t)))
    pts.append(add(root, nrm, -r))
    return pts, cap_c


def ellipse_poly(c, rx, ry, n=128, ang=0.0):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((c[0] + x * ca - y * sa, c[1] + x * sa + y * ca))
    return out


def rrect_poly(c, w, h, r, ang=0.0, n=12):
    """rounded rectangle centred at c, rotated by ang degrees."""
    r = min(r, w / 2, h / 2)
    corners = [(w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
               (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)]
    pts = []
    for cx, cy, a0 in corners:
        for i in range(n + 1):
            t = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return [(c[0] + x * ca - y * sa, c[1] + x * sa + y * ca) for x, y in pts]


# ---------------------------------------------------------------- build ----
def build_character(S, POSE):
    """Returns dict name -> (polygon in H units, fill colour, layer).
    Origin: hip joint (torso bottom centre); +x right (facing), +y down."""
    P = {}
    t = S["torso"]
    hip = (0.0, 0.0)
    torso_top_y = -t["length"]
    # torso: trapezoid, upright; top_width at top, bottom_width at bottom
    P["torso"] = ([(-t["top_width"] / 2, torso_top_y), (t["top_width"] / 2, torso_top_y),
                   (t["bottom_width"] / 2, 0.0), (-t["bottom_width"] / 2, 0.0)], t["color"])
    # neck: rectangle standing on torso top
    nk = S["neck"]
    neck_top = torso_top_y - nk["length"]
    P["neck"] = ([(-nk["width"] / 2, neck_top), (nk["width"] / 2, neck_top),
                  (nk["width"] / 2, torso_top_y + 0.05), (-nk["width"] / 2, torso_top_y + 0.05)],
                 nk["color"])
    # head: ellipse whose bottom touches the neck top; axis vertical
    hd = S["head"]
    head_c = (0.0, neck_top - hd["length"] / 2)
    P["head"] = (ellipse_poly(head_c, hd["width"] / 2, hd["length"] / 2), hd["color"])
    head_top = neck_top - hd["length"]
    # hat: brim + crown, total height = hat.length, sits down over the crown
    ht = S["hat"]
    brim_bottom = head_top + POSE["hat_sink"] * hd["length"]
    brim_th = POSE["brim_thickness_frac"] * ht["length"]
    crown_h = ht["length"] - brim_th
    crown_w = hd["width"] * POSE["crown_width_frac"]
    P["hat_brim"] = (rrect_poly((POSE["hat_shift"], brim_bottom - brim_th / 2), ht["width"],
                                brim_th, brim_th / 2), ht["color"])
    cb = brim_bottom - brim_th + 0.01
    cx0 = POSE["hat_shift"]
    P["hat_crown"] = ([(cx0 - crown_w / 2, cb), (cx0 + crown_w / 2, cb),
                       (cx0 + crown_w / 2 * 0.92, cb - crown_h),
                       (cx0 - crown_w / 2 * 0.92, cb - crown_h)], ht["color"])
    P["hat_band"] = ([(cx0 - crown_w / 2, cb - crown_h * 0.05), (cx0 + crown_w / 2, cb - crown_h * 0.05),
                      (cx0 + crown_w / 2 * 0.985, cb - crown_h * 0.28),
                      (cx0 - crown_w / 2 * 0.985, cb - crown_h * 0.28)], "#7a3b2a")
    # eye + ear (inside the head silhouette, do not change it)
    P["eye"] = (ellipse_poly(add(head_c, (hd["width"] * 0.30, 0.02)), 0.045, 0.06, 24), "#231a1c")
    P["ear"] = (ellipse_poly(add(head_c, (-hd["width"] * 0.05, 0.06)), 0.08, 0.12, 24), "#c9a17f")

    shoulder = (0.0, torso_top_y + S["joints"]["shoulder_from_torso_top"])

    def arm(prefix, a_up, a_fore):
        ua, fa, hn = S["upper_arm"], S["forearm"], S["hand"]
        p1, elbow = limb_poly(shoulder, a_up, ua["length"], ua["width"])
        p2, wrist = limb_poly(elbow, a_fore, fa["length"], fa["width"])
        hand_c = add(elbow, v(a_fore), fa["length"])   # hand centred on the forearm tip
        P[prefix + "upper_arm"] = (p1, ua["color"])
        P[prefix + "forearm"] = (p2, fa["color"])
        P[prefix + "hand"] = (ellipse_poly(hand_c, hn["width"] / 2, hn["length"] / 2, 48), hn["color"])
        return hand_c

    def leg(prefix, a_th, a_sh, a_ft):
        th, sh, ft = S["thigh"], S["shin"], S["foot"]
        p1, knee = limb_poly(hip, a_th, th["length"], th["width"])
        p2, ankle = limb_poly(knee, a_sh, sh["length"], sh["width"])
        # foot: rounded rect, length along a_ft, thickness = foot.width;
        # its top edge passes through the ankle, heel set back by one shin radius.
        d = v(a_ft)
        nrm = (-d[1], d[0])              # points "down" relative to the sole for a_ft ~ 0
        back = sh["width"] / 2
        centre = add(add(ankle, d, ft["length"] / 2 - back), nrm, ft["width"] / 2)
        P[prefix + "thigh"] = (p1, th["color"])
        P[prefix + "shin"] = (p2, sh["color"])
        P[prefix + "foot"] = (rrect_poly(centre, ft["length"], ft["width"], ft["width"] / 2, a_ft),
                              ft["color"])

    # far side (behind torso), then near side
    arm("far_", *POSE["far_arm"])
    leg("far_", *POSE["far_leg"])
    leg("near_", *POSE["near_leg"])
    hand = arm("near_", *POSE["near_arm"])

    # lamplighter pole through the near hand
    pl = S["pole"]
    d = v(POSE["pole_angle"])
    bottom = add(hand, d, -POSE["pole_grip_frac"] * pl["length"])
    top = add(bottom, d, pl["length"])
    nrm = (-d[1] * pl["width"] / 2, d[0] * pl["width"] / 2)
    P["pole"] = ([add(bottom, nrm), add(top, nrm), add(top, nrm, -1), add(bottom, nrm, -1)], pl["color"])
    # small brass wick-holder + flame at the tip (decorative, no sheet size)
    P["_pole_top"] = (top, d)
    return P


DRAW_ORDER = ["far_upper_arm", "far_forearm", "far_hand",
              "far_thigh", "far_shin", "far_foot",
              "near_thigh", "near_shin", "near_foot",
              "neck", "torso",
              "head", "eye", "ear", "hat_crown", "hat_band", "hat_brim",
              "pole", "near_upper_arm", "near_forearm", "near_hand"]

# mask name -> polygon key (near-camera limb)
MASK_KEYS = {"head": "head", "torso": "torso",
             "upper_arm": "near_upper_arm", "forearm": "near_forearm",
             "thigh": "near_thigh", "shin": "near_shin"}


def shade(hexc, k):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (int(r * k), int(g * k), int(b * k))


# ------------------------------------------------------------ background ----
def background():
    img = np.zeros((HGT, W, 3), np.float32)
    horizon = 700
    ys = np.arange(HGT, dtype=np.float32)[:, None]
    top, mid, low = np.array([28, 30, 68]), np.array([110, 72, 110]), np.array([236, 150, 96])
    t = np.clip(ys / horizon, 0, 1)
    sky = np.where(t < 0.6, top + (mid - top) * (t / 0.6), mid + (low - mid) * ((t - 0.6) / 0.4))
    img[:] = sky[:, None, :]
    im = Image.fromarray(img.astype(np.uint8), "RGB")
    d = ImageDraw.Draw(im)
    rng = random.Random(7)
    # far row of houses
    x = -20
    while x < W:
        w = rng.randint(90, 170)
        h = rng.randint(110, 210)
        base = horizon
        col = (52, 40, 66)
        d.rectangle([x, base - h, x + w, base], fill=col)
        roof = rng.choice(["gable", "flat", "gable"])
        if roof == "gable":
            d.polygon([(x - 6, base - h), (x + w / 2, base - h - rng.randint(40, 70)), (x + w + 6, base - h)],
                      fill=col)
        if rng.random() < 0.6:
            cx = x + rng.randint(15, max(16, w - 25))
            d.rectangle([cx, base - h - 38, cx + 14, base - h + 2], fill=col)
        for wy in range(base - h + 25, base - 30, 42):
            for wx in range(x + 16, x + w - 24, 34):
                if rng.random() < 0.28:
                    d.rectangle([wx, wy, wx + 12, wy + 18], fill=(250, 196, 110))
                elif rng.random() < 0.5:
                    d.rectangle([wx, wy, wx + 12, wy + 18], fill=(70, 56, 86))
        x += w + rng.randint(0, 14)
    # pavement and road
    d.rectangle([0, horizon, W, 740], fill=(74, 62, 80))
    d.rectangle([0, 740, W, 748], fill=(98, 86, 104))
    d.rectangle([0, 748, W, HGT], fill=(46, 42, 58))
    for i in range(0, W, 120):
        d.rectangle([i, 900, i + 60, 906], fill=(64, 58, 76))
    # an unlit street lamp ahead of the lamplighter
    lx = 1500
    d.rectangle([lx - 6, 470, lx + 6, 744], fill=(34, 30, 42))
    d.rectangle([lx - 22, 440, lx + 22, 476], fill=(34, 30, 42))
    d.polygon([(lx - 28, 440), (lx, 418), (lx + 28, 440)], fill=(34, 30, 42))
    d.rectangle([lx - 16, 446, lx + 16, 470], fill=(84, 78, 96))
    return im


# ----------------------------------------------------------------- main ----
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--out", default=HERE)
    a = ap.parse_args()
    sheet_path = find_sheet(a.sheet)
    S = json.load(open(sheet_path))

    TARGET_HEIGHT_PX = 320.0                          # brief: character ~320 px tall
    H_PX = TARGET_HEIGHT_PX / S["total_height_H"]     # px per 1 H

    # Authored pose (angles in degrees; 0 = pointing right, 90 = straight down)
    POSE = {
        "near_leg": (90 - 22, 90 - 8, -2),      # near leg forward: thigh 22 deg fwd, knee slightly bent, foot flat
        "far_leg": (90 + 20, 90 + 38, 28),      # far leg back: toe-off, heel lifted
        "near_arm": (90 - 38, -18, None),       # near arm forward, forearm raised holding pole
        "far_arm": (90 + 30, 90 + 18, None),    # far arm swinging back
        "pole_angle": -58,                      # pole rises forward-up
        "pole_grip_frac": 0.30,                 # hand grips at 30% of pole length from its bottom
        "hat_sink": 0.15,                       # brim bottom sits 0.15 * head.length below head top
        "brim_thickness_frac": 0.18,            # brim thickness = 18% of hat.length
        "crown_width_frac": 0.90,               # crown width = 90% of head.width
        "hat_shift": -0.02,
    }
    POSE["near_arm"] = POSE["near_arm"][:2]
    POSE["far_arm"] = POSE["far_arm"][:2]

    P = build_character(S, POSE)
    pole_top, pole_dir = P.pop("_pole_top")

    # place: lowest foot point on the pavement line; character at x ~ 1/3 of frame
    GROUND_Y = 738.0
    ANCHOR_X = 760.0
    lowest = max(y for k in ("near_foot", "far_foot") for _, y in P[k][0])
    ox, oy = ANCHOR_X, GROUND_Y - lowest * H_PX

    def to_px(pts, ss=1):
        return [((ox + x * H_PX) * ss, (oy + y * H_PX) * ss) for x, y in pts]

    os.makedirs(os.path.join(a.out, "masks"), exist_ok=True)

    # --- masks: each part alone, same transform, binary white on black
    for name, key in MASK_KEYS.items():
        m = Image.new("L", (W * SS, HGT * SS), 0)
        ImageDraw.Draw(m).polygon(to_px(P[key][0], SS), fill=255)
        m = m.resize((W, HGT), Image.BOX)
        m = m.point(lambda p: 255 if p >= 128 else 0)
        m.convert("RGB").save(os.path.join(a.out, "masks", f"{name}.png"))

    # --- frame
    bg = background()
    # ground shadow + lamp glow layer
    glow = Image.new("RGB", (W, HGT), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    ftip = (ox + pole_top[0] * H_PX, oy + pole_top[1] * H_PX)
    gd.ellipse([ftip[0] - 70, ftip[1] - 70, ftip[0] + 70, ftip[1] + 70], fill=(120, 80, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    bg = Image.fromarray(np.clip(np.asarray(bg, np.int32) + np.asarray(glow, np.int32), 0, 255).astype(np.uint8))

    FSS = FS
    big = bg.resize((W * FSS, HGT * FSS), Image.NEAREST)
    d = ImageDraw.Draw(big)
    cx = ox * FSS
    d.ellipse([cx - 1.6 * H_PX * FSS, (GROUND_Y - 6) * FSS, cx + 1.9 * H_PX * FSS, (GROUND_Y + 8) * FSS],
              fill=(40, 32, 48, 255))
    for key in DRAW_ORDER:
        if key not in P:
            continue
        pts, col = P[key]
        fill = shade(col, 0.72) if key.startswith("far_") else shade(col, 1.0)
        d.polygon(to_px(pts, FSS), fill=fill)
    # wick holder + flame
    hx, hy = ftip
    d.ellipse([(hx - 5) * FSS, (hy - 5) * FSS, (hx + 5) * FSS, (hy + 5) * FSS], fill=(190, 150, 70))
    d.ellipse([(hx - 4) * FSS, (hy - 16) * FSS, (hx + 4) * FSS, (hy - 3) * FSS], fill=(255, 214, 120))
    d.ellipse([(hx - 2) * FSS, (hy - 11) * FSS, (hx + 2) * FSS, (hy - 4) * FSS], fill=(255, 250, 220))
    frame = big.convert("RGB").resize((W, HGT), Image.LANCZOS)
    frame.save(os.path.join(a.out, "frame.png"))

    meta = {"sheet": sheet_path, "H_px": H_PX, "target_height_px": TARGET_HEIGHT_PX,
            "origin_hip_px": [ox, oy], "ground_y": GROUND_Y, "supersample_masks": 8, "supersample_frame": FS,
            "pose": POSE, "masks": {k: f"masks/{k}.png" for k in MASK_KEYS}}
    with open(os.path.join(a.out, "render-meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"sheet={sheet_path}\nH_px={H_PX:.4f}\nwrote frame.png + {len(MASK_KEYS)} masks")


if __name__ == "__main__":
    main()
