"""PT2 · hàm chung: đọc EXR, giải mã lượt mã lớp (cls = mã vùng × 64 + mã vật liệu), mặt nạ vùng bảo vệ dữ kiện (HC2), mặt nạ được sửa (HC1)."""
import os, json, numpy as np, cv2
os.environ.setdefault('OPENCV_IO_ENABLE_OPENEXR', '1')

def exr(p):
    import OpenEXR
    a = list(OpenEXR.File(p).channels().values())[0].pixels; return (a[..., 0] if a.ndim == 3 else a).astype(np.float32)

def srgb2lin(a): return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
def lin2srgb(a): a = np.clip(a, 0, 1); return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)

# vùng (mã CUR của build_scene.py)
REG_NAMES = {9000: 'Line Wall (công trình mốc)', 9510: 'thùng', 9511: 'xe kéo', 9513: 'quầy hàng', 9514: 'gạch vụn', 9515: 'dầm gỗ', 9520: 'pháo',
             9521: 'đống đạn pháo', 9530: 'đèn', 9540: 'cột cờ', 9541: 'chốt gác', 9542: 'hầm trú ẩn', 9550: 'xe tải quân sự', 9516: 'vật nền phụ V6 (bảo vệ)', 9560: 'người 3D (bản tốt nhất, bảo vệ)', 9600: 'đồi bên kia vịnh / đường chân trời',
             9700: 'biển', 9800: 'mặt đất', 9900: 'tàu'}
# ĐƯỢC SỬA (HC1): bề mặt tường/mái của toà (vật liệu vữa, gạch, đá, ngói, bao cát) · mặt đất · đồ vật nền (thùng, xe kéo, quầy, gạch vụn, dầm gỗ)
EDIT_MATS_BUILDING = ('vua', 'gach', 'da_voi', 'da_hoc', 'ngoi', 'cat', 'vua_go')   # gờ tầng/gờ mái: bề mặt tường (vệt bóng gờ xử lý khi ghép)
EDIT_REGIONS = (9800, 9510, 9511, 9513, 9514, 9515)
# BẢO VỆ (HC2): mọi thứ còn lại — trời, biển, đồi/chân trời, Line Wall, tàu, pháo, đạn pháo, đèn, cột cờ, chốt gác, hầm, xe tải,
# và trên toà: kính, lòng cửa (nguồn sáng đêm), cửa chớp, cửa, khung, ban công sắt/gỗ, biển hiệu trơn. Cờ + người + khói = lớp sống của mình (ghép sau C).

def load_cls(d):
    meta = json.load(open(os.path.join(d, 'meta.json'))); mc = meta['matcode']
    cls = np.round(exr(os.path.join(d, 'cls.exr'))).astype(np.int64); return cls // 64, cls % 64, mc, meta

def editable_raw(d, reveals=False):
    """reveals=True (chỉ khi GHÉP): má ô cửa (vữa) lấy từ C — mặt nạ GỬI AI vẫn giữ má cửa; nội dung má cửa C được rà ở HC4."""
    reg, mat, mc, meta = load_cls(d)
    bmat = np.isin(mat, [mc[k] for k in EDIT_MATS_BUILDING + (('vua_mo',) if reveals else ()) if k in mc])
    ed = (((reg >= 1) & (reg < 9000)) & bmat) | np.isin(reg, EDIT_REGIONS)
    dep = exr(os.path.join(d, 'depth.exr')); ed &= dep < 20000
    return ed

def protected_mask(d, grow=3, reveals=False):
    """True = bảo vệ. Vật mang dữ kiện ngoài toà (trời, Line Wall, tàu, cờ, pháo, đèn…) nở `grow` px (1080p); phần gắn trên toà
    (ô cửa, cửa chớp, ban công, biển hiệu, đổ nát, gờ) chỉ nở 1 px — nở 3 px để lộ viền vữa A (xám lam) quanh mọi ô cửa (rà 200 % PT2)."""
    ed = editable_raw(d, reveals); prot = ~ed
    reg, mat, mc, meta = load_cls(d); onb = (reg >= 1) & (reg < 9000)
    k = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    nguoi = reg == 9560   # V6 bản tốt nhất: người 3D — KHÔNG nở (nở 3 px để lộ viền đất A sáng quanh người)
    big = cv2.dilate((prot & ~onb & ~nguoi).astype(np.uint8), k(grow)) > 0 if grow else (prot & ~onb)
    small = cv2.dilate((prot & onb).astype(np.uint8), k(1)) > 0
    return big | small | prot

def class_table(d):
    """thống kê điểm ảnh theo nhóm (để báo cáo % trời, % đất trống, % bảo vệ)."""
    reg, mat, mc, meta = load_cls(d); dep = exr(os.path.join(d, 'depth.exr'))
    inv = {v: k for k, v in mc.items()}; out = {'troi': float((dep > 20000).mean())}
    out['mat_dat'] = float((reg == 9800).mean()); out['toa'] = float(((reg >= 1) & (reg < 9000)).mean())
    for r, n in REG_NAMES.items(): out[n] = float((reg == r).mean())
    return out
