#!/opt/cine/bin/python
"""K-R1…K-R9 luật tập "ĐỎ-K" (ĐỎ có kiểm soát) — bản 1.14.0 (phiên K, 17/10/2026). Mặc định CHỈ BÁO trong k2check (cấp: cap112.py).
Căn cứ: reports/NC-LICH-SU-2-BAO-CAO.md §5.3 (K-R1…K-R9), §5.2 (G1-R); channel-k2/QUAN-TRI-RUI-RO.md hàng ĐỎ-K (chủ dự án duyệt XX1–XX2,
YY5–YY6 ngày 17/10). Định nghĩa: checks/ll/RULES-LL.md mục "1.14".

  q_dok.py <episode.yaml> [--tl timeline.json] [--logs <thư mục *.log.json>] [--hang-doi HANG-DOI.md] [--json ra.json]

BẬT chỉ khi episode.yaml khai `rui_ro: do-k` (nhận ĐỎ-K / do_k); không khai → mọi hàng KHÔNG ÁP.
Đầu vào: khối `do_k:` của episode.yaml (đường dẫn tương đối thư mục episode):
  tu_cam [tệp]        tu-cam-chung.txt + tu-cam-<tập>.txt: mỗi dòng một cụm (không phân biệt hoa thường, nhận số nhiều -s/-es); `re:` = regex; `#` = chú thích
  srt, mo_ta, the     phụ đề .en.srt, mô tả (description.en.txt), thẻ; tiêu đề = `do_k.tieu_de` hoặc `title`
  claims              claims.json ({claims: [...]} hoặc danh sách): `khoang` [thấp, cao] hoặc nguồn có `truyen_thong` (claim.truyen_thong
                      hoặc nguon: [{ten, truyen_thong}])
  tai_san             [{id, bieu_tuong: khong|co_lich_su|ton_giao|cuc_doan, the: [...], dung_o: ["seg/i", …]}]
  bieu_tuong_khung    [{f (khung phim 24 fps), id, pct}] — diện tích tài sản trong khung (mặt nạ theo id, hero_pct mở rộng)
  thumbnail           [{id, the: [...], chu: "chữ trên thumbnail"}]
  cham_mu             cham-mu-nhay-cam.json {vai: [{vai, co: [...], diem}]}
  binh_luan_ghim      tệp bình luận ghim
  truyen_thong        {tên truyền thống: [tên nguồn/tác giả xuất hiện trong mô tả]}
  khai                g1r-khai.yaml: [{ma, noi_dung (≥ 20 ký tự), nguoi_ky, vai: chu_du_an, ngay: YYYY-MM-DD, ket_luan: dong_y|dat}]
  thu_tu              vị trí trong HANG-DOI.md (vd T7); không khai → tìm id tập trong cột "Tập"
KIỂM BẰNG MÁY được thì kiểm; phần máy không thấy (nội dung hình sau thẻ tự khai, thao tác trên Studio) → MỤC KHAI bắt buộc có chữ ký chủ dự án
ở G1-R (KHAI_BAT_BUOC; thêm `K-R2.do` khi có cờ lịch sử mà không có bieu_tuong_khung, `K-R3.khong_ranh` thay cho manifest lớp khi tập có bản đồ
mà không vẽ ranh). Thiếu mục khai → THIẾU (không ĐẠT).
K-R1 Từ cấm: 0 lần trong lời (srt; không có → vo đặc tả), chữ trên hình (log chữ), tiêu đề, mô tả, thẻ, chữ thumbnail.
K-R2 Biểu tượng: (a) tài sản thiếu/sai bieu_tuong; (b) cuc_doan/ton_giao: 0 khung (và không dung_o); (c) co_lich_su ≤ FLAG_PCT % khung,
     ≤ FLAG_S s/lần, ≤ FLAG_N lần/tập.
K-R3 Biên giới hiện đại: mọi lớp bản đồ có `loai`; bien_gioi_lich_su có nam + nguon; bien_gioi_hien_dai ∩ (NE disputed ⊕ 10 km) = ∅ (= BD-5 (a)).
K-R4 Thương vong: mọi câu lời có số + từ chết/thương vong phải chứa một số `numbers` có claim, claim có `khoang` hoặc ≥ 2 truyền thống.
K-R5 Hình bạo lực: tài sản thẻ nguoi_bi_thuong / thi_the / vu_khi_chia_nguoi: 0 khung, không dung_o.
K-R6 Thumbnail: không thẻ cờ/ton_giao/cuc_doan/vũ khí chĩa người/lửa có người; chữ qua K-R1; mọi số trong chữ có trong claims/numbers.
K-R7 Nhịp (HANG-DOI.md, bảng "Thứ tự … Mức" đầu tiên): (a) mọi cửa sổ 4 tập liền chứa tập này ≤ 1 ĐỎ-K; (b) tập liền trước/sau ≠ VÀNG
     (chưa xếp → THIẾU); (c) không ở T3–T5; (d) HANG-DOI ghi mức tập này là ĐỎ-K.
K-R8 Chấm mù 3 góc: ≥ 3 vai, mỗi vai 0 cờ, điểm ≥ BLIND_MIN/5.
K-R9 Mô tả + bình luận ghim: (a) mô tả có "as of"; (b) ≥ 2 truyền thống có nguồn trong mô tả; (c) có tệp bình luận ghim; (d) khai K-R9.tu_chan.
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

FLAG_PCT, FLAG_S, FLAG_N, BLIND_MIN, BLIND_ROLES = 2.0, 3.0, 3, 4.0, 3
BT = {'khong', 'co_lich_su', 'ton_giao', 'cuc_doan'}
VIOLENT = {'nguoi_bi_thuong', 'thi_the', 'vu_khi_chia_nguoi'}
THUMB_BAD = {'co', 'co_lich_su', 'ton_giao', 'cuc_doan', 'vu_khi_chia_nguoi', 'lua_co_nguoi'}
KHAI_BAT_BUOC = {'K-R2.the': 'mọi tài sản hiện trên hình đã gắn bieu_tuong/the đúng (máy chỉ đọc thẻ tự khai)',
                 'K-R5.the': 'không tài sản nào có người bị thương, thi thể, vũ khí chĩa người mà thiếu thẻ',
                 'K-R6.the': 'thẻ thumbnail đầy đủ (cờ, tôn giáo, cực đoan, vũ khí, lửa có người)',
                 'K-R9.tu_chan': 'danh sách từ chặn đã nạp vào YouTube Studio (chủ dự án xác nhận)'}
DEATH = re.compile(r"\b(kill(?:ed|ing|s)?|dead|deaths?|died|dying|casualt(?:y|ies)|victims?|wounded|injured|perish(?:ed)?|fatalit(?:y|ies)|death toll|toll|lives|bodies)\b", re.I)
NUMW = r"(?:\d[\d,.]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundreds?|thousands?|millions?|dozens?)"
NUM = re.compile(r'\b' + NUMW + r'\b', re.I)
LVL = {'đỏ-k': 'DO-K', 'do-k': 'DO-K', 'vàng': 'VANG', 'vang': 'VANG', 'xanh': 'XANH', 'đỏ': 'DO'}


def r(ok, loi=None, thieu=None, val='', **kw):
    loi = loi or []; thieu = thieu or []
    if thieu and not loi and 'ket_qua' not in kw: kw['ket_qua'] = 'THIẾU'
    return dict(ok=ok and not loi and not thieu, loi=loi, thieu=thieu, val=val, note='; '.join((loi + thieu)[:5]), **kw)


def la_do_k(E): return re.sub(r'[\s_]+', '-', str(E.get('rui_ro') or '').strip().lower()).replace('đỏ', 'do') == 'do-k'


def _p(base, x): return None if not x else (x if os.path.isabs(x) else os.path.join(base, x))


def _read(base, x):
    p = _p(base, x)
    return open(p, encoding='utf-8').read() if p and os.path.exists(p) else None


def _json(base, x):
    if isinstance(x, (list, dict)): return x
    p = _p(base, x)
    if not p or not os.path.exists(p): return None
    if p.endswith(('.yaml', '.yml')):
        import yaml
        return yaml.safe_load(open(p, encoding='utf-8'))
    return json.load(open(p, encoding='utf-8'))


# ================================================================ K-R1
def word_list(base, files):
    pats, miss = [], []
    for f in files or []:
        t = _read(base, f)
        if t is None: miss.append(str(f)); continue
        for ln in t.splitlines():
            ln = ln.strip()
            if not ln or ln.startswith('#'): continue
            if ln.startswith('re:'): pats.append((ln, re.compile(ln[3:].strip(), re.I)))
            else:
                w = r'\s+'.join(re.escape(x) for x in ln.split())
                pats.append((ln, re.compile(r'(?<!\w)' + w + r'(?:s|es)?(?!\w)', re.I)))
    return pats, miss


def srt_text(t):
    return [ln for ln in (t or '').splitlines() if ln.strip() and not ln.strip().isdigit() and '-->' not in ln]


def texts(E, TL, base, logdir):
    D = E.get('do_k') or {}; out = []
    s = _read(base, D.get('srt'))
    if s is not None: out += [('lời (srt)', x) for x in srt_text(s)]
    else: out += [(f"lời đoạn {g.get('id')}", str(g.get('vo') or '')) for g in E.get('segments') or [] if isinstance(g, dict)]
    out.append(('tiêu đề', str(D.get('tieu_de') or E.get('title') or '')))
    m = _read(base, D.get('mo_ta'))
    if m: out += [('mô tả', x) for x in m.splitlines()]
    out += [('thẻ', str(x)) for x in D.get('the') or []]
    if logdir:
        import glob
        for f in glob.glob(os.path.join(logdir, '*.log.json')):
            try: J = json.load(open(f))
            except (OSError, ValueError): continue
            for e in J.get('text') or []:
                out += [(f"chữ trên hình {J.get('id')} khung {e.get('f')}", str(i.get('s', ''))) for i in e.get('items') or []]
    else:   # không log: chữ khai trong đặc tả (tags/where/cap/src)
        for sg in (TL or {}).get('segments') or []:
            for i, sh in enumerate(sg.get('shots') or []):
                p = sh.get('p') or {}
                for k in ('where', 'src', 'asof'):
                    if isinstance(p.get(k), str): out.append((f"chữ đặc tả {sg['id']}/{i}", p[k]))
                for x in (p.get('tags') or []) + (p.get('cap') or []):
                    if isinstance(x, dict):
                        out += [(f"chữ đặc tả {sg['id']}/{i}", str(x[k])) for k in ('s', 'sub', 'text', 'src') if isinstance(x.get(k), str)]
    for t in _json(base, D.get('thumbnail')) or []:
        if isinstance(t, dict) and t.get('chu'): out.append((f"thumbnail {t.get('id')}", str(t['chu'])))
    return out


def kr1(E, TL, base, logdir):
    D = E.get('do_k') or {}; pats, miss = word_list(base, D.get('tu_cam'))
    th = [f'không đọc được danh sách từ cấm {m}' for m in miss] + ([] if D.get('tu_cam') else ['chưa khai do_k.tu_cam (tu-cam-chung.txt + tu-cam-<tập>.txt)'])
    if not pats and not th: th.append('danh sách từ cấm rỗng')
    T = texts(E, TL, base, logdir); loi = []
    for where, s in T:
        for ln, rx in pats:
            m = rx.search(s)
            if m: loi.append(f'{where}: "{m.group(0)}" (mục "{ln}") trong "{s[:60]}"')
    th += [] if _read(base, D.get('srt')) is not None else ['không có phụ đề .en.srt (do_k.srt) — kiểm lời theo vo đặc tả']
    return r(True, loi, [x for x in th if 'phụ đề' not in x], val=f'{len(pats)} mục từ cấm · {len(T)} dòng chữ/lời · {len(loi)} lần', ghi_chu=[x for x in th if 'phụ đề' in x])


# ================================================================ K-R2 / K-R5
def _assets(base, D): return [a for a in _json(base, D.get('tai_san')) or [] if isinstance(a, dict)]


def _runs(fr, ids, thr=0.0, fps=24):
    """khung (f, pct) của tài sản ids với pct > thr → [(t0, t1, max pct)]"""
    F = sorted({int(x['f']): max(float(x.get('pct') or 0), 0) for x in fr if str(x.get('id')) in ids and float(x.get('pct') or 0) > thr}.items())
    R = []
    for f, p in F:
        if R and f - R[-1][1] <= 1: R[-1][1] = f; R[-1][2] = max(R[-1][2], p)
        else: R.append([f, f, p])
    return [(a / fps, (b + 1) / fps, p) for a, b, p in R]


def kr2(E, base):
    D = E.get('do_k') or {}; A = _assets(base, D); fr = _json(base, D.get('bieu_tuong_khung')); loi, th, need = [], [], []
    if D.get('tai_san') is None: th.append('chưa khai do_k.tai_san (manifest tài sản có thẻ bieu_tuong)')
    for a in A:
        if str(a.get('bieu_tuong')) not in BT: loi.append(f"(a) tài sản {a.get('id')}: bieu_tuong = {a.get('bieu_tuong')!r} ngoài {{{', '.join(sorted(BT))}}}")
    bad = {str(a['id']) for a in A if a.get('bieu_tuong') in ('cuc_doan', 'ton_giao')}; flag = {str(a['id']) for a in A if a.get('bieu_tuong') == 'co_lich_su'}
    for a in A:
        if str(a.get('id')) in bad and a.get('dung_o'): loi.append(f"(b) tài sản {a['id']} ({a['bieu_tuong']}) dùng ở {', '.join(map(str, a['dung_o'][:4]))}")
    if fr is not None:
        for t0, t1, p in _runs(fr, bad): loi.append(f'(b) cuc_doan/ton_giao hiện {t0:.2f}–{t1:.2f} s ({p:.1f} % khung)')
        R = _runs(fr, flag)
        big = [x for x in fr if str(x.get('id')) in flag and float(x.get('pct') or 0) > FLAG_PCT]
        if big: loi.append(f"(c) co_lich_su > {FLAG_PCT:g} % khung ở {len(big)} khung (lớn nhất {max(float(x['pct']) for x in big):.1f} %)")
        loi += [f'(c) co_lich_su hiện liền {t1 - t0:.2f} s > {FLAG_S:g} s ({t0:.2f}–{t1:.2f} s)' for t0, t1, _ in R if t1 - t0 > FLAG_S + 1e-6]
        if len(R) > FLAG_N: loi.append(f'(c) co_lich_su {len(R)} lần > {FLAG_N}/tập')
    elif flag and any(a.get('dung_o') for a in A if str(a.get('id')) in flag): need.append('K-R2.do')
    elif bad or flag: th.append('không có bieu_tuong_khung — chỉ kiểm dung_o')
    return r(True, loi, th, val=f"{len(A)} tài sản · cuc_doan/ton_giao {len(bad)} · co_lich_su {len(flag)} · khung đo: {'có' if fr is not None else 'không'}"), need + ['K-R2.the']


def kr5(E, base):
    D = E.get('do_k') or {}; A = _assets(base, D); fr = _json(base, D.get('bieu_tuong_khung')) or []; loi = []
    v = {str(a['id']) for a in A if set(a.get('the') or []) & VIOLENT}
    for a in A:
        if str(a.get('id')) in v and a.get('dung_o'): loi.append(f"tài sản {a['id']} ({'/'.join(sorted(set(a['the']) & VIOLENT))}) dùng ở {', '.join(map(str, a['dung_o'][:4]))}")
    loi += [f'tài sản bạo lực hiện {t0:.2f}–{t1:.2f} s' for t0, t1, _ in _runs(fr, v)]
    return r(True, loi, [] if D.get('tai_san') is not None else ['chưa khai do_k.tai_san'], val=f'{len(A)} tài sản · thẻ bạo lực {len(v)}'), ['K-R5.the']


# ================================================================ K-R3
def kr3(E, TL, base):
    from checks.ll import q_bando
    C = q_bando.cfg_of(E, base); LOP = (C['lop'] or {}).get('lop') or []; loi = []; need = []
    S = q_bando._shots(E, TL) if TL else []
    maps = [z for z in S if z['ty'] in ('map', 'strategic') or str(z['scene']).startswith(('relief/', 'map/'))]
    if not LOP:
        if maps: need.append('K-R3.khong_ranh')
        return r(True, [], [], val=f'không có manifest lớp · {len(maps)} shot bản đồ' + (' → cần khai K-R3.khong_ranh' if maps else '')), need
    for Ly in LOP:
        lid = Ly.get('id') or '?'
        if not Ly.get('loai'): loi.append(f'lớp {lid}: thiếu loai')
        elif Ly['loai'] == 'bien_gioi_lich_su' and (Ly.get('nam') is None or not Ly.get('nguon')): loi.append(f'lớp {lid}: bien_gioi_lich_su thiếu nam/nguon')
        if Ly.get('loai') == 'bien_gioi_hien_dai':
            rg = [x for f in Ly['_features'] for x in q_bando._rings(f.get('geometry'))]
            loi += [f'lớp {lid}: giao vùng tranh chấp NE "{t}" ({d:g} km ≤ {q_bando.DISP_KM:g} km)' for t, d in q_bando.line_vs_disputed(rg)]
    return r(True, loi, [], val=f"{len(LOP)} lớp · hiện đại {sum(1 for x in LOP if x.get('loai') == 'bien_gioi_hien_dai')}"), need


# ================================================================ K-R4
def _claims(base, D):
    c = _json(base, D.get('claims'))
    return None if c is None else {str(x.get('id')): x for x in (c.get('claims') if isinstance(c, dict) else c) or [] if isinstance(x, dict)}


def claim_ok(c):
    k = c.get('khoang') or c.get('range')
    if isinstance(k, list) and len(k) == 2 and all(isinstance(v, (int, float)) for v in k) and k[0] < k[1]: return True, f"khoảng {k[0]:g}–{k[1]:g}"
    tt = set(c.get('truyen_thong') or []) if isinstance(c.get('truyen_thong'), list) else set()
    tt |= {str(n.get('truyen_thong')) for n in c.get('nguon') or [] if isinstance(c.get('nguon'), list) and isinstance(n, dict) and n.get('truyen_thong')}
    return (len(tt) >= 2), f"{len(tt)} truyền thống"


def sentences(E, base):
    D = E.get('do_k') or {}; s = _read(base, D.get('srt'))
    txt = ' '.join(srt_text(s)) if s is not None else ' '.join(str(g.get('vo') or '') for g in E.get('segments') or [] if isinstance(g, dict))
    return [x.strip() for x in re.split(r'(?<=[.!?])\s+', txt) if x.strip()]


def kr4(E, base):
    D = E.get('do_k') or {}; CL = _claims(base, D); N = E.get('numbers') or {}; loi, n = [], 0
    if CL is None: return r(True, [], ['chưa khai do_k.claims (claims.json)'], val='—')
    for s in sentences(E, base):
        if not (DEATH.search(s) and NUM.search(s)): continue
        n += 1
        cand = [(k, v) for k, v in N.items() if isinstance(v, dict) and any(str(v.get(f) or '').strip() and str(v[f]).strip().lower() in s.lower() for f in ('text', 'say'))]
        ok = []
        for k, v in cand:
            ids = v.get('claims') or ([v['claim']] if v.get('claim') else [])
            for c in ids:
                good, why = claim_ok(CL.get(str(c)) or {})
                if good: ok.append(f'{k}→{c} ({why})')
        if not ok: loi.append(f'"{s[:90]}": số thương vong không nối claim có khoảng hoặc ≥ 2 truyền thống' + (f" (số khai: {', '.join(k for k, _ in cand)})" if cand else ''))
    return r(True, loi, [], val=f'{n} câu có số + từ chết/thương vong · không nối {len(loi)}')


# ================================================================ K-R6
def kr6(E, base):
    D = E.get('do_k') or {}; TH = _json(base, D.get('thumbnail')); loi = []
    if TH is None: return r(True, [], ['chưa khai do_k.thumbnail'], val='—'), ['K-R6.the']
    pats, _ = word_list(base, D.get('tu_cam')); CL = _claims(base, D) or {}; N = E.get('numbers') or {}
    known = ' '.join(json.dumps(c, ensure_ascii=False) for c in CL.values()) + ' ' + ' '.join(str(v.get('text') or '') for v in N.values() if isinstance(v, dict))
    known_n = {re.sub(r'[,\s]', '', x) for x in re.findall(r'\d[\d,.]*', known)}
    for t in TH:
        tid = t.get('id') or '?'; bad = set(t.get('the') or []) & THUMB_BAD
        if bad: loi.append(f"thumbnail {tid}: thẻ {', '.join(sorted(bad))}")
        chu = str(t.get('chu') or '')
        loi += [f'thumbnail {tid}: từ cấm "{rx.search(chu).group(0)}"' for ln, rx in pats if rx.search(chu)]
        for x in re.findall(r'\d[\d,.]*', chu):
            if re.sub(r'[,\s]', '', x).rstrip('.') not in {k.rstrip('.') for k in known_n}: loi.append(f'thumbnail {tid}: số "{x}" không có trong claims/numbers')
    return r(True, loi, [], val=f'{len(TH)} thumbnail'), ['K-R6.the']


# ================================================================ K-R7
def hang_doi(path):
    """bảng "Thứ tự … Mức" đầu tiên → {n: (mức, tập, đề tài)}"""
    t = open(path, encoding='utf-8').read().splitlines(); out = {}; hdr = None
    for ln in t:
        if not ln.strip().startswith('|'):
            if out: break
            hdr = None; continue
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if hdr is None:
            if any('Thứ tự' in x for x in c) and any(x.strip('* ') == 'Mức' for x in c): hdr = c
            continue
        if set(''.join(c)) <= set('-: '): continue
        m = re.fullmatch(r'\**T(\d+)\**', c[0])
        if not m: continue
        get = lambda name: next((c[i] for i, h in enumerate(hdr) if h.strip('* ') == name and i < len(c)), '')
        out[int(m.group(1))] = (_lvl(get('Mức')), get('Tập'), get('Đề tài (tên làm việc)') or get('Đề tài'))
    return out


def _lvl(s):
    s = re.sub(r'[*]', '', s).strip().lower(); ks = [v for k, v in LVL.items() if k in s]
    return 'DO-K' if 'DO-K' in ks else (ks[0] if ks else (s.upper() or '—'))


def kr7(E, path):
    if not path or not os.path.exists(path): return r(True, [], [f'không đọc được HANG-DOI.md ({path})'], val='—')
    H = hang_doi(path); tt = str(E.get('thu_tu') or '').strip().upper(); n = int(tt[1:]) if re.fullmatch(r'T\d+', tt) else None
    if n is None:
        hit = [k for k, v in H.items() if E.get('id') and str(E['id']).lower() in v[1].lower()]
        n = hit[0] if len(hit) == 1 else None
    if n is None: return r(True, [], ['không xác định vị trí tập trong HANG-DOI (khai thu_tu: T<n>)'], val=f'{len(H)} hàng')
    loi, th = [], []
    lv = lambda k: 'DO-K' if k == n else (H[k][0] if k in H else None)
    if n in H and H[n][0] != 'DO-K': loi.append(f'(d) HANG-DOI ghi T{n} mức {H[n][0]} ≠ ĐỎ-K')
    if 3 <= n <= 5: loi.append(f'(c) T{n} nằm trong T3–T5')
    for s in range(n - 3, n + 1):
        w = [k for k in range(s, s + 4) if k >= 1]; dk = [k for k in w if lv(k) == 'DO-K']
        if len(dk) > 1: loi.append(f"(a) cửa sổ T{w[0]}–T{w[-1]}: {len(dk)} ĐỎ-K ({', '.join(f'T{k}' for k in dk)})")
    for k in (n - 1, n + 1):
        if k < 1: continue
        if lv(k) is None: th.append(f'(b) T{k} chưa xếp trong HANG-DOI — không xác nhận được "liền trước/sau ≠ VÀNG"')
        elif lv(k) == 'VANG': loi.append(f'(b) T{k} liền {"trước" if k < n else "sau"} là VÀNG')
    return r(True, loi, th, val=f"T{n} · T{n - 1}: {lv(n - 1) or 'chưa xếp'} · T{n + 1}: {lv(n + 1) or 'chưa xếp'} · ĐỎ-K trong HANG-DOI: "
                                + (', '.join(f'T{k}' for k, v in sorted(H.items()) if v[0] == 'DO-K') or '—'))


# ================================================================ K-R8 / K-R9
def kr8(E, base):
    D = E.get('do_k') or {}; J = _json(base, D.get('cham_mu') or 'cham-mu-nhay-cam.json')
    if J is None: return r(True, [], ['không có cham-mu-nhay-cam.json'], val='—')
    V = J.get('vai') if isinstance(J, dict) else J; V = [v for v in V or [] if isinstance(v, dict)]; loi = []
    if len({str(v.get('vai')) for v in V}) < BLIND_ROLES: loi.append(f'{len(V)} vai < {BLIND_ROLES}')
    for v in V:
        co = v.get('co') or []; d = v.get('diem')
        if (len(co) if isinstance(co, list) else int(co or 0)) > 0: loi.append(f"vai {v.get('vai')}: {len(co) if isinstance(co, list) else co} cờ")
        if not isinstance(d, (int, float)) or d < BLIND_MIN: loi.append(f"vai {v.get('vai')}: điểm {d} < {BLIND_MIN:g}/5")
    return r(True, loi, [], val=f"{len(V)} vai · điểm {', '.join(str(v.get('diem')) for v in V)}", sat_nguong=[f"vai {v.get('vai')} điểm {v['diem']} (ngưỡng {BLIND_MIN:g})" for v in V if isinstance(v.get('diem'), (int, float)) and abs(v['diem'] - BLIND_MIN) <= 0.05 * BLIND_MIN])


def kr9(E, base):
    D = E.get('do_k') or {}; m = _read(base, D.get('mo_ta')); loi, th = [], []
    if m is None: return r(True, [], ['không có mô tả (do_k.mo_ta)'], val='—'), ['K-R9.tu_chan']
    if not re.search(r'\bas of\b', m, re.I): loi.append('(a) mô tả không có "as of"')
    TT = D.get('truyen_thong') or {}
    if not TT: th.append('(b) chưa khai do_k.truyen_thong — không đếm được truyền thống')
    else:
        co = [k for k, v in TT.items() if any(str(x).lower() in m.lower() for x in v or [])]
        if len(co) < 2: loi.append(f"(b) mô tả có nguồn của {len(co)} truyền thống ({', '.join(co) or '—'}) < 2")
    g = _read(base, D.get('binh_luan_ghim'))
    if not (g or '').strip(): loi.append('(c) không có tệp bình luận ghim (do_k.binh_luan_ghim)')
    return r(True, loi, th, val=f'mô tả {len(m)} ký tự · truyền thống khai {len(TT)}'), ['K-R9.tu_chan']


# ================================================================ khai G1-R
def khai_check(base, D, need):
    K = _json(base, D.get('khai')) or []; K = K.get('khai') if isinstance(K, dict) else K; got = {}; bad = []
    for k in K or []:
        if not isinstance(k, dict): continue
        p = []
        if len(str(k.get('noi_dung') or '').strip()) < 20: p.append('noi_dung < 20 ký tự')
        nk = str(k.get('nguoi_ky') or '').strip()
        if not nk: p.append('thiếu nguoi_ky')
        elif '@' in nk: p.append('nguoi_ky chứa email (che email: ghi tên/vai)')
        if str(k.get('vai') or '') != 'chu_du_an': p.append('vai ≠ chu_du_an')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(k.get('ngay') or '')): p.append('ngay không dạng YYYY-MM-DD')
        if str(k.get('ket_luan') or '').lower() not in ('dong_y', 'đồng ý', 'dat', 'đạt'): p.append('ket_luan ≠ dong_y/dat')
        (bad.append(f"khai {k.get('ma')}: {', '.join(p)}") if p else got.__setitem__(str(k.get('ma')), k))
    miss = [m for m in dict.fromkeys(need) if m not in got]
    return got, bad, miss


def check(E, TL=None, ep_dir='.', logdir=None, hang_doi_path=None):
    NAMES = ['K-R1', 'K-R2', 'K-R3', 'K-R4', 'K-R5', 'K-R6', 'K-R7', 'K-R8', 'K-R9']
    if not la_do_k(E): return {k: dict(ok=True, loi=[], thieu=[], val='tập không khai rui_ro: do-k', ket_qua='KHÔNG ÁP') for k in NAMES}
    from checks.ll import base as B
    D = E.get('do_k') or {}; need = {}
    R = {'K-R1': kr1(E, TL, ep_dir, logdir)}
    R['K-R2'], need['K-R2'] = kr2(E, ep_dir)
    R['K-R3'], need['K-R3'] = kr3(E, TL, ep_dir)
    R['K-R4'] = kr4(E, ep_dir)
    R['K-R5'], need['K-R5'] = kr5(E, ep_dir)
    R['K-R6'], need['K-R6'] = kr6(E, ep_dir)
    R['K-R7'] = kr7(E, hang_doi_path or _p(ep_dir, D.get('hang_doi')) or os.path.join(B.REPO, 'channel-k2', 'HANG-DOI.md'))
    R['K-R8'] = kr8(E, ep_dir)
    R['K-R9'], need['K-R9'] = kr9(E, ep_dir)
    got, bad, _ = khai_check(ep_dir, D, [m for v in need.values() for m in v])
    for k, ms in need.items():
        x = R[k]; miss = [m for m in ms if m not in got]
        x['thieu'] = x['thieu'] + [f"mục khai {m} chưa có chữ ký chủ dự án ở G1-R ({KHAI_BAT_BUOC.get(m, 'phần máy không kiểm được')})" for m in miss]
        x['loi'] = x['loi'] + [b for b in bad if any(b.startswith(f'khai {m}:') for m in ms)]
        x['khai'] = {m: ('đã ký ' + str(got[m].get('ngay'))) if m in got else 'THIẾU' for m in ms}
        R[k] = r(True, x['loi'], x['thieu'], val=x['val'] + (' · khai: ' + ', '.join(f'{m} {v}' for m, v in x['khai'].items()) if ms else ''), **{q: v for q, v in x.items() if q not in ('ok', 'loi', 'thieu', 'val', 'note', 'ket_qua')})
    return R


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    from checks.ll import base
    E = base.load(a[0]); E['_path'] = os.path.abspath(a[0]); tp = g('tl') or os.path.join(E['out'], 'timeline.json')
    R = check(E, json.load(open(tp)) if os.path.exists(tp) else None, os.path.dirname(os.path.abspath(a[0])), g('logs'), g('hang-doi'))
    for k, v in R.items():
        kq = v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')
        print(f"{k} {kq} · {v['val']}" + ''.join('\n  ' + x for x in (v['loi'] + v['thieu'])[:20]))
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
