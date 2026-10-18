"""PT2 · ghép tấm C vào nền A (HC2 + HC3 phần nền): ra bộ nền LAI cùng cấu trúc thư mục nền A (d1..d4, n, depth, cls, sunvis, meta).
1) Chiếu sáng theo lượt: LAI_p = C' × S_p, S_p = (A_p + ε)/(A_d2 + ε) (tuyến tính) — tỉ số đổ bóng của chính hình học A (vân A triệt tiêu),
   lọc mở/đóng 21 px (trần ×10) bỏ vệt bóng mảnh của gờ mà AI đã xoá; vùng C lệch bóng LỚN so với A (|log C/A − TB mờ σ40| > 1,0, mở 21 px) → tỉ số đổ bóng nội suy từ lân cận;
   lượt d2 = C ⇒ bóng, nắng, giờ xanh, đêm ĐỀU từ lượt chiếu sáng A (không sinh C đêm, không nguồn sáng mới).
2) Vùng bảo vệ (mã lớp, nở 3 px): GHÉP LẠI đúng giá trị 16 bit của A_p (trùng điểm ảnh tuyệt đối); mép hoà 2 px nằm hoàn toàn PHÍA vùng được sửa.
3) Vật AI thêm bị loại ở kiểm dữ kiện (HC4) → `--xoa mask.png`: ghép lại A ở các vùng đó (cùng cách như vùng bảo vệ).
  /opt/cine/bin/python -I compose_c2.py <nền A dir> <ảnh C png> <ra dir> [--xoa xoa.png]"""
import sys, os, json, shutil, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lai_common as LC
BG, CP, OUT = sys.argv[1:4]; XOA = sys.argv[sys.argv.index('--xoa') + 1] if '--xoa' in sys.argv else None
os.makedirs(OUT, exist_ok=True); ORDER = ['d1', 'd2', 'd3', 'd4', 'n']

def rd16(p): return cv2.imread(p, cv2.IMREAD_UNCHANGED)[..., :3][..., ::-1].copy()
A16 = {p: rd16(os.path.join(BG, p + '.png')) for p in ORDER}
H, W = A16['d2'].shape[:2]
lin = lambda a16: LC.srgb2lin(a16.astype(np.float32) / 65535.0)
A2 = lin(A16['d2'])
C8 = cv2.imread(CP, cv2.IMREAD_UNCHANGED)[..., :3][..., ::-1]
C = LC.srgb2lin(cv2.resize(C8, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0)

prot = LC.protected_mask(BG, reveals='--ma-cua-A' not in sys.argv)
if XOA: prot |= cv2.imread(XOA, cv2.IMREAD_GRAYSCALE) > 127
XL = sys.argv[sys.argv.index('--xoa-lop') + 1].split(',') if '--xoa-lop' in sys.argv else []
if XL:   # HC4: loại điểm ảnh C của cả một lớp vật (vd. 'cat' = bao cát A bị AI xoá thành bóng ma; '9510' = thùng A bị AI vẽ thành thùng kim loại)
    reg_, mat_, mc_, _ = LC.load_cls(BG); xm = np.zeros_like(prot)
    for k in XL: xm |= (reg_ == int(k)) if k.isdigit() else (mat_ == mc_[k])
    prot |= cv2.dilate(xm.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
edit = ~prot
eps = 2e-3
T = (C + eps) / (A2 + eps)
# PT2 (sau rà 200 %): chiếu sáng chuẩn bằng tỉ số đổ bóng của chính hình học A (xem đầu tệp). Bản "chi tiết tách vùng σ40/σ150" để lại
# dải mờ ở gờ tường mảnh → bỏ.
lt = np.log(np.clip(T.mean(-1), 1e-3, 1e3)); med = cv2.GaussianBlur(lt, (0, 0), 40)
# chỗ bóng/nắng của C lệch A trên VÙNG LỚN (mở hình thái 21 px)
k9 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)); k21 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
hi = cv2.morphologyEx(((lt - med) > 1.0).astype(np.uint8), cv2.MORPH_OPEN, k21) > 0
lo = cv2.morphologyEx(((lt - med) < -1.0).astype(np.uint8), cv2.MORPH_OPEN, k21) > 0
# vùng lệch bóng lớn (AI đổi hình chi tiết nhỏ, vd. công-xon ban công mất bóng): giữ C, tỉ số đổ bóng NỘI SUY từ lân cận (σ 15 px);
# (đã thử: kẹp độ sáng / ghép A / vá ảnh + bóng A — đều để lại mảng tròn ở rà 400 % → bỏ)
# (bản kẹp độ sáng tạo mảng tròn phẳng; bản ghép lại A tạo mảng xám — cả hai bỏ sau rà 400 %)
lech = cv2.dilate((hi | lo).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0
stat_lech = round(float((edit & lech).mean() * 100), 2)
Cc = C
def shade(Ap):
    """log tỉ số đổ bóng A_p/A_d2, bỏ vệt mảnh < 21 px; trần ×10 (bóng gờ mà AI đã xoá) bằng mở + đóng hình thái; mép bóng lớn giữ sắc."""
    ls = (np.log(Ap + 1e-4) - np.log(A2 + 1e-4)).astype(np.float32)   # ε nhỏ: lượt đêm ~0,003 — ε lớn làm đêm sáng giả
    ls = cv2.morphologyEx(cv2.morphologyEx(ls, cv2.MORPH_OPEN, k21), cv2.MORPH_CLOSE, k21)
    if lech.any():   # vùng lệch: tỉ số đổ bóng nội suy từ lân cận không lệch (σ 15 px) — d2 vẫn = C
        ok = (~lech).astype(np.float32); f = cv2.GaussianBlur(ls * ok[..., None], (0, 0), 15) / np.maximum(cv2.GaussianBlur(ok, (0, 0), 15), 1e-4)[..., None]
        ls = np.where(lech[..., None], f, ls)
    return np.exp(np.clip(ls, -8, 2.3))
# hoà mép: alpha của LAI = 1 sâu trong vùng sửa, 0 ở vùng bảo vệ; dốc 2 px chỉ trong vùng sửa
dist = cv2.distanceTransform(edit.astype(np.uint8), cv2.DIST_L2, 3)
alpha = np.clip(dist / 2.0, 0, 1)[..., None]; alpha[prot] = 0
stat = {'xoa_lop': XL, 'pct_bao_ve': round(float(prot.mean() * 100), 2), 'pct_duoc_sua': round(float(edit.mean() * 100), 2), 'lech_bong_lon_noi_suy_pct': stat_lech, 'luot': {}}
for p in ORDER:
    Ap = lin(A16[p]); L = Cc * shade(Ap)
    if p == 'n': L = np.minimum(L, 1.5 * Ap + 1e-4)    # đêm: không chỗ nào sáng hơn 1,5× chính A (độ sáng) (quầng đèn/cửa sổ A không bị khuếch đại thành nguồn sáng mới)
    o = Ap * (1 - alpha) + L * alpha
    o16 = np.clip(np.round(LC.lin2srgb(o) * 65535.0), 0, 65535).astype(np.uint16)
    o16[prot] = A16[p][prot]                  # vùng bảo vệ = đúng giá trị A (không qua phép tính nào)
    cv2.imwrite(os.path.join(OUT, p + '.png'), o16[..., ::-1])
    d = np.abs(o16[prot].astype(np.int64) - A16[p][prot].astype(np.int64)).mean() / 257.0
    stat['luot'][p] = {'sai_khac_vung_bao_ve_TB_tren_255': round(float(d), 6)}
for f in os.listdir(BG):
    if f.endswith('.exr') or f == 'meta.json': shutil.copy(os.path.join(BG, f), OUT)
m = json.load(open(os.path.join(OUT, 'meta.json'))); m['lai'] = {'c_plate': os.path.basename(CP), 'ai_image': True, **stat}; m['ai_image'] = True
json.dump(m, open(os.path.join(OUT, 'meta.json'), 'w'), indent=1, ensure_ascii=False)
cv2.imwrite(os.path.join(OUT, 'bao_ve.png'), (prot * 255).astype(np.uint8))
print(json.dumps(stat, ensure_ascii=False))
