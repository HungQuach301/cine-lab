#!/opt/cine/bin/python
"""ANIMATIC-T4 · việc 4 + 8 — GHÉP HÌNH animatic 640×360 24 fps theo BANG-SHOT-v2.json (không AI ở bước này; AI chỉ đến từ clip/tấm đã qua cổng).
Nguồn từng shot: 3D (render_look.js, áp LUT kênh k2c-t3-kenh-v030.cube) · KHOP (hai nửa cùng máy, hoà 1 s) · tấm nền N2+ (tn.py tl, hoà 2 s với 3D) ·
M-d (clip Omni đã chọn, khớp màu Lab k = 0,7 về khung 3D kề, kéo dài ≤ 13 % nếu clip ngắn hơn shot) · PP (2 thẻ chữ).
Lớp chồng (§17, §19 b–c): bản đồ Doornick 1666 chiếu lên mặt đất CÙNG MÁY 3D (khung đầu H1-09; H5-03 phủ mờ) + lửa lan theo lưới giờ bén (luoi_chay, bậc 2×1, nội suy bậc 5);
ranh vùng cháy 1666 (Doornick, bậc 1) / vùng bom 1940 (ước lượng, bậc 5) chiếu theo máy từng khung (log.json); tranh khắc/tư liệu ở góc khung ≤ 1/3 với chú thích ≤ 6 từ (không AI, chỉ đặt/mờ);
thẻ nhân vật + bộ đếm theo mốc câu lời dựng; thẻ chương §13.3 (≤ 3 s, góc dưới trái, mờ dần); thẻ phương pháp. Ra: $ANIM_OUT/hinh.mp4 + channel-k2/k2c-t4-02/animatic/ghep-log.json.
  ghep.py [--tu 0 --den 730] [--nhap]   (--nhap: shot thiếu nguồn → tấm chờ có mã shot; mặc định dừng báo thiếu)"""
import shutil, argparse, json, math, os, subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; AN = EP / 'animatic'
R3 = Path(os.environ.get('ANIM_R', '/var/tmp/anim/r')); LUTD = Path('/var/tmp/anim/lut'); MDF = Path('/var/tmp/anim/mdf'); TN = Path('/var/tmp/anim/tn')
OUT = Path(os.environ.get('ANIM_OUT', '/var/tmp/anim/out')); LD = Path(os.environ.get('LDN_DATA', '/var/tmp/ldn'))
W, H, FPS = 640, 360, 24
LUT = REPO / 'channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube'
FD = '/usr/share/fonts/opentype/inter/'
def F(w, s): return ImageFont.truetype(FD + {'b': 'Inter-SemiBold.otf', 'r': 'Inter-Regular.otf', 'B': 'Inter-Bold.otf', 'm': 'Inter-Medium.otf'}[w], s)
TL_DIR = EP / 'tu-lieu'
CHUONG = {'HỒI 1': ('1666', 'The Great Fire'), 'HỒI 2': ('1666', 'Rebuilding on the old streets'), 'HỒI 3': ('1711', 'The dome rules the skyline'),
          'HỒI 4': ('1940', 'The second great fire'), 'HỒI 5': ('1946', 'Second rebuilding, same streets')}
# thẻ nhân vật (ten, vai, ảnh PD hoặc None) · bộ đếm (số, ≤ 2 từ) — mốc = giây trong phim (theo loi-dung-moc.json), dài = lớp THE của bảng
THE = [(57.5, 3.0, 'Thomas Farriner', 'baker to the King', None), (98.4, 3.0, 'Samuel Pepys', 'diarist, Navy Office', None), (109.1, 3.0, 'Sir Thomas Bludworth', 'Lord Mayor of London', None),
       (178.8, 4.0, 'John Evelyn', 'diarist', None), (287.6, 3.5, 'Christopher Wren', 'architect', 'nga-wren-0'), (298.4, 3.5, 'Robert Hooke', 'City surveyor', None),
       (374.2, 4.0, 'Nicholas Barbon', 'founder, Fire Office', None), (480.0, 4.0, 'Godfrey Allen', "St Paul's surveyor", None), (603.8, 4.0, 'Charles Holden · William Holford', 'planners, 1946–47', None)]
DEM = [(252.2, 2.0, '13,200', 'houses'), (255.1, 2.0, '87', 'churches'), (364.0, 2.5, '202 ft', ''), (396.9, 2.5, '365 ft', ''), (523.0, 3.0, '100,000', 'incendiaries'), (571.4, 2.5, '160', 'killed')]
KHAC = {'H1-03': ('met-360649-1', 'Hollar: London before the Fire (pub. 1666)', 1.0, 6.0, 'dai'), 'H1-13': ('ycba-266-0', 'The fire at Ludgate, c. 1670', 1.0, 4.0, 'goc'),
        'H2-06': ('rijks-monument-0', 'The Monument, engraving', 1.5, 3.0, 'goc'), 'H2-12': ('met-360649-1', 'Hollar: London before the Fire (pub. 1666)', 0.5, 3.0, 'dai'),
        'H2-02': ('loc-wren-plan-0', "Wren's 1666 plan, engraved 1767", 0.2, 8.0, 'goc')}
# Lệnh bổ sung 24/10/2026 12:55: met-360649-1 = tấm TRƯỚC cháy ("A TRUE AND EXACT PROSPECT … FROM S.T MARIE OVERS STEEPLE … BEFORE THE FIRE"); -0 = tấm SAU cháy — không dùng ở H1-03/H2-12.
NHAN_MAP = [('Pudding Lane', 532905, 180800), ('London Bridge', 532800, 180560), ('Royal Exchange', 532900, 181120)]


def mm(t): return f'{int(t // 60)}:{t % 60:04.1f}'


def ensure_lut(src, dst):
    if (dst / 'xong').exists() and (dst / 'xong').stat().st_mtime >= (src / 'log.json').stat().st_mtime: return   # shot dựng lại → làm lại đệm LUT
    shutil.rmtree(dst, ignore_errors=True)
    dst.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-start_number', '0', '-i', str(src / '%05d.jpg'), '-vf', f"lut3d=file='{LUT}':interp=tetrahedral", '-q:v', '2', '-start_number', '0', str(dst / '%05d.jpg')], check=True)
    (dst / 'xong').write_text('1')


def seq(ma):
    s = R3 / ma
    if not (s / 'log.json').exists(): return None, None
    d = LUTD / ma; ensure_lut(s, d); fs = sorted(d.glob('[0-9]*.jpg')); return fs, json.loads((s / 'log.json').read_text())


def rd(p): return cv2.imread(str(p))


def project(log_f, pts):
    """EN(h) → px theo ma trận máy của khung (log.json render_look: view/proj cột-chính)."""
    V = np.array(log_f['view']).reshape(4, 4).T; P = np.array(log_f['proj']).reshape(4, 4).T; out = []
    for e, n, h in pts:
        c = P @ V @ np.array([e - 532000, h, -(n - 180800), 1.0])
        out.append([(c[0] / c[3] + 1) / 2 * W, (1 - c[1] / c[3]) / 2 * H] if c[3] > 1e-3 else [np.nan, np.nan])
    return np.array(out, np.float32)


DOORNICK = None
def doornick():
    global DOORNICK
    if DOORNICK is None:
        K = json.loads((EP / 'mo-hinh/khop-doornick.json').read_text()); im = cv2.imread(str(LD / 'tu-lieu/rijks-doornick-0.jpg'))
        if im is None: im = cv2.imread(str(TL_DIR / 'rijks-doornick-0.jpg')); sc = im.shape[1] / K['anh']['co'][0]
        else: sc = im.shape[1] / K['anh']['co'][0]
        P = [(np.array(d['px']) * sc, d['en']) for d in K['diem'] if d.get('dung', True)]
        Hm, _ = cv2.findHomography(np.float32([p for p, _ in P]), np.float32([e for _, e in P]))   # px bản đồ → EN (mặt phẳng, xấp xỉ khớp affine/poly2 của khop_ban_do.py)
        DOORNICK = (im, Hm)
    return DOORNICK


def warp_map(frame_log, alpha=1.0, base=None, h=12.0):
    im, Hm = doornick(); hh, ww = im.shape[:2]
    cor = np.float32([[0, 0], [ww, 0], [ww, hh], [0, hh]]); en = cv2.perspectiveTransform(cor[None], Hm)[0]
    scr = project(frame_log, [(e, n, h) for e, n in en])
    if np.isnan(scr).any(): return base
    Hs = cv2.getPerspectiveTransform(cor, scr); out = cv2.warpPerspective(im, Hs, (W, H), flags=cv2.INTER_AREA, borderValue=(0, 0, 0))
    m = cv2.warpPerspective(np.full((hh, ww), 255, np.uint8), Hs, (W, H)) > 0
    if base is None: base = np.zeros((H, W, 3), np.uint8)
    o = base.copy(); o[m] = (alpha * out[m] + (1 - alpha) * base[m]).astype(np.uint8); return o


LC = None
def fire_overlay(img, frame_log, hour, h=12.0):
    global LC
    if LC is None:
        m = json.loads((LD / 'look2/ldn2.json').read_text())['luoi_chay']; g = np.fromfile(LD / 'look2/luoi_chay.f32', '<f4').reshape(m['nz'], m['nx']); LC = (m, g)
    m, g = LC; nx, nz = m['nx'], m['nz']
    burn = (g >= 0) & (g <= hour); front = burn & (g > hour - 3)
    rgba = np.zeros((nz, nx, 4), np.float32); rgba[burn] = (40, 70, 200, 0.42); rgba[front] = (40, 160, 255, 0.70)
    big = cv2.resize(rgba, (nx * 8, nz * 8), interpolation=cv2.INTER_LINEAR); big[..., 3] = cv2.GaussianBlur(big[..., 3], (0, 0), 3)
    cor = np.float32([[0, 0], [nx * 8, 0], [nx * 8, nz * 8], [0, nz * 8]]); en = [(m['E0'], m['N0']), (m['E0'] + nx * m['buoc'], m['N0']), (m['E0'] + nx * m['buoc'], m['N0'] - nz * m['buoc']), (m['E0'], m['N0'] - nz * m['buoc'])]
    scr = project(frame_log, [(e, n, h) for e, n in en])
    if np.isnan(scr).any(): return img
    Hs = cv2.getPerspectiveTransform(cor, scr); o = cv2.warpPerspective(big, Hs, (W, H))
    a = o[..., 3:4]; return np.clip(img * (1 - a) + o[..., :3] * a, 0, 255).astype(np.uint8)


def poly_overlay(img, frame_log, en, color=(60, 170, 255), fill=0.12, h=14.0, w=2):
    p = project(frame_log, [(e, n, h) for e, n in en])
    if np.isnan(p).any(): return img
    q = np.round(p).astype(np.int32); o = img.copy()
    if fill: f = img.copy(); cv2.fillPoly(f, [q], color); o = cv2.addWeighted(f, fill, img, 1 - fill, 0)
    cv2.polylines(o, [q], True, color, w, cv2.LINE_AA); return o


def lab_match(img, ref_stats, k=0.7):
    if ref_stats is None: return img
    l = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32); m, s = l.reshape(-1, 3).mean(0), l.reshape(-1, 3).std(0) + 1e-3; mr, sr = ref_stats
    return cv2.cvtColor(np.clip((l - m) * (1 + k * (sr / s - 1)) + m + k * (mr - m), 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def stats(img): l = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32).reshape(-1, 3); return l.mean(0), l.std(0)


def md_frames(ma, n):
    ch = AN / 'omni/chon' / f'{ma}.txt'
    if not ch.exists(): return None, None
    tag = ch.read_text().strip(); clip = Path('/var/tmp/anim/omni') / ma / f'{tag}.mp4'
    if not clip.exists(): clip = AN / 'omni/clip' / f'{tag}.mp4'
    d = MDF / tag
    if not (d / 'xong').exists():
        d.mkdir(parents=True, exist_ok=True); dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(clip)], capture_output=True, text=True).stdout)
        k = max(1.0, n / FPS / dur)
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(clip), '-vf', f'setpts={k:.5f}*PTS,fps={FPS},scale={W}:{H}:flags=lanczos', '-q:v', '2', '-start_number', '0', str(d / '%05d.jpg')], check=True)
        (d / 'keo.txt').write_text(f'{k:.4f}'); (d / 'xong').write_text('1')
    return sorted(d.glob('[0-9]*.jpg')), {'tag': tag, 'keo_dai': float((d / 'keo.txt').read_text())}


def corner(img, key, cap, a, kind):
    if a <= 0: return img
    src = cv2.imread(str(TL_DIR / f'{key}.jpg'))
    if kind == 'dai':   # dải ngang trên cùng (tranh toàn cảnh rất dài) — diện tích ≤ 1/3 khung
        hh = int(W * src.shape[0] / src.shape[1]); hh = min(hh, int(H * 0.26)); s = cv2.resize(src, (W - 20, hh), interpolation=cv2.INTER_AREA); x0, y0 = 10, H - hh - 34
    else:
        mx = (int(W * 0.33), int(H * 0.52)); r = min(mx[0] / src.shape[1], mx[1] / src.shape[0]); s = cv2.resize(src, (int(src.shape[1] * r), int(src.shape[0] * r)), interpolation=cv2.INTER_AREA)
        x0, y0 = W - s.shape[1] - 14, H - s.shape[0] - 34
    o = img.copy(); reg = o[y0:y0 + s.shape[0], x0:x0 + s.shape[1]]
    o[y0:y0 + s.shape[0], x0:x0 + s.shape[1]] = (a * s + (1 - a) * reg).astype(np.uint8)
    cv2.rectangle(o, (x0 - 1, y0 - 1), (x0 + s.shape[1], y0 + s.shape[0]), (235, 235, 235), 1)
    o = cv2.addWeighted(o, a, img, 1 - a, 0) if a < 1 else o
    return text_box(o, cap, (x0, y0 + s.shape[0] + 3), F('r', 11), a, right=(kind != 'dai'))


def text_box(img, txt, xy, font, a, right=False, pad=4):
    if not txt or a <= 0: return img
    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGBA'); ov = Image.new('RGBA', pil.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    bb = d.textbbox((0, 0), txt, font=font); tw, th = bb[2] - bb[0], bb[3] - bb[1]; x, y = xy
    if right: x = W - 14 - tw - 2 * pad
    d.rectangle((x, y, x + tw + 2 * pad, y + th + 2 * pad + 2), fill=(10, 10, 12, int(200 * a))); d.text((x + pad, y + pad - bb[1]), txt, font=font, fill=(240, 236, 228, int(255 * a)))
    return cv2.cvtColor(np.array(Image.alpha_composite(pil, ov).convert('RGB')), cv2.COLOR_RGB2BGR)


def card(img, l1, l2, a, kind='the', thumb=None):
    """thẻ góc dưới trái: 'chuong' = NĂM — cụm (§13.3) · 'the' = tên + vai (§17 (3)) · 'dem' = số lớn + ≤ 2 từ."""
    if a <= 0: return img
    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGBA'); ov = Image.new('RGBA', pil.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    A = lambda v: int(v * a)
    if kind == 'chuong':
        f1, f2 = F('B', 22), F('m', 17); t1 = l1; t2 = '— ' + l2; b1 = d.textbbox((0, 0), t1, font=f1); b2 = d.textbbox((0, 0), t2, font=f2)
        x, y = 22, H - 58; d.rectangle((x - 10, y - 8, x + b1[2] + 10 + b2[2] + 10, y + 34), fill=(8, 8, 10, A(170)))
        d.text((x, y - b1[1] + 2), t1, font=f1, fill=(255, 214, 140, A(255))); d.text((x + b1[2] + 10, y - b2[1] + 6), t2, font=f2, fill=(240, 236, 228, A(255)))
    elif kind == 'dem':
        f1, f2 = F('B', 30), F('m', 15); b1 = d.textbbox((0, 0), l1, font=f1); b2 = d.textbbox((0, 0), l2 or ' ', font=f2); x, y = 22, 22
        d.rectangle((x - 10, y - 8, x + max(b1[2], b2[2]) + 12, y + 46 + (18 if l2 else 0)), fill=(8, 8, 10, A(165)))
        d.text((x, y - b1[1]), l1, font=f1, fill=(255, 214, 140, A(255)))
        if l2: d.text((x, y + 40 - b2[1]), l2, font=f2, fill=(240, 236, 228, A(255)))
    else:
        f1, f2 = F('b', 18), F('r', 13); b1 = d.textbbox((0, 0), l1, font=f1); b2 = d.textbbox((0, 0), l2, font=f2); x, y = 22, H - 66; tx = x
        tw = max(b1[2], b2[2]); pw = 0
        if thumb is not None: pw = 44
        d.rectangle((x - 10, y - 8, x + pw + tw + 12, y + 46), fill=(8, 8, 10, A(170)))
        if thumb is not None:
            t = Image.open(TL_DIR / f'{thumb}.jpg').convert('RGB'); t.thumbnail((40, 52)); t = t.convert('RGBA'); t.putalpha(A(255)); ov.alpha_composite(t, (x, y - 4)); tx = x + pw
        d.text((tx, y - b1[1]), l1, font=f1, fill=(255, 255, 255, A(255))); d.text((tx, y + 25 - b2[1]), l2, font=f2, fill=(220, 214, 200, A(255)))
    return cv2.cvtColor(np.array(Image.alpha_composite(pil, ov).convert('RGB')), cv2.COLOR_RGB2BGR)


THANG = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
MD_NGAY = {1: '2 SEPT 1666', 2: '2 SEPT 1666', 3: '3 SEPT 1666', 4: '3 SEPT 1666', 5: '4 SEPT 1666', 7: '5 SEPT 1666', 8: 'SEPT 1666', 9: '2 SEPT 1666', 10: '1667', 11: '1668',
           12: '1711', 13: '1680', 14: '1930s', 15: '29 DEC 1940', 16: '29 DEC 1940', 17: '29 DEC 1940', 18: '2026', 19: '1667'}


def nhan_nam(r, lf, t):
    """bộ đếm năm (Kinh thánh §11.2: chữ chính, góc cố định, suốt tập): năm của khung (log máy) · ngày–tháng trong các ngày cháy 1666 (giờ kể từ 2/9) và 29–30/12/1940."""
    tg = r['thoi_gian']
    if r['cu_may'] == 'MD': return MD_NGAY.get(r.get('md_moc'))
    if r['cu_may'] == 'PP' or tg is None: return None
    if tg[0] == 'khop': tg = tg[1] if t < tg[3] else tg[2]
    if tg[0] == 'h66' or (lf is not None and lf.get('hour') is not None and lf.get('hour', -1) >= 0 and tg[0] == 'h66'):
        h = (lf.get('hour') if lf is not None and lf.get('hour') is not None else tg[1]); return f"{2 + int(h // 24)} SEPT 1666"
    if tg[0] == 'h40':
        h = lf.get('h40') if lf is not None and lf.get('h40') is not None else tg[1]; return f"{29 + int((18 + h) // 24)} DEC 1940"
    y = lf.get('year') if lf is not None and lf.get('year') is not None else tg[1] if tg[0] == 'y' else tg[1][0]
    return str(int(round(y)) if tg[0] == 'y' and abs(tg[2] - tg[1]) > 0.5 else int(y))


def dem_nam(img, txt):
    if not txt: return img
    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); d = ImageDraw.Draw(pil); f = F('B', 24 if len(txt) <= 6 else 19)
    w = d.textlength(txt, font=f); x, y = W - 18 - w, 14
    d.text((x + 1, y + 1), txt, font=f, fill=(0, 0, 0)); d.text((x, y), txt, font=f, fill=(250, 244, 232))
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)


def fade(t, t0, d, f=0.4): return 0.0 if t < t0 or t > t0 + d else min(1.0, (t - t0) / f, (t0 + d - t) / f)


def pp_card(bg, lines, title, a=1.0):
    img = cv2.GaussianBlur(bg, (0, 0), 6) * 0.25 if bg is not None else np.zeros((H, W, 3))
    pil = Image.fromarray(cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)); d = ImageDraw.Draw(pil); y = 70
    if title: d.text((60, y), title, font=F('B', 22), fill=(255, 214, 140)); y += 46
    f = F('r', 17)
    for ln in lines:
        words, cur = ln.split(), ''
        for w_ in words:
            if d.textlength(cur + ' ' + w_, font=f) > W - 120: d.text((60, y), cur.strip(), font=f, fill=(236, 232, 224)); y += 26; cur = w_
            else: cur += ' ' + w_
        d.text((60, y), cur.strip(), font=f, fill=(236, 232, 224)); y += 34
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--tu', type=float, default=0); ap.add_argument('--den', type=float, default=1e9); ap.add_argument('--nhap', action='store_true'); ap.add_argument('--ra')
    a = ap.parse_args(); B = json.loads((EP / 'BANG-SHOT-v2.json').read_text()); rows = B['shot']; T = B['tong']['thoi_luong_s']; N = int(round(T * FPS))
    PP = json.loads((AN / 'the-phuong-phap.json').read_text()) if (AN / 'the-phuong-phap.json').exists() else None
    OUT.mkdir(parents=True, exist_ok=True); ra = Path(a.ra) if a.ra else OUT / 'hinh.mp4'
    f0, f1 = int(round(a.tu * FPS)), min(N, int(round(a.den * FPS)))
    ff = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', str(ra)], stdin=subprocess.PIPE)
    logg = {'shot': [], 'thieu': []}; cache = {}; last3d = None; prev = np.zeros((H, W, 3), np.uint8)
    chuong_t0 = {}
    for r in rows:
        if r['phan'] in CHUONG and r['phan'] not in chuong_t0: chuong_t0[r['phan']] = r['t0'] + 0.5
    for r in rows:
        s0, s1 = int(round(r['t0'] * FPS)), int(round(r['t1'] * FPS)); n = s1 - s0
        if s1 <= f0 or s0 >= f1: continue
        ma, cu, them = r['ma'], r['cu_may'], r['them']; info = {'ma': ma, 'f0': s0, 'f1': s1, 'nguon': cu}
        # --- nguồn
        A3 = Bq = None; L3 = Lb = None; MD = None; TNf = None
        if cu == 'MD':
            MD, mi = md_frames(ma, n); info.update(mi or {})
            ref = stats(last3d) if last3d is not None else None
        elif cu == 'PP': pass
        elif cu == 'KHOP': A3, L3 = seq(ma + '-a'); Bq, Lb = seq(ma + '-b')
        else: A3, L3 = seq(ma)
        if them.get('tam_nen'):
            k = {'M01': 'P1-2026', 'H5-04': 'P1-2026', 'H5-05a': 'P9-2026', 'H5-06': 'P3-2026'}[ma]
            ch = AN / 'tam-nen/chon' / f'{ma}.txt'
            if ch.exists():
                d = Path(ch.read_text().strip()); TNf = sorted((d / 'tl').glob('[0-9]*.jpg')); info['tam_nen'] = str(d)
        miss = (cu == 'MD' and not MD) or (cu not in ('MD', 'PP') and (not A3 or (cu == 'KHOP' and not Bq)))
        if miss:
            logg['thieu'].append(ma)
            if not a.nhap: ff.stdin.close(); sys.exit(f'THIẾU nguồn {ma}')
        for i in range(max(0, f0 - s0), min(n, f1 - s0)):
            t = i / FPS; tt = r['t0'] + t; lf = None
            if miss:
                img = np.full((H, W, 3), 30, np.uint8); cv2.putText(img, f'{ma} ({cu}) - CHUA CO NGUON', (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
            elif cu == 'MD':
                img = rd(MD[min(i, len(MD) - 1)]); img = lab_match(img, ref, 0.7)
            elif cu == 'PP':
                img = None
            elif cu == 'KHOP':
                cut = r['thoi_gian'][3]; ia = min(i, len(A3) - 1); ib = i - int(round((cut - 0.5) * FPS))
                if t < cut - 0.5: img = rd(A3[ia]); lf = L3['frames'][ia]
                elif t > cut + 0.5 or ib >= 0 and ia >= len(A3) - 1: img = rd(Bq[min(max(ib, 0), len(Bq) - 1)]); lf = Lb['frames'][min(max(ib, 0), len(Bq) - 1)]
                else: u = (t - (cut - 0.5)) / 1.0; img = cv2.addWeighted(rd(A3[ia]), 1 - u, rd(Bq[min(max(ib, 0), len(Bq) - 1)]), u, 0); lf = L3['frames'][ia]
            else:
                j = min(i, len(A3) - 1); img = rd(A3[j]); lf = L3['frames'][min(j, len(L3['frames']) - 1)]
            # tấm nền: khoảng [p0, p1] trong shot; hoà 2 s ở phía tiếp giáp 3D
            if TNf and them.get('tam_nen') and not miss:
                p0, p1 = them['tam_nen']
                if p0 - 1e-6 <= t <= p1 + 1e-6:
                    j = min(len(TNf) - 1, i - int(round(p0 * FPS))); pl = rd(TNf[max(0, j)])
                    if p0 == 0 and p1 < r['dur'] - 0.01: u = min(1.0, max(0.0, (p1 - t) / 2.0))     # hoà ra 3D ở 2 s cuối khoảng
                    elif p0 > 0: u = min(1.0, max(0.0, (t - p0) / 2.0))                              # hoà vào từ 3D ở 2 s đầu
                    else: u = 1.0
                    img = cv2.addWeighted(pl, u, img, 1 - u, 0)
            # bản đồ cổ (MAP) + lửa theo ngày + nhãn ≤ 3 tên
            if not miss and them.get('ban_do') and lf is not None:
                bd = them['ban_do']; s = bd['s']
                if t < s:
                    hr = bd['h0'] + (bd['h1'] - bd['h0']) * min(1, t / (s - 1.0)); lf0 = L3['frames'][0]
                    mp = warp_map(lf0, 1.0, None); mp = fire_overlay(mp, lf0, hr)
                    for nm, e, nn in NHAN_MAP:
                        q = project(lf0, [(e, nn, 12)])[0]
                        if not np.isnan(q).any(): cv2.circle(mp, (int(q[0]), int(q[1])), 3, (255, 255, 255), -1, cv2.LINE_AA); mp = text_box(mp, nm, (int(q[0]) + 6, int(q[1]) - 9), F('m', 11), 1.0)
                    u = 1.0 if t < s - 1.0 else (s - t) / 1.0; img = cv2.addWeighted(mp, u, img, 1 - u, 0)
            if not miss and them.get('ban_do_chong') and lf is not None: img = warp_map(lf, 0.5, img)
            if not miss and lf is not None and ma in ('H1-18', 'H2-02') and (ma == 'H1-18' and 257.0 <= tt <= 262.4 or ma == 'H2-02' and t >= r['dur'] - 4.0):
                en = json.loads((EP / 'mo-hinh/ranh-chay-1666-cuoi.json').read_text())['tps']['en']; img = poly_overlay(img, lf, en, (40, 120, 255), 0.18)
            if not miss and lf is not None and ma == 'H4-07':
                en = json.loads((LD / 'look2/ldn2.json').read_text())['blitz_1940']; img = poly_overlay(img, lf, en, (40, 120, 255), 0.18)
            if not miss and lf is not None and ma == 'H3-05' and t >= 4.0:   # St Paul's Heights: mặt phẳng trần cao độ (minh hoạ, vành 300 m quanh mái vòm ở cao độ ≈ 52 m)
                ring = [(532118 + 300 * math.cos(q), 181150 + 300 * math.sin(q)) for q in np.linspace(0, 2 * math.pi, 48)]; img = poly_overlay(img, lf, ring, (230, 210, 150), 0.16, h=52.0, w=1)
            if cu == 'PP':
                if PP is None: img = np.full((H, W, 3), 12, np.uint8)
                else:
                    c = PP['the'][0] if t < PP['the'][0]['giay'] else PP['the'][1]; img = pp_card(prev if i == 0 else cache.get('ppbg', prev), c['dong'], c.get('tieu_de'))
                if i == 0: cache['ppbg'] = prev.copy()
            # chồng tư liệu / tranh khắc ở góc khung
            if ma in KHAC and not miss:
                key, cap, st, dd, kind = KHAC[ma]; img = corner(img, key, cap, fade(t, st, dd, 0.5), kind)
            for (t0_, d_, n1, n2, th) in THE:
                if t0_ - 0.5 <= tt <= t0_ + d_ + 0.5: img = card(img, n1, n2, fade(tt, t0_, d_, 0.3), 'the', th)
            for (t0_, d_, n1, n2) in DEM:
                if t0_ - 0.5 <= tt <= t0_ + d_ + 0.5: img = card(img, n1, n2, fade(tt, t0_, d_, 0.3), 'dem')
            for ph, t0_ in chuong_t0.items():
                if t0_ - 0.5 <= tt <= t0_ + 3.5: y, ph_ = CHUONG[ph]; img = card(img, y, ph_, fade(tt, t0_, 3.0, 0.6), 'chuong')
            if not miss:
                lab = nhan_nam(r, lf, t)
                if them.get('ban_do') and t < them['ban_do']['s']: hr = them['ban_do']['h0'] + (them['ban_do']['h1'] - them['ban_do']['h0']) * min(1, t / (them['ban_do']['s'] - 1.0)); lab = f"{2 + int(hr // 24)} SEPT 1666"
                img = dem_nam(img, lab)
            ff.stdin.write(np.ascontiguousarray(img, np.uint8).tobytes()); prev = img
            if cu not in ('MD', 'PP') and not miss: last3d = img
        logg['shot'].append(info)
    ff.stdin.close(); ff.wait()
    (AN / 'ghep-log.json').write_text(json.dumps(logg, ensure_ascii=False, indent=1)); print('XONG', ra, 'thiếu:', logg['thieu'])


if __name__ == '__main__': main()
