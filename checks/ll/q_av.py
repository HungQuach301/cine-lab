"""Q28 âm thanh · Q29 hình–lời · Q30 liền mạch — luật khoá LL v3 (phiên K, 07/10/2026). Định nghĩa: checks/ll/RULES-LL.md.

Mỗi hàm trả dict(ok, val, note, loi=[...]). Dữ liệu: đặc tả (map: mỗi đoạn), timeline.json, mix.json (mix.py ghi), tệp lời
(vo_file trong timeline, kèm .align.json), master hoặc các phần bản xem (đo màu, đo loudness).
Khác thước làm việc của P (scripts/ll/cont.py): xem bảng "Phán quyết K — checks LL v3" trong checks-appeal.md.
"""
import difflib, hashlib, json, os, re, subprocess
import numpy as np

from checks.ll import base

ACT_COLOR = {1: 'warm', 2: 'sepia', 3: 'cold', 4: 'warm'}
HERO = {'plate', 'diptych'}                                      # cảnh đinh 3D
PHYS = {'plate', 'diptych', 'archive', 'jobboard', 'filmstrip', 'pasteup', 'sign', 'isotype', 'stack', 'desk', 'street',
        'inspect', 'office', 'rows', 'teller'}                    # hình vật chất (cảnh toàn khung có vật/người/nơi chốn); thẻ giấy, bản đồ, chữ: không
FULL = PHYS | {'endcard'}                                        # cảnh toàn khung (đo màu theo hồi)
AUTO_SFX = {'assets/ll/sfx/paper-slide.mp3', 'assets/ll/sfx/paper-flip.mp3'}   # tiếng chuyển thẻ tự sinh: không phải âm thanh nghề
THEME_SHA = 'b138685f01f2c3857303ef4f8ab1be1de1a23dad17bac1676d3820bcc2cd34d4'  # nhạc hiệu kênh "Reawakening" (RIGHTS LL-MUS-1)
MUSIC_REPEAT_MAX = 60.0
SIL_MIN, SIL_MAX, SIL_DB = 0.5, 1.0, -50.0
LUFS, LUFS_TOL, TP_MAX = -14.0, 0.5, -1.0
WIN29, VIS29 = 1.0, 0.5                                          # ±1 s quanh từ; hình phải hiện ≥ 0,5 s trong cửa sổ (không tính đuôi fade)
JL_MIN = 0.3
# màu theo hồi (CIELAB, điểm ảnh L* > 15 của cảnh toàn khung). Q-L30 = B (chủ dự án 07/10/2026): chỉ đòi hồi 3 (hôm nay) LẠNH NHẤT trong
# 4 hồi = b* trung bình (trục vàng–xanh) thấp nhất. Chưa đặt ngưỡng tuyệt đối; hiệu chuẩn lại sau tập 7–8.
COLD_ACT = 3
NAME_SIM = 0.75
# cảnh đinh (cảnh, biến thể góc máy) K đã xem tận mắt có ngọn đèn trong khung (07/10/2026, tập 6 v2). ep06/cellar b (khay chữ cận) và
# ep06/printshop b chưa thấy đèn: không có trong danh sách. Cảnh mới: P khai heroes.<khoá>.lamp: true; người xem Q31 và K đối chiếu.
LAMP_SEEN = {('ep06/printshop', 'a'), ('ep06/printshop', 'c'), ('ep06/printshop', 'd'), ('ep06/cellar', 'a'),
             ('ep06/linotype', 'a'), ('ep06/linotype', 'b'), ('ep06/drafts', 'a'), ('ep06/drafts', 'b')}


def P(p): return p if os.path.isabs(p) else os.path.join(base.REPO, p)


def sha(p):
    h = hashlib.sha256()
    with open(P(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def fdur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', P(p)], capture_output=True, text=True, check=True).stdout)


def pcm(p, sr=16000):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', P(p), '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32)


def ov(a, b): return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


def acts(E):
    return {s['id']: (s.get('map') or {}).get('act') for s in E['segments']}


def flat_words(TL):
    """{đoạn: [(từ đã chuẩn hoá, đầu tuyệt đối, cuối tuyệt đối, đầu trong tệp lời, là phần đầu của từ gốc)]}; từ có gạch nối tách ra"""
    out = {}
    for s in TL['segments']:
        if not s.get('vo_file'): continue
        al = json.load(open(P(s['vo_file'].replace('.mp3', '.align.json')))); off = s['t0'] + s['vo_offset']; L = []
        for w in base.words(al):
            parts = [base.norm(x) for x in re.split(r'[-‐–—]', w[3]) if base.norm(x)]
            for j, p in enumerate(parts): L.append((p.strip("'"), off + w[1], off + w[2], w[1], j == 0))
        out[s['id']] = L
    return out


def say_words(say): return [base.norm(x).strip("'") for x in re.split(r'[\s\-‐–—]+', str(say or '')) if base.norm(x)]


def anchor_hits(E, TL, FW=None):
    """mọi lần đọc số neo: [(khoá, đoạn, chỉ số từ, đầu tuyệt đối, đầu trong tệp lời, cuối từ trước (tuyệt đối) hoặc None)]"""
    FW = FW or flat_words(TL); out = []
    for k in E.get('anchors') or []:
        sw = say_words((E['numbers'].get(k) or {}).get('say'))
        for sid, L in FW.items():
            for i in range(len(L) - len(sw) + 1):
                if sw and L[i][4] and [x[0] for x in L[i:i + len(sw)]] == sw:
                    out.append((k, sid, i, L[i][1], L[i][3], L[i - 1][2] if i else None))
    return out


def silence_before(vo, t_local):
    """khoảng lặng thật (âm tệp lời, khung 10 ms < −50 dBFS) liền trước tiếng đầu tiên trong [t − 0,15, t + 0,25] s"""
    x = pcm(vo); fr = 160; n = len(x) // fr
    db = 20 * np.log10(np.sqrt((x[:n * fr].reshape(n, fr) ** 2).mean(1)) + 1e-9)
    a, b = max(0, int((t_local - 0.15) * 100)), min(n, int((t_local + 0.25) * 100))
    on = next((j for j in range(a, b) if db[j] >= SIL_DB), None)
    if on is None: return None
    j = on - 1
    while j >= 0 and db[j] < SIL_DB: j -= 1
    return round((on - j - 1) / 100.0, 2)


def ebur128(p):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', P(p), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = r[r.rfind('Summary:'):]; g = lambda k: float(s.split(k)[1].split()[0]); return g('I:'), g('Peak:')


# ---------------------------------------------------------------- Q28
def asr_check(E, TL, model='small.en'):
    """ASR độc lập trên từng tệp lời (faster-whisper, tất định: beam 5, nhiệt 0, không VAD). Từ khoá: mọi số trong lời
    (so theo GIÁ TRỊ, chặt) và tên riêng (chữ hoa không đứng đầu câu, ≥ 3 chữ; giống ≥ 0,75)."""
    from faster_whisper import WhisperModel
    M = WhisperModel(model, device='cpu', compute_type='int8', cpu_threads=4); bad = []
    spec = {s['id']: s for s in E['segments']}
    for s in TL['segments']:
        if not s.get('vo_file'): continue
        vo = ' '.join((spec[s['id']].get('vo') or '').split())
        names = set()
        for sent in re.split(r'(?<=[.!?:—])\s+', vo):
            for w in sent.split()[1:]:
                c = re.sub(r"[^A-Za-z'’-]", '', w)
                if c[:1].isupper() and len(c) > 2 and c.lower() not in ('the', 'its', 'and'): names.add(base.norm(c.replace('’', "'")).replace("'s", ''))
        vals = nums_of(vo)
        segs, _ = M.transcribe(pcm(s['vo_file']), language='en', beam_size=5, vad_filter=False, temperature=0.0, condition_on_previous_text=False)
        txt = ' '.join(z.text for z in segs); heard = {base.norm(w).replace("'s", '') for w in txt.split()}; hv = nums_of(txt)
        miss = [n for n in sorted(names - {''}) if not any(n == h or difflib.SequenceMatcher(None, n, h).ratio() >= NAME_SIM for h in heard)]
        missv = [v for v in sorted(vals) if not any(abs(v - h) < 1e-6 for h in hv) and not year_said(v, txt)]
        if miss or missv: bad.append(f"{s['id']}: thiếu {', '.join(miss + [str(v) for v in missv])}")
    return bad


UNITS = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split())}
TENS = {w: 10 * i for i, w in enumerate('_ _ twenty thirty forty fifty sixty seventy eighty ninety'.split()) if w != '_'}
SCALE = {'hundred': 100, 'thousand': 1e3, 'million': 1e6, 'billion': 1e9}


def nums_of(text):
    t = text.lower().replace('-', ' ').replace('—', ' ').replace('–', ' ')
    out = set(float(x.replace(',', '')) for x in re.findall(r'\d[\d,]*(?:\.\d+)?', t) if x.replace(',', '').replace('.', '', 1).isdigit())
    W = re.findall(r"[a-z]+|\d[\d,.]*", t); i = 0
    while i < len(W):
        if W[i] in UNITS or W[i] in TENS:
            tot, cur, j, dec = 0, 0, i, None
            while j < len(W) and (W[j] in UNITS or W[j] in TENS or W[j] in SCALE or W[j] in ('and', 'point')):
                w = W[j]
                if w == 'point': dec = ''; j += 1; continue
                if dec is not None:
                    if w in UNITS: dec += str(UNITS[w]); j += 1; continue
                    break
                if w in UNITS: cur += UNITS[w]
                elif w in TENS: cur += TENS[w]
                elif w == 'hundred': cur *= 100
                elif w in SCALE: tot += cur * SCALE[w]; cur = 0
                j += 1
            v = tot + cur
            if dec: v = float(f'{int(v)}.{dec}') if v == int(v) else v
            out.add(float(v)); i = j
        else: i += 1
    return out


def _say99(n):
    U = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
    T = '_ _ twenty thirty forty fifty sixty seventy eighty ninety'.split()
    return U[n] if n < 20 else T[n // 10] + ('' if n % 10 == 0 else ' ' + U[n % 10])


def year_said(y, txt):
    t = ' ' + re.sub(r'[^a-z ]', ' ', txt.lower().replace('-', ' ')) + ' '
    if not (1800 <= y <= 2100 and y == int(y)): return False
    y = int(y); a, b = _say99(y // 100), y % 100
    c = [f' {a} {_say99(b)} ', f' {a} hundred ' if b == 0 else '', f' {a} oh {_say99(b)} ' if b < 10 else '']
    if b % 10 == 0: c.append(f' {a} {_say99(b).replace("ty", "ties")} ')
    return any(x and x in t for x in c)


def q28(E, TL, MX, master=None, asr=True, rights=None):
    bad, segs, T = [], TL['segments'], TL['tong_s']
    U = MX.get('music_used') or []
    if not U: bad.append('mix.json không có music_used')
    # a. không lặp nguyên đoạn > 60 s; không cue nào phải lặp vòng
    for u in U:
        nm = os.path.basename(u['file'])
        if u.get('loop'): bad.append(f'{nm} lặp vòng')
        if u['src_to'] > fdur(u['file']) + 0.05: bad.append(f"{nm}: dùng tới {u['src_to']:.1f} s, bài dài {fdur(u['file']):.1f} s")
        if abs((u['src_to'] - u['ss']) - (u['t1'] - u['t0'])) > 0.1: bad.append(f"{nm}: đoạn bài {u['src_to'] - u['ss']:.1f} s ≠ thời lượng cue {u['t1'] - u['t0']:.1f} s")
    for i in range(len(U)):
        for j in range(i + 1, len(U)):
            if U[i]['file'] == U[j]['file']:
                o = ov((U[i]['ss'], U[i]['src_to']), (U[j]['ss'], U[j]['src_to']))
                if o > MUSIC_REPEAT_MAX: bad.append(f"{os.path.basename(U[i]['file'])} dùng lại {o:.0f} s")
    # b. nhạc hiệu kênh mở và kết; hồi 2 và hồi 3 mỗi hồi đúng một cue riêng, khác nhạc hiệu, khác nhau
    cue_at = lambda t: next((u['file'] for u in reversed(U) if u['t0'] <= t + 0.01), None)
    A = acts(E)
    for sid, a in A.items():
        if a not in ACT_COLOR: bad.append(f'{sid}: map.act = {a!r} (cần 1–4)')
    th = {f: sha(f) == THEME_SHA for f in {u['file'] for u in U}}
    if U and not th.get(cue_at(0.0)): bad.append(f'mở đầu không phải nhạc hiệu kênh ({os.path.basename(cue_at(0.0) or "?")})')
    if U and not th.get(cue_at(T - 1.0)): bad.append(f'kết không phải nhạc hiệu kênh ({os.path.basename(cue_at(T - 1.0) or "?")})')
    per = {a: {cue_at(s['t0'] + 3.5) for s in segs if A.get(s['id']) == a} for a in (2, 3)}
    for a in (2, 3):
        if len(per[a]) != 1 or any(th.get(x) for x in per[a]): bad.append(f'hồi {a}: cue {sorted(os.path.basename(x or "?") for x in per[a])}')
    if per[2] and per[2] == per[3]: bad.append('hồi 2 và hồi 3 cùng bài')
    # c. ≥ 1 âm thanh nghề mỗi shot cảnh đinh (plate, diptych): cue bắt đầu trong [đầu shot − 1,5 s, cuối shot]; tệp có SHA-256 ghi trong
    #    RIGHTS.md; không phải tiếng chuyển thẻ tự sinh
    R = rights if rights is not None else open(os.path.join(base.REPO, 'RIGHTS.md'), encoding='utf-8').read()
    sfx = [(c['at'], c['at'] + float(c.get('dur') or 1.0), c['file']) for c in MX.get('sfx_used') or [] if c['file'] not in AUTO_SFX]
    reg = {f: os.path.exists(P(f)) and sha(f) in R for f in {f for _, _, f in sfx}}
    norights = sorted(os.path.basename(f) for f, ok in reg.items() if not ok)
    if norights: bad.append('SFX không có SHA-256 trong RIGHTS.md: ' + ', '.join(norights))
    nohero, nh = [], 0
    for s in segs:
        for sh in s['shots']:
            if sh['tpl'] not in HERO: continue
            nh += 1; a0, a1 = s['t0'] + sh['t0'], s['t0'] + sh['t1']
            if not any(a0 - 1.5 <= b0 <= a1 and reg[f] for b0, _, f in sfx): nohero.append(f"{s['id']}@{sh['t0']:.1f}/{sh['tpl']}")
    if nohero: bad.append('cảnh đinh không có âm thanh nghề: ' + ', '.join(nohero))
    # d. khoảng lặng 0,5–1,0 s trước MỌI lần đọc số neo, đo trên âm thật của tệp lời; mỗi số neo phải tìm thấy
    FW = flat_words(TL); H = anchor_hits(E, TL, FW); vo = {s['id']: s['vo_file'] for s in segs if s.get('vo_file')}; sil = []
    for k in E.get('anchors') or []:
        if not any(h[0] == k for h in H): bad.append(f"số neo {k}: không tìm thấy cụm say {(E['numbers'].get(k) or {}).get('say')!r} trong lời")
    for k, sid, i, ta, tl, prev in H:
        g = silence_before(vo[sid], tl); sil.append((k, sid, g, round(ta - prev, 2) if prev is not None else None))
        if g is None or not SIL_MIN <= g <= SIL_MAX: bad.append(f'lặng trước {k} ở {sid}: {g} s')
    # e. loudness đo trên master (không có thì lấy mix.json)
    if master and os.path.exists(P(master)): I, TP = ebur128(master); src = 'master'
    else: I, TP = MX['master']['I'], MX['master']['TP']; src = 'mix.json'
    if not (abs(I - LUFS) <= LUFS_TOL and TP <= TP_MAX): bad.append(f'{src} {I} LUFS / {TP} dBTP')
    # f. ASR
    if asr:
        a = asr_check(E, TL) if asr is True else asr
        if a: bad.append('ASR ' + '; '.join(a))
    val = (f"{len(U)} cue · cảnh đinh có âm thanh nghề {nh - len(nohero)}/{nh} · lặng trước số neo "
           f"{[g for _, _, g, _ in sil]} s · {src} {I} LUFS / {TP} dBTP" + ('' if asr else ' · ASR: không chạy'))
    near = [f'lặng trước {k} ở {sid}: {g} s' for k, sid, g, _ in sil if g is not None and (abs(g - SIL_MIN) <= 0.05 * SIL_MIN or abs(g - SIL_MAX) <= 0.05 * SIL_MAX)]
    if TP > TP_MAX - 0.05 * abs(TP_MAX): near.append(f'TP {TP} dBTP')
    return dict(ok=not bad, val=val, note='; '.join(bad), loi=bad, sat_nguong=near, lang=sil)


# ---------------------------------------------------------------- Q29
def resolve_at(w, L, ctx):
    m = re.fullmatch(r'@([^#+]+?)(?:#(\d+))?([+\-][\d.]+)?', str(w).strip())
    if not m: return None, f'{ctx}: mốc sai cú pháp {w!r}'
    key = [x.strip("'") for x in say_words(m.group(1))]; nth, d = int(m.group(2) or 1), float(m.group(3) or 0)
    key = ''.join(key)   # "@eightysix" và "@eighty-six" cùng nghĩa
    hits, i = [], 0
    while i < len(L):
        if not L[i][4]: i += 1; continue
        j = i + 1
        while j < len(L) and not L[j][4]: j += 1
        if ''.join(x[0] for x in L[i:j]) == key: hits.append(L[i][1])
        i = j
    if len(hits) < nth: return None, f'{ctx}: không thấy "{m.group(1)}" lần {nth} trong lời'
    return hits[nth - 1] + d, None


def q29(E, TL):
    segs, spec = TL['segments'], {s['id']: s for s in E['segments']}; FW = flat_words(TL); bad, n = [], 0

    def phys(t):
        out = []
        for s in segs:
            for sh in s['shots']:
                v = ov((s['t0'] + sh['t0'], s['t0'] + sh['t1']), (t - WIN29, t + WIN29))
                if v > 0: out.append((sh['tpl'], v))
        return out
    for s in segs:
        mp = spec[s['id']].get('map') or {}
        if s.get('vo_file') and not mp.get('nouns'): bad.append(f"{s['id']}: bản đồ không khai danh từ chính (map.nouns)"); continue
        for nn in mp.get('nouns') or []:
            t, err = resolve_at(nn['w'], FW.get(s['id']) or [], s['id'])
            if err: bad.append(err); continue
            n += 1; P_ = phys(t)
            if not any(tp in PHYS and v >= VIS29 for tp, v in P_): bad.append(f"{s['id']} {nn['w']} @{t:.1f}s ({'/'.join(tp for tp, _ in P_)})")
    for k, sid, i, ta, tl, prev in anchor_hits(E, TL, FW):
        n += 1; P_ = phys(ta)
        if not any(tp in PHYS and v >= VIS29 for tp, v in P_): bad.append(f"số neo {k} ở {sid} @{ta:.1f}s ({'/'.join(tp for tp, _ in P_)})")
    return dict(ok=not bad and n > 0, val=f'{n - len(bad)}/{n} danh từ chính và lần đọc số neo có hình vật chất ≥ {VIS29} s trong ±{WIN29:.0f} s',
                note='; '.join(bad[:8]), loi=bad)


# ---------------------------------------------------------------- Q30
def act_tone(E, TL, videos):
    """tông trung bình mỗi hồi trên điểm ảnh: cảnh toàn khung, lưới 0,5 s, 32×18 RGB → CIELAB, chỉ điểm ảnh L* > 15"""
    import cv2
    F, Tt, off = [], [], 0.0
    for v in videos:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', P(v), '-vf', 'fps=2,scale=32:18:flags=area,format=rgb24', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
        c = np.frombuffer(raw, np.uint8).reshape(-1, 18, 32, 3); F.append(c); Tt.append(off + np.arange(len(c)) / 2.0); off += fdur(v)
    C = np.concatenate(F); t = np.concatenate(Tt)
    lab = cv2.cvtColor(C.reshape(1, -1, 3), cv2.COLOR_RGB2LAB).reshape(C.shape).astype(np.float64)
    L, a, b = lab[..., 0] * 100 / 255, lab[..., 1] - 128, lab[..., 2] - 128
    A = acts(E); out = {}
    for k in (1, 2, 3, 4):
        m = np.zeros(len(t), bool)
        for s in TL['segments']:
            if A.get(s['id']) != k: continue
            for sh in s['shots']:
                if sh['tpl'] in FULL: m |= (t >= s['t0'] + sh['t0']) & (t < s['t0'] + sh['t1'])
        w = L[m] > 15
        if not w.any(): continue
        am, bm = float(a[m][w].mean()), float(b[m][w].mean())
        out[k] = dict(a=round(am, 1), b=round(bm, 1), C=round(float(np.hypot(am, bm)), 1), h=round(float(np.degrees(np.arctan2(bm, am)) % 360), 1), mau=int(m.sum()))
    return out


def tone_errors(tone):
    """Q-L30 = B: hồi 3 phải có b* thấp nhất trong 4 hồi; thiếu hồi nào (không có cảnh toàn khung) thì TRƯỢT"""
    miss = [k for k in (1, 2, 3, 4) if k not in tone]
    if miss: return [f'hồi {miss} không có cảnh toàn khung để đo màu']
    other = min(tone[k]['b'] for k in (1, 2, 4))
    return [] if tone[COLD_ACT]['b'] < other else [f"hồi 3 không lạnh nhất: b* {tone[COLD_ACT]['b']} ≥ {other} (hồi khác thấp nhất)"]


def q30(E, TL, MX, videos=None, tone=None):
    segs, spec = TL['segments'], {s['id']: s for s in E['segments']}; A = acts(E); bad = []
    sfx = [(c['at'], c['at'] + float(c.get('dur') or 1.0)) for c in MX.get('sfx_used') or [] if c['file'] not in AUTO_SFX]
    HZ = E.get('heroes') or {}
    lamp_hero = lambda key: bool((HZ.get(key) or {}).get('lamp')) or ((HZ.get(key) or {}).get('hero'), (HZ.get(key) or {}).get('variant')) in LAMP_SEEN
    n = 0
    for a, b in zip(segs, segs[1:]):
        if A.get(a['id']) == A.get(b['id']): continue
        n += 1; ma, mb = spec[a['id']].get('map') or {}, spec[b['id']].get('map') or {}; cut = b['t0']; tag = f"{a['id']}→{b['id']}"
        # a. kiểu chuyển: hai phía khai cùng một kiểu, thuộc match / jcut / lcut; J/L-cut phải có tiếng kéo qua điểm cắt
        ty_o, ty_i = ma.get('out'), mb.get('in')
        if ty_o != ty_i or ty_o not in ('match', 'jcut', 'lcut'): bad.append(f'{tag}: chuyển out={ty_o} / in={ty_i}')
        note = (ma.get('out_note') or '') + ' ' + (mb.get('in_note') or '')
        if ty_o == 'jcut' or re.search(r'J-?cut', note, re.I):
            if not any(b0 <= cut - JL_MIN and b1 > cut for b0, b1 in sfx): bad.append(f'{tag}: J-cut không có tiếng vào trước điểm cắt ≥ {JL_MIN} s')
        if ty_o == 'lcut' or re.search(r'L-?cut', note, re.I):
            if not any(b0 < cut and b1 >= cut + JL_MIN for b0, b1 in sfx): bad.append(f'{tag}: L-cut không có tiếng kéo qua điểm cắt ≥ {JL_MIN} s')
        # b. ngọn đèn ở shot cuối trước và shot đầu sau điểm chuyển hồi
        if not ((ma.get('lamp') or {}).get('out') and (mb.get('lamp') or {}).get('in')): bad.append(f'{tag}: map không khai ngọn đèn')
        for sh, side in ((a['shots'][-1], 'trước'), (b['shots'][0], 'sau')):
            p = sh['p']; ok = sh['tpl'] == 'street' or (sh['tpl'] == 'text' and p.get('lamp')) or (sh['tpl'] == 'plate' and lamp_hero(p.get('hero'))) or \
                (sh['tpl'] == 'diptych' and any(lamp_hero((p.get(x) or {}).get('hero')) for x in ('left', 'right')))
            if not ok: bad.append(f'{tag}: shot {side} điểm cắt ({sh["tpl"]}{":" + str(p.get("hero")) if p.get("hero") else ""}) không có đèn (heroes.<khoá>.lamp)')
    if n == 0: bad.append('không có chuyển hồi (map.act)')
    # c. màu: map.color đúng hồi, và tông trung bình đo trên điểm ảnh đúng kịch bản màu
    for s in segs:
        c, a = (spec[s['id']].get('map') or {}).get('color'), A.get(s['id'])
        if a in ACT_COLOR and c != ACT_COLOR[a]: bad.append(f"{s['id']}: map.color {c}, hồi {a} cần {ACT_COLOR[a]}")
    tone = tone if tone is not None else (act_tone(E, TL, videos) if videos else None)
    if tone is None: bad.append('không có video để đo tông màu')
    else:
        bad += tone_errors(tone)
    val = f'{n} chuyển hồi · tông đo (b*): ' + (', '.join(f"hồi {k} {x['b']}" for k, x in sorted((tone or {}).items())) or '—')
    near = []
    if tone and all(k in tone for k in (1, 2, 3, 4)):
        o = min(tone[k]['b'] for k in (1, 2, 4))
        if abs(tone[COLD_ACT]['b'] - o) <= 0.05 * max(abs(o), 1e-9): near.append(f"b* hồi 3 {tone[COLD_ACT]['b']} sát hồi khác {o}")
    return dict(ok=not bad, val=val, note='; '.join(bad[:8]), loi=bad, tong=tone, sat_nguong=near)
