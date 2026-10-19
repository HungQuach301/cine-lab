#!/opt/cine/bin/python
"""K-LAI-1…K-LAI-6 + K-LAI-B khung neo LAI "A + C có kiểm soát" — bản 1.15.0 (phiên K, 18/10/2026). Mặc định CHỈ BÁO trong k2check (cấp: cap112.py).
Căn cứ: reports/pt2/PT2-BAO-CAO.md §9 Q-PT2-2 (6 luật K đề xuất), §5 (định dạng kiem-du-kien.json), §2.2 (sổ goi-api.jsonl), §2.6 (nhãn + log khung)
— nhánh pt2-lai; chủ dự án duyệt P2-2 ngày 18/10 (trần 20 %, mức Chặn 1–6; P2-3 bão hoà ≤ 0,40 mức Cảnh báo). Định nghĩa: RULES-LL.md mục "1.15".

  q_lai.py <episode.yaml> [--tl timeline.json] [--logs <thư mục *.log.json>] [--json ra.json]

BẬT khi episode.yaml có khối `lai:` hoặc một shot khai `ai_image`/`ai_texture`/`lai: true`; không có → mọi hàng KHÔNG ÁP. Khối `lai:` (đường dẫn
tương đối thư mục episode):
  log_khung     log MỌI khung (jsonl hoặc JSON list; một tệp hoặc danh sách): {f (khung phim), ai_image, ai_texture?, nhan_phuong_phap, shot?, dem?}
  log_chu       log chữ theo khung phim [{f, text|items: [{s, role?, px1080 | cap, box? [x0, y0, x1, y1]}]}] (định dạng bo-tl); không có thì
                đọc --logs (k2.js `<đoạn>.log.json`, f trong đoạn → cộng t0 đoạn của timeline)
  W, H          cỡ khung của box trong log chữ (mặc định 1920 × 1080)
  kiem_du_kien  kiem-du-kien.json (PT2 §5): khung_neo {<tên>: {tam_C_dung, loi_chac_cuoi, nghi_van_con_lai, ngoai_le_cho_duyet?, duoc_dung,
                ngoai_le_duyet?}}, tong {nghi_van_cuoi*?}, cach_kiem, bang_chung
  duyet         tệp duyệt ngoại lệ (yaml/json): [{ma: <id ngoại lệ>, khung_neo?, nguoi_ky, vai: chu_du_an, ngay: YYYY-MM-DD, ket_luan: chap_nhan}]
  goi_api       goi-api.jsonl (PT2 §2.2): mỗi lệnh {anh, khung_neo, moc?, lan_thu, ai_image, model_req, model_resp, prompt, mask.pct_duoc_sua,
                usage, usd, c2pa, date_utc, input.pass, http, file, sha256}
  bao_ve        [{lai: PNG, a: PNG, mat_na: PNG (trắng = vùng bảo vệ), bat_buoc?: PNG (trời/cờ/tàu/mốc/ô cửa/đèn — phải ⊂ mat_na)}]
                khung LAI và A-thuần CÙNG khung, KHÔNG chữ
  dem           [{lai, a}] khung đêm LAI và A cùng khung, không chữ
  khung_lai     thư mục khung LAI không chữ (*.png|*.jpg) — K-LAI-B
  tong_s        thời lượng phim khi không có timeline (mặc định: timeline.tong_s → tổng dur đặc tả)
K-LAI-1 Thời lượng: tổng giây khung `ai_image` hoặc `ai_texture` ≤ AI_MAX (20 %) thời lượng tập. Log phải phủ MỌI khung của phim (thiếu → THIẾU).
K-LAI-2 Nhãn: mọi khung của shot có khung AI (không khai shot → của quãng AI liền) có `nhan_phuong_phap: true`; log chữ trong các quãng đó có dòng
        LABEL (log k2.js cắt 40 ký tự: nhận tiền tố) ≥ LABEL_PX px @1080 ở MỌI mẫu, box góc dưới trái (x0 ≤ 10 % W, y0 ≥ 66 % H).
K-LAI-3 Kiểm dữ kiện: (a) mỗi tấm C dùng (sổ goi-api, ai_image) có mục khung_neo trỏ đúng tệp; (b) loi_chac_cuoi = 0; (c) nghi_van_con_lai = 0 và
        sổ tổng không ghi nghi vấn còn lại; (d) mọi ngoại lệ có duyệt của chủ dự án (vai chu_du_an, ngày, không email); (e) không dùng chấm mù
        làm bằng chứng (bang_chung/cach_kiem trỏ kiem-mu / blind).
K-LAI-4 Vùng bảo vệ: sai khác TB |LAI − A| (8 bit, mọi kênh) trên mặt nạ < PROT_MAX (1/255); tệp phải là PNG (JPEG làm sai số nén);
        bat_buoc (nếu có) ⊂ mat_na.
K-LAI-5 Một tấm, ban ngày: (a) ≤ 1 tấm C dùng / khung neo × mốc; (b) ≤ 1 + REGEN_MAX lệnh sinh thành công / khung neo × mốc; (c) lượt vào là
        lượt ngày (input.pass d…/ngay/day), không sinh C đêm; (d) đêm: độ chói tuyến tính TB LAI / A ≤ NIGHT_MAX và ≤ NIGHT_PX % điểm ảnh có
        L_LAI > 1,5 × L_A + 2/255.
K-LAI-6 Sổ AI: mỗi lệnh goi-api có model (req + resp), prompt nguyên văn, mask.pct_duoc_sua, usage, usd, c2pa, date_utc (giờ), file + sha256.
K-LAI-B (P2-3, Cảnh báo) Bão hoà: mỗi khung LAI không chữ, bão hoà HSV trung vị (thước MAU1: 640×360, vùng giữa 15–85 %) ≤ SAT_MAX (0,40).
Trong ±5 % quanh ngưỡng: nêu tên.
"""
import glob, json, os, re, statistics, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

FPS = 24
AI_MAX = 0.20
LABEL = 'Surface detail AI-assisted · layout, landmarks & flags from sources'
LABEL_PX, LABEL_X0, LABEL_Y0 = 38.0, 0.10, 0.66
PROT_MAX = 1.0
REGEN_MAX = 2
NIGHT_MAX, NIGHT_PX, NIGHT_TOL = 1.5, 0.5, 2.0 / 255
SAT_MAX = 0.40
CAP_PX = 0.727   # k2.js: cap = px1080 × 0,727 (như q_bando)
ROWS = ('K-LAI-1', 'K-LAI-2', 'K-LAI-3', 'K-LAI-4', 'K-LAI-5', 'K-LAI-6', 'K-LAI-B')
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
DAY = re.compile(r'^(d\d*|ngay|day)\b', re.I)
NIGHT = re.compile(r'^(n\d*|dem|night)\b', re.I)


def r(ok=True, loi=None, thieu=None, val='', **kw):
    loi, thieu = loi or [], thieu or []
    kq = kw.pop('ket_qua', None) or ('THIẾU' if thieu and not loi else None)
    return dict(ok=ok and not loi and not thieu, ket_qua=kq, loi=loi, thieu=thieu, val=val, **kw)


def na(why): return r(True, val=why, ket_qua='KHÔNG ÁP')


def sat(name, v, thr): return [f'{name} {v} (ngưỡng {thr})'] if thr and abs(v - thr) <= 0.05 * abs(thr) else []


def _p(base, p): return p if os.path.isabs(p) else os.path.join(base, p)


def _load(path):
    if path.endswith('.jsonl'): return [json.loads(l) for l in open(path) if l.strip()]
    if path.endswith(('.yaml', '.yml')):
        import yaml; return yaml.safe_load(open(path))
    if path.endswith('.gz'):
        import gzip; return json.load(gzip.open(path))
    return json.load(open(path))


def shot_ai(E):
    """shot của đặc tả khai AI → [seg/i]"""
    out = []
    for s in E.get('segments') or []:
        for i, sh in enumerate(s.get('shots') or []):
            p = sh.get('p') or {}
            if any(sh.get(k) or p.get(k) for k in ('ai_image', 'ai_texture')) or sh.get('lai') is True: out.append(f"{s['id']}/{i}")
    return out


def ap_dung(E): return bool(E.get('lai')) or bool(shot_ai(E))


def tong_s(E, TL, L):
    if TL and TL.get('tong_s'): return float(TL['tong_s']), 'timeline'
    if L.get('tong_s'): return float(L['tong_s']), 'lai.tong_s'
    d = [float(s['dur']) for s in E.get('segments') or [] if s.get('dur') is not None]
    return (sum(d), 'tổng dur đặc tả') if d else (None, '')


def frames(L, base):
    src = L.get('log_khung')
    if not src: return None
    F = {}
    for p in ([src] if isinstance(src, str) else src):
        for x in _load(_p(base, p)) or []:
            if isinstance(x, dict) and isinstance(x.get('f'), int): F[x['f']] = x
    return [F[k] for k in sorted(F)]


def is_ai(x): return bool(x.get('ai_image') or x.get('ai_texture'))


def spans(F):
    """quãng phải có nhãn: mọi khung của shot có khung AI (khi log có `shot`), không thì quãng AI liền → [(f0, f1, tên)]"""
    if F and all('shot' in x for x in F):
        S = {}
        for x in F: S.setdefault(str(x['shot']), []).append(x)
        return [(xs[0]['f'], xs[-1]['f'], f'shot {k}') for k, xs in S.items() if any(is_ai(x) for x in xs)]
    out, cur = [], None
    for x in F:
        if is_ai(x):
            if cur and x['f'] == cur[1] + 1: cur[1] = x['f']
            else:
                if cur: out.append(tuple(cur) + ('quãng AI',))
                cur = [x['f'], x['f']]
        elif cur: out.append(tuple(cur) + ('quãng AI',)); cur = None
    if cur: out.append(tuple(cur) + ('quãng AI',))
    return out


def text_map(L, base, TL, logs):
    """→ ({khung phim: [mục chữ]}, W, H, nguồn) hoặc (None, …)"""
    W, H = float(L.get('W', 1920)), float(L.get('H', 1080)); M = {}
    if L.get('log_chu'):
        J = _load(_p(base, L['log_chu'])); J = J['frames'] if isinstance(J, dict) and 'frames' in J else J
        for x in J or []: M[int(x['f'])] = x.get('text') or x.get('items') or []
        return M, W, H, 'lai.log_chu'
    if logs and TL:
        t0 = {s['id']: float(s['t0']) for s in TL.get('segments') or []}
        for f in glob.glob(os.path.join(logs, '*.log.json')):
            try: J = json.load(open(f))
            except (OSError, ValueError): continue
            if J.get('fmt', '16x9') != '16x9' or str(J.get('id')) not in t0: continue
            W, H = float(J.get('W', W)), float(J.get('H', H))
            for x in J.get('text') or []:
                M.setdefault(int(round(t0[str(J['id'])] * FPS)) + int(x['f']), []).extend(x.get('items') or x.get('text') or [])
        return (M, W, H, '--logs') if M else (None, W, H, '')
    return None, W, H, ''


def _px(it): return float(it['px1080']) if it.get('px1080') is not None else (float(it['cap']) / CAP_PX if it.get('cap') is not None else None)


def _is_label(s):
    s = re.sub(r'\s+', ' ', str(s or '')).strip()
    return len(s) >= 20 and LABEL.startswith(s) or s == LABEL


# ------------------------------------------------------------------ K-LAI-1
def klai1(F, T, src):
    if F is None: return r(thieu=['không có lai.log_khung (log mọi khung: f, ai_image, ai_texture, nhan_phuong_phap)'], val='—')
    if T is None: return r(thieu=['không biết thời lượng phim (timeline.tong_s / lai.tong_s / dur đặc tả)'], val='—')
    n = int(round(T * FPS)); fs = [x['f'] for x in F]; miss = n - len([f for f in fs if 0 <= f < n])
    ai = sum(1 for x in F if is_ai(x) and 0 <= x['f'] < n); s = ai / FPS; p = s / T if T else 0.0
    val = f"{s:.2f} s AI / {T:.2f} s ({src}) = {100 * p:.1f} % · log {len(F)} khung" + (f' (thiếu {miss})' if miss > 0 else '')
    th = [f'log khung phủ {n - miss}/{n} khung — khung không có log không biết có AI hay không'] if miss > 0 else []
    loi = [f'{s:.2f} s khung ai_image/ai_texture = {100 * p:.1f} % > {100 * AI_MAX:.0f} % thời lượng'] if p > AI_MAX else []
    return r(loi=loi, thieu=th, val=val, sat_nguong=sat('tỷ lệ AI', round(p, 4), AI_MAX), ty_le=round(p, 4), giay=round(s, 2))


# ------------------------------------------------------------------ K-LAI-2
def klai2(F, TX, W, H, txsrc):
    if F is None: return r(thieu=['không có lai.log_khung'], val='—')
    SP = spans(F)
    if not SP: return na('không có khung AI')
    loi, th, mx = [], [], []; by = {x['f']: x for x in F}; ns = 0
    for f0, f1, nm in SP:
        no = [f for f in range(f0, f1 + 1) if not (by.get(f) or {}).get('nhan_phuong_phap')]
        if no: loi.append(f'(a) {nm} khung {f0}–{f1}: {len(no)} khung không có nhan_phuong_phap (đầu tiên {no[0]})')
        if TX is None: continue
        sm = sorted(f for f in TX if f0 <= f <= f1)
        if not sm: th.append(f'(b) {nm} khung {f0}–{f1}: log chữ không có mẫu nào trong quãng'); continue
        bad_px, bad_box, no_box, absent = [], [], 0, []
        for f in sm:
            it = [x for x in TX[f] if _is_label(x.get('s'))]
            if not it: absent.append(f); continue
            x = it[0]; px = _px(x); ns += 1
            if px is not None: mx.append(px)
            if px is None or px < LABEL_PX: bad_px.append((f, px))
            b = x.get('box')
            if not b: no_box += 1
            elif not (b[0] <= LABEL_X0 * W and b[1] >= LABEL_Y0 * H): bad_box.append((f, b))
        if absent: loi.append(f'(b) {nm}: {len(absent)}/{len(sm)} mẫu log chữ không có dòng "{LABEL[:40]}…" (khung {absent[0]})')
        if bad_px: loi.append(f'(b) {nm}: {len(bad_px)} mẫu nhãn < {LABEL_PX:g} px @1080 (khung {bad_px[0][0]}: {bad_px[0][1]})')
        if bad_box: loi.append(f'(b) {nm}: {len(bad_box)} mẫu nhãn không ở góc dưới trái (x0 ≤ {100 * LABEL_X0:g} % W, y0 ≥ {100 * LABEL_Y0:g} % H; khung {bad_box[0][0]}: {bad_box[0][1]})')
        if no_box and not bad_box: th.append(f'(b) {nm}: {no_box} mẫu nhãn không có box — không kiểm được góc dưới trái')
    if TX is None: th.append('(b) không có log chữ (lai.log_chu hoặc --logs) — không đo được cỡ/vị trí nhãn')
    ai_f = sum(f1 - f0 + 1 for f0, f1, _ in SP)
    val = (f"{len(SP)} quãng ({ai_f} khung) · nhan_phuong_phap {sum(1 for f0, f1, _ in SP for f in range(f0, f1 + 1) if (by.get(f) or {}).get('nhan_phuong_phap'))}/{ai_f}"
           + (f" · log chữ ({txsrc}) {ns} mẫu có nhãn, cỡ nhỏ nhất {min(mx):.1f} px" if mx else ''))
    return r(loi=loi, thieu=th, val=val, sat_nguong=sat('nhãn px nhỏ nhất', round(min(mx), 1), LABEL_PX) if mx else [])


# ------------------------------------------------------------------ K-LAI-3 / 5 / 6 (sổ)
def _file_of(s): return os.path.basename(str(s or '').strip().split()[0]) if str(s or '').strip() else ''


def _used(KD):
    return {k: v for k, v in ((KD or {}).get('khung_neo') or {}).items() if isinstance(v, dict) and v.get('duoc_dung', True)}


def klai3(KD, G, DY, kpath):
    if KD is None: return r(thieu=['không có lai.kiem_du_kien (kiem-du-kien.json)'], val='—')
    loi, th = [], []; U = _used(KD); Gf = {str(g.get('file')): g for g in G or [] if g.get('ai_image', True) and g.get('file')}
    ref = {}
    for k, v in U.items():
        fn = _file_of(v.get('tam_C_dung'))
        if not fn: loi.append(f'(a) {k}: không ghi tam_C_dung'); continue
        ref[fn] = k
        if G is not None and fn not in Gf: loi.append(f'(a) {k}: tấm "{fn}" không có trong sổ goi-api')
        if v.get('loi_chac_cuoi') is None: th.append(f'(b) {k}: không ghi loi_chac_cuoi')
        elif v['loi_chac_cuoi'] != 0: loi.append(f"(b) {k}: loi_chac_cuoi = {v['loi_chac_cuoi']} (phải 0)")
        nv = v.get('nghi_van_con_lai')
        if nv is None: th.append(f'(c) {k}: không ghi nghi_van_con_lai')
        elif nv != 0: loi.append(f'(c) {k}: nghi_van_con_lai = {nv} (nghi vấn chưa xử lý)')
        nl = v.get('ngoai_le_cho_duyet') or v.get('ngoai_le') or []
        for e in ([nl] if isinstance(nl, str) else nl):
            ok, why = _duyet(e, k, v, DY)
            if not ok: loi.append(f'(d) {k}: ngoại lệ {e} chưa có duyệt của chủ dự án ({why})')
    if G is not None:
        dung = {fn for fn in Gf if fn in ref}
        if not dung and Gf: loi.append('(a) không tấm C nào trong sổ goi-api được kiem-du-kien ghi là tấm dùng')
    tg = (KD.get('tong') or {}); con = sum(int(v) for kk, v in tg.items() if kk.startswith('nghi_van_cuoi') and isinstance(v, (int, float)))
    per = sum(int(v.get('nghi_van_con_lai') or 0) for v in U.values())
    if con > per: loi.append(f'(c) sổ tổng ghi {con} nghi vấn còn lại (tong.nghi_van_cuoi*) nhưng mục từng tấm ghi {per} — nghi vấn chưa xử lý / sổ không khớp')
    ev = ' '.join(str(KD.get(k) or '') for k in ('bang_chung',)) + ' ' + ' '.join(str(v.get('bang_chung') or '') for v in U.values())
    if re.search(r'kiem-mu|blind', ev, re.I): loi.append('(e) bằng chứng kiểm dữ kiện trỏ tới chấm mù (kiem-mu/blind) — chấm mù không thay kiểm dữ kiện')
    cm = str(KD.get('cach_kiem') or '')
    if re.search(r'chấm mù|blind', cm, re.I) and not re.search(r'(không|KHÔNG|not)\s+(dùng|use)[^.;]*(chấm mù|blind)', cm): loi.append('(e) cach_kiem dùng chấm mù')
    val = f"{len(U)} tấm dùng · lỗi chắc cuối {sum(int(v.get('loi_chac_cuoi') or 0) for v in U.values())} · nghi vấn còn {per} (sổ tổng {con}) · ngoại lệ " + \
          str(sum(len(v.get('ngoai_le_cho_duyet') or v.get('ngoai_le') or []) for v in U.values()))
    return r(loi=loi, thieu=th, val=val)


def _duyet(e, k, v, DY):
    D = [x for x in (v.get('ngoai_le_duyet') or []) if isinstance(x, dict)] + [x for x in (DY or []) if isinstance(x, dict)]
    D = [x for x in D if str(x.get('ma') or x.get('id')) == str(e) and (not x.get('khung_neo') or str(x['khung_neo']) == str(k))]
    if not D: return False, 'không có mục duyệt'
    x = D[-1]; p = []
    if x.get('vai') != 'chu_du_an': p.append(f"vai {x.get('vai')!r} ≠ chu_du_an")
    nk = str(x.get('nguoi_ky') or '')
    if not nk.strip(): p.append('thiếu nguoi_ky')
    elif EMAIL.search(nk): p.append('nguoi_ky chứa email (che email: ghi tên/vai)')
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(x.get('ngay') or '')): p.append('ngay không dạng YYYY-MM-DD')
    if str(x.get('ket_luan') or '') not in ('chap_nhan', 'dong_y', 'dat'): p.append(f"ket_luan {x.get('ket_luan')!r} không phải chap_nhan")
    return (not p), '; '.join(p)


def _key(g): return (str(g.get('khung_neo')), str(g.get('moc', g.get('khung_neo'))))


def klai5(KD, G, base, L):
    loi, th = [], []
    if G is None: th.append('không có lai.goi_api (sổ goi-api.jsonl)')
    ok200 = [g for g in G or [] if g.get('ai_image', True) and (g.get('http') in (None, 200))]
    K = {}
    for g in ok200: K.setdefault(_key(g), []).append(g)
    Gf = {str(g.get('file')): g for g in ok200}
    U = _used(KD) if KD is not None else {}
    dung = {}
    for k, v in U.items():
        g = Gf.get(_file_of(v.get('tam_C_dung')))
        if g: dung.setdefault(_key(g), []).append(_file_of(v.get('tam_C_dung')))
    for key, fs in dung.items():
        if len(fs) > 1: loi.append(f'(a) khung neo {key[0]} × mốc {key[1]}: {len(fs)} tấm C dùng ({", ".join(fs)}) > 1')
    for key, gs in K.items():
        if len(gs) > 1 + REGEN_MAX: loi.append(f'(b) khung neo {key[0]} × mốc {key[1]}: {len(gs)} lệnh sinh thành công > 1 + {REGEN_MAX} lần sinh lại')
        lt = max((int(g.get('lan_thu') or 0) for g in gs), default=0)
        if lt > 1 + REGEN_MAX: loi.append(f'(b) khung neo {key[0]} × mốc {key[1]}: lan_thu {lt} > {1 + REGEN_MAX}')
    for g in ok200:
        ps = str(((g.get('input') or {}).get('pass')) or g.get('pass') or '')
        if not ps: th.append(f"(c) {g.get('file') or g.get('anh')}: sổ không ghi lượt vào (input.pass)")
        elif NIGHT.match(ps) or not DAY.match(ps): loi.append(f"(c) {g.get('file') or g.get('anh')}: sinh C từ lượt {ps!r} — chỉ lượt ngày (không sinh C đêm)")
    nd = []
    for i, x in enumerate(L.get('dem') or []):
        try: q = night_ratio(_p(base, x['lai']), _p(base, x['a']))
        except Exception as e: th.append(f'(d) cặp đêm {i}: không đọc được ({e})'); continue
        nd.append(q)
        if q['ti_le'] > NIGHT_MAX: loi.append(f"(d) {os.path.basename(x['lai'])}: độ chói TB LAI/A {q['ti_le']:.3f} > {NIGHT_MAX}")
        if q['pct_vuot'] > NIGHT_PX: loi.append(f"(d) {os.path.basename(x['lai'])}: {q['pct_vuot']:.2f} % điểm ảnh LAI > 1,5 × A (> {NIGHT_PX} %)")
    if L.get('dem') is None: th.append('(d) không có cặp khung đêm LAI/A (lai.dem) — không kiểm được trần 1,5× (khai `dem: []` khi tập không có đêm)')
    val = (f"{len(K)} khung neo × mốc · lệnh sinh thành công {len(ok200)} · tấm dùng {sum(len(v) for v in dung.values())}"
           + (' · đêm ' + ', '.join(f"{q['ti_le']:.2f}× ({q['pct_vuot']:.2f} %)" for q in nd) if nd else ''))
    s = sum((sat('đêm LAI/A', q['ti_le'], NIGHT_MAX) for q in nd), [])
    return r(loi=loi, thieu=th, val=val, sat_nguong=s, dem=nd)


def _lin(img):
    import numpy as np
    x = img[..., ::-1].astype(np.float64) / 255.0
    x = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
    return 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]


def night_ratio(lai, a):
    import cv2, numpy as np
    A, B = cv2.imread(a, cv2.IMREAD_COLOR), cv2.imread(lai, cv2.IMREAD_COLOR)
    if A is None or B is None: raise FileNotFoundError(a if A is None else lai)
    if A.shape != B.shape: raise ValueError(f'khác cỡ {A.shape} / {B.shape}')
    la, lb = _lin(A), _lin(B)
    return dict(ti_le=round(float(lb.mean() / max(la.mean(), 1e-6)), 3), pct_vuot=round(float(100 * (lb > NIGHT_MAX * la + NIGHT_TOL).mean()), 3))


FIELDS = (('model_req', 'model'), ('model_resp', None), ('prompt', None), ('mask.pct_duoc_sua', None), ('usage', None), ('usd', None),
          ('c2pa', None), ('date_utc', None), ('file', None), ('sha256', None))


def _get(g, k):
    for part in k.split('.'):
        g = g.get(part) if isinstance(g, dict) else None
    return g


def klai6(G):
    if G is None: return r(thieu=['không có lai.goi_api (sổ goi-api.jsonl)'], val='—')
    loi = []; n = 0
    for i, g in enumerate(G):
        if not g.get('ai_image', True): continue
        n += 1; ok200 = g.get('http') in (None, 200); miss = []
        for k, alt in FIELDS:
            if not ok200 and k in ('model_resp', 'usage', 'c2pa', 'file', 'sha256'): continue   # lệnh lỗi đường truyền: không có ảnh
            v = _get(g, k)
            if v is None and alt: v = g.get(alt)
            if v is None or (isinstance(v, str) and not v.strip()): miss.append(k)
        if isinstance(g.get('prompt'), str) and 0 < len(g['prompt'].strip()) < 40: miss.append('prompt (< 40 ký tự — không phải nguyên văn?)')
        if ok200 and g.get('usd') is not None and not isinstance(g.get('usd'), (int, float)): miss.append('usd (không phải số)')
        if ok200 and g.get('c2pa') is not None and not isinstance(g.get('c2pa'), bool): miss.append('c2pa (không phải true/false)')
        if miss: loi.append(f"lệnh {i + 1} ({g.get('file') or g.get('anh') or '?'}): thiếu {', '.join(miss)}")
    usd = sum(float(g.get('usd') or 0) for g in G if isinstance(g.get('usd'), (int, float)))
    return r(loi=loi, val=f'{n} lệnh AI · ${usd:.4f} · C2PA {sum(1 for g in G if g.get("c2pa") is True)}/{sum(1 for g in G if g.get("http") in (None, 200))}')


# ------------------------------------------------------------------ K-LAI-4
def prot_diff(lai, a, mask, must=None):
    import cv2, numpy as np
    A, B, M = cv2.imread(a, cv2.IMREAD_COLOR), cv2.imread(lai, cv2.IMREAD_COLOR), cv2.imread(mask, cv2.IMREAD_GRAYSCALE)
    for p_, x in ((a, A), (lai, B), (mask, M)):
        if x is None: raise FileNotFoundError(p_)
    if A.shape != B.shape or M.shape != A.shape[:2]: raise ValueError(f'khác cỡ: A {A.shape} · LAI {B.shape} · mặt nạ {M.shape}')
    m = M > 127
    if not m.any(): raise ValueError('mặt nạ rỗng')
    d = np.abs(A.astype(np.int16) - B.astype(np.int16))[m]
    out = dict(sai_khac_tb=round(float(d.mean()), 4), pct_khac=round(float(100 * (d.max(axis=1) > 0).mean()), 3), pct_bao_ve=round(float(100 * m.mean()), 2))
    if must:
        U = cv2.imread(must, cv2.IMREAD_GRAYSCALE)
        if U is None: raise FileNotFoundError(must)
        u = U > 127; out['bat_buoc_ngoai'] = round(float(100 * (u & ~m).sum() / max(u.sum(), 1)), 3)
    return out


def klai4(L, base):
    P = L.get('bao_ve')
    if not P: return r(thieu=['không có lai.bao_ve [{lai, a, mat_na}] (PNG không chữ cùng khung)'], val='—')
    loi, th, rs = [], [], []
    for i, x in enumerate(P):
        nm = os.path.basename(str(x.get('lai')))
        if not all(x.get(k) for k in ('lai', 'a', 'mat_na')): th.append(f'cặp {i}: thiếu lai/a/mat_na'); continue
        if not all(str(x[k]).lower().endswith('.png') for k in ('lai', 'a', 'mat_na')): loi.append(f'(a) {nm}: phải là PNG (JPEG có sai số nén, không so được < 1/255)'); continue
        try: q = prot_diff(_p(base, x['lai']), _p(base, x['a']), _p(base, x['mat_na']), _p(base, x['bat_buoc']) if x.get('bat_buoc') else None)
        except Exception as e: th.append(f'cặp {nm}: {e}'); continue
        rs.append((nm, q))
        if q['sai_khac_tb'] >= PROT_MAX: loi.append(f"(a) {nm}: vùng bảo vệ sai khác TB {q['sai_khac_tb']:.3f}/255 ≥ {PROT_MAX:g}/255 ({q['pct_khac']} % điểm ảnh khác)")
        if q.get('bat_buoc_ngoai'): loi.append(f"(b) {nm}: {q['bat_buoc_ngoai']} % vùng bắt buộc (trời/cờ/tàu/mốc/ô cửa/đèn) nằm ngoài mặt nạ bảo vệ")
    val = '; '.join(f"{nm}: {q['sai_khac_tb']:.3f}/255, {q['pct_khac']} % khác, bảo vệ {q['pct_bao_ve']} %" for nm, q in rs) or '—'
    return r(loi=loi, thieu=th, val=val, sat_nguong=sum((sat(f'{nm} sai khác', q['sai_khac_tb'], PROT_MAX) for nm, q in rs), []))


# ------------------------------------------------------------------ K-LAI-B
def klaib(L, base):
    d = L.get('khung_lai')
    if not d: return r(thieu=['không có lai.khung_lai (thư mục khung LAI không chữ)'], val='—')
    from checks.ll import q_hinh
    fs = sorted(glob.glob(os.path.join(_p(base, d), '*.png')) + glob.glob(os.path.join(_p(base, d), '*.jpg')))
    if not fs: return r(thieu=[f'thư mục {d} không có khung'], val='—')
    loi, S, near = [], [], []
    for f in fs:
        m = q_hinh.measure(f); v = round(float(m['sat_med']), 3); S.append(v)
        if v > SAT_MAX: loi.append(f'{os.path.basename(f)}: bão hoà trung vị {v} > {SAT_MAX}')
        near += sat(f'{os.path.basename(f)} bão hoà', v, SAT_MAX)
    return r(loi=loi, val=f'{len(fs)} khung · bão hoà trung vị {min(S):.3f}–{max(S):.3f} (trung vị {statistics.median(S):.3f}) · > {SAT_MAX}: {len(loi)}', sat_nguong=near,
             bao_hoa={os.path.basename(f): v for f, v in zip(fs, S)})


# ------------------------------------------------------------------ 1.16 (khiếu nại A-V6-1): nhánh vân bề mặt `ai_texture` (HC7)
def _is_van_ledger(KD): return isinstance(KD, dict) and isinstance(KD.get('tep'), list) and not KD.get('khung_neo')


def _van_used(KD):
    return [t for t in KD.get('tep') or [] if isinstance(t, dict) and str(t.get('ket_luan') or '').strip().lower().startswith('dùng')]


def klai3v(KD, G, DY):
    """K-LAI-3 cho vân (§11.3 "kiểm dữ kiện từng tấm/vân … 0 lỗi chắc mới dùng, ngoại lệ phải chủ dự án duyệt"): sổ dạng PT3 {quy_tac, tep: [{tep, anh,
    ket_luan, loi_chac, nghi_van, …}]}. (a) có tệp vân được dùng, mỗi tệp có trong sổ goi-api; (b) loi_chac rỗng; (d) kết luận có điều kiện
    ("dùng nếu …") phải ghi `dieu_kien_dat: true` (không có → THIẾU), ngoại lệ có duyệt; (e) không lấy chấm mù làm bằng chứng.
    Nghi vấn còn ghi của tệp dùng → hàng K-LAI-3V (Cảnh báo; chờ chủ dự án quyết có nâng lên Chặn như tấm C không)."""
    if KD is None: return r(thieu=['không có sổ kiểm dữ kiện vân (lai.kiem_du_kien_van / lai.kiem_du_kien dạng `tep`)'], val='—'), r(val='—', ket_qua='KHÔNG ÁP')
    loi, th, nv = [], [], []; U = _van_used(KD); Gf = {str(g.get('file')) for g in G or [] if g.get('file')}
    if not U: loi.append('(a) sổ vân không có tệp nào kết luận "dùng"')
    for t in U:
        fn = os.path.basename(str(t.get('tep') or ''))
        if G is not None and fn not in Gf: loi.append(f'(a) vân {fn}: không có trong sổ goi-api')
        if t.get('loi_chac'): loi.append(f"(b) vân {fn}: {len(t['loi_chac'])} lỗi chắc mà vẫn dùng")
        if re.match(r'^dùng\s+(nếu|khi)', str(t.get('ket_luan')).strip(), re.I) and t.get('dieu_kien_dat') is not True:
            th.append(f'(d) vân {fn}: kết luận có điều kiện ({str(t.get("ket_luan"))[:40]!r}) chưa ghi dieu_kien_dat: true')
        for e in t.get('ngoai_le_cho_duyet') or []:
            ok, why = _duyet(e, fn, t, DY)
            if not ok: loi.append(f'(d) vân {fn}: ngoại lệ {e} chưa có duyệt của chủ dự án ({why})')
        if t.get('nghi_van'): nv.append(f"(n) vân {fn}: {len(t['nghi_van'])} nghi vấn còn ghi ({str(t['nghi_van'][0])[:50]})")
    q = str(KD.get('quy_tac') or '') + ' ' + ' '.join(str(t.get('bang_chung') or '') for t in U)
    if re.search(r'kiem-mu|blind', ' '.join(str(t.get('bang_chung') or '') for t in U), re.I): loi.append('(e) bằng chứng trỏ tới chấm mù')
    elif re.search(r'chấm mù|blind', q, re.I) and not re.search(r'(không|KHÔNG|not)\s+(dùng|dựa|use)[^.;]*(chấm mù|blind)', q): loi.append('(e) quy_tac dùng chấm mù')
    th = sorted(set(th)); thd = th[:3] + ([f'… {len(th) - 3} tệp nữa'] if len(th) > 3 else [])
    return (r(loi=loi, thieu=thd, val=f'vân: {len(U)} tệp dùng / {len(KD.get("tep") or [])} trong sổ · lỗi chắc {sum(len(t.get("loi_chac") or []) for t in U)} · có điều kiện chưa xác nhận {len(th)}'),
            r(loi=nv, val=f'{len(nv)}/{len(U)} tệp vân dùng còn ghi nghi vấn'))


def klai6v(G):
    """K-LAI-6 cho vân: như K-LAI-6, nhận `input.mask_frac` (sổ PT3) thay cho `mask.pct_duoc_sua`; lệnh không mặt nạ khai `mask: null`."""
    if G is None: return r(thieu=['không có sổ goi-api của vân'], val='—')
    G2 = []
    for g in G:
        g = dict(g)
        if _get(g, 'mask.pct_duoc_sua') is None:
            mf = _get(g, 'input.mask_frac')
            if mf is not None: g['mask'] = dict(g.get('mask') or {}, pct_duoc_sua=round(100 * float(mf), 2))
            elif 'mask' in g and g['mask'] is None: g['mask'] = {'pct_duoc_sua': 'không mặt nạ'}
        G2.append(g)
    x = klai6(G2); return dict(x, val='vân: ' + x['val'])


def _merge(a, b, tag_a, tag_b):
    if a is None: return b
    if b is None: return a
    return r(loi=[f'[{tag_a}] {x}' for x in a['loi']] + [f'[{tag_b}] {x}' for x in b['loi']], thieu=[f'[{tag_a}] {x}' for x in a['thieu']] + [f'[{tag_b}] {x}' for x in b['thieu']],
             val=f"{tag_a}: {a['val']} · {tag_b}: {b['val']}", sat_nguong=(a.get('sat_nguong') or []) + (b.get('sat_nguong') or []))


def check116(E, TL=None, ep_dir='.', logs=None):
    """1.16 (CHỈ tập từ T3): K-LAI-2 theo §12.1 (q_k116.k_lai2); tách tấm C (`ai_image`) và vân (`ai_texture`): K-LAI-4, K-LAI-5, K-LAI-B chỉ áp
    khi có khung ai_image; K-LAI-3/6 áp cho từng sổ (tấm C: lai.kiem_du_kien/goi_api dạng khung_neo; vân: lai.kiem_du_kien_van/goi_api_van, hoặc sổ
    dạng `tep` của PT3); thêm K-LAI-3V (nghi vấn vân, Cảnh báo)."""
    from checks.ll import q_k116
    if not ap_dung(E): return {k: na('tập không có khối lai: và không shot nào khai ai_image/ai_texture') for k in ROWS + ('K-LAI-3V',)}
    L = E.get('lai') or {}; base = ep_dir
    if not L: return {k: r(thieu=[f"shot khai AI ({', '.join(shot_ai(E)[:4])}) nhưng episode.yaml không có khối lai:"], val='—') for k in ROWS + ('K-LAI-3V',)}
    F = frames(L, base); T, src = tong_s(E, TL, L)
    if T is None and F: T, src = len(F) / FPS, 'số khung log'
    TX, W, H, txs = text_map(L, base, TL, logs)

    def opt(k):
        try: return _load(_p(base, L[k])) if L.get(k) else None
        except Exception as e: return e
    KD, G, DY, KV, GV = opt('kiem_du_kien'), opt('goi_api'), opt('duyet'), opt('kiem_du_kien_van'), opt('goi_api_van')
    err = [f'không đọc được lai.{k}: {v}' for k, v in (('kiem_du_kien', KD), ('goi_api', G), ('duyet', DY), ('kiem_du_kien_van', KV), ('goi_api_van', GV)) if isinstance(v, Exception)]
    KD, G, DY, KV, GV = [None if isinstance(x, Exception) else x for x in (KD, G, DY, KV, GV)]
    if isinstance(DY, dict): DY = DY.get('duyet') or DY.get('ngoai_le') or []
    if KV is None and _is_van_ledger(KD): KV, GV, KD, G = KD, G, None, None
    if F is not None: img, tex = any(x.get('ai_image') for x in F), any(x.get('ai_texture') for x in F)
    else:
        sp = [sh for s in E.get('segments') or [] for sh in s.get('shots') or []]
        img = any(sh.get('ai_image') or (sh.get('p') or {}).get('ai_image') for sh in sp); tex = any(sh.get('ai_texture') or (sh.get('p') or {}).get('ai_texture') for sh in sp)
    chi_van = 'chỉ có vân bề mặt ai_texture (không tấm C): không có khung A / tấm dùng / khung đêm để so (1.16, khiếu nại A-V6-1)'
    k3c = klai3(KD, G, DY, L.get('kiem_du_kien')) if img else None
    k3v, k3n = klai3v(KV, GV, DY) if tex else (None, na('không có khung ai_texture'))
    out = {'K-LAI-1': klai1(F, T, src), 'K-LAI-2': q_k116.k_lai2(E, TL, F, TX, base), 'K-LAI-3': _merge(k3c, k3v, 'tấm C', 'vân') or na('không có khung AI'),
           'K-LAI-4': klai4(L, base) if img else na(chi_van), 'K-LAI-5': klai5(KD, G, base, L) if img else na(chi_van),
           'K-LAI-6': _merge(klai6(G) if img else None, klai6v(GV) if tex else None, 'tấm C', 'vân') or na('không có khung AI'),
           'K-LAI-B': klaib(L, base) if img else na(chi_van), 'K-LAI-3V': k3n}
    if err:
        for k in ('K-LAI-3', 'K-LAI-5', 'K-LAI-6'):
            if out[k].get('ket_qua') != 'KHÔNG ÁP': out[k] = dict(out[k], thieu=out[k]['thieu'] + err, ok=False, ket_qua=out[k]['ket_qua'] or 'THIẾU')
    return out


# ------------------------------------------------------------------
def check(E, TL=None, ep_dir='.', logs=None):
    if not ap_dung(E): return {k: na('tập không có khối lai: và không shot nào khai ai_image/ai_texture') for k in ROWS}
    L = E.get('lai') or {}; base = ep_dir
    if not L: return {k: r(thieu=[f"shot khai AI ({', '.join(shot_ai(E)[:4])}) nhưng episode.yaml không có khối lai:"], val='—') for k in ROWS}
    F = frames(L, base); T, src = tong_s(E, TL, L)
    if T is None and F: T, src = len(F) / FPS, 'số khung log'
    TX, W, H, txs = text_map(L, base, TL, logs)

    def opt(k):
        try: return _load(_p(base, L[k])) if L.get(k) else None
        except Exception as e: return e
    KD, G, DY = opt('kiem_du_kien'), opt('goi_api'), opt('duyet')
    err = {k: v for k, v in (('kiem_du_kien', KD), ('goi_api', G), ('duyet', DY)) if isinstance(v, Exception)}
    if err:
        bad = r(thieu=[f'không đọc được lai.{k}: {v}' for k, v in err.items()], val='—')
        KD, G, DY = [None if isinstance(x, Exception) else x for x in (KD, G, DY)]
    else: bad = None
    if isinstance(DY, dict): DY = DY.get('duyet') or DY.get('ngoai_le') or []
    out = {'K-LAI-1': klai1(F, T, src), 'K-LAI-2': klai2(F, TX, W, H, txs), 'K-LAI-3': klai3(KD, G, DY, L.get('kiem_du_kien')),
           'K-LAI-4': klai4(L, base), 'K-LAI-5': klai5(KD, G, base, L), 'K-LAI-6': klai6(G), 'K-LAI-B': klaib(L, base)}
    if bad:
        for k in ('K-LAI-3', 'K-LAI-5', 'K-LAI-6'): out[k] = dict(out[k], thieu=out[k]['thieu'] + bad['thieu'], ok=False, ket_qua=out[k]['ket_qua'] or 'THIẾU')
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    from checks.ll import base as _b
    E = _b.load(a[0]); TL = json.load(open(g('tl'))) if g('tl') else None
    R = check(E, TL, os.path.dirname(os.path.abspath(a[0])), g('logs'))
    for k, v in R.items():
        print(f"{k} {v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')} · {v['val']}" + ''.join('\n  ' + x for x in (v['loi'] + v['thieu'])[:20])
              + ('\n  sát ngưỡng: ' + '; '.join(v['sat_nguong']) if v.get('sat_nguong') else ''))
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1, default=str)
    sys.exit(0 if all(v['ok'] or v.get('ket_qua') == 'KHÔNG ÁP' for v in R.values()) else 1)
