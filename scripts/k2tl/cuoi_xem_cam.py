#!/opt/cine/bin/python
"""BAN-CUOI-T3 (việc 9) · khai XEM CÂM cho k2check (§13.4) theo mẫu channel-k2/k2c-t3-01/v7p/xem-cam-v7c.json:
đọc reports/ban-cuoi-t3/xem-cam/ket-qua.json (anim_cam.py: 3 người chấm AI, 8 câu, 0/1/2 theo từ khoá) → channel-k2/k2c-t3-01/cuoi/xem-cam-cuoi.json.
Chủ dự án CHƯA chấm (cổng chờ người); 'p_doc' (P đọc lại nguyên văn) để trống cho phiên P.   cuoi_xem_cam.py <master.mp4>"""
import datetime, hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / 'scripts/k2tl')); import anim_cam as A
R = json.loads((ROOT / 'reports/ban-cuoi-t3/xem-cam/ket-qua.json').read_text()); vid = Path(sys.argv[1])
out = dict(tat_tieng=True, cau_hoi=A.Q, ghi=f'8 câu §13.4 (0/1/2 mỗi câu, chấm theo từ khoá anim_cam.py); chuỗi 1 khung/{A.STEP} s, 320×180, không tiếng, không phụ đề; '
           'người chấm AI chỉ THAM KHẢO; chủ dự án CHƯA chấm; P chưa đọc lại nguyên văn (p_doc)',
           nguoi_cham=[dict(id=k, vai='ai', model=A.MODEL, dung=round(sum(v['diem'].values()) / 2, 1), tong=len(A.Q), diem_tho=sum(v['diem'].values()), diem_tho_toi_da=2 * len(A.Q), ngay=datetime.date.today().isoformat()) for k, v in R['nguoi'].items()],
           chi_phi_usd=R.get('chi_phi_usd'), ket_qua='reports/ban-cuoi-t3/xem-cam/ket-qua.json',
           video=str(vid), video_sha256=hashlib.sha256(vid.read_bytes()).hexdigest())
(ROOT / 'channel-k2/k2c-t3-01/cuoi/xem-cam-cuoi.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n'); print([(x['id'], x['dung']) for x in out['nguoi_cham']])
