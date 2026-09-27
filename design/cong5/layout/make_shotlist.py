"""Sinh shots/animatic/SHOTLIST.md + shots.json từ bảng shot trong design/cong5/layout/film.js (nguồn duy nhất).
Chạy: /opt/cine/bin/python design/cong5/layout/make_shotlist.py [timing.json]"""
import json, os, subprocess, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
out = subprocess.run(['node', os.path.join(REPO, 'design/cong5/layout/render_film.js'), '--list', '--out', '/tmp'], capture_output=True, text=True, check=True).stdout
L = json.loads(out)
timing = {}
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    for s in json.load(open(sys.argv[1]))['summary']: timing[s['id']] = s
tc = lambda x: f"{int(x // 60)}:{x % 60:05.2f}".replace('.', ',')
SC = {1: 'Cảnh 1 — Vòng đèn', 2: 'Cảnh 2 — Bật điện (đêm)', 3: 'Cảnh 3 — Chạy đua', 4: 'Cảnh 4 — Bức tường', 5: 'Cảnh 5 — Ngọn cuối', 6: 'Cảnh 6 — Ô cửa'}
os.makedirs(os.path.join(REPO, 'shots/animatic'), exist_ok=True)
json.dump(L, open(os.path.join(REPO, 'shots/animatic/shots.json'), 'w'), ensure_ascii=False, indent=1)
md = ['# SHOT LIST — ANIMATIC "Last Round" (Cổng 4 · v2)', '',
      'Sinh tự động từ `design/cong5/layout/film.js` (nguồn duy nhất; sửa ở đó rồi chạy lại `make_shotlist.py`). Kịch bản: `scripts/last-round.fountain` nháp 3. Luật thế giới v0.4.', '',
      f'**{len(L)} shot · tổng {L[-1]["t1"] - L[0]["t0"]:.1f} s ({tc(L[-1]["t1"])}) · 24 fps · 16:9.** Tiêu cự: mm tương đương full-frame 35 mm (FOV dọc = 2·atan(12/f)).', '',
      '## Quy ước địa lý và luật 180°',
      '- Phố Ostler chạy theo trục x. Quảng trường và đồng hồ nằm ở **phải khung**; nhà kho và ngọn thứ 11 nằm ở **trái khung**. Máy luôn đặt ở phía nam phố.',
      '  - Cảnh 1–3: Ida đi **phải → trái**; sóng trắng tới từ **phải**.',
      '  - Khi bà quay nhìn quảng trường (s11), bà nhìn sang **phải**; s15 bà quay về dốc xuống (**trái**).',
      '- Cảnh 4–5 (tường, hốc cửa): máy luôn ở **sau-phải** hai người; Ida **trái**, Cas **phải**.',
      '  - Cận Ida nói L3 (s31) chụp qua vai phải Cas, vẫn ở cùng phía đường nối Ida–Cas.',
      '- Cận thoại trên thang (s36–s39): Ida nhìn **lên phố (phải khung)**. Cas dưới chân thang nhìn **lên** (s38, máy cao gần mắt Ida).',
      '- Cảnh 5 cuối (s42a–s42): Cas đi từ phố trắng (ngoài) vào vòm hốc cửa (trong); s42 máy đặt TRONG hốc nhìn ra vòm, Ida đứng ở miệng vòm.', '',
      '## Ba nhịp đồng hồ (giờ tiến; lý do từng nhịp ở cột "Lý do chọn")',
      '- **Nhịp 1 (s06, 0:16):** đồng hồ bỏ túi 7:31 — gieo mô-típ chậm 7 phút, gõ kính.',
      '- **Nhịp 2 (s09 → s09w, 0:25–0:30) = lúc bật điện:** đồng hồ quảng trường sáng đúng 8:00 + chuông; cắt sang đồng hồ bỏ túi 7:53.',
      '- **Nhịp 3 (s45 → s45c → s46, 2:09–2:15):** đồng hồ bỏ túi 9:53, đồng hồ quảng trường 10:00; bà vặn lên 10:00, gập lại không gõ.', '',
      '## Nguồn sáng điện thấy được và góc tối (chỉ đạo chủ dự án)',
      '- Bóng đèn điện nhấp hai lần rồi đứng trong khung: s10e (quảng trường), s12 (x=85), s19 (x=57), s27 (cột phố chính cạnh nhà kho), s37w (cột góc — đoạn cáp cuối).',
      '- Góc ngọn 11 tối từ s23 tới giữa s37w (luật thế giới v0.4, "đoạn cáp cuối").', '',
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
               '| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn | Nguồn khung |',
               '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    md.append(f"| {i} | {s['id']} | {tc(s['t0'])}–{tc(s['t1'])} | {s['t1'] - s['t0']:.1f} | {s['size']} | {s['angle']} | {s['mm']} | {s['move']} | {s['light']} | {s['sound']} | {s['action']} | {s['why']} | {'render v2' if s['src'] == 'new' else 'tái dùng ' + s['src']} |")
    if i == len(L) or L[i]['scene'] != cur: md.append('')
if timing:
    md += ['## Thời gian render thật (960×540, 1 mẫu, không DOF)', '', '| Shot | Khung | Dựng cảnh (s) | s/khung (TB) | s/khung (max) | Tổng (s) |', '|---|---|---|---|---|---|']
    for s in L:
        t = timing.get(s['id']);
        if t: md.append(f"| {s['id']} | {t['frames']} | {t['setup_s']:.1f} | {t['per_frame_s']['mean']:.2f} | {t['per_frame_s']['max']:.2f} | {t['wall_s']:.0f} |")
open(os.path.join(REPO, 'shots/animatic/SHOTLIST.md'), 'w').write('\n'.join(md) + '\n')
print(len(L), 'shot')
