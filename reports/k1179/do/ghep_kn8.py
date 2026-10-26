#!/opt/cine/bin/python
"""K-1.17.9 · KN-8 — ghép thử bằng MÁY (0 API sinh ảnh) lớp (a)-E "bờ" : mặt nước BÊN TRONG đường bờ render lấy từ ảnh AI.
Đầu vào CHỈ ĐỌC (git @bc1693b5, archive vào /var/tmp/k1179/in): e/tam/<khung>/{render.png, matna*.png, mat_na_ct*.png, toa*.json}, e/ai/<khung>-<lượt>.jpg.
Ghép = đúng thủ tục `scripts/k2ldn/bc/ghep_e_bc.py ghep_mn` của phiên A (AI 2560×1440 → 1080p INTER_AREA; vùng bảo vệ = (a)-E nở 1 px, vật < 60 px nở 3 px,
= render đúng từng điểm; chuyển mềm 2 px phía AI) — CHỈ khác lớp (a)-E: bỏ lõi nước = nước(mặt nạ) − dải bờ ±8 px @1080 (giữ dải bờ, nha 235 gồm
cầu/kè/tường, tàu, congsu/lua/co/pin/nguoi). Ra: /var/tmp/k1179/kn8/<khung>-<lượt>-<mn>/ghep.png + episode.yaml (khai `nuoc_ai: true`) + tờ so trước/sau.
  ghep_kn8.py <khung> <lượt> <mn: thap|du> [bo8|bo_dat]
"""
import hashlib, json, os, shutil, sys
import cv2, numpy as np
IN = '/var/tmp/k1179/in/channel-k2/k2c-t4-02/ban-cuoi/e'; RA = '/var/tmp/k1179/kn8'
PAL = {'nuoc': (0, 170, 190), 'nha': (235, 235, 235), 'tau': (255, 0, 0)}
A_LOP = ('nha', 'nuoc', 'tau', 'congsu', 'lua', 'co', 'pin', 'nguoi')
PAL_X = {'congsu': (170, 150, 120), 'co': (255, 255, 0), 'pin': (255, 0, 255), 'lua': (255, 128, 0), 'nguoi': (0, 255, 0)}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


def lop(M, k): return np.all(M == np.array(dict(PAL, **PAL_X)[k][::-1]), -1)


def bo(M, px=8):
    W = lop(M, 'nuoc').astype(np.uint8); r = int(round(px * M.shape[0] / 1080))
    return cv2.dilate((cv2.morphologyEx(W, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0).astype(np.uint8), np.ones((2 * r + 1,) * 2, np.uint8)) > 0


def lop_a(M, nuoc_ai, kieu='bo8'):
    """kieu 'bo8' = đúng đề xuất KN-8 (bỏ lõi nước, giữ dải bờ ±8 px cả hai phía); 'bo_dat' = biến thể K (bỏ MỌI điểm nước: dải bờ chỉ giữ phía đất)"""
    A = np.zeros(M.shape[:2], bool)
    for k in A_LOP: A |= lop(M, k)
    B = bo(M); A |= B
    if nuoc_ai: A &= ~(lop(M, 'nuoc') & (~B if kieu == 'bo8' else True))
    return A


def bao_ve(A):
    n, lb, st, _ = cv2.connectedComponentsWithStats(A.astype(np.uint8), 8)
    nho = np.isin(lb, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] < 60])
    return (cv2.dilate(A.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) | (cv2.dilate(nho.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0)


def ghep(Rr, AI, A):
    B = bao_ve(A); al = np.clip(cv2.distanceTransform((~B).astype(np.uint8), cv2.DIST_L2, 3) / 2.0, 0, 1)[..., None]
    G = np.round(al * AI + (1 - al) * Rr).astype(np.uint8); G[B] = Rr[B]; return G, B


def main(k, luot, mn, kieu='bo8'):
    t = f'{IN}/tam/{k}'; suf = '-thap' if mn == 'thap' else ''
    Rr = cv2.imread(f'{t}/render.png'); H, W = Rr.shape[:2]; aip = f'{IN}/ai/{k}-{luot}.jpg'
    AI = cv2.resize(cv2.imread(aip), (W, H), interpolation=cv2.INTER_AREA); M = cv2.imread(f'{t}/matna{suf}.png')
    d = f'{RA}/{k}-{luot}-{mn}' + ('' if kieu == 'bo8' else f'-{kieu}'); os.makedirs(d, exist_ok=True)
    A0, A1 = lop_a(M, False), lop_a(M, True, kieu)
    G0, _ = ghep(Rr, AI, A0); G1, B1 = ghep(Rr, AI, A1)
    goc = f'{t}/{luot}{suf}/ghep.png'
    cv2.imwrite(f'{d}/ghep.png', G1); cv2.imwrite(f'{d}/ghep-cu.png', G0)
    nuoc = lop(M, 'nuoc'); loi = nuoc & ~bo(M)
    rec = dict(khung=k, luot=luot, kieu=kieu, mat_na=f'matna{suf}.png', sha_ai=sha(aip), sha_render=sha(f'{t}/render.png'), sha_mat_na=sha(f'{t}/matna{suf}.png'),
               ghep_cu_trung_ban_A=bool(os.path.exists(goc) and np.array_equal(cv2.imread(goc), G0)), sha_ghep_moi=sha(f'{d}/ghep.png'),
               nuoc_pct=round(float(nuoc.mean() * 100), 2), loi_nuoc_pct=round(float(loi.mean() * 100), 2),
               lop_a_E_cu_pct=round(float(A0.mean() * 100), 2), lop_a_E_moi_pct=round(float(A1.mean() * 100), 2), bao_ve_moi_pct=round(float(B1.mean() * 100), 2),
               sai_khac_lop_a_moi_max=int(np.abs(G1.astype(int) - Rr.astype(int))[A1].max()))
    json.dump(rec, open(f'{d}/ghep.json', 'w'), ensure_ascii=False, indent=1)
    # episode.yaml cho k2check: chép khai tấm của phiên A, thay ghep + khai nuoc_ai
    import yaml
    E = yaml.safe_load(open(f'{IN}/kiem/{k}-{luot}{suf}/episode.yaml')); kd = f'{IN}/kiem/{k}-{luot}{suf}'
    T = E['n2p']['tam'][0]
    for x in ('render', 'mat_na', 'mat_na_ct'): T[x] = os.path.normpath(os.path.join(kd, T[x]))
    T['ghep'] = f'{d}/ghep.png'; T['id'] = f"{T['id']}-kn8" + ('' if kieu == 'bo8' else '-' + kieu); T['nuoc_ai'] = True if kieu == 'bo8' else kieu; E['id'] += '-kn8'; E['n2p'].pop('video', None)
    yaml.safe_dump(E, open(f'{d}/episode.yaml', 'w'), allow_unicode=True, sort_keys=False)
    for x in ('timeline.json', 'log-shot.json'): shutil.copy(f'{kd}/{x}', f'{d}/{x}')
    print(json.dumps(rec, ensure_ascii=False))


if __name__ == '__main__': main(*sys.argv[1:5])
