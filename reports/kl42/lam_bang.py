#!/opt/cine/bin/python
"""KL42 · sinh bang-gian-shot.md từ nhip.py (A = chỉ giãn, B = giãn + trần đuôi) — chạy nhip.py A rồi B; nhip-that.json = B (đề xuất), nhip-that-A.json = A."""
import json, shutil, subprocess, sys
import kl_lib as K
py = sys.executable
subprocess.run([py, str(K.H / 'nhip.py'), 'A'], check=True, capture_output=True); shutil.copy(K.H / 'nhip-that.json', K.H / 'nhip-that-A.json')
subprocess.run([py, str(K.H / 'nhip.py'), 'B'], check=True, capture_output=True)
A = json.loads((K.H / 'nhip-that-A.json').read_text()); B = json.loads((K.H / 'nhip-that.json').read_text())
GC = {r['id']: r for r in json.loads((K.R / 'reports/giong-chot/gian-shot-v2-s1.03-do.json').read_text())['tat_ca']}
ra, rb = {r['id']: r for r in A['shot']}, {r['id']: r for r in B['shot']}
f = lambda x: f'{x:.3f}'.replace('.', ',')
L = ['# Bảng giãn shot theo lời thu thật — K2C-T3-01 lời v4.2, G1 speed 1,03 (KL42, 19/10/2026)', '',
     '> CHỈ ĐỀ XUẤT — không sửa `vay-ham/treatment.json`. Thay bảng GIỌNG-CHỐT §5 (bảng đó ước lời theo số từ; bảng này dùng mốc thật của bản thu). '
     'Số liệu đầy đủ (mốc từng câu/shot trong bản thu và trên trục phim): `nhip-that.json` (B, đề xuất) và `nhip-that-A.json` (A). Công cụ: `nhip.py`, `lam_bang.py`.',
     '', '**Thứ tự shot theo lời v4.2:** ‹2o›, ‹2p› đứng ngay sau ‹KA1782›, trước ‹2j› (`treatment.json` vẫn theo thứ tự cũ: G1b/V7 dời 2 shot này khi dựng).', '',
     '**Luật** (giữ khung GIỌNG-CHỐT §5 đã được duyệt): mỗi shot chứa lời của nó + 0,4 s; lời chảy sang shot kế tối đa 0,5 s, nhưng không chảy vào tấm im lặng và không chảy ra ngoài shot cuối; '
     'khi có lời chảy sang, lời của shot kế bắt đầu sau phần chảy + 0,4 s. Shot giãn được là shot 3D không phải khung neo, mốc đinh, cú liên hoàn hay 0c. '
     'Thẻ, ảnh, tranh, bản đồ giãn tới trần của loại; footage (2p) tạm lấy trần 12 s. Không giãn tấm im lặng, không cắt lời. Bậc 1/24 s.',
     f"- **A, chỉ giãn:** {f(A['tong_cu'])} → **{f(A['tong_moi'])} s** (+{f(A['them'])}), {A['so_shot_gian']} shot giãn.",
     f"- **B, giãn + trần đuôi (đề xuất):** sau A, mỗi shot giãn được hoặc thẻ/ảnh/bản đồ có lời giữ tối đa **{str(B['phuong_an']['B']['tran_duoi']).replace('.', ',')} s hình sau lời** "
     f"(khung neo, mốc đinh, cú liên hoàn, 0c và tấm im lặng giữ nguyên). Kết quả **{f(B['tong_moi'])} s**: {B['so_shot_gian']} shot giãn, {len(B['phuong_an']['B']['shot_rut'])} shot rút.",
     f"- Để so: kéo nhịp lời ×1,02 sau thu → {f(B['phuong_an']['C102']['tong'])} s; ×1,03 → {f(B['phuong_an']['C103']['tong'])} s (chỉ giãn, không rút). Phải nghe tệp kéo nhịp trước khi chọn.",
     f"- Kiểm cả hai phương án: không có lời nào cách lời kế < 0,4 s, không có lời rơi vào tấm im lặng (KB1943, KA2026), không có lời tràn ra cuối phim. Tổng lời theo shot là {f(B['tong_loi_shot'])} s.", '',
     '## Shot đổi thời lượng', '', '| Shot | Loại | Kiểu | Lời thật (s) | Chảy vào (s) | Dur cũ | **B (đề xuất)** | A | GIỌNG-CHỐT §5 (ước) |', '|---|---|---|---|---|---|---|---|---|']
for i in B['thu_tu_v42']:
    a, b = ra[i], rb[i]; g = GC.get(i, {})
    if abs(a['dur_moi'] - a['dur']) > 1e-6 or abs(b['dur_moi'] - b['dur']) > 1e-6 or abs(g.get('dur_moi', a['dur']) - a['dur']) > 1e-6:
        L.append(f"| {i} | {b['loai']} | {b['kieu']} | {f(b['loi'])} | {f(b['chay_vao'])} | {f(b['dur'])} | **{f(b['dur_moi'])}** ({'+' if b['them'] >= 0 else ''}{f(b['them'])}) | "
                 f"{f(a['dur_moi'])} | {f(g['dur_moi']) if g else '—'} |")
L += ['', '## Theo chương', '', '| Chương | Dur cũ | B | A |', '|---|---|---|---|']
for k in sorted(B['chuong'], key=int):
    L.append(f"| {k} | {f(B['chuong'][k]['cu'])} | {f(B['chuong'][k]['moi'])} | {f(A['chuong'][k]['moi'])} |")
L.append(f"| **Tổng** | {f(B['tong_cu'])} | **{f(B['tong_moi'])}** | {f(A['tong_moi'])} |")
L += ['', '## Ghi chú cho G1b/V7',
      '- **2o (mặt cắt hầm, M11):** ở v4.2, 2o không còn hứng 5,4 s lời chảy từ chuỗi 2k–2n như bảng GIỌNG-CHỐT, nên không cần +6 s. Ở B, 2o rút 2,04 s (12,5 → 10,458).',
      '- **Lời chảy từ chuỗi 2k–2n** (thẻ 2n chạm trần, cú liên hoàn 2m cố định) nay được hấp thụ ở **2q** (3D vùng), +4,6 s.',
      '- **4g:** hấp thụ phần chảy 8,5 s của SM3, trước tấm im lặng KB1943. Lời SM3 kết thúc trước KB1943 ≥ 0,4 s.',
      '- **5j:** +0,96 s; lời 5j kết thúc trước KA2026 ≥ 0,4 s (lỗi lời tràn từ KHOA-LOI-41 không còn).',
      '- Vị trí đặt lời: `nhip-that.json` → `shot[].loi_bd_phim / loi_kt_phim` (giây trên trục phim theo phương án), `shot[].cau[]` (từng câu), '
      '`shot[].ban_thu` (mốc trong stem `T3-loi-G1-v42-14LUFS.wav` và trong từng chương). Mốc lấy theo alignment ký tự của ElevenLabs.']
(K.H / 'bang-gian-shot.md').write_text('\n'.join(L) + '\n'); print('\n'.join(L))
