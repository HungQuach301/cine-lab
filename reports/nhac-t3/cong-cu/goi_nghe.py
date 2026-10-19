"""NHẠC-T3 · gói nghe mù: 4 cặp X/Y (A vs B), MP3 160 kb/s, kiểm I/TP trên chính tệp MP3 (BAI-HOC-LL #69).
  goi_nghe.py <thư mục wav> <thư mục ra>
Cần sẵn trong <thư mục wav>: {A,B}-moc.wav, {A,B}-pin.wav (trộn thử có lời, −14 LUFS, từ tron.py) và full-{A,B}.wav (cả phim −14 LUFS)
— hai tấm im lặng cắt từ bản cả phim (đúng nhạc + tự động hoá như trong phim), rồi đưa CẢ HAI bản về cùng −17,0 LUFS (gần mức trong phim;
  không chuẩn −14 vì nhạc trần ở −14 to hơn trong phim ≈ 3 LU).
Gán X/Y ngẫu nhiên (secrets), ghi khoa.json."""
import json, os, secrets, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../scripts/audio'))
import lib
CAP = [('1-moc', 'móc 0a–0f (phim 0,0–34,0 s)', '{p}-moc.wav', None, -14.0),
       ('2-pin-noi', '2k–2n pin nổi (phim 302,0–356,5 s)', '{p}-pin.wav', None, -14.0),
       ('3-KB1943', 'tấm im lặng KB1943 — chỉ nhạc (phim 549,3–558,6 s)', 'full-{p}.wav', (549.3, 558.6), -17.0),
       ('4-KA2026', 'tấm im lặng KA2026 — chỉ nhạc (phim 716,1–725,0 s)', 'full-{p}.wav', (716.1, 725.0), -17.0)]
# Cặp im lặng: hai bản đưa về CÙNG −17,0 LUFS (≈ mức nhạc tấm im lặng trong bản cả phim −14: −16,3…−17,8) để tai không thiên về bản to hơn.


def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-y', *a], check=True)


def mp3(src, out, cut=None, dich=-14.0, tran=0.84):
    pre = ['-ss', str(cut[0]), '-t', str(round(cut[1] - cut[0], 3))] if cut else []
    fade = f',afade=t=in:d=0.4,afade=t=out:st={round(cut[1] - cut[0] - 0.6, 3)}:d=0.6' if cut else ''
    g = 0.0
    for _ in range(8):   # bù tuyến tính tới |I − đích| ≤ 0,1 LU, hạ trần limiter nếu đỉnh thật (đo trên MP3) > −1 dBTP
        ff(*pre, '-i', src, '-af', f'volume={g:.2f}dB,aresample=192000,alimiter=limit={tran}:attack=1:release=60:level=disabled:asc=1,aresample=48000{fade}', '-c:a', 'libmp3lame', '-b:a', '160k', out)
        E = lib.ebur128(out); ok_tp = E['TP'] <= -1.0; ok_i = abs(E['I'] - dich) <= 0.1
        if ok_tp and ok_i: return E, tran, round(g, 2)
        if not ok_tp: tran = round(tran * 10 ** (-(E['TP'] + 1.0 + 0.1) / 20), 4)
        if not ok_i: g += dich - E['I']
    raise SystemExit(f'{out}: không đạt (I {E["I"]}, TP {E["TP"]}) sau 8 vòng')


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True); K = dict(ghi='MỞ SAU KHI ĐÃ CHẤM. X/Y gán ngẫu nhiên bằng secrets.randbelow(2) cho từng cặp.', cap={})
    for ten, mo_ta, mau, cut, dich in CAP:
        gan = ('A', 'B') if secrets.randbelow(2) == 0 else ('B', 'A'); rec = dict(mo_ta=mo_ta)
        for nhan, p in zip(('X', 'Y'), gan):
            out = os.path.join(dst, f'{ten}-{nhan}.mp3'); E, tran, g = mp3(os.path.join(src, mau.format(p=p)), out, cut, dich)
            rec[nhan] = dict(phuong_an=p, tep=os.path.basename(out), I=E['I'], TP=E['TP'], dich_LUFS=dich, bu_db=g, tran_limiter=tran, sha256=lib.sha256(out), mb=round(os.path.getsize(out) / 1e6, 2))
        K['cap'][ten] = rec
    json.dump(K, open(os.path.join(dst, 'khoa.json'), 'w'), ensure_ascii=False, indent=1)
    for t, r in K['cap'].items(): print(t, {n: (r[n]['I'], r[n]['TP'], r[n]['mb']) for n in 'XY'})
