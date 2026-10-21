#!/opt/cine/bin/python
"""Luật kênh 2 bản 1.17.0 (phiên K-1.17, 21/10/2026) + 1.17.1 (phiên K-1.17.1, 21/10/2026: ngưỡng EO-DAT theo Kinh thánh §14.7 nguyên văn, thêm R4) — CHỈ tập kênh 2 từ T3 (`khung_sach: true` | `kenh2_tu_t3: true`, như 1.16); tập cũ giữ
đúng hành vi 1.16.1 (không thêm hàng). Luật N2+ (T4) ở q_n2p.py. Định nghĩa: checks/ll/RULES-LL.md mục "1.17".

Căn cứ: Kinh thánh kênh 2 §14.1 (c) N2 minh hoạ ≤ 20 %, nhãn "Illustration" suốt đoạn (ngoại lệ §12.1); §15 (T4, M-d); §14.7 R1–R4 eo đất
(1.17.0 viết khi §14.7 chưa có trên repo, ngưỡng R1/R2 K đề xuất tạm; 1.17.1 khớp §14.7 nguyên văn — docs/BIBLE-KENH2.md trên main @96b5017c,
SHA tệp 14ca13aa…: "R1 … chiếm ≥ 15–20 % khung", "R2 Đồng cỏ/cát trống (> 50 % khung) ≤ 6 s liên tục và ≤ 10 % thời lượng mỗi chương",
"R4 Câu lời không có vật trên eo đất → góc phố/lâu đài/cảng; bản đồ phủ ≤ 3 s (TL-4)").

Hàng (cấp ở cap112.py: Chặn ở cổng G2 · Cảnh báo ở animatic (`animatic: true` trong đặc tả) — như K116-D5; không khai → G2):
  MINH-HOA  shot log `minh_hoa: true` (T3 theo N2, T4 theo M-d): (a) tổng minh hoạ ≤ 20 % thời lượng; (b) nhãn "Illustration" hiện SUỐT đoạn —
            log chữ (`log_chu`/--logs: mục có chữ "Illustration") phủ mọi khung mẫu của shot, hoặc trường log shot `nhan_minh_hoa` (chữ) +
            `nhan_t` [t0, t1] (giây trong shot; không có = cả shot); không có cả hai → THIẾU (chưa có OCR — giới hạn đã biết); (c) đoạn KẸP giữa
            hai shot 3D (shot liền trước và liền sau có goc cao/thap/neo, không phải minh hoạ/thẻ); (d) máy ≤ 40 m AGL khi log có `agl_m`;
            (e) sổ AI có dòng cho mỗi đoạn: model + lệnh (lenh | prompt | lenh_sha | prompt_sha) + SHA đầu ra (sha_ra | sha_out | sha256) —
            trường log shot `so_ai` (dict hoặc list) hoặc tệp `so_ai:` của episode.yaml (.jsonl/.json, mục có `shot` = id đoạn).
  EO-DAT-R1 shot log `chu_the_eo_dat: true`: chủ thể chiếm khung (trường `chu_the_pct`: số TB shot hoặc [[t, %], …] từ mặt nạ ID; dùng
            trung vị): (a) < R1_MIN (15 %) → lỗi (Chặn ở G2); (b) R1_MIN ≤ chủ thể < R1_TOT (15–20 %) → Cảnh báo (vùng "15–20 %" của §14.7).
            Thiếu → THIẾU (tính như (a)).
  EO-DAT-R2 shot eo đất (`noi: eo_dat`), trường `trong_pct` (% cỏ/cát không vật; số TB shot, hoặc [[t, %], …] theo khung mẫu — từ mặt nạ ID);
            "trống" = trong_pct > TRONG_PCT (50 %): (a) giây trống LIÊN TỤC ≤ R2_GIAY (6 s, nối qua ranh shot); (b) mỗi chương: tổng giây
            trống ≤ R2_CHUONG (10 %) × THỜI LƯỢNG CHƯƠNG (mọi shot log của chương, không chỉ shot eo đất). Thiếu trong_pct → THIẾU.
  EO-DAT-R3 shot eo đất dài > 15 s: (a) ≥ 2 góc máy (trường `so_goc` số nguyên, hoặc `goc_may` danh sách); (b) biến cố thấy được cách nhau
            ≤ 6 s (log `su_kien[].t`, `tl_buoc[].t`, tính cả đầu/cuối shot).
  EO-DAT-R4 (1.17.1) shot log `loi_khong_vat_eo_dat: true` (câu lời nói về eo đất nhưng không có vật để thấy): (a) `noi` ∈ R4_NOI (pho |
            lau_dai | cang; `thanh_pho` coi là pho — tên log hiện dùng) HOẶC (b) bản đồ phủ `ban_do_phu` ≤ R4_BAN_DO (3 s, TL-4): số giây,
            [t0, t1], [[t0, t1], …] (xét lần phủ dài nhất) hoặc {dur}. Có `ban_do_phu` > 3 s → lỗi (b) dù noi hợp lệ (TL-4 là trần riêng).
            Không shot khai → KHÔNG ÁP.
Sửa luật cũ (khiếu nại 8 hàng Chặn animatic T3 chấp nhận — báo cáo §4), chỉ khi ap_117:
  Q33 / Q33-K2 / Q33 (1.13): lần xuất hiện cùng (cảnh, góc) — khai hay pHash — ở đoạn KHÁC và khoảng năm (log `nam` [y0, y1]) KHÔNG chồng mọi lần
            trước → miễn (Kinh thánh §13.6 TL-1 "mỗi phần phim quay lại cùng điểm máy ở năm khác").
  ML1       `cau: ""` (chuỗi rỗng) = không gắn câu (không còn lỗi (c) "cau '' không khớp"); shot vẫn tính vào (a)/(b) như shot không khai cau.
  NC-H1     lớp nhà khai của cảnh tl/* (V7C-D5): `opt.bfile` (tệp nhà, page.js), `opt.cityOpt`, `opt.pre1704town`, `opt.pho2026`, hoặc trường chung
            `lop_nha: "<mô tả>"` (shot p hoặc heroes.<k>.opt).
  SACH-1    chữ "Illustration" (vai `minh_hoa` hoặc chữ đúng "Illustration") TRONG shot `minh_hoa` là hợp lệ (§14.1 (c)); ngoài shot minh hoạ vẫn là lỗi (e).
"""
import json, os, statistics, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import q_k116 as K6  # noqa: E402

MH_MAX, MH_AGL = 20.0, 40.0                       # §14.1 (c) N2 ≤ 20 %; máy ≤ 40 m AGL (lệnh K-1.17)
NHAN = 'Illustration'
GOC_3D = {'cao', 'thap', 'neo'}
R1_MIN, R1_TOT = 15.0, 20.0   # §14.7 R1 "≥ 15–20 % khung": < 15 % lỗi; 15–20 % Cảnh báo (1.17.0 tạm: 25 %)
TRONG_PCT = 50.0       # §14.7 R2 "Đồng cỏ/cát trống (> 50 % khung)" (1.17.0 tạm: > 60 %)
R2_GIAY = 6.0          # §14.7 R2 "≤ 6 s liên tục"
R2_CHUONG = 10.0       # §14.7 R2 "≤ 10 % thời lượng mỗi chương" — mẫu số = thời lượng chương (1.17.0 tạm: 1/3 thời lượng eo đất)
R4_NOI = {'pho', 'lau_dai', 'cang'}; R4_ALIAS = {'thanh_pho': 'pho'}   # §14.7 R4 "góc phố/lâu đài/cảng"
R4_BAN_DO = 3.0        # §14.7 R4 "bản đồ phủ ≤ 3 s (TL-4)"
R3_DAI, R3_GOC, R3_GAP = 15.0, 2, 6.0             # lệnh K-1.17: shot > 15 s → ≥ 2 góc, biến cố ≤ 6 s
LOP_NHA_KEYS = ('bfile', 'cityOpt', 'pre1704town', 'pho2026', 'lop_nha')
ROWS = ('MINH-HOA', 'EO-DAT-R1', 'EO-DAT-R2', 'EO-DAT-R3', 'EO-DAT-R4')
LEN = 1e-6


def ap_117(E): return K6.ap_116(E)


def _dur(s):
    if isinstance(s.get('dur'), (int, float)): return float(s['dur'])
    if isinstance(s.get('t1'), (int, float)) and isinstance(s.get('t0'), (int, float)): return float(s['t1']) - float(s['t0'])
    return 0.0


def _num(x): return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def _series(v):
    """số → [(None, v)]; [[t, v], …] hoặc [{t, v|pct}] → [(t, v)]; khác → []"""
    if _num(v) is not None: return [(None, float(v))]
    out = []
    for x in v if isinstance(v, list) else []:
        if isinstance(x, (list, tuple)) and len(x) == 2 and _num(x[1]) is not None: out.append((_num(x[0]), float(x[1])))
        elif isinstance(x, dict) and _num(x.get('v', x.get('pct'))) is not None: out.append((_num(x.get('t')), float(x.get('v', x.get('pct')))))
    return out


def _abs_t(LS, TL=None):
    """→ [(shot log, t0 tuyệt đối, t1)] theo thứ tự thời gian; log không có t0 → cộng dồn dur theo thứ tự log"""
    out, t = [], 0.0
    for s in LS or []:
        a = _num(s.get('t0')); d = _dur(s)
        a = t if a is None else a; out.append((s, a, a + d)); t = a + d
    return sorted(out, key=lambda z: z[1])


# ================================================================ MINH-HOA
def _so_ai(E, ep_dir):
    p = E.get('so_ai')
    if not p: return None
    try: J = K6._load(K6._p(ep_dir, p))
    except Exception as e: return f'không đọc được so_ai ({p}): {e}'   # noqa: BLE001
    return J if isinstance(J, list) else (J.get('dong') or J.get('records') or [J]) if isinstance(J, dict) else []


def _dong_ok(d):
    if not isinstance(d, dict): return False
    return bool(d.get('model')) and any(d.get(k) for k in ('lenh', 'prompt', 'lenh_sha', 'prompt_sha')) and any(d.get(k) for k in ('sha_ra', 'sha_out', 'sha256'))


def _mh_spans(LS):
    return [(str(s.get('shot')), a, b) for s, a, b in _abs_t(LS) if s.get('minh_hoa')]


def minh_hoa(E, TL, LS, ep_dir='.', TX=None, step=12, why=None):
    if LS is None: return K6.r(thieu=[why or 'không có log shot'], val='—')
    Z = _abs_t(LS); mh = [(s, a, b) for s, a, b in Z if s.get('minh_hoa')]
    if not mh: return K6.na('không shot minh_hoa trong log shot')
    T = K6.tong(E, TL) if (TL or E.get('segments')) else sum(_dur(s) for s in LS)
    M = {k: [] for k in 'abcde'}; th, near = [], []
    tot = sum(b - a for _, a, b in mh); pct = 100 * tot / T if T else 0.0
    if pct > MH_MAX + LEN: M['a'].append(f'(a) minh hoạ {tot:.1f} s = {pct:.1f} % > {MH_MAX:g} % thời lượng ({len(mh)} đoạn)')
    near += K6.sat('minh hoạ %', round(pct, 2), MH_MAX)
    SA = _so_ai(E, ep_dir)
    if isinstance(SA, str): th.append(SA); SA = None
    for k, (s, a, b) in enumerate(Z):
        if not s.get('minh_hoa'): continue
        sid = str(s.get('shot')); w = f'{sid} @{K6.mmss(a)}'
        # (b) nhãn suốt đoạn
        if TX is not None:
            f0, f1 = int(round(a * K6.FPS)), int(round(b * K6.FPS)); fs = [f for f in TX if f0 <= f < f1]
            co = [f for f in fs if any(K6._vis(x) and NHAN.lower() in str(x.get('s') or '').lower() for x in TX[f])]
            if not fs: th.append(f'(b) {w}: log chữ không có khung mẫu trong đoạn')
            elif len(co) < len(fs): M['b'].append(f'(b) {w}: nhãn "{NHAN}" hiện {len(co)}/{len(fs)} khung mẫu (cần suốt đoạn)')
        elif s.get('nhan_minh_hoa') is not None or s.get('nhan') is not None:
            nh = str(s.get('nhan_minh_hoa') if s.get('nhan_minh_hoa') is not None else s.get('nhan'))
            nt = s.get('nhan_t') or [0.0, b - a]
            if nh.strip() != NHAN: M['b'].append(f'(b) {w}: nhãn {nh!r} ≠ "{NHAN}"')
            elif _num(nt[0]) is None or _num(nt[1]) is None or nt[0] > 1 / K6.FPS + LEN or nt[1] < (b - a) - 1 / K6.FPS - LEN:
                M['b'].append(f'(b) {w}: nhãn hiện {nt} không phủ cả đoạn 0–{b - a:.2f} s')
        else: th.append(f'(b) {w}: không đo được nhãn "{NHAN}" — cần log chữ (`log_chu`) hoặc trường `nhan_minh_hoa` (+ `nhan_t`); chưa có OCR')
        # (c) kẹp giữa hai shot 3D
        tr = Z[k - 1][0] if k > 0 else None; sa = Z[k + 1][0] if k + 1 < len(Z) else None
        is3d = lambda x: x is not None and not x.get('minh_hoa') and str(x.get('goc') or '') in GOC_3D
        if not (is3d(tr) and is3d(sa)):
            M['c'].append(f"(c) {w}: không kẹp giữa hai shot 3D (trước: {tr.get('shot') if tr else 'đầu phim'} goc {tr.get('goc') if tr else '—'}; "
                          f"sau: {sa.get('shot') if sa else 'cuối phim'} goc {sa.get('goc') if sa else '—'})")
        # (d) máy ≤ 40 m AGL
        ag = [v for v in (s.get('agl_m') if isinstance(s.get('agl_m'), list) else [s.get('agl_m')]) if _num(v) is not None]
        if ag:
            if max(ag) > MH_AGL + LEN: M['d'].append(f'(d) {w}: máy cao {max(ag):.0f} m AGL > {MH_AGL:g} m')
            near += K6.sat(f'{sid} AGL m', round(max(ag), 1), MH_AGL)
        # (e) sổ AI
        d = s.get('so_ai'); dl = (d if isinstance(d, list) else [d]) if d else [x for x in SA or [] if isinstance(x, dict) and str(x.get('shot') or x.get('doan')) == sid]
        if not dl: M['e'].append(f'(e) {w}: sổ AI không có dòng cho đoạn (log shot `so_ai` hoặc tệp so_ai: mục shot = {sid})')
        elif not any(_dong_ok(x) for x in dl): M['e'].append(f'(e) {w}: dòng sổ AI thiếu model / lệnh / SHA đầu ra')
    loi = sum(M.values(), [])
    return K6.r(loi=loi, thieu=th, muc=M, sat_nguong=near, val=f'{len(mh)} đoạn minh hoạ · {tot:.1f} s = {pct:.1f} % · nhãn: {"log chữ" if TX is not None else "trường log shot"} · '
                                                              f'lỗi kẹp {len(M["c"])} · AGL {len(M["d"])} · sổ AI {len(M["e"])}')


# ================================================================ EO-DAT R1–R4
def _chuong(s, Z_seg):
    return str(s.get('chuong') if s.get('chuong') is not None else Z_seg.get(str(s.get('shot')), '?'))


def eo_dat(E, TL, LS, why=None):
    if LS is None: return {k: K6.r(thieu=[why or 'không có log shot'], val='—') for k in ROWS[1:]}
    Z = _abs_t(LS); SEG = {str(s['id']): str(s.get('chuong', s.get('part', '?'))) for s in E.get('segments') or []}
    out = {}
    # ---- R1
    L1, th1, rows1, near1 = [], [], [], []
    for s, a, b in Z:
        if not s.get('chu_the_eo_dat'): continue
        sid = str(s.get('shot')); v = [x for _, x in _series(s.get('chu_the_pct'))]
        if not v: th1.append(f'(a) {sid}: chu_the_eo_dat nhưng không có `chu_the_pct` (đo từ mặt nạ ID)'); continue
        med = statistics.median(v); rows1.append(f'{sid}: chủ thể trung vị {med:.1f} %')
        near1 += K6.sat(f'{sid} chủ thể %', round(med, 1), R1_MIN) + K6.sat(f'{sid} chủ thể %', round(med, 1), R1_TOT)
        if med < R1_MIN - LEN: L1.append(f'(a) {sid} @{K6.mmss(a)}: chủ thể {med:.1f} % khung < {R1_MIN:g} %')
        elif med < R1_TOT - LEN: L1.append(f'(b) {sid} @{K6.mmss(a)}: chủ thể {med:.1f} % khung trong vùng {R1_MIN:g}–{R1_TOT:g} % (Cảnh báo)')
    n1 = sum(1 for s in LS if s.get('chu_the_eo_dat'))
    out['EO-DAT-R1'] = (K6.r(loi=L1, thieu=th1, sat_nguong=near1, muc={c_: [x for x in L1 + th1 if x.startswith(f'({c_})')] for c_ in 'ab'}, val=f'{n1} shot chu_the_eo_dat · ' + ('; '.join(rows1[:6]) or 'chưa đo')) if n1
                        else K6.na('không shot khai chu_the_eo_dat'))
    # ---- R2
    eo = [(s, a, b) for s, a, b in Z if str(s.get('noi') or '') == 'eo_dat']
    if not eo: out['EO-DAT-R2'] = K6.na('không shot eo đất (noi: eo_dat)')
    else:
        th2, L2, near2, runs, cur, ch = [], [], [], [], None, {}
        for s, a, b in Z: ch.setdefault(_chuong(s, SEG), [0.0, 0.0])[0] += b - a   # mẫu số = thời lượng chương (mọi shot log)
        for s, a, b in eo:
            sid = str(s.get('shot')); ser = _series(s.get('trong_pct'))
            if not ser: th2.append(f'{sid}: thiếu `trong_pct`'); continue
            if ser[0][0] is None: ivs = [(a, b, ser[0][1])]   # số TB shot → cả shot
            else:
                ts = sorted((t, v) for t, v in ser if t is not None); ivs = []
                for j, (t, v) in enumerate(ts):
                    t1 = ts[j + 1][0] if j + 1 < len(ts) else (b - a)
                    ivs.append((a + t, a + min(max(t1, t), b - a), v))
            c = ch.setdefault(_chuong(s, SEG), [0.0, 0.0])
            for x0, x1, v in ivs:
                tr = v > TRONG_PCT
                if tr: c[1] += x1 - x0
                if tr and cur is not None and x0 - cur[1] <= 1 / K6.FPS + LEN: cur[1] = x1; cur[2].add(sid)
                elif tr: cur = [x0, x1, {sid}]; runs.append(cur)
                else: cur = None
        dmax = max((r_[1] - r_[0] for r_ in runs), default=0.0)
        for r_ in runs:
            if r_[1] - r_[0] > R2_GIAY + LEN: L2.append(f"(a) trống liên tục {r_[1] - r_[0]:.1f} s > {R2_GIAY:g} s @{K6.mmss(r_[0])} ({', '.join(sorted(r_[2]))})")
        near2 += K6.sat('trống liên tục dài nhất s', round(dmax, 2), R2_GIAY)
        rows2 = []
        for k, (tot, tr) in sorted(ch.items()):
            if not tr: continue
            p = 100 * tr / tot if tot else 0.0; rows2.append(f'ch {k}: {p:.1f} %')
            if p > R2_CHUONG + LEN: L2.append(f'(b) chương {k}: trống {tr:.1f} s / thời lượng chương {tot:.1f} s = {p:.1f} % > {R2_CHUONG:g} %')
            near2 += K6.sat(f'chương {k} trống %', round(p, 2), R2_CHUONG)
        out['EO-DAT-R2'] = K6.r(loi=L2, thieu=th2, sat_nguong=near2, muc={c_: [x for x in L2 if x.startswith(f'({c_})')] for c_ in 'ab'},
                                val=f'{len(eo)} shot eo đất · đo {len(eo) - len(th2)} · trống liên tục dài nhất {dmax:.1f} s · ' + (' · '.join(rows2) or '—'))
    # ---- R3
    dai = [(s, a, b) for s, a, b in eo if b - a > R3_DAI + LEN]
    if not eo: out['EO-DAT-R3'] = K6.na('không shot eo đất (noi: eo_dat)')
    elif not dai: out['EO-DAT-R3'] = K6.r(val=f'{len(eo)} shot eo đất · 0 shot > {R3_DAI:g} s')
    else:
        L3, th3, rows3 = [], [], []
        for s, a, b in dai:
            sid = str(s.get('shot')); w = f'{sid} @{K6.mmss(a)} ({b - a:.1f} s)'
            ng = s.get('so_goc') if _num(s.get('so_goc')) is not None else (len(s['goc_may']) if isinstance(s.get('goc_may'), list) else None)
            if ng is None: th3.append(f'(a) {w}: thiếu `so_goc` (hoặc `goc_may`)')
            elif ng < R3_GOC: L3.append(f'(a) {w}: {int(ng)} góc máy < {R3_GOC}')
            ev = sorted({0.0, b - a} | {float(x['t']) for k in ('su_kien', 'tl_buoc') for x in s.get(k) or [] if isinstance(x, dict) and _num(x.get('t')) is not None and 0 <= x['t'] <= b - a})
            g = max((y - x for x, y in zip(ev, ev[1:])), default=b - a); rows3.append(f'{sid} {g:.1f} s')
            if g > R3_GAP + LEN: L3.append(f'(b) {w}: khoảng không biến cố dài nhất {g:.1f} s > {R3_GAP:g} s ({len(ev) - 2} biến cố log)')
        out['EO-DAT-R3'] = K6.r(loi=L3, thieu=th3, muc={c_: [x for x in L3 if x.startswith(f'({c_})')] for c_ in 'ab'},
                                val=f'{len(dai)}/{len(eo)} shot eo đất > {R3_DAI:g} s · khoảng biến cố dài nhất: ' + ', '.join(rows3[:8]))
    # ---- R4 (1.17.1)
    r4 = [(s, a, b) for s, a, b in Z if s.get('loi_khong_vat_eo_dat')]
    if not r4: out['EO-DAT-R4'] = K6.na('không shot khai loi_khong_vat_eo_dat')
    else:
        L4, th4, rows4, near4 = [], [], [], []
        for s, a, b in r4:
            sid = str(s.get('shot')); w = f'{sid} @{K6.mmss(a)}'
            noi = str(s.get('noi') or (s.get('p') or {}).get('noi') or '').strip().lower(); noi = R4_ALIAS.get(noi, noi)
            bd, why4 = _ban_do(s.get('ban_do_phu'))
            if why4: th4.append(f'(b) {w}: `ban_do_phu` không đọc được ({why4})'); continue
            if bd is not None:
                near4 += K6.sat(f'{sid} bản đồ phủ s', round(bd, 2), R4_BAN_DO)
                if bd > R4_BAN_DO + LEN: L4.append(f'(b) {w}: bản đồ phủ {bd:.1f} s > {R4_BAN_DO:g} s (TL-4)'); continue
            if noi in R4_NOI: rows4.append(f'{sid}: noi {noi}')
            elif bd is not None: rows4.append(f'{sid}: bản đồ phủ {bd:.1f} s')
            else: L4.append(f"(a) {w}: câu lời không vật trên eo đất nhưng noi '{noi or '—'}' ∉ {{pho, lau_dai, cang}} và không bản đồ phủ")
        out['EO-DAT-R4'] = K6.r(loi=L4, thieu=th4, sat_nguong=near4, muc={c_: [x for x in L4 + th4 if x.startswith(f'({c_})')] for c_ in 'ab'},
                                val=f'{len(r4)} shot loi_khong_vat_eo_dat · ' + ('; '.join(rows4[:6]) or '—'))
    return out


def _ban_do(v):
    """`ban_do_phu` → (giây, lỗi): số | [t0, t1] | [[t0, t1], …] | {dur} | {t: [t0, t1]}; None/False → (None, None)"""
    if v is None or v is False: return None, None
    if _num(v) is not None: return float(v), None
    if isinstance(v, dict):
        if _num(v.get('dur')) is not None: return float(v['dur']), None
        v = v.get('t')
    if isinstance(v, (list, tuple)) and len(v) == 2 and all(_num(x) is not None for x in v): v = [v]
    if isinstance(v, (list, tuple)) and v and all(isinstance(x, (list, tuple)) and len(x) == 2 and all(_num(y) is not None for y in x) for x in v):
        return max(max(0.0, float(x[1]) - float(x[0])) for x in v), None   # TL-4: MỖI lần phủ ≤ 3 s → lấy lần dài nhất
    return None, f'kiểu {type(v).__name__}'


# ================================================================ sửa luật cũ (chỉ ap_117)
def nam_log(LS):
    """{id đoạn: (năm đầu, năm cuối)} từ log shot `nam` [y0, y1] | số | `moc`"""
    out = {}
    for s in LS or []:
        v = s.get('nam') if s.get('nam') is not None else s.get('moc')
        ys = [float(x) for x in (v if isinstance(v, list) else [v]) if _num(x) is not None]
        if ys: out[str(s.get('shot'))] = (min(ys), max(ys))
    return out


def q33_mien(allap, NL):
    """lần xuất hiện được miễn (TL-1): khác đoạn VÀ khoảng năm không chồng MỌI lần trước (khai hay pHash). → tập id(ap)"""
    if not NL: return set()
    seg = lambda x: str(x.get('seg') or (x.get('shots') or ['?/'])[0].split('/')[0])
    seen, mien = [], set()
    for a in sorted(allap, key=lambda x: x['t0']):
        y = NL.get(seg(a))
        if seen and y is not None and all(seg(p) != seg(a) for p, _ in seen) and all(py is not None and (y[1] < py[0] or y[0] > py[1]) for _, py in seen):
            mien.add(id(a))
        seen.append((a, y))
    return mien


def co_lop_nha(z):
    o = z.get('o') or {}; p = z.get('p') or {}
    for k in LOP_NHA_KEYS:
        if o.get(k) or p.get(k): return {'bfile': 'tệp nhà (opt.bfile)', 'lop_nha': f"lop_nha: {o.get(k) or p.get(k)}"}.get(k, f'opt.{k}')
    return None


# ================================================================ cả bộ
def check(E, TL=None, ep_dir='.', logs=None, log_shot_path=None):
    if not ap_117(E): return {k: K6.na('tập trước T3: giữ hành vi 1.16.1') for k in ROWS}
    TX, step, _, _ = K6.text_frames(TL, logs, E.get('log_chu'), ep_dir)
    LS, why = K6.log_shot(E, ep_dir, log_shot_path)
    out = {}
    try: out['MINH-HOA'] = minh_hoa(E, TL, LS, ep_dir, TX, step, why)
    except Exception as e: out['MINH-HOA'] = K6.r(thieu=[f'không chạy được: {type(e).__name__}: {e}'], val='—')   # noqa: BLE001
    try: out.update(eo_dat(E, TL, LS, why))
    except Exception as e: out.update({k: K6.r(thieu=[f'không chạy được: {type(e).__name__}: {e}'], val='—') for k in ROWS[1:]})   # noqa: BLE001
    cong = 'animatic' if E.get('animatic') else 'G2'
    return {k: dict(v, cong=cong) for k, v in out.items()}
