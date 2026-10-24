#!/var/tmp/cine-out/giong-t4/venv-am-vi/bin/python
"""GIONG-T4 · nhận dạng ÂM VỊ (IPA) cho đoạn tiếng — "tai thứ hai" khách quan cho tên riêng (ASR chữ hay tự sửa về chính tả).
Mô hình: facebook/wav2vec2-lv-60-espeak-cv-ft (Hugging Face; chỉ dùng để đo, không vào phim). Môi trường: venv riêng
/var/tmp/cine-out/giong-t4/venv-am-vi (torch 2.5.1 CPU, transformers 4.46.3) — không đụng /opt/cine (ghim D17).
Dùng: am_vi.py <tệp vào.json: [{"id":..,"wav":..,"bd":s,"kt":s}]> <tệp ra.json>"""
import json, sys, subprocess
import numpy as np, torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2FeatureExtractor
from huggingface_hub import hf_hub_download
M = 'facebook/wav2vec2-lv-60-espeak-cv-ft'
fe = Wav2Vec2FeatureExtractor.from_pretrained(M); mod = Wav2Vec2ForCTC.from_pretrained(M).eval()
VOC = {i: t for t, i in json.load(open(hf_hub_download(M, 'vocab.json'))).items()}   # giải mã CTC tham lam bằng vocab (không cần phonemizer)
def giai(ids):
    out, tr = [], None
    for i in ids:
        if i != tr and VOC.get(i, '<pad>') not in ('<pad>', '<s>', '</s>', '<unk>'): out.append(VOC[i])
        tr = i
    return ' '.join(out)
def doc(wav, bd, kt):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{bd:.3f}', '-to', f'{kt:.3f}', '-i', wav, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)
out = []
for it in json.load(open(sys.argv[1])):
    x = doc(it['wav'], it['bd'], it['kt'])
    with torch.no_grad(): lg = mod(fe(x, sampling_rate=16000, return_tensors='pt').input_values).logits
    it['ipa'] = giai(torch.argmax(lg, -1)[0].tolist()); out.append(it); print(it['id'], it['ipa'], flush=True)
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
