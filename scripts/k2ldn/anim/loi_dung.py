#!/opt/cine/bin/python
"""ANIMATIC-T4 · việc 1 — LỜI DỰNG theo G-1 = (c) K1-C1: cắt 7 câu NGUYÊN trên bản thu G1 (không thu lại, 0 ký tự) và đặt lời từng nhóm theo BANG-SHOT-v2.
Vào: master WAV tái tạo bit-trùng (scripts/k2ldn/giong/tai_tao.sh → $GL_OUT/xuat/T4-loi-G1-v2-14LUFS.wav, SHA b9cec467…) + mốc câu am-thanh/master/T4-loi-moc.json.
Cách: mỗi nhóm lời = đoạn từ đầu câu đầu tới cuối câu cuối của shot v1; câu bỏ (k1c1.CAT) cắt cùng khoảng ngừng SAU câu (câu cuối: khoảng ngừng TRƯỚC) — như cách tính tiết kiệm của GIAN-SHOT;
mối cắt hoà 8 ms; không kéo nhịp, không đổi mức. Nhóm đặt tại t0 nhóm + 0,2 s (BANG-SHOT-v2.json `nhom_loi_t0`). Kiểm: không chồng nhóm kề; mỗi nhóm kết trước hết nhóm.
Ra: $ANIM_OUT/loi-dung.wav (48 kHz mono 24-bit, ngoài git, SHA trong mốc) + channel-k2/k2c-t4-02/animatic/loi-dung-moc.json (mốc câu mới trong phim, trong git)."""
import hashlib, json, os, sys
from pathlib import Path
import numpy as np, soundfile as sf
sys.path.insert(0, str(Path(__file__).resolve().parent)); import k1c1  # noqa: E402
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'
SRC = Path(os.environ.get('GL_OUT', '/var/tmp/cine-out/giong-t4-tai-tao')) / 'xuat/T4-loi-G1-v2-14LUFS.wav'
OUT = Path(os.environ.get('ANIM_OUT', '/var/tmp/anim/am')); OUT.mkdir(parents=True, exist_ok=True)
XF = 0.008


def main():
    x, sr = sf.read(SRC, dtype='float64'); assert sr == 48000
    sha_src = hashlib.sha256(SRC.read_bytes()).hexdigest(); assert sha_src.startswith('b9cec467'), sha_src
    B = json.loads((EP / 'BANG-SHOT-v2.json').read_text()); T = B['tong']['thoi_luong_s']; t0n = B['nhom_loi_t0']
    K = k1c1.bang(); y = np.zeros(int(round(T * sr)) + sr)
    moc, loi = [], []
    nhom_ket = {}
    ks = list(t0n.keys())
    for i, g in enumerate(ks):
        cs = K[g]['cau']
        if not cs: continue
        # khoảng giữ trong stem: [bd câu đầu, kt câu cuối] trừ các câu bỏ (+ khoảng ngừng)
        a, b = cs[0]['bd_stem'], cs[-1]['kt_stem']; bo = []
        for k, c in enumerate(cs):
            if not c['bo']: continue
            if k + 1 < len(cs): bo.append((c['bd_stem'], cs[k + 1]['bd_stem']))
            else: bo.append((cs[k - 1]['kt_stem'], c['kt_stem']))
        giu = []; s = a
        for (u, v) in sorted(bo): giu.append((s, u)); s = v
        giu.append((s, b)); giu = [(u, v) for u, v in giu if v - u > 0.01]
        pos = t0n[g] + 0.2; seg_t = []
        for (u, v) in giu:
            seg = x[int(round(u * sr)):int(round(v * sr))].copy(); n = int(XF * sr)
            if len(seg) > 2 * n: seg[:n] *= np.linspace(0, 1, n); seg[-n:] *= np.linspace(1, 0, n)
            j = int(round(pos * sr)); y[j:j + len(seg)] += seg; seg_t.append((u, v, pos)); pos += (v - u)
        ket = pos; nhom_ket[g] = ket
        het = t0n[ks[i + 1]] if i + 1 < len(ks) else T
        if ket > het + 1e-3: loi.append(f'{g}: lời kết {ket:.3f} > hết nhóm {het:.3f}')
        for c in cs:
            if c['bo']: moc.append({'nhom': g, 'L': c['L'], 'khoa': c['khoa'], 'bo': True}); continue
            for (u, v, p) in seg_t:
                if u - 1e-3 <= c['bd_stem'] and c['kt_stem'] <= v + 1e-3:
                    moc.append({'nhom': g, 'L': c['L'], 'khoa': c['khoa'], 'bo': False, 'bd': round(p + c['bd_stem'] - u, 3), 'kt': round(p + c['kt_stem'] - u, 3)}); break
    y = y[:int(round(T * sr))]
    wav = OUT / 'loi-dung.wav'; sf.write(wav, y, sr, subtype='PCM_24')
    rec = {'nguon': {'tep': 'T4-loi-G1-v2-14LUFS.wav', 'sha256': sha_src}, 'phuong_an': 'K1-C1', 'cau_bo': k1c1.CAT, 'thoi_luong_s': T,
           'ra': {'tep': str(wav), 'sha256': hashlib.sha256(wav.read_bytes()).hexdigest()}, 'loi_kiem': loi,
           'giay_loi': round(sum(m['kt'] - m['bd'] for m in moc if not m['bo']), 3), 'so_cau': sum(1 for m in moc if not m['bo']), 'so_cau_bo': sum(1 for m in moc if m['bo']), 'cau': moc}
    (EP / 'animatic').mkdir(parents=True, exist_ok=True); (EP / 'animatic/loi-dung-moc.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in rec.items() if k != 'cau'}, ensure_ascii=False))


if __name__ == '__main__': main()
