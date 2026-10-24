#!/opt/cine/bin/python
"""THU-B-T4 · cấu hình tờ so (nhãn rõ, không mù) + dòng kết quả kiểm dưới mỗi ô → $THUB/toso/cau-hinh.json (rồi to_so_thub.py)."""
import json, os
T = os.environ.get('THUB', '/var/tmp/ldn/thub')
PHU_B = (('render', '+2 h: V2 render'), ('anh_tinh', '+2 h: (i) ảnh tĩnh'), ('chieu_3d', '+2 h: (ii-a) chiếu 3D'), ('chieu_tiso', '+2 h: (ii-b) tỉ số bóng'))


def b(k, ten, vai, v2, i, ii):
    return dict(ten=ten, vai=vai, o=[dict(anh=f'{T}/bp/{k}/render.png', nhan='V2 đã chọn (dựng lại, cùng máy/giờ)', ten_tep=f'{k}-v2', ghi=v2),
                                     dict(anh=f'{T}/bp/{k}/l2/ghep.png', nhan='B ảnh tĩnh (i) — lượt 2', ten_tep=f'{k}-B-anh-tinh', ghi=i),
                                     dict(anh=f'{T}/bp/{k}/l2/khung0-cuoi.png', nhan='B chiếu 3D (ii) — khung 0', ten_tep=f'{k}-B-chieu-3d', ghi=ii)],
                phu=[dict(anh=f'{T}/toso/{k}-cuoi-{v}.png', nhan=n) for v, n in PHU_B])


def d(k, ten, vai, v2, dd, d2, phu=None):
    h = dict(ten=ten, vai=vai, o=[dict(anh=f'{T}/test/{k}-v2-lut.jpg', nhan='V2 đã chọn (P1 fov 36°)', ten_tep=f'{k}-v2', ghi=v2),
                                  dict(anh=f'{T}/test/{k}-d-lut.jpg', nhan='D 3D (nâng hình học + bề mặt)', ten_tep=f'{k}-D', ghi=dd),
                                  dict(anh=f'{T}/test/{k}-d2-lut.jpg', nhan='D + vân nướng (D2, AI)', ten_tep=f'{k}-D2', ghi=d2)])
    if phu: h['phu'] = phu
    return h


C = dict(ra='reports/thu-b-t4/to-so-thu-b.jpg', o_dir='reports/thu-b-t4/khung', hang=[
    b('M1-trung', 'B1 · M1-trung 1666', 'tháp St Saviour 70 m · 11/9/1666 16:00 · timelapse +2 h',
      ['8 510 nhà thường thấy · 557 đo được (6,5 % số nhà;', '79,3 % diện tích nhà; 27,7 % khung)', 'mặt tiền gần: khối hộp, mái trơn'],
      ['BE-MAT-NHA (a) 0 Chặn · (w) 2 (dời? ở 2,3–2,4 px/m)', '(b) 0/255 · (c) 0 lỗi thời đại (2 mô hình + O2)', '(d) video: 100 % nhà lệch; nhấp nháy 0,088 → TRƯỢT',
       'N2P-1 (a) TRƯỢT 218/255 = vùng BMN (KN-2) · N2P-3 ĐẠT'],
      ['khung 0 (1080p) ΔE 2,43 / p95 8,09 so tấm', '(e) 4,9/12,9 so tấm 1080p · ĐẠT so tấm 640×360', '(d) 3D: 39,3 % nhà lệch, nhấp nháy 0,020 → TRƯỢT',
       '(d) tỉ số bóng: 32,1 %, nhấp nháy 0,014 → TRƯỢT']),
    b('M4-trung', 'B2 · M4-trung 2026', 'Fleet St 19 m · 2/9/2026 16:30 · timelapse +2 h',
      ['34 toà thường thấy · 14 đo được (41,2 % số toà;', '92,0 % diện tích; 29,4 % khung)', '"hộp trắng" giữa-phải = toà CÓ TÊN (lớp a): giữ render'],
      ['BE-MAT-NHA (a) 0 Chặn · 0 (w) · (b) 0/255', '(c) 0 lỗi thời đại', '(d) video: 57,1 % nhà lệch; nhấp nháy 0,046 → TRƯỢT', 'N2P-*: không chạy được (KeyError, không nước — KN-1)'],
      ['khung 0 (1080p) ΔE 2,90 / p95 9,52 sau 4 vòng', '(e) 4,8/14,7 so tấm 1080p · ĐẠT so tấm 640×360', '(d) 3D: 7,1 % (1/14 toà), nhấp nháy 0,0138 (+15 %)',
       '(d) tỉ số bóng: 7,1 % (1/14), nhấp nháy ĐẠT']),
    b('B3-p4-1938', 'B3 · H3-05 P4 1938', 'Fleet St/Ludgate 40 m · 2/9/1938 15:00 · timelapse +2 h',
      ['1 248 nhà thường thấy · 153 đo được (12,3 %;', '91,7 % diện tích nhà; 41,0 % khung)', 'khối Victoria–Edward ước lượng (bậc 5)'],
      ['BE-MAT-NHA (a) 0 Chặn · (w) 1 (nhà 34226 dời?) · (b) 0/255', '(c) 0 lỗi thời đại · lượt 1: gpt 10 (w) thêm ống khói', '(d) video: 88,2 % nhà lệch; nhấp nháy 0,047 → TRƯỢT',
       'N2P-*: không chạy được (KN-1)'],
      ['khung 0 (1080p) ΔE 2,36 / p95 9,77', '(e) 4,6/12,6 so tấm 1080p · ĐẠT so tấm 640×360', '(d) 3D: 15,0 % nhà lệch, nhấp nháy ĐẠT', '(d) tỉ số bóng: 7,2 % (11/153) — KN-5']),
    d('M1-rong-hep', 'D1 · M1-rong 1666', 'P1 fov 36° · 11/9/1666 15:30 · timelapse +2 h (dải dưới)',
      ['2 275 896 tam giác', 'bão hoà TV 0,137 · trời + sương 7,0 %'],
      ['4 601 432 tam giác (×2,02)', 'bão hoà TV 0,137 · trời + sương 7,0 %', 'công trình có tên: tam giác trùng từng bit'],
      ['bão hoà TV 0,122 · trời + sương 7,0 %', 'vân nướng: 8 mặt tiền/thời kỳ + 3 mái (4 ảnh AI $0,30)', 'giây/khung: xem báo cáo §4 (đo không chạy chồng)'],
      phu=[dict(anh=f'{T}/toso/M1-rong-cuoi-{v}.png', nhan=n) for v, n in (('v2', '+2 h: V2'), ('d', '+2 h: D'), ('d2', '+2 h: D2'))]),
    d('M4-rong-hep', 'D2 · M4-rong 2026', 'P1 fov 36° · 2/9/2026 15:00',
      ['bão hoà TV 0,114 · trời + sương 7,0 %', '(cột V2 chọn ở fov 50° là V2 + tấm nền OpenAI)'],
      ['bão hoà TV 0,114 · trời + sương 7,0 %', 'lan can + phòng máy + lam ở toà KHÔNG tên', 'kính phản chiếu dải phố + trời'],
      ['bão hoà TV 0,141 · trời + sương 7,0 %', 'mặt tiền văn phòng AI (gạch 2026 giữ thủ tục)', 'giây/khung: xem báo cáo §4'])])
os.makedirs(f'{T}/toso', exist_ok=True); json.dump(C, open(f'{T}/toso/cau-hinh.json', 'w'), ensure_ascii=False, indent=1); print('ok')
