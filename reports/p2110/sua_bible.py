#!/usr/bin/env python3
"""P-2110 · việc 2: ghi Kinh thánh §14.7 (look T3 + R1–R4 + mở đầu ban ngày) + §15 (luật AI N2+, M-d) + §16 (hậu kỳ chuẩn) theo lệnh chủ dự án
duyệt 21/10/2026. Khối LOOK chép NGUYÊN VĂN từ channel-k2/k2c-t3-01/LOOK-KHOA.md; §15 chép NGUYÊN VĂN nháp reports/NC-N2P-BAO-CAO.md §6.3 (a)–(e)
rồi sửa đúng các chỗ chủ dự án quyết. Mỗi chỗ neo/thay kiểm "đúng 1 lần xuất hiện"; SHA trước/sau → reports/p2110/sua-bible.json. Chạy một lần."""
import hashlib, json, os, re
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
B = 'docs/BIBLE-KENH2.md'; SHA_TRUOC = '50554dcce70fab49b20906aeea598dd0c4bc1130b042d3e817b895add56e83dd'   # bản P-2010b
LK = 'channel-k2/k2c-t3-01/LOOK-KHOA.md'; N2P = 'reports/NC-N2P-BAO-CAO.md'
doc = lambda p: open(os.path.join(R, p), encoding='utf-8').read()
sha = lambda p: hashlib.sha256(open(os.path.join(R, p), 'rb').read()).hexdigest()


def mot(s, a, ten):
    n = s.count(a); assert n == 1, (ten, n); return s


# §14.7 — khối LOOK-1…LOOK-5 + "Tham chiếu ngữ pháp máy" nguyên văn
lk = doc(LK).split('\n'); i0 = [i for i, l in enumerate(lk) if l.startswith('- LOOK-1 ')]; assert len(i0) == 1
LOOK = lk[i0[0]:i0[0] + 6]
assert [l[:8] for l in LOOK[:5]] == [f'- LOOK-{k}' for k in range(1, 6)] and LOOK[5].startswith('- Tham chiếu ngữ pháp máy'), LOOK
R14 = ('R1 Chủ thể trên eo đất (dòng người, Línea, trại, công sự, lửa, hầm) chiếm ≥ 15–20 % khung, vẫn giữ dải chân trời mỏng, Rock không cắt mép. '
       'R2 Đồng cỏ/cát trống (> 50 % khung) ≤ 6 s liên tục và ≤ 10 % thời lượng mỗi chương. '
       'R3 Shot > 15 s chia 2–3 góc, mỗi góc có biến cố thấy được ≤ 6 s. '
       'R4 Câu lời không có vật trên eo đất → góc phố/lâu đài/cảng; bản đồ phủ ≤ 3 s (TL-4). '
       'R1–R4 thắng LOOK-2 ở shot có chủ thể trên eo đất.')
MO = ('Mở đầu tập: timelapse bắt đầu bằng cảnh ban ngày rồi mới sang tối để thấy tính timelapse và nhận ra nơi chốn trong vài giây đầu '
      '(chủ dự án 21/10 21:09).')
S147 = '\n'.join(['', '### 14.7 Look T3 (chủ dự án chọn mù 21/10/2026 07:05)', *LOOK,
                  f'- Thông số tái lập: channel-k2/k2c-t3-01/LOOK-KHOA.md (SHA {sha(LK)}).',
                  f'- R1–R4 (chủ dự án đồng ý 21/10 21:05): {R14}', f'- {MO}'])

# §15 — nháp §6.3 nguyên văn + sửa (i)–(vi)
nb = doc(N2P); m = re.search(r'### §6\.3 Nháp Kinh thánh §15 "N2\+" \(nguyên văn đề xuất\)\n\n(.*?)\n\n### §6\.4', nb, re.S); assert m
q = m.group(1).split('\n'); assert len(q) == 6 and all(l.startswith('> ') for l in q), q
DAU = q[0][2:]; assert DAU == '**§15. Luật AI N2+ (áp từ T4; chủ dự án duyệt …/10/2026).**', DAU
MUC = {l[3]: l[2:] for l in q[1:]}; assert list(MUC) == list('abcde') and all(v.startswith(f'({k}) ') for k, v in MUC.items())
CU_B = 'khớp màu về render trên lớp nền'
MOI_B = ('khớp màu render VÀO tông tấm nền AI (không kéo tấm AI về tông render); vật lớp (a) nằm trên nền đất (vd dãy trại) dựng lại có vân/bóng '
         'cùng tông tấm nền')
mot(MUC['b'], CU_B, '(b) khớp màu'); MUC['b'] = MUC['b'].replace(CU_B, MOI_B)
MUC['d'] = ('(d) Trần T4: tấm nền N2+ ≤ 50 % thời lượng (chỉ shot timelapse máy cố định); minh hoạ M-d ≤ 20 %; tổng khung có AI ≤ 70 %; '
            'hai loại không chồng nhau trên một shot; chuyển tấm nền chỉ bằng hoà ≥ 2 s. Không dùng AI video→video (sửa video theo video nguồn) '
            'cho shot timelapse hoặc shot mang dữ kiện; video AI chỉ cho minh hoạ M-d.')
MUC['f'] = ("(f) Minh hoạ M-d (duyệt 21/10 15:56): đoạn AI đứng riêng, máy tầm người 0–40 m (toàn cảnh cao do 3D); không công trình có tên làm chủ thể "
            "— nếu buộc có thì ảnh đầu lấy từ render; mỗi đoạn kẹp giữa hai shot timelapse 3D cùng thời điểm, bộ đếm chạy tiếp, nhãn 'Illustration' "
            "suốt đoạn; khớp lớp (a) (gió, trăng, ranh lửa theo ngày); không dựng nhân vật lịch sử có tên; qua cùng bộ kiểm (c). Khung T4: 8 khoảnh "
            "khắc — (1) Pudding Lane 01:00 2/9; (2) bờ sông gần cầu sáng 2/9; (3) Thames sà lan + đồ trôi, bờ bắc rực lửa; (4) Watling Street "
            "xe/người khiêng/người bệnh; (5) chì chảy quanh St Paul's đêm 4/9; (6) nổ nhà bằng thuốc súng Tower Street; (7) Moorfields lều/chòi/đống "
            "đồ; (8) phế tích bốc khói 7/9.")
MUC['g'] = ('(g) Lối mòn/đường đất: có trên bản đồ đo đạc thời đó (bậc 1) thuộc lớp (a); không nguồn thuộc lớp (c); mặt nạ ID ghi trường lối mòn có '
            'nguồn.')
MUC['h'] = '(h) Bộ kiểm N2+ đưa vào checks/ ở phiên K (N2P-D4); Cosmos-Transfer gác (N2P-D6).'
MUC['i'] = ('(i) T3 (luật N2 §14.1): được dùng minh hoạ AI có nhãn theo đúng nguyên tắc (f), ≤ 20 % thời lượng — chủ dự án mở cho vòng sửa T3 '
            'ngày 21/10 21:15 (5 đoạn: Rodney dỡ hàng Old Mole 1780, hái rau dại 1780, dân rời phố 8/1704, phố cháy đêm 4/1781, cận chân người qua '
            'đường băng 2026).')
S15 = '\n'.join(['', '## 15. Luật AI N2+ (áp từ T4; chủ dự án duyệt 21/10/2026 15:59)', '',
                 '(Nháp `reports/NC-N2P-BAO-CAO.md` §6.3 (a)–(e) chép nguyên văn, trừ các chỗ chủ dự án quyết: (b) khớp màu; (d) thay toàn bộ; thêm (f)–(i).)',
                 *[f'- {MUC[k]}' for k in 'abcdefghi']])
S16 = '\n'.join(['', '## 16. Hậu kỳ chuẩn mỗi tập (chủ dự án duyệt 21/10 20:10)',
                 '- Phiên bản cuối gồm: chỉnh màu toàn phim (khớp tông giữa cách A, cú lặn Cycles GPU, đoạn minh hoạ AI và các mốc năm; một LUT kênh; '
                 'đo ΔE shot kề) và SFX + âm nền theo hình (pháo, sóng, gió, lửa, đám đông, chim biển) chỉ từ nguồn CC0 hoặc giấy phép thương mại rõ, '
                 'ghi RIGHTS từng tiếng, trộn dưới lời theo §4.'])

assert sha(B) == SHA_TRUOC, 'Kinh thánh không phải bản P-2010b'
s = doc(B); truoc = sha(B)
SUA = [('tiêu đề', '§14 + sửa 20/10, 20/10 22:34)', '§14 + sửa 20/10, 20/10 22:34; §14.7 + §15 + §16 — 21/10/2026)'),
       ('neo cuối §14.6 → §14.7 + §15 + §16', '- Master âm thanh phát hành (giọng, nhạc, stem) PHẢI vào LFS kèm SHA.\n',
        '- Master âm thanh phát hành (giọng, nhạc, stem) PHẢI vào LFS kèm SHA.\n' + S147 + '\n' + S15 + '\n' + S16 + '\n')]
for ten, a, b in SUA:
    mot(s, a, ten); s = s.replace(a, b)
assert s.endswith(S16 + '\n')
for ten, a in [('§14.7', '### 14.7 '), ('§15', '## 15. '), ('§16', '## 16. ')]: mot(s, a, ten)
open(os.path.join(R, B), 'w', encoding='utf-8').write(s)
json.dump(dict(tep=B, sha_truoc=truoc, sha_sau=sha(B), look_khoa=dict(tep=LK, sha=sha(LK)), nhap_n2p=dict(tep=N2P, sha=sha(N2P)),
               sua=[t for t, _, _ in SUA], muc_15=list('abcdefghi')),
          open(os.path.join(R, 'reports/p2110/sua-bible.json'), 'w'), ensure_ascii=False, indent=1)
print(truoc, '→', sha(B))
