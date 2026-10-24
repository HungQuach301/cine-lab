#!/opt/cine/bin/python
"""THU-B-T4 · hàng đợi dựng (P tiến trình, chờ RAM ≥ 5 GB trước mỗi việc, bỏ qua việc đã có đầu ra) → $THUB/r/<việc>/ (+ <việc>.log).
  dung.py <P> <nhóm …>     nhóm: b0 (V2 + mặt nạ + bóng khung B), btl (timelapse V2 khung B), id (kiểm look3 ≡ look2), d0 (D khung tĩnh), dtl (D timelapse), d2 (D + vân nướng),
                                 bp:<khung>:<tag> (chiếu ảnh AI — khung 0 1080p + timelapse), m2:<khung> (mặt nạ khung D)
Máy gốc: channel-k2/k2c-t4-02/thu-b/may/<khung>.json; bản dẫn xuất (cờ khung: bong, d, d2, proj; trang; hình học) ghi ở $THUB/may/<việc>.json (tất định, tái tạo bằng lệnh này)."""
import copy, json, os, subprocess, sys, time
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
THUB = os.environ.get('THUB', '/var/tmp/ldn/thub'); D = os.environ.get('LDN_DATA', '/var/tmp/ldn')
MAY = os.path.join(REPO, 'channel-k2/k2c-t4-02/thu-b/may'); os.makedirs(f'{THUB}/may', exist_ok=True); os.makedirs(f'{THUB}/r', exist_ok=True)
B = ['M1-trung', 'M4-trung', 'B3-p4-1938']; DK = ['M1-rong-hep', 'M4-rong-hep']
BAKE = {'1666': '1666.6', '2026': '2026.7', '1938': '1938.7'}


def job(name, base, page='look2', lk='look2/', key=None, top=None, spp=None, png=True, mask=None, fac=None):
    sh = json.load(open(os.path.join(MAY, base + '.json')))
    for k in sh['keys']: k.update(key or {})
    sh.update(top or {})
    if lk != 'look2/' and 'bake' in sh: sh['bake']['url'] = sh['bake']['url'].replace('/look2/', '/' + lk)
    p = f'{THUB}/may/{name}.json'; json.dump(sh, open(p, 'w'), ensure_ascii=False, indent=1)
    cmd = ['node', os.path.join(REPO, 'scripts/k2ldn/thu-b/render_thub.js'), '--shot', p, '--out', f'{THUB}/r/{name}', '--page', page, '--lk', lk]
    if spp: cmd += ['--spp', str(spp)]
    if mask: cmd += ['--mask', str(mask)]
    elif png: cmd += ['--png', '1']
    if fac: cmd += ['--fac', fac]
    n = max(1, round(sh.get('dur', 0.0417) * sh.get('fps', 24)))
    return name, cmd, n


def nhom(g):
    J = []
    if g == 'b0':
        for f in B:
            J.append(job(f'{f}-v2', f))
            if f.startswith('M1'): J.append(job(f'{f}-v2-kk', f + '-khongkhoi'))
            for mk in (1, 3, 4, 6): J.append(job(f'{f}-m{mk}', f, 'thu-b/look3', 'look3b/', mask=mk))
            J.append(job(f'{f}-bong', f, 'thu-b/look3', 'look3b/', key={'bong': True, 'chim': False}))
    elif g == 'btl':
        for f in B:
            J.append(job(f'tl-{f}-v2', 'tl-' + f))
            if f.startswith('M1'): J.append(job(f'tl-{f}-v2-kk', 'tl-' + f + '-khongkhoi'))
    elif g == 'id':
        J.append(job('M4-trung-l3id', 'M4-trung', 'thu-b/look3', 'look3b/', top={'W': 640, 'H': 360}))
        J.append(job('M4-trung-l2id', 'M4-trung', top={'W': 640, 'H': 360}))
    elif g == 'd0':
        for f in DK:
            J.append(job(f'{f}-v2', f, png=False)); J.append(job(f'{f}-m1', f, 'thu-b/look3', 'look3b/', mask=1))
            J.append(job(f'{f}-d', f, 'thu-b/look3', 'look3d/', key={'d': True}, png=False)); J.append(job(f'{f}-dm1', f, 'thu-b/look3', 'look3d/', mask=1))
    elif g == 'dtl':
        J.append(job('tl-M1-rong-hep-v2', 'tl-M1-rong-hep', png=False)); J.append(job('tl-M1-rong-hep-d', 'tl-M1-rong-hep', 'thu-b/look3', 'look3d/', key={'d': True}, png=False))
    elif g == 'd2':
        fac = f'{THUB}/fac/fac.json'
        for f in DK: J.append(job(f'{f}-d2', f, 'thu-b/look3', 'look3d/', key={'d': True, 'd2': True}, png=False, fac=fac))
        J.append(job('tl-M1-rong-hep-d2', 'tl-M1-rong-hep', 'thu-b/look3', 'look3d/', key={'d': True, 'd2': True}, png=False, fac=fac))
    elif g == 'uoc':
        for f in sorted(x[:-5] for x in os.listdir(MAY) if x.startswith('uoc-')):
            J.append(job(f'{f}-v2', f, spp=8))
            for mk in (1, 3, 4): J.append(job(f'{f}-m{mk}', f, 'thu-b/look3', 'look3b/', mask=mk))
            J.append(job(f'{f}-bong', f, 'thu-b/look3', 'look3b/', key={'bong': True, 'chim': False}, spp=8))
    elif g.startswith('bp:'):
        _, f, tag = g.split(':'); pj = json.load(open(f'{THUB}/bp/{f}/{tag}/proj.json'))
        pr = {'proj': {'url': f'/data/thub/bp/{f}/{tag}/proj.png', 'vp': pj['vp']}}
        J.append(job(f'{f}-bp-{tag}', f, 'thu-b/look3', 'look3b/', key=pr))
        J.append(job(f'tl-{f}-bp-{tag}', 'tl-' + f, 'thu-b/look3', 'look3b/', key=pr))
    elif g.startswith('bp0:'):
        _, f, tag = g.split(':'); pj = json.load(open(f'{THUB}/bp/{f}/{tag}/proj.json'))
        J.append(job(f'{f}-bp-{tag}', f, 'thu-b/look3', 'look3b/', key={'proj': {'url': f'/data/thub/bp/{f}/{tag}/proj.png', 'vp': pj['vp']}}))
    elif g == 'tl30':
        J.append(job('tl30-M1-trung-v2', 'tl30-M1-trung')); J.append(job('tl30-M1-trung-v2-kk', 'tl30-M1-trung-khongkhoi'))
    elif g.startswith('bp360:'):
        _, f, tag = g.split(':'); pj = json.load(open(f'{THUB}/bp/{f}/{tag}/proj.json'))
        J.append(job(f'{f}-bp360-{tag}', f, 'thu-b/look3', 'look3b/', key={'proj': {'url': f'/data/thub/bp/{f}/{tag}/proj.png', 'vp': pj['vp']}}, top={'W': 640, 'H': 360}, spp=4))
    elif g.startswith('bptl:'):
        _, f, tag = g.split(':'); pj = json.load(open(f'{THUB}/bp/{f}/{tag}/proj.json'))
        J.append(job(f'tl-{f}-bp-{tag}', 'tl-' + f, 'thu-b/look3', 'look3b/', key={'proj': {'url': f'/data/thub/bp/{f}/{tag}/proj.png', 'vp': pj['vp']}}))
    return J


def xong(name, n):
    d = f'{THUB}/r/{name}'
    return os.path.exists(f'{d}/log.json') and len([x for x in os.listdir(d) if x[:5].isdigit()]) >= n


def ram(): return int(open('/proc/meminfo').read().split('MemAvailable:')[1].split()[0]) // 1024


def main():
    P = int(sys.argv[1]); J = [j for g in sys.argv[2:] for j in nhom(g)]; run = []
    env = dict(os.environ, LDN_DATA=D)
    for name, cmd, n in J:
        if xong(name, n): print('ĐÃ CÓ', name, flush=True); continue
        while len([r for r in run if r[1].poll() is None]) >= P: time.sleep(2)
        while ram() < 5000: time.sleep(5)
        lg = open(f'{THUB}/r/{name}.log', 'w'); t0 = time.time()
        pr = subprocess.Popen(cmd, stdout=lg, stderr=subprocess.STDOUT, env=env); run.append((name, pr, t0)); print('CHẠY', name, flush=True); time.sleep(6)
    for name, pr, t0 in run:
        pr.wait(); print('XONG' if pr.returncode == 0 else f'LỖI {pr.returncode}', name, round(time.time() - t0, 1), 's', flush=True)
    print('DUNG-XONG', flush=True)


if __name__ == '__main__': main()
