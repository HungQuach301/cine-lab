#!/opt/cine/bin/python
"""GIONG-T4 · nối bản thu (theo reports/kl42/ghep.py) thành stem lời: mỗi phần giải mã 48 kHz mono, cắt lặng đầu/cuối theo năng lượng (giữ 80 ms đầu, 150 ms cuối, fade 10 ms),
đặt phần sau sao cho khoảng ngừng (theo alignment) ở chỗ nối = trung vị khoảng ngừng tự nhiên giữa các đoạn trong chương. Không kéo nhịp, không đổi chữ. Câu thu lại đã chọn (thay.json, chon=true) được ghép đè bằng ghep_cau().
Chương nối nhau cách 2,0 s (chỉ để nghe; V7 đặt lời theo shot).
→ $GL_OUT/stem/{NN}.wav (thô, 24-bit), stem/T4-loi-tho.wav; mốc: $GL_OUT/stem/moc.json (giây trong chương và trong stem)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import gl_lib as K
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
    for t in sorted([t for t in THAY if t['chon'] and t['chuong'] == rec['chuong'][:2]], key=lambda t: -[c['bd'] for d in doan if d['shot'] == t['shot'] for c in d['cau']][t['i']]):
        out = ghep_cau(out, doan, t)
    for d in doan: d['bd'], d['kt'] = d['cau'][0]['bd'], d['cau'][-1]['kt']
    return out, doan, g


def ghep_cau(out, doan, t):
    """câu thu lại: cắt [bd − pre, kt + post] của câu cũ (pre/post = ½ khoảng ngừng tới câu kề, ≤ 0,25 s), chèn bản mới cắt cùng lề theo alignment; dời mốc sau đó."""
    C = [c for d in doan for c in d['cau']]; c = [c for d in doan if d['shot'] == t['shot'] for c in d['cau']][t['i']]; k = C.index(c)
    pe = C[k - 1]['kt'] if k else 0.0; nb = C[k + 1]['bd'] if k + 1 < len(C) else len(out) / SR
    pre, post = min(0.25, (c['bd'] - pe) / 2), min(0.25, (nb - c['kt']) / 2)
    y = mono(K.OUT / 'raw' / Path(t['tep']).name); seg = y[max(0, int((t['bd'] - pre) * SR)):int((t['kt'] + post) * SR)].copy(); f = int(FADE * SR)
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    a, b = int(round((c['bd'] - pre) * SR)), int(round((c['kt'] + post) * SR)); delta = (len(seg) - (b - a)) / SR
    g = muc_noi(out[int(c['bd'] * SR):int(c['kt'] * SR)]) - muc_noi(y[int(t['bd'] * SR):int(t['kt'] * SR)])   # GIONG-T4: khớp mức tiếng nói câu thay với câu bị thay
    g = max(-6.0, min(6.0, g)); seg *= 10 ** (g / 20); t['khop_muc_db'] = round(g, 2)
    out = np.concatenate([out[:a], seg, out[b:]])
    c['bd'] = round(a / SR + pre, 3); c['kt'] = round(c['bd'] + t['kt'] - t['bd'], 3); c['thu_lai'] = dict(seed=t['seed'], tep=t['tep'])
    for x in C[k + 1:]: x['bd'] = round(x['bd'] + delta, 3); x['kt'] = round(x['kt'] + delta, 3)
    return out


def muc_noi(x, n=960):
    """mức RMS (dBFS) của các khung 20 ms trong 25 dB dưới khung to nhất — mức tiếng nói, bỏ lặng"""
    fr = x[:len(x) // n * n].reshape(-1, n).astype(np.float64); r = np.sqrt((fr ** 2).mean(1)); db = 20 * np.log10(r + 1e-9); m = db > db.max() - 25
    return float(20 * np.log10(np.sqrt((fr[m] ** 2).mean()) + 1e-12))


THAY = json.loads((K.G / 'thay.json').read_text()) if (K.G / 'thay.json').exists() else []


if __name__ == '__main__':
    d = K.OUT / 'stem'; d.mkdir(exist_ok=True)
    C = [c for c, _ in K.doan()]; full = np.zeros(0, np.float32); M = dict(chuong=[], gap_chuong=GAP_CH, sr=SR)
    for cid in C:
        rec = json.loads((K.OUT / 'thu' / f'{cid[:2]}.json').read_text()); x, doan, g = chuong(rec)
        lib.write(str(d / f'{cid[:2]}.wav'), x[:, None]); t0 = len(full) / SR + (GAP_CH if len(full) else 0.0)
        full = np.concatenate([full, np.zeros(int(round((t0 - len(full) / SR) * SR)), np.float32), x])
        M['chuong'].append(dict(chuong=cid, bd_stem=round(t0, 3), giay=round(len(x) / SR, 3), ngung_noi=round(g, 3), so_phan=len(rec['phan']),
                                doan=[dict(dd, bd_stem=round(dd['bd'] + t0, 3), kt_stem=round(dd['kt'] + t0, 3)) for dd in doan]))
    lib.write(str(d / 'T4-loi-tho.wav'), full[:, None]); M['giay_stem'] = round(len(full) / SR, 3)
    M['thu_lai'] = [dict(chuong=t['chuong'], shot=t['shot'], i=t['i'], seed=t['seed'], khop_muc_db=t.get('khop_muc_db')) for t in THAY if t['chon']]
    json.dump(M, open(d / 'moc.json', 'w'), ensure_ascii=False, indent=1)
    print('stem', M['giay_stem'], 's;', [(c['chuong'], c['giay'], c['ngung_noi']) for c in M['chuong']])
