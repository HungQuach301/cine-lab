#!/opt/cine/bin/python -I
"""ANIMATIC-T4-V2 · việc 6 — SFX mới CC0 (BigSoundBank, Joseph Sardin — "CC0 (public domain): Free and royalty-free", đọc trên trang 25/10/2026): chuông nhà thờ, còi báo động.
Lưu: reports/animatic-t4-v2/sfx/<id>.ogg (mono, −23 LUFS, ≤ 40 s) + sfx.json (trang, dòng giấy phép nguyên văn, SHA tệp gốc + đoạn). UA nghiên cứu, không email."""
import hashlib, json, re, subprocess, urllib.request
from pathlib import Path
R = Path(__file__).resolve().parents[3]; O = R / 'reports/animatic-t4-v2/sfx'; G = Path('/var/tmp/anim/sfx-goc'); G.mkdir(parents=True, exist_ok=True)
UA = 'CineLab-research (+https://github.com/HungQuach301/cine-lab)'
L = [('CHUONG-1', 'https://bigsoundbank.com/4-church-bells-s0829.html', '0829', 'chuông nhà thờ (4 quả)'), ('COI-40', 'https://bigsoundbank.com/national-alert-signal-remalard-61-s3257.html', '3257', 'còi báo động (thay cho còi 1940 — tiếng hú cùng loại, ghi là còi hiện đại)')]
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=300).read()
out = {}
for k, u, n, vai in L:
    h = get(u).decode('utf8', 'replace'); lic = re.search(r'CC0 \(public domain\)[^<(]*', h).group(0).strip(); ten = re.search(r'<title>([^<]*)</title>', h).group(1).strip()
    (O / f'{k}-trang.txt').write_text(re.sub(r'<[^>]+>', ' ', h)[:20000])
    w = G / f'{n}.wav'; w.write_bytes(get(f'https://bigsoundbank.com/UPLOAD/bwf-en/{n}.wav'))
    ogg = O / f'{k}.ogg'
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(w), '-t', '40', '-ac', '1', '-ar', '48000', '-af', 'loudnorm=I=-23:TP=-1:LRA=11', '-c:a', 'libvorbis', '-q:a', '5', str(ogg)], check=True)
    out[k] = dict(id=k, vai=vai, nguon='BigSoundBank', tac_gia='Joseph Sardin', url=u, ten_trang=ten, tep_goc=f'https://bigsoundbank.com/UPLOAD/bwf-en/{n}.wav', giay_phep=lic,
                  sha256_goc=hashlib.sha256(w.read_bytes()).hexdigest(), tep=str(ogg.relative_to(R)), sha256_doan=hashlib.sha256(ogg.read_bytes()).hexdigest(), trang_sha256=hashlib.sha256(h.encode()).hexdigest(), ngay_doc='2026-10-25')
(O / 'sfx.json').write_text(json.dumps(out, ensure_ascii=False, indent=1)); print(json.dumps({k: (v['ten_trang'], v['giay_phep']) for k, v in out.items()}, ensure_ascii=False))
