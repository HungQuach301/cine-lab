#!/opt/cine/bin/python
"""KÊNH 2 · luật đa dạng bối cảnh (chủ dự án 11/10/2026): bối cảnh = cảnh 3D nền của shot (kể cả nền mờ của thẻ).
Đạt khi: không bối cảnh nào > 25 % thời lượng; không đoạn liên tục cùng bối cảnh > 90 s; nửa sau (từ giữa phim) có ≥ 3 bối cảnh.
  settings.py <timeline.json> [--json ra.json]"""
import json, sys
TL = json.load(open(sys.argv[1])); H = TL['heroes']; T = TL['tong_s']
runs = []
for sg in TL['segments']:
    for sh in sg['shots']:
        k = sh['p'].get('hero'); s = H[k]['hero'].split('/')[1] if k else '2d'
        a, b = sg['t0'] + sh['t0'], sg['t0'] + sh['t1']
        if runs and runs[-1][0] == s: runs[-1][2] = b
        else: runs.append([s, a, b])
tot = {}
for s, a, b in runs: tot[s] = tot.get(s, 0) + b - a
longest = max(runs, key=lambda r: r[2] - r[1]); half = {s for s, a, b in runs if b > T / 2}
R = dict(tong_s=round(T, 1), ty_le={s: round(100 * v / T, 1) for s, v in sorted(tot.items(), key=lambda x: -x[1])}, lien_tuc_dai_nhat=[longest[0], round(longest[2] - longest[1], 1), round(longest[1], 1)],
         nua_sau=sorted(half), dat=bool(max(tot.values()) / T <= 0.25 and longest[2] - longest[1] <= 90 and len(half) >= 3))
print(json.dumps(R, ensure_ascii=False))
if '--json' in sys.argv: json.dump(R, open(sys.argv[sys.argv.index('--json') + 1], 'w'), ensure_ascii=False, indent=1)
