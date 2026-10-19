#!/opt/cine/bin/python
"""Biến thể kênh 2 của luật LL — bản 1.12.2 (phiên K, 17/10/2026; chủ dự án duyệt 17/10: NN2, NN3; khiếu nại Q14/Q15/Q17 14/10, T2 G2 §12.4).
Mặc định CHỈ BÁO (cấp đề xuất: reports/K-1.12.2-BAO-CAO.md, cap112.py). Định nghĩa: checks/ll/RULES-LL.md mục "1.12.2".

  q_k2var.py <episode.yaml> [--tl timeline.json] [--video master.mp4] [--json ra.json]

NHIP-K2 (khiếu nại 14/10 Q14/Q15/Q17): kênh 2 (`is_k2`) → Q14–Q18 KHÔNG ÁP; nhịp = Q37 (q_nhip.py). Đặc tả chưa khai `beats` → mốc đặc tả
  (cận trên số biến cố): TRƯỢT khi TB > 3,5 s hoặc dài nhất > 6 s; không thì "ĐẠT (cận)".

Q26b-K2 đa dạng cảnh kênh 2 (thay Q26b khi đặc tả là kênh 2). Mỗi shot có:
  LOẠI cảnh (theo `type` Q34): ban_do (map) · 3d (scene3d) · timelapse · anh (photo, document, record) · footage · the_so (card, chart3d — thẻ/biểu đồ số)
  VÙNG địa lý: `vung` khai ở shot (hoặc `p.vung`, `heroes.<k>.vung`); không khai → suy: scene_id `relief/<vùng>` → <vùng>, `map/globe` →
    "toan-cau", footage → `p.setting`. BỐI CẢNH K2 (dùng ở (c), (d), (e)) = vùng; shot 3D/timelapse không khai vùng → bộ cảnh (scene_id);
    ảnh/thẻ không khai vùng → trung tính (không dứt, không tính)
  (a) mỗi NỬA phim có ≥ LOAI_MIN loại cảnh, mỗi loại hiện ≥ 3 s trong nửa đó
  (b) một loại cảnh chiếm > LOAI_MAX % thời lượng phim
  (c) một bối cảnh K2 chiếm > VUNG_MAX % thời lượng phim
  (d) một bối cảnh K2 hiện LIÊN TỤC > VUNG_RUN s (quãng: như Q26b(b) — shot không có vùng không làm dứt, không tính; vùng khác cộng dồn ≥ 8 s mới dứt)
  (e) nửa sau có < VUNG_HALF bối cảnh K2 (mỗi vùng ≥ 3 s trong nửa sau)
  Bản đồ KHÔNG còn trung tính: thời lượng bản đồ tính vào loại ban_do và vào vùng của nó.

Q33-K2 lặp cảnh kênh 2. Lần xuất hiện = chuỗi shot liền nhau cùng KHOÁ (scene_id theo vùng, camera_id) — như Q33. Thêm:
  ẢNH MÀU trên VÙNG NỘI DUNG (y 18–72 % khung: bỏ dải nhãn trên và dải chú thích + nguồn dưới, giống nhau ở mọi khung kênh 2), 3 khung
  30/50/70 % mỗi lần: pHash 63 bit kênh L (Lab) + màu trung bình CIELAB. Hai lần CÙNG VÙNG (scene_id) khác camera_id là lặp không khai khi
  pHash L ≤ THETA_L VÀ ΔE màu ≤ DE_MAX (min trên cặp khung). Khác vùng không bao giờ gộp (pHash xám toàn khung cũ gộp nhầm địa hình
  khác vùng). Khoá máy (`heroes.<k>.opt.cam` lon/lat/dist/tilt/head) đo và báo kèm, không quyết.
  Số lần của khoá = số lần khai + lần lặp không khai.
  TRƯỢT khi một khoá > 2 lần, TRỪ lần nằm ở CHƯƠNG KHÁC lần đầu VÀ khai khác `nam` (năm hiện trên cảnh) hoặc khác `lop` (lớp dữ liệu) —
  khai ở shot, `p` hoặc `heroes.<k>.opt` (`year`, `nam`, `lop`, `layer`); lần được miễn ghi tên, không tính.
  Không có master → chỉ số lần khai (THIẾU phần pHash, không coi là ĐẠT pHash).

Q32b-K2 trần thời lượng mỗi clip/ảnh (thay 8 s chung của Q32b cho kênh 2; NN2):
  footage chuyển động (`type: footage`, hoặc `p.clip` không phải ảnh) ≤ 8 s (giữ)
  ảnh tĩnh (`type: photo | document | record`) ≤ 12 s KHI có chuyển động máy (Ken Burns: `heroes.<k>.opt.push|zoom|pan` ≠ 0, hoặc
    `heroes.<k>.cam`/`opt.preset` ∈ push/pan/ken/dolly/zoom, hoặc `p.cam` có ≥ 2 mốc) HOẶC chú thích đổi ≥ 1 lần trong shot (mốc `at` của
    `side.lines`, `cap`, `tags` sau đầu shot ≥ 0,5 s); ảnh tĩnh hoàn toàn (không có cả hai) ≤ 8 s
  Đoạn liên tục = các shot kề nhau cùng clip/ảnh (như Q32). Mọi phần khác của Q32 (a, c–i) không đổi.
"""
import json, math, os, re, subprocess, sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

LOAI = {'map': 'ban_do', 'scene3d': '3d', 'chart3d': 'the_so', 'timelapse': 'timelapse', 'photo': 'anh', 'document': 'anh', 'record': 'anh',
        'footage': 'footage', 'card': 'the_so'}
LOAI_MIN, LOAI_MAX, VUNG_MAX, VUNG_RUN, VUNG_HALF, HALF_S, BREAK = 3, 70.0, 25.0, 90.0, 3, 3.0, 8.0   # (c)–(e) giữ số chủ dự án đặt cho Q26b (09/10), chỉ đổi cái được đếm
THETA_L = 16   # hiệu chuẩn 1.12.2 trên master Steel (28e4d113…) + T1 (4f2d280b…): khác bộ ≤ θ 0,65 %, cùng bộ khác góc 1,8 % (cách chọn như Q33 1.10.1)
SAMPLES = (0.3, 0.5, 0.7)
FT_MAX, ANH_MAX, ANH_TINH_MAX, CAP_DOI_S = 8.0, 12.0, 8.0, 0.5
MOVE = ('push', 'pan', 'ken', 'dolly', 'zoom', 'orbit', 'drift', 'tilt')


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def _sat(name, v, thr, up):
    return [f'{name} {v} (ngưỡng {thr})'] if thr and abs(v - thr) <= 0.05 * abs(thr) else []


def is_k2(E):
    """kênh 2 = `kenh: 2` khai ở đặc tả, đặc tả dưới channel-k2/, hoặc mã tập bắt đầu bằng 'k2' (1.11.0 q_rhythm.is_k2 + khai rõ 1.12.2)"""
    k = E.get('kenh')
    if k is not None: return str(k).strip() in ('2', 'k2')
    return '/channel-k2/' in str(E.get('_path') or '').replace(os.sep, '/') or str(E.get('id') or '').startswith('k2')


def _f(x, k):
    return (x or {}).get(k) if (x or {}).get(k) is not None else ((x or {}).get('p') or {}).get(k)


def shots(E, TL):
    """→ [dict(seg, i, t0, t1, ty, loai, vung, scene, cam, hero, sh, spec)] phim chính theo thời gian"""
    H = E.get('heroes') or {}; TH = TL.get('heroes') or {}
    SP = {s['id']: s.get('shots') or [] for s in E.get('segments') or [] if isinstance(s, dict) and 'id' in s}
    out = []
    for s in TL['segments']:
        sp = SP.get(s['id'], [])
        for i, sh in enumerate(s['shots']):
            a, b = s['t0'] + sh['t0'], s['t0'] + sh['t1']
            if b <= a: continue
            spec = sp[i] if i < len(sp) else {}; p = sh.get('p') or {}; k = p.get('hero'); h = dict(TH.get(k) or {}, **(H.get(k) or {}))
            ty = spec.get('type') or (spec.get('p') or {}).get('type') or sh.get('type') or p.get('type')
            if p.get('card'): ty = 'card'
            sc = spec.get('scene_id') or p.get('scene_id') or h.get('scene_id') or h.get('hero') or k
            cam = spec.get('camera_id') or p.get('camera_id') or h.get('camera_id') or k
            vung = _f(spec, 'vung') or p.get('vung') or h.get('vung')
            if not vung:
                if str(sc).startswith('relief/'): vung = str(sc).split('/', 1)[1]
                elif str(sc) == 'map/globe': vung = 'toan-cau'
                elif ty == 'footage' and str(p.get('setting') or '').strip(): vung = str(p['setting']).strip()
            boi = vung or (str(sc) if sc and LOAI.get(ty) in ('3d', 'timelapse') else None)   # bối cảnh K2: vùng; 3D/timelapse không khai vùng → bộ cảnh
            out.append(dict(seg=s['id'], i=i, t0=round(a, 3), t1=round(b, 3), ty=ty, loai=LOAI.get(ty, 'khac'), vung=vung, boi=boi, scene=str(sc), cam=str(cam),
                            hero=k, sh=sh, spec=spec, h=h, st0=s['t0']))
    return out


# ================================================================ Q26b-K2
def _runs(S, x, key):
    R, cur = [], None
    for z in S:
        d = z['t1'] - z['t0']; v = z[key]
        if v == x:
            if cur is None: cur = dict(s=z['t0'], n=0.0, pend=0.0, other=0.0)
            cur['n'] += cur['pend']; cur['pend'] = cur['other'] = 0.0; cur['e'] = z['t1']
        elif cur is None: continue
        elif not v: cur['pend'] += d
        else:
            cur['other'] += d
            if cur['other'] >= BREAK: R.append(cur); cur = None
    if cur is not None: R.append(cur)
    return [(c['e'] - c['s'] - c['n'], c['s'], c['e']) for c in R]


def q26b_k2(E, TL):
    S = shots(E, TL); T = float(TL['tong_s']); half = T / 2; P = {k: [] for k in 'abcde'}; sat = []
    tl, tv, h1, h2, v2 = {}, {}, {}, {}, {}
    for z in S:
        d = z['t1'] - z['t0']; tl[z['loai']] = tl.get(z['loai'], 0) + d
        if z['boi']: tv[z['boi']] = tv.get(z['boi'], 0) + d
        d1 = max(0.0, min(z['t1'], half) - z['t0']); d2 = max(0.0, z['t1'] - max(z['t0'], half))
        h1[z['loai']] = h1.get(z['loai'], 0) + d1; h2[z['loai']] = h2.get(z['loai'], 0) + d2
        if z['boi']: v2[z['boi']] = v2.get(z['boi'], 0) + d2
    for nm, hh in (('nửa đầu', h1), ('nửa sau', h2)):
        L = sorted(x for x, v in hh.items() if v >= HALF_S and x != 'khac')
        if len(L) < LOAI_MIN: P['a'].append(f'{nm}: {len(L)} loại cảnh ≥ {HALF_S:g} s ({", ".join(L) or "—"}) < {LOAI_MIN}')
        elif len(L) == LOAI_MIN: sat.append(f'{nm} đúng {LOAI_MIN} loại cảnh (bằng ngưỡng)')
    for x, v in sorted(tl.items(), key=lambda z: -z[1]):
        pc = 100 * v / T
        if pc > LOAI_MAX: P['b'].append(f'loại {x} chiếm {pc:.1f} % > {LOAI_MAX:g} %')
        sat += _sat(f'loại {x} %', round(pc, 1), LOAI_MAX, False)
    for x, v in sorted(tv.items(), key=lambda z: -z[1]):
        pc = 100 * v / T
        if pc > VUNG_MAX: P['c'].append(f'vùng {x} chiếm {pc:.1f} % > {VUNG_MAX:g} %')
        sat += _sat(f'vùng {x} %', round(pc, 1), VUNG_MAX, False)
    lr = {}
    for x in tv:
        d, a, b = max(_runs(S, x, 'boi')); lr[x] = (round(d, 1), mmss(a), mmss(b))
        if d > VUNG_RUN: P['d'].append(f'vùng {x} liên tục {d:.1f} s ({mmss(a)}–{mmss(b)}) > {VUNG_RUN:g} s')
        sat += _sat(f'vùng {x} liên tục s', round(d, 1), VUNG_RUN, False)
    V2 = sorted(x for x, v in v2.items() if v >= HALF_S)
    if len(V2) < VUNG_HALF: P['e'].append(f'nửa sau ({mmss(half)}–{mmss(T)}) {len(V2)} vùng ≥ {HALF_S:g} s ({", ".join(V2) or "—"}) < {VUNG_HALF}')
    elif len(V2) == VUNG_HALF: sat.append(f'nửa sau đúng {VUNG_HALF} vùng (bằng ngưỡng)')
    loi = [f'({k}) {x}' for k in 'abcde' for x in P[k]]
    kv = 100 * sum(z['t1'] - z['t0'] for z in S if not z['boi']) / T
    return dict(ok=not loi, loi=loi, muc=P, sat_nguong=sat, loai={x: round(100 * v / T, 1) for x, v in sorted(tl.items(), key=lambda z: -z[1])},
                vung={x: round(100 * v / T, 1) for x, v in sorted(tv.items(), key=lambda z: -z[1])}, lien_tuc=lr,
                nua={'dau': {x: round(v, 1) for x, v in h1.items() if v}, 'sau': {x: round(v, 1) for x, v in h2.items() if v}}, vung_nua_sau=V2,
                val=f"loại: " + ', '.join(f'{x} {100 * v / T:.1f} %' for x, v in sorted(tl.items(), key=lambda z: -z[1])) +
                    f" · {len(tv)} vùng, lớn nhất " + (max(tv.items(), key=lambda z: z[1])[0] + f" {100 * max(tv.values()) / T:.1f} %" if tv else '—') +
                    f" · nửa sau {len(V2)} vùng · không vùng {kv:.1f} %")


# ================================================================ Q33-K2
WIN = (0.18, 0.72)   # vùng nội dung (tỉ lệ chiều cao): bỏ dải chip/nhãn trên và dải chú thích + dòng nguồn dưới (giống nhau ở mọi khung kênh 2)
CAM_D, CAM_R, CAM_TILT, CAM_HEAD = 0.25, 1.5, 10.0, 20.0
DE_MAX = 10.0   # ΔE CIELAB màu trung bình vùng nội dung: T2 cặp khác bảng màu (sepia ↔ xanh) 21–23, cặp cùng bảng 0,2–6,2   # khoá máy "cùng góc": tâm lệch ≤ 25 % tầm xa, tầm xa ×≤ 1,5, nghiêng ≤ 10°, hướng ≤ 20°


def _dct32(x):
    n = np.arange(32); C = np.cos(np.pi * (2 * n[None, :] + 1) * n[:, None] / 64)
    d = (C @ x @ C.T)[:8, :8].flatten()[1:]
    return int(''.join('1' if v else '0' for v in d > np.median(d)), 2)


def phash_img(bgr):
    """ảnh BGR → (pL, pa, pb, (L*, a*, b*)): pHash 63 bit của kênh L, a, b (Lab) trên VÙNG NỘI DUNG WIN (thu 32×32 INTER_AREA) + màu trung bình
    CIELAB của vùng đó. Luật dùng pL (cấu trúc địa hình/khối) + ΔE màu trung bình (bảng màu vùng: sepia ≠ xanh); pa, pb chỉ báo kèm."""
    import cv2
    h = bgr.shape[0]; w = bgr[int(WIN[0] * h):int(WIN[1] * h)]
    lab = cv2.cvtColor(cv2.resize(w, (32, 32), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2LAB).astype(np.float64)
    m = cv2.cvtColor(w, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float64).mean(0)
    return tuple(_dct32(lab[..., c]) for c in range(3)) + ((round(m[0] * 100 / 255, 2), round(m[1] - 128, 2), round(m[2] - 128, 2)),)


def phash_video(video, t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', '-vf', 'scale=320:180:flags=area', '-pix_fmt', 'bgr24',
                          '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    return phash_img(np.frombuffer(raw, np.uint8).reshape(180, 320, 3).copy())


def ham(a, b): return bin(a ^ b).count('1')


def dL(A, B): return min(ham(x[0], y[0]) for x in A['phm'] for y in B['phm'])


def dC(A, B): return min((ham(x[1], y[1]) + ham(x[2], y[2])) / 2 for x in A['phm'] for y in B['phm'])


def dE(A, B): return min(math.dist(x[3], y[3]) for x in A['phm'] for y in B['phm'])


def cam_keys(h):
    """mốc máy quay bản đồ nổi (`heroes.<k>.opt.cam`: [{lon, lat, dist, tilt, head}]) → [(lon, lat, dist, tilt, head)]"""
    out = []
    for c in ((h or {}).get('opt') or {}).get('cam') or []:
        if isinstance(c, dict) and all(isinstance(c.get(k), (int, float)) for k in ('lon', 'lat', 'dist')):
            out.append((c['lon'], c['lat'], float(c['dist']), float(c.get('tilt') or 0), float(c.get('head') or 0)))
    return out


def cam_gan(K1, K2):
    """hai bộ mốc máy có cặp 'cùng góc'? None = không đo được (thiếu mốc)"""
    if not K1 or not K2: return None
    for a in K1:
        for b in K2:
            km = math.hypot((a[0] - b[0]) * 111.32 * math.cos(math.radians((a[1] + b[1]) / 2)), (a[1] - b[1]) * 110.57)
            dh = abs((a[4] - b[4] + 180) % 360 - 180)
            if km <= CAM_D * min(a[2], b[2]) and max(a[2], b[2]) / max(min(a[2], b[2]), 1e-6) <= CAM_R and abs(a[3] - b[3]) <= CAM_TILT and dh <= CAM_HEAD: return True
    return False


def appearances(E, TL):
    S = shots(E, TL); out, open_, tp = [], {}, None
    for z in S:
        if z['ty'] == 'card' or not z['hero']: open_, tp = {}, z['t1']; continue
        key = (z['scene'], z['cam']); ap = open_.get(key)
        if ap is not None and tp is not None and z['t0'] - tp <= 1 / 24 + 0.001: ap['t1'] = z['t1']; ap['shots'].append(f"{z['seg']}/{z['i']}")
        else:
            h = z['h']; o = h.get('opt') or {}
            mk = lambda k: _f(z['spec'], k) or (z['sh'].get('p') or {}).get(k) or o.get(k)
            ap = dict(scene=z['scene'], cam=z['cam'], vung=z['vung'], seg=z['seg'], t0=z['t0'], t1=z['t1'], shots=[f"{z['seg']}/{z['i']}"],
                      nam=mk('nam') or mk('year'), lop=mk('lop') or mk('layer'), camk=cam_keys(h)); out.append(ap)
        open_, tp = {key: ap}, z['t1']
    for ap in out:
        if isinstance(ap['nam'], dict): ap['nam'] = ap['nam'].get('s')
    return out


def hashes(video, aps):
    for ap in aps: ap['phm'] = [phash_video(video, ap['t0'] + f * (ap['t1'] - ap['t0'])) for f in SAMPLES]
    return aps


def lien_ket(o, x, theta):
    """lần o (khác camera_id, CÙNG vùng) là lặp không khai của x: pHash L ≤ θ VÀ ΔE màu trung bình ≤ DE_MAX. Khoá máy (cam_gan) chỉ báo kèm:
    đo trên T2, mốc máy khai cho cả cảnh (không theo từng lần) nên loại cả cặp cùng góc thật (§4.3 báo cáo)."""
    return dL(o, x) <= theta and dE(o, x) <= DE_MAX


def q33_k2(E, TL, video=None, theta=THETA_L, aps=None):
    aps = aps if aps is not None else appearances(E, TL)
    if video and aps and 'phm' not in aps[0]: hashes(video, aps)
    hp = bool(aps) and all('phm' in a for a in aps)
    G = {}
    for ap in aps: G.setdefault((ap['scene'], ap['cam']), []).append(ap)
    bad, near, rows, th = [], [], {}, []
    for (sc, cam), g in sorted(G.items()):
        extra = [o for o in aps if o['scene'] == sc and o['cam'] != cam and any(lien_ket(o, x, theta) for x in g)] if hp else []
        allap = sorted(g + extra, key=lambda a: a['t0']); first = allap[0]
        mien = [a for a in allap[1:] if a['seg'] != first['seg'] and ((a.get('nam') and str(a['nam']) != str(first.get('nam') or '')) or
                                                                      (a.get('lop') and str(a['lop']) != str(first.get('lop') or '')))]
        n = len(allap) - len(mien)
        when = ', '.join(f"{(a['cam'] + ' ') if a['cam'] != cam else ''}{mmss(a['t0'])}" + (' (miễn: khác chương + khác năm/lớp)' if a in mien else '') for a in allap)
        rows[f'{sc} · {cam}'] = dict(khai=len(g), anh_them=len(extra), mien=len(mien), tong=n, luc=when)
        if n > 2: bad.append(f'{sc} · {cam}: {n} lần ({when}) > 2')
        elif n == 2: near.append(f'{sc} · {cam}: đúng 2 lần')
    if aps and not hp: th.append('không có master: pHash không đo (chỉ đếm lần khai)')
    top = max(rows.items(), key=lambda z: z[1]['tong']) if rows else ('—', dict(tong=0))
    return dict(ok=not bad and not th, ket_qua='THIẾU' if th and not bad else None, loi=bad, thieu=th, sat_nguong=near, bang=rows, aps=aps,
                val=f"{len(G)} khoá (vùng, góc) · {len(aps)} lần xuất hiện · nhiều nhất {top[0]} {top[1]['tong']} · {len(bad)} khoá > 2"
                    + (f" · pHash L θ={theta} + ΔE ≤ {DE_MAX:g}, thêm {sum(r['anh_them'] for r in rows.values())} lần lặp không khai, miễn {sum(r['mien'] for r in rows.values())}" if hp else ''))


# ================================================================ Q32b-K2
def _cap_doi(sh, z):
    """số lần chú thích đổi trong shot: mốc `at` (giây trong đoạn) của side.lines / cap / tags sau đầu shot ≥ 0,5 s"""
    p = sh.get('p') or {}; t0, t1 = sh['t0'], sh['t1']; ts = set()
    for x in ((p.get('side') or {}).get('lines') or []) + (p.get('cap') or []) + (p.get('tags') or []):
        a = x.get('at') if isinstance(x, dict) else None
        if isinstance(a, (int, float)) and t0 + CAP_DOI_S <= a < t1: ts.add(round(a, 2))
    return len(ts)


def _may(z):
    """chuyển động máy của ảnh: Ken Burns khai ở cảnh (opt.push/zoom/pan ≠ 0, cam/preset di chuyển) hoặc p.cam ≥ 2 mốc"""
    h = z['h'] or {}; o = h.get('opt') or {}; p = z['sh'].get('p') or {}
    if any(isinstance(o.get(k), (int, float)) and abs(o[k]) > 1e-6 for k in ('push', 'zoom', 'pan')): return 'opt.' + next(k for k in ('push', 'zoom', 'pan') if isinstance(o.get(k), (int, float)) and abs(o[k]) > 1e-6)
    for c in (h.get('cam'), o.get('preset'), z['cam']):
        if c and any(m in str(c).lower() for m in MOVE): return f'cam {c}'
    if isinstance(p.get('cam'), list) and len(p['cam']) >= 2: return 'p.cam'
    return None


def q32b_k2(E, TL):
    S = shots(E, TL); runs = []
    for z in S:
        p = z['sh'].get('p') or {}; c = p.get('clip') or p.get('photo')
        if z['ty'] not in ('footage', 'photo', 'document', 'record') and not p.get('clip'): continue
        c = c or z['hero']
        if runs and runs[-1]['c'] == c and abs(z['t0'] - runs[-1]['t1']) <= 1 / 24 + 0.001:
            r = runs[-1]; r['t1'] = z['t1']; r['cap'] += _cap_doi(z['sh'], z); r['may'] = r['may'] or _may(z)
        else: runs.append(dict(c=c, ty=z['ty'], t0=z['t0'], t1=z['t1'], cap=_cap_doi(z['sh'], z), may=_may(z)))
    loi, sat, rows = [], [], []
    for r in runs:
        d = r['t1'] - r['t0']
        if r['ty'] == 'footage': lim, kind = FT_MAX, 'footage chuyển động'
        elif r['may'] or r['cap'] >= 1: lim, kind = ANH_MAX, 'ảnh có ' + ' + '.join(x for x in ((r['may'] or '') and f"máy ({r['may']})", (r['cap'] >= 1) and f"chú thích đổi {r['cap']} lần") if x)
        else: lim, kind = ANH_TINH_MAX, 'ảnh tĩnh hoàn toàn'
        rows.append(dict(clip=r['c'], loai=kind, t=[mmss(r['t0']), mmss(r['t1'])], s=round(d, 2), tran=lim))
        if d > lim + 1e-6: loi.append(f"{r['c']} ({kind}) liên tục {d:.2f} s ({mmss(r['t0'])}–{mmss(r['t1'])}) > {lim:g} s")
        sat += _sat(f"{r['c']} s", round(d, 2), lim, False)
    return dict(ok=not loi, loi=loi, sat_nguong=sat, bang=rows,
                val=f"{len(runs)} clip/ảnh · " + '; '.join(f"{x['clip']} {x['s']} s/{x['tran']:g} s" for x in sorted(rows, key=lambda x: -x['s'])[:4]))


# ================================================================ NHIP-K2 (Q14–Q18 → Q37 cho kênh 2)
def nhip_k2(E, TL, mp4=None, tl=None, mien=None):
    """Kênh 2: Q14–Q18 (luật nhịp LL) KHÔNG ÁP; nhịp đo bằng Q37 (TB ≤ 3,5 s, dài nhất ≤ 6 s — Kinh thánh §4, thước scripts/k2/rhythm.py).
    Đặc tả chưa khai `beats` → dùng MỐC ĐẶC TẢ (mọi mốc thật khai trong đặc tả): TRƯỢT khi mốc đã vượt ngưỡng (máy 3D di chuyển liên tục không
    sinh mốc nên phải chốt bằng beats hoặc master); mốc ĐẠT → "ĐẠT (cận)" (mốc ≥ biến cố khai được)."""
    from checks.ll import q_nhip, q_rhythm
    if not is_k2(E): return dict(ok=True, loi=[], val='không áp (tập LL: Q14–Q18 như cũ)', khong_ap=True)
    ll = q_rhythm.measure(dict(E, kenh=2, id=E.get('id') or 'k2'), TL)
    r = q_nhip.q37(E, TL, mp4, tl=tl, mien=mien); M = r.get('moc_dac_ta')
    if r.get('bien_co') or not M: return dict(r, ll=ll, val='Q37: ' + r['val'])
    loi = [x for x in (r.get('loi') or []) if not x.startswith('(a)') or 'không khai beats' not in x]
    if M['tb'] > 3.5: loi.append(f"(b) mốc đặc tả: TB {M['tb']} s > 3,5 s (mốc đặc tả; chuyển động máy liên tục của cảnh 3D không sinh mốc — chốt bằng beats hoặc master)")
    if M['dai_nhat'] > 6.0: loi.append(f"(c) mốc đặc tả: dài nhất {M['dai_nhat']} s > 6 s ({M['dai_nhat_tu']}; chốt bằng beats hoặc master)")
    sat = _sat('TB s', M['tb'], 3.5, False) + _sat('dài nhất s', M['dai_nhat'], 6.0, False)
    return dict(ok=not loi, ket_qua=None if loi else 'ĐẠT (cận)', loi=loi, sat_nguong=sat, ll=ll, moc_dac_ta=M,
                val=f"Q14–Q18 không áp · chưa khai beats → mốc đặc tả (cận trên): TB {M['tb']} s, dài nhất {M['dai_nhat']} s ({M['dai_nhat_tu']}) · {M['gop']} mốc sau gộp")


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    from checks.ll import base
    E = base.load(a[0]); E['_path'] = os.path.abspath(a[0])
    tl = a[a.index('--tl') + 1] if '--tl' in a else os.path.join(E['out'], 'timeline.json'); TL = json.load(open(tl))
    v = a[a.index('--video') + 1] if '--video' in a else None
    R = {'NHIP-K2': nhip_k2(E, TL, v), 'Q26b-K2': q26b_k2(E, TL), 'Q33-K2': q33_k2(E, TL, v), 'Q32b-K2': q32b_k2(E, TL)}
    R['Q33-K2'].pop('aps', None)
    for k, r in R.items(): print(f"{k}: {r.get('ket_qua') or ('ĐẠT' if r['ok'] else 'TRƯỢT')} — {r['val']}" + ''.join('\n    ' + x for x in r['loi'] + r.get('thieu', [])))
    if '--json' in a: json.dump(R, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False, indent=1, default=str)


if __name__ == '__main__':
    main()
