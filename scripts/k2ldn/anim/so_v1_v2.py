#!/opt/cine/bin/python
"""ANIMATIC-T4 · bảng so BANG-SHOT v1 ↔ v2 theo NHÓM LỜI (shot v1) → reports/animatic-t4/SO-V1-V2.md: dài v1 → v2 (K1-C1), cú máy, điểm máy, lớp, đổi gì + căn cứ."""
import json, re
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'
v1 = []
for l in (EP / 'BANG-SHOT-v1.md').read_text().splitlines():
    c = [x.strip() for x in l.split('|')]
    if len(c) > 10 and re.match(r'^(M\d\d|H\d-\d\d)$', c[1]): v1.append(dict(ma=c[1], dai=float(c[3]), loi=c[4], dm=c[5], cu=c[6], moc=c[7], lop=c[9]))
B = json.loads((EP / 'BANG-SHOT-v2.json').read_text()); v2 = B['shot']
L = ['# BẢNG SO BANG-SHOT v1 ↔ v2 — K2C-T4-02 (ANIMATIC-T4, 24/10/2026)', '', '> Sinh bằng `scripts/k2ldn/anim/so_v1_v2.py`. Mỗi dòng = một nhóm lời (shot v1); v2 có thể tách nhóm thành nhiều shot. Thứ tự theo v2 (H1-12 trước H1-11).', '',
     '| Nhóm v1 | v1: dài · máy · cú · lớp | v2: shot · dài · máy · cú · lớp | Δ dài (s) | Đổi + căn cứ |', '|---|---|---|---|---|']
seen = []
for r in v2:
    g = r['nhom_loi']
    if g in seen: continue
    seen.append(g); a = next(x for x in v1 if x['ma'] == g); bs = [x for x in v2 if x['nhom_loi'] == g]
    d2 = sum(x['dur'] for x in bs); doi = []
    if len(bs) > 1: doi.append(f'tách {len(bs)} shot')
    if any(x['cu_may'] == 'MD' for x in bs) and a['cu'] != 'MD': doi.append('thêm M-d (Q1 20–23 %)')
    if a['cu'] == 'MD' and len(bs) > 1: doi.append('M-d > 8 s tách (GIAN-SHOT §6)')
    if all(x['cu_may'] != 'MD' for x in bs) and a['cu'] == 'MD': doi.append('M-d → 3D')
    if a['dm'] == 'P1' or any(x['diem_may'] == 'P1' for x in bs): doi.append('P1 fov 36° (V5)')
    if 'B (' in a['lop']: doi.append('Cycles → cách A look2.js (V2 = a, §14.2)')
    if 'N2P' in a['lop'] and not any('N2P' in x['lop'] for x in bs): doi.append('bỏ tấm nền (V1: chỉ 2026 ngày)')
    if g in ('H1-11', 'H1-12'): doi.append('đổi chỗ H1-11 ↔ H1-12 (GIAN-SHOT §6)')
    if g == 'H1-05': doi.append('thẻ Pepys → H1-05')
    if g == 'H2-02': doi.append('thẻ Hooke → H2-02 (L45 bỏ)')
    if g == 'H3-02': doi.append('năm 1758 (LMA, V09)')
    if g == 'H5-05': doi.append('tách 2 cú máy (GIAN-SHOT §6)')
    if g == 'H2-11': doi.append('Ogilby không lên hình (D13) → 3D XUONG 1676')
    for x in bs:
        if x['diem_may'] in ('P2', 'P3', 'P9') : doi.append(f"{x['diem_may']} nâng ≥ 120 m (GOC-CAO-60)"); break
    s2 = '<br>'.join(f"{x['ma']} · {x['dur']:.3f} · {x['diem_may']} · {x['cu_may']} · {', '.join(f'{k} {v:g}' for k, v in x['lop'].items())}" for x in bs)
    L.append(f"| {g} | {a['dai']:g} · {a['dm']} · {a['cu']} · {a['lop']} | {s2} | {d2 - a['dai']:+.3f} | {'; '.join(dict.fromkeys(doi))} |")
t1 = sum(x['dai'] for x in v1); t2 = sum(x['dur'] for x in v2)
L += ['', f'**Tổng:** v1 {t1:g} s · {len(v1)} shot → v2 {t2:.3f} s · {len(v2)} shot (K1-C1 730,083 s, +1,40 % so 720 s).']
(REPO / 'reports/animatic-t4/SO-V1-V2.md').write_text('\n'.join(L) + '\n'); print(len(seen), t1, round(t2, 3))
