#!/opt/cine/bin/python
"""ANIMATIC-T4 · tệp máy dựng cho từng shot 3D của BANG-SHOT-v2.json → channel-k2/k2c-t4-02/animatic/may/<ma>[-a|-b].json (đầu vào render_look.js --page look2).
Cú máy §19 (a) dựng bằng khoá dày (mỗi 0,25 s) theo đúng quỹ đạo, easeKeys = false → tốc độ đều, không đỉnh do nội suy (bản thử tiền kỳ trượt vì nén 3 s + ease):
  CODINH tĩnh · DAY tiến 1,0 %/s khoảng cách tiêu điểm · KEO lùi 1,4 %/s · CAU dọc theo `cau_dz` (≤ 4 m/s) · VONG quanh `tam` theo `vong_deg` (≤ 2,5°/s) · TRUOT tịnh tiến ngang để tiêu điểm dịch 2 %/s bề ngang
  · NGHIENG ngửa `nghieng_deg` (≤ 1,5°/s) · THAP máy thấp ngửa 5–15° (tĩnh) · XUONG chúc −88° → −30° trong 4–6 s từ `xuong.tu` · KHOP hai nửa cùng máy (a: năm A, b: năm B, chồng 0,5 s để hoà 1 s) · LAN quỹ đạo khoá tay.
Look theo mốc (CHON-V2.json, LOOK-T4-1…3): 1666 cháy ngày = M2-ngay (ấm C) · 1666 cháy đêm = M2-dem (khói than B) · 1940 = M3-rong (ấm C) · ≥ 1960 = M4-rong · còn lại = M1-rong (A, σ 1/10 km).
Lightmap: mốc nướng gần nhất (scripts/k2ldn/anim/du_lieu.sh NAM)."""
import json, math, os, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; OUT = EP / 'animatic/may'; MV = EP / 'look/may-v2'
W, H, FPS, SPP = 640, 360, 24, 2
BAKE = [1666.6, 1667.3, 1700.5, 1711.5, 1800.5, 1860.5, 1900.5, 1938.5, 1940.98, 1941.3, 1955.5, 1975.5, 1995.5, 2026.7]
LOOK = {k: json.loads((MV / f'{k}.json').read_text())['look'] for k in ('M1-rong', 'M2-ngay', 'M2-dem', 'M3-rong', 'M4-rong')}
TZ66 = -0.006533333333333334
DT = 0.25


def jd_year_of_hour(h): return 1666.0 + (245 + h / 24.0) / 365.0   # ≈ năm thập phân của giờ cháy (chỉ để chọn lightmap)


def sun_el_1666(hour):   # độ cao mặt trời gần đúng ở London đầu tháng 9 (chỉ để chọn look ngày/đêm)
    hh = hour % 24; return 39 * math.cos((hh - 12.9) / 24 * 2 * math.pi) - 2


def t_val(tg, u, them, t):
    """giá trị thời gian tại tỉ lệ u ∈ [0, 1] (hoặc theo 'gio'/'nam' khoá tay theo giây t)."""
    k = tg[0]
    if k == 'h66': a, b = tg[1], tg[2]; return {'hour': a + (b - a) * u}
    if k == 'h40':
        h = tg[1] + (tg[2] - tg[1]) * u; return {'h40': h, 'date': [1940, 12, 29, 18.0 + h], 'tz': 0}
    if k == 'd':
        a, b = tg[1], tg[2]; hr = a[3] + (b[3] - a[3]) * u
        if 'gio' in them: hr = float(np.interp(t, [x[0] for x in them['gio']], [x[1] for x in them['gio']]))
        return {'date': [a[0], a[1], a[2], hr], 'tz': tg[3], 'year': a[0] + (243 + hr / 24) / 365 if a[1] == 9 else a[0] + 0.99}
    if k == 'y':
        y = tg[1] + (tg[2] - tg[1]) * u
        if 'nam' in them: y = float(np.interp(t, [x[0] for x in them['nam']], [x[1] for x in them['nam']]))
        M, D, hr = tg[3]; tz = TZ66 if y < 1880 else tg[4]
        return {'year': y, 'date': [int(y), M, D, hr], 'tz': tz}
    raise ValueError(tg)


def chon_look(tg, vals):
    k = tg[0]
    if k == 'h66':
        hs = [v['hour'] for v in vals]; el = np.mean([sun_el_1666(h) for h in hs])
        if hs[0] > 110: return 'M1-rong', 1667.3          # phế tích sau cháy (7/9 trở đi) — look A
        return ('M2-ngay' if el > 0 else 'M2-dem'), 1666.6
    if k == 'h40': return 'M3-rong', 1940.98
    y = np.mean([v['year'] for v in vals])
    if 1940.9 < y < 1941.0: return 'M3-rong', 1940.98
    lk = 'M4-rong' if y >= 1960 else 'M1-rong'
    return lk, min(BAKE, key=lambda b: abs(b - y) + (100 if (y < 1667.3 and b > 1667) or (1667 < y < 1667.4 and b != 1667.3) else 0))


def wind_leaf(tg, v):
    if tg[0] == 'h66': return [-1.0, 0.12], 1
    if tg[0] == 'h40' or ('date' in v and v['date'][1] == 12): return [0.3, -1.0], 0
    if 'date' in v and v['date'][1] in (1, 2, 3): return [0.6, -0.8], 0
    return [0.6, -0.8], 1


def en(p): return np.array(p, float)
def look_dir(p, l): d = en(l) - en(p); return d / np.linalg.norm(d)


def path(r, dur):
    """danh sách (t, p, l, fov) mỗi DT cho cú máy của shot."""
    them = r['them']; dm = r['may']; p0, l0, fov = en(dm['p']), en(dm['l']), dm['fov']; cu = r['cu_may']
    if them.get('p'): p0 = en(them['p'])
    if them.get('l'): l0 = en(them['l'])
    td = en(r['tieu_diem_en']) if r['tieu_diem_en'] else l0
    ts = np.arange(0, dur + 1e-6, DT); ts[-1] = min(ts[-1], dur)
    if ts[-1] < dur - 1e-6: ts = np.append(ts, dur)
    out = []
    for t in ts:
        p, l = p0.copy(), l0.copy()
        if cu == 'DAY': d0 = np.linalg.norm(td - p0); p = p0 + look_dir(p0, td) * d0 * 0.010 * t; l = l0
        elif cu == 'KEO': d0 = np.linalg.norm(td - p0); p = p0 - look_dir(p0, td) * d0 * 0.014 * t
        elif cu == 'CAU': p = p0 + np.array([0, 0, them['cau_dz'] * t / dur]) + (np.array([0, 0, them['cau_h0'] - p0[2]]) if 'cau_h0' in them else 0)
        elif cu == 'VONG':
            c = en(them['tam']); a = math.radians(them['vong_deg']) * (t / dur - 0.5); v = p0 - c
            R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]]); p = c + R @ v; l = c
        elif cu == 'TRUOT':
            d = np.linalg.norm(td - p0); hf = 2 * math.atan(math.tan(math.radians(fov) / 2) * W / H); fw = 2 * d * math.tan(hf / 2)
            fwd = look_dir(p0, l0); side = np.cross(fwd, [0, 0, 1]); side /= np.linalg.norm(side); s = 0.020 * fw * (t - dur / 2)
            p, l = p0 + side * s, l0 + side * s
        elif cu == 'NGHIENG':
            v = l0 - p0; dist = np.linalg.norm(v); hz = math.hypot(v[0], v[1]); el = math.atan2(v[2], hz) + math.radians(them['nghieng_deg']) * (t / dur - 0.5)
            l = p0 + np.array([v[0] / hz * math.cos(el) * dist, v[1] / hz * math.cos(el) * dist, math.sin(el) * dist])
        elif cu == 'XUONG':
            c = td.copy(); c[2] = 0; tu = them['xuong']['tu']; tl = min(6.0, max(4.0, dur - tu)); u = min(1, max(0, (t - tu) / tl)); u = u * u * (3 - 2 * u) if tl > 0 else 1
            el = math.radians(-88 + (88 - 30) * u); D0, D1 = 2200.0, 1600.0; D = D0 + (D1 - D0) * u
            hz = D * math.cos(el); p = c + np.array([0, -hz, D * math.sin(-el)]); l = c + np.array([0, 0.0001, 0])
        elif cu == 'LAN':
            q1, q2 = en(them['lan']['cuoi_p']), en(them['lan']['cuoi_l']); u = t / dur; e = u * u * (3 - 2 * u)
            mid = (p0 + q1) / 2 + np.array([0, 0, 40]); p = (1 - e) ** 2 * p0 + 2 * (1 - e) * e * mid + e * e * q1; l = (1 - e) * td + e * q2
            if u < 0.02: l = l0 * (1 - u / 0.02) + l * (u / 0.02)
        out.append((round(float(t), 4), [round(float(x), 3) for x in p], [round(float(x), 3) for x in l], fov))
    return out


def shot_json(r, tg, dur, t_off=0.0, ten=None):
    them = r['them']; P = path(r, r['dur'])
    vals = [t_val(tg, (t + t_off) / dur if dur > 0 else 0, them, t + t_off) for t in np.linspace(0, dur, 5)]
    lk, bake = chon_look(tg, vals); look = dict(LOOK[lk])
    keys = []
    for (t, p, l, fov) in P:
        if t < t_off - 1e-6 or t > t_off + dur + 1e-6: continue
        u = (t - t_off) / dur if dur > 0 else 0; v = t_val(tg, u, them, t); w, leaf = wind_leaf(tg, v)
        k = dict(t=round(t - t_off, 4), p=p, l=l, fov=fov, leaf=leaf, wind=w, **v)
        if 'year' not in k: k['year'] = 1940.995 if tg[0] == 'h40' else jd_year_of_hour(k.get('hour', 0))
        k['moon'] = 0.25 if tg[0] == 'h66' else 0.35
        if lk == 'M2-ngay': k['smokeSky'] = 0.55
        keys.append(k)
    return {'fps': FPS, 'dur': round(dur, 4), 'W': W, 'H': H, 'spp': SPP, 'easeKeys': False, 'shadow': 2048, 'look': look, 'look_ten': lk, 'keys': keys,
            'bake': {'url': f'/data/look2/bake_{bake}.png', 'box': [530800, 179700, 534000, 182000]}, 'shot': ten or r['ma'], 'cu_may': r['cu_may'],
            'tieu_diem_en': r['tieu_diem_en'], 'hero_EN': r['tieu_diem_en'], 'vai': r['vai']}


def main():
    B = json.loads((EP / 'BANG-SHOT-v2.json').read_text()); OUT.mkdir(parents=True, exist_ok=True); n = 0
    for r in B['shot']:
        if r['cu_may'] in ('MD', 'PP') or not r['thoi_gian']: continue
        tg = r['thoi_gian']
        if tg[0] == 'khop':
            cut = tg[3]; a = shot_json(r, tg[1], cut + 0.5, 0.0, r['ma'] + '-a'); b = shot_json(r, tg[2], r['dur'] - cut + 0.5, 0.0, r['ma'] + '-b')
            b['t_trong_shot'] = cut - 0.5; a['t_trong_shot'] = 0.0
            for k in b['keys']: k['t'] = round(k['t'], 4)
            (OUT / f"{r['ma']}-a.json").write_text(json.dumps(a, ensure_ascii=False)); (OUT / f"{r['ma']}-b.json").write_text(json.dumps(b, ensure_ascii=False)); n += 2
        else:
            j = shot_json(r, tg, r['dur']); (OUT / f"{r['ma']}.json").write_text(json.dumps(j, ensure_ascii=False)); n += 1
    print('tệp máy', n)


if __name__ == '__main__': main()
