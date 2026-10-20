#!/opt/cine/bin/python
"""P-2010b · đo (c) cho ghep_lai.py: tìm nguồn của 70 ms âm ở 94,875 s chương 01 trong bản xem gốc (chỗ nối câu thay 1i#0 → 1i#1) bằng tương quan chuẩn hoá
với bản thu chương 01 và hai tệp câu thay (audio lịch sử). Kết quả: bản thu chương ở 95,561 s, r = 1,0 → câu cũ 1i#0 kết thúc 95,306 s (mốc trước ghép)."""
import os, sys
import numpy as np
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); sys.path.insert(0, os.path.join(R, 'scripts/audio')); import lib  # noqa: E402
SR = 48000; PO = os.environ.get('P_OUT', '/var/tmp/cine-out/p2010b'); T0 = 44.678; TRE = 95.5   # độ trễ bản xem so với stem ở chương 01 (mẫu, ghep-lai.json)
g0 = lib.dec(os.path.join(R, 'reports/kl42/nghe/T3-loi-G1-v42-xem-1-ch00-02.mp3'), 1, dtype=np.float32)[:, 0].astype(np.float64)
i = int((T0 + 94.875) * SR + TRE); sn = g0[i:i + int(0.07 * SR)]
for ten in ('01-ROCK-p0', '01-thay-1i-0', '01-thay-1i-1'):
    x = lib.dec(f'{PO}/lich-su/{ten}.mp3', 1, dtype=np.float32)[:, 0].astype(np.float64); n = len(sn)
    L = 1 << int(np.ceil(np.log2(len(x) + n))); c = np.fft.irfft(np.fft.rfft(x, L) * np.conj(np.fft.rfft(sn, L)), L)[:len(x) - n + 1]
    e = np.sqrt(np.convolve(x ** 2, np.ones(n), 'valid')) * np.sqrt((sn ** 2).sum()); r = c / np.maximum(e, 1e-12); k = int(np.argmax(r))
    print(ten, 'vị trí', round(k / SR, 4), 's · r', round(float(r[k]), 4))
