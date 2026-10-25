#!/opt/cine/bin/python
"""ANIMATIC-T4 · việc 10 — PHIẾU XEM (reports/animatic-t4/PHIEU-XEM.md) — mục A: chỗ cần xem kỹ, mốc theo tệp xem + cả phim (tự sinh từ BANG-SHOT-v2 + xuat.json);
mục B/C viết tay trong khuôn dưới (chủ dự án xem MỘT lần, gom nhận xét theo mã shot; phiên KHÔNG chấm mù thay chủ dự án)."""
import json
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]; EP = REPO / 'channel-k2/k2c-t4-02'; RP = REPO / 'reports/animatic-t4'
def mm(t): return f'{int(t // 60)}:{t % 60:05.2f}'


def main():
    B = json.loads((EP / 'BANG-SHOT-v2.json').read_text()); X = json.loads((RP / 'xuat.json').read_text()); parts = X['xem']
    def vi_tri(t0, t1):
        for i, p in enumerate(parts):
            if p['tu_s'] - 1e-6 <= t0 < p['den_s']: return f"`xem-{i + 1}` {mm(t0 - p['tu_s'])}–{mm(t1 - p['tu_s'])}"
    rows = B['shot']; A = []
    def add(nhom, r, ghi): A.append(f"| {nhom} | **{r['ma']}** | {vi_tri(r['t0'], r['t1'])} | {mm(r['t0'])}–{mm(r['t1'])} | {r['vai']} | {ghi} |")
    chon = {p.stem: p.read_text().strip() for p in (EP / 'animatic/omni/chon').glob('*.txt')}
    for r in rows:
        if r['cu_may'] == 'MD': add('Omni M-d', r, f"khoảnh khắc {r['md_moc']}: {r['md_ten']} · clip `{chon.get(r['ma'], 'CHƯA CÓ')}` — xem: lỗi thời đại (mũ/áo), chữ, mặt/tay méo, khớp lời")
    for r in rows:
        if r['ai_nen']: add('Tấm nền 2026', r, f"tấm {r['them']['tam_nen'][0]:g}–{r['them']['tam_nen'][1]:g} s trong shot — xem trời/sông/đất có 'thật' hơn 3D không, mối hoà 2 s")
    for r in rows:
        tg = r['thoi_gian']
        if tg and (tg[0] in ('h66', 'h40') or (tg[0] == 'khop' and any(x[0] in ('h66', 'h40') for x in tg[1:3]))): add('Lửa 1666/1940', r, 'lửa/khói cách A look2.js (V2 = a) — xem khói ngày tầng cao, ánh lửa trên St Paul\'s')
    for r in rows:
        if r['cu_may'] in ('THAP',) or r['ma'] in ('H2-06', 'H2-10', 'H3-05', 'H4-04c', 'H5-05a', 'H5-05b'): add('Công trình', r, "St Paul's / Monument / Tower — chi tiết đọc được ở 640×360?")
    for r in rows:
        if r['diem_may'] == 'P1': add('P1 fov 36°', r, 'khung xương sống fov 36° (V5) — mái vòm ở mép trái khung (x ≈ 18 %)')
    L = ['# PHIẾU XEM — animatic T4 London (K2C-T4-02, ANIMATIC-T4, 24/10/2026)', '',
         'Chủ dự án xem **MỘT lần** cả tập, gom mọi nhận xét theo **mã shot** (`<mã>: …`). Ba tệp xem 640×360 trong `reports/animatic-t4/xem/` (giọng G1 K1-C1 + SFX/nhạc nháp, không phụ đề). '
         'Tờ khung 1 khung/shot có mã + mốc giờ: `reports/animatic-t4/to-khung.jpg`. Bảng shot: `channel-k2/k2c-t4-02/BANG-SHOT-v2.md`. Trong phim không có nhãn/chữ AI (§14.1 c, f).', '',
         '| Tệp | Từ → đến (cả phim) | Cỡ |', '|---|---|---|']
    for i, p in enumerate(parts): L.append(f"| `{Path(p['tep']).name}` | {mm(p['tu_s'])} → {mm(p['den_s'])} | {p['bytes'] / 1e6:.2f} MB |")
    L += ['', '## A. Chỗ cần xem kỹ', '', '| Nhóm | Mã | Trong tệp | Cả phim | Vai | Xem gì |', '|---|---|---|---|---|---|'] + A
    (RP / 'phieu-A.md').write_text('\n'.join(L) + '\n'); print(len(A))


if __name__ == '__main__': main()
