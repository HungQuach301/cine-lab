"""Test tự chứng minh cho thay đổi v1.2: J1 (ghép/tách, im lặng số, từng câu — 3 khiếu nại được chấp nhận)
và C3b (mặt nạ phóng to từ độ phân giải thấp; δ = 2 px). Mỗi thay đổi có mẫu TRƯỢT và mẫu SẠCH.
Mẫu J1 dùng chính audio table read nháp 1 bị khiếu nại (fixtures/tableread_d1.m4a, luồng AAC chép nguyên từ
reports/m1/cong2/tableread/last-round-tableread.mp4, nhánh claude/cine-lab-m1-last-round-f1667s)."""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from cinecheck.common import FAIL, PASS, metric, result  # noqa: E402
from cinecheck.rule_c3 import check_c3, length_px, uncertainty  # noqa: E402
from cinecheck.rule_j1 import SR, _word_list, align, check_j1, normalize, silence_mask  # noqa: E402

import cases_v1 as v1  # noqa: E402
import run_selftest as base  # noqa: E402

FIX = HERE / "fixtures"
TR = FIX / "tableread_d1.m4a"
TR_SCRIPT = FIX / "tableread_d1.script.txt"
WARM = (139.40, 139.86)  # "Warm" (câu 5): khởi âm 139,45 s theo RMS 50 ms, ASR mốc chữ 138,88–139,86 s


def _expect(r, cond, why):
    """Bổ sung điều kiện bằng chứng vào kết quả luật: không thoả thì ca coi như TRƯỢT."""
    r["metrics"].append(metric(why, bool(cond), "==", True))
    if not cond:
        r["status"] = FAIL
    return r


def _script(d, name, text):
    p = d / f"{name}.script.txt"
    p.write_text(text)
    return p


def _audio_edit(d, name, zero=None):
    """Chép audio table read ra WAV 48 kHz; tuỳ chọn đặt 0 tuyệt đối trong khoảng zero (giây)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(TR), "-ac", "2", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    if zero:
        x[int(zero[0] * 48000):int(zero[1] * 48000)] = 0
    p = d / f"{name}.wav"
    base.write_wav(p, x)
    return p


# ------------------------------------------------------------------ J1
def j1_appeals():
    r = check_j1(TR, "shot", TR_SCRIPT)
    e = r["evidence"]
    missed = {m["tu"] for m in e["tu_truot"]}
    r = _expect(r, not ({"good", "night", "warm"} & missed), "khiếu nại 1 và 3: 'goodnight' và 'warm' được nghe đúng")
    r = _expect(r, all(c["cua_so"][0] <= WARM[0] for c in e["theo_cau"] if c["loi"].startswith("Warm")),
                "khiếu nại 3: cửa sổ câu 5 chứa trọn 'Warm'")
    return r


def j1_compound_unit():
    ref, hyp = normalize("Goodnight, old street. Alright, okay."), normalize("Good night old street. All right OK")
    S, D, I, hit = align(ref, hyp)
    return result("J1", None, [metric("lỗi căn sau chuẩn hoá ghép/tách", S + D + I, "<=", 0),
                               metric("từ đúng", 100.0 * sum(hit) / len(ref), ">=", 100.0, "%", near_check=False)],
                  notes=[f"ref={ref}", f"hyp={hyp}"])


def j1_compound_strict():
    """Không nới: 'good' thay cho 'goodnight' vẫn là mất một từ."""
    ref, hyp = normalize("Goodnight, old street."), normalize("Good, old street.")
    S, D, I, hit = align(ref, hyp)
    return result("J1", None, [metric("lỗi căn", S + D + I, "<=", 0),
                               metric("từ đúng", 100.0 * sum(hit) / len(ref), ">=", 100.0, "%", near_check=False)],
                  notes=[f"ref={ref}", f"hyp={hyp}"])


def j1_silence_unit():
    """Chữ bịa trong đoạn 0 tuyệt đối bị bỏ; chữ thật chạm vùng có tiếng được giữ."""
    t = np.arange(int(3 * SR)) / SR
    audio = np.concatenate([0.1 * np.sin(2 * np.pi * 220 * t), np.zeros(int(2 * SR)), 0.1 * np.sin(2 * np.pi * 220 * t)])
    sil = silence_mask(audio.astype(np.float32))
    words = [(0.5, 0.9, "evening"), (3.4, 4.6, "you"), (4.8, 5.3, "old"), (5.9, 6.4, "street")]
    kept, dropped = _word_list(words, sil)
    return result("J1", None, [metric("chữ trong im lặng số bị bỏ", len(dropped), "==", 1),
                               metric("chữ chạm vùng có tiếng được giữ", len(kept), "==", 3)],
                  notes=[f"giữ={[w for _, _, w in kept]}", f"bỏ={dropped}"])


def cases(d):
    C = []

    def add(code, name, expect, fn):
        C.append((code, name, expect, fn))

    add("J1", "v1.2: table read nháp 1 bị khiếu nại (goodnight; 'you' trong im lặng số; 'warm' ở ranh giới đoạn)",
        PASS, j1_appeals)
    add("J1", "v1.2: bảng ghép/tách: goodnight = good night, alright = all right, okay = OK", PASS, j1_compound_unit)
    add("J1", "v1.2: không nới — 'good' thay cho 'goodnight' vẫn là lỗi", FAIL, j1_compound_strict)
    add("J1", "v1.2: chữ bịa trong đoạn 0 tuyệt đối bị bỏ, chữ ở vùng có tiếng được giữ", PASS, j1_silence_unit)
    add("J1", "v1.2: thiếu từ thật — xoá 'Warm' khỏi audio (đặt 0 tuyệt đối 139,40–139,86 s)", FAIL,
        lambda: check_j1(_audio_edit(d, "j1v12_nowarm", WARM), "shot", TR_SCRIPT))
    add("J1", "v1.2: chèn từ thật trong vùng có tiếng — kịch bản thiếu câu \"You'll be brighter now.\"", FAIL,
        lambda: check_j1(TR, "shot", _script(d, "j1v12_insert", TR_SCRIPT.read_text().replace(
            " You'll be brighter now.", ""))))
    add("J1", "v1.2: thiếu từ thật — kịch bản có thêm 'more' không nói (\"Three more counts\")", FAIL,
        lambda: check_j1(TR, "shot", _script(d, "j1v12_more", TR_SCRIPT.read_text().replace(
            "Three counts.", "Three more counts."))))

    # C3b
    def c3(name, H, **kw):
        v, pd = v1.c3_sample(d, name, H, **kw)
        return check_c3(v, "shot", pd, d)
    add("C3", "v1.2: mặt nạ thật 4× khử răng cưa (xám ở chính 4×), đầu 100 px", PASS,
        lambda: c3("c3v12_soft4", 100, s=4, soft=True))
    add("C3", "v1.2: matte 1× khử răng cưa phóng to 4× song tuyến, giữ xám (biên mờ)", FAIL,
        lambda: c3("c3v12_up_gray", 100, s=4, aa_up=("linear", True)))
    add("C3", "v1.2: matte 1× khử răng cưa phóng to 2× song tuyến, giữ xám (biên mờ)", FAIL,
        lambda: c3("c3v12_up_gray2", 146, s=2, aa_up=("linear", True)))
    add("C3", "v1.2: matte 1× khử răng cưa phóng to 4× láng giềng gần rồi ngưỡng hoá (bậc thang)", FAIL,
        lambda: c3("c3v12_up_nn", 100, s=4, aa_up=("nearest", False)))
    add("C3", "v1.2: δ = 2 px phủ sai số mặt nạ thật và mặt nạ phóng to ngưỡng hoá (s = 2, 3, 4; đầu 40–146 px)",
        PASS, c3_guard_band)
    return C


def c3_guard_band(heads=(40, 57, 85, 120, 146), n=2):
    """Loại phóng to không phát hiện được (matte 1× khử răng cưa → song tuyến/bicubic/Lanczos → ngưỡng) phải
    có sai số tỷ lệ ≤ U(δ = 2): khi đó nó không thể cho kết luận 'đạt' sai. Mặt nạ thật cũng phải ≤ U."""
    rng = np.random.default_rng(7)
    K = {"thật": None, "song tuyến": cv2.INTER_LINEAR, "bicubic": cv2.INTER_CUBIC, "Lanczos": cv2.INTER_LANCZOS4}
    worst = {k: 0.0 for k in K}
    for s in (2, 3, 4):
        for H in heads:
            for _ in range(n):
                size = (int(4.2 * H) + 80, int(6.2 * H) + 80)
                _, m = v1.figure(H * s, size=(size[0] * s, size[1] * s), ss=v1.gen_ss(H * s),
                                 jitter=tuple(rng.uniform(0, s, 2)))
                for kn, k in K.items():
                    c = m if k is None else {
                        p: cv2.resize(cv2.resize(mm.astype(np.float32), size, interpolation=cv2.INTER_AREA),
                                      (size[0] * s, size[1] * s), interpolation=k) >= 0.5 for p, mm in m.items()}
                    lh = length_px(c["head"])
                    for p in ("torso", "upper_arm", "forearm", "thigh", "shin"):
                        lp = length_px(c[p])
                        e = abs((lp / lh) / v1.SHEET[p]["length"] - 1)
                        worst[kn] = max(worst[kn], e / uncertainty(lp, lh))
    return result("C3", None, [metric(f"sai số / U(δ=2) lớn nhất — {k}", v, "<=", 1.0) for k, v in worst.items()],
                  notes=[json.dumps({k: round(v, 3) for k, v in worst.items()}, ensure_ascii=False)])
