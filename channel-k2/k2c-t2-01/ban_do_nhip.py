#!/opt/cine/bin/python
"""K2C-T2-01 · BẢN ĐỒ NHỊP (Dựng, Mốc B — G2): từ timeline THẬT của bản dựng (timeline.json), mix.json và đặc tả đã giải (est.py → episode-resolved.yaml).
Mỗi chương: khoảng giây, đoạn nhạc (tệp, điểm vào, chồng mép), các shot (giây vào, loại, cảnh), SFX với độ lệch so với mối cắt
(âm < 0 = J: tiếng vào trước hình; âm kéo qua mối cắt sau = L: tiếng ở lại sau hình), biến cố hình (số, khoảng TB, khoảng dài nhất).
  ban_do_nhip.py <thư mục out bản dựng> [--resolved <episode-resolved.yaml>] → g2/BAN-DO-NHIP.md"""
import importlib.util, json, os, sys
import yaml
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(f'{H}/../..')
O = sys.argv[1]; RP = sys.argv[sys.argv.index('--resolved') + 1] if '--resolved' in sys.argv else '/var/tmp/cine-out/k2c-t2-01-est/episode-resolved.yaml'
TL = json.load(open(f'{O}/timeline.json')); MX = json.load(open(f'{O}/mix.json')); R = yaml.safe_load(open(RP))
sp = importlib.util.spec_from_file_location('k2rhythm', f'{REPO}/scripts/k2/rhythm.py'); rh = importlib.util.module_from_spec(sp); sp.loader.exec_module(rh)
mmss = lambda s: f'{int(s // 60)}:{s % 60:04.1f}'
L = ['# K2C-T2-01 — BẢN ĐỒ NHỊP (Dựng, G2)', '',
     f'Sinh bởi `ban_do_nhip.py` từ timeline thật ({TL["tong_s"]:.1f} s), mix.json (master {MX["master"]["I"]} LUFS, {MX["master"]["TP"]} dBTP, nén lời {MX["duck_db"]} dB) và đặc tả đã giải.',
     'SFX: "J −x s" = tiếng vào trước mối cắt x giây; "L +y s" = tiếng còn y giây sau mối cắt kế tiếp. Nhạc: mỗi chương một đoạn, chồng mép (xfade) ở ranh chương.', '']
RS = {s['id']: s for s in R['segments']}
for sg in TL['segments']:
    t0, t1 = sg['t0'], sg['t1']; rs = RS[sg['id']]
    T = sorted(t for t in rh.spec_times(R, rs) if 0 <= t < rs['dur']) + [rs['dur']]
    gaps = [b - a for a, b in zip(T, T[1:])]
    mus = [m for m in MX['music_used'] if m['t0'] <= t0 + 1 < m['t1']]
    L += [f'## {sg["id"]} · {sg.get("part", "")} · {mmss(t0)}–{mmss(t1)} ({t1 - t0:.1f} s)', '',
          f'- Nhạc: ' + '; '.join(f'`{os.path.basename(m["file"])}` từ {m["ss"]:.2f} s nguồn, {mmss(m["t0"])}–{mmss(m["t1"])}' for m in mus),
          f'- Biến cố hình: {len(T) - 1} · khoảng TB {sum(gaps) / len(gaps):.2f} s · dài nhất {max(gaps):.2f} s', '',
          '| Vào | Shot | Loại | Cảnh | SFX (J/L) |', '|---|---|---|---|---|']
    cuts = [t0 + sh['t0'] for sh in sg['shots']] + [t1]

    def owner(st):   # SFX thuộc shot có mối cắt ngay sau nó trong vòng 1,5 s (J), không thì shot chứa nó
        for i in range(len(cuts) - 1):
            if 0 < cuts[i] - st <= 1.5: return i
        return max(i for i in range(len(cuts) - 1) if cuts[i] <= st + 1e-6)
    for i, sh in enumerate(sg['shots']):
        a, b = cuts[i], cuts[i + 1]; fx = []
        for s in sg.get('sfx') or []:
            st = s['at_abs']; en = st + s.get('dur', 0)
            if owner(st) != i: continue
            lead = st - a; tail = en - b
            tag = f'J −{-lead:.1f} s' if lead < -0.05 else f'+{lead:.1f} s'
            if tail > 0.05: tag += f', L +{tail:.1f} s'
            fx.append(f'{os.path.basename(s["file"]).replace(".mp3", "")} ({tag})')
        L.append(f'| {mmss(a)} | {i} | {sh.get("type", "")} | {sh["p"].get("hero", "")} | {"; ".join(fx)} |')
    L.append('')
open(f'{H}/g2/BAN-DO-NHIP.md', 'w').write('\n'.join(L) + '\n'); print(f'{H}/g2/BAN-DO-NHIP.md')
