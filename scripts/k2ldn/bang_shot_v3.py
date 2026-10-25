#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · BẢNG SHOT v3 — sinh channel-k2/k2c-t4-02/BANG-SHOT-v3.{json,md} (v1, v2 giữ nguyên).
Căn cứ (chủ dự án, giờ Asia/Saigon, 25/10/2026): 06:56 nhận xét 1–4; 07:01 N1–N6; 09:08 (chi phí là mối lo chính, các mặt khác nới để tăng độ chân thực);
09:15 "Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị"; 12:52 năm vị trí tư liệu; C1–C14 + F1–F5 theo khuyến nghị điều phối.
Gói 50 %: góc cao ≥ 50 % thân phim + 5 chốt — (1) mỗi chương mở và kết bằng shot góc cao; (2) P1 tái xuất ≥ 1 lần mỗi hồi cùng khung;
(3) ≤ 2 shot thấp / M-d / ảnh thật / tư liệu toàn khung liền nhau; (4) mỗi chương ≥ 40 % góc cao; (5) mục tiêu cảnh báo TL-1 60 % (ghi, không chặn).
≈ 80 s góc cao giải phóng → ≈ 25 s ảnh/tư liệu thật ($0) + ≈ 15 s 3D tầm phố có người/xe (look2d) + ≈ 40 s Omni (thêm góc cho 15 điểm nhấn, không thêm sự kiện).
Omni ≈ 30–35 %; TL + KHAC + THE + THAT ≤ 20 % (chủ dự án duyệt — chờ K-1.17.7; checks 1.17.6 còn trần 15 %); tổng AI ≤ 70 %; thời lượng ≤ 780 s; M-d ≤ 8 s/clip;
ảnh/tư liệu toàn khung ≤ 10 s mỗi lần, KHÔNG liền clip Omni (cách ≥ 1 shot 3D).
Lời: lời dựng v3 (scripts/k2ldn/anim/loi_v3.py: K1-C1 + N0a/N0b/N1/N2/N3/N9 mới, N4/N5/N6 sửa, N7 Churchill bỏ). Nhóm lời đặt tại t0 nhóm + 0,2 s; kiểm lời vừa nhóm.
Lớp: A cách A · N2P tấm nền · MD Omni · MAP · MAP3D · KHAC tranh khắc · THE thẻ/bộ đếm · TL tư liệu · THAT ảnh chụp/footage thật · PP.
Cú máy mới: TL (ảnh/tư liệu toàn khung, chuyển động máy 2D chậm — không AI chạm). Trang look2d = 3D tầm phố có lớp người/xe L3 (máy ≤ 60 m)."""
import collections, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anim'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'giong'))
import bang_shot_v2 as V2  # noqa: E402
import loi_v3  # noqa: E402
REPO = V2.REPO; DOME = V2.DOME; FPS = 24
DM = dict(V2.DM)
DM['P6h'] = {'ten': 'SÔNG-CẦU CAO (P6 nâng lên 125 m, nhìn tây — góc cao)', 'p': [533250, 180480, 125], 'l': [532300, 180850, 30], 'fov': 45}
DM['P10'] = {'ten': 'KING STREET 1670 (tầm phố, 38 m ODN, nhìn bắc tới Guildhall — look2d)', 'p': [532545, 181150, 38], 'l': [532550, 181420, 22], 'fov': 45}
DM['P11'] = {'ten': 'LONDON WALL 1976 (tầm phố, 45 m ODN, nhìn đông dọc đường — look2d)', 'p': [532150, 181540, 45], 'l': [532600, 181580, 25], 'fov': 45}
GOC_CAO = V2.GOC_CAO | {'P6h'}
# C6 (chủ dự án duyệt theo khuyến nghị (b)): xoay hướng nhìn P1 sang trái để mái vòm ≈ 30 % bề ngang (tính ở scripts/k2ldn/anim/may_v3.py, đo trên khung thử)
G = collections.OrderedDict([
 ('M00', 17.0), ('M01', 17.875), ('M02', 10.0833), ('M03', 11.0), ('M04', 12.0),
 ('H1-01', 11.875), ('H1-02', 8.9167), ('H1-03', 15.875), ('H1-04', 10.5833), ('H1-05', 10.6667), ('H1-06', 23.8333), ('H1-07', 15.4583), ('H1-08', 18.2083),
 ('H1-09', 13.1667), ('H1-10', 2.9167), ('H1-12', 6.4583), ('H1-11', 14.4167), ('H1-13', 20.7083), ('H1-14', 6.5), ('H1-15', 33.125), ('H1-16', 7.25), ('H1-17', 12.2917), ('H1-18', 16.2917),
 ('H2-01', 13.1667), ('H2-02', 14.625), ('H2-03', 26.1667), ('H2-04', 11.7083), ('H2-05', 18.8333), ('H2-06', 17.2917), ('H2-07', 7.9167), ('H2-08', 5.7083), ('H2-09', 10.0),
 ('H2-10', 18.0417), ('H2-11', 6.0), ('H2-12', 10.5), ('H2-13', 6.0), ('H2-14', 6.0),
 ('H3-01', 6.1667), ('H3-02', 11.2917), ('H3-03', 14.4583), ('H3-04', 10.9583), ('H3-05', 19.7083), ('H3-06', 8.0),
 ('H4-01', 12.0), ('H4-02', 10.5833), ('H4-03', 8.2917), ('H4-04', 23.0), ('H4-05', 4.5417), ('H4-06', 10.2083), ('H4-07', 5.4583), ('H4-08', 10.5),
 ('H5-01', 12.5417), ('H5-02', 14.875), ('H5-03', 6.4583), ('H5-04', 10.4167), ('H5-05', 25.625), ('H5-06', 6.0), ('H5-07', 21.3333), ('H5-08', 14.0), ('H5-09', 16.0)])
V2S = {s[0]: s for s in V2.S}
R_ = None   # độ dài = phần còn lại của nhóm


def v2(ma_v2, **k):
    """lấy nguyên shot v2 (mã, phần, nhóm, giây, máy, cú máy, thời gian, vai, lớp, thêm) rồi đè các trường đổi."""
    s = list(V2S[ma_v2]); keys = ['ma', 'phan', 'nhom', 'dur', 'dm', 'cu', 'tg', 'vai', 'lop', 'them']; d = dict(zip(keys, s)); d['them'] = dict(d['them'])
    for a, b in k.items():
        if a == 'them':
            d['them'].update(b); [d['them'].pop(x) for x in [x for x, y in b.items() if y is None]]
        else: d[a] = b
    d['nguon_v2'] = ma_v2; return d


def moi(ma, phan, nhom, dur, dm, cu, tg, vai, lop, them): return dict(ma=ma, phan=phan, nhom=nhom, dur=dur, dm=dm, cu=cu, tg=tg, vai=vai, lop=lop, them=them, nguon_v2=None)


def md(ma, phan, nhom, dur, moc, vai, clip=None, ten=(), kiem='nen', the=None, **them):
    t = dict(md=moc, md_clip=clip, nhan_vat_ten=list(ten), muc_kiem=kiem, **them)
    if the: t['the'] = the
    return dict(ma=ma, phan=phan, nhom=nhom, dur=dur, dm='—', cu='MD', tg=None, vai=vai, lop={'MD': dur}, them=t, nguon_v2=ma if clip else None)


def tl(ma, phan, nhom, dur, anh, lop, chu, vai, kb, nam):
    return dict(ma=ma, phan=phan, nhom=nhom, dur=dur, dm='—', cu='TL', tg=None, vai=vai, lop={lop: dur}, them={'tl_anh': anh, 'chu': chu, 'kb': kb, 'nam_nhan': nam}, nguon_v2=None)


D = DOME
S = [
 # ---------------- MÓC — P1 mở lạnh (P1 = A): lửa 1666 trước, hoà 1 s sang 2026 cùng khung
 moi('M00', 'MÓC', 'M00', 17.0, 'P1', 'DAY', ('h66', 19.6, 20.6), 'MỞ LẠNH (P1 = A): Bankside đêm 2/9/1666 — vòng cung lửa đang mở; N0a/N0b (Pepys)', {'A': 17.0},
     {'day_k': 0.004, 'hoa_ra': 1.0, 'nang_toi': 0.8, 'tieu_diem_en': [532700, 180900, 20], 'dung_sua': 'mới'}),
 v2('M01', cu='DAY', tg=('d', [2026, 9, 2, 14.0], [2026, 9, 2, 18.0], 1), vai='nhận ra nơi chốn: City 2026 chiều — mái vòm giữa toà cao (bỏ tấm nền tĩnh 0–11 s; cú máy DAY chậm)',
    lop={'A': 17.875}, them={'tam_nen': None, 'gio': None, 'day_k': 0.006, 'dung_sua': 'MO-DAU §3: CODINH + tấm nền → DAY, bỏ tấm nền'}),
 v2('M02'), v2('M03'), v2('M04', them={'nang_toi': 0.7, 'dung_sua': 'nâng tối γ 0,7 ở bước ghép (đêm 1 giờ sáng gần đen trên tờ khung)'}),
 # ---------------- HỒI 1
 moi('H1-01h', 'HỒI 1', 'H1-01', 3.0, 'P8', 'DAY', ('h66', 0.9, 1.05), 'mở chương (góc cao): City ngủ, đốm lửa đầu ở Pudding Lane 01:00', {'A': 3.0}, {'day_k': 0.006, 'nang_toi': 0.7, 'tieu_diem_en': [532905, 180810, 6]}),
 md('H1-01a', 'HỒI 1', 'H1-01', 5.0, 1, 'M-d (1) lò bánh bén lửa', clip='H1-01a-l1-360p', the=['Thomas Farriner (thợ làm bánh nhà vua)']),
 md('H1-01b', 'HỒI 1', 'H1-01', R_, 1, 'M-d (1) tàn lửa bay lên hẻm gỗ; hàng xóm cầm đèn', clip='H1-01b-l1-360p'),
 moi('H1-02h', 'HỒI 1', 'H1-02', 2.0, 'P2', 'DAY', ('h66', 1.8, 2.0), 'kẹp 3D (C8): lửa nhỏ giữa mái gỗ phía bắc cầu', {'A': 2.0}, {'day_k': 0.008, 'nang_toi': 0.7, 'tieu_diem_en': [532880, 180780, 10]}),
 md('H1-02', 'HỒI 1', 'H1-02', R_, 1, 'M-d (1) hẻm nhà khung gỗ tầng nhô, lửa liếm mái hiên', clip='H1-02-l1-360p'),
 v2('H1-03', dur=15.875, them={'chuyen_s': 0.0, 'dung_sua': 'M-d H1-03b (Hollar vẽ trên tháp 1647) TRƯỢT 3/3 → 3D TRUOT như v1'}),
 v2('H1-04', dur=R_, cu='DAY', tg=('h66', 7.0, 12.0), them={'day_k': 0.006, 'dung_sua': 'MO-DAU §3: CODINH → DAY chậm; M-d H1-04b (nền) trượt 2/2 ở ảnh đầu (tàu lớn, đèn, mái vòm) → 3D'}),
 md('H1-05a', 'HỒI 1', 'H1-05', 5.0, 21, 'M-d (21) DN02 Whitehall: người viết nhật ký báo tin cho nhà Vua (khung trung/xa, không cận mặt)', ten=['Samuel Pepys', 'Charles II'], kiem='day_du',
    the=['Samuel Pepys (người viết nhật ký)']),
 moi('H1-05h', 'HỒI 1', 'H1-05', 2.0, 'P6h', 'DAY', ('h66', 9.4, 9.6), 'kẹp 3D góc cao: sông trước đầu cầu cháy, thuyền rời bến', {'A': 2.0}, {'day_k': 0.008, 'tieu_diem_en': [532800, 180600, 10]}),
 md('H1-05b', 'HỒI 1', 'H1-05', R_, 2, 'M-d (2) sà lan đầy đồ đạc rời bến', clip='H1-05b-l1-360p'),
 v2('H1-06', dur=R_, tg=('h66', 12.0, 16.0), them={'cau_dz': -52, 'dung_sua': 'M-d H1-06x (DN03 sà lan hoàng gia) TRƯỢT 3/3 (mũ tricorn/áo đồng phục 1690+, tay méo) → 3D'}),
 md('H1-06b', 'HỒI 1', 'H1-06', 4.3333, 23, 'M-d (23) DN03 móc sắt dài kéo đổ mặt nhà gỗ ("pull down houses apace")'),
 v2('H1-07', dur=9.4583, them={'vong_deg': 24}),
 md('H1-07b', 'HỒI 1', 'H1-07', R_, 24, 'M-d (24) THÊM GÓC: khoảng trống 1633 trên cầu London — lửa dừng ở chỗ trống giữa hai dãy nhà trên cầu', kiem='day_du'),
 v2('H1-08b', dur=R_, tg=('h66', 17.2, 22.0), them={'khac': 'ycba-40597-0', 'dung_sua': 'M-d H1-08a (clip v1) trượt lớp CÔNG TRÌNH MỐC q_thoi_dai 1.17.7 (chân trời 1666 thiếu Old St Paul\'s) → 3D P1 cả nhóm'}),
 v2('H1-09'), md('H1-10', 'HỒI 1', 'H1-10', 7.083, 4, 'M-d (4)+(6) Watling Street / Cheapside 3/9', clip='H1-10-l1-360p', chuyen_s=4.167),
 md('H1-12', 'HỒI 1', 'H1-12', 6.4583, 3, 'M-d (3) Thames đêm 3/9: sà lan, đồ trôi, bờ bắc rực lửa', clip='H1-12-l2-360p'),
 v2('H1-11', dur=8.4167, tg=('h66', 38.0, 43.0), them={'the': ['John Evelyn (người viết nhật ký)'], 'the_anh': {'John Evelyn': 'wellcome-b6zd76cd-evelyn-nanteuil'}}),
 md('H1-11b', 'HỒI 1', 'H1-11', R_, 25, "M-d (25) DN06 sân Royal Exchange cháy: hàng tượng vua trong hốc, mái đổ", kiem='day_du'),
 v2('H1-13', ma='H1-13a', dur=7.0, tg=('h66', 66.0, 67.3), vai="lửa leo đồi Ludgate tới Old St Paul's bọc giàn giáo gỗ (3D thấp)", lop={'A': 7.0}, them={'chuyen_s': 0.0, 'khac': None}),
 moi('H1-12x', 'HỒI 1', 'H1-13', 7.5, 'P9', 'DAY', ('y', 1666.655, 1666.6551, [8, 27, 15.0], 0), "DN01: sáu ngày trước cháy — Old St Paul's bọc giàn giáo (Evelyn + Wren khảo sát, đề xuất mái vòm); tranh Hollar từ phía Đông",
     {'A': 7.5, 'KHAC': 5.0, 'THE': 4.0}, {'day_k': 0.006, 'khac': 'met-395057-0', 'nhan': '27 AUG 1666', 'tieu_diem_en': [532080, 181140, 60],
      'the': ['John Evelyn · Christopher Wren'], 'the_anh': {'John Evelyn · Christopher Wren': 'nga-wren-0'}}),
 v2('H1-13', ma='H1-13c', dur=R_, tg=('h66', 68.0, 69.5), vai="Old St Paul's bốc cháy tối 4/9 (3D thấp; M-d H1-13c: Omni từ chối 3/3 INVALID_ARGUMENT, $0 → 3D)", lop={'A': 6.2}, them={'chuyen_s': 0.0, 'khac': None}),
 md('H1-14', 'HỒI 1', 'H1-14', 6.5, 5, "M-d (5) DN05 + C12: mái nhà thờ lớn sập, chì chảy thành dòng xuống phố", kiem='day_du'),
 v2('H1-15', dur=8.0, tg=('h66', 68.0, 69.4), them={'cau_dz': 40, 'f4': True}),
 md('H1-15m', 'HỒI 1', 'H1-15', 6.0, 27, 'M-d (27) THÊM GÓC: nổ thuốc súng mở khoảng chặn lửa trên phố (Tower Street)'),
 md('H1-15b', 'HỒI 1', 'H1-15', 7.5, 28, 'M-d (28) Navy Office: hai người đào hố trong vườn chôn rượu và phô mai Parmesan (khung xa)', ten=['Samuel Pepys'], kiem='day_du'),
 moi('H1-15h', 'HỒI 1', 'H1-15', R_, 'P3', 'DAY', ('h66', 70.0, 71.6), 'tuyến chặn lửa phía tây — lời N3 (M-d H1-15x DN04 TRƯỢT 3/3: mặt/tay méo → 3D)', {'A': 11.625}, {'day_k': 0.008, 'tieu_diem_en': [532300, 181050, 10], 'f4': True}),
 v2('H1-16', them={'khac': 'rijks-luyken-0'}),
 md('H1-17a', 'HỒI 1', 'H1-17', 6.0, 7, 'M-d (7) Moorfields: lều, chòi, đống đồ cứu được', clip='H1-17a-l1-360p'),
 md('H1-17b', 'HỒI 1', 'H1-17', R_, 7, 'M-d (7) Moorfields chạng vạng', clip='H1-17b-l1-360p'),
 v2('H1-18', ma='H1-18a', dur=6.0, tg=('h66', 128.0, 129.5), lop={'A': 6.0, 'THE': 4}, vai='phế tích 7/9 nhìn thẳng xuống → xiên; bộ đếm 13 200 nhà / 87 nhà thờ', them={'xuong': {'tu': 0.0}}),
 tl('H1-18t', 'HỒI 1', 'H1-18', 5.0, 'met-360649-0', 'KHAC', 'Hollar: London after the Fire, 1666', 'tư liệu toàn khung (12:52): tấm Hollar SAU cháy — dải phế tích', {'tu': [0.3, 0.5, 1.0], 'den': [0.7, 0.5, 1.0], 'phu': True}, '1666'),
 v2('H1-18', ma='H1-18b', dur=R_, cu='CODINH', tg=('h66', 129.5, 131.0), lop={'A': 5.2917, 'MAP3D': 5.0}, vai='ranh vùng cháy 1666 chiếu trên phế tích (kết chương góc cao)', them={'xuong': None, 'xuong_cuoi': True, 'ranh66': True}),
 # ---------------- HỒI 2
 moi('H2-00', 'HỒI 2', 'H2-01', 3.0, 'P5', 'DAY', ('y', 1666.72, 1666.72, [9, 16, 11.0], 0), 'mở chương (góc cao): City cháy trụi, khói mỏng, tháp nhà thờ cháy dở', {'A': 3.0}, {'day_k': 0.006, 'tieu_diem_en': [532300, 181000, 10]}),
 md('H2-01a', 'HỒI 2', 'H2-01', 5.0, 8, 'M-d (8) lối đi giữa tro còn nóng', clip='H2-01a-l1-360p'),
 md('H2-01b', 'HỒI 2', 'H2-01', R_, 30, 'M-d (30) DN06 tượng Gresham rơi khỏi hốc còn nguyên giữa tro Royal Exchange (Evelyn 7/9)', kiem='day_du'),
 v2('H2-02', lop={'A': 14.625, 'TL': 8, 'MAP3D': 4, 'THE': 7}, them={'dung_sua': 'M-d H2-02b TRƯỢT 3/3 (mũ tricorn; tháp kiểu Big Ben qua cửa sổ) → 3D cả nhóm', 'the': ['Christopher Wren', 'Charles II', 'Robert Hooke'],
    'the_anh': {'Christopher Wren': 'nga-wren-0', 'Charles II': 'met-435943-charles2-cooper'}}),
 v2('H2-03b', dur=R_, cu='DAY', tg=('y', 1667.05, 1667.45, [3, 10, 13.0], 0), them={'day_k': 0.008, 'dung_sua': 'CODINH → DAY chậm; M-d H2-03a (clip v1) trượt lớp CÔNG TRÌNH MỐC (thiếu tàn tích Old St Paul\'s) → 3D'}),
 md('H2-03c', 'HỒI 2', 'H2-03', 6.0, 19, 'M-d (19) Toà Cháy 1667', clip='H2-03c-l1-360p'),
 moi('H2-04h', 'HỒI 2', 'H2-04', 2.5, 'P2', 'NGHIENG', ('y', 1667.6, 1667.9, [6, 1, 11.0], 0), 'kẹp 3D góc cao: nhà gạch mọc dọc phố cũ', {'A': 2.5}, {'nghieng_deg': 3, 'tieu_diem_en': [532300, 181050, 20]}),
 v2('H2-04a', dur=3.5, tg=('y', 1667.9, 1668.4, [6, 1, 11.0], 0), them={'page': 'look2d', 'f2': True}),
 md('H2-04b', 'HỒI 2', 'H2-04', R_, 11, 'M-d (11) xe chở gạch, giàn giáo gỗ', clip='H2-04b-l1-360p'),
 v2('H2-05', dur=11.0, tg=('y', 1668.0, 1670.2, [9, 1, 15.0], 0)),
 moi('H2-05s', 'HỒI 2', 'H2-05', R_, 'P10', 'TRUOT', ('y', 1670.2, 1671.0, [9, 1, 14.0], 0), '3D TẦM PHỐ (look2d): King Street mới cắt về Guildhall — xe ngựa, người, nhà gạch', {'A': 7.8333},
     {'page': 'look2d', 'tieu_diem_en': [532550, 181400, 20]}),
 v2('H2-06', dur=R_, them={'vong_deg': 26, 'dung_sua': 'M-d H2-06b (DN09 đá Portland) TRƯỢT 3/3 ở ảnh đầu (mái vòm St Paul\'s năm 1675 — lỗi thời đại) → 3D VONG cả nhóm'}),
 md('H2-07', 'HỒI 2', 'H2-07', 7.9167, 13, 'M-d (13) phố gạch 1680 + dấu bảo hiểm cháy', clip='H2-07-l2-360p', the=['Nicholas Barbon']),
 v2('H2-08'),
 v2('H2-09', dur=R_, them={'dung_sua': 'M-d H2-09x (DN08 viên đá đầu tiên 1675) TRƯỢT 3/3 (tay/người biến dạng — Flash) → 3D P1 cả nhóm'}),
 v2('H2-10', them={'thap_nghieng_deg': 3, 'dung_sua': 'M-d H2-10b (DN10) TRƯỢT 3/3 ở ảnh đầu (cầu đá chưa có năm 1708, tàu lớn) → 3D cả nhóm'}),
 v2('H2-11'), v2('H2-12', dur=10.5, tg=('khop', ('y', 1647.0, 1647.0, [9, 1, 15.0], 0), ('y', 1711.0, 1711.0, [9, 1, 15.0], 0), 5.25)),
 md('H2-13', 'HỒI 2', 'H2-13', 6.0, 12, "M-d (12) F1 Thames 1711: đò chở khách; chân trời có MÁI VÒM St Paul's mới (không chóp Gothic)", kiem='day_du'),
 v2('H2-14'),
 # ---------------- HỒI 3
 v2('H3-01', dur=3.0, tg=('y', 1711.0, 1800.0, [9, 1, 15.0], 0)),
 tl('H3-01t', 'HỒI 3', 'H3-01', R_, 'rijks-200323435-theems-stpauls-1892', 'THAT', "St Paul's from the Thames, 1892", 'ẢNH THẬT toàn khung (P6): mái vòm vẫn cao nhất chân trời (Rijksmuseum, PDM) — thay phần footage H5-07a không tải được', {'tu': [0.5, 0.5, 1.0], 'den': [0.5, 0.45, 1.12]}, '1892'),
 v2('H3-02', dm='P6h', dur=6.7917, tg=('y', 1756.0, 1832.0, [9, 1, 15.0], 0), them={'dung_sua': 'P6 nâng 35 → 125 m (góc cao)'}),
 tl('H3-02t', 'HỒI 3', 'H3-02', R_, 'loc-2002696930-londonbridge-pc', 'THAT', 'London Bridge (1831), c. 1890–1900', 'ẢNH THẬT toàn khung: cầu London mới (photochrom LoC)', {'tu': [0.5, 0.5, 1.0], 'den': [0.55, 0.48, 1.12]}, '1900'),
 v2('H3-03', dur=9.4583, lop={'A': 9.4583, 'MAP3D': 4, 'KHAC': 3.0, 'THE': 3.5}, them={'khac': 'wellcome-uv3mugch-embankment-1865', 'the': ['Joseph Bazalgette (kỹ sư)'], 'the_anh': {'Joseph Bazalgette (kỹ sư)': 'rijks-200348829-bazalgette'}}),
 tl('H3-03t', 'HỒI 3', 'H3-03', R_, 'loc-2002696941-embankment-pc', 'THAT', 'Victoria Embankment, c. 1890–1900', 'ẢNH THẬT toàn khung: kè Victoria (photochrom LoC)', {'tu': [0.45, 0.5, 1.12], 'den': [0.55, 0.5, 1.0]}, '1900'),
 v2('H3-04a', dur=5.0, tg=('y', 1900.0, 1937.0, [9, 1, 15.0], 0)),
 md('H3-04b', 'HỒI 3', 'H3-04', R_, 14, 'M-d (14) hẻm City 1930s', clip='H3-04b-l1-360p'),
 md('H3-05b', 'HỒI 3', 'H3-05', 6.0, 35, 'M-d (35) 1937: người khảo sát đặt máy kinh vĩ trên mái nhà, ngắm mái vòm (khung xa)', ten=['Godfrey Allen'], kiem='day_du'),
 v2('H3-05', dm='P9', dur=R_, cu='DAY', tg=('y', 1937.0, 1938.5, [9, 1, 16.0], 0), them={'day_k': 0.006, 'dung_sua': 'THAP P4b → P9 góc cao (5 chốt (3)); vành Heights từ 4 s'}),
 v2('H3-06'),
 # ---------------- HỒI 4
 v2('H4-01a'), md('H4-01b', 'HỒI 4', 'H4-01', 6.0, 15, 'M-d (15) phố City vắng chiều Chủ nhật 1940', clip='H4-01b-l1-360p'),
 v2('H4-02', them={'dung_sua': 'M-d H4-02b (nền) TRƯỢT 2/2 ở ảnh đầu (đèn đường sáng giữa giờ tắt đèn) → 3D'}),
 md('H4-03', 'HỒI 4', 'H4-03', 8.0, 16, 'M-d (16) vòi rồng trên bãi bùn triều thấp', clip='H4-03-l1-360p', chuyen_s=-0.292),
 v2('H4-04a', dm='P5', cu='DAY', dur=7.5, them={'day_k': 0.008, 'dung_sua': 'THAP P4b → P5 góc cao (5 chốt (3))', 'tieu_diem_en': [532118, 181150, 60]}),
 md('H4-04b', 'HỒI 4', 'H4-04', 6.5, 17, "M-d (17) St Paul's Watch trên mái chì", clip='H4-04b-l3-360p'),
 v2('H4-04c', dur=4.0, tg=('h40', 5.0, 5.4)),
 md('H4-04d', 'HỒI 4', 'H4-04', R_, 38, "M-d (38) THÊM GÓC DN13: mái Guildhall cháy", kiem='day_du'),
 v2('H4-05'),
 v2('H4-06', dur=5.2083, tg=('h40', 14.0, 18.0)),
 tl('H4-06t', 'HỒI 4', 'H4-06', R_, 'commons-iwm-d6418', 'THAT', "St Paul's, January 1942", 'ẢNH THẬT toàn khung (P6): MoI Crown, IWM D 6418 — mái vòm sau Blitz (chú thích đúng năm)', {'tu': [0.5, 0.45, 1.0], 'den': [0.5, 0.4, 1.12]}, '1942'),
 v2('H4-07'), v2('H4-08', dur=10.5, tg=('khop', ('h66', 130.0, 132.0), ('y', 1941.3, 1941.3, [3, 1, 13.0], 0), 5.25)),
 # ---------------- HỒI 5
 v2('H5-01', cu='DAY', them={'day_k': 0.006, 'dung_sua': 'MO-DAU §3: CODINH → DAY chậm; M-d H5-01b TRƯỢT 3/3 (mặt/tay méo) → 3D'}),
 v2('H5-02', dur=7.875, tg=('y', 1957.0, 1971.0, [9, 1, 15.0], 1), them={'cau_dz': -40}),
 moi('H5-02s', 'HỒI 5', 'H5-02', R_, 'P11', 'TRUOT', ('y', 1976.0, 1976.0, [9, 1, 15.0], 1), '3D TẦM PHỐ (look2d): đường London Wall 1976 — ô tô, xe buýt, người; Barbican', {'A': 7.0},
     {'page': 'look2d', 'tieu_diem_en': [532600, 181580, 25]}),
 v2('H5-03'), v2('H5-04', lop={'A': 10.4167}, them={'tam_nen': None, 'tam_nen_tu': None, 'dung_sua': 'bỏ tấm nền P1-2026 (C6 xoay P1 4° → tấm AI cũ lệch khung; không làm tấm mới vòng này)'}),
 v2('H5-05a', dur=6.0, tg=('d', [2026, 9, 2, 17.0], [2026, 9, 2, 17.1], 1), lop={'A': 6.0, 'N2P': 6.0}, them={'tam_nen': [0, 6.0], 'dung_sua': 'C14: tấm nền ≤ 6 s'}),
 moi('H5-05c', 'HỒI 5', 'H5-05', 10.5, 'P2', 'VONG', ('d', [2026, 9, 2, 17.1], [2026, 9, 2, 17.5], 1), 'C14 biến cố thật: vòng quanh mái vòm từ bờ nam, nắng chiều dịch — tầm nhìn bảo vệ',
     {'A': 10.5}, {'vong_deg': 20, 'tam': DOME, 'tieu_diem_en': DOME}),
 v2('H5-05b', dur=R_, them={'thap_nghieng_deg': 3}),
 v2('H5-06'),
 v2('H5-07a', cu='DAY', tg=('d', [2026, 9, 2, 22.0], [2026, 9, 2, 22.15], 1), them={'day_k': 0.006, 'dung_sua': 'P7 footage C3 (Commons CC BY 3.0) KHÔNG tải được (Commons 429 ≈ 2 h; Pixabay X1/Pexels 403 Cloudflare) → 3D P9 đêm, DAY chậm; chủ dự án tải tay'}),
 v2('H5-07b'), v2('H5-08', dur=14.0), v2('H5-09'),
]
MD_MOC = dict(V2.MD_MOC); MD_MOC.update({5: "mái nhà thờ lớn sập, chì chảy (DN05 + C12)", 12: "Thames 1711 + mái vòm mới (F1)", 20: 'Fish Street Hill sáng 2/9', 21: 'Whitehall: Pepys báo Vua (DN02)', 22: 'sà lan hoàng gia (DN03)',
               23: 'móc sắt phá nhà (DN03)', 24: 'khoảng trống 1633 trên cầu London', 25: 'Royal Exchange cháy (DN06)', 26: "giàn giáo Old St Paul's bén lửa (DN05)", 27: 'nổ thuốc súng mở khoảng chặn',
               28: 'Navy Office: chôn rượu + Parmesan', 29: 'Vua + Công tước chữa cháy (DN04)', 30: 'tượng Gresham (DN06)', 31: 'bản vẽ Wren (DN07)', 32: 'đá Portland lên Monument (DN09)',
               33: "viên đá đầu tiên 1675 (DN08)", 34: 'viên đá cuối đèn lồng 1708 (DN10)', 35: 'người khảo sát 1937 (DN15 Heights)', 36: 'Hollar vẽ từ St Saviour 1647', 37: 'bom cháy rơi 29/12/1940 (DN13)',
               38: 'mái Guildhall cháy (DN13)', 39: 'nhà quy hoạch 1946–47 (DN14)'})
NON_CAO = ('thap', 'md', 'tl')


def main():
    LV = loi_v3.nhom()
    # điền độ dài "phần còn lại"
    by = collections.defaultdict(list)
    for s in S: by[s['nhom']].append(s)
    for g, ss in by.items():
        r = [s for s in ss if s['dur'] is None]; assert len(r) <= 1, g
        if r:
            r[0]['dur'] = round(G[g] - sum(s['dur'] for s in ss if s['dur'] is not None) + sum(s['them'].get('chuyen_s', 0) for s in ss), 4)
            if 'A' in r[0]['lop'] or not r[0]['lop'] or r[0]['cu'] not in ('MD', 'TL'): r[0]['lop'] = {k: (r[0]['dur'] if k == 'A' else v) for k, v in (r[0]['lop'] or {'A': 0}).items()}
            if r[0]['cu'] == 'MD': r[0]['lop'] = {'MD': r[0]['dur']}
            if r[0]['cu'] == 'TL': r[0]['lop'] = {k: r[0]['dur'] for k in r[0]['lop']}
    for s in S:
        if s['cu'] not in ('MD', 'TL', 'PP') and 'A' in s['lop']: s['lop']['A'] = s['dur']
        if s['cu'] == 'MD': s['lop']['MD'] = s['dur']
    loi = []
    for g, ss in by.items():
        tot = sum(s['dur'] for s in ss) - sum(s['them'].get('chuyen_s', 0) for s in ss)
        if abs(tot - G[g]) > 2e-3: loi.append(f'{g}: shot {tot:.4f} ≠ nhóm {G[g]}')
        if g in LV and 0.2 + LV[g]['loi_s'] > G[g] + 1e-3: loi.append(f'{g}: lời {LV[g]["loi_s"]:.3f} + 0,2 > nhóm {G[g]}')
    assert set(by) == set(G), set(G) ^ set(by)
    if abs(sum(s['dur'] for s in S) - sum(G.values())) > 2e-3: loi.append(f"tổng shot {sum(s['dur'] for s in S):.4f} ≠ tổng nhóm {sum(G.values()):.4f}")
    assert not [g for g in LV if g not in G], [g for g in LV if g not in G]
    rows, t, nhom_t0 = [], 0.0, collections.OrderedDict()
    for g in G: nhom_t0[g] = round(t, 4); t += G[g]
    T = round(t, 4); t = 0.0
    for s in S:
        ma, dm, cu, them = s['ma'], s['dm'], s['cu'], s['them']
        may = (dict(DM[dm], fov=them['fov']) if dm in DM and 'fov' in them else DM.get(dm))
        cau = LV.get(s['nhom'], {}).get('cau', []) if by[s['nhom']][0] is s else []
        goc = 'cao' if dm in GOC_CAO else ('md' if cu == 'MD' else ('pp' if cu == 'PP' else ('tl' if cu == 'TL' else 'thap')))
        r = {'ma': ma, 'phan': s['phan'], 'chuong': s['phan'], 'nhom_loi': s['nhom'], 'bat_dau_s': round(t, 4), 'giay': s['dur'], 't0': round(t, 4), 't1': round(t + s['dur'], 4), 'dur': s['dur'],
             'cau_loi': [c['khoa'] for c in cau], 'diem_may': dm, 'may': may, 'cu_may': cu, 'loai_may': cu, 'thoi_gian': s['tg'], 'vai': s['vai'], 'lop': {k: round(v, 4) for k, v in s['lop'].items() if v},
             'goc': goc, 'tl': cu not in ('MD', 'PP', 'TL'), 'minh_hoa': cu == 'MD', 'ai_nen': bool(them.get('tam_nen')), 'tieu_diem_en': them.get('tieu_diem_en'), 'them': them,
             'trang': them.get('page', 'look2') if cu not in ('MD', 'PP', 'TL') else None, 'nguon_v2': s['nguon_v2'], 'loi_bd_s': round(nhom_t0[s['nhom']] + 0.2, 4) if cau else None}
        if cu == 'KHOP': r.update(khop_voi=them['khop_voi'], hoa_s=them['hoa_s'], diem_neo=them.get('tieu_diem_en'))
        if cu == 'KEO': r['lo_ra'] = them['lo_ra']
        if cu == 'MD': r.update(md_moc=them['md'], md_ten=MD_MOC[them['md']], nhan_vat_ten=them['nhan_vat_ten'], muc_kiem=them['muc_kiem'], md_clip=them['md_clip'])
        if cu == 'MD' and them['md_clip']:   # clip v1 giữ phải đúng lượt v1 đã chọn (sự cố 25/10: H1-12, H2-07 lấy nhầm l1 LOẠI)
            _c = open(os.path.join(REPO, 'channel-k2/k2c-t4-02/animatic/omni/chon', ma + '.txt')).read().strip(); assert them['md_clip'] == _c, (ma, them['md_clip'], _c)
        if cu == 'TL': r.update(tl_anh=them['tl_anh'], lop_tl=list(s['lop'])[0])
        rows.append(r); t += s['dur']
    for r in rows:
        Ls = sorted({c['L'] for g in [r['nhom_loi']] for c in LV.get(g, {}).get('cau', []) if c['L']}, key=lambda x: int(x[1:3]) if x[1:3].isdigit() else 0)
        Ns = [c['N'] for c in LV.get(r['nhom_loi'], {}).get('cau', []) if c['N']]
        lab = (f"{Ls[0]}–{Ls[-1]}" if len(Ls) > 1 else (Ls[0] if Ls else '')) + ((' + ' if Ls else '') + ', '.join(Ns) if Ns else '')
        anh = [x['ma'] for x in rows if x['nhom_loi'] == r['nhom_loi']]
        r['loi'] = (lab or ('(lặng)' if r['cu_may'] != 'PP' else '—')) + (f" (nhóm {r['nhom_loi']}: {', '.join(anh)})" if len(anh) > 1 else '')
    L = collections.Counter()
    for r in rows:
        for k, v in r['lop'].items(): L[k] += v
    than = T - L['PP']; pct = {k: round(100 * v / T, 2) for k, v in L.items()}
    cao = sum(r['dur'] for r in rows if r['goc'] == 'cao') - sum(r['them']['ban_do']['s'] for r in rows if 'ban_do' in r['them'])
    md_s = L['MD']; tlx = L['TL'] + L['KHAC'] + L['THE'] + L['THAT']
    look2d = sum(r['dur'] for r in rows if r.get('trang') == 'look2d')
    tong = {'thoi_luong_s': T, 'so_shot': len(rows), 'shot_tb_s': round(T / len(rows), 2), 'lop_s': {k: round(v, 3) for k, v in L.items()}, 'lop_pct': pct, 'than_phim_s': round(than, 3),
            'MD_pct': round(100 * md_s / T, 2), 'N2P_pct': pct.get('N2P', 0), 'AI_pct': round(100 * (L['N2P'] + md_s) / T, 2), 'MAP_ALL_pct': round(100 * (L['MAP'] + L['MAP3D']) / T, 2),
            'TL_KHAC_THE_pct': round(100 * (L['TL'] + L['KHAC'] + L['THE']) / T, 2), 'TL_KHAC_THE_THAT_pct': round(100 * tlx / T, 2), 'THAT_s': round(L['THAT'], 3),
            'TL_toan_khung_s': round(sum(r['dur'] for r in rows if r['cu_may'] == 'TL'), 3), 'look2d_s': round(look2d, 3),
            'THAP_pct': round(100 * sum(r['dur'] for r in rows if r['goc'] == 'thap') / T, 2), 'goc_cao_s': round(cao, 3), 'goc_cao_than_phim_pct': round(100 * cao / than, 2),
            'md_clip': sum(1 for r in rows if r['cu_may'] == 'MD'), 'md_moi': sum(1 for r in rows if r['cu_may'] == 'MD' and not r['md_clip']),
            'md_moi_s': round(sum(r['dur'] for r in rows if r['cu_may'] == 'MD' and not r['md_clip']), 3)}
    kiem = []
    def k_(ten, v, cap=None, duoi=None, dat=None, ghi=''):
        d = dat if dat is not None else ((cap is None or v <= cap) and (duoi is None or v >= duoi))
        near = lambda n: n not in (None, 0) and isinstance(v, (int, float)) and not isinstance(v, bool) and abs(v - n) <= 0.05 * abs(n)
        kiem.append({'chi_so': ten, 'gia_tri': v, 'tran': cap, 'san': duoi, 'dat': d, 'trong_5pct': near(cap) or near(duoi), 'ghi': ghi})
    k_('Nhóm lời khớp, lời vừa nhóm', len(loi), cap=0, ghi='; '.join(loi))
    k_('Thời lượng ≤ 780 s', T, cap=780)
    k_('Góc cao / thân phim % (gói 50 %: ≥ 50)', tong['goc_cao_than_phim_pct'], duoi=50, ghi='ước theo điểm máy (≥ 120 m); số đo thật: k2check theo log khung')
    k_('Mục tiêu cảnh báo TL-1: góc cao ≥ 60 % (chốt 5, không chặn)', tong['goc_cao_than_phim_pct'], duoi=60, ghi='chỉ cảnh báo (gói 50 %)')
    k_('Omni % (≈ 30–35, mục tiêu gần đúng)', tong['MD_pct'], cap=35, duoi=30, dat=28.5 <= tong['MD_pct'] <= 36.75, ghi='≈: đạt khi trong ±5 % quanh dải; dưới 30 vì 11 clip v3 trượt hết lượt + 2 clip v1 trượt lớp mốc 1.17.7 (H1-08a, H2-03a) về 3D (H1-03b, H1-04b, H1-06x, H1-13c, H1-15x, H2-02b, H2-06b, H2-09x, H2-10b, H4-02b, H5-01b) — không thêm clip chỉ để vượt ngưỡng; xem PHIEU-XEM-V2 C')
    k_('TL + KHAC + THE + THAT % (≤ 20, chủ dự án duyệt — chờ K-1.17.7)', tong['TL_KHAC_THE_THAT_pct'], cap=20)
    k_('TU-LIEU 1.17.6: TL + KHAC + THE + THAT % (≤ 15)', tong['TL_KHAC_THE_THAT_pct'], cap=15, ghi='chờ K-1.17.7 (20 %)')
    k_('Tổng AI % (≤ 70)', tong['AI_pct'], cap=70)
    k_('Bản đồ MAP + MAP3D % (≤ 12)', tong['MAP_ALL_pct'], cap=12)
    k_('THAP % (≤ 12)', tong['THAP_pct'], cap=12)
    k_('M-d mỗi clip ≤ 8 s', max(r['dur'] for r in rows if r['cu_may'] == 'MD'), cap=8.0)
    k_('Ảnh/tư liệu toàn khung mỗi lần ≤ 10 s', max(r['dur'] for r in rows if r['cu_may'] == 'TL'), cap=10.0)
    k_('Ảnh/tư liệu thật toàn khung ≈ 25 s', tong['TL_toan_khung_s'], duoi=20, cap=30)
    k_('3D tầm phố mới (look2d) ≈ 15 s', round(sum(r['dur'] for r in rows if r.get('trang') == 'look2d' and not r['nguon_v2']), 3), duoi=12, cap=18)
    k_('Ảnh/tư liệu toàn khung KHÔNG liền clip Omni', '', dat=all(not (rows[i]['cu_may'] == 'TL' and ((i and rows[i - 1]['cu_may'] == 'MD') or (i + 1 < len(rows) and rows[i + 1]['cu_may'] == 'MD'))) for i in range(len(rows))))
    k_('N2P chỉ trên CODINH, chỉ 2026 ban ngày', '', dat=all(r['cu_may'] == 'CODINH' and r['thoi_gian'][0] in ('d', 'y') for r in rows if r['ai_nen']))
    k_('M-d không liền PP, không cuối phim', '', dat=all(i + 1 < len(rows) and rows[i + 1]['cu_may'] != 'PP' and (not i or rows[i - 1]['cu_may'] != 'PP') for i, r in enumerate(rows) if r['cu_may'] == 'MD'))
    run, mx, where = 0, 0, ''
    for r in rows:
        if r['cu_may'] == 'PP': run = 0; continue
        run = run + 1 if r['goc'] in NON_CAO else 0
        if run > mx: mx, where = run, r['ma']
    k_('Chốt 3: ≤ 2 shot thấp/M-d/ảnh thật liền nhau', mx, cap=2, ghi=f'dài nhất kết ở {where}')
    ch = collections.OrderedDict()
    for r in rows:
        if r['cu_may'] != 'PP': ch.setdefault(r['phan'], []).append(r)
    per = {}
    for ph, rs in ch.items():
        c = sum(r['dur'] for r in rs if r['goc'] == 'cao') - sum(r['them']['ban_do']['s'] for r in rs if 'ban_do' in r['them']); tot = sum(r['dur'] for r in rs); per[ph] = round(100 * c / tot, 2)
        k_(f'Chốt 1 {ph}: mở và kết bằng góc cao', f"{rs[0]['ma']} / {rs[-1]['ma']}", dat=rs[0]['goc'] == 'cao' and rs[-1]['goc'] == 'cao')
        k_(f'Chốt 4 {ph}: góc cao ≥ 40 %', per[ph], duoi=40)
        if ph != 'MÓC': k_(f'Chốt 2 {ph}: P1 tái xuất (fov 36°, cùng khung)', ', '.join(r['ma'] for r in rs if r['diem_may'] == 'P1'), dat=any(r['diem_may'] == 'P1' for r in rs))
        loai = {r['cu_may'] for r in rs if r['cu_may'] not in ('MD', 'PP', 'TL')}
        k_(f'{ph}: số loại cú máy ≥ 4', len(loai), duoi=4 if ph != 'MÓC' else 3)
    tong['goc_cao_chuong_pct'] = per
    out = {'nhom_loi_t0': nhom_t0, 'nhom_s': G, 'tap': 'K2C-T4-02', 'phien': 'ANIMATIC-T4-V2', 'ngay': '2026-10-25', 'loi': 'v3 (loi-khoa-v3.txt; scripts/k2ldn/anim/loi_v3.py)', 'diem_may': DM, 'shot': rows,
           'tong': tong, 'kiem': kiem, 'md_moc': MD_MOC, 'mo_ta_lop': 'giây trong shot; THE/KHAC/TL/MAP3D chồng trên A; TL/THAT toàn khung ở shot cu_may = TL'}
    EP = os.path.join(REPO, 'channel-k2/k2c-t4-02')
    json.dump(out, open(os.path.join(EP, 'BANG-SHOT-v3.json'), 'w'), ensure_ascii=False, indent=1)
    md_ = ['# BẢNG SHOT v3 — K2C-T4-02 London (ANIMATIC-T4-V2, 25/10/2026)', '',
           '> Sinh bằng `scripts/k2ldn/bang_shot_v3.py` (nguồn thật của bảng). Bản máy đọc: `BANG-SHOT-v3.json`. v1, v2 giữ nguyên.',
           '> Căn cứ: chủ dự án 25/10/2026 (giờ Asia/Saigon) 06:56 / 07:01 / 09:08 / 09:15 "Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị" / 12:52 (5 vị trí tư liệu); C1–C14, F1–F5 theo khuyến nghị điều phối.',
           '> Lời v3: `loi-khoa-v3.txt`; mỗi **nhóm** lời đặt ở đầu nhóm + 0,2 s. Góc: cao = máy ≥ 120 m; thap = 3D thấp (gồm look2d tầm phố); md = Omni; tl = ảnh/tư liệu toàn khung.', '',
           '## Điểm máy', '', '| Mã | Tên | Vị trí E, N, h (m) | Nhìn tới | FOV dọc |', '|---|---|---|---|---|']
    for k, v in DM.items(): md_.append(f"| {k} | {v['ten']} | {v['p']} | {v['l']} | {v['fov']}° |")
    md_ += ['', '## Bảng', '', '| Mã | t | Dài (s) | Lời | Máy | Cú máy | Góc | Thời gian | Vai truyện | Lớp | Ghi |', '|---|---|---|---|---|---|---|---|---|---|---|']
    def tgs(tg):
        if not tg: return '—'
        if tg[0] == 'd': return f"{tg[1][2]}/{tg[1][1]}/{tg[1][0]} {tg[1][3]:g}h → {tg[2][3]:g}h"
        if tg[0] == 'h66': return f"lửa 1666 giờ {tg[1]:g} → {tg[2]:g}"
        if tg[0] == 'h40': return f"29/12/1940 18:00 + {tg[1]:g} → {tg[2]:g} h"
        if tg[0] == 'y': return f"{tg[1]:g} → {tg[2]:g}" if tg[1] != tg[2] else f"{tg[1]:g}"
        if tg[0] == 'khop': return f"KHOP: {tgs(tg[1])} ↔ {tgs(tg[2])} (cắt {tg[3]:g} s)"
    for r in rows:
        m, s_ = divmod(r['t0'], 60); g = []; th = r['them']
        if th.get('the'): g.append('thẻ: ' + '; '.join(th['the']))
        if th.get('dem'): g.append('bộ đếm: ' + ' / '.join(th['dem']))
        if th.get('khac'): g.append('góc khung: ' + th['khac'])
        if th.get('tam_nen'): g.append(f"tấm nền {th['tam_nen'][0]:g}–{th['tam_nen'][1]:g} s")
        if r.get('khop_voi'): g.append(f"KHOP với {r['khop_voi']}")
        if r['cu_may'] == 'MD': g.append(('clip v1 ' + r['md_clip']) if r['md_clip'] else f"MỚI · kiểm {r['muc_kiem']}" + (' · nhân vật: ' + ', '.join(r['nhan_vat_ten']) if r['nhan_vat_ten'] else ''))
        if r['cu_may'] == 'TL': g.append(f"{r['lop_tl']}: {r['tl_anh']} — \"{th['chu']}\"")
        if r.get('trang') == 'look2d': g.append('look2d (người/xe)')
        if th.get('dung_sua'): g.append(th['dung_sua'])
        if th.get('chuyen_s'): g.append(f"chuyển {th['chuyen_s']:+.3f} s")
        md_.append(f"| {r['ma']} | {int(m)}:{s_:04.1f} | {r['dur']:.3f} | {r['loi']} | {r['diem_may']} | {r['cu_may']} | {r['goc']} | {tgs(r['thoi_gian'])} | {r['vai']} | {', '.join(f'{k} ({v:g})' for k, v in r['lop'].items())} | {'; '.join(g)} |")
    md_ += ['', '## Tổng + tự kiểm trước dựng', '', f"- Thời lượng **{T:.3f} s** · **{len(rows)} shot** · TB {tong['shot_tb_s']} s · Omni {tong['md_clip']} clip ({tong['md_moi']} mới/đổi, {tong['md_moi_s']} s).",
            f"- Lớp (s): {tong['lop_s']}", f"- Góc cao từng chương %: {per}", '', '| Chỉ số | Giá trị | Trần | Sàn | Đạt | ±5 % quanh ngưỡng | Ghi |', '|---|---|---|---|---|---|---|']
    for k in kiem: md_.append(f"| {k['chi_so']} | {k['gia_tri']} | {k['tran'] if k['tran'] is not None else ''} | {k['san'] if k['san'] is not None else ''} | {'ĐẠT' if k['dat'] else '**TRƯỢT**'} | {'**CÓ**' if k['trong_5pct'] else ''} | {k['ghi']} |")
    md_ += ['', '## Khoảnh khắc M-d', '', '| # | Khoảnh khắc | Shot | Giây | Mức kiểm | Nhân vật có tên |', '|---|---|---|---|---|---|']
    for n, ten in MD_MOC.items():
        sh = [r for r in rows if r.get('md_moc') == n]
        if sh: md_.append(f"| {n} | {ten} | {', '.join(r['ma'] for r in sh)} | {sum(r['dur'] for r in sh):.3f} | {', '.join(sorted({('v1' if r['md_clip'] else r['muc_kiem']) for r in sh}))} | {', '.join(sorted({x for r in sh for x in r['nhan_vat_ten']}))} |")
    open(os.path.join(EP, 'BANG-SHOT-v3.md'), 'w').write('\n'.join(md_) + '\n')
    print(json.dumps({k: v for k, v in tong.items() if k not in ('lop_s', 'lop_pct')}, ensure_ascii=False))
    [print('TRƯỢT', k['chi_so'], k['gia_tri'], k['ghi']) for k in kiem if not k['dat']]
    [print('±5 %', k['chi_so'], k['gia_tri']) for k in kiem if k['trong_5pct']]


if __name__ == '__main__': main()
