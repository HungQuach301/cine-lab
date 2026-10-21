#!/opt/cine/bin/python
"""ANIMATIC-T3-V2 (21/10/2026) · ĐO R1/R2 BẰNG MẶT NẠ ID (design/k2v/v7c/idmask_v7c.js qua do_bocuc.js), 1 khung/giây mỗi shot cảnh đinh.
R2: khung 'cỏ/cát trống' = lớp 'bang' (đất bằng không vật) > 50 % khung. Ghi theo shot: % lớp từng khung + chủ thể (vật trên đất: người, trại, công sự, nhà, phố, lửa, tàu, pin, cờ, khác).
  v2_do_r2.py do <thư mục opt (mk_ep_anim.py --opt-dir)> <thư mục ra> [--root <cây repo>] [--shots A,B] [--P 2]
  v2_do_r2.py gop <thư mục ra> <bang-shot.json> [<tệp tóm tắt .json>]       → % thời lượng cỏ/cát trống mỗi chương, đoạn liên tục dài nhất, chủ thể % shot eo đất
Mỗi mẫu đại diện 1 s (khung 0, 24, 48 …; mẫu cuối đại diện phần lẻ)."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
CHU_THE = ['nguoi', 'trai', 'congsu', 'nha', 'pho', 'lua', 'tau', 'pin', 'co', 'khac']


def do(od, out, root, only, P):
    out.mkdir(parents=True, exist_ok=True); jobs = []
    for f in sorted(od.glob('anim_*.json')):
        o = json.loads(f.read_text())
        if only and o['shot'] not in only: continue
        o.pop('nc', None)   # đo bố cục: tắt cách A (cùng máy/vật; nhanh)
        jobs.append((o['shot'], o))
    def one(j):
        sid, o = j; r = out / f"{sid.replace('.', '_')}.json"
        if r.exists(): return sid, 'có'
        p = subprocess.run(['node', str(REPO / 'design/k2v/v7c/do_bocuc.js'), '--root', str(root), '--opt', json.dumps(o), '--every', '24', '--out', str(r), '--w', '960', '--h', '540', '--scale', '0.5'],
                           capture_output=True, text=True, env=dict(os.environ, K2TL_CACHE=os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache')))
        return sid, ('xong' if p.returncode == 0 and r.exists() else 'LỖI ' + (p.stderr or p.stdout)[-300:])
    with ThreadPoolExecutor(P) as ex:
        for sid, st in ex.map(one, jobs): print(sid, st, flush=True)


def gop(out, bang_p, tom=None):
    B = json.loads(Path(bang_p).read_text()); rows = []; per_ch = {}; runs = []
    LOG = {x['shot']: x for x in json.loads((Path(bang_p).parent / 'log-shot.json').read_text()) if 'kieu_khung' in x}
    for b in B:
        if b['kieu'] == 'the': continue
        sid = b['ma']; f = out / f"{sid.replace('.', '_')}.json"
        if not f.exists(): continue
        fr = json.loads(f.read_text())['frames']; n = len(fr); d = b['dur']
        w = [min(1.0, d - i) for i in range(n)]   # giây đại diện mỗi mẫu
        trong = [x['pct'].get('bang', 0) > 50 for x in fr]; ct = [sum(x['pct'].get(c, 0) for c in CHU_THE) for x in fr]
        sec_trong = sum(wi for wi, t in zip(w, trong) if t)
        ch = LOG.get(sid.replace('.', '_'), {}).get('chuong_so') or b.get('chuong') or '?'
        rows.append(dict(shot=sid, t0=b['t0'], dur=d, giay_trong=round(sec_trong, 2), pct_trong=round(100 * sec_trong / d, 1), chu_the_tb=round(sum(ct) / n, 2), chu_the_min=round(min(ct), 2),
                         bang_tb=round(sum(x['pct'].get('bang', 0) for x in fr) / n, 1), mau=n))
        for i, t in enumerate(trong): runs.append((b['t0'] + i, t, sid, w[i]))
    runs.sort(); best, cur, st = (0, None), 0.0, None   # đoạn liên tục dài nhất trên cả phim (nối qua ranh shot)
    for t, tr, sid, wi in runs:
        if tr: cur += wi; st = st or (t, sid); best = max(best, (cur, st), key=lambda x: x[0])
        else: cur, st = 0.0, None
    CH = [('0 móc', 0, 43.833), ('1 Rock 1704', 43.833, 173.083), ('2 vây hãm', 173.083, 382.583), ('3 đất trung lập', 382.583, 471.625), ('4 đường băng', 471.625, 585.833), ('5 cổng', 585.833, 745.0)]
    chuong = [dict(chuong=c, giay=round(b1 - b0, 2), giay_trong=round(sum(r['giay_trong'] for r in rows if b0 - 0.01 <= r['t0'] < b1 - 0.01), 2)) for c, b0, b1 in CH]
    for c in chuong: c['pct_trong'] = round(100 * c['giay_trong'] / c['giay'], 1)
    res = dict(shot=rows, chuong=chuong, lien_tuc_dai_nhat_s=round(best[0], 2), bat_dau=best[1], so_shot_tren_15s=sum(1 for r in rows if r['dur'] > 15))
    if tom: Path(tom).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    for r in rows: print(f"{r['shot']:8s} {r['t0']:7.1f} {r['dur']:6.2f}  trống {r['giay_trong']:5.1f} s ({r['pct_trong']:5.1f} %)  bang TB {r['bang_tb']:5.1f}  chủ thể TB {r['chu_the_tb']:5.1f} min {r['chu_the_min']:5.1f}")
    for c in res['chuong']: print('CHƯƠNG', c)
    print('liên tục dài nhất', res['lien_tuc_dai_nhat_s'], res['bat_dau'], '· shot > 15 s:', res['so_shot_tren_15s'])
    return res


if __name__ == '__main__':
    a = sys.argv; arg = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    if a[1] == 'do': do(Path(a[2]), Path(a[3]), Path(arg('--root', str(REPO))), set(arg('--shots', '').split(',')) - {''}, int(arg('--P', '2')))
    else: gop(Path(a[2]), a[3], a[4] if len(a) > 4 else None)
