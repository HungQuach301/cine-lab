#!/opt/cine/bin/python
"""Q33 lặp cảnh — luật khoá bản 1.10.1 (phiên K, 12/10/2026; chủ dự án xem Steel). Áp LL (từ tập 9) và kênh 2 (từ K2 tập 2).
Định nghĩa: checks/ll/RULES-LL.md (dòng Q33).

  q_scene.py <episode.yaml> [--tl timeline.json] [--video master.mp4] [--json ra.json]

Một LẦN XUẤT HIỆN = chuỗi shot liền nhau của phim chính hiện RÕ cùng (scene_id, camera_id):
  scene_id  = shot `scene_id` trong đặc tả, hoặc `p.scene_id`; không khai → bộ cảnh 3D `heroes.<khoá>.hero`
  camera_id = shot `camera_id` trong đặc tả, hoặc `p.camera_id`; không khai → khoá `heroes.<khoá>` (mỗi khoá là một bố trí máy quay)
  chỉ tính shot cảnh 3D hiện rõ (`plate`, hai nửa `diptych`); shot có `p.card` (thẻ trên nền cảnh mờ) thuộc bối cảnh "the" của Q26b, không tính ở đây.
Xác nhận bằng hình (pHash 64 bit: DCT 32×32 → 8×8, 3 khung 30/50/70 % mỗi lần xuất hiện trên master 1080p; khoảng cách = Hamming nhỏ nhất):
  số lần của một (scene_id, camera_id) = số lần KHAI + số lần xuất hiện khác của CÙNG bộ cảnh khai camera_id khác mà pHash ≤ THETA với
  một lần đã khai (lặp không khai). pHash KHÔNG hạ số lần khai: đo trên Steel, pHash toàn khung không tách được "cùng góc" khi máy
  dịch nhẹ, phụ đề và nhãn đổi (c_own 2:39.9 ↔ 15:06.7 mắt thấy cùng góc nhưng 24/63 bit) — xem RULES-LL.md, BAO-CAO mục 18.
  Không có master: chỉ số lần khai.
TRƯỢT khi một (scene_id, camera_id) xuất hiện > 2 lần. Đúng 2 lần: nêu tên (bằng ngưỡng).
THETA tự hiệu chuẩn trên Steel (K2G-01 bản phát hành, master 28e4d113…): θ lớn nhất để cặp KHÁC bộ cảnh bị coi là giống ≤ 1 % và cặp
  cùng bộ cảnh đã khai khác góc ≤ 2 % (calibrate(); dữ liệu: checks/ll/fixtures/k2g01/q33-steel.json). Kiểm bằng mắt trên Steel: θ = 16
  gộp nhầm v_rail↔v_coke, v_bf↔v_night (thung lũng tối); θ = 14 chỉ nối c_draw↔c_own (đúng là cùng góc bản đồ).
1.13 (khiếu nại T2 G2 §14.5; q33(…, k2=True), CHỈ BÁO tới khi duyệt): KÊNH 2 băm SAU KHI BỎ LỚP CHỮ CỐ ĐỊNH — chip nơi + "Facts as of" (dải trên) và dải chú thích +
  dòng nguồn / tấm chữ gọn (dải dưới) giống nhau ở mọi khung kênh 2, kéo pHash toàn khung lại gần nhau (T2 L5: thêm chip nơi + hai tấm chữ →
  pHash thêm 26 lần lặp). Băm = pHash 63 bit kênh L (Lab) trên VÙNG NỘI DUNG y 18–72 % (cùng hàm Q33-K2, `q_k2var.phash_video`),
  θ = q_k2var.THETA_L (16; hiệu chuẩn 1.12.2 trên master Steel + T1 cùng vùng: khác bộ ≤ θ 0,65 %, cùng bộ khác góc 1,8 % — đạt tiêu chí 1 %/2 %
  của calibrate()). LL giữ pHash xám toàn khung, θ 14.
"""
import json, os, subprocess, sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
MAX_APPEAR = 2
THETA = 14          # bit Hamming (của 63); hiệu chuẩn 1.10.1 trên Steel (calibrate): khác bộ cảnh ≤ θ 3/1051 = 0,29 %; cùng bộ cảnh khai khác góc 2/149 = 1,3 %
FPR_MAX = 0.01      # cặp KHÁC bộ cảnh
FPR_MAX_SAME = 0.02 # cặp CÙNG bộ cảnh đã khai khác camera_id (khai được coi là đúng trừ khi hình rất gần)
SAMPLES = (0.3, 0.5, 0.7)
GAP = 1 / 24 + 0.001


def _spec_shot(E, sid, i, short=False):
    for s in (E.get('shorts') if short else E.get('segments')) or []:
        if s.get('id') == sid:
            sh = s.get('shots') or []
            return sh[i] if i < len(sh) else {}
    return {}


def ids(sh, spec, heroes):
    """→ [(scene_id, camera_id, trọng số)] của các vùng cảnh 3D hiện RÕ trong shot"""
    p = sh.get('p') or {}
    if p.get('card'): return []
    def one(k, src):
        sc = spec.get('scene_id') or src.get('scene_id') or (heroes.get(k) or {}).get('hero') or k
        cam = spec.get('camera_id') or src.get('camera_id') or k
        return (str(sc), str(cam))
    if sh.get('tpl') == 'plate' and p.get('hero'): return [one(p['hero'], p) + (1.0,)]
    if sh.get('tpl') == 'diptych':
        hs = [x for x in (p.get('left'), p.get('right')) if isinstance(x, dict) and x.get('hero')]
        return [one(x['hero'], x) + (1.0 / len(hs),) for x in hs]
    return []


def appearances(E, TL):
    """→ [dict(scene, cam, t0, t1, shots=[…])] theo thời gian (phim chính); shot liền ngay sau cùng góc nối vào lần xuất hiện đang mở"""
    H = TL.get('heroes') or {}; out = []; open_ = {}; t_prev = None
    for s in TL['segments']:
        for i, sh in enumerate(s['shots']):
            a, b = s['t0'] + sh['t0'], s['t0'] + sh['t1']
            if b <= a: continue
            cur = {(sc, cam) for sc, cam, _ in ids(sh, _spec_shot(E, s['id'], i), H)}
            nxt = {}
            for key in cur:
                ap = open_.get(key)
                if ap is not None and t_prev is not None and a - t_prev <= GAP: ap['t1'] = round(b, 3); ap['shots'].append(f"{s['id']}/{i}")
                else: ap = dict(scene=key[0], cam=key[1], t0=round(a, 3), t1=round(b, 3), shots=[f"{s['id']}/{i}"]); out.append(ap)
                nxt[key] = ap
            open_, t_prev = nxt, b
    return out


def phash_frame(video, t):
    """pHash 64 bit của khung tại t (giây): xám 32×32, DCT-II 2D, 8×8 tần số thấp bỏ DC, so trung vị"""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', '-vf', 'scale=32:32:flags=area,format=gray',
                          '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.uint8).astype(np.float64).reshape(32, 32)
    n = np.arange(32); C = np.cos(np.pi * (2 * n[None, :] + 1) * n[:, None] / 64)
    d = (C @ x @ C.T)[:8, :8].flatten()[1:]
    bits = d > np.median(d)
    return int(''.join('1' if v else '0' for v in bits), 2)


def ham(a, b): return bin(a ^ b).count('1')


def hashes(video, aps, k2=False):
    from checks.ll import q_k2var
    for ap in aps:
        d = ap['t1'] - ap['t0']
        ap['ph'] = [q_k2var.phash_video(video, ap['t0'] + f * d)[0] if k2 else phash_frame(video, ap['t0'] + f * d) for f in SAMPLES]
    return aps


def dist(a, b): return min(ham(x, y) for x in a['ph'] for y in b['ph'])


def calibrate(aps):
    """θ lớn nhất sao cho (i) cặp lần xuất hiện KHÁC bộ cảnh có khoảng cách ≤ θ không quá FPR_MAX và (ii) cặp CÙNG bộ cảnh đã khai
    khác camera_id không quá FPR_MAX_SAME. → (θ, bảng đo). Khoảng cách pHash luôn chẵn (trung vị chia 63 hệ số thành hai nửa cố định)."""
    pos = [dist(a, b) for i, a in enumerate(aps) for b in aps[i + 1:] if (a['scene'], a['cam']) == (b['scene'], b['cam'])]
    neg = [dist(a, b) for i, a in enumerate(aps) for b in aps[i + 1:] if a['scene'] != b['scene']]
    sam = [dist(a, b) for i, a in enumerate(aps) for b in aps[i + 1:] if a['scene'] == b['scene'] and a['cam'] != b['cam']]
    fr = lambda L, t: sum(d <= t for d in L) / max(len(L), 1)
    th = max([t for t in range(0, 64, 2) if fr(neg, t) <= FPR_MAX and fr(sam, t) <= FPR_MAX_SAME] or [0])
    hist = lambda L: {str(k): sum(d == k for d in L) for k in range(0, 64) if any(d == k for d in L)}
    return th, dict(theta=th, fpr_khac_bo=round(fr(neg, th), 4), fpr_cung_bo_khac_goc=round(fr(sam, th), 4), khai_cung_goc_le_theta=round(fr(pos, th), 3),
                    n_khac_bo=len(neg), n_cung_bo_khac_goc=len(sam), n_khai_cung_goc=len(pos),
                    hist_khac_bo=hist(neg), hist_cung_bo_khac_goc=hist(sam), hist_khai_cung_goc=hist(pos))


def q33(E, TL, video=None, theta=None, aps=None, k2=False):
    """k2=True: băm 1.13 bỏ lớp chữ cố định (kênh 2) — CHỈ BÁO (k2check hàng "Q33 (1.13)") tới khi chủ dự án duyệt; mặc định luật 1.10.1"""
    from checks.ll import q_k2var
    theta = theta if theta is not None else (q_k2var.THETA_L if k2 else THETA)
    aps = aps if aps is not None else appearances(E, TL)
    if video and aps and 'ph' not in aps[0]: hashes(video, aps, k2)
    hp = bool(aps) and 'ph' in aps[0]
    G = {}
    for ap in aps: G.setdefault((ap['scene'], ap['cam']), []).append(ap)
    bad, near, rows = [], [], {}
    for (sc, cam), g in sorted(G.items()):
        extra = [o for o in aps if o['scene'] == sc and o['cam'] != cam and any(dist(o, x) <= theta for x in g)] if hp else []
        n = len(g) + len(extra)
        when = ', '.join(f"{int(a['t0'] // 60)}:{a['t0'] % 60:04.1f}" for a in g)
        more = ' + pHash: ' + ', '.join(f"{o['cam']} {int(o['t0'] // 60)}:{o['t0'] % 60:04.1f}" for o in extra) if extra else ''
        rows[f'{sc} · {cam}'] = dict(khai=len(g), phash_them=len(extra), tong=n, luc=when + more)
        if n > MAX_APPEAR: bad.append(f'{sc} · {cam}: {n} lần ({when}{more}) > {MAX_APPEAR}')
        elif n == MAX_APPEAR: near.append(f'{sc} · {cam}: đúng {MAX_APPEAR} lần')
    top = max(rows.items(), key=lambda z: z[1]['tong']) if rows else ('—', dict(tong=0))
    return dict(ok=not bad, loi=bad, sat_nguong=near, note='; '.join(bad[:6]), bang=rows,
                val=f"{len(G)} góc máy · {len(aps)} lần xuất hiện · nhiều nhất {top[0]} {top[1]['tong']} lần · {len(bad)} góc > {MAX_APPEAR}"
                    + (f' · pHash {"L vùng nội dung (bỏ lớp chữ cố định)" if k2 else "xám toàn khung"} θ={theta}, thêm {sum(r["phash_them"] for r in rows.values())} lần lặp không khai' if hp else ' · chưa đo pHash (không có master)'))


if __name__ == '__main__':
    from checks.ll import base
    a = sys.argv[1:]; E = base.load(a[0])
    tl = a[a.index('--tl') + 1] if '--tl' in a else os.path.join(E['out'], 'timeline.json')
    v = a[a.index('--video') + 1] if '--video' in a else None
    r = q33(E, json.load(open(tl)), video=v)
    for k, x in r['bang'].items(): print(f"  {x['tong']} (khai {x['khai']})  {k}  ({x['luc']})")
    print('Q33 ' + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ''.join('\n  ' + x for x in r['loi']))
    if '--json' in a: json.dump(r, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r['ok'] else 1)
