"""Hàm dùng chung: ffprobe/ffmpeg, giải mã khung và âm, dựng kết quả luật."""
import json
import math
import subprocess

import numpy as np

from .registry import RULES

PASS, FAIL, MISSING, NA = "PASS", "FAIL", "MISSING", "N/A"
NEAR_PCT = 0.05  # CLAUDE.md: chỉ số trong ±5% quanh ngưỡng phải nêu tên


# ---------------------------------------------------------------- kết quả
def metric(name, value, op, threshold, unit="", near_check=True):
    """Một số đo so với ngưỡng. op: '<=', '>=', '==', 'in' (threshold=(lo, hi)).
    near_check=False cho ngưỡng tuyệt đối (ví dụ 100% từ) nơi 'sát ngưỡng' không có nghĩa."""
    if op == "<=":
        ok = value <= threshold
    elif op == ">=":
        ok = value >= threshold
    elif op == "==":
        ok = value == threshold
    elif op == "in":
        ok = threshold[0] <= value <= threshold[1]
    else:
        raise ValueError(op)
    near = False
    if near_check and isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
        bounds = threshold if op == "in" else ((threshold,) if op in ("<=", ">=") else ())
        for b in bounds:
            if isinstance(b, (int, float)) and b != 0 and abs(value - b) <= NEAR_PCT * abs(b):
                near = True
    if isinstance(value, float):
        value = round(value, 4)
    return dict(name=name, value=value, op=op, threshold=threshold, unit=unit, ok=bool(ok), near=near)


def result(code, status, metrics=(), notes=(), evidence=None):
    meta = RULES[code]
    metrics = list(metrics)
    if status is None:
        status = PASS if all(m["ok"] for m in metrics) else FAIL
    return dict(code=code, section=meta["section"], title=meta["title"], level=meta["level"],
                measure=meta["measure"], threshold_text=meta["threshold"], status=status,
                metrics=metrics, notes=list(notes), evidence=evidence or {})


def missing(code, what):
    return result(code, MISSING, notes=[f"Thiếu dữ liệu đầu vào: {what}"])


def not_applicable(code, why):
    return result(code, NA, notes=[why])


# ---------------------------------------------------------------- ffmpeg
def run_text(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Lệnh lỗi ({p.returncode}): {' '.join(cmd)}\n{p.stderr[-2000:]}")
    return p.stdout, p.stderr


def probe(path):
    out, _ = run_text(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    return json.loads(out)


def stream(info, kind):
    for s in info.get("streams", []):
        if s.get("codec_type") == kind:
            return s
    return None


def frac(s):
    if not s or s in ("0/0", "N/A"):
        return None
    a, b = s.split("/") if "/" in s else (s, "1")
    return float(a) / float(b) if float(b) else None


def packets(path, sel="v:0"):
    """Danh sách (pts_time, size) của mọi gói trong luồng."""
    out, _ = run_text(["ffprobe", "-v", "error", "-select_streams", sel, "-show_entries",
                       "packet=pts_time,size", "-of", "csv=p=0", str(path)])
    rows = []
    for line in out.splitlines():
        parts = line.strip().split(",")
        if len(parts) < 2 or parts[0] in ("", "N/A"):
            continue
        rows.append((float(parts[0]), int(parts[1])))
    return rows


def frame_count(path):
    return len(packets(path))


def read_luma(path, step=12, max_frames=240):
    """Trả về list (chỉ số khung, mảng luma float32 ở mã gốc, bit_depth). Không đổi dải."""
    info = probe(path)
    v = stream(info, "video")
    w, h = int(v["width"]), int(v["height"])
    pix = v.get("pix_fmt", "")
    deep = any(t in pix for t in ("10", "12", "16"))
    bit_depth = 10 if "10" in pix else (12 if "12" in pix else (16 if "16" in pix else 8))
    out_fmt = {10: "gray10le", 12: "gray12le", 16: "gray16le"}.get(bit_depth, "gray")
    n = frame_count(path)
    if n and n // step > max_frames:
        step = int(math.ceil(n / max_frames))
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0",
           "-vf", f"select='not(mod(n\\,{step}))',extractplanes=y", "-fps_mode", "passthrough",
           "-f", "rawvideo", "-pix_fmt", out_fmt, "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    dtype = np.uint16 if deep else np.uint8
    arr = np.frombuffer(raw, dtype=dtype)
    per = w * h
    k = arr.size // per
    frames = [(i * step, arr[i * per:(i + 1) * per].reshape(h, w).astype(np.float32)) for i in range(k)]
    return frames, bit_depth


def read_rgb(path, indices):
    """Trả về dict chỉ số khung -> mảng RGB uint8 (giải mã theo BT.709, dải limited)."""
    info = probe(path)
    v = stream(info, "video")
    w, h = int(v["width"]), int(v["height"])
    rng = "tv" if v.get("color_range", "tv") != "pc" else "pc"
    wanted = sorted(set(int(i) for i in indices))
    frames = {}
    for c in range(0, len(wanted), 80):
        chunk = wanted[c:c + 80]
        expr = "+".join(f"eq(n\\,{i})" for i in chunk)
        cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0",
               "-vf", f"select='{expr}',scale=in_color_matrix=bt709:in_range={rng}:out_range=pc,format=rgb24",
               "-fps_mode", "passthrough", "-f", "rawvideo", "-"]
        raw = subprocess.run(cmd, capture_output=True, check=True).stdout
        per = w * h * 3
        arr = np.frombuffer(raw, dtype=np.uint8)
        for j, idx in enumerate(chunk[: arr.size // per]):
            frames[idx] = arr[j * per:(j + 1) * per].reshape(h, w, 3)
    return frames


def read_audio(path, sr=48000, channels=2):
    """Giải mã luồng âm đầu tiên về float32 (n, channels). Trả None nếu không có âm."""
    info = probe(path)
    if stream(info, "audio") is None:
        return None
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-ac", str(channels),
           "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, channels)
