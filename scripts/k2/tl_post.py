#!/opt/cine/bin/python
"""V5b-2b (K-1.13 §8.1) · sau khi dựng cảnh tl (scripts/k2/hero.js → <dir>/meta.json frames_meta), ghi AGL vào timeline.json của tập:
  p.agl = [[giây trong shot, km], …] mỗi 0,5 s + điểm cuối · p.agl_max (km) · p.noi_khung (nơi theo khung của cảnh, nếu cảnh khai) — để NC-H2/H3 đọc thẳng, không suy từ máy quay.
Cảnh BÁO VV2 sau dựng: địa cầu (AGL > 50 km) > 1 lần hoặc một lần > 3 s trên cả tập (theo AGL thật mỗi khung).
  tl_post.py <timeline.json>       (build.sh gọi sau bước cảnh đinh, trước render đoạn)"""
import json, os, sys

FPS = 24


def main(tlp):
    TL = json.load(open(tlp)); runs, cur, changed = [], None, 0
    for sg in TL['segments']:
        for sh in sg['shots']:
            p = sh.get('p') or {}
            if sh.get('tpl') != 'plate' or not p.get('tl') or not p.get('dir'): continue
            try: FM = json.load(open(os.path.join(p['dir'], 'meta.json'))).get('frames_meta') or {}
            except (OSError, ValueError): print(f'CẢNH BÁO: {p["dir"]}/meta.json chưa có (dựng cảnh trước)', file=sys.stderr); continue
            if not FM: continue
            n = max(int(k) for k in FM) + 1; d = sh['t1'] - sh['t0']; pts = []
            k = 0.0
            while True:
                f = min(n - 1, int(round(p.get('off', 0) + k * FPS * p.get('speed', 1)))); m = FM.get(str(f)) or FM.get(f)
                if m: pts.append([round(k, 2), m['agl_km']])
                if k >= d - 1e-6: break
                k = min(d, k + 0.5)
            p['agl'] = pts; p['agl_max'] = max(a for _, a in pts) if pts else None; changed += 1
            for q in pts:
                g = q[1] > 50; t = sg['t0'] + sh['t0'] + q[0]
                if g and cur is None: cur = [t, t]
                elif g: cur[1] = t
                elif cur: runs.append(cur); cur = None
    if cur: runs.append(cur)
    json.dump(TL, open(tlp, 'w'), indent=1, ensure_ascii=False)
    if len(runs) > 1: print(f'CẢNH BÁO VV2: địa cầu (AGL > 50 km) {len(runs)} lần', file=sys.stderr)
    for a, b in runs:
        if b - a > 3: print(f'CẢNH BÁO VV2: địa cầu {a:.1f}–{b:.1f} s dài {b - a:.1f} s > 3 s', file=sys.stderr)
    print(json.dumps(dict(shot_tl=changed, dia_cau=runs)))


if __name__ == '__main__':
    main(sys.argv[1])
