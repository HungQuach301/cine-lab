#!/opt/cine/bin/python
"""Bộ luật kênh 2 — một lệnh (phiên K, bản 1.11.0, 15/10/2026; 1.12.0, 16/10/2026; 1.12.1, 17/10/2026; 1.13.0, 17/10/2026; 1.14.0, 17/10/2026; 1.15.0, 18/10/2026). Áp cho tập kênh 2 từ K2 tập 3 (T2 chạy checks 1.10.2 đã ghim).
Phiên xưởng chỉ CHẠY (không đọc mã). Định nghĩa: checks/ll/RULES-LL.md.

  k2check.py <episode.yaml> [--tl timeline.json] [--master master.mp4] [--mix mix.json] [--logs <thư mục *.log.json>]
             [--vo vo.flac --bed bed.flac] [--no-asr] [--json ra.json] [--md ra.md]
             1.12.0 (CHỈ BÁO): [--root <gốc repo có vo/*.align.json>] [--khai mach.yaml] [--ml2-api] [--mask mask.json --moc f0-f1,… --hero f0-f1,…]
             [--look <thư mục khung không chữ>] [--vang <thư mục khung vàng> --moi <thư mục khung mới>] [--bo-tl bo-tl.json]…
             1.12.1: --bo-tl lặp được (mọi bộ timelapse của TẬP → TL-Q9 đếm cú liên hoàn/vertigo cả tập); --cap áp cấp Chặn/Cảnh báo (cap112.py)
             1.15.0: [--o2 <video>|master] [--o2-api] [--o2-ket ra.json]
             1.16.0 (CHỈ tập từ T3: `khung_sach: true` | `kenh2_tu_t3: true`): [--tl16-video <video>] [--log-shot log-shot.json]

Gọi: Q26b bối cảnh · Q32 footage/ảnh nguồn ngoài · Q33 lặp cảnh · Q34 loại shot · Q35 nhãn loại số (D5) · Q36 chữ trên màn hình ·
Q37 nhịp thị giác · A1–A13 âm thanh · LOCK. Mã thoát 0 khi mọi mục ĐẠT (âm thanh của tập cũ: CHỈ BÁO, không tính).
1.12.0 (chủ dự án duyệt luật 16/10; cấp Chặn/Cảnh báo chờ duyệt → mọi mục dưới đây CHỈ BÁO, không tính vào mã thoát): ML1 mạch truyện ·
ML2 lời lặp ý (câu trả lời ngữ nghĩa đã lưu ở <out>/ml2-cache.json; --ml2-api chấm cặp mới qua Claude API, mô hình ghim) · ML3 lời mời đăng ký ·
FT1 chỉ báo footage · BC1 bố cục (khi có --mask) · MAU1 màu/chi tiết (--look) · KHOP1 đổi trình dựng (--vang/--moi) · TL-Q1…Q6 (--bo-tl).
1.12.1 (chủ dự án duyệt 16–17/10): Q35-TL "≈" bộ đếm (HH3) · TL-Q7 năm/s theo pha (MM2) · TL-Q8 nội dung bay thấp (MM1) · TL-Q9 tiết chế máy
(JJ1/KK1) — mỗi hàng ghi CẤP; mặc định vẫn CHỈ BÁO, `--cap` áp cấp vào mã thoát.
1.13.0 (17/10, CHỈ BÁO, chờ duyệt): NC-H1 thành phố có nhà · NC-H2 địa cầu · NC-H3 tầm mặc định · NC-H4 nơi có tên · NC-H5 đúng thời kỳ (tập; và
mỗi --bo-tl: hàng "NC-Hx [bộ]") · Q7/Q8-K2 nhận estimate · Q33 (1.13) pHash bỏ lớp chữ cố định · Q36 (1.13) câu miễn trừ theo chữ · Q37 (1.13)
khung tĩnh theo khung neo. Hàng Q33/Q36/Q37 cũ giữ nguyên mã thoát tới khi chủ dự án duyệt thay.
1.14.0 (17/10, CHỈ BÁO; chủ dự án duyệt B1–B8, YY5): BD-1…BD-8 bản đồ chiến lược `type: strategic` / inset / ranh lịch sử (khối `ban_do:` của
episode.yaml + --logs) · K-R1…K-R9 khi episode.yaml khai `rui_ro: do-k` (khối `do_k:`; [--hang-doi HANG-DOI.md]) · NC-H2/H3 loại strategic hợp lệ.
1.15.0 (18/10, CHỈ BÁO; chủ dự án duyệt P2-2, O2, I3, I8): K-LAI-1…6 + K-LAI-B khung neo LAI (khối `lai:`) · O2 máy soi lỗi thời đại
(khối `o2:` {nam | nam_theo [{t, nam}], neo?, buoc?, noi?}; [--o2 <video>] [--o2-api] gọi Claude API, bộ đệm <out>/o2-cache.json; hoặc --o2-ket ra.json)
· BC2–BC4 bố cục (mỗi --bo-tl) · Q37/Q37 (1.13)/NHIP-K2 nhận biến cố cảnh tl (pha + đồng hồ dừng) của --bo-tl · TL-Q1 nhận mốc dừng giờ.
1.16.0 (19/10, CHỈ BÁO; Kinh thánh §12.1 sửa, §13, D6; khiếu nại V6/G1b): tập từ T3 → SACH-1 khung sạch · CHUONG-1 thẻ chương · PP-1 thẻ
phương pháp · TL-1/TL-2/TL-3 ngữ pháp timelapse (log shot + video) · NHIP-NGHIA · XEM-CAM · PC-1 phục chế · K-LAI-3V; thay K-LAI-2, NC-H5, BD-3 theo
§12.1; Q26b theo vùng cho cảnh tl/*; Q37 miễn khung neo/tấm im lặng ≤ 10 s; A* theo lời/animatic; ML1 đọc lời khoá. Tập cũ: đúng hành vi 1.15.
Mặc định: timeline <out>/timeline.json, master <out>/<id>-v1-master.mp4 nếu có, mix <out>/mix.json, log <out>/ nếu có *.mkv.log.json.
"""
import glob, json, os, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base, q_setting, q_footage, q_scene, q_types, q_chu, q_nhip, q_amthanh, q_mach, q_ftg, q_hinh, q_tl, q_k2var, cap112, q_k116  # noqa: E402
from checks.cinecheck import VERSION  # noqa: E402


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    EP = a[0]; E = base.load(EP); E['_path'] = os.path.abspath(EP); ep_dir = os.path.dirname(os.path.abspath(EP)); O = E['out']
    TL = json.load(open(g('tl') or os.path.join(O, 'timeline.json')))
    m = g('master') or next(iter(sorted(glob.glob(os.path.join(O, f"{E['id']}-*-master.mp4")))), None)
    mp = g('mix') or os.path.join(O, 'mix.json'); MX = json.load(open(mp)) if os.path.exists(mp) else None
    logs = g('logs') or (O if glob.glob(os.path.join(O, '*.log.json')) else None)
    rows = []
    V16 = q_k116.ap_116(E)   # 1.16: chỉ tập từ T3
    MIEN = q_k116.q37_mien(E, TL) if V16 else None
    BT = [a[i + 1] for i, x in enumerate(a) if x == '--bo-tl']
    TLB = []   # 1.15 (I8): biến cố cảnh tl cho Q37 — bản đọc riêng (q_tl.check sửa bộ tại chỗ)
    for bp in BT:
        try: TLB.append((json.load(open(bp)), os.path.dirname(os.path.abspath(bp))))
        except (OSError, ValueError): pass

    def row(q, ten, r, nguong=''):
        kq = r.get('ket_qua') or ('ĐẠT' if r['ok'] else 'TRƯỢT')
        rows.append(dict(q=q, ten=ten, kq=kq, val=r.get('val', ''), nguong=nguong, sat='; '.join(r.get('sat_nguong') or []), loi=(r.get('loi') or []) + (r.get('thieu') or [])))
    row('Q26b', 'Đa dạng bối cảnh' + (' (1.16: cảnh tl/* theo vùng)' if V16 else ''), q_setting.q26b(TL, E, v116=V16), '≤ 25 % · ≤ 90 s · nửa sau ≥ 3')
    row('Q32', 'Footage/ảnh nguồn ngoài', q_footage.q32(E, TL, ep_dir), '≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5×')
    row('Q33', 'Lặp cảnh', q_scene.q33(E, TL, video=m if m and os.path.exists(m) else None), '≤ 2 lần')
    row('Q34', 'Loại shot', q_types.q34(E, TL, ep_dir), 'type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document ≤ 3 s · record ≤ 12 s + dòng tô + nguồn')
    row('Q35', 'Nhãn loại số (D5)', q_chu.q35(E, TL, logs), 'ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL')
    row('Q36', 'Chữ trên màn hình', q_chu.q36(E, TL, logs), 'nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực (+ 1 lần trong câu miễn trừ 0:00–0:15)')
    row('Q37', 'Nhịp thị giác' + (' (1.16: miễn khung neo/im lặng ≤ 10 s)' if V16 else ''), q_nhip.q37(E, TL, m if m and os.path.exists(m) else None, tl=TLB or None, mien=MIEN),
        'TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s')
    ra = q_amthanh.check(E, TL, master=m, MX=MX, vo=g('vo'), bed=g('bed'), asr='--no-asr' not in a, v116=V16)
    row('A1–A13', 'Âm thanh (' + ('MIX=audio' if ra['ap_dung'] else 'tập cũ — chỉ báo') + ')', ra, 'docs/AUDIO-THUOC-DO.md')
    # ---- 1.12.0: CHỈ BÁO (cấp đề xuất trong reports/K-1.12-BAO-CAO.md, chờ chủ dự án duyệt)
    CAPON = '--cap' in a

    def bao(q, ten, fn, nguong=''):
        try: r = fn()
        except Exception as e: r = dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—')
        sub = r.get('ket_qua') or ('ĐẠT' if r['ok'] else 'TRƯỢT'); mo, ch, cb = cap112.cap(q, r)
        if CAPON: kq = 'TRƯỢT' if ch else ('CẢNH BÁO' if cb else 'ĐẠT')
        else: kq = f'CHỈ BÁO ({sub})'
        r = dict(r, ket_qua=kq); row(q, ten, r, nguong); rows[-1]['cap'] = mo; rows[-1]['chan'] = len(ch); rows[-1]['canh_bao'] = len(cb)
    import yaml
    khai = yaml.safe_load(open(g('khai'))) if g('khai') else (E.get('mach') or {})
    C = []
    try: C = q_mach.cau_tu_loi(TL, g('root'))
    except Exception as e: C = e
    cp = os.path.join(O, 'ml2-cache.json'); cache = json.load(open(cp)) if os.path.exists(cp) else {}
    need = lambda: (_ for _ in ()).throw(C) if isinstance(C, Exception) else C
    def ml1():
        if V16 and (isinstance(C, Exception) or not C) and E.get('loi_khoa'):   # 1.16: chưa có căn chữ lời → câu của lời khoá (không có giờ)
            return q_mach.ml1(E, TL, q_k116.cau_tu_loi_khoa(q_k116._p(ep_dir, E['loi_khoa'])), ep_dir, claims=q_k116.claims_file(E, ep_dir))
        return q_mach.ml1(E, TL, need(), ep_dir, claims=q_k116.claims_file(E, ep_dir) if V16 else None)
    bao('ML1', 'Mạch truyện', ml1, 'mỗi shot gắn câu/claim · timelapse trôi ≤ 15 %')
    bao('ML2', 'Lời lặp ý', lambda: q_mach.ml2(need(), float(TL['tong_s']), khai, cache, api='--ml2-api' in a, out_dir=O), 'n-gram/IDF + chấm ngữ nghĩa ghim mô hình; ngoài tóm tắt cuối')
    if '--ml2-api' in a and os.path.isdir(O): json.dump(cache, open(cp, 'w'), ensure_ascii=False, indent=1)
    bao('ML3', 'Lời mời đăng ký', lambda: q_mach.ml3(need(), TL, khai), '60 s cuối hoặc ±5 s ranh chương · không trong 20 s trước luận điểm chính')
    bao('FT1', 'Chỉ báo footage/ảnh', lambda: q_ftg.ft1(E, TL), '≤ 20 % (trần) · mỗi shot có lý do · ảnh ≤ 1/3 khung ≤ 6 s không tính')
    if g('mask'): bao('BC1', 'Bố cục (EE1)', lambda: q_hinh.bc1(json.load(open(g('mask'))), 24, q_hinh._spans(g('moc')), q_hinh._spans(g('hero'))), 'nội dung < 30 % ≤ 2 s (trừ mốc đinh) · cận hero ≥ 25 %')
    if g('look'):
        fs = sorted(glob.glob(os.path.join(g('look'), '*.jpg')) + glob.glob(os.path.join(g('look'), '*.png')))
        bao('MAU1', 'Màu/chi tiết', lambda: q_hinh.mau1([(os.path.splitext(os.path.basename(p))[0], p) for p in fs]), 'bão hoà ≥ 0,35 · colorfulness ≥ 35 · chi tiết ≥ 16 · cháy ≤ 1 %')
    if g('vang') and g('moi'): bao('KHOP1', 'Khớp cấu trúc khi đổi trình dựng', lambda: q_hinh.khop1(g('vang'), g('moi')), 'tần thấp ≤ 3 % · dịch ≤ 1 · PSNR¼ ≥ 40 · SSIM ≥ 0,90 · renderer ghi rõ, không trộn')
    # ---- 1.12.2: biến thể kênh 2 (NN2, NN3, khiếu nại Q14/Q15/Q17) — CHỈ BÁO cạnh luật cũ tới khi chủ dự án duyệt thay
    mv = m if m and os.path.exists(m) else None
    bao('NHIP-K2', 'Nhịp kênh 2 (Q14–Q18 không áp → Q37)', lambda: q_k2var.nhip_k2(E, TL, mv, tl=TLB or None, mien=MIEN), 'TB ≤ 3,5 s · dài nhất ≤ 6 s')
    bao('Q26b-K2', 'Đa dạng loại cảnh + vùng', lambda: q_k2var.q26b_k2(E, TL), '≥ 3 loại/nửa · loại ≤ 70 % · vùng ≤ 25 %, ≤ 90 s, nửa sau ≥ 3')
    bao('Q33-K2', 'Lặp cảnh (vùng, góc) + pHash L/ΔE', lambda: {k: v for k, v in q_k2var.q33_k2(E, TL, mv).items() if k != 'aps'}, '≤ 2 lần (miễn: khác chương + khác năm/lớp)')
    bao('Q32b-K2', 'Trần clip/ảnh', lambda: q_k2var.q32b_k2(E, TL), 'footage ≤ 8 s · ảnh có máy/chú thích đổi ≤ 12 s · ảnh tĩnh ≤ 8 s')
    NG = {'Q35-TL': '"≈" bộ đếm chỉ khi dòng phương pháp "≈ = interpolated between counts" trong 6 s đầu', 'TL-Q7': 'bay thấp (AGL ≤ 150 m) ≤ 10 năm/s · crane/reveal ≤ 20 năm/s',
          'TL-Q8': 'bay thấp của cú liên hoàn: content_pct trung vị ≥ 30 %', 'TL-Q2': '≥ 3 s ≤ 15 m · AGL ≤ 120 m phố / ≤ 300 m eo đất, sông, đại lộ',
          'TL-Q9': '≤ 2 liên hoàn, ≤ 1 vertigo/tập · vai mọi pha · orbit 4–6 s · ≤ 90 °/s'}
    tap = []
    for k_, bp in enumerate(BT):
        nm = os.path.basename(os.path.dirname(os.path.abspath(bp))) or f'bo{k_}'
        try:
            BB = json.load(open(bp)); RT = q_tl.check(BB, os.path.dirname(os.path.abspath(bp))); F_ = q_tl._frames(q_tl._ld(BB['_base'], BB['campath']))
            tap.append((nm, BB, F_, BB.get('fps', q_tl.FPS)))
        except Exception as e: RT = {'TL-Q1…Q8': dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[str(e)], val='—')}
        for k, v in RT.items():
            if k != 'TL-Q9': bao(k + (f' [{nm}]' if len(BT) > 1 else ''), 'Timelapse', lambda v=v: v, NG.get(k, 'research/timelapse/BAO-CAO.md §6.8'))
    if tap: bao('TL-Q9', 'Tiết chế máy (cả tập)', lambda: q_tl.tlq9(tap), NG['TL-Q9'])
    # ---- 1.13: NC-H1…H5 (NC-LS §6, đánh giá T2 của chủ dự án) + hàng đợi khiếu nại T2 G2 §13–§14 — CHỈ BÁO tới khi chủ dự án duyệt
    from checks.ll import q_noi, llcheck
    NCT = {'NC-H1': 'Thành phố có nhà', 'NC-H2': 'Địa cầu', 'NC-H3': 'Tầm mặc định', 'NC-H4': 'Nơi có tên', 'NC-H5': 'Đúng thời kỳ'}
    NCN = {'NC-H1': 'fabric trung vị ≥ 25 % · không khung < 15 % (trừ ≤ 3 s cuối reveal)', 'NC-H2': 'AGL > 50 km: ≤ 1 lần/tập · ≤ 3 s/lần',
           'NC-H3': 'AGL ≤ 60 km ≥ 70 % 3D · có thành phố: AGL ≤ 3 km ≥ 40 %', 'NC-H4': 'mọi shot bản đồ: chip nơi hoặc nhãn địa danh',
           'NC-H5': 'năm xây ≤ bộ đếm · ghost: nhãn nguồn ≥ 38 px, ≥ 3 s lần đầu'}
    try: NC = q_noi.nc_tap(E, TL)
    except Exception as e: NC = {k: dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—') for k in NCT}
    if V16:   # 1.16 (khiếu nại A-G1B-2): nhận bộ đếm cảnh tl/*; (b) nguồn ghost trong dữ liệu + mô tả, không đòi nhãn trên hình (§12.1)
        NCN = dict(NCN, **{'NC-H5': 'năm xây ≤ bộ đếm (nam_khung) · ghost có nguồn + nguồn trong mô tả (§12.1: không nhãn trên hình)'})
        try: NC['NC-H5'] = q_k116.nch5(E, TL, ep_dir)
        except Exception as e: NC['NC-H5'] = dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—')
    for k in NCT: bao(k, NCT[k], lambda k=k: NC[k], NCN[k])
    for k_, bp in enumerate(BT):
        nm = os.path.basename(os.path.dirname(os.path.abspath(bp))) or f'bo{k_}'
        try: NB = q_noi.nc_bo(json.load(open(bp)), os.path.dirname(os.path.abspath(bp)))
        except Exception as e: NB = {k: dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—') for k in NCT}
        for k in NCT: bao(f'{k} [{nm}]', NCT[k] + ' (bộ timelapse)', lambda k=k, NB=NB: NB[k], NCN[k])
    LG = {}
    for f in (glob.glob(os.path.join(logs, '*.log.json')) if logs else []):
        try: J = json.load(open(f))
        except (OSError, ValueError): continue
        if J.get('fmt', '16x9') == '16x9' and J.get('id'): LG[str(J['id'])] = J

    def q78k():
        a7, a8 = llcheck.q7(E, TL, LG, est=True), llcheck.q8k(E)
        return dict(ok=not a7 and not a8, loi=[f'(Q7) {x}' for x in a7] + [f'(Q8) {x}' for x in a8],
                    val=f"Q7 nhận ESTIMATE: {len(a7)} lỗi ({'log ' + str(len(LG)) + ' đoạn' if LG else 'không log: chỉ kiểm kind khai'}) · Q8 loại số: {len(a8)} lỗi")
    bao('Q7/Q8-K2', 'Nhãn/loại số nhận estimate (khiếu nại TT5 i)', q78k, 'kind ∈ actual/projection/estimate (kênh 2) · đủ nhãn, không thừa nhãn')
    bao('Q33 (1.13)', 'Lặp cảnh — pHash bỏ lớp chữ cố định', lambda: q_scene.q33(E, TL, video=mv, k2=True), '≤ 2 lần · pHash L vùng nội dung y 18–72 %, θ 16')
    bao('Q36 (1.13)', 'Chữ — câu miễn trừ nhận theo chữ', lambda: q_chu.q36(E, TL, logs, v113=True), '"This video explains… Facts as of" 1 lần trong 0:00–0:15 không đòi nguồn luật')
    bao('Q37 (1.13)', 'Nhịp — khung tĩnh theo khung neo', lambda: q_nhip.q37(E, TL, mv, v113=True, tl=TLB or None, mien=MIEN), 'khung tĩnh (mọi khung khác khung đầu quãng < 2,0/255) ≤ 6 s')
    # ---- 1.14: BD-1…BD-8 bản đồ chiến lược/inset/ranh (NC-BD §3.4; chủ dự án duyệt B1–B8 17/10) + K-R1…K-R9 ĐỎ-K (NC-LS2 §5.3; YY5) — CHỈ BÁO
    from checks.ll import q_bando, q_dok
    BDT = {'BD-1': 'Bản đồ chiến lược: tỷ trọng + định nghĩa', 'BD-2': 'Bản đồ chiến lược: chuyển động', 'BD-3': 'Nhãn ranh "approx. borders c. YYYY — nguồn"',
           'BD-4': 'Manifest lớp ranh', 'BD-5': 'Biên hiện đại tranh chấp + lãnh thổ nhỏ', 'BD-6': 'Tuyến biển không cắt đất', 'BD-7': 'Màu phe cố định (+ B8 bản địa)',
           'BD-8': 'Inset định vị'}
    BDN = {'BD-1': '≤ 15 % · ≤ 8 s · ≤ 2/chương · không liền nhau · nghiêng ≤ 30°, 300–5 000 km · mốc thời gian, chú giải ≤ 3 phe, kề 3D nơi chỉ tới',
           'BD-2': 'phần tử chuyển động bắt đầu ≤ 1,5 s, phủ ≥ 60 %', 'BD-3': 'nhãn regex ≥ 38 px ở ≥ 95 % khung có ranh',
           'BD-4': 'nam/nguon/nguon_doi_chieu/lech_tb_px/giay_phep ∈ CC0·PD·CC-BY-4.0; lệch > 4 px → mép mềm/gạch', 'BD-5': '∩ (NE disputed ⊕ 10 km) = ∅ · lãnh thổ < 8 px là điểm',
           'BD-6': 'tuyến biển ∩ đất NE 1:10m (trừ 5 km quanh cảng) = ∅ · ≥ 1 claim', 'BD-7': 'một faction_id một màu · không cờ/biểu tượng làm fill · bản địa không tô như đất trống',
           'BD-8': '≤ 12 % khung · góc trên trái, an toàn 5 % · 2,5–4 s · không giao chữ/LL.occ · không trong liên hoàn/thẻ số/ảnh lưu trữ/2 s sau cắt cứng'}
    try: BD = q_bando.check(E, TL, ep_dir, logs)
    except Exception as e: BD = {k: dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—') for k in BDT}
    if V16:   # 1.16 (khiếu nại A-G1B-3): nhãn ranh trong dữ liệu + nguồn trong mô tả; nhãn hiện trên hình là lỗi (§12.1)
        BDT = dict(BDT, **{'BD-3': 'Ranh lịch sử: nhãn trong dữ liệu, nguồn trong mô tả (§12.1)'})
        BDN = dict(BDN, **{'BD-3': 'manifest nam + nguon · nguồn ranh trong mô tả · KHÔNG hiện "approx. borders" trên hình'})
        try: BD['BD-3'] = q_k116.bd3(E, TL, ep_dir, logs)
        except Exception as e: BD['BD-3'] = dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—')
    if all(v.get('ket_qua') == 'KHÔNG ÁP' for v in BD.values()): bao('BD-1…BD-8', 'Bản đồ chiến lược / inset / ranh', lambda: dict(ok=True, loi=[], val='không có shot strategic, lớp ranh, tuyến hay inset', ket_qua='KHÔNG ÁP'))
    else:
        for k in BDT: bao(k, BDT[k], lambda k=k: BD[k], BDN[k])
    KRT = {'K-R1': 'Từ cấm', 'K-R2': 'Biểu tượng trong khung', 'K-R3': 'Biên giới hiện đại', 'K-R4': 'Thương vong có claim', 'K-R5': 'Hình bạo lực',
           'K-R6': 'Thumbnail', 'K-R7': 'Nhịp ĐỎ-K (HANG-DOI)', 'K-R8': 'Chấm mù 3 góc', 'K-R9': 'Mô tả + bình luận ghim'}
    KRN = {'K-R1': '0 lần', 'K-R2': 'cuc_doan/ton_giao 0 khung · co_lich_su ≤ 2 %, ≤ 3 s, ≤ 3 lần', 'K-R3': '0 giao (NE disputed ⊕ 10 km)', 'K-R4': '100 % số có claim khoảng / ≥ 2 truyền thống',
           'K-R5': '0', 'K-R6': '0 vi phạm', 'K-R7': '≤ 1 ĐỎ-K/4 tập · kề ≠ VÀNG · không T3–T5', 'K-R8': '3 vai · 0 cờ · ≥ 4/5', 'K-R9': 'as of · ≥ 2 truyền thống · ghim · từ chặn (khai)'}
    if not q_dok.la_do_k(E): bao('K-R1…K-R9', 'ĐỎ-K', lambda: dict(ok=True, loi=[], val='tập không khai rui_ro: do-k', ket_qua='KHÔNG ÁP'))
    else:
        try: DK = q_dok.check(E, TL, ep_dir, logs, g('hang-doi'))
        except Exception as e: DK = {k: dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—') for k in KRT}
        for k in KRT: bao(k, KRT[k], lambda k=k: DK[k], KRN[k])
    # ---- 1.15: K-LAI-1…6 + K-LAI-B (PT2 Q-PT2-2, chủ dự án duyệt P2-2/P2-3 18/10) · O2 máy soi lỗi thời đại (O2) · BC2–BC4 bố cục (I3) — CHỈ BÁO
    from checks.ll import q_lai, q_thoi_dai, q_bocuc
    LAT = {'K-LAI-1': 'LAI: thời lượng khung AI', 'K-LAI-2': 'LAI: nhãn phương pháp', 'K-LAI-3': 'LAI: kiểm dữ kiện từng tấm C', 'K-LAI-4': 'LAI: vùng bảo vệ = A',
           'K-LAI-5': 'LAI: một tấm, ban ngày, đêm ≤ 1,5× A', 'K-LAI-6': 'LAI: sổ gọi API', 'K-LAI-B': 'LAI: bão hoà khung (P2-3)'}
    LAN = {'K-LAI-1': 'ai_image/ai_texture ≤ 20 % thời lượng', 'K-LAI-2': '"Surface detail AI-assisted · layout, landmarks & flags from sources" ≥ 38 px góc dưới trái suốt shot',
           'K-LAI-3': 'mỗi tấm C: loi_chac_cuoi 0 · nghi vấn đã xử lý · ngoại lệ có duyệt · không chấm mù', 'K-LAI-4': 'sai khác TB < 1/255 trên mặt nạ bao_ve (PNG)',
           'K-LAI-5': '≤ 1 tấm/khung neo × mốc · ≤ 2 lần sinh lại · chỉ lượt ngày · đêm ≤ 1,5× A', 'K-LAI-6': 'model, prompt, % mặt nạ, usage, $, C2PA, giờ',
           'K-LAI-B': 'bão hoà trung vị ≤ 0,40 mỗi khung LAI'}
    if V16:
        LAT = dict(LAT, **{'K-LAI-2': 'LAI: công bố AI (§12.1)', 'K-LAI-3V': 'LAI: nghi vấn còn ghi của vân (1.16)'})
        LAN = dict(LAN, **{'K-LAI-2': 'cờ ai_* mọi khung · shot khai khớp log · thẻ phương pháp nói AI · mô tả "AI use = Yes" · KHÔNG nhãn trên hình',
                           'K-LAI-3V': 'tệp vân dùng không còn nghi vấn chưa xử lý (Cảnh báo)'})
    if not q_lai.ap_dung(E): bao('K-LAI-1…6', 'Khung neo LAI', lambda: dict(ok=True, loi=[], val='tập không có khối lai: / shot AI', ket_qua='KHÔNG ÁP'))
    else:
        try: LA = (q_lai.check116 if V16 else q_lai.check)(E, TL, ep_dir, logs)
        except Exception as e: LA = {k: dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—') for k in LAT}
        for k in LAT: bao(k, LAT[k], lambda k=k: LA[k], LAN[k])

    def o2():
        if g('o2-ket'): return json.load(open(g('o2-ket')))
        C2 = E.get('o2') or {}
        if not C2: return dict(ok=False, ket_qua='THIẾU', loi=[], thieu=['chưa soi: khai khối o2: {nam | nam_theo} và chạy --o2 <master> --o2-api (Claude API, có chi phí)'], val='—')
        vid = g('o2') if g('o2') and g('o2') != 'master' else mv
        if not vid: return dict(ok=False, ket_qua='THIẾU', loi=[], thieu=['chưa soi: không có video (--o2 <master>)'], val='—')
        nt = [(float(x['t'][0]), float(x['t'][1]), int(x['nam'])) for x in C2.get('nam_theo') or []]
        neo = [float(t) for t in C2.get('neo') or []] + [round(sg['t0'] + (sh['t0'] + sh['t1']) / 2, 3) for sg in TL.get('segments') or [] for sh in sg.get('shots') or []
                                                       if sh.get('khung_neo') or (sh.get('p') or {}).get('khung_neo') or (sh.get('p') or {}).get('ai_image')]
        cp = os.path.join(O, 'o2-cache.json'); cache = json.load(open(cp)) if os.path.exists(cp) else {}
        R = q_thoi_dai.check_video(vid, float(TL['tong_s']), os.path.join(O, 'o2'), C2.get('nam'), nt, neo, float(C2.get('buoc', q_thoi_dai.BUOC)), C2.get('noi', ''),
                                   api='--o2-api' in a, cache=cache)
        if os.path.isdir(O): json.dump(cache, open(cp, 'w'), ensure_ascii=False, indent=1)
        return R
    bao('O2', 'Máy soi lỗi thời đại (lưới lọc thứ hai)', o2, '1 khung/5 s + khung neo · cờ/quân phục/tàu/đèn/xe/vật hiện đại/chữ/kiến trúc theo năm · không thay kiểm nguồn')
    BCT = {'BC2': 'Bố cục thành phố (I3)', 'BC3': 'Khối quân/tàu ≥ 6 px (I3)', 'BC4': 'Hero không "tấm phẳng" (I3)'}
    BCN = {'BC2': 'thanh_pho: nội dung ≥ 50 % · nước + cỏ trống ≤ 1/3', 'BC3': 'cao ≥ 6 px @1080p (log vật)', 'BC4': 'chi tiết hero ≥ 16 · lệch pháp tuyến ≥ 10°'}
    for k_, bp in enumerate(BT):
        nm = os.path.basename(os.path.dirname(os.path.abspath(bp))) or f'bo{k_}'
        try: BCR = q_bocuc.check(json.load(open(bp)), os.path.dirname(os.path.abspath(bp)))
        except Exception as e: BCR = {k: dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—') for k in BCT}
        for k in BCT: bao(k + (f' [{nm}]' if len(BT) > 1 else ''), BCT[k], lambda k=k, BCR=BCR: {kk: vv for kk, vv in BCR[k].items() if kk != 'khung'}, BCN[k])
    # ---- 1.16: luật mới cho tập từ T3 (Kinh thánh §12.1 sửa, §13.2–§13.4, §13.6, D6; §12.3 PC-1) — CHỈ BÁO
    K6T = {'SACH-1': 'Khung sạch §12.1 + TL-4', 'CHUONG-1': 'Thẻ chương §13.3', 'PP-1': 'Thẻ phương pháp (D6)', 'TL-1': 'Xương sống timelapse §13.6',
           'TL-2': 'Lướt thấp §13.6', 'TL-3': 'Không shot trống §13.6', 'NHIP-NGHIA': 'Nhịp → vật mang nghĩa §13.2', 'XEM-CAM': 'Cổng XEM CÂM §13.4',
           'PC-1': 'Thước phục chế §12.3'}
    K6N = {'SACH-1': 'chỉ bộ đếm · chip nơi ≤ 3 s · thẻ chương · thẻ phương pháp; không tấm số/trích, không tư liệu đứng riêng (phủ ≤ 3 s)',
           'CHUONG-1': '≤ 8/tập · "năm — ≤ 6 từ" · ≤ 3 s · không trong móc · trung tính', 'PP-1': '2 thẻ × 7–9 s, cuối phim · nguồn/ước tính/AI · ≤ 3 từ/s',
           'TL-1': 'góc cao + thời gian chạy ≥ 75 % · ≤ 5 cắt/phút (đặc tả + video) · trôi ≤ 2 %/s · 6–8 điểm máy (hiệu chỉnh sau V7-PILOT)',
           'TL-2': 'lướt thấp ≤ 10 % · có vai, phố/người (hiệu chỉnh sau V7-PILOT)', 'TL-3': 'mỗi shot 3D: thời gian chạy hoặc biến cố · trống ≤ 60 % (hiệu chỉnh sau V7-PILOT)',
           'NHIP-NGHIA': '≥ 90 % nhịp chính', 'XEM-CAM': '8 câu · 3 AI + chủ dự án · tắt tiếng · ≥ 6/8 mỗi người', 'PC-1': 'Δ cạnh mới so bicubic ≤ 1,0 điểm % · PSNR ≥ bicubic'}
    if not V16: bao('1.16', 'Luật T3 (SACH-1…PC-1)', lambda: dict(ok=True, loi=[], val='tập trước T3: giữ hành vi 1.15', ket_qua='KHÔNG ÁP'))
    else:
        vid = g('tl16-video') or mv
        try: K6 = q_k116.check(E, TL, ep_dir, logs, vid, g('log-shot'))
        except Exception as e: K6 = {k: dict(ok=False, ket_qua='THIẾU', loi=[], thieu=[f'không chạy được: {e}'], val='—') for k in K6T}
        for k in K6T: bao(k, K6T[k], lambda k=k: K6[k], K6N[k])
    lk = subprocess.run([sys.executable, os.path.join(base.REPO, 'checks', 'lock.py'), '--verify'], capture_output=True, text=True)
    rows.append(dict(q='LOCK', ten=f'checks/ khớp LOCK ({VERSION})', kq='ĐẠT' if lk.returncode == 0 else 'TRƯỢT', val='KHỚP' if lk.returncode == 0 else 'KHÔNG KHỚP', nguong='', sat='', loi=[]))
    ok = all(r['kq'] in ('ĐẠT', 'CẢNH BÁO') or r['kq'].startswith('CHỈ BÁO') for r in rows)
    md = [f"# Luật kênh 2 (checks {VERSION}) — {E['id']} — {'ĐẠT' if ok else 'TRƯỢT'}", '',
          '| Mục | Kiểm | Kết quả | Cấp (1.12.1) | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) |', '|---|---|---|---|---|---|---|']
    capv = lambda r: f"{r['cap']} — lỗi Chặn {r['chan']}, Cảnh báo {r['canh_bao']}" if r.get('cap') else ''
    md += [f"| {r['q']} | {r['ten']} | **{r['kq']}** | {capv(r)} | {str(r['val']).replace('|', '/')} | {r['nguong']} | {r['sat'].replace('|', '/')} |" for r in rows]
    md += ['', '## Âm thanh A1–A13', q_amthanh.table(ra), '', '## Chi tiết lỗi']
    for r in rows:
        if r['loi']: md += [f"### {r['q']}"] + [f'- {x}' for x in r['loi'][:60]] + ([f"- … {len(r['loi']) - 60} mục nữa"] if len(r['loi']) > 60 else [])
    txt = '\n'.join(md) + '\n'; print(txt)
    if g('md'): open(g('md'), 'w').write(txt)
    if g('json'): json.dump(dict(rows=rows, am_thanh=ra, version=VERSION), open(g('json'), 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
