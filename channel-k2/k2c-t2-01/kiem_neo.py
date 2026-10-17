#!/opt/cine/bin/python
"""K2C-T2-01 · KIỂM ĐỦ ĐIỂM NEO cảnh 3D (G2 §12, chủ dự án 17/10) sau khi sửa lỗi hero.js --resume và vá neo:
mỗi cảnh: (1) số khung có neo = meta.frames, không khung rỗng (trừ cảnh không khai vật có neo); (2) so với lượt dựng trước (danh sách khung thiếu ghi lúc phát hiện);
(3) khung đã vá liền mạch: cùng tập tên neo với khung kề, độ lệch vị trí so với khung kề ≤ max(0,02; 3 × độ lệch lớn nhất giữa hai khung kề tự nhiên của chính cảnh đó).
  kiem_neo.py → g2/kiem-neo.json"""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); O = '/var/tmp/cine-out/k2c-t2-01'
TRUOC = {'r00_launch': [(1, 4)], 'r00_philly': [(49, 84), (193, 206)], 'r01_yards': [(193, 209)], 'p02_jones': [(1, 15)], 'r02_quotes': [(241, 265)], 'r02_subsidy': [(529, 531)],
         'r03_myth': [(49, 88)], 'r03_ladder': [(97, 130)], 'r03_tanker': [(193, 235)], 'r03_scale': [(769, 795)], 'r04_state': [(433, 459)], 'r04_abroad': [(433, 447)],
         'd05_unions2': [(145, 183)], 'r05_fees': [(49, 72)], 'd05_susp': [(1, 19)], 'd05_susp2': [(145, 155)], 'r05_cost': [(193, 228), (337, 343)], 'r05_philly': [(673, 713)],
         'r06_watch': [(193, 200)], 'r06_home': [(1, 41)], 's_loop': [(193, 217)]}
HE = json.load(open(f'{O}/heroes.json')); out = []; ok_all = True
def step(a, b):
    k = [n for n in a if n in b and a[n][2] and b[n][2]]
    return max([abs(a[n][0] - b[n][0]) + abs(a[n][1] - b[n][1]) for n in k] or [0])
for k, v in HE.items():
    m = json.load(open(v['dir'] + '/meta.json')); N = m['frames']; foot = v['hero'].startswith('footage')
    A = json.load(open(v['dir'] + '/anchors.json'))
    thieu = [f for f in range(N) if str(f) not in A] if not foot else []
    co_nguon = any(v['opt'].get(x) for x in ('pins', 'cols', 'props', 'places', 'routes', 'hl', 'page'))   # cảnh không khai vật nào có neo (vd r06_score: chỉ bảng điểm 2D) → neo rỗng là đúng
    rong = [f for f in range(N) if str(f) in A and not A[str(f)] and not foot and co_nguon]
    vao = [f for a, b in TRUOC.get(k, []) for f in range(a, b + 1)]
    nat = max([step(A[str(f)], A[str(f + 1)]) for f in range(N - 1) if str(f) in A and str(f + 1) in A and f not in vao and f + 1 not in vao] or [0])
    lech = []
    for f in vao:
        if str(f) not in A: continue
        for g in (f - 1, f + 1):
            if str(g) in A and 0 <= g < N:
                if set(A[str(f)]) != set(A[str(g)]): lech.append([f, g, 'khác tên neo'])
                elif step(A[str(f)], A[str(g)]) > max(0.02, 3 * nat): lech.append([f, g, round(step(A[str(f)], A[str(g)]), 4)])
    ok = not thieu and not rong and not lech; ok_all &= ok
    out.append(dict(canh=k, khung=N, co_nguon_neo=co_nguon if not foot else None, co_neo=len(A) if not foot else None, thieu=len(thieu), rong=len(rong), da_va=len(vao), thieu_truoc=len(vao), buoc_tu_nhien=round(nat, 4), lech=lech[:5], ket_qua='ĐẠT' if ok else 'TRƯỢT'))
json.dump(dict(ket_qua='ĐẠT' if ok_all else 'TRƯỢT', so_canh=len(out), canh=out), open(f'{H}/g2/kiem-neo.json', 'w'), indent=1, ensure_ascii=False)
for r in out:
    if r['thieu_truoc'] or r['ket_qua'] != 'ĐẠT': print(r['canh'], r['ket_qua'], 'thiếu trước', r['thieu_truoc'], '→ nay', r['thieu'], 'rỗng', r['rong'], 'lệch', r['lech'][:2])
print('TỔNG', 'ĐẠT' if ok_all else 'TRƯỢT', len(out), 'cảnh')
