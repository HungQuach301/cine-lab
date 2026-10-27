#!/opt/cine/bin/python
"""BAN-CUOI-T4-B2a · M01 thử E (K1179-D5 đẩy 2D, K1179-D6 nước AI) — tấm E-P1-2026 ngày lượt 2 (ảnh AI phiên A, KHÔNG sinh lại: 0 API) trên render look3-b1.
Thủ tục ghép = reports/k1179/do/ghep_kn8.py (K1179 §4: `ghep_kn8.py <khung> <lượt> thap bo_dat`; hàm lop/bo/lop_a/bao_ve/ghep NẠP NGUYÊN từ tệp đó)
— chỉ khác đầu vào: render + mặt nạ dựng lại bằng trang bc/look3-b1 (sà lan có boong — hết elip đen của lớp tàu look3), 2304×1296 (đẩy 2D không phóng to).
Trước ghép: CHE bóng cầu AI lệch (vệt tối trên mặt nước sát cầu, phía không có bóng render) — mặt nạ vệt = điểm nước AI trong dải ≤ 28 px quanh cầu tối hơn
trung vị nước AI vòng ngoài (28–70 px) quá 14/255 (bóng cầu AI lệch), hoặc SÁNG hơn quá 14/255 (mặt cầu AI lệch ra ngoài cầu render) → inpaint TELEA từ chính nước AI (không lấy màu render).
  e_m01_b2a.py prep            → e/tam/E-M01/: render.png (LUT kênh), matna.png, matna-thap.png, mat_na_ct(-thap).png, toa(-thap).json, prep.json
  e_m01_b2a.py ghep            → e/tam/E-M01/l2-thap-bo_dat/: ai-sua.png (AI 2304×1296 đã che bóng cầu), vet-bong-cau.png, ghep.png, ghep.json
  e_m01_b2a.py video           → /var/tmp/bc/e-m01/: ghép từng khung (tấm + (a)-E từ render tl CODINH) → đẩy 2D 1,0 %/s một phép cho cả khung → 1920×1080
                                 ghep-1080p.mp4 (CRF 16) + bản kiểm 640×360 (ghep/render, không mất) + bản xem ≤ 5 MB
Toà có tên (K1179 KN-5): loai thap (y1_m ≥ 75 m ODN) · lich_su (nguon_lich_su) · mai_vom (St Paul's). "Guildhall Art Gallery" (toà 1999) KHÔNG còn là lịch sử → hạ nhà thường."""
import hashlib, json, os, subprocess, sys, types
import cv2, numpy as np
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
R = os.environ.get('BC_R', '/var/tmp/bc/r'); D = os.environ.get('LDN_DATA', '/var/tmp/ldn')
E = f'{REPO}/channel-k2/k2c-t4-02/ban-cuoi/e'; T = f'{E}/tam/E-M01'; TAG = 'l2-thap-bo_dat'; AI_SRC = f'{E}/ai/E-P1-ngay-l2.jpg'
LUT = f'{REPO}/channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube'; VO = '/var/tmp/bc/e-m01'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
K8 = types.ModuleType('ghep_kn8'); exec(compile(open(f'{REPO}/reports/k1179/do/ghep_kn8.py').read().split("\nif __name__ == '__main__'")[0], 'ghep_kn8.py', 'exec'), K8.__dict__)
# công trình lịch sử có tên trong khung P1 (nguồn: Historic England, National Heritage List for England — các toà dưới đều là di sản xếp hạng)
LICH_SU = {'Guildhall': 'Historic England NHLE — Guildhall (Grade I)', 'Royal Exchange': 'Historic England NHLE — Royal Exchange (Grade I)',
           'Bank of England': 'Historic England NHLE — Bank of England (Grade I)', 'Mansion House': 'Historic England NHLE — Mansion House (Grade I)',
           'Tower of St Mary Somerset': 'Historic England NHLE — Tower of St Mary Somerset (Grade I)', 'Monument': 'Historic England NHLE — The Monument (Grade I)'}
THAP_Y1 = 75.0


def lut(src, dst): subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', src, '-vf', f"lut3d=file='{LUT}':interp=tetrahedral", dst], check=True)
def dec24(im): im = im.astype(np.int64); return (im[..., 2] << 16) | (im[..., 1] << 8) | im[..., 0]


def prep():
    os.makedirs(T, exist_ok=True); lut(f'{R}/E-M01/00000.png', f'{T}/render.png')
    M = cv2.imread(f'{R}/E-M01-m1/00000.png'); cv2.imwrite(f'{T}/matna.png', M)
    M2 = cv2.imread(f'{R}/E-M01-m2/00000.png')[:, :, ::-1].astype(int); M3 = dec24(cv2.imread(f'{R}/E-M01-m3e/00000.png'))
    ten = {t['ma']: t for t in json.load(open(f'{D}/look3e/ten.json'))}; nha = K8.lop(M, 'nha'); CT = np.zeros(M.shape, np.uint8); toa = []
    sp = nha & (M2[..., 1] == 0) & (M2[..., 2] == 200) & np.isin(M2[..., 0], [20, 40, 60, 80, 100])     # mask 2 lớp 5 St Paul's mới (như ghep_e_bc.prep)
    if sp.sum() >= 50:
        CT[sp] = (200, 0, 20); ys, xs = np.nonzero(sp)
        toa.append(dict(ten="St Paul's Cathedral", mau=[20, 0, 200], px=int(sp.sum()), hop=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())], loai='mai_vom',
                        nguon_lich_su='Historic England NHLE — St Paul\'s Cathedral (Grade I)', nguon='mask2 lớp 5'))
    giu = {}
    for m, t in ten.items():
        if t['y1'] >= THAP_Y1: giu[m] = dict(loai='thap', dinh_odn_m=round(float(t['y1']), 1))
        elif t['ten'] in LICH_SU: giu[m] = dict(loai='lich_su', nguon_lich_su=LICH_SU[t['ten']])
    ids, cnt = np.unique(M3[(M3 > 0) & nha & ~sp], return_counts=True); i = 1; ha = np.zeros(M.shape[:2], bool)
    for m, c in zip(ids, cnt):
        m = int(m); sel = (M3 == m) & nha & ~sp
        if m not in ten: continue
        if m not in giu or c < 50: ha |= sel; continue
        i += 1; mau = [min(255, 10 + 9 * i), 128, 200 - (i % 20)]; CT[sel] = mau[::-1]; ys, xs = np.nonzero(sel); t = ten[m]
        toa.append(dict(ten=t['ten'], osm_id=t['osm_id'], mau=mau, px=int(c), hop=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())], y1_m=t['y1'], nguon='OSM name (look3e)', **giu[m]))
    Mt = M.copy(); Mt[ha] = (215, 215, 215); cv2.imwrite(f'{T}/matna-thap.png', Mt); cv2.imwrite(f'{T}/mat_na_ct-thap.png', CT)
    json.dump(toa, open(f'{T}/toa-thap.json', 'w'), ensure_ascii=False, indent=1)
    st = dict(khung='E-M01', W=M.shape[1], H=M.shape[0], toa_co_ten=len(toa), ha_ve_nha_thuong_pct=round(float(ha.mean() * 100), 2), nuoc_pct=round(float(K8.lop(M, 'nuoc').mean() * 100), 2),
              sha_render=sha(f'{T}/render.png'), sha_matna=sha(f'{T}/matna.png'), sha_matna_thap=sha(f'{T}/matna-thap.png'), sha_ct=sha(f'{T}/mat_na_ct-thap.png'),
              nguon='render bc/look3-b1 cờ d spp 24, khoá 0 của M01 (≡ E-P1-ngay.json), LUT k2c-t3-kenh-v030')
    json.dump(st, open(f'{T}/prep.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(st, ensure_ascii=False)); print([(t['ten'], t['loai']) for t in toa])


def bong_cau(AI, M):
    """mặt nạ vệt bóng cầu AI lệch: cầu = nhà/kè (nha 235) nằm GIỮA lòng sông (đóng nước bằng nhân 61 px phủ được) — không đụng bờ kè"""
    s = M.shape[0] / 1080; W = K8.lop(M, 'nuoc'); nha = ~W & ~K8.lop(M, 'tau')
    k = int(61 * s) | 1; Wc = cv2.morphologyEx(W.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((k, k), np.uint8)) > 0
    cau = nha & Wc; n, lb, st, _ = cv2.connectedComponentsWithStats(cau.astype(np.uint8), 8)
    cau = np.isin(lb, [j for j in range(1, n) if st[j, cv2.CC_STAT_AREA] >= 400 * s * s])
    r1, r2 = int(28 * s), int(70 * s); dist = cv2.distanceTransform((~cau).astype(np.uint8), cv2.DIST_L2, 5)
    gan = W & (dist <= r1); xa = W & (dist > r1) & (dist <= r2)
    Y = cv2.cvtColor(AI, cv2.COLOR_BGR2GRAY).astype(float)
    med = float(np.median(Y[xa])) if xa.any() else 0.0
    vet = gan & (np.abs(Y - med) > 14);   # tối = bóng cầu AI lệch; sáng = mặt cầu AI lệch ra ngoài cầu render vet = cv2.morphologyEx(vet.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
    vet = cv2.dilate(vet.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0; vet &= W
    return vet, cau, med


def ghep():
    o = f'{T}/{TAG}'; os.makedirs(o, exist_ok=True); Rr = cv2.imread(f'{T}/render.png'); H, W = Rr.shape[:2]
    AI = cv2.resize(cv2.imread(AI_SRC), (W, H), interpolation=cv2.INTER_AREA); M = cv2.imread(f'{T}/matna-thap.png')
    vet, cau, med = bong_cau(AI, M); AIs = cv2.inpaint(AI, vet.astype(np.uint8) * 255, int(round(5 * H / 1080)), cv2.INPAINT_TELEA)
    cv2.imwrite(f'{o}/ai-sua.png', AIs); cv2.imwrite(f'{o}/vet-bong-cau.png', vet.astype(np.uint8) * 255)
    A = K8.lop_a(M, True, 'bo_dat'); G, B = K8.ghep(Rr, AIs, A); cv2.imwrite(f'{o}/ghep.png', G)
    rec = dict(khung='E-M01', luot='l2', mat_na='matna-thap.png', kieu='bo_dat (K1179 §4)', sha_ai_goc=sha(AI_SRC), sha_ai_sua=sha(f'{o}/ai-sua.png'), sha_render=sha(f'{T}/render.png'),
               vet_bong_cau_px=int(vet.sum()), cau_px=int(cau.sum()), trung_vi_nuoc_ai=med, lop_a_E_pct=round(float(A.mean() * 100), 2), bao_ve_pct=round(float(B.mean() * 100), 2),
               nuoc_pct=round(float(K8.lop(M, 'nuoc').mean() * 100), 2), sai_khac_lop_a_max=int(np.abs(G.astype(int) - Rr.astype(int))[A].max()), sha_ghep=sha(f'{o}/ghep.png'))
    json.dump(rec, open(f'{o}/ghep.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(rec, ensure_ascii=False))


def day(img, t, v=0.01, out=(1920, 1080)):
    """đẩy 2D một phép cho CẢ khung: tỉ lệ s = 1 + v·t quanh tâm khung (tâm cố định). Nội suy dưới điểm ảnh: warp (bicubic) lên 2× khung ra rồi thu INTER_AREA
    → không nhảy bậc nguyên điểm, không răng cưa; không phóng to nguồn (2304/1,179 = 1954 ≥ 1920)"""
    H, W = img.shape[:2]; s = 1.0 + v * t; cw, ch = W / s, H / s; o2 = (out[0] * 2, out[1] * 2)
    M = np.float32([[o2[0] / cw, 0, -(W - cw) / 2 * o2[0] / cw], [0, o2[1] / ch, -(H - ch) / 2 * o2[1] / ch]])
    return cv2.resize(cv2.warpAffine(img, M, o2, flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT), out, interpolation=cv2.INTER_AREA)


def video():
    os.makedirs(f'{VO}/g', exist_ok=True); os.makedirs(f'{VO}/r', exist_ok=True); os.makedirs(f'{VO}/r0', exist_ok=True)
    M = cv2.imread(f'{T}/matna-thap.png'); A = K8.lop_a(M, True, 'bo_dat'); B = K8.bao_ve(A)
    al = np.clip(cv2.distanceTransform((~B).astype(np.uint8), cv2.DIST_L2, 3) / 2.0, 0, 1)[..., None]; Tm = cv2.imread(f'{T}/{TAG}/ai-sua.png').astype(np.float64)
    fs = sorted(x for x in os.listdir(f'{R}/E-M01-tl') if x.endswith('.jpg')); tmp = f'{VO}/lut.png'
    for i, f in enumerate(fs):
        lut(f'{R}/E-M01-tl/{f}', tmp); Rb = cv2.imread(tmp).astype(np.float64)
        G = al * Tm + (1 - al) * Rb; G[B] = Rb[B]; G = np.round(G).astype(np.uint8); t = i / 24.0
        cv2.imwrite(f'{VO}/g/{i:05d}.png', day(G, t)); cv2.imwrite(f'{VO}/r/{i:05d}.png', day(Rb.astype(np.uint8), t)); cv2.imwrite(f'{VO}/r0/{i:05d}.png', cv2.resize(Rb.astype(np.uint8), (1920, 1080), interpolation=cv2.INTER_AREA))
    ff = lambda a: subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-framerate', '24'] + a, check=True)
    ff(['-i', f'{VO}/g/%05d.png', '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', '-an', '-movflags', '+faststart', f'{VO}/M01-E-1080p.mp4'])
    for src, n in (('g', 'ghep'), ('r', 'render-day'), ('r0', 'render-codinh')):
        ff(['-i', f'{VO}/{src}/%05d.png', '-vf', 'scale=640:360:flags=area', '-c:v', 'libx264', '-preset', 'slow', '-crf', '0', '-pix_fmt', 'yuv444p', f'{VO}/M01-E-{n}-640.mp4'])
    cv2.imwrite(f'{VO}/matna-640.png', cv2.resize(M, (640, 360), interpolation=cv2.INTER_NEAREST))
    print('video', len(fs), 'khung', sha(f'{VO}/M01-E-1080p.mp4'))


if __name__ == '__main__': dict(prep=prep, ghep=ghep, video=video)[sys.argv[1]]()
