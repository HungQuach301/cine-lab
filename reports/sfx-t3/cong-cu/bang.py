"""SFX-T3 · sinh bảng cho báo cáo: ung-vien.md (ứng viên + số đo + soát AST + trạng thái), de-xuat-RIGHTS.md (dòng RIGHTS đề xuất — phiên P ghi),
goi-de-xuat.md (gói theo shot). Đọc: ung-vien/ung-vien.json, so-do/do-ung-vien.json, so-do/phan-loai-ung-vien.json, goi-de-xuat.json, sha-goc (đối số)."""
import json, os, sys, collections
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
UV = json.load(open(f'{D}/ung-vien/ung-vien.json')); DO = json.load(open(f'{D}/so-do/do-ung-vien.json')); PL = json.load(open(f'{D}/so-do/phan-loai-ung-vien.json'))
G = json.load(open(f'{D}/goi-de-xuat.json')); SHA = {l.split()[1]: l.split()[0] for l in open(sys.argv[1])}
# trạng thái do phiên đặt sau soát AST (lý do ghi trong báo cáo §2)
TT = {'HOAMAI-1': 'CHỜ TAI — còn tiếng hô "fire" (AST Speech 0,44–0,62 ở mọi điểm cắt 2,65–2,85 s)', 'CHIM-1': 'CHỜ TAI — AST nhận là quạ (Crow 0,72)',
      'MAYBAY-1': 'CHỜ TAI — AST không nhận ra máy bay (Gong/Hum); máy bay hiện đại cỡ nhỏ, không rõ đời', 'COI-1': 'CHỜ TAI — còi tàu khách hiện đại (AST Foghorn/Music) cho tàu 1940',
      'PGAN-1': 'DỰ PHÒNG — tái hiện trận có tiếng người la (AST Speech 0,09–0,16); gói dùng chùm PXA thay', 'LUAN-2': 'LOẠI — AST Vehicle 0,165 trong đoạn 2,9 s; LUAN-1 thay',
      'PXA-3': 'DÙNG (phụ) — súng hơi doạ chim, AST Firecracker 0,41: chỉ dùng xa, lọc thấp', 'GIO-3': 'DÙNG (phụ) — gió tổng hợp, sạch nhất'}
dung = collections.Counter(e['uv'] for e in G['su_kien'])
with open(f'{D}/ung-vien.md', 'w') as f:
    f.write('| ID | Loại | Nguồn · tác giả · tên | Đoạn gốc (s) | Dài (s) | I gốc (LUFS) | TP gốc | Sàn nhiễu (dBFS) | Băng 99 % (Hz) | AST top-1 | AST hiện đại max | AST lời max | Dùng trong gói | Trạng thái |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')
    for k, u in UV.items():
        d = DO.get(k + '.ogg', {}); p = PL.get(k + '.ogg', {}); top = p['cua_so'][0]['top'][0] if p.get('cua_so') else ('—', 0)
        g = DO.get(k + '.ogg'); hd = p.get('hien_dai_max') or ('—', 0)
        f.write(f"| {k} | {u['loai']} | {u['nguon']} · {u['tac_gia']} · {u['ten']} | {u.get('ss', 0)}+{u['dai_s']} | {u['dai_s']} | {d.get('I')} | {d.get('TP')} | {d.get('san_nhieu_dbfs')} | {d.get('bang_thong_99_hz')} | {top[0]} {top[1]} | {hd[0]} {hd[1]} | {p.get('loi_max')} | {dung.get(k, 0)} lần | {TT.get(k, 'DÙNG' if dung.get(k) else 'DỰ PHÒNG')} |\n")
with open(f'{D}/de-xuat-RIGHTS.md', 'w') as f:
    f.write('# Dòng RIGHTS đề xuất — SFX T3 (phiên P ghi vào RIGHTS.md khi chủ dự án duyệt; phiên SFX-T3 KHÔNG sửa sổ)\n\n')
    f.write('Cột theo RIGHTS.md. Mã đề xuất `K2-SFX-T3-xx`. Tệp đặt khi duyệt: `assets/k2/sfx/t3/<ID>.ogg` (chép từ `reports/sfx-t3/ung-vien/`). SHA gốc = tệp tải về nguyên vẹn; SHA đoạn = tệp OGG đã cắt/chuẩn mức.\n\n')
    f.write('| Mã | Tài sản | Loại | Nguồn/URL | Tác giả | Giấy phép (trích nguyên câu + link) | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 | Ngày thêm |\n|---|---|---|---|---|---|---|---|---|---|\n')
    n = 0
    for k, u in UV.items():
        if not dung.get(k): continue
        n += 1; nps = u['nguon'] == 'NPS'
        lic = (u['giay_phep'] + ' — "material created by the National Park Service and presented on this website, unless otherwise indicated, is generally considered in the public domain" (https://www.nps.gov/aboutus/disclaimer.htm, đọc 2026-10-22; `reports/sfx-t3/giay-phep/nps-disclaimer.txt`)') if nps else \
              (f"\"{u.get('dong_giay_phep_trang', u['giay_phep'])}\" (trang tiếng, đọc 2026-10-22) + trang Licenses: \"You are allowed to: … Use, including for commercial purposes. Without any restrictions. … Creative Commons CC0 1.0 Universal\" (https://bigsoundbank.com/licenses.html; `reports/sfx-t3/giay-phep/bigsoundbank-licenses.txt`)" if u['nguon'] == 'BigSoundBank' else
               f"OpenGameArt — License(s): CC0 → http://creativecommons.org/publicdomain/zero/1.0/ (trang tiếng, đọc 2026-10-22; `reports/sfx-t3/giay-phep/cc0-legalcode.txt`)")
        cong = 'Không bắt buộc. Bản bán phim: dòng "No claim to original U.S. Government works" trong credit (NPS disclaimer, 17 U.S.C. §403)' if nps else ('Không bắt buộc ("Nothing is mandatory"); đề xuất credit "Additional sounds: Joseph SARDIN - BigSoundBank.com"' if u['nguon'] == 'BigSoundBank' else 'Không bắt buộc (CC0); đề xuất ghi tên tác giả OGA trong mô tả')
        tg = SHA.get(u['goc'], '?')
        f.write(f"| K2-SFX-T3-{n:02d} | {k}: {u['ten']} — đoạn {u.get('ss', 0)} s + {u['dai_s']} s, 48 kHz Vorbis q6, chuẩn tuyến tính −23 LUFS, không EQ (lọc/đặt mức khi trộn) | SFX (ghi âm{'/thiết kế' if u['nguon']=='OpenGameArt' else ''}, không AI) | {u['url']} · tệp {u['tep_goc']} | {u['tac_gia']} | {lic} | Được — YouTube / bán phim / LHP (CC0/tài sản công: không NC/ND/SA). Content ID: xem SFX-T3 §6 | {cong} | gốc {tg} · đoạn {u['sha256_doan']} | (ngày P ghi) |\n")
    f.write(f'\n{n} dòng.\n')
with open(f'{D}/goi-de-xuat.md', 'w') as f:
    f.write('| Shot | t phim (s) | Tệp | Neo (áp lại khi V2) | Mức (LUFS trước master) | Dài (s) | Dốc vào/ra (s) | Lọc / pan | Ghi |\n|---|---|---|---|---|---|---|---|---|\n')
    for e in G['su_kien']:
        lp = '/'.join(x for x in [f"LP {e['lp']}" if e.get('lp') else '', f"HP {e['hp']}" if e.get('hp') else '', f"pan {e['pan']}" if 'pan' in e else ''] if x) or '—'
        f.write(f"| {e['shot']} | {e['t']:.2f} | {e['uv']} | {e['neo']} {'+' if e['lech'] >= 0 else ''}{e['lech']} | {e.get('muc', '')} | {e.get('dai') or '(cả tệp)'} | {e.get('fi', 0.01)}/{e.get('fo', 0.05)} | {lp} | {e.get('ghi', '')} |\n")
print('ok', n)
