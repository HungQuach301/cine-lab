#!/opt/cine/bin/python
"""O2 máy soi lỗi thời đại (O-AI) — bản 1.15.0 (phiên K, 18/10/2026; chủ dự án duyệt O2 ngày 18/10). Mức CẢNH BÁO.
LƯỚI LỌC THỨ HAI: KHÔNG thay kiểm nguồn/kiểm dữ kiện của người (K-LAI-3, kiem-du-kien.json). Căn cứ: reports/pt/PT-BAO-CAO.md §15.4–15.5 (AI đổi cờ
Union 1707 → 1801 ở 3/3 khung 1782; 3 người chấm mù không bắt được và gán nhầm cho khung đúng) — máy soi hỏi ĐÚNG một danh mục cố định trên khung
phóng to, không chấm thẩm mỹ.

  q_thoi_dai.py --video <master.mp4> --nam 1782 [--nam-theo 0-9.5:1782,11.5-20:1943] [--neo 4.5,13.0] [--buoc 5] --out <thư mục>
                [--noi "Gibraltar"] [--api] [--cache cache.json] [--json ra.json]
  q_thoi_dai.py --anh <ảnh.png> [--anh …] --nam 1782 --out <thư mục> [--api] [--cache …]

Lấy mẫu: 1 khung mỗi BUOC (5) giây ở giữa cửa sổ (2,5 s, 7,5 s, …) + MỌI khung neo (--neo, giây). Mỗi khung (1920×1080) thành 5 ảnh: toàn khung
(1568×882) + 4 ô phần tư phóng 1,5× (1440×810). Mỗi khung MỘT lần gọi `claude -p` (judge.call: --bare --restricted, chỉ công cụ Read, không MCP,
không lưu phiên, HOME tạm, khoá CONSOLE_API_KEY qua biến môi trường), mô hình GHIM claude-sonnet-5-5 (judge.MODEL; mô hình khác → lỗi), trần
CAP_USD/khung. Đề bài cố định (PROMPT_VER) với danh mục MUC (cờ — mẫu theo năm, quân phục, tàu, đèn/nguồn sáng, xe, vật hiện đại, chữ/biển
hiệu, kiến trúc/địa hình mốc) + năm khung; trả JSON: nghi_van [{muc, mo_ta, ly_do, nam_xuat_hien, toa_do [x0, y0, x1, y1] (0–1 toàn khung), do_tin}].
Nghi vấn = do_tin ≥ TIN_MIN (0,5); thấp hơn → ghi_chu (không tính). Toạ độ đổi ra px @1920×1080.
BƯỚC 2 (xác nhận phóng to, K thêm sau lượt thử thật 18/10 — khung PT A 1782 cờ 1707 ~20×25 px bị bước 1 báo nhầm "1801", đúng lỗi người chấm PT):
mỗi nghi vấn có toạ độ → vùng vuông quanh hộp (lề = cạnh lớn của hộp, ≥ ZOOM_MIN px) phóng lên ZOOM_PX, một lần gọi nữa (trần CAP2_USD) với câu
hỏi TRUNG TÍNH (chỉ nêu loại mục, không nêu kết luận bước 1): mô tả + "đã có ở năm khung?" → chỉ giữ nghi vấn khi trả lời "no"; "yes" hoặc
"cannot_tell" → hạ xuống ghi_chu kèm lý do. Giới hạn đã đo: cờ ~20–25 px @1080 không đọc được mẫu (K nhìn bằng mắt cũng không thấy chéo đỏ ở khung
C PT) → máy soi KHÔNG bảo đảm bắt cờ nhỏ; bảo vệ cờ bằng cấu trúc (cờ không qua AI — K-LAI-4) và kiểm nguồn.
Bộ đệm: khoá = sha256(ảnh 1080p) + năm + nơi + PROMPT_VER + MODEL; không --api thì chỉ đọc bộ đệm (khung chưa có → THIẾU, không gọi mạng).
Chi phí: total_cost_usd của từng lần gọi (ghi mỗi khung + tổng + TB/khung).
Kết quả hàng O2: ĐẠT khi 0 nghi vấn trên mọi khung mẫu; có nghi vấn → lỗi (mức Cảnh báo, người kiểm từng toạ độ); khung lỗi API/không đọc
được → THIẾU (Cảnh báo).
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import judge  # noqa: E402

PROMPT_VER = 'o2-v2 (K-1.15, 18/10/2026: + bước 2 xác nhận phóng to)'
MODEL = judge.MODEL
BUOC = 5.0
TIN_MIN = 0.5
CAP_USD = 0.40
CAP2_USD = 0.10
ZOOM_PX, ZOOM_MIN = 672, 48   # bước 2: vùng vuông quanh hộp (lề = cạnh lớn của hộp, ≥ ZOOM_MIN px @1080) phóng lên ZOOM_PX
W1080, H1080 = 1920, 1080
MUC = (('co', 'flags and ensigns — identify each flag design and the year that exact design was introduced (and withdrawn); report it if the design '
               'was introduced after {nam} or withdrawn before {nam}'),
       ('quan_phuc', 'uniforms, headgear, insignia, weapons carried by people'),
       ('tau', 'ships and boats — rig, hull form, funnels, steam vs sail, armament, paint scheme'),
       ('den', 'lamps and light sources — electric light, gas light, lit windows, searchlights, floodlights'),
       ('xe', 'vehicles — carts, carriages, motor vehicles, rail, aircraft'),
       ('vat_hien_dai', 'modern objects — plastic, power or telephone lines, antennas, dishes, road markings, modern street furniture, concrete '
                        'or steel structures'),
       ('chu', 'writing and signage IN THE SCENE — painted signs, shop fronts, numbers, typefaces'),
       ('kien_truc', 'architecture and landmark terrain — buildings, fortifications, harbour works, land reclamation, coastline, any structure '
                     'built after {nam}'))
O_TILES = (('o1', 'top-left quarter', (0.0, 0.0)), ('o2', 'top-right quarter', (0.5, 0.0)), ('o3', 'bottom-left quarter', (0.0, 0.5)),
           ('o4', 'bottom-right quarter', (0.5, 0.5)))

PROMPT = """You are a period-accuracy inspector for a historical documentary. The frame depicts the year {nam}{noi}. Your only job: find things \
visible in the scene that did NOT exist yet in {nam}, or that looked different in {nam} (an anachronism). Do not judge beauty or style.

Read ALL five image files with the Read tool before answering:
- {d}/full.jpg — the whole frame (16:9)
{tiles}

Check every item of this fixed list, in order:
{muc}

Rules:
- Report only what you can actually see. If something is too small or blurred to identify, do not report it.
- Ignore documentary overlay graphics that are not part of the scene (caption boxes, year or clock counters, place labels, source/method lines).
- Give each finding's bounding box in FULL-frame normalized coordinates [x0, y0, x1, y1] (0–1, origin top-left). If you saw it in a quarter image, \
convert: full = quarter offset + 0.5 × quarter coordinate.
- do_tin is your confidence (0–1) that it is really anachronistic for {nam}.

Answer with ONLY one JSON object, no other text:
{{"nam": {nam}, "da_kiem": ["co", "quan_phuc", "tau", "den", "xe", "vat_hien_dai", "chu", "kien_truc"], \
"nghi_van": [{{"muc": "<one of the list keys>", "mo_ta": "<what you see>", "ly_do": "<why it is wrong for {nam}>", \
"nam_xuat_hien": <year the thing appeared, or null>, "toa_do": [x0, y0, x1, y1], "do_tin": <0-1>}}]}}
Use "nghi_van": [] when nothing is anachronistic."""


def prompt_for(d, nam, noi=''):
    tiles = '\n'.join(f'- {d}/{k}.jpg — {nm} of the frame, enlarged 1.5× (covers x {ox:.1f}–{ox + 0.5:.1f}, y {oy:.1f}–{oy + 0.5:.1f} of the full frame)'
                      for k, nm, (ox, oy) in O_TILES)
    muc = '\n'.join(f'{i + 1}. {k} — {v.format(nam=nam)}' for i, (k, v) in enumerate(MUC))
    return PROMPT.format(nam=int(nam), noi=f' at {noi}' if noi else '', d=d, tiles=tiles, muc=muc)


def lay_mau(T, buoc=BUOC, neo=()):
    """giây mẫu: giữa mỗi cửa sổ `buoc` + mọi khung neo (bỏ trùng < 1 khung)"""
    ts, k = [], 0
    while k * buoc + buoc / 2 < T: ts.append(round(k * buoc + buoc / 2, 3)); k += 1
    for t in neo:
        if 0 <= t < T and not any(abs(t - x) < 1 / 24 for x in ts): ts.append(round(float(t), 3))
    return sorted(ts)


def nam_tai(t, nam=None, nam_theo=()):
    for a, b, y in nam_theo:
        if a <= t <= b: return y
    return nam


def tach_khung(video, t, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', '-vf', f'scale={W1080}:{H1080}', out], check=True)
    return out


def chuan_bi(img_path, d):
    """ảnh → d/full.jpg + d/o1..o4.jpg; trả về sha256 của ảnh 1080p (khoá bộ đệm)"""
    import cv2
    im = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if im is None: raise FileNotFoundError(img_path)
    if im.shape[:2] != (H1080, W1080): im = cv2.resize(im, (W1080, H1080), interpolation=cv2.INTER_AREA if im.shape[1] > W1080 else cv2.INTER_CUBIC)
    ok, buf = cv2.imencode('.png', im); h = hashlib.sha256(buf.tobytes()).hexdigest()
    os.makedirs(d, exist_ok=True); q = [cv2.IMWRITE_JPEG_QUALITY, 92]
    cv2.imwrite(os.path.join(d, 'full.jpg'), cv2.resize(im, (1568, 882), interpolation=cv2.INTER_AREA), q)
    for k, _, (ox, oy) in O_TILES:
        x0, y0 = int(ox * W1080), int(oy * H1080)
        cv2.imwrite(os.path.join(d, f'{k}.jpg'), cv2.resize(im[y0:y0 + H1080 // 2, x0:x0 + W1080 // 2], (1440, 810), interpolation=cv2.INTER_CUBIC), q)
    return h


def _khoa(h, nam, noi): return hashlib.sha256(f'{h}|{int(nam)}|{noi}|{PROMPT_VER}|{MODEL}'.encode()).hexdigest()[:32]


def _chuan(rep):
    """JSON trả lời → (nghi vấn ≥ TIN_MIN, ghi chú) với toạ độ px @1920×1080; lỗi định dạng → ValueError"""
    if not isinstance(rep, dict) or not isinstance(rep.get('nghi_van'), list): raise ValueError('không có danh sách nghi_van')
    keys = {k for k, _ in MUC}; nv, gc = [], []
    for x in rep['nghi_van']:
        if not isinstance(x, dict): continue
        b = x.get('toa_do'); px = None
        if isinstance(b, list) and len(b) == 4 and all(isinstance(v, (int, float)) for v in b):
            b = [min(max(float(v), 0.0), 1.0) for v in b]; px = [round(b[0] * W1080), round(b[1] * H1080), round(b[2] * W1080), round(b[3] * H1080)]
        y = dict(muc=x.get('muc') if x.get('muc') in keys else f"khác:{x.get('muc')}", mo_ta=str(x.get('mo_ta') or '')[:300], ly_do=str(x.get('ly_do') or '')[:300],
                 nam_xuat_hien=x.get('nam_xuat_hien'), toa_do_px=px, do_tin=float(x['do_tin']) if isinstance(x.get('do_tin'), (int, float)) else None)
        (nv if (y['do_tin'] is None or y['do_tin'] >= TIN_MIN) else gc).append(y)
    return nv, gc


PROMPT2 = """Read the image file {d}/zoom.jpg with the Read tool. It is an enlargement ({k:.1f}×) of one small region of a frame that depicts the year \
{nam}{noi}; the region is {w}×{h} pixels in the 1920×1080 frame, so expect blur. The object of interest is near the centre and belongs to this \
category: {muc_en}.
Describe only what you can actually distinguish (for a flag: field colour, crosses, diagonals and their colours). Then decide whether this exact \
kind of object or design already existed in {nam}.
Answer with ONLY one JSON object: {{"vat": "<what it is>", "dac_diem": "<identifying features you can see>", \
"co_tu_nam": <year this kind/design was introduced, or null>, "da_co_nam_{nam}": "yes" | "no" | "cannot_tell", "ly_do": "<short>"}}"""


def xac_nhan(img1080, x, nam, noi, d, cache_key=None):
    """bước 2 (trung tính: KHÔNG nêu kết luận bước 1): phóng vùng quanh hộp nghi vấn → giữ nghi vấn chỉ khi trả lời da_co_nam_<năm> = "no"."""
    import cv2
    x0, y0, x1, y1 = x['toa_do_px']; s = max(x1 - x0, y1 - y0, ZOOM_MIN); m = s; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; hs = (s + 2 * m) / 2
    X0, Y0 = int(max(0, cx - hs)), int(max(0, cy - hs)); X1, Y1 = int(min(W1080, cx + hs)), int(min(H1080, cy + hs))
    cr = img1080[Y0:Y1, X0:X1]; k = ZOOM_PX / max(cr.shape[:2])
    os.makedirs(d, exist_ok=True); cv2.imwrite(os.path.join(d, 'zoom.jpg'), cv2.resize(cr, (round(cr.shape[1] * k), round(cr.shape[0] * k)), interpolation=cv2.INTER_CUBIC), [cv2.IMWRITE_JPEG_QUALITY, 95])
    muc_en = next((v.format(nam=nam) for kk, v in MUC if kk == x['muc']), str(x['muc']))
    p = PROMPT2.format(d=d, k=k, nam=int(nam), noi=f' at {noi}' if noi else '', w=X1 - X0, h=Y1 - Y0, muc_en=muc_en); y = judge.call(p, d, CAP2_USD)
    open(os.path.join(d, 'run.jsonl'), 'w').write(y['transcript'])
    e = ([f"lỗi API: {y['error']}"] if y['is_error'] else []) + judge.model_errors(y['model_usage'])
    if not y['is_error'] and os.path.join(d, 'zoom.jpg') not in (y.get('reads') or []): e.append('không đọc ảnh phóng')
    rep = judge.parse_json(y.get('result')) if not e else None
    if not e and rep is None: e.append('trả lời không đọc được')
    v = (rep or {}).get(f'da_co_nam_{int(nam)}')
    return dict(vung_px=[X0, Y0, X1, Y1], phong=round(k, 2), tra_loi=rep, da_co=v, giu=(v == 'no'), cost_usd=y.get('cost_usd'), loi='; '.join(e) or None)


def soi_khung(img_path, nam, out_dir, kid, noi='', api=False, cache=None):
    """một khung → dict(id, nam, nghi_van, ghi_chu, cost_usd, model_usage, secs, loi?)"""
    d = os.path.abspath(os.path.join(out_dir, kid)); h = chuan_bi(img_path, d); k = _khoa(h, nam, noi)
    if cache is not None and k in cache: return dict(cache[k], id=kid, tu_bo_dem=True)
    if not api: return dict(id=kid, nam=nam, sha256=h, loi='chưa có trong bộ đệm và không chạy --api', nghi_van=[], ghi_chu=[], cost_usd=None)
    p = prompt_for(d, nam, noi); x = judge.call(p, d, CAP_USD)
    open(os.path.join(d, 'run.jsonl'), 'w').write(x['transcript'])
    e = ([f"lỗi API: {x['error']}"] if x['is_error'] else []) + judge.model_errors(x['model_usage'])
    need = [os.path.join(d, f) for f in ('full.jpg', 'o1.jpg', 'o2.jpg', 'o3.jpg', 'o4.jpg')]
    miss = [os.path.basename(m) for m in need if m not in (x.get('reads') or [])]
    if not x['is_error'] and miss: e.append(f'không đọc đủ ảnh: thiếu {", ".join(miss)}')
    nv, gc = [], []
    if not e:
        try: nv, gc = _chuan(judge.parse_json(x['result']))
        except ValueError as ex: e.append(f'trả lời không đọc được ({ex})')
    c2 = 0.0
    if nv:   # bước 2: xác nhận phóng to từng nghi vấn có toạ độ
        import cv2
        im = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if im.shape[:2] != (H1080, W1080): im = cv2.resize(im, (W1080, H1080), interpolation=cv2.INTER_AREA if im.shape[1] > W1080 else cv2.INTER_CUBIC)
        giu = []
        for i, q in enumerate(nv):
            if not q.get('toa_do_px'): q['xac_nhan'] = dict(loi='không có toạ độ — giữ nghi vấn, không phóng được'); giu.append(q); continue
            z = xac_nhan(im, q, nam, noi, os.path.join(d, f'z{i + 1}')); q['xac_nhan'] = z; c2 += z.get('cost_usd') or 0.0
            if z['loi']: e.append(f"bước 2 nghi vấn {i + 1}: {z['loi']}"); giu.append(q)
            elif z['giu']: giu.append(q)
            else: q['ly_do_ha'] = f"phóng to {z['phong']}×: da_co_nam = {z['da_co']!r} — không xác nhận"; gc.append(q)
        nv = giu
    R = dict(id=kid, nam=int(nam), noi=noi, sha256=h, prompt_ver=PROMPT_VER, model=MODEL, nghi_van=nv, ghi_chu=gc,
             cost_usd=(x.get('cost_usd') or 0.0) + c2 if x.get('cost_usd') is not None else None, cost_buoc2=round(c2, 5),
             model_usage=x.get('model_usage'), secs=x.get('secs'), so_anh_doc=len(x.get('reads') or []), loi='; '.join(e) or None,
             tra_loi=(x.get('result') or '')[:4000])
    if cache is not None and not e: cache[k] = {kk: v for kk, v in R.items() if kk != 'id'}
    return R


def soi(mau, out_dir, api=False, cache=None):
    """mau: [{id, anh, nam, noi?, t?}] → kết quả hàng O2"""
    KQ = [dict(soi_khung(m['anh'], m['nam'], out_dir, m['id'], m.get('noi', ''), api, cache), t=m.get('t')) for m in mau]
    return tong_hop(KQ)


def tong_hop(KQ):
    loi, th = [], []
    for k in KQ:
        if k.get('loi'): th.append(f"khung {k['id']}" + (f" ({k['t']:.1f} s)" if k.get('t') is not None else '') + f": {k['loi']}"); continue
        for x in k['nghi_van']:
            loi.append(f"khung {k['id']}" + (f" ({k['t']:.1f} s)" if k.get('t') is not None else '') + f" năm {k['nam']}: [{x['muc']}] {x['mo_ta']} — {x['ly_do']}"
                       + (f" (xuất hiện {x['nam_xuat_hien']})" if x.get('nam_xuat_hien') else '') + f" @px {x['toa_do_px']} tin {x['do_tin']}")
    cs = [k['cost_usd'] for k in KQ if isinstance(k.get('cost_usd'), (int, float))]; moi = [k for k in KQ if not k.get('tu_bo_dem') and isinstance(k.get('cost_usd'), (int, float))]
    val = (f"{len(KQ)} khung soi · nghi vấn {sum(len(k['nghi_van']) for k in KQ)} ở {sum(1 for k in KQ if k['nghi_van'])} khung · ghi chú (tin < {TIN_MIN}) "
           f"{sum(len(k.get('ghi_chu') or []) for k in KQ)} · chi phí ${sum(cs):.3f}" + (f" (TB ${sum(cs) / len(cs):.3f}/khung)" if cs else '')
           + (f" · gọi mới {len(moi)}" if moi else ' · từ bộ đệm') + f" · {MODEL}")
    kq = 'THIẾU' if th and not loi else None
    return dict(ok=not loi and not th, ket_qua=kq, loi=loi, thieu=th, val=val, khung=KQ, chi_phi_usd=round(sum(cs), 4),
                chi_phi_tb=round(sum(cs) / len(cs), 4) if cs else None, ghi_chu_luat='lưới lọc thứ hai — không thay kiểm nguồn (K-LAI-3)')


def check_video(video, T, out_dir, nam=None, nam_theo=(), neo=(), buoc=BUOC, noi='', api=False, cache=None):
    mau = []
    tmp = tempfile.mkdtemp(prefix='o2-')
    try:
        for t in lay_mau(T, buoc, neo):
            y = nam_tai(t, nam, nam_theo)
            if y is None: continue
            mau.append(dict(id=f't{t:07.2f}'.replace('.', '_'), anh=tach_khung(video, t, os.path.join(tmp, f'{t:.3f}.png')), nam=y, noi=noi, t=t))
        return soi(mau, out_dir, api, cache)
    finally: shutil.rmtree(tmp, ignore_errors=True)


def _dur(video):
    o = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nk=1:nw=1', video], capture_output=True, text=True, check=True)
    return float(o.stdout.strip())


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or not ('--video' in a or '--anh' in a) or '--out' not in a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    cp = g('cache'); cache = json.load(open(cp)) if cp and os.path.exists(cp) else ({} if cp else None)
    nt = [(float(x.split(':')[0].split('-')[0]), float(x.split(':')[0].split('-')[1]), int(x.split(':')[1])) for x in (g('nam-theo') or '').split(',') if x]
    nam = int(g('nam')) if g('nam') else None
    if g('video'):
        R = check_video(g('video'), _dur(g('video')), g('out'), nam, nt, [float(x) for x in (g('neo') or '').split(',') if x], float(g('buoc') or BUOC), g('noi') or '', '--api' in a, cache)
    else:
        imgs = [a[i + 1] for i, x in enumerate(a) if x == '--anh']
        R = soi([dict(id=os.path.splitext(os.path.basename(p))[0], anh=p, nam=nam, noi=g('noi') or '') for p in imgs], g('out'), '--api' in a, cache)
    if cp and cache is not None: json.dump(cache, open(cp, 'w'), ensure_ascii=False, indent=1)
    print('O2 ' + (R['ket_qua'] or ('ĐẠT' if R['ok'] else 'CẢNH BÁO')) + ' · ' + R['val'] + ''.join('\n  ' + x for x in (R['loi'] + R['thieu'])[:40]))
    if g('json'): json.dump(R, open(g('json'), 'w'), ensure_ascii=False, indent=1)
