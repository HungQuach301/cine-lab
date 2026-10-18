#!/opt/cine/bin/python
"""CASTING-GIỌNG · gói nghe mù: nghe_mu.py <ma> [<ma> …] (các giọng ĐẠT máy kiểm, gồm đối chứng)
→ nghe-mu/G1.mp3 … Gn.mp3 (thứ tự ngẫu nhiên bằng secrets, stereo 112 kb/s, đo lại −14 LUFS / ≤ −1 dBTP trên chính tệp phát hành)
→ khoa-ten.json (G ↔ mã nội bộ; KHÔNG mở trước khi chấm)."""
import json, os, secrets, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cg_lib as L, kiem_lib as K
sys.path.insert(0, str(K.R / 'scripts/audio')); import lib as AL
H = os.path.dirname(os.path.abspath(__file__)); os.makedirs(f'{H}/nghe-mu', exist_ok=True)
ma = sys.argv[1:]; thu_tu = ma[:]
for i in range(len(thu_tu) - 1, 0, -1):
    j = secrets.randbelow(i + 1); thu_tu[i], thu_tu[j] = thu_tu[j], thu_tu[i]
khoa = {}
for i, m in enumerate(thu_tu, 1):
    g = f'G{i}'; R = json.load(open(f'{L.OUT}/kiem-{m}.json')); src = f'{L.OUT}/{m}-noi.wav'; out = f'{H}/nghe-mu/{g}.mp3'
    # stereo dual-mono (như bản phát YouTube; đo mono thấp hơn ≈ 3 LU) · gain + alimiter (trần mẫu −2,5 dBFS) · lặp gain tới −14,0 ± 0,1 LUFS
    gain, lim = 7.0, 0.75
    for _ in range(8):
        af = f'volume={gain:.3f}dB,alimiter=limit={lim}:level=false:attack=2:release=80'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', af, '-ac', '2', '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '112k', '-map_metadata', '-1', out], check=True)
        M = AL.ebur128(out)
        if abs(M['I'] + 14) <= 0.1 and M['TP'] <= -1.0: break
        if M['TP'] > -1.0: lim *= 0.95
        gain += -14 - M['I']
    khoa[g] = dict(limiter=round(lim, 3), gain_dB=round(gain, 2), ma=m, voice_id=R['voice_id'], I=M['I'], TP=M['TP'], giay=round(K.dur(out), 2), sha256=AL.sha256(out), mb=round(os.path.getsize(out) / 1e6, 2))
    print(g, khoa[g]['I'], khoa[g]['TP'], khoa[g]['mb'])
json.dump(dict(ghi='KHOÁ TÊN — chỉ mở SAU khi chủ dự án đã chấm xong. Thứ tự G do secrets.randbelow (Fisher–Yates) sinh, không chọn tay.', G=khoa),
          open(f'{H}/khoa-ten.json', 'w'), ensure_ascii=False, indent=1)
