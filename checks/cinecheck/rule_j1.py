"""J1 — ASR trên bản mix cuối: 100% từ bắt buộc và WER.

v1.2 (3 khiếu nại J1 được chấp nhận, 27/09/2026):
1. Chuẩn hoá từ ghép/tách theo bảng COMPOUND (goodnight = good night…), áp cho cả kịch bản lẫn bản nghe.
2. Chữ ASR nằm hoàn toàn trong vùng im lặng số (RMS khung 50 ms < −60 dBFS) bị bỏ trước khi căn; vùng bị bỏ
   ghi vào báo cáo.
3. Kiểm theo từng câu thoại (mỗi dòng kịch bản): lượt ASR toàn file (có mốc từng chữ) để căn kịch bản với
   thời gian; cắt audio theo mốc câu; ASR riêng từng câu; căn từng câu. Chữ lượt toàn file nằm ngoài mọi
   cửa sổ câu (và không nằm trong im lặng số) vẫn tính là chèn.
Ngưỡng không đổi: 100% từ bắt buộc; WER ≤ 5%.

v1.3 (Q-J1c): khi có <video>.stems/dialogue.* (bắt buộc theo J1b), một chữ ASR chỉ được giữ (và tính chèn nếu
không khớp kịch bản) khi stem thoại có lời nói tại thời điểm đó: có ít nhất một khung 10 ms "có lời" (định nghĩa
như J1b: năng lượng > max(đỉnh − 35 dB, −60 dBFS)) trong [đầu chữ − 0,15 s, cuối chữ + 0,15 s]. Chữ rơi vào đoạn
stem thoại im lặng bị bỏ và liệt kê. Không có stem: giữ quy tắc im lặng số −60 dBFS của v1.2 (J1b khi đó báo THIẾU).
"""
import re
import subprocess
import unicodedata
from pathlib import Path

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


# Bảng quy tắc v1.2: từ ghép/tách và cách viết tương đương về âm → dạng chuẩn (tách). Áp sau khi bỏ dấu câu,
# dấu nháy và gạch nối (nên "good-night" đã thành "good night"). Chỉ các mục ghi ở đây; không so gần đúng.
COMPOUND = {
    # chào/đáp
    "goodnight": "good night", "goodbye": "good bye", "goodmorning": "good morning",
    "alright": "all right", "okay": "ok",
    # any-/every-/some-/no-
    "anymore": "any more", "anyone": "any one", "anybody": "any body", "anything": "any thing",
    "anywhere": "any where", "anyway": "any way", "anyways": "any ways",
    "everyone": "every one", "everybody": "every body", "everything": "every thing",
    "everywhere": "every where", "everyday": "every day",
    "someone": "some one", "somebody": "some body", "something": "some thing", "somewhere": "some where",
    "sometime": "some time", "sometimes": "some times", "noone": "no one", "nobody": "no body",
    "nothing": "no thing", "nowhere": "no where",
    # thời gian
    "tonight": "to night", "today": "to day", "tomorrow": "to morrow",
    # ghép thường gặp khi ASR viết tách
    "cannot": "can not", "maybe": "may be", "into": "in to", "onto": "on to",
    "outside": "out side", "inside": "in side", "upstairs": "up stairs", "downstairs": "down stairs",
    "streetlight": "street light", "streetlights": "street lights", "lamplight": "lamp light",
    "lamplighter": "lamp lighter", "lamppost": "lamp post", "lampposts": "lamp posts",
    # viết tắt đọc thành chữ
    "mr": "mister", "mrs": "missus", "ms": "miz", "dr": "doctor", "st": "saint",
}


def normalize(text):
    text = unicodedata.normalize("NFKC", text).lower()
    text = text.replace("’", "'").replace("‘", "'")
    text = re.sub(r"(\d),(\d)", r"\1\2", text)
    text = re.sub(r"\d+", lambda m: " " + _num_words(int(m.group())) + " ", text)
    text = text.replace("'", "")
    text = re.sub(r"[^a-z\s]", " ", text)
    out = []
    for w in text.split():
        out += COMPOUND.get(w, w).split()
    return out


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
SR = 16000
SIL_DB = -60.0      # im lặng số: RMS khung 50 ms < −60 dBFS
SIL_FRAME = 0.05
SPEECH_MARGIN = 0.15  # dung sai mốc chữ ASR so với stem (J1b cho phép lệch stem–mix ±100 ms)
PAD_MAX = 2.0       # cửa sổ câu nới tối đa 2 s ra ngoài chữ neo đầu/cuối (không vượt điểm giữa khoảng lặng)
WIN_MAX = 28.0      # cửa sổ > 28 s được tách tại khoảng cách câu lớn nhất (Whisper giải mã 30 s)


def _get_model():
    global _model
    from faster_whisper import WhisperModel
    from huggingface_hub import snapshot_download
    if _model is None:
        try:
            local = snapshot_download(MODEL_REPO, revision=MODEL_REVISION, local_files_only=True)
        except Exception:
            local = snapshot_download(MODEL_REPO, revision=MODEL_REVISION)
        _model = WhisperModel(local, device="cpu", compute_type="int8", cpu_threads=4)
    return _model


def load_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def asr(audio, offset=0.0):
    """ASR một đoạn audio 16 kHz. Trả (văn bản, đoạn, chữ [(bắt đầu, kết thúc, chữ)] theo thời gian file)."""
    segs, _ = _get_model().transcribe(audio, language="en", beam_size=5, temperature=0.0,
                                      condition_on_previous_text=False, vad_filter=False,
                                      initial_prompt=None, without_timestamps=False, word_timestamps=True)
    segs = list(segs)
    words = [(offset + w.start, offset + w.end, w.word.strip()) for sg in segs for w in (sg.words or [])]
    return (" ".join(sg.text for sg in segs),
            [(round(offset + sg.start, 2), round(offset + sg.end, 2), sg.text.strip()) for sg in segs], words)


def transcribe(path):
    """Giữ giao diện v1: ASR toàn file."""
    t, segs, _ = asr(load_audio(path))
    return t, segs


def silence_mask(audio):
    n = int(SR * SIL_FRAME)
    k = len(audio) // n
    fr = audio[:k * n].reshape(k, n).astype(np.float64)
    return 10 * np.log10((fr ** 2).mean(1) + 1e-20) < SIL_DB


def silent_regions(sil):
    out, start = [], None
    for i, v in enumerate(list(sil) + [False]):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((round(start * SIL_FRAME, 2), round(i * SIL_FRAME, 2)))
            start = None
    return out


def in_silence(sil, t0, t1):
    """Chữ nằm hoàn toàn trong im lặng số: mọi khung 50 ms chạm [t0, t1] đều im lặng."""
    a, b = int(np.floor(t0 / SIL_FRAME)), int(np.ceil(t1 / SIL_FRAME))
    a, b = max(0, a), min(len(sil), max(b, a + 1))
    return a < len(sil) and bool(sil[a:b].all())


def script_lines(path):
    """Câu thoại = mỗi dòng kịch bản (cùng quy tắc bỏ nhãn, chỉ dẫn như script_text)."""
    out = []
    for line in open(path, encoding="utf-8"):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"^[A-Z][A-Z0-9 .'\-]{0,30}:\s+", "", s)
        s = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", s)
        w = normalize(s)
        if w:
            out.append((s.strip(), w))
    return out


def dialogue_activity(stem_dir):
    """(mặt nạ 'có lời' khung 10 ms như J1b, tên file, năng lượng 50 ms). (None, None, None) nếu không có stem thoại."""
    from .rule_j1b import AUDIO_EXT
    d = Path(stem_dir)
    dia = [p for p in sorted(d.iterdir()) if p.suffix.lower() in AUDIO_EXT and p.stem.lower() == "dialogue"]
    if not dia:
        return None, None, None
    x = load_audio(dia[0])
    hop = SR // 100
    fr = len(x) // hop
    e = 10 * np.log10(np.mean(x[:fr * hop].astype(np.float64).reshape(fr, hop) ** 2, 1) + 1e-20)
    if fr == 0 or e.max() < -60:
        return np.zeros(max(fr, 1), bool), dia[0].name, energy50(x)
    return e > max(e.max() - 35, -60), dia[0].name, energy50(x)


def speech_at(act, t0, t1):
    a = max(0, int(np.floor((t0 - SPEECH_MARGIN) * 100)))
    b = min(len(act), int(np.ceil((t1 + SPEECH_MARGIN) * 100)) + 1)
    return a < b and bool(act[a:b].any())


def _word_list(words, sil, act=None):
    """Tách chữ ASR thành [(t0, t1, từ chuẩn hoá)] giữ lại, và danh sách chữ bị bỏ.
    act (mặt nạ lời của stem thoại) có thì bỏ chữ ngoài đoạn có lời; không có thì bỏ chữ trong im lặng số."""
    kept, dropped = [], []
    for t0, t1, w in words:
        toks = normalize(w)
        if not toks:
            continue
        if act is not None:
            if not speech_at(act, t0, t1):
                dropped.append(dict(bat_dau=round(t0, 2), ket_thuc=round(t1, 2), chu=w, ly_do="stem thoại im"))
                continue
        elif in_silence(sil, t0, t1):
            dropped.append(dict(bat_dau=round(t0, 2), ket_thuc=round(t1, 2), chu=w, ly_do="im lặng số"))
            continue
        kept += [(t0, t1, t) for t in toks]
    return kept, dropped


def _align_map(ref, hyp):
    """Căn Levenshtein, trả ánh xạ chỉ số ref → chỉ số hyp cho các cặp trùng."""
    n, m = len(ref), len(hyp)
    d = np.zeros((n + 1, m + 1), dtype=np.int32)
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            c = 0 if ref[i - 1] == hyp[j - 1] else 1
            d[i, j] = min(d[i - 1, j - 1] + c, d[i - 1, j] + 1, d[i, j - 1] + 1)
    i, j, mp = n, m, {}
    while i > 0 and j > 0:
        c = 0 if ref[i - 1] == hyp[j - 1] else 1
        if d[i, j] == d[i - 1, j - 1] + c:
            if c == 0:
                mp[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif d[i, j] == d[i - 1, j] + 1:
            i -= 1
        else:
            j -= 1
    return mp


def energy50(x):
    """Năng lượng (dB) theo khung 50 ms."""
    n = int(SR * SIL_FRAME)
    k = len(x) // n
    return 10 * np.log10(np.mean(x[:k * n].astype(np.float64).reshape(k, n) ** 2, 1) + 1e-20)


def quiet_cut(e, t0, t1):
    """Điểm cắt giữa hai câu: tâm đoạn lặng dài nhất (khung ≤ min + 10 dB) trong [t0, t1] (giây).
    v1.3: không dùng mốc KẾT THÚC chữ của Whisper (chữ cuối câu có thể bị kéo dài nuốt chữ đầu câu sau)."""
    a, b = int(np.floor(t0 / SIL_FRAME)), int(np.ceil(t1 / SIL_FRAME))
    a, b = max(0, a), min(len(e), b)
    if b - a < 3:
        return (t0 + t1) / 2
    seg = e[a:b]
    q = seg <= seg.min() + 10
    best, cur, start, bs = 0, 0, 0, 0
    for i, v in enumerate(list(q) + [False]):
        if v:
            if cur == 0:
                start = i
            cur += 1
        else:
            if cur > best:
                best, bs = cur, start
            cur = 0
    return (a + bs + best / 2) * SIL_FRAME


def sentence_windows(lines, full_words, dur, e=None):
    """Mốc câu từ căn kịch bản với chữ lượt toàn file. Trả list (t0, t1, neo) mỗi câu.
    Ranh giới hai câu neo được = đoạn lặng dài nhất giữa lúc BẮT ĐẦU chữ neo cuối câu trước và lúc bắt đầu
    chữ neo đầu câu sau (e: năng lượng 50 ms của stem thoại nếu có, không thì của mix)."""
    ref, owner = [], []
    for k, (_, w) in enumerate(lines):
        ref += w
        owner += [k] * len(w)
    hyp = [w for _, _, w in full_words]
    mp = _align_map(ref, hyp)
    anchors = [[] for _ in lines]
    for ri, hj in mp.items():
        anchors[owner[ri]].append((full_words[hj][0], full_words[hj][1]))
    # (bắt đầu chữ neo đầu, kết thúc chữ neo cuối, bắt đầu chữ neo cuối)
    span = [(min(a[0] for a in an), max(a[1] for a in an), max(a[0] for a in an)) if an else None
            for an in anchors]
    idx = [k for k in range(len(lines)) if span[k]]
    cut = {}
    for k, k2 in zip(idx, idx[1:]):
        t0, t1 = span[k][2], span[k2][0]
        cut[(k, k2)] = quiet_cut(e, t0, t1) if e is not None and t1 > t0 else (span[k][1] + t1) / 2
    wins = []
    for k in range(len(lines)):
        pk = next((j for j in range(k - 1, -1, -1) if span[j]), None)
        nk = next((j for j in range(k + 1, len(lines)) if span[j]), None)
        if span[k]:
            a0, a1, _ = span[k]
            lo = max(a0 - PAD_MAX, cut[(pk, k)] if pk is not None else 0.0, 0.0)
            hi = min(a1 + PAD_MAX, cut[(k, nk)] if nk is not None else dur, dur)
        else:  # câu không neo được: từ lúc bắt đầu chữ neo cuối câu trước tới chữ neo đầu câu sau
            lo = span[pk][2] if pk is not None else 0.0
            hi = span[nk][0] if nk is not None else dur
        wins.append((lo, hi, (span[k][0], span[k][1]) if span[k] else None))
    return wins


def _split_long(lo, hi, words):
    """Cửa sổ > WIN_MAX: tách đệ quy tại khoảng lặng lớn nhất giữa các chữ (lượt toàn file)."""
    if hi - lo <= WIN_MAX:
        return [(lo, hi)]
    inside = [w for w in words if lo <= w[0] and w[1] <= hi]
    gaps = [((a[1] + b[0]) / 2, b[0] - a[1]) for a, b in zip(inside, inside[1:]) if lo + 2 < (a[1] + b[0]) / 2 < hi - 2]
    cut = max(gaps, key=lambda g: g[1])[0] if gaps else (lo + hi) / 2
    return _split_long(lo, cut, words) + _split_long(cut, hi, words)


def check_j1(path, profile, script_path=None, stem_dir=None):
    if stream(probe(path), "audio") is None:
        return result("J1", FAIL, notes=["Không có luồng âm."])
    ref = normalize(script_text(script_path))
    if not ref:
        return result("J1", None, [metric("số từ kịch bản", 0, ">=", 0)],
                      notes=["Kịch bản thoại rỗng: shot không có lời. Mọi lời ASR nghe thấy vẫn được ghi."])
    lines = script_lines(script_path)
    ref = [w for _, rw in lines for w in rw]
    audio = load_audio(path)
    dur = len(audio) / SR
    sil = silence_mask(audio)
    act, stem_name, e_cut = None, None, energy50(audio)
    if stem_dir is not None and Path(stem_dir).is_dir():
        act, stem_name, e_stem = dialogue_activity(stem_dir)
        if e_stem is not None:
            e_cut = e_stem
    # lượt 1: toàn file, để căn kịch bản với thời gian và bắt lời nằm ngoài mọi câu
    full_text, full_segs, full_raw = asr(audio)
    full_words, dropped_full = _word_list(full_raw, sil, act)
    wins = sentence_windows(lines, full_words, dur, e_cut)
    # lượt 2: từng câu
    S = D = I = 0
    hit_all, per, dropped = [], [], list(dropped_full)
    for k, ((text, rw), (lo, hi, span)) in enumerate(zip(lines, wins)):
        hyp_words = []
        for a, b in _split_long(lo, hi, full_words):
            _, _, raw = asr(audio[int(a * SR):int(b * SR)], offset=a)
            kept, dr = _word_list(raw, sil, act)
            hyp_words += kept
            dropped += dr
        hw = [w for _, _, w in hyp_words]
        s_, d_, i_, hit = align(rw, hw)
        S, D, I = S + s_, D + d_, I + i_
        hit_all += hit
        per.append(dict(cau=k + 1, loi=text[:120], cua_so=[round(lo, 2), round(hi, 2)],
                        neo=[round(span[0], 2), round(span[1], 2)] if span else None,
                        nghe=" ".join(hw)[:300], thay=s_, mat=d_, chen=i_,
                        tu_truot=[rw[j] for j, h in enumerate(hit) if not h]))
    # chữ lượt toàn file nằm ngoài mọi cửa sổ câu: lời không có trong kịch bản → chèn
    outside = [w for w in full_words if not any(lo <= (w[0] + w[1]) / 2 <= hi for lo, hi, _ in wins)]
    I += len(outside)
    cov = 100.0 * sum(hit_all) / len(ref)
    wer = 100.0 * (S + D + I) / len(ref)
    missed = []
    k0 = 0
    for (_, rw) in lines:
        for j, w in enumerate(rw):
            if not hit_all[k0 + j]:
                missed.append(dict(vi_tri=k0 + j, tu=w, ngu_canh=" ".join(rw[max(0, j - 3):j + 4])))
        k0 += len(rw)
    ms = [metric("từ bắt buộc nghe đúng", cov, ">=", 100.0, "%", near_check=False),
          metric("WER", wer, "<=", 5.0, "%")]
    sil_regions = [r for r in silent_regions(sil) if r[1] - r[0] >= 0.5]
    notes = [f"{len(lines)} câu thoại, ASR từng câu (cửa sổ theo căn kịch bản với lượt toàn file). "
             + ((f"Chữ ASR bị bỏ vì stem thoại '{stem_name}' không có lời tại đó (Q-J1c): {len(dropped)}")
              if act is not None else
              f"Không có stem thoại: chữ ASR bị bỏ vì nằm hoàn toàn trong im lặng số (RMS 50 ms < {SIL_DB:g} dBFS): "
              f"{len(dropped)}")
             + (": " + "; ".join(f"'{x['chu']}' {x['bat_dau']}–{x['ket_thuc']} s" for x in dropped[:10])
                if dropped else "") + ".",
             f"Chữ lượt toàn file nằm ngoài mọi câu (tính chèn): {len(outside)}"
             + (": " + "; ".join(f"'{w}' {a:.2f} s" for a, _, w in outside[:10]) if outside else "") + ".",
             "Chuẩn hoá ghép/tách theo bảng COMPOUND (RULES.md), áp cho cả kịch bản và bản nghe."]
    ev = dict(so_tu_kich_ban=len(ref), thay=S, mat=D, chen=I, tu_truot=missed[:50], theo_cau=per[:200],
              chu_bo_vi_im_lang_so=dropped[:100], vung_im_lang_so=sil_regions[:200],
              chen_ngoai_cau=[dict(bat_dau=round(a, 2), ket_thuc=round(b, 2), chu=w) for a, b, w in outside[:100]],
              ban_nghe_toan_file=full_text.strip()[:4000], doan_toan_file=full_segs[:200],
              mo_hinh=f"{MODEL_REPO}@{MODEL_REVISION}")
    return result("J1", None, ms, notes, evidence=ev)
