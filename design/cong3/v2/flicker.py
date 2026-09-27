"""Đo nhấp nháy của lớp vẽ trên shot máy tĩnh (Cổng 3 v2).
So hai chuỗi RGB24 thô (hàng từ dưới lên) cùng shot, cùng khung: có lớp vẽ (paint) và không (nopaint).
- Thu nhỏ 4×4 (trung bình) để loại grain (σ 1,5 mã → ~0,4 mã).
- Điểm tĩnh = điểm mà |ΔL| giữa hai khung kề ở bản nopaint < 0,5 mã (cảnh đứng yên, lửa thở ±4 % vẫn có ở cả hai bản).
- Chỉ số: trung bình |ΔL_paint| trên điểm tĩnh (mã 8 bit) và tỷ lệ điểm tĩnh có |ΔL_paint| > 2 mã, so với cùng số đo của nopaint.
Chạy: python flicker.py paint.rgb nopaint.rgb W H [n_frames]"""
import sys, json, numpy as np
pa, pb, W, H = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
n = int(sys.argv[5]) if len(sys.argv) > 5 else None
def frames(p):
    a = np.fromfile(p, np.uint8); k = a.size // (W * H * 3); a = a[: k * W * H * 3].reshape(k, H, W, 3).astype(np.float32)
    L = a @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    return L.reshape(k, H // 4, 4, W // 4, 4).mean(axis=(2, 4))
A, B = frames(pa), frames(pb); k = min(len(A), len(B), n or 10**9); A, B = A[:k], B[:k]
dA, dB = np.abs(np.diff(A, axis=0)), np.abs(np.diff(B, axis=0))
static = dB < 0.5
out = {'cap_khung': int(k - 1), 'ty_le_diem_tinh': round(float(static.mean()), 4),
       'paint_dL_tb_diem_tinh': round(float(dA[static].mean()), 3), 'nopaint_dL_tb_diem_tinh': round(float(dB[static].mean()), 3),
       'paint_ty_le_diem_tinh_dL_gt2': round(float((dA[static] > 2).mean()), 5), 'nopaint_ty_le_diem_tinh_dL_gt2': round(float((dB[static] > 2).mean()), 5),
       'paint_dL_tb_toan_khung': round(float(dA.mean()), 3), 'nopaint_dL_tb_toan_khung': round(float(dB.mean()), 3)}
print(json.dumps(out, ensure_ascii=False, indent=1))
