#!/opt/cine/bin/python
"""Luật kênh 2 bản 1.16.1 (phiên K-1.16, 19/10/2026; K-1.16.1 cùng ngày: thước cắt cấu trúc + duyệt K116-D1…D9) — CHỈ cho tập kênh 2 từ T3; tập cũ
giữ đúng hành vi 1.15.
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

Hàng (cấp ở cap112.py — chủ dự án duyệt K116-D1…D9 19/10 18:48; ngưỡng TL "hiệu chỉnh sau V7-PILOT"):
  SACH-1  Khung sạch §12.1 + TL-4: (a) không tấm số/câu trích (p.so, thẻ num/quote/list ngoài thẻ chương/phương pháp); (b) không tư liệu đứng riêng
          (photo/document/record/footage) — chỉ phủ lên địa hình `p.phu_dia_hinh` ≤ 3 s; (c) log chữ: không vai/chữ bị cấm hiện (alpha > 0);
          (d) chip nơi (vai where) mỗi lần ≤ 3 s; (e) chữ bản đồ (K116-D3, Chặn từ 1.16.1): nhãn địa danh (diem, inset, tag) ≤ 2/shot,
          hiện trong ≤ 3 s; chú giải chữ (chu_giai) và chữ khác (index, card, vai lạ) là lỗi;
          (f) mọi shot `p.sach: true`.
  CHUONG-1 Thẻ chương §13.3: (a) ≤ 8/tập; (b) "năm — cụm ≤ 6 từ"; (c) ≤ 3 s; (d) không trong móc mở đầu (chương 0 / part CH0 / t < moc_s);
          (e) lời trung tính (không captur*/liberat*/conquer*/seiz*); (f) log: góc dưới trái + mờ vào/ra — Cảnh báo.
  PP-1    Thẻ phương pháp D6: (a) đúng 2 thẻ; (b) mỗi thẻ 7–9 s (≈ 8 s); (c) liền nhau, kết ở cuối phim; (d) nói đủ nguồn/bản đồ, chỗ ước tính, AI;
          (e) tốc độ đọc ≤ 3 từ/s — Cảnh báo.
  TL-1    §13.6 TL-1: (a) góc cao có thời gian chạy ≥ 75 % thân phim (trừ thẻ phương pháp); (b) số shot đặc tả = cận trên số cắt (chỉ báo); (c) cắt/phút
          đo trên video ≤ 5 (1.16.1: cắt = đổi CẤU TRÚC — tương quan gradient sau cân bằng histogram + bù tịnh tiến, bỏ dải chữ dưới; đối chiếu ranh shot
          đặc tả ±0,5 s, báo cả hai số); (d) góc cao trôi ≤ 2 % khung/s (tịnh tiến phase correlation + phóng LK, trung vị shot); (e) 6–8 điểm máy cao; (f) mỗi điểm máy
          ≥ 2 năm khác nhau.
  TL-2    §13.6 TL-2: (a) lướt thấp ≤ 10 %; (b) mỗi shot lướt thấp có `vai` và là phố (noi thanh_pho) hoặc khoảnh khắc người (`nguoi: true`).
  TL-3    §13.6 TL-3: (a) shot 3D có thời gian chạy hoặc biến cố thấy được; (b) "trống": trong_pct > 60 % mà không có thời gian chạy; (c) ghi `bac`.
  NHIP-NGHIA §13.2: nhịp chính có ≥ 1 vật mang nghĩa hợp lệ ≥ 90 %.
  XEM-CAM  §13.4: kết quả chấm có đủ (8 câu, 3 AI + chủ dự án, tắt tiếng); đạt = chủ dự án ≥ 6/8 VÀ trung bình người chấm AI ≥ 6/8 (K116-D2). K KHÔNG tự chấm.
  PC-1    §12.3 phục chế (khiếu nại A-G1B-6): cạnh mới so với MỐC BICUBIC cùng ô: Δ ≤ 1,0 điểm % và PSNR ≥ bicubic; ảnh dùng phải đạt.
Thay cho luật cũ ở tập từ T3 (khiếu nại chấp nhận): K-LAI-2 (k_lai2), NC-H5 (nch5), BD-3 (bd3); ML1 đọc lời khoá (cau_tu_loi_khoa).
Trong ±5 % quanh ngưỡng: nêu tên.
1.17.3 (khiếu nại BAN-CUOI-T3): TL-3 nhận trong_pct [[t, %], …] (tb_pct, A1); SACH-1 nhận chữ thẻ chương / thẻ PP theo đặc tả (A6).
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
CUT_Y = (0.06, 0.70)                                       # thước cắt 1.16.1: vùng đo — bỏ dải chữ dưới (phụ đề nung, thẻ chương, bộ đếm) và mép trên
CUT_S, CUT_DS, CUT_W, CUT_TOL = 0.30, 0.40, 0.5, 0.5       # cắt: tương quan cấu trúc < 0,30 VÀ thấp hơn trung vị ±0,5 s ≥ 0,40; đối chiếu đặc tả ±0,5 s
CUT_GRID, CUT_DARK, CUT_SHIFT = (4, 3), 2.0, 0.04          # ô 4×3 · khung tối/phẳng (σ xám < 2/255) bỏ qua · bù tịnh tiến ≤ 4 % bề ngang
LBL_X0, LBL_Y0 = 0.10, 0.66
CROP_Y = (0.10, 0.68)                                      # vùng đo chuyển động máy (theo chiều cao khung)
VAT_LOAI = {'co_chu_quyen', 'dem_nam', 'ranh_dong', 'mui_ten', 'su_kien', 'the_chuong'}
MAP_LABEL_ROLES, MAP_LABEL_N, MAP_LABEL_S = {'diem', 'inset', 'tag'}, 2, 3.0   # K116-D3 (duyệt 19/10 18:48): bản đồ phủ địa hình ≤ 2 nhãn địa danh, hiện trong ≤ 3 s
LEGEND_ROLES = {'chu_giai'}                                # K116-D3: KHÔNG chú giải chữ — phe bằng màu + cờ
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
def sach1(E, TL, TX=None, step=12, mh=None):
    """mh = [(id, t0, t1)] shot minh hoạ (1.17, §14.1 (c)): nhãn "Illustration" (vai minh_hoa hoặc đúng chữ đó) trong các shot này hợp lệ."""
    M = {k: [] for k in 'abcdef'}; S = shot_list(E, TL); PP = {x[0] for x in pp_spans(E, TL)}
    for z in S:
        p = z['sh'].get('p') or {}; ps = z['spec'].get('p') or {}; P = dict(p, **ps); w = f"{z['seg']}/{z['i']} @{mmss(z['t0'])}"
        if z['seg'] in PP: continue
        if P.get('so'): M['a'].append(f'(a) {w}: số/câu trích trên hình (p.so: {str((P["so"][0] or {}).get("s") if isinstance(P["so"], list) and P["so"] else P["so"])[:40]!r}) — TL-4: lời + CC mang')
        c = P.get('card') or {}
        if (z['ty'] == 'card' or c) and not P.get('the_chuong') and not P.get('the_phuong_phap'):
            M['a'].append(f"(a) {w}: tấm {c.get('type') or 'card'} đứng riêng ({str(c.get('big') or c.get('title') or c.get('s') or '')[:30]!r}) — TL-4")
        doc = z['ty'] in DOC_TYPES or z['sh'].get('tpl') in ('footage', 'archive') or P.get('clip') or P.get('photo')
        if doc and P.get('that') and (E.get('kenh2_tu_t4') or E.get('n2p')): doc = False   # 1.17.7 (tập từ T4): ảnh/footage thật toàn khung (`p.that`) là shot hợp lệ — TU-LIEU-10/OMNI/THAT kiểm
        if doc:
            ov = P.get('phu_dia_hinh')
            dur = float((ov or {}).get('dur') or 0) if isinstance(ov, dict) else 0.0
            if not ov: M['b'].append(f'(b) {w}: tư liệu đứng riêng ({z["ty"]}, {z["t1"] - z["t0"]:.1f} s) — TL-4: chỉ phủ lên địa hình ≤ {DOC_S:g} s')
            elif dur <= 0 or dur > DOC_S + 1e-6: M['b'].append(f'(b) {w}: tư liệu phủ địa hình {dur:.2f} s (cần 0 < dur ≤ {DOC_S:g} s)')
        if not P.get('sach'): M['f'].append(f'(f) {w}: shot không bật lọc khung sạch (p.sach)')
    th, nv, chip, nl = [], 0, [], []
    # 1.17.3 (khiếu nại A6 BAN-CUOI-T3): chữ của thẻ chương (§13.3) và thẻ phương pháp (§12.1 (b), D6) nhận theo ĐẶC TẢ, không chỉ theo tên vai log:
    # mọi chữ trong khoảng giờ của đoạn thẻ phương pháp (pp_spans — PP-1 xét nội dung); chữ trùng nguyên văn thẻ chương khai ở đặc tả (p.the_chuong)
    # trong khoảng [at, at + dur] ± 1 bước mẫu (CHUONG-1 xét dạng/thời lượng). Ngoài hai khoảng đó vẫn xét như 1.16.1.
    PPT = [(a, b) for _, a, b, _ in pp_spans(E, TL)]
    CHT = [(re.sub(r'\s+', ' ', c['s']).strip().lower(), c['t0'], c['t0'] + c['d']) for c in the_chuong(E, TL) if c['nguon'] == 'đặc tả' and c['d'] > 0]
    n_the = {'pp': 0, 'chuong': 0}
    if TX is None: th.append('(c) không có log chữ (--logs k2.js) — không đo được chữ thực hiện trên hình; (d) chip nơi chưa đo')
    else:
        by_role = {}; nhan = {}   # nhan: shot → {chữ: [khung]} (nhãn địa danh K116-D3)
        def shot_of(f):
            t = f / FPS
            return next((f"{z['seg']}/{z['i']}" for z in S if z['t0'] - 1e-6 <= t < z['t1']), '?')
        for f, it in TX.items():
            for x in it:
                if not _vis(x): continue
                ro, s_ = str(x.get('role') or ''), str(x.get('s') or '')
                nv += 1
                if mh and (ro == 'minh_hoa' or s_.strip() == 'Illustration') and any(t0 - 1e-6 <= f / FPS < t1 for _, t0, t1 in mh): continue   # 1.17 §14.1 (c)
                if any(a - 1e-6 <= f / FPS < b + 1e-6 for a, b in PPT): n_the['pp'] += 1; continue   # 1.17.3 A6: thẻ phương pháp
                if ro not in OK_ROLES and any(re.sub(r'\s+', ' ', s_).strip().lower() == k and a - step / FPS - 1e-6 <= f / FPS <= b + step / FPS + 1e-6 for k, a, b in CHT):
                    n_the['chuong'] += 1; continue   # 1.17.3 A6: thẻ chương khai ở đặc tả (log ghi vai khác `the_chuong`)
                if ro in OK_ROLES:
                    if ro == 'where': by_role.setdefault(s_, []).append(f)
                    continue
                if ro in BANNED_ROLES or BANNED_TXT.search(s_): by_role.setdefault(('BAN', ro), []).append((f, s_))
                elif ro in MAP_LABEL_ROLES: nhan.setdefault(shot_of(f), {}).setdefault(s_, []).append(f)
                else: by_role.setdefault(('KHAC', ro), []).append((f, s_))
        for k, v in by_role.items():
            if isinstance(k, tuple):
                f0, s_ = min(v)
                why = '' if k[0] == 'BAN' else (' — chú giải chữ (K116-D3: phe bằng màu + cờ)' if k[1] in LEGEND_ROLES else ' — chữ ngoài danh sách §12.1 + K116-D3')
                (M['c'] if k[0] == 'BAN' else M['e']).append(f"({'c' if k[0] == 'BAN' else 'e'}) vai {k[1] or '—'}: {len(v)} mẫu hiện, đầu tiên {mmss(f0 / FPS)} {s_!r}" + why)
            else:
                for f0, f1 in _runs(v, step):
                    d = _run_s(f0, f1, step); chip.append(d)
                    if d > CHIP_S + step / FPS / 2: M['d'].append(f'(d) chip nơi {k!r} @{mmss(f0 / FPS)}: {d:.2f} s > {CHIP_S:g} s')
        for sh, L in sorted(nhan.items()):   # K116-D3: ≤ 2 nhãn địa danh mỗi shot, hiện trong ≤ 3 s (từ lúc nhãn đầu hiện tới lúc nhãn cuối tắt)
            fs = sorted(f for v in L.values() for f in v); d = _run_s(fs[0], fs[-1], step); nl.append(d)
            if len(L) > MAP_LABEL_N: M['e'].append(f"(e) shot {sh} @{mmss(fs[0] / FPS)}: {len(L)} nhãn địa danh > {MAP_LABEL_N} ({', '.join(repr(x) for x in list(L)[:4])})")
            if d > MAP_LABEL_S + step / FPS / 2: M['e'].append(f"(e) shot {sh} @{mmss(fs[0] / FPS)}: nhãn địa danh hiện {d:.2f} s > {MAP_LABEL_S:g} s")
    loi = sum(M.values(), [])
    near = (sat('chip nơi dài nhất s', round(max(chip), 2), CHIP_S) if chip else []) + (sat('nhãn địa danh dài nhất s', round(max(nl), 2), MAP_LABEL_S) if nl else [])
    return r(loi=loi, thieu=th, muc=M, sat_nguong=near,
             val=f"{len(S)} shot · tấm số/trích {len(M['a'])} · tư liệu đứng riêng {len(M['b'])} · " + (f"log chữ {nv} mục hiện · cấm {len(M['c'])} · chip {len(chip)} lần, dài nhất {max(chip or [0]):.2f} s · nhãn địa danh {len(nl)} shot, dài nhất {max(nl or [0]):.2f} s · lỗi chữ bản đồ/khác {len(M['e'])}" if TX is not None else 'không log chữ')
                 + (f" · chữ thẻ theo đặc tả (1.17.3): PP {n_the['pp']} mẫu, chương {n_the['chuong']} mẫu" if TX is not None and (n_the['pp'] or n_the['chuong']) else ''))


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
    # 1.17.2 (quyết định chủ dự án 22/10/2026 11:09 — không câu AI trong phim): (d) = nói nguồn/bản đồ + chỗ ước tính; bỏ "AI dùng vào việc gì"
    # (công bố AI chuyển sang mô tả + cài đặt YouTube: CONG-BO-1). Không thêm luật cấm chữ.
    for k, rg in (('nguồn/bản đồ', r'\b(source|sources|map|maps|record|records|archive|registers?|built from)\b'), ('chỗ ước tính', r'\b(estimat\w*|approximat\w*|reconstruct\w*|illustrative)\b')):
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


def _cau_truc(f):
    """khung xám → (ảnh cân bằng histogram, biên độ gradient Sobel, σ xám thô) trên vùng CUT_Y. Cân bằng histogram bỏ độ sáng/tương phản toàn khung
    (ngày–đêm, chớp đèn, khói mỏng) trước khi lấy cấu trúc."""
    import cv2, numpy as np
    h = f.shape[0]; c = f[int(CUT_Y[0] * h):int(CUT_Y[1] * h)]
    e = cv2.equalizeHist(np.ascontiguousarray(c)); b = cv2.GaussianBlur(e, (0, 0), 1.2).astype(np.float32)
    return e.astype(np.float32), np.hypot(cv2.Sobel(b, cv2.CV_32F, 1, 0), cv2.Sobel(b, cv2.CV_32F, 0, 1)), float(c.std())


def tuong_quan_cau_truc(A, B):
    """tương quan cấu trúc của hai khung đã qua _cau_truc: bù tịnh tiến (phase correlation trên ảnh cân bằng, ≤ CUT_SHIFT bề ngang), rồi hệ số
    tương quan Pearson của bản đồ gradient trên từng ô lưới CUT_GRID; trả trung vị các ô có cấu trúc (σ > 0). Cùng góc máy đổi sáng/màu → cao;
    đổi cảnh → ≈ 0. → [-1, 1]"""
    import cv2, numpy as np
    (ea, ga, _), (eb, gb, _) = A, B
    (dx, dy), _ = cv2.phaseCorrelate(ea, eb); H, W = ga.shape; lim = CUT_SHIFT * W
    dx, dy = (int(round(dx)), int(round(dy))) if abs(dx) <= lim and abs(dy) <= lim else (0, 0)
    a = ga[max(0, -dy):H - max(0, dy), max(0, -dx):W - max(0, dx)]; b = gb[max(0, dy):H - max(0, -dy), max(0, dx):W - max(0, -dx)]
    nx, ny = CUT_GRID; th, tw = a.shape[0] // ny, a.shape[1] // nx
    ta = a[:th * ny, :tw * nx].reshape(ny, th, nx, tw).transpose(0, 2, 1, 3).reshape(nx * ny, -1)
    tb = b[:th * ny, :tw * nx].reshape(ny, th, nx, tw).transpose(0, 2, 1, 3).reshape(nx * ny, -1)
    ta = ta - ta.mean(axis=1, keepdims=True); tb = tb - tb.mean(axis=1, keepdims=True)
    sa, sb = np.sqrt((ta * ta).sum(axis=1)), np.sqrt((tb * tb).sum(axis=1)); ok = (sa > 1e-3) & (sb > 1e-3)
    if not ok.any(): return 1.0
    return float(np.median((ta[ok] * tb[ok]).sum(axis=1) / (sa[ok] * sb[ok])))


def chuoi_cau_truc(F):
    """→ mảng s[i] = tương quan cấu trúc khung i với khung sáng gần nhất trước nó (nan: khung tối/phẳng σ < CUT_DARK, hoặc khung 0)"""
    import numpy as np
    s = np.full(len(F), np.nan); prev = None
    for i, f in enumerate(F):
        P = _cau_truc(f)
        if P[2] < CUT_DARK: continue
        if prev is not None: s[i] = tuong_quan_cau_truc(prev, P)
        prev = P
    return s


def cuts_video(F, fps, S=None):
    """cắt (1.16.1, thay thước histogram + điểm ảnh của 1.16.0) = khung i (bỏ 0,5 s đầu) mà đổi CẤU TRÚC so với khung sáng trước:
    s[i] = tương_quan_cấu_trúc < CUT_S VÀ trung vị s trong ±CUT_W s (trừ i±1) − s[i] ≥ CUT_DS; là cực tiểu ±2 khung; cách cắt trước > 2 khung.
    Đo trên vùng y CUT_Y (bỏ phụ đề/chữ dưới), sau cân bằng histogram (bỏ độ sáng/màu toàn khung) và bù tịnh tiến. Đổi ngày–đêm, chớp đèn, khói,
    nhà mọc dần cùng góc máy KHÔNG là cắt; cắt cứng giữa hai cảnh cùng độ sáng LÀ cắt. Hiệu chuẩn có đáp án: reports/k1161/K1161-BAO-CAO.md §3. → [giây]"""
    import numpy as np
    n = len(F)
    if n < 2: return []
    s = chuoi_cau_truc(F) if S is None else S
    w = max(2, int(round(CUT_W * fps))); out = []
    for i in range(max(1, int(0.5 * fps)), n):
        if np.isnan(s[i]) or s[i] >= CUT_S: continue
        nb = np.r_[s[max(1, i - w):max(1, i - 1)], s[i + 2:i + w + 1]]; nb = nb[~np.isnan(nb)]
        med = float(np.median(nb)) if len(nb) else 1.0
        loc = s[max(1, i - 2):i + 3]; loc = loc[~np.isnan(loc)]
        if med - s[i] >= CUT_DS and s[i] <= loc.min() + 1e-9 and (not out or i - out[-1] > 2): out.append(i)
    return [i / fps for i in out]


def doi_chieu_cat(cv, cs, tol=CUT_TOL):
    """ghép một-một cắt video cv với ranh shot đặc tả cs (lệch ≤ tol s, gần nhất trước) → (số khớp, [cắt chỉ ở video], [ranh chỉ ở đặc tả])"""
    used, miss = set(), []
    for t in cs:
        c = [j for j, x in enumerate(cv) if j not in used and abs(x - t) <= tol]
        if c: used.add(min(c, key=lambda j: abs(cv[j] - t)))
        else: miss.append(t)
    return len(used), [x for j, x in enumerate(cv) if j not in used], miss


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


def _n_goc(x):
    """shot log khai R3: `so_goc` (số nguyên) hoặc `goc_may` (danh sách) → (số góc, [giây trong shot của các lần cắt góc] | None)"""
    g = x.get('goc_may')
    if isinstance(g, list) and g:
        ts = [float(y['t']) for y in g if isinstance(y, dict) and isinstance(y.get('t'), (int, float)) and y['t'] > 0]
        return len(g), (sorted(ts) if len(ts) == len(g) - 1 else None)
    n = x.get('so_goc')
    return (int(n), None) if isinstance(n, (int, float)) and not isinstance(n, bool) else (None, None)


def cat_r3(D, cv):
    """1.17.2 (V2-D7, duyệt 22/10 11:09): cắt video trong shot khai R3 (`so_goc`/`goc_may` ≥ 2) được miễn trần cắt/phút — mỗi shot tối đa
    (số góc − 1) cắt nằm TRONG shot (cách hai ranh shot > CUT_TOL); `goc_may` có `t` (giây trong shot) → chỉ miễn cắt khớp ±CUT_TOL. → [giây cắt miễn]"""
    out = []
    for x, a, b in D:
        n, ts = _n_goc(x)
        if not n or n < 2: continue
        inner = [c for c in cv if a + CUT_TOL < c < b - CUT_TOL and c not in out]
        if ts is not None: inner = [c for c in inner if any(abs(c - (a + t)) <= CUT_TOL for t in ts)]
        out += inner[:n - 1]
    return sorted(out)


def tl1(E, TL, LS=None, why=None, video=None, VF=None):
    T = tong(E, TL); PPd = sum(b - a for _, a, b, _ in pp_spans(E, TL)); Tb = T - PPd; M = {k: [] for k in 'abcdef'}; th = []; near = []
    from checks.ll import q_k117, q_k1177
    ap_r3 = q_k117.ap_117(E)   # 1.17.2: miễn cắt góc R3 chỉ tập từ T3 (như mọi luật 1.17)
    ap_77 = q_k1177.ap_1177(E)   # 1.17.7 (P9, tập từ T4): miễn ranh vào/ra M-d + tư liệu/ảnh thật khỏi cắt/phút
    tv = E.get('tl1_muc_tieu_pct'); TL_CAO_PCT = float(tv) if isinstance(tv, (int, float)) and not isinstance(tv, bool) and 0 < tv <= 100 else globals()['TL_CAO_PCT']   # 1.17.7 GOC-CAO (e)
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
    vt = ''; cvn = None
    if VF is not None or video:
        try:
            F, fps = VF if VF is not None else video_gray(video)
            cv = cuts_video(F, fps); Tv = len(F) / fps; Tvb = max(1e-6, Tv - PPd); cpm_v = len([c for c in cv if c < Tv - PPd]) / (Tvb / 60)
            nk, chi_v, chi_s = doi_chieu_cat(cv, cuts_s); cvn = dict(n=len(cv), khop=nk, chi_video=len(chi_v), chi_dac_ta=len(chi_s))   # 1.16.1: đối chiếu ranh shot đặc tả (±CUT_TOL s), báo cả hai số
            cr3 = cat_r3(D, [c for c in cv if c < Tv - PPd]) if ap_r3 else []   # 1.17.2 (V2-D7): cắt góc trong shot khai R3 không tính vào trần
            cmd = q_k1177.cat_mien(q_k1177.ranh_mien(LS), [c for c in cv if c < Tv - PPd], CUT_TOL, cr3) if ap_77 else []   # 1.17.7 (P9)
            cpm_t = (len([c for c in cv if c < Tv - PPd]) - len(cr3) - len(cmd)) / (Tvb / 60); cvn.update(r3=len(cr3), cpm_tho=round(cpm_v, 2), cpm_tran=round(cpm_t, 2))
            if ap_77: cvn.update(mien_md_tl=len(cmd), cpm_truoc_mien=round((len([c for c in cv if c < Tv - PPd]) - len(cr3)) / (Tvb / 60), 2))
            r3t = (f' − {len(cr3)} cắt góc R3 (so_goc/goc_may)' + (f' − {len(cmd)} ranh vào/ra M-d/tư liệu/ảnh thật (1.17.7; trước miễn {cvn["cpm_truoc_mien"]:.2f}/phút)' if ap_77 else '')
                   + f' = {cpm_t:.2f}/phút tính trần') if ap_r3 else ''
            if cpm_t > TL_CUT_MIN: M['c'].append(f'(c) video: {len(cv)} cắt đo / {Tvb / 60:.2f} phút = {cpm_v:.2f} cắt/phút{r3t} > {TL_CUT_MIN:g} (đặc tả {len(cuts_s)} ranh = {cpm_s:.2f}/phút; khớp ±{CUT_TOL:g} s {nk})')
            near += sat('cắt/phút (video, tính trần)', round(cpm_t, 2), TL_CUT_MIN); dr = []
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
            vt = (f' · video {len(cv)} cắt = {cpm_v:.2f}/phút (thô){r3t} · đặc tả {len(cuts_s)} ranh = {cpm_s:.2f}/phút · khớp ±{CUT_TOL:g} s {nk}'
                  + f' (chỉ video {len(chi_v)}' + (f': {", ".join(mmss(x) for x in chi_v[:6])}{"…" if len(chi_v) > 6 else ""}' if chi_v else '')
                  + f'; chỉ đặc tả {len(chi_s)} — cùng góc máy đổi năm/giờ hoặc chưa cắt)' + (f' · trôi góc cao trung vị {statistics.median(dr):.2f} %/s ({len(dr)} shot)' if dr else '')
                  + (f' · (tham khảo, chưa có goc) trôi máy shot 3D: trung vị {statistics.median(d3):.2f} %/s, ≤ {TL_DRIFT:g} %/s ở {sum(v <= TL_DRIFT for v in d3)}/{len(d3)} shot' if d3 else ''))
        except Exception as e: th.append(f'(c) không đo được video: {e}')
    else: th.append(f'(c)(d) không có video (master/--tl16-video) — cắt/phút và trôi máy chưa đo (đặc tả: cận trên {cpm_s:.2f} cắt/phút)')
    return r(loi=sum(M.values(), []), thieu=th, muc=M, sat_nguong=near, cat_dac_ta=len(cuts_s), cat_video=cvn,
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


def tb_pct(v, dur):
    """1.17.3 (khiếu nại A1 BAN-CUOI-T3): trường % theo shot → số TB. Số → chính nó; [[t, %], …] / [{t, v|pct}] (khung mẫu, t giây trong shot)
    → trung bình theo thời gian (mẫu i giữ tới mẫu i+1, mẫu cuối tới hết shot; t thiếu → trung bình cộng); khác → None."""
    if isinstance(v, (int, float)) and not isinstance(v, bool): return float(v)
    xs = []
    for x in v if isinstance(v, list) else []:
        if isinstance(x, (list, tuple)) and len(x) == 2 and isinstance(x[1], (int, float)) and not isinstance(x[1], bool): xs.append((x[0], float(x[1])))
        elif isinstance(x, dict) and isinstance(x.get('v', x.get('pct')), (int, float)): xs.append((x.get('t'), float(x.get('v', x.get('pct')))))
    if not xs: return None
    if any(not isinstance(t, (int, float)) for t, _ in xs) or not dur: return sum(v_ for _, v_ in xs) / len(xs)
    xs = sorted((float(t), v_) for t, v_ in xs); w = []
    for j, (t, v_) in enumerate(xs):
        t1 = xs[j + 1][0] if j + 1 < len(xs) else max(dur, t); w.append((max(0.0, min(t1, dur) - max(t, 0.0)), v_))
    W = sum(d for d, _ in w)
    return sum(d * v_ for d, v_ in w) / W if W > 0 else sum(v_ for _, v_ in xs) / len(xs)


def tl3(E, TL, LS=None, why=None):
    if LS is None: return r(thieu=[f'(a) {why}'], val='—')
    M = {'a': [], 'b': [], 'c': []}; th = []; D = shot_durs(E, TL, LS); n3 = 0; near = []
    nog = [str(x.get('shot')) for x, a, b in D if goc_of(x, E) is None]
    for x, a, b in D:
        g = goc_of(x, E)
        if g not in ('cao', 'thap', 'neo'): continue
        n3 += 1; tl_ = x.get('tl') is True; ev = bool(x.get('su_kien'))
        if not tl_ and not ev: M['a'].append(f"(a) shot {x.get('shot')} ({g}, {b - a:.1f} s): không thời gian chạy, không biến cố thấy được")
        tp = tb_pct(x.get('trong_pct'), b - a)   # 1.17.3 (khiếu nại A1): số TB shot hoặc [[t, %], …] (dạng EO-DAT-R2) → TB theo thời gian
        if tp is None: th.append(f"(b) shot {x.get('shot')}: không có trong_pct" + (' đọc được (cần số hoặc [[t, %], …])' if x.get('trong_pct') is not None else ''))
        else:
            if tp > TRONG_PCT and not tl_: M['b'].append(f"(b) shot {x.get('shot')}: trống {tp:.1f} % > {TRONG_PCT:g} % mà không có thời gian chạy")
            near += sat(f"shot {x.get('shot')} trống %", round(tp, 1), TRONG_PCT)
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
    sc, sai = [], []   # K116-D2 (duyệt 19/10 18:48): đạt = chủ dự án ≥ 6/8 VÀ trung bình người chấm AI ≥ 6/8 (không còn "mỗi người ≥ 6/8")
    for x in NC:
        d, t = x.get('dung'), x.get('tong', XC_CAU)
        if not isinstance(d, (int, float)): th.append(f"(c) {x.get('id')}: không có số câu đúng"); continue
        sc.append((str(x.get('id')), d, t))
        if t != XC_CAU: loi.append(f"(c) {x.get('id')}: chấm trên {t} câu ≠ {XC_CAU}")
        if x.get('vai') == 'chu_du_an' and d < XC_DAT: loi.append(f"(c) {x.get('id')} (chủ dự án): {d}/{t} < {XC_DAT}/{XC_CAU}")
        if x.get('vai') == 'ai': sai.append(d)
    tb_ai = sum(sai) / len(sai) if sai else None
    if tb_ai is not None and tb_ai < XC_DAT - 1e-9: loi.append(f"(c) trung bình {len(sai)} người chấm AI {tb_ai:.2f}/{XC_CAU} < {XC_DAT}/{XC_CAU}")
    if EMAIL.search(json.dumps(XC, ensure_ascii=False)): loi.append('(d) tệp kết quả chứa email (che email)')
    vp = XC.get('video')
    if vp and XC.get('video_sha256') and os.path.exists(_p(base, vp)):
        import hashlib
        h = hashlib.sha256(open(_p(base, vp), 'rb').read()).hexdigest()
        if h != XC['video_sha256']: loi.append(f'(e) SHA animatic {h[:12]}… ≠ video_sha256 đã chấm {XC["video_sha256"][:12]}… — chấm trên bản khác')
    near = sum((sat(f'{i} câu đúng', d, XC_DAT) for i, d, _ in sc if i in {str(x.get('id')) for x in cd}), []) + (sat('TB AI câu đúng', round(tb_ai, 2), XC_DAT) if tb_ai is not None else [])
    return r(loi=loi, thieu=th, sat_nguong=near, val=f"{len(q)} câu · AI {len(ai)} · chủ dự án {len(cd)} · " + ', '.join(f'{i} {d}/{t}' for i, d, t in sc)
             + (f' · TB AI {tb_ai:.2f}/{XC_CAU}' if tb_ai is not None else ''))


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


def k_lai2(E, TL, F, TX, base, LS=None):
    """(a) log khung có cờ ai_image/ai_texture ở MỌI khung; (b) shot có khung AI ⇔ shot khai AI (đặc tả/log shot); (c) BỎ ở 1.17.2 (thẻ phương pháp
    nói AI — quyết định chủ dự án 22/10/2026 11:09: không câu AI trong phim); (d) mô tả có "AI use = Yes"; (e) nhãn "Surface detail AI-assisted"
    KHÔNG hiện trên hình (§12.1).
    1.17.2 (V2-D5): không có lai.log_khung mà log shot khai AI (đoạn `minh_hoa`, `ai_image`) → (a) đọc cờ `ai_image` ở MỌI shot log; (b) thêm chiều
    ngược: đoạn minh hoạ khai ở shot ghi `ai_image: false` là mâu thuẫn khai."""
    from checks.ll import q_k117
    loi, th = [], []
    if LS is None: LS, _ = log_shot(E, base)
    if LS:
        _, MT = q_k117.doan_ai(LS)
        if MT: loi.append(f"(b) đoạn minh hoạ khai trong log shot nhưng shot ghi ai_image: false: {', '.join(d['id'] for d in MT[:6])} — sửa log (bỏ mục đoạn, hoặc ai_image: true)")
    if F is None and LS and (q_k117.doan_ai(LS)[0] or any(x.get('ai_image') is True for x in LS)):
        miss = [str(x.get('shot')) for x in LS if not isinstance(x.get('ai_image'), bool)]
        if miss: th.append(f"(a) không có lai.log_khung; log shot thiếu cờ ai_image true/false ở {len(miss)} shot ({', '.join(miss[:6])})")
    elif F is None: th.append('(a) không có lai.log_khung')
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
    mt, why = mo_ta(E, base)
    if mt is None: th.append(f'(d) {why}')
    elif not re.search(r'AI use[^\n]{0,12}?(=|:)\s*\**\s*Yes', mt, re.I): loi.append('(d) mô tả không có "AI use = Yes"')
    if TX is not None:
        hit = sorted(f for f, it in TX.items() for x in it if _vis(x) and (x.get('role') == 'ai_label' or re.search(r'AI-assisted', str(x.get('s') or ''))))
        if hit: loi.append(f'(e) nhãn AI hiện trên hình ở {len(hit)} mẫu (đầu {mmss(hit[0] / FPS)}) — §12.1 bỏ nhãn khỏi hình')
    return r(loi=loi, thieu=th, val=f"thẻ phương pháp {'có' if re.search(r'[A-Za-z]', txt) else 'không'} (1.17.2: không đòi câu AI) · mô tả {'có' if mt else 'không'} · log chữ {'có' if TX is not None else 'không'}"
             + (' · cờ AI: log shot' if F is None and LS else ''))


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
    # 1.17.4 (K1173-D6, chủ dự án duyệt Q7 23/10/2026 21:45): đoạn thẻ phương pháp (D6: 2 thẻ × ≈ 8 s, cuối phim) miễn Q37 (c) như khung neo /
    # tấm im lặng. Chỉ nhận khối thẻ PP liền nhau KẾT ở cuối phim (± PP_END); trần ≤ 10 s/thẻ (q37: MIEN_MAX) và ≤ 2 thẻ (q37: PP_MIEN_N).
    PS = sorted(pp_spans(E, TL), key=lambda x: x[1]); T = tong(E, TL); khoi = []
    for x in reversed(PS):
        if (not khoi and abs(x[2] - T) <= PP_END) or (khoi and khoi[-1][1] - x[2] <= 0.05): khoi.append(x)
        elif khoi: break
    out += [(round(a, 3), round(b, 3), 'the_pp', str(sid)) for sid, a, b, _ in reversed(khoi)]
    return out


# ------------------------------------------------------------------ cả bộ 1.16
ROWS = ('SACH-1', 'CHUONG-1', 'PP-1', 'TL-1', 'TL-2', 'TL-3', 'NHIP-NGHIA', 'XEM-CAM', 'PC-1')


def check(E, TL=None, ep_dir='.', logs=None, video=None, log_shot_path=None, VF=None):
    if not ap_116(E): return {k: na('tập trước T3 (không khai khung_sach/kenh2_tu_t3): giữ hành vi 1.15') for k in ROWS}
    TX, step, W, H = text_frames(TL, logs, E.get('log_chu'), ep_dir)
    LS, why = log_shot(E, ep_dir, log_shot_path)
    NV, wn = opt_file(E, 'nhip_vat', ep_dir); XC, wx = opt_file(E, 'xem_cam', ep_dir)
    out = {}
    from checks.ll import q_k117
    MH = q_k117._mh_spans(LS) if LS else None   # 1.17: nhãn "Illustration" trong shot minh hoạ không là lỗi SACH-1
    for k, fn in (('SACH-1', lambda: sach1(E, TL, TX, step, MH)), ('CHUONG-1', lambda: chuong1(E, TL, TX, step, W, H)), ('PP-1', lambda: pp1(E, TL)),
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
