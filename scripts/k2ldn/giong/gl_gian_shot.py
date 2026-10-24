#!/opt/cine/bin/python
"""GIONG-T4 · việc 5: bảng giãn shot ĐỀ XUẤT (KHÔNG sửa BANG-SHOT-v1; animatic sẽ áp).
Lời mỗi shot = mốc thật bản thu G1 ($GL_OUT/stem/moc.json: từ đầu câu đầu tới cuối câu cuối của đoạn gán cho shot — khoa-loi/doan-shot.json).
Luật (như KL42 nhip.py, giản lược): shot có lời phải chứa lời + 0,4 s (luật G1); không cắt lời; không kéo nhịp giọng; làm tròn lên 1/24 s.
Phương án: A = chỉ giãn (shot dư giữ nguyên) · B = A + rút đuôi hình sau lời xuống ≤ ĐUÔI s ở shot có lời đang dư (không rút shot không lời,
khung neo P1 tái xuất, KHOP, cú lặn) · C = B + rút shot không lời ('nối'/'lặng') về sàn đề xuất (chỉ để chủ dự án cân nhắc).
Phương án lời: K0 = giữ đủ lời khoá · K1 = bỏ NGUYÊN CÂU trong dựng (không thu lại; CAT bên dưới — chờ chủ dự án).
→ reports/giong-t4/gian-shot.json + in bảng (gl_gian_shot.py md → GIAN-SHOT.md phần bảng)."""
import json, math, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import gl_lib as GL   # noqa: E402
PAD, DUOI, FPS = 0.4, 1.5, 24
SAN = {'nối': 6.0}   # sàn đề xuất cho shot 'nối' ở phương án C (≥ 6 s: đủ một cú máy §19 ở tốc độ giới hạn); 'lặng'/KHOP/PP giữ, trừ H5-08 (kéo lùi cuối 28 → 18 s, giữ 6 s lặng)
SAN_RIENG = {'H5-08': 18.0}
md = (GL.EP / 'BANG-SHOT-v1.md').read_text()
ROWS = []
for l in md.splitlines():
    c = [x.strip() for x in l.split('|')]
    if len(c) > 10 and re.match(r'^(M\d\d|H\d-\d\d)$', c[1]):
        ROWS.append(dict(ma=c[1], dai=float(c[3]), loi_v1=c[4], may=c[5], cu=c[6], vai=c[8], lop=c[9]))
M = json.loads((GL.OUT / 'stem/moc.json').read_text())
D = {d['shot']: d for ch in M['chuong'] for d in ch['doan']}
CAT = ['L81', 'L41b', 'L45', 'L38', 'L77', 'L15', 'L54']   # câu đề xuất bỏ ở K1 (xem PHIEU-GIONG.md)
SO = json.loads((GL.EP / 'khoa-loi/so-nhap-khoa.json').read_text()); SUA = {x['L']: x for x in json.loads((GL.EP / 'khoa-loi/sua-v2.json').read_text())}
CATK = {'L41b': 'Four classes of house'}   # nửa sau L41 (tách ở dấu chấm)
def ma_cau(c):
    for x in SO:
        if c in x['khoa'] or x['khoa'].startswith(c[:40]): return x['L']
def tiet_kiem(d, cat):
    cs = d['cau']; bo = 0.0
    for k, c in enumerate(cs):
        L = ma_cau(c['khoa']); hit = (L in cat and L != 'L41') or ('L41b' in cat and c['khoa'].startswith(CATK['L41b']))
        if L == 'L15' and 'L15' in cat: hit = c['khoa'].startswith('"I have been')
        if L == 'L14': hit = False
        if hit: bo += (c['kt'] - c['bd']) + ((cs[k + 1]['bd'] - c['kt']) if k + 1 < len(cs) else (c['bd'] - cs[k - 1]['kt'] if k else 0.0))
    return bo
up = lambda x: math.ceil(x * FPS - 1e-6) / FPS
def tinh(cat, duoi, san_noi, san_rieng):
  out = []
  for r in ROWS:
      d = D.get(r['ma']); l = round(d['kt'] - d['bd'] - tiet_kiem(d, cat), 3) if d else 0.0
      lang = float(m.group(1)) if (m := re.search(r'lặng (\d+) s', r['loi_v1'])) else 0.0   # lặng có chủ ý trong bảng v1 (giữ)
      can = up(l + PAD + lang) if d else 0.0
      A = max(r['dai'], can)
      giu = r['cu'] in ('KHOP', 'LAN') or 'tái xuất' in r['vai'] or 'KHOẢNH KHẮC' in r['vai']
      B = A if (not d or giu) else max(can, min(A, up(l + duoi + lang)))
      loai = 'có lời' if d else ('PP' if r['cu'] == 'PP' else ('lặng' if 'lặng' in r['loi_v1'] else 'nối'))
      C = san_rieng.get(r['ma'], B if d or loai == 'PP' or r['cu'] in ('KHOP',) else min(B, san_noi))
      md_vuot = r['cu'] == 'MD' and A > 8.0
      out.append(dict(r, loai=loai, loi_that=l, lang_v1=lang, can=round(can, 3), A=round(A, 3), B=round(B, 3), C=round(C, 3), lech_v1=round(A - r['dai'], 3), md_vuot_8s=md_vuot,
                      cau=[c['khoa'] for c in d['cau']] if d else []))
  return out

out = tinh([], DUOI, SAN['nối'], SAN_RIENG)
tong = {k: round(sum(x[k] for x in out), 3) for k in ('dai', 'A', 'B', 'C')}
loi_lien = round(sum(ch['giay'] for ch in M['chuong']), 3); loi_shot = round(sum(x['loi_that'] for x in out), 3)
PA = {}
for ten, cat, duoi, sn, sr in [('K0-B', [], DUOI, 99, {}), ('K0-C', [], DUOI, SAN['nối'], SAN_RIENG), ('K0-C1', [], 1.0, SAN['nối'], dict(SAN_RIENG, **{'H4-08': 12.0, 'H3-06': 8.0})),
                                 ('K1-B', CAT, DUOI, 99, {}), ('K1-C', CAT, DUOI, SAN['nối'], SAN_RIENG), ('K1-C1', CAT, 1.0, SAN['nối'], dict(SAN_RIENG, **{'H4-08': 12.0, 'H3-06': 8.0}))]:
    o = tinh(cat, duoi, sn, sr); k = 'B' if ten.endswith('-B') else 'C'; t = round(sum(x[k] for x in o), 3)
    PA[ten] = dict(cat=cat, duoi=duoi, san_noi=None if sn == 99 else sn, san_rieng=sr, phim=t, lech_pct=round((t / 720 - 1) * 100, 2))
R = dict(phuong_an=PA, luat=dict(pad=PAD, duoi=DUOI, san=SAN, fps=FPS), tong=tong, loi_theo_shot=loi_shot, loi_lien_chuong=loi_lien, muc_tieu=720.0,
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
