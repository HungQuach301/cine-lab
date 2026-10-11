#!/opt/cine/bin/python
"""Người "nghe" mù giọng (API). GIỚI HẠN: API Claude không nhận âm thanh → người chấm chỉ thấy phiếu đặc trưng đo được
(tốc độ, khoảng lặng, cao độ, độ ồn, bản ASR) + ảnh phổ/cao độ của 3 mẫu ẩn danh A/B/C. Không phải nghe thật."""
import json, os, re, subprocess, sys, tempfile, base64
from pathlib import Path
H = Path(__file__).resolve().parent; sys.path.insert(0, str(H.parent)); import ai
D = json.load(open(H / 'do-mau.json'))
feat = {k: {x: v for x, v in D[k].items() if x not in ('wer_raw',)} for k in D}
P = {"L1": "You are a documentary narration casting director.", "L2": "You are an audio engineer who preps voice-over for YouTube explainers.",
     "L3": "You are a viewer who watches 15-minute economics explainers and drops videos whose narrator sounds salesy or robotic."}
Q = """{p}
You CANNOT hear audio. You get, for three anonymous synthetic narration takes (A, B, C) of the same 277-character opening of a steel-economics documentary, measured features and an ASR transcript, plus image files (spectrogram + pitch contour) in your working directory — read them with your Read tool: {imgs}
Measured features (wpm = words per minute over speech span; pitch range in semitones p5–p95; LUFS before mastering):
{feat}
The episode script is 2,586 words and must land at 14–18 minutes (needs >= 144 wpm).
Judge, from this evidence only, each take on: clarity (1-10), trustworthy/not-salesy (1-10), fit for a calm, sourced economics documentary (1-10), and say what the evidence cannot tell you. Return ONLY JSON:
{{"A": {{"clarity": n, "trust": n, "fit": n, "why": "..."}}, "B": {{...}}, "C": {{...}}, "pick": "A|B|C", "pick_why": "...", "cannot_tell": "..."}}"""
if __name__ == '__main__':
    imgs = ', '.join(f'mau-{k}.png' for k in 'ABC'); F = [H / f'mau-{k}.png' for k in 'ABC']
    out = {}
    for k, p in P.items():
        out[k] = ai.ai(Q.format(p=p, imgs=imgs, feat=json.dumps(feat, indent=1)), f'giong-{k}', 'claude-sonnet-5-5', files=F)
        print(k, json.dumps(out[k], ensure_ascii=False))
    json.dump(out, open(H / 'nghe-mu.json', 'w'), indent=1, ensure_ascii=False)
