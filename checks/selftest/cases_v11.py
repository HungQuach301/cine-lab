"""Test tự chứng minh cho thay đổi v1.1: C3 (hệ số mặt nạ 2–4×, đo từ kích thước PNG, chống phóng to),
P0/G4/P1 (nhãn "diegetic"), N3 (master YouTube có grain ≥ 30 Mbps). Mỗi thay đổi có mẫu TRƯỢT và mẫu SẠCH.
Được run_selftest.py gọi sau cases_v1."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from cinecheck.common import FAIL, PASS  # noqa: E402
from cinecheck.rule_c3 import check_c3  # noqa: E402
from cinecheck.rule_p0 import check_p0  # noqa: E402
from cinecheck.rules_file import check_n3  # noqa: E402
from cinecheck.rules_text import check_g4, check_p1  # noqa: E402

import cases_v1 as v1  # noqa: E402
import run_selftest as base  # noqa: E402

SIZE = (1280, 720)
BG = (18, 24, 40)
W_ = (235, 235, 230)


# ------------------------------------------------------------------ chữ diegetic
def dieg_sample(d, name, elements, bg=BG, n=24, script=None, matte_offset=None):
    """elements: list dict(id, text, xy, px, color, first, last, diegetic, matte=True, extra={}).
    Ghi video + <name>.text/ (+ <name>.script.txt nếu có). Phần tử matte=False có trong hình, không có matte."""
    tdir = d / f"{name}.text"
    tdir.mkdir(parents=True, exist_ok=True)
    spec, layers = [], []
    for e in elements:
        lay = base.text_layer(SIZE, e["text"], e["xy"], e["px"], e["color"])
        layers.append((lay, e["first"], e["last"]))
        if not e.get("matte", True):
            continue
        mxy = e["xy"] if matte_offset is None else (e["xy"][0] + matte_offset[0], e["xy"][1] + matte_offset[1])
        base.text_layer(SIZE, e["text"], mxy, e["px"], e["color"]).save(tdir / f"{e['id']}.png")
        item = dict(id=e["id"], first_frame=e["first"], last_frame=e["last"], matte=f"{e['id']}.png")
        if "diegetic" in e:
            item["diegetic"] = e["diegetic"]
        item.update(e.get("extra", {}))
        spec.append(item)
    (tdir / "elements.json").write_text(json.dumps({"elements": spec}, indent=1))
    frames = []
    for i in range(n):
        im = Image.new("RGBA", SIZE, bg + (255,))
        for lay, a, b in layers:
            if a <= i <= b:
                im = Image.alpha_composite(im, lay)
        frames.append(np.asarray(im.convert("RGB")))
    v = d / f"{name}.mp4"
    base.encode_rgb(frames, v)
    sp = None
    if script is not None:
        sp = d / f"{name}.script.txt"
        sp.write_text(script)
    return v, tdir, sp


TITLE = dict(id="title", text="THE LAST BELL", xy=(120, 60), px=72, color=W_, first=0, last=23)
SIGN = dict(id="sign", text="ROSE AND CROWN", xy=(700, 330), px=44, color=(215, 190, 140), first=0, last=23,
            diegetic=True)
SIGN_LOW = dict(id="sign", text="ROSE AND CROWN", xy=(120, 330), px=44, color=(120, 120, 120), first=0, last=23,
                diegetic=True)
SUB = dict(id="sub", text="Nobody answered the bell that night.", xy=(120, 600), px=40, color=W_, first=0, last=23)
SCRIPT = (base.FIX / "speech_en.script.txt").read_text()


# ------------------------------------------------------------------ N3 grain
def n3_grain(d, name, mbps, sigma=2.5, n=48):
    """Master 1080p24 có grain Gauss động σ (mã RGB) trên nền gradient + khối, AAC 48 kHz stereo."""
    h, w = 1080, 1920
    rng = np.random.default_rng(21)
    yy = np.linspace(0, 1, h)[:, None, None]
    bg = np.broadcast_to(np.array([40, 60, 110]) + yy * np.array([70, 60, 60]), (h, w, 3)).copy()
    bg[600:900, 300:900] = (160, 140, 120)
    frames = [np.clip(np.round(bg + sigma * rng.normal(0, 1, (h, w, 1))), 0, 255).astype(np.uint8)
              for _ in range(n)]
    t = np.arange(int(n / 24 * base.SR)) / base.SR
    a = d / f"{name}.wav"
    base.write_wav(a, 0.1 * np.stack([np.sin(2 * np.pi * 440 * t)] * 2, 1))
    v = d / f"{name}.mp4"
    vb = f"{mbps}M"
    base.encode_rgb(frames, v, audio=a,
                    vcodec=["-c:v", "libx264", "-profile:v", "high", "-preset", "veryfast", "-b:v", vb,
                            "-minrate", vb, "-maxrate", vb, "-bufsize", vb, "-x264-params", "nal-hrd=cbr",
                            "-tune", "grain"],
                    extra=["-c:a", "aac", "-b:a", "384k", "-ar", base.SR, "-ac", 2, "-shortest"])
    return v


# ------------------------------------------------------------------ bảng ca
def cases(d):
    C = []

    def add(code, name, expect, fn):
        C.append((code, name, expect, fn))

    # C3 — hệ số mặt nạ (Q-C3)
    def c3(name, H, **kw):
        v, pd = v1.c3_sample(d, name, H, **kw)
        return check_c3(v, "shot", pd, d)
    add("C3", "v1.1: đúng sheet đầu 146 px nhưng mặt nạ 1× (hệ số < 2)", FAIL, lambda: c3("c3v11_1x", 146))
    add("C3", "v1.1: cùng ca đầu 57 px thân +2% nhưng mặt nạ 4×: nay chứng minh được đạt", PASS,
        lambda: c3("c3v11_small4x", 57, scale_dev={"torso": 1.02}, s=4))
    add("C3", "v1.1: đúng sheet, đầu 100 px, mặt nạ 3×", PASS, lambda: c3("c3v11_3x", 100, s=3))
    add("C3", "v1.1: mặt nạ 1× phóng to lên 4× (láng giềng gần nhất), khai scale 4", FAIL,
        lambda: c3("c3v11_upscaled", 146, s=4, upscale=True))
    add("C3", "v1.1: mặt nạ thật 2× nhưng khai scale 4", FAIL, lambda: c3("c3v11_declared", 146, s=2, declare=4))
    add("C3", "v1.1: mặt nạ 2× không khai scale (máy tự đo)", PASS, lambda: _c3_nodecl(d))

    # P0 — nhãn diegetic và chống lạm dụng (Q-P0)
    def p0(name, els, script=None, **kw):
        v, t, sp = dieg_sample(d, name, els, script=script, **kw)
        return check_p0(v, "shot", t, sp)
    add("P0", "v1.1: tiêu đề + biển hiệu diegetic 'ROSE AND CROWN' đủ matte, có kịch bản", PASS,
        lambda: p0("p0v11_sign", [TITLE, SIGN], SCRIPT))
    add("P0", "v1.1: phụ đề (trùng câu thoại trong kịch bản) gắn diegetic", FAIL,
        lambda: p0("p0v11_subdieg", [TITLE, dict(SUB, diegetic=True)], SCRIPT))
    add("P0", "v1.1: chữ gắn diegetic trùng tiêu đề không diegetic (không có kịch bản)", FAIL,
        lambda: p0("p0v11_titledieg", [dict(TITLE, last=11), dict(TITLE, id="endcard", xy=(120, 400), first=12,
                                                                   diegetic=True)]))
    add("P0", "v1.1: biển hiệu diegetic không xuất matte", FAIL,
        lambda: p0("p0v11_signnomatte", [TITLE, dict(SIGN, matte=False)], SCRIPT))

    # G4 — miễn tương phản cho diegetic, vẫn kiểm độ khớp matte
    def g4(name, els, **kw):
        v, t, _ = dieg_sample(d, name, els, bg=(150, 150, 150), **kw)
        return check_g4(v, "shot", t)
    title_dark = dict(TITLE, color=(20, 20, 24))
    add("G4", "v1.1: biển hiệu xám trên nền xám (~1,4:1) gắn diegetic + tiêu đề đạt tương phản", PASS,
        lambda: g4("g4v11_dieg", [title_dark, SIGN_LOW]))
    add("G4", "v1.1: cùng biển hiệu nhưng không gắn diegetic", FAIL,
        lambda: g4("g4v11_nodieg", [title_dark, {k: v for k, v in SIGN_LOW.items() if k != "diegetic"}]))
    add("G4", "v1.1: nhãn diegetic sai kiểu (chuỗi \"true\") không được miễn", FAIL,
        lambda: g4("g4v11_str", [title_dark, dict(SIGN_LOW, diegetic="true")]))
    add("G4", "v1.1: chỉ có chữ diegetic nhưng matte khai lệch 60 px so với render", FAIL,
        lambda: g4("g4v11_fake", [SIGN_LOW], matte_offset=(0, 60)))

    # P1 — diegetic vẫn phải qua P1
    def p1(name, els):
        v, t, _ = dieg_sample(d, name, els)
        return check_p1(v, "shot", t)
    add("P1", "v1.1: biển hiệu diegetic tách rời phụ đề", PASS, lambda: p1("p1v11_ok", [SUB, SIGN]))
    add("P1", "v1.1: phụ đề đè lên biển hiệu diegetic", FAIL,
        lambda: p1("p1v11_hit", [SUB, dict(SIGN, xy=(160, 590))]))

    # N3 — master YouTube có grain phải ≥ 30 Mbps (Q-G3b)
    add("N3", "v1.1: YouTube 1080p có grain σ 2,5, H.264 14 Mbps (đạt ngưỡng cũ 12)", FAIL,
        lambda: check_n3(n3_grain(d, "n3v11_grain14", 14), "youtube"))
    add("N3", "v1.1: YouTube 1080p có grain σ 2,5, H.264 36 Mbps", PASS,
        lambda: check_n3(n3_grain(d, "n3v11_grain36", 36), "youtube"))
    return C


def _c3_nodecl(d):
    v, pd = v1.c3_sample(d, "c3v11_nodecl", 146, s=2)
    spec = json.loads((pd / "parts.json").read_text())
    spec.pop("scale")
    (pd / "parts.json").write_text(json.dumps(spec))
    return check_c3(v, "shot", pd, d)
