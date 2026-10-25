#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · việc 7 — GHÉP HÌNH animatic v3 640×360 24 fps theo BANG-SHOT-v3.json (dựng trên ghep.py của ANIMATIC-T4: dùng lại các hàm chiếu/lớp chồng/thẻ).
Khác v1: nguồn 3D $ANIM_R=/var/tmp/anim/r3 (tệp máy animatic2/may); M-d = clip v1 giữ (cột md_clip) hoặc clip v3 đã chọn (animatic2/omni/chon); shot TL = ảnh/tư liệu thật
TOÀN KHUNG (chuyển động máy 2D chậm — không AI chạm: chỉ đặt, mờ nền, chuyển động) hoặc footage thật (cắt 16:9, thu 640×360); chú thích ≤ 6 từ. Thẻ nhân vật có chân dung (P6) và
bộ đếm neo theo MỐC CÂU lời dựng v3 (animatic/loi-dung-moc-v3.json) thay vì giây gõ tay. M00 → M01 hoà 1 s (mở lạnh P1 = A). Tranh khắc góc khung theo 12:52 (YCBA → H1-08b, Luyken → H1-16,
Hollar phía Đông → H1-12x, Hollar sau cháy → H1-18 toàn khung).
  ghep_v3.py [--tu 0 --den 780] [--nhap] [--ra <tệp>]"""
import argparse, json, os, subprocess, sys
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('ANIM_R', '/var/tmp/anim/r3')
import ghep as GH  # noqa: E402
REPO = GH.REPO; EP = GH.EP; AN = EP / 'animatic'; AN2 = EP / 'animatic2'; W, H, FPS = GH.W, GH.H, GH.FPS
GH.LUTD = Path('/var/tmp/anim/lut3'); GH.MDF = Path('/var/tmp/anim/mdf3')
TLX = Path('/var/tmp/anim/tlx'); TLX.mkdir(parents=True, exist_ok=True)
for d in (EP / 'tu-lieu', EP / 'nc/anh', AN2 / 'tu-lieu'):
    for f in (d.glob('*.jpg') if d.exists() else []):
        if not (TLX / f.name).exists(): os.symlink(f, TLX / f.name)
GH.TL_DIR = TLX
OUT = Path(os.environ.get('ANIM_OUT', '/var/tmp/anim/out3'))
# tranh khắc / tư liệu góc khung: mã → (ảnh, chú thích ≤ 6 từ, bắt đầu s trong shot, dài s, kiểu)
KHAC = {'H1-03': ('met-360649-1', 'Hollar: London before the Fire (pub. 1666)', 1.0, 6.0, 'dai'),
        'H1-08b': ('ycba-40597-0', 'The Great Fire, period print', 4.0, 5.0, 'goc'),
        'H1-12x': ('met-395057-0', "Hollar: Old St Paul's from the east", 1.0, 5.0, 'goc'),
        'H1-16': ('rijks-luyken-0', 'Luyken: the Great Fire, 1698', 1.0, 4.0, 'goc'),
        'H2-02': ('loc-wren-plan-0', "Wren's 1666 plan, engraved 1767", 0.2, 8.0, 'goc'),
        'H2-06': ('rijks-monument-0', 'The Monument, engraving', 1.5, 3.0, 'goc'),
        'H2-12': ('met-360649-1', 'Hollar: London before the Fire (pub. 1666)', 0.5, 3.0, 'dai'),
        'H3-03': ('wellcome-uv3mugch-embankment-1865', 'Embankment works, 1865 drawing', 5.5, 3.0, 'goc')}
# bộ đếm: (shot, đầu câu neo, + giây, dài, số, chữ)
DEM_NEO = [('H1-18a', 'About thirteen thousand', 0.2, 2.2, '13,200', 'houses'), ('H1-18a', 'Eighty-seven parish', 0.1, 2.0, '87', 'churches'),
           ('H2-06', 'Two hundred and two feet', 0.2, 2.5, '202 ft', ''), ('H2-10', 'In 1711, Parliament', 3.0, 2.5, '365 ft', ''),
           ('H4-02', 'As dusk falls', 3.0, 3.0, '100,000', 'incendiaries'), ('H4-06', 'About a hundred and sixty', 0.2, 2.5, '160', 'killed')]
TEN_NEO = {'Thomas Farriner': 'Thomas Farriner', 'Samuel Pepys': 'Samuel Pepys hurries', 'Sir Thomas Bludworth': 'The Lord Mayor', 'John Evelyn': 'Monday.', 'John Evelyn · Christopher Wren': 'Six days before',
           'Christopher Wren': 'Within days', 'Charles II': 'Within days', 'Robert Hooke': 'Robert Hooke', 'Nicholas Barbon': 'In 1680', 'Godfrey Allen': 'In 1937',
           'Joseph Bazalgette': 'Between 1864', 'Charles Holden · William Holford': 'In 1946'}
VAI = {'Thomas Farriner': 'baker to the King', 'Samuel Pepys': 'diarist, Navy Office', 'Sir Thomas Bludworth': 'Lord Mayor of London', 'John Evelyn': 'diarist', 'John Evelyn · Christopher Wren': 'surveyors, August 1666',
       'Christopher Wren': 'architect', 'Charles II': 'King of England', 'Robert Hooke': 'City surveyor', 'Nicholas Barbon': 'founder, Fire Office', 'Godfrey Allen': "St Paul's surveyor",
       'Joseph Bazalgette': 'engineer', 'Charles Holden · William Holford': 'planners, 1946–47'}
MD_NGAY = dict(GH.MD_NGAY); MD_NGAY.update({5: '4 SEPT 1666', 12: '1711', 20: '2 SEPT 1666', 21: '2 SEPT 1666', 22: '2 SEPT 1666', 23: '2 SEPT 1666', 24: '2 SEPT 1666', 25: '3 SEPT 1666', 26: '4 SEPT 1666',
               27: '5 SEPT 1666', 28: '4 SEPT 1666', 29: '5 SEPT 1666', 30: 'SEPT 1666', 31: 'SEPT 1666', 32: '1675', 33: '1675', 34: 'OCT 1708', 35: '1937', 36: '1647', 37: '29 DEC 1940', 38: '29 DEC 1940', 39: '1946'})


def ten_goc(n): return n.split(' (')[0]


def lich(B, M):
    """→ THE [(t0, dài, tên, vai, ảnh)], DEM [(t0, dài, số, chữ)] theo mốc câu v3."""
    rows = {r['ma']: r for r in B['shot']}; cau = M['cau']
    def neo(ma, dau):
        r = rows[ma]; cs = [c for c in cau if c['nhom'] == r['nhom_loi'] and c['khoa'].startswith(dau)]
        return cs[0]['bd'] if cs else None
    THE = []
    for r in B['shot']:
        names = r['them'].get('the') or []; anh = r['them'].get('the_anh') or {}; tcur = None
        for n in names:
            nn = ten_goc(n); t = neo(r['ma'], TEN_NEO.get(nn, '###')) if nn in TEN_NEO else None
            t = max(t if t is not None else r['t0'] + 0.6, r['t0'] + 0.3) if tcur is None else tcur
            d = 3.5 if len(names) > 1 else 4.0; THE.append((round(t + 0.3, 3), d, nn, VAI.get(nn, ''), anh.get(n) or anh.get(nn))); tcur = t + 0.3 + d + 0.2
    DEM = []
    for ma, dau, dt, d, so, chu in DEM_NEO:
        t = neo(ma, dau)
        if t is not None: DEM.append((round(t + dt, 3), d, so, chu))
    return THE, DEM


def md_frames(r, n):
    ch = AN2 / 'omni/chon' / f"{r['ma']}.txt"; tag = ch.read_text().strip() if ch.exists() else r.get('md_clip')
    if not tag: return None, None
    clip = next((p for p in (AN2 / 'omni/clip' / f'{tag}.mp4', AN / 'omni/clip' / f'{tag}.mp4') if p.exists()), None)
    if clip is None: return None, None
    d = GH.MDF / f"{r['ma']}-{tag}"
    if not (d / 'xong').exists():
        d.mkdir(parents=True, exist_ok=True); dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(clip)], capture_output=True, text=True).stdout)
        k = max(1.0, n / FPS / dur)
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(clip), '-vf', f'setpts={k:.5f}*PTS,fps={FPS},scale={W}:{H}:flags=lanczos', '-q:v', '2', '-start_number', '0', str(d / '%05d.jpg')], check=True)
        (d / 'keo.txt').write_text(f'{k:.4f}'); (d / 'xong').write_text('1')
    return sorted(d.glob('[0-9]*.jpg')), {'tag': tag, 'clip': str(clip.relative_to(REPO)), 'keo_dai': float((d / 'keo.txt').read_text()), 'v1': not ch.exists()}


def ease(u): u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)


def tl_frame(r, t, cache):
    """ảnh thật / tư liệu toàn khung: nền = cùng ảnh phủ kín, mờ + tối; tiền cảnh = ảnh vừa khung (contain) × zoom, tâm trượt chậm (Ken Burns); không chỉnh nội dung ảnh."""
    key = r['tl_anh']; kb = r['them']['kb']
    if kb.get('video'):
        fs = cache.get(key)
        if fs is None:
            d = Path('/var/tmp/anim/tlv') / key; src = AN2 / 'tu-lieu' / f'{key}.mp4'
            if not (d / 'xong').exists():
                d.mkdir(parents=True, exist_ok=True); st = float(kb.get('bat_dau', 0))
                subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-ss', f'{st:.3f}', '-i', str(src), '-t', f"{r['dur'] + 0.5:.3f}", '-vf', f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}',
                                '-q:v', '2', '-start_number', '0', str(d / '%05d.jpg')], check=True); (d / 'xong').write_text('1')
            fs = cache[key] = sorted(d.glob('[0-9]*.jpg'))
        return cv2.imread(str(fs[min(int(t * FPS), len(fs) - 1)]))
    im = cache.get(key)
    if im is None: im = cache[key] = cv2.imread(str(TLX / f'{key}.jpg'))
    ih, iw = im.shape[:2]; u = ease(t / max(r['dur'], 1e-3)); a, b = np.array(kb['tu'], float), np.array(kb['den'], float); cx, cy, z = a + (b - a) * u
    sc_cov = max(W / iw, H / ih); bg = cv2.resize(im, (int(iw * sc_cov) + 2, int(ih * sc_cov) + 2), interpolation=cv2.INTER_AREA)
    bg = bg[(bg.shape[0] - H) // 2:(bg.shape[0] - H) // 2 + H, (bg.shape[1] - W) // 2:(bg.shape[1] - W) // 2 + W]; bg = (cv2.GaussianBlur(bg, (0, 0), 14) * 0.35).astype(np.uint8)
    sc = min(W / iw, H / ih) * z; fw, fh = iw * sc, ih * sc
    M = np.float32([[sc, 0, W / 2 - cx * fw], [0, sc, H / 2 - cy * fh]])   # điểm (cx, cy) của ảnh về tâm khung
    fg = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    mk = cv2.warpAffine(np.full((ih, iw), 255, np.uint8), M, (W, H), flags=cv2.INTER_NEAREST) > 0
    o = bg.copy(); o[mk] = fg[mk]; return o


def nhan_nam(r, lf, t):
    th = r['them']
    if th.get('nhan'): return th['nhan']
    if r['cu_may'] == 'TL': return th.get('nam_nhan')
    if r['cu_may'] == 'MD': return MD_NGAY.get(r.get('md_moc'))
    return GH.nhan_nam(r, lf, t)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--tu', type=float, default=0); ap.add_argument('--den', type=float, default=1e9); ap.add_argument('--nhap', action='store_true'); ap.add_argument('--ra')
    a = ap.parse_args(); B = json.loads((EP / 'BANG-SHOT-v3.json').read_text()); rows = B['shot']; T = B['tong']['thoi_luong_s']; N = int(round(T * FPS))
    M = json.loads((AN / 'loi-dung-moc-v3.json').read_text()); THE, DEM = lich(B, M)
    PP = json.loads((AN / 'the-phuong-phap.json').read_text()) if (AN / 'the-phuong-phap.json').exists() else None
    OUT.mkdir(parents=True, exist_ok=True); ra = Path(a.ra) if a.ra else OUT / 'hinh.mp4'
    f0, f1 = int(round(a.tu * FPS)), min(N, int(round(a.den * FPS)))
    ff = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', str(ra)], stdin=subprocess.PIPE)
    logg = {'shot': [], 'thieu': [], 'the': THE, 'dem': DEM, 'khac': KHAC}; cache = {}; last3d = None; prev = np.zeros((H, W, 3), np.uint8)
    ch_t0 = {}
    for r in rows:
        if r['phan'] in GH.CHUONG and r['phan'] not in ch_t0: ch_t0[r['phan']] = r['t0'] + 0.5
    hoa = {}   # hoà ra 1 s giữa hai shot 3D: khung cuối/đầu đóng băng dưới lớp mờ (M00 → M01)
    for i, r in enumerate(rows):
        if r['them'].get('hoa_ra') and i + 1 < len(rows): hoa[r['ma']] = (rows[i + 1]['ma'], r['them']['hoa_ra'])
    for k_, r in enumerate(rows):
        s0, s1 = int(round(r['t0'] * FPS)), int(round(r['t1'] * FPS)); n = s1 - s0
        if s1 <= f0 or s0 >= f1: continue
        ma, cu, them = r['ma'], r['cu_may'], r['them']; info = {'ma': ma, 'f0': s0, 'f1': s1, 'nguon': cu}
        A3 = Bq = L3 = Lb = MD = TNf = None
        if cu == 'MD':
            MD, mi = md_frames(r, n); info.update(mi or {}); ref = GH.stats(last3d) if last3d is not None else None
        elif cu in ('PP', 'TL'): pass
        elif cu == 'KHOP': A3, L3 = GH.seq(ma + '-a'); Bq, Lb = GH.seq(ma + '-b')
        else: A3, L3 = GH.seq(ma)
        if them.get('tam_nen'):
            ch = AN2 / 'tam-nen/chon' / f'{ma}.txt'
            if ch.exists(): d = Path(ch.read_text().strip()); TNf = sorted((d / 'tl').glob('[0-9]*.jpg')); info['tam_nen'] = str(d)
        if cu == 'TL':
            p = AN2 / 'tu-lieu' / (r['tl_anh'] + ('.mp4' if them['kb'].get('video') else '.jpg'))
            miss = not (p.exists() or (TLX / f"{r['tl_anh']}.jpg").exists())
        else: miss = (cu == 'MD' and not MD) or (cu not in ('MD', 'PP', 'TL') and (not A3 or (cu == 'KHOP' and not Bq)))
        if them.get('tam_nen') and not TNf: info['tam_nen_thieu'] = True
        if miss:
            logg['thieu'].append(ma)
            if not a.nhap: ff.stdin.close(); sys.exit(f'THIẾU nguồn {ma}')
        nxt = None
        if ma in hoa and not miss: nb, nl = GH.seq(hoa[ma][0]); nxt = cv2.imread(str(nb[0])) if nb else None
        for i in range(max(0, f0 - s0), min(n, f1 - s0)):
            t = i / FPS; tt = r['t0'] + t; lf = None
            if miss:
                img = np.full((H, W, 3), 30, np.uint8); cv2.putText(img, f'{ma} ({cu}) - CHUA CO NGUON', (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
            elif cu == 'MD': img = GH.lab_match(GH.rd(MD[min(i, len(MD) - 1)]), ref, 0.7)
            elif cu == 'TL': img = tl_frame(r, t, cache)
            elif cu == 'PP': img = None
            elif cu == 'KHOP':
                cut = r['thoi_gian'][3]; ia = min(i, len(A3) - 1); ib = i - int(round((cut - 0.5) * FPS))
                if t < cut - 0.5: img = GH.rd(A3[ia]); lf = L3['frames'][ia]
                elif t > cut + 0.5 or ib >= 0 and ia >= len(A3) - 1: img = GH.rd(Bq[min(max(ib, 0), len(Bq) - 1)]); lf = Lb['frames'][min(max(ib, 0), len(Bq) - 1)]
                else: u = (t - (cut - 0.5)) / 1.0; img = cv2.addWeighted(GH.rd(A3[ia]), 1 - u, GH.rd(Bq[min(max(ib, 0), len(Bq) - 1)]), u, 0); lf = L3['frames'][ia]
            else:
                j = min(i, len(A3) - 1); img = GH.rd(A3[j]); lf = L3['frames'][min(j, len(L3['frames']) - 1)]
            if nxt is not None and t > r['dur'] - hoa[ma][1] / 2: u = (t - (r['dur'] - hoa[ma][1] / 2)) / hoa[ma][1]; img = cv2.addWeighted(img, 1 - u, nxt, u, 0)
            if k_ and rows[k_ - 1]['ma'] in hoa and t < hoa[rows[k_ - 1]['ma']][1] / 2 and 'hoa_vao' in cache and not miss:
                u = 0.5 + t / hoa[rows[k_ - 1]['ma']][1]; img = cv2.addWeighted(cache['hoa_vao'], 1 - u, img, u, 0)
            if TNf and them.get('tam_nen') and not miss:
                p0, p1 = them['tam_nen']
                if p0 - 1e-6 <= t <= p1 + 1e-6:
                    j = min(len(TNf) - 1, i - int(round(p0 * FPS))); pl = GH.rd(TNf[max(0, j)])
                    u = min(1.0, max(0.0, (p1 - t) / 2.0)) if (p0 == 0 and p1 < r['dur'] - 0.01) else (min(1.0, max(0.0, (t - p0) / 2.0)) if p0 > 0 else 1.0)
                    img = cv2.addWeighted(pl, u, img, 1 - u, 0)
            if not miss and them.get('ban_do') and lf is not None:
                bd = them['ban_do']; s = bd['s']
                if t < s:
                    hr = bd['h0'] + (bd['h1'] - bd['h0']) * min(1, t / (s - 1.0)); lf0 = L3['frames'][0]
                    mp = GH.warp_map(lf0, 1.0, None); mp = GH.fire_overlay(mp, lf0, hr)
                    for nm, e, nn in GH.NHAN_MAP:
                        q = GH.project(lf0, [(e, nn, 12)])[0]
                        if not np.isnan(q).any(): cv2.circle(mp, (int(q[0]), int(q[1])), 3, (255, 255, 255), -1, cv2.LINE_AA); mp = GH.text_box(mp, nm, (int(q[0]) + 6, int(q[1]) - 9), GH.F('m', 11), 1.0)
                    u = 1.0 if t < s - 1.0 else (s - t) / 1.0; img = cv2.addWeighted(mp, u, img, 1 - u, 0)
            if not miss and them.get('ban_do_chong') and lf is not None: img = GH.warp_map(lf, 0.5, img)
            if not miss and lf is not None and (them.get('ranh66') or (ma == 'H2-02' and t >= r['dur'] - 4.0)):
                en = json.loads((EP / 'mo-hinh/ranh-chay-1666-cuoi.json').read_text())['tps']['en']; img = GH.poly_overlay(img, lf, en, (40, 120, 255), 0.18)
            if not miss and lf is not None and ma == 'H4-07':
                en = json.loads((GH.LD / 'look2/ldn2.json').read_text())['blitz_1940']; img = GH.poly_overlay(img, lf, en, (40, 120, 255), 0.18)
            if not miss and lf is not None and ma == 'H3-05' and t >= 4.0:
                ring = [(532118 + 300 * np.cos(q), 181150 + 300 * np.sin(q)) for q in np.linspace(0, 2 * np.pi, 48)]; img = GH.poly_overlay(img, lf, ring, (230, 210, 150), 0.16, h=52.0, w=1)
            if cu == 'PP':
                c = PP['the'][0] if t < PP['the'][0]['giay'] else PP['the'][1]; img = GH.pp_card(prev if i == 0 else cache.get('ppbg', prev), c['dong'], c.get('tieu_de'))
                if i == 0: cache['ppbg'] = prev.copy()
            raw_img = img
            if cu == 'TL' and not miss: img = GH.text_box(img, them['chu'], (14, H - 34), GH.F('m', 13), min(1.0, t / 0.4, (r['dur'] - t) / 0.4))
            if ma in KHAC and not miss:
                key, cap_, st, dd, kind = KHAC[ma]; img = GH.corner(img, key, cap_, GH.fade(t, st, dd, 0.5), kind)
            for (t0_, d_, n1, n2, th) in THE:
                if t0_ - 0.5 <= tt <= t0_ + d_ + 0.5: img = GH.card(img, n1, n2, GH.fade(tt, t0_, d_, 0.3), 'the', th)
            for (t0_, d_, n1, n2) in DEM:
                if t0_ - 0.5 <= tt <= t0_ + d_ + 0.5: img = GH.card(img, n1, n2, GH.fade(tt, t0_, d_, 0.3), 'dem')
            for ph, t0_ in ch_t0.items():
                if t0_ - 0.5 <= tt <= t0_ + 3.5: y, ph_ = GH.CHUONG[ph]; img = GH.card(img, y, ph_, GH.fade(tt, t0_, 3.0, 0.6), 'chuong')
            if not miss:
                lab = nhan_nam(r, lf, t)
                if them.get('ban_do') and t < them['ban_do']['s']: hr = them['ban_do']['h0'] + (them['ban_do']['h1'] - them['ban_do']['h0']) * min(1, t / (them['ban_do']['s'] - 1.0)); lab = f"{2 + int(hr // 24)} SEPT 1666"
                img = GH.dem_nam(img, lab)
            ff.stdin.write(np.ascontiguousarray(img, np.uint8).tobytes()); prev = img
            if cu not in ('MD', 'PP', 'TL') and not miss: last3d = img
        if ma in hoa: cache['hoa_vao'] = raw_img.copy()   # khung cuối TRƯỚC lớp chữ (không mang nhãn năm sang shot sau)
        logg['shot'].append(info)
    ff.stdin.close(); ff.wait()
    (AN2 / 'ghep-log.json').write_text(json.dumps(logg, ensure_ascii=False, indent=1)); print('XONG', ra, 'thiếu:', logg['thieu'])


if __name__ == '__main__': main()
