"""A3 (lớp sống ghép bằng cộng hiệu render có/không khói) + A4 (khớp màu cục bộ trong vòng bảo vệ vật nhỏ) — số đo trên T6 (mặt nạ trong git)."""
import sys, json, hashlib, cv2, numpy as np
sys.path.insert(0, '/home/user/cine-lab')
from checks.ll import q_n2p as Q
S = '/tmp/claude-0/-home-user-cine-lab/55041e27-e67f-5c13-a28e-87011125b16b/scratchpad'; G0 = S + '/look2/channel-k2/k2c-t4-02/ai/goc/'
sys.path.insert(0, S + '/look2/scripts/k2ldn/ai'); import n2p_lib as NL  # bản sao (không sửa) — bao_ve/ghep của phía dựng


def lab(b): return cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32) - np.array([0, 128, 128], np.float32)


def khop_toan_cuc(R, AI, Ab, k=0.7):
    l = lambda x: cv2.cvtColor(x, cv2.COLOR_BGR2LAB).astype(np.float32); Rl, Al = l(R), l(AI)
    mr, sr = Rl[Ab].mean(0), Rl[Ab].std(0) + 1e-3; ma, sa = Al[Ab].mean(0), Al[Ab].std(0) + 1e-3
    return cv2.cvtColor(np.clip((Rl - mr) * (1 + k * (sa / sr - 1)) + mr + k * (ma - mr), 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def khoi(R, rng, n=14):
    """khói bếp tổng hợp: cột mảnh bốc lên từ mái (cộng sáng/xám), tất định"""
    H, W = R.shape[:2]; a = np.zeros((H, W), np.float32)
    for _ in range(n):
        x, y = rng.integers(200, W - 200), rng.integers(330, 640)
        for j in range(40):
            yy, xx = int(y - j * 2.2), int(x + j * 0.9 + rng.normal(0, 1))
            cv2.circle(a, (xx, yy), int(2 + j * 0.25), float(0.5 * (1 - j / 40)), -1)
    a = cv2.GaussianBlur(a, (0, 0), 2.0)[..., None]
    return np.clip(R * (1 - a) + np.array([200, 200, 205], np.float32) * a, 0, 255).astype(np.uint8)


def kiem_song(G, P, R, N, Ab):
    """(i-s) lớp sống: ngoài vùng bảo vệ G == clip(P + (R − N)) (sai ≤ 1 do làm tròn); trong vùng bảo vệ (đã có (i)) bỏ qua"""
    exp = np.clip(P.astype(np.int16) + (R.astype(np.int16) - N.astype(np.int16)), 0, 255)
    d = np.abs(G.astype(np.int16) - exp).max(-1); d[Ab] = 0
    return int(d.max()), int((d > 1).sum())


out = {}
R0 = cv2.imread(G0 + 'T6-render-l1l2.jpg'); L, n = Q.idmap(G0 + 'T6-matna-l1l2.png', (1920, 1080)); A = Q.lop(L, n, Q.LOP_A)
AI = cv2.resize(cv2.imread(G0 + 'T6-l2-ai.jpg'), (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
Ab = NL.bao_ve(A, no=1, nho_px=60, no_nho=3)
rng = np.random.default_rng(1666)
N = R0; R = khoi(R0, rng)                              # N = render KHÔNG khói (ảnh vào AI), R = render CÓ khói
RK = khop_toan_cuc(R, AI, Ab)
P, _ = NL.ghep(RK, AI, Ab, feather=3, bao=False)       # tấm nền đã ghép lớp (a), CHƯA có lớp sống
song = (np.abs(R.astype(np.int16) - N.astype(np.int16)).max(-1) > 0)
G_dung = np.clip(P.astype(np.int16) + (R.astype(np.int16) - N.astype(np.int16)) * (~Ab)[..., None], 0, 255).astype(np.uint8)
dif = np.abs(R.astype(np.int16) - N.astype(np.int16)).max(-1) > 8
G_dan = P.copy(); G_dan[dif & ~Ab] = RK[dif & ~Ab]                                    # cách T6 cũ: dán nguyên điểm ảnh render (cả nền sương)
sh = np.roll(R.astype(np.int16) - N.astype(np.int16), 6, axis=1)
G_lech = np.clip(P.astype(np.int16) + sh * (~Ab)[..., None], 0, 255).astype(np.uint8)   # lớp sống lệch 6 px (khung khác / máy khác)
G_nua = np.clip(P.astype(np.int16) + ((R.astype(np.int16) - N.astype(np.int16)) * 0.5).astype(np.int16) * (~Ab)[..., None], 0, 255).astype(np.uint8)
P_ai_khoi = khoi(P, np.random.default_rng(7), 5)                                       # AI tự vẽ khói lên tấm (tấm có vật chuyển động)
G_aik = np.clip(P_ai_khoi.astype(np.int16) + (R.astype(np.int16) - N.astype(np.int16)) * (~Ab)[..., None], 0, 255).astype(np.uint8)
for nm, G, PP in (('dung_cong_hieu', G_dung, P), ('dan_nguyen_T6', G_dan, P), ('lech_6px', G_lech, P), ('nua_cuong_do', G_nua, P), ('ai_ve_khoi_tren_tam', G_aik, P_ai_khoi)):
    mx, cnt = kiem_song(G, PP, R, N, Ab)
    i_a = int(np.abs(G.astype(np.int16) - RK.astype(np.int16)).max(-1)[A].max())
    out[f'A3 {nm}'] = dict(i_a_max=i_a, song_max=mx, song_diem_lech=cnt, dat_i_s=mx <= 1, song_pct=round(float(song.mean() * 100), 2))
cv2.imwrite(S + '/a3-T6-dung.png', G_dung); cv2.imwrite(S + '/a3-T6-nen.png', P); cv2.imwrite(S + '/a3-T6-dan.png', G_dan); cv2.imwrite(S + '/a3-T6-aikhoi-nen.png', P_ai_khoi)

# ---------------- A4: quầng vòng bảo vệ (vùng bảo vệ − mặt nạ) quanh vật nhỏ khi tông tấm lệch render
def quang(G, A, Ab, nho_px=60):
    """độ tương phản quầng: mỗi vật (a) nhỏ: ΔE76 giữa TB Lab của VÒNG bảo vệ (Ab − A) và TB của dải 2 px ngay ngoài vùng bảo vệ"""
    Gl = lab(G); n_, cc, st, _ = cv2.connectedComponentsWithStats(A.astype(np.uint8), 8); r = []
    for i in range(1, n_):
        if st[i, 4] >= nho_px: continue
        x0, y0, w, h = st[i, :4]; sl = (slice(max(0, y0 - 8), y0 + h + 8), slice(max(0, x0 - 8), x0 + w + 8))
        m = cc[sl] == i; pr = cv2.dilate(m.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        ring = Ab[sl] & ~A[sl] & pr; outer = (cv2.dilate((Ab[sl] & pr).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0) & ~Ab[sl] & ~A[sl]
        if ring.sum() < 3 or outer.sum() < 3: continue
        r.append(float(np.sqrt(((Gl[sl][ring].mean(0) - Gl[sl][outer].mean(0)) ** 2).sum())))
    return np.array(r)


def khop_cuc_bo(RK, AI, A, Ab, feather=3):
    """đề xuất phía dựng: quanh MỖI vật (a) (vòng bảo vệ + viền mềm) dùng render-khớp CỘNG một độ lệch màu không đổi (BGR) = trung vị(AI)
    − trung vị(render-khớp) ở dải 2 px ngay ngoài viền mềm (chênh tông cục bộ); rồi ghép như cũ. Điểm trong mặt nạ (a) GIỮ render-khớp."""
    RK2 = RK.astype(np.float32).copy(); n_, cc = cv2.connectedComponents(Ab.astype(np.uint8), 8); off = np.zeros(RK.shape, np.float32)
    for i in range(1, n_):
        m = cc == i; x, y, w, h = cv2.boundingRect(m.astype(np.uint8)); pad = feather + 4
        sl = (slice(max(0, y - pad), y + h + pad), slice(max(0, x - pad), x + w + pad)); ms = m[sl]
        zone = cv2.dilate(ms.astype(np.uint8), np.ones((2 * feather + 1,) * 2, np.uint8)) > 0
        outer = (cv2.dilate(zone.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0) & ~zone
        if outer.sum() < 3: continue
        o = np.median(AI[sl][outer].astype(np.float32), 0) - np.median(RK[sl][outer].astype(np.float32), 0)
        z = zone & ~A[sl]; blk = RK2[sl]; blk[z] = RK[sl][z].astype(np.float32) + o
    RK2 = np.clip(np.rint(RK2), 0, 255).astype(np.uint8); RK2[A] = RK[A]
    G2, _ = NL.ghep(RK2, AI, Ab, feather=feather, bao=False); G2[A] = RK[A]
    return G2, RK2


def quang2(G, AI, A, Ab, feather=3):
    """quầng = ΔE76 TB giữa ảnh ghép và ẢNH AI trên vòng bảo vệ + viền mềm (ngoài mặt nạ (a)) của vật nhỏ (< 60 px)"""
    Gl, Al = lab(G), lab(AI); n_, cc, st, _ = cv2.connectedComponentsWithStats(A.astype(np.uint8), 8)
    small = np.isin(cc, [i for i in range(1, n_) if st[i, 4] < 60])
    z = (cv2.dilate(small.astype(np.uint8), np.ones((2 * (3 + feather) + 1,) * 2, np.uint8)) > 0) & ~A
    d = np.sqrt(((Gl - Al) ** 2).sum(-1))[z]; return d


for tag, rm in (('l1', 'l1l2'), ('l2', 'l1l2'), ('l3', 'l3')):
    R0 = cv2.imread(G0 + f'T6-render-{rm}.jpg'); L, n = Q.idmap(G0 + f'T6-matna-{rm}.png', (1920, 1080)); A = Q.lop(L, n, Q.LOP_A)
    AI = cv2.resize(cv2.imread(G0 + f'T6-{tag}-ai.jpg'), (1920, 1080), interpolation=cv2.INTER_LANCZOS4); Ab = NL.bao_ve(A, no=1, nho_px=60, no_nho=3)
    RK = khop_toan_cuc(R0, AI, Ab); G, _ = NL.ghep(RK, AI, Ab, feather=3, bao=False)
    G2, RK2 = khop_cuc_bo(RK, AI, A, Ab)
    q1, q2 = quang2(G, AI, A, Ab), quang2(G2, AI, A, Ab)
    dA = int(np.abs(G2.astype(np.int16) - RK.astype(np.int16)).max(-1)[A].max())
    ringm = Ab & ~A; Dl = RK2.astype(np.int16) - RK.astype(np.int16); n_, cc = cv2.connectedComponents(Ab.astype(np.uint8), 8); res = 0
    for i in range(1, n_):
        ring = (cc == i) & ~A
        if ring.sum() < 2: continue
        res = max(res, float(np.abs(Dl[ring] - np.median(Dl[ring], 0)).max()))
    out[f'A4 T6-{tag}'] = dict(diem_vong_vien=int(len(q1)), quang_dE_tb_truoc=round(float(q1.mean()), 2), quang_dE_p90_truoc=round(float(np.percentile(q1, 90)), 2),
                             quang_dE_tb_sau=round(float(q2.mean()), 2), quang_dE_p90_sau=round(float(np.percentile(q2, 90)), 2), i_trong_a_sau=dA,
                             du_vong_sau_tru_lech_bgr=round(res, 2))
    if tag == 'l2': cv2.imwrite(S + '/a4-T6-l2-truoc.png', G); cv2.imwrite(S + '/a4-T6-l2-sau.png', G2)
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open(S + '/a3a4.json', 'w'), ensure_ascii=False, indent=1)
