#!/opt/cine/bin/python
"""KÊNH 2 · chuẩn bị một tập: dùng nguyên scripts/ll/ll.py (kiểm đặc tả, lời ElevenLabs có cache, mốc "@từ", nguồn tự sinh, timeline, .srt),
thay riêng bước kế hoạch cảnh 3D:
  - opt của cảnh 3D nhận mốc lời: "@từ" (± giây) → giây trong cảnh, tính theo shot ĐẦU TIÊN dùng cảnh đó (hoặc "NN@từ" = shot đầu tiên trong đoạn NN):
        giây_cảnh = (mốc_trong_đoạn − t0_shot) × speed + frame0 / 24   → sự kiện trong cảnh 3D (rót thép, vẽ tuyến, thanh chắn nâng…) khớp lời.
  - dấu (stamp) chỉ băm mã K2 (design/ll-hero/k2g01.js, k2page.js, kit.js, scripts/k2/hero.js) + tham số → sửa cảnh K2 không đổi dấu cảnh LL và ngược lại.
  - K2_DRAFT=1: nháp 960×540 (9:16 → 540×960), thư mục cảnh hậu tố -d.
  prep.py prep|check <episode.yaml>
"""
import hashlib, json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'll'))
import ll  # noqa: E402

REPO, FPS = ll.REPO, ll.FPS
DRAFT = os.environ.get('K2_DRAFT') == '1'
CODE = ['design/ll-hero/k2g01.js', 'design/ll-hero/k2page.js', 'design/ll-hero/kit.js', 'scripts/k2/hero.js']


def seg_words(sg):
    if not sg.get('vo_file'): return []
    return ll.words(json.load(open(os.path.join(REPO, sg['vo_file'][:-4] + '.align.json'))))


def heroes_plan(E, TL):
    # chặn shot sai thứ tự (G2 K2G-01: "@by"/"@question" khớp nhầm lần xuất hiện đầu → thẻ số neo không hiện)
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
        h = dict(HZ[k]); h['opt'] = res(h.get('opt', {}), k, f'heroes.{k}.opt')
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

if __name__ == '__main__':
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == 'prep': ll.prep(path)
    elif cmd == 'check':
        e, w = ll.check(ll.load(path)); [print('CẢNH BÁO', x) for x in w]; [print('LỖI', x) for x in e]; print('ĐẠT' if not e else 'TRƯỢT'); sys.exit(1 if e else 0)
