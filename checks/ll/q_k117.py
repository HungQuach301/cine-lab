#!/opt/cine/bin/python
"""Luật kênh 2 bản 1.17.0 (phiên K-1.17, 21/10/2026) + 1.17.1 (phiên K-1.17.1, 21/10/2026: ngưỡng EO-DAT theo Kinh thánh §14.7 nguyên văn, thêm R4) + 1.17.2
(phiên K-1.17.2, 22/10/2026: MINH-HOA theo đoạn khai + bỏ nhãn bắt buộc, EO-DAT-R1 chỉ báo + vùng nở, CONG-BO-1) — CHỈ tập kênh 2 từ T3 (`khung_sach: true` | `kenh2_tu_t3: true`, như 1.16); tập cũ giữ
đúng hành vi 1.16.1 (không thêm hàng). Luật N2+ (T4) ở q_n2p.py. Định nghĩa: checks/ll/RULES-LL.md mục "1.17".

Căn cứ: Kinh thánh kênh 2 §14.1 (c) N2 minh hoạ ≤ 20 % (nhãn "Illustration" bỏ theo quyết định chủ dự án 22/10/2026 11:09); §14.1 (f) công bố; §15 (T4, M-d); §14.7 R1–R4 eo đất
(1.17.0 viết khi §14.7 chưa có trên repo, ngưỡng R1/R2 K đề xuất tạm; 1.17.1 khớp §14.7 nguyên văn — docs/BIBLE-KENH2.md trên main @96b5017c,
SHA tệp 14ca13aa…: "R1 … chiếm ≥ 15–20 % khung", "R2 Đồng cỏ/cát trống (> 50 % khung) ≤ 6 s liên tục và ≤ 10 % thời lượng mỗi chương",
"R4 Câu lời không có vật trên eo đất → góc phố/lâu đài/cảng; bản đồ phủ ≤ 3 s (TL-4)").

Hàng (cấp ở cap112.py: Chặn ở cổng G2 · Cảnh báo ở animatic (`animatic: true` trong đặc tả) — như K116-D5; không khai → G2):
  MINH-HOA  (1.17.2, quyết định chủ dự án 22/10/2026 11:09 — duyệt V2-D1…D8, không nhãn/câu AI trong phim) ĐOẠN minh hoạ khai trong log shot
            (`doan_ai`): shot `minh_hoa: true` (cả shot) | danh sách `minh_hoa: [{t0, t1, ma?, so_ai?, luot?, kiem?, agl_m?}]` (giây trong
            shot; mục `minh_hoa: false` / `ai_image: false` = không phải đoạn AI) — V2-D5. Đoạn khai mà shot ghi `ai_image: false` là MÂU THUẪN
            KHAI: không đo ở đây, báo ở K-LAI-2 (b). T3 theo N2, T4 theo M-d: (a) tổng giây minh hoạ ≤ 20 % thời lượng; (b) BỎ (1.17.2: không nhãn
            "Illustration" bắt buộc); (c) đoạn KẸP giữa hai khung 3D: khung ngay trước đầu đoạn và ngay sau cuối đoạn (kể cả trong cùng shot)
            thuộc shot `goc` cao/thap/neo và không nằm trong đoạn minh hoạ khác; (d) máy ≤ 40 m AGL: `agl_m` của đoạn, hoặc `agl_m` của shot
            ứng với khoá `cam[].t` trong đoạn (log V2: agl_m[i] ↔ cam[i]); (e) sổ AI có dòng cho mỗi đoạn: model (model | model_req |
            model_resp) + lệnh (lenh | prompt | lenh_sha | prompt_sha) + SHA đầu ra (sha_ra | sha_out | sha256 | output.sha256) — `so_ai` của
            đoạn/shot (dict hoặc list) hoặc tệp `so_ai:` của episode.yaml (.jsonl/.json; mục khớp khi `shot`/`doan`/`ma` = id đoạn, mã đoạn hoặc
            id shot, hoặc `tag` = `luot` của đoạn, hoặc `tag` bắt đầu bằng "<mã đoạn>-").
  EO-DAT-R1 shot log `chu_the_eo_dat: true`: chủ thể chiếm khung (trường `chu_the_pct`: số TB shot hoặc [[t, %], …] từ mặt nạ ID; dùng
            trung vị): (a) < R1_MIN (15 %); (b) R1_MIN ≤ chủ thể < R1_TOT (15–20 %) (vùng "15–20 %" của §14.7). Thiếu → THIẾU.
            1.17.2 (V2-D2): CHỈ BÁO ở mọi cổng (chủ dự án chấm bằng mắt); in thêm % VÙNG chủ thể theo mặt nạ NỞ ≈ R1_NO (1,5 %) bề ngang khung
            cạnh % pixel thô — K tự đo khi log có `chu_the_mat_na` (PNG nhị phân, trắng = chủ thể; một tệp hoặc danh sách khung mẫu), không thì
            đọc `chu_the_pct_no` (số hoặc [[t, %], …]); (a)/(b) vẫn xét trên pixel thô (định nghĩa chưa đổi — K1172-D3).
  EO-DAT-R2 shot eo đất (`noi: eo_dat`), trường `trong_pct` (% cỏ/cát không vật; số TB shot, hoặc [[t, %], …] theo khung mẫu — từ mặt nạ ID);
            "trống" = trong_pct > TRONG_PCT (50 %): (a) giây trống LIÊN TỤC ≤ R2_GIAY (6 s, nối qua ranh shot); (b) mỗi chương: tổng giây
            trống ≤ R2_CHUONG (10 %) × THỜI LƯỢNG CHƯƠNG (mọi shot log của chương, không chỉ shot eo đất). Thiếu trong_pct → THIẾU.
  EO-DAT-R3 shot eo đất dài > 15 s: (a) ≥ 2 góc máy (trường `so_goc` số nguyên, hoặc `goc_may` danh sách); (b) biến cố thấy được cách nhau
            ≤ 6 s (log `su_kien[].t`, `tl_buoc[].t`, tính cả đầu/cuối shot).
  EO-DAT-R4 (1.17.1) shot log `loi_khong_vat_eo_dat: true` (câu lời nói về eo đất nhưng không có vật để thấy): (a) `noi` ∈ R4_NOI (pho |
            lau_dai | cang; `thanh_pho` coi là pho — tên log hiện dùng) HOẶC (b) bản đồ phủ `ban_do_phu` ≤ R4_BAN_DO (3 s, TL-4): số giây,
            [t0, t1], [[t0, t1], …] (xét lần phủ dài nhất) hoặc {dur}. Có `ban_do_phu` > 3 s → lỗi (b) dù noi hợp lệ (TL-4 là trần riêng).
            Không shot khai → KHÔNG ÁP.
  CONG-BO-1 (1.17.2, mới) tập có khung AI (đoạn minh hoạ / `ai_image` ở log shot hoặc log khung `lai.log_khung`) HOẶC giọng tổng hợp
            (episode.yaml `giong_tong_hop: true` | `vo.tong_hop` / `voice.synthetic` true | `vo.engine` / `voice.engine` / `vo.nguon` chứa
            elevenlabs/tts/synthetic): (a) tệp mô tả YouTube của gói phát hành (`phat_hanh.mo_ta`) có câu công bố chứa "AI" hoặc "synthetic";
            (b) đặc tả gói khai `phat_hanh.youtube_altered_content: true` (cài đặt "AI use" = Yes ở YouTube Studio). Căn cứ: Kinh thánh §14.1 (f)
            ("bật khai báo nội dung AI trên YouTube"; sửa 22/10 theo quyết định chủ dự án 22/10 11:09) + YouTube Help "Disclosing use of GenAI
            content" (support.google.com/youtube/answer/14328491, đọc 22/10/2026). Cấp: Chặn ở cổng GÓI PHÁT HÀNH (episode.yaml `cong:
            phat_hanh` hoặc `phat_hanh.goi: true`); mọi cổng trước đó (animatic, G2) chỉ báo (Cảnh báo). Tập không AI, không giọng tổng hợp →
            KHÔNG ÁP.
Sửa luật cũ (khiếu nại 8 hàng Chặn animatic T3 chấp nhận — báo cáo §4), chỉ khi ap_117:
  Q33 / Q33-K2 / Q33 (1.13): lần xuất hiện cùng (cảnh, góc) — khai hay pHash — ở đoạn KHÁC và khoảng năm (log `nam` [y0, y1]) KHÔNG chồng mọi lần
            trước → miễn (Kinh thánh §13.6 TL-1 "mỗi phần phim quay lại cùng điểm máy ở năm khác").
  ML1       `cau: ""` (chuỗi rỗng) = không gắn câu (không còn lỗi (c) "cau '' không khớp"); shot vẫn tính vào (a)/(b) như shot không khai cau.
  NC-H1     lớp nhà khai của cảnh tl/* (V7C-D5): `opt.bfile` (tệp nhà, page.js), `opt.cityOpt`, `opt.pre1704town`, `opt.pho2026`, hoặc trường chung
            `lop_nha: "<mô tả>"` (shot p hoặc heroes.<k>.opt).
  SACH-1    chữ "Illustration" (vai `minh_hoa` hoặc chữ đúng "Illustration") TRONG shot `minh_hoa` là hợp lệ (§14.1 (c)); ngoài shot minh hoạ vẫn là lỗi (e).
            1.17.2: KHÔNG ĐỔI (lệnh K-1.17.2) — vẫn xét theo SHOT có `minh_hoa` (`_mh_spans`), không theo đoạn.
1.17.3 (phiên K-1.17.3, 23/10/2026; khiếu nại BAN-CUOI-T3 — phán quyết checks-appeal.md): EO-DAT-R3 (b) ranh góc máy `goc_may[].t` + lưới khung (A3);
  EO-DAT-R3 (a) ngoại lệ có khai `r3_ngoai_le` + dòng AUTHORSHIP (đề xuất K1173-D1); Q33 miễn năm theo khoảng năm HIỆN (`nam_hien`/`nam_khoang`, A5).
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
R1_NO = 1.5            # 1.17.2 (V2-D2): mặt nạ nở ≈ 1,5 % bề ngang khung (bán kính) cho "vùng chủ thể"
CB_RE = r'\bAI\b|synthetic'                       # CONG-BO-1 (a): câu công bố có "AI" hoặc "synthetic" (lệnh K-1.17.2)
GIONG_RE = r'elevenlabs|\btts\b|synthetic|tổng hợp'   # CONG-BO-1: nguồn giọng là giọng tổng hợp
LOP_NHA_KEYS = ('bfile', 'cityOpt', 'pre1704town', 'pho2026', 'lop_nha')
ROWS = ('MINH-HOA', 'EO-DAT-R1', 'EO-DAT-R2', 'EO-DAT-R3', 'EO-DAT-R4', 'CONG-BO-1')
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


def _get(d, k):
    for part in k.split('.'):
        d = d.get(part) if isinstance(d, dict) else None
    return d


def _dong_ok(d):
    """dòng sổ AI đủ model + lệnh + SHA đầu ra (1.17.2: nhận cả tên trường sổ thật V2 — model_req/model_resp, output.sha256)"""
    if not isinstance(d, dict): return False
    return (any(d.get(k) for k in ('model', 'model_req', 'model_resp')) and any(d.get(k) for k in ('lenh', 'prompt', 'lenh_sha', 'prompt_sha'))
            and any(_get(d, k) for k in ('sha_ra', 'sha_out', 'sha256', 'output.sha256')))


def _mh_spans(LS):
    """SACH-1 (1.17; KHÔNG đổi ở 1.17.2): shot có `minh_hoa` truthy → [(id, t0, t1)] cả shot"""
    return [(str(s.get('shot')), a, b) for s, a, b in _abs_t(LS) if s.get('minh_hoa')]


def _doan_list(s):
    """mục khai đoạn minh hoạ của MỘT shot log → [(t0 trong shot, t1, mục)]; `minh_hoa: true` = cả shot (mục {})"""
    v = s.get('minh_hoa'); d = _dur(s)
    if v is True: return [(0.0, d, {})]
    out = []
    for x in v if isinstance(v, list) else []:
        if not isinstance(x, dict) or x.get('minh_hoa') is False or x.get('ai_image') is False: continue
        t0, t1 = _num(x.get('t0')), _num(x.get('t1'))
        if t0 is None or t1 is None or t1 <= t0: continue
        out.append((max(0.0, t0), min(d, t1) if d else t1, x))
    return out


def doan_ai(LS):
    """1.17.2 (V2-D5): đoạn minh hoạ khai trong log shot → (đoạn hợp lệ, đoạn mâu thuẫn). Đoạn = dict(id, ma, shot, s (shot log), m (mục đoạn),
    a, b (giây tuyệt đối)). Mâu thuẫn: shot ghi `ai_image: false` mà mục đoạn không ghi `ai_image: true` (log V2: C4/M1 trượt 3 lượt → giữ 3D)."""
    ok, bad = [], []
    for s, a0, _ in _abs_t(LS):
        for t0, t1, x in _doan_list(s):
            sid = str(s.get('shot')); ma = str(x.get('ma') or sid)
            d = dict(id=f'{sid}/{ma}' if x else sid, ma=ma, shot=sid, s=s, m=x, a=a0 + t0, b=a0 + t1, t0=t0, t1=t1)
            (bad if s.get('ai_image') is False and x.get('ai_image') is not True else ok).append(d)
    return sorted(ok, key=lambda z: z['a']), bad


def _goc_at(Z, DS, t):
    """khung tại t (giây tuyệt đối) có phải khung 3D không → (bool, mô tả)"""
    sh = next(((s, a, b) for s, a, b in Z if a - LEN <= t < b - LEN), None)
    if sh is None: return False, 'đầu phim' if not Z or t < Z[0][1] + LEN else 'cuối phim'
    s = sh[0]; g = str(s.get('goc') or '')
    if any(d['a'] - LEN <= t < d['b'] - LEN for d in DS): return False, f"{s.get('shot')} @{t - sh[1]:.2f} s trong đoạn minh hoạ khác"
    return g in GOC_3D, f"{s.get('shot')} @{t - sh[1]:.2f} s goc {g or '—'}"


def _agl_doan(d):
    """→ [AGL m] của đoạn: `agl_m` của mục đoạn; không có → agl_m[i] của shot ứng khoá cam[i].t trong đoạn (log V2: hai danh sách cùng độ dài); không khoá
    nào trong đoạn → khoá gần nhất trước đầu đoạn; không có cam khớp → cả agl_m của shot khi đoạn = cả shot, không thì None (không xét)"""
    m, s, t0, t1 = d['m'], d['s'], d['t0'], d['t1']
    v = m.get('agl_m') if isinstance(m, dict) else None
    if v is not None: return [float(x) for x in (v if isinstance(v, list) else [v]) if _num(x) is not None]
    ag = s.get('agl_m'); ag = ag if isinstance(ag, list) else ([ag] if _num(ag) is not None else [])
    if not ag: return None
    cam = s.get('cam') if isinstance(s.get('cam'), list) else None
    if cam and len(cam) == len(ag) and all(isinstance(c, dict) and _num(c.get('t')) is not None for c in cam):
        vals = [float(ag[i]) for i, c in enumerate(cam) if t0 - LEN <= float(c['t']) < t1 - LEN and _num(ag[i]) is not None]
        if not vals:
            prev = [i for i, c in enumerate(cam) if float(c['t']) <= t0 + LEN]
            vals = [float(ag[prev[-1]])] if prev and _num(ag[prev[-1]]) is not None else []
        return vals
    return [float(x) for x in ag if _num(x) is not None] if not m or (t0 <= LEN and abs(t1 - _dur(s)) <= LEN) else None


def _so_ai_rows(d, SA):
    m, s = d['m'], d['s']
    v = (m.get('so_ai') if isinstance(m, dict) else None) or s.get('so_ai')
    if v: return v if isinstance(v, list) else [v]
    keys = {d['id'], d['ma'], d['shot']}; luot = str(m.get('luot') or '') if isinstance(m, dict) else ''
    out = []
    for x in SA or []:
        if not isinstance(x, dict): continue
        k = {str(x.get(f)) for f in ('shot', 'doan', 'ma') if x.get(f) is not None}; tag = str(x.get('tag') or '')
        if k & keys or (luot and tag == luot) or (not luot and m and tag.startswith(d['ma'] + '-')): out.append(x)
    return out


def minh_hoa(E, TL, LS, ep_dir='.', TX=None, step=12, why=None):
    """1.17.2: đo theo ĐOẠN khai (doan_ai). (b) nhãn đã bỏ — TX/step giữ trong chữ ký cho tương thích, không dùng."""
    if LS is None: return K6.r(thieu=[why or 'không có log shot'], val='—')
    Z = _abs_t(LS); DS, MT = doan_ai(LS)
    mt = f" (đoạn khai mâu thuẫn ai_image: false: {', '.join(d['id'] for d in MT)} — K-LAI-2 (b))" if MT else ''
    if not DS: return K6.na('không đoạn minh hoạ khai trong log shot' + mt)
    T = K6.tong(E, TL) if (TL or E.get('segments')) else sum(_dur(s) for s in LS)
    M = {k: [] for k in 'acde'}; th, near = [], []
    tot = sum(d['b'] - d['a'] for d in DS); pct = 100 * tot / T if T else 0.0
    if pct > MH_MAX + LEN: M['a'].append(f'(a) minh hoạ {tot:.1f} s = {pct:.1f} % > {MH_MAX:g} % thời lượng ({len(DS)} đoạn)')
    near += K6.sat('minh hoạ %', round(pct, 2), MH_MAX)
    SA = _so_ai(E, ep_dir)
    if isinstance(SA, str): th.append(SA); SA = None
    for d in DS:
        w = f"{d['id']} @{K6.mmss(d['a'])}–{K6.mmss(d['b'])}"
        # (c) kẹp giữa hai khung 3D: khung ngay trước đầu đoạn và ngay sau cuối đoạn (kể cả trong cùng shot)
        ok0, w0 = _goc_at(Z, DS, d['a'] - 0.5 / K6.FPS); ok1, w1 = _goc_at(Z, DS, d['b'] + 0.5 / K6.FPS)
        if not (ok0 and ok1): M['c'].append(f'(c) {w}: không kẹp giữa hai khung 3D (trước: {w0}; sau: {w1})')
        # (d) máy ≤ 40 m AGL
        ag = _agl_doan(d)
        if ag:
            if max(ag) > MH_AGL + LEN: M['d'].append(f'(d) {w}: máy cao {max(ag):.0f} m AGL > {MH_AGL:g} m')
            near += K6.sat(f"{d['id']} AGL m", round(max(ag), 1), MH_AGL)
        # (e) sổ AI
        dl = _so_ai_rows(d, SA)
        if not dl: M['e'].append(f"(e) {w}: sổ AI không có dòng cho đoạn (so_ai của đoạn/shot, hoặc tệp so_ai: có shot/doan/ma = {d['ma']} hoặc tag = luot)")
        elif not any(_dong_ok(x) for x in dl): M['e'].append(f'(e) {w}: dòng sổ AI thiếu model / lệnh / SHA đầu ra')
    return K6.r(loi=sum(M.values(), []), thieu=th, muc=M, sat_nguong=near,
                val=f"{len(DS)} đoạn minh hoạ ({', '.join(d['id'] for d in DS[:6])}) · {tot:.1f} s = {pct:.1f} % · lỗi kẹp {len(M['c'])} · AGL {len(M['d'])} · sổ AI {len(M['e'])}"
                    + ' · nhãn: không bắt buộc (1.17.2)' + mt)


# ================================================================ EO-DAT R1–R4
def _chuong(s, Z_seg):
    return str(s.get('chuong') if s.get('chuong') is not None else Z_seg.get(str(s.get('shot')), '?'))


def eo_dat(E, TL, LS, why=None, ep_dir='.'):
    if LS is None: return {k: K6.r(thieu=[why or 'không có log shot'], val='—') for k in ROWS[1:5]}
    Z = _abs_t(LS); SEG = {str(s['id']): str(s.get('chuong', s.get('part', '?'))) for s in E.get('segments') or []}
    out = {}
    # ---- R1
    L1, th1, rows1, near1 = [], [], [], []
    for s, a, b in Z:
        if not s.get('chu_the_eo_dat'): continue
        sid = str(s.get('shot')); v = [x for _, x in _series(s.get('chu_the_pct'))]; vn = [x for _, x in _series(s.get('chu_the_pct_no'))]; nguon = 'khai'
        if s.get('chu_the_mat_na'):   # 1.17.2 (V2-D2): K tự đo pixel thô + vùng nở từ mặt nạ (số đo thật thắng số khai)
            try:
                q = [vung_no(K6._p(ep_dir, f)) for f in (s['chu_the_mat_na'] if isinstance(s['chu_the_mat_na'], list) else [s['chu_the_mat_na']])]
                v, vn, nguon = [x[0] for x in q], [x[1] for x in q], f'đo {len(q)} mặt nạ'
            except Exception as e: th1.append(f'(a) {sid}: không đọc được chu_the_mat_na ({type(e).__name__}: {e})'); continue   # noqa: BLE001
        if not v: th1.append(f'(a) {sid}: chu_the_eo_dat nhưng không có `chu_the_pct` (đo từ mặt nạ ID)'); continue
        med = statistics.median(v); mn = statistics.median(vn) if vn else None
        no = f' · vùng nở {R1_NO:g} % bề ngang {mn:.1f} %' if mn is not None else ' · vùng nở: chưa đo (`chu_the_mat_na` | `chu_the_pct_no`)'
        rows1.append(f'{sid}: pixel thô trung vị {med:.1f} %{no} ({nguon})')
        near1 += K6.sat(f'{sid} chủ thể %', round(med, 1), R1_MIN) + K6.sat(f'{sid} chủ thể %', round(med, 1), R1_TOT)
        if med < R1_MIN - LEN: L1.append(f'(a) {sid} @{K6.mmss(a)}: chủ thể {med:.1f} % khung (pixel thô) < {R1_MIN:g} %{no}')
        elif med < R1_TOT - LEN: L1.append(f'(b) {sid} @{K6.mmss(a)}: chủ thể {med:.1f} % khung (pixel thô) trong vùng {R1_MIN:g}–{R1_TOT:g} %{no}')
    n1 = sum(1 for s in LS if s.get('chu_the_eo_dat'))
    out['EO-DAT-R1'] = (K6.r(loi=L1, thieu=th1, sat_nguong=near1, muc={c_: [x for x in L1 + th1 if x.startswith(f'({c_})')] for c_ in 'ab'},
                             val=f'{n1} shot chu_the_eo_dat · ' + ('; '.join(rows1[:6]) or 'chưa đo') + ' · CHỈ BÁO mọi cổng (V2-D2, chủ dự án chấm bằng mắt)') if n1
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
        L3, th3, rows3, rows3n, near3 = [], [], [], [], []
        for s, a, b in dai:
            sid = str(s.get('shot')); w = f'{sid} @{K6.mmss(a)} ({b - a:.1f} s)'
            ng = s.get('so_goc') if _num(s.get('so_goc')) is not None else (len(s['goc_may']) if isinstance(s.get('goc_may'), list) else None)
            if ng is None: th3.append(f'(a) {w}: thiếu `so_goc` (hoặc `goc_may`)')
            elif ng < R3_GOC:
                nl, why_nl = r3_ngoai_le(s, ep_dir)
                if nl: rows3n.append(f'{sid}: {int(ng)} góc — ngoại lệ có khai ({nl})')
                else: L3.append(f'(a) {w}: {int(ng)} góc máy < {R3_GOC}' + (f' — {why_nl}' if why_nl else ''))
            # (b) 1.17.3 (khiếu nại A3): đầu mỗi góc máy (`goc_may[].t0 | t` > 0) là ranh như đầu/cuối shot (R3 "mỗi góc có biến cố ≤ 6 s");
            # mốc quy về lưới khung phim (round(t · 24) / 24) — video không hiện được biến cố giữa hai khung
            cg = {float(x.get('t0', x.get('t'))) for x in s.get('goc_may') or [] if isinstance(x, dict) and _num(x.get('t0', x.get('t'))) is not None and 0 < float(x.get('t0', x.get('t'))) < b - a}
            evr = {float(x['t']) for k in ('su_kien', 'tl_buoc') for x in s.get(k) or [] if isinstance(x, dict) and _num(x.get('t')) is not None and 0 <= x['t'] <= b - a}
            ev = sorted({round(t * K6.FPS) / K6.FPS for t in {0.0, b - a} | evr | cg})
            g = max((y - x for x, y in zip(ev, ev[1:])), default=b - a); rows3.append(f'{sid} {g:.2f} s'); near3 += K6.sat(f'{sid} khoảng biến cố s', round(g, 2), R3_GAP)
            if g > R3_GAP + LEN: L3.append(f'(b) {w}: khoảng không biến cố dài nhất {g:.2f} s > {R3_GAP:g} s ({len(evr)} biến cố log + {len(cg)} ranh góc máy)')
        out['EO-DAT-R3'] = K6.r(loi=L3, thieu=th3, sat_nguong=near3, muc={c_: [x for x in L3 if x.startswith(f'({c_})')] for c_ in 'ab'},
                                val=f'{len(dai)}/{len(eo)} shot eo đất > {R3_DAI:g} s · khoảng biến cố dài nhất (tính ranh góc máy, 1.17.3): ' + ', '.join(rows3[:8])
                                    + (' · ' + '; '.join(rows3n) if rows3n else ''))
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


def _authorship(ep_dir):
    """AUTHORSHIP.md của repo: tìm ngược từ thư mục episode.yaml lên gốc → nội dung hoặc None"""
    d = os.path.abspath(ep_dir or '.')
    for _ in range(12):
        f = os.path.join(d, 'AUTHORSHIP.md')
        if os.path.isfile(f): return open(f, encoding='utf-8').read()
        if os.path.dirname(d) == d: break
        d = os.path.dirname(d)
    return None


def r3_ngoai_le(s, ep_dir='.'):
    """1.17.3 (đề xuất K1173-D1 — chờ chủ dự án duyệt): shot eo đất > 15 s MỘT góc là ý đồ (vd. bookend) → log shot khai
    `r3_ngoai_le: {ly_do: "<lý do>", authorship: "YYYY-MM-DD HH:MM"}`. Chỉ nhận khi AUTHORSHIP.md có MỘT dòng chứa đúng ngày (YYYY-MM-DD), đúng giờ
    (HH:MM), id shot (N4_5 hoặc N4.5) và chữ "R3" — tức chủ dự án đã duyệt và P đã ghi. K không tự cho đạt: khai mà không có dòng → vẫn lỗi (a).
    → (mô tả ngoại lệ, None) | (None, lý do không nhận | None khi không khai)"""
    import re
    v = s.get('r3_ngoai_le')
    if not v: return None, None
    if not isinstance(v, dict) or not str(v.get('ly_do') or '').strip() or not str(v.get('authorship') or '').strip():
        return None, 'r3_ngoai_le khai thiếu `ly_do` hoặc `authorship` (ngày giờ dòng duyệt)'
    m = re.match(r'^\s*(\d{4}-\d{2}-\d{2})[ T]+(\d{1,2}:\d{2})\s*$', str(v['authorship']))
    if not m: return None, f"r3_ngoai_le.authorship {v['authorship']!r} không đúng dạng 'YYYY-MM-DD HH:MM'"
    A = _authorship(ep_dir)
    if A is None: return None, 'r3_ngoai_le: không tìm thấy AUTHORSHIP.md'
    sid = str(s.get('shot')); ids = {sid, sid.replace('_', '.')}
    ok = [l for l in A.splitlines() if m.group(1) in l and m.group(2) in l and 'R3' in l and any(re.search(r'(?<![\w.])' + re.escape(i) + r'(?![\w])', l) for i in ids)]
    if not ok: return None, f"r3_ngoai_le: AUTHORSHIP.md không có dòng {m.group(1)} {m.group(2)} nêu {sid} + R3 (chủ dự án chưa duyệt / P chưa ghi)"
    return f"{str(v['ly_do']).strip()[:60]} — AUTHORSHIP {m.group(1)} {m.group(2)}", None


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


def vung_no(path, no=R1_NO):
    """1.17.2 (V2-D2): mặt nạ chủ thể (PNG, trắng = chủ thể) → (% pixel thô, % vùng sau khi nở đĩa bán kính no % bề ngang khung)"""
    import cv2, numpy as np
    m = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if m is None: raise FileNotFoundError(path)
    b = (m > 127).astype(np.uint8); r = max(1, int(round(no / 100.0 * m.shape[1])))
    d = cv2.dilate(b, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
    return round(float(100 * b.mean()), 2), round(float(100 * d.mean()), 2)


# ================================================================ CONG-BO-1 (1.17.2)
def co_ai(E, LS, ep_dir='.'):
    """→ [mô tả nguồn khung AI]: đoạn minh hoạ khai, shot log ai_image, log khung lai.log_khung ai_image, shot đặc tả ai_image"""
    out = []
    if LS:
        DS, _ = doan_ai(LS)
        if DS: out.append(f"{len(DS)} đoạn minh hoạ ({', '.join(d['id'] for d in DS[:4])})")
        ai = [str(s.get('shot')) for s in LS if s.get('ai_image') is True]
        if ai: out.append(f"{len(ai)} shot log ai_image ({', '.join(ai[:4])})")
    lk = (E.get('lai') or {}).get('log_khung')
    if lk:
        n = 0
        for p in ([lk] if isinstance(lk, str) else lk):
            try: n += sum(1 for x in K6._load(K6._p(ep_dir, p)) or [] if isinstance(x, dict) and x.get('ai_image'))
            except Exception: pass   # noqa: BLE001 — log hỏng: K-LAI-1/2 báo
        if n: out.append(f'{n} khung log ai_image')
    sp = [f"{s['id']}/{i}" for s in E.get('segments') or [] for i, sh in enumerate(s.get('shots') or []) if sh.get('ai_image') or (sh.get('p') or {}).get('ai_image')]
    if sp: out.append(f"{len(sp)} shot đặc tả ai_image ({', '.join(sp[:4])})")
    return out


def giong_tong_hop(E):
    """→ mô tả nếu tập khai giọng tổng hợp: giong_tong_hop: true | vo/voice {tong_hop | synthetic: true | engine/nguon/model ~ elevenlabs/tts/synthetic}"""
    import re
    if E.get('giong_tong_hop') is True: return 'giong_tong_hop: true'
    for k in ('vo', 'voice', 'giong'):
        v = E.get(k)
        if not isinstance(v, dict): continue
        if v.get('tong_hop') is True or v.get('synthetic') is True: return f'{k}.tong_hop/synthetic: true'
        for f in ('engine', 'nguon', 'model', 'nha'):
            if v.get(f) and re.search(GIONG_RE, str(v[f]), re.I): return f'{k}.{f}: {v[f]}'
    return None


def cong_bo1(E, LS, ep_dir='.'):
    import re
    AI, GI = co_ai(E, LS, ep_dir), giong_tong_hop(E)
    if not AI and not GI: return K6.na('tập không có khung AI (đoạn minh hoạ / ai_image) và không khai giọng tổng hợp')
    M = {'a': [], 'b': []}; th = []; why = ' · '.join(AI + ([f'giọng tổng hợp ({GI})'] if GI else []))
    mt, w = K6.mo_ta(E, ep_dir)
    if mt is None: th.append(f'(a) {w} — cần câu công bố có "AI" hoặc "synthetic" trong mô tả YouTube của gói phát hành')
    else:
        cau = [c.strip() for c in re.split(r'(?<=[.!?])\s+|\n+', mt) if re.search(CB_RE, c, re.I)]
        if not cau: M['a'].append('(a) mô tả YouTube không có câu công bố chứa "AI" hoặc "synthetic"')
    ph = E.get('phat_hanh') if isinstance(E.get('phat_hanh'), dict) else {}
    ya = ph.get('youtube_altered_content')
    if ya is None: th.append('(b) đặc tả gói không khai phat_hanh.youtube_altered_content (cần true — "AI use" = Yes ở YouTube Studio)')
    elif ya is not True: M['b'].append(f'(b) phat_hanh.youtube_altered_content = {ya!r} (cần true)')
    return K6.r(loi=sum(M.values(), []), thieu=th, muc=M,
                val=f"áp vì: {why} · mô tả {'có câu công bố' if mt is not None and not M['a'] else 'thiếu/không câu' if mt is not None else 'không khai'} · youtube_altered_content {ya!r}")


def cong_cb(E):
    """cổng của CONG-BO-1: gói phát hành (`cong: phat_hanh` | `phat_hanh.goi: true`) → Chặn; trước đó chỉ báo"""
    ph = E.get('phat_hanh') if isinstance(E.get('phat_hanh'), dict) else {}
    if str(E.get('cong') or '') == 'phat_hanh' or ph.get('goi') is True: return 'phat_hanh'
    return 'animatic' if E.get('animatic') else 'G2'


# ================================================================ sửa luật cũ (chỉ ap_117)
def nam_log(LS):
    """{id đoạn: (năm đầu, năm cuối)} từ log shot `nam` [y0, y1] | số | `moc`"""
    out = {}
    for s in LS or []:
        v = s.get('nam') if s.get('nam') is not None else s.get('moc')
        ys = [float(x) for x in (v if isinstance(v, list) else [v]) if _num(x) is not None]
        if ys: out[str(s.get('shot'))] = (min(ys), max(ys))
    return out


JUMP_S = 0.125   # 1.17.3 (khiếu nại A5): hai mốc opt.time cách ≤ 3 khung (0,125 s) = BƯỚC NĂM (cắt thời gian) — năm giữa hai mốc không hiện


def nam_hien(E, TL=None):
    """1.17.3 (khiếu nại A5 BAN-CUOI-T3): {id đoạn: [(y0, y1), …]} = các KHOẢNG NĂM HIỆN TRÊN HÌNH, đọc từ đặc tả: đường cong `heroes.<p.hero>.opt.time`
    (bản sao độc lập tl7.timeline của trình dựng: JD + Hermite Fritsch–Carlson, mốc hold) lấy mẫu mỗi khung trong khung shot (frame0, speed);
    bước năm (hai mốc cách ≤ JUMP_S) tách khoảng. Đoạn không có cảnh opt.time → không có mục (k2check dùng `nam` của log shot như 1.17)."""
    from checks.ll import q_nhip
    H = dict(E.get('heroes') or {}, **((TL or {}).get('heroes') or {})); out = {}
    for sid, dur, _, shots, _ in q_nhip.view(E, TL):
        for j, sh in enumerate(shots):
            p = sh.get('p') or {}; o = (H.get(p.get('hero')) or {}).get('opt') or {}
            yr, K = q_nhip.tl_year(o)
            if yr is None: continue
            at = _num(sh.get('at')) or 0.0; end = _num(shots[j + 1].get('at')) if j + 1 < len(shots) else dur
            f0 = (_num(p.get('frame0', p.get('off', 0))) or 0.0) / K6.FPS; sp = _num(p.get('speed', 1)) or 1.0
            J = [(K[i][0], K[i + 1][0]) for i in range(len(K) - 1) if 0 < K[i + 1][0] - K[i][0] <= JUMP_S + LEN and K[i + 1][1] != K[i][1]]
            n = max(1, int(round(((end or at) - at) * K6.FPS))); runs = {}
            for f in range(n + 1):
                tau = f0 + min(f / K6.FPS, (end or at) - at) * sp
                if any(a_ + LEN < tau < b_ - LEN for a_, b_ in J): continue   # khung nằm giữa bước năm (≤ 3 khung chuyển) — không phải năm "hiện"
                k = sum(1 for a_, b_ in J if b_ - LEN <= tau)
                y = yr(tau); r_ = runs.setdefault(k, [y, y]); r_[0] = min(r_[0], y); r_[1] = max(r_[1], y)
            out.setdefault(str(sid), []).extend((round(a, 4), round(b, 4)) for a, b in runs.values())
    return out


def nam_khoang(E, TL=None, LS=None):
    """1.17.3: {id đoạn: [(y0, y1), …]} — năm hiện theo đặc tả (nam_hien) thắng; đoạn không có → `nam` của log shot (1.17)."""
    NL = {k: [v] for k, v in nam_log(LS).items()}
    try: NL.update(nam_hien(E, TL))
    except Exception: pass   # noqa: BLE001 — đặc tả lạ: giữ năm log
    return NL


def _khoang(y):
    if y is None: return None
    return [tuple(y)] if isinstance(y, tuple) and len(y) == 2 and all(_num(v) is not None for v in y) else [tuple(v) for v in y]


def q33_mien(allap, NL):
    """lần xuất hiện được miễn (TL-1): khác đoạn VÀ khoảng năm không chồng MỌI lần trước (khai hay pHash). → tập id(ap).
    NL = {đoạn: (y0, y1)} (1.17, năm log) hoặc {đoạn: [(y0, y1), …]} (1.17.3, các khoảng năm hiện — nam_khoang)."""
    if not NL: return set()
    seg = lambda x: str(x.get('seg') or (x.get('shots') or ['?/'])[0].split('/')[0])
    cho = lambda A, B: any(not (a[1] < b[0] or a[0] > b[1]) for a in A for b in B)
    seen, mien = [], set()
    for a in sorted(allap, key=lambda x: x['t0']):
        y = _khoang(NL.get(seg(a)))
        if seen and y and all(seg(p) != seg(a) for p, _ in seen) and all(py and not cho(y, py) for _, py in seen):
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
    try: out.update(eo_dat(E, TL, LS, why, ep_dir))
    except Exception as e: out.update({k: K6.r(thieu=[f'không chạy được: {type(e).__name__}: {e}'], val='—') for k in ROWS[1:5]})   # noqa: BLE001
    cong = 'animatic' if E.get('animatic') else 'G2'
    out = {k: dict(v, cong=cong) for k, v in out.items()}
    try: out['CONG-BO-1'] = cong_bo1(E, LS, ep_dir)
    except Exception as e: out['CONG-BO-1'] = K6.r(thieu=[f'không chạy được: {type(e).__name__}: {e}'], val='—')   # noqa: BLE001
    out['CONG-BO-1'] = dict(out['CONG-BO-1'], cong=cong_cb(E))
    return out
