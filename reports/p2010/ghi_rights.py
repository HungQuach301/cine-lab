#!/usr/bin/env python3
"""P-2010 · thêm vào RIGHTS.md: 8 bản Scott Buckley (K2-MUS-6…13, từ reports/nhac-t3/nguon-moi.json), 18 vân Poly Haven NC-CPU
(reports/nc-cpu/RIGHTS-NC.md), 3 tài sản mới của NC-V2V (reports/nc-v2v/ref/NGUON.md; tác giả tra api.polyhaven.com/info 20/10),
8 vân 4k NC-GPU (NC-GPU-BAO-CAO.md:253), 2 ảnh Flickr ĐÓNG-GÓI v2 (reports/dong-goi-t3-v2/nguon-anh.json).
Mỗi dòng mới phải có giấy phép trích nguyên văn trong ngoặc kép — kiểm ở cuối. Chạy một lần."""
import json, os, re, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
P = os.path.join(R, 'RIGHTS.md'); s = open(P, encoding='utf-8').read()
if 'K2-MUS-6' in s: sys.exit('DỪNG: đã có K2-MUS-6')
HEAD = '| Mã | Tài sản | Loại | Nguồn/URL | Tác giả | Giấy phép (trích nguyên câu + link) | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 | Ngày thêm |\n|---|---|---|---|---|---|---|---|---|---|\n'
D = '2026-10-20'
PH = ('"Our assets are all licensed as CC0, which is effectively Public Domain even in jurisdictions that do not support the Public Domain."'
      ' (https://polyhaven.com/license — P-2010 đọc lại 20/10/2026, khớp)')
rows = []

# 1. Nhạc
nm = json.load(open(os.path.join(R, 'reports/nhac-t3/nguon-moi.json'), encoding='utf-8'))['de_xuat']
assert len(nm) == 8
for i, m in enumerate(nm):
    dk = m['dieu_khoan_nguyen_van']
    rows.append(f"| K2-MUS-{6 + i} | \"{m['ten']}\" ({m['id']}, {float(m['giay']):.1f} s) — nhạc T3 phương án B (chủ dự án chọn 1X–4X 19/10; trừ tấm KA2026 = A). Tệp `{m['tep']}` "
                f"ngoài git, **chưa vào `assets/`** | Nhạc (người sáng tác/biểu diễn, không AI) | {m['trang']} · tệp {m['tep_url']} | {m['nguoi_sang_tac_bieu_dien']} | "
                f"CC BY 4.0 — \"{dk}\" (trang bài, đọc {m['ngay_doc']}; `reports/nhac-t3/giay-phep/scottbuckley-tung-bai.txt`) — https://creativecommons.org/licenses/by/4.0/ | "
                f"YouTube / bán phim / LHP: được (trang Licensing: CC-BY ✓ \"Film – other than online only (i.e. cinema distribution)\"). Cấm: bán riêng bản nhạc, đưa lên dịch vụ phát nhạc / nhận dạng âm thanh, phát tán soundtrack (Kinh thánh §14.6). "
                f"Content ID: tác giả đăng ký Smart Content ID (We Are Era Music BV) → ghi công trong mô tả TRƯỚC khi đăng | **Bắt buộc, trong mô tả YouTube** (không trong hình): "
                f"{m['ghi_cong']} (edited) — chữ \"(edited)\" theo CC BY 4.0 §3(a)(1)(B), NHAC-T3 §2.2; chờ chủ dự án duyệt mẫu | {m['sha256']} | {D} |")

# 2. 18 vân NC-CPU (2k/1k)
nc = open(os.path.join(R, 'reports/nc-cpu/RIGHTS-NC.md'), encoding='utf-8').read().splitlines()
tex = [l for l in nc if re.match(r'\| [a-z0-9_]+ \| ', l)]
assert len(tex) == 18, len(tex)
CO = {'clay_roof_tiles_02': ' (cùng tài sản P1810-PH05, khác độ phân giải → tệp khác)', 'stony_dirt_path': ' (mở rộng P1810-PH07 / P1810C-PH-NOR: diff, nor cùng SHA; thêm rough)'}
for i, l in enumerate(tex):
    c = [x.strip() for x in l.strip('|').split('|')]
    tid, tg, co, tep = c[0], c[1], c[2], c[3]
    rows.append(f"| NCCPU-PH{i + 1:02d} | Poly Haven `{tid}` ({co}){CO.get(tid, '')} — vân lớp phủ cách A (three.js) và Blender, NC-CPU → sản xuất G0 (Kinh thánh §14.2) | "
                f"Vân vật liệu (ảnh chụp/quét, không AI; màu + pháp tuyến + độ nhám) | https://polyhaven.com/a/{tid} (tải qua api.polyhaven.com/files/{tid}, 19/10/2026) | {tg} | {PH} | "
                f"Được mọi phạm vi | Không bắt buộc (CC0) | {tep} (12 ký tự đầu; tệp ngoài git `/var/tmp/cine-out/nc/tex/`; `reports/nc-cpu/RIGHTS-NC.md`) | {D} |")

# 3. NC-GPU bản 4k (8 vân cùng tài sản, tệp khác)
G4 = ['aerial_beach_01', 'aerial_grass_rock', 'aerial_rocks_02', 'clay_roof_tiles_02', 'dry_ground_rocks', 'marble_cliff_02', 'seaworn_sandstone_brick', 'white_plaster_rough_01']
tg = {[x.strip() for x in l.strip('|').split('|')][0]: [x.strip() for x in l.strip('|').split('|')][1] for l in tex}
for i, t in enumerate(G4):
    rows.append(f"| NCGPU-PH{i + 1:02d} | Poly Haven `{t}` bản **4k** (diff, nor) — Cycles GPU NC-GPU, cú lặn G0 (§14.2); cùng tài sản với NCCPU, khác độ phân giải | Vân vật liệu (ảnh chụp/quét, không AI) | "
                f"https://polyhaven.com/a/{t} | {tg[t]} | {PH} | Được mọi phạm vi | Không bắt buộc (CC0) | **chưa có trong repo** (`/var/tmp/cine-out/nc/tex/sha.json` ngoài git, mất theo container NC-GPU; ghi lại khi tải lại) | {D} |")

# 4. NC-V2V bảng vật liệu tham chiếu (biến thể b) — chỉ ảnh đích ngoài phim (V2V-D2), không lên hình
V2V = [('marble_cliff_01', 'Amal Kumar', 'texture, Diffuse 2k JPG', '60107dd7…130694'),
       ('coast_sand_01', 'Rob Tuytel', 'texture, Diffuse 2k', 'e1c37ea8…b979'),
       ('simons_town_harbour', 'Greg Zaal, Rico Cilliers', 'HDRI, bản Tonemapped JPG 8192×4096; chỉ cắt mặt nước 7 % × 3,5 %', 'c8833621…bedd')]
for i, (t, a, k, sha) in enumerate(V2V):
    rows.append(f"| NCV2V-PH{i + 1} | Poly Haven `{t}` ({k}) — ô trong `reports/nc-v2v/ref/bang-vat-lieu.jpg` (SHA 84228e44…bda05), ảnh tham chiếu gửi mô hình ở NC-V2V biến thể (b); **không lên hình** (ĐÍCH LOOK §14.4) | "
                f"Ảnh tham chiếu nội bộ (ảnh chụp, không AI) | https://polyhaven.com/a/{t} | {a} (tra api.polyhaven.com/info 20/10/2026) | {PH} | Được mọi phạm vi | Không bắt buộc (CC0) | {sha} (rút gọn, `reports/nc-v2v/ref/NGUON.md`) | {D} |")

# 5. Ảnh Flickr ĐÓNG-GÓI v2
an = json.load(open(os.path.join(R, 'reports/dong-goi-t3-v2/nguon-anh.json'), encoding='utf-8'))['anh']
assert len(an) == 2
for i, a in enumerate(an):
    rows.append(f"| DG3V2-PH{i + 1} | \"{a['tieu_de']}\" (ảnh chụp {a['ngay_chup_flickr'][:10]}) — {a['dung_o']} của thumbnail T3 (ĐÓNG-GÓI v2, mã {a['ma']}); chỉnh: {a['chinh_sua']} | "
                f"Ảnh chụp (Flickr, không AI) | {a['trang_nguon']} · tệp {a['url_tai']} | {a['tac_gia']} ({a['tac_gia_url']}) | {a['giay_phep']} — \"{a['giay_phep_nguyen_van_deed']}\" ({a['giay_phep_url']}; kiểm trang Flickr 19/10/2026) | "
                f"Được mọi phạm vi (kể cả thương mại) với ghi công + nêu chỉnh sửa | **Bắt buộc**: {a['ghi_cong_de_xuat']} | {a['sha256']} | {D} |")

# kiểm: mọi dòng có câu giấy phép nguyên văn trong ngoặc kép ở cột giấy phép
for r in rows:
    c = r.strip('|').split(' | ')
    assert len(c) == 10, (len(c), r[:80])
    assert re.search(r'"[^"]{40,}"', c[5]), r[:60]
sec = ('\n## Kênh 2 — nhạc T3 (Scott Buckley), vân CC0 NC-CPU/NC-GPU, tham chiếu NC-V2V, ảnh thumbnail ĐÓNG-GÓI v2 (phiên P-2010 ghi theo '
       '`reports/nhac-t3/NHAC-T3-BAO-CAO.md` §2.2, `reports/nc-cpu/RIGHTS-NC.md`, `reports/nc-gpu/NC-GPU-BAO-CAO.md` dòng 253, `reports/nc-v2v/ref/NGUON.md`, '
       '`reports/dong-goi-t3-v2/DONG-GOI-V2-BAO-CAO.md` §3; 20/10/2026)\n\n' + HEAD + '\n'.join(rows) + '\n')
open(P, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + sec)
print('thêm', len(rows), 'dòng; mọi dòng có giấy phép nguyên văn')
