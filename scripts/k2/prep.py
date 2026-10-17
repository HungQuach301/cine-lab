#!/opt/cine/bin/python
"""KÊNH 2 · chuẩn bị một tập: dùng nguyên scripts/ll/ll.py (kiểm đặc tả, lời ElevenLabs có cache, mốc "@từ", nguồn tự sinh, timeline, .srt),
thay riêng bước kế hoạch cảnh 3D:
  - opt của cảnh 3D nhận mốc lời: "@từ" (± giây) → giây trong cảnh, tính theo shot ĐẦU TIÊN dùng cảnh đó (hoặc "NN@từ" = shot đầu tiên trong đoạn NN):
        giây_cảnh = (mốc_trong_đoạn − t0_shot) × speed + frame0 / 24   → sự kiện trong cảnh 3D (rót thép, vẽ tuyến, thanh chắn nâng…) khớp lời.
  - dấu (stamp) chỉ băm mã K2 (design/ll-hero/k2g01.js, k2page.js, kit.js, scripts/k2/hero.js) + tham số → sửa cảnh K2 không đổi dấu cảnh LL và ngược lại.
  - K2_DRAFT=1: nháp 960×540 (9:16 → 540×960), thư mục cảnh hậu tố -d.
  - CHỐNG LẶP (chủ dự án 12/10/2026): mỗi shot thấy cảnh 3D mang (scene_id, camera_id); cùng cặp > 2 lần trong một tập → DỪNG trước khi gọi ElevenLabs.
        scene_id = heroes.<k>.hero (vd k2g01/port, map/globe); camera_id = heroes.<k>.cam (tên preset trong scripts/k2/cams.yaml, hoặc opt.preset của module k2v)
        hoặc 'inline:<băm 6 ký tự>' khi máy quay khai trực tiếp, 'default' khi không khai. Shot thẻ (p.card) không tính (bối cảnh 'card' riêng, BAI-HOC-K2 K6).
        Biến thể rẻ: cùng cảnh, khác preset (thư viện ≥ 6 preset/bộ cảnh) → không dựng cảnh mới.
  - Trường đặc tả shot (cho luật K Q33/Q34): type (scene3d|map|chart3d|photo|document|footage|card — luật K Q34, checks 1.10.1), scene_id, camera_id, places, people —
        suy từ cảnh khi không khai; khai ở shot thì thắng. Ghi vào timeline.json (mỗi shot) và <out>/shots-meta.json.
  prep.py prep|check|cams <episode.yaml>      (cams: in bảng đếm scene_id+camera_id, không dựng gì)
"""
import hashlib, json, math, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'll'))
import ll  # noqa: E402

REPO, FPS = ll.REPO, ll.FPS
DRAFT = os.environ.get('K2_DRAFT') == '1'
CODE = ['design/ll-hero/k2g01.js', 'design/ll-hero/k2c106.js', 'design/ll-hero/k2page.js', 'design/ll-hero/kit.js', 'scripts/k2/hero.js',
        'design/k2v/page.js', 'design/k2v/common.js', 'design/k2v/map.js', 'design/k2v/chart3d.js', 'design/k2v/photo.js', 'design/k2v/relief.js', 'design/k2v/sticker-lab.js', 'scripts/k2/lib/sticker.js']
# V5b-2b (V5B2A §8.6): cảnh xương sống thời gian 'tl/<cảnh>' — mã riêng vào dấu cảnh CHỈ của cảnh tl (cảnh k2v/LL cũ không đổi dấu, không dựng lại)
TL_CODE = sorted(os.path.relpath(os.path.join(dp, f), REPO) for dp, _, fs in os.walk(os.path.join(REPO, 'design/k2v/tl')) for f in fs if f.endswith('.js')) + ['scripts/k2tl/render.js', 'scripts/k2tl/gl.js']
TL_PRESETS = {'lien-hoan', 'push-in', 'boundary-trace', 'follow-object', 'lateral-parallax', 'top-down-rise', 'vertigo'}   # campath.js (JJ1/KK1)
NOI = {'thanh_pho', 'eo_dat', 'vung', 'bien', 'song', 'trong_nha'}   # K-1.13 NC-H1: khai nơi theo cửa sổ (T3 trở đi BẮT BUỘC cho shot cảnh 3D địa lý)
CAMS = os.path.join(REPO, 'scripts/k2/cams.yaml')
MAX_SAME = 2   # cùng góc máy (scene_id + camera_id) tối đa 2 lần/tập


def code_bytes(tl=False):
    return b''.join(open(os.path.join(REPO, f), 'rb').read() for f in CODE + (TL_CODE if tl else []))


def is_tl(hero):
    return str(hero or '').startswith('tl/')


def cam_lib():
    import yaml
    return yaml.safe_load(open(CAMS)) if os.path.exists(CAMS) else {}


def lift_props(E):
    """V2b (D2b, chủ dự án 14/10 18:08): sticker của shot dựng trên cảnh relief/* chuyển từ lớp 2D (p.stickers) vào cảnh 3D (heroes.<k>.opt.props):
    vật thư viện ('stk:<tên>') dựng bằng mô hình 3D trên địa hình (ánh sáng chung, bóng thật, viền shader); nhân vật ('role:<vai>' | {role, hat, hand} | 'stk:role-<vai>')
    là billboard phẳng trong cảnh. Tập vẫn khai như cũ. Mốc giây trong đoạn → giây trong cảnh (trừ at của shot); "@từ" để nguyên (prep đổi theo cảnh)."""
    HZ = E.get('heroes') or {}
    for sg in E.get('segments', []):
        for sh in sg.get('shots', []):
            p = sh.get('p') or {}; h = HZ.get(p.get('hero')) if sh.get('tpl', 'plate') == 'plate' else None
            if not h or not str(h.get('hero', '')).startswith('relief/') or not p.get('stickers'): continue
            off = sh.get('at', 0) if isinstance(sh.get('at', 0), (int, float)) else 0; o = h.setdefault('opt', {}); props = o.setdefault('props', [])
            f0, sp = float(p.get('frame0', p.get('off', 0)) or 0) / 24, float(p.get('speed', 1))   # T2 G1b: shot bắt đầu giữa cảnh → giây cảnh = (giây đoạn − at)·speed + frame0/24
            sec = lambda v: (v - off) * sp + f0 if isinstance(v, (int, float)) else v
            for i, S in enumerate(p.pop('stickers')):
                img = S.get('img'); q = {k: S[k] for k in ('a', 'px', 'walk', 'hz', 'face', 'yaw', 'pop', 'dx', 'dz') if k in S}; q['id'] = S.get('id') or f'{sg.get("id")}-{len(props)}'
                if 'at' in S: q['t'] = sec(S['at'])
                if 'out' in S: q['out'] = sec(S['out'])
                if isinstance(img, dict): q['char'] = img
                elif str(img).startswith('role:'): q['char'] = {'role': str(img)[5:]}
                elif str(img).startswith('stk:role-'): q['char'] = {'role': str(img)[9:]}
                else: q['obj'] = str(img).replace('stk:', '')
                props.append(q)


def resolve_cams(E):
    """heroes.<k>.cam: '<preset>' → opt.cam từ thư viện (scene_id phải có preset đó). Gắn _camera_id cho mỗi khoá cảnh."""
    lift_props(E)
    L = cam_lib()
    for k, h in (E.get('heroes') or {}).items():
        o = h.setdefault('opt', {}); c = h.get('cam')
        if isinstance(o.get('cam'), str): c = o.pop('cam')
        if is_tl(h['hero']):   # V5b-2b: máy của cảnh tl là cú ngữ pháp (campath.js) khai trong cảnh; camera_id = preset (lien-hoan…) hoặc 'cau' (ML1) của shot
            pr = c or o.get('preset') or o.get('cau') or 'default'
            if pr != 'default' and pr not in TL_PRESETS and not o.get('cau'): raise SystemExit(f'heroes.{k}: preset máy "{pr}" không có trong ngữ pháp tl ({", ".join(sorted(TL_PRESETS))})')
            h['_camera_id'] = pr; h['_cam_geo'] = None; continue
        if c:
            P = (L.get(h['hero']) or {}).get(c)
            if not P: raise SystemExit(f'heroes.{k}: không có preset máy quay "{c}" cho cảnh {h["hero"]} trong scripts/k2/cams.yaml')
            if P.get('loai'): raise SystemExit(f'heroes.{k}: preset "{c}" của {h["hero"]} đã bị loại khi rà tờ khung')
            if P.get('module'): o['preset'] = c
            else: o['cam'] = P['cam']
            h['_camera_id'] = c
        elif o.get('preset'): h['_camera_id'] = o['preset']
        elif o.get('cam'): h['_camera_id'] = 'inline:' + hashlib.sha1(json.dumps(o['cam'], sort_keys=True).encode()).hexdigest()[:6]
        else: h['_camera_id'] = 'default'
        h['_cam_geo'] = cam_geo(o.get('cam') or ((L.get(h['hero']) or {}).get('default') or {}).get('cam'))


def cam_geo(cam):
    """(phương vị°, độ cao°, khoảng cách, tiêu cự mm, điểm nhìn) trung bình của máy quay dạng [{p, l, mm}]; None nếu không phải dạng đó (preset module)."""
    if not isinstance(cam, list) or not cam or not all(isinstance(k, dict) and 'p' in k and 'l' in k for k in cam): return None
    q = [(a + b) / 2 for a, b in zip(cam[0]['p'], cam[-1]['p'])]; l = [(a + b) / 2 for a, b in zip(cam[0]['l'], cam[-1]['l'])]
    d = [q[i] - l[i] for i in range(3)]; r = math.hypot(*d) or 1e-6
    return (math.degrees(math.atan2(d[0], d[2])), math.degrees(math.asin(max(-1, min(1, d[1] / r)))), r, (cam[0].get('mm', 32) + cam[-1].get('mm', 32)) / 2, l)


def cam_near(a, b):
    """Hai góc máy cùng cảnh coi là MỘT góc khi: lệch phương vị < 25°, độ cao < 10°, khoảng cách < 1,4×, tiêu cự < 1,3×, điểm nhìn lệch < 15 % khoảng cách.
    Hiệu chuẩn trên shot mẫu D (12/10/2026): mid-push ↔ orbit-r12-low lệch 21° → Q33 pHash (θ = 14) của K cũng gộp; orbit-l45 lệch 36° → K tách."""
    if not a or not b: return False
    return (abs((a[0] - b[0] + 180) % 360 - 180) < 25 and abs(a[1] - b[1]) < 10 and max(a[2], b[2]) / min(a[2], b[2]) < 1.4
            and max(a[3], b[3]) / min(a[3], b[3]) < 1.3 and math.dist(a[4], b[4]) / max(a[2], b[2]) < 0.15)


def shot_type(hero):
    """loại shot theo luật K Q34 (checks 1.10.1): scene3d | map | chart3d | photo | document | footage | card"""
    if not hero: return 'card'
    m, n = hero.split('/')[0], hero.split('/')[-1]
    # relief/map (V2): bản đồ nổi = map
    # tl (V5b-2b, V5B2A §8.6): cảnh 3D xương sống thời gian = scene3d trong danh sách Q34 (khai thêm tl: true ở shots-meta; K §7.4 đề xuất loại 'timelapse')
    return {'map': 'map', 'relief': 'map', 'chart3d': 'chart3d', 'footage': 'footage'}.get(m) or ({'print': 'photo', 'doc': 'document', 'headline': 'document'}.get(n) if m == 'photo' else 'scene3d')


def shot_meta(E, sh):
    p = sh.get('p', {}); HZ = E.get('heroes') or {}; k = p.get('hero') if sh.get('tpl') == 'plate' else None; h = HZ.get(k) if k else None
    card = bool(p.get('card'))
    M = dict(type='card' if card else shot_type(h['hero'] if h else None), scene_id=h['hero'] if h else None, camera_id=h.get('_camera_id') if h else None,
             places=[x['a'] if isinstance(x, dict) else x for x in p.get('places', [])], people=[])
    if h and is_tl(h['hero']): M.update(tl=True, cau=(h.get('opt') or {}).get('cau') or h.get('_camera_id'))
    if p.get('noi') or sh.get('noi'): M['noi'] = sh.get('noi') or p.get('noi')
    for f in ('type', 'scene_id', 'camera_id', 'places', 'people', 'noi'):
        if f in sh: M[f] = sh[f]
    return M


def repeat_check(E):
    resolve_cams(E); cnt, where, geo = {}, {}, {}
    HZ = E.get('heroes') or {}
    for sg in E['segments']:
        prev = None
        for i, sh in enumerate(sg.get('shots', [])):
            M = shot_meta(E, sh)
            if M['type'] == 'card' or not M['scene_id']: prev = None; continue
            key = (M['scene_id'], M['camera_id'])
            if key == prev: where[key].append(f"{sg['id']}/{i}"); continue   # shot liền nhau cùng góc = một lần (như Q33)
            cnt[key] = cnt.get(key, 0) + 1; where.setdefault(key, []).append(f"{sg['id']}/{i}"); prev = key
            k = (sh.get('p') or {}).get('hero'); geo.setdefault(key, (HZ.get(k) or {}).get('_cam_geo'))
    # cộng thêm lần xuất hiện của góc KHAI KHÁC nhưng hình học gần (không bao giờ trừ số khai)
    eff = {key: n + sum(m for k2, m in cnt.items() if k2 != key and k2[0] == key[0] and cam_near(geo.get(key), geo.get(k2))) for key, n in cnt.items()}
    for key in cnt:
        near = [k2[1] for k2 in cnt if k2 != key and k2[0] == key[0] and cam_near(geo.get(key), geo.get(k2))]
        if near: where[key] = where[key] + [f"(gần: {', '.join(near)})"]
    bad = {k: v for k, v in eff.items() if v > MAX_SAME}
    return eff, where, bad


def seg_words(sg):
    if not sg.get('vo_file'): return []
    return ll.words(json.load(open(os.path.join(REPO, sg['vo_file'][:-4] + '.align.json'))))


def heroes_plan(E, TL):
    # chặn shot sai thứ tự (G2 K2G-01: "@by"/"@question" khớp nhầm lần xuất hiện đầu → thẻ số neo không hiện)
    # trường đặc tả shot (Q33/Q34): TL giữ thứ tự shot của E (Shorts có thêm endcard ở cuối)
    meta = []
    for kind, ek in (('segments', 'segments'), ('shorts', 'shorts')):
        for sg, esg in zip(TL[kind], E.get(ek, [])):
            for sh, esh in zip(sg['shots'], esg.get('shots', [])):
                sh.update(shot_meta(E, esh)); meta.append(dict(seg=sg['id'], kind=kind, t0=round(sg.get('t0', 0) + sh['t0'], 3), t1=round(sg.get('t0', 0) + sh['t1'], 3),
                                                               **{f: sh[f] for f in ('type', 'scene_id', 'camera_id', 'places', 'people', 'tl', 'cau', 'noi') if f in sh}))
                if sh.get('tl'): sh['p']['tl'] = True   # lớp chữ tl (k2.js tlLayer)
                if sh.get('noi'): sh['p']['noi'] = sh['noi']
    json.dump(meta, open(os.path.join(E['out'], 'shots-meta.json'), 'w'), indent=1, ensure_ascii=False)
    for w in vv2_warn(E, meta): print('CẢNH BÁO VV2:', w, file=sys.stderr)
    bad = [f"{sg['id']}/{i}" for kind in ('segments', 'shorts') for sg in TL[kind] for i, sh in enumerate(sg['shots']) if sh['t1'] <= sh['t0'] + 0.3]
    if bad: raise SystemExit('Shot sai thứ tự hoặc < 0,3 s (mốc "@từ" khớp nhầm lần xuất hiện? dùng #n): ' + ', '.join(bad))
    HZ = E.get('heroes') or {}
    if not HZ: return
    code, code_tl = code_bytes(), code_bytes(True)
    need, first = {}, {}
    for kind in ('segments', 'shorts'):
        for sg in TL[kind]:
            for sh in sg['shots']:
                p = sh['p']
                if sh['tpl'] == 'plate' and p.get('hero'):
                    k = p['hero']; d = (sh['t1'] - sh['t0'] + 1.8) * p.get('speed', 1) + p.get('off', 0) / FPS
                    need[k] = max(need.get(k, 0), d); first.setdefault(k, []).append((sg, sh))

    def res(x, k, ctx):
        if isinstance(x, str) and re.match(r'^(\d\d)?@', x):
            sid, w = (x[:2], x[2:]) if x[0] != '@' else (None, x)
            uses = [(sg, sh) for sg, sh in first[k] if sid is None or sg['id'] == sid]
            if not uses: raise SystemExit(f'cảnh {k}: không có shot nào trong đoạn {sid} dùng cảnh này ({x})')
            sg, sh = uses[0]; p = sh['p']
            t = ll.anchor(w, seg_words(sg), sg['vo_offset'], ctx)
            return round((t - sh['t0']) * p.get('speed', 1) + p.get('off', 0) / FPS, 3)
        if isinstance(x, list): return [res(v, k, ctx) for v in x]
        if isinstance(x, dict): return {kk: res(v, k, ctx) for kk, v in x.items()}
        return x
    plan = {}
    for k, d in need.items():
        h = {kk: v for kk, v in HZ[k].items() if not kk.startswith('_') and kk != 'cam'}; h['opt'] = res(h.get('opt', {}), k, f'heroes.{k}.opt')
        dur = round(max(2.0, d) + 0.5, 1); size = h.get('size', [1920, 1080])
        if DRAFT: size = [size[0] // 2, size[1] // 2]
        stamp = hashlib.sha1((code_tl if is_tl(h['hero']) else code) + json.dumps([h, dur, size], sort_keys=True).encode()).hexdigest()[:12]
        plan[k] = dict(hero=h['hero'], variant=h.get('variant', 'a'), opt=h['opt'], dur=dur, size=size, dir=f"{ll.HERO_ROOT}/{E['id']}-{k}{'-d' if DRAFT else ''}", stamp=stamp)
    for kind in ('segments', 'shorts'):
        for sg in TL[kind]:
            for sh in sg['shots']:
                p = sh['p']
                if sh['tpl'] == 'plate' and p.get('hero'): p['dir'] = plan[p['hero']]['dir']; p['stamp'] = plan[p['hero']]['stamp']
    TL['heroes'] = plan; TL['draft'] = DRAFT
    json.dump(plan, open(os.path.join(E['out'], 'heroes.json'), 'w'), indent=1, ensure_ascii=False)


ll.heroes_plan = heroes_plan


def vv2_warn(E, meta):
    """Luật hình VV2 (chủ dự án 17/10) trong máy dựng — CẢNH BÁO khi prep (không chặn; bộ kiểm K NC-H1/H2 mới là luật):
    (1) shot khai/ suy thành phố mà không có lớp nhà; (2) địa cầu (AGL > 50 km) xuất hiện > 1 lần hoặc một lần > 3 s; (3) shot cảnh 3D địa lý từ T3 phải khai `noi`."""
    HZ, out, globe = E.get('heroes') or {}, [], []
    for m in meta:
        if m.get('type') not in ('scene3d', 'map') or not m.get('scene_id'): continue
        sid = m['scene_id']
        h = next((v for v in HZ.values() if v.get('hero') == sid), {}); o = h.get('opt') or {}
        geo = is_tl(sid) or sid.split('/')[0] in ('relief', 'map')
        if geo and not m.get('noi'): out.append(f"{m['seg']} @{m['t0']}: shot cảnh địa lý {sid} chưa khai noi (thanh_pho | eo_dat | vung | bien | song)")
        if m.get('noi') and m['noi'] not in NOI: out.append(f"{m['seg']} @{m['t0']}: noi '{m['noi']}' không hợp lệ ({', '.join(sorted(NOI))})")
        if m.get('noi') == 'thanh_pho':
            nha = (is_tl(sid) and (o.get('tech') or {}).get('city', True) is not False) or bool(o.get('aerial') or o.get('buildings') or o.get('layers'))
            if not nha: out.append(f"{m['seg']} @{m['t0']}: shot khai thành phố ({sid}) nhưng cảnh không có lớp nhà (NC-H1/VV2)")
        if sid.startswith('map/globe') or (sid.startswith('relief/') and max([0] + [float(c.get('km', c.get('alt', 0)) or 0) for c in (o.get('cam') if isinstance(o.get('cam'), list) else []) if isinstance(c, dict)]) > 50):
            globe.append((m['seg'], m['t0'], m['t1']))
    if len(globe) > 1: out.append(f"địa cầu / tầm cao > 50 km xuất hiện {len(globe)} lần (> 1): " + ', '.join(f'{a}@{b}' for a, b, _ in globe))
    out += [f"địa cầu {a} @{b}: {c - b:.1f} s > 3 s" for a, b, c in globe if c - b > 3]
    return out
_load = ll.load


def load_checked(path):
    """ll.load + chặn lặp góc máy (trước TTS) + gắn preset máy quay."""
    E = _load(path); cnt, where, bad = repeat_check(E)
    if bad: raise SystemExit('LẶP GÓC MÁY (> %d lần/tập, chủ dự án 12/10/2026): ' % MAX_SAME + '; '.join(f'{a} @ {b}: {n} lần ({", ".join(where[(a, b)])})' for (a, b), n in sorted(bad.items())))
    return E


ll.load = load_checked

_check_ll = ll.check
def check_k2(E):
    """K2C-T2-01 (G2): kênh 2 có thêm loại số 'estimate' (nhãn ESTIMATE trong lib/k2.js, ước của một bên thứ ba, không phải dự báo) — kiểm như số thực đo."""
    import copy
    E2 = copy.deepcopy(E)
    for n in (E2.get('numbers') or {}).values():
        if n.get('kind') == 'estimate': n['kind'] = 'actual'
    return _check_ll(E2)


ll.check = check_k2

_tts_ll = ll.tts
def tts_k2(E, key, text, speed=1.0):
    """K2C-T2-01 (G2): proxy cắt yêu cầu ElevenLabs sau ~30 s → đoạn > 1 900 ký tự thu thành 2–3 phần tách ở ranh giới câu,
    mỗi phần gửi kèm previous_text/next_text (giữ ngữ điệu liền), ghép mp3 (ffmpeg concat, không mã hoá lại) và cộng bù mốc căn chữ
    theo thời lượng thật của phần trước (ffprobe). Chữ ký cache vẫn là toàn văn đoạn → đoạn ngắn và tập cũ không đổi."""
    if len(text) <= 1900: return _tts_ll(E, key, text, speed)
    import base64, subprocess, tempfile, urllib.request
    d = ll.P(E['vo_dir']); os.makedirs(d, exist_ok=True)
    mp3, al, tx = (os.path.join(d, f'{key}.{x}') for x in ('mp3', 'align.json', 'txt'))
    v = E['voice']; sig = hashlib.sha1(json.dumps([text, v] + ([speed] if speed != 1.0 else []), sort_keys=True).encode()).hexdigest()[:12]
    if os.path.exists(mp3) and os.path.exists(tx) and open(tx).read().split('\n')[0] == sig: return mp3, json.load(open(al)), 0
    S = re.split(r'(?<=[.?!"])\s+(?=[A-Z"])', text); n = -(-len(text) // 1900); parts, cur = [], ''
    for x in S:
        if cur and len(cur) + len(x) + 1 > len(text) / n + 120: parts.append(cur); cur = x
        else: cur = (cur + ' ' + x).strip()
    parts.append(cur); assert ' '.join(parts) == text, 'tách câu làm đổi chữ'
    A = dict(characters=[], character_start_times_seconds=[], character_end_times_seconds=[]); off = 0.0; files = []; sent = 0
    with tempfile.TemporaryDirectory() as td:
        for i, ptxt in enumerate(parts):
            body = dict(text=ptxt, model_id=v.get('model', 'eleven_multilingual_v2'), voice_settings=dict(stability=v.get('stability', 0.5), similarity_boost=v.get('similarity', 0.75), speed=float(speed)))
            if i: body['previous_text'] = ' '.join(parts[:i])[-900:]
            if i + 1 < len(parts): body['next_text'] = ' '.join(parts[i + 1:])[:900]
            r = ll.el(f"/v1/text-to-speech/{v['id']}/with-timestamps?output_format=mp3_44100_128", body); sent += len(ptxt)
            f = os.path.join(td, f'p{i}.mp3'); open(f, 'wb').write(base64.b64decode(r['audio_base64'])); files.append(f)
            a = r['alignment']
            if i:   # khoảng trắng nối hai phần
                A['characters'].append(' '); A['character_start_times_seconds'].append(off); A['character_end_times_seconds'].append(off)
            A['characters'] += a['characters']; A['character_start_times_seconds'] += [t + off for t in a['character_start_times_seconds']]; A['character_end_times_seconds'] += [t + off for t in a['character_end_times_seconds']]
            off += float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
        lst = os.path.join(td, 'l.txt'); open(lst, 'w').write(''.join(f"file '{f}'\n" for f in files))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', mp3], check=True)
    json.dump(A, open(al, 'w')); open(tx, 'w').write(sig + '\n' + text + '\n')
    print(f'[tts] {key}: {len(parts)} phần {[len(x) for x in parts]} ký tự', file=sys.stderr)
    return mp3, A, sent


ll.tts = tts_k2

if __name__ == '__main__':
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == 'prep':
        ll.prep(path); import yaml; E0 = yaml.safe_load(open(path))
        if E0.get('brand'):   # chữ thẻ kết Short → timeline (render.js đọc TL.brand)
            tp = os.path.join(E0.get('out') or f"/var/tmp/cine-out/{E0['id']}", 'timeline.json'); T = json.load(open(tp)); T['brand'] = E0['brand']; json.dump(T, open(tp, 'w'), indent=1, ensure_ascii=False)
    elif cmd == 'cams':
        E = _load(path); cnt, where, bad = repeat_check(E)
        for (a, b), n in sorted(cnt.items(), key=lambda x: -x[1]): print(f"{'LỖI ' if n > MAX_SAME else '    '}{n:>2}  {a:<18} {b:<16} {', '.join(where[(a, b)])}")
        print(f"tổng {sum(cnt.values())} shot cảnh 3D, {len(cnt)} góc máy khác nhau, {len(bad)} góc vượt {MAX_SAME}"); sys.exit(1 if bad else 0)
    elif cmd == 'check':
        e, w = ll.check(ll.load(path)); [print('CẢNH BÁO', x) for x in w]; [print('LỖI', x) for x in e]; print('ĐẠT' if not e else 'TRƯỢT'); sys.exit(1 if e else 0)
