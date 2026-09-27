"""Test tự chứng minh: với mỗi luật, tự tạo mẫu nhỏ phải TRƯỢT và mẫu phải SẠCH, chạy luật,
so kết quả với kỳ vọng. Cuối cùng chạy lệnh duy nhất run.py trên một mẫu tổng hợp sạch.

Dùng: /opt/cine/bin/python checks/selftest/run_selftest.py [--keep DIR] [--only N1,G3]
Kết quả: reports/checks-selftest/selftest.json + .md (tính từ gốc repo).
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pyloudnorm
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
CHECKS = HERE.parent
sys.path.insert(0, str(CHECKS))

from cinecheck.common import FAIL, PASS  # noqa: E402
from cinecheck.rule_g3 import check_g3  # noqa: E402
from cinecheck.rule_h1 import check_h1  # noqa: E402
from cinecheck.rule_j1 import check_j1  # noqa: E402
from cinecheck.rule_o3 import check_o3  # noqa: E402
from cinecheck.rules_audio import check_m1, check_m3  # noqa: E402
from cinecheck.rules_file import check_n1, check_n2, check_n3  # noqa: E402
from cinecheck.rules_text import check_g4, check_p1  # noqa: E402

FIX = HERE / "fixtures"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SR = 48000
TAGS = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
RGB2YUV = ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"]
X264 = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "8"]


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], check=True)


def write_wav(path, x):
    """float (n, ch) → WAV PCM 24 bit 48 kHz qua ffmpeg."""
    x = np.ascontiguousarray(np.atleast_2d(x.T).T.astype(np.float32))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(x.shape[1]),
                    "-i", "-", "-c:a", "pcm_s24le", str(path)], input=x.tobytes(), check=True)


def encode_rgb(frames, path, extra=(), audio=None, vcodec=X264):
    h, w, _ = frames[0].shape
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", "24", "-i", "-"]
    if audio is not None:
        cmd += ["-i", str(audio)]
    cmd += [*RGB2YUV, *vcodec, *TAGS, *map(str, extra), str(path)]
    subprocess.run(cmd, input=b"".join(np.ascontiguousarray(f).tobytes() for f in frames), check=True)


def encode_y(frames, path, extra=(), tags=TAGS, vcodec=X264):
    """Ghi luma trực tiếp vào yuv420p (không đổi dải) — dùng cho G3 và N2."""
    h, w = frames[0].shape
    chroma = np.full((h // 2) * (w // 2) * 2, 128, np.uint8).tobytes()
    raw = b"".join(np.clip(f, 0, 255).astype(np.uint8).tobytes() + chroma for f in frames)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", f"{w}x{h}",
           "-r", "24", "-i", "-", *vcodec, *tags, *map(str, extra), str(path)]
    subprocess.run(cmd, input=raw, check=True)


def lavfi_video(path, extra=(), size="640x360", rate=24, dur=2, tags=TAGS, vf=None):
    args = ["-f", "lavfi", "-i", f"testsrc2=size={size}:rate={rate}", "-t", dur]
    if vf:
        args += ["-vf", vf]
    ff(*args, *X264, *tags, *extra, path)


# ------------------------------------------------------------------ âm thanh mẫu
def music_bed(sec, seed=1, width=0.1):
    """Nhạc giả: hợp âm có bao biên độ + nhiễu hồng; stereo tương quan cao."""
    rng = np.random.default_rng(seed)
    t = np.arange(int(sec * SR)) / SR
    x = np.zeros_like(t)
    for f, a in ((110, 1), (220, .5), (277.2, .4), (329.6, .35), (440, .2)):
        x += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6))
    x *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t)
    pink = np.cumsum(rng.normal(size=t.size))
    pink = pink - np.convolve(pink, np.ones(200) / 200, "same")
    x = x / np.abs(x).max() + 0.3 * pink / np.abs(pink).max()
    d = rng.normal(size=t.size)
    d = np.convolve(d, np.ones(8) / 8, "same")
    L = x + width * d / np.abs(d).max()
    R = x - width * d / np.abs(d).max()
    return np.stack([L, R], 1)


def set_lufs(x, target):
    m = pyloudnorm.Meter(SR)
    return x * 10 ** ((target - m.integrated_loudness(x)) / 20)


def speech():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(FIX / "speech_en.flac"), "-ar", str(SR),
                          "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def dialogue_mix(noise_burst=False):
    """Lời + nhạc nền thấp 22 dB; tuỳ chọn một đoạn nhạc/ồn lấn át lời (mẫu trượt J1)."""
    s = speech()
    pad = int(0.5 * SR)
    s = np.concatenate([np.zeros(pad), s, np.zeros(pad)])
    bed = music_bed(len(s) / SR, seed=3)[: len(s)]
    rms = lambda v: np.sqrt(np.mean(v ** 2))
    bed *= rms(s[s != 0]) / rms(bed) * 10 ** (-22 / 20)
    mix = bed + s[:, None]
    if noise_burst:
        rng = np.random.default_rng(7)
        a, b = int(1.7 * SR), int(4.2 * SR)
        n = rng.normal(size=(b - a, 2))
        mix[a:b] += n / rms(n) * rms(s[s != 0]) * 10 ** (9 / 20)
    return mix


def limit(x, ceiling_db=-1.6):
    """Giới hạn đỉnh mẫu đơn giản (lấy mẫu vượt 4× để ước lượng true peak)."""
    from scipy.signal import resample_poly
    up = resample_poly(x, 4, 1, axis=0)
    peak = np.abs(up).max()
    c = 10 ** (ceiling_db / 20)
    return x * (c / peak) if peak > c else x


def master(x, lufs, ceiling_db=-2.5):
    """Chuẩn hoá độ ồn + giới hạn mềm (tanh) lặp vài lần để vừa đạt độ ồn vừa giữ đỉnh."""
    c = 10 ** (ceiling_db / 20)
    for _ in range(6):
        x = c * np.tanh(set_lufs(x, lufs) / c)
    return limit(x, ceiling_db + 0.4)


# ------------------------------------------------------------------ chữ mẫu
def text_layer(size, txt, xy, px, color):
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(im).text(xy, txt, font=ImageFont.truetype(FONT, px), fill=color + (255,))
    return im


def text_sample(d, name, bg, elements, n=24, matte_offset=None, size=(1280, 720)):
    """elements: list (id, text, xy, px, color, first, last). Ghi video + thư mục <name>.text/."""
    tdir = d / f"{name}.text"
    tdir.mkdir(parents=True, exist_ok=True)
    layers = {}
    spec = []
    for eid, txt, xy, px, color, a, b in elements:
        lay = text_layer(size, txt, xy, px, color)
        layers[eid] = (lay, a, b)
        mxy = xy if matte_offset is None else (xy[0] + matte_offset[0], xy[1] + matte_offset[1])
        text_layer(size, txt, mxy, px, color).save(tdir / f"{eid}.png")
        spec.append(dict(id=eid, first_frame=a, last_frame=b, matte=f"{eid}.png"))
    (tdir / "elements.json").write_text(json.dumps({"elements": spec}, indent=1))
    frames = []
    for i in range(n):
        im = Image.new("RGBA", size, bg + (255,))
        for eid, (lay, a, b) in layers.items():
            if a <= i <= b:
                im = Image.alpha_composite(im, lay)
        frames.append(np.asarray(im.convert("RGB")))
    v = d / f"{name}.mp4"
    encode_rgb(frames, v)
    return v, tdir


# ------------------------------------------------------------------ chuyển động mẫu
def smooth(a, b, n):
    t = np.linspace(0, 1, n)
    return a + (b - a) * (t * t * (3 - 2 * t))


def lin(a, b, n):
    return np.linspace(a, b, n)


def motion_json(path, linear_part=False):
    arm = np.concatenate([np.zeros(6), (lin if linear_part else smooth)(0, 90, 20), np.full(10, 90.0),
                          smooth(90, -8, 12), smooth(-8, 0, 6), np.zeros(8)])
    t = np.linspace(0, 1, 40)
    e = t * t * (3 - 2 * t)
    hand = np.stack([0.3 * e, 0.2 * np.sin(np.pi * e), 0.05 * e], 1)  # cung, có easing
    head = np.concatenate([np.zeros(4), smooth(0, 35, 96), np.zeros(4)])  # quay chậm 4 giây
    root = np.stack([lin(0, 3, 60), np.zeros(60), np.zeros(60)], 1)
    clock = lin(0, 360, 48)
    spec = {"fps": 24, "channels": [
        {"id": "hero/upperarm_R.rot_x", "class": "character_part", "first_frame": 0, "values": arm.tolist()},
        {"id": "hero/hand_R.loc", "class": "character_part", "first_frame": 0, "values": hand.tolist()},
        {"id": "hero/head.rot_z", "class": "character_part", "first_frame": 0, "values": head.tolist()},
        {"id": "hero/root.loc", "class": "character_root", "first_frame": 0, "values": root.tolist()},
        {"id": "clock/second_hand.rot", "class": "mechanical", "reason": "kim giây quay đều có chủ ý",
         "first_frame": 0, "values": clock.tolist()},
    ]}
    Path(path).write_text(json.dumps(spec))
    return path


# ------------------------------------------------------------------ tài sản mẫu
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def asset_repo(d, dirty=False, tag=""):
    repo = d / (("repo_bad" if dirty else "repo_good") + tag)
    (repo / "assets/characters").mkdir(parents=True)
    (repo / "assets/sets").mkdir(parents=True)
    (repo / "shots/sh010/render").mkdir(parents=True)
    hero = repo / "assets/characters/hero_v1.blend"
    room = repo / "assets/sets/room_v1.png"
    hero.write_bytes(b"BLENDER-v0 hero model sheet v1" * 50)
    Image.new("RGB", (64, 36), (40, 60, 90)).save(room)
    lib = {"assets": [
        {"id": "CHR-hero-v1", "path": "assets/characters/hero_v1.blend", "sha256": sha(hero), "rights": "R-000"},
        {"id": "SET-room-v1", "path": "assets/sets/room_v1.png", "sha256": sha(room), "rights": "R-000"}]}
    (repo / "assets/LIBRARY.json").write_text(json.dumps(lib, indent=1))
    (repo / "shots/sh010/sh010.blend").write_bytes(b"BLENDER-v0 scene linking library")
    Image.new("RGB", (64, 36)).save(repo / "shots/sh010/render/0001.png")
    used = ["assets/characters/hero_v1.blend", "assets/sets/room_v1.png"]
    if dirty:
        with open(hero, "ab") as f:  # sửa tài sản sau khi khoá
            f.write(b"tweaked proportions")
        Image.new("RGB", (64, 36), (200, 10, 10)).save(repo / "shots/sh010/hero_redraw.png")
        used.append("assets/characters/villain_v1.blend")
    man = {"workdir": "shots/sh010", "scene_files": ["shots/sh010/sh010.blend"], "assets": used}
    mp = d / (("bad" if dirty else "good") + tag + ".assets.json")
    mp.write_text(json.dumps(man, indent=1))
    return repo, mp


# ------------------------------------------------------------------ các ca kiểm
def cases(d):
    """Trả về list (mã, tên mẫu, kỳ vọng, hàm tạo-và-đo)."""
    C = []

    def add(code, name, expect, fn):
        C.append((code, name, expect, fn))

    # N1
    def n1_good():
        p = d / "n1_good.mp4"; lavfi_video(p); return check_n1(p, "shot")
    def n1_drop():
        p = d / "n1_drop.mp4"
        lavfi_video(p, vf="select='not(eq(n\\,10))'", extra=["-fps_mode", "passthrough"])
        return check_n1(p, "shot")
    def n1_25():
        p = d / "n1_25fps.mp4"; lavfi_video(p, rate=25); return check_n1(p, "shot")
    add("N1", "24 fps CFR (testsrc2)", PASS, n1_good)
    add("N1", "rơi khung 10 (PTS hở)", FAIL, n1_drop)
    add("N1", "25 fps", FAIL, n1_25)

    # N2
    def n2_good():
        p = d / "n2_good.mp4"; lavfi_video(p); return check_n2(p, "shot")
    def n2_untagged():
        p = d / "n2_untagged.mp4"; lavfi_video(p, tags=[]); return check_n2(p, "shot")
    def n2_fullrange_content():
        f = np.zeros((360, 640), np.uint8); f[:, 320:] = 255  # nhãn tv nhưng giá trị full range
        p = d / "n2_fullrange.mp4"; encode_y([f] * 24, p); return check_n2(p, "shot")
    add("N2", "BT.709 đủ nhãn, dải limited", PASS, n2_good)
    add("N2", "không có nhãn màu", FAIL, n2_untagged)
    add("N2", "nhãn tv nhưng luma 0/255 (full range)", FAIL, n2_fullrange_content)

    # N3
    def yt(p, vb, ab, ar):
        ff("-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=24", "-f", "lavfi",
           "-i", f"sine=frequency=440:sample_rate={ar}", "-t", 2, "-c:v", "libx264", "-profile:v", "high",
           "-preset", "veryfast", "-b:v", vb, "-minrate", vb, "-maxrate", vb, "-bufsize", vb,
           "-x264-params", "nal-hrd=cbr", *TAGS, "-c:a", "aac", "-b:a", ab, "-ac", 2, p)
    def n3_yt_good():
        p = d / "n3_yt_good.mp4"; yt(p, "14M", "384k", 48000); return check_n3(p, "youtube")
    def n3_yt_bad():
        p = d / "n3_yt_bad.mp4"; yt(p, "3M", "128k", 44100); return check_n3(p, "youtube")
    def n3_arch_good():
        p = d / "n3_arch_good.mov"
        ff("-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=24", "-f", "lavfi", "-i", "sine=sample_rate=48000",
           "-t", 1, "-c:v", "prores_ks", "-profile:v", 3, "-pix_fmt", "yuv422p10le", *TAGS,
           "-c:a", "pcm_s24le", "-ac", 2, p)
        return check_n3(p, "archive")
    def n3_arch_bad():
        p = d / "n3_arch_bad.mov"
        ff("-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=24", "-f", "lavfi", "-i", "sine=sample_rate=48000",
           "-t", 1, *X264, *TAGS, "-c:a", "aac", "-ac", 2, p)
        return check_n3(p, "archive")
    add("N3", "YouTube: H.264 High 14 Mbps, AAC 384k 48 kHz", PASS, n3_yt_good)
    add("N3", "YouTube: 3 Mbps, AAC 128k 44,1 kHz", FAIL, n3_yt_bad)
    add("N3", "Lưu trữ: ProRes 422 HQ + PCM 24 bit", PASS, n3_arch_good)
    add("N3", "Lưu trữ: H.264 + AAC", FAIL, n3_arch_bad)

    # P1 / G4
    W = (235, 235, 230)
    title = ("title", "THE LAST BELL", (120, 110), 72, W, 0, 23)
    sub_ok = ("sub", "Nobody answered the bell that night.", (120, 600), 40, W, 6, 23)
    sub_hit = ("sub", "Nobody answered the bell that night.", (140, 150), 40, W, 6, 23)
    def p1_good():
        v, t = text_sample(d, "p1_good", (18, 24, 40), [title, sub_ok]); return check_p1(v, "shot", t)
    def p1_overlap():
        v, t = text_sample(d, "p1_overlap", (18, 24, 40), [title, sub_hit]); return check_p1(v, "shot", t)
    def p1_fake_matte():
        v, t = text_sample(d, "p1_fake", (18, 24, 40), [title, sub_ok], matte_offset=(0, 60))
        return check_p1(v, "shot", t)
    add("P1", "tiêu đề + phụ đề tách rời", PASS, p1_good)
    add("P1", "phụ đề đè lên tiêu đề", FAIL, p1_overlap)
    add("P1", "matte khai lệch vị trí so với render", FAIL, p1_fake_matte)
    def g4_good():
        v, t = text_sample(d, "g4_good", (18, 24, 40), [title, sub_ok]); return check_g4(v, "shot", t)
    def g4_low():
        grey = ("sub", "Nobody answered the bell that night.", (120, 600), 40, (120, 120, 120), 0, 23)
        v, t = text_sample(d, "g4_low", (150, 150, 150), [grey]); return check_g4(v, "shot", t)
    add("G4", "chữ sáng trên nền tối (~14:1)", PASS, g4_good)
    add("G4", "chữ xám trên nền xám (~1,4:1)", FAIL, g4_low)

    # G3
    h, w = 1080, 1920
    ramp = np.tile(np.linspace(30, 62, w), (h, 1))
    def g3_banded():
        p = d / "g3_banded.mp4"; encode_y([np.round(ramp)] * 24, p); return check_g3(p, "shot")
    def g3_dithered():
        rng = np.random.default_rng(5)
        fr = [np.round(ramp + rng.normal(0, 1.2, ramp.shape)) for _ in range(24)]
        p = d / "g3_dither.mp4"; encode_y(fr, p, extra=["-tune", "grain"]); return check_g3(p, "shot")
    def g3_flat_style():
        f = np.full((h, w), 40.0)
        yy, xx = np.mgrid[:h, :w]
        f[(yy - 540) ** 2 + (xx - 700) ** 2 < 260 ** 2] = 180
        f[200:420, 1200:1700] = 90
        f[700:760, :] = 43  # hai mảng phẳng chênh 3 mã, biên cứng
        p = d / "g3_flat.mp4"; encode_y([f] * 24, p); return check_g3(p, "shot")
    add("G3", "gradient 8 bit không dither (bậc thang)", FAIL, g3_banded)
    add("G3", "cùng gradient có dither/grain", PASS, g3_dithered)
    add("G3", "mảng phẳng phong cách hoá, biên cứng", PASS, g3_flat_style)

    # M1
    def m1_file(name, lufs, clip=False):
        x = set_lufs(music_bed(10, seed=2), lufs)
        x = np.clip(x, -1, 1) if clip else limit(x)
        a = d / f"{name}.wav"; write_wav(a, x)
        p = d / f"{name}.mp4"
        ff("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=24", "-i", a, "-t", 10, *X264, *TAGS,
           "-c:a", "aac", "-b:a", "384k", "-ar", SR, p)
        return p
    add("M1", "−14 LUFS, đỉnh giới hạn −1,6 dBFS", PASS, lambda: check_m1(m1_file("m1_good", -14), "youtube"))
    add("M1", "−8 LUFS, cắt đỉnh tại 0 dBFS", FAIL, lambda: check_m1(m1_file("m1_hot", -8, clip=True), "youtube"))

    # M3
    def m3_file(name, invert):
        x = set_lufs(music_bed(10, seed=4), -16)
        if invert:
            x[:, 1] = -x[:, 1]
        a = d / f"{name}.wav"; write_wav(a, limit(x))
        p = d / f"{name}.mkv"
        ff("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=24", "-i", a, "-t", 10, *X264, *TAGS,
           "-c:a", "pcm_s24le", p)
        return p
    add("M3", "stereo tương quan cao", PASS, lambda: check_m3(m3_file("m3_good", False), "shot"))
    add("M3", "kênh phải đảo pha", FAIL, lambda: check_m3(m3_file("m3_inverted", True), "shot"))

    # J1
    def j1_file(name, burst):
        a = d / f"{name}.wav"; write_wav(a, limit(set_lufs(dialogue_mix(burst), -16)))
        p = d / f"{name}.mp4"
        ff("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=24", "-i", a, "-shortest", *X264, *TAGS,
           "-c:a", "aac", "-b:a", "320k", p)
        return p
    script = FIX / "speech_en.script.txt"
    add("J1", "lời + nhạc nền thấp 22 dB", PASS, lambda: check_j1(j1_file("j1_clean", False), "shot", script))
    add("J1", "nhạc/ồn lấn át lời 1,7–4,2 s", FAIL, lambda: check_j1(j1_file("j1_masked", True), "shot", script))

    # H1
    add("H1", "easing, cung, quay chậm 4 s; kim đồng hồ 'mechanical'", PASS,
        lambda: check_h1(None, "shot", motion_json(d / "h1_good.motion.json")))
    add("H1", "cánh tay nội suy tuyến tính 20 khung", FAIL,
        lambda: check_h1(None, "shot", motion_json(d / "h1_linear.motion.json", linear_part=True)))

    # O3
    def o3(dirty):
        repo, man = asset_repo(d, dirty)
        return check_o3(None, "shot", man, repo / "assets/LIBRARY.json", repo)
    add("O3", "tài sản khớp SHA thư viện", PASS, lambda: o3(False))
    add("O3", "tài sản bị sửa sau khoá + vẽ lại ngoài thư viện", FAIL, lambda: o3(True))
    import cases_v1  # luật mới v1: P0, G3b, J1b, H1b, C3
    C += cases_v1.cases(d)
    import cases_v11  # thay đổi v1.1: C3 hệ số mặt nạ, diegetic (P0/G4/P1), N3 bitrate khi có grain
    C += cases_v11.cases(d)
    import cases_v12  # thay đổi v1.2: J1 (3 khiếu nại), C3b
    C += cases_v12.cases(d)
    return C


def e2e(d):
    """Mẫu tổng hợp sạch 1080p24 8 giây, master YouTube, chạy qua lệnh duy nhất run.py.
    v1.1: mặt nạ C3 ở 2×; master có grain nên N3 đòi ≥ 30 Mbps (mẫu mã 40 Mbps)."""
    import cases_v1 as v1
    name = "e2e_clean"
    size = (1920, 1080)
    dia, bed = v1.dialogue_stems(False)
    g = 10 ** ((-14.0 - pyloudnorm.Meter(SR).integrated_loudness(dia + bed)) / 20)
    dia, bed = dia * g, bed * g
    mix = v1.peak_limiter(dia + bed, -3.0)
    n = int(np.ceil(len(mix) / SR * 24))
    a = d / f"{name}.wav"; write_wav(a, mix)
    sd = d / f"{name}.stems"; sd.mkdir()
    write_wav(sd / "dialogue.wav", dia); write_wav(sd / "me.wav", bed)
    ms = 2  # v1.1 (Q-C3): mặt nạ bộ phận render ở 2× khung
    fig_hi, fmasks = v1.figure(150 * ms, size=(size[0] * ms, size[1] * ms), cx=1500 * ms, ss=4)
    fig = v1.cv2.resize(fig_hi, size, interpolation=v1.cv2.INTER_AREA)
    fa = v1.cv2.resize(np.stack([fmasks[k] for k in fmasks]).any(0).astype(np.float32), size,
                       interpolation=v1.cv2.INTER_AREA) >= 0.5
    pd = d / f"{name}.parts"; (pd / "m").mkdir(parents=True)
    json.dump(v1.SHEET, open(pd / "sheet.json", "w"))
    for k, m in fmasks.items():
        Image.fromarray((m * 255).astype(np.uint8)).save(pd / "m" / f"{k}.png")
    json.dump({"model_sheet": "sheet.json", "scale": ms,
               "frames": {str(i): {k: f"m/{k}.png" for k in fmasks} for i in range(0, n, 12)}},
              open(pd / "parts.json", "w"))
    path = v1.h1b_path(n) * np.array([1.2, 1.0]) + np.array([-40, 380])
    yy_, xx_ = np.mgrid[-28:29, -28:29]
    disc = (xx_ ** 2 + yy_ ** 2) <= 28 ** 2
    chk = (((xx_ + 28) // 7 + (yy_ + 28) // 7) % 2).astype(np.float32)
    tex = np.stack([230 * chk + 20, 60 + 0 * chk, 40 + 180 * (1 - chk)], -1)
    rng = np.random.default_rng(11)
    yy = np.linspace(0, 1, size[1])[:, None, None]
    base = (np.array([14, 20, 38]) + yy * np.array([20, 18, 30]))
    title = text_layer(size, "THE LAST BELL", (160, 140), 96, (235, 235, 230))
    sub = text_layer(size, "Nobody answered the bell that night.", (160, 900), 52, (235, 235, 230))
    tdir = d / f"{name}.text"; tdir.mkdir()
    title.save(tdir / "title.png"); sub.save(tdir / "sub.png")
    (tdir / "elements.json").write_text(json.dumps({"elements": [
        dict(id="title", first_frame=0, last_frame=47, matte="title.png"),
        dict(id="sub", first_frame=48, last_frame=n - 1, matte="sub.png")]}))
    frames = []
    for i in range(n):
        f = np.broadcast_to(base, (size[1], size[0], 3)).copy()
        f[fa] = fig[fa]
        xi, yi = (int(round(c)) for c in path[i])
        f[yi - 28:yi + 29, xi - 28:xi + 29][disc] = tex[disc]
        f = f + rng.normal(0, 2.0, (size[1], size[0], 1))
        im = Image.fromarray(np.clip(np.round(f), 0, 255).astype(np.uint8)).convert("RGBA")
        im = Image.alpha_composite(im, title if i < 48 else sub)
        frames.append(np.asarray(im.convert("RGB")))
    v = d / f"{name}.mp4"
    vb = "40M"  # grain σ 2 cần bitrate cao; ở 14 Mbps x264 làm grain dao động theo khung I/P/B (G3b bắt)
    encode_rgb(frames, v, audio=a, vcodec=["-c:v", "libx264", "-profile:v", "high", "-preset", "veryfast",
                                           "-b:v", vb, "-minrate", vb, "-maxrate", vb, "-bufsize", vb,
                                           "-x264-params", "nal-hrd=cbr", "-tune", "grain"],
               extra=["-c:a", "aac", "-b:a", "384k", "-ar", SR, "-shortest"])
    shutil.copy(FIX / "speech_en.script.txt", d / f"{name}.script.txt")
    motion_json(d / f"{name}.motion.json")
    mj = json.loads((d / f"{name}.motion.json").read_text())
    mj["screen_tracks"] = [{"id": "hero/hand_R", "first_frame": 0,
                            "values": [[round(float(x), 2), round(float(y), 2)] for x, y in np.round(path)]}]
    (d / f"{name}.motion.json").write_text(json.dumps(mj))
    repo, man = asset_repo(d, False, "_e2e")
    shutil.copy(man, d / f"{name}.assets.json")
    out = d / "e2e_report"
    p = subprocess.run([sys.executable, str(CHECKS / "run.py"), str(v), "--profile", "youtube",
                        "--repo", str(repo), "--out", str(out)], capture_output=True, text=True)
    rep = json.loads((out / f"{name}.checks.json").read_text())
    # mẫu bẩn qua cùng lệnh: file rơi khung, nhãn thiếu → phải TRƯỢT (exit 1)
    bad = d / "e2e_dirty.mp4"
    lavfi_video(bad, tags=[], vf="select='not(eq(n\\,10))'", extra=["-fps_mode", "passthrough"])
    q = subprocess.run([sys.executable, str(CHECKS / "run.py"), str(bad), "--only", "N1,N2",
                        "--out", str(d / "e2e_dirty_report")], capture_output=True, text=True)
    return p.returncode, rep, q.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", help="giữ mẫu tại thư mục này")
    ap.add_argument("--only")
    ap.add_argument("--no-e2e", action="store_true")
    a = ap.parse_args()
    d = Path(a.keep) if a.keep else Path(tempfile.mkdtemp(prefix="cine-selftest-"))
    d.mkdir(parents=True, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    rows = []
    for code, name, expect, fn in cases(d):
        if only and code not in only:
            continue
        t = time.time()
        try:
            r = fn()
            got, metrics = r["status"], [(m["name"], m["value"], m["op"], m["threshold"], m["ok"]) for m in r["metrics"]]
            notes = r["notes"]
        except Exception as e:
            got, metrics, notes = "ERROR", [], [f"{type(e).__name__}: {e}"]
        ok = got == expect
        rows.append(dict(code=code, sample=name, expect=expect, got=got, ok=ok,
                         seconds=round(time.time() - t, 1), metrics=metrics, notes=notes))
        print(f"{'OK ' if ok else 'SAI'} {code:3} kỳ vọng {expect:4} → {got:5} | {name}", flush=True)
    e2e_res = None
    if not a.no_e2e and not only:
        code, rep, dirty_code = e2e(d)
        st = {r["code"]: r["status"] for r in rep["results"]}
        lock_ok = rep["lock"]["match"]
        e2e_ok = all(v == PASS for v in st.values()) and (
            (code == 0 and dirty_code == 1) if lock_ok else (code == 3 and dirty_code == 3))
        e2e_res = dict(exit_code=code, dirty_exit_code=dirty_code, verdict=rep["verdict"], statuses=st,
                       lock_match=lock_ok, near_threshold=rep["near_threshold"], ok=e2e_ok)
        print(f"E2E run.py: sạch verdict={rep['verdict']} exit={code}; bẩn exit={dirty_code}; "
              f"{'OK' if e2e_ok else 'SAI'} {st}", flush=True)
    per_rule = {}
    for r in rows:
        per_rule.setdefault(r["code"], []).append(r["ok"])
    summary = {k: all(v) and any(r["expect"] == FAIL for r in rows if r["code"] == k)
               and any(r["expect"] == PASS for r in rows if r["code"] == k) for k, v in per_rule.items()}
    repo_root = CHECKS.parent
    out = repo_root / "reports" / "checks-selftest"
    out.mkdir(parents=True, exist_ok=True)
    res = dict(cases=rows, rule_proven=summary, e2e=e2e_res, sample_dir=str(d))
    (out / "selftest.json").write_text(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    L = ["# Test tự chứng minh — luật L1 (phiên K)", "",
         "| Mã | Mẫu | Kỳ vọng | Kết quả | Khớp | Số đo |", "|---|---|---|---|---|---|"]
    for r in rows:
        ms = "; ".join(f"{n}={v} ({op} {th})" for n, v, op, th, _ in r["metrics"]) or "; ".join(r["notes"])
        L.append(f"| {r['code']} | {r['sample']} | {r['expect']} | {r['got']} | {'✔' if r['ok'] else '✘'} | {ms} |")
    L += ["", "## Luật được chứng minh (có mẫu TRƯỢT và mẫu SẠCH, mọi ca khớp)", ""]
    L += [f"- {k}: {'ĐẠT' if v else 'CHƯA ĐẠT'}" for k, v in summary.items()]
    if e2e_res:
        L += ["", "## Chạy đầu–cuối bằng lệnh duy nhất (run.py, profile youtube)", "",
              f"- Mẫu sạch: {e2e_res['verdict']} (exit {e2e_res['exit_code']}); LOCK khớp: {e2e_res['lock_match']}",
              f"- Mẫu bẩn (rơi khung, thiếu nhãn màu; --only N1,N2): exit {e2e_res['dirty_exit_code']} "
              "(kỳ vọng 1 khi LOCK khớp, 3 khi chưa khoá)",
              f"- Khớp kỳ vọng: {'✔' if e2e_res['ok'] else '✘'}",
              f"- Trạng thái: {e2e_res['statuses']}",
              f"- Sát ngưỡng ±5%: {e2e_res['near_threshold'] or 'không'}"]
    (out / "selftest.md").write_text("\n".join(L) + "\n")
    all_ok = all(r["ok"] for r in rows) and all(summary.values()) and (e2e_res is None or e2e_res["ok"])
    print("TẤT CẢ KHỚP" if all_ok else "CÓ CA SAI", f"— báo cáo: {out}/selftest.md")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
