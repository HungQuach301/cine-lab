"""PT · ghép lớp sống lên nền tĩnh (máy cố định = phim trường): nền mỗi thời kỳ dựng MỘT lần ở 5 lượt chiếu sáng, chỉ lớp sống chuyển động.
- ngày→đêm: hoà các lượt nền theo "giờ ảo" (cùng hình học, cùng máy) + giờ xanh (tối dần, ngả lam) trước lượt đêm;
- người: sprite thủ tục (people.py) cùng lượt chiếu sáng, đặt theo chiếu phối cảnh của máy neo, che khuất bằng lượt khoảng cách của cảnh;
  người đi = vệt mờ phơi sáng dài (bộ đếm chạy nhanh: mỗi khung ≈ 3–4 phút ảo); người đứng (gác, nhóm, chợ, đội hình) hiện rồi tắt;
- khói ống khói/ống tàu, hải âu, cờ (Union flag đúng thời kỳ: 1782 bản trước 1801; 1943 bản 1801), đèn pha phòng không 1943 (đêm phong toả ánh sáng);
- chuyển F1: hoà chéo đêm 1782 → sáng 1943 trong khi bộ đếm năm chạy nhanh; bộ đếm năm dưới-phải (F2); nhãn phương pháp dưới-trái (kiểu SH §5).
Không dùng mô hình AI ở bất kỳ bước nào. Nhánh B chỉ khác nền (vân AI) → mọi khung ghi `ai_texture: true` trong log.
  /opt/cine/bin/python -I live.py --tex A|B --out DIR [--video 960x540] [--stills 1920x1080] [--frames a:b]"""
import os, sys, json, math, argparse, subprocess, random, hashlib
os.environ.setdefault('OPENCV_IO_ENABLE_OPENEXR', '1')
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pt_site as S
ap = argparse.ArgumentParser(); ap.add_argument('--tex', default='A'); ap.add_argument('--out', required=True)
ap.add_argument('--bg', default='/var/tmp/pt/final'); ap.add_argument('--spr', default='/var/tmp/pt/spr')
ap.add_argument('--video', default=''); ap.add_argument('--stills', default=''); ap.add_argument('--frames', default=''); ap.add_argument('--notext', action='store_true')
A = ap.parse_args(); os.makedirs(A.out, exist_ok=True)
FPS = 24; SEG = 9.0; TR = 2.0; TOTAL = SEG * 2 + TR      # 9 s 1782 · 2 s chuyển · 9 s 1943
PASS_H = json.load(open(os.path.join(HERE, 'passes.json'))); PASS_H['n'] = 20.6
ORDER = ['d1', 'd2', 'd3', 'd4', 'n']
H0, H1 = 8.6, 22.4                                              # giờ ảo đầu/cuối mỗi đoạn
FONT_B = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'; FONT_R = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
LABEL = {1782: ['Reconstructed from J. Drinkwater, Plan of the Batteries, 1782', 'Facades: procedural, period style · not a photograph'],
         1943: ['Buildings: OpenStreetMap, checked against U.S. Army Map Service plan, 1943', 'Map data from OpenStreetMap (ODbL) · facades procedural']}

def srgb2lin(a): return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
def lin2srgb(a): a = np.clip(a, 0, 1); return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)

class Epoch:
    def __init__(s, ep, W, H):
        s.ep = ep; d = os.path.join(A.bg, f'{ep}{A.tex}'); s.meta = json.load(open(os.path.join(d, 'meta.json')))
        s.W, s.H = W, H; s.k = W / s.meta['camera']['W']
        s.bg = {}
        for p in ORDER:
            im = cv2.imread(os.path.join(d, p + '.png'), cv2.IMREAD_UNCHANGED)[..., :3][..., ::-1].astype(np.float32) / 65535.0
            s.bg[p] = srgb2lin(cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA))
        import OpenEXR   # bản OpenCV của môi trường không đọc EXR
        dep = list(OpenEXR.File(os.path.join(d, 'depth.exr')).channels().values())[0].pixels
        dep = dep[..., 0] if dep.ndim == 3 else dep
        s.depth = cv2.resize(dep.astype(np.float32), (W, H), interpolation=cv2.INTER_NEAREST)
        s.sky = s.depth > 20000
        # phối cảnh không khí: màu mù lấy từ trời sát chân trời của chính lượt đó
        s.haze = {}
        hz = s.sky & (np.arange(H)[:, None] > H * 0.25)
        s.bg['n'] *= 3.0 if ep == 1782 else 1.6        # lượt đêm: nâng phơi sáng (trăng) — mắt người xem TV vẫn đọc được hình khối
        for p in ORDER:
            c = s.bg[p][hz].mean(0) if hz.sum() > 50 else s.bg[p][s.sky].mean(0); s.haze[p] = c
            T = np.exp(-np.minimum(s.depth, 30000) / (5500 if p != 'n' else 1e9))[..., None]
            amt = 0.85 if p != 'n' else 0.0
            s.bg[p] = np.where(s.sky[..., None], s.bg[p], s.bg[p] * (1 - amt * (1 - T)) + c * amt * (1 - T))
        # sprite
        sp = os.path.join(A.spr + str(ep)); s.sm = json.load(open(os.path.join(sp, 'sprites.json')))
        s.sheet = {p: cv2.imread(os.path.join(sp, f'sprites_{p}.png'), cv2.IMREAD_UNCHANGED)[..., [2, 1, 0, 3]].astype(np.float32) / 255.0 for p in ORDER}
        for p in ORDER:
            s.sheet[p][..., :3] = srgb2lin(s.sheet[p][..., :3])
        s.cell = {(c['role'], c['face'], c['walk']): c for c in s.sm['cells']}
        s.polys = [b['pts'] for b in S.load(ep, kinds=['nha', 'khoi_pho', 'phao_dai', 'cong_su'], R=330) if not b['line']]
        cam = s.meta['camera']; s.fpx = cam['fpx'] * s.k; s.ch = cam['pos'][2]
        h = math.radians(cam['head']); p_ = math.radians(cam['pitch'])
        s.f = np.array([math.sin(h) * math.cos(p_), math.cos(h) * math.cos(p_), math.sin(p_)]); s.r = np.array([math.cos(h), -math.sin(h), 0.0]); s.u = np.cross(s.r, s.f)
        s.rng = random.Random(ep); s.plan_people()

    def proj(s, x, y, z):
        d = np.array([x, y, z - s.ch]); zc = d @ s.f
        if zc < 0.5: return None
        return (s.W / 2 + s.fpx * (d @ s.r) / zc, s.H / 2 - s.fpx * (d @ s.u) / zc, zc, float(np.linalg.norm(d)))

    def free(s, x, y):
        if any(S.inside(x, y, q) for q in s.polys): return False
        if x < -104: return False
        p = s.proj(x, y, 0)
        if not p or not (0 < p[0] < s.W and 0 < p[1] < s.H): return False
        if p[3] < 10.0: return False                                # người ≥ 10 m (lệnh)
        return s.depth[int(p[1]), int(p[0])] > p[3] - 1.5       # điểm chân không bị nhà che

    def rand_free(s, dmax=130.0):
        """lấy mẫu theo ĐIỂM ẢNH mặt đất nhìn thấy (mật độ người ∝ diện tích trên khung, gần nhiều hơn xa), khoảng cách 10–dmax m."""
        for _ in range(600):
            u, v = s.rng.uniform(0, s.W - 1), s.rng.uniform(s.H * 0.5, s.H - 1)
            d = s.f + ((u - s.W / 2) / s.fpx) * s.r - ((v - s.H / 2) / s.fpx) * s.u
            if d[2] >= -1e-3: continue
            t = -s.ch / d[2]; x, y = t * d[0], t * d[1]; dist = t * float(np.linalg.norm(d))
            if not (10.0 <= dist <= dmax): continue
            if abs(s.depth[int(v), int(u)] - dist) > 0.04 * dist + 0.3: continue       # điểm ảnh này đúng là mặt đất
            if any(S.inside(x, y, q) for q in s.polys) or x < -104: continue
            return (x, y)
        return None

    def plan_people(s):
        R = s.rng; roles = list({c['role'] for c in s.sm['cells']}); s.stand = []; s.walk = []
        mil = [r for r in roles if r.startswith(('linh', 'phao', 'thuy', 'raf'))]; civ = [r for r in roles if r not in mil] or mil
        busy = lambda hr: max(0.05, math.exp(-((hr - 11.5) / 3.2) ** 2) + 0.8 * math.exp(-((hr - 17.5) / 1.8) ** 2))
        # nhóm đứng (trò chuyện, chợ, gác)
        for k in range(70):
            hr = R.uniform(H0, H1);
            if R.random() > busy(hr): continue
            c = s.rand_free();
            if not c: continue
            n = R.choice((1, 2, 2, 3, 4)); dur = R.uniform(0.25, 1.4)
            role_pool = mil if (s.ep == 1943 and R.random() < 0.8) or (s.ep == 1782 and R.random() < 0.65) else civ
            grp = [(c[0] + R.uniform(-1.2, 1.2), c[1] + R.uniform(-1.2, 1.2), R.choice(role_pool), R.choice(('mat', 'trai', 'phai', 'lung'))) for _ in range(n)]
            grp = [g for g in grp if s.free(g[0], g[1])]
            s.stand.append({'t0': hr, 't1': hr + dur, 'people': grp})
        # gác cố định cả ngày đêm (chốt gác 1782 / lối hầm trú ẩn 1943)
        gx, gy = (-8.6, 16.0) if s.ep == 1782 else (-36.0, 13.0)
        if s.free(gx, gy): s.stand.append({'t0': H0, 't1': H1, 'people': [(gx, gy, 'linh', 'mat')], 'sentry': True})
        # 1782: đội hình tập trên Grand Parade (sáng) — 4 hàng × 8
        if s.ep == 1782:
            for (t0, t1, cx, cy) in ((9.0, 10.6, -46, 4), (16.4, 17.3, -40, -2)):
                grp = [(cx + i * 1.1, cy + j * 1.3 - 4, 'linh', 'trai') for i in range(8) for j in range(4) if s.free(cx + i * 1.1, cy + j * 1.3 - 4)]
                s.stand.append({'t0': t0, 't1': t1, 'people': grp, 'formation': True})
        # người đi: tuyến giữa hai điểm trống
        for k in range(1700):
            hr = R.uniform(H0, H1)
            if R.random() > busy(hr) * (0.25 if hr > 20.5 else 1): continue
            a, b = s.rand_free(), s.rand_free()
            if not a or not b or math.dist(a, b) < 12: continue
            s.walk.append({'t': hr, 'a': a, 'b': b, 'role': R.choice(mil if R.random() < 0.6 else civ)})

    def weights(s, hr):
        hs = [PASS_H[p] for p in ORDER]
        if hr <= hs[0]: return {'d1': 1.0}, 0.0
        for i in range(len(hs) - 1):
            if hs[i] <= hr <= hs[i + 1]:
                a = (hr - hs[i]) / (hs[i + 1] - hs[i]); a = a * a * (3 - 2 * a)
                blue = 0.0
                if ORDER[i + 1] == 'n': blue = a
                return {ORDER[i]: 1 - a, ORDER[i + 1]: a}, blue
        return {'n': 1.0}, 1.0

    def sprite(s, w, role, face, walk):
        c = s.cell.get((role, face, walk)) or s.cell.get((role, 'mat', walk))
        pxm = s.sm['pxm']; fx, fy = c['foot_px']; x0, x1 = int(fx - 0.75 * pxm), int(fx + 0.75 * pxm); y0, y1 = int(fy - 2.05 * pxm), int(fy + 0.9 * pxm)
        im = sum(s.sheet[p][y0:y1, x0:x1] * wt for p, wt in w.items())
        return im, (fx - x0, fy - y0)

    def stamp(s, canvas, alpha_acc, im, foot, x, y, op=1.0, extra_scale=1.0):
        p = s.proj(x, y, 0)
        if not p: return
        sc = s.fpx / p[2] / s.sm['pxm'] * extra_scale
        h, w = im.shape[:2]; nw, nh = max(1, int(w * sc)), max(1, int(h * sc))
        if nh < 3: return
        sm = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA)
        ox, oy = int(round(p[0] - foot[0] * sc)), int(round(p[1] - foot[1] * sc))
        X0, Y0 = max(0, ox), max(0, oy); X1, Y1 = min(s.W, ox + nw), min(s.H, oy + nh)
        if X1 <= X0 or Y1 <= Y0: return
        sub = sm[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox]
        vis = (s.depth[Y0:Y1, X0:X1] > p[3] - 0.6).astype(np.float32)
        a = sub[..., 3] * vis * op
        canvas[Y0:Y1, X0:X1] = canvas[Y0:Y1, X0:X1] * (1 - a[..., None]) + sub[..., :3] * a[..., None]

    def frame(s, hr, dt_h, frame_seed):
        w, blue = s.weights(hr)
        img = sum(s.bg[p] * wt for p, wt in w.items())
        R = random.Random(frame_seed)
        n_st = n_wk = 0
        # người đứng
        for g in s.stand:
            if g['t0'] <= hr <= g['t1']:
                fade = min(1.0, (hr - g['t0']) / 0.05, (g['t1'] - hr) / 0.05)
                for (x, y, role, face) in g['people']:
                    im, foot = s.sprite(w, role, face, False); s.stamp(img, None, im, foot, x, y, op=fade); n_st += 1
        # người đi: vệt phơi sáng — mọi tuyến có giờ trong [hr - dt/2, hr + dt/2] in dọc đường đi với độ mờ ~ 1/K
        for wk in s.walk:
            if abs(wk['t'] - hr) <= dt_h * 0.6:
                ax, ay = wk['a']; bx, by = wk['b']; K = 22
                face = 'trai' if (s.proj(bx, by, 0) or (0,))[0] < (s.proj(ax, ay, 0) or (0,))[0] else 'phai'
                im, foot = s.sprite(w, wk['role'], face, True); n_wk += 1
                s.streak(img, im, foot, (ax, ay), (bx, by))
        # khói
        light = sum(wt * (0.05 if p == 'n' else 1.0) for p, wt in w.items())
        warm = w.get('d4', 0) + 0.5 * w.get('d3', 0)
        smoke_col = np.array([0.55, 0.55, 0.56]) * (0.25 + 0.75 * light) * np.array([1.0, 1 - 0.15 * warm, 1 - 0.3 * warm])
        cook = 0.25 + math.exp(-((hr - 8.5) / 1.2) ** 2) + math.exp(-((hr - 18.5) / 1.5) ** 2)
        for i, (x, y, z) in enumerate(s.meta['chimneys']):
            rr = random.Random(i * 31 + s.ep)
            ship = z < 0
            if not ship and rr.random() > 0.35 * cook: continue
            p0 = s.proj(x, y, z)
            if not p0 or not (-50 < p0[0] < s.W + 50 and 0 < p0[1] < s.H): continue
            if s.depth[int(min(s.H - 1, max(0, p0[1]))), int(min(s.W - 1, max(0, p0[0])))] < p0[3] - 2: continue
            for j in range(10):
                age = j / 10 + R.random() * 0.08
                wx, wy, wz = x - 9 * age * (1 + 2 * ship), y + 2 * age, z + (4 + 6 * ship) * age + R.uniform(-0.4, 0.4)
                pp = s.proj(wx, wy, wz)
                if not pp: continue
                rad = max(1.5, s.fpx * (0.5 + 2.2 * age) * (1 + ship) / pp[2])
                col = smoke_col * (0.35 if ship else 1.0)
                s.puff(img, pp[0], pp[1], rad, col, (0.22 if not ship else 0.35) * (1 - age), pp[3])
        # cờ
        for (x, y, z) in s.meta['flags']:
            s.flag(img, x, y, z, light, warm, R)
        # hải âu (ban ngày)
        if light > 0.3:
            for b in range(R.randint(0, 5)):
                bx, by = R.uniform(0.05, 0.95) * s.W, R.uniform(0.05, 0.42) * s.H
                if not s.sky[int(by), int(bx)]: continue
                sz = R.uniform(2.5, 6.0) * s.W / 1920; c = (0.92, 0.92, 0.9) if R.random() < 0.5 else (0.25, 0.25, 0.27)
                pts = np.array([[bx - sz, by - sz * 0.35], [bx, by], [bx + sz, by - sz * 0.35]], np.int32)
                cv2.polylines(img, [pts], False, c, max(1, int(s.W / 1920 + 0.5)), cv2.LINE_AA)
        # giờ xanh → đêm
        if blue > 0:
            b = blue
            tint = np.array([0.75, 0.85, 1.15])
            img = img * (1 - 0.0 * b)   # (lượt đêm đã tối; chỉ ngả lam phần còn sáng)
            img = img * (1 - 0.35 * b * (1 - b) * 4) * (1 + (tint - 1) * b * 0.6)
        if w.get('n', 0) > 0.05:   # quầng đèn dầu (1782) / đèn che chụp phong toả (1943) tại vị trí đèn thật của cảnh
            for (x, y, z) in s.meta['lamps']:
                pp = s.proj(x, y, z)
                if not pp or not (0 <= pp[0] < s.W and 0 <= pp[1] < s.H): continue
                if s.depth[int(pp[1]), int(pp[0])] < pp[3] - 1.0: continue
                r = s.fpx * (1.6 if s.ep == 1782 else 0.5) / pp[2]
                s.puff(img, pp[0], pp[1], r * 3, np.array([1.0, 0.55, 0.22]) * (0.5 if s.ep == 1782 else 0.15), 0.5 * w['n'], pp[3])
                s.puff(img, pp[0], pp[1], max(1.5, r * 0.5), np.array([1.0, 0.85, 0.6]), 0.9 * w['n'], pp[3])
        if s.ep == 1943 and w.get('n', 0) > 0.2: s.searchlights(img, hr, w['n'])
        if w.get('n', 0) > 0.3: s.stars(img, w['n'])
        return img, {'weights': {k: round(v, 3) for k, v in w.items()}, 'blue': round(blue, 3), 'nguoi_dung': n_st, 'vet_di': n_wk}

    def streak(s, img, im, foot, a, b, cover=0.38):
        """vệt phơi sáng dài liền: thu sprite một lần theo khoảng cách giữa tuyến, in một dấu mỗi ~2 px dọc tuyến chiếu,
        độ mờ mỗi dấu chọn sao cho tổng độ phủ = cover."""
        pa, pb = s.proj(a[0], a[1], 0), s.proj(b[0], b[1], 0)
        if not pa or not pb: return
        mid = s.proj((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0); sc = s.fpx / mid[2] / s.sm['pxm']
        h, w = im.shape[:2]; nw, nh = max(1, int(w * sc)), max(1, int(h * sc))
        if nh < 4: return
        sm = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA); fx, fy = foot[0] * sc, foot[1] * sc
        L = math.hypot(pb[0] - pa[0], pb[1] - pa[1]); N = int(max(4, min(400, L / 2)))
        op = 1 - (1 - cover) ** (1.0 / max(1, N * min(1.0, nw / max(1.0, L / N)) / 1.0)) if L > 0 else cover
        op = min(op, cover)
        for j in range(N):
            u = (j + 0.5) / N; x, y = pa[0] + (pb[0] - pa[0]) * u, pa[1] + (pb[1] - pa[1]) * u; dist = pa[3] + (pb[3] - pa[3]) * u
            ox, oy = int(round(x - fx)), int(round(y - fy))
            X0, Y0 = max(0, ox), max(0, oy); X1, Y1 = min(s.W, ox + nw), min(s.H, oy + nh)
            if X1 <= X0 or Y1 <= Y0: continue
            sub = sm[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox]
            al = sub[..., 3] * (s.depth[Y0:Y1, X0:X1] > dist - 0.6) * op
            img[Y0:Y1, X0:X1] = img[Y0:Y1, X0:X1] * (1 - al[..., None]) + sub[..., :3] * al[..., None]

    def puff(s, img, x, y, r, col, a, dist):
        r = int(max(2, r)); X0, Y0 = int(x - 2 * r), int(y - 2 * r); X1, Y1 = int(x + 2 * r), int(y + 2 * r)
        X0c, Y0c, X1c, Y1c = max(0, X0), max(0, Y0), min(s.W, X1), min(s.H, Y1)
        if X1c <= X0c or Y1c <= Y0c: return
        yy, xx = np.mgrid[Y0c:Y1c, X0c:X1c]; g = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * r * r)) * a
        g *= (s.depth[Y0c:Y1c, X0c:X1c] > dist - 3)
        img[Y0c:Y1c, X0c:X1c] = img[Y0c:Y1c, X0c:X1c] * (1 - g[..., None]) + col * g[..., None]

    def flag_img(s, phase):
        Wf, Hf = 300, 150; im = Image.new('RGB', (Wf, Hf), (16, 36, 104)); d = ImageDraw.Draw(im)
        wt = 30
        d.line([(0, 0), (Wf, Hf)], fill=(245, 245, 245), width=wt); d.line([(0, Hf), (Wf, 0)], fill=(245, 245, 245), width=wt)
        if s.ep == 1943:   # bản 1801: chéo đỏ St Patrick so le
            d.line([(0, -4), (Wf / 2, Hf / 2 - 4)], fill=(200, 16, 46), width=10); d.line([(Wf / 2, Hf / 2 + 4), (Wf, Hf + 4)], fill=(200, 16, 46), width=10)
            d.line([(0, Hf + 4), (Wf / 2, Hf / 2 + 4)], fill=(200, 16, 46), width=10); d.line([(Wf / 2, Hf / 2 - 4), (Wf, -4)], fill=(200, 16, 46), width=10)
        d.rectangle([Wf / 2 - 25, 0, Wf / 2 + 25, Hf], fill=(245, 245, 245)); d.rectangle([0, Hf / 2 - 25, Wf, Hf / 2 + 25], fill=(245, 245, 245))
        d.rectangle([Wf / 2 - 15, 0, Wf / 2 + 15, Hf], fill=(200, 16, 46)); d.rectangle([0, Hf / 2 - 15, Wf, Hf / 2 + 15], fill=(200, 16, 46))
        a = srgb2lin(np.asarray(im).astype(np.float32) / 255)
        # gợn sóng vải: dịch dọc + sáng tối theo pha
        xs = np.arange(Wf); off = (np.sin(xs / Wf * 2 * math.pi * 1.6 + phase) * 6 * xs / Wf).astype(int)
        b = np.zeros_like(a); sh = np.ones((Hf, Wf), np.float32)
        for xx in range(Wf): b[:, xx] = np.roll(a[:, xx], off[xx], axis=0)
        sh *= (0.8 + 0.2 * np.cos(xs / Wf * 2 * math.pi * 1.6 + phase))[None, :]
        return b * sh[..., None]

    def flag(s, img, x, y, z, light, warm, R):
        L, Hm = (2.6, 1.3)
        dx, dy = -0.9, 0.45; n = math.hypot(dx, dy); dx, dy = dx / n, dy / n      # gió Levante (đông) → cờ bay về tây
        cs = [s.proj(x, y, z), s.proj(x + dx * L, y + dy * L, z - 0.15), s.proj(x + dx * L, y + dy * L, z - Hm - 0.15), s.proj(x, y, z - Hm)]
        if any(c is None for c in cs): return
        src = np.float32([[0, 0], [299, 0], [299, 149], [0, 149]]); dst = np.float32([[c[0], c[1]] for c in cs])
        if (dst[:, 0].max() < 0) or dst[:, 0].min() > s.W: return
        f = s.flag_img(R.uniform(0, 6.28)) * (0.15 + 0.85 * light) * np.array([1.0, 1 - 0.12 * warm, 1 - 0.25 * warm])
        M = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(f.astype(np.float32), M, (s.W, s.H), flags=cv2.INTER_LINEAR)
        mask = cv2.warpPerspective(np.ones((150, 300), np.float32), M, (s.W, s.H), flags=cv2.INTER_LINEAR)
        mask *= (s.depth > cs[0][3] - 1)
        img[:] = img * (1 - mask[..., None]) + warped * mask[..., None]

    def searchlights(s, img, hr, wn):
        H, W = s.H, s.W; yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        for k, (bx, ph) in enumerate(((0.15, 0.0), (0.72, 2.1), (1.05, 4.0))):
            ang = math.radians(-70 + 35 * math.sin(hr * 9 + ph))
            ox, oy = bx * W, H * 0.62
            dxv, dyv = math.cos(ang), math.sin(ang)
            t = (xx - ox) * dxv + (yy - oy) * dyv; perp = np.abs(-(xx - ox) * dyv + (yy - oy) * dxv)
            wbeam = 4 + t * 0.03
            g = np.exp(-(perp / np.maximum(wbeam, 1)) ** 2) * (t > 0) * np.exp(-np.maximum(t, 0) / (H * 0.9)) * 0.07 * wn
            g *= s.sky
            img += g[..., None] * np.array([0.75, 0.82, 1.0])

    def stars(s, img, wn):
        rr = np.random.RandomState(7); n = int(220 * s.W / 1920)
        xs = rr.randint(0, s.W, n); ys = rr.randint(0, int(s.H * 0.45), n); br = rr.uniform(0.02, 0.12, n) * wn
        for x, y, b in zip(xs, ys, br):
            if s.sky[y, x]: img[y, x] += b

def overlay(rgb8, ep_label_year, label_ep, notext, scale):
    if notext: return rgb8
    im = Image.fromarray(rgb8); d = ImageDraw.Draw(im); W, H = im.size
    fy = ImageFont.truetype(FONT_B, int(78 * scale)); fl = ImageFont.truetype(FONT_R, max(12, int(38 * scale)))   # dòng nguồn ≥ 38 px @1080p (Kinh thánh §4, E2)
    txt = str(ep_label_year); bb = d.textbbox((0, 0), txt, font=fy); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x, y = W - tw - int(60 * scale), H - th - int(64 * scale)
    d.rounded_rectangle([x - 22 * scale, y - 16 * scale, x + tw + 22 * scale, y + th + 26 * scale], radius=int(10 * scale), fill=(14, 14, 16))
    d.text((x - bb[0], y - bb[1]), txt, font=fy, fill=(245, 236, 214))
    if label_ep:
        ly = H - int(56 * scale) - 2 * int(48 * scale)
        for i, line in enumerate(LABEL[label_ep]):
            bb = d.textbbox((0, 0), line, font=fl)
            d.rectangle([int(52 * scale), ly + i * int(48 * scale) - 6 * scale, int(52 * scale) + bb[2] + 16 * scale, ly + i * int(48 * scale) + bb[3] + 6 * scale], fill=(14, 14, 16))
            d.text((int(60 * scale), ly + i * int(48 * scale)), line, font=fl, fill=(230, 226, 214))
    return np.asarray(im)

GRADE = {'sat': 1.85, 'contrast': 0.42, 'warm': 0.04}   # chỉnh màu chung cho MỌI khung, cả hai nhánh (không thêm phần tử)
def grade(img):
    x = np.clip(img, 0, None)
    out = lin2srgb(x / (1 + 0.15 * x))            # vai mềm nhẹ
    Y = (out * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
    out = Y + (out - Y) * GRADE['sat']                                   # bão hoà theo độ sáng (giữ độ sáng)
    sc_ = out * out * (3 - 2 * out); out = out + (np.clip(sc_, 0, 1) - out) * GRADE['contrast']   # đường cong S
    out = out * np.array([1 + GRADE['warm'], 1.0, 1 - GRADE['warm']])    # ấm nhẹ (nắng Địa Trung Hải)
    return np.clip(out, 0, 1)

def timeline(t):
    """→ (thời kỳ, giờ ảo, trộn chuyển, năm hiển thị, nhãn)"""
    if t < SEG: return 1782, H0 + (H1 - H0) * t / SEG, 0.0, 1782, 1782
    if t < SEG + TR:
        a = (t - SEG) / TR; a2 = a * a * (3 - 2 * a); yr = int(round(1782 + (1943 - 1782) * a2))
        return 'tr', None, a2, yr, None
    tt = t - SEG - TR; return 1943, H0 + (H1 - H0) * tt / SEG, 0.0, 1943, 1943

def run(W, H, frames, write_video, stills_at, notext):
    class Lazy(dict):
        def __missing__(self, ep): self[ep] = Epoch(ep, W, H); return self[ep]
    E = Lazy(); scale = W / 1920
    dt_h = (H1 - H0) / SEG / FPS
    log = open(os.path.join(A.out, f'log-{A.tex}-{W}x{H}.jsonl'), 'w')
    ff = None
    if write_video:
        out = os.path.join(A.out, f'pt-{A.tex}-{W}x{H}.mp4')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for f in frames:
        t = f / FPS; ep, hr, mix, yr, lab = timeline(t)
        if ep == 'tr':
            a_img, ia = E[1782].frame(H1, dt_h, f); b_img, ib = E[1943].frame(H0, dt_h, f)
            img = a_img * (1 - mix) + b_img * mix; info = {'tr': round(mix, 3), 'a': ia, 'b': ib}; lab = 1782 if mix < 0.5 else 1943
        else:
            img, info = E[ep].frame(hr, dt_h, f * 7919 + ep)
        rgb = (grade(img) * 255 + 0.5).astype(np.uint8)
        rgb = overlay(rgb, yr, lab, notext, scale)
        rec = {'f': f, 't': round(t, 3), 'epoch': ep, 'gio_ao': None if hr is None else round(hr, 3), 'nam': yr, 'tex': A.tex, 'ai_texture': A.tex == 'B', **info}
        log.write(json.dumps(rec, ensure_ascii=False) + '\n')
        if ff: ff.stdin.write(rgb.tobytes())
        if f in stills_at:
            Image.fromarray(rgb).save(os.path.join(A.out, f'{stills_at[f]}-{A.tex}{"-notext" if notext else ""}.jpg'), quality=92)
    if ff: ff.stdin.close(); ff.wait()
    log.close()

if __name__ == '__main__':
    N = int(TOTAL * FPS)
    frames = range(N)
    if A.frames: a, b = map(int, A.frames.split(':')); frames = range(a, b)
    # khung tĩnh khai TRƯỚC khi xem kết quả: trưa (giờ ảo 12,8 = lượt d2), chiều vàng (17,55), đêm (21,8) mỗi thời kỳ
    def fr_of(ep, hr): return int(round((((hr - H0) / (H1 - H0)) * SEG + (0 if ep == 1782 else SEG + TR)) * FPS))
    ST = {fr_of(1782, 12.8): '1782-trua', fr_of(1782, 17.55): '1782-chieu', fr_of(1782, 21.8): '1782-dem',
          fr_of(1943, 12.8): '1943-trua', fr_of(1943, 17.55): '1943-chieu', fr_of(1943, 21.8): '1943-dem', int((SEG + TR / 2) * FPS): 'chuyen'}
    if A.video:
        W, H = map(int, A.video.split('x')); run(W, H, frames, True, {}, A.notext)
    if A.stills:
        W, H = map(int, A.stills.split('x')); run(W, H, sorted(ST), False, ST, A.notext)
    json.dump({'stills': {str(k): v for k, v in ST.items()}, 'fps': FPS, 'seg': SEG, 'tr': TR}, open(os.path.join(A.out, 'stills.json'), 'w'), indent=1)
