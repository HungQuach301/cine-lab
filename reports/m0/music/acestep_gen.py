"""M0 bước 4 — sinh 60 s nhạc chủ đề bằng ACE-Step 1.5 (turbo) trên CPU.
Chạy (qua peakmem để đo RSS đỉnh):
  cd /opt/acestep-src/ACE-Step-1.5 && /opt/cine/bin/python /home/user/cine-lab/reports/m0/peakmem.py \
     /home/user/cine-lab/reports/m0/raw/music-<tag>.mem.json -- \
     /opt/acestep/bin/python .../acestep_gen.py --tag <tag> [--lm 0|1] [--steps 8] [--quant int8_weight_only]
Biến môi trường bắt buộc trên máy 15 GB: ACESTEP_VAE_DECODE_CHUNK_SIZE=64 (mặc định 256 bị OOM khi giải mã VAE).
Ghi: reports/m0/music/<tag>*.flac và reports/m0/raw/music-<tag>.json."""
import argparse, json, os, sys, time
t_start = time.time()
ap = argparse.ArgumentParser()
ap.add_argument('--tag', default='theme-dit'); ap.add_argument('--lm', type=int, default=0)
ap.add_argument('--steps', type=int, default=8); ap.add_argument('--seed', type=int, default=20260926)
ap.add_argument('--duration', type=float, default=60.0); ap.add_argument('--threads', type=int, default=4)
ap.add_argument('--quant', default=None)  # None | int8_weight_only
a = ap.parse_args()
import torch
torch.set_num_threads(a.threads)
ROOT = '/opt/acestep-src/ACE-Step-1.5'; sys.path.insert(0, ROOT); os.chdir(ROOT)
from acestep.handler import AceStepHandler
from acestep.llm_inference import LLMHandler
from acestep.inference import GenerationParams, GenerationConfig, generate_music

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(OUT, '..', 'raw')
CAPTION = ("Quiet cinematic theme for an animated short film. Solo felt piano with soft sustained strings and a "
           "distant celesta. Sad, still and tender at first, slowly opening into a small, warm feeling of hope. "
           "Slow tempo, sparse, intimate, lots of space, no drums, no vocals.")

t0 = time.time()
dit = AceStepHandler()
msg, ok = dit.initialize_service(project_root=ROOT, config_path='acestep-v15-turbo', device='cpu', quantization=a.quant)
dit_load = time.time() - t0
llm = LLMHandler(); lm_load = 0.0
if a.lm:
    t1 = time.time()
    msg2, ok2 = llm.initialize(checkpoint_dir=os.path.join(ROOT, 'checkpoints'), lm_model_path='acestep-5Hz-lm-1.7B',
                               backend='pt', device='cpu')
    lm_load = time.time() - t1
    print('LM init:', ok2, msg2[:300] if isinstance(msg2, str) else msg2, flush=True)
params = GenerationParams(caption=CAPTION, lyrics='[Instrumental]', instrumental=True, bpm=66, keyscale='D minor',
                          timesignature='4', duration=a.duration, inference_steps=a.steps, shift=3.0, seed=a.seed,
                          thinking=bool(a.lm), use_cot_caption=False, use_cot_language=False)
cfg = GenerationConfig(batch_size=1, use_random_seed=False, seeds=[a.seed], audio_format='flac')
t2 = time.time()
res = generate_music(dit, llm, params, cfg, save_dir=OUT)
gen_s = time.time() - t2
files = []
if res.success:
    for i, au in enumerate(res.audios):
        dst = os.path.join(OUT, f'{a.tag}-{i + 1}.flac'); os.replace(au['path'], dst); files.append(os.path.relpath(dst, OUT))
rec = {'tag': a.tag, 'model': 'acestep-v15-turbo' + (' + 5Hz-lm-1.7B (pt)' if a.lm else ' (DiT only)'), 'quant': a.quant,
       'device': 'cpu', 'threads': a.threads, 'steps': a.steps, 'duration_req_s': a.duration, 'seed': a.seed,
       'caption': CAPTION, 'init_msg': str(msg)[:500], 'dit_load_s': round(dit_load, 1), 'lm_load_s': round(lm_load, 1),
       'generate_s': round(gen_s, 1), 'total_s': round(time.time() - t_start, 1), 'success': res.success,
       'error': getattr(res, 'error', None), 'files': files, 'torch': torch.__version__}
print(json.dumps(rec, ensure_ascii=False, indent=1))
json.dump(rec, open(os.path.join(RAW, f'music-{a.tag}.json'), 'w'), indent=1, ensure_ascii=False)
