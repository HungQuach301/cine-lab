#!/opt/cine/bin/python
"""GIONG-T4 · việc 5: bảng giãn shot ĐỀ XUẤT (KHÔNG sửa BANG-SHOT-v1; animatic sẽ áp).
Lời mỗi shot = mốc thật bản thu G1 ($GL_OUT/stem/moc.json: từ đầu câu đầu tới cuối câu cuối của đoạn gán cho shot — khoa-loi/doan-shot.json).
Luật (như KL42 nhip.py, giản lược): shot có lời phải chứa lời + 0,4 s (luật G1); không cắt lời; không kéo nhịp giọng; làm tròn lên 1/24 s.
Phương án: A = chỉ giãn (shot dư giữ nguyên) · B = A + rút đuôi hình sau lời xuống ≤ ĐUÔI s ở shot có lời đang dư (không rút shot không lời,
khung neo P1 tái xuất, KHOP, cú lặn) · C = B + rút shot không lời ('nối'/'lặng') về sàn đề xuất (chỉ để chủ dự án cân nhắc).
→ reports/giong-t4/gian-shot.json + in bảng (gl_gian_shot.py md → GIAN-SHOT.md phần bảng)."""
import json, math, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import gl_lib as GL   # noqa: E402
PAD, DUOI, FPS = 0.4, 1.5, 24
SAN = {'nối': 6.0, 'lặng': 6.0}   # sàn đề xuất cho shot không lời ở phương án C (≥ 6 s: đủ một cú máy §19 ở tốc độ giới hạn)
md = (GL.EP / 'BANG-SHOT-v1.md').read_text()
ROWS = []
for l in md.splitlines():
    c = [x.strip() for x in l.split('|')]
    if len(c) > 10 and re.match(r'^(M\d\d|H\d-\d\d)$', c[1]):
        ROWS.append(dict(ma=c[1], dai=float(c[3]), loi_v1=c[4], may=c[5], cu=c[6], vai=c[8], lop=c[9]))
M = json.loads((GL.OUT / 'stem/moc.json').read_text())
D = {d['shot']: d for ch in M['chuong'] for d in ch['doan']}
up = lambda x: math.ceil(x * FPS - 1e-6) / FPS
out = []
for r in ROWS:
    d = D.get(r['ma']); l = round(d['kt'] - d['bd'], 3) if d else 0.0
    can = up(l + PAD) if d else 0.0
    A = max(r['dai'], can)
    giu = r['cu'] in ('KHOP', 'LAN') or 'tái xuất' in r['vai'] or 'KHOẢNH KHẮC' in r['vai']
    B = A if (not d or giu) else max(can, min(A, up(l + DUOI)))
    loai = 'có lời' if d else ('PP' if r['cu'] == 'PP' else ('lặng' if 'lặng' in r['loi_v1'] else 'nối'))
    C = B if d or loai == 'PP' or r['cu'] in ('KHOP',) else min(B, max(SAN.get(loai, B), 0))
    md_vuot = r['cu'] == 'MD' and A > 8.0
    out.append(dict(r, loai=loai, loi_that=l, can=round(can, 3), A=round(A, 3), B=round(B, 3), C=round(C, 3), lech_v1=round(A - r['dai'], 3), md_vuot_8s=md_vuot,
                    cau=[c['khoa'] for c in d['cau']] if d else []))
tong = {k: round(sum(x[k] for x in out), 3) for k in ('dai', 'A', 'B', 'C')}
loi_lien = round(sum(ch['giay'] for ch in M['chuong']), 3); loi_shot = round(sum(x['loi_that'] for x in out), 3)
R = dict(luat=dict(pad=PAD, duoi=DUOI, san=SAN, fps=FPS), tong=tong, loi_theo_shot=loi_shot, loi_lien_chuong=loi_lien, muc_tieu=720.0,
         lech_pct={k: round((v / 720 - 1) * 100, 2) for k, v in tong.items()}, shot=out)
(GL.G / 'gian-shot.json').write_text(json.dumps(R, ensure_ascii=False, indent=1) + '\n')
print(json.dumps({k: v for k, v in R.items() if k != 'shot'}, ensure_ascii=False))
if sys.argv[1:] == ['md']:
    print('| Shot | Cú máy | Loại | Dài v1 (s) | Lời thật (s) | Cần (lời + 0,4) | A | B | C | Lệch A − v1 | Ghi chú |\n|---|---|---|---|---|---|---|---|---|---|---|')
    for x in out:
        g = []
        if x['md_vuot_8s']: g.append('M-d > 8 s')
        if x['lech_v1'] > 0: g.append('GIÃN')
        print(f"| {x['ma']} | {x['cu']} | {x['loai']} | {x['dai']:g} | {x['loi_that']:.2f} | {x['can']:.2f} | {x['A']:.2f} | {x['B']:.2f} | {x['C']:.2f} | {x['lech_v1']:+.2f} | {'; '.join(g)} |")
