"""Test tự chứng minh cho thay đổi v1.5 (chủ dự án duyệt mở 29/09/2026):
1. P0 — hai khiếu nại Cổng 5 (chủ dự án CHẤP NHẬN): mặt/dáng nhân vật đọc thành chữ ("56" ở mắt Cas s42a khung 2775,
   "MA" ở dáng hai nhân vật s33 khung 1980). Chuỗi ≤ 3 ký tự nằm trên nhân vật (xoá nhân vật thì máy hết đọc ra chữ;
   mặt nạ khớp cạnh ảnh quanh hộp chữ) được miễn. Chữ thật vẫn bị bắt: ≥ 4 ký tự trên áo; "56" trên tường ngoài nhân
   vật; "56" sát nhân vật; mặt nạ giả che chữ. Hai khung khiếu nại là mẫu thật, giải mã khớp từng điểm ảnh bản gốc
   (x264 không mất dữ liệu; bản gốc layout.mp4 ở commit 8a707d7 và 44a469a).
2. C3 — trục đầu: đầu nhìn thấy rộng hơn cao (Cas 'bl' 0°/180°) làm trục chính PCA lật ngang. Model sheet khai
   'c3_head_axis': 'doc' → độ dài đầu đo theo trục dọc thân (thân→đầu), không lật; không khai → như v1.4.
3. Kiểm toán: 'silhouettes' nằm trong SHA bộ mặt nạ và được render lại như mặt nạ bộ phận.
"""
import contextlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
CHECKS = HERE.parent
sys.path.insert(0, str(CHECKS))

from cinecheck import audit as au  # noqa: E402
from cinecheck.common import FAIL, MISSING, PASS, read_rgb  # noqa: E402
from cinecheck.rule_c3 import check_c3, head_flipped, body_axis, load_mask  # noqa: E402
from cinecheck.rule_p0 import check_p0  # noqa: E402

import cases_v1 as v1  # noqa: E402
import cases_v14 as v14  # noqa: E402
import run_selftest as base  # noqa: E402

FIX = HERE / "fixtures"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LOSSLESS = ["-c:v", "libx264", "-qp", "0", "-preset", "veryfast"]
S42A, S33 = "p0_cong5_s42a_f2775", "p0_cong5_s33_f1980"
WIDE = 1.63  # đầu Cas 'bl' ở 0°: rộng 782 / cao 481 px mặt nạ
_why = v14._why


# ------------------------------------------------------------------ P0
def _parts_sil(d, name, sil_png, fake=None):
    """<name>.parts/ chỉ có bóng nhân vật cho khung 0 (không có mặt nạ C3). fake=(x0, y0, x1, y1): tô thêm khối giả."""
    pd = d / f"{name}.parts"
    pd.mkdir(parents=True, exist_ok=True)
    m = load_mask(sil_png)
    if fake is not None:
        m = m.copy()
        x0, y0, x1, y1 = fake
        m[y0:y1, x0:x1] = True
    Image.fromarray(m.astype(np.uint8) * 255).save(pd / "sil_00000.png")
    (pd / "parts.json").write_text(json.dumps({"silhouettes": {"0": "sil_00000.png"}}))
    return pd


def p0_real(d, name, fixture, masks=True):
    """Khung khiếu nại thật (bản gốc, không mã hoá lại)."""
    v = d / f"{name}.mp4"
    shutil.copy(FIX / f"{fixture}.mp4", v)
    pd = _parts_sil(d, name, FIX / f"{fixture}.sil.png") if masks else None
    return check_p0(v, "shot", None, None, pd)


def p0_insert(d, name, txt, xy, px=11, color=(250, 230, 120), fake=None):
    """Chèn chữ thật vào khung s42a (giải mã từ mẫu gốc), mã hoá không mất dữ liệu, kèm bóng nhân vật thật."""
    f = read_rgb(FIX / f"{S42A}.mp4", [0])[0]
    im = Image.fromarray(f.copy())
    ImageDraw.Draw(im).text(xy, txt, font=ImageFont.truetype(FONT, px), fill=color)
    v = d / f"{name}.mp4"
    base.encode_rgb([np.asarray(im)], v, vcodec=LOSSLESS)
    pd = _parts_sil(d, name, FIX / f"{S42A}.sil.png", fake)
    return check_p0(v, "shot", None, None, pd)


def _ev(r, key):
    return r["evidence"].get(key) or []


def _read(r, key, txt):
    return [x for x in _ev(r, key) if x["chu"] == txt]


# ------------------------------------------------------------------ C3
@contextlib.contextmanager
def head_width(w):
    """Bộ vẽ mẫu dùng v1.SHEET: tạm đổi bề ngang đầu (đầu rộng hơn cao), trả lại sau."""
    old = v1.SHEET["head"]["width"]
    v1.SHEET["head"]["width"] = w
    try:
        yield
    finally:
        v1.SHEET["head"]["width"] = old


def sheet15(axis="doc"):
    s = json.loads(json.dumps(v14.SHEET14))
    if axis is not None:
        s["c3_head_axis"] = axis
    return s


def c3_wide(d, name, axis="doc", dev=None, **kw):
    with head_width(WIDE):
        v, pd = v14.c3_video(d, name, v14.one(dev), sheet=sheet15(axis), views=lambda k: v14.nominal(), **kw)
    return v, pd


def c3_roll(d, name, deg, axis="doc", H=146, s=2):
    """Đầu rộng hơn cao, cả nhân vật nghiêng deg độ trong mặt phẳng ảnh (máy nghiêng). Vẽ ở s×, xoay khung và mặt nạ
    (mặt nạ mềm xoay rồi ngưỡng 0,5, vẫn là mặt nạ render ở s×), thu khung về 1×."""
    size = (int(6.6 * H) // 2 * 2, int(7.0 * H) // 2 * 2)
    with head_width(WIDE):
        fh, mh = v1.figure(H * s, size=(size[0] * s, size[1] * s), ss=v1.gen_ss(H * s), soft=True)
    c = (size[0] * s / 2, size[1] * s / 2)
    R = cv2.getRotationMatrix2D(c, deg, 1.0)
    wh = (size[0] * s, size[1] * s)
    fr = cv2.warpAffine(fh, R, wh, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    fr = cv2.resize(fr, size, interpolation=cv2.INTER_AREA)
    masks = {p: cv2.warpAffine(m.astype(np.float32), R, wh, flags=cv2.INTER_LINEAR) >= 0.5 for p, m in mh.items()}
    v = d / f"{name}.mp4"
    base.encode_rgb([fr], v)
    pd = d / f"{name}.parts"
    (pd / "00000").mkdir(parents=True, exist_ok=True)
    (pd / "sheet.json").write_text(json.dumps(sheet15(axis), ensure_ascii=False))
    spec = {"model_sheet": "sheet.json", "scale": s, "frames": {"0": {}}, "views": {"0": v14.nominal()}}
    for p, m in masks.items():
        Image.fromarray(m.astype(np.uint8) * 255).save(pd / "00000" / f"{p}.png")
        spec["frames"]["0"][p] = f"00000/{p}.png"
    (pd / "parts.json").write_text(json.dumps(spec))
    return v, pd, masks


def _flips(r):
    return len(_ev(r, "dau_rong_hon_cao"))


def _audit(d, name, sil=True, rerender_sil=True, change_after=False, axis="doc", extra=(), rerender_extra=True):
    """Nộp mặt nạ (đầu rộng, sheet 'doc') + 'silhouettes' (hợp các bộ phận), P phát yêu cầu, xưởng render lại.
    extra: khung CHỈ có bóng nhân vật (ngoài khung C3; hình tĩnh nên bóng = bóng khung 0)."""
    with head_width(WIDE):
        v, pd = v14.c3_video(d, name, [dict(n=16 if extra else 1)], H=100, s=4, sheet=sheet15(axis),
                             views=lambda k: v14.nominal())
    spec = json.loads((pd / "parts.json").read_text())
    if sil:
        spec["silhouettes"] = {}
        for k, fr in spec["frames"].items():
            m = np.any([load_mask(pd / rel) for rel in fr.values()], axis=0)
            Image.fromarray(m.astype(np.uint8) * 255).save(pd / f"sil_{int(k):05d}.png")
            spec["silhouettes"][k] = f"sil_{int(k):05d}.png"
        for k in extra:
            shutil.copy(pd / "sil_00000.png", pd / f"sil_{k:05d}.png")
            spec["silhouettes"][str(k)] = f"sil_{k:05d}.png"
        (pd / "parts.json").write_text(json.dumps(spec))
    scene = d / f"{name}_scene.blend"
    scene.write_bytes(b"BLENDER-selftest scene " + name.encode())
    assets = d / f"{name}.assets.json"
    assets.write_text(json.dumps({"workdir": ".", "scene_files": [scene.name], "assets": []}))
    req = au.issue(v, pd, "selftest", seed=515151)
    ad = au.audit_dir(v)
    for f in req["frames"]:
        rr = ad / "rerender" / f"{f:05d}"
        rr.mkdir(parents=True, exist_ok=True)
        for p, rel in spec["frames"][str(f)].items():
            shutil.copy(pd / rel, rr / f"{p}.png")
        (rr / "views.json").write_text(json.dumps(v14.nominal()))
        if sil and rerender_sil:
            shutil.copy(pd / spec["silhouettes"][str(f)], rr / "silhouette.png")
    for f in req.get("sil_frames", []):
        if rerender_extra:
            rr = ad / "rerender" / f"{f:05d}"
            rr.mkdir(parents=True, exist_ok=True)
            shutil.copy(pd / spec["silhouettes"][str(f)], rr / "silhouette.png")
    (ad / "render.log").write_text(f"SCENE {scene.name} SHA256 {au.sha256_file(scene)}\n"
                                   + "".join(f"FRAME {f} CMD selftest figure --frame {f} --scale 4 --sil\n"
                                             for f in req["frames"] + req.get("sil_frames", [])))
    if change_after:  # sửa bóng nhân vật sau khi đã phát yêu cầu kiểm toán
        k = next(iter(spec["silhouettes"]))
        m = load_mask(pd / spec["silhouettes"][k]).copy()
        m[:40, :40] = True
        Image.fromarray(m.astype(np.uint8) * 255).save(pd / spec["silhouettes"][k])
    r = check_c3(v, "shot", pd, d, audit=True, assets=assets)
    r["_req"] = req
    return r


def _audit_row(r, name):
    return next((m for m in r["metrics"] if m["name"].startswith(name)), None)


def cases(d):
    C = []

    def add(code, name, expect, fn):
        C.append((code, name, expect, fn))

    # ---------------- P0 (a): hai khung khiếu nại thật
    for fx, txt, lbl in ((S42A, "56", "s42a khung 2775, '56' ở mắt Cas"), (S33, "MA", "s33 khung 1980, 'MA' ở dáng hai nhân vật")):
        add("P0", f"v1.5 (a): {lbl}, không mặt nạ nhân vật (v1.4, đối chứng: mẫu tái tạo đúng báo nhầm)", FAIL,
            lambda fx=fx, txt=txt: (lambda r: _why(r, bool(_read(r, "chu_khong_matte", txt)),
                                                   f"'{txt}' bị tính chữ không matte", FAIL))(
                p0_real(d, f"p0v15_{fx}_nomask", fx, masks=False)))
        add("P0", f"v1.5 (a): {lbl}, có bóng nhân vật → không báo chữ", PASS,
            lambda fx=fx, txt=txt: (lambda r: _why(r, bool(_read(r, "vung_nhan_vat_mien", txt)),
                                                   f"'{txt}' được miễn vì nằm trên nhân vật", PASS))(
                p0_real(d, f"p0v15_{fx}", fx)))

    # ---------------- P0 (b): chữ thật ≥ 4 ký tự trên áo Cas (trong mặt nạ) vẫn bị bắt
    def on_shirt(name, txt, x):
        r = p0_insert(d, name, txt, (x, 250))
        hit = _read(r, "chu_khong_matte", txt)
        m = load_mask(FIX / f"{S42A}.sil.png")
        inside = bool(hit) and m[hit[0]["hop"][1]:hit[0]["hop"][3] + 1, hit[0]["hop"][0]:hit[0]["hop"][2] + 1].mean() >= 0.9
        return _why(r, inside, f"'{txt}' dò được, hộp nằm ≥ 90% trong mặt nạ nhân vật, vẫn tính chữ không matte", FAIL)
    add("P0", "v1.5 (b): chữ thật 'BAKERY' (6 ký tự) in trên áo Cas → vẫn TRƯỢT", FAIL,
        lambda: on_shirt("p0v15_b_bakery", "BAKERY", 455))
    add("P0", "v1.5 (b): chữ thật 'CAFE' (4 ký tự, sát giới hạn) in trên áo Cas → vẫn TRƯỢT", FAIL,
        lambda: on_shirt("p0v15_b_cafe", "CAFE", 464))

    # ---------------- P0 (c): "56" ngoài nhân vật vẫn bị bắt
    def wall(name, xy, color, why_key):
        r = p0_insert(d, name, "56", xy, px=12, color=color)
        hit = _read(r, "chu_khong_matte", "56")
        return _why(r, bool(hit) and why_key in hit[0].get("ly_do_khong_mien", ""),
                    f"'56' không được miễn vì: {why_key}", FAIL)
    add("P0", "v1.5 (c): '56' trên tường, ngoài nhân vật → vẫn TRƯỢT", FAIL,
        lambda: wall("p0v15_c_wall", (250, 160), (40, 40, 50), "không chạm"))
    add("P0", "v1.5 (c): '56' trên nền cửa tối, chạm mép đầu Cas → vẫn TRƯỢT (xoá nhân vật vẫn đọc ra '56')", FAIL,
        lambda: wall("p0v15_c_ke", (521, 196), (235, 235, 235), "vẫn đọc ra chữ"))
    add("P0", "v1.5 (c): '56' trên tường + mặt nạ giả vẽ thêm che chữ → vẫn TRƯỢT (mặt nạ không khớp cạnh ảnh)", FAIL,
        lambda: (lambda r: _why(r, bool(_read(r, "chu_khong_matte", "56")) and "không khớp cạnh ảnh"
                                in _read(r, "chu_khong_matte", "56")[0].get("ly_do_khong_mien", ""),
                                "'56' không được miễn vì mặt nạ giả không khớp cạnh ảnh", FAIL))(
            p0_insert(d, "p0v15_d_fake", "56", (250, 160), px=12, color=(40, 40, 50), fake=(240, 150, 290, 185))))
    add("P0", "v1.5 giới hạn đã biết (phán quyết cho phép): chữ thật ≤ 3 ký tự in trên áo ('56') được miễn, liệt kê "
        "trong bằng chứng để người duyệt soi", PASS,
        lambda: (lambda r: _why(r, bool(_read(r, "vung_nhan_vat_mien", "56")), "'56' trên áo nằm trong danh sách miễn",
                                PASS))(p0_insert(d, "p0v15_lim_56", "56", (472, 250))))

    def via_run():
        """run.py tự tìm <video>.parts/ và đưa vào P0."""
        v = d / "p0v15_runpy.mp4"
        shutil.copy(FIX / f"{S42A}.mp4", v)
        _parts_sil(d, "p0v15_runpy", FIX / f"{S42A}.sil.png")
        out = d / "p0v15_runpy_rep"
        subprocess.run([sys.executable, str(CHECKS / "run.py"), str(v), "--only", "P0", "--out", str(out)],
                       capture_output=True, text=True)
        rep = json.loads(next(out.glob("*.json")).read_text())
        r = next(x for x in rep["results"] if x["code"] == "P0")
        return _why(r, bool(_read(r, "vung_nhan_vat_mien", "56")), "run.py đưa <video>.parts/ vào P0", PASS)
    add("P0", "v1.5: run.py tự dùng <video>.parts/ (bóng nhân vật) cho P0, khung s42a → không báo chữ", PASS, via_run)

    # ---------------- C3: trục đầu
    def wide(name, axis, dev=None):
        v, pd = c3_wide(d, name, axis=axis, dev=dev)
        r = check_c3(v, "shot", pd, d)
        return r, _flips(r) > 0
    add("C3", f"v1.5: đầu rộng hơn cao (rộng {WIDE:g} × cao 1 H) ở 0°, sheet khai c3_head_axis 'doc' → ĐẠT", PASS,
        lambda: (lambda rf: _why(rf[0], rf[1], "trục chính PCA của đầu lật ngang (ghi trong 'dau_rong_hon_cao') mà "
                                 "độ dài đầu vẫn là chiều cao", PASS))(wide("c3v15_wide_doc", "doc")))
    add("C3", "v1.5 đối chứng: cùng mặt nạ, sheet không khai (đo như v1.4, trục chính) → trục lật, TRƯỢT", FAIL,
        lambda: (lambda rf: _why(rf[0], rf[1] and any("đo bề ngang đầu" in n for n in rf[0]["notes"]),
                                 "trục lật và có ghi chú khuyên đo lại theo 'doc'", FAIL))(wide("c3v15_wide_pca", None)))
    add("C3", "v1.5: đầu rộng hơn cao, 'doc', thân dài +20% → vẫn TRƯỢT", FAIL,
        lambda: wide("c3v15_wide_torso", "doc", dev={"torso": 1.2})[0])

    def roll(deg):
        v, pd, m = c3_roll(d, f"c3v15_roll{deg}", deg)
        r = check_c3(v, "shot", pd, d)
        ref, src = body_axis(m)
        tilt = float(np.degrees(np.arccos(min(1.0, abs(ref[1])))))
        return _why(r, src == "thân→đầu" and abs(tilt - abs(deg)) < 3 and head_flipped(m["head"], ref),
                    f"trục dọc thân nghiêng theo nhân vật ({tilt:.1f}° ≈ {abs(deg)}°) và đầu rộng hơn cao", PASS)
    add("C3", "v1.5: đầu rộng hơn cao, cả nhân vật nghiêng 20° trong khung (máy nghiêng), 'doc' → ĐẠT", PASS,
        lambda: roll(20))
    def bad_axis():
        v, pd = c3_wide(d, "c3v15_badaxis", axis="vertical")
        r = check_c3(v, "shot", pd, d)
        return _why(r, v14._no_leak(r) and any("c3_head_axis" in n for n in r["notes"]),
                    "thông báo nêu đúng trường c3_head_axis", MISSING)
    add("C3", "v1.5: c3_head_axis sai giá trị ('vertical') → THIẾU, thông báo rõ", MISSING, bad_axis)

    # ---------------- kiểm toán: 'doc' + silhouettes
    add("C3", "v1.5 kiểm toán: sheet 'doc' + 'silhouettes', render lại khớp (cả silhouette.png) → ĐẠT", PASS,
        lambda: _audit(d, "c3v15_aud_ok"))
    add("C3", "v1.5 kiểm toán: có 'silhouettes' mà render lại thiếu silhouette.png → TRƯỢT", FAIL,
        lambda: (lambda r: _why(r, not _audit_row(r, "kiểm toán: mặt nạ render lại thiếu")["ok"],
                                "thiếu silhouette.png render lại", FAIL))(
            _audit(d, "c3v15_aud_nosil", rerender_sil=False)))
    add("C3", "v1.5 kiểm toán: sửa bóng nhân vật sau khi phát yêu cầu → TRƯỢT (SHA bộ mặt nạ gồm 'silhouettes')", FAIL,
        lambda: (lambda r: _why(r, not _audit_row(r, "kiểm toán: bộ mặt nạ nộp không đổi")["ok"],
                                "SHA bộ mặt nạ đổi", FAIL))(_audit(d, "c3v15_aud_changed", change_after=True)))
    add("C3", "v1.5 kiểm toán: bóng nhân vật ở khung ngoài C3 (khung P0) → phiếu chọn thêm 1 khung bóng; render lại khớp "
        "→ ĐẠT", PASS,
        lambda: (lambda r: _why(r, r["_req"].get("sil_frames") in ([6], [15]) and r["_req"].get("sil_candidates") == 2,
                                "phiếu kiểm toán có 1 khung trong 2 khung chỉ có bóng", PASS))(
            _audit(d, "c3v15_aud_extra", extra=(6, 15))))
    add("C3", "v1.5 kiểm toán: khung bóng được chọn (ngoài C3) không render lại silhouette.png → TRƯỢT", FAIL,
        lambda: (lambda r: _why(r, not _audit_row(r, "kiểm toán: mặt nạ render lại thiếu")["ok"],
                                "thiếu silhouette.png của khung bóng được chọn", FAIL))(
            _audit(d, "c3v15_aud_extra_miss", extra=(6, 15), rerender_extra=False)))
    return C
