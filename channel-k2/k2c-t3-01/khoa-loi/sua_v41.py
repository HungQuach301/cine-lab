"""Khoá lời v4.1 (lệnh chủ dự án 18/10, LK2 + LK3) — CHỈ hai sửa này lên script-v4-KHOA.md → script-v4.1-KHOA.md. Ghi khoa-loi/sua-v41.json.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/khoa-loi/sua_v41.py"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent; EP = HERE.parent
S = [
 ('LK2', 'SM3', 'June 1940: Spain turns "non-belligerent" and occupies Tangier. Gibraltar sends its women and children away. By 1942, the invasion of North Africa is run from inside the Rock. {T021} {T022} {S114} {T023} {T024} {S122}',
  'May 1940: Gibraltar sends its women and children away. June: Spain turns "non-belligerent" and occupies Tangier. By 1942, the invasion of North Africa is run from inside the Rock. {S114} {T021} {T022} {T023} {T024} {S122}',
  'chủ dự án (LK2)', 'S114 T021 T022 T023 T024 S122', 'S114: sơ tán bắt đầu 22/5/1940, trước tháng 6 → ý sơ tán lên trước. Mẫu lệnh ("From May 1940… In June…") = 35 từ nói ≈ 14,0 s > cửa sổ SM3 + 4g 13,5 s (tràn sang tấm im lặng KB1943) → bỏ "From"/"In", dùng nhãn mốc "May 1940: … June: …" như câu SM3 cũ ("June 1940: …"): 33 từ ≈ 13,2 s'),
 ('LK3', '5a', 'In June 1969, Spain closed the land frontier completely. {C19}',
  "In June 1969, Spain closed the land frontier completely. {C19} It followed Gibraltar's new constitution; a Spanish historian says Madrid applied Utrecht strictly. {G003}",
  'chủ dự án (LK3)', 'G003 (mới)', 'bối cảnh trực tiếp của việc đóng biên giới: thời điểm (HMGoG + Langa Nuño, hai phía khớp) + cách giải thích của sử gia TBN (Sánchez Mantero) có ghi nguồn; 13 từ (bản 16 từ "It came sixteen days after…" đẩy tổng phim lên 724 s; tấm im lặng + thẻ chỉ rút được 3,5 s → rút câu, giữ đủ hai ý có nguồn)'),
]
t = (EP / 'script-v4-KHOA.md').read_text()
for code, sh, a, b, *_ in S:
    blk = t.split(f'‹{sh}›', 1)[1].split('\n‹', 1)[0]
    assert t.count(a) == 1 and a in blk, (code, sh)
    t = t.replace(a, b)
t = t.replace('— lời v4 KHOÁ 18/10/2026 (G1 duyệt 09:35; sau kiểm mù 2 vòng + REVIEWER 2 vòng)', '— lời v4.1 KHOÁ 18/10/2026 (G1 duyệt 09:35; v4 sau kiểm mù 2 vòng + REVIEWER 2 vòng; v4.1 = LK2 + LK3 của chủ dự án)')
assert 'v4.1 KHOÁ' in t
(EP / 'script-v4.1-KHOA.md').write_text(t)
(HERE / 'sua-v41.json').write_text(json.dumps([dict(ma=c, shot=s, truoc=a, sau=b, ai_neu=w, claim=cl, ly_do=l) for c, s, a, b, w, cl, l in S], ensure_ascii=False, indent=1) + '\n')
print(len(S), 'sửa → script-v4.1-KHOA.md')
