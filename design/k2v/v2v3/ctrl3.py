#!/opt/cine/bin/python -I
"""NC-V2V3 · ĐIỀU KHIỂN cho Wan-VACE từ đầu ra dung3.js (CPU, không GPU) — một cửa sổ khung [s, s+n).
  ctrl3.py <thư mục dung3> <thư mục ra> --s 80 --n 81
Ra (PNG 1280×720, đánh số 00000… theo cửa sổ):
  depth/   ĐỘ SÂU: nghịch đảo khoảng cách (1/z, z từ chính renderer), chuẩn hoá MỘT LẦN cho cả cửa sổ (phân vị 1–99 % điểm không phải trời) → gần sáng, xa tối, trời 0
           (cùng quy ước bản đồ độ sâu tương đối mà VACE học; KHÔNG ước độ sâu bằng AI)
  canny/   CẠNH: Canny trên khung màu nguồn (mờ Gauss σ 1,5, ngưỡng 60/150) — chỉ cạnh cấu trúc, bớt răng cưa/vân thủ tục
  mask/    MẶT NẠ chế độ B: trắng = AI được vẽ = trời ∪ nước ∪ đất/thảm thực vật ∪ MÁI NHÀ PHỐ (lớp nhà ∩ mesh makeCity ∩ pháp tuyến thế giới lên ≥ 0,8);
           mọi vùng tàu/cờ/pin nổi/lửa/người/khác/công trình (nhà không phải mái phố) = đen, nới 2 px (AI không chạm viền vật)
  bdepth/, bcanny/  (JPG q95, để tải lên pod nhanh) khung điều khiển B: điểm ảnh NGUỒN ở vùng giữ (đen) + độ sâu / cạnh ở vùng vẽ
  alpha/   hệ số ghép sau cùng: 0 trên mọi vùng giữ (đúng điểm ảnh nguồn), tăng tuyến tính tới 1 trong 3 px phía vùng vẽ (viền mềm ≤ 3 px)
  ctrl3.json  dải độ sâu, % vùng vẽ mỗi khung, % mái."""
import argparse, json, math, os
import cv2, numpy as np

PAL = {'troi': (40, 80, 200), 'nuoc': (0, 170, 190), 'dat': (140, 105, 60), 'nha': (235, 235, 235)}
ZN, ZF = 1.0, 60000.0


def dec_depth(p):
    b = cv2.imread(p, cv2.IMREAD_COLOR)   # BGR
    v = b[..., 2].astype(np.float64) * 256 + b[..., 1]; sky = b[..., 0] > 127
    return ZN * np.exp(v / 65535 * math.log(ZF / ZN)), sky


def normals_up(z, fr):
    h, w = z.shape; ty = math.tan(math.radians(fr['fov']) / 2); tx = ty * fr['aspect']
    xs = ((np.arange(w) + 0.5) / w * 2 - 1)[None, :]; ys = (1 - (np.arange(h) + 0.5) / h * 2)[:, None]
    P = np.stack([xs * tx * z, ys * ty * z, -z], -1)
    dx = np.zeros_like(P); dy = np.zeros_like(P); dx[:, 1:-1] = (P[:, 2:] - P[:, :-2]) / 2; dy[1:-1] = (P[2:] - P[:-2]) / 2
    n = np.cross(dx, dy); n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
    n[n[..., 2] < 0] *= -1                                   # quay về phía máy (+z mắt)
    M = np.array(fr['mw']).reshape(4, 4).T[:3, :3]           # three.js: cột-chính
    return (n @ M.T)[..., 1]                                  # thành phần Y thế giới (lên)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('--s', type=int, default=80); ap.add_argument('--n', type=int, default=81)
    ap.add_argument('--f0', type=int, default=0, help='chỉ số khung đầu của thư mục dung3 (vd c1: 264)')
    ap.add_argument('--disp', default='', help='lo,hi cố định (chế độ C: cùng chuẩn hoá cho mọi cửa sổ, tránh nhảy độ sáng bản đồ độ sâu ở đường nối)')
    a = ap.parse_args(); mp = os.path.join(a.src, 'meta3.json'); meta = {r['f']: r for r in json.load(open(mp if os.path.exists(mp) else mp + '.part'))['frames']}
    for d in ('depth', 'canny', 'mask', 'bdepth', 'bcanny', 'alpha', 'src'): os.makedirs(os.path.join(a.out, d), exist_ok=True)
    F = [a.f0 + a.s + i for i in range(a.n)]; nm = lambda f, e: f'{f:05d}{e}'
    Z = [dec_depth(os.path.join(a.src, 'depth', nm(f, '.png'))) for f in F]
    disp = np.concatenate([(1 / z)[~s] for z, s in Z]); lo, hi = (np.percentile(disp, 1), np.percentile(disp, 99)) if not a.disp else map(float, a.disp.split(','))
    rows = []; K2 = np.ones((5, 5), np.uint8)
    for i, (f, (z, sky)) in enumerate(zip(F, Z)):
        rgb = cv2.imread(os.path.join(a.src, 'rgb', nm(f, '.jpg')), cv2.IMREAD_COLOR); h, w = rgb.shape[:2]
        dg = np.where(sky, 0, np.clip((1 / z - lo) / (hi - lo), 0, 1)); dimg = cv2.cvtColor((dg * 255 + 0.5).astype(np.uint8), cv2.COLOR_GRAY2BGR)
        e = cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY), (0, 0), 1.5), 60, 150); cimg = cv2.cvtColor(e, cv2.COLOR_GRAY2BGR)
        idm = cv2.cvtColor(cv2.imread(os.path.join(a.src, 'id', nm(f, '.png')), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        if idm.shape[:2] != (h, w): idm = cv2.resize(idm, (w, h), interpolation=cv2.INTER_NEAREST)
        cls = {k: np.all(idm == v, -1) for k, v in PAL.items()}
        pho = cv2.imread(os.path.join(a.src, 'pho', nm(f, '.png')), cv2.IMREAD_GRAYSCALE) > 127
        up = normals_up(z, meta[f]['depth']); mai = cls['nha'] & pho & (up >= 0.8) & ~sky
        mai = cv2.morphologyEx(mai.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0   # bỏ điểm lẻ (cạnh tường)
        allow = cls['troi'] | cls['nuoc'] | cls['dat'] | mai
        keep = cv2.dilate((~allow).astype(np.uint8), K2) > 0; allow = ~keep                      # nới vùng giữ 2 px
        dist = cv2.distanceTransform(allow.astype(np.uint8), cv2.DIST_L2, 3); alpha = np.clip(dist / 3.0, 0, 1)   # 0 trên vùng giữ, 1 sau 3 px
        m3 = allow[..., None]
        cv2.imwrite(os.path.join(a.out, 'src', nm(i, '.png')), rgb)
        cv2.imwrite(os.path.join(a.out, 'depth', nm(i, '.png')), dimg); cv2.imwrite(os.path.join(a.out, 'canny', nm(i, '.png')), cimg)
        cv2.imwrite(os.path.join(a.out, 'mask', nm(i, '.png')), (allow * 255).astype(np.uint8))
        J95 = [cv2.IMWRITE_JPEG_QUALITY, 95]; cv2.imwrite(os.path.join(a.out, 'bdepth', nm(i, '.jpg')), np.where(m3, dimg, rgb), J95); cv2.imwrite(os.path.join(a.out, 'bcanny', nm(i, '.jpg')), np.where(m3, cimg, rgb), J95)
        cv2.imwrite(os.path.join(a.out, 'alpha', nm(i, '.png')), (alpha * 255 + 0.5).astype(np.uint8))
        rows.append(dict(f=f, ve_pct=round(float(allow.mean() * 100), 2), mai_pct=round(float(mai.mean() * 100), 3), canh_pct=round(float((e > 0).mean() * 100), 2)))
    J = dict(src=a.src, s=a.s, n=a.n, f0=a.f0, disp_p1=lo, disp_p99=hi, z_gan_m=round(1 / hi, 1), z_xa_m=round(1 / lo, 1),
             ve_pct_tb=round(float(np.mean([r['ve_pct'] for r in rows])), 2), mai_pct_tb=round(float(np.mean([r['mai_pct'] for r in rows])), 3), frames=rows)
    json.dump(J, open(os.path.join(a.out, 'ctrl3.json'), 'w'), indent=1); print({k: v for k, v in J.items() if k != 'frames'})


if __name__ == '__main__': main()
