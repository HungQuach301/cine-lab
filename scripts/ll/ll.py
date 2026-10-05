#!/opt/cine/bin/python
"""Last Lamplighters · nhà máy — chuẩn bị một tập từ episode.yaml.

  ll.py prep <episode.yaml>        kiểm đặc tả → thu lời Bill (ElevenLabs, có cache) → giải mốc "@từ" → <out>/timeline.json, sfx, phụ đề .srt
  ll.py check <episode.yaml>       chỉ kiểm đặc tả (không gọi mạng); in lỗi, mã thoát 1 nếu có lỗi
  ll.py est <episode.yaml>         ước trước khi thu lời (không gọi mạng): thời lượng từng đoạn, tỷ lệ STORY/HISTORY/TODAY theo
                                   tốc độ đọc thật của Bill (BILL_WPS, đo tập 2), mọi mốc "@từ" giải được, và khung đồ hoạ có thể đứng trống > 3 s

Đặc tả (xem scripts/ll/README.md): id, title, out, voice, music, sources, numbers, segments[{id, part, vo, shots[{tpl, at, in, p}]}], shorts[...].
Luật kiểm sẵn ở đây (chặn trước khi render):
  - mỗi số (numbers) có nguồn; nguồn có read: fulltext; URL nguồn không phải Wikipedia/Wikimedia;
  - số dự báo phải khai kind: projection (mẫu tự gắn nhãn PROJECTION); compare hai vế cùng đơn vị;
  - số có trường say: cụm đọc phải có trong lời của đoạn chứa hình (số trên hình khớp lời đọc);
  - shot đồ hoạ số có dòng nguồn (tự sinh từ nguồn của các số dùng trong shot).
"""
import base64, hashlib, json, os, re, subprocess, sys, urllib.request
import yaml

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FPS = 24
DATA_TPL = {'bars', 'line', 'compare', 'bignum'}
GFX_TPL = DATA_TPL | {'text', 'quote'}
BILL_WPS = 2.214   # từ/giây lời Bill đo trên 15 đoạn tập 2 (1 062 từ / 479,6 s), tốc độ 1,00
BLANK_MAX = 3.0    # luật kênh §5.1: khung đồ hoạ không đứng trống quá 3 s khi đang có lời
P = lambda p: p if os.path.isabs(p) else os.path.join(REPO, p)


def norm(w): return re.sub(r"[^a-z0-9']", '', w.lower())


def load(path):
    E = yaml.safe_load(open(path))
    E.setdefault('out', f"/var/tmp/cine-out/{E['id']}")
    E.setdefault('vo_dir', os.path.join(os.path.dirname(os.path.relpath(path, REPO)), 'vo'))
    return E


def nums_in(x, acc):
    if isinstance(x, dict):
        if 'num' in x and not x.get('echo'): acc.append(x['num'])
        for v in x.values(): nums_in(v, acc)
    elif isinstance(x, list):
        for v in x: nums_in(v, acc)
    return acc


def check(E):
    err, warn = [], []
    S, N = E.get('sources', {}), E.get('numbers', {})
    for k, s in S.items():
        if re.search(r'wikipedia\.org|wikimedia\.org', s.get('url', ''), re.I): err.append(f'nguồn {k}: Wikipedia/Wikimedia không được làm nguồn chính')
        if s.get('read') != 'fulltext': err.append(f'nguồn {k}: chưa đọc toàn văn (read: {s.get("read")})')
        for f in ('short', 'url', 'accessed'):
            if not s.get(f): err.append(f'nguồn {k}: thiếu {f}')
    for k, n in N.items():
        if n.get('src') not in S: err.append(f'số {k}: nguồn {n.get("src")} không có trong sources')
        if n.get('kind') not in ('actual', 'projection'): err.append(f'số {k}: kind phải là actual hoặc projection')
        if n.get('kind') == 'projection' and not n.get('period'): err.append(f'số {k}: số dự báo phải ghi period (ví dụ 2024–34)')
    allv = E.get('segments', []) + E.get('shorts', [])
    for sg in allv:
        vo = ' '.join(norm(w) for w in (sg.get('vo') or '').split())
        for sh in sg.get('shots', []):
            used = nums_in(sh.get('p', {}), [])
            for k in used:
                if k not in N: err.append(f'{sg["id"]}/{sh["tpl"]}: số {k} không có trong numbers'); continue
                say = N[k].get('say')
                if say and ' '.join(norm(w) for w in say.split()) not in vo:
                    (err if sg in E.get('segments', []) else warn).append(f'{sg["id"]}/{sh["tpl"]}: số {k} ("{say}") không có trong lời đoạn')
            if sh['tpl'] in DATA_TPL and not used and not sh.get('p', {}).get('src'):
                err.append(f'{sg["id"]}/{sh["tpl"]}: shot số liệu không có số khai báo hay nguồn')
            if sh['tpl'] == 'compare':
                p = sh['p']; u = [N.get(p[s].get('num'), {}).get('unit') for s in ('left', 'right') if 'num' in p[s]]
                if len(set(u)) > 1: err.append(f'{sg["id"]}/compare: hai vế khác đơn vị {u} (luật so sánh tương xứng điểm 2)')
    return err, warn


# ---------- ước trước khi thu lời (rút kinh nghiệm tập 2) ----------
def fake_words(text, off=0.0):
    ws = text.split(); return [(norm(w), off * 0 + i / BILL_WPS, (i + 1) / BILL_WPS, w) for i, w in enumerate(ws)]


def ats_in(x, acc, skip=('cam',)):
    """mọi giá trị 'at' / 'noteAt' / 'midAt' / 'diffAt' / 'capAt' trong p (bỏ quỹ đạo máy) = lúc nội dung gắn lời hiện ra"""
    if isinstance(x, dict):
        for k, v in x.items():
            if k in skip: continue
            if k in ('at', 'noteAt', 'midAt', 'diffAt', 'capAt') and isinstance(v, (int, float)): acc.append(float(v))
            else: ats_in(v, acc, skip)
    elif isinstance(x, list):
        for v in x: ats_in(v, acc, skip)
    return acc


def est(E):
    N, S = E.get('numbers', {}), E.get('sources', {})
    rows, parts, warn, t_abs = [], {}, [], 0.0
    for sg in E['segments']:
        off = float(sg.get('vo_offset', 0.8 if sg.get('vo') else 0)); W = fake_words(sg.get('vo') or '')
        vlen = W[-1][2] if W else 0
        dur = max(float(sg.get('min_dur', 0)), off + vlen + float(sg.get('tail', 1.0))) if W else float(sg.get('dur', 6))
        try: shots, _ = build_seg(E, sg, W, off, dur)
        except SystemExit as e: warn.append(f'{sg["id"]}: {e}'); shots = []
        for sh in shots:
            if sh['tpl'] not in GFX_TPL: continue
            if sh['tpl'] == 'text' and any('at' not in l for l in sh['p'].get('lines', [])): continue   # thẻ tựa: chữ hiện ngay
            first = min([a for a in ats_in(sh['p'], []) if a >= sh['t0'] - 0.01] or [sh['t1']])
            speaking = W and first > off and sh['t0'] < off + vlen
            gap = first - max(sh['t0'], off) if speaking else 0
            if gap > BLANK_MAX - 0.5: warn.append(f'{sg["id"]}/{sh["tpl"]}@{sh["t0"]:.1f}s: ước {gap:.1f} s chưa có nội dung gắn lời (ngưỡng {BLANK_MAX} s, ước sai ±0,5 s) — thêm beats hoặc neo sớm hơn')
        parts[sg.get('part')] = parts.get(sg.get('part'), 0) + dur
        rows.append((sg['id'], sg.get('part'), len(W), round(dur, 1))); t_abs += dur
    return rows, {k: round(100 * v / t_abs, 1) for k, v in parts.items()}, t_abs, warn


# ---------- lời Bill ----------
def el(path, body=None):
    req = urllib.request.Request('https://api.elevenlabs.io' + path, data=json.dumps(body).encode() if body else None,
                                 headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=300))


def chars_used():
    try: return el('/v1/user/subscription').get('character_count')
    except Exception as e: return f'không đọc được ({e})'


def tts(E, key, text):
    d = P(E['vo_dir']); os.makedirs(d, exist_ok=True)
    mp3, al, tx = (os.path.join(d, f'{key}.{x}') for x in ('mp3', 'align.json', 'txt'))
    v = E['voice']; sig = hashlib.sha1(json.dumps([text, v], sort_keys=True).encode()).hexdigest()[:12]
    if os.path.exists(mp3) and os.path.exists(tx) and open(tx).read().split('\n')[0] == sig: return mp3, json.load(open(al)), 0
    r = el(f"/v1/text-to-speech/{v['id']}/with-timestamps?output_format=mp3_44100_128",
           dict(text=text, model_id=v.get('model', 'eleven_multilingual_v2'),
                voice_settings=dict(stability=v.get('stability', 0.5), similarity_boost=v.get('similarity', 0.75), speed=1.0)))
    open(mp3, 'wb').write(base64.b64decode(r['audio_base64'])); json.dump(r['alignment'], open(al, 'w'))
    open(tx, 'w').write(sig + '\n' + text + '\n')
    return mp3, r['alignment'], len(text)


def words(al):
    out, cur, t0 = [], '', None
    for c, s, e in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if c.isspace():
            if cur: out.append((norm(cur), t0, last, cur)); cur = ''
            continue
        if not cur: t0 = s
        cur += c; last = e
    if cur: out.append((norm(cur), t0, last, cur))
    return out


def anchor(s, W, off, ctx):
    m = re.fullmatch(r'@([^#+\-]+(?:-[a-z]+)*)(?:#(\d+))?([+\-][\d.]+)?', s.strip())
    if not m: raise SystemExit(f'{ctx}: mốc sai cú pháp {s!r}')
    key, nth, d = norm(m.group(1)), int(m.group(2) or 1), float(m.group(3) or 0)
    hits = [w for w in W if w[0] == key]
    if len(hits) < nth: raise SystemExit(f'{ctx}: không thấy từ "{m.group(1)}" (lần {nth}) trong lời')
    return round(off + hits[nth - 1][1] + d, 3)


def resolve(x, W, off, ctx, N, S, srcs):
    if isinstance(x, str) and x.startswith('@'): return anchor(x, W, off, ctx)
    if isinstance(x, list): return [resolve(v, W, off, ctx, N, S, srcs) for v in x]
    if isinstance(x, dict):
        y = {k: resolve(v, W, off, ctx, N, S, srcs) for k, v in x.items()}
        if 'num' in y:
            n = N[y['num']]; srcs.add(n['src'])
            y.setdefault('value', n['v']); y.setdefault('text', n.get('text')); y.setdefault('kind', n['kind'])
        return y
    return x


def build_seg(E, sg, W, off, dur, ctx_short=False):
    N, S = E.get('numbers', {}), E.get('sources', {})
    shots, cues = [], []
    ats = [sh.get('at', 0) for sh in sg['shots']]
    ats = [anchor(a, W, off, sg['id']) if isinstance(a, str) else float(a) for a in ats]
    for i, sh in enumerate(sg['shots']):
        srcs = set(); p = resolve(sh.get('p', {}), W, off, f"{sg['id']}/{sh['tpl']}", N, S, srcs)
        if isinstance(p.get('src'), list): srcs |= set(p['src']); p.pop('src')
        if srcs and not isinstance(p.get('src'), str):
            ks = sorted(srcs); p['src'] = ('Sources: ' if len(ks) > 1 else 'Source: ') + ' · '.join(S[k]['short'] for k in ks)
        t1 = ats[i + 1] if i + 1 < len(ats) else dur
        tr = sh.get('in', 'cut'); tr = tr if isinstance(tr, dict) else {'type': tr, 'd': 0.7}
        shots.append(dict(tpl=sh['tpl'], t0=ats[i], t1=t1, **({'in': tr} if i else {}), p=p))
        if i and tr['type'] in ('slide', 'flip'): cues.append(dict(file='assets/ll/sfx/paper-slide.mp3' if tr['type'] == 'slide' else 'assets/ll/sfx/paper-flip.mp3',
                                                              at=ats[i] + 0.05, gain_db=-4, **({} if tr['type'] == 'slide' else {'src_ss': 3.55, 'dur': 0.85})))
        if sh['tpl'] == 'street':
            for l in p.get('lamps', []):
                if 'lit' in l: cues.append(dict(file='assets/ll/sfx/gas-hiss.mp3', at=l['lit'], src_ss=2.0, dur=1.6, gain_db=-10, fade_ms=200))
        for c in sh.get('sfx', []):
            c = dict(c); c['at'] = anchor(c['at'], W, off, sg['id']) if isinstance(c['at'], str) else float(c['at']); cues.append(c)
    return shots, cues


def srt_lines(W, off, maxc=42):
    out, cur = [], []
    for w in W:
        cand = ' '.join(x[3] for x in cur + [w])
        if cur and (len(cand) > maxc or re.search(r'[.!?]$', cur[-1][3])): out.append(cur); cur = []
        cur.append(w)
    if cur: out.append(cur)
    return [(off + c[0][1], off + c[-1][2], ' '.join(x[3] for x in c)) for c in out]


def ts(s): h, r = divmod(s, 3600); m, r = divmod(r, 60); return f'{int(h):02d}:{int(m):02d}:{r:06.3f}'.replace('.', ',')


def prep(path):
    E = load(path); err, warn = check(E)
    for w in warn: print('CẢNH BÁO', w)
    if err: print('\n'.join('LỖI ' + e for e in err)); sys.exit(1)
    os.makedirs(E['out'], exist_ok=True)
    c0 = chars_used(); sent = 0
    TL = dict(id=E['id'], title=E.get('title'), music=E.get('music', []), segments=[], shorts=[], el_before=c0)
    t_abs, srt = 0.0, []
    for sg in E['segments']:
        W, mp3, al, off = [], None, None, float(sg.get('vo_offset', 0.8 if sg.get('vo') else 0))
        if sg.get('vo'):
            mp3, al, n = tts(E, f"{E['id']}-{sg['id']}", sg['vo'].strip()); sent += n; W = words(al)
        vlen = (W[-1][2] if W else 0)
        dur = max(float(sg.get('min_dur', 0)), off + vlen + float(sg.get('tail', 1.0)) if W else float(sg.get('dur', 6)))
        frames = int(round(dur * FPS)); dur = frames / FPS
        shots, cues = build_seg(E, sg, W, off, dur)
        for c in cues: c['at_abs'] = round(t_abs + c.pop('at'), 3)
        TL['segments'].append(dict(id=sg['id'], part=sg.get('part'), t0=round(t_abs, 4), t1=round(t_abs + dur, 4), frames=frames,
                                   vo_file=os.path.relpath(mp3, REPO) if mp3 else None, vo_offset=off, vo_len=round(vlen, 3),
                                   speech=[[round(off + w[1], 3), round(off + w[2], 3)] for w in W], shots=shots, sfx=cues,
                                   fadeIn=sg.get('fadeIn'), fadeOut=sg.get('fadeOut')))
        srt += [(t_abs + a, t_abs + b, s) for a, b, s in srt_lines(W, off)]
        t_abs += dur
    for sh in E.get('shorts', []):
        lead = 0.6; mp3, W = None, []
        if sh.get('vo'): mp3, al, n = tts(E, f"{E['id']}-short-{sh['id']}", sh['vo'].strip()); sent += n; W = words(al)
        dur = (lead + W[-1][2] + float(sh.get('tail', 0.8)) + 1.5) if W else float(sh['dur']); frames = int(round(dur * FPS)); dur = frames / FPS
        sh2 = dict(sh); sh2.setdefault('vo', ''); sh2['shots'] = sh['shots'] + [dict(tpl='endcard', at=dur - 1.5, **{'in': 'fade'}, p=dict(line='full film on the channel'))]
        shots, cues = build_seg(E, sh2, W, lead, dur, True)
        for c in cues: c['at_abs'] = round(c.pop('at'), 3)
        TL['shorts'].append(dict(id=sh['id'], hook=sh.get('hook'), t0=0, t1=dur, frames=frames, vo_file=os.path.relpath(mp3, REPO) if mp3 else None, vo_offset=lead,
                                 speech=[[round(lead + w[1], 3), round(lead + w[2], 3)] for w in W], shots=shots, sfx=cues, fadeOut=0))
    TL['tong_s'] = round(t_abs, 4); TL['tong_khung'] = sum(s['frames'] for s in TL['segments'])
    TL['el_sent'] = sent; TL['el_after'] = chars_used() if sent else c0
    parts = {}
    for s in TL['segments']: parts[s['part']] = parts.get(s['part'], 0) + s['t1'] - s['t0']
    TL['ty_le'] = {k: round(100 * v / t_abs, 1) for k, v in parts.items()}
    json.dump(TL, open(os.path.join(E['out'], 'timeline.json'), 'w'), indent=1, ensure_ascii=False)
    open(os.path.join(E['out'], E['id'] + '.en.srt'), 'w').write(''.join(f'{i}\n{ts(a)} --> {ts(b)}\n{s}\n\n' for i, (a, b, s) in enumerate(srt, 1)))
    print(json.dumps(dict(tong_s=TL['tong_s'], khung=TL['tong_khung'], ty_le=TL['ty_le'], el=[c0, sent, TL['el_after']],
                          doan=[(s['id'], round(s['t1'] - s['t0'], 2)) for s in TL['segments']], shorts=[(s['id'], round(s['t1'], 2)) for s in TL['shorts']]), ensure_ascii=False))


if __name__ == '__main__':
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == 'check':
        e, w = check(load(path)); [print('CẢNH BÁO', x) for x in w]; [print('LỖI', x) for x in e]; print('ĐẠT' if not e else 'TRƯỢT'); sys.exit(1 if e else 0)
    elif cmd == 'prep': prep(path)
    elif cmd == 'est':
        rows, ty, T, w = est(load(path))
        for r in rows: print(f'  {r[0]:>4} {r[1]:<8} {r[2]:>4} từ  {r[3]:>6.1f} s')
        print(f'TỔNG ≈ {int(T // 60)}:{T % 60:04.1f} ({sum(r[2] for r in rows)} từ, {BILL_WPS} từ/s)  tỷ lệ {ty}')
        [print('CẢNH BÁO', x) for x in w]
