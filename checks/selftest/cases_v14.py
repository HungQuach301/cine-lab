"""Test tự chứng minh cho thay đổi v1.4 (3 khiếu nại Cổng 3 được chủ dự án chấp nhận, chat 27/09/2026):
1. J1/J1b với file không có luồng âm: kịch bản rỗng → "—"; kịch bản có lời → THIẾU; có âm mà thiếu từ vẫn TRƯỢT.
2. C3 lược đồ model sheet: độ dài ở cấp gốc, trong parts{} hoặc c3_views; sai định dạng → THIẾU kèm thông báo.
3. C3 theo góc nhìn và tư thế: chỉ so ở mẫu đo được (góc nhìn ≤ 30° quanh một góc c3_views, không gập, không bị che,
   không lệch phối cảnh, không cắt khung), so với số của góc gần nhất; shot có nhân vật mà không mẫu nào đo được →
   CẦN NGƯỜI XEM. Kèm kiểm toán 'views' khi render lại.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
CHECKS = HERE.parent
sys.path.insert(0, str(CHECKS))

from cinecheck import audit as au  # noqa: E402
from cinecheck.common import FAIL, MISSING, NA, PASS, REVIEW, metric  # noqa: E402
from cinecheck.rule_c3 import check_c3  # noqa: E402
from cinecheck.rule_j1 import check_j1  # noqa: E402
from cinecheck.rule_j1b import check_j1b  # noqa: E402

import cases_v1 as v1  # noqa: E402
import run_selftest as base  # noqa: E402

FIX = HERE / "fixtures"
MEASURED = [p for p in v1.SHEET["measured_parts"] if p != "head"]
# Sheet thử có bảng nhiều góc (ratio so với đầu); '−90°' dùng dấu trừ Unicode để kiểm cách đọc khoá góc.
C3_VIEWS = {
    "0°": {"head": 1.0, "torso": 1.9, "upper_arm": 0.95, "forearm": 0.85, "thigh": 1.2, "shin": 1.15},
    "45°": {"head": 1.0, "torso": 1.75, "upper_arm": 0.9, "forearm": 0.8, "thigh": 1.15, "shin": 1.1},
    "90°": {"head": 1.0, "torso": 1.6, "upper_arm": None, "forearm": None, "thigh": 1.1, "shin": 1.05},
    "−90°": {"head": 1.0, "torso": 1.6, "upper_arm": 0.92, "forearm": 0.83, "thigh": 1.1, "shin": 1.05},
}
SHEET14 = dict(v1.SHEET, c3_views=C3_VIEWS)


def _why(r, cond, why, expect):
    """Ca phải ra kết quả đúng VÌ đúng lý do: không thoả thì đổi trạng thái để ca hiện SAI."""
    r["metrics"].append(metric(f"đúng lý do: {why}", bool(cond), "==", True))
    if not cond:
        r["status"] = "SAI-LÝ-DO" if r["status"] == expect else r["status"]
    return r


# ------------------------------------------------------------------ J1 / J1b: không có luồng âm
def _silent_video(d, name):
    v = d / f"{name}.mp4"
    base.lavfi_video(v, dur=1)
    return v


def _script(d, name, text):
    p = d / f"{name}.script.txt"
    p.write_text(text)
    return p


# ------------------------------------------------------------------ C3: mẫu render thật ở s×
def nominal(view=0.0, elev=0.0, **over):
    """Một mục 'views': mọi bộ phận không gập (foreshorten 1), không bị che, cùng độ sâu với đầu; over ghi đè."""
    parts = {p: dict(foreshorten=1.0, hidden=0.0, depth=1.0) for p in ["head"] + MEASURED}
    for p, q in over.items():
        parts[p] = dict(parts[p], **q)
    return dict(view_deg=view, elev_deg=elev, parts=parts)


def c3_video(d, name, blocks, H=146, s=2, sheet=SHEET14, views=None, empty=()):
    """blocks: danh sách shot, mỗi shot dict(n=số khung, dev={bộ phận: hệ số độ dài}, jy=dịch dọc px video, bg=màu nền
    hoặc None). Mỗi shot là một hình tĩnh lặp lại; mặt nạ render thật ở s× cho mọi khung chia hết cho 12.
    views: hàm khung → mục views (None = không ghi 'views'). empty: bộ phận ghi mặt nạ rỗng (xuất ra nhưng không thấy)."""
    size = (max(640, (int(4.2 * H) + 80) // 2 * 2), (int(6.2 * H) + 80) // 2 * 2)
    frames, masks_at, f0 = [], {}, 0
    for b in blocks:
        fh, mh = v1.figure(H * s, size=(size[0] * s, size[1] * s), scale_dev=b.get("dev"),
                           jitter=(0.0, b.get("jy", 0.0) * s), ss=v1.gen_ss(H * s))
        fr = cv2.resize(fh, size, interpolation=cv2.INTER_AREA)
        if b.get("bg") is not None:
            sil = cv2.resize(np.stack(list(mh.values())).any(0).astype(np.float32), size,
                             interpolation=cv2.INTER_AREA)[..., None]
            fr = np.clip(fr * sil + np.array(b["bg"], np.float32) * (1 - sil), 0, 255).astype(np.uint8)
        frames += [fr] * b["n"]
        for k in range(f0, f0 + b["n"]):
            if k % 12 == 0:
                masks_at[k] = mh
        f0 += b["n"]
    v = d / f"{name}.mp4"
    base.encode_rgb(frames, v)
    pd = d / f"{name}.parts"
    pd.mkdir(parents=True, exist_ok=True)
    (pd / "sheet.json").write_text(json.dumps(sheet, ensure_ascii=False))
    spec = {"model_sheet": "sheet.json", "scale": s, "frames": {}}
    for k, mh in masks_at.items():
        sub = pd / f"{k:05d}"
        sub.mkdir(exist_ok=True)
        spec["frames"][str(k)] = {}
        for p, m in mh.items():
            m = np.zeros_like(m) if p in empty else m
            Image.fromarray(np.asarray(m, np.uint8) * 255).save(sub / f"{p}.png")
            spec["frames"][str(k)][p] = f"{k:05d}/{p}.png"
    if views is not None:
        spec["views"] = {str(k): views(k) for k in masks_at}
    (pd / "parts.json").write_text(json.dumps(spec, ensure_ascii=False))
    return v, pd


def c3(d, name, blocks, **kw):
    v, pd = c3_video(d, name, blocks, **kw)
    return check_c3(v, "shot", pd, d)


def one(dev=None, jy=0.0):
    return [dict(n=1, dev=dev, jy=jy)]


def ratio_dev(view_key):
    """Hệ số vẽ để nhân vật khớp đúng số của một góc trong c3_views (so với số góc 0° mà bộ vẽ dùng)."""
    return {p: C3_VIEWS[view_key][p] / C3_VIEWS["0°"][p] for p in MEASURED if C3_VIEWS[view_key][p] is not None}


def _audit_views(d, name, rerender_view=0.0):
    """Nộp mặt nạ + views (góc 0°), P phát yêu cầu, xưởng render lại mặt nạ (khớp) và views.json (góc rerender_view)."""
    v, pd = c3_video(d, name, one(), H=100, s=4, views=lambda k: nominal())
    scene = d / f"{name}_scene.blend"
    scene.write_bytes(b"BLENDER-selftest scene " + name.encode())
    assets = d / f"{name}.assets.json"
    assets.write_text(json.dumps({"workdir": ".", "scene_files": [scene.name], "assets": []}))
    req = au.issue(v, pd, "selftest", seed=424242)
    ad = au.audit_dir(v)
    spec = json.loads((pd / "parts.json").read_text())
    for f in req["frames"]:
        rr = ad / "rerender" / f"{f:05d}"
        rr.mkdir(parents=True, exist_ok=True)
        for p, rel in spec["frames"][str(f)].items():
            shutil.copy(pd / rel, rr / f"{p}.png")
        (rr / "views.json").write_text(json.dumps(nominal(view=rerender_view)))
    (ad / "render.log").write_text(f"SCENE {scene.name} SHA256 {au.sha256_file(scene)}\n"
                                   + "".join(f"FRAME {f} CMD selftest figure --frame {f} --scale 4 --views\n"
                                             for f in req["frames"]))
    return check_c3(v, "shot", pd, d, audit=True, assets=assets)


def _no_leak(r):
    """Sai định dạng phải báo THIẾU bằng thông báo rõ, không để lộ tên lỗi Python."""
    txt = " ".join(r["notes"])
    return "Sai định dạng" in txt and not any(t in txt for t in ("KeyError", "TypeError", "Traceback", "AttributeError"))


def cases(d):
    C = []

    def add(code, name, expect, fn):
        C.append((code, name, expect, fn))

    # ---------------- J1 / J1b: file không có luồng âm (khiếu nại Cổng 3 v3)
    def j_na(fn, code):
        v = _silent_video(d, f"{code}v14_na")
        sp = _script(d, f"{code}v14_na", "# khung phong cách, chưa làm âm\n[Ida nhìn đèn]\n")
        return fn(v, "shot", sp) if code == "j1" else fn(v, "shot", None, sp)
    add("J1", "v1.4: không có luồng âm, kịch bản rỗng (chỉ ghi chú/chỉ dẫn) → — (như M3)", NA,
        lambda: j_na(check_j1, "j1"))
    add("J1b", "v1.4: không có luồng âm, kịch bản rỗng → — (không cần stem)", NA, lambda: j_na(check_j1b, "j1b"))

    def j_missing(fn, code):
        v = _silent_video(d, f"{code}v14_miss")
        sp = _script(d, f"{code}v14_miss", "IDA: Goodnight, lamp.\n")
        return fn(v, "shot", sp) if code == "j1" else fn(v, "shot", None, sp)
    add("J1", "v1.4: không có luồng âm nhưng kịch bản có lời → THIẾU (không ĐẠT)", MISSING,
        lambda: j_missing(check_j1, "j1"))
    add("J1b", "v1.4: không có luồng âm nhưng kịch bản có lời → THIẾU (không ĐẠT)", MISSING,
        lambda: j_missing(check_j1b, "j1b"))

    def j1_short():
        sp = _script(d, "j1v14_short", (FIX / "speech_en.script.txt").read_text().rstrip("\n")
                     + "\nThe lamps were never lit again.\n")
        return check_j1(FIX / "speech_en.flac", "shot", sp)
    add("J1", "v1.4: có luồng âm nhưng thiếu từ (kịch bản thêm câu không nói) → vẫn TRƯỢT", FAIL, j1_short)

    def runpy_na():
        v = _silent_video(d, "runv14_na")
        _script(d, "runv14_na", "")
        out = d / "runv14_na_report"
        p = subprocess.run([sys.executable, str(CHECKS / "run.py"), str(v), "--only", "J1,J1b,M3", "--out", str(out)],
                           capture_output=True, text=True)
        rep = json.loads((out / "runv14_na.checks.json").read_text())
        st = {r["code"]: r["status"] for r in rep["results"]}
        r = [x for x in rep["results"] if x["code"] == "J1b"][0]
        return _why(r, st == {"J1": NA, "J1b": NA, "M3": NA} and p.returncode in (0, 3),
                    f"run.py: J1, J1b, M3 đều '—' khi không có luồng âm, kịch bản rỗng, không có stem ({st})", NA)
    add("J1b", "v1.4 run.py: không luồng âm + kịch bản rỗng + không có thư mục stem → J1, J1b, M3 đều —", NA, runpy_na)

    # ---------------- C3: góc nhìn và tư thế (chủ dự án chọn B-i)
    fold = {"forearm": 0.55}  # cẳng tay chĩa về máy: độ dài 2D còn 55%
    add("C3", "v1.4 (a): đúng tỷ lệ, cẳng tay gập về phía máy (2D còn 55%), views khai foreshorten 0,55 → không TRƯỢT",
        PASS, lambda: c3(d, "c3v14_a", one(fold), views=lambda k: nominal(forearm=dict(foreshorten=0.55))))
    add("C3", "v1.4 (a, đối chứng): cùng mẫu, không có views → so mọi mẫu như v1.3 → TRƯỢT oan (lý do khiếu nại)",
        FAIL, lambda: c3(d, "c3v14_a0", one(fold)))
    add("C3", "v1.4 (b): cánh tay (trên + cẳng) dài thêm 20% ở góc chuẩn 0°, không gập → TRƯỢT", FAIL,
        lambda: c3(d, "c3v14_b", one({"upper_arm": 1.2, "forearm": 1.2}), views=lambda k: nominal()))

    def c3_c():
        r = c3(d, "c3v14_c", one({"upper_arm": 1.2, "forearm": 1.2}), views=lambda k: nominal(view=150.0))
        sh = r["evidence"].get("theo_shot") or []
        return _why(r, len(sh) == 1 and sh[0]["do_duoc"] == 0 and len(r["evidence"]["khong_do_duoc"]) == len(MEASURED),
                    "báo 0/5 mẫu đo được trên shot, liệt kê 5 mẫu không đo được", REVIEW)
    add("C3", "v1.4 (c): shot toàn góc lệch (view 150°, cách góc gần nhất 60°), tay dài 20% → CẦN NGƯỜI XEM (không ĐẠT)",
        REVIEW, c3_c)
    add("C3", "v1.4: góc nhìn 0° nhưng máy ngẩng 35° (lệch 3D 35° > 30°) → CẦN NGƯỜI XEM", REVIEW,
        lambda: c3(d, "c3v14_elev", one(), views=lambda k: nominal(elev=35.0)))
    add("C3", "v1.4: nhân vật đúng số góc 45°, views 40° → so với góc gần nhất 45° → ĐẠT", PASS,
        lambda: c3(d, "c3v14_v45", one(ratio_dev("45°")), views=lambda k: nominal(view=40.0)))
    add("C3", "v1.4: cùng nhân vật (số góc 45°) nhưng views khai 5° → so với 0° → TRƯỢT", FAIL,
        lambda: c3(d, "c3v14_v45_at0", one(ratio_dev("45°")), views=lambda k: nominal(view=5.0)))

    def c3_null():
        r = c3(d, "c3v14_v90", one(ratio_dev("90°")), views=lambda k: nominal(view=85.0))
        sk = {x["bo_phan"] for x in r["evidence"]["khong_do_duoc"]}
        return _why(r, sk == {"upper_arm", "forearm"}, "tay trên, cẳng tay 'khuất ở góc tham chiếu' (c3_views null)", PASS)
    add("C3", "v1.4: view 85° → góc 90° ghi null cho tay → 2 tay không đo được, thân/chân đạt", PASS, c3_null)
    add("C3", "v1.4: cẳng tay gần máy hơn đầu 6% (vẽ dài 6%), views depth 0,94 → không đo được, còn lại ĐẠT", PASS,
        lambda: c3(d, "c3v14_depth", one({"forearm": 1.06}), views=lambda k: nominal(forearm=dict(depth=0.94))))
    add("C3", "v1.4 chống khai sai: mặt nạ cẳng tay rỗng nhưng views khai không bị che (hidden 0) → TRƯỢT", FAIL,
        lambda: c3(d, "c3v14_empty", one(), views=lambda k: nominal(), empty=("forearm",)))
    add("C3", "v1.4: cẳng tay bị che hoàn toàn (hidden 1,0), mặt nạ rỗng → không đo được, còn lại ĐẠT", PASS,
        lambda: c3(d, "c3v14_hidden", one(), views=lambda k: nominal(forearm=dict(hidden=1.0)), empty=("forearm",)))

    def c3_cut():
        r = c3(d, "c3v14_cut", one(jy=-60.0))
        return _why(r, all(x["ly_do"].startswith("đầu chạm mép khung") for x in r["evidence"]["khong_do_duoc"]),
                    "máy tự thấy đầu bị cắt khung (không cần views)", REVIEW)
    add("C3", "v1.4: đầu bị cắt ở mép trên khung, không có views → máy tự loại mẫu → CẦN NGƯỜI XEM", REVIEW, c3_cut)

    def c3_two_shots():
        blocks = [dict(n=24), dict(n=24, bg=(20, 30, 70))]
        r = c3(d, "c3v14_2shot", blocks, views=lambda k: nominal(view=0.0 if k < 24 else 150.0))
        sh = r["evidence"].get("theo_shot") or []
        ok = len(sh) == 2 and sh[0]["ty_le_pct"] == 100.0 and sh[1]["ty_le_pct"] == 0.0
        return _why(r, ok, f"tách 2 shot, tỷ lệ đo được theo shot 100% / 0% ({[x.get('ty_le_pct') for x in sh]})", REVIEW)
    add("C3", "v1.4: 2 shot trong một file, shot 2 toàn góc lệch → CẦN NGƯỜI XEM, báo tỷ lệ đo được từng shot", REVIEW,
        c3_two_shots)

    # ---------------- C3: kiểm toán views
    add("C3", "v1.4 kiểm toán: views render lại khớp bản nộp (mặt nạ khớp, log đủ)", PASS,
        lambda: _audit_views(d, "c3v14_aud_ok"))

    def aud_bad():
        r = _audit_views(d, "c3v14_aud_bad", rerender_view=40.0)
        return _why(r, any("views render lại lệch" in m["name"] and not m["ok"] for m in r["metrics"]),
                    "trượt vì views render lại lệch bản nộp", FAIL)
    add("C3", "v1.4 kiểm toán: views nộp khai 0° nhưng render lại ra 40° (khai sai góc để chọn số so) → TRƯỢT", FAIL,
        aud_bad)

    # ---------------- C3: lược đồ model sheet (khiếu nại tài liệu)
    nested = {"id": "SELFTEST-nested", "measured_parts": v1.SHEET["measured_parts"],
              "parts": {p: {"length": v1.SHEET[p]["length"]} for p in ["head"] + MEASURED}}
    add("C3", "v1.4 lược đồ: độ dài chỉ nằm trong parts{} (sheet của phim) → đọc được, ĐẠT", PASS,
        lambda: c3(d, "c3v14_nested", one(), sheet=nested))

    def fmt(name, sheet=None, views=None):
        r = c3(d, name, one(), sheet=sheet or SHEET14, views=views)
        return _why(r, _no_leak(r), "báo 'Sai định dạng' rõ ràng, không lộ lỗi Python", MISSING)
    bad = json.loads(json.dumps(nested))
    del bad["parts"]["torso"]
    add("C3", "v1.4 lược đồ: thiếu độ dài 'torso' ở mọi nơi (trước: LỖI ĐO KeyError) → THIẾU, thông báo rõ", MISSING,
        lambda: fmt("c3v14_badsheet", sheet=bad))
    add("C3", "v1.4 lược đồ: c3_views có khoá góc không đọc được ('front') → THIẾU, thông báo rõ", MISSING,
        lambda: fmt("c3v14_badkey", sheet=dict(SHEET14, c3_views=dict(C3_VIEWS, front=C3_VIEWS["0°"]))))
    add("C3", "v1.4 lược đồ: views thiếu trường foreshorten → THIẾU, thông báo rõ", MISSING,
        lambda: fmt("c3v14_badviews", views=lambda k: {"view_deg": 0, "elev_deg": 0, "parts": {
            p: {"hidden": 0, "depth": 1} for p in ["head"] + MEASURED}}))
    return C
