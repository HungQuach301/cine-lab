#!/opt/cine/bin/python
"""K-1.17.8 · K1174-D2 — HIỆU CHUẨN LẠI thước biến cố video (checks/ll/q_bcv.py) trên ANIMATIC T4 v2 (bản xem 4 phần nối, SHA ghi ở ra.json)
+ LOG MÁY THẬT trong git (channel-k2/k2c-t4-02/animatic2/log-may/*.json: mỗi khung năm thế giới, lửa, mặt trời, máy).
Tham chiếu (không tự khai):
  CẮT  = ranh shot timeline (q_bcv.ranh_shot) — đúng phép (h) của hàng BIEN-CO-V
  BEAT = beat khai (không `cut`) KHỚP mốc đặc tả ±0,3 s (phần Q37 (a) nhận) — như K-1.17.4
  TĨNH THẬT     = shot 3D (không M-d) mà log máy cho máy đứng yên (< 3 m) và năm, lửa, mặt trời KHÔNG đổi (Δnăm ≤ 0,01; Δlửa ≤ 0,1; Δmặt trời ≤ 2,0°);
                  lớp ngoài A/N2P chỉ được có khi nằm trong cửa sổ đã biết giờ (tu_lieu_lan, ghep-log thẻ/bộ đếm, thẻ chương) — các cửa sổ đó ±0,5 s
                  và 0,5 s hai đầu shot bị cắt bỏ → mọi biến cố còn lại = báo NHẦM
  CHỈ MÁY THẬT  = như trên nhưng máy DI CHUYỂN (log máy ≥ 3 m), cú máy không phải KHOP (then–now = biến cố thật) và không lớp MAP/MAP3D
                  (chuyển bản đồ) → mọi biến cố = báo NHẦM
  (Định nghĩa hai tập thật sửa MỘT lần trước lượt đo biến cố: bản đầu — CODINH + Δmặt trời ≤ 1° + chỉ lớp A — cho 0 s tĩnh và 10 s chỉ máy,
   không đủ để đo báo nhầm/phút; chưa xem số biến cố nào khi sửa.)
  TỔNG HỢP      = 6 khung T4 v2 (bản xem) làm clip 10 s chỉ máy đi (trượt 2 %/s + phóng 1,5 %/s + quay 0,5°/s) và cùng clip + một ô 96 px đổi ở 5,0 s
                  (như K-1.17.4; khung T4 thay khung T3)
Tiêu chí ĐẠT (đặt TRƯỚC khi đo, = K-1.17.4 §2 cộng hai tập thật): R cắt ≥ 95 % · R beat ≥ 70 % · Δt trung vị ≤ 0,25 s · báo nhầm ≤ 1/phút trong
TĨNH THẬT và trong CHỈ MÁY THẬT · 0 trên clip tổng hợp chỉ máy đi · bắt 6/6 vật đổi tổng hợp ±0,25 s. Chọn (θ, k) trên NỬA ĐẦU, kiểm NỬA SAU;
θ 8, k 2 (T3) được giữ nếu đạt cả hai nửa.
  hieu_chuan_bcv_t4.py <video> <episode.yaml> <timeline.json> <log-shot.json> <ghep-log.json> <thư mục log-may> <thư mục ra> [--song-song 2]"""
import gzip, json, math, os, statistics, sys, multiprocessing as mp
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')); sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, 'reports', 'k1174', 'do'))
from checks.ll import q_bcv as B, base  # noqa: E402
import hieu_chuan_bcv as H  # noqa: E402  (tham_chieu, _clip, _chay, LUOI — K-1.17.4)

DY, DF, DS, MOVE_M, LE = 0.01, 0.1, 2.0, 3.0, 0.5
FR_T = (20.0, 150.0, 260.0, 400.0, 560.0, 690.0)


def _log(p):
    raw = open(p, 'rb').read()
    return json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)


def quang_that(LS, GL, ld, chuong=()):
    """→ (tĩnh [(a, b, shot)], chỉ máy [(a, b, shot)], bảng lý do). chuong = [(t0, t1)] thẻ chương."""
    phu = [(float(t) - LE, float(t) + float(d) + LE) for t, d, *_ in (GL.get('the') or []) + (GL.get('dem') or [])] + [(a - LE, b + LE) for a, b in chuong]
    tinh, may, bang = [], [], []
    for s in LS:
        if not s.get('log_may') or s.get('minh_hoa'): continue
        lop = {k: v for k, v in (s.get('lop') or {}).items() if v}
        J = _log(os.path.join(ld, os.path.basename(s['log_may']))); F = J['frames']
        y = [x.get('year') or 0 for x in F]; fi = [x.get('fire') or 0 for x in F]; se = [x.get('sun_el') or 0 for x in F]
        mv = sum(math.dist(a['cam']['p'], b['cam']['p']) for a, b in zip(F, F[1:]))
        a0, b0 = float(s['t0']) + LE, float(s['t1']) - LE
        cua = [(float(x['t0']) - LE, float(x['t1']) + LE) for x in s.get('tu_lieu_lan') or []]
        gl_the = [z for z in phu if z[0] < b0 and z[1] > a0]
        khac = set(lop) - {'A', 'N2P'}
        biet_gio = (not khac) or (khac <= {'KHAC', 'TL', 'THE'} and (('THE' not in khac) or gl_the) and (not (khac & {'KHAC', 'TL'}) or cua))
        ok_hang = max(y) - min(y) <= DY and max(fi) - min(fi) <= DF and max(se) - min(se) <= DS and biet_gio and not (khac & {'MAP', 'MAP3D', 'THAT'})
        cu = s.get('cu_may'); loai = None
        if ok_hang and mv < MOVE_M and cu != 'KHOP': loai = 'tinh'
        elif ok_hang and mv >= MOVE_M and cu != 'KHOP': loai = 'may'
        bang.append(dict(shot=s['shot'], cu=cu, lop=lop, dy=round(max(y) - min(y), 4), dfire=round(max(fi) - min(fi), 2), dsun=round(max(se) - min(se), 2), move_m=round(mv, 1), loai=loai))
        if not loai: continue
        iv = [(a0, b0)]
        for c, d in phu + cua:   # bỏ quãng có lớp chồng / tư liệu
            iv = [z for a, b in iv for z in ((a, min(b, c)), (max(a, d), b)) if z[1] - z[0] > 0.5]
        for a, b in iv: (tinh if loai == 'tinh' else may).append((round(a, 3), round(b, 3), s['shot']))
    return tinh, may, bang


def nham(U, Q):
    n, s = 0, 0.0
    for a, b, _ in Q: s += b - a; n += sum(1 for u in U if a < u < b)
    return n, round(s, 2), round(n / (s / 60), 2) if s else 0.0


def main():
    a = sys.argv[1:]; vid, ep, tlp, lsp, glp, ld, out = a[:7]; os.makedirs(out, exist_ok=True)
    nj = int(a[a.index('--song-song') + 1]) if '--song-song' in a else 2
    E = base.load(ep); TL = json.load(open(tlp)); LS = json.load(open(lsp)); LS = LS.get('shots', LS) if isinstance(LS, dict) else LS; GL = json.load(open(glp))
    moc, beat, cat, T = H.tham_chieu(E, TL, LS)
    cat = sorted(set(round(x, 3) for x in B.ranh_shot(TL)))   # CẮT = ranh shot timeline (phép (h))
    from checks.ll import q_k116
    CH = [(c['t0'], c['t0'] + c['d']) for c in q_k116.the_chuong(E, TL)]
    tinh, may, bang = quang_that(LS, GL, ld, CH)
    json.dump(dict(tinh=tinh, chi_may=may, bang=bang), open(os.path.join(out, 'quang-that.json'), 'w'), ensure_ascii=False, indent=1)
    H.FR_T = FR_T
    syn = [(H._clip(vid, t, os.path.join(out, f'syn-{int(t)}.mp4')), H._clip(vid, t, os.path.join(out, f'syn-{int(t)}-doi.mp4'), True)) for t in FR_T]
    jobs = [(vid, th, k, out) for th, k in H.LUOI] + [(c, th, k, out) for th, k in H.LUOI for pair in syn for c in pair]
    with mp.Pool(nj) as P: P.map(H._chay, jobs, chunksize=1)
    KQ = []
    for th, k in H.LUOI:
        R = json.load(open(os.path.join(out, f'ev-{th:g}-{k:g}-{os.path.basename(vid)}.json')))
        U = B.gop([e[0] for e in R['su_kien']])
        def nua(lo, hi):
            h = H.danh_gia(R['su_kien'], cat, moc, beat, [], lo, hi)
            Uh = [u for u in U if lo <= u < hi]
            n1, s1, p1 = nham(Uh, [q for q in tinh if lo <= q[0] < hi]); n2, s2, p2 = nham(Uh, [q for q in may if lo <= q[0] < hi])
            return dict(h, tinh_that=dict(giay=s1, bao_nham=n1, phut=p1), chi_may_that=dict(giay=s2, bao_nham=n2, phut=p2))
        h1, h2 = nua(0.0, T / 2), nua(T / 2, T + 1)
        sn, sb = 0, 0
        for c0, c1 in syn:
            e0 = json.load(open(os.path.join(out, f'ev-{th:g}-{k:g}-{os.path.basename(c0)}.json')))['su_kien']
            e1 = json.load(open(os.path.join(out, f'ev-{th:g}-{k:g}-{os.path.basename(c1)}.json')))['su_kien']
            sn += len(B.gop([e[0] for e in e0])); sb += int(any(abs(e[0] - 5.0) <= 0.25 for e in e1))
        dat = lambda h: (h['R_cat'] >= B.HC_R_CAT and h['R_beat'] >= B.HC_R_BEAT and (h['dt_tv'] if h['dt_tv'] is not None else 9) <= B.HC_DT
                         and h['tinh_that']['phut'] <= B.HC_FP_PHUT and h['chi_may_that']['phut'] <= B.HC_FP_PHUT)
        KQ.append(dict(theta=th, k=k, nua_dau=h1, nua_sau=h2, tong_hop=dict(bao_nham_chi_may=sn, bat_vat_doi=f'{sb}/{len(syn)}'),
                       dat_nua_dau=dat(h1) and sn == 0 and sb == len(syn), dat_nua_sau=dat(h2) and sn == 0 and sb == len(syn)))
    ung = [x for x in KQ if x['dat_nua_dau']]
    g82 = next(x for x in KQ if x['theta'] == 8.0 and x['k'] == 2.0)
    chon = g82 if g82['dat_nua_dau'] and g82['dat_nua_sau'] else (min(ung, key=lambda x: (x['nua_dau']['tinh_that']['bao_nham'] + x['nua_dau']['chi_may_that']['bao_nham'], -x['nua_dau']['R_beat'], -x['theta'])) if ung else None)
    import hashlib
    ra = dict(video=os.path.basename(vid), video_sha=hashlib.sha256(open(vid, 'rb').read()).hexdigest(), tong_s=T,
              so_tham_chieu=dict(cat=len(cat), beat=len(beat), moc=len(moc), tinh_that=len(tinh), tinh_that_s=round(sum(b - a for a, b, _ in tinh), 1),
                                 chi_may_that=len(may), chi_may_that_s=round(sum(b - a for a, b, _ in may), 1)),
              tieu_chi=dict(R_cat=B.HC_R_CAT, R_beat=B.HC_R_BEAT, dt_tv=B.HC_DT, bao_nham_tinh_phut=B.HC_FP_PHUT, bao_nham_chi_may_that_phut=B.HC_FP_PHUT, bao_nham_chi_may_tong_hop=0, bat_vat_doi='6/6'),
              luoi=KQ, chon=dict(theta=chon['theta'], k=chon['k'], dat_nua_dau=chon['dat_nua_dau'], dat_nua_sau=chon['dat_nua_sau']) if chon else None)
    json.dump(ra, open(os.path.join(out, 'hieu-chuan-bcv-t4.json'), 'w'), ensure_ascii=False, indent=1)
    for x in KQ: print(x['theta'], x['k'], 'đầu', x['nua_dau'], '\n   sau', x['nua_sau'], x['tong_hop'], x['dat_nua_dau'], x['dat_nua_sau'])
    print('CHỌN', ra['chon'])


if __name__ == '__main__':
    main()
