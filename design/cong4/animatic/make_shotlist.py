"""Sinh shots/animatic/SHOTLIST.md + shots.json từ bảng shot trong design/cong4/animatic/film.js (nguồn duy nhất).
Chạy: /opt/cine/bin/python design/cong4/animatic/make_shotlist.py [timing.json]"""
import json, os, subprocess, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
out = subprocess.run(['node', os.path.join(REPO, 'design/cong4/animatic/render_film.js'), '--list', '--out', '/tmp'], capture_output=True, text=True, check=True).stdout
L = json.loads(out)
timing = {}
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    for s in json.load(open(sys.argv[1]))['summary']: timing[s['id']] = s
tc = lambda x: f"{int(x // 60)}:{x % 60:05.2f}".replace('.', ',')
SC = {1: 'Cảnh 1 — Vòng đèn', 2: 'Cảnh 2 — Bật điện', 3: 'Cảnh 3 — Chạy đua', 4: 'Cảnh 4 — Bức tường', 5: 'Cảnh 5 — Ngọn cuối', 6: 'Cảnh 6 — Ô cửa'}
os.makedirs(os.path.join(REPO, 'shots/animatic'), exist_ok=True)
json.dump(L, open(os.path.join(REPO, 'shots/animatic/shots.json'), 'w'), ensure_ascii=False, indent=1)
md = ['# SHOT LIST — ANIMATIC "Last Round" (Cổng 4)', '',
      'Sinh tự động từ `design/cong4/animatic/film.js` (nguồn duy nhất; sửa ở đó rồi chạy lại `make_shotlist.py`). Kịch bản: `scripts/last-round.fountain` nháp 2.', '',
      f'**{len(L)} shot · tổng {L[-1]["t1"] - L[0]["t0"]:.1f} s ({tc(L[-1]["t1"])}) · 24 fps · 16:9.** Tiêu cự: mm tương đương full-frame 35 mm (FOV dọc = 2·atan(12/f)).', '',
      '## Quy ước địa lý và luật 180°',
      '- Phố Ostler chạy theo trục x. Quảng trường và đồng hồ nằm ở **phải khung**; nhà kho và ngọn thứ 11 nằm ở **trái khung**. Máy luôn đặt ở phía nam phố.',
      '  - Cảnh 1–3: Ida đi **phải → trái**; sóng trắng tới từ **phải**.',
      '  - Khi bà quay nhìn quảng trường (s11, s15), bà nhìn sang **phải**.',
      '- Cảnh 4–5 (tường, hốc cửa): máy luôn ở **sau-phải** hai người; Ida **trái**, Cas **phải**.',
      '  - Cận Ida nói L3 (s31) chụp qua vai phải Cas, vẫn ở cùng phía đường nối Ida–Cas.',
      '- Cận thoại trên thang (s36–s39): Ida nhìn **lên phố (phải khung)**. Cas dưới chân thang nhìn **lên** (s38, máy cao gần mắt Ida).',
      '- Match cut 8B (s16 → s17): hai mặt đồng hồ ở **cùng vị trí, cùng cỡ** trong khung.', '',
      '## Sai khác previs so với thiết kế khoá (cần xử lý ở layout/Cổng 5)',
      '- **Phố thẳng và phẳng.** Bản khoá (s1) là phố cong, dốc nhẹ. Khoảng cách: đèn khí 14 m; cột điện đặt theo chỉ số của s1.',
      '- **Cảnh 3 là montage nén thời gian.** Nhịp bật cột điện chọn cho từng shot đọc được "nở hổ phách → trắng phủ", không theo một đồng hồ vật lý liên tục.',
      '- **Các đạo cụ previs chưa có trang thiết kế:**',
      '  - đồng hồ bỏ túi (theo kích thước sheet);',
      '  - cột đồng hồ quảng trường (chép bố cục s1);',
      '  - phòng Cas (s48).',
      '- **Thang:**',
      '  - khi Ida trèo, thang dựng ở phía bắc cột (như a_close_ida);',
      '  - khi Ida đi, thang vác trên vai;',
      '  - ở ngõ (s47), thang xuất hiện trên vai không qua nhịp nhặt.',
      '- **Không có khẩu hình.** Thoại đặt đúng mốc nhưng môi không mấp máy (C′ chưa có rig miệng nói).',
      '- **Tư thế ngoài sheet** (IDA_POSES_C4, film.js: đẩy mũ, xem đồng hồ, trao đèn…) là previs. Cần duyệt thành tư thế sheet trước khi animate thật.', '']
cur = None
for i, s in enumerate(L, 1):
    if s['scene'] != cur:
        cur = s['scene']; sub = [x for x in L if x['scene'] == cur]
        md += [f'## {SC[cur]} ({tc(sub[0]["t0"])}–{tc(sub[-1]["t1"])}, {len(sub)} shot)', '',
               '| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn |',
               '|---|---|---|---|---|---|---|---|---|---|---|---|']
    md.append(f"| {i} | {s['id']} | {tc(s['t0'])}–{tc(s['t1'])} | {s['t1'] - s['t0']:.1f} | {s['size']} | {s['angle']} | {s['mm']} | {s['move']} | {s['light']} | {s['sound']} | {s['action']} | {s['why']} |")
    if i == len(L) or L[i]['scene'] != cur: md.append('')
if timing:
    md += ['## Thời gian render thật (960×540, 1 mẫu, không DOF)', '', '| Shot | Khung | Dựng cảnh (s) | s/khung (TB) | s/khung (max) | Tổng (s) |', '|---|---|---|---|---|---|']
    for s in L:
        t = timing.get(s['id']);
        if t: md.append(f"| {s['id']} | {t['frames']} | {t['setup_s']:.1f} | {t['per_frame_s']['mean']:.2f} | {t['per_frame_s']['max']:.2f} | {t['wall_s']:.0f} |")
open(os.path.join(REPO, 'shots/animatic/SHOTLIST.md'), 'w').write('\n'.join(md) + '\n')
print(len(L), 'shot')
