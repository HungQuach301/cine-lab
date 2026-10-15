#!/opt/cine/bin/python
"""DÙNG CHUNG · kiểm gói phát hành YouTube của mọi tập (phiên V5a, 15/10/2026). Không sửa bản riêng trong thư mục tập cũ.

  release_check.py <thư mục phat-hanh>  [--title "…"] [--them cap-nhat.txt] [--khong-tai-chinh] [--md ra.md] [--json ra.json]
  release_check.py --self-test

Gói đọc từ thư mục: description*.txt (mô tả), titles.txt (dòng "CHÍNH: …", "DỰ PHÒNG …: …"; dòng LOẠI/không dùng bỏ qua),
nguon-binh-luan-ghim*.txt (bình luận ghim). --them: đoạn cập nhật sẽ dán thêm vào mô tả (vd UPDATE-14-10.txt), chèn ngay sau
dòng miễn trừ để đo độ dài sau khi dán. Mã thoát 1 khi có LỖI.

Mục kiểm (LỖI = chặn đăng; BÁO = in ra để người duyệt xem, không chặn):
  R1 LỖI  tiêu đề (chính và dự phòng Test & Compare) ≤ 60 ký tự (TEARDOWN-FON §6/§9)
  R2 LỖI  mô tả ≤ 5 000 ký tự (giới hạn YouTube); mô tả không chứa '<' hoặc '>' (YouTube từ chối)
  R3 LỖI  dòng 1 của mô tả là câu móc: không trống, không phải câu miễn trừ / "Facts as of" / dòng tiêu đề mục
          BÁO  dòng 1 > 150 ký tự (trang tìm kiếm cắt ngắn), hoặc không có dấu hỏi lẫn con số
  R4 LỖI  câu miễn trừ "…isn't financial or investment advice." nằm trong 3 dòng đầu mô tả, KHÔNG ở dòng 1
          (QUAN-TRI-RUI-RO §4 mục 5, chủ dự án duyệt 15/10 O6/N4; --khong-tai-chinh khi tập không chạm đầu tư/tài chính)
  R5 LỖI  không email trong mô tả, tiêu đề, bình luận ghim (RUNBOOK §3)
  R6 LỖI  nguồn đầy đủ nằm ở tệp bình luận ghim: tệp có, ≥ 1 URL, ≤ 10 000 ký tự (giới hạn bình luận YouTube);
          mô tả không liệt kê > 3 URL nguồn trong mục SOURCES
          BÁO  mô tả không nhắc "pinned comment"; URL nguồn trong mô tả mà không có trong bình luận ghim
  R7 LỖI  chương YouTube: ≥ 3 mốc, mốc đầu 0:00, tăng dần, mỗi chương ≥ 10 s
  R8 BÁO  tiêu đề có emoji, cụm cấm (QUAN-TRI-RUI-RO §1.2: secret, hidden, who really controls…) hoặc từ giật gân (TEARDOWN §6)
"""
import glob, json, os, re, sys

TITLE_MAX, DESC_MAX, PIN_MAX, DISC_LINES = 60, 5000, 10000, 3
EMAIL = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}')
EMAIL_OK = re.compile(r'^(noreply@anthropic\.com|.*@users\.noreply\.github\.com|.*@example\.(com|org|net))$', re.I)
DISC = re.compile(r"(isn[’']t|is not|not) (financial|investment)( or (investment|financial))? advice", re.I)
NOT_HOOK = re.compile(r"^(facts as of\b|chapters\b|sources\b|credits\b|notes\b|this video explains how the system works)", re.I)
URL = re.compile(r'https?://[^\s)\]>"]+')
CHAP = re.compile(r'^\s*((?:\d+:)?\d{1,2}:\d{2})\s+\S')
BANNED = re.compile(r'\b(secret|hidden|who really controls|insane|impossible|shocking|you won[’\']t believe)\b', re.I)
EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]')
SECTION = re.compile(r'^[A-Z][A-Z &/\-]{2,}$')


def secs(t):
    p = [int(x) for x in t.split(':')]; s = 0
    for x in p: s = s * 60 + x
    return s


def read(p): return open(p, encoding='utf-8').read() if p and os.path.exists(p) else None


def first(d, pat):
    c = sorted(glob.glob(os.path.join(d, pat))); return c[0] if c else None


def parse_titles(txt):
    """[(nhãn, tiêu đề)] từ titles.txt; bỏ dòng LOẠI / "không dùng"; bỏ đuôi "(N ký tự)"."""
    out = []
    for l in (txt or '').splitlines():
        if ':' not in l: continue
        lab, t = l.split(':', 1); lab = lab.strip()
        if re.match(r'(?i)^loại', lab) or re.search(r'(?i)không dùng', lab): continue
        t = re.sub(r'\s*\(\d+\s*ký tự\)\s*$', '', t).strip()
        if t: out.append((lab, t))
    return out


def sources_block(lines):
    """các dòng thuộc mục SOURCES của mô tả (tới mục in hoa kế tiếp)."""
    out, on = [], False
    for l in lines:
        s = l.strip()
        if SECTION.match(s): on = s.startswith('SOURCES'); continue
        if on: out.append(l)
    return out


def check(desc, titles, pinned, finance=True):
    E, W = [], []   # (mã, thông điệp)
    # R1, R8 tiêu đề
    if not titles: E.append(('R1', 'không có tiêu đề (titles.txt hoặc --title)'))
    for lab, t in titles:
        n = len(t)
        if n > TITLE_MAX: E.append(('R1', f'tiêu đề {lab} {n} ký tự > {TITLE_MAX}: "{t}"'))
        if EMOJI.search(t): W.append(('R8', f'tiêu đề {lab} có emoji: "{t}"'))
        m = BANNED.search(t)
        if m: W.append(('R8', f'tiêu đề {lab} có cụm cấm/giật gân "{m.group(0)}": "{t}"'))
    if desc is None:
        E.append(('R2', 'không có tệp mô tả (description*.txt)')); return E, W, {}
    lines = desc.splitlines(); n = len(desc)
    info = dict(desc_chars=n, line1=lines[0] if lines else '', titles=[dict(nhan=a, tieu_de=b, ky_tu=len(b)) for a, b in titles])
    # R2
    if n > DESC_MAX: E.append(('R2', f'mô tả {n} ký tự > {DESC_MAX} (thừa {n - DESC_MAX})'))
    if '<' in desc or '>' in desc: E.append(('R2', "mô tả có '<' hoặc '>' (YouTube từ chối mô tả chứa dấu ngoặc nhọn)"))
    # R3 dòng 1 là câu móc
    l1 = lines[0].strip() if lines else ''
    if not l1: E.append(('R3', 'dòng 1 mô tả trống — dòng 1 phải là câu móc'))
    elif DISC.search(l1) or NOT_HOOK.match(l1) or SECTION.match(l1):
        E.append(('R3', f'dòng 1 mô tả không phải câu móc (là câu miễn trừ/dòng mục): "{l1[:120]}"'))
    else:
        if len(l1) > 150: W.append(('R3', f'dòng 1 dài {len(l1)} ký tự > 150 — phần móc có thể bị cắt ở trang tìm kiếm'))
        if '?' not in l1 and not re.search(r'\d', l1): W.append(('R3', 'dòng 1 không có câu hỏi lẫn con số — kiểm lại sức móc'))
    # R4 câu miễn trừ trong 3 dòng đầu (không ở dòng 1)
    if finance:
        hit = [i + 1 for i, l in enumerate(lines[:DISC_LINES]) if DISC.search(l)]
        anywhere = [i + 1 for i, l in enumerate(lines) if DISC.search(l)]
        info['disclaimer_line'] = anywhere[0] if anywhere else None
        if not hit:
            E.append(('R4', f'câu miễn trừ không nằm trong {DISC_LINES} dòng đầu mô tả' + (f' (đang ở dòng {anywhere[0]})' if anywhere else ' (không có)')))
        elif hit == [1]: pass   # đã báo ở R3: dòng 1 dành cho câu móc
    # R5 email
    for where, txt in (('mô tả', desc), ('tiêu đề', '\n'.join(t for _, t in titles)), ('bình luận ghim', pinned or '')):
        for m in set(EMAIL.findall(txt)):
            if not EMAIL_OK.match(m): E.append(('R5', f'email trong {where}: {m}'))
    # R6 nguồn đầy đủ ở bình luận ghim
    src_urls = [u for l in sources_block(lines) for u in URL.findall(l)]
    info['desc_source_urls'] = len(src_urls)
    if pinned is None: E.append(('R6', 'thiếu tệp bình luận ghim (nguon-binh-luan-ghim*.txt) — nguồn đầy đủ phải ở bình luận ghim'))
    else:
        pu = URL.findall(pinned); info.update(pinned_chars=len(pinned), pinned_urls=len(pu))
        if not pu: E.append(('R6', 'bình luận ghim không có URL nguồn nào'))
        if len(pinned) > PIN_MAX: E.append(('R6', f'bình luận ghim {len(pinned)} ký tự > {PIN_MAX} (giới hạn bình luận YouTube) — tách 2 bình luận'))
        miss = [u for u in src_urls if u.rstrip('.,;') not in pinned]
        if miss: W.append(('R6', f'{len(miss)} URL nguồn trong mô tả không có trong bình luận ghim: ' + ', '.join(miss[:3])))
        if not re.search(r'(?i)pinned comment', desc): W.append(('R6', 'mô tả không nhắc "pinned comment" — người xem không biết nguồn đầy đủ ở đâu'))
    if len(src_urls) > 3: E.append(('R6', f'mục SOURCES của mô tả liệt kê {len(src_urls)} URL — nguồn đầy đủ phải chuyển sang bình luận ghim (Kinh thánh §4, 14/10)'))
    # R7 chương
    ch = [(secs(m.group(1)), l.strip()) for l in lines if (m := CHAP.match(l))]
    info['chapters'] = len(ch)
    if ch:
        if len(ch) < 3: E.append(('R7', f'chỉ {len(ch)} mốc chương (< 3, YouTube không hiện chương)'))
        if ch[0][0] != 0: E.append(('R7', f'mốc chương đầu không phải 0:00: "{ch[0][1]}"'))
        for (a, la), (b, lb) in zip(ch, ch[1:]):
            if b <= a: E.append(('R7', f'mốc chương không tăng: "{la}" → "{lb}"'))
            elif b - a < 10: E.append(('R7', f'chương "{la}" dài {b - a} s < 10 s'))
    else: W.append(('R7', 'mô tả không có mốc chương'))
    return E, W, info


def insert_update(desc, upd):
    """chèn đoạn cập nhật ngay dưới dòng miễn trừ/"Facts as of" (cách ghi chú UPDATE của Steel, D8); không có thì sau dòng 1."""
    L = desc.splitlines(); k = next((i for i, l in enumerate(L) if DISC.search(l) or re.search(r'(?i)facts as of', l)), 0)
    return '\n'.join(L[:k + 1] + [upd.strip()] + L[k + 1:]) + ('\n' if desc.endswith('\n') else '')


def run(d, title=None, finance=True, them=None):
    desc = read(first(d, 'description*.txt'))
    if desc is not None and them: desc = insert_update(desc, read(them) or '')
    titles = [('--title', title)] if title else parse_titles(read(os.path.join(d, 'titles.txt')))
    pinned = read(first(d, 'nguon-binh-luan-ghim*.txt'))
    E, W, info = check(desc, titles, pinned, finance)
    return dict(goi=os.path.relpath(d), ket_qua='ĐẠT' if not E else 'TRƯỢT', loi=[dict(ma=a, chi_tiet=b) for a, b in E],
                bao=[dict(ma=a, chi_tiet=b) for a, b in W], so_do=info)


def to_md(r):
    o = [f"### Gói `{r['goi']}` — **{r['ket_qua']}** ({len(r['loi'])} LỖI, {len(r['bao'])} BÁO)", '',
         f"- Mô tả: {r['so_do'].get('desc_chars', '—')} ký tự; chương: {r['so_do'].get('chapters', '—')}; "
         f"URL nguồn trong mô tả: {r['so_do'].get('desc_source_urls', '—')}; bình luận ghim: {str(r['so_do']['pinned_chars']) + ' ký tự' if 'pinned_chars' in r['so_do'] else 'KHÔNG CÓ'}"]
    for t in r['so_do'].get('titles', []): o.append(f"- Tiêu đề {t['nhan']}: {t['ky_tu']} ký tự — \"{t['tieu_de']}\"")
    o += [f"- **LỖI {x['ma']}** {x['chi_tiet']}" for x in r['loi']] + [f"- BÁO {x['ma']} {x['chi_tiet']}" for x in r['bao']]
    return '\n'.join(o) + '\n'


def self_test():
    good = ("Why does a rock with no farmland outrank its neighbour by 3 to 1?\n\nThis video explains how the system works. "
            "It isn't financial or investment advice. Facts as of 1 October 2026.\n\nCHAPTERS\n0:00 The question\n0:40 The fence\n2:10 The answer\n\n"
            "SOURCES\nAll sources are listed in the pinned comment.\n")
    pin = "SOURCES\n- A: https://example.org/a\n"; T = [('CHÍNH', 'Why Gibraltar Got Rich')]
    cases = [('đủ', good, T, pin, set()),
             ('tiêu đề 61', good, [('CHÍNH', 'W' * 61)], pin, {'R1'}),
             ('mô tả 5001', good + 'x' * (5001 - len(good)), T, pin, {'R2'}),
             ('ngoặc nhọn', good + '<b>\n', T, pin, {'R2'}),
             ('miễn trừ dòng 1', good.split('\n\n', 1)[1], T, pin, {'R3'}),
             ('miễn trừ dòng 5', good.replace("\n\nThis video", "\n\n\n\n\nThis video"), T, pin, {'R4'}),
             ('email', good + 'contact: nobody' + '@' + 'mail.test\n', T, pin, {'R5'}),   # địa chỉ giả (.test dành riêng), ghép chuỗi để preflight P1 không coi là email thật
             ('thiếu ghim', good, T, None, {'R6'}),
             ('nguồn trong mô tả', good + ''.join(f'- s{i}: https://e.org/{i}\n' for i in range(5)), T, pin, {'R6'}),
             ('chương 5 s', good.replace('0:40', '0:05'), T, pin, {'R7'}),
             ('không tài chính', good.replace("It isn't financial or investment advice. ", ''), T, pin, {'R4'})]
    bad = 0
    for name, d, t, p, want in cases:
        got = {a for a, _ in check(d, t, p)[0]}
        ok = got == want; bad += not ok
        print(('ĐẠT ' if ok else 'SAI ') + f'{name}: muốn {sorted(want)} được {sorted(got)}')
    got = {a for a, _ in check(good.replace("It isn't financial or investment advice. ", ''), T, pin, finance=False)[0]}
    print(('ĐẠT ' if not got else 'SAI ') + f'--khong-tai-chinh bỏ R4: {sorted(got)}'); bad += bool(got)
    print(f'self-test: {len(cases) + 1 - bad}/{len(cases) + 1}'); return bad == 0


def main():
    a = sys.argv[1:]
    if '--self-test' in a: sys.exit(0 if self_test() else 1)
    if not a or a[0].startswith('-'): print(__doc__); sys.exit(2)
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    r = run(a[0], opt('--title'), '--khong-tai-chinh' not in a, opt('--them'))
    if opt('--them'): r['them'] = opt('--them')
    md = to_md(r); print(md)
    if opt('--md'): open(opt('--md'), 'w', encoding='utf-8').write(md)
    if opt('--json'): json.dump(r, open(opt('--json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sys.exit(1 if r['loi'] else 0)


if __name__ == '__main__':
    main()
