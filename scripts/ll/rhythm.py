#!/opt/cine/bin/python
"""Last Lamplighters · luật nhịp Q14–Q18 (chủ dự án, 05/10/2026, "HẤP DẪN & GIỮ CHÂN"). Đo trên timeline (sau prep) — không cần render.

  rhythm.py <episode.yaml>          in bảng đo; mã thoát 1 nếu trượt (dùng trong qc.py và trước render)

Q14 móc câu: trước 0:15 có câu hỏi/mâu thuẫn bằng lời (câu có "?" hoặc but/yet…) VÀ hình (shot đồ hoạ hoặc dòng chữ) bắt đầu trước 0:15;
    thẻ tựa phim (shot `text` có `lamp: true`) bắt đầu ≤ 0:20; câu hỏi mở đầu được trả lời ở cuối: `hook.answer` (đoạn) chứa mọi từ trong `hook.keys`.
Q15 đổi hình: sự kiện hình = đầu shot, mọi mốc nội dung (at/noteAt/…/beats/lines/bars), mốc máy quay (cam), đèn thắp, đèn tắt, màn hình;
    không quãng nào > 8 s không có sự kiện; trung bình ≤ 6 s.
Q16 tỷ lệ thẻ giấy (mẫu đồ hoạ, không tính cảnh toàn khung) ≤ 55 % (tập 4–5), ≤ 40 % từ tập 6 (`rhythm.paper_max` trong đặc tả).
Q17 mật độ số: số MỚI trên hình (khoá `num` phân biệt + nhãn số trên đường) ≤ 2/phút trung bình; đặc tả khai `anchors` = đúng 3 số neo, có xuất hiện trên hình.
Q18 thẻ trống: shot số liệu (bars/line/compare/bignum) phải có số đầu tiên ≤ 1,5 s sau đầu shot.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); import ll

FULL = {'street', 'office', 'rows', 'endcard', 'teller', 'isotype', 'stack', 'sign', 'desk', 'archive', 'inspect', 'plate', 'jobboard', 'filmstrip', 'pasteup', 'diptych'}   # v2 (05/10/2026): cảnh toàn khung
DATA = {'bars', 'line', 'compare', 'bignum'}
CONTENT_KEYS = ('at', 'noteAt', 'midAt', 'diffAt', 'capAt')


def _ats(x, acc):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == 'cam' and isinstance(v, list): acc += [c['t'] for c in v if isinstance(c.get('t'), (int, float))]
            elif k in CONTENT_KEYS + ('lit', 'screen', 'look', 'estimate') and isinstance(v, (int, float)): acc.append(float(v))
            elif k in ('dim', 'walk', 'flash') and isinstance(v, list): acc += [float(a) for a in v if isinstance(a, (int, float))]
            else: _ats(v, acc)
    elif isinstance(x, list):
        for v in x: _ats(v, acc)
    return acc


def _first_data(sh):
    p = sh['p']; c = []
    if sh['tpl'] == 'bignum': c.append(p.get('at', sh['t0'] + 0.8))
    if sh['tpl'] == 'line': c.append(p.get('at', sh['t0'] + 0.8))
    if sh['tpl'] == 'bars': c += [b.get('at', sh['t0']) for b in p.get('bars', [])]
    if sh['tpl'] == 'compare': c += [p.get(s, {}).get('at', sh['t0']) for s in ('left', 'right')]
    return min(c) if c else sh['t0']


def measure(E, TL):
    out = {}
    T = TL['tong_s']; segs = TL['segments']
    # Q14
    W = []
    for s in segs:
        if s.get('vo_file'):
            al = json.load(open(os.path.join(ll.REPO, s['vo_file'].replace('.mp3', '.align.json'))))
            W += [(w[3], s['t0'] + s['vo_offset'] + w[1]) for w in ll.words(al)]
    early = ' '.join(w for w, t in W if t < 15)
    q_word = bool(re.search(r'\?|\b(but|yet|didn\'t|did not|never)\b', early, re.I))
    gfx = [s['t0'] + sh['t0'] for s in segs for sh in s['shots'] if sh['tpl'] not in FULL]
    gfx += [s['t0'] + c['at'] for s in segs for sh in s['shots'] for c in sh['p'].get('cap', []) if isinstance(c.get('at'), (int, float))]   # chú thích đè lên cảnh cũng là hình
    q_img = any(t < 15 for t in gfx)
    title = [s['t0'] + sh['t0'] for s in segs for sh in s['shots'] if sh['tpl'] == 'text' and sh['p'].get('lamp')]
    t_title = min(title) if title else None
    hk = E.get('hook') or {}
    ans = next((x for x in E['segments'] if x['id'] == hk.get('answer')), None)
    keys = [ll.norm(k) for k in hk.get('keys', [])]
    ans_ok = bool(ans and keys and all(k in [ll.norm(w) for w in (ans.get('vo') or '').split()] for k in keys))
    out['Q14'] = dict(ok=q_word and q_img and t_title is not None and t_title <= 20 and ans_ok,
                      val=f"câu hỏi<0:15 {'có' if q_word else 'KHÔNG'} · hình<0:15 {'có' if q_img else 'KHÔNG'} · tựa {t_title if t_title is None else round(t_title, 1)} s · trả lời ở {hk.get('answer')} {'có' if ans_ok else 'KHÔNG'}")
    # Q15
    ev = [0.0, T]
    for s in segs:
        ev.append(s['t0'])
        for sh in s['shots']:
            ev.append(s['t0'] + sh['t0']); ev += [s['t0'] + a for a in _ats(sh['p'], []) if sh['t0'] - 0.01 <= a <= sh['t1']]
    ev = sorted(set(round(e, 2) for e in ev if 0 <= e <= T))
    gaps = [(b - a, a) for a, b in zip(ev, ev[1:])]
    mx = max(gaps); mean = T / max(1, len(ev) - 1)
    seg_at = lambda t: next((x['id'] for x in segs if x['t0'] <= t < x['t1']), '?')
    long = [f"{seg_at(a)} {int(a // 60)}:{a % 60:04.1f} ({g:.1f} s)" for g, a in sorted(gaps, reverse=True) if g > 8]
    out['Q15'] = dict(ok=mx[0] <= 8 and mean <= 6, val=f"dài nhất {mx[0]:.1f} s · TB {mean:.1f} s", note='; '.join(long[:6]))
    # Q16
    paper = sum(sh['t1'] - sh['t0'] for s in segs for sh in s['shots'] if sh['tpl'] not in FULL)
    pm = float((E.get('rhythm') or {}).get('paper_max', 55))
    out['Q16'] = dict(ok=100 * paper / T <= pm, val=f"{100 * paper / T:.1f} % (trần {pm:.0f} %)")
    # Q17
    seen, shown = set(), []
    for s in segs:
        for sh in s['shots']:
            for k in ll.nums_in(sh['p'], []) + [n['num'] for n in sh['p'].get('nums', []) if isinstance(n, dict) and 'num' in n]:
                tx = (E['numbers'].get(k) or {}).get('text', k)
                if k not in seen: seen.add(k); seen.add(f'line:{tx}')
                if f'#{tx}' not in seen: seen.add(f'#{tx}'); shown.append(k)
            for se in sh['p'].get('series', []):
                for i in se.get('labels', []):
                    lt = (se.get('ltext') or [''] * 99)[i] if se.get('ltext') and i < len(se['ltext']) else ''
                    key = f"line:{lt or se['points'][i][1]}"
                    if re.search(r'\d', key) and key not in seen and f"#{key[5:]}" not in seen: seen.add(key); seen.add(f"#{key[5:]}"); shown.append(key)
    per_min = len(shown) / (T / 60)
    A = E.get('anchors') or []
    a_ok = len(A) == 3 and all(a in seen for a in A)
    out['Q17'] = dict(ok=per_min <= 2 and a_ok, val=f"{len(shown)} số / {T / 60:.1f} phút = {per_min:.2f}/phút · neo {A if A else 'CHƯA KHAI'}{'' if a_ok else ' TRƯỢT'}")
    # Q18
    bad = []
    for s in segs:
        for sh in s['shots']:
            if sh['tpl'] in DATA:
                d = _first_data(sh) - sh['t0']
                if d > 1.5: bad.append(f"{s['id']}/{sh['tpl']}@{sh['t0']:.1f} ({d:.1f} s)")
    out['Q18'] = dict(ok=not bad, val=len(bad), note='; '.join(bad[:6]))
    return out


if __name__ == '__main__':
    E = ll.load(sys.argv[1]); TL = json.load(open(os.path.join(E['out'], 'timeline.json')))
    R = measure(E, TL)
    for k, r in R.items(): print(f"{k} {'ĐẠT' if r['ok'] else 'TRƯỢT'} · {r['val']} {('· ' + r['note']) if r.get('note') else ''}")
    sys.exit(0 if all(r['ok'] for r in R.values()) else 1)
