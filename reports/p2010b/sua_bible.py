#!/usr/bin/env python3
"""P-2010b · việc 2: áp các điểm chủ dự án duyệt 20/10 22:34 (báo cáo P-2010 §9) vào docs/BIBLE-KENH2.md + bỏ tên làm việc "14 Times"
trong docs/ và channel-k2/k2c-t3-01/phat-hanh/ (KHÔNG sửa loi-khoa.txt). Mỗi thay thế kiểm "đúng 1 lần xuất hiện" trước khi áp; SHA trước/sau
→ reports/p2010b/sua-bible.json. Kiểm SHA đầu vào: Kinh thánh phải là bản P-2010 (9e7492a5…). Chạy một lần."""
import hashlib, json, os, subprocess, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
B = 'docs/BIBLE-KENH2.md'; SHA_TRUOC = '9e7492a5a6742a0578dc9c06518e92a8ecc077dd345bfdefb426c1438c5631ad'
MOI_106 = ('Narration: synthetic voice. Visuals: 3D reconstructions built from the cited sources and registers. In some shots AI repaints background '
           'surfaces only (terrain, water, sky, vegetation, textures); buildings, street layout, flags, ships, people, lights, text, dates and numbers '
           'come from the sources and are never AI-generated. Segments labelled "Illustration" are fully AI-generated and carry no location facts. '
           'Historical images: public domain / CC0 / CC BY, credited.')   # = P-2010 §9 mục 3, nguyên văn (kiểm bên dưới)
KHUON = 'Gibraltar: <lời hứa> | 3D Timelapse'
SUA = {B: [
    ('tiêu đề', '§14 + sửa 20/10)', '§14 + sửa 20/10, 20/10 22:34)'),
    ('(a) §10.6',
     '- Mô tả ghi minh bạch: *"Narration: synthetic voice. Visuals: 3D reconstructions built from the cited sources and registers; on two street frames, '
     'surface detail is AI-assisted — layout, landmarks and flags come from the sources. Historical images: public domain / CC0, credited."* (§11.3)',
     f'- Mô tả ghi minh bạch (viết lại theo N1/N2 §14.1; chủ dự án duyệt 20/10 22:34): *"{MOI_106}"* (§11.3, §14.1)'),
    ('(a) §14.1 (f) theo §10.6',
     'mô tả §10.6 viết lại theo N1/N2 (câu hiện hành ở §10.6 giữ tới khi chủ dự án duyệt bản viết lại)',
     'mô tả §10.6 viết lại theo N1/N2 (đã viết lại, chủ dự án duyệt 20/10 22:34)'),
    ('(b) §11.3 bão hoà',
     '≤ 20 % tập; khung lai bão hoà trung vị ≤ 0,40 và chỉnh màu riêng; màu sơn',
     '≤ 20 % tập; khung lai theo chuẩn chung §14.4 (bão hoà trung vị ≥ 0,40; sửa 20/10 22:34); màu sơn'),
    ('(c) §11.3 Được dùng',
     '- Được dùng: (a) tấm C khung neo phố hẹp',
     '- Được dùng — VÍ DỤ của N1 (§14.1), không còn là danh sách đóng (sửa 20/10 22:34): (a) tấm C khung neo phố hẹp'),
    ('(e) §12.5 Cycles',
     '(sửa 20/10: và cú lặn/cận cảnh đêm có lửa dựng trọn bằng Cycles GPU — §14.2).',
     '(sửa 20/10: và cú lặn/cận cảnh đêm có lửa dựng trọn bằng Cycles GPU — §14.2; chủ dự án xác nhận 20/10 22:34).'),
    ('(f) §14.4 thực vật 9/1782',
     '- Mật độ bụi trước 1900 = 0,45 × hiện nay là bậc 5 TẠM (NC-D5); kết quả tra nguồn: `reports/p2010/P2010-BAO-CAO.md` §4.',
     '- Mật độ bụi trước 1900 = 0,45 × hiện nay là bậc 5 TẠM (NC-D5); kết quả tra nguồn: `reports/p2010/P2010-BAO-CAO.md` §4.\n'
     '- Thực vật mốc 9/1782 — hai ràng buộc có nguồn (chủ dự án duyệt 20/10 22:34; nguồn `reports/p2010/THUC-VAT-1782.md`, trích khớp nguyên văn tệp có SHA; '
     'hướng: bậc 2; hệ số 0,45 giữ TẠM bậc 5): (a) sườn Rock gần trơ, cây/bụi chủ yếu là cọ lùn (palmetto), không phải cây gỗ — Drinkwater 1786 tr. 49: '
     '*"The appearance of the rock is barren and forbidding ; as few trees or (hrubs, excepting palmettos, are to be feen on the face of the hill"*; '
     'Ancell 1784 tr. 40: *"Our barren rock yields but little"*; (b) tông khô cuối mùa khô (cỏ úa, bụi cọ khô; đợt tấn công lớn 13/9/1782) — '
     'Drinkwater 1786 tr. 50: *"nothing offers to the eye but fharp uncouth rocks, and dried palmetto bufhes."*'),
], 'channel-k2/k2c-t3-01/phat-hanh/titles.txt': [
    ('(d) titles THỬ 3', 'THỬ 3: Why Gibraltar Was Besieged 14 Times (35 ký tự)',
     f'THỬ 3: {KHUON} (khuôn Kinh thánh §14.5, ≤ 60 ký tự; lời hứa chờ chủ dự án chốt — tên làm việc cũ đã bỏ, chủ dự án duyệt 20/10 22:34)'),
], 'channel-k2/k2c-t3-01/phat-hanh/PACKAGING-BRIEF.md': [
    ('(d) brief bảng 1.1', '| THỬ 3 | Why Gibraltar Was Besieged 14 Times | 35 | (a) §2 "Why" | 7,42 |',
     '| THỬ 3 | Gibraltar: <lời hứa> \\| 3D Timelapse (khuôn §14.5; tên làm việc cũ đã bỏ 20/10 22:34) | ≤ 60 | (c) §14.5 | 7,42 (điểm của tên cũ) |'),
    ('(d) brief 1.4', 'Bỏ "3D Timelapse" khỏi tiêu đề và dùng **"Why Gibraltar Was Besieged 14 Times"** làm CHÍNH.',
     '(Sửa 20/10 22:34: tên làm việc cũ đã bỏ; mọi tiêu đề theo khuôn Kinh thánh §14.5 `<Nơi>: <lời hứa> | 3D Timelapse`, ≤ 60 ký tự, dữ kiện đúng lời khoá.)'),
], 'channel-k2/k2c-t3-01/phat-hanh/nguon-mo-ta.md': [
    ('(d) mô tả v1 tiêu đề', '# K2C-T3-01 "Why Gibraltar Was Besieged 14 Times":', f'# K2C-T3-01 "{KHUON}" (khuôn Kinh thánh §14.5; tên làm việc cũ đã bỏ 20/10 22:34):'),
], 'channel-k2/k2c-t3-01/phat-hanh/nguon-mo-ta-v2.md': [
    ('(d) mô tả v2 THỬ 3', 'Nếu chốt THỬ 3 ("Why Gibraltar Was Besieged 14 Times"): thay dòng 1 bằng',
     f'Nếu chốt THỬ 3 (nay theo khuôn §14.5 "{KHUON}"; tên làm việc cũ đã bỏ 20/10 22:34): dòng 1 viết lại theo lời hứa đã chốt; bản cũ để tham khảo:'),
]}
bc = open(os.path.join(R, 'reports/p2010/P2010-BAO-CAO.md'), encoding='utf-8').read()
assert f'*"{MOI_106}"*' in bc, 'bản nháp §10.6 không khớp nguyên văn P-2010 §9 mục 3'
th = open(os.path.join(R, 'reports/p2010/THUC-VAT-1782.md'), encoding='utf-8').read()
for q in ('The appearance of the rock is barren and forbidding ; as few trees or (hrubs, excepting palmettos, are to be feen on the face of the hill',
          'Our barren rock yields but little', 'nothing offers to the eye but fharp uncouth rocks, and dried palmetto bufhes.'):
    assert q in th, ('trích không khớp THUC-VAT-1782.md', q)
sha = lambda p: hashlib.sha256(open(os.path.join(R, p), 'rb').read()).hexdigest()
assert sha(B) == SHA_TRUOC, 'Kinh thánh không phải bản P-2010'
LK = 'channel-k2/k2c-t3-01/loi-khoa.txt'; lk0 = sha(LK); ghi = dict(tep={}, loi_khoa_truoc=lk0)
for p, L in SUA.items():
    s = open(os.path.join(R, p), encoding='utf-8').read(); h0 = sha(p)
    for nhan, cu, moi in L:
        n = s.count(cu)
        if n != 1: sys.exit(f'DỪNG: "{nhan}" xuất hiện {n} lần trong {p} (cần đúng 1)')
        s = s.replace(cu, moi)
    open(os.path.join(R, p), 'w', encoding='utf-8').write(s); ghi['tep'][p] = dict(truoc=h0, sau=sha(p), sua=[x[0] for x in L])
con = subprocess.run(['grep', '-rln', '14 Times', 'docs', 'channel-k2/k2c-t3-01/phat-hanh'], cwd=R, capture_output=True, text=True).stdout.split()
ghi.update(loi_khoa_sau=sha(LK), con_14_times=con); assert ghi['loi_khoa_sau'] == lk0 and not con, ghi
json.dump(ghi, open(os.path.join(R, 'reports/p2010b/sua-bible.json'), 'w'), ensure_ascii=False, indent=1); print(json.dumps(ghi, ensure_ascii=False, indent=1))
