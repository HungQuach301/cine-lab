"""J1 — ASR trên bản mix cuối: 100% từ bắt buộc và WER."""
import re
import subprocess
import unicodedata

import numpy as np

from .common import FAIL, metric, probe, result, stream

MODEL_REPO = "Systran/faster-whisper-small.en"
MODEL_REVISION = "d1d751a5f8271d482d14ca55d9e2deeebbae577f"

_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen " \
        "fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _num_words(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + _num_words(n % 100))
    if n < 1_000_000:
        return _num_words(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + _num_words(n % 1000))
    return " ".join(_ONES[int(c)] for c in str(n))


def normalize(text):
    text = unicodedata.normalize("NFKC", text).lower()
    text = text.replace("’", "'").replace("‘", "'")
    text = re.sub(r"(\d),(\d)", r"\1\2", text)
    text = re.sub(r"\d+", lambda m: " " + _num_words(int(m.group())) + " ", text)
    text = text.replace("'", "")
    text = re.sub(r"[^a-z\s]", " ", text)
    return text.split()


def script_text(path):
    """Kịch bản thoại: bỏ dòng trống, dòng chú thích '#', và nhãn người nói 'NAME:' đầu dòng."""
    lines = []
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"^[A-Z][A-Z0-9 .'\-]{0,30}:\s+", "", s)
        s = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", s)  # chỉ dẫn diễn xuất không phải lời
        lines.append(s)
    return " ".join(lines)


def align(ref, hyp):
    """Căn Levenshtein. Trả về (S, D, I, danh sách cờ trúng cho từng từ ref)."""
    n, m = len(ref), len(hyp)
    d = np.zeros((n + 1, m + 1), dtype=np.int32)
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            c = 0 if ref[i - 1] == hyp[j - 1] else 1
            d[i, j] = min(d[i - 1, j - 1] + c, d[i - 1, j] + 1, d[i, j - 1] + 1)
    i, j, S, D, I = n, m, 0, 0, 0
    hit = [False] * n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i, j] == d[i - 1, j - 1] + (0 if ref[i - 1] == hyp[j - 1] else 1):
            if ref[i - 1] == hyp[j - 1]:
                hit[i - 1] = True
            else:
                S += 1
            i, j = i - 1, j - 1
        elif i > 0 and d[i, j] == d[i - 1, j] + 1:
            D += 1
            i -= 1
        else:
            I += 1
            j -= 1
    return S, D, I, hit


_model = None


def transcribe(path):
    global _model
    from faster_whisper import WhisperModel
    from huggingface_hub import snapshot_download
    if _model is None:
        try:
            local = snapshot_download(MODEL_REPO, revision=MODEL_REVISION, local_files_only=True)
        except Exception:
            local = snapshot_download(MODEL_REPO, revision=MODEL_REVISION)
        _model = WhisperModel(local, device="cpu", compute_type="int8", cpu_threads=4)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-ac", "1",
                          "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    segs, _ = _model.transcribe(audio, language="en", beam_size=5, temperature=0.0,
                                condition_on_previous_text=False, vad_filter=False,
                                initial_prompt=None, without_timestamps=False)
    segs = list(segs)
    return " ".join(s.text for s in segs), [(round(s.start, 2), round(s.end, 2), s.text.strip()) for s in segs]


def check_j1(path, profile, script_path=None):
    if stream(probe(path), "audio") is None:
        return result("J1", FAIL, notes=["Không có luồng âm."])
    ref = normalize(script_text(script_path))
    if not ref:
        return result("J1", None, [metric("số từ kịch bản", 0, ">=", 0)],
                      notes=["Kịch bản thoại rỗng: shot không có lời. Mọi lời ASR nghe thấy vẫn được ghi."])
    hyp_text, segs = transcribe(path)
    hyp = normalize(hyp_text)
    S, D, I, hit = align(ref, hyp)
    cov = 100.0 * sum(hit) / len(ref)
    wer = 100.0 * (S + D + I) / len(ref)
    missed = [dict(vi_tri=k, tu=ref[k], ngu_canh=" ".join(ref[max(0, k - 3):k + 4]))
              for k, h in enumerate(hit) if not h]
    ms = [metric("từ bắt buộc nghe đúng", cov, ">=", 100.0, "%", near_check=False),
          metric("WER", wer, "<=", 5.0, "%")]
    ev = dict(so_tu_kich_ban=len(ref), thay=S, mat=D, chen=I, tu_truot=missed[:50],
              ban_nghe=hyp_text.strip()[:4000], doan=segs[:200],
              mo_hinh=f"{MODEL_REPO}@{MODEL_REVISION}")
    return result("J1", None, ms, evidence=ev)
