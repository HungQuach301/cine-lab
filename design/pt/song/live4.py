"""PT4 · lớp sống + KHÔNG KHÍ trên nền LAI (A+C) hoặc A-thuần — kế thừa design/pt/lai/live2.py (PT2), CÙNG hạt giống cho mọi bản.
- Người (mh_people4.py): 2 dáng thân/vai; đi 8 pha với TỐC ĐỘ RIÊNG từng người (nhịp bước theo tốc độ); đi tay mang vật (thùng/hòm/bao/giỏ);
  CẶP KHIÊNG (hai người một thùng); NHÓM 2–4 người đứng quay vào nhau (nói, nhìn quanh, chắp tay); TỔ VIỆC sát tường (chữa tường 1782 / thợ 1943),
  GÁC (súng dựng) ở cặp cố định; KHÔNG xếp hàng (không có đội hình có nguồn). Người ≥ 10 m, không cận mặt, không người ngã/chết.
- Bóng: bóng nắng theo mặt trời từng lượt (như PT2) + BÓNG TIẾP ĐẤT mềm dưới chân (mọi lúc) → hết "đặt lên ảnh".
- Không khí: sương/khói phố theo lượt độ sâu (đậm dần theo khoảng cách, trôi chậm), TIA NẮNG + bụi trong nắng (từ lượt nắng của A, quét về phía mặt trời),
  chiều sâu tông (xa nhạt + lạnh). Đêm 1943 phong toả: không thêm nguồn sáng nào (sương đêm chỉ nhận ánh trăng của nền A).
- Chỉnh màu RIÊNG cho LAI (P2-3): bão hoà thấp hơn chung PT, giữ tương phản; A-thuần giữ chỉnh màu PT2 để so.
- Nhãn như PT2. Log mỗi khung: ai_image, số người/nhóm/vật cầm.
  /opt/cine/bin/python -I live4.py --ban LAI|A --out DIR [--video 960x540] [--stills 1920x1080] [--notext] [--nen1943 1943L] [--grade lai|chung]"""
import os, sys, json, math, argparse, subprocess, random
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'scene'))
import lai_common as LC
os.environ['PT_CAM'] = 'pt'
import pt_site as S
ap = argparse.ArgumentParser(); ap.add_argument('--ban', default='LAI'); ap.add_argument('--out', required=True)
ap.add_argument('--bg', default='/var/tmp/pt4/bg'); ap.add_argument('--spr', default='/var/tmp/pt4/spr')
ap.add_argument('--nen1782', default=''); ap.add_argument('--nen1943', default=''); ap.add_argument('--grade', default=''); ap.add_argument('--nokhi', action='store_true')
ap.add_argument('--video', default=''); ap.add_argument('--stills', default=''); ap.add_argument('--notext', action='store_true'); ap.add_argument('--stillset', default='')
ap.add_argument('--frames', default='')
A = ap.parse_args(); os.makedirs(A.out, exist_ok=True)
FPS = 24; SEG = 9.0; TR = 2.0; TOTAL = SEG * 2 + TR
PASS_H = json.load(open(os.path.join(HERE, '..', 'scene', 'passes.json'))); PASS_H['n'] = 20.6
ORDER = ['d1', 'd2', 'd3', 'd4', 'n']; DAY = ORDER[:4]
H0, H1 = 8.6, 22.4
PAD = 300
CROWD = 3.0; WALK = 1.35 * CROWD     # m/s trên phim (tua nhanh ngày→đêm như PT2); mỗi người nhân thêm hệ số tốc độ riêng 0,75–1,3
FONT_B = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'; FONT_R = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
LABEL_A = {1782: ['Reconstructed from J. Drinkwater, Plan of the Batteries, 1782', 'Facades: procedural, period style · not a photograph'],
           1943: ['Buildings: OpenStreetMap, checked against U.S. Army Map Service plan, 1943', 'Map data from OpenStreetMap (ODbL) · facades procedural']}
LABEL_L = {1782: ['Reconstructed from J. Drinkwater, Plan of the Batteries, 1782', 'Surface detail AI-assisted · layout, landmarks & flags from sources'],
           1943: ['Buildings: OpenStreetMap, checked against U.S. Army Map Service plan, 1943', 'Surface detail AI-assisted · layout, landmarks & flags from sources']}
CAMK = {1782: 'k1782', 1943: 'pt'}
# vai và tỉ lệ theo thời kỳ: 1782 phố sau pháo kích 4/1781 dân chạy về nam (S062) → chủ yếu quân đồn trú; 1943 KHÔNG phụ nữ/trẻ em (sơ tán 1940, S114)
PMAP = {'d1': 'd1', 'd2': 'd2', 'd3': 'd4', 'd4': 'd4', 'n': 'd2'}   # sprite dựng 3 lượt; d3 dùng d4, đêm dùng d2 tối + lam (NIGHT)
NIGHT = np.array([0.022, 0.026, 0.038], np.float32)
WORKER = {1782: ('linh2', 'phao_binh'), 1943: ('tho',)}             # tổ việc sát tường: chữa tường 1782 (dầm chống, S063) / thợ 1943
ROLEW = {1782: {'linh': 0.34, 'linh2': 0.22, 'phao_binh': 0.16, 'thuy_thu': 0.12, 'dan_nam': 0.12, 'dan_nu': 0.04},
         1943: {'linh': 0.28, 'linh2': 0.22, 'thuy_thu': 0.17, 'thuy_thu_trang': 0.08, 'raf': 0.12, 'tho': 0.13}}

def busy(hr): return max(0.66 if hr < 19.6 else 0.04, math.exp(-((hr - 11.5) / 3.2) ** 2) + 0.8 * math.exp(-((hr - 17.5) / 1.8) ** 2))   # sàn ban ngày: ≥ 30 người/khung (HC3)

class Epoch:
    def __init__(s, ep, W, H):
        s.ep = ep; s.W, s.H = W, H
        tag = (A.nen1782 if ep == 1782 else A.nen1943) or f'{ep}{"L" if A.ban == "LAI" else "A"}'
        d = os.path.join(A.bg, tag); s.meta = json.load(open(os.path.join(d, 'meta.json'))); s.bgdir = d
        s.k = W / s.meta['camera']['W']
        s.bg = {}
        for p in ORDER:
            im = cv2.imread(os.path.join(d, p + '.png'), cv2.IMREAD_UNCHANGED)[..., :3][..., ::-1].astype(np.float32) / 65535.0
            s.bg[p] = LC.srgb2lin(cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA))
        s.depth = cv2.resize(LC.exr(os.path.join(d, 'depth.exr')), (W, H), interpolation=cv2.INTER_NEAREST)
        s.sky = s.depth > 20000
        reg = np.round(LC.exr(os.path.join(d, 'cls.exr'))).astype(np.int64) // 64
        s.ground = cv2.resize((reg == 9800).astype(np.uint8), (W, H), interpolation=cv2.INTER_NEAREST) > 0
        s.sunvis = {}
        for p in DAY:
            v = LC.exr(os.path.join(d, f'sunvis_{p}.exr')); v = cv2.resize(v, (W, H), interpolation=cv2.INTER_LINEAR)
            s.sunvis[p] = np.clip(v / max(1e-6, np.percentile(v[v > 0], 95)) / 0.6, 0, 1) if (v > 0).any() else np.zeros((H, W), np.float32)
        s.sun = {r['pass']: (r.get('sun_alt'), r.get('sun_az')) for r in s.meta['renders'] if r['pass'] in DAY}
        hz = s.sky & (np.arange(H)[:, None] > H * 0.25)
        s.bg['n'] *= 3.0 if ep == 1782 else 1.6
        for p in ORDER:   # phối cảnh không khí như PT (cùng cho hai bản)
            c = s.bg[p][hz].mean(0) if hz.sum() > 50 else s.bg[p][s.sky].mean(0)
            T = np.exp(-np.minimum(s.depth, 30000) / (5500 if p != 'n' else 1e9))[..., None]; amt = 0.85 if p != 'n' else 0.0
            s.bg[p] = np.where(s.sky[..., None], s.bg[p], s.bg[p] * (1 - amt * (1 - T)) + c * amt * (1 - T))
        # sprite PT4: vai "<vai>~<dáng>" + "khieng"; cột = tư thế (meta 'poses'), ô rộng 'cellx'; 3 lượt (PMAP)
        sp = A.spr + str(ep); js = [f for f in os.listdir(sp) if f.startswith('sprites-') and f.endswith('.json')]
        s.sm = {}
        for f in js: s.sm.update(json.load(open(os.path.join(sp, f)))['roles'])
        smeta = json.load(open(os.path.join(sp, js[0]))); s.pxm = smeta['pxm']; s.na = smeta['na']
        s.sheet = {}
        import OpenEXR
        for role in s.sm:
            for p in sorted(set(PMAP.values())):
                c = OpenEXR.File(os.path.join(sp, f'{role}_{p}.exr')).parts[0].channels['ViewLayer.Combined'].pixels.astype(np.float32)
                s.sheet[(role, p)] = np.pad(c, ((PAD, PAD), (PAD, PAD), (0, 0)))
        s.dirs = {}; s.cell = {}
        for role, rm in s.sm.items():
            for c in rm['cells']: s.dirs[(role, c['a'])] = np.array(c['dir']); s.cell[(role, c['a'], c['pose'])] = c
        s.carry = {r.split('~')[0]: next((p_[1:-1] for p_ in rm['poses'] if p_[0] == 'c' and p_[-1].isdigit()), None) for r, rm in s.sm.items()}
        s.work = {r.split('~')[0]: next((p_ for p_ in rm['poses'] if p_.startswith('work_')), None) for r, rm in s.sm.items()}
        os.environ['PT_CAM'] = CAMK[ep]; import importlib; importlib.reload(S)
        s.polys = [b['pts'] for b in S.load(ep, kinds=['nha', 'khoi_pho', 'phao_dai', 'cong_su'], R=330) if not b['line']]
        cam = s.meta['camera']; s.fpx = cam['fpx'] * s.k; s.ch = cam['pos'][2]
        h = math.radians(cam['head']); p_ = math.radians(cam['pitch'])
        s.f = np.array([math.sin(h) * math.cos(p_), math.cos(h) * math.cos(p_), math.sin(p_)]); s.r = np.array([math.cos(h), -math.sin(h), 0.0]); s.u = np.cross(s.r, s.f)
        s.rng = random.Random(ep * 31 + 7); s.plan()

    def proj(s, x, y, z):
        d = np.array([x, y, z - s.ch]); zc = d @ s.f
        if zc < 0.5: return None
        return (s.W / 2 + s.fpx * (d @ s.r) / zc, s.H / 2 - s.fpx * (d @ s.u) / zc, zc, float(np.linalg.norm(d)))

    def ground_pt(s, dmin=10.0, dmax=60.0):
        for _ in range(800):
            u, v = s.rng.uniform(0, s.W - 1), s.rng.uniform(s.H * 0.5, s.H - 1)
            d = s.f + ((u - s.W / 2) / s.fpx) * s.r - ((v - s.H / 2) / s.fpx) * s.u
            if d[2] >= -1e-3: continue
            t = -s.ch / d[2]; x, y = t * d[0], t * d[1]; dist = t * float(np.linalg.norm(d))
            if not (dmin <= dist <= dmax): continue
            if not s.ground[int(v), int(u)] or abs(s.depth[int(v), int(u)] - dist) > 0.04 * dist + 0.3: continue
            if any(S.inside(x, y, q) for q in s.polys): continue
            return (x, y)
        return None

    def on_ground(s, x, y):
        p = s.proj(x, y, 0)
        if not p or not (0 <= p[0] < s.W and 0 <= p[1] < s.H): return False
        return bool(s.ground[int(p[1]), int(p[0])]) and abs(s.depth[int(p[1]), int(p[0])] - p[3]) < 0.05 * p[3] + 0.4 and 10.0 <= p[3] <= 62.0

    def pick_role(s, R):
        w = ROLEW[s.ep]; x = R.random() * sum(w.values())
        for k, v in w.items():
            x -= v
            if x <= 0: return k
        return k

    def near_wall(s, R, dmin=11.0, dmax=45.0):
        """điểm mặt đất sát chân tường nhà (≤ 1,2 m) + hướng NHÌN vào tường (pháp tuyến cạnh gần nhất) — cho tổ chữa tường / thợ."""
        for _ in range(400):
            c = s.ground_pt(dmin, dmax)
            if not c: continue
            best = None
            for q in s.polys:
                for i in range(len(q)):
                    (x0, y0), (x1, y1) = q[i], q[(i + 1) % len(q)]; dx, dy = x1 - x0, y1 - y0; L2 = dx * dx + dy * dy
                    if L2 < 1: continue
                    t = max(0, min(1, ((c[0] - x0) * dx + (c[1] - y0) * dy) / L2)); px, py = x0 + t * dx, y0 + t * dy; dd = math.hypot(c[0] - px, c[1] - py)
                    if best is None or dd < best[0]: best = (dd, px, py)
            if best and best[0] < 4.0:
                dd, px, py = best; ux, uy = (px - c[0]) / max(dd, 1e-3), (py - c[1]) / max(dd, 1e-3)
                x, y = px - ux * 0.75, py - uy * 0.75
                if s.on_ground(x, y): return (x, y), (ux, uy)
        return None, None

    def plan(s):
        """người đi: tuyến thẳng giữa hai điểm mặt đất nhìn thấy (10–60 m), tốc độ riêng; một phần mang vật; vài cặp khiêng.
        nhóm đứng 2–4 người quay vào tâm nhóm (nói/nhìn/chắp tay), tổ việc sát tường, gác cặp — KHÔNG xếp hàng."""
        R = s.rng; s.walk = []; s.stand = []; s.n_group = 0; s.n_work = 0
        tries = 0
        while len(s.walk) < 120 and tries < 20000:
            tries += 1
            t0 = R.uniform(-8.0, SEG); hr = H0 + (H1 - H0) * max(0, t0) / SEG
            if R.random() > busy(hr) * (0.12 if hr > 19.6 else 1.0): continue
            a, b = s.ground_pt(), s.ground_pt()
            if not a or not b or math.dist(a, b) < 8: continue
            if not all(s.on_ground(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u) for u in (0.25, 0.5, 0.75)): continue
            pair = R.random() < 0.05 and hr < 19.0
            role = 'khieng' if pair else s.pick_role(R)
            carry = (not pair) and s.carry.get(role) and R.random() < 0.3
            spd = R.uniform(0.75, 1.3) * (0.8 if (pair or carry) else 1.0)
            s.walk.append({'t0': t0, 'a': a, 'b': b, 'L': math.dist(a, b), 'role': role, 'b_': 0 if pair else R.randrange(2), 'carry': s.carry.get(role) if carry else None,
                           'ph0': R.randrange(8), 'sc': R.uniform(0.94, 1.06), 'u': R.random(), 'spd': spd, 'tone': R.uniform(0.88, 1.1)})
        for k in range(16):   # nhóm trò chuyện 2–4 người (quay vào tâm)
            hr = R.uniform(H0, H1 - 1.2)
            if R.random() > busy(hr): continue
            c = s.ground_pt(10.5, 50.0)
            if not c: continue
            n = R.choice((2, 2, 3, 3, 4)); dur = R.uniform(1.4, 3.6); grp = []
            for j in range(n):
                ang = 2 * math.pi * j / n + R.uniform(-0.35, 0.35); rad = R.uniform(0.55, 0.85)
                x, y = c[0] + rad * math.cos(ang), c[1] + rad * math.sin(ang)
                if not s.on_ground(x, y): continue
                role = s.pick_role(R); pose = R.choice(('talk', 'look', 'st', 'st', 'back' if role.startswith(('linh', 'raf', 'phao')) else 'talk'))
                fd = (c[0] - x, c[1] - y); grp.append((x, y, role, R.randrange(2), pose, fd, R.uniform(0.94, 1.06), R.uniform(0.88, 1.1)))
            if len(grp) >= 2:
                s.stand.append({'t0': (hr - H0) / (H1 - H0) * SEG, 't1': (hr - H0) / (H1 - H0) * SEG + dur, 'people': grp, 'kind': 'nhom'}); s.n_group += 1
        for k in range(5):    # tổ việc sát tường: 1–3 người làm, 0–1 người đứng xem
            hr = R.uniform(8.8, 18.0); pos, nrm = s.near_wall(R)
            if not pos: continue
            grp = []
            for j in range(R.choice((1, 2, 2, 3))):
                off = (j - 1) * 1.1; x, y = pos[0] - nrm[1] * off, pos[1] + nrm[0] * off
                if s.on_ground(x, y):
                    role = R.choice(WORKER[s.ep]); grp.append((x, y, role, R.randrange(2), s.work.get(role) or 'st', nrm, R.uniform(0.95, 1.05), R.uniform(0.9, 1.08)))
            if R.random() < 0.6:
                x, y = pos[0] - nrm[0] * 2.2, pos[1] - nrm[1] * 2.2
                if s.on_ground(x, y): grp.append((x, y, s.pick_role(R), R.randrange(2), 'st', nrm, 1.0, 1.0))
            if grp:
                t0 = (hr - H0) / (H1 - H0) * SEG; s.stand.append({'t0': t0, 't1': t0 + R.uniform(2.0, 4.0), 'people': grp, 'kind': 'viec'}); s.n_work += 1
        for k in range(2):    # gác: hai lính súng dựng, cả ngày tới chập tối
            pos, nrm = s.near_wall(R, 14.0, 40.0)
            if not pos: continue
            grp = []
            for j in (-1, 1):
                x, y = pos[0] - nrm[1] * 0.9 * j - nrm[0] * 0.4, pos[1] + nrm[0] * 0.9 * j - nrm[1] * 0.4
                if s.on_ground(x, y): grp.append((x, y, 'linh', j > 0, s.work.get('linh') or 'st', (-nrm[0], -nrm[1]), 1.0, 1.0))
            if grp: s.stand.append({'t0': 0.6, 't1': SEG * 0.78, 'people': grp, 'kind': 'gac'})

    def weights(s, hr):
        hs = [PASS_H[p] for p in ORDER]
        if hr <= hs[0]: return {'d1': 1.0}, 0.0
        for i in range(len(hs) - 1):
            if hs[i] <= hr <= hs[i + 1]:
                a = (hr - hs[i]) / (hs[i + 1] - hs[i]); a = a * a * (3 - 2 * a)
                return {ORDER[i]: 1 - a, ORDER[i + 1]: a}, (a if ORDER[i + 1] == 'n' else 0.0)
        return {'n': 1.0}, 1.0

    def face_index(s, role, wdir):
        """hướng sprite gần nhất với hướng đi (thế giới)."""
        best, bi = -9, 0
        for ai in range(s.na):
            d = s.dirs[(role, ai)]; c = d[0] * wdir[0] + d[1] * wdir[1]
            if c > best: best, bi = c, ai
        return bi

    def sprite(s, w, role, ai, pose):
        rk = role if role in s.sm else role
        c = s.cell[(rk, ai, pose)]; fx, fy = c['foot_px'][0] + PAD, c['foot_px'][1] + PAD; px = s.pxm; hw = s.sm[rk]['cellx'] / 2
        x0, x1 = int(fx - hw * px), int(fx + hw * px); y0, y1 = int(fy - 2.08 * px), int(fy + 0.12 * px)
        im = 0
        for p, wt in w.items():
            sh = s.sheet[(rk, PMAP[p])][y0:y1, x0:x1]
            if p == 'n': sh = sh * np.concatenate([NIGHT / 0.5, [1.0]]).astype(np.float32)   # đêm: sprite d2 tối + lam (alpha giữ)
            im = im + sh * wt
        return im, (fx - x0, fy - y0)

    def sun_vec(s, w):
        """hướng bóng (thế giới, ngang) + chiều dài bóng / chiều cao + độ đậm, trung bình theo trọng số lượt ngày."""
        out = []
        for p, wt in w.items():
            if p == 'n' or p not in s.sun or wt < 0.02: continue
            alt, az = s.sun[p]
            if alt is None or alt <= 1: continue
            dx, dy = -math.sin(math.radians(az)), -math.cos(math.radians(az))      # bóng đổ ngược phía mặt trời
            out.append((p, wt, dx, dy, min(8.0, 1 / math.tan(math.radians(alt)))))
        return out

    def stamp(s, img, im, foot, x, y, sc_, op, w, shadow=True, tone=1.0):
        p = s.proj(x, y, 0)
        if not p: return
        sc = s.fpx / p[2] / s.pxm * sc_
        h, wd = im.shape[:2]; nw, nh = max(1, int(wd * sc)), max(1, int(h * sc))
        if nh < 4: return
        sm = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA)
        ox, oy = int(round(p[0] - foot[0] * sc)), int(round(p[1] - foot[1] * sc))
        # nắng tại chân: người trong bóng nhà → bỏ phần nắng (tối + ngả lam)
        fxp, fyp = int(min(s.W - 1, max(0, p[0]))), int(min(s.H - 1, max(0, p[1] - 2)))
        lit = sum(s.sunvis[q][fyp, fxp] * wt for q, wt in w.items() if q in s.sunvis) / max(1e-6, sum(wt for q, wt in w.items() if q in s.sunvis)) if any(q in s.sunvis for q in w) else 0.0
        rgb = sm[..., :3]; yl = (rgb * np.array([0.2126, 0.7152, 0.0722], np.float32)).sum(-1, keepdims=True)
        rgb = yl + (rgb - yl) * 0.72                  # vải nhuộm thời kỳ: bớt bão hoà (chỉnh màu chung ×1,85 làm áo rực như nhựa)
        col = rgb * 0.85 * tone * (0.42 + 0.58 * lit) * np.array([1 - 0.12 * (1 - lit), 1.0, 1 + 0.15 * (1 - lit)], np.float32)
        al = np.clip(sm[..., 3], 0, 1)
        # bóng tiếp đất (che sáng trời dưới chân, mọi lúc): elip mềm rộng ~0,9 m × sâu ~0,5 m
        rx = max(1.5, 0.45 * s.fpx / p[2] * sc_); ry = max(1.0, rx * 0.32); cx_, cy_ = p[0], p[1]
        X0a, Y0a, X1a, Y1a = int(max(0, cx_ - 2 * rx)), int(max(0, cy_ - 2 * ry)), int(min(s.W, cx_ + 2 * rx)), int(min(s.H, cy_ + 2 * ry))
        if X1a > X0a and Y1a > Y0a:
            yy, xx = np.mgrid[Y0a:Y1a, X0a:X1a]; g = np.exp(-(((xx - cx_) / rx) ** 2 + ((yy - cy_) / ry) ** 2)) * 0.42 * op * s.ground[Y0a:Y1a, X0a:X1a]
            img[Y0a:Y1a, X0a:X1a] *= (1 - g[..., None])
        if shadow and lit > 0.05:
            for (q, wt, dx, dy, ln) in s.sun_vec(w):
                s.cast(img, al, nw, nh, ox, oy, p, x, y, dx, dy, ln, 0.55 * wt * op, q)
        X0, Y0 = max(0, ox), max(0, oy); X1, Y1 = min(s.W, ox + nw), min(s.H, oy + nh)
        if X1 <= X0 or Y1 <= Y0: return
        sub_c = col[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox]; sub_a = al[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox]
        vis = (s.depth[Y0:Y1, X0:X1] > p[3] - 0.6).astype(np.float32)
        k = vis * op                                  # EXR của Cycles (nền trong suốt): màu đã nhân alpha
        img[Y0:Y1, X0:X1] = img[Y0:Y1, X0:X1] * (1 - (sub_a * k)[..., None]) + sub_c * k[..., None]

    def cast(s, img, al, nw, nh, ox, oy, p, x, y, dx, dy, ln, strength, q):
        """bóng người: ảnh hình người (alpha) biến đổi phối cảnh: chân giữ nguyên, đỉnh đầu → chân + hướng bóng × chiều cao × cot(độ cao mặt trời)."""
        hm = nh / (s.fpx / p[2])                     # chiều cao ô (m)
        px_ = np.array([-dy, dx])                    # ngang, vuông góc hướng bóng
        half = (nw / 2) / (s.fpx / p[2])
        fx_, fy_ = p[0] - ox, p[1] - oy              # chân trong ô
        top = hm * (fy_ / nh)                        # phần trên mặt đất của ô (m)
        pts_w = [(x - px_[0] * half, y - px_[1] * half), (x + px_[0] * half, y + px_[1] * half),
                 (x + px_[0] * half + dx * top * ln, y + px_[1] * half + dy * top * ln), (x - px_[0] * half + dx * top * ln, y - px_[1] * half + dy * top * ln)]
        dst = [s.proj(a_, b_, 0) for a_, b_ in pts_w]
        if any(d is None for d in dst): return
        src = np.float32([[0, fy_], [nw, fy_], [nw, 0], [0, 0]]); dstp = np.float32([[d[0], d[1]] for d in dst])
        x0, y0 = int(max(0, dstp[:, 0].min() - 2)), int(max(0, dstp[:, 1].min() - 2)); x1, y1 = int(min(s.W, dstp[:, 0].max() + 3)), int(min(s.H, dstp[:, 1].max() + 3))
        if x1 <= x0 or y1 <= y0: return
        M = cv2.getPerspectiveTransform(src, dstp - np.float32([x0, y0]))
        m = cv2.warpPerspective(al, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
        m = cv2.GaussianBlur(m, (3, 3), 0.8) * strength * s.sunvis[q][y0:y1, x0:x1] * s.ground[y0:y1, x0:x1]
        img[y0:y1, x0:x1] *= (1 - m[..., None])

    def frame(s, t, hr, fseed):
        w, blue = s.weights(hr)
        img = sum(s.bg[p] * wt for p, wt in w.items()).copy()
        R = random.Random(fseed); people = []; n_carry = 0; n_pair = 0
        for g in s.stand:
            if g['t0'] <= t <= g['t1']:
                fade = min(1.0, (t - g['t0']) / 0.3, (g['t1'] - t) / 0.3)
                if hr > 19.6 and g['kind'] != 'gac': continue
                for (x, y, role, bi, pose, fd, sc_, tone) in g['people']:
                    rk = f'{role}~{int(bi)}'; ai = s.face_index(rk, fd); pp = s.proj(x, y, 0)
                    if pp: people.append((pp[2], 'st', x, y, rk, ai, pose, sc_, fade, tone))
        n_wk = 0
        for wk in s.walk:
            v = WALK * wk['spd']; dt = t - wk['t0']; dur = wk['L'] / v
            if not (0 <= dt <= dur): continue
            if hr > 19.6 and wk['u'] > 0.15: continue
            ux, uy = (wk['b'][0] - wk['a'][0]) / wk['L'], (wk['b'][1] - wk['a'][1]) / wk['L']
            rk = wk['role'] if wk['role'] == 'khieng' else f"{wk['role']}~{wk['b_']}"
            ai = s.face_index(rk, (ux, uy)); fade = min(1.0, dt / 0.25, (dur - dt) / 0.25)
            n_wk += 1 + (wk['role'] == 'khieng'); n_carry += bool(wk['carry']); n_pair += wk['role'] == 'khieng'
            for j, op in enumerate((1.0, 0.24, 0.12, 0.06, 0.03)):
                d = dt * v - j * 0.18 * wk['spd']
                if d < 0: break
                x, y = wk['a'][0] + ux * d, wk['a'][1] + uy * d
                ph = int(wk['ph0'] + (t * FPS) * wk['spd'] - j) % 8          # nhịp bước theo tốc độ riêng
                pose = (f"c{wk['carry']}{ph}" if wk['carry'] else f'w{ph}')
                pp = s.proj(x, y, 0)
                if pp: people.append((pp[2], 'wk', x, y, rk, ai, pose, wk['sc'], fade * op * (1.0 if j == 0 else 0.9), wk['tone']))
        people.sort(key=lambda r: -r[0])
        for (_, kind, x, y, rk, ai, pose, sc_, op, tone) in people:
            im, foot = s.sprite(w, rk, ai, pose)
            s.stamp(img, im, foot, x, y, sc_, op, w, shadow=op > 0.5, tone=tone)
        n_st = sum(1 for r in people if r[1] == 'st')
        if not A.nokhi: img = s.khi(img, w, hr, t)
        # khói, cờ, chim, giờ xanh, quầng đèn A, sao
        light = sum(wt * (0.05 if p == 'n' else 1.0) for p, wt in w.items()); warm = w.get('d4', 0) + 0.5 * w.get('d3', 0)
        smoke_col = np.array([0.55, 0.55, 0.56]) * (0.25 + 0.75 * light) * np.array([1.0, 1 - 0.15 * warm, 1 - 0.3 * warm])
        cook = 0.25 + math.exp(-((hr - 8.5) / 1.2) ** 2) + math.exp(-((hr - 18.5) / 1.5) ** 2)
        for i, (x, y, z) in enumerate(s.meta['chimneys']):
            rr = random.Random(i * 31 + s.ep); ship = z < 0
            if not ship and rr.random() > 0.35 * cook: continue
            p0 = s.proj(x, y, z)
            if not p0 or not (-50 < p0[0] < s.W + 50 and 0 < p0[1] < s.H): continue
            if s.depth[int(min(s.H - 1, max(0, p0[1]))), int(min(s.W - 1, max(0, p0[0])))] < p0[3] - 2: continue
            for j in range(10):
                age = j / 10 + R.random() * 0.08
                pp = s.proj(x - 9 * age * (1 + 2 * ship), y + 2 * age, z + (4 + 6 * ship) * age + R.uniform(-0.4, 0.4))
                if not pp: continue
                rad = max(1.5, s.fpx * (0.5 + 2.2 * age) * (1 + ship) / pp[2])
                s.puff(img, pp[0], pp[1], rad, smoke_col * (0.35 if ship else 1.0), (0.22 if not ship else 0.35) * (1 - age), pp[3])
        for (x, y, z) in s.meta['flags']: s.flag(img, x, y, z, light, warm, R)
        if light > 0.3:
            for b in range(R.randint(0, 4)):
                bx, by = R.uniform(0.05, 0.95) * s.W, R.uniform(0.03, 0.3) * s.H
                if not s.sky[int(by), int(bx)]: continue
                sz = R.uniform(2.5, 5.0) * s.W / 1920; c = (0.92, 0.92, 0.9) if R.random() < 0.5 else (0.25, 0.25, 0.27)
                cv2.polylines(img, [np.array([[bx - sz, by - sz * 0.35], [bx, by], [bx + sz, by - sz * 0.35]], np.int32)], False, c, max(1, int(s.W / 1920 + 0.5)), cv2.LINE_AA)
        if blue > 0:
            img = img * (1 - 0.35 * blue * (1 - blue) * 4) * (1 + (np.array([0.75, 0.85, 1.15]) - 1) * blue * 0.6)
        if w.get('n', 0) > 0.05 and s.ep == 1782:   # quầng đèn dầu tại đúng vị trí đèn của nền A (1943 phong toả: không quầng)
            for (x, y, z) in s.meta['lamps']:
                pp = s.proj(x, y, z)
                if not pp or not (0 <= pp[0] < s.W and 0 <= pp[1] < s.H) or s.depth[int(pp[1]), int(pp[0])] < pp[3] - 1.0: continue
                r = s.fpx * 1.6 / pp[2]
                s.puff(img, pp[0], pp[1], r * 3, np.array([1.0, 0.55, 0.22]) * 0.5, 0.5 * w['n'], pp[3])
                s.puff(img, pp[0], pp[1], max(1.5, r * 0.5), np.array([1.0, 0.85, 0.6]), 0.9 * w['n'], pp[3])
        if w.get('n', 0) > 0.3: s.stars(img, w['n'])
        n_grp = sum(1 for g in s.stand if g['t0'] <= t <= g['t1'] and (hr <= 19.6 or g['kind'] == 'gac'))
        return img, {'weights': {k: round(v, 3) for k, v in w.items()}, 'nguoi_dung': n_st, 'nguoi_di': n_wk, 'nguoi_tren_hinh': n_st + n_wk,
                     'nhom_dung': n_grp, 'nguoi_mang_vat': n_carry, 'cap_khieng': n_pair}

    def khi(s, img, w, hr, t):
        """sương/khói phố theo độ sâu + tia nắng/bụi trong nắng + chiều sâu tông. Không nguồn sáng mới: mọi ánh sáng tán xạ lấy từ chính nền
        (màu trời gần chân trời của lượt, lượt nắng của A); đêm chỉ còn sương nhận ánh trăng (rất mờ)."""
        if not hasattr(s, 'hz_col'):
            hz = s.sky & (np.arange(s.H)[:, None] > s.H * 0.2)
            s.hz_col = {p: (s.bg[p][hz].mean(0) if hz.sum() > 50 else s.bg[p][s.sky].mean(0)) for p in ORDER}
            yy, xx = np.mgrid[0:s.H, 0:s.W].astype(np.float32); s.xx, s.yy = xx, yy
            rr = np.random.RandomState(s.ep); s.noise = cv2.resize(rr.rand(18, 32).astype(np.float32), (s.W * 2, s.H), interpolation=cv2.INTER_CUBIC)
            s.dust = rr.rand(int(900 * s.W / 1920), 4).astype(np.float32)
        col = sum(s.hz_col[p] * wt for p, wt in w.items()); night = w.get('n', 0.0)
        dpt = np.minimum(s.depth, 4000.0)
        morning = math.exp(-((hr - 8.8) / 1.3) ** 2); evening = math.exp(-((hr - 18.3) / 1.2) ** 2)   # khói bếp sáng/chiều
        dens = (0.0042 + 0.004 * morning + 0.003 * evening) * (1 - 0.6 * night)
        sh = int((t * 6) % s.W); nz = s.noise[:, sh:sh + s.W] if sh + s.W <= s.noise.shape[1] else np.roll(s.noise, -sh, 1)[:, :s.W]
        fog = 1 - np.exp(-dpt * dens * (0.7 + 0.6 * nz))
        fog = np.where(s.sky, 0.0, fog)[..., None]
        fcol = col * (1 - night) * 0.95 + night * np.array([0.004, 0.006, 0.011]) + (np.array([0.02, 0.015, 0.01]) * (morning + evening) * (1 - night))
        img = img * (1 - fog) + fcol * fog
        # tia nắng + bụi: lượt nắng của A (đất/tường có nắng) → quét mờ hướng về phía mặt trời trên màn hình; chỉ ban ngày
        sv = sum(s.sunvis[p] * wt for p, wt in w.items() if p in s.sunvis)
        day = 1 - night
        if day > 0.05 and isinstance(sv, np.ndarray):
            alt_az = [(s.sun[p], wt) for p, wt in w.items() if p in s.sun and wt > 0.05]
            if alt_az:
                (alt, az), _ = max(alt_az, key=lambda q: q[1])
                sd = np.array([math.sin(math.radians(az)) * math.cos(math.radians(alt)), math.cos(math.radians(az)) * math.cos(math.radians(alt)), math.sin(math.radians(alt))])
                zc = sd @ s.f; sx = s.W / 2 + s.fpx * (sd @ s.r) / max(zc, 0.05); sy = s.H / 2 - s.fpx * (sd @ s.u) / max(zc, 0.05)
                back = max(0.0, zc)                                   # ngược sáng: tán xạ mạnh khi mặt trời trước máy
                src = (sv * (dpt < 120) + 1.4 * s.sky).astype(np.float32) * (s.depth > 6)
                acc = np.zeros_like(src); k = 0
                for q in np.linspace(0.0, 0.32, 9):                     # mờ hướng tâm về phía mặt trời
                    M = np.float32([[1 - q, 0, q * sx], [0, 1 - q, q * sy]]); acc += cv2.warpAffine(src, M, (s.W, s.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT); k += 1
                acc /= k
                warm = w.get('d4', 0) + 0.5 * w.get('d3', 0)
                scol = np.array([1.0, 0.93 - 0.15 * warm, 0.82 - 0.3 * warm]) * float(np.mean(col)) * 1.6
                amt = (0.05 + 0.22 * back) * day * (1 - np.exp(-dpt / 60.0))
                img = img + (acc * amt)[..., None] * scol
                # bụi: hạt sáng nhỏ trôi chậm, chỉ trong không khí có nắng ở 8–30 m
                dd = s.dust; xs = ((dd[:, 0] * s.W + t * 9 * (dd[:, 2] - 0.3)) % s.W).astype(int); ys = ((dd[:, 1] * s.H * 0.9 + t * 4 * (dd[:, 3] - 0.5)) % s.H).astype(int)
                lit = sv[ys, xs] * (s.depth[ys, xs] > 9) * (0.3 + back)
                img[ys, xs] += (lit * 0.06 * day)[:, None] * scol
        return img

    def puff(s, img, x, y, r, col, a, dist):
        r = int(max(2, r)); X0c, Y0c, X1c, Y1c = max(0, int(x - 2 * r)), max(0, int(y - 2 * r)), min(s.W, int(x + 2 * r)), min(s.H, int(y + 2 * r))
        if X1c <= X0c or Y1c <= Y0c: return
        yy, xx = np.mgrid[Y0c:Y1c, X0c:X1c]; g = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * r * r)) * a * (s.depth[Y0c:Y1c, X0c:X1c] > dist - 3)
        img[Y0c:Y1c, X0c:X1c] = img[Y0c:Y1c, X0c:X1c] * (1 - g[..., None]) + col * g[..., None]

    def flag_img(s, phase):
        """Union flag: 1782 = bản 1707–1801 (chữ thập St George trên chéo trắng St Andrew, KHÔNG chéo đỏ St Patrick); 1943 = bản 1801."""
        Wf, Hf = 300, 150; im = Image.new('RGB', (Wf, Hf), (16, 36, 104)); d = ImageDraw.Draw(im)
        d.line([(0, 0), (Wf, Hf)], fill=(245, 245, 245), width=30); d.line([(0, Hf), (Wf, 0)], fill=(245, 245, 245), width=30)
        if s.ep == 1943:
            d.line([(0, -4), (Wf / 2, Hf / 2 - 4)], fill=(200, 16, 46), width=10); d.line([(Wf / 2, Hf / 2 + 4), (Wf, Hf + 4)], fill=(200, 16, 46), width=10)
            d.line([(0, Hf + 4), (Wf / 2, Hf / 2 + 4)], fill=(200, 16, 46), width=10); d.line([(Wf / 2, Hf / 2 - 4), (Wf, -4)], fill=(200, 16, 46), width=10)
        d.rectangle([Wf / 2 - 25, 0, Wf / 2 + 25, Hf], fill=(245, 245, 245)); d.rectangle([0, Hf / 2 - 25, Wf, Hf / 2 + 25], fill=(245, 245, 245))
        d.rectangle([Wf / 2 - 15, 0, Wf / 2 + 15, Hf], fill=(200, 16, 46)); d.rectangle([0, Hf / 2 - 15, Wf, Hf / 2 + 15], fill=(200, 16, 46))
        a = LC.srgb2lin(np.asarray(im).astype(np.float32) / 255)
        xs = np.arange(Wf); off = (np.sin(xs / Wf * 2 * math.pi * 1.6 + phase) * 6 * xs / Wf).astype(int)
        b = np.zeros_like(a)
        for xx in range(Wf): b[:, xx] = np.roll(a[:, xx], off[xx], axis=0)
        return b * (0.8 + 0.2 * np.cos(xs / Wf * 2 * math.pi * 1.6 + phase))[None, :, None]

    def flag(s, img, x, y, z, light, warm, R):
        L, Hm = 2.6, 1.3; dx, dy = -0.9, 0.45; n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
        cs = [s.proj(x, y, z), s.proj(x + dx * L, y + dy * L, z - 0.15), s.proj(x + dx * L, y + dy * L, z - Hm - 0.15), s.proj(x, y, z - Hm)]
        if any(c is None for c in cs): return
        dst = np.float32([[c[0], c[1]] for c in cs])
        if dst[:, 0].max() < 0 or dst[:, 0].min() > s.W: return
        f = s.flag_img(R.uniform(0, 6.28)) * (0.15 + 0.85 * light) * np.array([1.0, 1 - 0.12 * warm, 1 - 0.25 * warm])
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [299, 0], [299, 149], [0, 149]]), dst)
        warped = cv2.warpPerspective(f.astype(np.float32), M, (s.W, s.H)); mask = cv2.warpPerspective(np.ones((150, 300), np.float32), M, (s.W, s.H)) * (s.depth > cs[0][3] - 1)
        img[:] = img * (1 - mask[..., None]) + warped * mask[..., None]

    def stars(s, img, wn):
        rr = np.random.RandomState(7); n = int(220 * s.W / 1920)
        xs = rr.randint(0, s.W, n); ys = rr.randint(0, int(s.H * 0.45), n); br = rr.uniform(0.02, 0.12, n) * wn
        for x, y, b in zip(xs, ys, br):
            if s.sky[y, x]: img[y, x] += b

GRADE = {'sat': 1.85, 'contrast': 0.42, 'warm': 0.04}   # chỉnh màu chung PT (A-thuần, và LAI khi --grade chung)
GRADE_LAI = {'sat': 1.18, 'contrast': 0.46, 'warm': 0.025, 'sat_hi': 0.82}   # P2-3: LAI riêng — tấm C đã giàu màu; bớt bão hoà, giữ tương phản (đo §5)
def grade(img):
    if (A.grade or ('lai' if A.ban == 'LAI' else 'chung')) == 'lai': return grade_lai(img)
    x = np.clip(img, 0, None); out = LC.lin2srgb(x / (1 + 0.15 * x))
    Y = (out * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True); out = Y + (out - Y) * GRADE['sat']
    sc_ = out * out * (3 - 2 * out); out = out + (np.clip(sc_, 0, 1) - out) * GRADE['contrast']
    return np.clip(out * np.array([1 + GRADE['warm'], 1.0, 1 - GRADE['warm']]), 0, 1)

def grade_lai(img):
    G = GRADE_LAI; x = np.clip(img, 0, None); out = LC.lin2srgb(x / (1 + 0.15 * x))
    Y = (out * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
    k = G['sat'] * (1 - (1 - G['sat_hi']) * np.clip((out.max(-1, keepdims=True) - out.min(-1, keepdims=True) - 0.25) / 0.4, 0, 1))   # màu đã đậm: tăng ít hơn
    out = Y + (out - Y) * k
    sc_ = out * out * (3 - 2 * out); out = out + (np.clip(sc_, 0, 1) - out) * G['contrast']
    return np.clip(out * np.array([1 + G['warm'], 1.0, 1 - G['warm']]), 0, 1)

def overlay(rgb8, yr, lab, notext, scale):
    if notext: return rgb8
    im = Image.fromarray(rgb8); d = ImageDraw.Draw(im); W, H = im.size
    fy = ImageFont.truetype(FONT_B, int(78 * scale)); fl = ImageFont.truetype(FONT_R, max(12, int(38 * scale)))   # ≥ 38 px @1080p
    txt = str(yr); bb = d.textbbox((0, 0), txt, font=fy); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x, y = W - tw - int(60 * scale), H - th - int(64 * scale)
    d.rounded_rectangle([x - 22 * scale, y - 16 * scale, x + tw + 22 * scale, y + th + 26 * scale], radius=int(10 * scale), fill=(14, 14, 16))
    d.text((x - bb[0], y - bb[1]), txt, font=fy, fill=(245, 236, 214))
    lines = (LABEL_L if A.ban == 'LAI' else LABEL_A)[lab]
    ly = H - int(56 * scale) - 2 * int(48 * scale)
    for i, line in enumerate(lines):
        bb = d.textbbox((0, 0), line, font=fl)
        d.rectangle([int(52 * scale), ly + i * int(48 * scale) - 6 * scale, int(52 * scale) + bb[2] + 16 * scale, ly + i * int(48 * scale) + bb[3] + 6 * scale], fill=(14, 14, 16))
        d.text((int(60 * scale), ly + i * int(48 * scale)), line, font=fl, fill=(230, 226, 214))
    return np.asarray(im)

def timeline(t):
    if t < SEG: return 1782, H0 + (H1 - H0) * t / SEG, t, 0.0, 1782, 1782
    if t < SEG + TR:
        a = (t - SEG) / TR; a2 = a * a * (3 - 2 * a); return 'tr', None, None, a2, int(round(1782 + (1943 - 1782) * a2)), None
    tt = t - SEG - TR; return 1943, H0 + (H1 - H0) * tt / SEG, tt, 0.0, 1943, 1943

def run(W, H, frames, write_video, stills_at, notext):
    class Lazy(dict):
        def __missing__(self, ep): self[ep] = Epoch(ep, W, H); return self[ep]
    E = Lazy(); scale = W / 1920
    log = open(os.path.join(A.out, f'log-{A.ban}-{W}x{H}.jsonl'), 'w'); ff = None
    if write_video:
        out = os.path.join(A.out, f'pt4-{A.ban}-{W}x{H}.mp4')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for f in frames:
        t = f / FPS; ep, hr, tt, mix, yr, lab = timeline(t)
        if ep == 'tr':
            a_img, ia = E[1782].frame(SEG, H1, f); b_img, ib = E[1943].frame(0.0, H0, f)
            img = a_img * (1 - mix) + b_img * mix; info = {'tr': round(mix, 3), 'a': ia, 'b': ib}; lab = 1782 if mix < 0.5 else 1943
        else:
            img, info = E[ep].frame(tt, hr, f * 7919 + ep)
        rgb = overlay((grade(img) * 255 + 0.5).astype(np.uint8), yr, lab, notext, scale)
        rec = {'f': f, 't': round(t, 3), 'epoch': ep, 'gio_ao': None if hr is None else round(hr, 3), 'nam': yr, 'ban': A.ban, 'ai_image': A.ban == 'LAI',
               'nhan_phuong_phap': (not notext) and A.ban == 'LAI', **info}
        log.write(json.dumps(rec, ensure_ascii=False) + '\n')
        if ff: ff.stdin.write(rgb.tobytes())
        if f in stills_at:
            Image.fromarray(rgb).save(os.path.join(A.out, f'{stills_at[f]}-{A.ban}{"-notext" if notext else ""}.jpg'), quality=92)
            if notext: Image.fromarray(rgb).save(os.path.join(A.out, f'{stills_at[f]}-{A.ban}-notext.png'))   # PNG không tổn hao để đo vùng bảo vệ
    if ff: ff.stdin.close(); ff.wait()
    log.close()

if __name__ == '__main__':
    N = int(TOTAL * FPS); frames = range(N)
    if A.frames: a, b = map(int, A.frames.split(':')); frames = range(a, b)
    def fr_of(ep, hr): return int(round((((hr - H0) / (H1 - H0)) * SEG + (0 if ep == 1782 else SEG + TR)) * FPS))
    # khung tĩnh khai TRƯỚC (như PT): sáng 10,0 · trưa 12,8 (= lượt d2, giờ của tấm C) · chiều vàng 17,55 · đêm 21,8
    ST = {fr_of(e, h): f'{e}-{n}' for e in (1782, 1943) for n, h in (('sang', 10.0), ('trua', 12.8), ('chieu', 17.55), ('dem', 21.8))}
    if A.stillset: ST = {int(x.split(':')[1]): x.split(':')[0] for x in A.stillset.split(',')}
    if A.video:
        W, H = map(int, A.video.split('x')); run(W, H, frames, True, {}, A.notext)
    if A.stills:
        W, H = map(int, A.stills.split('x')); run(W, H, sorted(ST), False, ST, A.notext)
    json.dump({'stills': {str(k): v for k, v in ST.items()}, 'fps': FPS, 'seg': SEG, 'tr': TR, 'crowd_speed': CROWD}, open(os.path.join(A.out, 'stills.json'), 'w'), indent=1)
