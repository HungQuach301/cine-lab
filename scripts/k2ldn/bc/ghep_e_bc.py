#!/opt/cine/bin/python
"""BAN-CUOI-T4-A · LUẬT E (RULES-LL 1.17.8 N2P-E) — chuẩn bị + ghép tấm E toàn khung 2026 máy CODINH.
  ghep_e_bc.py prep <khung>          → $BCE/<khung>/: render.png (look3 cờ d + LUT kênh), matna.png (mask 1 look3d: nha_thuong 215 / nha 235 / nước …),
                                       mat_na_ct.png (mã công trình 24 bit: mái vòm St Paul's (mask 2 lớp 5) + toà OSM có tên (mask 3 look3e)), toa.json [{ten, mau, px, hop}]
  ghep_e_bc.py ghep <khung> <ai.jpg> <tag>   → <tag>/ghep.png: ảnh AI toàn khung (2560×1440 → 1080p, INTER_AREA); lớp (a)-E = nha 235 ∪ nước ∪ dải bờ ±8 px ∪ tàu
                                       (+ congsu/lua/co/pin/nguoi nếu có) NỞ 1 px (vật < 60 px nở 3 px) = render ĐÚNG TỪNG ĐIỂM; ngoài vùng bảo vệ chuyển mềm 2 px phía AI.
  ghep_e_bc.py video <khung> <tag> <thư mục khung render tl> → <tag>/tl-ghep.mp4 + tl-render.mp4 (640×360, không mất): nền = tấm AI tĩnh, lớp (a)-E ghép lại TỪNG KHUNG từ render.
Mặt nạ đọc từ $BC_R/<khung>-m1|-m2|-m3e/00000.png (dung_bc.py)."""
import hashlib, json, os, subprocess, sys
import numpy as np, cv2
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
R = os.environ.get('BC_R', '/var/tmp/bc/r'); BCE = os.environ.get('BCE', os.path.join(REPO, 'channel-k2/k2c-t4-02/ban-cuoi/e/tam')); D = os.environ.get('LDN_DATA', '/var/tmp/ldn')
LUT = os.path.join(REPO, 'channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube')
PAL = {'troi': (40, 80, 200), 'nuoc': (0, 170, 190), 'bang': (200, 170, 90), 'suon': (150, 120, 70), 'nha': (235, 235, 235), 'nha_thuong': (215, 215, 215),
       'tau': (255, 0, 0), 'khac': (128, 128, 128), 'cay': (60, 140, 60)}
A_LOP = ('nha', 'nuoc', 'tau')
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def lop(m, k): return np.all(m == np.array(PAL[k][::-1]), -1)
def dec24(im): im = im.astype(np.int64); return (im[..., 2] << 16) | (im[..., 1] << 8) | im[..., 0]
def lut(src, dst): subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', src, '-vf', f"lut3d=file='{LUT}':interp=tetrahedral", dst], check=True)


def lop_a(M):
    A = np.zeros(M.shape[:2], bool)
    for k in A_LOP: A |= lop(M, k)
    W = lop(M, 'nuoc').astype(np.uint8); s = M.shape[0] / 1080
    bien = cv2.morphologyEx(W, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    r = int(round(8 * s)); bo = cv2.dilate(bien.astype(np.uint8), np.ones((2 * r + 1, 2 * r + 1), np.uint8)) > 0
    return A | bo


def bao_ve(A):
    """vùng bảo vệ = (a)-E nở 1 px; thành phần < 60 px nở 3 px (§15 (a))"""
    n, lb, st, _ = cv2.connectedComponentsWithStats(A.astype(np.uint8), 8)
    nho = np.isin(lb, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] < 60])
    return (cv2.dilate(A.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) | (cv2.dilate(nho.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0)


def prep(k):
    o = f'{BCE}/{k}'; os.makedirs(o, exist_ok=True)
    lut(f'{R}/{k}/00000.png', f'{o}/render.png')
    M = cv2.imread(f'{R}/{k}-m1/00000.png'); cv2.imwrite(f'{o}/matna.png', M)
    M2 = cv2.imread(f'{R}/{k}-m2/00000.png')[:, :, ::-1].astype(int); M3 = dec24(cv2.imread(f'{R}/{k}-m3e/00000.png'))
    ten = {t['ma']: t for t in json.load(open(f'{D}/look3e/ten.json'))}
    nha = lop(M, 'nha'); CT = np.zeros(M.shape, np.uint8); toa = []
    # mái vòm St Paul's: mask 2 = mã công trình lớp 5 (màu R = 20 × chỉ số; St Paul's mới = các mã 1675.5…1708.8 → chỉ số 1–5)
    sp = nha & (M2[..., 1] == 0) & (M2[..., 2] == 200) & np.isin(M2[..., 0], [20, 40, 60, 80, 100])
    if sp.sum() >= 50:
        CT[sp] = (200, 0, 20); ys, xs = np.nonzero(sp); toa.append(dict(ten="St Paul's Cathedral", mau=[20, 0, 200], px=int(sp.sum()), hop=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())], nguon='mask2 lớp 5'))
    ids, cnt = np.unique(M3[(M3 > 0) & nha & ~sp], return_counts=True); i = 1
    for m, c in zip(ids, cnt):
        if c < 50 or int(m) not in ten: continue
        i += 1; mau = [min(255, 10 + 9 * i), 128, 200 - (i % 20)]; sel = (M3 == m) & nha & ~sp
        CT[sel] = mau[::-1]; ys, xs = np.nonzero(sel); t = ten[int(m)]
        toa.append(dict(ten=t['ten'], osm_id=t['osm_id'], mau=mau, px=int(c), hop=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())], y1_m=t['y1'], nguon='OSM name (look3e)'))
    cv2.imwrite(f'{o}/mat_na_ct.png', CT); json.dump(toa, open(f'{o}/toa.json', 'w'), ensure_ascii=False, indent=1)
    A = lop_a(M); st = dict(khung=k, lop_a_E_pct=round(float(A.mean() * 100), 2), nha_thuong_pct=round(float(lop(M, 'nha_thuong').mean() * 100), 2),
                            toa_co_ten=len(toa), sha_render=sha(f'{o}/render.png'), sha_matna=sha(f'{o}/matna.png'), sha_ct=sha(f'{o}/mat_na_ct.png'))
    json.dump(st, open(f'{o}/prep.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(st, ensure_ascii=False)); print([t['ten'] for t in toa])


def ghep(k, ai, tag):
    o = f'{BCE}/{k}'; t = f'{o}/{tag}'; os.makedirs(t, exist_ok=True)
    Rr = cv2.imread(f'{o}/render.png'); H, W = Rr.shape[:2]; AI = cv2.resize(cv2.imread(ai), (W, H), interpolation=cv2.INTER_AREA)
    M = cv2.imread(f'{o}/matna.png'); A = lop_a(M); B = bao_ve(A)
    al = np.clip(cv2.distanceTransform((~B).astype(np.uint8), cv2.DIST_L2, 3) / 2.0, 0, 1)[..., None]   # 0 trong vùng bảo vệ → 1 sau 2 px
    G = np.round(al * AI + (1 - al) * Rr).astype(np.uint8); G[B] = Rr[B]
    cv2.imwrite(f'{t}/ghep.png', G); cv2.imwrite(f'{t}/ai-1080.png', AI)
    d = int(np.abs(G.astype(int) - Rr.astype(int))[A].max()) if A.any() else 0
    rec = dict(khung=k, tag=tag, ai=os.path.relpath(ai, REPO) if os.path.abspath(ai).startswith(REPO) else ai, sha_ai=sha(ai), lop_a_E_pct=round(float(A.mean() * 100), 2),
               bao_ve_pct=round(float(B.mean() * 100), 2), pct_diem_anh_ai=round(float((~B).mean() * 100), 2), sai_khac_lop_a_max=d, sha_ghep=sha(f'{t}/ghep.png'))
    json.dump(rec, open(f'{t}/ghep.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(rec, ensure_ascii=False))


def video(k, tag, src, mn=''):
    """tấm tĩnh + lớp (a)-E từ render từng khung (640×360); mặt nạ khung 0 (máy CODINH)"""
    o = f'{BCE}/{k}'; t = f'{o}/{tag}'; tmp = f'/var/tmp/bc/tmp-{k}-{tag}'; os.makedirs(tmp, exist_ok=True)
    M = cv2.imread(f'{R}/{src}-m1/00000.png')
    if mn: M = cv2.resize(cv2.imread(f'{o}/matna-{mn}.png'), (M.shape[1], M.shape[0]), interpolation=cv2.INTER_NEAREST)   # mặt nạ biến thể (thu nhỏ NEAREST)
    A = lop_a(M); B = bao_ve(A); al = np.clip(cv2.distanceTransform((~B).astype(np.uint8), cv2.DIST_L2, 3) / 2.0, 0, 1)[..., None]
    T = cv2.resize(cv2.imread(f'{t}/ghep.png'), (M.shape[1], M.shape[0]), interpolation=cv2.INTER_AREA).astype(np.float64)
    fs = sorted(x for x in os.listdir(f'{R}/{src}') if x.endswith('.png'))
    for i, f in enumerate(fs):
        lut(f'{R}/{src}/{f}', f'{tmp}/r{i:05d}.png'); Rb = cv2.imread(f'{tmp}/r{i:05d}.png').astype(np.float64)
        G = al * T + (1 - al) * Rb; G[B] = Rb[B]; cv2.imwrite(f'{tmp}/g{i:05d}.png', np.round(G).astype(np.uint8))
    for p, n in (('g', 'tl-ghep.mp4'), ('r', 'tl-render.mp4')):
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-framerate', '24', '-i', f'{tmp}/{p}%05d.png', '-c:v', 'libx264', '-preset', 'slow', '-crf', '0', '-pix_fmt', 'yuv444p', f'/var/tmp/bc/{k}-{tag}-{n}'], check=True)
    cv2.imwrite(f'{t}/matna-640.png', M); subprocess.run(['rm', '-rf', tmp]); print('video', k, tag, len(fs), 'khung → /var/tmp/bc/')


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'prep': prep(sys.argv[2])
    elif c == 'ghep': ghep(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == 'video': video(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else '')


# ---- biến thể mặt nạ "thap" (đề xuất E1-b): lớp (a)-E công trình có tên = mái vòm St Paul's + mọi lớp không phải nhà OSM (cầu, tường, nhà thờ, Monument…)
#      + toà OSM có tên là THÁP (đỉnh ≥ THAP_Y1 m ODN) hoặc thuộc danh sách công trình lịch sử; toà OSM có tên khác (cửa hàng, văn phòng thấp) → nha_thuong 215.
THAP_Y1 = 75.0
LICH_SU = ('Guildhall', 'Royal Exchange', 'Bank of England', 'Mansion House', 'Tower of St Mary Somerset', 'Monument')


def prep_thap(k):
    o = f'{BCE}/{k}'; M = cv2.imread(f'{o}/matna.png'); M3 = dec24(cv2.imread(f'{R}/{k}-m3e/00000.png')); CT = cv2.imread(f'{o}/mat_na_ct.png')
    ten = {t['ma']: t for t in json.load(open(f'{D}/look3e/ten.json'))}
    giu = [m for m, t in ten.items() if t['y1'] >= THAP_Y1 or any(t['ten'].startswith(x) for x in LICH_SU)]
    ha = (M3 > 0) & ~np.isin(M3, np.array(giu, np.int64)) & lop(M, 'nha')
    M2 = M.copy(); M2[ha] = (215, 215, 215); CT2 = CT.copy(); CT2[ha] = 0
    cv2.imwrite(f'{o}/matna-thap.png', M2); cv2.imwrite(f'{o}/mat_na_ct-thap.png', CT2)
    toa = [t for t in json.load(open(f'{o}/toa.json')) if t['ten'] == "St Paul's Cathedral" or ('osm_id' in t and any(tt['osm_id'] == t['osm_id'] and m in giu for m, tt in ten.items()))]
    # toà còn lại phải còn ≥ 50 điểm sau khi hạ
    toa = [t for t in toa if (np.all(CT2 == np.array(t['mau'][::-1]), -1)).sum() >= 50]
    json.dump(toa, open(f'{o}/toa-thap.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(dict(khung=k, ha_ve_nha_thuong_pct=round(float(ha.mean() * 100), 2), lop_a_E_pct=round(float(lop_a(M2).mean() * 100), 2), toa=[t['ten'] for t in toa]), ensure_ascii=False))


def ghep_mn(k, ai, tag, mn):
    """ghép với mặt nạ khác (matna-<mn>.png)"""
    o = f'{BCE}/{k}'; t = f'{o}/{tag}'; os.makedirs(t, exist_ok=True)
    Rr = cv2.imread(f'{o}/render.png'); H, W = Rr.shape[:2]; AI = cv2.resize(cv2.imread(ai), (W, H), interpolation=cv2.INTER_AREA)
    M = cv2.imread(f'{o}/matna-{mn}.png'); A = lop_a(M); B = bao_ve(A)
    al = np.clip(cv2.distanceTransform((~B).astype(np.uint8), cv2.DIST_L2, 3) / 2.0, 0, 1)[..., None]
    G = np.round(al * AI + (1 - al) * Rr).astype(np.uint8); G[B] = Rr[B]; cv2.imwrite(f'{t}/ghep.png', G); cv2.imwrite(f'{t}/ai-1080.png', AI)
    rec = dict(khung=k, tag=tag, mat_na=f'matna-{mn}.png', sha_ai=sha(ai), lop_a_E_pct=round(float(A.mean() * 100), 2), pct_diem_anh_ai=round(float((~B).mean() * 100), 2),
               sai_khac_lop_a_max=int(np.abs(G.astype(int) - Rr.astype(int))[A].max()), sha_ghep=sha(f'{t}/ghep.png'))
    json.dump(rec, open(f'{t}/ghep.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(rec, ensure_ascii=False))


if __name__ == '__main__' and sys.argv[1] == 'prep_thap': prep_thap(sys.argv[2])
if __name__ == '__main__' and sys.argv[1] == 'ghep_mn': ghep_mn(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
