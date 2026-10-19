#!/opt/cine/bin/python
"""KL42 · nối bản thu thành stem lời: mỗi phần giải mã 48 kHz mono, cắt lặng đầu/cuối theo năng lượng (giữ 80 ms đầu, 150 ms cuối, fade 10 ms),
đặt phần sau sao cho khoảng ngừng (theo alignment) ở chỗ nối = trung vị khoảng ngừng tự nhiên giữa các đoạn trong chương. Không kéo nhịp, không đổi chữ.
Chương nối nhau cách 2,0 s (chỉ để nghe; V7 đặt lời theo shot).
→ $KL_OUT/stem/{NN}.wav (thô, 24-bit), stem/T3-loi-tho.wav; mốc: $KL_OUT/stem/moc.json (giây trong chương và trong stem)."""
import json, sys
import numpy as np
import kl_lib as K
sys.path.insert(0, str(K.R / 'scripts/audio')); import lib   # noqa: E402
SR = lib.SR; GAP_CH = 2.0; HEAD, TAIL, FADE = 0.08, 0.15, 0.01


def mono(p): return lib.dec(p, 1, sr=SR, dtype=np.float32)[:, 0]


def trim(x, thr_db=-50.0, win=0.02):
    n = int(win * SR); r = np.sqrt(np.convolve(x.astype(np.float64) ** 2, np.ones(n) / n, 'same')); on = np.where(r > 10 ** (thr_db / 20))[0]
    a, b = max(0, on[0] - int(HEAD * SR)), min(len(x), on[-1] + int(TAIL * SR)); y = x[a:b].copy(); f = int(FADE * SR)
    y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f); return y, a / SR


def chuong(rec):
    P = rec['phan']; gaps = [b['bd'] - a['kt'] for p in P for a, b in zip(p['doan'], p['doan'][1:])]
    g = float(np.median(gaps)) if gaps else 0.6
    out = np.zeros(0, np.float32); doan = []; last_kt = None
    for p in P:
        x = mono(p['tep'])
        y, off = trim(x); d0 = p['doan'][0]['bd'] - off            # mốc đầu lời của phần, trong y
        st = 0.0 if last_kt is None else last_kt + g - d0           # vị trí đặt y trong chương
        i0 = int(round(st * SR)); need = i0 + len(y)
        if need > len(out): out = np.concatenate([out, np.zeros(need - len(out), np.float32)])
        out[i0:i0 + len(y)] += y; sh = st - off
        for d in p['doan']:
            doan.append(dict(shot=d['shot'], bd=round(d['bd'] + sh, 3), kt=round(d['kt'] + sh, 3), cau=[dict(khoa=c['khoa'], bd=round(c['bd'] + sh, 3), kt=round(c['kt'] + sh, 3)) for c in d['cau']]))
        last_kt = p['doan'][-1]['kt'] + sh
    return out, doan, g


if __name__ == '__main__':
    d = K.OUT / 'stem'; d.mkdir(exist_ok=True)
    C = [c for c, _ in K.doan_v42()]; full = np.zeros(0, np.float32); M = dict(chuong=[], gap_chuong=GAP_CH, sr=SR)
    for cid in C:
        rec = json.loads((K.OUT / 'thu' / f'{cid[:2]}.json').read_text()); x, doan, g = chuong(rec)
        lib.write(str(d / f'{cid[:2]}.wav'), x[:, None]); t0 = len(full) / SR + (GAP_CH if len(full) else 0.0)
        full = np.concatenate([full, np.zeros(int(round((t0 - len(full) / SR) * SR)), np.float32), x])
        M['chuong'].append(dict(chuong=cid, bd_stem=round(t0, 3), giay=round(len(x) / SR, 3), ngung_noi=round(g, 3), so_phan=len(rec['phan']),
                                doan=[dict(dd, bd_stem=round(dd['bd'] + t0, 3), kt_stem=round(dd['kt'] + t0, 3)) for dd in doan]))
    lib.write(str(d / 'T3-loi-tho.wav'), full[:, None]); M['giay_stem'] = round(len(full) / SR, 3)
    json.dump(M, open(d / 'moc.json', 'w'), ensure_ascii=False, indent=1)
    print('stem', M['giay_stem'], 's;', [(c['chuong'], c['giay'], c['ngung_noi']) for c in M['chuong']])
