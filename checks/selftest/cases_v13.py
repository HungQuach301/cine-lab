"""Test tự chứng minh cho thay đổi v1.3: J1 theo stem thoại (Q-J1c), C3 bắt buộc 4× khi đầu < 100 px (Q-δ),
kiểm toán ngẫu nhiên mặt nạ C3 (Q-C3c). Mỗi thay đổi có mẫu TRƯỢT và mẫu SẠCH."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from cinecheck import audit as au  # noqa: E402
from cinecheck.common import FAIL, MISSING, PASS, metric, result  # noqa: E402
from cinecheck.rule_c3 import check_c3  # noqa: E402
from cinecheck.rule_j1 import SR, _word_list, check_j1, silence_mask  # noqa: E402

import cases_v1 as v1  # noqa: E402
import cases_v12 as v12  # noqa: E402
import run_selftest as base  # noqa: E402

ROOM_DB = -55.0  # room tone: trên ngưỡng im lặng số −60 dBFS (quy tắc v1.2 không bỏ được chữ bịa ở đây)


def _tr_stereo():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(v12.TR), "-ac", "2", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def room_tone(n, db=ROOM_DB, seed=5):
    """Nhiễu hồng stereo, RMS mỗi kênh = db dBFS."""
    rng = np.random.default_rng(seed)
    w = rng.normal(size=(n, 2))
    f = np.fft.rfftfreq(n, 1 / 48000)
    spec = np.fft.rfft(w, axis=0) / np.sqrt(np.maximum(f, 20))[:, None]
    x = np.fft.irfft(spec, n, axis=0)
    return x / np.sqrt(np.mean(x ** 2)) * 10 ** (db / 20)


def j1_stem_sample(d, name):
    """Mix = thoại table read + room tone −55 dBFS; stems: dialogue.wav (thoại, im giữa các câu), me.wav (room tone)."""
    dia = _tr_stereo()
    rt = room_tone(len(dia))
    mix = d / f"{name}.wav"
    base.write_wav(mix, dia + rt)
    sd = d / f"{name}.stems"
    sd.mkdir(exist_ok=True)
    base.write_wav(sd / "dialogue.wav", dia)
    base.write_wav(sd / "me.wav", rt)
    return mix, sd


def j1_room_unit():
    """Cùng một chữ bịa trong room tone −55 dBFS: quy tắc −60 dBFS (không stem) giữ lại → tính chèn;
    quy tắc stem thoại (v1.3) bỏ đi. Chữ thật lúc stem thoại có lời được giữ ở cả hai."""
    t = np.arange(int(2 * SR)) / SR
    speech = 0.1 * np.sin(2 * np.pi * 220 * t)
    gap = np.random.default_rng(1).normal(0, 10 ** (ROOM_DB / 20), int(3 * SR))
    mix = np.concatenate([speech + gap[:len(speech)] * 0, gap, speech]).astype(np.float32)
    dia = np.concatenate([speech, np.zeros(len(gap)), speech])
    hop = SR // 100
    e = 10 * np.log10(np.mean(dia[:len(dia) // hop * hop].reshape(-1, hop) ** 2, 1) + 1e-20)
    act = e > max(e.max() - 35, -60)
    words = [(0.5, 0.9, "evening"), (3.0, 3.6, "you"), (5.4, 5.9, "street")]
    kept_old, drop_old = _word_list(words, silence_mask(mix))
    kept_new, drop_new = _word_list(words, silence_mask(mix), act)
    return result("J1", None, [
        metric("không stem (−60 dBFS): chữ bịa trong room tone vẫn bị giữ", len(kept_old), "==", 3),
        metric("có stem thoại (v1.3): chữ bịa khi stem im bị bỏ", len(drop_new), "==", 1),
        metric("có stem thoại (v1.3): chữ lúc stem có lời được giữ", len(kept_new), "==", 2)],
        notes=[f"bỏ={drop_new}"])


# ------------------------------------------------------------------ C3: kiểm toán
def _write_masks(dirp, masks):
    dirp.mkdir(parents=True, exist_ok=True)
    for k, m in masks.items():
        Image.fromarray(np.round(np.asarray(m, np.float32) * 255).astype(np.uint8)).save(dirp / f"{k}.png")


def audit_sample(d, name, H=100, s=4, submit="genuine", log="ok", touch_after=False, rerender=True, issue=True):
    """Khung + mặt nạ nộp + (tuỳ chọn) yêu cầu kiểm toán, mặt nạ render lại (luôn là render thật), log.
    submit: 'genuine' | 'upscaled' (matte 1× AA → bicubic → ngưỡng) | 'torso+2' (thân dài hơn 2% trong mặt nạ nộp).
    log: 'ok' | 'missing' | 'badsha' | 'noframe'."""
    kw = dict(s=s)
    if submit == "upscaled":
        kw["aa_up"] = ("cubic", False)
    v, pd = v1.c3_sample(d, name, H, **kw)
    size = cv2.imread(str(pd / "00000" / "head.png"), cv2.IMREAD_GRAYSCALE).shape[::-1]
    _, genuine = v1.figure(H * s, size=size, ss=v1.gen_ss(H * s))  # cùng hình học với khung render
    if submit == "torso+2":
        _, alt = v1.figure(H * s, size=size, ss=v1.gen_ss(H * s), scale_dev={"torso": 1.02})
        _write_masks(pd / "00000", {"torso": alt["torso"]})
    scene = d / f"{name}_scene.blend"
    scene.write_bytes(b"BLENDER-selftest scene " + name.encode())
    assets = d / f"{name}.assets.json"
    assets.write_text(json.dumps({"workdir": ".", "scene_files": [scene.name], "assets": []}))
    if not issue:
        return v, pd, assets
    req = au.issue(v, pd, "selftest", seed=12345)
    ad = au.audit_dir(v)
    if rerender:
        for f in req["frames"]:
            _write_masks(ad / "rerender" / f"{f:05d}", genuine)
    if log != "missing":
        sha = au.sha256_file(scene) if log != "badsha" else "0" * 64
        lines = [f"SCENE {scene.name} SHA256 {sha}"]
        if log != "noframe":
            lines += [f"FRAME {f} CMD blender -b {scene.name} -P render_masks.py -- --frame {f} --scale {s}"
                      for f in req["frames"]]
        (ad / "render.log").write_text("\n".join(lines) + "\n")
    if touch_after:  # xưởng sửa mặt nạ nộp sau khi đã biết khung được chọn
        _write_masks(pd / "00000", {"forearm": genuine["forearm"] & ~np.roll(genuine["forearm"], 3, 0)})
    return v, pd, assets


def _c3a(d, name, **kw):
    v, pd, assets = audit_sample(d, name, **kw)
    return check_c3(v, "shot", pd, d, audit=True, assets=assets)


def _audit_fail(r, key):
    """Ca TRƯỢT phải trượt đúng vì chỉ số kiểm toán mang tên key (không phải lý do khác)."""
    bad = [m["name"] for m in r["metrics"] if not m["ok"]]
    ok = any(key in n for n in bad)
    r["metrics"].append(metric(f"trượt đúng vì: {key}", ok, "==", True))
    if not ok:
        r["status"] = PASS  # để ca hiện SAI: trượt vì lý do khác
    return r


def cases(d):
    C = []

    def add(code, name, expect, fn):
        C.append((code, name, expect, fn))

    # J1 — Q-J1c
    def j1_room():
        mix, sd = j1_stem_sample(d, "j1v13_room")
        r = check_j1(mix, "shot", v12.TR_SCRIPT, sd)
        return v12._expect(r, any("stem thoại" in n for n in r["notes"]), "dùng quy tắc stem thoại (không phải −60 dBFS)")
    add("J1", "v1.3: table read + room tone −55 dBFS trong mix, stem thoại im giữa câu (Q-J1c)", PASS, j1_room)
    add("J1", "v1.3: chữ bịa trong room tone −55 dBFS: quy tắc −60 giữ, quy tắc stem thoại bỏ", PASS, j1_room_unit)

    def j1_insert():
        mix, sd = j1_stem_sample(d, "j1v13_insert")
        sp = v12._script(d, "j1v13_insert", v12.TR_SCRIPT.read_text().replace(" You'll be brighter now.", ""))
        return check_j1(mix, "shot", sp, sd)
    add("J1", "v1.3: chèn thật khi stem thoại có tiếng (kịch bản thiếu câu có trong stem thoại)", FAIL, j1_insert)

    # C3 — Q-δ
    def c3(name, H, **kw):
        v, pd = v1.c3_sample(d, name, H, **kw)
        return check_c3(v, "shot", pd, d)
    add("C3", "v1.3: đúng sheet, đầu 57 px, mặt nạ 2× (đầu < 100 px phải 4×)", FAIL,
        lambda: _audit_fail(c3("c3v13_small2x", 57, s=2), "mặt nạ ≥ 4×"))
    add("C3", "v1.3: đúng sheet, đầu 80 px, mặt nạ 4×", PASS, lambda: c3("c3v13_80_4x", 80, s=4))

    # C3 — kiểm toán ngẫu nhiên (Q-C3c)
    add("C3", "v1.3 kiểm toán: mặt nạ render lại khớp mặt nạ nộp, log đủ", PASS, lambda: _c3a(d, "c3a_ok"))
    add("C3", "v1.3 kiểm toán: mặt nạ nộp là matte 1× phóng to 4× bicubic rồi ngưỡng hoá (loại C3b không bắt được)",
        FAIL, lambda: _audit_fail(_c3a(d, "c3a_up", submit="upscaled"), "điểm ảnh khác nhau"))
    add("C3", "v1.3 kiểm toán: mặt nạ nộp khác render lại (thân dài hơn 2%)", FAIL,
        lambda: _audit_fail(_c3a(d, "c3a_torso", submit="torso+2"), "lệch tỷ lệ"))
    add("C3", "v1.3 kiểm toán: thiếu render.log", FAIL,
        lambda: _audit_fail(_c3a(d, "c3a_nolog", log="missing"), "render.log"))
    add("C3", "v1.3 kiểm toán: log ghi SHA file cảnh sai", FAIL,
        lambda: _audit_fail(_c3a(d, "c3a_badsha", log="badsha"), "SCENE"))
    add("C3", "v1.3 kiểm toán: log thiếu dòng FRAME … CMD", FAIL,
        lambda: _audit_fail(_c3a(d, "c3a_noframe", log="noframe"), "FRAME"))
    add("C3", "v1.3 kiểm toán: không render lại được (thiếu mặt nạ render lại)", FAIL,
        lambda: _audit_fail(_c3a(d, "c3a_norr", rerender=False), "thiếu hoặc khác kích thước"))
    add("C3", "v1.3 kiểm toán: mặt nạ nộp bị sửa sau khi phát yêu cầu", FAIL,
        lambda: _audit_fail(_c3a(d, "c3a_touch", touch_after=True), "không đổi sau khi phát"))

    def no_request():
        v, pd, assets = audit_sample(d, "c3a_noreq", issue=False)
        return check_c3(v, "shot", pd, d, audit=True, assets=assets)
    add("C3", "v1.3 kiểm toán: chưa có yêu cầu kiểm toán → THIẾU (không ĐẠT)", MISSING, no_request)

    def reissue():
        v, pd, _ = audit_sample(d, "c3a_reissue")
        try:
            au.issue(v, pd, "selftest")
        except FileExistsError as e:
            return result("C3", PASS, [metric("phát lại yêu cầu bị từ chối", True, "==", True)], notes=[str(e)])
        return result("C3", FAIL, [metric("phát lại yêu cầu bị từ chối", False, "==", True)])
    add("C3", "v1.3 kiểm toán: không phát lại yêu cầu khi đã có (chống chọn lại khung)", PASS, reissue)
    return C
