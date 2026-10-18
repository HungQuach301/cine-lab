"""NC-AI · AI-1 thử SAM (facebook/sam-vit-base, Apache-2.0) trên CPU: mỗi khối phố dò tay của SH cho MỘT điểm click
(điểm trong đa giác gần trọng tâm nhất — mô phỏng người dựng click 1 lần/khối), SAM vẽ đường bao; so IoU với khối dò tay.
Đây là bán tự động (người chọn khối, máy vẽ bao) — không phải phát hiện tự động. Dùng: <venv>/python -I ai1_sam.py <anh> <so-hoa-px.json> <ra_dir>"""
import sys, json, time, cv2, numpy as np, torch
from transformers import SamModel, SamProcessor
img, sh, out = sys.argv[1:4]
im = cv2.imread(img); F0 = json.load(open(sh))['features']
F = [f for f in F0 if f['vung'] == 'pho' and f['loai'] == 'khoi_pho']
allp = np.vstack([np.array(f['px']) for f in F0 if f['vung'] == 'pho' and f['loai'] in ('khoi_pho', 'nha')])
x0, y0 = allp.min(0) - 60; x1, y1 = allp.max(0) + 60
C = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_BGR2RGB); H, W = C.shape[:2]
t0 = time.time(); proc = SamProcessor.from_pretrained('facebook/sam-vit-base'); model = SamModel.from_pretrained('facebook/sam-vit-base').eval(); tl = time.time() - t0
def rast(p): r = np.zeros((H, W), np.uint8); cv2.fillPoly(r, [np.asarray(p, np.int32)], 1); return r
pts, hands = [], []
for f in F:
    h = np.array(f['px']) - [x0, y0]; R = rast(h); hands.append(R)
    d = cv2.distanceTransform(R, cv2.DIST_L2, 3); y, x = np.unravel_index(np.argmax(d), d.shape); pts.append([int(x), int(y)])  # điểm sâu nhất trong khối
t1 = time.time()
with torch.no_grad():
    inp = proc(images=C, return_tensors='pt'); emb = model.get_image_embeddings(inp['pixel_values'])
    te = time.time() - t1; res = []; MA = np.zeros((H, W), np.uint8); RH = np.zeros((H, W), np.uint8)
    for f, p, R in zip(F, pts, hands):
        ip = proc(images=C, input_points=[[[p]]], return_tensors='pt')
        o = model(image_embeddings=emb, input_points=ip['input_points'], multimask_output=True)
        ms = proc.image_processor.post_process_masks(o.pred_masks, ip['original_sizes'], ip['reshaped_input_sizes'])[0][0].numpy()
        sc = o.iou_scores[0, 0].numpy(); k = int(np.argmax(sc)); M = ms[k].astype(np.uint8)
        iou = float((M & R).sum() / max(1, (M | R).sum())); MA |= M; RH |= R
        res.append({'id': f['id'], 'diem': p, 'iou': round(iou, 3), 'sam_score': round(float(sc[k]), 3), 'tran_ra_px': int((M & (1 - R)).sum()), 'thieu_px': int((R & (1 - M)).sum())})
ious = [r['iou'] for r in res]
S = {'model': 'facebook/sam-vit-base', 'o': [int(x0), int(y0), int(x1), int(y1)], 'so_khoi': len(res), 'iou_trung_vi': round(float(np.median(ious)), 3),
     'iou_tb': round(float(np.mean(ious)), 3), 'khoi_iou_ge_0_5': sum(i >= 0.5 for i in ious), 'khoi_iou_ge_0_7': sum(i >= 0.7 for i in ious),
     'khoi_iou_ge_0_85': sum(i >= 0.85 for i in ious), 'iou_hop': round(float((MA & RH).sum() / max(1, (MA | RH).sum())), 3),
     'giay_nap_model': round(tl, 1), 'giay_ma_hoa_anh': round(te, 1), 'giay_moi_click': round((time.time() - t1 - te) / len(res), 2), 'tung_khoi': res}
json.dump(S, open(f'{out}/sam-1click.json', 'w'), ensure_ascii=False, indent=1)
vis = im[y0:y1, x0:x1].copy()
cs, _ = cv2.findContours(MA, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(vis, cs, -1, (0, 160, 0), 2)
for f in F: cv2.polylines(vis, [(np.array(f['px']) - [x0, y0]).astype(np.int32)], True, (0, 0, 255), 2)
for p in pts: cv2.circle(vis, tuple(p), 5, (255, 0, 0), -1)
cv2.imwrite(f'{out}/sam-1click.jpg', vis, [cv2.IMWRITE_JPEG_QUALITY, 85])
print({k: v for k, v in S.items() if k != 'tung_khoi'})
