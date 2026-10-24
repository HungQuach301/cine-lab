"""A5 (d)(e): timelapse 6 khung (mặt trời đổi 18→43°, phương vị 200→240°), 960×540. Đáp án:
 dung_chieu3d = bề mặt AI dựng lại đúng ánh sáng từng khung (render bề mặt mới ở từng khung — 'chiếu lên hình học + dựng lại ánh sáng' lý tưởng)
 khu_sang     = ảnh AI khung 0 × (render_t / render_0) trong vùng nhà (khử sáng theo tỉ số — cách chiếu 3D phía dựng làm được)
 anh_tinh     = ảnh AI khung 0 dán tĩnh theo mặt nạ mọi khung (sai khi ánh sáng đổi)
 chong_sang   = ảnh AI khung 0 × bóng render_t (không khử sáng → sáng chồng 2 lần; quỹ đạo đúng nhưng khung 0 lệch tấm)
 nhap_nhay    = dung_chieu3d + nhiễu bề mặt khác nhau mỗi khung (AI mỗi khung)"""
import sys, os, json, cv2, numpy as np
sys.path.insert(0, '/home/user/cine-lab')
from checks.ll import q_k1175 as K
D = '/tmp/claude-0/-home-user-cine-lab/55041e27-e67f-5c13-a28e-87011125b16b/scratchpad/a5tl'; out = {}
for nua in 'AB':
    if not os.path.exists(f'{D}/{nua}-goc-t0/iid.png') or not os.path.exists(f'{D}/{nua}-bm-t5/rgb.png'): continue
    cls = cv2.imread(f'{D}/{nua}-goc-t0/cls.png')[..., ::-1]; I = K._ma(f'{D}/{nua}-goc-t0/iid.png'); I[~np.all(cls == K.NHA_THUONG, -1)] = 0
    ids, cnt = np.unique(I, return_counts=True); small = ids[cnt < 30]; I[np.isin(I, small)] = 0     # nhà thấy < 30 px ở 960×540 bỏ
    M = cv2.dilate((I > 0).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    R = [cv2.imread(f'{D}/{nua}-goc-t{i}/rgb.png') for i in range(6)]; B = [cv2.imread(f'{D}/{nua}-bm-t{i}/rgb.png') for i in range(6)]
    gh = lambda base, top: np.where(M[..., None], top, base)
    Rf = [r.astype(np.float32) + 1 for r in R]
    cases = {'dung_chieu3d': [gh(R[i], B[i]) for i in range(6)],
             'khu_sang': [gh(R[i], np.clip(B[0] * (Rf[i] / Rf[0]), 0, 255).astype(np.uint8)) for i in range(6)],
             'anh_tinh': [gh(R[i], B[0]) for i in range(6)],
             'chong_sang': [gh(R[i], np.clip(B[0] * (Rf[i] / 160.0), 0, 255).astype(np.uint8)) for i in range(6)],
             'nhap_nhay': [gh(R[i], np.clip(B[i] + np.random.default_rng(i).normal(0, 4, B[i].shape), 0, 255).astype(np.uint8)) for i in range(6)]}
    for k, Cs in cases.items():
        q = K.quy_dao(Cs, R, I); e = np.array(list(q['e_h'].values()))
        t0 = np.sqrt(((K._lab(Cs[0]) - K._lab(B[0])) ** 2).sum(-1))[I > 0]
        out[f'{nua} {k}'] = dict(nha=len(e), e_p50=round(float(np.median(e)), 4), e_p95=round(float(np.percentile(e, 95)), 4), e_p99=round(float(np.percentile(e, 99)), 4),
                                pct_e_gt_010=round(float((e > 0.10).mean() * 100), 2), pct_e_gt_015=round(float((e > 0.15).mean() * 100), 2),
                                nhap_be_mat=q['nhap_be_mat'], t0_dE_tb=round(float(t0.mean()), 2), t0_dE_p95=round(float(np.percentile(t0, 95)), 2))
    # đổi ánh sáng render (đối chứng): ln R_t/R_0 TB
    q = K.quy_dao(R, R, I)
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open(D + '/../a5-tl.json', 'w'), ensure_ascii=False, indent=1)
