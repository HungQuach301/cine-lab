#!/opt/cine/bin/python
"""KÊNH 2 · dựng SHOT MẪU độc lập cho module hình k2v (không cần lời/ElevenLabs): cảnh 3D (scripts/k2/hero.js) → lớp chữ 2D (scripts/k2/render.js,
mẫu `plate` của scripts/k2/lib/k2.js: places, tags, cap, src, asof) → mp4 1080p + tờ khung + số đo s/khung.
Đặc tả = định dạng episode của kênh 2 (để chạy được luật K: checks/ll/q_types.py, q_scene.py, q_footage.py trên <out>/timeline.json):

  id: k2v-mau-a
  out: /var/tmp/cine-out/k2v-shots/k2v-mau-a
  heroes: {a_pair: {hero: map/globe, cam: <preset scripts/k2/cams.yaml> | opt.cam, opt: {...}}}
  places: [...], people: [...], anchors: [...]          # khai báo cấp tập theo luật K Q34
  segments:
    - id: A
      dur: 12
      shots:
        - {tpl: plate, at: 0, type: map, scene_id: map/globe, camera_id: pair, places: [...], people: [...], in: fade, p: {hero: a_pair, places: [...], tags: [...], cap: [...], src: ...}}

  vshot.py <spec.yaml> [--spp 4] [--draft] [--measure N]   (--measure N: chỉ đo s/khung trên N khung, không ghép)
Ra: <out>/{shot.mp4, timeline.json, f*.jpg, measure-*.json}. type/scene_id/camera_id thiếu thì suy bằng scripts/k2/prep.py (cùng luật chặn lặp).
"""
import json, os, subprocess, sys, time, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep  # noqa: E402

REPO = prep.REPO
FPS = 24


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def main():
    E = yaml.safe_load(open(sys.argv[1])); sid = E['id']; out = E.get('out') or f'/var/tmp/cine-out/k2v-shots/{sid}'; os.makedirs(out, exist_ok=True)
    cnt, where, bad = prep.repeat_check(E)
    if bad: sys.exit(f'LẶP GÓC MÁY: {bad}')
    spp = int(arg('spp', E.get('spp', 4))); draft = '--draft' in sys.argv; meas = int(arg('measure', 0))
    W, H = (960, 540) if draft else (1920, 1080)
    TL = dict(id=sid, title=E.get('title'), segments=[], shorts=[], heroes={}); M = []; t_abs = 0.0; gi = 0; JOBS = []
    par = int(arg('par', 1))   # V2: --par N dựng N cảnh 3D song song (đo giờ máy: ghi cả đồng hồ thật)
    for sg in E['segments']:
        dur = float(sg['dur']); frames = int(round(dur * FPS)); ats = [float(s.get('at', 0)) for s in sg['shots']]; shots = []
        for i, sh in enumerate(sg['shots']):
            t0, t1 = ats[i], (ats[i + 1] if i + 1 < len(ats) else dur); k = sh['p']['hero']; h = E['heroes'][k]
            hdir = os.path.join(out, f'hero{gi}-{"d" if draft else "f"}-spp{spp}'); gi += 1; hd = round(t1 - t0 + 0.5, 2)
            # T2 G1b: shot bắt đầu giữa cảnh (p.frame0, speed) — trước đây vshot bỏ qua frame0 (lớp 2D đọc p.off) nên cảnh 3D luôn chạy từ giây 0, lệch với chữ/mốc.
            # Nay: dựng đúng các khung frame0 … frame0 + (t1 − t0)·speed·24 (+12), lớp 2D đọc từ khung frame0 (p.off).
            f0 = int(sh['p'].get('frame0', sh['p'].get('off', 0)) or 0); nneed = int(-(-(t1 - t0) * float(sh['p'].get('speed', 1)) * FPS // 1)) + 12
            if f0 or float(sh['p'].get('speed', 1)) != 1: hd = round((f0 + nneed) / FPS, 3)
            cmd = ['node', os.path.join(REPO, 'scripts/k2/hero.js'), '--hero', h['hero'], '--variant', h.get('variant', 'a'), '--dur', str(hd),
                   '--w', str(W), '--h', str(H), '--spp', str(spp), '--opt', json.dumps(h.get('opt', {})), '--out', hdir]
            if meas: cmd += ['--only', ','.join(str(f) for f in range(0, int(hd * FPS), max(1, int(hd * FPS) // meas)))]
            elif f0: cmd += ['--only', ','.join(str(f) for f in range(f0, f0 + nneed))]
            st = prep.hashlib.sha1((prep.code_bytes() + json.dumps([h['hero'], h.get('opt', {}), hd, W, H, spp, f0], sort_keys=True).encode())).hexdigest()[:12]
            sf = os.path.join(hdir, 'vshot.stamp'); fresh = os.path.exists(os.path.join(hdir, 'meta.json')) and open(sf).read() == st if os.path.exists(sf) else False
            if meas or not fresh:
                if not meas and os.path.isdir(hdir) and not os.path.exists(sf) and os.path.exists(os.path.join(hdir, 'meta.json')) and '--keep' in sys.argv: fresh = True   # khung dựng trước khi có stamp
            if meas or not fresh: JOBS.append((cmd, None if meas else (sf, st), f'{sg["id"]}/{i}'))
            MT = prep.shot_meta(E, sh); M.append(dict(seg=sg['id'], shot=i, hero=h['hero'], type=MT['type'], w=W, h=H, spp=spp, _dir=hdir))
            p = dict(sh['p']); p['dir'] = hdir; p['stamp'] = 'vshot'
            if 'frame0' in p: p['off'] = p.pop('frame0')   # lớp 2D (k2.js plateX) đọc p.off
            shots.append(dict(tpl=sh.get('tpl', 'plate'), t0=t0, t1=t1, p=p, **({'in': {'type': sh.get('in', 'cut'), 'd': 0.7}} if i else {}), **MT))
            TL['heroes'][k] = dict(hero=h['hero'], variant=h.get('variant', 'a'), opt=h.get('opt', {}), dur=hd, size=[W, H], dir=hdir, stamp='vshot')
        TL['segments'].append(dict(id=sg['id'], part=sg.get('part', 'BODY'), t0=round(t_abs, 4), t1=round(t_abs + dur, 4), frames=frames, vo_file=None, vo_offset=0, vo_len=0,
                                   speech=[], shots=shots, sfx=[], fadeIn=sg.get('fadeIn', 6), fadeOut=sg.get('fadeOut', 6)))
        t_abs += dur
    t_wall = time.time()
    # V3 (E6d): --chunk K chia cảnh dài thành các phần ≤ K khung (--only theo khoảng), mỗi phần một tiến trình, ra thư mục con rồi gộp; xếp việc dài trước (LPT)
    chunk = int(arg('chunk', 0)); WORK = []
    for cmd, stamp, tag in JOBS:
        nfr = int(-(-float(cmd[cmd.index('--dur') + 1]) * FPS // 1)); hdir = cmd[cmd.index('--out') + 1]
        if chunk and not meas and nfr > chunk:
            k = -(-nfr // chunk); b = [round(i * nfr / k) for i in range(k + 1)]
            for i in range(k):
                c2 = list(cmd); c2[c2.index('--out') + 1] = os.path.join(hdir, f'part{i}'); c2 += ['--only', ','.join(str(f) for f in range(b[i], b[i + 1]))]
                WORK.append(dict(cmd=c2, n=b[i + 1] - b[i], tag=f'{tag}#{i}', parent=hdir))
        else: WORK.append(dict(cmd=cmd, n=nfr, tag=tag, parent=None))
    WORK.sort(key=lambda w: -w['n'])
    def run(w):
        r = subprocess.run(w['cmd'], stderr=subprocess.PIPE, text=True)
        if r.returncode: print(r.stderr[-3000:]); return f'lỗi cảnh 3D {w["tag"]}'
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max(1, par)) as ex: errs = [e for e in ex.map(run, WORK) if e]
    if errs: sys.exit('; '.join(errs))
    import glob, shutil
    for hdir in dict.fromkeys(w['parent'] for w in WORK if w['parent']):   # gộp các phần: khung, điểm neo, meta (s/khung = TB theo số khung)
        anc, tot, sec, meta0 = {}, 0, 0.0, None
        for w in [w for w in WORK if w['parent'] == hdir]:
            pd = w['cmd'][w['cmd'].index('--out') + 1]
            for f in glob.glob(os.path.join(pd, '[0-9]' * 5 + '.jpg')): os.replace(f, os.path.join(hdir, os.path.basename(f)))
            anc.update(json.load(open(os.path.join(pd, 'anchors.json')))); m = json.load(open(os.path.join(pd, 'meta.json'))); tot += w['n']; sec += m['s_per_frame'] * w['n']; meta0 = m; shutil.rmtree(pd)
        meta0.update(s_per_frame=round(sec / max(1, tot), 2), chunks=True); json.dump(anc, open(os.path.join(hdir, 'anchors.json'), 'w')); json.dump(meta0, open(os.path.join(hdir, 'meta.json'), 'w'))
    for cmd, stamp, tag in JOBS:
        if stamp: open(stamp[0], 'w').write(stamp[1])
    if JOBS: print(json.dumps(dict(dung_canh=len(JOBS), phan=len(WORK), song_song=par, chunk=chunk, dong_ho_s=round(time.time() - t_wall, 1))), file=sys.stderr)
    for m in M:
        meta = json.load(open(os.path.join(m.pop('_dir'), 'meta.json'))); m.update(s_per_frame=meta['s_per_frame'], frames=meta['frames'])
    TL['tong_s'] = round(t_abs, 4); TL['tong_khung'] = sum(s['frames'] for s in TL['segments'])
    json.dump(M, open(os.path.join(out, f'measure-spp{spp}{"-d" if draft else ""}.json'), 'w'), indent=1)
    print(json.dumps(M, ensure_ascii=False))
    if meas: return
    tl = os.path.join(out, 'timeline.json'); json.dump(TL, open(tl, 'w'), indent=1, ensure_ascii=False)
    parts = []
    for sg in TL['segments']:
        mkv = os.path.join(out, f'seg-{sg["id"]}.mkv')
        r = subprocess.run(['node', os.path.join(REPO, 'scripts/k2/render.js'), '--tl', tl, '--seg', sg['id'], '--out', mkv], stderr=subprocess.PIPE, text=True)
        if r.returncode: print(r.stderr[-3000:]); sys.exit('lỗi lớp 2D')
        parts.append(mkv)
    mp4 = os.path.join(out, 'shot.mp4'); lst = os.path.join(out, 'parts.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24', '-movflags', '+faststart', mp4], check=True)
    for f in os.listdir(out):
        if f.startswith('f') and f.endswith('.jpg'): os.remove(os.path.join(out, f))
    picks = sorted(set([int(TL['tong_khung'] * k / 6) for k in range(6)] + [int(round((sg['t0'] + s['t1']) * FPS)) - 3 for sg in TL['segments'] for s in sg['shots']]))
    for f in picks:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-vf', f'select=eq(n\\,{f})', '-vframes', '1', '-q:v', '2', os.path.join(out, f'f{f:05d}.jpg')], check=True)
    small = low = 0; s2d = []
    for p in parts:
        lg = json.load(open(p + '.log.json')); s2d.append(lg['s_per_frame'])
        small += sum(1 for e in lg.get('text', []) for x in e['items'] if x['cap'] < 21.8); low += sum(1 for e in lg.get('text', []) for x in e['items'] if x['ratio'] < 4.5)
    print(json.dumps(dict(mp4=mp4, frames=TL['tong_khung'], s_per_frame_2d=s2d, chu_nho=small, tuong_phan_thap=low), ensure_ascii=False))


if __name__ == '__main__':
    main()
