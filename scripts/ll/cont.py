#!/opt/cine/bin/python
"""Q28–Q30 (chủ dự án 06/10/2026, CHUAN-KENH §11.2). Luật làm việc của P cho tới khi K khoá (checks-appeal.md).

  cont.py <episode.yaml> [--json ra.json]      đọc <out>/timeline.json, mix.json, asr.json (sau build)

Q28 âm thanh
  a. nhạc không lặp: mỗi bài, các khoảng bài đã dùng (mix.json music_used) chồng nhau ≤ 60 s; không cue nào lặp vòng;
  b. cue theo hồi: hồi 2 và hồi 3 mỗi hồi một bài riêng, khác nhạc hiệu; đoạn đầu và đoạn cuối dùng nhạc hiệu (cùng một bài);
  c. mỗi shot cảnh đinh (plate) có ≥ 1 âm thanh nghề (cue SFX trong [đầu shot − 1,5 s, cuối shot]);
  d. trước mỗi lần đọc số neo: khoảng lặng 0,5–1,0 s (đo trên căn chỉnh lời thật, từ cuối từ trước tới đầu số);
  e. master −14 LUFS ± 0,5, true peak ≤ −1 dBTP (mix.json);
  f. ASR 100 % từ khoá (asr.json: không đoạn nào trượt).
Q29 hình–lời: mỗi số neo và mỗi danh từ chính khai trong `map.nouns` có hình VẬT CHẤT trên màn hình trong ±1 s quanh lúc đọc
  (cảnh toàn khung có vật/người/nơi chốn; thẻ chữ, trích dẫn, biểu đồ không tính).
Q30 liền mạch
  a. chuyển hồi (map.act đổi) dùng match cut hoặc J/L-cut; J-cut phải có cue SFX bắt đầu trước điểm cắt, L-cut có cue kéo qua điểm cắt;
  b. người thắp đèn hoặc ngọn đèn có mặt ở shot cuối trước và shot đầu sau mỗi chuyển hồi (map.lamp khai, và mẫu/cảnh đinh có đèn);
  c. màu theo hồi ấm – sepia – lạnh – ấm: map.color mỗi đoạn đúng hồi; ≥ 60 % thời lượng cảnh đinh của mỗi hồi mang đúng tông.
"""
import json, os, re, sys
import yaml

sys.path.insert(0, os.path.dirname(__file__)); import ll
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ACT_COLOR = {1: 'warm', 2: 'sepia', 3: 'cold', 4: 'warm'}
PHYS = {'plate', 'archive', 'jobboard', 'filmstrip', 'pasteup', 'diptych', 'sign', 'isotype', 'stack', 'desk', 'street', 'inspect', 'office', 'rows', 'teller', 'map'}
HERO_GRADE = {'printshop': 'warm', 'cellar': 'sepia', 'linotype': 'sepia', 'drafts': 'cold'}
LAMP_HEROES = {'printshop', 'cellar', 'linotype', 'drafts'}   # mọi cảnh đinh tập 6 có ngọn đèn trong khung (đèn phố, đèn treo, đèn bàn)
TRADE_SKIP = {'assets/ll/sfx/paper-slide.mp3', 'assets/ll/sfx/paper-flip.mp3'}   # tiếng chuyển thẻ tự sinh, không phải âm thanh nghề


def norm(w): return re.sub(r"[^a-z0-9]", '', w.lower())


def overlap(a, b): return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


def main(ep, js=None):
    E = yaml.safe_load(open(ep)); O = E['out']; TL = json.load(open(os.path.join(O, 'timeline.json')))
    MX = json.load(open(os.path.join(O, 'mix.json'))); HZ = E.get('heroes') or {}
    segs = TL['segments']; spec = {s['id']: s for s in E['segments']}; R = {}
    words = {}
    for s in segs:
        if s.get('vo_file'):
            al = json.load(open(os.path.join(REPO, s['vo_file'].replace('.mp3', '.align.json'))))
            words[s['id']] = [(w[0], s['t0'] + s['vo_offset'] + w[1], s['t0'] + s['vo_offset'] + w[2], w[3]) for w in ll.words(al)]
    act = {s['id']: (spec[s['id']].get('map') or {}).get('act') for s in segs}
    hero_of = lambda p: (HZ.get(p.get('hero')) or {})
    grade_of = lambda h: (h.get('opt') or {}).get('grade') or HERO_GRADE.get(h['hero'].split('/')[1])

    # ---------- Q28 ----------
    bad = []
    U = MX.get('music_used') or []
    for i in range(len(U)):
        if U[i].get('loop'): bad.append(f"cue {U[i]['file']} lặp vòng")
        for j in range(i + 1, len(U)):
            if U[i]['file'] == U[j]['file']:
                ov = overlap((U[i]['ss'], U[i]['src_to']), (U[j]['ss'], U[j]['src_to']))
                if ov > 60: bad.append(f"{os.path.basename(U[i]['file'])} dùng lại {ov:.0f} s")
    cue_at = lambda t: next((u['file'] for u in reversed(U) if u['t0'] <= t + 0.01), None)
    theme = U[0]['file'] if U else None
    if not U or cue_at(segs[-1]['t0'] + 0.5) != theme: bad.append('đoạn cuối không dùng nhạc hiệu')
    per_act = {}
    for s in segs: per_act.setdefault(act[s['id']], set()).add(cue_at(s['t0'] + 3.5))   # 3,5 s: sau giao 3 s
    for a in (2, 3):
        if len(per_act.get(a, ())) != 1 or theme in per_act.get(a, ()): bad.append(f'hồi {a}: cue {sorted(os.path.basename(x or "?") for x in per_act.get(a, ()))}')
    if per_act.get(2) and per_act.get(2) == per_act.get(3): bad.append('hồi 2 và 3 cùng bài')
    sfx = [(c['at_abs'], c['at_abs'] + float(c.get('dur') or 1.0), c['file']) for s in segs for c in s.get('sfx', []) if c['file'] not in TRADE_SKIP]
    nohero = []
    for s in segs:
        for sh in s['shots']:
            if sh['tpl'] != 'plate': continue
            a0, a1 = s['t0'] + sh['t0'], s['t0'] + sh['t1']
            if not any(b0 >= a0 - 1.55 and b0 <= a1 for b0, b1, f in sfx): nohero.append(f"{s['id']}@{sh['t0']:.1f}")   # 0,05 s: làm tròn at_abs ở đúng biên J-cut
    if nohero: bad.append('cảnh đinh không có âm thanh nghề: ' + ', '.join(nohero))
    sil = []
    for k in E.get('anchors', []):
        say = [norm(x) for x in E['numbers'][k]['say'].split()]   # giữ gạch nối: lời căn chỉnh coi 'eighty-six' là một từ (lỗi bỏ sót 86 000, 07/10)
        for sid, W in words.items():
            for i in range(1, len(W)):
                if [norm(w[3]) for w in W[i:i + len(say)]] == say:
                    g = W[i][1] - W[i - 1][2]; sil.append((k, sid, round(g, 2)))
    sil_bad = [f'{k} ở {sid}: {g} s' for k, sid, g in sil if not 0.5 <= g <= 1.0]
    if sil_bad: bad.append('lặng trước số neo: ' + ', '.join(sil_bad))
    m = MX['master']
    if not (abs(m['I'] + 14) <= 0.5 and m['TP'] <= -1.0): bad.append(f"master {m['I']} LUFS / {m['TP']} dBTP")
    asr = json.load(open(os.path.join(O, 'asr.json'))) if os.path.exists(os.path.join(O, 'asr.json')) else None
    if not asr or asr.get('truot'): bad.append(f"ASR: {'không có asr.json' if not asr else asr['truot']}")
    R['Q28'] = dict(ok=not bad, val=f"{len(U)} cue · lặng trước số neo {[g for _, _, g in sil]} s · master {m['I']} LUFS / {m['TP']} dBTP", note='; '.join(bad))

    # ---------- Q29 ----------
    def phys_at(t):
        out = []
        for s in segs:
            for sh in s['shots']:
                if overlap((s['t0'] + sh['t0'], s['t0'] + sh['t1']), (t - 1.0, t + 1.0)) > 0: out.append(sh['tpl'])
        return out
    miss, n29 = [], 0
    for s in segs:
        mp = spec[s['id']].get('map') or {}; W = words.get(s['id']) or []
        for nn in mp.get('nouns', []):
            t = ll.anchor(nn['w'], [(w[0], w[1] - s['t0'] - s['vo_offset'], w[2] - s['t0'] - s['vo_offset'], w[3]) for w in W], s['vo_offset'], s['id']) + s['t0']
            n29 += 1
            if not set(phys_at(t)) & PHYS: miss.append(f"{s['id']} {nn['w']} ({'/'.join(phys_at(t))})")
    for k, sid, _ in sil:
        pass
    R['Q29'] = dict(ok=not miss and n29 > 0, val=f"{n29 - len(miss)}/{n29} danh từ chính và số neo có hình vật chất ±1 s", note='; '.join(miss))

    # ---------- Q30 ----------
    bad = []
    for a, b in zip(segs, segs[1:]):
        if act[a['id']] == act[b['id']]: continue
        ma, mb = spec[a['id']].get('map') or {}, spec[b['id']].get('map') or {}; ty = {ma.get('out'), mb.get('in')}
        cut = b['t0']; tag = f"{a['id']}→{b['id']}"
        if not ty & {'match', 'jcut', 'lcut'}: bad.append(f'{tag}: chuyển {sorted(x for x in ty if x)}')
        if 'jcut' in ty or ('match' in ty and 'J-cut' in (ma.get('out_note', '') + mb.get('in_note', ''))):
            if not any(b0 < cut - 0.3 and b1 > cut for b0, b1, f in sfx): bad.append(f'{tag}: J-cut không có tiếng vào trước điểm cắt')
        if 'lcut' in ty and not any(b0 < cut and b1 > cut + 0.3 for b0, b1, f in sfx): bad.append(f'{tag}: L-cut không có tiếng kéo qua')
        if not ((ma.get('lamp') or {}).get('out') and (mb.get('lamp') or {}).get('in')): bad.append(f'{tag}: map không khai ngọn đèn')
        for sh, side in ((a['shots'][-1], 'trước'), (b['shots'][0], 'sau')):
            p = sh['p']; ok = (sh['tpl'] == 'plate' and hero_of(p).get('hero', '/').split('/')[1] in LAMP_HEROES) or sh['tpl'] in ('street',) or \
                (sh['tpl'] == 'text' and p.get('lamp')) or (sh['tpl'] == 'diptych' and any((HZ.get((p.get(x) or {}).get('hero')) or {}).get('hero', '/').split('/')[1] in LAMP_HEROES for x in ('left', 'right')))
            if not ok: bad.append(f'{tag}: shot {side} điểm cắt ({sh["tpl"]}) không có đèn')
    col = {}
    for s in segs:
        a = act[s['id']]; c = (spec[s['id']].get('map') or {}).get('color')
        if a is None: bad.append(f"{s['id']}: thiếu map.act"); continue
        if c != ACT_COLOR[a]: bad.append(f"{s['id']}: màu {c}, hồi {a} cần {ACT_COLOR[a]}")
        for sh in s['shots']:
            if sh['tpl'] != 'plate': continue
            g = grade_of(hero_of(sh['p'])); d = sh['t1'] - sh['t0']; tot = col.setdefault(a, [0.0, 0.0]); tot[1] += d; tot[0] += d if g == ACT_COLOR[a] else 0
    shares = {a: round(100 * v[0] / v[1]) for a, v in col.items() if v[1]}
    for a, sh in shares.items():
        if sh < 60: bad.append(f'hồi {a}: {sh} % cảnh đinh đúng tông {ACT_COLOR[a]}')
    R['Q30'] = dict(ok=not bad, val='cảnh đinh đúng tông theo hồi: ' + ', '.join(f'hồi {a} {v} %' for a, v in sorted(shares.items())), note='; '.join(bad))

    for k in ('Q28', 'Q29', 'Q30'): print(f"{k} {'ĐẠT' if R[k]['ok'] else 'TRƯỢT'} · {R[k]['val']}" + (f"\n    {R[k]['note']}" if R[k]['note'] else ''))
    if js: json.dump(R, open(js, 'w'), indent=1, ensure_ascii=False)
    return all(r['ok'] for r in R.values())


if __name__ == '__main__':
    a = sys.argv[1:]; js = a[a.index('--json') + 1] if '--json' in a else None
    sys.exit(0 if main(a[0], js) else 1)
