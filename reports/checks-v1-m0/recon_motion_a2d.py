"""Phiên K dựng lại dữ liệu chuyển động của a-2d-mb8.mp4 từ mã cảnh M0 (scene2d.js, scene.json,
model-sheet.json) — minh hoạ H1/H1b trên hình render thật; KHÔNG phải dữ liệu do render xuất."""
import json, math, sys
import numpy as np
S = {"width": 1920, "fps": 24, "duration_s": 10, "camera": {"pan_px_per_s": 60},
     "character": {"start_x": -250, "end_x": 2500, "ground_y": 900, "height_px": 260, "step_hz": 1.8}}
M = {"head": 1.0, "neck": 0.15, "torso": 1.9, "thigh": 1.2, "shin": 1.15, "foot_w": 0.2, "total": 5.6}
def lcg(seed):
    s = [seed & 0xffffffff]
    def r():
        s[0] = (s[0] * 1664525 + 1013904223) & 0xffffffff
        return s[0] / 4294967296
    return r
def near_posts():
    r = lcg(7)
    x = -400
    while x < 5200:
        r(); r(); r(); x += 90 + r() * 140
    x = -400
    while x < 7000:
        w = 220 + r() * 120; h = 300 + r() * 220
        wy = 60
        while wy < h - 60:
            wx = 30
            while wx < w - 40:
                r(); wx += 60
            wy += 70
        r(); x += 260 + r() * 120
    posts = []
    x = -300
    while x < 12000:
        kind = 'post' if r() < 0.5 else 'fence'; w = 60 + r() * 40
        posts.append((x, kind, w)); x += 520 + r() * 380
    return posts
POSTS = near_posts()
def state(t):
    C = S["character"]; u = C["height_px"] / M["total"]
    cam = t * S["camera"]["pan_px_per_s"]
    hx = C["start_x"] + (C["end_x"] - C["start_x"]) * (t / S["duration_s"])
    ph = t * C["step_hz"] * math.pi * 2
    bob = abs(math.cos(ph)) * 0.06 * u
    hy = C["ground_y"] - (M["thigh"] + M["shin"] + M["foot_w"]) * u * 0.97 - bob
    sx = hx - cam
    hcy = hy - M["torso"] * u - M["neck"] * u - M["head"] * u / 2
    s, c = math.sin(ph), math.cos(ph)
    pose = dict(thighF=0.42 * s, shinF=-max(0, 0.7 * math.sin(ph + 1.2)), thighB=-0.42 * s,
                shinB=-max(0, -0.7 * math.sin(ph + 1.2)), armF=0.12 - 0.05 * s, armB=0.35 * s, foreB=0.35 + 0.1 * c)
    return sx, hcy, hy, cam, pose, u
def occluded(x, cam, pad=30):
    for px, kind, w in POSTS:
        X = px - cam * 1.4
        if kind == 'post' and X - pad <= x <= X + w + pad:
            return True
    return False
fake = len(sys.argv) > 2 and sys.argv[2] == "fake"
n = 240
head, hip, chans = [], [], {k: [] for k in ("thighF", "shinF", "thighB", "shinB", "armF", "armB", "foreB")}
root = []
for f in range(n):
    t = f / 24
    if fake:  # khai báo: khởi bước có easing trong 1 giây đầu (render thật đi đều từ khung 0)
        tt = 1.0
        t = (0.5 * tt * (f / 24 / tt) ** 2) if f / 24 < tt else f / 24 - 0.5 * tt
    sx, hcy, hy, cam, pose, u = state(t)
    for k in chans: chans[k].append(pose[k])
    root.append([sx + cam, hy])
    ok = 40 < sx < 1880 and not occluded(sx, cam)
    head.append([round(sx, 2), round(hcy, 2)] if ok else None)
    hip.append([round(sx, 2), round(hy - 0.5 * M["torso"] * u, 2)] if ok else None)
spec = {"fps": 24, "_nguon": "Phiên K dựng lại từ reports/m0/bench/scene2d.js + scene.json + model-sheet.json; "
        "không phải dữ liệu render xuất; chỉ minh hoạ" + (" — BẢN KHAI GIẢ (easing khởi bước)" if fake else ""),
        "channels": [{"id": f"lamplighter/{k}.rot", "class": "character_part", "first_frame": 0, "values": v}
                     for k, v in chans.items()] +
                    [{"id": "lamplighter/root.loc", "class": "character_root", "first_frame": 0, "values": root}],
        "screen_tracks": [{"id": "lamplighter/head", "first_frame": 0, "values": head},
                          {"id": "lamplighter/chest", "first_frame": 0, "values": hip}]}
json.dump(spec, open(sys.argv[1], "w"))
print("visible", sum(h is not None for h in head))
