"""Test tự chứng minh cho luật mới của v1: P0, G3b, J1b, H1b, C3.
Mỗi luật có ít nhất một mẫu phải TRƯỢT và một mẫu phải SẠCH. Được run_selftest.py gọi."""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from cinecheck.common import FAIL, PASS, metric, result  # noqa: E402
from cinecheck.rule_c3 import DELTA_PX, check_c3, length_px, uncertainty  # noqa: E402
from cinecheck.rule_g3b import check_g3b  # noqa: E402
from cinecheck.rule_h1b import check_h1b  # noqa: E402
from cinecheck.rule_j1b import check_j1b  # noqa: E402
from cinecheck.rule_p0 import check_p0  # noqa: E402

import run_selftest as base  # noqa: E402

SR = base.SR
W_ = (235, 235, 230)


# ------------------------------------------------------------------ P0
def windows_bg(size=(1280, 720)):
    """Nền có lưới cửa sổ sáng (dễ bị máy dò nhầm là chữ) — mẫu sạch phải không bị báo."""
    im = Image.new("RGB", size, (28, 24, 40))
    d = ImageDraw.Draw(im)
    for bx in range(60, size[0] - 200, 260):
        d.rectangle([bx, 180, bx + 200, 560], fill=(46, 38, 58))
        for wy in range(210, 530, 50):
            for wx in range(bx + 20, bx + 180, 45):
                d.rectangle([wx, wy, wx + 24, wy + 32], fill=(232, 154, 74) if (wx * 7 + wy) % 3 else (26, 21, 32))
    return im


def p0_sample(d, name, export_ids, bg=None, n=24):
    """Tiêu đề + phụ đề trong hình; chỉ xuất matte cho export_ids (None = không có thư mục chữ)."""
    size = (1280, 720)
    els = [("title", "THE LAST BELL", (120, 40), 72, W_, 0, n - 1),
           ("sub", "Nobody answered the bell that night.", (120, 620), 40, W_, 0, n - 1)]
    bg_im = bg or Image.new("RGB", size, (18, 24, 40))
    frame = bg_im.convert("RGBA")
    spec = []
    tdir = d / f"{name}.text"
    if export_ids is not None:
        tdir.mkdir(parents=True, exist_ok=True)
    for eid, txt, xy, px, col, a, b in els:
        lay = base.text_layer(size, txt, xy, px, col)
        frame = Image.alpha_composite(frame, lay)
        if export_ids is not None and eid in export_ids:
            lay.save(tdir / f"{eid}.png")
            spec.append(dict(id=eid, first_frame=a, last_frame=b, matte=f"{eid}.png"))
    if export_ids is not None:
        (tdir / "elements.json").write_text(json.dumps({"elements": spec}))
    v = d / f"{name}.mp4"
    base.encode_rgb([np.asarray(frame.convert("RGB"))] * n, v)
    return v, (tdir if export_ids is not None else None)


# ------------------------------------------------------------------ G3b
def g3b_video(d, name, sig1, sig2, frozen=False, n=48):
    """Hai shot 24 khung khác màu (trời xanh tím / nội thất cam), grain Gauss đơn sắc σ (mã RGB)."""
    h, w = 540, 960
    rng = np.random.default_rng(3)
    yy = np.linspace(0, 1, h)[:, None, None]
    shot1 = np.broadcast_to(np.array([30, 40, 90]) + yy * np.array([60, 50, 70]), (h, w, 3)).copy()
    shot1[300:420, 100:400] = (150, 140, 170)
    shot2 = np.broadcast_to(np.array([200, 130, 60]) - yy * np.array([90, 60, 20]), (h, w, 3)).copy()
    shot2[:, 600:] -= 40
    shot2[80:200, 200:330] = (230, 190, 120)
    still = rng.normal(0, 1, (h, w, 1))
    fr = []
    for i in range(n):
        base_im, s = (shot1, sig1) if i < n // 2 else (shot2, sig2)
        g = still if frozen else rng.normal(0, 1, (h, w, 1))
        fr.append(np.clip(np.round(base_im + s * g), 0, 255).astype(np.uint8))
    p = d / f"{name}.mp4"
    base.encode_rgb(fr, p, vcodec=["-c:v", "libx264", "-preset", "veryfast", "-crf", "8", "-tune", "grain"])
    return p


# ------------------------------------------------------------------ J1b
def dialogue_stems(noise_burst=False):
    """Như base.dialogue_mix nhưng trả về từng stem (thoại, nền) stereo; mix = tổng."""
    s = base.speech()
    pad = int(0.5 * SR)
    s = np.concatenate([np.zeros(pad), s, np.zeros(pad)])
    bed = base.music_bed(len(s) / SR, seed=3)[: len(s)]
    rms = lambda v: np.sqrt(np.mean(v ** 2))
    bed *= rms(s[s != 0]) / rms(bed) * 10 ** (-22 / 20)
    if noise_burst:
        rng = np.random.default_rng(7)
        a, b = int(1.7 * SR), int(4.2 * SR)
        nz = rng.normal(size=(b - a, 2))
        bed[a:b] += nz / rms(nz) * rms(s[s != 0]) * 10 ** (9 / 20)
    return np.stack([s, s], 1), bed


def peak_limiter(x, ceiling_db, release_s=0.05):
    """Limiter đỉnh đơn giản (không nhìn trước): hệ số tức thời ≤ trần, nhả theo hàm mũ."""
    c = 10 ** (ceiling_db / 20)
    need = np.minimum(1.0, c / np.maximum(np.abs(x).max(1), 1e-12))
    g = np.empty_like(need)
    r = np.exp(-1 / (release_s * SR))
    cur = 1.0
    for i, v in enumerate(need):
        cur = v if v < cur else min(v, 1 - (1 - cur) * r)
        g[i] = cur
    return x * g[:, None]


def j1b_sample(d, name, burst=False, hot_dialogue_db=0.0, master=False, unstemmed_burst=False):
    dia, bed = dialogue_stems(burst)
    extra = np.zeros_like(bed)
    if unstemmed_burst:  # âm có trong mix nhưng không có trong stem nào
        extra = dialogue_stems(True)[1] - bed
    g = 10 ** (-16 / 20) / max(np.abs(dia + bed).max(), 1e-9) * 3
    dia, bed, extra = dia * g, bed * g, extra * g
    mix = dia + bed + extra
    if master:
        mix = peak_limiter(base.set_lufs(mix, -14.0), -1.5)
    else:
        mix = base.limit(mix)
    a = d / f"{name}.wav"
    base.write_wav(a, mix)
    v = d / f"{name}.mp4"
    base.ff("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=24", "-i", a, "-shortest", *base.X264, *base.TAGS,
            "-c:a", "aac", "-b:a", "320k", v)
    sd = d / f"{name}.stems"
    sd.mkdir(exist_ok=True)
    base.write_wav(sd / "dialogue.wav", dia * 10 ** (hot_dialogue_db / 20))
    base.write_wav(sd / "me.wav", bed)
    return v, sd


# ------------------------------------------------------------------ H1b
def ease(t):
    return t * t * (3 - 2 * t)


def h1b_path(n=40):
    """Quỹ đoạn có easing: đứng 6 khung, đi 24 khung, đứng 10 khung."""
    t = np.concatenate([np.zeros(6), ease(np.linspace(0, 1, 24)), np.ones(n - 30)])
    return np.stack([200 + 520 * t, 300 - 120 * np.sin(np.pi * t)], 1)


def h1b_video(d, name, path, size=(960, 540)):
    rng = np.random.default_rng(12)
    bg = cv2.GaussianBlur(rng.uniform(40, 200, (size[1], size[0], 3)).astype(np.float32), (0, 0), 2.0)
    yy, xx = np.mgrid[-28:29, -28:29]
    disc = (xx ** 2 + yy ** 2) <= 28 ** 2
    chk = (((xx + 28) // 7 + (yy + 28) // 7) % 2).astype(np.float32)
    tex = np.stack([230 * chk + 20, 60 + 0 * chk, 40 + 180 * (1 - chk)], -1)
    frames = []
    for x, y in path:
        f = bg.copy()
        xi, yi = int(round(x)), int(round(y))
        sub = f[yi - 28:yi + 29, xi - 28:xi + 29]
        sub[disc] = tex[disc]
        frames.append(np.clip(f, 0, 255).astype(np.uint8))
    v = d / f"{name}.mp4"
    base.encode_rgb(frames, v)
    return v


def h1b_motion(p, track, with_tracks=True):
    arm = np.concatenate([np.zeros(6), base.smooth(0, 90, 24), np.full(10, 90.0)])
    spec = {"fps": 24, "channels": [
        {"id": "hero/upperarm_R.rot_x", "class": "character_part", "first_frame": 0, "values": arm.tolist()}]}
    if with_tracks:
        spec["screen_tracks"] = [{"id": "hero/hand_R", "first_frame": 0,
                                  "values": [[round(float(x), 2), round(float(y), 2)] for x, y in track]}]
    Path(p).write_text(json.dumps(spec))
    return p


# ------------------------------------------------------------------ C3
SHEET = {"id": "SELFTEST", "unit": "H",
         "head": {"length": 1.0, "width": 0.86}, "torso": {"length": 1.9, "width": 1.1},
         "upper_arm": {"length": 0.95, "width": 0.28}, "forearm": {"length": 0.85, "width": 0.24},
         "thigh": {"length": 1.2, "width": 0.36}, "shin": {"length": 1.15, "width": 0.30},
         "measured_parts": ["head", "torso", "upper_arm", "forearm", "thigh", "shin"]}
COLORS = {"head": (224, 184, 148), "torso": (107, 63, 46), "upper_arm": (150, 90, 60), "forearm": (190, 120, 80),
          "thigh": (58, 50, 64), "shin": (90, 80, 110)}


def _capsule(img, p1, p2, w, val, ss):
    sh = 4
    f = 1 << sh
    P1 = tuple(int(c * ss * f) for c in p1)
    P2 = tuple(int(c * ss * f) for c in p2)
    cv2.line(img, P1, P2, val, thickness=max(1, int(round(w * ss))), lineType=cv2.LINE_8, shift=sh)
    cv2.circle(img, P1, int(w / 2 * ss * f), val, -1, shift=sh)
    cv2.circle(img, P2, int(w / 2 * ss * f), val, -1, shift=sh)


def figure(H, size=(1280, 1080), scale_dev=None, jitter=(0.0, 0.0), ss=8, cx=None, soft=False):
    """Nhân vật que theo SHEET, đầu cao H px. scale_dev: {bộ phận: hệ số độ dài}. Trả (khung RGB, mặt nạ)."""
    scale_dev = scale_dev or {}
    L = {k: SHEET[k]["length"] * H * scale_dev.get(k, 1.0) for k in COLORS}
    Wd = {k: SHEET[k]["width"] * H for k in COLORS}
    cx, top = (size[0] / 2 if cx is None else cx) + jitter[0], 40 + jitter[1]
    head_c = (cx, top + L["head"] / 2)
    neck = top + L["head"] + 0.1 * H
    hip = neck + L["torso"]
    geo = {"torso": ((cx, neck + Wd["torso"] / 2), (cx, hip - Wd["torso"] / 2), Wd["torso"])}
    sh = (cx + 0.3 * H, neck + 0.2 * H)
    a1 = np.radians(25)
    el = (sh[0] + np.sin(a1) * (L["upper_arm"] - Wd["upper_arm"]), sh[1] + np.cos(a1) * (L["upper_arm"] - Wd["upper_arm"]))
    geo["upper_arm"] = (sh, el, Wd["upper_arm"])
    a2 = np.radians(70)
    wr = (el[0] + np.sin(a2) * (L["forearm"] - Wd["forearm"]), el[1] + np.cos(a2) * (L["forearm"] - Wd["forearm"]))
    geo["forearm"] = (el, wr, Wd["forearm"])
    hp = (cx - 0.2 * H, hip)
    a3 = np.radians(-10)
    kn = (hp[0] + np.sin(a3) * (L["thigh"] - Wd["thigh"]), hp[1] + np.cos(a3) * (L["thigh"] - Wd["thigh"]))
    geo["thigh"] = (hp, kn, Wd["thigh"])
    an = (kn[0], kn[1] + (L["shin"] - Wd["shin"]))
    geo["shin"] = (kn, an, Wd["shin"])
    S = (size[1] * ss, size[0] * ss)
    masks = {}
    for k, (p1, p2, w) in geo.items():
        # đầu mút bo tròn nằm trong độ dài: tâm hai đầu cách nhau L − w
        img = np.zeros(S, np.uint8)
        _capsule(img, p1, p2, w, 255, ss)
        masks[k] = cv2.resize(img.astype(np.float32) / 255, size, interpolation=cv2.INTER_AREA)
    img = np.zeros(S, np.uint8)
    f = 16
    cv2.ellipse(img, (int(head_c[0] * ss * f), int(head_c[1] * ss * f)),
                (int(Wd["head"] / 2 * ss * f), int(L["head"] / 2 * ss * f)), 0, 0, 360, 255, -1, shift=4)
    masks["head"] = cv2.resize(img.astype(np.float32) / 255, size, interpolation=cv2.INTER_AREA)
    rng = np.random.default_rng(1)
    frame = cv2.GaussianBlur(rng.uniform(120, 150, (size[1], size[0], 3)).astype(np.float32), (0, 0), 3)
    for k in ("thigh", "shin", "torso", "upper_arm", "forearm", "head"):
        a = masks[k][..., None]
        frame = frame * (1 - a) + np.array(COLORS[k], np.float32) * a
    if soft:  # v1.2: mặt nạ khử răng cưa (độ phủ 0–1) thay vì ngưỡng hoá
        return np.clip(frame, 0, 255).astype(np.uint8), masks
    return np.clip(frame, 0, 255).astype(np.uint8), {k: (m >= 0.5) for k, m in masks.items()}


def gen_ss(head_mask_px):
    """Siêu lấy mẫu của bộ vẽ mẫu tổng hợp so với px mặt nạ: 8× (4× khi đầu > 300 px mặt nạ, để vừa bộ nhớ).
    Khảo sát v1.1: bộ vẽ thô hơn (2×) tự nó sai tới 1,5·U — đó là lỗi bộ sinh mẫu, không phải của mặt nạ."""
    return 8 if head_mask_px <= 300 else 4


def c3_sample(d, name, H, scale_dev=None, mask_shift=0, s=1, upscale=False, declare=None, size=None,
              aa_up=None, soft=False):
    """Khung 1× + mặt nạ ở hệ số s. s > 1: vẽ nhân vật ở s× rồi thu nhỏ ra khung (render mặt nạ độ phân
    giải cao thật). upscale=True: vẽ ở 1× rồi phóng to mặt nạ lên s× (láng giềng gần nhất) — khai man.
    declare: số 'scale' ghi vào parts.json (mặc định = s)."""
    if size is None:  # khung vừa nhân vật (chiều chẵn cho H.264)
        size = (max(640, (int(4.2 * H) + 80) // 2 * 2), (int(6.2 * H) + 80) // 2 * 2)
    if aa_up is not None:  # v1.2: matte 1× khử răng cưa phóng to lên s× bằng nhân aa_up = (tên, giữ xám?)
        fh, mh = figure(H * s, size=(size[0] * s, size[1] * s), scale_dev=scale_dev, ss=gen_ss(H * s), soft=True)
        frame = cv2.resize(fh, size, interpolation=cv2.INTER_AREA)
        kern = {"nearest": cv2.INTER_NEAREST, "linear": cv2.INTER_LINEAR, "cubic": cv2.INTER_CUBIC}[aa_up[0]]
        masks = {}
        for k, m in mh.items():
            up = cv2.resize(cv2.resize(m, size, interpolation=cv2.INTER_AREA), (size[0] * s, size[1] * s),
                            interpolation=kern)
            masks[k] = np.clip(up, 0, 1) if aa_up[1] else up >= 0.5
    elif s == 1 or upscale:
        frame, masks = figure(H, size=size, scale_dev=scale_dev)
        if upscale:
            masks = {k: np.kron(m, np.ones((s, s), bool)) for k, m in masks.items()}
    elif soft:  # render thật ở s×, mặt nạ khử răng cưa (xám) ở chính độ phân giải s×
        fh, masks = figure(H * s, size=(size[0] * s, size[1] * s), scale_dev=scale_dev, ss=gen_ss(H * s), soft=True)
        frame = cv2.resize(fh, size, interpolation=cv2.INTER_AREA)
    else:
        fh, masks = figure(H * s, size=(size[0] * s, size[1] * s), scale_dev=scale_dev, ss=gen_ss(H * s))
        frame = cv2.resize(fh, size, interpolation=cv2.INTER_AREA)
    v = d / f"{name}.mp4"
    base.encode_rgb([frame], v)
    pd = d / f"{name}.parts"
    (pd / "00000").mkdir(parents=True, exist_ok=True)
    (pd / "sheet.json").write_text(json.dumps(SHEET))
    fr = {}
    for k, m in masks.items():
        if mask_shift:
            m = np.roll(m, mask_shift * s, 1)
        Image.fromarray(np.round(np.asarray(m, np.float32) * 255).astype(np.uint8)).save(pd / "00000" / f"{k}.png")
        fr[k] = f"00000/{k}.png"
    (pd / "parts.json").write_text(json.dumps({"model_sheet": "sheet.json", "scale": s if declare is None else declare,
                                               "frames": {"0": fr}}))
    return v, pd


def c3_noise_model(n=60, heads=(40, 57, 100, 146), scales=(1, 2, 4)):
    """Hiệu chuẩn nhiễu đo: vẽ nhân vật đúng sheet ở vị trí lệch dưới điểm ảnh ngẫu nhiên, đo tỷ lệ,
    kiểm U(δ = 1 px mặt nạ) phủ mọi sai số thật. v1.1: lặp ở hệ số mặt nạ s = 1, 2, 4 (đầu H px video →
    H·s px mặt nạ; bộ vẽ siêu lấy mẫu gen_ss so với px mặt nạ). Trả kết quả kiểu luật cho bảng selftest."""
    rng = np.random.default_rng(0)
    worst, cover, tot, rows = 0.0, 0, 0, {}
    for s_, H0 in [(s_, H0) for s_ in scales for H0 in heads]:
        H = H0 * s_
        errs = []
        for _ in range(n // len(heads) if H <= 300 else 6):
            _, m = figure(H, size=(int(4.2 * H) + 80, int(6.2 * H) + 80),
                          jitter=tuple(rng.uniform(0, s_, 2)), ss=gen_ss(H))
            lh = length_px(m["head"])
            for p in ("torso", "upper_arm", "forearm", "thigh", "shin"):
                lp = length_px(m[p])
                e = abs((lp / lh) / (SHEET[p]["length"] / SHEET["head"]["length"]) - 1)
                u = uncertainty(lp, lh, DELTA_PX)
                cover += e <= u
                tot += 1
                errs.append(e)
                worst = max(worst, e / u)
        rows[f"s{s_}_H{H0}"] = dict(sai_so_max_pct=round(100 * max(errs), 2), sai_so_p95_pct=round(100 * float(np.percentile(errs, 95)), 2))
    pct = 100.0 * cover / tot
    return result("C3", None, [metric("tỷ lệ sai số thật nằm trong U(δ)", pct, ">=", 100.0, "%", near_check=False),
                               metric("sai số / U lớn nhất", worst, "<=", 1.0)],
                  notes=[json.dumps(rows, ensure_ascii=False)])


# ------------------------------------------------------------------ bảng ca
def cases(d):
    C = []

    def add(code, name, expect, fn):
        C.append((code, name, expect, fn))

    # P0
    def p0(name, ids, bg=None):
        v, t = p0_sample(d, name, ids, bg)
        return check_p0(v, "shot", t)
    add("P0", "tiêu đề + phụ đề, chỉ xuất matte tiêu đề (giới hạn 2 của v0)", FAIL, lambda: p0("p0_missing", {"title"}))
    add("P0", "chữ trong hình, không có thư mục chữ", FAIL, lambda: p0("p0_nodir", None))
    add("P0", "tiêu đề + phụ đề đủ matte, nền lưới cửa sổ sáng", PASS,
        lambda: p0("p0_good", {"title", "sub"}, windows_bg()))
    add("P0", "không có chữ, nền lưới cửa sổ sáng, không thư mục chữ", PASS,
        lambda: check_p0(base_video_from(d, "p0_nochar", windows_bg()), "shot", None))

    def p0_m0():
        im = Image.open(base.FIX / "m0_a2d_f204.png").convert("RGB")
        return check_p0(base_video_from(d, "p0_m0_f204", im, n=2), "shot", None)
    add("P0", "hồi quy: khung 204 của M0 a-2d-mb8, lưới cửa sổ bị đọc thành '88:18' (độ tin 0,86)", PASS, p0_m0)

    # G3b
    add("G3b", "2 shot, grain động σ 1,8 đều", PASS, lambda: check_g3b(g3b_video(d, "g3b_good", 1.8, 1.8), "shot"))
    add("G3b", "không grain", FAIL, lambda: check_g3b(g3b_video(d, "g3b_none", 0.0, 0.0), "shot"))
    add("G3b", "shot 2 grain σ 1,1 so với shot 1 σ 1,8", FAIL, lambda: check_g3b(g3b_video(d, "g3b_shot", 1.8, 1.1), "shot"))
    add("G3b", "grain đứng yên (cùng mẫu nhiễu mọi khung)", FAIL,
        lambda: check_g3b(g3b_video(d, "g3b_frozen", 1.8, 1.8, frozen=True), "shot"))

    # J1b
    def j1b(name, **kw):
        v, s = j1b_sample(d, name, **kw)
        return check_j1b(v, "shot", s)
    add("J1b", "lời + nhạc nền −22 dB; stem cộng đúng mix", PASS, lambda: j1b("j1b_clean"))
    add("J1b", "lời + nhạc nền, chuẩn −14 LUFS + limiter đỉnh −1,5 dBFS", PASS, lambda: j1b("j1b_master", master=True))
    add("J1b", "ồn lấn lời +9 dB 1,7–4,2 s (mẫu J1 vẫn đoán đúng 17/18 từ)", FAIL, lambda: j1b("j1b_masked", burst=True))
    add("J1b", "stem thoại xuất to hơn trong mix 6 dB (khai man)", FAIL, lambda: j1b("j1b_hot", hot_dialogue_db=6.0))
    add("J1b", "mix có tiếng ồn 2,5 s không nằm trong stem nào", FAIL, lambda: j1b("j1b_unstemmed", unstemmed_burst=True))

    # H1b
    true_path = h1b_path()
    lin_path = true_path.copy()
    lin_path[6:30, 0] = np.linspace(true_path[6, 0], true_path[29, 0], 24)
    def h1b(name, render_path, track, tracks=True):
        v = h1b_video(d, name, render_path)
        return check_h1b(v, "shot", h1b_motion(d / f"{name}.motion.json", track, tracks))
    add("H1b", "track khai báo = chuyển động render (easing, cung)", PASS, lambda: h1b("h1b_good", true_path, true_path))
    add("H1b", "khai báo easing nhưng render chạy tuyến tính", FAIL, lambda: h1b("h1b_fake", lin_path, true_path))
    add("H1b", "có kênh bộ phận nhân vật nhưng không có screen track", FAIL,
        lambda: h1b("h1b_notrack", true_path, true_path, tracks=False))

    # C3
    def c3(name, H, **kw):
        v, pd = c3_sample(d, name, H, **kw)
        return check_c3(v, "shot", pd, d)
    # v1.1 (Q-C3): các ca v1 dùng mặt nạ 1× được chuyển sang mặt nạ 2× (cùng ý nghĩa); ca đầu 57 px giữ 1×.
    add("C3", "đúng sheet, đầu 146 px (mặt nạ 2×)", PASS, lambda: c3("c3_good", 146, s=2))
    add("C3", "thân dài hơn sheet 6%, đầu 146 px (mặt nạ 2×)", FAIL,
        lambda: c3("c3_torso6", 146, scale_dev={"torso": 1.06}, s=2))
    add("C3", "thân dài hơn 2%, đầu 57 px: nhiễu đo vượt biên 3%, không chứng minh được (cả bộ phận đúng)", FAIL,
        lambda: c3("c3_small", 57, scale_dev={"torso": 1.02}))
    add("C3", "thân dài hơn 2%, đầu 146 px: chứng minh được đạt (mặt nạ 2×)", PASS,
        lambda: c3("c3_small146", 146, scale_dev={"torso": 1.02}, s=2))
    add("C3", "mặt nạ khai lệch 20 px so với render (mặt nạ 2×)", FAIL,
        lambda: c3("c3_shift", 146, mask_shift=20, s=2))
    add("C3", "hiệu chuẩn mô hình nhiễu U(δ mặt nạ; v1.2: δ = 2 px), đầu 40–146 px, s = 1, 2, 4", PASS,
        c3_noise_model)
    return C


def base_video_from(d, name, im, n=24):
    v = d / f"{name}.mp4"
    base.encode_rgb([np.asarray(im.convert("RGB"))] * n, v)
    return v
