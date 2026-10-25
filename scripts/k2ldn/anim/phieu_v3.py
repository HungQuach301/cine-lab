#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · việc 9 — PHIẾU XEM v2, mục A (chỗ đổi so animatic v1, theo mã shot + vị trí trong tệp xem) và A1 (clip có nhân vật có tên — chủ dự án duyệt từng clip, P2 = (b)).
Nguồn: BANG-SHOT-v3.json (cột nguon_v2, them.dung_sua, md_clip), BANG-SHOT-v2.json, reports/animatic-t4-v2/xuat.json. Ra: reports/animatic-t4-v2/phieu-A.md (PHIEU-XEM-V2.md chèn tệp này)."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[3]; EP = R / 'channel-k2/k2c-t4-02'; RP = R / 'reports/animatic-t4-v2'
def mm(t): return f'{int(t // 60)}:{t % 60:05.2f}'


def main():
    B = json.loads((EP / 'BANG-SHOT-v3.json').read_text()); V2 = {r['ma']: r for r in json.loads((EP / 'BANG-SHOT-v2.json').read_text())['shot']}
    X = json.loads((RP / 'xuat.json').read_text())['xem']
    def tep(t):
        for i, x in enumerate(X):
            if x['tu_s'] - 1e-6 <= t < x['den_s'] + 1e-6: return f"`xem-{i + 1}` {mm(t - x['tu_s'])}"
        return '—'
    L = ['| Mã | Loại đổi | Trong tệp xem | Cả phim | Nội dung | Căn cứ / xem gì |', '|---|---|---|---|---|---|']
    A1 = ['| Mã | Trong tệp xem | Cả phim | Nhân vật có tên | Clip | Chân dung tham chiếu (chỉ trang phục/dáng) | Duyệt (✓/✗ + ghi chú) |', '|---|---|---|---|---|---|---|']
    MC = json.loads((EP / 'animatic2/omni/lenh/muc-luc.json').read_text())
    for r in B['shot']:
        v = V2.get(r.get('nguon_v2') or '') if r.get('nguon_v2') else None; th = r['them']; loai = None
        if r['cu_may'] == 'MD' and not r.get('md_clip'): loai = 'Omni MỚI (v3)'
        elif r['cu_may'] == 'TL': loai = 'ẢNH/TƯ LIỆU THẬT toàn khung'
        elif not r.get('nguon_v2'): loai = '3D MỚI'
        elif th.get('dung_sua'): loai = 'SỬA'
        elif v and (abs(v['dur'] - r['dur']) > 0.05 or v['cu_may'] != r['cu_may'] or v['thoi_gian'] != r['thoi_gian']): loai = 'đổi độ dài/cú máy/giờ'
        elif r['diem_may'] == 'P1': loai = 'C6 (P1 xoay 4°)'
        if r['ma'] in ('M00', 'M03', 'M04', 'H1-01h', 'H1-02h', 'H1-04', 'H1-06', 'H1-07', 'H1-08b', 'H1-09', 'H1-11', 'H1-13a', 'H1-13c', 'H1-15', 'H1-15h', 'H1-16') and not loai: loai = 'C9 (+0,5 EV đêm 1666)'
        if not loai: continue
        xem = th.get('dung_sua') or ''
        if r['cu_may'] == 'MD' and not r.get('md_clip'):
            xem = (f"clip `{(EP / 'animatic2/omni/chon' / (r['ma'] + '.txt')).read_text().strip()}` · mức kiểm {r.get('muc_kiem')} — xem lỗi thời đại, chữ, mặt/tay méo, khớp lời; " + xem).strip('; ')
        if r['cu_may'] == 'TL': xem = f"{r['tl_anh']} — chú thích \"{th['chu']}\"; " + xem
        L.append(f"| **{r['ma']}** | {loai} | {tep(r['t0'])} | {mm(r['t0'])}–{mm(r['t1'])} | {r['vai']} | {xem} |")
        if r['cu_may'] == 'MD' and r.get('nhan_vat_ten'):
            tag = (EP / 'animatic2/omni/chon' / (r['ma'] + '.txt')).read_text().strip()
            A1.append(f"| **{r['ma']}** | {tep(r['t0'])} | {mm(r['t0'])}–{mm(r['t1'])} | {', '.join(r['nhan_vat_ten'])} | `{tag}` | {', '.join(Path(x).name for x in MC[r['ma']]['tham_chieu']) or 'không (không có chân dung xác thực/sạch quyền) — khung xa'} | ☐ |")
    (RP / 'phieu-A.md').write_text('## A. Chỗ đổi so animatic v1 (theo mã shot)\n\n' + '\n'.join(L) + '\n\n## A1. Clip có NHÂN VẬT CÓ TÊN — chủ dự án duyệt TỪNG clip (P2 = (b): khung trung/xa, không cận mặt, trang phục/dáng theo chân dung thật)\n\n' + '\n'.join(A1) + '\n')
    print(len(L) - 2, 'dòng A;', len(A1) - 2, 'dòng A1')


if __name__ == '__main__': main()
