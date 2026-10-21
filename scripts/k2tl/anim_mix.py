#!/opt/cine/bin/python
"""ANIMATIC-T3 · TRỘN TIẾNG cả tập 761 s: giọng master G1 v4.2 (LFS channel-k2/k2c-t3-01/am-thanh/master/T3-loi-G1-v42-14LUFS.wav, SHA ba50fba7…)
đặt theo animatic/anim-loi.json (nhịp B) + nhạc phương án B theo cue sheet reports/nhac-t3/cue/cue-B.json, TRỪ tấm im lặng KA2026 (717,0 → 725,0 s) dùng cue A8
(Sincerely 139,46 → 147,46 s bài, +4,5 dB như A8; Kinh thánh §14.6). Nền nhạc dựng bằng chính hàm nen() của reports/nhac-t3/cong-cu/tron.py (−24 LUFS/nhóm, crossfade
công suất bằng nhau); hoàn thiện bằng scripts/audio/master.py finish() (lời −17 LUFS → duck thích ứng §4 → loudness 2 lượt −14 LUFS, đỉnh thật ≤ −1 dBTP kiểm sau AAC).
  anim_mix.py <anim-loi.json> <ra.wav> [--json ra.json] [--khong-nhac]"""
import copy, json, os, sys
import numpy as np
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.environ.setdefault('NHAC_T3_NGOAI', os.path.join(REPO, 'assets/k2/music'))
sys.path.insert(0, os.path.join(REPO, 'reports/nhac-t3/cong-cu')); sys.path.insert(0, os.path.join(REPO, 'scripts/audio'))
import tron, lib, master   # tron: nen(), cua_so(), CAP (bắt stem đã xử lý để đo SMR)
SR = lib.SR
MASTER = os.path.join(REPO, 'channel-k2/k2c-t3-01/am-thanh/master/T3-loi-G1-v42-14LUFS.wav')
KA = (717.0, 725.0)

def cue_sheet():
    B = json.load(open(os.path.join(REPO, 'reports/nhac-t3/cue/cue-B.json'))); A = {c['id']: c for c in json.load(open(os.path.join(REPO, 'reports/nhac-t3/cue/cue-A.json')))['cue']}
    P = copy.deepcopy(B); P['phim_s'] = 761.0; out = []
    for c in P['cue']:
        if c['phim_vao'] < KA[0] < c['phim_ra']:   # B11 phủ KA2026 → tách hai nửa quanh tấm im lặng
            c1 = dict(c, id=c['id'] + 'a', phim_ra=KA[0], xf_ra=1.0, tang=[t for t in c.get('tang', []) if t[1] <= KA[0]])
            c2 = dict(c, id=c['id'] + 'b', phim_vao=KA[1], xf_vao=1.0, vao_bai=c['vao_bai'] + (KA[1] - c['phim_vao']), tang=[t for t in c.get('tang', []) if t[0] >= KA[1]])
            out += [c1, c2]
        else: out.append(c)
    a8 = A['A8']; ins = dict(a8, id='A8-KA2026', phim_vao=KA[0], phim_ra=KA[1], xf_vao=1.0, xf_ra=1.0, vao_bai=a8['vao_bai'] + (KA[0] - a8['phim_vao']), nhom='A8', tang=[[KA[0], KA[1], 4.5]])
    out.append(ins); P['cue'] = sorted(out, key=lambda c: c['phim_vao']); P['ghi'] = 'cue-B (NHẠC-T3) + KA2026 = A8 (§14.6); phim 745,0 s + 2 thẻ × 8 s'
    return P

def giong(L, N, pad=0.12):
    a = lib.dec(MASTER, 1, dtype=np.float32)[:, 0]; vo = np.zeros(N, np.float32); sp = []; r = int(0.01 * SR)
    for d in L['dong']:
        s0, s1 = max(0.0, d['bd_stem'] - pad), d['kt_stem'] + pad; x = a[int(s0 * SR):int(s1 * SR)].copy(); x[:r] *= np.linspace(0, 1, r); x[-r:] *= np.linspace(1, 0, r)
        i = int(round((d['bd_phim'] - (d['bd_stem'] - s0)) * SR)); m = min(len(x), N - i); vo[i:i + m] += x[:m]
        sp.append((round(d['bd_phim'], 3), round(d['bd_phim'] + d['kt_stem'] - d['bd_stem'], 3)))
    return vo, sorted(sp)

if __name__ == '__main__':
    L = json.load(open(sys.argv[1])); out = sys.argv[2]; js = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else out.rsplit('.', 1)[0] + '.json'
    P = cue_sheet(); json.dump(P, open(out.rsplit('.', 1)[0] + '-cue.json', 'w'), ensure_ascii=False, indent=1)
    bed, log = tron.nen(P, 0.0, P['phim_s']); N = len(bed)
    if '--khong-nhac' in sys.argv: bed = np.zeros_like(bed)
    vo, sp = giong(L, N)
    R = master.finish(dict(vo=vo[:, None], music=bed, sfx=None), speech=[tuple(x) for x in lib.merge([list(x) for x in sp], 0.55)], out_wav=out, fade_in=0.3, fade_out=2.0)
    R['cua_so_smr'] = tron.cua_so(tron.CAP['vo'], tron.CAP['bed'], tron.CAP['sp'], 0.0); R['nen'] = log; R['cue'] = 'cue-B + A8 ở KA2026'; R['giong'] = dict(tep=MASTER, sha256='ba50fba75aa956731226f7269adbffb6728853d6d2a7fc95b4eefba8e13b586d', dong=len(L['dong']))
    json.dump(R, open(js, 'w'), ensure_ascii=False, indent=0)
    print(json.dumps({k: R.get(k) for k in ('dau_ra', 'smr', 'dat')}, ensure_ascii=False))
