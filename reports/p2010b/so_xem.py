#!/opt/cine/bin/python
"""P-2010b · việc 1 bước 5: thử triệt (null test) master ghép lại ↔ bản xem gốc trong git. Mã hoá lại master mới thành bản xem bằng ĐÚNG lệnh + tham số vòng cuối
của xuat.py (xuat.json `ban_xem`), rồi theo từng chương đo: SNR(bản xem gốc vs master mới), SNR(bản xem mới vs master mới) = mức lỗi riêng của MP3 96 kb/s,
và SNR(bản xem gốc vs bản xem mới). Căn mẫu bằng tương quan chéo toàn tệp (độ trễ giải mã MP3). → so-xem.json"""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; R = H.parents[1]; PO = Path(os.environ.get('P_OUT', '/var/tmp/cine-out/p2010b'))
sys.path.insert(0, str(R / 'scripts/audio')); import lib   # noqa: E402
SR = 48000; W = PO / 'master/T3-loi-G1-v42-14LUFS.wav'; X = json.loads((R / 'reports/kl42/xuat.json').read_text())['ban_xem']
M = json.loads((PO / 'stem/moc.json').read_text())['chuong']
m = lib.dec(str(W), 1, dtype=np.float32)[:, 0]


def snr(a, b): return round(float(10 * np.log10((b.astype(np.float64) ** 2).sum() / max(((a.astype(np.float64) - b) ** 2).sum(), 1e-20))), 2)


def lagk(a, b, n=SR * 20, w=SR // 10):   # mẫu trễ của a so với b (a[k+lag] ≈ b[k])
    s = np.argmax(np.abs(b[:n * 3])); s = max(0, s - n // 2); x, y = a[s:s + n + 2 * w].astype(np.float64), b[s + w:s + w + n].astype(np.float64)
    c = [np.dot(x[k:k + n], y) for k in range(2 * w)]; return int(np.argmax(c)) - w


out = []
for x in X:
    v = x['vong'][-1]; f = PO / ('xem-moi-' + Path(x['tep']).name)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{x['tu']:.3f}", '-to', f"{x['den']:.3f}", '-i', str(W), '-af',
                    f"volume={v['gain_db']:.3f}dB,aresample=192000,alimiter=limit={v['tran']:.3f}:attack=1:release=60:level=false,aresample=48000",
                    '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '96k', str(f)], check=True)
    g0 = lib.dec(str(R / x['tep']), 1, dtype=np.float32)[:, 0]; g1 = lib.dec(str(f), 1, dtype=np.float32)[:, 0]
    i0 = int(round(x['tu'] * SR)); ref = m[i0:i0 + int(round((x['den'] - x['tu']) * SR))] * 10 ** (v['gain_db'] / 20)
    L0, L1 = lagk(g0, ref), lagk(g1, ref)
    for c in M:
        a, b = c['bd_stem'] - x['tu'], c['bd_stem'] + c['giay'] - x['tu']
        if a < -0.01 or b > x['den'] - x['tu'] + 0.01: continue
        s0, s1 = int(max(a, 0) * SR) + 2400, int(b * SR) - 2400; r = ref[s0:s1]
        A0 = g0[s0 + L0:s1 + L0]; A1 = g1[s0 + L1:s1 + L1]; n = min(len(r), len(A0), len(A1)); r, A0, A1 = r[:n], A0[:n], A1[:n]
        out.append(dict(ban_xem=Path(x['tep']).name, chuong=c['chuong'], tre_mau=[L0, L1], snr_goc_vs_master_moi_db=snr(A0, r),
                        snr_xem_moi_vs_master_moi_db=snr(A1, r), snr_goc_vs_xem_moi_db=snr(A0, A1)))
        print(out[-1], flush=True)
json.dump(dict(ghi=__doc__.splitlines()[0], chuong=out), open(H / 'so-xem.json', 'w'), ensure_ascii=False, indent=1)
