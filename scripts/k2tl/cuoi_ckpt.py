#!/opt/cine/bin/python
"""BAN-CUOI-T3 (bản sao anim_ckpt.py, đường bản cuối) · cập nhật khối TRẠNG THÁI TỰ ĐỘNG trong reports/ban-cuoi-t3/CHECKPOINT.md từ log dựng thật (cảnh xong/còn, khung, giờ ước, tệp ngoài git + SHA).
Khối nằm giữa hai dấu <!-- TRANG-THAI --> … <!-- /TRANG-THAI -->; phần còn lại của tệp giữ nguyên.
  anim_ckpt.py            (chỉ ghi tệp; commit/đẩy do anim_ckpt.sh)"""
import datetime as dt, hashlib, json, os, re
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]; CK = REPO / os.environ.get('ANIM_CK', 'reports/ban-cuoi-t3/CHECKPOINT.md'); O = Path('/var/tmp/cine-out/k2c-t3-cuoi')
H = json.loads((O / 'heroes.json').read_text()) if (O / 'heroes.json').exists() else {}; xong, con = [], []
for k, v in sorted(H.items()):
    d = Path(v['dir']); ok = (d / 'stamp').exists() and (d / 'stamp').read_text().strip() == v['stamp']; n = int(round(v['dur'] * 24))
    if ok: xong.append((k, n))
    else:
        nn = Path(str(d) + '.new'); have = len([p for p in nn.glob('*.jpg')]) if nn.exists() else 0; con.append((k, n, have))
gio = [l.split() for l in (O / 'heroes-gio.log').read_text().splitlines() if l.strip()] if (O / 'heroes-gio.log').exists() else []
spf = [float(x[3]) for x in gio[-12:] if float(x[3]) > 1]; s = sum(spf) / len(spf) if spf else 4.0
khung_con = sum(n - h for _, n, h in con); P = 3; eta_h = khung_con * s / P / 3600
vong = (Path('/var/tmp/cine-out/log/vong.log').read_text().splitlines() or [''])[-1] if Path('/var/tmp/cine-out/log/vong.log').exists() else '(chưa chạy vòng dựng)'
def sha(p):
    p = Path(p); return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else '—'
now = dt.datetime.now(dt.timezone.utc).strftime('%d/%m/%Y %H:%M UTC')
L = [f'<!-- TRANG-THAI -->', f'## Trạng thái tự động ({now}) — `scripts/k2tl/anim_ckpt.py`', '',
     f'- Cảnh đinh XONG: **{len(xong)}/{len(H)}** ({sum(n for _, n in xong)} khung) · CÒN: **{len(con)}** ({khung_con} khung chưa dựng).',
     f'- s/khung TB 12 cảnh gần nhất (mỗi tiến trình, P = 3): {s:.2f} → ước còn **≈ {eta_h:.1f} h** dựng cảnh đinh; sau đó: ghép cú lặn → render đoạn → ghép master → LOOK-4 → xuất (≈ 1,5 h).',
     f'- Dòng cuối log vòng: `{vong.strip()}`',
     '- Xong: ' + ', '.join(k.replace('anim_', '') for k, _ in xong),
     '- Còn: ' + ', '.join(f"{k.replace('anim_', '')} ({h}/{n})" for k, n, h in con), '',
     '| Tệp ngoài git | SHA-256 | Tái tạo |', '|---|---|---|',
     f'| `/var/tmp/cine-out/k2c-t3-cuoi/mix/mix.wav` | `{sha(O / "mix/mix.wav")}` | `scripts/k2tl/cuoi_mix.py channel-k2/k2c-t3-01/cuoi/anim-loi.json <su-kien-cuoi.json> <ra>` |',
     '| cảnh đinh 1080p `/var/tmp/cine-out/hero/k2c-t3-cuoi-anim_*` | (stamp từng cảnh) | `build.sh channel-k2/k2c-t3-01/cuoi/episode.yaml prep` (chặn mạng) → `anim_vong2.sh` |',
     '| lightmap 7 mốc `$K2TL_CACHE/nc/bake/b*/` | meta `reports/ban-cuoi-t3/do/nuong-*.json` | `NUONG_META=reports/ban-cuoi-t3/do bash scripts/k2tl/anim_nuong.sh` |',
     '<!-- /TRANG-THAI -->']
t = CK.read_text(); blk = '\n'.join(L)
t = re.sub(r'<!-- TRANG-THAI -->.*?<!-- /TRANG-THAI -->', lambda m: blk, t, flags=re.S) if '<!-- TRANG-THAI -->' in t else t.replace('\n## Xong', '\n' + blk + '\n\n## Xong', 1)
CK.write_text(t); print(f'{len(xong)}/{len(H)} xong · còn {khung_con} khung · ≈ {eta_h:.1f} h')
