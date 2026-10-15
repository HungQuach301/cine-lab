#!/opt/cine/bin/python
"""Bộ luật kênh 2 — một lệnh (phiên K, bản 1.11.0, 15/10/2026). Áp cho tập kênh 2 từ K2 tập 3 (T2 chạy checks 1.10.2 đã ghim).
Phiên xưởng chỉ CHẠY (không đọc mã). Định nghĩa: checks/ll/RULES-LL.md.

  k2check.py <episode.yaml> [--tl timeline.json] [--master master.mp4] [--mix mix.json] [--logs <thư mục *.log.json>]
             [--vo vo.flac --bed bed.flac] [--no-asr] [--json ra.json] [--md ra.md]

Gọi: Q26b bối cảnh · Q32 footage/ảnh nguồn ngoài · Q33 lặp cảnh · Q34 loại shot · Q35 nhãn loại số (D5) · Q36 chữ trên màn hình ·
Q37 nhịp thị giác · A1–A13 âm thanh · LOCK. Mã thoát 0 khi mọi mục ĐẠT (âm thanh của tập cũ: CHỈ BÁO, không tính).
Mặc định: timeline <out>/timeline.json, master <out>/<id>-v1-master.mp4 nếu có, mix <out>/mix.json, log <out>/ nếu có *.mkv.log.json.
"""
import glob, json, os, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from checks.ll import base, q_setting, q_footage, q_scene, q_types, q_chu, q_nhip, q_amthanh  # noqa: E402
from checks.cinecheck import VERSION  # noqa: E402


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    g = lambda k: a[a.index('--' + k) + 1] if '--' + k in a else None
    EP = a[0]; E = base.load(EP); E['_path'] = os.path.abspath(EP); ep_dir = os.path.dirname(os.path.abspath(EP)); O = E['out']
    TL = json.load(open(g('tl') or os.path.join(O, 'timeline.json')))
    m = g('master') or next(iter(sorted(glob.glob(os.path.join(O, f"{E['id']}-*-master.mp4")))), None)
    mp = g('mix') or os.path.join(O, 'mix.json'); MX = json.load(open(mp)) if os.path.exists(mp) else None
    logs = g('logs') or (O if glob.glob(os.path.join(O, '*.log.json')) else None)
    rows = []

    def row(q, ten, r, nguong=''):
        kq = r.get('ket_qua') or ('ĐẠT' if r['ok'] else 'TRƯỢT')
        rows.append(dict(q=q, ten=ten, kq=kq, val=r.get('val', ''), nguong=nguong, sat='; '.join(r.get('sat_nguong') or []), loi=(r.get('loi') or []) + (r.get('thieu') or [])))
    row('Q26b', 'Đa dạng bối cảnh', q_setting.q26b(TL, E), '≤ 25 % · ≤ 90 s · nửa sau ≥ 3')
    row('Q32', 'Footage/ảnh nguồn ngoài', q_footage.q32(E, TL, ep_dir), '≤ 40 % · footage ≤ 20 % · ≤ 8 s/clip · < 720p trong khung ≤ 1,5×')
    row('Q33', 'Lặp cảnh', q_scene.q33(E, TL, video=m if m and os.path.exists(m) else None), '≤ 2 lần')
    row('Q34', 'Loại shot', q_types.q34(E, TL, ep_dir), 'type · map ±6 s · photo ±6 s · số neo 3D ≥ 60 % · document')
    row('Q35', 'Nhãn loại số (D5)', q_chu.q35(E, TL, logs), 'ACTUAL ≤ 1/khung · ESTIMATE bắt buộc · số có năm rõ không cần ACTUAL')
    row('Q36', 'Chữ trên màn hình', q_chu.q36(E, TL, logs), 'nguồn ≥ 38 px, 1 dòng, ≤ 70 ký tự · Facts as of chỉ với luật hiệu lực')
    row('Q37', 'Nhịp thị giác', q_nhip.q37(E, TL, m if m and os.path.exists(m) else None), 'TB ≤ 3,5 s · dài nhất ≤ 6 s · khung tĩnh ≤ 6 s')
    ra = q_amthanh.check(E, TL, master=m, MX=MX, vo=g('vo'), bed=g('bed'), asr='--no-asr' not in a)
    row('A1–A13', 'Âm thanh (' + ('MIX=audio' if ra['ap_dung'] else 'tập cũ — chỉ báo') + ')', ra, 'docs/AUDIO-THUOC-DO.md')
    lk = subprocess.run([sys.executable, os.path.join(base.REPO, 'checks', 'lock.py'), '--verify'], capture_output=True, text=True)
    rows.append(dict(q='LOCK', ten=f'checks/ khớp LOCK ({VERSION})', kq='ĐẠT' if lk.returncode == 0 else 'TRƯỢT', val='KHỚP' if lk.returncode == 0 else 'KHÔNG KHỚP', nguong='', sat='', loi=[]))
    ok = all(r['kq'] in ('ĐẠT', 'CHỈ BÁO') for r in rows)
    md = [f"# Luật kênh 2 (checks {VERSION}) — {E['id']} — {'ĐẠT' if ok else 'TRƯỢT'}", '',
          '| Mục | Kiểm | Kết quả | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) |', '|---|---|---|---|---|---|']
    md += [f"| {r['q']} | {r['ten']} | **{r['kq']}** | {str(r['val']).replace('|', '/')} | {r['nguong']} | {r['sat'].replace('|', '/')} |" for r in rows]
    md += ['', '## Âm thanh A1–A13', q_amthanh.table(ra), '', '## Chi tiết lỗi']
    for r in rows:
        if r['loi']: md += [f"### {r['q']}"] + [f'- {x}' for x in r['loi'][:60]] + ([f"- … {len(r['loi']) - 60} mục nữa"] if len(r['loi']) > 60 else [])
    txt = '\n'.join(md) + '\n'; print(txt)
    if g('md'): open(g('md'), 'w').write(txt)
    if g('json'): json.dump(dict(rows=rows, am_thanh=ra, version=VERSION), open(g('json'), 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
