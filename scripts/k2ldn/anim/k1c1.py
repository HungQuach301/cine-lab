#!/opt/cine/bin/python
"""ANIMATIC-T4 · phương án G-1 = (c) K1-C1 (chủ dự án 24/10/2026 "Duyệt G-1, G-2, G-3 theo khuyến nghị"): độ dài shot v1 + lời thật sau khi bỏ 7 câu NGUYÊN.
Cùng luật với scripts/k2ldn/giong/gl_gian_shot.py (không sửa tệp đó): lời + 0,4 s; đuôi hình ≤ 1,0 s; shot 'nối' → 6 s; H5-08 18 s, H4-08 12 s, H3-06 8 s; giữ KHOP/LAN/khung tái xuất/khoảnh khắc đinh.
Khác gl_gian_shot: đọc mốc câu từ am-thanh/master/T4-loi-moc.json (trong git) thay vì $GL_OUT/stem/moc.json (cùng nội dung, SHA trong master/SHA256SUMS).
  k1c1.py → in JSON {ma: {dai, loi, cau:[{khoa, L, bd_stem, kt_stem, bo}], ...}}; dùng như module: bang()"""
import json, math, re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'
PAD, DUOI, FPS = 0.4, 1.0, 24
SAN_NOI = 6.0; SAN_RIENG = {'H5-08': 18.0, 'H4-08': 12.0, 'H3-06': 8.0}
CAT = ['L81', 'L41b', 'L45', 'L38', 'L77', 'L15', 'L54']
up = lambda x: math.ceil(x * FPS - 1e-6) / FPS


def rows_v1():
    out = []
    for l in (EP / 'BANG-SHOT-v1.md').read_text().splitlines():
        c = [x.strip() for x in l.split('|')]
        if len(c) > 10 and re.match(r'^(M\d\d|H\d-\d\d)$', c[1]):
            out.append(dict(ma=c[1], dai=float(c[3]), loi_v1=c[4], may=c[5], cu=c[6], moc=c[7], vai=c[8], lop=c[9], ghi=c[10]))
    return out


def bang():
    M = json.loads((EP / 'am-thanh/master/T4-loi-moc.json').read_text())
    D = {}
    for ch in M['chuong']:
        for d in ch['doan']: D[d['shot']] = dict(d, chuong=ch['chuong'], ch_bd=ch['bd_stem'])
    SO = json.loads((EP / 'khoa-loi/so-nhap-khoa.json').read_text())
    def ma(c):
        for x in SO:
            if c in x['khoa'] or x['khoa'].startswith(c[:40]): return x['L']
    R = {}
    for r in rows_v1():
        d = D.get(r['ma']); cau = []; bo_s = 0.0
        if d:
            cs = d['cau']
            for k, c in enumerate(cs):
                L = ma(c['khoa'])
                hit = (L in CAT and L != 'L41') or c['khoa'].startswith('Four classes of house')
                if L == 'L15': hit = c['khoa'].startswith('"I have been')
                if L == 'L14': hit = False
                g = ((cs[k + 1]['bd'] - c['kt']) if k + 1 < len(cs) else (c['bd'] - cs[k - 1]['kt'] if k else 0.0))
                if hit: bo_s += (c['kt'] - c['bd']) + g
                cau.append(dict(khoa=c['khoa'], L=L, bd_stem=round(d['ch_bd'] + c['bd'], 3), kt_stem=round(d['ch_bd'] + c['kt'], 3), bo=hit))
        l = round(d['kt'] - d['bd'] - bo_s, 3) if d else 0.0
        lang = float(m.group(1)) if (m := re.search(r'lặng (\d+) s', r['loi_v1'])) else 0.0
        can = up(l + PAD + lang) if d else 0.0
        A = max(r['dai'], can)
        giu = r['cu'] in ('KHOP', 'LAN') or 'tái xuất' in r['vai'] or 'KHOẢNH KHẮC' in r['vai']
        B = A if (not d or giu) else max(can, min(A, up(l + DUOI + lang)))
        loai = 'có lời' if d else ('PP' if r['cu'] == 'PP' else ('lặng' if 'lặng' in r['loi_v1'] else 'nối'))
        C = SAN_RIENG.get(r['ma'], B if d or loai == 'PP' or r['cu'] == 'KHOP' else min(B, SAN_NOI))
        R[r['ma']] = dict(r, dai_k1c1=round(C, 4), loi_s=l, lang=lang, loai=loai, cau=cau, chuong=d['chuong'] if d else None)
    return R


if __name__ == '__main__':
    R = bang(); t = 0
    for k, v in R.items():
        print(f"{k:6s} {v['cu']:8s} v1 {v['dai']:5.1f} → {v['dai_k1c1']:6.3f}  lời {v['loi_s']:6.2f}  bỏ {sum(c['bo'] for c in v['cau'])}  t0 {t:7.2f}"); t += v['dai_k1c1']
    print('TỔNG', round(t, 3))
