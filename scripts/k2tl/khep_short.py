#!/opt/cine/bin/python
"""KHEP-T3 (23/10/2026) · SHORT DỌC T3 "Gibraltar, 1704 → 2026" — k2-t3-short-S1.mp4 (1080×1920, 24 fps, H.264, −14 LUFS, ≤ −1 dBTP).
Hình = DỰNG LẠI khung dọc bằng cách A (cảnh tl/t3tl, cùng opt cảnh đinh bản cuối, cùng lightmap anim_nuong.sh, LUT kênh v0,30) từ 3 điểm máy
xương sống: D7 (eo đất + đường băng, nhìn Rock từ bắc), vịnh (từ tây bắc, phố + hạm đội), Línea (eo đất thấp, nhìn Rock). Ngày → đêm, bộ đếm năm.
Chèn pin nổi cháy 13/9/1782 cắt từ khung Cycles N2.9 của master (cắt dọc 608×1080 → phóng 1,776×). KHÔNG dùng đoạn minh hoạ AI.
Giọng = chỉ cắt câu từ master T3-loi-G1-v42-14LUFS (mốc T3-loi-moc.json), không tạo giọng mới. Nhạc = sb_intervention_nomelody (cue B1 của T3, CC BY 4.0).
SFX = gói T3 (reports/sfx-t3/ung-vien). Chữ trên hình: chỉ bộ đếm năm + phụ đề lời (cháy cứng), trong vùng an toàn Shorts (tránh 15 % dưới, 10 % phải).
Không sửa mã cảnh (design/k2v/tl) hay scripts/k2 — chỉ gọi hero.js với opt mới (cam/time/dur/nc.bakes).
  khep_short.py heroes                 → $O/heroes.json (opt từng cảnh dọc)
  khep_short.py dung <khoá> [--spp 4]  → $O/hero/<khoá>/%05d.jpg (hero.js 1080×1920; --resume khi có pending)
  khep_short.py loi                    → $O/loi.json (câu cắt từ master giọng + mốc từ bằng faster-whisper cho phụ đề)
  khep_short.py tron                   → $O/mix/mix.wav + mix.json (bước như cuoi_mix.py)
  khep_short.py ghep                   → $O/k2-t3-short-S1.mp4 + $O/chu.json (hộp chữ mọi khung)
  khep_short.py do <ra.json>           → số đo + tờ khung 9 ô"""
import copy, hashlib, json, os, subprocess, sys
import numpy as np
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
O = os.environ.get('KHEP_OUT', '/var/tmp/cine-out/khep'); os.makedirs(O, exist_ok=True)
PY = '/opt/cine/bin/python'; FPS = 24; W, H = 1080, 1920
EP = os.path.join(REPO, 'channel-k2/k2c-t3-01/cuoi/episode.yaml')
MASTER_V = os.path.join(REPO, 'channel-k2/k2c-t3-01/am-thanh/master/T3-loi-G1-v42-14LUFS.wav')
MOC = os.path.join(REPO, 'channel-k2/k2c-t3-01/am-thanh/master/T3-loi-moc.json')
LUT = os.path.join(REPO, 'channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube')
MASTER_T3 = os.environ.get('MASTER_T3', os.path.join(O, 'k2-t3-v1-master.mp4'))   # SHA-256 5b9f0bcc… (release-k2-t3-g2)
NC = {'b1704': [1300, 1779.0], 'b1900': [1783.6, 1938], 'b1940': [1938, 1946], 'b2026': [1946, 2030]}

# ---------- kịch bản Short (giây trên Short) ----------
# cảnh: khoá, nguồn opt (cảnh đinh bản cuối), [t0, t1], máy (đầu → cuối, trôi ≤ 2 %/s), mốc thời gian (như opt.time của bản cuối), lightmap
D7 = dict(p=[470, 340, 1000], l=[260, 0, -350], fov=60); D7b = dict(p=[462, 337, 985], l=[260, 0, -350], fov=60)
SHOTS = [
    dict(k='A', src='anim_H1', t=[0.0, 4.2], cam=[D7, D7b], nc=['b2026'], diem='D7 (eo đất + đường băng, nhìn Rock từ bắc)',
         time=[dict(t=0, at='2026-10-19 15:00', sun='real', lab='dt'), dict(t=4.2, at='2026-10-19 15:40', sun='real', lab='dt')]),
    dict(k='B', src='anim_H2', t=[4.2, 16.0], nc=['b1704'], diem='vịnh (từ tây bắc: phố trong tường, hạm đội, Rock)',
         cam=[dict(p=[-2500, 1000, 1500], l=[-200, 0, -1750], fov=58), dict(p=[-2440, 982, 1452], l=[-200, 0, -1750], fov=58)],
         time=[dict(t=0, at='1704-08-04 09:30', sun=10.5, lab='y'), dict(t=4.8, at='1704-08-04 15:30', sun=13.5, lab='y'),
               dict(t=4.85, at=1705.0, sun=14.5, lab='y', hold=True), dict(t=7.3, at=1705.004, sun=14.5, lab='y', hold=True),
               dict(t=7.35, at=1727.5, sun=15.5, lab='y', hold=True), dict(t=11.8, at=1727.504, sun=15.5, lab='y', hold=True)]),
    dict(k='C', cycles=True, t=[16.0, 20.3], ss=347.0, crop=[608, 1080, 760, 0], diem='Cycles N2.9 (master 347,0–351,3 s)'),
    dict(k='D', src='anim_N5_6', t=[20.3, 35.0], nc=['b1900', 'b1940'], diem='Línea (eo đất thấp, nhìn Rock từ bắc)',
         cam=[dict(p=[-200, 95, 1250], l=[70, 60, -600], fov=60), dict(t=5.98, p=[-196, 94, 1234], l=[70, 60, -600], fov=60),   # góc 1: Spanish Lines 1783 (≤ 6 s, R2)
              dict(t=6.0, p=[330, 150, 800], l=[230, -150, -600], fov=58), dict(p=[324, 148, 786], l=[230, -150, -600], fov=58)],   # góc 2: gần ranh giới — hàng rào 1909, đường băng 1941 (vật lời nhắc tới, BAI-HOC K24)
         time=[dict(t=0, at=1783.65, sun=14.0, lab='y', hold=True), dict(t=5.98, at=1783.66, sun=14.0, lab='y', hold=True),
               dict(t=6.0, at=1909.7, sun=16.0, lab='y', hold=True), dict(t=9.9, at=1909.71, sun=16.0, lab='y', hold=True),
               dict(t=9.95, at=1941.7, sun=17.2, lab='y', hold=True), dict(t=14.7, at=1941.71, sun=18.2, lab='y', hold=True)]),
    dict(k='E', src='anim_H1', t=[35.0, 48.5], cam=[D7, D7b], nc=['b2026'], diem='D7 (cùng điểm máy cảnh A — ngày → đêm)',
         time=[dict(t=0, at='2026-10-19 19:30', sun='real', lab='dt'), dict(t=13.5, at='2026-10-19 23:52', sun='real', lab='dt')]),
]
DUR = 48.5
# bộ đếm năm (chỉ năm, §12.1 + lệnh 23/10): [giây Short, chữ]
DEM = [(0.0, '2026'), (4.2, '1704'), (9.05, '1705'), (11.55, '1727'), (16.0, '1782'), (20.3, '1783'), (26.3, '1909'), (30.25, '1941'), (35.0, '2026')]
# câu cắt từ master giọng: (giây Short đặt câu, chương, mã đoạn, chữ khoá) — thứ tự chương trong T3-loi-moc.json
LOI = [(0.5, '00 HOOK', 'To walk in from Spain, you cross an airport runway.'),
       (4.7, '00 HOOK', 'The Rock sits at the western gate of the Mediterranean.'),
       (8.2, '00 HOOK', 'Historians on both sides count fourteen sieges of it, between 1309 and 1783.'),
       (16.25, '00 HOOK', 'In 1782, ten floating batteries came to break it.'),
       (20.9, '05 GATE', 'The last siege ended in 1783.'),
       (24.4, '05 GATE', "The argument didn't."),
       (27.3, '05 GATE', 'A fence in 1909.'),
       (30.7, '05 GATE', 'A runway in 1941.'),
       (36.0, '00 HOOK', 'Since July 2026, this gate has had no routine checks.'),
       (43.0, '00 HOOK', 'Midnight at the Gibraltar frontier.')]

def sha(p, n=1 << 20):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(n), b''): h.update(b)
    return h.hexdigest()

def heroes():
    import yaml
    E = yaml.safe_load(open(EP))['heroes']; out = {}
    for s in SHOTS:
        if s.get('cycles'): continue
        d = round(s['t'][1] - s['t'][0], 4); o = copy.deepcopy(E[s['src']]['opt'])
        o['cam'] = [dict(c, t=c.get('t', 0 if i == 0 else d)) for i, c in enumerate(s['cam'])]; o['time'] = copy.deepcopy(s['time']); o['dur'] = d
        o['nc'] = {'bakes': [dict(dir=b, wY=NC[b]) for b in s['nc']]}; o['shot'] = 'short-S1-' + s['k']; o.pop('td', None)
        st = hashlib.sha1(json.dumps(o, sort_keys=True, default=str).encode()).hexdigest()
        out['short_' + s['k']] = dict(hero='tl/t3tl', variant='a', dur=d, size=[W, H], dir=f"{O}/hero/short_{s['k']}", stamp=st, src=s['src'], opt=o)
    json.dump(out, open(f'{O}/heroes.json', 'w'), ensure_ascii=False, indent=1, default=str); print(json.dumps({k: [v['dur'], v['stamp'][:12]] for k, v in out.items()}))

def dung(k, spp):
    H_ = json.load(open(f'{O}/heroes.json'))[k]; d = H_['dir']
    if open(f'{d}/stamp').read().strip() == H_['stamp'] if os.path.exists(f'{d}/stamp') else False: print('giữ', k); return
    os.makedirs(d, exist_ok=True); rs = []
    if os.path.exists(f'{d}/pending') and open(f'{d}/pending').read().strip() == H_['stamp']: rs = ['--resume']
    else: subprocess.run(['bash', '-c', f'rm -f {d}/*.jpg']); open(f'{d}/pending', 'w').write(H_['stamp'])
    env = dict(os.environ, K2TL_CACHE=os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache'))
    cmd = ['node', f'{REPO}/scripts/k2/hero.js', '--hero', H_['hero'], '--variant', 'a', '--dur', str(H_['dur']), '--w', str(W), '--h', str(H),
           '--spp', str(spp), '--opt', json.dumps(H_['opt'], separators=(',', ':'), default=str), '--out', d] + rs
    r = subprocess.run(cmd, env=env)
    if r.returncode: sys.exit(r.returncode)
    open(f'{d}/stamp', 'w').write(H_['stamp']); os.remove(f'{d}/pending')

def loi():
    M = json.load(open(MOC)); L = []
    for t, ch, khoa in LOI:
        C = next(c for c in M['chuong'] if c['chuong'] == ch); cau = next(s for o in C['doan'] for s in o['cau'] if s['khoa'] == khoa)
        L.append(dict(t=t, khoa=khoa, bd_stem=round(C['bd_stem'] + cau['bd'], 3), kt_stem=round(C['bd_stem'] + cau['kt'], 3)))
    import soundfile as sf
    from faster_whisper import WhisperModel
    a, sr = sf.read(MASTER_V, dtype='float32'); a = a.mean(1) if a.ndim > 1 else a
    m = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=2)
    for x in L:
        s0 = max(0.0, x['bd_stem'] - 0.05); off = x['bd_stem'] - s0; seg = a[int(s0 * sr):int((x['kt_stem'] + 0.05) * sr)]
        import scipy.signal as ss
        y = ss.resample_poly(seg, 1, sr // 16000).astype(np.float32)
        S, _ = m.transcribe(y, language='en', word_timestamps=True, beam_size=5, initial_prompt=x['khoa'])
        wd = [dict(w=w.word.strip(), a=round(w.start - off, 3), b=round(w.end - off, 3)) for s in S for w in s.words]
        x['tu'] = wd; x['asr'] = ' '.join(w['w'] for w in wd)
    json.dump(dict(giong=dict(tep=os.path.relpath(MASTER_V, REPO), sha256=sha(MASTER_V)), cau=L), open(f'{O}/loi.json', 'w'), ensure_ascii=False, indent=1)
    for x in L: print(x['t'], x['bd_stem'], x['kt_stem'], '|', x['khoa'], '|', x['asr'])

# phụ đề: chữ KHOÁ (không phải chữ ASR) chia thẻ ≤ 2 dòng; thời điểm thẻ theo mốc từ ASR (khớp theo số từ)
def the_phu_de(L, maxch=44):
    out = []
    for x in L:
        ws = x['khoa'].split(); tu = x['tu']; n = len(ws)
        def tt(i, end=False):   # mốc của từ khoá thứ i (ánh xạ tỉ lệ khi số từ ASR khác)
            j = min(len(tu) - 1, round(i * (len(tu) - 1) / max(1, n - 1))) if tu else 0
            return x['t'] + (tu[j]['b'] if end else tu[j]['a']) if tu else x['t'] + (x['kt_stem'] - x['bd_stem']) * (i + end) / n
        L_ = len(x['khoa']); nc = -(-L_ // maxch); groups = []   # số thẻ = ⌈ký tự / maxch⌉, cắt ở ranh từ gần mốc chia đều nhất (ưu tiên sau dấu phẩy)
        cuts, pos, acc = [], [], 0
        for i, w in enumerate(ws): acc += len(w) + 1; pos.append(acc)
        for c in range(1, nc):
            tg = L_ * c / nc; cuts.append(min(range(n - 1), key=lambda i: abs(pos[i] - tg) - (6 if ws[i].endswith(',') else 0)) + 1)
        b0 = 0
        for c in sorted(set(cuts)) + [n]: groups.append(list(range(b0, c))); b0 = c
        for g in groups:
            s = ' '.join(ws[k] for k in g); out.append(dict(a=round(tt(g[0]) - 0.08, 3), b=round(tt(g[-1], True) + 0.25, 3), s=s))
    for i in range(len(out) - 1):
        if out[i + 1]['a'] - out[i]['b'] <= 0.15: out[i]['b'] = out[i + 1]['a']; out[i]['noi_sau'] = out[i + 1]['noi_truoc'] = True   # thẻ liền nhau: đổi chữ tại chỗ, không mờ (tránh nháy)
        else: out[i]['b'] = min(out[i]['b'], out[i + 1]['a'] - 0.04)
    return out

def tron():
    sys.path[:0] = [os.path.join(REPO, p) for p in ('reports/nhac-t3/cong-cu', 'scripts/audio', 'reports/sfx-t3/cong-cu', 'scripts/k2tl')]
    os.environ.setdefault('NHAC_T3_NGOAI', os.path.join(REPO, 'assets/k2/music'))
    import tron as TR, lib, master, tron_thu, cuoi_mix
    L = json.load(open(f'{O}/loi.json'))['cau']; T = DUR
    P = dict(phuong_an='B1 (cue mở đầu T3)', phim_s=T, cue=[dict(id='S1', tep='NGOAI-GIT/sb_intervention_nomelody.mp3', vao_bai=0.0, phim_vao=0.0, phim_ra=T,
             xf_vao=0.3, xf_ra=3.0, muc='mid', nhom='INT', doan='Short S1', ghi='cùng bài + đoạn với cue B1 (móc 0a–0h) của bản cuối T3')])
    bed, nlog = TR.nen(P, 0.0, T); N = len(bed)
    LL = dict(dong=[dict(bd_stem=x['bd_stem'], kt_stem=x['kt_stem'], bd_phim=x['t'], cau=True) for x in L])
    vo, sp = cuoi_mix.giong(LL, N)
    SK = [  # sự kiện SFX (mã gói T3), mức dB như gói bản cuối (tối giản dưới lời)
        dict(uv='GIO-1', t=0.0, muc=-43, dai=4.2, fi=0.8, fo=0.6), dict(uv='PHO-1', t=0.0, muc=-43, dai=4.2, fi=1.0, fo=0.6, ghi='phố 2026 ban ngày'),
        dict(uv='MAYBAY-1', t=0.6, muc=-44, dai=3.6, fi=1.0, fo=1.0, ghi='đường băng'),
        dict(uv='SONG-1', t=4.2, muc=-42, dai=11.8, fi=0.6, fo=0.8, ghi='vịnh 1704'), dict(uv='CHIM-1', t=4.4, muc=-45, dai=6.0, fi=1.0, fo=1.0),
        dict(uv='PXA-1', t=9.1, muc=-38, dai=2.5, fo=0.6, pan=-0.3, ghi='vây 1705 (pháo xa, dưới lời)'), dict(uv='PXA-3', t=11.85, muc=-40, dai=2.5, fo=0.8, pan=0.3, ghi='vây 1727 (khe lời 11,81–12,31)'),
        dict(uv='LUAL-1', t=16.0, muc=-36, dai=4.3, fi=0.3, fo=0.6, ghi='pin nổi cháy'), dict(uv='NO-1', t=16.05, muc=-31, vao=0.1, dai=4.2, lp=1800, fo=1.5, ghi='pin nổ'),
        dict(uv='GIO-2', t=20.3, muc=-43, dai=14.7, fi=0.8, fo=0.8, ghi='eo đất'), dict(uv='CO-2', t=26.8, muc=-44, dai=3.0, fi=0.4, fo=0.6, ghi='1909'),
        dict(uv='MAYBAY-1', t=30.3, muc=-40, dai=4.7, fi=0.6, fo=1.2, ghi='đường băng 1941'),
        dict(uv='PHO-3', t=35.0, muc=-43, dai=13.5, fi=0.8, fo=2.5, ghi='đêm 2026'), dict(uv='DEM-1', t=38.0, muc=-42, dai=10.5, fi=1.5, fo=2.5, ghi='đêm biên giới')]
    fx, flog = tron_thu.sfx_stem(SK, 0.0, T); fx = fx[:N] if len(fx) >= N else np.pad(fx, ((0, N - len(fx)), (0, 0)))
    spm = [tuple(x) for x in lib.merge([list(x) for x in sp], 0.55)]
    C = dict(master.DEF, fade_in=0.3, fade_out=2.0); os.makedirs(f'{O}/mix', exist_ok=True)
    R, ST = cuoi_mix.finish_stem(vo, bed, fx, spm, f'{O}/mix/mix.wav', C)
    R.update(nhac=nlog, sfx=flog, su_kien=SK, khoang_loi=spm, giong=json.load(open(f'{O}/loi.json'))['giong'])
    json.dump(R, open(f'{O}/mix/mix.json', 'w'), ensure_ascii=False, indent=0, default=str)
    print(json.dumps({k: R.get(k) for k in ('dau_ra', 'smr', 'dat')}, ensure_ascii=False))

# ---------- lớp chữ (cùng kiểu bộ đếm của scripts/k2/lib/k2.js tlLayer ở 9:16: Inter Display 700, 72 px × 1,45, tấm rgba(12,18,27,0,9) viền trắng 30 %) ----------
FD = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; FB = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
SAFE_R, SAFE_B = int(W * 0.90), int(H * 0.85)   # vùng an toàn Shorts: tránh 10 % phải, 15 % dưới
def ve_chu(t, sub):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(im); hop = []
    k = max(i for i, (a, _) in enumerate(DEM) if t >= a); a, ys = DEM[k]
    u = min(1.0, (t - a) / 0.4) if k else 1.0; c1, c3 = 1.70158, 2.70158; sc = 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2 if k else 1.0   # backOut 0,4 s như k2.js
    sc = max(sc, 0.05); px = max(4, int(round(72 * 1.45 * sc))); f = ImageFont.truetype(FD, px); tw = g.textlength(ys, font=f); w, h = tw + 52 * sc, px * 1.42
    x0, y0 = 70, 210; cx, cy = x0 + (tw + 52) / 2, y0 + 72 * 1.45 * 1.42 / 2; x, y = cx - w / 2, cy - h / 2
    g.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(12, 18, 27, 230), outline=(230, 235, 240, 77), width=2)
    g.text((x + 26 * sc, y + h / 2), ys, font=f, fill=(230, 235, 240, 255), anchor='lm'); hop.append(dict(vai='year', s=ys, box=[x, y, x + w, y + h]))
    for s in sub:
        if not (s['a'] <= t < s['b']): continue
        al = min(1.0, 1.0 if s.get('noi_truoc') else (t - s['a']) / 0.12, 1.0 if s.get('noi_sau') else (s['b'] - t) / 0.12); fs = 66; f = ImageFont.truetype(FB, fs); mw = SAFE_R - 70 - 64
        ln, cur = [], ''
        for wd in s['s'].split():
            n = (cur + ' ' + wd).strip()
            if g.textlength(n, font=f) > mw and cur: ln.append(cur); cur = wd
            else: cur = n
        ln.append(cur); lh = fs * 1.28; bw = max(g.textlength(l, font=f) for l in ln) + 64; bh = len(ln) * lh + 40
        cxm = (70 + SAFE_R) / 2; bx, by = cxm - bw / 2, 1560 - bh
        g.rounded_rectangle([bx, by, bx + bw, by + bh], radius=14, fill=(12, 18, 27, int(205 * al)))
        for i, l in enumerate(ln): g.text((cxm, by + 20 + lh * (i + 0.5)), l, font=f, fill=(255, 255, 255, int(255 * al)), anchor='mm')
        hop.append(dict(vai='phu_de', s=s['s'], box=[bx, by, bx + bw, by + bh], a=round(al, 3)))
    return im, hop

def ghep():
    from PIL import Image
    L = json.load(open(f'{O}/loi.json'))['cau']; SUB = the_phu_de(L); json.dump(SUB, open(f'{O}/phu-de.json', 'w'), ensure_ascii=False, indent=0)
    HJ = json.load(open(f'{O}/heroes.json')); NF = int(round(DUR * FPS)); log = []
    enc = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-i', f'{O}/mix/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'slow', '-crf', '17', '-maxrate', '19M', '-bufsize', '38M',
                            '-vf', 'scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p', '-color_range', 'tv', '-color_primaries', 'bt709',
                            '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-movflags', '+faststart', '-shortest', f'{O}/k2-t3-short-S1.mp4'], stdin=subprocess.PIPE)
    for s in SHOTS:
        f0, f1 = int(round(s['t'][0] * FPS)), int(round(s['t'][1] * FPS)); n = f1 - f0
        if s.get('cycles'):   # master đã mang LUT kênh → không áp lại
            cw, ch, cx, cy = s['crop']
            src = ['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', str(s['ss']), '-i', MASTER_T3, '-frames:v', str(n),
                   '-vf', f'crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.45,format=rgb24', '-f', 'rawvideo', '-']
        else:
            d = HJ['short_' + s['k']]['dir']; assert open(f'{d}/stamp').read().strip() == HJ['short_' + s['k']]['stamp'], 'cảnh chưa dựng xong ' + s['k']
            src = ['ffmpeg', '-nostdin', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{d}/%05d.jpg', '-frames:v', str(n),
                   '-vf', f'lut3d=file={LUT}:interp=tetrahedral,format=rgb24', '-f', 'rawvideo', '-']
        p = subprocess.Popen(src, stdout=subprocess.PIPE); got = 0
        for i in range(n):
            b = p.stdout.read(W * H * 3)
            if len(b) < W * H * 3: break
            fr = Image.frombuffer('RGB', (W, H), b); t = (f0 + i) / FPS; ov, hop = ve_chu(t, SUB); fr = fr.convert('RGBA'); fr.alpha_composite(ov)
            enc.stdin.write(fr.convert('RGB').tobytes()); log.append(dict(f=f0 + i, shot=s['k'], chu=hop)); got += 1
        p.wait(); assert got == n, f'thiếu khung {s["k"]}: {got}/{n}'
    enc.stdin.close(); assert enc.wait() == 0
    json.dump(dict(khung=NF, chu=log), open(f'{O}/chu.json', 'w'), separators=(',', ':'))
    print('XONG', f'{O}/k2-t3-short-S1.mp4', sha(f'{O}/k2-t3-short-S1.mp4'))

def do(ra):
    V = f'{O}/k2-t3-short-S1.mp4'
    pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', V], capture_output=True, text=True).stdout)
    v = next(s for s in pr['streams'] if s['codec_type'] == 'video'); a = next(s for s in pr['streams'] if s['codec_type'] == 'audio')
    e = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-i', V, '-map', '0:a', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]); LRA = float(re.findall(r'LRA:\s+([\d.]+) LU', e)[-1]); TP = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1])
    C = json.load(open(f'{O}/chu.json')); vi = []; nb = 0
    for k in C['chu']:
        for hp in k['chu']:
            x0, y0, x1, y1 = hp['box']; nb += 1
            if x1 > W * 0.90 + 0.5 or y1 > H * 0.85 + 0.5 or x0 < 0 or y0 < 0: vi.append(dict(f=k['f'], vai=hp['vai'], box=[round(z, 1) for z in hp['box']]))
    R = dict(tep=os.path.basename(V), sha256=sha(V), bytes=os.path.getsize(V), w=v['width'], h=v['height'], fps=v['r_frame_rate'], codec=f"{v['codec_name']} {v.get('profile')}",
             pix_fmt=v['pix_fmt'], khung=int(v.get('nb_frames', 0)), thoi_luong_s=float(pr['format']['duration']), am=f"{a['codec_name']} {a['sample_rate']} Hz {a.get('bit_rate')} b/s",
             LUFS=I, LRA=LRA, dinh_that_dBTP=TP, vung_an_toan=dict(hop_chu=nb, vi_pham=len(vi), mau=vi[:5], quy_tac='x1 ≤ 0,90 W và y1 ≤ 0,85 H'),
             cycles=dict(nguon='k2-t3-v1-master.mp4 (5b9f0bcc…)', doan_s=[347.0, 351.3], cat='608×1080 tại x = 760 (độ phân giải gốc 1920×1080)', phong=round(H / 1080, 3)))
    json.dump(R, open(ra, 'w'), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False))
    # tờ khung 9 ô: giữa mỗi nhịp chính
    ts = [1.8, 6.0, 10.5, 14.5, 18.0, 23.0, 28.0, 32.5, 44.0]
    fl = ';'.join(f'[0:v]trim=start={t}:duration=0.05,setpts=PTS-STARTPTS,scale=360:640,drawtext=fontfile={FB}:text=\'{t:.1f} s\':x=12:y=600:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.6[v{i}]' for i, t in enumerate(ts))
    fl += ';' + ''.join(f'[v{i}]' for i in range(9)) + 'xstack=inputs=9:layout=' + '|'.join(f'{(i % 3) * 360}_{(i // 3) * 640}' for i in range(9)) + '[o]'
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', V, '-filter_complex', fl, '-map', '[o]', '-frames:v', '1', '-q:v', '3', os.path.splitext(ra)[0] + '-to-khung-9.jpg'], check=True)

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'heroes': heroes()
    elif c == 'dung': dung(sys.argv[2], int(sys.argv[sys.argv.index('--spp') + 1]) if '--spp' in sys.argv else 4)
    elif c == 'loi': loi()
    elif c == 'tron': tron()
    elif c == 'ghep': ghep()
    elif c == 'do': do(sys.argv[2])
