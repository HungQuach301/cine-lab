#!/opt/cine/bin/python
"""K2C-T2-01 · ƯỚC timeline trước khi thu giọng (G1b) và đo trên đặc tả:
  - lời giả lập ở tốc độ Eric 151,2 từ/phút (đo ở K2G-01) qua ll.est_timeline (cùng build_seg như prep; BAI-HOC LL #58);
  - giải mọi mốc "@từ" (shot, p.*, opt của cảnh) → giây; ghi đặc tả ĐÃ GIẢI (định dạng vshot/rhythm: segments[].dur, shots[].at số);
  - biến cố hình (beats) SINH TỪ mốc thật của đặc tả (đầu shot, nhãn/địa danh/sticker/chú thích/năm/bảng điểm/asof ở p; vùng/tuyến/vòng/cột/máy/bảng màu/đạo cụ ở opt)
    → scripts/k2/rhythm.py đo trung bình ≤ 3,5 s, khoảng dài nhất ≤ 6 s; scripts/k2/footage_share.py đo tỉ lệ footage ≤ 20 %.
  - tùy chọn --sub <đoạn/shot,…> --max <giây>: đặc tả CON (mỗi shot chọn thành một đoạn, cắt ≤ max giây) cho tờ khung 540p (vshot.py --draft).
  est.py [--out <thư mục>] [--sub 00/0,01/2:6,…] [--max 7]   (đoạn/shot[:giây bắt đầu cửa sổ trong shot])"""
import copy, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'scripts/k2')); import prep  # noqa: E402  (vá ll.load: chặn lặp góc máy)
ll = prep.ll
ll.BILL_WPS = 151.2 / 60   # Eric (K2G-01) thay cho Bill (LL)


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def words_of(sg):
    return ll.words(json.load(open(sg['vo_file'][:-4] + '.align.json'))) if sg.get('vo_file') else []


def main():
    out = arg('out', '/var/tmp/cine-out/k2c-t2-01-est'); os.makedirs(out, exist_ok=True)
    E = ll.load(os.path.join(H, 'episode.yaml')); TL = ll.est_timeline(E); HZ = E.get('heroes') or {}
    # cảnh: mốc "@từ" theo shot đầu tiên dùng cảnh
    first = {}
    for sg in TL['segments']:
        for sh in sg['shots']:
            k = (sh.get('p') or {}).get('hero')
            if k: first.setdefault(k, (sg, sh))

    def res(x, k, ctx):
        if isinstance(x, str) and re.match(r'^(\d\d)?@', x):
            sg, sh = first[k]; p = sh['p']; t = ll.anchor(x if x[0] == '@' else x[2:], words_of(sg), sg['vo_offset'], ctx)
            return round((t - sh['t0']) * p.get('speed', 1) + p.get('frame0', p.get('off', 0)) / ll.FPS, 3)
        if isinstance(x, list): return [res(v, k, ctx) for v in x]
        if isinstance(x, dict): return {kk: res(v, k, ctx) for kk, v in x.items()}
        return x
    R = {k: v for k, v in E.items() if k not in ('segments', 'heroes', 'shorts')}; R['heroes'] = {}
    for k, h in HZ.items():
        if k in first: hh = copy.deepcopy(h); hh['opt'] = res(hh.get('opt', {}), k, f'heroes.{k}.opt'); R['heroes'][k] = hh
    bad = [f"{sg['id']}/{i}" for sg in TL['segments'] for i, sh in enumerate(sg['shots']) if sh['t1'] <= sh['t0'] + 0.3]
    if bad: raise SystemExit('Shot sai thứ tự hoặc < 0,3 s (mốc "@từ" khớp nhầm lần xuất hiện? dùng #n): ' + ', '.join(bad))
    R['segments'] = []
    for sg, esg in zip(TL['segments'], E['segments']):
        dur = round(sg['t1'] - sg['t0'], 3); shots = []; beats = []
        for sh, esh in zip(sg['shots'], esg['shots']):
            p = copy.deepcopy(sh['p']); s = {kk: esh[kk] for kk in ('tpl', 'type', 'scene_id', 'camera_id', 'places', 'people', 'in') if kk in esh}
            s['at'] = round(sh['t0'], 3); s['p'] = p; shots.append(s)
        R['segments'].append(dict(id=sg['id'], part=sg.get('part'), dur=dur, shots=shots, beats=beats))
    # beats = mốc thật của đặc tả (cùng tập mốc rhythm.py đối chiếu)
    import importlib.util; _sp = importlib.util.spec_from_file_location('k2rhythm', os.path.join(REPO, 'scripts/k2/rhythm.py')); rhythm = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(rhythm)   # rhythm.py của kênh 2 (scripts/ll có module cùng tên)
    for sg in R['segments']:
        T = sorted(t for t in rhythm.spec_times(R, sg) if 0 <= t < sg['dur'])
        sg['beats'] = [dict(t=round(t, 3), k='cut' if any(abs(t - s['at']) < 1e-3 for s in sg['shots']) else 'label', s='mốc đặc tả') for t in T]
    import yaml
    rp = os.path.join(out, 'episode-resolved.yaml'); yaml.safe_dump(R, open(rp, 'w'), allow_unicode=True, sort_keys=False, width=200)
    tot = sum(s['dur'] for s in R['segments']); print(f'timeline ước: {int(tot // 60)}:{tot % 60:04.1f} ({tot:.1f} s), {sum(len(s["shots"]) for s in R["segments"])} shot → {rp}')
    for sg in R['segments']: print(f"  {sg['id']} {sg['dur']:6.1f} s  {len(sg['shots'])} shot")
    if arg('sub'):
        mx = float(arg('max', 7)); S = {k: v for k, v in R.items() if k != 'segments'}; S['id'] = 't2-tokhung'; S['out'] = '/var/tmp/cine-out/k2v-shots/t2-tokhung'; S['segments'] = []
        for key in arg('sub').split(','):
            key, _, w = key.partition(':'); sid, i = key.split('/'); sg = next(x for x in R['segments'] if x['id'] == sid); i = int(i); sh = copy.deepcopy(sg['shots'][i])
            t0 = sh['at']; t1 = sg['shots'][i + 1]['at'] if i + 1 < len(sg['shots']) else sg['dur']; win = float(w or 0)   # "04/2:36" = cửa sổ bắt đầu 36 s sau đầu shot
            a = max(t0, min(t1 - mx, t0 + win)); d = round(min(mx, t1 - a), 3)
            def shift(o):
                if isinstance(o, dict): return {kk: (round(v - a, 3) if kk in ('at', 'out', 't', 'asofAt') and isinstance(v, (int, float)) else shift(v)) for kk, v in o.items()}
                if isinstance(o, list): return [shift(v) for v in o]
                return o
            p = shift(sh['p']); p['frame0'] = int(round((a - t0) * 24 * sh['p'].get('speed', 1))) + int(sh['p'].get('frame0', 0))
            sh['p'] = p; sh['at'] = 0
            S['segments'].append(dict(id=f'{sid}-{i}' + (f'-{int(win)}' if w else ''), dur=d, shots=[sh], beats=[dict(t=0, k='cut', s='đầu shot')]))
        sp = os.path.join(H, 'g1b', 'tokhung.yaml'); os.makedirs(os.path.dirname(sp), exist_ok=True)
        yaml.safe_dump(S, open(sp, 'w'), allow_unicode=True, sort_keys=False, width=200); print('đặc tả tờ khung →', sp)
    return rp


if __name__ == '__main__':
    rp = main()
    for cmd in (['scripts/k2/rhythm.py', rp, '--json', os.path.join(H, 'g1b', 'rhythm-g1b.json')], ['scripts/k2/footage_share.py', rp, '--json', os.path.join(H, 'g1b', 'footage-g1b.json')]):
        os.makedirs(os.path.join(H, 'g1b'), exist_ok=True)
        r = subprocess.run([sys.executable, os.path.join(REPO, cmd[0])] + cmd[1:], capture_output=True, text=True, cwd=REPO); print(cmd[0], 'mã', r.returncode); print(r.stdout[-1500:], r.stderr[-800:])
