#!/opt/cine/bin/python
"""P-2010b · việc 1 bước 4: master lời từ stem ghép lại — CÙNG cách chuẩn của reports/kl42/xuat.py (−14 LUFS, alimiter trên tín hiệu nâng mẫu ×4,
trần 0,84 ≈ −1,5 dBFS, bù tuyến tính tới khi lệch ≤ 0,1 LU và đỉnh thật ≤ −1 dBTP, ≤ 4 vòng; FLAC mức nén 8). Không tạo bản xem (bản xem gốc giữ trong git).
→ $P_OUT/master/T3-loi-G1-v42-14LUFS.{wav,flac}; reports/p2010b/xuat-lai.json"""
import json, os, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; R = H.parents[1]; PO = Path(os.environ.get('P_OUT', '/var/tmp/cine-out/p2010b'))
sys.path.insert(0, str(R / 'scripts/audio')); import lib   # noqa: E402
X = PO / 'master'; X.mkdir(parents=True, exist_ok=True)
SRC = PO / 'stem/T3-loi-tho.wav'; WAV = X / 'T3-loi-G1-v42-14LUFS.wav'; FLAC = X / 'T3-loi-G1-v42-14LUFS.flac'
I_T, TP_T, CEIL = -14.0, -1.0, 0.84


def ff(src, dst, af, codec='pcm_s24le'):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-af', af, '-ar', '48000', '-ac', '1', '-c:a', codec, str(dst)], check=True)


def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


m0 = lib.ebur128(str(SRC)); g = I_T - m0['I']; vong = []
for k in range(4):
    ff(SRC, WAV, f'volume={g:.3f}dB,aresample=192000,alimiter=limit={CEIL}:attack=1:release=60:level=false,aresample=48000')
    m = lib.ebur128(str(WAV)); vong.append(dict(gain_db=round(g, 3), **m))
    if abs(m['I'] - I_T) <= 0.1 and m['TP'] <= TP_T: break
    g += I_T - m['I']
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(WAV), '-c:a', 'flac', '-compression_level', '8', str(FLAC)], check=True)
KL = json.loads((R / 'reports/kl42/xuat.json').read_text())
out = dict(nguon_tho=dict(tep=str(SRC), sha256=lib.sha256(str(SRC)), **m0), vong=vong,
           master=dict(wav=str(WAV), wav_sha256=lib.sha256(str(WAV)), flac=str(FLAC), flac_sha256=lib.sha256(str(FLAC)), giay=round(dur(WAV), 3),
                       giay_flac=round(dur(FLAC), 3), byte_wav=WAV.stat().st_size, byte_flac=FLAC.stat().st_size, **vong[-1]),
           kl42=dict(stem_tho=KL['nguon_tho'], master=KL['master'], vong=KL['vong']))
json.dump(out, open(H / 'xuat-lai.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(dict(tho=m0, vong=vong, master={k: out['master'][k] for k in ('wav_sha256', 'flac_sha256', 'giay', 'giay_flac', 'byte_wav', 'byte_flac')},
                      kl42_master={k: KL['master'][k] for k in KL['master'] if k not in ('wav', 'flac')}), ensure_ascii=False, indent=1))
