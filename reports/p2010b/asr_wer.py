#!/opt/cine/bin/python
"""P-2010b · việc 1 bước 6: ASR (faster-whisper, như KL42: M = medium.en beam 5, S = small.en beam 1, không hotwords) trên master đã khôi phục,
từng chương (cắt theo moc.json), so chữ với loi-khoa.txt của chương → WER (khoảng cách sửa theo từ / số từ khoá). Chuẩn hoá: chữ thường, bỏ dấu câu
và dấu phụ, "%"→"percent", nối gạch nối; số giữ dạng ASR viết (năm viết số ở cả hai bên). Giải mã bằng ffmpeg (BAI-HOC #66). → asr-wer.json"""
import json, os, re, subprocess, sys, time, unicodedata
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
H = Path(__file__).resolve().parent; R = H.parents[1]; PO = Path(os.environ.get('P_OUT', '/var/tmp/cine-out/p2010b'))
W = PO / 'master/T3-loi-G1-v42-14LUFS.wav'; M = json.loads((PO / 'stem/moc.json').read_text())['chuong']
LK = (R / 'channel-k2/k2c-t3-01/loi-khoa.txt').read_text()
CH = {m.group(1): m.group(2) for m in re.finditer(r'^\[(\d\d \w+)\]\n(.*?)(?=^\[|\Z)', LK, re.S | re.M)}


def norm(t):
    t = ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn').replace('%', ' percent')
    t = re.sub(r'(\d),(\d)', r'\1\2', t); t = re.sub(r'[-–—]', ' ', t); t = re.sub(r"[^a-z0-9' ]", ' ', t).replace("'", '')
    return t.split()


def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        p, d[0] = d[0], i
        for j, h in enumerate(hyp, 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (r != h))
    return d[-1]


x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(W), '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32)
out = dict(ghi=__doc__.splitlines()[0], master=str(W.name), cach={})
for ten, mdl, beam in (('S', 'small.en', 1), ('M', 'medium.en', 5)):
    m = WhisperModel(mdl, device='cpu', compute_type='int8', cpu_threads=3); res = []; t0 = time.time()
    for c in M:
        a, b = int(max(0, c['bd_stem'] - 0.3) * 16000), int((c['bd_stem'] + c['giay'] + 0.3) * 16000)
        seg, _ = m.transcribe(x[a:b], language='en', beam_size=beam, condition_on_previous_text=False); hyp = ' '.join(s.text.strip() for s in seg)
        rf, hy = norm(CH[c['chuong']]), norm(hyp); e = wer(rf, hy)
        res.append(dict(chuong=c['chuong'], tu_khoa=len(rf), tu_asr=len(hy), sua=e, wer=round(e / len(rf), 4), asr=hyp)); print(ten, c['chuong'], len(rf), e, round(e / len(rf), 4), flush=True)
    tk, ts = sum(r['tu_khoa'] for r in res), sum(r['sua'] for r in res)
    out['cach'][ten] = dict(model=mdl, beam=beam, giay_chay=round(time.time() - t0, 1), tong_tu=tk, tong_sua=ts, wer=round(ts / tk, 4), chuong=res)
    json.dump(out, open(H / 'asr-wer.json', 'w'), ensure_ascii=False, indent=1)
print({k: (v['wer'], v['tong_sua'], v['tong_tu']) for k, v in out['cach'].items()})
