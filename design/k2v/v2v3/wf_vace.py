"""NC-V2V3 · CHẠY TRÊN POD: dựng đồ thị ComfyUI (dạng API) cho Wan2.2-VACE-Fun-A14B (fp8, hai chuyên gia nhiễu cao/thấp) rồi gửi tới ComfyUI 127.0.0.1:8188, chờ xong.
Chỉ thư viện chuẩn. Một lượt = một cửa sổ ≤ 81 khung (giới hạn huấn luyện của Wan); nối 10 s ở bước khác (noi_cua_so).
  python3 wf_vace.py <job.json>
job.json: {"w":1280,"h":720,"n":81,"start":0,"seed":..,"steps":20,"split":10,"cfg":3.5,"shift":8.0,"sampler":"euler","sched":"simple",
           "pos":"…","neg":"…", ["init_dir":"/w/ctrl/<clip>/src", "denoise":0.6,]"ctrl":[{"dir":"/w/…/depth","strength":1.0,"mask_dir":null|"/w/…/m"}, …], "out":"/w/ra/<nhãn>"}
Điều khiển nhiều lớp: mỗi lớp một nút WanVaceToVideo nối tiếp (ComfyUI gắn thêm vace_frames/vace_mask/vace_strength, append=True).
Mặt nạ: trắng (1) = AI vẽ; đen (0) = giữ điểm ảnh ở khung điều khiển (WanVaceToVideo: inactive = ctrl·(1−m), reactive = ctrl·m)."""
import json, sys, time, urllib.request

U = 'http://127.0.0.1:8188'
HI = 'wan2.2_fun_vace_high_noise_14B_fp8_scaled.safetensors'; LO = 'wan2.2_fun_vace_low_noise_14B_fp8_scaled.safetensors'
TE = 'umt5_xxl_fp8_e4m3fn_scaled.safetensors'; VAE = 'wan_2.1_vae.safetensors'


def graph(j):
    g = {'hi': {'class_type': 'UNETLoader', 'inputs': {'unet_name': HI, 'weight_dtype': 'default'}},
         'lo': {'class_type': 'UNETLoader', 'inputs': {'unet_name': LO, 'weight_dtype': 'default'}},
         'te': {'class_type': 'CLIPLoader', 'inputs': {'clip_name': TE, 'type': 'wan', 'device': 'default'}},
         'vae': {'class_type': 'VAELoader', 'inputs': {'vae_name': VAE}},
         'pos': {'class_type': 'CLIPTextEncode', 'inputs': {'text': j['pos'], 'clip': ['te', 0]}},
         'neg': {'class_type': 'CLIPTextEncode', 'inputs': {'text': j['neg'], 'clip': ['te', 0]}},
         'mhi': {'class_type': 'ModelSamplingSD3', 'inputs': {'model': ['hi', 0], 'shift': j.get('shift', 8.0)}},
         'mlo': {'class_type': 'ModelSamplingSD3', 'inputs': {'model': ['lo', 0], 'shift': j.get('shift', 8.0)}}}
    p, n = ['pos', 0], ['neg', 0]
    for i, c in enumerate(j['ctrl']):
        g[f'c{i}'] = {'class_type': 'V2V3LoadFrames', 'inputs': {'dir': c['dir'], 'start': j.get('start', 0), 'count': j['n']}}
        inp = {'positive': p, 'negative': n, 'vae': ['vae', 0], 'width': j['w'], 'height': j['h'], 'length': j['n'], 'batch_size': 1,
               'strength': c.get('strength', 1.0), 'control_video': [f'c{i}', 0]}
        if c.get('mask_dir'):
            g[f'm{i}'] = {'class_type': 'V2V3LoadFrames', 'inputs': {'dir': c['mask_dir'], 'start': j.get('start', 0), 'count': j['n']}}
            inp['control_masks'] = [f'm{i}', 1]
        g[f'v{i}'] = {'class_type': 'WanVaceToVideo', 'inputs': inp}; p, n = [f'v{i}', 0], [f'v{i}', 1]
    lat = [f'v{len(j["ctrl"]) - 1}', 2]
    S, sp = j.get('steps', 20), j.get('split', 10); s0 = 0
    if j.get('init_dir'):   # B2: khởi từ khung NGUỒN (VAE mã hoá) + nhiễu tới bước s0 = round(S·(1 − denoise)) — giữ màu/ngữ nghĩa vùng (đất vẫn là đất), AI chỉ thêm bề mặt
        g['ini'] = {'class_type': 'V2V3LoadFrames', 'inputs': {'dir': j['init_dir'], 'start': j.get('start', 0), 'count': j['n']}}
        g['enc'] = {'class_type': 'VAEEncode', 'inputs': {'pixels': ['ini', 0], 'vae': ['vae', 0]}}; lat = ['enc', 0]; s0 = int(round(S * (1 - j.get('denoise', 1.0))))
    g['k1'] = {'class_type': 'KSamplerAdvanced', 'inputs': {'model': ['mhi', 0], 'add_noise': 'enable', 'noise_seed': j['seed'], 'steps': S, 'cfg': j.get('cfg', 3.5),
               'sampler_name': j.get('sampler', 'euler'), 'scheduler': j.get('sched', 'simple'), 'positive': p, 'negative': n, 'latent_image': lat,
               'start_at_step': s0, 'end_at_step': sp, 'return_with_leftover_noise': 'enable'}}
    g['k2'] = {'class_type': 'KSamplerAdvanced', 'inputs': {'model': ['mlo', 0], 'add_noise': 'disable', 'noise_seed': j['seed'], 'steps': S, 'cfg': j.get('cfg', 3.5),
               'sampler_name': j.get('sampler', 'euler'), 'scheduler': j.get('sched', 'simple'), 'positive': p, 'negative': n, 'latent_image': ['k1', 0],
               'start_at_step': sp, 'end_at_step': 10000, 'return_with_leftover_noise': 'disable'}}
    g['dec'] = {'class_type': 'VAEDecode', 'inputs': {'samples': ['k2', 0], 'vae': ['vae', 0]}}
    g['save'] = {'class_type': 'V2V3SaveFrames', 'inputs': {'images': ['dec', 0], 'dir': j['out']}}
    return g


def call(path, body=None):
    r = urllib.request.Request(U + path, data=json.dumps(body).encode() if body is not None else None, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(r, timeout=60) as f: return json.loads(f.read())


if __name__ == '__main__':
    j = json.load(open(sys.argv[1])); t0 = time.time()
    pid = call('/prompt', {'prompt': graph(j)})['prompt_id']; print('PROMPT', pid, flush=True)
    while True:
        time.sleep(5); h = call('/history/' + pid)
        if pid in h:
            st = h[pid].get('status', {}); dt = time.time() - t0
            print(json.dumps({'xong': st.get('completed'), 'trang_thai': st.get('status_str'), 's': round(dt, 1), 's_khung': round(dt / j['n'], 2),
                              'msg': [m for m in st.get('messages', []) if m[0] in ('execution_error',)]}, ensure_ascii=False)[:3000], flush=True)
            sys.exit(0 if st.get('status_str') == 'success' else 1)
