"""PT4 · ghép tấm C vào nền A (HC2) — kế thừa design/pt/lai/compose_c2.py (PT2), thêm:
1) --nen-cu DIR: tấm C được sinh trên nền A CŨ (PT2) nhưng nền A đã dựng thêm (lòng nhà đổ nát…) → tỉ số đổ bóng
   S_p = lọc(A_p/A_d2) [hình học mới] × (A_d2 / A_cu_d2) [chỉ nơi hình học đổi, không lọc] ⇒ bóng của vật mới vào đúng tấm C cũ;
   vùng bảo vệ = hợp của mã lớp mới và cũ (nơi C không được phép sửa ở lần sinh).
2) --sac-A: biến thể "độ sáng chi tiết từ C + sắc độ từ A": ở vùng được sửa, màu = A_p × (Y_LAI / Y_A) (giữ tông màu/bão hoà của A, chi tiết sáng tối của C).
3) Vùng bảo vệ = đúng giá trị 16 bit của A (như PT2); --xoa-lop như PT2.
  /opt/cine/bin/python -I compose4.py <nền A> <ảnh C> <ra> [--nen-cu DIR] [--xoa-lop 9510] [--sac-A] [--mat-na <mặt nạ RGBA đã gửi>]"""
import sys, os, json, shutil, numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'lai'))
import lai_common as LC
BG, CP, OUT = sys.argv[1:4]; OLD = sys.argv[sys.argv.index('--nen-cu') + 1] if '--nen-cu' in sys.argv else None
SAC_A = '--sac-A' in sys.argv
os.makedirs(OUT, exist_ok=True); ORDER = ['d1', 'd2', 'd3', 'd4', 'n']
def rd16(p): return cv2.imread(p, cv2.IMREAD_UNCHANGED)[..., :3][..., ::-1].copy()
A16 = {p: rd16(os.path.join(BG, p + '.png')) for p in ORDER}
H, W = A16['d2'].shape[:2]
lin = lambda a16: LC.srgb2lin(a16.astype(np.float32) / 65535.0)
A2 = lin(A16['d2']); A2old = lin(rd16(os.path.join(OLD, 'd2.png'))) if OLD else A2
C8 = cv2.imread(CP, cv2.IMREAD_UNCHANGED)[..., :3][..., ::-1]
C = LC.srgb2lin(cv2.resize(C8, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0)
RV = '--ma-cua-A' not in sys.argv   # --ma-cua-A: má ô cửa lấy từ A (PT4 HC4 W6: AI vẽ thanh kim loại trong lòng cửa tầng trệt 1943)
prot = LC.protected_mask(BG, reveals=RV)
if OLD: prot |= LC.protected_mask(OLD, reveals=RV)
if '--mat-na' in sys.argv:   # PT4: vùng GIỮ của chính mặt nạ đã gửi AI (gồm dải chặn kiến trúc) cũng ghép lại A — trừ má ô cửa (lấy C như PT2)
    mk = cv2.imread(sys.argv[sys.argv.index('--mat-na') + 1], cv2.IMREAD_UNCHANGED)[..., 3]
    mk = cv2.resize(mk, (W, H), interpolation=cv2.INTER_NEAREST) > 127
    reg_m, mat_m, mc_m, _ = LC.load_cls(BG); prot |= mk & ~(mat_m == mc_m['vua_mo'])
XL = sys.argv[sys.argv.index('--xoa-lop') + 1].split(',') if '--xoa-lop' in sys.argv else []
if XL:
    reg_, mat_, mc_, _ = LC.load_cls(BG); xm = np.zeros_like(prot)
    for k in XL: xm |= (reg_ == int(k)) if k.isdigit() else (mat_ == mc_[k])
    prot |= cv2.dilate(xm.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
edit = ~prot
k21 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
lt = np.log(np.clip(((C + 2e-3) / (A2old + 2e-3)).mean(-1), 1e-3, 1e3)); med = cv2.GaussianBlur(lt, (0, 0), 40)
hi = cv2.morphologyEx(((lt - med) > 1.0).astype(np.uint8), cv2.MORPH_OPEN, k21) > 0
lo = cv2.morphologyEx(((lt - med) < -1.0).astype(np.uint8), cv2.MORPH_OPEN, k21) > 0
lech = cv2.dilate((hi | lo).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
# hình học đổi so với nền cũ (bóng/vật mới): log(A_d2 / A_cu_d2), chỉ giữ nơi lệch rõ
dnew = (np.log(A2 + 1e-4) - np.log(A2old + 1e-4)).astype(np.float32)
dnew = np.where(np.abs(dnew) > 0.03, dnew, 0.0)
def shade(Ap):
    ls = (np.log(Ap + 1e-4) - np.log(A2 + 1e-4)).astype(np.float32)
    ls = cv2.morphologyEx(cv2.morphologyEx(ls, cv2.MORPH_OPEN, k21), cv2.MORPH_CLOSE, k21)
    if lech.any():
        ok = (~lech).astype(np.float32); f = cv2.GaussianBlur(ls * ok[..., None], (0, 0), 15) / np.maximum(cv2.GaussianBlur(ok, (0, 0), 15), 1e-4)[..., None]
        ls = np.where(lech[..., None], f, ls)
    return np.exp(np.clip(ls + dnew, -8, 2.3))
dist = cv2.distanceTransform(edit.astype(np.uint8), cv2.DIST_L2, 3)
alpha = np.clip(dist / 2.0, 0, 1)[..., None]; alpha[prot] = 0
LUM = np.array([0.2126, 0.7152, 0.0722], np.float32)
stat = {'xoa_lop': XL, 'nen_cu': bool(OLD), 'sac_A': SAC_A, 'pct_bao_ve': round(float(prot.mean() * 100), 2), 'pct_duoc_sua': round(float(edit.mean() * 100), 2),
        'pct_hinh_hoc_doi': round(float(((dnew != 0).any(-1) & edit).mean() * 100), 2), 'luot': {}}
for p in ORDER:
    Ap = lin(A16[p]); L = C * shade(Ap)
    if p == 'n': L = np.minimum(L, 1.5 * Ap + 1e-4)
    if SAC_A:   # sắc độ của A, độ sáng (chi tiết) của LAI
        yl = (L * LUM).sum(-1, keepdims=True); ya = (Ap * LUM).sum(-1, keepdims=True)
        L = Ap * (yl / np.maximum(ya, 1e-5))
    o = Ap * (1 - alpha) + L * alpha
    o16 = np.clip(np.round(LC.lin2srgb(o) * 65535.0), 0, 65535).astype(np.uint16)
    o16[prot] = A16[p][prot]
    cv2.imwrite(os.path.join(OUT, p + '.png'), o16[..., ::-1])
    stat['luot'][p] = {'sai_khac_vung_bao_ve_TB_tren_255': round(float(np.abs(o16[prot].astype(np.int64) - A16[p][prot].astype(np.int64)).mean() / 257.0), 6)}
for f in os.listdir(BG):
    if f.endswith('.exr') or f == 'meta.json': shutil.copy(os.path.join(BG, f), OUT)
m = json.load(open(os.path.join(OUT, 'meta.json'))); m['lai'] = {'c_plate': os.path.basename(CP), 'ai_image': True, **stat}; m['ai_image'] = True
json.dump(m, open(os.path.join(OUT, 'meta.json'), 'w'), indent=1, ensure_ascii=False)
cv2.imwrite(os.path.join(OUT, 'bao_ve.png'), (prot * 255).astype(np.uint8))
print(json.dumps(stat, ensure_ascii=False))
