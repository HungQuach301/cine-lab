#!/opt/cine/bin/python
"""ANIMATIC-T3-V2 · PHIEU-XEM-V2.md — CHỈ shot đổi + đoạn minh hoạ: mã shot, lý do, tệp xem (reports/animatic-t3-v2/xem/NN-…mp4), mốc giây TRONG TỆP và CẢ PHIM,
giây cắt góc trong shot (R3), đoạn minh hoạ (nhãn "Illustration"). Tệp xem cắt theo cùng ranh chương như ANIMATIC-T3 (anim_xuat.py).
  v2_phieu.py <log minh hoạ .json (anim_minh_hoa.py)> [--ra reports/animatic-t3-v2/PHIEU-XEM-V2.md]"""
import json, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]; EPD = REPO / 'channel-k2/k2c-t3-01/animatic'
CH = [('01-mo-dau', 0.0, 43.833), ('02-ch1-rock-1704', 43.833, 173.083), ('03-ch2a-vay-ham', 173.083, 262.167), ('04-ch2b-tan-cong-1782', 262.167, 382.583),
      ('05-ch3-dat-trung-lap', 382.583, 471.625), ('06-ch4-duong-bang', 471.625, 585.833), ('07-ch5a-cong', 585.833, 666.083), ('08-ch5b-ket', 666.083, 761.0)]
DOI = {   # shot đổi → lý do (nhận xét chủ dự án 21/10 21:05–21:15 + luật R1–R4 + sửa mã)
    'H1': 'mở đầu BAN NGÀY → hoàng hôn → đêm (Rock nhận ra 0–3 s), M5 minh hoạ 4,5–10,5 s',
    'H2': 'nối giờ kết thúc H1 (đêm 23:53)',
    'N1.4': 'R1: máy hạ sát dòng dân rời phố; M3 minh hoạ 3,5–11,5 s',
    'N1.5': 'R4 + R3: cảng 1713 → lâu đài (cờ) → eo đất trống ≤ 4 s rồi 2015',
    'N1.6': 'R1 + R3: vách bắc + khói vây 1704–05/1727 → cận Línea mọc 1730–35 → 2026 La Línea',
    'C1': 'R1 + R3: Línea đóng đường 21/6/1779 → cận trại dựng → dải trại tới 10/1779',
    'C3': 'M2 minh hoạ 0–8 s (người hái rau dại), rồi cẩu lên',
    'C4': 'hết "đồ chơi": máy thấp chéo từ vịnh; M1 trượt 3 lượt → giữ 3D góc thấp gần bến',
    'C5': 'M4 minh hoạ 6,1–12,5 s (đêm 13→14/4/1781, phố cháy)',
    'N2.10': 'R1 + R3: máy hạ trước vách bắc, 2 góc (đào · nổ lỗ thông hơi)',
    'N2.7': 'R1: hạ 320 → 48 m; sửa lỗi cũ quầng lửa lơ lửng trên trời',
    'N2.11': 'R1 + R3: công sự + Rock → khẩu đội phát súng cuối → trại rút 1783',
    'N3.1': 'R2 + R3: hai góc thấp ở hai đồn Línea (nổ 14/2/1810)',
    'N3.2': 'R4: phố + cảng từ vịnh 1810 → 1860 (thay eo đất trống)',
    'N3.4': 'R2 + R3: mép nam La Línea + Rock → dọc hàng rào 1909',
    'N3.5': 'R2: hạ máy, Rock chiếm khung',
    'N4.1': 'R2 + R3: 2 góc thấp dọc đường băng đang mọc',
    'N4.2': 'R2 + R3: đường băng lấn vịnh từ vịnh → vách bắc (bụi đá)',
    'N4.3': 'NƯỚC: hết mảng xanh nhạt ở vùng đất lấn chưa xây (AT-D1)',
    'N4.4': 'NƯỚC: hết mảng xanh nhạt (AT-D1)',
    'N5.4': 'hết "bản đồ trò chơi": khung lai thấp có chân trời + cây/đèn/xe phố 2026, 2 góc (cổng · hàng rào)',
    'N5.5': 'NƯỚC: hết mảng xanh nhạt ở bước năm 1943 (AT-D1)',
}


def main():
    MH = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 and Path(sys.argv[1]).exists() else []
    out = Path(sys.argv[sys.argv.index('--ra') + 1]) if '--ra' in sys.argv else REPO / 'reports/animatic-t3-v2/PHIEU-XEM-V2.md'
    B = {b['ma']: b for b in json.loads((EPD / 'bang-shot.json').read_text())}
    mm = lambda t: f'{int(t // 60)}:{t % 60:05.2f}'
    tep = lambda t: [c for c in CH if c[1] - 1e-6 <= t < c[2] - 1e-6][0]
    L = ['# PHIẾU XEM v2 — animatic T3 Gibraltar, CHỈ shot đổi + đoạn minh hoạ (ANIMATIC-T3-V2)', '',
         'Mở tệp trong `reports/animatic-t3-v2/xem/` (640×360, giọng + nhạc, không phụ đề; cùng tên/thứ tự 01…08 như ANIMATIC-T3). Mốc "trong tệp" tính từ đầu tệp.',
         'Ghi nhận xét dạng `<mã shot>: …`. Đoạn có nhãn **Illustration** góc dưới phải là minh hoạ AI (luật N2: không mang dữ kiện vị trí; dữ kiện do lời).', '',
         '| Mã | Tệp | Trong tệp | Cả phim | Cắt góc trong shot (giây trong shot) | Lý do đổi |', '|---|---|---|---|---|---|']
    for ma, ly in DOI.items():
        b = B[ma]; k, a0, _ = tep(b['t0'])
        L.append(f"| **{ma}** | `{k}.mp4` | {mm(b['t0'] - a0)} → {mm(b['t1'] - a0)} | {mm(b['t0'])} → {mm(b['t1'])} | {', '.join(f'{x:.1f}' for x in b.get('cat') or []) or '—'} | {ly} |")
    L += ['', '## Đoạn minh hoạ AI (Omni)', '', '| Đoạn | Shot | Tệp | Trong tệp | Cả phim | Trạng thái |', '|---|---|---|---|---|---|']
    for m in MH:
        b = B[m['shot']]; t0, t1 = b['t0'] + m['t0'], b['t0'] + m['t1']; k, a0, _ = tep(t0)
        st = 'CHÈN (nhãn Illustration)' if m.get('chen') else 'GIỮ 3D — ' + (m.get('ly_do') or '')
        L.append(f"| {m['ma']} | {m['shot']} | `{k}.mp4` | {mm(t0 - a0)} → {mm(t1 - a0)} | {mm(t0)} → {mm(t1)} | {st} |")
    L += ['', 'Shot không có trong bảng: máy/vật/lời giữ nguyên ANIMATIC-T3 nhưng dựng lại (mã `tl/*.js` đổi → dấu cảnh đổi); nước ở mọi năm < 2026 dùng bờ theo đúng mốc đất lấn.']
    out.write_text('\n'.join(L) + '\n'); print('PHIEU', out)


if __name__ == '__main__': main()
