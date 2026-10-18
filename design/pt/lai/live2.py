"""PT2 · lớp sống TRÊN CÙNG (HC3) — ghép lên nền LAI (A+C) hoặc A-thuần, CÙNG hạt giống ⇒ hai bản có lớp sống giống hệt nhau.
- Người: tờ sprite MakeHuman/MPFB (mh_people.py), 8 hướng × (đứng + chu kỳ đi 8 khung); đám đông theo giờ ảo; 10–60 m; tốc độ đám đông ×3
  (một chu kỳ bước = 8 khung @24 fps), vệt mờ phơi sáng = 5 dấu lùi dọc đường đi (0,18 m/dấu), độ mờ 1 / 0,24 / 0,12 / 0,06 / 0,03.
- Bóng người: hình bóng chiếu theo hướng mặt trời của từng lượt nền (sun_alt/az trong meta), CHỈ trên mặt đất đang có nắng ở lượt nắng của cảnh A;
  người đứng trong bóng nhà → tắt nắng trên người (tối + ngả lam trời).
- Cờ (vẽ 2D, đúng mẫu theo nguồn: 1782 = Union flag 1707–1801, KHÔNG chéo đỏ St Patrick; 1943 = bản 1801), khói ống khói/tàu, hải âu, sao.
  KHÔNG đèn pha phòng không (PT có — không có nguồn trong TIEN-KY), đêm 1943 phong toả: không đèn nào ngoài đèn của nền A.
- Nhãn: LAI có dòng phương pháp "Surface detail AI-assisted · layout, landmarks & flags from sources" ≥ 38 px góc dưới trái SUỐT shot;
  A-thuần giữ nhãn nguồn của PT. Bộ đếm năm dưới phải. Log mỗi khung: ai_image true/false.
  /opt/cine/bin/python -I live2.py --ban LAI|A --out DIR [--video 960x540] [--stills 1920x1080] [--notext] [--stillset ten:khung,...]"""
import os, sys, json, math, argparse, subprocess, random
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'scene'))
import lai_common as LC
os.environ['PT_CAM'] = 'pt'
import pt_site as S
ap = argparse.ArgumentParser(); ap.add_argument('--ban', default='LAI'); ap.add_argument('--out', required=True)
ap.add_argument('--bg', default='/var/tmp/pt2/bg'); ap.add_argument('--spr', default='/var/tmp/pt2/spr')
ap.add_argument('--video', default=''); ap.add_argument('--stills', default=''); ap.add_argument('--notext', action='store_true'); ap.add_argument('--stillset', default='')
ap.add_argument('--frames', default='')
A = ap.parse_args(); os.makedirs(A.out, exist_ok=True)
FPS = 24; SEG = 9.0; TR = 2.0; TOTAL = SEG * 2 + TR
PASS_H = json.load(open(os.path.join(HERE, '..', 'scene', 'passes.json'))); PASS_H['n'] = 20.6
ORDER = ['d1', 'd2', 'd3', 'd4', 'n']; DAY = ORDER[:4]
H0, H1 = 8.6, 22.4
PAD = 300
CROWD = 3.0; WALK = 1.35 * CROWD     # m/s trên phim
FONT_B = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'; FONT_R = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
LABEL_A = {1782: ['Reconstructed from J. Drinkwater, Plan of the Batteries, 1782', 'Facades: procedural, period style · not a photograph'],
           1943: ['Buildings: OpenStreetMap, checked against U.S. Army Map Service plan, 1943', 'Map data from OpenStreetMap (ODbL) · facades procedural']}
LABEL_L = {1782: ['Reconstructed from J. Drinkwater, Plan of the Batteries, 1782', 'Surface detail AI-assisted · layout, landmarks & flags from sources'],
           1943: ['Buildings: OpenStreetMap, checked against U.S. Army Map Service plan, 1943', 'Surface detail AI-assisted · layout, landmarks & flags from sources']}
CAMK = {1782: 'k1782', 1943: 'pt'}
# vai và tỉ lệ theo thời kỳ: 1782 phố sau pháo kích 4/1781 dân chạy về nam (S062) → chủ yếu quân đồn trú; 1943 KHÔNG phụ nữ/trẻ em (sơ tán 1940, S114)
ROLEW = {1782: {'linh': 0.34, 'linh2': 0.22, 'phao_binh': 0.16, 'thuy_thu': 0.12, 'dan_nam': 0.12, 'dan_nu': 0.04},
         1943: {'linh': 0.28, 'linh2': 0.22, 'thuy_thu': 0.17, 'thuy_thu_trang': 0.08, 'raf': 0.12, 'tho': 0.13}}

def busy(hr): return max(0.66 if hr < 19.6 else 0.04, math.exp(-((hr - 11.5) / 3.2) ** 2) + 0.8 * math.exp(-((hr - 17.5) / 1.8) ** 2))   # sàn ban ngày: ≥ 30 người/khung (HC3)

class Epoch:
    def __init__(s, ep, W, H):
        s.ep = ep; s.W, s.H = W, H
        d = os.path.join(A.bg, f'{ep}{"L" if A.ban == "LAI" else "A"}'); s.meta = json.load(open(os.path.join(d, 'meta.json')))
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
        # sprite
        sp = A.spr + str(ep); js = [f for f in os.listdir(sp) if f.startswith('sprites-') and f.endswith('.json')]
        s.sm = {}
        for f in js: s.sm.update(json.load(open(os.path.join(sp, f)))['roles'])
        smeta = json.load(open(os.path.join(sp, js[0]))); s.pxm = smeta['pxm']; s.na = smeta['na']
        s.sheet = {}
        import OpenEXR
        for role in s.sm:
            for p in ORDER:
                c = OpenEXR.File(os.path.join(sp, f'{role}_{p}.exr')).parts[0].channels['ViewLayer.Combined'].pixels.astype(np.float32)
                s.sheet[(role, p)] = np.pad(c, ((PAD, PAD), (PAD, PAD), (0, 0)))      # tuyến tính, màu đã nhân alpha (Cycles, film trong suốt); đệm biên
        s.dirs = {}
        for role, rm in s.sm.items():
            for c in rm['cells']: s.dirs[(role, c['a'])] = np.array(c['dir'])
        s.cell = {(role, c['a'], c['p']): c for role, rm in s.sm.items() for c in rm['cells']}
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

    def plan(s):
        """người đi: tuyến thẳng giữa hai điểm mặt đất nhìn thấy (10–60 m), mọi điểm giữa cũng trên mặt đất; giờ xuất phát theo mật độ busy(giờ ảo)."""
        R = s.rng; s.walk = []; s.stand = []
        tries = 0
        while len(s.walk) < 140 and tries < 20000:   # luật 30–80 người/khung (HC3)
            tries += 1
            t0 = R.uniform(-8.0, SEG); hr = H0 + (H1 - H0) * max(0, t0) / SEG
            if R.random() > busy(hr) * (0.12 if hr > 19.6 else 1.0): continue   # đêm: rất ít người (1943 phong toả)
            a, b = s.ground_pt(), s.ground_pt()
            if not a or not b or math.dist(a, b) < 8: continue
            if not all(s.on_ground(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u) for u in (0.25, 0.5, 0.75)): continue
            s.walk.append({'t0': t0, 'a': a, 'b': b, 'L': math.dist(a, b), 'role': s.pick_role(R), 'ph0': R.randrange(8), 'sc': R.uniform(0.95, 1.05), 'u': R.random()})
        for k in range(26):   # nhóm đứng (trò chuyện, gác) — hiện/tắt theo giờ ảo
            hr = R.uniform(H0, H1)
            if R.random() > busy(hr): continue
            c = s.ground_pt(10.0, 55.0)
            if not c: continue
            n = R.choice((1, 2, 2, 3)); dur = R.uniform(0.8, 2.6)
            grp = []
            for _ in range(n):
                x, y = c[0] + R.uniform(-0.9, 0.9), c[1] + R.uniform(-0.9, 0.9)
                if s.on_ground(x, y): grp.append((x, y, s.pick_role(R), R.randrange(8), R.uniform(0.95, 1.05)))
            s.stand.append({'t0': (hr - H0) / (H1 - H0) * SEG, 't1': (hr - H0) / (H1 - H0) * SEG + dur, 'people': grp})

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

    def sprite(s, w, role, ai, pi):
        c = s.cell[(role, ai, pi)]; fx, fy = c['foot_px'][0] + PAD, c['foot_px'][1] + PAD; px = s.pxm
        x0, x1 = int(fx - 0.85 * px), int(fx + 0.85 * px); y0, y1 = int(fy - 2.08 * px), int(fy + 0.12 * px)
        im = sum(s.sheet[(role, p)][y0:y1, x0:x1] * wt for p, wt in w.items())
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

    def stamp(s, img, im, foot, x, y, sc_, op, w, shadow=True):
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
        col = rgb * 0.85 * (0.42 + 0.58 * lit) * np.array([1 - 0.12 * (1 - lit), 1.0, 1 + 0.15 * (1 - lit)], np.float32)
        al = np.clip(sm[..., 3], 0, 1)
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
        R = random.Random(fseed); people = []
        # người đứng
        for g in s.stand:
            if g['t0'] <= t <= g['t1']:
                fade = min(1.0, (t - g['t0']) / 0.3, (g['t1'] - t) / 0.3)
                for (x, y, role, ai, sc_) in g['people']: people.append((s.proj(x, y, 0)[2], 'st', x, y, role, ai, 0, sc_, fade))
        # người đi (+ vệt phơi sáng: 5 dấu lùi theo đường, 0,9 m mỗi dấu ở tốc độ ×3)
        n_wk = 0
        for wk in s.walk:
            dt = t - wk['t0']; dur = wk['L'] / WALK
            if not (0 <= dt <= dur): continue
            if hr > 19.6 and wk['u'] > 0.15: continue          # đêm: chỉ ~15 % người còn đi (1943 phong toả; 1782 đêm vây)
            ux, uy = (wk['b'][0] - wk['a'][0]) / wk['L'], (wk['b'][1] - wk['a'][1]) / wk['L']
            ai = s.face_index(wk['role'], (ux, uy)); fade = min(1.0, dt / 0.25, (dur - dt) / 0.25)
            n_wk += 1
            for j, op in enumerate((1.0, 0.24, 0.12, 0.06, 0.03)):
                d = dt * WALK - j * 0.18
                if d < 0: break
                x, y = wk['a'][0] + ux * d, wk['a'][1] + uy * d
                ph = (wk['ph0'] + int(round(t * FPS)) - j) % 8
                pp = s.proj(x, y, 0)
                if pp: people.append((pp[2], 'wk', x, y, wk['role'], ai, ph + 1, wk['sc'], fade * op * (1.0 if j == 0 else 0.9)))
        people.sort(key=lambda r: -r[0])     # xa trước
        for (_, kind, x, y, role, ai, pi, sc_, op) in people:
            im, foot = s.sprite(w, role, ai, pi if kind == 'wk' else 0)
            s.stamp(img, im, foot, x, y, sc_, op, w, shadow=op > 0.5)
        n_st = sum(1 for r in people if r[1] == 'st')
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
        return img, {'weights': {k: round(v, 3) for k, v in w.items()}, 'nguoi_dung': n_st, 'nguoi_di': n_wk,
                     'nguoi_tren_hinh': n_st + n_wk}

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

GRADE = {'sat': 1.85, 'contrast': 0.42, 'warm': 0.04}   # chỉnh màu chung PT cho MỌI khung, cả hai bản
def grade(img):
    x = np.clip(img, 0, None); out = LC.lin2srgb(x / (1 + 0.15 * x))
    Y = (out * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True); out = Y + (out - Y) * GRADE['sat']
    sc_ = out * out * (3 - 2 * out); out = out + (np.clip(sc_, 0, 1) - out) * GRADE['contrast']
    return np.clip(out * np.array([1 + GRADE['warm'], 1.0, 1 - GRADE['warm']]), 0, 1)

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
        out = os.path.join(A.out, f'pt2-{A.ban}-{W}x{H}.mp4')
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
