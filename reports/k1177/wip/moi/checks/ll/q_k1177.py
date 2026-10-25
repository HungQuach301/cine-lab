#!/opt/cine/bin/python
"""Luật 1.17.7 (phiên K-1.17.7, 25/10/2026) — CHỈ tập kênh 2 từ T4 (`kenh2_tu_t4: true` hoặc khối `n2p:`). T3 và trước: KHÔNG ÁP (không hồi tố).
Căn cứ (nguyên văn, Asia/Saigon): chủ dự án 25/10 09:08 "Vấn đề tôi concern nhất là chỉ phí bị đội nhiều, còn các vấn đề khác đều có thể nới để
tăng chất lượng và độ chân thực của hình ảnh / Người xem cũng không phải là người chuyên về khảo cổ hay gì để có thể nhận ra những dự khác biệt nhỏ
trong những frame hình ngắn"; 09:15 "Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị"; 06:56 C11, C13 theo khuyến nghị. Khiếu nại ANIMATIC-T4
A1–A5 + C13 (checks-appeal.md, mục K-1.17.7). Số đo, hiệu chuẩn, tiêu chí: reports/k1177/.
Mỗi luật: tham số theo tập, MẶC ĐỊNH GIỮ HÀNH VI CŨ khi tập không khai.

GOC-CAO (thay GOC-CAO-60 trong k2check cho tập từ T4):
  (p) góc cao có thời gian chạy ≥ `goc_cao_min_pct` % thân phim (mặc định 60; nhận 50–100; < 50 hoặc không phải số → (k), dùng 60). Đo như
      GOC-CAO-60 (shot `goc: cao` + `tl: true`; có log máy → tỉ lệ khung đạt V7B-D1) TRỪ giây lớp THAT (ảnh/footage thật không tính góc cao).
  5 chốt cấu trúc — BẬT khi `goc_cao_min_pct` < 60, hoặc khai `goc_cao_cau_truc: true`, hoặc khai `goc_cao_chuong_min_pct` (hạ ngưỡng phải đổi
  bằng cấu trúc). "Shot góc cao" = goc cao, không M-d, không THAT; có log máy → ≥ 50 % khung đạt V7B-D1. Thân phim = mọi shot trừ thẻ PP.
  (a) mỗi chương (`chuong` của log shot) MỞ và KẾT bằng shot góc cao;
  (b) điểm máy xương sống (`goc_cao_p1`, mặc định "P1") tái xuất ≥ 1 lần MỖI HỒI (chương có tên bắt đầu "HỒI"/"HOI"/"ACT", hoặc danh sách
      `goc_cao_hoi`): shot khai `diem_may` = P1 (hoặc KHOP với shot P1) và — khi có log máy — có khung CÙNG KHUNG với khung đầu của shot P1 đầu
      tiên trong phim (vị trí ≤ 1 m, hướng nhìn ≤ 1°, cùng FOV); không log → nhận theo khai ở animatic, THIẾU ở G2;
  (c) ≤ 2 shot liền nhau (thứ tự phim, bỏ thẻ PP) thuộc {góc thấp (`goc` thap/can/…), cận, M-d, ảnh/footage thật};
  (d) mỗi chương: giây góc cao ≥ `goc_cao_chuong_min_pct` % thời lượng chương (mặc định 40 khi chốt bật);
  (e) TL-1 (a) mục tiêu cảnh báo `tl1_muc_tieu_pct` (mặc định 75; T4 khai 60) — áp trong q_k116.tl1 (hàng TL-1, luôn Cảnh báo).
  Cấp: Chặn ở G2 · Cảnh báo ở animatic (cap112); (w) luôn Cảnh báo.
TU-LIEU (q_k1176): `tu_lieu_tran_pct` nhận tới 20 (T4 khai 20); lớp THAT tính vào tư liệu (TU-LIEU-10 (a)(b), TU-LIEU-OMNI); hàng mới
  TU-LIEU-THAT: (a) shot THAT không khai AI (minh_hoa/ai_image/ai_texture/ai_nen); (b) không tính góc cao — khai `goc: cao` → (w) nhắc;
  (g) footage HIỆN ĐẠI (`that.hien_dai: true` hoặc `that.loai: footage_hien_dai`) phải khai `that.giay_phep: {tep, sha256}` (tệp bằng chứng có thật,
  SHA khớp) — thiếu/khác → THIẾU (Chặn ở G2). Mỗi lần ≤ 10 s và không trùng/ghép liền clip M-d: TU-LIEU-10 (b) + TU-LIEU-OMNI (giữ).
K-LAI-1 theo Q2 (C11): tập từ T4 — minh hoạ M-d (đoạn `minh_hoa`) KHÔNG tính trần 20 % `ai_image` (đã tính ở MINH-HOA / N2P-6, tổng AI ≤ 70 %);
  shot/khung ai_image NGOÀI M-d vẫn ≤ 20 %. T3 giữ (q_lai không đổi).
TL-1 (c) nhịp cắt (P9; q_k116.tl1, tập từ T4): cắt đo trên video khớp (±0,5 s) RANH VÀO/RA đoạn M-d và lần tư liệu/ảnh thật (shot THAT, `tu_lieu_lan`
  có giờ) không tính vào số cắt/phút (như miễn cắt góc R3); in số trước/sau miễn.
NHAN-VAT-TEN (P2 b): đoạn M-d khai `nhan_vat_ten` (chuỗi | danh sách) phải khai `chan_dung_tham_chieu` ({tep, sha256} | danh sách — tệp có thật, SHA
  khớp) và `duyet_chu_du_an` (dòng AUTHORSHIP/ngày giờ chủ dự án duyệt); thiếu → THIẾU (Chặn ở G2). Phép đo: bộ dò mặt YuNet chạy máy (checks/models/
  face_detection_yunet_2023mar.onnx, không API) trên video đoạn (`clip` khai, hoặc master [t0, t1]) mỗi 2 khung: mặt lớn nhất (điểm ≥ MAT_DIEM 0,75)
  cao ≤ 1/8 chiều cao khung → ĐẠT; lớn hơn → (a) TRƯỢT (cận mặt); hộp điểm 0,60–0,75 cao > 1/8 → (w) nghi cận mặt, người soi (hiệu chuẩn:
  reports/k1177 §5 — dưới 0,75 lẫn lửa/khói).
KIEM-2-MUC (gói tiết kiệm): BẬT khi episode.yaml khai `kiem_2_muc: true` hoặc đoạn M-d nào khai `muc_kiem`. Mỗi đoạn M-d: `muc_kiem: day_du | nen`
  (thiếu → (k)); `luot` (số lượt sinh); `kiem_t1` (tệp kiểm tầng Flash, kết luận ĐẠT…); `kiem` (tầng 2: gpt + q_thoi_dai mỗi khung, ket_luan_may ĐẠT);
  `to_khung` (tờ khung soi tay). (a) đoạn có `nhan_vat_ten`, `cong_trinh_moc` (danh sách) hoặc `chan_troi_city: true` BẮT BUỘC day_du;
  (b) nen: kiem_t1 ĐẠT + to_khung có thật; day_du: kiem_t1 ĐẠT + kiem tầng 2 ĐẠT có q_thoi_dai mỗi khung; (c) nen ≤ 2 lượt, day_du ≤ 3 lượt;
  (d) đoạn có `cong_trinh_moc`/`chan_troi_city`: q_thoi_dai tầng 2 phải chạy đề bài lớp công trình mốc (PROMPT_VER_MOC). Chặn ở G2 · Cảnh báo animatic.
"""
import hashlib, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

GOC_CAO_MAC_DINH, GOC_CAO_SAN_DUYET = 60.0, 50.0     # goc_cao_min_pct: mặc định 60 (Q2 iii); thấp nhất chủ dự án duyệt 50 (T4, 25/10 09:15)
GOC_CHUONG_MAC_DINH = 40.0                           # goc_cao_chuong_min_pct khi chốt cấu trúc bật mà không khai
LIEN_MAX = 2                                         # (c) ≤ 2 shot liền thuộc {thấp, cận, M-d, THAT}
P1_TOL_M, P1_TOL_DEG = 1.0, 1.0                      # (b) cùng khung với P1: vị trí ≤ 1 m, hướng ≤ 1°, cùng FOV
V7B_SHOT = 0.5                                       # shot góc cao có log: ≥ 50 % khung đạt V7B-D1
GOC_THAP = ('thap', 'can', 'can_canh', 'cận', 'thấp', 'luot_thap')
HOI_TIEN_TO = ('HỒI', 'HOI', 'ACT')
MAT_TRAN = 1.0 / 8.0                                 # mặt ≤ 1/8 chiều cao khung
MAT_DIEM, MAT_DIEM_W = 0.75, 0.60                    # điểm YuNet: ≥ 0,75 tính (hiệu chuẩn 23 clip M-d T4); 0,60–0,75 > 1/8 → (w)
MAT_BUOC = 2                                         # đo mỗi 2 khung
MODEL_MAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'face_detection_yunet_2023mar.onnx')
LUOT = dict(nen=2, day_du=3)


def ap_1177(E): return bool(E.get('kenh2_tu_t4') or E.get('n2p'))


def _num(x): return isinstance(x, (int, float)) and not isinstance(x, bool)


def _K(): from checks.ll import q_k1174 as K; return K   # noqa: E702


# ================================================================ GOC-CAO
def goc_cao_min(E):
    """→ (ngưỡng %, lỗi khai | None)"""
    v = E.get('goc_cao_min_pct')
    if v is None: return GOC_CAO_MAC_DINH, None
    if not _num(v) or float(v) > 100: return GOC_CAO_MAC_DINH, f'(k) goc_cao_min_pct {v!r} không phải số 50–100 — dùng {GOC_CAO_MAC_DINH:g} %'
    if float(v) < GOC_CAO_SAN_DUYET - 1e-9:
        return GOC_CAO_MAC_DINH, f'(k) goc_cao_min_pct {v:g} < {GOC_CAO_SAN_DUYET:g} % (thấp nhất chủ dự án duyệt, gói 50 % tiết kiệm 25/10/2026 09:15) — dùng {GOC_CAO_MAC_DINH:g} %'
    return float(v), None


def cau_truc_bat(E, gmin):
    return bool(E.get('goc_cao_cau_truc')) or gmin < GOC_CAO_MAC_DINH - 1e-9 or E.get('goc_cao_chuong_min_pct') is not None


def chuong_min(E):
    v = E.get('goc_cao_chuong_min_pct')
    if v is None: return GOC_CHUONG_MAC_DINH, None
    if not _num(v) or not 0 <= float(v) <= 100: return GOC_CHUONG_MAC_DINH, f'(k) goc_cao_chuong_min_pct {v!r} không phải số 0–100 — dùng {GOC_CHUONG_MAC_DINH:g} %'
    return float(v), None


def _la_hoi(ch, E):
    if isinstance(E.get('goc_cao_hoi'), list): return str(ch) in [str(x) for x in E['goc_cao_hoi']]
    return str(ch).strip().upper().startswith(HOI_TIEN_TO)


def _log(s, E, ep_dir):
    K = _K()
    try: return K.chuan_log(K._ld(ep_dir, s.get('log_may')), tuple(E.get('goc_toa_do') or K.GOC0))
    except Exception: return None   # noqa: BLE001


def goc_cao(E, TL, LS, ep_dir='.', cong=None):
    cong = cong or ('animatic' if E.get('animatic') else 'G2')
    K = _K(); K6 = K.K6
    if LS is None: return K.r(thieu=['không có log shot'], val='—', cong=cong)
    gmin, lk = goc_cao_min(E); ct = cau_truc_bat(E, gmin); cmin, lk2 = chuong_min(E) if ct else (None, None)
    M = {k: [] for k in 'pabcdkw'}; M['k'] += [x for x in (lk, lk2) if x]
    T = K6.tong(E, TL) if (TL or E.get('segments')) else sum(K._dur(s) for s in LS)
    PPd = sum(b - a for _, a, b, _ in K6.pp_spans(E, TL)) if (TL or E.get('segments')) else sum(K._dur(s) for s in LS if K._cu(s) == 'PP')
    Tb = T - PPd; Z = sorted(LS, key=lambda s: float(s.get('t0') or 0)); D = {}
    cao_s, nlog, cao_shot = 0.0, 0, {}
    for s in Z:
        w = str(s.get('shot')); d = K._dur(s); that = K._lop(s, 'THAT')
        L = _log(s, E, ep_dir) if s.get('log_may') else None
        ty = None
        if L:
            nlog += 1; ty = K.do_shot(L, K._tieu_diem(s, E), float(s.get('mat_dat_m') or E.get('mat_dat_m') or 0))['v7b_ty']; D[w] = (L, ty)
        g = K6.goc_of(s, E); la_that = K.la_that(s)
        if s.get('tl') and g == 'cao' and not la_that: cao_s += max(0.0, d - that) * (ty if ty is not None else 1.0)
        cao_shot[w] = g == 'cao' and not s.get('minh_hoa') and not la_that and K._cu(s) not in K.KHONG_MAY and (ty is None or ty >= V7B_SHOT)
    nog = [str(s.get('shot')) for s in LS if K6.goc_of(s, E) is None and K._cu(s) not in K.KHONG_MAY]
    p = 100 * cao_s / Tb if Tb else 0.0; near = K.sat('góc cao %', round(p, 1), gmin)
    if p < gmin - 1e-9: M['p'].append(f'(p) góc cao timelapse {cao_s:.1f} s = {p:.1f} % < {gmin:g} % thân phim ({Tb:.1f} s)' + (' (khai goc_cao_min_pct)' if E.get('goc_cao_min_pct') is not None and not lk else ''))
    th = [f'(p) {len(nog)} shot không khai `goc` ({", ".join(nog[:6])})'] if nog and not M['p'] else []
    val = f'{cao_s:.1f} s / {Tb:.1f} s = {p:.1f} % / ngưỡng {gmin:g} % (log khung V7B-D1: {nlog} shot)'
    if ct:
        body = [s for s in Z if K._cu(s) != 'PP']
        chs = []
        for s in body:
            c = str(s.get('chuong', '?'))
            if not chs or chs[-1][0] != c: chs.append((c, []))
            chs[-1][1].append(s)
        # (a) mở/kết chương
        for c, ss in chs:
            for nm, s in (('mở', ss[0]), ('kết', ss[-1])):
                if not cao_shot.get(str(s.get('shot'))): M['a'].append(f"(a) chương {c}: {nm} bằng {s.get('shot')} ({K6.goc_of(s, E) or '—'}{', M-d' if s.get('minh_hoa') else ''}{', THAT' if K.la_that(s) else ''}) — phải là shot góc cao")
        # (b) P1 mỗi hồi
        p1 = str(E.get('goc_cao_p1') or 'P1'); ref = None
        for s in Z:
            if str(s.get('diem_may')) == p1 and str(s.get('shot')) in D:
                f0 = sorted(D[str(s.get('shot'))][0]['frames'], key=lambda x: x.get('f', 0))[0]['cam']; ref = (f0, str(s.get('shot'))); break

        def cung_khung(s):
            w = str(s.get('shot'))
            if w not in D: return None
            if ref is None: return None
            import numpy as np
            pr, lr = np.array(ref[0]['p'], float), np.array(ref[0]['l'], float); dr = (lr - pr) / np.linalg.norm(lr - pr)
            for fr in D[w][0]['frames']:
                c_ = fr['cam']; p_, l_ = np.array(c_['p'], float), np.array(c_['l'], float); d_ = (l_ - p_) / np.linalg.norm(l_ - p_)
                if np.linalg.norm(p_ - pr) <= P1_TOL_M and np.degrees(np.arccos(np.clip(d_ @ dr, -1, 1))) <= P1_TOL_DEG and abs(float(c_.get('fov') or 0) - float(ref[0].get('fov') or 0)) < 1e-6: return True
            return False
        sp1 = {str(s.get('shot')) for s in Z if str(s.get('diem_may')) == p1}
        for c, ss in chs:
            if not _la_hoi(c, E): continue
            ung = [s for s in ss if str(s.get('diem_may')) == p1 or (K._cu(s) == 'KHOP' and str(s.get('khop_voi')) in sp1)]
            ok_ = [s for s in ung if cung_khung(s) is True]; khong_log = [s for s in ung if cung_khung(s) is None]
            if ok_: continue
            if khong_log and cong == 'animatic': M['w'].append(f"(w) hồi {c}: P1 nhận theo khai ({', '.join(str(s.get('shot')) for s in khong_log[:3])}) — chưa đo cùng khung (thiếu log máy)"); continue
            if khong_log: th.append(f"(b) hồi {c}: shot P1 ({', '.join(str(s.get('shot')) for s in khong_log[:3])}) không có log máy — ở G2 phải đo cùng khung"); continue
            M['b'].append(f"(b) hồi {c}: điểm máy {p1} không tái xuất (cùng khung với {ref[1] if ref else p1}: ≤ {P1_TOL_M:g} m, ≤ {P1_TOL_DEG:g}°, cùng FOV)" + (f" — {len(ung)} shot khai {p1} nhưng khác khung" if ung else ''))
        # (c) ≤ 2 liền {thấp, cận, M-d, THAT}
        run = []
        for s in body:
            g = str(K6.goc_of(s, E) or '').lower(); thuoc = g in GOC_THAP or bool(s.get('minh_hoa')) or K.la_that(s)
            run = run + [s] if thuoc else []
            if len(run) == LIEN_MAX + 1: M['c'].append(f"(c) {', '.join(str(x.get('shot')) for x in run)}: {len(run)} shot liền thuộc {{thấp, cận, M-d, ảnh/footage thật}} > {LIEN_MAX}")
        # (d) % mỗi chương
        pc_ch = []
        for c, ss in chs:
            tc = sum(K._dur(s) for s in ss); cs = 0.0
            for s in ss:
                w = str(s.get('shot'))
                if s.get('tl') and K6.goc_of(s, E) == 'cao' and not K.la_that(s): cs += max(0.0, K._dur(s) - K._lop(s, 'THAT')) * (D[w][1] if w in D else 1.0)
            pcc = 100 * cs / tc if tc else 0.0; pc_ch.append(f'{c} {pcc:.0f}'); near += K.sat(f'góc cao chương {c} %', round(pcc, 1), cmin)
            if pcc < cmin - 1e-9: M['d'].append(f'(d) chương {c}: góc cao {cs:.1f} s = {pcc:.1f} % < {cmin:g} % thời lượng chương ({tc:.1f} s)')
        val += (f' · cấu trúc: mở/kết {len(M["a"])} lỗi · P1/hồi {len(M["b"])} · liền {len(M["c"])} · chương ≥ {cmin:g} %: ' + ', '.join(pc_ch))
    else: val += ' · chốt cấu trúc TẮT (ngưỡng 60 %, không khai goc_cao_cau_truc)'
    loi = M['p'] + M['a'] + M['b'] + M['c'] + M['d'] + M['k'] + M['w']
    return K.r(loi, th, val, muc=M, sat_nguong=near, cong=cong, pct=round(p, 2), nguong=gmin, cau_truc=ct)


# ================================================================ TU-LIEU-THAT
def _sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def _tep_sha(x, ep_dir, ten):
    """{tep, sha256} | [..] → [lỗi]"""
    K = _K(); out = []
    for y in (x if isinstance(x, list) else [x]):
        if not isinstance(y, dict) or not y.get('tep') or not y.get('sha256'): out.append(f'{ten} phải là {{tep, sha256}} (có {y!r:.60})'); continue
        p = K.K6._p(ep_dir, y['tep'])
        if not os.path.exists(p): out.append(f"{ten}: tệp {y['tep']} không có"); continue
        if _sha(p) != str(y['sha256']).lower(): out.append(f"{ten}: SHA {y['tep']} khác khai ({str(y['sha256'])[:12]}…)")
    return out


def tu_lieu_that(E, LS, ep_dir='.', cong=None):
    cong = cong or ('animatic' if E.get('animatic') else 'G2')
    K = _K()
    if LS is None: return K.r(thieu=['không có log shot'], val='—', cong=cong)
    M = {'a': [], 'g': [], 'w': []}; n, s_ = 0, 0.0
    for s in LS:
        v = K._lop(s, 'THAT')
        if v <= 0 and not s.get('that'): continue
        n += 1; s_ += v or K._dur(s); w = str(s.get('shot')); T = s.get('that') if isinstance(s.get('that'), dict) else {}
        ai = [k for k in ('minh_hoa', 'ai_image', 'ai_texture', 'ai_nen') if s.get(k)]
        if ai: M['a'].append(f"(a) {w}: ảnh/footage thật khai {', '.join(ai)} — lớp THAT không có AI")
        if K.la_that(s) and str(s.get('goc') or '') == 'cao': M['w'].append(f'(w) {w}: shot THAT khai goc cao — không tính vào góc cao (GOC-CAO)')
        if s.get('that') and v <= 0: M['g'].append(f'(g) {w}: shot khai `that` nhưng không khai `lop.THAT` (giây) — không tính được vào trần tư liệu')
        if T.get('hien_dai') or str(T.get('loai') or '') == 'footage_hien_dai':
            if not T.get('giay_phep'): M['g'].append(f'(g) {w}: footage hiện đại chưa khai `that.giay_phep: {{tep, sha256}}` (tệp bằng chứng giấy phép)')
            else: M['g'] += [f'(g) {w}: {x}' for x in _tep_sha(T['giay_phep'], ep_dir, 'that.giay_phep')]
    if not n: return dict(K.na('không có shot/lớp ảnh chụp/footage thật (THAT)'), cong=cong)
    return K.r(M['a'] + M['w'], M['g'], val=f'{n} shot có lớp THAT · {s_:.1f} s (tính vào tư liệu, không tính AI, không tính góc cao)', muc=M, cong=cong)


# ================================================================ K-LAI-1 theo Q2 (C11)
def klai1_t4(E, TL, LS, ep_dir='.'):
    from checks.ll import q_lai as LA
    K = _K()
    DS, SH, _ = LA.log_ai(LS) if LS else ([], [], [])
    T, src = LA.tong_s(E, TL, E.get('lai') or {})
    if T is None and LS: T, src = sum(b - a for _, a, b in LA.q_k117_abs(LS)), 'tổng thời lượng log shot'
    if T is None: return K.r(thieu=['không biết thời lượng phim'], val='—')
    md = sum(d['b'] - d['a'] for d in DS); win = [(d['a'], d['b']) for d in DS]
    L = E.get('lai') or {}; F = None
    if L.get('log_khung'):
        try: F = LA.frames(L, ep_dir)
        except Exception: F = None   # noqa: BLE001
    if F is not None:
        ngoai = [x for x in F if LA.is_ai(x) and not any(a - 1e-6 <= x['f'] / LA.FPS < b + 1e-6 for a, b in win)]
        s_ngoai, nguon = len(ngoai) / LA.FPS, f'log khung ({len(F)} khung)'
    else: s_ngoai, nguon = sum(b - a for _, a, b in SH), f'log shot ({len(SH)} shot ai_image ngoài M-d)'
    pn = s_ngoai / T if T else 0.0
    loi = [f'{s_ngoai:.2f} s khung ai_image/ai_texture NGOÀI minh hoạ M-d = {100 * pn:.1f} % > {100 * LA.AI_MAX:.0f} % thời lượng'] if pn > LA.AI_MAX else []
    return K.r(loi, val=f'1.17.7 (Q2/C11): minh hoạ M-d {md:.2f} s ({100 * md / T:.1f} %) tính ở MINH-HOA/N2P-6 (tổng AI ≤ 70 %), không tính trần 20 % · AI ngoài M-d '
               f'{s_ngoai:.2f} s / {T:.2f} s ({src}) = {100 * pn:.1f} % · nguồn: {nguon}', sat_nguong=K.sat('tỷ lệ AI ngoài M-d', round(pn, 4), LA.AI_MAX),
               ty_le=round(pn, 4), giay=round(s_ngoai, 2), md_giay=round(md, 2))


# ================================================================ TL-1 (c) miễn ranh M-d / tư liệu / ảnh thật (P9)
def ranh_mien(LS):
    """→ [giây tuyệt đối] ranh vào/ra đoạn M-d, shot THAT, lần tư liệu có giờ (`tu_lieu_lan`) — gộp ranh cách nhau < 0,25 s"""
    from checks.ll import q_k117 as K7
    K = _K(); r = []
    if not LS: return r
    DS, _ = K7.doan_ai(LS)
    r += [d['a'] for d in DS] + [d['b'] for d in DS]
    for s, a, b in K7._abs_t(LS):
        if K.la_that(s): r += [a, b]
        for x in s.get('tu_lieu_lan') or []:
            if isinstance(x, dict) and _num(x.get('t0')) and _num(x.get('t1')): r += [float(x['t0']), float(x['t1'])]
    out = []
    for t in sorted(r):
        if not out or t - out[-1] >= 0.25: out.append(t)
    return out


def cat_mien(ranh, cv, tol, da=()):
    """mỗi ranh miễn tối đa MỘT cắt đo gần nhất trong ±tol (không trùng cắt đã miễn khác) → [giây cắt miễn]"""
    out = []
    for t in ranh:
        c = [x for x in cv if abs(x - t) <= tol and x not in out and x not in da]
        if c: out.append(min(c, key=lambda x: abs(x - t)))
    return sorted(out)


# ================================================================ NHAN-VAT-TEN
_DET = {}


def det_mat():
    import cv2
    if 'y' not in _DET: _DET['y'] = cv2.FaceDetectorYN.create(os.path.abspath(MODEL_MAT), '', (320, 320), MAT_DIEM_W, 0.3, 5000)
    return _DET['y']


def mat_khung(f):
    """→ [(cao/H, điểm, hộp)] mọi mặt điểm ≥ MAT_DIEM_W"""
    d = det_mat(); H, W = f.shape[:2]; d.setInputSize((W, H)); _, fa = d.detect(f)
    return [] if fa is None else [(float(z[3]) / H, float(z[14]), [int(v) for v in z[:4]]) for z in fa]


def do_mat(video, t0=None, t1=None, buoc=MAT_BUOC):
    """→ dict(khung, max_ty (điểm ≥ MAT_DIEM), khung_max, nghi [(f, ty, điểm)] (0,60–0,75 > 1/8), tren [(f, ty, điểm)])"""
    import cv2
    cap = cv2.VideoCapture(video); fps = cap.get(cv2.CAP_PROP_FPS) or 24.0; i = 0; n = 0; mx, fm = 0.0, None; nghi, tren = [], []
    if t0 is not None: cap.set(cv2.CAP_PROP_POS_MSEC, 1000.0 * t0); i = int(round(t0 * fps))
    while True:
        ok, f = cap.read()
        if not ok or (t1 is not None and i / fps > t1 + 1e-6): break
        if (i - (int(round(t0 * fps)) if t0 is not None else 0)) % buoc == 0:
            n += 1
            for ty, sc, _ in mat_khung(f):
                if sc >= MAT_DIEM:
                    if ty > mx: mx, fm = ty, i
                    if ty > MAT_TRAN: tren.append((i, round(ty, 3), round(sc, 2)))
                elif ty > MAT_TRAN: nghi.append((i, round(ty, 3), round(sc, 2)))
        i += 1
    return dict(khung=n, max_ty=round(mx, 4), khung_max=fm, nghi=nghi, tren=tren)


def _doan_md(LS):
    from checks.ll import q_k117 as K7
    DS, _ = K7.doan_ai(LS or [])
    g = lambda d, k: (d['m'] or {}).get(k) if (d['m'] or {}).get(k) is not None else d['s'].get(k)
    return DS, g


def nhan_vat_ten(E, TL, LS, ep_dir='.', video=None, cong=None):
    cong = cong or ('animatic' if E.get('animatic') else 'G2')
    K = _K()
    if LS is None: return K.r(thieu=['không có log shot'], val='—', cong=cong)
    DS, g = _doan_md(LS); M = {'a': [], 'k': [], 'u': [], 'm': [], 'w': []}; n = 0; so = []
    for d in DS:
        nv = g(d, 'nhan_vat_ten')
        if not nv: continue
        n += 1; w = d['id']; ten = ', '.join(nv) if isinstance(nv, list) else str(nv)
        cd = g(d, 'chan_dung_tham_chieu')
        if not cd: M['k'].append(f'(k) {w} ({ten}): chưa khai `chan_dung_tham_chieu: {{tep, sha256}}`')
        else: M['k'] += [f'(k) {w}: {x}' for x in _tep_sha(cd, ep_dir, 'chan_dung_tham_chieu')]
        if not g(d, 'duyet_chu_du_an'): M['u'].append(f'(u) {w} ({ten}): chưa khai `duyet_chu_du_an` (dòng AUTHORSHIP chủ dự án duyệt nhân vật có tên trong M-d)')
        clip = g(d, 'clip'); src = None
        try:
            if clip and os.path.exists(K.K6._p(ep_dir, clip)): R = do_mat(K.K6._p(ep_dir, clip)); src = 'clip'
            elif video and os.path.exists(video): R = do_mat(video, d['a'], d['b']); src = f"master {d['a']:.1f}–{d['b']:.1f} s"
            else: R = None
        except Exception as e: R = None; M['m'].append(f'(m) {w}: không đo được mặt: {type(e).__name__}: {e}')   # noqa: BLE001
        if R is None:
            if not any(x.startswith(f'(m) {w}') for x in M['m']): M['m'].append(f'(m) {w}: không có video để đo mặt (khai `clip` của đoạn hoặc chạy k2check có --master)')
            continue
        so.append(f"{w} {R['max_ty']:.3f}")
        if R['tren']: M['a'].append(f"(a) {w} ({ten}): mặt cao {max(x[1] for x in R['tren']):.3f} khung > 1/8 ở {len(R['tren'])}/{R['khung']} khung đo (đầu tiên khung {R['tren'][0][0]}, {src}) — cận mặt nhân vật có tên")
        if R['nghi']: M['w'].append(f"(w) {w}: {len(R['nghi'])} hộp điểm {MAT_DIEM_W:g}–{MAT_DIEM:g} cao > 1/8 (lớn nhất {max(x[1] for x in R['nghi']):.3f} @khung {R['nghi'][0][0]}) — người soi: có phải mặt cận?")
    if not n: return dict(K.na('không đoạn M-d nào khai nhan_vat_ten'), cong=cong)
    return K.r(M['a'] + M['k'] + M['w'], M['u'] + M['m'], val=f'{n} đoạn M-d có nhân vật có tên · mặt lớn nhất/khung: ' + (', '.join(so) or '—') + f' (trần 1/8 = {MAT_TRAN:.3f}; YuNet điểm ≥ {MAT_DIEM:g})',
               muc=M, cong=cong)


# ================================================================ KIEM-2-MUC
def _kl(J):
    k = J.get('ket_luan_may') if isinstance(J.get('ket_luan_may'), dict) else J
    return str(k.get('ket_qua') or k.get('ket_luan') or '')


def kiem_2_muc(E, LS, ep_dir='.', cong=None):
    cong = cong or ('animatic' if E.get('animatic') else 'G2')
    K = _K()
    if LS is None: return K.r(thieu=['không có log shot'], val='—', cong=cong)
    DS, g = _doan_md(LS)
    if not (E.get('kiem_2_muc') or any(g(d, 'muc_kiem') for d in DS)): return dict(K.na('tập không khai kiem_2_muc / muc_kiem — giữ kiểm hiện hành (K-LAI-3)'), cong=cong)
    from checks.ll import q_thoi_dai as QT
    M = {k: [] for k in 'abcdk'}; dem = {'day_du': 0, 'nen': 0}
    for d in DS:
        w = d['id']; mk = g(d, 'muc_kiem')
        bb = [k for k in ('nhan_vat_ten', 'cong_trinh_moc', 'chan_troi_city') if g(d, k)]
        if mk not in ('day_du', 'nen'): M['k'].append(f'(k) {w}: `muc_kiem` {mk!r} — phải là day_du | nen'); continue
        dem[mk] += 1
        if bb and mk != 'day_du': M['a'].append(f"(a) {w}: có {', '.join(bb)} → BẮT BUỘC muc_kiem: day_du (khai {mk})")
        lu = g(d, 'luot')
        if not _num(lu): M['c'].append(f'(c) {w}: chưa khai `luot` (số lượt sinh)')
        elif int(lu) > LUOT[mk]: M['c'].append(f'(c) {w}: {int(lu)} lượt > {LUOT[mk]} (mức {mk})')

        def doc(k):
            p = g(d, k)
            if not p: return None, f'chưa khai `{k}`'
            try: return K.K6._load(K.K6._p(ep_dir, p)), None
            except Exception as e: return None, f'không đọc được {k} ({p}): {e}'   # noqa: BLE001
        T1, e1 = doc('kiem_t1')
        if e1: M['b'].append(f'(b) {w}: tầng Flash: {e1}')
        elif not _kl(T1).upper().startswith('ĐẠT'): M['b'].append(f'(b) {w}: tầng Flash kết luận {_kl(T1)!r} (cần ĐẠT)')
        if mk == 'nen':
            tk = g(d, 'to_khung')
            if not tk or not os.path.exists(K.K6._p(ep_dir, tk)): M['b'].append(f'(b) {w}: mức nen cần `to_khung` (tờ khung soi tay) có thật' + (f' — {tk} không có' if tk else ''))
            continue
        T2, e2 = doc('kiem')
        if e2: M['b'].append(f'(b) {w}: tầng 2: {e2}'); continue
        if not _kl(T2).upper().startswith('ĐẠT'): M['b'].append(f'(b) {w}: tầng 2 kết luận máy {_kl(T2)!r} (cần ĐẠT)')
        kh = T2.get('khung') or []
        thieu_q = [str(k.get('u')) for k in kh if not isinstance(k.get('q_thoi_dai'), dict)]
        if not kh or thieu_q: M['b'].append(f"(b) {w}: tầng 2 thiếu q_thoi_dai ({'không có khung' if not kh else 'khung ' + ', '.join(thieu_q)})")
        if any(k in bb for k in ('cong_trinh_moc', 'chan_troi_city')):
            pv = {kk.get('prompt_ver') for k in kh for kk in ((k.get('q_thoi_dai') or {}).get('khung') or [])}
            if pv != {QT.PROMPT_VER_MOC}: M['d'].append(f'(d) {w}: có công trình mốc / chân trời City nhưng q_thoi_dai chưa chạy lớp công trình mốc (đề bài {sorted(str(x) for x in pv) or "—"}; cần {QT.PROMPT_VER_MOC!r}, `--moc`)')
    return K.r(sum(M.values(), []), val=f"{len(DS)} đoạn M-d · day_du {dem['day_du']} · nen {dem['nen']} · lỗi a {len(M['a'])} b {len(M['b'])} c {len(M['c'])} d {len(M['d'])} k {len(M['k'])}", muc=M, cong=cong)


ROWS = ('GOC-CAO', 'TU-LIEU-THAT', 'NHAN-VAT-TEN', 'KIEM-2-MUC')


def check(E, TL=None, ep_dir='.', LS=None, video=None):
    K = _K()
    if not ap_1177(E): return {k: K.na('tập trước T4 — 1.17.7 không hồi tố') for k in ROWS}
    cong = 'animatic' if E.get('animatic') else 'G2'; out = {}
    for k, fn in (('GOC-CAO', lambda: goc_cao(E, TL, LS, ep_dir, cong)), ('TU-LIEU-THAT', lambda: tu_lieu_that(E, LS, ep_dir, cong)),
                  ('NHAN-VAT-TEN', lambda: nhan_vat_ten(E, TL, LS, ep_dir, video, cong)), ('KIEM-2-MUC', lambda: kiem_2_muc(E, LS, ep_dir, cong))):
        try: out[k] = fn()
        except Exception as e: out[k] = K.r(thieu=[f'không chạy được: {type(e).__name__}: {e}'], val='—', cong=cong)   # noqa: BLE001
    return out
