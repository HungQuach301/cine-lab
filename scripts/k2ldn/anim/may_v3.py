#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · tệp máy dựng 3D cho mọi shot 3D của BANG-SHOT-v3.json → channel-k2/k2c-t4-02/animatic2/may/<ma>[-a|-b].json (render_look.js --page look2|look2d).
Giữ nguyên quỹ đạo §19 (a) của may_v2.py (khoá mỗi 0,25 s, easeKeys false) và thêm:
  · C6 (chủ dự án duyệt): P1 xoay hướng nhìn quanh trục đứng sang trái XOAY_P1 độ (mái vòm ≈ 30 % bề ngang; đo trên khung thử) — áp cho MỌI shot P1 (cùng khung xương sống);
  · C9: cảnh đêm 1666 (look M2-dem) exposure × 2^0,5 (+0,5 EV; lửa kiểm không cháy trắng trên khung thử);
  · DAY tốc độ theo `day_k` (phần khoảng cách tiêu điểm mỗi giây; mặc định 1,0 %/s); THAP có thể ngửa chậm `thap_nghieng_deg` cả shot (MO-DAU §3: THAP có trôi);
  · `xuong_cuoi`: shot CODINH đặt tại tư thế cuối của XUONG cùng tiêu điểm (H1-18b nối H1-18a sau tư liệu toàn khung);
  · `page` look2d cho máy tầm phố (người/xe L3)."""
import json, math, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent)); import may_v2 as MV  # noqa: E402
EP = MV.EP; OUT = EP / 'animatic2/may'
XOAY_P1 = float(__import__('os').environ.get('XOAY_P1', '4.0'))
EV_DEM = 2 ** 0.5
_path = MV.path


def xoay(p, l, deg):
    p, l = np.array(p, float), np.array(l, float); a = math.radians(deg); v = l - p
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]]); return list(p + R @ v)


def path(r, dur):
    them = r['them']; cu = r['cu_may']
    if cu == 'DAY' and them.get('day_k') is not None:
        dm = r['may']; p0, l0 = MV.en(dm['p']), MV.en(dm['l']); td = MV.en(r['tieu_diem_en']) if r['tieu_diem_en'] else l0
        ts = np.append(np.arange(0, dur, MV.DT), dur); d0 = np.linalg.norm(td - p0); out = []
        for t in ts:
            p = p0 + MV.look_dir(p0, td) * d0 * them['day_k'] * t; out.append((round(float(t), 4), [round(float(x), 3) for x in p], [round(float(x), 3) for x in l0], dm['fov']))
        return out
    if them.get('xuong_cuoi'):
        rr = dict(r, cu_may='XUONG', them=dict(them, xuong={'tu': 0.0})); end = _path(rr, 6.0)[-1]
        return [(round(float(t), 4), end[1], end[2], end[3]) for t in np.append(np.arange(0, dur, MV.DT), dur)]
    P = _path(r, dur)
    if cu == 'THAP' and them.get('thap_nghieng_deg'):
        out = []
        for (t, p, l, fov) in P:
            v = np.array(l) - np.array(p); dist = np.linalg.norm(v); hz = math.hypot(v[0], v[1]); el = math.atan2(v[2], hz) + math.radians(them['thap_nghieng_deg']) * (t / dur - 0.5)
            l2 = np.array(p) + np.array([v[0] / hz * math.cos(el) * dist, v[1] / hz * math.cos(el) * dist, math.sin(el) * dist]); out.append((t, p, [round(float(x), 3) for x in l2], fov))
        return out
    return P


MV.path = path


def main(only=None):
    B = json.loads((EP / 'BANG-SHOT-v3.json').read_text()); OUT.mkdir(parents=True, exist_ok=True); n = 0; ds = []
    for r in B['shot']:
        if r['cu_may'] in ('MD', 'PP', 'TL') or not r['thoi_gian']: continue
        if only and r['ma'] not in only: continue
        r = dict(r, them=dict(r['them']))
        if r['diem_may'] == 'P1':
            r['may'] = dict(r['may'], l=[round(x, 3) for x in xoay(r['may']['p'], r['may']['l'], XOAY_P1)])
            if r['tieu_diem_en'] and r['cu_may'] in ('KEO', 'DAY', 'LAN') and r['tieu_diem_en'] == MV.en(r['may']['l']).tolist(): pass
        tg = r['thoi_gian']; page = r['them'].get('page') or ('look2d' if r['goc'] == 'thap' and r['may']['p'][2] <= 60 else 'look2')
        def fix(j):
            if j['look_ten'] == 'M2-dem': j['look'] = dict(j['look'], exposure=round(j['look']['exposure'] * EV_DEM, 4)); j['c9_ev'] = 0.5
            if r['diem_may'] == 'P1': j['c6_xoay_deg'] = XOAY_P1
            j['page'] = page; return j
        if tg[0] == 'khop':
            cut = tg[3]; a = fix(MV.shot_json(r, tg[1], cut + 0.5, 0.0, r['ma'] + '-a')); b = fix(MV.shot_json(r, tg[2], r['dur'] - cut + 0.5, 0.0, r['ma'] + '-b'))
            b['t_trong_shot'] = cut - 0.5; a['t_trong_shot'] = 0.0
            (OUT / f"{r['ma']}-a.json").write_text(json.dumps(a, ensure_ascii=False)); (OUT / f"{r['ma']}-b.json").write_text(json.dumps(b, ensure_ascii=False)); n += 2; ds += [(r['ma'] + '-a', a['dur'], page), (r['ma'] + '-b', b['dur'], page)]
        else:
            j = fix(MV.shot_json(r, tg, r['dur'])); (OUT / f"{r['ma']}.json").write_text(json.dumps(j, ensure_ascii=False)); n += 1; ds.append((r['ma'], j['dur'], page))
    print('tệp máy', n, 'giây', round(sum(d for _, d, _ in ds), 2), 'look2d', [k for k, _, p in ds if p == 'look2d'])
    return ds


if __name__ == '__main__': main(sys.argv[1:] or None)
