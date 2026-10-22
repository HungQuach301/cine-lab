"""SFX-T3 · gói nghe mù: 2 cặp X/Y (bản KHÔNG SFX vs bản CÓ SFX), MP3 160 kb/s, −14,0 ± 0,1 LUFS, đỉnh thật ≤ −1 dBTP đo trên CHÍNH tệp MP3
(dùng nguyên hàm mp3() của reports/nhac-t3/cong-cu/goi_nghe.py; BAI-HOC-LL #69, #121). Gán X/Y ngẫu nhiên (secrets), ghi khoa.json.
  goi_nghe.py <thư mục wav (tron_thu.py)> <thư mục ra>"""
import json, os, secrets, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts/audio')); sys.path.insert(0, os.path.join(ROOT, 'reports/nhac-t3/cong-cu'))
import lib, importlib.util
spec = importlib.util.spec_from_file_location('gn_nt3', os.path.join(ROOT, 'reports/nhac-t3/cong-cu/goi_nghe.py')); gn = importlib.util.module_from_spec(spec); spec.loader.exec_module(gn)
CAP = [('1-moc', 'móc mở đầu H1–H3 + đầu N1.1 (phim 0,0–45,0 s)', 'moc'), ('2-pin-noi', 'pin nổi 13/9/1782: cuối N2.8 + N2.9 + đầu N2.11 (phim 321,0–358,0 s)', 'pin')]
src, dst = sys.argv[1], sys.argv[2]; os.makedirs(dst, exist_ok=True)
K = dict(ghi='MỞ SAU KHI ĐÃ CHẤM. X/Y gán ngẫu nhiên bằng secrets.randbelow(2) cho từng cặp. "khong-sfx" = nhạc B + lời G1; "co-sfx" = cùng bản + SFX/âm nền đề xuất.', cap={})
for ten, mo_ta, d in CAP:
    gan = ('khong-sfx', 'co-sfx') if secrets.randbelow(2) == 0 else ('co-sfx', 'khong-sfx'); rec = dict(mo_ta=mo_ta)
    for nhan, p in zip(('X', 'Y'), gan):
        out = os.path.join(dst, f'{ten}-{nhan}.mp3'); E, tran, g = gn.mp3(os.path.join(src, f'{d}-{p}.wav'), out, None, -14.0)
        rec[nhan] = dict(ban=p, tep=os.path.basename(out), I=E['I'], TP=E['TP'], dich_LUFS=-14.0, bu_db=g, tran_limiter=tran, sha256=lib.sha256(out), mb=round(os.path.getsize(out) / 1e6, 3))
    K['cap'][ten] = rec
json.dump(K, open(os.path.join(dst, 'khoa.json'), 'w'), ensure_ascii=False, indent=1)
for t, r in K['cap'].items(): print(t, {n: (r[n]['I'], r[n]['TP'], r[n]['mb']) for n in 'XY'})
