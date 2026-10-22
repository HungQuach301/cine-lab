"""SFX-T3 · trộn thử một đoạn: bản KHÔNG SFX vs bản CÓ SFX (chỉ đề xuất; KHÔNG phải bản phát hành).
  tron_thu.py <su-kien.json> <thư mục ra>
Nền nhạc: phương án B theo reports/nhac-t3/cue/cue-B.json, dựng bằng NGUYÊN hàm nen() của reports/nhac-t3/cong-cu/tron.py (import, không sửa),
  tệp nhạc từ assets/k2/music (LFS, SHA khớp SHA256SUMS). Lời: master FLAC G1 (dat_loi.py). SFX: các ứng viên ung-vien/*.ogg (−23 LUFS)
  đặt theo su-kien.json: {uv, t (giây phim), vao (giây trong tệp), dai, db (so với −23 LUFS), fi, fo, lp, hp, pan (−1…1, cho tệp mono), lap}.
Hoàn thiện: GỌI NGUYÊN scripts/audio/master.py finish() cho CẢ HAI bản (cùng tham số): lời −17 LUFS → duck thích ứng (nhạc −12 dB cơ bản,
  SFX hạ ½ mức của nhạc) → 2 lượt loudness −14 LUFS, trần −1 dBTP, kiểm sau AAC. SMR (A4) đo trên stem lời vs NỀN = nhạc + SFX đã duck."""
import json, os, sys, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
os.environ['NHAC_T3_NGOAI'] = os.path.join(ROOT, 'assets/k2/music')
sys.path.insert(0, os.path.join(ROOT, 'scripts/audio')); sys.path.insert(0, os.path.join(ROOT, 'reports/nhac-t3/cong-cu')); sys.path.insert(0, HERE)
import lib, measure, master, tron, dat_loi
SR = lib.SR; UV = os.path.join(ROOT, 'reports/sfx-t3/ung-vien'); CUE = os.path.join(ROOT, 'reports/nhac-t3/cue/cue-B.json')
_dec = {}
def tep_uv(uv):
    if uv not in _dec: _dec[uv] = lib.dec(os.path.join(UV, uv + '.ogg'), 2, dtype=np.float32)
    return _dec[uv]
def loc(x, lp, hp):
    if not lp and not hp: return x
    af = ','.join(([f'lowpass=f={lp}'] if lp else []) + ([f'highpass=f={hp}'] if hp else []))
    r = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', af, '-f', 'f32le', '-'], input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()
def sfx_stem(E, t0, t1):
    N = int(round((t1 - t0) * SR)); out = np.zeros((N, 2), np.float32); log = []
    for e in E:
        src = tep_uv(e['uv']); a = int(e.get('vao', 0) * SR); dai = e.get('dai') or (len(src) - a) / SR; n = int(dai * SR)
        seg = src[a:a + n]
        if len(seg) < n and e.get('lap'):
            reps = [src[a:]]; tot = len(reps[0]); xf = int(1.0 * SR)
            while tot < n: reps.append(src); tot += len(src) - xf
            seg = reps[0]
            for r in reps[1:]:
                w = np.linspace(0, 1, xf)[:, None]; seg = np.concatenate([seg[:-xf], seg[-xf:] * np.cos(w * np.pi / 2) + r[:xf] * np.sin(w * np.pi / 2), r[xf:]])
            seg = seg[:n]
        seg = loc(seg, e.get('lp'), e.get('hp'))
        if 'pan' in e:   # cân bằng công suất (tệp mono đã nhân đôi kênh khi giải mã)
            p = (e['pan'] + 1) * np.pi / 4; seg = seg * np.array([np.cos(p), np.sin(p)], np.float32) * np.sqrt(2)
        m = len(seg); env = np.ones(m, np.float32); fi, fo = int(e.get('fi', 0.01) * SR), int(e.get('fo', 0.05) * SR)
        if fi: env[:min(fi, m)] *= np.linspace(0, 1, min(fi, m))
        if fo: env[max(0, m - fo):] *= np.linspace(1, 0, m - max(0, m - fo))
        seg = seg * (env * 10 ** (e['db'] / 20))[:, None]
        i = int(round((e['t'] - t0) * SR)); j0 = max(0, -i); i = max(0, i); k = min(m - j0, N - i)
        if k > 0: out[i:i + k] += seg[j0:j0 + k]
        log.append(dict(uv=e['uv'], t=e['t'], dai=round(m / SR, 2), db=e['db']))
    return out, log
def st(x, a, b):  # loudness tích hợp của nền trong các khoảng (giây)
    m = np.zeros(len(x), bool)
    for p, q in a if b is None else [(a, b)]: m[int(p * SR):int(q * SR)] = True
    return round(float(lib.integrated(x[m])), 2) if m.sum() > SR else None
def chay(sk, ra):
    S = json.load(open(sk)); t0, t1, ten = S['t0'], S['t1'], S['doan']; P = json.load(open(CUE)); os.makedirs(ra, exist_ok=True)
    bed, nlog = tron.nen(P, t0, t1); vo, sp = dat_loi.dung(t0, t1); N = len(bed); vo = vo[:N] if len(vo) >= N else np.pad(vo, (0, N - len(vo)))
    fx, flog = sfx_stem(S['su_kien'], t0, t1); spm = lib.merge([list(x) for x in sp], 0.55)
    loi_kv = [(a, b) for a, b in spm]; ngoai = []; prev = 0.0
    for a, b in loi_kv: ngoai.append((prev, a)) if a - prev > 0.3 else None; prev = b
    ngoai.append((prev, t1 - t0))
    truoc = dict(nhac_LUFS_trong_loi=st(bed, loi_kv, None), sfx_LUFS_trong_loi=st(fx, loi_kv, None), sfx_LUFS_ngoai_loi=st(fx, ngoai, None),
                 sfx_LUFS_ca_doan=round(float(lib.integrated(fx)), 2) if np.abs(fx).max() > 0 else None)
    R = dict(doan=ten, khoang_phim=[t0, t1], truoc_master=truoc, nen=nlog, sfx=flog, ban={})
    fi = 0.3 if t0 == 0 else 1.0
    for nhan, sfx in (('khong-sfx', None), ('co-sfx', fx)):
        out = os.path.join(ra, f'{ten}-{nhan}.wav')
        M = master.finish(dict(vo=vo[:, None].copy(), music=bed.copy(), sfx=None if sfx is None else sfx.copy()), speech=[tuple(x) for x in spm], out_wav=out, fade_in=fi, fade_out=1.5)
        W = tron.cua_so(tron.CAP['vo'], tron.CAP['bed'], tron.CAP['sp'], t0)
        R['ban'][nhan] = dict(dau_ra=M['dau_ra'], smr=M['smr'], dat=M['dat'], duck={k: v for k, v in M['duck'].items() if k != 'ds'}, cua_so_smr_thap_nhat=sorted(W, key=lambda w: w[1])[:5])
        print(ten, nhan, M['dau_ra'], M['smr'], flush=True)
    json.dump(R, open(os.path.join(ra, f'{ten}.json'), 'w'), ensure_ascii=False, indent=1)
    return R
if __name__ == '__main__': chay(sys.argv[1], sys.argv[2])
