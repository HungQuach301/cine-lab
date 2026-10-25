#!/opt/cine/bin/python
"""Luật 1.17.4 (phiên K-1.17.4, 23/10/2026) — CHỈ tập kênh 2 từ T4 (`kenh2_tu_t4: true` hoặc khối `n2p:`). T3 và trước: KHÔNG ÁP (không hồi tố).
Căn cứ: Kinh thánh §19 (a)(b)(c) + §13.6 dòng "Từ T4" (chủ dự án duyệt 23/10/2026 17:42, G1 T4 D9); §15 (d) sửa theo Q2 (chủ dự án 23/10/2026
21:45, nguyên văn "Duyệt Q1–Q7"): bỏ trần cứng 20 % cho minh hoạ M-d, thay bằng (i) ngân sách Gemini mỗi tập do chủ dự án đặt, (ii) tổng khung có
AI ≤ 70 % (giữ, N2P-6 (c)), (iii) góc cao timelapse ≥ 60 % thời lượng; Q1: T4 ngân sách Gemini mốc theo dõi $25, chặn $30.
Cấp (cap112): Cảnh báo ở animatic (`animatic: true`) · Chặn ở G2 — trừ mục ghi "(w)" luôn Cảnh báo.

Đầu vào (đường dẫn tương đối thư mục episode.yaml):
  episode.yaml: `ngan_sach_gemini_usd` (trần chặn, $), `ngan_sach_gemini_moc_usd` (mốc theo dõi, $, tuỳ chọn), `so_ai_gemini` (jsonl; không có → `so_ai`,
     lọc dòng Gemini), `goc_toa_do: [E0, N0]` (gốc toạ độ cảnh của log máy; mặc định 532000, 180800 như scripts/k2ldn/t4_do.py), `sha_tu_lieu`
     (tệp danh sách SHA-256 tư liệu, vd licenses/SHA256-TU-LIEU.txt).
  log shot (`log_shot`) mỗi shot: `shot`, `t0`/`t1` hoặc `dur`, `chuong`, `goc` (`cao`…), `tl` (thời gian chạy), `cu_may` ∈ CU_MAY (§19 a; MD/PP/THE
     cho đoạn không phải cú máy 3D), `log_may` (log.json của scripts/k2ldn/render_ldn.js: frames[{f, cam{p, l, fov}, view?, proj?}], W, H, shot.fps),
     `tieu_diem` [x, y, z] toạ độ cảnh | `tieu_diem_en` [E, N, h] (mặc định: điểm nhìn `l` của khung đầu), `khop_voi` (shot tham chiếu của KHOP),
     `diem_neo` (điểm neo KHOP; mặc định tiêu điểm), `hoa_s` (KHOP: thời gian hoà), `lo_ra` (KEO: vật mang nghĩa lộ ra), `mat_dat_m` (cao độ đất
     dưới máy, mặc định 0), `lop: {MAP, MAP3D, KHAC, TL, THE, …: giây}` (như BANG-SHOT), `ai_nen`, `minh_hoa`, `ai_image`, `ai_texture`,
     `tu_lieu_chong_sau_ai` (tư liệu là lớp chồng SAU ghép AI).
     Thiếu `log_may` → được đọc `log_may_tom_tat` (bảng đo của t4_do.py: tieu_diem_pct_khung_s, quay_do_s, may_m_s, khop_lech_neo_px) — chỉ đủ ở
     animatic; ở G2 thiếu log khung = THIẾU (Chặn): số đo phải từ log khung của trình dựng, không từ bảng tóm tắt.

Hàng:
  MAY-19 (§19 a, đo từ log máy mỗi khung; tốc độ = TB trượt 1 s, lấy lớn nhất trong shot):
     (a) tốc độ theo cú máy: CODINH tiêu điểm ≤ 2 % khung/s · DAY tiêu điểm ≤ 1,5 % khung/s và tiến ≤ 1,5 % khoảng cách/s · KEO lùi ≤ 2 %
         khoảng cách/s · CAU dọc ≤ 6 m/s, chúc đổi ≤ 1,5°/s · VONG ≤ 3°/s quanh tiêu điểm, tổng ≤ 45° · TRUOT tiêu điểm ≤ 3 % khung/s · NGHIENG
         ≤ 2°/s · THAP máy 20–60 m trên đất, ngửa 5–15° · XUONG chúc từ ≤ −85° về −35…−20° trong 4–8 s · LAN (§14.3) không đo tốc độ;
     (b) shot có tấm nền N2+ (`ai_nen`) phải `cu_may: CODINH` và đo trôi ≤ 2 % khung/s;
     (c) KHOP: sai khác điểm neo giữa khung cuối shot `khop_voi` và khung đầu shot (hoặc đầu ↔ cuối cùng shot) ≤ 0,5 px (= 0 px ở lưới điểm
         ảnh), cùng FOV; hoà ≤ 1 s;
     (d) mỗi chương ≥ 4 loại cú máy (không tính MD, PP, THE);
     (e) ≤ 2 shot liền nhau cùng loại (thứ tự phim; MD/PP/THE xen giữa ngắt chuỗi);
     (f) THAP tổng ≤ 12 % thời lượng tập;
     (g) shot 3D thiếu `cu_may` hoặc thiếu log máy → THIẾU;
     (w) Cảnh báo: CAU TB dọc < 2 m/s hoặc cao ngoài 150–300 m; VONG tiêu điểm ra ngoài vùng 1/6–5/6 khung; KEO không khai `lo_ra`; DAY phóng
         ảnh > 1,5 %/s (thước phụ).
  BAN-DO-12 (§19 b): (a) bản đồ (MAP cổ + MAP3D 3D kiểu bản đồ) ≤ 12 % thời lượng; (b) mỗi lần dùng bản đồ cổ (MAP) ≤ 10 s.
  TU-LIEU-10 (§19 c): tư liệu + tranh khắc + thẻ (TL + KHAC + THE) ≤ 10 % thời lượng.
  AI-TU-LIEU (§19 b, c): (a) 0 shot có lớp MAP/KHAC/TL mà khai minh_hoa / ai_image / ai_texture; shot có ai_nen + tư liệu phải khai
     `tu_lieu_chong_sau_ai: true`; (b) 0 dòng sổ AI có SHA đầu vào trùng SHA tư liệu (`sha_tu_lieu`).
  GEMINI-NGAN-SACH (Q2 (i), Q1): tổng `usd` các dòng Gemini của sổ AI tập (giá thật từng lệnh) ≤ `ngan_sach_gemini_usd`; (a) vượt → Chặn ở G2;
     (k) thiếu khai ngân sách → Cảnh báo; (m) vượt mốc theo dõi → Cảnh báo; (u) dòng Gemini thiếu `usd` → THIẾU (chưa cộng được giá thật).
  GOC-CAO-60 (Q2 (iii)): thời lượng góc cao có thời gian chạy ≥ 60 % thân phim (trừ thẻ PP), đo theo định nghĩa hiện hành: shot `goc: cao` và
     `tl: true` (TL-1, q_k116.tl1); có log máy → mỗi khung đạt V7B-D1 (cao trên đất ≥ 120 m HOẶC chúc ≥ 15° với cao ≥ 50 m) mới tính.
     1.17.7: k2check thay hàng này bằng GOC-CAO (q_k1177.goc_cao: `goc_cao_min_pct` + 5 chốt cấu trúc); hàm goc_cao_60 giữ nguyên.

1.17.7 (phiên K-1.17.7, 25/10/2026; khiếu nại ANIMATIC-T4 A1, A2 / PHIEU-XEM C13 — chủ dự án 25/10 06:56 "C11, C13 theo khuyến nghị"):
  HỆ TOẠ ĐỘ (A1): log_may, tieu_diem, diem_neo đọc theo HỆ CẢNH y lên: x = E − E0, y = h, z = −(N − N0) (E0, N0 = `goc_toa_do`, mặc định 532000,
     180800). Log ghi [E, N, h] được nhận khi: log khai `toa_do: EN` (hoặc `he_toa_do: EN`), hoặc khung chỉ có `cam_en` (không `cam`) → đổi bằng
     goc_toa_do; điểm khai theo [E, N, h] dùng trường `*_en` (`tieu_diem_en`, `diem_neo_en`). Toạ độ cảnh có |x| hay |z| > 100 km (ngoài mọi cảnh
     tập) là [E, N, h] khai nhầm trường → đổi theo goc_toa_do + (w) nhắc dùng `*_en` (đo, không đoán: cảnh London ≤ vài km quanh gốc).
  KHOP (A2): (c) so khung ĐẦU shot KHOP với khung GẦN NHẤT của shot `khop_voi` (mọi khung, thước 7 điểm như cũ) — "cùng khung" là bất kỳ khung
     đã thấy của shot tham chiếu, không chỉ khung cuối (shot tham chiếu DAY/TRUOT di chuyển); khai `khop_khung: dau | cuoi | <giây trong shot>`
     để ghim một khung. In khung khớp (`khop_khung_ref`). Không `khop_voi`: đầu ↔ cuối cùng shot như cũ.
  THAT (ảnh chụp/footage thật toàn khung, chủ dự án 25/10 09:15): shot khai `that: {…}` hoặc lớp `THAT` phủ cả shot → không phải cú máy 3D
     (như MD/PP/THE: MAY-19 không đòi log máy, ngắt chuỗi (e)); ảnh có chuyển động máy 2D là shot hợp lệ.
"""
import json, math, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import q_k116 as K6  # noqa: E402

CU_MAY = ('CODINH', 'DAY', 'KEO', 'CAU', 'VONG', 'TRUOT', 'NGHIENG', 'THAP', 'XUONG', 'LAN', 'KHOP')
KHONG_MAY = ('MD', 'PP', 'THE', 'THAT')   # 1.17.7: + THAT (ảnh/footage thật toàn khung)
LIM = dict(CODINH_TD=2.0, DAY_TD=1.5, DAY_TIEN=1.5, DAY_PHONG=1.5, KEO_LUI=2.0, CAU_MS=6.0, CAU_MS_MIN=2.0, CAU_CAO=(150.0, 300.0), CAU_CHUC=1.5,
           VONG_DS=3.0, VONG_TONG=45.0, TRUOT_TD=3.0, NGHIENG_DS=2.0, THAP_CAO=(20.0, 60.0), THAP_NGUA=(5.0, 15.0), XUONG_DAU=-85.0, XUONG_CUOI=(-35.0, -20.0),
           XUONG_S=(4.0, 8.0), KHOP_PX=0.5, KHOP_HOA=1.0, THAP_PCT=12.0, LOAI_CHUONG=4, LIEN_MAX=2)
BAN_DO_PCT, BAN_DO_LAN, TU_LIEU_PCT, GOC_CAO_PCT = 12.0, 10.0, 10.0, 60.0
V7B_CAO, V7B_CHUC, V7B_SAN = 120.0, 15.0, 50.0
GOC0 = (532000.0, 180800.0)


def ap_1174(E): return bool(E.get('kenh2_tu_t4') or E.get('n2p'))


def r(loi=(), thieu=(), val='', **kw):
    loi, thieu = list(loi), list(thieu)
    return dict(ok=not loi and not thieu, ket_qua='THIẾU' if thieu and not loi else None, loi=loi, thieu=thieu, val=val, **kw)


def na(why): return dict(ok=True, ket_qua='KHÔNG ÁP', loi=[], val=why)


def sat(ten, v, ng): return [f'{ten} {v} (ngưỡng {ng})'] if ng and abs(v - ng) <= 0.05 * abs(ng) else []


def _dur(s):
    if isinstance(s.get('dur'), (int, float)): return float(s['dur'])
    if isinstance(s.get('t1'), (int, float)) and isinstance(s.get('t0'), (int, float)): return float(s['t1']) - float(s['t0'])
    return 0.0


def _tong(E, TL, LS):
    T = K6.tong(E, TL) if (TL or E.get('segments')) else 0.0
    return T or sum(_dur(s) for s in LS or [])


def _lop(s, *k):
    L = s.get('lop') or {}
    return sum(float(L.get(x) or 0) for x in k if isinstance(L.get(x), (int, float)))


def la_that(s):
    """1.17.7: shot ảnh chụp/footage thật toàn khung — khai `that: {…}` (dict/True) hoặc lớp THAT phủ cả shot"""
    if s.get('that'): return True
    d = _dur(s); v = _lop(s, 'THAT')
    return bool(v > 0 and d > 0 and v >= d - 0.05)


def _cu(s):
    c = str(s.get('cu_may') or '').upper()
    if not c and s.get('minh_hoa'): c = 'MD'
    if (not c or c in ('THAT', 'ANH', 'FOOTAGE')) and la_that(s): c = 'THAT'
    return c


# ---------------------------------------------------------------- hình học máy (toạ độ cảnh y lên, như design/k2v/ldn + t4_do.py)
def _np(): import numpy as np; return np  # noqa: E702


def _view_proj(fr, W, H):
    np = _np()
    if fr.get('view') and fr.get('proj'):
        return np.array(fr['view'], float).reshape(4, 4).T, np.array(fr['proj'], float).reshape(4, 4).T
    p, l = np.array(fr['cam']['p'], float), np.array(fr['cam']['l'], float); f = l - p; f /= np.linalg.norm(f)
    up = np.array([0.0, 1.0, 0.0]) if abs(f[1]) < 0.999 else np.array([0.0, 0.0, -1.0])
    s = np.cross(f, up); s /= np.linalg.norm(s); u = np.cross(s, f)
    V = np.eye(4); V[0, :3], V[1, :3], V[2, :3] = s, u, -f; V[:3, 3] = -V[:3, :3] @ p
    fy = 1.0 / math.tan(math.radians(float(fr['cam'].get('fov') or 50)) / 2); n, fa = 1.0, 1e5
    P = np.zeros((4, 4)); P[0, 0], P[1, 1] = fy / (W / H), fy; P[2, 2], P[2, 3], P[3, 2] = (fa + n) / (n - fa), 2 * fa * n / (n - fa), -1.0
    return V, P


def chieu(fr, W, H, X):
    np = _np(); V, P = _view_proj(fr, W, H); q = P @ V @ np.append(np.asarray(X, float), 1.0); q = q[:3] / q[3]
    return np.array([(q[0] + 1) / 2 * W, (1 - q[1]) / 2 * H])


def _tb1s(v, fps):
    np = _np(); v = np.asarray(v, float)
    if len(v) == 0: return v
    k = max(1, int(round(fps))); return np.convolve(v, np.ones(k) / k, mode='valid') if len(v) >= k else np.array([v.mean()])


def _en(x, goc):
    return [float(x[0]) - goc[0], float(x[2]), -(float(x[1]) - goc[1])]


XA_M = 1e5   # 1.17.7 (A1): toạ độ cảnh |x| hoặc |z| > 100 km = [E, N, h] khai nhầm trường


def _la_en(x):
    return x is not None and len(x) >= 3 and (abs(float(x[0])) > XA_M or abs(float(x[1])) > XA_M)


def chuan_log(L, goc, w=None, M=None):
    """1.17.7 (A1): log máy về hệ cảnh y lên. Đổi khi log khai `toa_do`/`he_toa_do` = EN, hoặc khung chỉ có `cam_en` (không `cam`), hoặc cam.p
    dạng [E, N, h] (> 100 km khỏi gốc cảnh — khai nhầm: (w)). Ma trận view/proj (hệ của trình dựng) bỏ khi đổi — dựng lại từ p, l, fov."""
    if not isinstance(L, dict) or not L.get('frames'): return L
    he = str(L.get('toa_do') or L.get('he_toa_do') or '').upper().replace(',', '').replace(' ', '')
    f0 = L['frames'][0]; cam0 = f0.get('cam') or {}
    khai_en = he in ('EN', 'ENH'); chi_en = not cam0 and bool(f0.get('cam_en')); nham = bool(cam0) and _la_en(cam0.get('p'))
    if not (khai_en or chi_en or nham): return L
    if nham and not khai_en and M is not None:
        M['w'].append(f'(w) {w}: log_may ghi cam.p theo [E, N, h] (> 100 km khỏi gốc cảnh) — khai `toa_do: EN` hoặc ghi hệ cảnh (x = E − E0, y = h, z = −(N − N0)); đã đổi theo goc_toa_do')
    FR = []
    for fr in L['frames']:
        c = (fr.get('cam') if fr.get('cam') and not chi_en else fr.get('cam_en')) or {}
        FR.append(dict({k: v for k, v in fr.items() if k not in ('view', 'proj', 'cam', 'cam_en')}, cam=dict(c, p=_en(c['p'], goc), l=_en(c['l'], goc))))
    return dict(L, frames=FR, toa_do='canh (đổi từ EN — 1.17.7)')


def do_shot(L, F=None, mat_dat=0.0):
    """log render_ldn.js → số đo (tốc độ đã TB trượt 1 s; lấy lớn nhất)."""
    np = _np(); W, H = float(L.get('W') or 1920), float(L.get('H') or 1080); fps = float((L.get('shot') or {}).get('fps') or L.get('fps') or 24)
    FR = sorted(L['frames'], key=lambda x: x.get('f', 0)); n = len(FR)
    p = np.array([x['cam']['p'] for x in FR], float); l = np.array([x['cam']['l'] for x in FR], float); fov = np.array([float(x['cam'].get('fov') or 50) for x in FR])
    F = np.asarray(F if F is not None else l[0], float)
    s = np.array([chieu(x, W, H, F) for x in FR]); d = np.linalg.norm(p - F, axis=1); dr = (l - p) / np.linalg.norm(l - p, axis=1, keepdims=True)
    chuc = np.degrees(np.arcsin(np.clip(dr[:, 1], -1, 1)))   # âm = nhìn xuống
    az = np.degrees(np.unwrap(np.arctan2(p[:, 2] - F[2], p[:, 0] - F[0])))
    out = dict(n=n, giay=round(n / fps, 3), fps=fps, W=W, H=H)
    if n >= 2:
        td = np.linalg.norm(np.diff(s, axis=0), axis=1) * fps / W * 100
        tien = -np.diff(d) / d[:-1] * fps * 100   # + = tiến vào
        sc = np.log(1.0 / (d * np.tan(np.radians(fov) / 2))); ph = np.abs(np.diff(sc)) * fps * 100
        quay = np.degrees(np.arccos(np.clip((dr[1:] * dr[:-1]).sum(1), -1, 1))) * fps
        doc = np.abs(np.diff(p[:, 1])) * fps; dchuc = np.abs(np.diff(chuc)) * fps; daz = np.abs(np.diff(az)) * fps
        m = lambda v: round(float(_tb1s(v, fps).max()), 3)
        out.update(td=m(td), tien=m(tien), lui=m(-tien), phong=m(ph), quay=m(quay), doc=m(doc), doc_tb=round(float(doc.mean()), 3), chuc_ds=m(dchuc), vong_ds=m(daz),
                   vong_tong=round(float(abs(az[-1] - az[0])), 2))
    else:
        out.update(td=0.0, tien=0.0, lui=0.0, phong=0.0, quay=0.0, doc=0.0, doc_tb=0.0, chuc_ds=0.0, vong_ds=0.0, vong_tong=0.0)
    cao = p[:, 1] - float(mat_dat)
    out.update(cao=[round(float(cao.min()), 1), round(float(cao.max()), 1)], chuc=[round(float(chuc.min()), 2), round(float(chuc.max()), 2)],
               chuc_dau=round(float(chuc[0]), 2), chuc_cuoi=round(float(chuc[-1]), 2), fov=[round(float(fov.min()), 3), round(float(fov.max()), 3)],
               td_x=[round(float(s[:, 0].min() / W), 3), round(float(s[:, 0].max() / W), 3)], td_y=[round(float(s[:, 1].min() / H), 3), round(float(s[:, 1].max() / H), 3)])
    # XUONG: thời gian từ khi rời ≤ −85° tới khi vào −35…−20°
    t_roi = next((i for i in range(n) if chuc[i] > LIM['XUONG_DAU']), None); t_vao = next((i for i in range(n) if LIM['XUONG_CUOI'][0] <= chuc[i] <= LIM['XUONG_CUOI'][1]), None)
    out['xuong_s'] = round((t_vao - t_roi) / fps, 2) if t_roi is not None and t_vao is not None and t_vao >= t_roi else None
    # V7B-D1 theo khung: cao ≥ 120 m HOẶC (chúc ≥ 15° và cao ≥ 50 m)
    v7 = (cao >= V7B_CAO) | ((-chuc >= V7B_CHUC) & (cao >= V7B_SAN)); out['v7b_ty'] = round(float(v7.mean()), 4)
    out['_s'], out['_fov'], out['_FR'] = s, fov, FR
    return out


def _ld(base, x):
    if x is None or isinstance(x, (dict, list)): return x
    return K6._load(K6._p(base, x))


def _tieu_diem(s, E):
    goc = tuple(E.get('goc_toa_do') or GOC0)
    if s.get('tieu_diem') is not None:
        if _la_en(s['tieu_diem']): return _en(s['tieu_diem'], goc)   # 1.17.7 (A1): [E, N, h] khai nhầm trường (> 100 km) → đổi
        return [float(v) for v in s['tieu_diem']]
    if s.get('tieu_diem_en') is not None: return _en(s['tieu_diem_en'], goc)
    return None


def _diem_neo(s, E, M=None, w=''):
    """1.17.7 (A1/A2): điểm neo KHOP — `diem_neo_en` [E, N, h] | `diem_neo` hệ cảnh; diem_neo dạng [E, N, h] (> 100 km) → đổi + (w)"""
    goc = tuple(E.get('goc_toa_do') or GOC0)
    if s.get('diem_neo_en') is not None: return _en(s['diem_neo_en'], goc)
    if s.get('diem_neo') is not None:
        if _la_en(s['diem_neo']):
            if M is not None: M['w'].append(f'(w) {w} KHOP: diem_neo {list(s["diem_neo"])} là [E, N, h] (> 100 km khỏi gốc cảnh) — khai `diem_neo_en`; đã đổi theo goc_toa_do')
            return _en(s['diem_neo'], goc)
        return [float(v) for v in s['diem_neo']]
    return None


def _ap_toc_do(c, D, M, w):
    """(a) tốc độ theo loại + (w) cảnh báo phụ"""
    L = LIM
    def vuot(ten, v, ng, muc='a'):
        if v is not None and v > ng + 1e-9: M[muc].append(f'({muc}) {w} {c}: {ten} {v:g} > {ng:g}')
    if c == 'CODINH': vuot('tiêu điểm % khung/s', D['td'], L['CODINH_TD'])
    elif c == 'DAY':
        vuot('tiêu điểm % khung/s', D['td'], L['DAY_TD']); vuot('tiến % khoảng cách/s', D['tien'], L['DAY_TIEN'])
        if D['phong'] > L['DAY_PHONG'] + 1e-9: M['w'].append(f"(w) {w} DAY: phóng ảnh tại tiêu điểm {D['phong']:g} %/s > {L['DAY_PHONG']:g} (thước phụ)")
    elif c == 'KEO': vuot('lùi % khoảng cách/s', D['lui'], L['KEO_LUI'])
    elif c == 'CAU':
        vuot('dọc m/s', D['doc'], L['CAU_MS']); vuot('chúc đổi °/s', D['chuc_ds'], L['CAU_CHUC'])
        if D['doc_tb'] < L['CAU_MS_MIN']: M['w'].append(f"(w) {w} CAU: dọc TB {D['doc_tb']:g} m/s < {L['CAU_MS_MIN']:g}")
        if D['cao'][0] < L['CAU_CAO'][0] - 1e-9 or D['cao'][1] > L['CAU_CAO'][1] + 1e-9: M['w'].append(f"(w) {w} CAU: cao {D['cao'][0]:g}–{D['cao'][1]:g} m ngoài {L['CAU_CAO'][0]:g}–{L['CAU_CAO'][1]:g} m")
    elif c == 'VONG':
        vuot('vòng °/s', D['vong_ds'], L['VONG_DS']); vuot('vòng tổng °', D['vong_tong'], L['VONG_TONG'])
        if D['td_x'][0] < 1 / 6 or D['td_x'][1] > 5 / 6 or D['td_y'][0] < 1 / 6 or D['td_y'][1] > 5 / 6: M['w'].append(f"(w) {w} VONG: tiêu điểm ra ngoài vùng 1/6–5/6 khung (x {D['td_x']}, y {D['td_y']})")
    elif c == 'TRUOT': vuot('tiêu điểm % khung/s', D['td'], L['TRUOT_TD'])
    elif c == 'NGHIENG': vuot('quay °/s', D['quay'], L['NGHIENG_DS'])
    elif c == 'THAP':
        if D['cao'][0] < L['THAP_CAO'][0] - 1e-9 or D['cao'][1] > L['THAP_CAO'][1] + 1e-9: M['a'].append(f"(a) {w} THAP: máy cao {D['cao'][0]:g}–{D['cao'][1]:g} m ngoài {L['THAP_CAO'][0]:g}–{L['THAP_CAO'][1]:g} m trên đất")
        if D['chuc'][0] < L['THAP_NGUA'][0] - 1e-9 or D['chuc'][1] > L['THAP_NGUA'][1] + 1e-9: M['a'].append(f"(a) {w} THAP: ngửa {D['chuc'][0]:g}…{D['chuc'][1]:g}° ngoài {L['THAP_NGUA'][0]:g}–{L['THAP_NGUA'][1]:g}°")
    elif c == 'XUONG':
        if D['chuc_dau'] > L['XUONG_DAU'] + 1e-9: M['a'].append(f"(a) {w} XUONG: chúc đầu {D['chuc_dau']:g}° (cần ≤ {L['XUONG_DAU']:g}°)")
        if not L['XUONG_CUOI'][0] - 1e-9 <= D['chuc_cuoi'] <= L['XUONG_CUOI'][1] + 1e-9: M['a'].append(f"(a) {w} XUONG: chúc cuối {D['chuc_cuoi']:g}° ngoài {L['XUONG_CUOI'][0]:g}…{L['XUONG_CUOI'][1]:g}°")
        xs = D.get('xuong_s')
        if xs is None or not L['XUONG_S'][0] - 1e-9 <= xs <= L['XUONG_S'][1] + 1e-9: M['a'].append(f"(a) {w} XUONG: chuyển {xs} s ngoài {L['XUONG_S'][0]:g}–{L['XUONG_S'][1]:g} s")


def _ap_tom_tat(c, R, M, w):
    """bảng tóm tắt t4_do.py: chỉ td (% khung/s, max) · quay (°/s, max) · may_m_s (max); loại cần số không có trong bảng → THIẾU (g)."""
    td = (R.get('tieu_diem_pct_khung_s') or {}).get('max'); qu = (R.get('quay_do_s') or {}).get('max'); ms = (R.get('may_m_s') or {}).get('max')
    def vuot(ten, v, ng):
        if v is None: M['g'].append(f'(g) {w} {c}: bảng tóm tắt không có {ten}')
        elif v > ng + 1e-9: M['a'].append(f'(a) {w} {c}: {ten} {v:g} > {ng:g} (bảng tóm tắt t4_do)')
    if c == 'CODINH': vuot('tiêu điểm % khung/s', td, LIM['CODINH_TD'])
    elif c in ('DAY', 'TRUOT'): vuot('tiêu điểm % khung/s', td, LIM[c + '_TD'])
    elif c == 'VONG': vuot('quay °/s (cận trên của vòng °/s)', qu, LIM['VONG_DS'])
    elif c == 'NGHIENG': vuot('quay °/s', qu, LIM['NGHIENG_DS'])
    elif c == 'CAU': vuot('máy m/s (cận trên của dọc m/s)', ms, LIM['CAU_MS']); vuot('quay °/s (cận trên của chúc °/s)', qu, LIM['CAU_CHUC'])
    elif c == 'KHOP':
        k = R.get('khop_lech_neo_px')
        if k is None: M['g'].append(f'(g) {w} KHOP: bảng tóm tắt không có khop_lech_neo_px')
        elif k > LIM['KHOP_PX'] + 1e-9: M['c'].append(f'(c) {w} KHOP: lệch neo {k:g} px > {LIM["KHOP_PX"]:g} (bảng tóm tắt)')
    elif c in ('KEO', 'THAP', 'XUONG'): M['g'].append(f'(g) {w} {c}: bảng tóm tắt không đủ số (cần log khung)')


def may19(E, TL, LS, ep_dir='.', cong='G2'):
    if LS is None: return r(thieu=['(g) không có log shot'], val='—', cong=cong)
    T = _tong(E, TL, LS); M = {k: [] for k in 'abcdefgw'}; near = []; DO = {}; nlog = ntt = 0
    Z = sorted(LS, key=lambda s: float(s.get('t0') or 0))
    for s in Z:
        c = _cu(s); w = str(s.get('shot'))
        if c in KHONG_MAY: continue
        if not c:
            if s.get('goc') in ('cao', 'thap', 'neo') or s.get('tl'): M['g'].append(f'(g) {w}: shot 3D không khai `cu_may`')
            continue
        if c not in CU_MAY: M['g'].append(f'(g) {w}: cu_may {c!r} không thuộc §19 (a) ({", ".join(CU_MAY)})'); continue
        if s.get('ai_nen') and c != 'CODINH': M['b'].append(f'(b) {w}: shot tấm nền N2+ (ai_nen) phải CODINH, khai {c}')
        Lg = None
        try: Lg = chuan_log(_ld(ep_dir, s.get('log_may')), tuple(E.get('goc_toa_do') or GOC0), w, M)   # 1.17.7 (A1): log [E, N, h] → hệ cảnh
        except Exception as e: M['g'].append(f'(g) {w}: không đọc được log_may: {e}')   # noqa: BLE001
        if Lg:
            nlog += 1; D = do_shot(Lg, _tieu_diem(s, E), float(s.get('mat_dat_m') or E.get('mat_dat_m') or 0)); DO[w] = D
            _ap_toc_do(c, D, M, w)
            if s.get('ai_nen') and D['td'] > LIM['CODINH_TD'] + 1e-9: M['b'].append(f"(b) {w}: tấm nền N2+ nhưng trôi {D['td']:g} % khung/s > {LIM['CODINH_TD']:g}")
            for nm, v, ng in (('tiêu điểm %/s', D['td'], {'CODINH': 2.0, 'DAY': 1.5, 'TRUOT': 3.0}.get(c)), ('vòng °/s', D['vong_ds'], 3.0 if c == 'VONG' else None),
                              ('quay °/s', D['quay'], 2.0 if c == 'NGHIENG' else None)):
                if ng: near += sat(f'{w} {nm}', v, ng)
            if c == 'KHOP':
                Fn = _diem_neo(s, E, M, w) or _tieu_diem(s, E) or Lg['frames'][0]['cam']['l']   # 1.17.7 (A1): diem_neo_en / diem_neo [E, N, h] đổi hệ cảnh
                ref = next((x for x in LS if str(x.get('shot')) == str(s.get('khop_voi'))), None) if s.get('khop_voi') else None
                try: LR = chuan_log(_ld(ep_dir, ref.get('log_may')), tuple(E.get('goc_toa_do') or GOC0)) if ref else Lg
                except Exception as e: LR = None; M['g'].append(f'(g) {w}: không đọc được log_may của {s.get("khop_voi")}: {e}')   # noqa: BLE001
                if LR:
                    FRb = sorted(Lg['frames'], key=lambda x: x.get('f', 0)); FRa = sorted(LR['frames'], key=lambda x: x.get('f', 0))
                    fb = FRb[0 if ref else -1]
                    Wd, Hd = float(Lg.get('W') or 1920), float(Lg.get('H') or 1080); np = _np()

                    def lech(fa):
                        # điểm neo + 6 điểm lệch ±25 % khoảng cách (ngang, dọc, trước/sau theo máy tham chiếu): khớp "cùng máy, cùng FOV" cả khung,
                        # không chỉ điểm nhìn (điểm nhìn luôn ở giữa khung dù máy dời)
                        pa, la = np.array(fa['cam']['p'], float), np.array(fa['cam']['l'], float); f_ = (la - pa) / np.linalg.norm(la - pa)
                        sx = np.cross(f_, [0.0, 1.0, 0.0]); sx = sx / (np.linalg.norm(sx) or 1.0); uy = np.cross(sx, f_); dd = 0.25 * float(np.linalg.norm(np.asarray(Fn, float) - pa))
                        P5 = [np.asarray(Fn, float)] + [np.asarray(Fn, float) + q * dd * v for v in (sx, uy, f_) for q in (-1.0, 1.0)]   # + trước/sau tiêu điểm (thị sai)
                        return max(float(np.linalg.norm(chieu(fa, Wd, Hd, X) - chieu(fb, Wd, Hd, X))) for X in P5)
                    if not ref: cand = [(0, FRb[0])]
                    else:   # 1.17.7 (A2): khung gần nhất của shot tham chiếu (mọi khung) — hoặc khung ghim `khop_khung`
                        kk = s.get('khop_khung'); fpsr = float((LR.get('shot') or {}).get('fps') or LR.get('fps') or 24)
                        if kk == 'dau': cand = [(0, FRa[0])]
                        elif kk == 'cuoi': cand = [(len(FRa) - 1, FRa[-1])]
                        elif isinstance(kk, (int, float)) and not isinstance(kk, bool): j = min(len(FRa) - 1, max(0, int(round(float(kk) * fpsr)))); cand = [(j, FRa[j])]
                        else: cand = list(enumerate(FRa))
                    dpx, jk = min((lech(fa), j) for j, fa in cand); fa = FRa[jk] if ref else FRb[0]
                    D['khop_px'] = round(dpx, 3); D['khop_khung_ref'] = (f'{jk}/{len(FRa)}' if ref else 'đầu ↔ cuối cùng shot')
                    if dpx > LIM['KHOP_PX'] + 1e-9: M['c'].append(f"(c) {w} KHOP: lệch điểm neo {dpx:.2f} px > {LIM['KHOP_PX']:g} px (0 px ở lưới điểm ảnh)")
                    if abs(float(fa['cam'].get('fov') or 0) - float(fb['cam'].get('fov') or 0)) > 1e-6: M['c'].append(f"(c) {w} KHOP: FOV khác ({fa['cam'].get('fov')} ↔ {fb['cam'].get('fov')})")
                if isinstance(s.get('hoa_s'), (int, float)) and s['hoa_s'] > LIM['KHOP_HOA'] + 1e-9: M['c'].append(f"(c) {w} KHOP: hoà {s['hoa_s']:g} s > {LIM['KHOP_HOA']:g} s")
        elif s.get('log_may_tom_tat'):
            ntt += 1
            try: R = _ld(ep_dir, s['log_may_tom_tat'])
            except Exception as e: M['g'].append(f'(g) {w}: không đọc được log_may_tom_tat: {e}'); continue   # noqa: BLE001
            _ap_tom_tat(c, R, M, w)
            if cong != 'animatic': M['g'].append(f'(g) {w}: chỉ có bảng tóm tắt (t4_do), không có log khung — ở G2 phải đo từ log khung')
        elif c != 'LAN': M['g'].append(f'(g) {w}: không có `log_may` (log.json render_ldn.js) — không đo được §19 (a)')
        if c == 'KEO' and not s.get('lo_ra'): M['w'].append(f'(w) {w} KEO: không khai `lo_ra` (vật mang nghĩa mới lộ ra — §19 a)')
    # (d) ≥ 4 loại/chương · (e) ≤ 2 liền · (f) THAP ≤ 12 %
    ch = {}
    for s in Z:
        c = _cu(s)
        if c in CU_MAY: ch.setdefault(str(s.get('chuong', '?')), set()).add(c)
    for k, v in ch.items():
        if len(v) < LIM['LOAI_CHUONG']: M['d'].append(f"(d) chương {k}: {len(v)} loại cú máy ({', '.join(sorted(v))}) < {LIM['LOAI_CHUONG']}")
    run, prev = 0, None
    for s in Z:
        c = _cu(s)
        if c in CU_MAY and c == prev: run += 1
        else: run = 1 if c in CU_MAY else 0
        prev = c if c in CU_MAY else None
        if run == LIM['LIEN_MAX'] + 1: M['e'].append(f"(e) {s.get('shot')}: {run} shot liền cùng loại {c} > {LIM['LIEN_MAX']}")
    th = sum(_dur(s) for s in Z if _cu(s) == 'THAP'); pth = 100 * th / T if T else 0.0
    if pth > LIM['THAP_PCT'] + 1e-9: M['f'].append(f"(f) THAP {th:.1f} s = {pth:.1f} % > {LIM['THAP_PCT']:g} % thời lượng tập")
    near += sat('THAP %', round(pth, 2), LIM['THAP_PCT'])
    thieu = M.pop('g'); loi = sum(M.values(), [])
    val = (f"{sum(1 for s in Z if _cu(s) in CU_MAY)} shot cú máy · log khung {nlog} · tóm tắt {ntt} · loại/chương " + ', '.join(f'{k}:{len(v)}' for k, v in sorted(ch.items()))
           + f" · THAP {pth:.1f} % · lỗi a {len(M['a'])} b {len(M['b'])} c {len(M['c'])} d {len(M['d'])} e {len(M['e'])} f {len(M['f'])} · cảnh báo w {len(M['w'])}")
    M['g'] = thieu
    return r(loi, thieu, val, muc=M, sat_nguong=near, cong=cong, do={k: {kk: vv for kk, vv in v.items() if not kk.startswith('_')} for k, v in DO.items()})


# ---------------------------------------------------------------- §19 (b)(c) trần
def ban_do_12(E, TL, LS, cong='G2'):
    if LS is None: return r(thieu=['không có log shot'], val='—', cong=cong)
    T = _tong(E, TL, LS); M = {'a': [], 'b': []}; tot = 0.0
    for s in LS:
        v = _lop(s, 'MAP', 'MAP3D') or (float(s['ban_do_s']) if isinstance(s.get('ban_do_s'), (int, float)) else 0.0); tot += v
        vc = _lop(s, 'MAP') or (float(s['ban_do_co_s']) if isinstance(s.get('ban_do_co_s'), (int, float)) else 0.0)   # "mỗi lần ≤ 10 s" là lần dùng BẢN ĐỒ CỔ (§19 b)
        if vc > BAN_DO_LAN + 1e-9: M['b'].append(f"(b) {s.get('shot')}: bản đồ cổ {vc:g} s > {BAN_DO_LAN:g} s/lần")
    p = 100 * tot / T if T else 0.0
    if p > BAN_DO_PCT + 1e-9: M['a'].append(f'(a) bản đồ (cổ + 3D kiểu bản đồ) {tot:.1f} s = {p:.2f} % > {BAN_DO_PCT:g} %')
    return r(sum(M.values(), []), val=f'{tot:.1f} s / {T:.1f} s = {p:.2f} %', sat_nguong=sat('bản đồ %', round(p, 2), BAN_DO_PCT), muc=M, cong=cong, pct=round(p, 2))


def tu_lieu_10(E, TL, LS, cong='G2'):
    if LS is None: return r(thieu=['không có log shot'], val='—', cong=cong)
    T = _tong(E, TL, LS); tot = sum(_lop(s, 'TL', 'KHAC', 'THE') for s in LS); p = 100 * tot / T if T else 0.0
    loi = [f'(a) tư liệu + tranh khắc + thẻ {tot:.1f} s = {p:.2f} % > {TU_LIEU_PCT:g} %'] if p > TU_LIEU_PCT + 1e-9 else []
    return r(loi, val=f'{tot:.1f} s / {T:.1f} s = {p:.2f} % (TL {sum(_lop(s, "TL") for s in LS):g} · KHAC {sum(_lop(s, "KHAC") for s in LS):g} · THE {sum(_lop(s, "THE") for s in LS):g} s)',
             sat_nguong=sat('tư liệu + khắc + thẻ %', round(p, 2), TU_LIEU_PCT), cong=cong, pct=round(p, 2))


def _so_gemini(E, ep_dir):
    p = E.get('so_ai_gemini') or E.get('so_ai')
    if not p: return None, 'không khai `so_ai_gemini` / `so_ai`'
    try: J = K6._load(K6._p(ep_dir, p))
    except Exception as e: return None, f'không đọc được sổ AI ({p}): {e}'   # noqa: BLE001
    J = J if isinstance(J, list) else (J.get('dong') or J.get('records') or [J]) if isinstance(J, dict) else []
    g = [x for x in J if isinstance(x, dict) and ('gemini' in str(x.get('nha') or '').lower() or 'gemini' in str(x.get('model_req') or x.get('model') or '').lower())]
    return g, None


def ai_tu_lieu(E, LS, ep_dir='.', cong='G2'):
    if LS is None: return r(thieu=['không có log shot'], val='—', cong=cong)
    M = {'a': [], 'b': []}; th = []; n = 0
    for s in LS:
        if _lop(s, 'MAP', 'KHAC', 'TL') <= 0: continue
        n += 1; w = str(s.get('shot'))
        ai = [k for k in ('minh_hoa', 'ai_image', 'ai_texture') if s.get(k)]
        if ai: M['a'].append(f"(a) {w}: shot có tư liệu (bản đồ cổ/tranh khắc/ảnh) khai {', '.join(ai)} — §19 (b)(c) không AI lên tư liệu")
        if s.get('ai_nen') and not s.get('tu_lieu_chong_sau_ai'): M['a'].append(f'(a) {w}: shot tấm nền N2+ có tư liệu nhưng không khai `tu_lieu_chong_sau_ai: true`')
    sha = set()
    if E.get('sha_tu_lieu'):
        try:
            for ln in open(K6._p(ep_dir, E['sha_tu_lieu']), encoding='utf-8'):
                sha.update(re.findall(r'\b[0-9a-f]{64}\b', ln))
        except OSError as e: th.append(f'(b) không đọc được sha_tu_lieu: {e}')
    else: th.append('(b) không khai `sha_tu_lieu` (danh sách SHA-256 tư liệu) — không đối chiếu được sổ AI')
    nso = 0
    for key in ('so_ai', 'so_ai_gemini', 'so_ai_openai'):
        if not E.get(key): continue
        try: J = K6._load(K6._p(ep_dir, E[key]))
        except Exception: continue   # noqa: BLE001
        for x in (J if isinstance(J, list) else []):
            nso += 1; vs = re.findall(r'\b[0-9a-f]{64}\b', json.dumps({k: v for k, v in x.items() if k in ('input', 'inputs', 'sha_vao', 'vao', 'anh_vao')}))
            hit = sha.intersection(vs)
            if hit: M['b'].append(f"(b) sổ AI {x.get('tag') or x.get('id')}: đầu vào là tư liệu (SHA {sorted(hit)[0][:12]}…) — cấm AI lên bản đồ cổ/tranh khắc")
    return r(sum(M.values(), []), th, val=f'{n} shot có tư liệu · {len(sha)} SHA tư liệu · {nso} dòng sổ AI đối chiếu', muc=M, cong=cong)


def gemini_ngan_sach(E, ep_dir='.', cong='G2'):
    G, why = _so_gemini(E, ep_dir); M = {'a': [], 'k': [], 'm': [], 'u': []}
    if G is None: return r(thieu=[f'(u) {why}'], val='—', muc=dict(M, u=[f'(u) {why}']), cong=cong)
    tot, thieu = 0.0, []
    for x in G:
        u = x.get('usd', x.get('chi_phi_usd', x.get('cost_usd')))
        if isinstance(u, (int, float)): tot += float(u)
        else: thieu.append(f"(u) dòng {x.get('tag') or x.get('id')}: không có giá thật `usd` (usage {str(x.get('usage'))[:60]})")
    ns, moc = E.get('ngan_sach_gemini_usd'), E.get('ngan_sach_gemini_moc_usd'); near = []
    if not isinstance(ns, (int, float)): M['k'].append('(k) episode.yaml không khai `ngan_sach_gemini_usd` (ngân sách Gemini của tập do chủ dự án đặt — Q2 (i))')
    elif tot > ns + 1e-9: M['a'].append(f'(a) Gemini ${tot:.2f} > ngân sách ${ns:g} ({len(G)} lệnh)')
    if isinstance(ns, (int, float)): near += sat('Gemini $', round(tot, 2), float(ns))
    if isinstance(moc, (int, float)) and tot > moc + 1e-9: M['m'].append(f'(m) Gemini ${tot:.2f} > mốc theo dõi ${moc:g}')
    M['u'] = thieu
    return r(M['a'] + M['k'] + M['m'], thieu, val=f'{len(G)} lệnh Gemini · ${tot:.2f}' + (f' / ngân sách ${ns:g}' if isinstance(ns, (int, float)) else ' / chưa khai ngân sách')
             + (f' (mốc ${moc:g})' if isinstance(moc, (int, float)) else ''), muc=M, sat_nguong=near, cong=cong, usd=round(tot, 4))


def goc_cao_60(E, TL, LS, ep_dir='.', cong='G2'):
    if LS is None: return r(thieu=['không có log shot'], val='—', cong=cong)
    T = K6.tong(E, TL) if (TL or E.get('segments')) else sum(_dur(s) for s in LS)
    PPd = sum(b - a for _, a, b, _ in K6.pp_spans(E, TL)) if (TL or E.get('segments')) else sum(_dur(s) for s in LS if _cu(s) == 'PP')
    Tb = T - PPd; cao = 0.0; th = []; nlog = 0
    for s in LS:
        if not s.get('tl') or K6.goc_of(s, E) != 'cao': continue
        d = _dur(s); Lg = None
        try: Lg = _ld(ep_dir, s.get('log_may'))
        except Exception: Lg = None   # noqa: BLE001
        if Lg:
            nlog += 1; D = do_shot(Lg, _tieu_diem(s, E), float(s.get('mat_dat_m') or E.get('mat_dat_m') or 0)); cao += d * D['v7b_ty']
        else: cao += d
    nog = [str(s.get('shot')) for s in LS if K6.goc_of(s, E) is None and _cu(s) not in KHONG_MAY]
    if nog: th.append(f'{len(nog)} shot không khai `goc` ({", ".join(nog[:6])})')
    p = 100 * cao / Tb if Tb else 0.0
    loi = [f'(a) góc cao timelapse {cao:.1f} s = {p:.1f} % < {GOC_CAO_PCT:g} % thân phim ({Tb:.1f} s)'] if p < GOC_CAO_PCT - 1e-9 else []
    return r(loi, th if not loi else [], val=f'{cao:.1f} s / {Tb:.1f} s = {p:.1f} % (log khung V7B-D1: {nlog} shot)', sat_nguong=sat('góc cao %', round(p, 1), GOC_CAO_PCT), cong=cong, pct=round(p, 2))


ROWS = ('MAY-19', 'BAN-DO-12', 'TU-LIEU-10', 'AI-TU-LIEU', 'GEMINI-NGAN-SACH', 'GOC-CAO-60')


def chuan_ls(LS):
    """nhận cả bảng shot tiền kỳ (scripts/k2ldn/bang_shot.py → BANG-SHOT-v*.json: {shot: [{ma, phan, bat_dau_s, giay, loai_may, may{cao}, lop}]}) → dạng log shot.
    Bảng shot là KẾ HOẠCH (khai): dùng cho thử luật/ước trước dựng; số đo máy §19 (a) vẫn cần log khung."""
    if isinstance(LS, dict) and isinstance(LS.get('shot'), list): LS = LS['shot']
    if not isinstance(LS, list): return LS
    out = []
    for x in LS:
        if 'ma' in x and 'shot' not in x:
            lop = dict(x.get('lop') or {}); c = str(x.get('loai_may') or '').upper(); may = x.get('may') or {}
            y = dict(shot=x['ma'], t0=float(x.get('bat_dau_s') or 0), dur=float(x.get('giay') or 0), chuong=x.get('phan'), cu_may=c, lop=lop,
                     ai_nen=bool(lop.get('N2P')), minh_hoa=(c == 'MD'), tl=c not in KHONG_MAY, goc=('cao' if may.get('cao') else 'thap') if may else ('phang' if c in ('PP', 'THE') else None),
                     diem_may=x.get('diem_may'), _bang_shot=True)
            y['t1'] = y['t0'] + y['dur']; out.append(y)
        else: out.append(x)
    return out


def check(E, TL=None, ep_dir='.', LS=None, video=None):
    if not ap_1174(E): return {k: na('tập trước T4 (không khai kenh2_tu_t4 / n2p) — 1.17.4 không hồi tố') for k in ROWS}
    cong = 'animatic' if E.get('animatic') else 'G2'; out = {}
    if not LS and E.get('log_shot'):   # log_shot là bảng shot tiền kỳ (dict {shot: […]}) — K6.log_shot chỉ đọc khoá `shots`
        try: LS = K6._load(K6._p(ep_dir, E['log_shot']))
        except Exception: LS = None   # noqa: BLE001
    LS = chuan_ls(LS)
    for k, fn in (('MAY-19', lambda: may19(E, TL, LS, ep_dir, cong)), ('BAN-DO-12', lambda: ban_do_12(E, TL, LS, cong)), ('TU-LIEU-10', lambda: tu_lieu_10(E, TL, LS, cong)),
                  ('AI-TU-LIEU', lambda: ai_tu_lieu(E, LS, ep_dir, cong)), ('GEMINI-NGAN-SACH', lambda: gemini_ngan_sach(E, ep_dir, cong)),
                  ('GOC-CAO-60', lambda: goc_cao_60(E, TL, LS, ep_dir, cong))):
        try: out[k] = fn()
        except Exception as e: out[k] = r(thieu=[f'không chạy được: {type(e).__name__}: {e}'], val='—', cong=cong)   # noqa: BLE001
    from checks.ll import q_k1176 as K76   # 1.17.6 (chủ dự án 24/10 12:52): TU-LIEU-10 theo trần của tập + (b) mỗi lần ≤ 10 s; TU-LIEU-OMNI mới
    out.update(K76.check_tu_lieu(E, TL, ep_dir, LS))
    from checks.ll import q_k1177 as K77   # 1.17.7 (chủ dự án 25/10 09:15): GOC-CAO thay GOC-CAO-60; TU-LIEU-THAT, NHAN-VAT-TEN, KIEM-2-MUC mới
    out.pop('GOC-CAO-60', None); out.update(K77.check(E, TL, ep_dir, LS, video))
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    from checks.ll import base
    E = base.load(a[0]); ep = os.path.dirname(os.path.abspath(a[0])); LS = K6.log_shot(E, ep, a[a.index('--log-shot') + 1] if '--log-shot' in a else None)[0]
    TL = json.load(open(a[a.index('--tl') + 1])) if '--tl' in a else None
    for k, v in check(E, TL, ep, LS).items():
        print(k, v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT'), '·', v['val']); [print('   ', x) for x in (v['loi'] + (v.get('thieu') or []))[:20]]
