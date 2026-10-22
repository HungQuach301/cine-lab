"""SFX-T3 · soát nội dung ứng viên bằng AST AudioSet (MIT/ast-finetuned-audioset-10-10-0.4593, BSD-3; bản ONNX lượng tử hoá của Xenova),
chạy CỤC BỘ bằng onnxruntime (không gửi tiếng ra ngoài). Đặc trưng: fbank Kaldi 128 mel, 25 ms / 10 ms, cửa sổ hanning (htk_compat), tiền nhấn 0,97,
log, chuẩn (x − mean) / (2·std) như ASTFeatureExtractor; dựng lại bằng numpy (không có torch) → số có thể lệch nhẹ so với bản gốc.
  phan_loai.py <model_dir> <tệp...>  → JSON: mỗi tệp, cửa sổ 10 s bước 5 s: top-5 nhãn + điểm các nhóm "hiện đại" / "lời nói" / "nhạc".
Chỉ là CÔNG CỤ SOÁT: nhãn "hiện đại" > 0,15 ở cửa sổ nào thì ghi để tai chủ dự án kiểm; không thay tai."""
import json, sys, subprocess, numpy as np, onnxruntime as ort
SR = 16000
HIEN_DAI = ['Vehicle', 'Car', 'Motor vehicle (road)', 'Traffic noise, roadway noise', 'Engine', 'Light engine (high frequency)', 'Medium engine (mid frequency)',
            'Heavy engine (low frequency)', 'Idling', 'Accelerating, revving, vroom', 'Truck', 'Bus', 'Motorcycle', 'Aircraft', 'Aircraft engine', 'Jet engine',
            'Propeller, airscrew', 'Helicopter', 'Fixed-wing aircraft, airplane', 'Motorboat, speedboat', 'Siren', 'Car alarm', 'Telephone', 'Ringtone',
            'Train', 'Rail transport', 'Railroad car, train wagon', 'Car passing by', 'Race car, auto racing', 'Air horn, truck horn', 'Vehicle horn, car horn, honking',
            'Reversing beeps', 'Beep, bleep', 'Mechanical fan', 'Air conditioning', 'Electric toothbrush', 'Hair dryer', 'Lawn mower', 'Chainsaw', 'Power tool',
            'Drill', 'Jackhammer', 'Ship', 'Boat, Water vehicle', 'Sewing machine', 'Typing', 'Computer keyboard', 'Camera', 'Single-lens reflex camera']
LOI = ['Speech', 'Male speech, man speaking', 'Female speech, woman speaking', 'Child speech, kid speaking', 'Conversation', 'Narration, monologue', 'Babbling', 'Shout', 'Yell', 'Children shouting']
NHAC = ['Music', 'Musical instrument', 'Singing', 'Drum', 'Brass instrument', 'Marching band']

def dec(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).astype(np.float64)

def mel_fb(n_fft=512, n_mels=128, lo=20.0, hi=8000.0):
    mel = lambda f: 1127.0 * np.log(1 + f / 700.0)
    m = np.linspace(mel(lo), mel(hi), n_mels + 2); fft_mel = mel(np.arange(n_fft // 2 + 1) * SR / n_fft)
    W = np.zeros((n_mels, n_fft // 2 + 1))
    for i in range(n_mels):
        l, c, r = m[i], m[i + 1], m[i + 2]
        W[i] = np.maximum(0, np.minimum((fft_mel - l) / (c - l), (r - fft_mel) / (r - c)))
    return W

FB = mel_fb()
def fbank(x):
    x = x - x.mean(); fl, sh = 400, 160; n = 1 + (len(x) - fl) // sh
    if n < 1: x = np.pad(x, (0, fl - len(x))); n = 1
    idx = np.arange(fl)[None, :] + sh * np.arange(n)[:, None]; F = x[idx]
    F = F - F.mean(1, keepdims=True)
    F = np.concatenate([F[:, :1] - 0.97 * F[:, :1], F[:, 1:] - 0.97 * F[:, :-1]], 1)
    win = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(fl) / (fl - 1)); F = F * win   # Kaldi 'hanning' (htk_compat, như ASTFeatureExtractor)
    P = np.abs(np.fft.rfft(F, 512)) ** 2
    return np.log(np.maximum(P @ FB.T, np.finfo(np.float32).eps))

def main():
    md = sys.argv[1]; cfg = json.load(open(md + '/config.json')); lab = [cfg['id2label'][str(i)] for i in range(len(cfg['id2label']))]
    S = ort.InferenceSession(md + '/model_quantized.onnx', providers=['CPUExecutionProvider']); inp = S.get_inputs()[0].name
    ihd = [lab.index(l) for l in HIEN_DAI if l in lab]; iloi = [lab.index(l) for l in LOI if l in lab]; inh = [lab.index(l) for l in NHAC if l in lab]
    out = {}
    for p in sys.argv[2:]:
        x = dec(p); W, H = 10 * SR, 5 * SR; res = []
        for a in range(0, max(1, len(x) - W // 2), H):
            seg = x[a:a + W]
            if len(seg) < SR: break
            f = fbank(seg); f = f[:1024] if len(f) >= 1024 else np.pad(f, ((0, 1024 - len(f)), (0, 0)))
            f = (f - (-4.2677393)) / (4.5689974 * 2)
            lo = S.run(None, {inp: f[None].astype(np.float32)})[0][0]; pr = 1 / (1 + np.exp(-lo))
            top = np.argsort(-pr)[:5]
            hd = max(((lab[i], float(pr[i])) for i in ihd), key=lambda t: t[1])
            res.append(dict(t=round(a / SR, 1), top=[(lab[i], round(float(pr[i]), 3)) for i in top], hien_dai=(hd[0], round(hd[1], 3)),
                            loi=round(float(max(pr[i] for i in iloi)), 3), nhac=round(float(max(pr[i] for i in inh)), 3)))
        out[p.rsplit('/', 1)[-1]] = dict(dai_s=round(len(x) / SR, 2), cua_so=res,
                                         hien_dai_max=max(res, key=lambda r: r['hien_dai'][1])['hien_dai'] if res else None,
                                         loi_max=max((r['loi'] for r in res), default=0), nhac_max=max((r['nhac'] for r in res), default=0))
        print(p.rsplit('/', 1)[-1], out[p.rsplit('/', 1)[-1]]['hien_dai_max'], out[p.rsplit('/', 1)[-1]]['loi_max'], out[p.rsplit('/', 1)[-1]]['nhac_max'], res[0]['top'][:3] if res else '', flush=True)
    json.dump(out, open(sys.argv[0].rsplit('/', 1)[0] + '/../so-do/phan-loai-tam.json', 'w'), ensure_ascii=False, indent=0)
main()
