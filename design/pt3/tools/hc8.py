"""PT3 · HC8 — TẤM CHIẾU cho cảnh điểm nhấn (King's Bastion): 3 tấm C = khung A dựng từ góc máy chính (phương vị 245°/270°/295°,
tức ±25° quanh giữa cung orbit), sửa ảnh AI CHỈ trong mặt nạ bastion (ánh sáng nướng sẵn trong tấm — đúng cho mặt trời tĩnh của cú máy),
rồi CHIẾU NGƯỢC lên hình học từng khung orbit (camera projection): điểm bề mặt P (lượt vị trí của khung) → toạ độ ảnh trong tấm k;
nhìn thấy nếu lượt vị trí của tấm k tại đó trùng P (≤ 0,12 m + 0,2 %·khoảng cách); hoà các tấm theo góc nhìn: w_k = exp(−(θ_k/12°)²),
θ_k = góc giữa tia khung hiện tại và tia tấm k tới P. Điểm không tấm nào thấy = "LỘ" (giữ A). Kéo giãn = phóng đại texel của tấm (định thức Jacobi).
  hc8.py prep <thư mục projA> <ra ai_in/hc8>          (ảnh vào 2048×1152 + mặt nạ bid 8000)
  hc8.py comp <projA> <ảnh C đã ghép> <kbA> <ra kbHC8> <đo.json>"""
import sys, os, json, math, glob
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'scene'))
import exr, cams as CM
ST = CM.SITE['kb']; AZ = ST['proj_az']; MM = ST['mm']

PROMPT2 = ("TEXTURE-ONLY EDIT. The output must overlay the input pixel for pixel: same framing, same zoom, same outline of every wall, the parapet on top of the "
           "walls with its notches (embrasures) and the low stone wall blocks along the sea front stay exactly where they are. Change only the surface material inside the "
           "masked area. ")
PROMPT = ("Edit only the transparent (masked) area of this image: the stone surfaces of King's Bastion, an 18th-century artillery bastion in Gibraltar, "
          "as it stood in 1782 — the masonry scarp walls, the stone cordon, the parapet and the earth gun platform. Make these surfaces photographically "
          "realistic: weathered limestone ashlar with fine mortar joints, colour variation between blocks, salt and water staining, darker damp and algae "
          "just above the water line; compacted earth and gravel on the platform. Keep EXACTLY the same geometry, outline, framing, camera, perspective, "
          "sun direction, shadows, light and colour grading; every edge stays where it is. Do not add or remove anything: no people, no flags, no cannons, "
          "no carts, no boats, no buildings, no openings, no signs, letters or numbers. Photorealistic.")

def prep(DP, OUT):
    os.makedirs(OUT, exist_ok=True); chunks = []
    for az in AZ:
        tag = f'proj{int(az):03d}'; im = Image.open(os.path.join(DP, tag + '.png')).convert('RGB')
        aux = exr.read(os.path.join(DP, tag + '_aux.exr'))[..., 0]; m = np.rint(aux) == 8000
        im.resize((2048, 1152), Image.LANCZOS).save(os.path.join(OUT, f'kb_hc8_{tag}.png'))
        mk = np.array(Image.fromarray(m.astype(np.uint8) * 255).resize((2048, 1152), Image.NEAREST)) > 127
        M = np.zeros((1152, 2048, 4), np.uint8); M[..., :3] = 255; M[..., 3] = np.where(mk, 0, 255); Image.fromarray(M, 'RGBA').save(os.path.join(OUT, f'kb_hc8_{tag}_mask.png'))
        chunks.append({'name': f'kb_hc8_{tag}', 'kind': 'hc8', 'W_api': 2048, 'H_api': 1152, 'mask_frac': round(float(mk.mean()), 4), 'prompt': PROMPT2 + PROMPT if '--thu2' in sys.argv else PROMPT, 'az': az})
    json.dump({'site': 'kb', 'chunks': chunks}, open(os.path.join(OUT, 'chunks.json'), 'w'), indent=1); print(chunks)

def comp(DP, DC, DA, OUT, DJ):
    os.makedirs(OUT, exist_ok=True); P = []
    for az in AZ:
        tag = f'proj{int(az):03d}'; pos, look = CM.orbit_cam(ST, az)
        C = np.asarray(Image.open(os.path.join(DC, tag + '.png')).convert('RGB'), np.float32)
        Pk = exr.read(os.path.join(DP, tag + '_pos.exr'))[..., :3]; P.append((az, pos, look, C, Pk))
    stats = []
    files = sorted(glob.glob(os.path.join(DA, '[0-9][0-9][0-9][0-9].png')))
    for fp in files:
        f = int(os.path.basename(fp)[:4]); cpos, clook, _ = CM.cam_at('kb', f)
        A = np.asarray(Image.open(fp).convert('RGB'), np.float32); H, W = A.shape[:2]
        pos = exr.read(fp[:-4] + '_pos.exr')[..., :3]; bid = np.rint(exr.read(fp[:-4] + '_aux.exr')[..., 0])
        m = bid == 8000; ys, xs = np.nonzero(m); X = pos[ys, xs]
        vf = X - np.array(cpos); vf /= np.linalg.norm(vf, axis=1, keepdims=True)
        num = np.zeros((len(ys), 3), np.float32); den = np.zeros(len(ys), np.float32); mag = np.full(len(ys), np.inf, np.float32)
        for (az, ppos, plook, C, Pk) in P:
            Hc, Wc = Pk.shape[:2]
            fwd, r, u = CM.basis(ppos, plook); d = X - np.array(ppos); z = d @ np.array(fwd)
            fpx = MM / 36.0 * Wc; px = Wc / 2 + fpx * (d @ np.array(r)) / z; py = Hc / 2 - fpx * (d @ np.array(u)) / z
            ok = (z > 1) & (px >= 0) & (px <= Wc - 1) & (py >= 0) & (py <= Hc - 1)
            q = np.stack([np.clip(py, 0, Hc - 1), np.clip(px, 0, Wc - 1)])
            Pq = np.stack([map_coordinates(Pk[..., c], q, order=0) for c in range(3)], 1)
            dist = np.linalg.norm(d, axis=1); ok &= np.linalg.norm(Pq - X, axis=1) < 0.12 + 0.002 * dist
            vk = d / dist[:, None]; th = np.degrees(np.arccos(np.clip((vf * vk).sum(1), -1, 1))); w = np.exp(-(th / 12.0) ** 2) * ok
            col = np.stack([map_coordinates(C[..., c], q, order=1) for c in range(3)], 1)
            num += col * w[:, None]; den += w
            # phóng đại texel: điểm ảnh khung (đổi về 1080p) / điểm ảnh tấm, qua Jacobi của toạ độ chiếu theo lưới ảnh
            PX = np.full((H, W), np.nan, np.float32); PY = np.full((H, W), np.nan, np.float32); PX[ys, xs] = px; PY[ys, xs] = py
            gx = np.gradient(PX, axis=1); gy = np.gradient(PY, axis=0); gxy = np.gradient(PX, axis=0); gyx = np.gradient(PY, axis=1)
            det = np.abs(gx * gy - gxy * gyx)[ys, xs] / (Wc / W) ** 2
            mk_ = ok & np.isfinite(det); mag[mk_] = np.minimum(mag[mk_], 1.0 / np.sqrt(np.maximum(det[mk_], 1e-6)))
        out = A.copy(); val = den > 1e-3
        out[ys[val], xs[val]] = num[val] / den[val][:, None]
        Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(OUT, os.path.basename(fp)))
        n = max(1, len(ys)); st = {'f': f, 'az': round(CM.az_at(f), 1), 'px_bastion': int(len(ys)), 'lo_pct': round(100 * float((~val).sum()) / n, 2),
                                   'gian_2x_pct': round(100 * float((val & (mag > 2.0)).sum()) / n, 2), 'gian_TB': round(float(np.median(mag[val])) if val.any() else 0, 2)}
        stats.append(st)
    json.dump({'phuong_phap': __doc__.split('\n')[0], 'khung': stats}, open(DJ, 'w'), indent=1, ensure_ascii=False)
    for s in stats[::12]: print(s)

if __name__ == '__main__':
    if sys.argv[1] == 'prep': prep(sys.argv[2], sys.argv[3])
    else: comp(*sys.argv[2:7])
