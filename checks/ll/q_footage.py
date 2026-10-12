#!/opt/cine/bin/python
"""Q32 footage/ảnh nguồn ngoài — luật khoá LL v3 bản 1.10.0 (phiên K, 12/10/2026). Áp cho Last Lamplighters VÀ kênh 2.
Định nghĩa: checks/ll/RULES-LL.md (mục Q32) và checks/ll/FOOTAGE.md (nguồn, giấy phép Pexels/Pixabay đọc lại 12/10/2026).

  q_footage.py <episode.yaml> [--tl <timeline.json>] [--desc <mô tả YouTube>] [--json ra.json]
      LL:    reports/m3/epXX/episode.yaml        → sổ reports/m3/epXX/SOURCES-FOOTAGE.csv
      kênh 2: channel-k2/<tập>/episode.yaml       → sổ channel-k2/<tập>/SOURCES-FOOTAGE.csv
      (sổ luôn nằm CẠNH episode.yaml; mô tả mặc định: <thư mục tập>/phat-hanh/*description*.txt)

Đoạn footage trong EDL (timeline): shot `tpl: footage` hoặc shot bất kỳ có `p.clip` (= clip_id của sổ). Tham số shot:
  p.clip     clip_id (bắt buộc)          p.file     đường dẫn file đã dùng khi render (ngoài repo); không khai thì tìm
  p.setting  bối cảnh theo nội dung hình  <clip_id>.* trong /var/tmp/k2-footage/<id>/, /var/tmp/ll-footage/<id>/, <out>/footage/
Sổ (UTF-8, dấu phẩy), đúng 10 cột:
  clip_id,url_trang,url_tai,ngay_tai_utc,giay_phep,yeu_cau_ghi_cong,sha256,timecode_dung,nguoi_nhan_dien,logo
TRƯỢT khi:
  (a) đoạn footage không có dòng sổ; sổ sai định dạng (cột, URL, ngày ISO 8601 UTC, SHA 64 hex, giấy phép ngoài danh sách hoặc có NC/ND,
      nguồn ngoài danh sách cho phép, giấy phép không hợp nguồn, Wikimedia không trỏ trang File:); SHA-256 file đã dùng ≠ sổ hoặc không thấy
      file; timecode_dung (phim chính) không khớp các đoạn dùng trong EDL (hai chiều, dung sai 0,05 s)
  (b) footage + ảnh tư liệu (`archive`) + (1.10.1, Q34d) shot khai type photo/document/footage > 40 % thời lượng tập (từng Short tính riêng); một clip hiện liên tục > 8 s (shot cùng clip kề nhau gộp lại)
  (c) giấy phép CC BY / CC BY-SA mà yeu_cau_ghi_cong trống hoặc câu ghi công không có nguyên văn trong mô tả (bỏ khác biệt khoảng trắng, hoa/thường)
  (d) logo rõ nét (logo=co, không ghi làm mờ/cắt) hoặc người nhận diện được (nguoi_nhan_dien=co, không ghi làm mờ/cắt) trong ngữ cảnh tiêu cực:
      lời đọc trong [đầu clip − 1 s, cuối clip + 1 s] hoặc chú thích của shot có từ thuộc danh sách NEG; Pixabay có logo rõ nét: luôn TRƯỢT
      (giấy phép Pixabay cấm dùng thương mại nội dung có nhãn hiệu nhận ra được)
  (e) cây git (mọi tệp đang theo dõi) có tệp media trong đường dẫn có "footage", hoặc tệp có SHA-256 trùng một dòng của bất kỳ sổ SOURCES-FOOTAGE.csv nào
  (f) đoạn footage không khai `p.setting` (Q26b đếm footage là bối cảnh theo nội dung hình: checks/ll/q_setting.py)
Trong ±5 % quanh ngưỡng 40 % và 8 s: nêu tên (sát ngưỡng).
"""
import csv, glob, hashlib, json, os, re, subprocess, sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base  # noqa: E402

COLS = ['clip_id', 'url_trang', 'url_tai', 'ngay_tai_utc', 'giay_phep', 'yeu_cau_ghi_cong', 'sha256', 'timecode_dung', 'nguoi_nhan_dien', 'logo']
SO = 'SOURCES-FOOTAGE.csv'
MAX_SHARE = 40.0          # % thời lượng
MAX_CLIP = 8.0            # s liên tục mỗi clip
TOL = 0.05                # s, dung sai timecode sổ ↔ EDL
GAP = 1 / 24 + 0.001      # shot cùng clip cách nhau ≤ 1 khung: một lần hiện liên tục
CTX = 1.0                 # s quanh clip để đọc ngữ cảnh lời
ROOTS = ('/var/tmp/k2-footage/{id}', '/var/tmp/ll-footage/{id}', '{out}/footage')

# nguồn cho phép (chủ dự án 12/10/2026). Nguồn khác: chủ dự án duyệt, ghi AUTHORSHIP.md, rồi K thêm vào DUYET_THEM (không ai khác sửa).
SRC = (('loc', r'(^|\.)loc\.gov$'), ('nara', r'(^|\.)archives\.gov$'), ('nasa', r'(^|\.)nasa\.gov$'), ('ia', r'(^|\.)archive\.org$'),
       ('wikimedia', r'^commons\.wikimedia\.org$'), ('pexels', r'(^|\.)pexels\.com$'), ('pixabay', r'(^|\.)pixabay\.com$'))
DUYET_THEM = {}           # {host: nhãn nguồn} — trống ở 1.10.0
LIC_OK = {'loc': {'PD', 'CC0'}, 'nara': {'PD', 'CC0'}, 'nasa': {'PD', 'CC0'}, 'ia': {'PD', 'CC0', 'CC BY', 'CC BY-SA'},
          'wikimedia': {'PD', 'CC0', 'CC BY', 'CC BY-SA'}, 'pexels': {'Pexels'}, 'pixabay': {'Pixabay'}}
MEDIA = re.compile(r'\.(jpe?g|png|tiff?|gif|webp|bmp|heic|mp4|mov|mkv|webm|avi|m4v|mxf|mpe?g|ogv|ts|mts|m2ts|prores)$', re.I)
HANDLED = re.compile(r'làm mờ|lam mo|\bmờ\b|blur|pixel|cắt|\bcat\b|crop|che |không nhận ra|khong nhan ra', re.I)
NEG = re.compile(r"^(crime|crimes|criminal|criminals|fraud|frauds|fraudulent|scam|scams|scammer|swindle|swindled|theft|thief|thieves|steal|stole|"
                 r"stolen|robbery|robbed|arrest|arrested|prison|jail|jailed|convict|convicted|indicted|guilty|lawsuit|sued|bankrupt|bankruptcy|"
                 r"insolvent|foreclosure|foreclosed|addict|addicts|addiction|drug|drugs|overdose|scandal|corrupt|corruption|bribe|bribes|bribery|"
                 r"abuse|abused|cheat|cheated|cheating|liar|lied|fail|fails|failed|failing|failure|failures|homeless|disease|diseased|dead|death|"
                 r"deaths|died|killed|murder|murdered|violence|violent|riot|riots|racist|racism|greed|greedy|crook|crooks|villain|victim|victims|"
                 r"poverty|layoff|layoffs|fired|evicted|eviction)$")


def _sha(p, cache=None):
    st = os.stat(p); k = f'{os.path.abspath(p)}|{st.st_size}|{st.st_mtime_ns}'
    if cache is not None and k in cache: return cache[k]
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    if cache is not None: cache[k] = h.hexdigest()
    return h.hexdigest()


def mmss(t): return f'{int(t // 60)}:{t % 60:05.2f}'


def parse_tc(x):
    """'m:ss.xx' | 'h:mm:ss.xx' (phần sau dấu chấm = phần thập phân giây) | 'hh:mm:ss:ff' (SMPTE, 24 khung/s) → giây"""
    x = x.strip(); p = x.split(':')
    if not all(re.fullmatch(r'\d+(\.\d+)?', q) for q in p): raise ValueError(x)
    if len(p) == 4: return int(p[0]) * 3600 + int(p[1]) * 60 + int(p[2]) + int(p[3]) / 24
    if len(p) == 3: return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2])
    if len(p) == 2: return int(p[0]) * 60 + float(p[1])
    raise ValueError(x)


def lic_class(s):
    s = (s or '').strip(); u = s.upper()
    if re.search(r'(^|[\s/-])(NC|ND)([\s/-]|$)|NONCOMMERCIAL|NO ?DERIV', u): return 'NC/ND'
    for k, rx in (('CC BY-SA', r'^CC[ -]BY[ -]SA\b'), ('CC BY', r'^CC[ -]BY\b'), ('CC0', r'^CC0\b|^CC ZERO'), ('PD', r'^PD\b|^PUBLIC DOMAIN'),
                  ('Pexels', r'^PEXELS'), ('Pixabay', r'^PIXABAY')):
        if re.search(rx, u): return k
    return None


def yes(v):
    t = (v or '').strip().lower()
    m = re.match(r'(có|co|không|khong)\b', t)
    return None if not m else m.group(1) in ('có', 'co')


def source_of(url):
    h = (urlparse(url or '').hostname or '').lower()
    for k, rx in SRC:
        if re.search(rx, h): return k
    return DUYET_THEM.get(h)


def load_so(path):
    """→ (dict clip_id → dòng, [lỗi định dạng])"""
    if not os.path.exists(path): return {}, []
    with open(path, encoding='utf-8-sig', newline='') as f:
        rd = csv.DictReader(f); hdr = [h.strip() for h in (rd.fieldnames or [])]
        if hdr != COLS: return {}, [f'{os.path.basename(path)}: tiêu đề cột {hdr} ≠ {COLS}']
        rows = [{k.strip(): (v or '').strip() for k, v in r.items() if k} for r in rd]
    R, bad = {}, []
    for i, r in enumerate(rows, 2):
        cid = r['clip_id']; ctx = f'sổ dòng {i} ({cid or "?"})'
        if not re.fullmatch(r'[A-Za-z0-9][\w.-]*', cid): bad.append(f'{ctx}: clip_id rỗng hoặc sai ký tự'); continue
        if cid in R: bad.append(f'{ctx}: clip_id trùng'); continue
        R[cid] = r; src = source_of(r['url_trang']); lic = lic_class(r['giay_phep']); r['_src'], r['_lic'] = src, lic
        for c in ('url_trang', 'url_tai'):
            if not re.match(r'https?://[^\s/]+\.[^\s/]+/?\S*$', r[c]): bad.append(f'{ctx}: {c} không phải URL')
        if src is None: bad.append(f'{ctx}: nguồn {urlparse(r["url_trang"]).hostname} ngoài danh sách cho phép (cần chủ dự án duyệt)')
        if src == 'wikimedia' and '/wiki/File:' not in r['url_trang']: bad.append(f'{ctx}: Wikimedia phải trỏ trang File: của đúng tệp (kiểm giấy phép từng file)')
        if not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d(\.\d+)?)?Z', r['ngay_tai_utc']): bad.append(f'{ctx}: ngay_tai_utc không phải ISO 8601 UTC (…Z)')
        if lic == 'NC/ND': bad.append(f'{ctx}: giấy phép NC/ND bị cấm')
        elif lic is None: bad.append(f'{ctx}: giấy phép "{r["giay_phep"]}" ngoài PD/CC0/CC BY/CC BY-SA/Pexels/Pixabay')
        elif src and lic not in LIC_OK.get(src, {'PD', 'CC0', 'CC BY', 'CC BY-SA', 'Pexels', 'Pixabay'}): bad.append(f'{ctx}: giấy phép {lic} không hợp nguồn {src}')
        if not re.fullmatch(r'[0-9a-f]{64}', r['sha256'].lower()): bad.append(f'{ctx}: sha256 không phải 64 hex')
        r['sha256'] = r['sha256'].lower()
        for c in ('nguoi_nhan_dien', 'logo'):
            if yes(r[c]) is None: bad.append(f'{ctx}: {c} phải bắt đầu bằng co|khong')
        r['_tc'] = []
        for part in [x for x in r['timecode_dung'].split(';') if x.strip()]:
            try:
                a, b = re.split(r'\s*[-–]\s*(?=\d)', part.strip(), maxsplit=1); a, b = parse_tc(a), parse_tc(b)
                if b <= a: raise ValueError
                r['_tc'].append((a, b))
            except ValueError: bad.append(f'{ctx}: timecode_dung "{part.strip()}" sai dạng (m:ss.xx-m:ss.xx)')
    return R, bad


def uses(TL):
    """→ [(video, t0, t1, shot)]; video = 'main' hoặc id Short; thời gian tuyệt đối trong video đó"""
    out = []
    for s in TL['segments']:
        for sh in s['shots']:
            if sh.get('tpl') == 'footage' or (sh.get('p') or {}).get('clip'): out.append(('main', s['t0'] + sh['t0'], s['t0'] + sh['t1'], sh, s['id']))
    for s in TL.get('shorts') or []:
        for sh in s['shots']:
            if sh.get('tpl') == 'footage' or (sh.get('p') or {}).get('clip'): out.append((s['id'], sh['t0'], sh['t1'], sh, s['id']))
    return out


def runs(U):
    """gộp shot cùng clip kề nhau (≤ 1 khung) → [(video, clip, đầu, cuối)]"""
    R = []
    for v, a, b, sh, _ in sorted(U, key=lambda z: (z[0], z[1])):
        c = (sh.get('p') or {}).get('clip')
        if R and R[-1][0] == v and R[-1][1] == c and a - R[-1][3] <= GAP: R[-1][3] = max(R[-1][3], b)
        else: R.append([v, c, a, b])
    return [tuple(r) for r in R]


def find_file(E, sh):
    p = (sh.get('p') or {}); f = p.get('file')
    if f: return f if os.path.isabs(f) else os.path.join(base.REPO, f)
    for r in ROOTS:
        g = sorted(glob.glob(os.path.join(r.format(id=E.get('id', ''), out=E.get('out', '')), glob.escape(p.get('clip') or '') + '.*')))
        if g: return g[0]
    return None


def desc_text(ep_dir, desc):
    fs = [desc] if desc else sorted(glob.glob(os.path.join(ep_dir, 'phat-hanh', '*description*.txt')))
    fs = [f for f in fs if f and os.path.exists(f)]
    return (' '.join(open(f, encoding='utf-8').read() for f in fs), fs)


def _sq(s): return re.sub(r'\s+', ' ', s or '').strip().lower()


def context_words(TL, v, a, b, sh, FW):
    W = []
    if v == 'main':
        for L in FW.values(): W += [w for w, t0, t1, *_ in L if t1 >= a - CTX and t0 <= b + CTX]
    for c in (sh.get('p') or {}).get('cap') or []:
        W += [base.norm(x).strip("'") for x in re.split(r'[\s\-–—]+', c.get('s', '') if isinstance(c, dict) else str(c))]
    return sorted({w for w in W if NEG.match(w or '')})


def git_scan(repo, so_paths=(), extra_sha=(), cache=None):
    """(e) → [lỗi]. Quét mọi tệp git đang theo dõi (chỉ mục + HEAD)"""
    r = subprocess.run(['git', '-C', repo, 'ls-files', '-z'], capture_output=True)
    if r.returncode: return [f'không đọc được cây git ở {repo}']
    files = [x for x in r.stdout.decode('utf-8', 'replace').split('\0') if x]
    bad = [f'tệp media nguồn ngoài trong git: {f}' for f in files if MEDIA.search(f) and re.search(r'(^|/)[^/]*footage[^/]*/', f, re.I)]
    shas = set(extra_sha)
    for f in [x for x in files if x.endswith(SO)] + list(so_paths):
        p = f if os.path.isabs(f) else os.path.join(repo, f)
        if os.path.exists(p): shas |= {r_['sha256'] for r_ in load_so(p)[0].values() if re.fullmatch(r'[0-9a-f]{64}', r_['sha256'])}
    if shas:
        for f in files:
            p = os.path.join(repo, f)
            if os.path.isfile(p) and not os.path.islink(p) and os.path.getsize(p) > 0 and _sha(p, cache) in shas:
                bad.append(f'tệp trùng SHA-256 một clip trong sổ (media nguồn ngoài bị commit): {f}')
    return sorted(set(bad))


def _cache_path(): return os.path.join(os.environ.get('Q32_CACHE_DIR', '/var/tmp/cine-out'), 'q32-sha-cache.json')


def q32(E, TL, ep_dir, desc=None, repo=None, scan=True):
    from checks.ll import q_av
    so_path = os.path.join(ep_dir, SO); R, fmt = load_so(so_path)
    U = uses(TL); P = {k: [] for k in 'abcdef'}; near = []
    P['a'] += fmt
    # (a) mọi đoạn có dòng sổ; SHA file đã dùng; timecode hai chiều (phim chính)
    seen = {}
    for v, a, b, sh, sid in U:
        c = (sh.get('p') or {}).get('clip'); w = f'{v if v != "main" else sid} @{mmss(a)}'
        if not c: P['a'].append(f'{w}: shot footage không khai p.clip'); continue
        if c not in R: P['a'].append(f'{w}: clip {c} không có dòng trong {SO}'); continue
        f = find_file(E, sh)
        if not f or not os.path.exists(f): P['a'].append(f'{w}: không thấy file đã dùng của clip {c} (p.file hoặc {ROOTS[0]}/<clip_id>.*): không kiểm được SHA')
        elif (f, c) not in seen:
            seen[(f, c)] = _sha(f)
            if seen[(f, c)] != R[c]['sha256']: P['a'].append(f'{w}: SHA-256 file {os.path.basename(f)} = {seen[(f, c)][:12]}… ≠ sổ {R[c]["sha256"][:12]}…')
    RN = runs(U)
    for c, r in R.items():
        mine = [(a, b) for v, cc, a, b in RN if v == 'main' and cc == c]
        for a, b in mine:
            if not any(abs(a - x) <= TOL and abs(b - y) <= TOL for x, y in r['_tc']): P['a'].append(f'clip {c} dùng {mmss(a)}–{mmss(b)} không có trong timecode_dung của sổ')
        for x, y in r['_tc']:
            if not any(abs(a - x) <= TOL and abs(b - y) <= TOL for a, b in mine): P['a'].append(f'clip {c}: timecode_dung {mmss(x)}–{mmss(y)} không khớp đoạn nào trong EDL')
    # (b) trần thời lượng
    vids = {'main': float(TL['tong_s'])} | {s['id']: float(s['t1'] - s['t0']) for s in TL.get('shorts') or []}
    shares = {}
    for v, T in vids.items():
        segs = TL['segments'] if v == 'main' else [s for s in TL['shorts'] if s['id'] == v]
        arch = sum(sh['t1'] - sh['t0'] for s in segs for sh in s['shots'] if sh.get('tpl') == 'archive' and not (sh.get('p') or {}).get('clip'))
        ft = sum(b - a for vv, a, b, *_ in U if vv == v)
        if v == 'main':                                  # 1.10.1 (Q34d): shot khai type photo/document/footage trong đặc tả cộng vào trần
            from checks.ll import q_types
            arch += q_types.ext_seconds(E, TL)
        if not T or not (ft + arch): continue
        sh_ = 100 * (ft + arch) / T; shares[v] = (sh_, ft, arch)
        nm = 'phim' if v == 'main' else f'Short {v}'
        if sh_ > MAX_SHARE: P['b'].append(f'{nm}: footage {ft:.1f} s + tư liệu/ảnh/báo {arch:.1f} s = {sh_:.1f} % > {MAX_SHARE:g} %')
        elif abs(sh_ - MAX_SHARE) <= 0.05 * MAX_SHARE: near.append(f'{nm}: nguồn ngoài {sh_:.1f} % (ngưỡng {MAX_SHARE:g} %)')
    for v, c, a, b in RN:
        d = b - a; nm = '' if v == 'main' else f'Short {v} '
        if d > MAX_CLIP + 1e-6: P['b'].append(f'{nm}clip {c} liên tục {d:.2f} s ({mmss(a)}–{mmss(b)}) > {MAX_CLIP:g} s')
        elif abs(d - MAX_CLIP) <= 0.05 * MAX_CLIP: near.append(f'{nm}clip {c} {d:.2f} s (ngưỡng {MAX_CLIP:g} s)')
    # (c) ghi công
    used = {(sh.get('p') or {}).get('clip') for *_, sh, _s in U} & set(R)
    need = [c for c in sorted(used) if R[c]['_lic'] in ('CC BY', 'CC BY-SA')]
    if need:
        txt, fs = desc_text(ep_dir, desc); T_ = _sq(txt)
        for c in need:
            at = R[c]['yeu_cau_ghi_cong']
            if not at: P['c'].append(f'clip {c} ({R[c]["_lic"]}): yeu_cau_ghi_cong trống')
            elif not fs: P['c'].append(f'clip {c} ({R[c]["_lic"]}): không có mô tả YouTube (phat-hanh/*description*.txt) để kiểm ghi công')
            elif _sq(at) not in T_: P['c'].append(f'clip {c} ({R[c]["_lic"]}): mô tả thiếu câu ghi công "{at}"')
    # (d) logo / người nhận diện được trong ngữ cảnh xấu
    FW = None
    for v, a, b, sh, sid in U:
        c = (sh.get('p') or {}).get('clip'); r = R.get(c)
        if not r: continue
        per = yes(r['nguoi_nhan_dien']) and not HANDLED.search(r['nguoi_nhan_dien'])
        logo = yes(r['logo']) and not HANDLED.search(r['logo'])
        if logo and r['_src'] == 'pixabay': P['d'].append(f'clip {c} @{mmss(a)}: Pixabay có logo/nhãn hiệu rõ nét (giấy phép cấm dùng thương mại)')
        if not (per or logo): continue
        if FW is None:
            try: FW = q_av.flat_words(TL)
            except (OSError, KeyError, ValueError) as e: FW = {}; P['d'].append(f'không đọc được lời (.align.json) để kiểm ngữ cảnh: {e}')
        neg = context_words(TL, v, a, b, sh, FW)
        if neg: P['d'].append(f'clip {c} @{mmss(a)}: {"người nhận diện được" if per else ""}{" + " if per and logo else ""}{"logo rõ nét" if logo else ""} cạnh lời/chữ tiêu cực: {", ".join(neg)}')
    # (e) cây git
    if scan:
        cp = _cache_path(); cache = {}
        try: cache = json.load(open(cp))
        except (OSError, ValueError): pass
        P['e'] = git_scan(repo or base.REPO, [so_path], {r['sha256'] for r in R.values() if re.fullmatch(r'[0-9a-f]{64}', r['sha256'])}, cache)
        try: os.makedirs(os.path.dirname(cp), exist_ok=True); json.dump(cache, open(cp, 'w'))
        except OSError: pass
    # (f) bối cảnh theo nội dung hình
    for v, a, b, sh, sid in U:
        if not str((sh.get('p') or {}).get('setting') or '').strip():
            P['f'].append(f'{v if v != "main" else sid} @{mmss(a)} clip {(sh.get("p") or {}).get("clip")}: không khai p.setting (bối cảnh theo nội dung hình, Q26b)')
    loi = [f'({k}) {x}' for k in 'abcdef' for x in P[k]]
    m = shares.get('main', (0.0, 0.0, 0.0)); lmax = max([b - a for v, c, a, b in RN] or [0.0])
    val = (f'{len(U)} đoạn footage · {len(used)} clip · sổ {len(R)} dòng · nguồn ngoài phim {m[0]:.1f} % (footage {m[1]:.1f} s + tư liệu/ảnh/báo {m[2]:.1f} s)'
           f' · clip dài nhất {lmax:.2f} s' if U or R or shares.get('main') else 'không dùng footage ngoài' + (' · sổ sai định dạng' if fmt else ''))
    return dict(ok=not loi, loi=loi, muc=P, sat_nguong=near, note='; '.join(loi[:6]), val=val, so=so_path if os.path.exists(so_path) else None)


if __name__ == '__main__':
    a = sys.argv[1:]; E = base.load(a[0]); ep_dir = os.path.dirname(os.path.abspath(a[0]))
    tl = a[a.index('--tl') + 1] if '--tl' in a else os.path.join(E['out'], 'timeline.json')
    r = q32(E, json.load(open(tl)), ep_dir, desc=a[a.index('--desc') + 1] if '--desc' in a else None)
    print('Q32 ' + ('ĐẠT' if r['ok'] else 'TRƯỢT') + ' · ' + r['val'] + ''.join('\n  ' + x for x in r['loi'])
          + ('\n  sát ngưỡng: ' + '; '.join(r['sat_nguong']) if r['sat_nguong'] else ''))
    if '--json' in a: json.dump(r, open(a[a.index('--json') + 1], 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if r['ok'] else 1)
