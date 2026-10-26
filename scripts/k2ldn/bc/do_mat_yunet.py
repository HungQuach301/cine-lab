"""Đo mặt bằng YuNet (chỉ dùng tệp mô hình checks/models/face_detection_yunet_2023mar.onnx, không đọc mã checks/).
Mọi khung, ở độ phân giải gốc và phóng ×2 (mặt nhỏ ở 360p). Ra JSON: mặt lớn nhất/khung, điểm, khung > 1/8.
dùng: do_mat_yunet.py <clip.mp4> <ra.json> [nguong_diem=0.5]"""
import sys, json, hashlib, cv2
clip, ra = sys.argv[1], sys.argv[2]; NG = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
MO = 'checks/models/face_detection_yunet_2023mar.onnx'
cap = cv2.VideoCapture(clip); W = int(cap.get(3)); H = int(cap.get(4)); fps = cap.get(5)
det = {s: cv2.FaceDetectorYN.create(MO, '', (W * s, H * s), NG, 0.3, 5000) for s in (1, 2)}
khung = []; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    hop = []
    for s, d in det.items():
        g = f if s == 1 else cv2.resize(f, (W * s, H * s), interpolation=cv2.INTER_CUBIC)
        _, r = d.detect(g)
        for x in (r if r is not None else []):
            hop.append(dict(ti_le=round(float(x[3]) / s / H, 4), diem=round(float(x[14]), 3), hop=[round(float(v) / s, 1) for v in x[:4]], phong=s))
    m = max(hop, key=lambda h: h['ti_le'], default=None)
    khung.append(dict(k=i, t=round(i / fps, 3), so_hop=len(hop), lon_nhat=m)); i += 1
co = [k for k in khung if k['lon_nhat']]
lon = max(co, key=lambda k: k['lon_nhat']['ti_le'], default=None)
out = dict(clip=clip, sha256=hashlib.sha256(open(clip, 'rb').read()).hexdigest(), mo_hinh=MO, mo_hinh_sha256=hashlib.sha256(open(MO, 'rb').read()).hexdigest(),
           W=W, H=H, fps=fps, so_khung=i, nguong_diem=NG, phong=[1, 2], so_khung_co_mat=len(co),
           mat_lon_nhat=dict(k=lon['k'], t=lon['t'], **lon['lon_nhat']) if lon else None,
           diem_cao_nhat=max((k['lon_nhat']['diem'] for k in co), default=None),
           khung_vuot_1_8=[k['k'] for k in co if k['lon_nhat']['ti_le'] > 1 / 8], tran=0.125, khung=khung)
json.dump(out, open(ra, 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'khung'}, ensure_ascii=False))
