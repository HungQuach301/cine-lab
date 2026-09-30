"""Cổng 7 THỬ MẶT — đo da mặt trong mặt nạ (frames.js --mask) và ghép ảnh trước/sau.
  do <thư mục> <shot>                     : bảng số đo từng khung dải + trung bình (JSON ra stdout)
  ghep <trước> <sau> <shot> <khung> <ra.jpg> : ảnh trước | sau cả khung (hàng trên) + cận mặt phóng to (hàng dưới)
  lech <a.png> <b.png>                    : số điểm ảnh khác nhau (kiểm 0 px)
Số đo (trong mặt nạ da mặt nhìn thấy, sRGB 8 bit sau toàn bộ đường ống):
  chay_pct   : % điểm ảnh có kênh ≥ 250 (cháy)       trang_pct: % điểm ảnh cả ba kênh ≥ 235 (trắng bệch)
  L_tb, L_p5, L_p95 : độ sáng CIE L*                  tuongphan: L_p95 − L_p5 (độ trải sáng–tối trên mặt, đơn vị L*)
  a_tb, b_tb, C_tb  : sắc CIELAB trung bình (a đỏ, b vàng, C = độ bão hoà)   C_sd: độ lệch chuẩn C (biến thiên màu da)
"""
import glob, json, os, sys
import numpy as np
from PIL import Image, ImageDraw


def lab(rgb):
    c = rgb / 255.0; c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[:, 1] - 16, 500 * (f[:, 0] - f[:, 1]), 200 * (f[:, 1] - f[:, 2])], 1)


def do_frame(png, mpng):
    im = np.asarray(Image.open(png).convert('RGB')).astype(float); m = np.asarray(Image.open(mpng).convert('L')) > 127
    # co mặt nạ 1 px (mép khử răng cưa trộn nền)
    m2 = m.copy(); m2[1:, :] &= m[:-1, :]; m2[:-1, :] &= m[1:, :]; m2[:, 1:] &= m[:, :-1]; m2[:, :-1] &= m[:, 1:]
    p = im[m2]; n = len(p)
    if n < 50: return {'px': int(n)}
    L = lab(p); C = np.hypot(L[:, 1], L[:, 2])
    return {'px': int(n), 'chay_pct': round(100 * float((p >= 250).any(1).mean()), 2), 'trang_pct': round(100 * float((p >= 235).all(1).mean()), 2),
            'L_tb': round(float(L[:, 0].mean()), 1), 'L_p5': round(float(np.percentile(L[:, 0], 5)), 1), 'L_p95': round(float(np.percentile(L[:, 0], 95)), 1),
            'tuongphan': round(float(np.percentile(L[:, 0], 95) - np.percentile(L[:, 0], 5)), 1),
            'a_tb': round(float(L[:, 1].mean()), 1), 'b_tb': round(float(L[:, 2].mean()), 1), 'C_tb': round(float(C.mean()), 1), 'C_sd': round(float(C.std()), 2)}


def do(d, shot):
    rows = {}
    for png in sorted(glob.glob(f'{d}/{shot}_f*.png')):
        if png.endswith('_mask.png'): continue
        f = int(png.rsplit('_f', 1)[1][:-4]); rows[f] = do_frame(png, png[:-4] + '_mask.png')
    keys = [k for k in next(iter(rows.values())).keys() if k != 'px']
    ok = [r for r in rows.values() if 'L_tb' in r]
    tb = {k: round(float(np.mean([r[k] for r in ok])), 2) for k in keys} if ok else {}
    return {'shot': shot, 'khung': rows, 'trung_binh': tb}


def bbox(mpng, pad=0.35):
    m = np.asarray(Image.open(mpng).convert('L')) > 127; ys, xs = np.nonzero(m)
    if len(xs) < 20: return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); w, h = x1 - x0, y1 - y0; s = max(w, h) * (1 + 2 * pad); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return (int(cx - s / 2), int(cy - s / 2), int(cx + s / 2), int(cy + s / 2))


def ghep(a_dir, b_dir, shot, f, out, la='hiện hành', lb='biến thể'):
    A = Image.open(f'{a_dir}/{shot}_f{f}.png').convert('RGB'); B = Image.open(f'{b_dir}/{shot}_f{f}.png').convert('RGB')
    bb = bbox(f'{a_dir}/{shot}_f{f}_mask.png') or (0, 0, A.width, A.height)
    Z = 540
    ca, cb = A.crop(bb).resize((Z, Z), Image.LANCZOS), B.crop(bb).resize((Z, Z), Image.LANCZOS)
    o = Image.new('RGB', (1920 + 6, 540 + 6 + Z), (20, 20, 20)); o.paste(A, (0, 0)); o.paste(B, (966, 0))
    o.paste(ca, (960 - Z, 546)); o.paste(cb, (966, 546)); d = ImageDraw.Draw(o)
    from PIL import ImageFont; fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    for x, t in ((4, la), (970, lb)): d.rectangle([x, 4, x + 9 * len(t) + 14, 26], fill=(0, 0, 0)); d.text((x + 5, 6), t, fill=(255, 255, 255), font=fnt)
    o.save(out, quality=90); print(out)


def lech(a, b):
    A = np.asarray(Image.open(a).convert('RGB')).astype(int); B = np.asarray(Image.open(b).convert('RGB')).astype(int)
    print(json.dumps({'px_khac': int((A != B).any(2).sum()), 'max': int(abs(A - B).max())}))


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'do': print(json.dumps(do(sys.argv[2], sys.argv[3]), ensure_ascii=False))
    elif c == 'ghep': ghep(*sys.argv[2:7])
    elif c == 'lech': lech(*sys.argv[2:4])
    elif c == 'bang':   # bang <trước> <sau> <ra.json>: trung bình từng shot; s03 tính riêng các khung SAU khi L4 bắt lửa (khung ≥ 228)
        R = {}
        for s in ('s03', 's05', 's22'):
            for nh, d in (('truoc', sys.argv[2]), ('sau', sys.argv[3])):
                j = do(d, s); ok = [v for f, v in j['khung'].items() if 'L_tb' in v and (s != 's03' or int(f) >= 228)]
                R[f'{s}/{nh}'] = {k: round(float(np.mean([r[k] for r in ok])), 2) for k in ok[0] if k != 'px'}; R[f'{s}/{nh}']['khung'] = len(ok)
                print(s, nh, R[f'{s}/{nh}'])
        json.dump(R, open(sys.argv[4], 'w'), ensure_ascii=False, indent=1)
