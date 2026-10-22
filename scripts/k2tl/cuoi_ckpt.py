#!/opt/cine/bin/python
"""BAN-CUOI-T3 · cập nhật khối TRẠNG THÁI trong reports/ban-cuoi-t3/CHECKPOINT.md từ số đo thật (chạy mỗi lần đẩy — cuoi_ckpt.sh và tay):
khung 1080p đã dựng (khung cảnh đinh + quy về 18 288 khung phim), đoạn đã render, N2.9 trọn Cycles (pod, khung đã nhận), lightmap, Omni đã chèn, việc còn lại theo thứ tự, ước giờ còn lại.
Khối nằm giữa <!-- TRANG-THAI --> … <!-- /TRANG-THAI -->; phần còn lại giữ nguyên.   cuoi_ckpt.py [--so-du]  (--so-du: đọc số dư RunPod, ghi một dòng vào reports/ban-cuoi-t3/gio-gpu.jsonl)"""
import datetime as dt, glob, json, os, re, subprocess, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]; CK = REPO / 'reports/ban-cuoi-t3/CHECKPOINT.md'; O = Path('/var/tmp/cine-out/k2c-t3-cuoi'); G = Path('/var/tmp/cine-out/cuoi-gpu'); LG = Path('/var/tmp/cine-out/log')
now = dt.datetime.now(dt.timezone.utc); T0 = dt.datetime(2026, 10, 22, 4, 30, tzinfo=dt.timezone.utc)
H = json.loads((O / 'heroes.json').read_text()); ok = lambda v: (Path(v['dir']) / 'stamp').exists() and (Path(v['dir']) / 'stamp').read_text().strip() == v['stamp']
xong = [k for k, v in H.items() if ok(v)]; con = [k for k in H if k not in xong]
nk = {k: round(v['dur'] * 24) for k, v in H.items()}; dang = {k: len(glob.glob(H[k]['dir'] + '.new/*.jpg')) for k in con}
k_xong = sum(nk[k] for k in xong) + sum(dang.values()); k_tong = sum(nk.values())
TL = json.loads((O / 'timeline.json').read_text()); segs = [s for s in TL['segments']]
co = [s['id'] for s in segs if (O / 'sec' / f"{s['id']}.mkv").exists() and (O / 'sec' / f"{s['id']}.mkv.hash").exists()]
khung_phim = sum(s['frames'] for s in segs if s['id'] in co); tong_phim = TL.get('tong_khung', 18288)
gio = [l.split() for l in (O / 'heroes-gio.log').read_text().splitlines() if l.strip()] if (O / 'heroes-gio.log').exists() else []
spf = [float(x[3]) for x in gio[-10:] if float(x[3]) > 1]; s = sum(spf) / len(spf) if spf else 6.0
P = int((LG / 'P').read_text().strip()) if (LG / 'P').exists() else 2; con_k = sum(nk[k] - dang[k] for k in con); eta = con_k * s / max(P, 1) / 3600
bake = sorted(p.parent.name for p in Path('/var/tmp/cine-out/k2tl-cache/nc/bake').glob('*/meta.json'))
cx = set((O / 'cho-xong.txt').read_text().split()) if (O / 'cho-xong.txt').exists() else set()
mh = json.loads((REPO / 'reports/ban-cuoi-t3/do/minh-hoa-ghep.json').read_text()) if (REPO / 'reports/ban-cuoi-t3/do/minh-hoa-ghep.json').exists() else []
def tail(p, n=1):
    try: return [l for l in Path(p).read_text().splitlines() if l.strip()][-n:] or ['—']
    except Exception: return ['—']
pods = []
for f in sorted(G.glob('pod*.json*')):
    try: d = json.loads(f.read_text()); pods.append(f"{d['lab']} {d['id']} bật {d['bat'][11:16]} UTC" + (' (đã tắt)' if '.json.' in f.name else ' (đang chạy)'))
    except Exception: pass
exr = {d: len(list((G / 'exr' / d).glob('*.exr'))) for d in ('h2t', 'n29', 'n29a') if (G / 'exr' / d).exists()}
if '--so-du' in sys.argv:
    r = subprocess.run(['/opt/cine/bin/python', str(REPO / 'scripts/k2tl/cuoi_gpu/pod.py'), 'du'], capture_output=True, text=True).stdout.strip().splitlines()
    if r: rec = dict(su_kien='so_du', luc=now.strftime('%Y-%m-%dT%H:%M:%SZ'), **json.loads(r[-1])); open(REPO / 'reports/ban-cuoi-t3/gio-gpu.jsonl', 'a').write(json.dumps(rec, ensure_ascii=False) + '\n')
sodu = [json.loads(l) for l in (REPO / 'reports/ban-cuoi-t3/gio-gpu.jsonl').read_text().splitlines() if '"so_du"' in l or '"so_du_sau"' in l]
L = ['<!-- TRANG-THAI -->', f"## Trạng thái ({now.strftime('%d/%m/%Y %H:%M UTC')}) — tự động `scripts/k2tl/cuoi_ckpt.py`", '',
     f"- **Khung cảnh đinh 1080p đã dựng:** {k_xong} / {k_tong} ({100 * k_xong / k_tong:.0f} %) — cảnh xong {len(xong)}/{len(H)}; đang dựng: " + (', '.join(f"{k[5:]} {dang[k]}/{nk[k]}" for k in con if dang[k]) or '—'),
     f"- **Đoạn đã render (sec/*.mkv, quy về khung phim):** {len(co)}/{len(segs)} đoạn = {khung_phim} / {tong_phim} khung phim ({100 * khung_phim / tong_phim:.0f} %). Còn: " + ', '.join(s['id'] for s in segs if s['id'] not in co),
     f"- **Cycles GPU:** H2T 0–119 {'ĐÃ THAY' if 'anim_H2T' in cx else 'chưa thay'} · N2.9 TRỌN Cycles (sửa ghép A↔B trong cú máy, 14:20): khung 396–671 EXR {exr.get('n29', 0)}/276, khung 0–395 EXR {exr.get('n29a', 0)}/396 — "
     + ('ĐÃ THAY + chờ render lại đoạn' if 'anim_N2_9' in cx else 'chưa thay') + '. Pod: ' + ('; '.join(pods) or '—') + f". Dòng cuối: pod3 `{tail(LG / 'pod3.log')[0][:90]}` · pod4 `{tail(LG / 'pod4.log')[0][:90]}` · xuất `{tail(LG / 'gpu_cb2.log')[0][:70]}`",
     f"- **Số dư RunPod:** " + (f"${sodu[-1].get('clientBalance', sodu[-1].get('so_du_sau')):.2f}" if sodu else '—') + ' (dòng `so_du` cuối gio-gpu.jsonl). Đầu phiên $22,95 → $13,97 sau pod 1/2 (chi thật $8,88); 14:57 đọc $28,97 = có nạp thêm $15,00 ngoài phiên, không phải hoàn tiền',
     f"- **Lightmap:** {len(bake)}/7 ({', '.join(bake)})",
     '- **Omni đã chèn (không nhãn):** ' + (', '.join(f"{r['ma']}→{r['shot']}" for r in mh if r.get('chen')) or '—') + ' · M1 giữ 3D',
     f"- **Ước còn:** cảnh đinh {con_k} khung × {s:.1f} s/khung ÷ P {P} ≈ **{eta:.1f} h**; sau đó render đoạn còn lại + LUT + ghép + k2check + xuất ≈ 2–3 h. Giờ máy đã chạy ≈ {(now - T0).total_seconds() / 3600:.1f} h (mốc 30 h).",
     '- **Việc còn lại (thứ tự):** (1) dựng nốt cảnh đinh; (2) chèn M3 (N1.4), M4 (C5) — tự động khi cảnh xong; (3) N2.9 trọn Cycles: pod 3/4 → nhận → render lại đoạn; (4) render các đoạn còn lại (tự động, chờ RAM);'
     ' (5) chốt LUT kênh (bão hoà ≥ 0,40) → ghép master + 3 phần + 8 tệp xem; (6) k2check 1.17.2 `--cap`, selftest, LOI-KHOA 3/3, tự đo, XEM CÂM AI; (7) release-k2-t3-g2 (LFS) + thumbnail; (8) báo cáo, DỪNG.',
     f"- Dòng cuối log vòng dựng: `{tail(LG / 'vong.log')[0][:100]}` · render đoạn: `{tail(LG / 'doan.log')[0][:100]}`",
     '<!-- /TRANG-THAI -->']
t = CK.read_text(); blk = '\n'.join(L)
if '<!-- TRANG-THAI -->' in t: t = re.sub(r'<!-- TRANG-THAI -->.*?<!-- /TRANG-THAI -->', lambda m: blk, t, flags=re.S)
else: t = re.sub(r'## Trạng thái \(cập nhật[^\n]*\n.*?(?=\n## )', lambda m: blk + '\n', t, count=1, flags=re.S)
CK.write_text(t); print(f'{len(xong)}/{len(H)} cảnh · {k_xong}/{k_tong} khung · đoạn {len(co)}/{len(segs)} · ≈ {eta:.1f} h')
