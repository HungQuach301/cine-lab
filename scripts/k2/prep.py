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
        'design/k2v/page.js', 'design/k2v/common.js', 'design/k2v/map.js', 'design/k2v/chart3d.js', 'design/k2v/photo.js']
CAMS = os.path.join(REPO, 'scripts/k2/cams.yaml')
MAX_SAME = 2   # cùng góc máy (scene_id + camera_id) tối đa 2 lần/tập


def code_bytes():
    return b''.join(open(os.path.join(REPO, f), 'rb').read() for f in CODE)


def cam_lib():
    import yaml
    return yaml.safe_load(open(CAMS)) if os.path.exists(CAMS) else {}


def resolve_cams(E):
    """heroes.<k>.cam: '<preset>' → opt.cam từ thư viện (scene_id phải có preset đó). Gắn _camera_id cho mỗi khoá cảnh."""
    L = cam_lib()
    for k, h in (E.get('heroes') or {}).items():
        o = h.setdefault('opt', {}); c = h.get('cam')
        if isinstance(o.get('cam'), str): c = o.pop('cam')
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
    return {'map': 'map', 'chart3d': 'chart3d'}.get(m) or ({'print': 'photo', 'doc': 'document', 'headline': 'document'}.get(n) if m == 'photo' else 'scene3d')


def shot_meta(E, sh):
    p = sh.get('p', {}); HZ = E.get('heroes') or {}; k = p.get('hero') if sh.get('tpl') == 'plate' else None; h = HZ.get(k) if k else None
    card = bool(p.get('card'))
    M = dict(type='card' if card else shot_type(h['hero'] if h else None), scene_id=h['hero'] if h else None, camera_id=h.get('_camera_id') if h else None,
             places=[x['a'] if isinstance(x, dict) else x for x in p.get('places', [])], people=[])
    for f in ('type', 'scene_id', 'camera_id', 'places', 'people'):
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
                                                               **{f: sh[f] for f in ('type', 'scene_id', 'camera_id', 'places', 'people')}))
    json.dump(meta, open(os.path.join(E['out'], 'shots-meta.json'), 'w'), indent=1, ensure_ascii=False)
    bad = [f"{sg['id']}/{i}" for kind in ('segments', 'shorts') for sg in TL[kind] for i, sh in enumerate(sg['shots']) if sh['t1'] <= sh['t0'] + 0.3]
    if bad: raise SystemExit('Shot sai thứ tự hoặc < 0,3 s (mốc "@từ" khớp nhầm lần xuất hiện? dùng #n): ' + ', '.join(bad))
    HZ = E.get('heroes') or {}
    if not HZ: return
    code = b''.join(open(os.path.join(REPO, f), 'rb').read() for f in CODE)
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
        stamp = hashlib.sha1(code + json.dumps([h, dur, size], sort_keys=True).encode()).hexdigest()[:12]
        plan[k] = dict(hero=h['hero'], variant=h.get('variant', 'a'), opt=h['opt'], dur=dur, size=size, dir=f"{ll.HERO_ROOT}/{E['id']}-{k}{'-d' if DRAFT else ''}", stamp=stamp)
    for kind in ('segments', 'shorts'):
        for sg in TL[kind]:
            for sh in sg['shots']:
                p = sh['p']
                if sh['tpl'] == 'plate' and p.get('hero'): p['dir'] = plan[p['hero']]['dir']; p['stamp'] = plan[p['hero']]['stamp']
    TL['heroes'] = plan; TL['draft'] = DRAFT
    json.dump(plan, open(os.path.join(E['out'], 'heroes.json'), 'w'), indent=1, ensure_ascii=False)


ll.heroes_plan = heroes_plan
_load = ll.load


def load_checked(path):
    """ll.load + chặn lặp góc máy (trước TTS) + gắn preset máy quay."""
    E = _load(path); cnt, where, bad = repeat_check(E)
    if bad: raise SystemExit('LẶP GÓC MÁY (> %d lần/tập, chủ dự án 12/10/2026): ' % MAX_SAME + '; '.join(f'{a} @ {b}: {n} lần ({", ".join(where[(a, b)])})' for (a, b), n in sorted(bad.items())))
    return E


ll.load = load_checked

if __name__ == '__main__':
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == 'prep': ll.prep(path)
    elif cmd == 'cams':
        E = _load(path); cnt, where, bad = repeat_check(E)
        for (a, b), n in sorted(cnt.items(), key=lambda x: -x[1]): print(f"{'LỖI ' if n > MAX_SAME else '    '}{n:>2}  {a:<18} {b:<16} {', '.join(where[(a, b)])}")
        print(f"tổng {sum(cnt.values())} shot cảnh 3D, {len(cnt)} góc máy khác nhau, {len(bad)} góc vượt {MAX_SAME}"); sys.exit(1 if bad else 0)
    elif cmd == 'check':
        e, w = ll.check(ll.load(path)); [print('CẢNH BÁO', x) for x in w]; [print('LỖI', x) for x in e]; print('ĐẠT' if not e else 'TRƯỢT'); sys.exit(1 if e else 0)
