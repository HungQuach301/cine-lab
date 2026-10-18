"""NC-AI · AI-3 thử phục chế CÓ ĐÁP ÁN trên bản khắc PD (Drinkwater 1786 "View from Gibraltar of the Spanish Batteries", IA leaf427, SHA bb057d4f…).
Ô 256×256 cắt từ gốc = đáp án; thu nhỏ ×4 (INTER_AREA) → phóng lại ×4 bằng (a) bicubic, (b) Swin2SR x4 (caidas/swin2SR-classical-sr-x4-64, Apache-2.0).
Đo PSNR/SSIM so đáp án + "cạnh bịa": tỉ lệ điểm cạnh Canny của bản phóng KHÔNG có cạnh gốc trong bán kính 2 px (precision cạnh).
Rồi độ sâu Depth Anything V2 Small (Apache-2.0) trên ảnh toàn khung: đo % điểm ảnh ở bước nhảy độ sâu lớn (sẽ rách khi trượt 2.5D) và tương quan thứ tự trời/xa/gần.
Dùng: <venv>/python -I ai3_phuc_che.py <anh> <ra_dir>"""
import sys, json, time, cv2, numpy as np, torch
from PIL import Image
from transformers import Swin2SRForImageSuperResolution, Swin2SRImageProcessor, pipeline
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim
img, out = sys.argv[1:3]; im = cv2.imread(img, cv2.IMREAD_GRAYSCALE); H, W = im.shape
rng = np.random.default_rng(20261018); tiles = []
while len(tiles) < 6:  # 6 ô có nội dung (độ lệch chuẩn > 25), hạt giống cố định
    y, x = rng.integers(0, H - 256), rng.integers(0, W - 256); t = im[y:y + 256, x:x + 256]
    if t.std() > 25: tiles.append((int(x), int(y), t))
pr = Swin2SRImageProcessor.from_pretrained('caidas/swin2SR-classical-sr-x4-64'); m = Swin2SRForImageSuperResolution.from_pretrained('caidas/swin2SR-classical-sr-x4-64').eval()
def edge_prec(a, ref):
    ea, er = cv2.Canny(a, 60, 150) > 0, cv2.dilate((cv2.Canny(ref, 60, 150) > 0).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    return float((ea & er).sum() / max(1, ea.sum()))
R = []; t0 = time.time(); strip = []
for x, y, t in tiles:
    lo = cv2.resize(t, (64, 64), interpolation=cv2.INTER_AREA)
    bic = cv2.resize(lo, (256, 256), interpolation=cv2.INTER_CUBIC)
    with torch.no_grad():
        o = m(**pr(Image.fromarray(lo).convert('RGB'), return_tensors='pt')).reconstruction[0]
    sr = (o.clamp(0, 1).permute(1, 2, 0).numpy() * 255).round().astype(np.uint8)[:256, :256]; sr = cv2.cvtColor(sr, cv2.COLOR_RGB2GRAY)
    R.append({'o': [x, y], 'psnr_bicubic': round(psnr(t, bic), 2), 'psnr_swin2sr': round(psnr(t, sr), 2), 'ssim_bicubic': round(ssim(t, bic), 3),
              'ssim_swin2sr': round(ssim(t, sr), 3), 'canh_dung_bicubic': round(edge_prec(bic, t), 3), 'canh_dung_swin2sr': round(edge_prec(sr, t), 3)})
    strip.append(np.hstack([t, bic, sr]))
tsr = (time.time() - t0) / len(tiles)
cv2.imwrite(f'{out}/phuc-che-goc-bicubic-swin2sr.jpg', np.vstack(strip[:3]), [cv2.IMWRITE_JPEG_QUALITY, 88])
# độ sâu
t1 = time.time(); de = pipeline('depth-estimation', model='depth-anything/Depth-Anything-V2-Small-hf')
small = Image.open(img).convert('RGB'); small = small.resize((1024, int(1024 * small.height / small.width)))
d = np.array(de(small)['predicted_depth'].squeeze().numpy() if hasattr(de(small)['predicted_depth'], 'numpy') else de(small)['depth'], np.float32)
d = cv2.resize(d, small.size); d = (d - d.min()) / max(1e-6, d.max() - d.min())  # gần = lớn (disparity tương đối)
gy, gx = np.gradient(d); jump = np.hypot(gx, gy) > 0.02
top, bot = float(np.median(d[: d.shape[0] // 5])), float(np.median(d[-d.shape[0] // 5:]))
cv2.imwrite(f'{out}/do-sau-da2s.jpg', np.hstack([cv2.cvtColor(np.array(small), cv2.COLOR_RGB2GRAY), (d * 255).astype(np.uint8)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
S = {'tile': R, 'tb': {k: round(float(np.mean([r[k] for r in R])), 3) for k in R[0] if k != 'o'}, 'giay_swin2sr_moi_o_64to256': round(tsr, 2),
     'do_sau': {'model': 'depth-anything/Depth-Anything-V2-Small-hf', 'giay': round(time.time() - t1, 1), 'pt_diem_buoc_nhay_gt_0_02': round(float(jump.mean() * 100), 2),
                'disparity_trung_vi_1_5_tren': round(top, 3), 'disparity_trung_vi_1_5_duoi': round(bot, 3)}}
json.dump(S, open(f'{out}/ket-qua.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps({k: v for k, v in S.items() if k != 'tile'}, ensure_ascii=False))
