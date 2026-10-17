#!/opt/cine/bin/python
"""Bộ luật kênh 2 — một lệnh (phiên K, bản 1.11.0, 15/10/2026; 1.12.0, 16/10/2026; 1.12.1, 17/10/2026; 1.13.0, 17/10/2026). Áp cho tập kênh 2 từ K2 tập 3 (T2 chạy checks 1.10.2 đã ghim).
Phiên xưởng chỉ CHẠY (không đọc mã). Định nghĩa: checks/ll/RULES-LL.md.

  k2check.py <episode.yaml> [--tl timeline.json] [--master master.mp4] [--mix mix.json] [--logs <thư mục *.log.json>]
             [--vo vo.flac --bed bed.flac] [--no-asr] [--json ra.json] [--md ra.md]
             1.12.0 (CHỈ BÁO): [--root <gốc repo có vo/*.align.json>] [--khai mach.yaml] [--ml2-api] [--mask mask.json --moc f0-f1,… --hero f0-f1,…]
             [--look <thư mục khung không chữ>] [--vang <thư mục khung vàng> --moi <thư mục khung mới>] [--bo-tl bo-tl.json]…
             1.12.1: --bo-tl lặp được (mọi bộ timelapse của TẬP → TL-Q9 đếm cú liên hoàn/vertigo cả tập); --cap áp cấp Chặn/Cảnh báo (cap112.py)

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
Mặc định: timeline <out>/timeline.json, master <out>/<id>-v1-master.mp4 nếu có, mix <out>/mix.json, log <out>/ nếu có *.mkv.log.json.
"""
import glob, json, os, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base, q_setting, q_footage, q_scene, q_types, q_chu, q_nhip, q_amthanh, q_mach, q_ftg, q_hinh, q_tl, q_k2var, cap112  # noqa: E402
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

    def row(q, ten, r, nguong=''):
        kq = r.get('ket_qua') or ('ĐẠT' if r['ok'] else 'TRƯỢT')
        rows.append(dict(q=q, ten=ten, kq=kq, val=r.get('val', ''), nguong=nguong, sat='; '.join(r.get('sat_nguong') or []), loi=(r.get('loi') or []) + (r.get('thieu') or [])))
    row('Q26b', 'Đa dạng bối cảnh', q_setting.q26b(TL, E), '≤ 25 % · ≤ 90 s · nửa sau ≥ 3')
    row('Q32', 'Footage/ảnh nguồn ngoài', q_footage.q32(E, TL, ep_dir), '≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5×')
    row('Q33', 'Lặp cảnh', q_scene.q33(E, TL, video=m if m and os.path.exists(m) else None), '≤ 2 lần')
    row('Q34', 'Loại shot', q_types.q34(E, TL, ep_dir), 'type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document ≤ 3 s · record ≤ 12 s + dòng tô + nguồn')
    row('Q35', 'Nhãn loại số (D5)', q_chu.q35(E, TL, logs), 'ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL')
    row('Q36', 'Chữ trên màn hình', q_chu.q36(E, TL, logs), 'nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực (+ 1 lần trong câu miễn trừ 0:00–0:15)')
    row('Q37', 'Nhịp thị giác', q_nhip.q37(E, TL, m if m and os.path.exists(m) else None), 'TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s')
    ra = q_amthanh.check(E, TL, master=m, MX=MX, vo=g('vo'), bed=g('bed'), asr='--no-asr' not in a)
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
    bao('ML1', 'Mạch truyện', lambda: q_mach.ml1(E, TL, need(), ep_dir), 'mỗi shot gắn câu/claim · timelapse trôi ≤ 15 %')
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
    bao('NHIP-K2', 'Nhịp kênh 2 (Q14–Q18 không áp → Q37)', lambda: q_k2var.nhip_k2(E, TL, mv), 'TB ≤ 3,5 s · dài nhất ≤ 6 s')
    bao('Q26b-K2', 'Đa dạng loại cảnh + vùng', lambda: q_k2var.q26b_k2(E, TL), '≥ 3 loại/nửa · loại ≤ 70 % · vùng ≤ 25 %, ≤ 90 s, nửa sau ≥ 3')
    bao('Q33-K2', 'Lặp cảnh (vùng, góc) + pHash L/ΔE', lambda: {k: v for k, v in q_k2var.q33_k2(E, TL, mv).items() if k != 'aps'}, '≤ 2 lần (miễn: khác chương + khác năm/lớp)')
    bao('Q32b-K2', 'Trần clip/ảnh', lambda: q_k2var.q32b_k2(E, TL), 'footage ≤ 8 s · ảnh có máy/chú thích đổi ≤ 12 s · ảnh tĩnh ≤ 8 s')
    BT = [a[i + 1] for i, x in enumerate(a) if x == '--bo-tl']
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
    bao('Q37 (1.13)', 'Nhịp — khung tĩnh theo khung neo', lambda: q_nhip.q37(E, TL, mv, v113=True), 'khung tĩnh (mọi khung khác khung đầu quãng < 2,0/255) ≤ 6 s')
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
