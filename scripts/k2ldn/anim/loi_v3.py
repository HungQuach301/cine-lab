#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · việc 1 — LỜI DỰNG v3 = lời dựng v2 (K1-C1, /var/tmp/anim/am/loi-dung.wav SHA 187e059a…, tái tạo bit-trùng bằng giong/tai_tao.sh + anim/loi_dung.py)
+ câu mới/sửa thu G1 (am-thanh/nguon-v3/*.mp3, trong git) theo gl_thu_v3.v3(); câu Churchill (N7) bỏ.
Trong mỗi nhóm lời: câu v2 giữ nguyên khoảng ngừng gốc giữa hai câu v2 liền nhau; câu mới chèn với khoảng ngừng GAP 0,85 s (TB khoảng ngừng câu của G1 v2 ≈ 0,8–0,9 s);
mức câu mới khớp về độ to TB (LUFS ngắn hạn) của câu v2 cùng chương; mối cắt hoà 8 ms. Nhóm đặt tại t0 nhóm (BANG-SHOT-v3.json `nhom_loi_t0`) + 0,2 s.
  loi_v3.py do     → in độ dài lời mỗi nhóm v3 (dùng cho bang_shot_v3.py; không cần âm thanh)
  loi_v3.py dung   → $ANIM_OUT/loi-dung-v3.wav + am-thanh/master-v3/ (mốc, SHA, bản nghe ≤ 5 MB) + animatic/loi-dung-moc-v3.json"""
import collections, hashlib, json, os, subprocess, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; NG3 = EP / 'am-thanh/nguon-v3'; MV3 = EP / 'am-thanh/master-v3'
sys.path.insert(0, str(REPO / 'scripts/k2ldn/giong'))
GAP, XF, SR = 0.85, 0.008, 48000
# bản thu chọn (reports/animatic-t4-v2/giong-v3.json): seed 19102026 trừ N2, N3 (thu lại seed 19102027 — lượt 1: N3 cả 2 cách nghe "worked"; N2 small.en "pull")
CHON = {'N0a': 19102026, 'N0b': 19102026, 'N1': 19102026, 'N2': 19102027, 'N3': 19102027, 'N9': 19102026, 'N4': 19102026, 'N5': 19102026, 'N6': 19102026}


def ban_thu():
    G = json.loads((REPO / 'reports/animatic-t4-v2/giong-v3.json').read_text()); out = {}
    for c in G['cau']:
        if c.get('seed', 19102026) == CHON[c['N']]: out[c['N']] = dict(c, tep_git=str((NG3 / f"{c['N']}-s{CHON[c['N']]}.mp3").relative_to(REPO)))
    assert set(out) == set(CHON), set(CHON) - set(out); return out


def nhom():
    import gl_thu_v3 as V
    C = V.v3(); BT = ban_thu(); G = collections.OrderedDict()
    for c in C: G.setdefault(c['nhom'], []).append(c)
    R = collections.OrderedDict()
    for g, cs in G.items():
        pos, prev, items = 0.0, None, []
        for c in cs:
            if c['nguon'] == 'v2':
                d = c['v2_kt'] - c['v2_bd']
                if prev is not None: pos += (c['v2_bd'] - prev['v2_kt']) if prev['nguon'] == 'v2' else GAP
                items.append(dict(c, off=round(pos, 3), dai=round(d, 3)))
            else:
                b = BT[c['N']]; d = b['kt'] - b['bd']
                if prev is not None: pos += GAP
                items.append(dict(c, off=round(pos, 3), dai=round(d, 3), mp3=b['tep_git'], mp3_bd=b['bd'], mp3_kt=b['kt']))
            pos += d; prev = c
        R[g] = dict(cau=items, loi_s=round(pos, 3))
    return R


def load_mp3(p):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', str(p), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def dung():
    import soundfile as sf, pyloudnorm as pyln
    B = json.loads((EP / 'BANG-SHOT-v3.json').read_text()); T = B['tong']['thoi_luong_s']; t0n = B['nhom_loi_t0']
    src = Path(os.environ.get('ANIM_AM', '/var/tmp/anim/am')) / 'loi-dung.wav'; x, sr = sf.read(src, dtype='float64'); assert sr == SR
    sha_src = hashlib.sha256(src.read_bytes()).hexdigest(); assert sha_src.startswith('187e059a'), sha_src
    R = nhom(); y = np.zeros(int(round(T * SR)) + SR); moc, loi = [], []; m = pyln.Meter(SR, block_size=0.4)
    def lufs(v): return m.integrated_loudness(v) if len(v) > 0.5 * SR else None
    ch_ref = collections.defaultdict(list)
    for g, v in R.items():
        for c in v['cau']:
            if c['nguon'] == 'v2': L = lufs(x[int(c['v2_bd'] * SR):int(c['v2_kt'] * SR)]); ch_ref[g[:2]].append(L) if L and np.isfinite(L) else None
    ks = list(t0n.keys())
    for i, g in enumerate(ks):
        if g not in R: continue
        base = t0n[g] + 0.2
        for c in R[g]['cau']:
            if c['nguon'] == 'v2': seg = x[int(round(c['v2_bd'] * SR)):int(round(c['v2_kt'] * SR))].copy(); gain = 0.0
            else:
                a = load_mp3(REPO / c['mp3']); seg = a[int(round(c['mp3_bd'] * SR)):int(round(c['mp3_kt'] * SR))].copy()
                ref = np.median(ch_ref.get(g[:2]) or sum(ch_ref.values(), [])); gain = ref - lufs(seg); seg *= 10 ** (gain / 20)
            n = int(XF * SR); seg[:n] *= np.linspace(0, 1, n); seg[-n:] *= np.linspace(1, 0, n)
            j = int(round((base + c['off']) * SR)); y[j:j + len(seg)] += seg
            moc.append({'nhom': g, 'L': c['L'], 'N': c['N'], 'nguon': c['nguon'], 'khoa': c['khoa'], 'bd': round(base + c['off'], 3), 'kt': round(base + c['off'] + c['dai'], 3),
                        'khop_muc_dB': round(gain, 2) if c['nguon'] != 'v2' else None})
        ket = base + R[g]['loi_s']; het = t0n[ks[i + 1]] if i + 1 < len(ks) else T
        if ket > het + 1e-3: loi.append(f'{g}: lời kết {ket:.3f} > hết nhóm {het:.3f}')
    y = y[:int(round(T * SR))]
    li = pyln.Meter(SR).integrated_loudness(y); y *= 10 ** ((-14.0 - li) / 20)
    OUT = Path(os.environ.get('ANIM_OUT', '/var/tmp/anim/out')); OUT.mkdir(parents=True, exist_ok=True); pre = OUT / 'loi-v3-truoc.wav'; sf.write(pre, y.astype(np.float32), SR, subtype='FLOAT')
    wav = Path(os.environ.get('ANIM_AM', '/var/tmp/anim/am')) / 'loi-dung-v3.wav'
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(pre), '-af', 'aresample=192000,alimiter=limit=0.84:level=false:attack=2:release=50,aresample=48000', '-c:a', 'pcm_s24le', '-fflags', '+bitexact', '-flags:a', '+bitexact', str(wav)], check=True)
    o = subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-i', str(wav), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(o.split('I:')[-1].split('LUFS')[0]); TP = float(o.split('Peak:')[-1].split('dBFS')[0])
    MV3.mkdir(parents=True, exist_ok=True); nghe = MV3 / 'T4-loi-v3-nghe.mp3'
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(wav), '-c:a', 'libmp3lame', '-b:a', '48k', '-ac', '1', '-fflags', '+bitexact', '-map_metadata', '-1', str(nghe)], check=True)
    sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    rec = {'nguon_v2': {'tep': str(src), 'sha256': sha_src}, 'nguon_v3': {k: {'tep': v['tep_git'], 'sha256': sha(REPO / v['tep_git'])} for k, v in ban_thu().items()}, 'thoi_luong_s': T,
           'ra': {'tep': str(wav), 'sha256': sha(wav), 'ngoai_git': True, 'I_LUFS': I, 'TP_dBTP': TP}, 'nghe': {'tep': str(nghe.relative_to(REPO)), 'sha256': sha(nghe), 'bytes': nghe.stat().st_size},
           'tai_tao': 'bash scripts/k2ldn/giong/tai_tao.sh && ANIM_OUT=/var/tmp/anim/am scripts/k2ldn/anim/loi_dung.py && scripts/k2ldn/bang_shot_v3.py && scripts/k2ldn/anim/loi_v3.py dung',
           'loi_kiem': loi, 'so_cau': len(moc), 'cau': moc}
    (MV3 / 'T4-loi-v3-moc.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1)); (EP / 'animatic/loi-dung-moc-v3.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1))
    (MV3 / 'SHA256SUMS').write_text(f"{rec['ra']['sha256']}  loi-dung-v3.wav (ngoài git: {wav})\n{rec['nghe']['sha256']}  T4-loi-v3-nghe.mp3\n")
    print(json.dumps({k: v for k, v in rec.items() if k not in ('cau', 'nguon_v3')}, ensure_ascii=False))


if __name__ == '__main__':
    if sys.argv[1] == 'do':
        for g, v in nhom().items(): print(g, v['loi_s'], [c['N'] for c in v['cau'] if c['N']])
    else: dung()
