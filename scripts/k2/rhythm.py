#!/opt/cine/bin/python
"""KÊNH 2 · đo NHỊP THỊ GIÁC (Kinh thánh kênh 2 §4, chủ dự án 14/10/2026 18:08; phiên V2b).
Luật: trung bình ≤ 3,5 s có một biến cố hình mới (máy đổi hướng/tầm, vùng/tuyến/sticker/số liệu xuất hiện, chuyển bảng màu, cắt cảnh);
cắt cứng chỉ khi đổi cảnh; không giữ khung tĩnh > 6 s.
Khai biến cố ở đặc tả: segments[].beats: [{t (giây trong đoạn), k: cut|cam|region|route|ring|sticker|number|label|text|palette|score, s}].
  rhythm.py <spec.yaml> [--mp4 <shot.mp4>] [--json out.json]
Đo:
  (1) mỗi biến cố khai phải KHỚP một mốc thật trong đặc tả (±0,3 s): opt (sepia/natural, regions.at, routes.draw, rings.t, cols.t, cam[].t, walkers.t, props.t)
      và p (places/tags/stickers at, cap at, year at, side.lines at, score corner/board/rows at); 'cut' = đầu đoạn. Không khớp → LỖI.
  (2) số biến cố (gộp biến cố cách nhau < 0,25 s), khoảng trung bình = thời lượng / số biến cố, khoảng dài nhất (kể cả tới cuối cuộn).
  (3) --mp4: khung tĩnh — chuỗi khung liên tiếp có sai khác trung bình < 0,6/255 (ảnh xám 160×90) dài nhất (giây).
Mã thoát 1 nếu: biến cố không khớp, trung bình > 3,5 s, khoảng dài nhất > 6 s, hoặc khung tĩnh > 6 s."""
import json, subprocess, sys
import yaml

TOL, MERGE, MEAN_MAX, GAP_MAX = 0.3, 0.25, 3.5, 6.0


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def num(v):
    return float(v) if isinstance(v, (int, float)) else None


def spec_times(E, sg):
    """mọi mốc thời gian (giây trong đoạn) mà đặc tả thật sự làm xuất hiện/đổi cái gì đó"""
    T = {0.0}
    HZ = E.get('heroes') or {}
    for sh in sg.get('shots', []):
        off = num(sh.get('at', 0)) or 0.0; T.add(off); p = sh.get('p') or {}; h = HZ.get(p.get('hero')) or {}; o = h.get('opt') or {}
        add = lambda v, base=off: T.add(base + v) if num(v) is not None and v >= 0 else None
        for k in ('sepia', 'natural'):
            if isinstance(o.get(k), list): add(o[k][0])
        for r in o.get('regions', []): add(r['at'][0] if isinstance(r.get('at'), list) else r.get('at'))
        for r in o.get('routes', []): add(r['draw'][0] if isinstance(r.get('draw'), list) else r.get('draw'))
        for r in o.get('rings', []): add(r.get('t'))
        for c in o.get('cols', []): add((c.get('t') or [None])[0])
        for c in o.get('cam', []) if isinstance(o.get('cam'), list) else []: add(c.get('t'))
        for w in o.get('walkers', []): add((w.get('t') or [None])[0])
        for q in o.get('props', []): add(q.get('t'))
        if isinstance(o.get('close'), dict): add((o['close'].get('at') or [None])[0])   # V4: tầng gần của zoom nhiều tầng hoà vào
        add = lambda v, base=0.0: T.add(base + v) if num(v) is not None and v >= 0 else None   # V4: mốc lớp 2D (p.*) là giây TRONG ĐOẠN (k2.js vis(t, at), t = giờ đoạn) — không cộng mốc shot
        for k in ('places', 'tags', 'stickers', 'labels'):
            for x in p.get(k, []) or []:
                if isinstance(x, dict): add(x.get('at'))
        for c in p.get('cap', []) or []: add(c.get('at'))
        if isinstance(p.get('year'), dict): add(p['year'].get('at'))
        sd = p.get('side') or {}
        add(sd.get('at'))
        for l in sd.get('lines', []): add(l.get('at'))
        sc = p.get('score') or {}
        for part in ('corner', 'board'):
            if sc.get(part): add(sc[part].get('at'))
        for r in (sc.get('board') or {}).get('rows', []): add(r.get('at'))
        for sd2 in (sc.get('corner') or {}).get('sides', []):
            if isinstance(sd2.get('n'), list):
                for e in sd2['n']: add(e.get('t'))
    return sorted(T)


def static_runs(mp4):
    """khung tĩnh dài nhất (giây): sai khác trung bình giữa hai khung liên tiếp (xám 160×90) < 0,6/255"""
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-vf', 'scale=160:90,format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(np.float32); d = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2))
    best = run = 0; at = 0
    for i, v in enumerate(d):
        run = run + 1 if v < 0.6 else 0
        if run > best: best, at = run, i - run + 1
    return round(best / 24, 2), round(at / 24, 2), round(float(np.median(d)), 3)


def main():
    E = yaml.safe_load(open(sys.argv[1])); t_abs = 0.0; ev = []; bad = []; per = []
    for sg in E['segments']:
        dur = float(sg['dur']); T = spec_times(E, sg); B = sg.get('beats') or []
        if not any(b.get('k') == 'cut' and float(b['t']) == 0 for b in B): bad.append(f'{sg["id"]}: thiếu biến cố cut ở 0 (đầu đoạn = cắt cảnh)')
        for b in B:
            t = float(b['t'])
            if not any(abs(t - x) <= TOL for x in T): bad.append(f'{sg["id"]} {t:.2f}s {b.get("k")} "{b.get("s")}": không khớp mốc nào trong đặc tả (±{TOL} s)')
            ev.append((t_abs + t, sg['id'], b.get('k'), b.get('s')))
        per.append(dict(doan=sg['id'], dur=dur, bien_co=len(B)))
        t_abs += dur
    ev.sort(); U = []
    for e in ev:
        if not U or e[0] - U[-1][0] >= MERGE: U.append(e)
    gaps = [b[0] - a[0] for a, b in zip(U, U[1:])] + [t_abs - U[-1][0]]
    mean = t_abs / len(U); gmax = max(gaps); ig = gaps.index(gmax)
    out = dict(tong_s=round(t_abs, 2), bien_co_khai=len(ev), bien_co_gop=len(U), khoang_tb_s=round(mean, 2), khoang_dai_nhat_s=round(gmax, 2),
               khoang_dai_nhat_tu=f'{U[ig][1]} {U[ig][0]:.2f}s ({U[ig][2]})', cat_cung=sum(1 for e in ev if e[2] == 'cut'), theo_doan=per, loi=bad)
    if arg('mp4'):
        s, at, med = static_runs(arg('mp4')); out.update(khung_tinh_dai_nhat_s=s, khung_tinh_tu_s=at, sai_khac_trung_vi=med)
    ok = not bad and mean <= MEAN_MAX and gmax <= GAP_MAX and out.get('khung_tinh_dai_nhat_s', 0) <= GAP_MAX
    out['ket_qua'] = 'ĐẠT' if ok else 'TRƯỢT'
    if arg('json'): json.dump(out, open(arg('json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False, indent=1)); sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
