#!/opt/cine/bin/python
"""Luật kênh 2 bản 1.16.0 (phiên K-1.16, 19/10/2026) — CHỈ cho tập kênh 2 từ T3; tập cũ giữ đúng hành vi 1.15.
Căn cứ: Kinh thánh kênh 2 (docs/BIBLE-KENH2.md) §12.1 (sửa 19/10), §13.2–§13.4, §13.6 TL-1…TL-6, D6; khiếu nại reports/v6/checks-appeal.md
và reports/g1b-t3/khieu-nai-K.md (xử lý: reports/k116/K116-BAO-CAO.md). Định nghĩa: checks/ll/RULES-LL.md mục "1.16".

BẬT (ap_116) khi episode.yaml khai `khung_sach: true` (đặc tả T3 đã có) hoặc `kenh2_tu_t3: true`. Không bật → mọi hàng 1.16 KHÔNG ÁP và các luật
cũ chạy đúng như 1.15 (selftest k114/k115 đối chiếu).

Đầu vào mới (khoá ở gốc episode.yaml; đường dẫn tương đối thư mục episode.yaml):
  log_shot      log shot JSON [{shot (id đoạn), goc: cao|thap|neo|phang, tl: bool (thời gian chạy trong shot), vai: "<vai truyện>" (bắt buộc với
                goc thap), noi, nguoi?: bool, trong_pct?: % diện tích đồng cỏ/khoảng trống không vật thể (TB shot), su_kien?: [{t?, k, s}] biến cố
                thấy được, diem_may?: id điểm máy cao, moc?, bac?, nguon?, ai_image?, ai_texture?}]  (g1b/log-shot.json đã có phần lớn)
  nhip_vat      bảng nhịp → vật mang nghĩa (§13.2) JSON {nhip: [{id, chinh: bool, cau, vat: [{loai, shot, t?}]}]}
  xem_cam       kết quả cổng XEM CÂM (§13.4) JSON {tat_tieng: true, cau_hoi: [8], nguoi_cham: [{id, vai: ai|chu_du_an, dung, tong: 8, ngay}], video_sha256?}
  phat_hanh     {mo_ta: <tệp mô tả + bình luận ghim>}  (câu "AI use = Yes", nguồn ghost/ranh)
  phuc_che      {kiem: <kiem.json của kiểm có đáp án>, dung: [{anh, cong_cu}]}  (§12.3)
  loi_khoa      lời khoá .txt (ML1 khi chưa có căn chữ lời) · claims_md: claims.md của tập · nam_khung: [{shot, nam_dem, nam_max: {lớp: năm}}]
  log_chu       log chữ dạng bo-tl [{f (khung phim), items}] khi không dùng --logs k2.js
  ghost         {<id ghost>: {nguon}} (NC-H5 (b) 1.16; không có thì lấy `nguon` của log shot dùng ghost)
Thẻ chương (§13.3): shot/đoạn `p.the_chuong` {s, at, dur} hoặc chữ log vai `the_chuong`. Thẻ phương pháp (D6): đoạn `the_phuong_phap: true`,
  đoạn id PP / part END, hoặc thẻ tiêu đề "How this film was made"; chữ log vai `the_phuong_phap`.

Hàng (mức đề xuất ở cap112.py; ngưỡng TL "hiệu chỉnh sau V7-PILOT"):
  SACH-1  Khung sạch §12.1 + TL-4: (a) không tấm số/câu trích (p.so, thẻ num/quote/list ngoài thẻ chương/phương pháp); (b) không tư liệu đứng riêng
          (photo/document/record/footage) — chỉ phủ lên địa hình `p.phu_dia_hinh` ≤ 3 s; (c) log chữ: không vai/chữ bị cấm hiện (alpha > 0);
          (d) chip nơi (vai where) mỗi lần ≤ 3 s; (e) chữ bản đồ khác (diem, chu_giai, inset, tag, index, card) — Cảnh báo, chờ chủ dự án;
          (f) mọi shot `p.sach: true`.
  CHUONG-1 Thẻ chương §13.3: (a) ≤ 8/tập; (b) "năm — cụm ≤ 6 từ"; (c) ≤ 3 s; (d) không trong móc mở đầu (chương 0 / part CH0 / t < moc_s);
          (e) lời trung tính (không captur*/liberat*/conquer*/seiz*); (f) log: góc dưới trái + mờ vào/ra — Cảnh báo.
  PP-1    Thẻ phương pháp D6: (a) đúng 2 thẻ; (b) mỗi thẻ 7–9 s (≈ 8 s); (c) liền nhau, kết ở cuối phim; (d) nói đủ nguồn/bản đồ, chỗ ước tính, AI;
          (e) tốc độ đọc ≤ 3 từ/s — Cảnh báo.
  TL-1    §13.6 TL-1: (a) góc cao có thời gian chạy ≥ 75 % thân phim (trừ thẻ phương pháp); (b) số shot đặc tả = cận trên số cắt (chỉ báo); (c) cắt/phút
          đo trên video (chênh lệch histogram + điểm ảnh) ≤ 5; (d) góc cao trôi ≤ 2 % khung/s (tịnh tiến phase correlation + phóng LK, trung vị shot); (e) 6–8 điểm máy cao; (f) mỗi điểm máy
          ≥ 2 năm khác nhau.
  TL-2    §13.6 TL-2: (a) lướt thấp ≤ 10 %; (b) mỗi shot lướt thấp có `vai` và là phố (noi thanh_pho) hoặc khoảnh khắc người (`nguoi: true`).
  TL-3    §13.6 TL-3: (a) shot 3D có thời gian chạy hoặc biến cố thấy được; (b) "trống": trong_pct > 60 % mà không có thời gian chạy; (c) ghi `bac`.
  NHIP-NGHIA §13.2: nhịp chính có ≥ 1 vật mang nghĩa hợp lệ ≥ 90 %.
  XEM-CAM  §13.4: kết quả chấm có đủ (8 câu, 3 AI + chủ dự án, tắt tiếng) và mỗi người chấm ≥ 6/8. K KHÔNG tự chấm.
  PC-1    §12.3 phục chế (khiếu nại A-G1B-6): cạnh mới so với MỐC BICUBIC cùng ô: Δ ≤ 1,0 điểm % và PSNR ≥ bicubic; ảnh dùng phải đạt.
Thay cho luật cũ ở tập từ T3 (khiếu nại chấp nhận): K-LAI-2 (k_lai2), NC-H5 (nch5), BD-3 (bd3); ML1 đọc lời khoá (cau_tu_loi_khoa).
Trong ±5 % quanh ngưỡng: nêu tên.
"""
import glob, json, os, re, statistics, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

FPS = 24
CHIP_S, DOC_S = 3.0, 3.0                                   # §12.1 chip nơi ≤ 3 s; TL-4 tư liệu phủ ≤ 3 s
CH_MAX, CH_WORDS, CH_S = 8, 6, 3.0                          # §13.3
PP_N, PP_S, PP_TOL, PP_WPS, PP_END = 2, 8.0, 1.0, 3.0, 0.5  # D6: 2 thẻ × ≈ 8 s (K đọc "≈" = ±1 s); đọc ≤ 3 từ/s; kết ≤ 0,5 s trước cuối
TL_CAO_PCT, TL_CUT_MIN, TL_DRIFT, TL_DIEM = 75.0, 5.0, 2.0, (6, 8)   # §13.6 TL-1 (hiệu chỉnh sau V7-PILOT)
TL_THAP_PCT, TRONG_PCT = 10.0, 60.0                        # TL-2; TL-3 "trống"
NHIP_PCT = 90.0                                            # §13.2
XC_CAU, XC_AI, XC_DAT = 8, 3, 6                            # §13.4
PC_DELTA = 1.0                                             # PC-1 (tạm, hiệu chuẩn trên ≥ 10 ảnh)
CUT_HIST, CUT_PX, CUT_PX2, CUT_K = 0.20, 12.0, 20.0, 3.0    # thước cắt (hiệu chuẩn trên animatic T3, báo cáo K-1.16 §3.4): xem cuts_video
LBL_X0, LBL_Y0 = 0.10, 0.66
CROP_Y = (0.10, 0.68)                                      # vùng đo chuyển động máy (theo chiều cao khung)
VAT_LOAI = {'co_chu_quyen', 'dem_nam', 'ranh_dong', 'mui_ten', 'su_kien', 'the_chuong'}
BANNED_ROLES = {'src', 'src_ngan', 'ai_label', 'ghost_src', 'inset_src', 'index_src', 'method', 'bien_gioi', 'so', 'trich', 'trich_dich'}
OK_ROLES = {'year', 'clock', 'calendar', 'where', 'the_chuong', 'the_phuong_phap'}
BANNED_TXT = re.compile(r'approx\. borders|estimated infill|ruins: estimated|illustrativ|ai-assisted|surface detail|^source:|^sources?:|^map:', re.I)
NOT_NEUTRAL = re.compile(r'\b(captur|recaptur|liberat|conquer|seiz)\w*', re.I)
CH_RE = re.compile(r'^\s*(\d{3,4}s?)\s*[—–-]\s*(.+?)\s*$')
DOC_TYPES = {'photo', 'document', 'record', 'footage'}
PP_TITLE = re.compile(r'how this film was made', re.I)
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
CAP_PX = 0.727


def r(ok=True, loi=None, thieu=None, val='', **kw):
    loi, thieu = loi or [], thieu or []
    kq = kw.pop('ket_qua', None) or ('THIẾU' if thieu and not loi else None)
    return dict(ok=ok and not loi and not thieu, ket_qua=kq, loi=loi, thieu=thieu, val=val, **kw)


def na(why): return r(True, val=why, ket_qua='KHÔNG ÁP')


def sat(name, v, thr): return [f'{name} {v} (ngưỡng {thr})'] if thr and abs(v - thr) <= 0.05 * abs(thr) else []


def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def ap_116(E): return bool(E.get('khung_sach') or E.get('kenh2_tu_t3'))


def _p(base, p): return p if os.path.isabs(p) else os.path.join(base or '.', p)


def _load(path):
    if path.endswith('.jsonl'): return [json.loads(l) for l in open(path) if l.strip()]
    if path.endswith(('.yaml', '.yml')):
        import yaml; return yaml.safe_load(open(path))
    return json.load(open(path))


def opt_file(E, k, base):
    """→ (dữ liệu, None) | (None, lý do THIẾU)"""
    v = E.get(k)
    if not v: return None, f'không khai `{k}:` trong episode.yaml'
    try: return _load(_p(base, v)), None
    except Exception as e: return None, f'không đọc được {k} ({v}): {e}'


def _f(x, k): return x.get(k) if x.get(k) is not None else (x.get('p') or {}).get(k)


# ------------------------------------------------------------------ shot của tập
def shot_list(E, TL):
    """→ [dict(seg, i, t0, t1, ty, sh, spec, sg)] theo giây tuyệt đối. Có timeline thì dùng timeline; không thì dựng từ đặc tả (at, dur)."""
    SG = {s['id']: s for s in E.get('segments') or []}; out = []
    if TL:
        for s in TL['segments']:
            sp = (SG.get(s['id']) or {}).get('shots') or []
            for i, sh in enumerate(s['shots']):
                spec = sp[i] if i < len(sp) else {}
                out.append(dict(seg=s['id'], i=i, t0=s['t0'] + sh['t0'], t1=s['t0'] + sh['t1'], ty=spec.get('type') or (spec.get('p') or {}).get('type') or sh.get('type'),
                                sh=sh, spec=spec, sg=SG.get(s['id']) or {}))
        return out
    t = 0.0
    for s in E.get('segments') or []:
        d = float(s.get('dur') or 0); sh = s.get('shots') or []
        ats = [float(x.get('at') or 0) if isinstance(x.get('at'), (int, float)) else 0.0 for x in sh] + [d]
        for i, x in enumerate(sh):
            out.append(dict(seg=s['id'], i=i, t0=t + ats[i], t1=t + max(ats[i], ats[i + 1]), ty=x.get('type') or (x.get('p') or {}).get('type'), sh=x, spec=x, sg=s))
        t += d
    return out


def tong(E, TL):
    if TL and TL.get('tong_s'): return float(TL['tong_s'])
    return sum(float(s.get('dur') or 0) for s in E.get('segments') or [])


def seg_spans(E, TL):
    """→ {id đoạn: (t0, t1)}"""
    if TL: return {s['id']: (float(s['t0']), float(s['t0']) + float(s.get('dur') or (max([x['t1'] for x in s['shots']] or [0])))) for s in TL['segments']}
    out, t = {}, 0.0
    for s in E.get('segments') or []:
        d = float(s.get('dur') or 0); out[s['id']] = (t, t + d); t += d
    return out


def is_pp_seg(s):
    if s.get('the_phuong_phap') or str(s.get('id')) == 'PP' or str(s.get('part')) == 'END': return True
    for x in s.get('shots') or []:
        c = (x.get('p') or {}).get('card') or {}
        if (x.get('p') or {}).get('the_phuong_phap') or PP_TITLE.search(str(c.get('title') or '')): return True
    return False


def pp_spans(E, TL):
    SP = seg_spans(E, TL)
    return [(s['id'], SP[s['id']][0], SP[s['id']][1], s) for s in E.get('segments') or [] if s['id'] in SP and is_pp_seg(s)]


# ------------------------------------------------------------------ log chữ (k2.js) → khung tuyệt đối
def text_frames(TL, logs, log_chu=None, base='.'):
    """→ ({khung phim: [mục]}, bước mẫu khung, W, H) hoặc (None, …)"""
    M, W, H = {}, 1920.0, 1080.0
    if log_chu:
        J = _load(_p(base, log_chu)); J = J['frames'] if isinstance(J, dict) and 'frames' in J else J
        for x in J or []: M.setdefault(int(x['f']), []).extend(x.get('items') or x.get('text') or [])
    elif logs and TL:
        t0 = {s['id']: float(s['t0']) for s in TL.get('segments') or []}
        for f in glob.glob(os.path.join(logs, '*.log.json')):
            try: J = json.load(open(f))
            except (OSError, ValueError): continue
            if J.get('fmt', '16x9') != '16x9' or str(J.get('id')) not in t0: continue
            W, H = float(J.get('W', W)), float(J.get('H', H))
            for x in J.get('text') or []:
                M.setdefault(int(round(t0[str(J['id'])] * FPS)) + int(x['f']), []).extend(x.get('items') or x.get('text') or [])
    if not M: return None, 12, W, H
    fs = sorted(M); d = [b - a for a, b in zip(fs, fs[1:]) if b > a]
    return M, (int(statistics.median(d)) if d else 12), W, H


def _vis(it): return it.get('alpha') is None or float(it.get('alpha') or 0) > 0.01


def _px(it): return float(it['px1080']) if it.get('px1080') is not None else (float(it['cap']) / CAP_PX if it.get('cap') is not None else None)


def _runs(fs, step):
    """các quãng khung mẫu liền (cách ≤ 1,5 bước) → [(f0, f1)]"""
    out = []
    for f in sorted(fs):
        if out and f - out[-1][1] <= 1.5 * step: out[-1][1] = f
        else: out.append([f, f])
    return [tuple(x) for x in out]


def _run_s(f0, f1, step): return (f1 - f0 + step) / FPS


# ------------------------------------------------------------------ SACH-1
def sach1(E, TL, TX=None, step=12):
    M = {k: [] for k in 'abcdef'}; S = shot_list(E, TL); PP = {x[0] for x in pp_spans(E, TL)}
    for z in S:
        p = z['sh'].get('p') or {}; ps = z['spec'].get('p') or {}; P = dict(p, **ps); w = f"{z['seg']}/{z['i']} @{mmss(z['t0'])}"
        if z['seg'] in PP: continue
        if P.get('so'): M['a'].append(f'(a) {w}: số/câu trích trên hình (p.so: {str((P["so"][0] or {}).get("s") if isinstance(P["so"], list) and P["so"] else P["so"])[:40]!r}) — TL-4: lời + CC mang')
        c = P.get('card') or {}
        if (z['ty'] == 'card' or c) and not P.get('the_chuong') and not P.get('the_phuong_phap'):
            M['a'].append(f"(a) {w}: tấm {c.get('type') or 'card'} đứng riêng ({str(c.get('big') or c.get('title') or c.get('s') or '')[:30]!r}) — TL-4")
        doc = z['ty'] in DOC_TYPES or z['sh'].get('tpl') in ('footage', 'archive') or P.get('clip') or P.get('photo')
        if doc:
            ov = P.get('phu_dia_hinh')
            dur = float((ov or {}).get('dur') or 0) if isinstance(ov, dict) else 0.0
            if not ov: M['b'].append(f'(b) {w}: tư liệu đứng riêng ({z["ty"]}, {z["t1"] - z["t0"]:.1f} s) — TL-4: chỉ phủ lên địa hình ≤ {DOC_S:g} s')
            elif dur <= 0 or dur > DOC_S + 1e-6: M['b'].append(f'(b) {w}: tư liệu phủ địa hình {dur:.2f} s (cần 0 < dur ≤ {DOC_S:g} s)')
        if not P.get('sach'): M['f'].append(f'(f) {w}: shot không bật lọc khung sạch (p.sach)')
    th, nv, chip = [], 0, []
    if TX is None: th.append('(c) không có log chữ (--logs k2.js) — không đo được chữ thực hiện trên hình; (d) chip nơi chưa đo')
    else:
        by_role = {}
        for f, it in TX.items():
            for x in it:
                if not _vis(x): continue
                ro, s_ = str(x.get('role') or ''), str(x.get('s') or '')
                nv += 1
                if ro in OK_ROLES:
                    if ro == 'where': by_role.setdefault(s_, []).append(f)
                    continue
                if ro in BANNED_ROLES or BANNED_TXT.search(s_): by_role.setdefault(('BAN', ro), []).append((f, s_))
                else: by_role.setdefault(('KHAC', ro), []).append((f, s_))
        for k, v in by_role.items():
            if isinstance(k, tuple):
                f0, s_ = min(v)
                (M['c'] if k[0] == 'BAN' else M['e']).append(f"({'c' if k[0] == 'BAN' else 'e'}) vai {k[1] or '—'}: {len(v)} mẫu hiện, đầu tiên {mmss(f0 / FPS)} {s_!r}"
                                                               + ('' if k[0] == 'BAN' else ' — chữ ngoài danh sách §12.1, chờ chủ dự án quyết'))
            else:
                for f0, f1 in _runs(v, step):
                    d = _run_s(f0, f1, step); chip.append(d)
                    if d > CHIP_S + step / FPS / 2: M['d'].append(f'(d) chip nơi {k!r} @{mmss(f0 / FPS)}: {d:.2f} s > {CHIP_S:g} s')
    loi = sum(M.values(), [])
    near = sat('chip nơi dài nhất s', round(max(chip), 2), CHIP_S) if chip else []
    return r(loi=loi, thieu=th, muc=M, sat_nguong=near,
             val=f"{len(S)} shot · tấm số/trích {len(M['a'])} · tư liệu đứng riêng {len(M['b'])} · " + (f"log chữ {nv} mục hiện · cấm {len(M['c'])} · chip {len(chip)} lần, dài nhất {max(chip or [0]):.2f} s · chữ khác {len(M['e'])}" if TX is not None else 'không log chữ'))


# ------------------------------------------------------------------ thẻ chương
def the_chuong(E, TL, TX=None, step=12):
    """→ [dict(s, t0, d, seg, nguon)] — từ đặc tả (p.the_chuong) hoặc log chữ vai the_chuong"""
    out = []; S = shot_list(E, TL); SP = seg_spans(E, TL)
    for z in S:
        P = dict(z['sh'].get('p') or {}, **(z['spec'].get('p') or {}))
        for c in ([P['the_chuong']] if isinstance(P.get('the_chuong'), dict) else P.get('the_chuong') or []):
            out.append(dict(s=str(c.get('s') or ''), t0=z['t0'] + float(c.get('at') or 0), d=float(c.get('dur') or 0), seg=z['seg'], nguon='đặc tả'))
    for s in E.get('segments') or []:
        c = s.get('the_chuong')
        if isinstance(c, dict) and s['id'] in SP: out.append(dict(s=str(c.get('s') or ''), t0=SP[s['id']][0] + float(c.get('at') or 0), d=float(c.get('dur') or 0), seg=s['id'], nguon='đặc tả'))
    if not out and TX is not None:
        R = {}
        for f, it in TX.items():
            for x in it:
                if x.get('role') == 'the_chuong' and _vis(x): R.setdefault(str(x.get('s')), []).append((f, x))
        for s_, v in R.items():
            for f0, f1 in _runs([f for f, _ in v], step):
                xs = [x for f, x in v if f0 <= f <= f1]
                out.append(dict(s=s_, t0=f0 / FPS, d=_run_s(f0, f1, step), seg=None, nguon='log', box=xs[0].get('box'), alpha=[x.get('alpha') for x in xs]))
    return sorted(out, key=lambda c: c['t0'])


def _seg_at(E, TL, t):
    for k, (a, b) in seg_spans(E, TL).items():
        if a <= t < b: return k
    return None


def chuong1(E, TL, TX=None, step=12, W=1920.0, H=1080.0):
    C = the_chuong(E, TL, TX, step); M = {k: [] for k in 'abcdef'}
    if not C: return r(val='0 thẻ chương (không bắt buộc; ≤ 8/tập)', muc=M)
    SG = {s['id']: s for s in E.get('segments') or []}; moc_s = float(E.get('moc_s') or 0)
    if len(C) > CH_MAX: M['a'].append(f'(a) {len(C)} thẻ chương > {CH_MAX}/tập')
    for c in C:
        w = f"thẻ {c['s'][:40]!r} @{mmss(c['t0'])}"; m = CH_RE.match(c['s'])
        if not m: M['b'].append(f'(b) {w}: không đúng dạng "năm — cụm ≤ {CH_WORDS} từ"')
        elif len(m.group(2).split()) > CH_WORDS: M['b'].append(f'(b) {w}: cụm {len(m.group(2).split())} từ > {CH_WORDS}')
        if c['d'] <= 0: M['c'].append(f'(c) {w}: không khai thời lượng')
        elif c['d'] > CH_S + (step / FPS / 2 if c['nguon'] == 'log' else 1e-6): M['c'].append(f"(c) {w}: {c['d']:.2f} s > {CH_S:g} s")
        sg = SG.get(c['seg'] or _seg_at(E, TL, c['t0'])) or {}
        if str(sg.get('chuong')) == '0' or str(sg.get('part')).upper() == 'CH0' or c['t0'] < moc_s: M['d'].append(f'(d) {w}: nằm trong móc mở đầu (chương 0 / CH0 / < moc_s)')
        bad = NOT_NEUTRAL.findall(c['s'])
        if bad: M['e'].append(f'(e) {w}: lời không trung tính ({", ".join(sorted(set(bad)))}…) — dùng "changes hands"')
        if c['nguon'] == 'log':
            b = c.get('box')
            if b and not (b[0] <= LBL_X0 * W and b[1] >= LBL_Y0 * H): M['f'].append(f'(f) {w}: không ở góc dưới trái (box {b})')
            al = [a for a in c.get('alpha') or [] if a is not None]
            if len(al) >= 3 and not (al[0] < max(al) and al[-1] < max(al)): M['f'].append(f'(f) {w}: không thấy mờ vào/ra (alpha {al[0]} … {al[-1]})')
    near = sum((sat(f"thẻ {c['s'][:20]!r} s", round(c['d'], 2), CH_S) for c in C), []) + sat('số thẻ', len(C), CH_MAX)
    return r(loi=sum(M.values(), []), muc=M, sat_nguong=near, the=C,
             val=f"{len(C)} thẻ ({C[0]['nguon']}) · dài nhất {max(c['d'] for c in C):.2f} s · " + '; '.join(f"{mmss(c['t0'])} {c['s'][:30]}" for c in C[:4]))


# ------------------------------------------------------------------ PP-1 thẻ phương pháp (D6)
def _pp_text(s):
    out = []
    for x in s.get('shots') or []:
        c = (x.get('p') or {}).get('card') or {}
        out += [str(c.get('title') or '')] + [str(i.get('s') if isinstance(i, dict) else i) for i in c.get('items') or []] + [str(c.get('s') or '')]
    return ' '.join(t for t in out if t)


def pp1(E, TL):
    P = pp_spans(E, TL); T = tong(E, TL); M = {k: [] for k in 'abcde'}
    if not P: return r(loi=[f'(a) không có thẻ phương pháp cuối phim (cần {PP_N} thẻ × ≈ {PP_S:g} s — D6)'], muc={'a': ['(a)']}, val='0 thẻ')
    if len(P) != PP_N: M['a'].append(f'(a) {len(P)} thẻ phương pháp ≠ {PP_N} (D6: 2 thẻ × ≈ 8 s)')
    near = []
    for sid, a, b, s in P:
        d = b - a
        if abs(d - PP_S) > PP_TOL + 1e-6: M['b'].append(f'(b) thẻ {sid}: {d:.2f} s ngoài {PP_S - PP_TOL:g}–{PP_S + PP_TOL:g} s (≈ {PP_S:g} s)')
        near += sat(f'thẻ {sid} s (cận dưới)', round(d, 2), PP_S - PP_TOL) + sat(f'thẻ {sid} s (cận trên)', round(d, 2), PP_S + PP_TOL)
        n = len(re.findall(r"[A-Za-z0-9'’]+", _pp_text(s))); wps = n / d if d else 99
        if wps > PP_WPS: M['e'].append(f'(e) thẻ {sid}: {n} từ / {d:.1f} s = {wps:.1f} từ/s > {PP_WPS:g} (khó đọc trên điện thoại)')
    P2 = sorted(P, key=lambda x: x[1])
    if abs(P2[-1][2] - T) > PP_END: M['c'].append(f'(c) thẻ cuối kết ở {mmss(P2[-1][2])}, phim kết {mmss(T)} — thẻ phương pháp phải ở cuối phim')
    for x, y in zip(P2, P2[1:]):
        if y[1] - x[2] > 0.05: M['c'].append(f'(c) thẻ {x[0]} và {y[0]} không liền nhau ({x[2]:.2f} → {y[1]:.2f} s)')
    txt = ' '.join(_pp_text(s) for _, _, _, s in P)
    for k, rg in (('nguồn/bản đồ', r'\b(source|sources|map|maps|record|records|archive|registers?|built from)\b'), ('chỗ ước tính', r'\b(estimat\w*|approximat\w*|reconstruct\w*|illustrative)\b'),
                  ('AI dùng vào việc gì', r'\bAI\b')):
        if not re.search(rg, txt, re.I): M['d'].append(f'(d) thẻ phương pháp không nói {k}')
    return r(loi=sum(M.values(), []), muc=M, sat_nguong=near, val=f"{len(P)} thẻ · " + ', '.join(f'{sid} {b - a:.1f} s' for sid, a, b, _ in P) + f' · {len(re.findall(r"[A-Za-z0-9]+", txt))} từ')


# ------------------------------------------------------------------ log shot (TL-1…3)
def log_shot(E, base, path=None):
    if path: path_ = path
    elif E.get('log_shot'): path_ = _p(base, E['log_shot'])
    else: return None, 'không khai `log_shot:` (log shot có goc/tl/vai/trong_pct)'
    try: J = _load(path_)
    except Exception as e: return None, f'không đọc được log_shot: {e}'
    return (J.get('shots') if isinstance(J, dict) else J) or [], None


def shot_durs(E, TL, LS):
    """log shot → [(mục, t0, t1)] (mục 'shot' = id đoạn; hoặc t: [t0, t1])"""
    SP = seg_spans(E, TL); out = []
    for x in LS:
        if isinstance(x.get('t'), list): out.append((x, float(x['t'][0]), float(x['t'][1])))
        elif str(x.get('shot')) in SP: a, b = SP[str(x['shot'])]; out.append((x, a, b))
    return out


def goc_of(x, E):
    g = x.get('goc')
    if g: return str(g)
    sg = next((s for s in E.get('segments') or [] if s['id'] == str(x.get('shot'))), None)
    if sg and all((sh.get('type') or (sh.get('p') or {}).get('type')) in ('card', 'photo', 'document', 'record', 'strategic', 'map') for sh in sg.get('shots') or []): return 'phang'
    if sg and is_pp_seg(sg): return 'phang'
    return None


def cut_times_spec(E, TL):
    """giây cắt theo đặc tả: đầu mỗi shot (trừ 0) + beats cut t > 0, gộp < 0,25 s"""
    ts = [z['t0'] for z in shot_list(E, TL) if z['t0'] > 0.05]
    SP = seg_spans(E, TL)
    for s in E.get('segments') or []:
        for b in s.get('beats') or []:
            if b.get('k') == 'cut' and isinstance(b.get('t'), (int, float)) and b['t'] > 0.05 and s['id'] in SP: ts.append(SP[s['id']][0] + float(b['t']))
    out = []
    for t in sorted(ts):
        if not out or t - out[-1] >= 0.25: out.append(t)
    return out


# ------------------------------------------------------------------ thước video
def video_gray(mp4, w=320, h=180):
    import numpy as np
    pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', mp4], capture_output=True, text=True).stdout.strip()
    a, b = (pr.split('/') + ['1'])[:2]; fps = float(a) / float(b or 1)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', mp4, '-map', '0:v:0', '-vf', f'scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w), fps


def cuts_video(F, fps):
    """cắt = khung i (bỏ 0,5 s đầu) mà so với khung trước: [chênh lệch histogram xám (L1/2, 32 bin) ≥ CUT_HIST VÀ lệch điểm ảnh TB ≥ CUT_PX]
    HOẶC [lệch điểm ảnh ≥ CUT_PX2 VÀ ≥ CUT_K × trung vị lệch của ±6 khung quanh]; và là cực đại cục bộ lệch điểm ảnh ±3 khung; cách cắt trước > 3 khung.
    Đổi năm cùng góc máy (cảnh tl) thường KHÔNG thành cắt — đúng ý TL-1 (đó là thời gian chạy). → [giây]"""
    import numpy as np
    n = len(F)
    if n < 2: return []
    Hs = np.stack([np.bincount((f >> 3).ravel(), minlength=32) for f in F]).astype(np.float64); Hs /= Hs.sum(axis=1, keepdims=True)
    dh = np.r_[0, 0.5 * np.abs(np.diff(Hs, axis=0)).sum(axis=1)]
    dp = np.r_[0, np.abs(np.diff(F.astype(np.int16), axis=0)).mean(axis=(1, 2))]
    out = []
    for i in range(max(1, int(0.5 * fps)), n):
        nb = np.r_[dp[max(1, i - 6):i], dp[i + 1:i + 7]]; med = float(np.median(nb)) if len(nb) else 0.0
        c = (dh[i] >= CUT_HIST and dp[i] >= CUT_PX) or (dp[i] >= CUT_PX2 and dp[i] >= CUT_K * max(med, 1.0))
        if c and dp[i] >= dp[max(1, i - 3):i + 4].max() - 1e-9 and (not out or i - out[-1] > 3): out.append(i)
    return [i / fps for i in out]


def zoom_lk(a, b):
    """tỉ lệ phóng b so với a: phép tương tự (tịnh tiến + xoay + phóng) ước từ dòng quang học Lucas–Kanade trên ≤ 200 điểm góc, RANSAC 1,5 px.
    (Thử log-polar phase correlation — Fourier–Mellin — trên video tổng hợp: sai cả chiều phóng; nên phóng đo bằng LK, tịnh tiến vẫn bằng phase
    correlation.) → tỉ lệ | None"""
    import cv2, numpy as np
    p = cv2.goodFeaturesToTrack(a, 200, 0.01, 6)
    if p is None or len(p) < 8: return None
    q, st, _ = cv2.calcOpticalFlowPyrLK(a, b, p, None, winSize=(21, 21), maxLevel=3); ok = st.ravel() == 1
    if ok.sum() < 8: return None
    M, _ = cv2.estimateAffinePartial2D(p[ok], q[ok], method=cv2.RANSAC, ransacReprojThreshold=1.5)
    return None if M is None else float(np.hypot(M[0, 0], M[1, 0]))


def drift_video(F, fps, a, b, cuts=(), step_s=0.25):
    """chuyển động máy (% bề ngang khung / giây) trong [a, b), mỗi cửa sổ 1 s không chứa cắt:
    vùng đo y 10–68 % (bỏ chữ tĩnh); tịnh tiến = tổng véc-tơ phase correlation (cửa sổ Hann) giữa các khung cách step_s; phóng = zoom_lk giữa đầu và cuối cửa sổ,
    quy ra độ dời góc khung |s − 1| × nửa đường chéo. Trị số cửa sổ = (|tịnh tiến| + dời do phóng) / bề ngang. → (trung vị %/s, số cửa sổ) | (None, 0)"""
    import cv2, numpy as np
    W, hd = F.shape[2], 0.5 * float(np.hypot(F.shape[2], F.shape[1]))
    F = F[:, int(CROP_Y[0] * F.shape[1]):int(CROP_Y[1] * F.shape[1]), :]   # bỏ dải chữ tĩnh (chip trên, bộ đếm/phụ đề dưới) — chữ tĩnh kéo đỉnh tương quan về 0
    win = cv2.createHanningWindow((W, F.shape[1]), cv2.CV_32F)
    st = max(1, int(round(step_s * fps))); per = max(1, int(round(1.0 / step_s)))
    i0, i1 = int(np.ceil(a * fps)) + 1, int(b * fps) - 1; v = []
    idx = list(range(i0, i1 - st, st))
    for k in range(0, len(idx) - per + 1, per):
        seg = idx[k:k + per]; t0_, t1_ = seg[0] / fps, (seg[-1] + st) / fps
        if any(t0_ - 0.1 <= c <= t1_ + 0.1 for c in cuts): continue
        dx = dy = 0.0
        for i in seg:
            (x, y), _ = cv2.phaseCorrelate(F[i].astype(np.float32), F[i + st].astype(np.float32), win); dx += x; dy += y
        z = zoom_lk(F[seg[0]], F[seg[-1] + st]) or 1.0
        v.append(100.0 * (float(np.hypot(dx, dy)) + abs(z - 1.0) * hd) / W / (len(seg) * st / fps))
    return (round(float(np.median(v)), 2), len(v)) if v else (None, 0)


def tl1(E, TL, LS=None, why=None, video=None, VF=None):
    T = tong(E, TL); PPd = sum(b - a for _, a, b, _ in pp_spans(E, TL)); Tb = T - PPd; M = {k: [] for k in 'abcdef'}; th = []; near = []
    cuts_s = cut_times_spec(E, TL); cpm_s = len(cuts_s) / (Tb / 60) if Tb else 0.0
    # (b) số shot của đặc tả = CẬN TRÊN số cắt (đổi năm cùng góc máy được khai là shot mới nhưng không phải cắt) → chỉ báo; (c) video quyết
    D = shot_durs(E, TL, LS) if LS is not None else []
    cao = sum(b - a for x, a, b in D if goc_of(x, E) == 'cao' and x.get('tl') is True)
    nog = [str(x.get('shot')) for x, a, b in D if goc_of(x, E) is None]
    if LS is None: th.append(f'(a) {why}')
    else:
        pc = 100 * cao / Tb if Tb else 0.0
        if nog: th.append(f'(a) {len(nog)} shot log không có `goc` ({", ".join(nog[:6])}{"…" if len(nog) > 6 else ""})')
        if pc < TL_CAO_PCT and not nog: M['a'].append(f'(a) góc cao có thời gian chạy {cao:.1f} s = {pc:.1f} % < {TL_CAO_PCT:g} % thân phim ({Tb:.1f} s)')
        elif pc < TL_CAO_PCT: th.append(f'(a) góc cao có thời gian chạy (đã khai) {pc:.1f} % < {TL_CAO_PCT:g} % — chưa kết luận vì thiếu `goc`')
        near += sat('góc cao + thời gian chạy %', round(pc, 1), TL_CAO_PCT)
        dm = {}
        for x, a, b in D:
            if goc_of(x, E) == 'cao':
                if not x.get('diem_may'): dm.setdefault(None, []).append(x)
                else: dm.setdefault(str(x['diem_may']), set()).add(str(x.get('moc') or x.get('nam') or '?'))
        nd = [k for k in dm if k is not None]
        if dm.get(None): th.append(f"(e)(f) {len(dm[None])} shot góc cao không khai `diem_may`")
        if nd:
            if not TL_DIEM[0] <= len(nd) <= TL_DIEM[1]: M['e'].append(f'(e) {len(nd)} điểm máy cao (cần {TL_DIEM[0]}–{TL_DIEM[1]})')
            for k in nd:
                if len(dm[k]) < 2: M['f'].append(f'(f) điểm máy {k}: chỉ ở năm {"/".join(sorted(dm[k]))} — phải quay lại ở năm khác')
    vt = ''
    if VF is not None or video:
        try:
            F, fps = VF if VF is not None else video_gray(video)
            cv = cuts_video(F, fps); Tv = len(F) / fps; Tvb = max(1e-6, Tv - PPd); cpm_v = len([c for c in cv if c < Tv - PPd]) / (Tvb / 60)
            if cpm_v > TL_CUT_MIN: M['c'].append(f'(c) video: {len(cv)} cắt đo / {Tvb / 60:.2f} phút = {cpm_v:.2f} cắt/phút > {TL_CUT_MIN:g}')
            near += sat('cắt/phút (video)', round(cpm_v, 2), TL_CUT_MIN); dr = []
            for x, a, b in D:
                if goc_of(x, E) == 'cao':
                    v, n = drift_video(F, fps, a, b, cv)
                    if v is None: continue
                    dr.append(v)
                    if v > TL_DRIFT: M['d'].append(f"(d) shot {x.get('shot')} góc cao trôi {v:.2f} % khung/s > {TL_DRIFT:g} (trung vị {n} cửa sổ 1 s)")
                    near += sat(f"shot {x.get('shot')} trôi %/s", v, TL_DRIFT)
            d3 = []
            if not dr:   # chưa khai goc: đo trôi máy mọi shot 3D để tham khảo (không tính lỗi)
                for z in shot_list(E, TL):
                    if z['ty'] in ('scene3d', 'timelapse'):
                        v, n = drift_video(F, fps, z['t0'], z['t1'], cv)
                        if v is not None: d3.append(v)
            vt = (f' · video {len(cv)} cắt = {cpm_v:.2f}/phút' + (f' · trôi góc cao trung vị {statistics.median(dr):.2f} %/s ({len(dr)} shot)' if dr else '')
                  + (f' · (tham khảo, chưa có goc) trôi máy shot 3D: trung vị {statistics.median(d3):.2f} %/s, ≤ {TL_DRIFT:g} %/s ở {sum(v <= TL_DRIFT for v in d3)}/{len(d3)} shot' if d3 else ''))
        except Exception as e: th.append(f'(c) không đo được video: {e}')
    else: th.append(f'(c)(d) không có video (master/--tl16-video) — cắt/phút và trôi máy chưa đo (đặc tả: cận trên {cpm_s:.2f} cắt/phút)')
    return r(loi=sum(M.values(), []), thieu=th, muc=M, sat_nguong=near, cat_dac_ta=len(cuts_s),
             val=f'thân phim {Tb:.1f} s · góc cao + tl {cao:.1f} s ({100 * cao / Tb if Tb else 0:.1f} %) · đặc tả ≤ {cpm_s:.2f} cắt/phút (cận trên)' + vt + ' · ngưỡng hiệu chỉnh sau V7-PILOT')


def tl2(E, TL, LS=None, why=None):
    if LS is None: return r(thieu=[f'(a) {why}'], val='—')
    T = tong(E, TL) - sum(b - a for _, a, b, _ in pp_spans(E, TL)); M = {'a': [], 'b': []}; D = shot_durs(E, TL, LS)
    th = [x for x, a, b in D if goc_of(x, E) == 'thap']; s = sum(b - a for x, a, b in D if goc_of(x, E) == 'thap'); pc = 100 * s / T if T else 0.0
    if pc > TL_THAP_PCT: M['a'].append(f'(a) lướt thấp {s:.1f} s = {pc:.1f} % > {TL_THAP_PCT:g} %')
    for x in th:
        if len(str(x.get('vai') or '').strip()) < 3: M['b'].append(f"(b) shot {x.get('shot')}: lướt thấp không ghi `vai` truyện")
        if not (x.get('noi') == 'thanh_pho' or x.get('nguoi') is True): M['b'].append(f"(b) shot {x.get('shot')}: lướt thấp không phải phố (noi thanh_pho) hay khoảnh khắc người (nguoi: true)")
    nog = [x for x, a, b in D if goc_of(x, E) is None]
    return r(loi=sum(M.values(), []), thieu=[f'{len(nog)} shot log không có `goc`'] if nog else [], muc=M, sat_nguong=sat('lướt thấp %', round(pc, 1), TL_THAP_PCT),
             val=f'lướt thấp {len(th)} shot · {s:.1f} s = {pc:.1f} % · ngưỡng hiệu chỉnh sau V7-PILOT')


def tl3(E, TL, LS=None, why=None):
    if LS is None: return r(thieu=[f'(a) {why}'], val='—')
    M = {'a': [], 'b': [], 'c': []}; th = []; D = shot_durs(E, TL, LS); n3 = 0; near = []
    nog = [str(x.get('shot')) for x, a, b in D if goc_of(x, E) is None]
    for x, a, b in D:
        g = goc_of(x, E)
        if g not in ('cao', 'thap', 'neo'): continue
        n3 += 1; tl_ = x.get('tl') is True; ev = bool(x.get('su_kien'))
        if not tl_ and not ev: M['a'].append(f"(a) shot {x.get('shot')} ({g}, {b - a:.1f} s): không thời gian chạy, không biến cố thấy được")
        tp = x.get('trong_pct')
        if tp is None: th.append(f"(b) shot {x.get('shot')}: không có trong_pct")
        else:
            if float(tp) > TRONG_PCT and not tl_: M['b'].append(f"(b) shot {x.get('shot')}: trống {float(tp):.1f} % > {TRONG_PCT:g} % mà không có thời gian chạy")
            near += sat(f"shot {x.get('shot')} trống %", round(float(tp), 1), TRONG_PCT)
        if not str(x.get('bac') or '').strip(): M['c'].append(f"(c) shot {x.get('shot')}: không ghi `bac` căn cứ")
    th2 = ([f'(b) {len(th)} shot 3D không có trong_pct (đầu: {th[0][4:]})'] if th else []) + ([f'(a) {len(nog)} shot log không có `goc` — không biết shot nào là 3D'] if nog else [])
    return r(loi=sum(M.values(), []), thieu=th2, muc=M, sat_nguong=near, val=f'{n3} shot 3D · không đổi {len(M["a"])} · trống {len(M["b"])} · thiếu trong_pct {len(th)}')


# ------------------------------------------------------------------ NHIP-NGHIA §13.2
def nhip_nghia(E, TL, NV=None, why=None):
    if NV is None: return r(thieu=[why], val='—')
    N = NV.get('nhip') if isinstance(NV, dict) else NV; SG = {s['id']: s for s in E.get('segments') or []}
    CH = {c['seg'] for c in the_chuong(E, TL)}; loi = []; ok = 0; main = [x for x in N or [] if x.get('chinh', True)]
    if not main: return r(thieu=['bảng nhịp không có nhịp chính (chinh: true)'], val='0 nhịp')
    for x in main:
        good = []
        for v in x.get('vat') or []:
            lo, sh = v.get('loai'), str(v.get('shot') or '')
            if lo not in VAT_LOAI: loi.append(f"nhịp {x.get('id')}: vật loại {lo!r} ngoài {'/'.join(sorted(VAT_LOAI))}"); continue
            if SG and sh not in SG: loi.append(f"nhịp {x.get('id')}: shot {sh!r} không có trong đặc tả"); continue
            if lo == 'the_chuong' and sh not in CH: loi.append(f"nhịp {x.get('id')}: vật the_chuong nhưng shot {sh} không có thẻ chương"); continue
            good.append(v)
        ok += bool(good)
    pc = 100 * ok / len(main)
    if pc < NHIP_PCT: loi.insert(0, f'nhịp chính có vật mang nghĩa {ok}/{len(main)} = {pc:.1f} % < {NHIP_PCT:g} %')
    return r(loi=loi, sat_nguong=sat('phủ nhịp %', round(pc, 1), NHIP_PCT), val=f'{ok}/{len(main)} nhịp chính có vật mang nghĩa = {pc:.1f} %')


# ------------------------------------------------------------------ XEM-CAM §13.4
def xem_cam(XC=None, why=None, base='.'):
    if XC is None: return r(thieu=[why + ' — cổng XEM CÂM bắt buộc từ T3 (§13.4); K không tự chấm'], val='—')
    loi, th = [], []
    q = XC.get('cau_hoi') or []
    if len(q) != XC_CAU: loi.append(f'(a) {len(q)} câu hỏi ≠ {XC_CAU}')
    if XC.get('tat_tieng') is not True: loi.append('(a) không ghi tat_tieng: true (animatic phải tắt tiếng)')
    NC = XC.get('nguoi_cham') or []; ai = {str(x.get('id')) for x in NC if x.get('vai') == 'ai'}; cd = [x for x in NC if x.get('vai') == 'chu_du_an']
    if len(ai) < XC_AI: loi.append(f'(b) {len(ai)} người chấm AI < {XC_AI}')
    if not cd: loi.append('(b) không có kết quả chủ dự án xem tắt tiếng')
    sc = []
    for x in NC:
        d, t = x.get('dung'), x.get('tong', XC_CAU)
        if not isinstance(d, (int, float)): th.append(f"(c) {x.get('id')}: không có số câu đúng"); continue
        sc.append((str(x.get('id')), d, t))
        if t != XC_CAU: loi.append(f"(c) {x.get('id')}: chấm trên {t} câu ≠ {XC_CAU}")
        if d < XC_DAT: loi.append(f"(c) {x.get('id')} ({x.get('vai')}): {d}/{t} < {XC_DAT}/{XC_CAU}")
    if EMAIL.search(json.dumps(XC, ensure_ascii=False)): loi.append('(d) tệp kết quả chứa email (che email)')
    vp = XC.get('video')
    if vp and XC.get('video_sha256') and os.path.exists(_p(base, vp)):
        import hashlib
        h = hashlib.sha256(open(_p(base, vp), 'rb').read()).hexdigest()
        if h != XC['video_sha256']: loi.append(f'(e) SHA animatic {h[:12]}… ≠ video_sha256 đã chấm {XC["video_sha256"][:12]}… — chấm trên bản khác')
    near = sum((sat(f'{i} câu đúng', d, XC_DAT) for i, d, _ in sc), [])
    return r(loi=loi, thieu=th, sat_nguong=near, val=f"{len(q)} câu · AI {len(ai)} · chủ dự án {len(cd)} · " + ', '.join(f'{i} {d}/{t}' for i, d, t in sc))


# ------------------------------------------------------------------ PC-1 thước phục chế (§12.3; khiếu nại A-G1B-6)
def pc1(E, base):
    C = E.get('phuc_che')
    if not C: return na('tập không khai phuc_che: (không dùng ảnh phục chế)')
    try: K = _load(_p(base, C['kiem']))
    except Exception as e: return r(thieu=[f'không đọc được phuc_che.kiem: {e}'], val='—')
    V, loi, th, near = {}, [], [], []
    for anh, x in K.items():
        cc = (x or {}).get('cong_cu') or {}; bc = cc.get('bicubic')
        for k, y in cc.items():
            if k == 'bicubic': continue
            if not bc: V[(anh, k)] = None; continue
            d = round(float(y['canh_moi_pt']) - float(bc['canh_moi_pt']), 2); ok = d <= PC_DELTA and float(y['psnr']) >= float(bc['psnr'])
            V[(anh, k)] = (ok, d, round(float(y['psnr']) - float(bc['psnr']), 2)); near += sat(f'{anh} {k} Δ cạnh mới', d, PC_DELTA)
    for u in C.get('dung') or []:
        key = (str(u.get('anh')), str(u.get('cong_cu')))
        if key not in V: th.append(f'{key[0]} · {key[1]}: không có trong kiểm có đáp án'); continue
        if V[key] is None: th.append(f'{key[0]} · {key[1]}: không có mốc bicubic cùng ô'); continue
        ok, d, dp = V[key]
        if not ok: loi.append(f'{key[0]} · {key[1]}: Δ cạnh mới {d:+.2f} điểm % (≤ {PC_DELTA:g}), ΔPSNR {dp:+.2f} dB (≥ 0) — không được dùng')
    tb = '; '.join(f"{a} {k}: {'ĐẠT' if v and v[0] else 'TRƯỢT' if v else 'THIẾU mốc'} (Δ {v[1]:+.2f})" if v else f'{a} {k}: THIẾU mốc' for (a, k), v in V.items())
    return r(loi=loi, thieu=th, sat_nguong=near, bang={f'{a}|{k}': v for (a, k), v in V.items()}, val=f"{len(C.get('dung') or [])} ảnh dùng · " + tb)


# ------------------------------------------------------------------ K-LAI-2 (1.16; khiếu nại A-G1B-1)
def mo_ta(E, base):
    ph = (E.get('phat_hanh') or {}).get('mo_ta')
    if not ph: return None, 'không khai phat_hanh.mo_ta (mô tả + bình luận ghim)'
    try: return open(_p(base, ph), encoding='utf-8').read(), None
    except OSError as e: return None, f'không đọc được mô tả: {e}'


def k_lai2(E, TL, F, TX, base):
    """(a) log khung có cờ ai_image/ai_texture ở MỌI khung; (b) shot có khung AI ⇔ shot khai AI (đặc tả/log shot); (c) thẻ phương pháp nói AI;
    (d) mô tả có "AI use = Yes"; (e) nhãn "Surface detail AI-assisted" KHÔNG hiện trên hình (§12.1)."""
    loi, th = [], []
    if F is None: th.append('(a) không có lai.log_khung')
    else:
        miss = [x['f'] for x in F if not isinstance(x.get('ai_image'), bool) or not isinstance(x.get('ai_texture', False), bool)]
        if miss: loi.append(f'(a) {len(miss)} khung log không có cờ ai_image/ai_texture dạng true/false (đầu {miss[0]})')
        if all('shot' in x for x in F):
            seg_ai = {str(x['shot']).split('/')[0] for x in F if x.get('ai_image') or x.get('ai_texture')}
            spec_ai = {s['id'] for s in E.get('segments') or [] for sh in s.get('shots') or [] if any(_f(sh, k) for k in ('ai_image', 'ai_texture'))}
            LS, _ = log_shot(E, base)
            if LS: spec_ai |= {str(x.get('shot')) for x in LS if x.get('ai_image') or x.get('ai_texture')}
            khac = seg_ai - spec_ai
            if khac: loi.append(f"(b) đoạn có khung AI trong log nhưng đặc tả/log shot không khai: {', '.join(sorted(khac)[:6])}")
    txt = ' '.join(_pp_text(s) for _, _, _, s in pp_spans(E, TL))
    if not re.search(r'\bAI\b', txt): loi.append('(c) thẻ phương pháp không nói AI dùng vào việc gì')
    mt, why = mo_ta(E, base)
    if mt is None: th.append(f'(d) {why}')
    elif not re.search(r'AI use[^\n]{0,12}?(=|:)\s*\**\s*Yes', mt, re.I): loi.append('(d) mô tả không có "AI use = Yes"')
    if TX is not None:
        hit = sorted(f for f, it in TX.items() for x in it if _vis(x) and (x.get('role') == 'ai_label' or re.search(r'AI-assisted', str(x.get('s') or ''))))
        if hit: loi.append(f'(e) nhãn AI hiện trên hình ở {len(hit)} mẫu (đầu {mmss(hit[0] / FPS)}) — §12.1 bỏ nhãn khỏi hình')
    return r(loi=loi, thieu=th, val=f"thẻ phương pháp {'có' if re.search(r'[A-Za-z]', txt) else 'không'} · mô tả {'có' if mt else 'không'} · log chữ {'có' if TX is not None else 'không'}")


# ------------------------------------------------------------------ NC-H5 (1.16; khiếu nại A-G1B-2)
def has_counter(E, TL):
    H = dict(E.get('heroes') or {}, **((TL or {}).get('heroes') or {}))
    if any(str(v.get('hero') or '').startswith('tl/') and ((v.get('opt') or {}).get('year') is not None or (v.get('opt') or {}).get('counter')) for v in H.values()): return True
    return any((sh.get('p') or {}).get('counter') for s in E.get('segments') or [] for sh in s.get('shots') or [])


def nch5(E, TL, base):
    if not has_counter(E, TL): return na('tập không có bộ đếm năm (cảnh tl/* có opt.year/counter, hoặc p.counter)')
    M = {'a': [], 'b': []}; th = []; H = dict(E.get('heroes') or {}, **((TL or {}).get('heroes') or {}))
    NK, why = opt_file(E, 'nam_khung', base)
    if NK is None: th.append(f'(a) {why} — năm xây ≤ bộ đếm chưa đo ở cấp tập (bộ timelapse: hàng NC-H5 [bộ])')
    else:
        for x in NK:
            nd = x.get('nam_dem')
            for lop, y in (x.get('nam_max') or {}).items():
                if nd is not None and y is not None and float(y) > float(nd): M['a'].append(f"(a) shot {x.get('shot')}: lớp {lop} năm xây {y} > bộ đếm {nd}")
    LS, _ = log_shot(E, base); LSd = {str(x.get('shot')): x for x in LS or []}; GH = E.get('ghost') or {}
    gh = {}
    for s in E.get('segments') or []:
        for sh in s.get('shots') or []:
            p = sh.get('p') or {}; o = (H.get(p.get('hero')) or {}).get('opt') or {}
            for g in [p.get('ghost'), o.get('ghost')]:
                if g: gh.setdefault(str(g), set()).add(s['id'])
    mt, why2 = mo_ta(E, base)
    for g, segs in sorted(gh.items()):
        src = str((GH.get(g) or {}).get('nguon') or '') or next((str(LSd[k].get('nguon')) for k in sorted(segs) if k in LSd and LSd[k].get('nguon')), '')
        if not src.strip(): M['b'].append(f'(b) ghost {g}: không có nguồn (ghost.{g}.nguon / log shot nguon)'); continue
        if mt is None: th.append(f'(b) ghost {g}: {why2}'); continue
        names = [re.split(r'[\s(,]+\d|\s*\(', it.strip())[0].strip() for it in re.split(r'\s*[+;·]\s*', src) if it.strip()]
        if not any(len(n) >= 3 and n.lower() in mt.lower() for n in names): M['b'].append(f'(b) ghost {g}: nguồn "{src[:50]}" không có trong mô tả/bình luận ghim')
    return r(loi=sum(M.values(), []), thieu=th, muc=M, val=f"bộ đếm có · nam_khung {'có' if NK is not None else 'không'} · ghost {len(gh)} ({', '.join(sorted(gh)[:4])})")


# ------------------------------------------------------------------ BD-3 (1.16; khiếu nại A-G1B-3)
def bd3(E, TL, ep_dir, logs):
    from checks.ll import q_bando
    S = q_bando._shots(E, TL); C = q_bando.cfg_of(E, ep_dir); L = q_bando.load_logs(logs)
    LOP = {str(x.get('id')): x for x in (C['lop'] or {}).get('lop') or []}
    hist = {k: v for k, v in LOP.items() if v.get('loai') == 'bien_gioi_lich_su'}
    pairs = [(z, lid) for z in S for lid in q_bando._lops_of(z, LOP) if lid in hist]
    if not pairs: return na('không có lớp bien_gioi_lich_su hiện trong shot nào')
    loi, th = [], []; mt, why = mo_ta(E, ep_dir)
    for z, lid in pairs:
        Ly = hist[lid]
        if Ly.get('nam') is None or not str(Ly.get('nguon') or '').strip(): loi.append(f'(a) {q_bando._w(z)} lớp {lid}: manifest thiếu nam/nguon')
        if mt is None: th.append(f'(b) {why}')
        elif str(Ly.get('nguon') or '').strip() and str(Ly['nguon']).split(' (')[0].split(',')[0].strip().lower() not in mt.lower():
            loi.append(f"(b) lớp {lid}: nguồn ranh {Ly['nguon']!r} không có trong mô tả")
        fr = q_bando.frames_in(L, z)
        if fr:
            vis = [f for f, it, _ in fr if any(q_bando.LBL_RE.match(str(x.get('s', ''))) and _vis(x) for x in it)]
            if vis: loi.append(f'(c) {q_bando._w(z)} lớp {lid}: nhãn "approx. borders" hiện trên hình ở {len(vis)} khung log — §12.1 bỏ khỏi hình')
    return r(loi=loi, thieu=sorted(set(th)), val=f'{len(pairs)} cặp shot–lớp ranh · nhãn trong dữ liệu (manifest) + nguồn trong mô tả; không đòi trên hình')


# ------------------------------------------------------------------ ML1 (1.16): câu từ lời khoá khi chưa có căn chữ
def cau_tu_loi_khoa(path):
    """lời khoá .txt → [dict(i, seg, part, t0, t1, s)] (không có giờ: t0 = t1 = −1e9 nên mốc "@từ" không suy được)"""
    from checks.ll import q_mach
    txt = open(path, encoding='utf-8').read(); out = []
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith('#') or re.match(r'^[‹<\[]?[A-Z0-9]{1,4}[›>\]]?\s*$', line): continue
        cur = []
        for w in line.split():
            cur.append(w)
            if q_mach._end(w): out.append(dict(i=len(out), seg=None, part=None, t0=-1e9, t1=-1e9, s=' '.join(cur))); cur = []
        if cur: out.append(dict(i=len(out), seg=None, part=None, t0=-1e9, t1=-1e9, s=' '.join(cur)))
    return out


def claims_file(E, base):
    p = E.get('claims_md')
    if not p: return None
    return set(re.findall(r'^\|\s*([CS]\d+[a-z]?)\s*\|', open(_p(base, p), encoding='utf-8').read(), re.M))


# ------------------------------------------------------------------ miễn Q37 (khiếu nại A-G1B-5)
def q37_mien(E, TL):
    out = []
    for z in shot_list(E, TL):
        P = dict(z['sh'].get('p') or {}, **(z['spec'].get('p') or {})); S = z['spec']
        if S.get('khung_neo') or S.get('neo') or P.get('khung_neo') or P.get('neo'): out.append((z['t0'], z['t1'], 'khung_neo', f"{z['seg']}/{z['i']}"))
        elif S.get('im_lang') or P.get('im_lang'): out.append((z['t0'], z['t1'], 'im_lang', f"{z['seg']}/{z['i']}"))
    return out


# ------------------------------------------------------------------ cả bộ 1.16
ROWS = ('SACH-1', 'CHUONG-1', 'PP-1', 'TL-1', 'TL-2', 'TL-3', 'NHIP-NGHIA', 'XEM-CAM', 'PC-1')


def check(E, TL=None, ep_dir='.', logs=None, video=None, log_shot_path=None, VF=None):
    if not ap_116(E): return {k: na('tập trước T3 (không khai khung_sach/kenh2_tu_t3): giữ hành vi 1.15') for k in ROWS}
    TX, step, W, H = text_frames(TL, logs, E.get('log_chu'), ep_dir)
    LS, why = log_shot(E, ep_dir, log_shot_path)
    NV, wn = opt_file(E, 'nhip_vat', ep_dir); XC, wx = opt_file(E, 'xem_cam', ep_dir)
    out = {}
    for k, fn in (('SACH-1', lambda: sach1(E, TL, TX, step)), ('CHUONG-1', lambda: chuong1(E, TL, TX, step, W, H)), ('PP-1', lambda: pp1(E, TL)),
                  ('TL-1', lambda: tl1(E, TL, LS, why, video, VF)), ('TL-2', lambda: tl2(E, TL, LS, why)), ('TL-3', lambda: tl3(E, TL, LS, why)),
                  ('NHIP-NGHIA', lambda: nhip_nghia(E, TL, NV, wn)), ('XEM-CAM', lambda: xem_cam(XC, wx, ep_dir)), ('PC-1', lambda: pc1(E, ep_dir))):
        try: out[k] = fn()
        except Exception as e: out[k] = r(thieu=[f'không chạy được: {type(e).__name__}: {e}'], val='—')
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    from checks.ll import base as _b
    E = _b.load(a[0]); TL = json.load(open(g('tl'))) if g('tl') else None
    R = check(E, TL, os.path.dirname(os.path.abspath(a[0])), g('logs'), g('video'), g('log-shot'))
    for k, v in R.items():
        print(f"{k} {v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')} · {v['val']}" + ''.join('\n  ' + x for x in (v['loi'] + v['thieu'])[:20])
              + ('\n  sát ngưỡng: ' + '; '.join(v['sat_nguong']) if v.get('sat_nguong') else ''))
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1, default=str)
