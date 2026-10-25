#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · hàng dựng (P ≤ 2 tiến trình, chờ RAM ≥ 5 GB trước mỗi việc, bỏ qua việc đã có log.json) → $BC_R/<việc>/ (+ <việc>.log, <việc>.time.json).
Việc khai trong tệp JSON (danh sách): {ten, shot: <tệp máy .json trong git>, page: thu-b/look3|look2|look2d, lk: look3d/|look3e/|look2/, mask?, png?, spp?, w?, h?, only?, key?: {…ghi đè mọi khoá}, top?: {…}}.
Dựng bằng scripts/k2ldn/thu-b/render_thub.js (bản sao render_look.js của THU-B; không sửa). Bake của look3d/look3e: thay '/look2/' → '/look3d/' trong url bake.
  dung_bc.py <P> <viec.json> [ten …]"""
import copy, json, os, subprocess, sys, time
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
R = os.environ.get('BC_R', '/var/tmp/bc/r'); os.makedirs(R + '/may', exist_ok=True)


def ram_mb():
    for l in open('/proc/meminfo'):
        if l.startswith('MemAvailable'): return int(l.split()[1]) // 1024
    return 0


def lenh(j):
    sh = json.load(open(os.path.join(REPO, j['shot'])))
    for k in sh['keys']: k.update(j.get('key') or {})
    sh.update(j.get('top') or {})
    lk = j.get('lk', 'look2/')
    if 'bake' in sh and lk != 'look2/': sh['bake']['url'] = sh['bake']['url'].replace('/look2/', '/' + ('look3d/' if lk.startswith('look3') else lk))
    p = f"{R}/may/{j['ten']}.json"; json.dump(sh, open(p, 'w'), ensure_ascii=False, indent=1)
    c = ['node', os.path.join(REPO, 'scripts/k2ldn/thu-b/render_thub.js'), '--shot', p, '--out', f"{R}/{j['ten']}", '--page', j.get('page', 'thu-b/look3'), '--lk', lk,
         '--w', str(j.get('w', 1920)), '--h', str(j.get('h', 1080))]
    if j.get('spp'): c += ['--spp', str(j['spp'])]
    if j.get('mask'): c += ['--mask', str(j['mask'])]
    elif j.get('png'): c += ['--png', '1']
    if j.get('only') is not None: c += ['--only', ','.join(map(str, j['only']))]
    return c


def main():
    P = int(sys.argv[1]); V = json.load(open(sys.argv[2])); chon = set(sys.argv[3:])
    J = [j for j in V if not chon or j['ten'] in chon]; run = []
    for j in J:
        if os.path.exists(f"{R}/{j['ten']}/log.json"): print('ĐÃ CÓ', j['ten']); continue
        while len([p for p in run if p[0].poll() is None]) >= P: time.sleep(3)
        while ram_mb() < 5000: time.sleep(10)
        subprocess.run(['rm', '-rf', f"{R}/{j['ten']}"]); c = lenh(j)
        lg = open(f"{R}/{j['ten']}.log", 'w'); p = subprocess.Popen(c, stdout=lg, stderr=subprocess.STDOUT, env=dict(os.environ, LDN_DATA=os.environ.get('LDN_DATA', '/var/tmp/ldn')))
        run.append((p, j, time.time())); print('CHẠY', j['ten'], time.strftime('%H:%M:%S'), flush=True); time.sleep(5)
    for p, j, t0 in run:
        rc = p.wait(); w = time.time() - t0
        try: lj = json.load(open(f"{R}/{j['ten']}/log.json")); spf = lj.get('s_per_frame'); setup = lj.get('setup_s'); n = len(lj['frames'])
        except Exception: spf = setup = n = None
        json.dump(dict(ten=j['ten'], rc=rc, wall_s=round(w, 1), s_per_frame=spf, setup_s=setup, khung=n, song_song=P), open(f"{R}/{j['ten']}.time.json", 'w'))
        print('XONG' if rc == 0 else 'LỖI', j['ten'], rc, round(w, 1), 's', spf, flush=True)
    print('DUNG-BC-XONG')


if __name__ == '__main__': main()
