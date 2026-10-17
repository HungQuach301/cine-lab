"""V5b-2b · ĐO một tập/đoạn kênh 2 có cảnh tl (dựng qua scripts/k2/build.sh) — số liệu cho checks 1.13 + tự rà (bài học T2 TT3):
  1. mặt nạ MỌI khung của mỗi cảnh tl (scripts/k2tl/render.js --maskonly, cùng opt của shot) → theo khung TOÀN ĐOẠN: content_pct, fabric_pct, hero_pct, ghost_pct, noi, nam_khung;
  2. AGL mỗi khung (meta.json frames_meta của hero.js), SPP theo pha;
  3. chuẩn hình MAU1 (measure_look: bão hoà, colorfulness, chi tiết, cháy) mỗi 1 s trên khung KHÔNG chữ (plate) + BC1 (nội dung ≥ 30 %);
  4. lửa đỏ % khung (luật hình chiến tranh §6.2: ≤ 15 %) mỗi 0,5 s trên master; người A-lite trong vùng khói (phải 0);
  5. log chữ từ sec/*.log.json: vai (role), độ đục, nhãn nguồn ghost hiện liền ≥ 3 s từ lần ghost đầu, chip nơi mỗi shot;
  6. neo: mỗi khung cảnh có anchors.json (kiem_neo); tờ khung mỗi 1 s (JPG ≤ 4 MB).
Dùng: k2_measure.py <thư mục out của tập> <thư mục ra trong repo> [--no-mask]"""
import argparse, glob, gzip, json, os, subprocess, sys
from pathlib import Path
import cv2, numpy as np
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE)); import measure_look  # noqa: E402
from tl_bundle import gz  # noqa: E402
FPS = 24


def run_mask(scene, opt, n, out):
    if out.exists(): return json.load(open(out))
    r = subprocess.run(['node', str(HERE / 'render.js'), '--scene', scene, '--pack', opt.get('pack', 'gib'), '--opt', json.dumps(opt), '--w', '1920', '--h', '1080', '--from', '0', '--to', str(n), '--maskonly', str(out)],
                       cwd=ROOT, capture_output=True, text=True, env=dict(os.environ))
    if r.returncode: raise SystemExit('mặt nạ lỗi ' + scene + ': ' + r.stderr[-1500:])
    return json.load(open(out))


def red_pct(img):   # lửa đỏ/cam bão hoà: H ∈ [0, 22]∪[170, 180] (OpenCV), S ≥ 0,55, V ≥ 0,45
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    return float((((h <= 22) | (h >= 170)) & (s >= 140) & (v >= 115)).mean() * 100)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('dst'); ap.add_argument('--no-mask', action='store_true'); a = ap.parse_args()
    O, D = Path(a.out), Path(a.dst); D.mkdir(parents=True, exist_ok=True); TL = json.load(open(O / 'timeline.json')); H = json.load(open(O / 'heroes.json'))
    tmp = Path('/var/tmp/cine-out/v5b2b-do'); tmp.mkdir(parents=True, exist_ok=True)
    masks, metas = {}, {}
    for k, h in H.items():
        if not h['hero'].startswith('tl/'): continue
        m = json.load(open(Path(h['dir']) / 'meta.json')); metas[k] = m
        if not a.no_mask: masks[k] = {r['f']: r for r in run_mask(h['hero'].split('/')[1], h['opt'], m['frames'], tmp / f'mask-{k}.json')}
    hero_of_dir = {h['dir']: k for k, h in H.items()}
    rows, noi_win = [], []
    for sg in TL['segments']:
        for sh in sg['shots']:
            p = sh['p']; k = hero_of_dir.get(p.get('dir'))
            f0, f1 = int(round((sg['t0'] + sh['t0']) * FPS)), int(round((sg['t0'] + sh['t1']) * FPS))
            noi_win.append(dict(t=[round(sg['t0'] + sh['t0'], 3), round(sg['t0'] + sh['t1'], 3)], noi=sh.get('noi') or p.get('noi'), shot=f"{sg['id']}/{sh['t0']}", where_chip=None))
            for F in range(f0, f1):
                sf = min(metas[k]['frames'] - 1, int(round(p.get('off', 0) + (F / FPS - sg['t0'] - sh['t0']) * FPS * p.get('speed', 1)))) if k else None
                r = dict(f=F, t=round(F / FPS, 3), seg=sg['id'], canh=k, f_canh=sf, noi=sh.get('noi') or p.get('noi'))
                if k:
                    fm = metas[k]['frames_meta'].get(str(sf), {}); r.update(agl_km=fm.get('agl_km'), spp=fm.get('spp'), phase=fm.get('phase'))
                    mk = masks.get(k, {}).get(sf)
                    if mk: r.update({x: mk.get(x) for x in ('content_pct', 'content_center_pct', 'fabric_pct', 'hero_pct', 'hero_id', 'ghost_pct', 'nam_khung')}, noi_canh=mk.get('noi'))
                rows.append(r)
    json.dump(rows, open(tmp / 'khung.json', 'w')); gz(tmp / 'khung.json', D / 'noi-dung-mask.json.gz')
    # chuẩn hình mỗi 1 s trên khung không chữ (plate)
    look = []
    for r in rows[::FPS]:
        if not r['canh']: continue
        pth = Path(H[r['canh']]['dir']) / f"{r['f_canh']:05d}.jpg"; mm = measure_look.measure(str(pth)); mm.update(f=r['f'], t=r['t'], content=r.get('content_pct')); look.append(mm)
    # master: lửa đỏ mỗi 0,5 s + tờ khung mỗi 1 s
    master = sorted(glob.glob(str(O / '*-master.mp4')))[-1]; reds = []; tiles = []
    dur = TL['tong_s']
    for i in range(int(dur * 2)):
        t = i / 2 + 0.25; f = tmp / f'm{i:03d}.jpg'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', master, '-frames:v', '1', '-q:v', '3', str(f)], check=True)
        im = cv2.imread(str(f)); reds.append(dict(t=t, red_pct=round(red_pct(im), 3)))
        if i % 2 == 1: tiles.append(f)
    sheet = D / 'to-khung-moi-1s.jpg'
    cols = 4; th = [cv2.resize(cv2.imread(str(f)), (480, 270), interpolation=cv2.INTER_AREA) for f in tiles]
    for j, (im, f) in enumerate(zip(th, tiles)): cv2.putText(im, f'{(j * 1 + 0.75):.2f}s', (8, 262), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    while len(th) % cols: th.append(np.zeros_like(th[0]))
    cv2.imwrite(str(sheet), np.vstack([np.hstack(th[i:i + cols]) for i in range(0, len(th), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 82])
    # log chữ
    logs = {Path(f).name.split('.')[0]: json.load(open(f)) for f in glob.glob(str(O / 'sec' / '*.log.json'))}
    roles, ghost_runs, low_alpha = {}, [], []
    for sid, L in sorted(logs.items()):
        seg = next(s for s in TL['segments'] if s['id'] == sid)
        for e in L['text']:
            t = seg['t0'] + e['f'] / FPS
            for it in e['items']: roles.setdefault(it.get('role') or '-', set()).add(round(t, 1))
            g = [it for it in e['items'] if it.get('role') == 'ghost_src']
            if g: ghost_runs.append(round(t, 3))
    gfirst = next((r['t'] for r in rows if (r.get('ghost_pct') or 0) > 0.05), None)
    # chuỗi nhãn ghost liền (mẫu mỗi 12 khung = 0,5 s): dài nhất từ lần đầu
    run = 0.0
    if ghost_runs:
        s0 = ghost_runs[0]; prev = s0
        for t in ghost_runs[1:]:
            if t - prev > 0.51: break
            prev = t
        run = round(prev - s0 + 0.5, 2)
    ag = [r['agl_km'] for r in rows if r.get('agl_km') is not None]
    def stat(k, sel=lambda r: True):
        v = [r[k] for r in rows if r.get(k) is not None and sel(r)]
        return dict(n=len(v), trung_vi=round(float(np.median(v)), 2), min=round(min(v), 2), p10=round(float(np.percentile(v, 10)), 2), max=round(max(v), 2)) if v else None
    S = dict(khung=len(rows), renderer={k: m.get('renderer') for k, m in metas.items()}, s_khung_hero={k: m.get('s_per_frame') for k, m in metas.items()},
             agl_km=dict(min=min(ag), max=max(ag), tren_50km=sum(1 for x in ag if x > 50), tren_3km=sum(1 for x in ag if x > 3)) if ag else None,
             fabric=stat('fabric_pct'), fabric_thanh_pho=stat('fabric_pct', lambda r: r['noi'] == 'thanh_pho'), content=stat('content_pct'), hero=stat('hero_pct', lambda r: r.get('hero_pct') and r.get('phase') in ('orbit', 'pin')),
             ghost=stat('ghost_pct'), ghost_lan_dau_s=gfirst, nhan_ghost_lien_s=run, nhan_ghost_dau_s=ghost_runs[0] if ghost_runs else None,
             bc1_duoi30_khung=sum(1 for r in rows if (r.get('content_pct') or 100) < 30), lua_do_max_pct=max(x['red_pct'] for x in reds), roles=sorted(roles), noi=noi_win,
             mau1=dict(n=len(look), sat_trung_vi=round(float(np.median([x['sat_med'] for x in look])), 3), colorful_trung_vi=round(float(np.median([x['colorful'] for x in look])), 1),
                       detail_trung_vi=round(float(np.median([x['detail'] for x in look])), 1), chay_max=round(max(x['clip_pct'] for x in look), 2),
                       dat_sat=sum(1 for x in look if x['sat_med'] >= 0.35), dat_colorful=sum(1 for x in look if x['colorful'] >= 35), dat_detail=sum(1 for x in look if x['detail'] >= 16)))
    neo = {}
    for k, h in H.items():
        A = json.load(open(Path(h['dir']) / 'anchors.json')); n = metas[k]['frames'] if k in metas else 0
        neo[k] = dict(khung=n, co_neo=sum(1 for f in range(n) if str(f) in A), co_lop_chu=sum(1 for f in range(n) if str(f) in A and A[str(f)].get('_tl')))
    S['neo'] = neo
    json.dump(dict(tong=S, mau1=look, lua_do=reds), open(D / 'so-do.json', 'w'), ensure_ascii=False, indent=1)
    # campath theo khung TOÀN ĐOẠN (grammarLog của từng cảnh qua render.js --campath, ánh xạ khung cảnh → khung đoạn); agl (m) như gib20
    cams = {}
    for k, h in H.items():
        if not h['hero'].startswith('tl/'): continue
        cp = tmp / f'campath-{k}.json'
        if not cp.exists(): subprocess.run(['node', str(HERE / 'render.js'), '--scene', h['hero'].split('/')[1], '--pack', h['opt'].get('pack', 'gib'), '--opt', json.dumps(h['opt']), '--campath', str(cp)], cwd=ROOT, check=True, capture_output=True)
        cams[k] = json.load(open(cp))
    cf, shots_c = [], []
    for r in rows:
        if not r['canh']: continue
        c = cams[r['canh']]['frames'][min(r['f_canh'], len(cams[r['canh']]['frames']) - 1)]
        cf.append(dict(c, f=r['f'], t=r['t'], f_canh=r['f_canh'], canh=r['canh']))
    for k, c in cams.items():
        for s0 in c.get('shots', []): shots_c.append(dict(s0, canh=k))
    json.dump(dict(frames=cf, shots=shots_c, renderer=sorted({m.get('renderer') for m in metas.values()})), open(tmp / 'campath.json', 'w')); gz(tmp / 'campath.json', D / 'campath.json.gz')
    # log chữ theo khung đoạn (render.js k2: cap = cỡ chữ hoa hiệu dụng → px1080 ≈ cap / 0,727)
    lc = []
    for sid, L in sorted(logs.items()):
        seg = next(s for s in TL['segments'] if s['id'] == sid); F0 = int(round(seg['t0'] * FPS))
        for e in L['text']: lc.append(dict(f=F0 + e['f'], text=[dict(s=it['s'], role=it.get('role') or '', px1080=round(it['cap'] / 0.727, 1), ratio=it['ratio']) for it in e['items']]))
    json.dump(dict(nguon='scripts/k2/render.js *.log.json (mẫu mỗi 12 khung)', renderer=S['renderer'], frames=lc), open(D / 'log-chu.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    bo = dict(ten='V5b-2b-T (đoạn thử T3, dây chuyền scripts/k2)', ghi_chu='Bộ timelapse V5b-2b (scripts/k2tl/k2_measure.py): khung = khung TOÀN ĐOẠN thử (master).', fps=FPS,
              campath='campath.json.gz', mat_bang='xz', mat_na='noi-dung-mask.json.gz', log_chu='log-chu.json', noi=[dict(t=w['t'], noi=w['noi']) for w in noi_win],
              nam_khung=[dict(f=r['f'], nam_max=r['nam_khung']) for r in rows if r.get('nam_khung')], ghost_lan_dau_s=gfirst,
              dia_danh=['Gibraltar', 'Bay of Gibraltar', "King's Bastion", 'Main Street'],
              tuyen=[dict(t=[0.0, 4.0], loai='song', nguon='mặt vịnh (vinh1782.js; loại "vinh" chưa có trong HH2 → khai như sông ≤ 300 m)'), dict(t=[18.0, 26.0], loai='pho', nguon='OSM Main Street (pho2026.js)')])
    json.dump(bo, open(D / 'bo-tl.json', 'w'), ensure_ascii=False)
    print(json.dumps(S, ensure_ascii=False, indent=1, default=list))


if __name__ == '__main__':
    main()
