#!/opt/cine/bin/python
"""Last Lamplighters · nhà máy — bộ kiểm tự động một tập (gọi qua scripts/ll/qc.sh). Xuất bảng ĐẠT/TRƯỢT (Markdown + JSON).

Luật làm việc của P (Mốc B). Không phải luật khoá của K: luật khoá nằm trong checks/ (chỉ K sửa); đề xuất gửi K qua checks-appeal.md.
Mục kiểm (ngưỡng ở bảng R dưới đây):
  Q1 judder: đoạn giữ khung giống hệt 2–12 khung (scripts/p/judder.py, framemd5) trên trung gian từng đoạn = 0
  Q2 khung gần trùng: |chênh| TB ≤ 0,1 mức xám (192×108) mà 6 khung trước và sau đều chuyển động rõ (trung vị > 0,5) = 0
  Q3 máy xuyên hình học: (a) cảnh 2.5D báo khoảng cách máy tới lớp gần nhất ≤ 0,05 → lỗi; (b) khung có > 85 % ô 16×16 phẳng (nghi máy nằm trong khối) ngoài vùng mờ chuyển = 0
  Q4 loudness −14 ± 1 LUFS, true peak ≤ −1 dBTP (master, 3 phần, Shorts)
  Q5 tương phản chữ ≥ 4,5:1 (đo trên điểm ảnh thật ở khung mẫu); Q6 cỡ chữ hoa ≥ 18 px (16:9) / 30 px (9:16) ở mọi khung mẫu
  Q7 nhãn ACTUAL/PROJECTION: shot có số dự báo phải hiện chữ PROJECTION; shot có số thực tế phải hiện ACTUAL
  Q8 nguồn: đọc toàn văn, không Wikipedia/Wikimedia làm nguồn chính, số khớp lời (ll.py check)
  Q9 số khung trung gian = timeline; master = tổng khung
  Q10 bản xem: mỗi phần ≤ 90 MB; Short ≤ 60 s
  Q11 chữ đứng: không quá 3 s liền không có nội dung mới khi lời đang nói (shot đồ hoạ; cảnh truyện toàn khung miễn)
Mọi số trong ±5 % quanh ngưỡng được nêu tên ở cột "sát ngưỡng".
"""
import glob, json, os, re, subprocess, sys
import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__)); import ll  # noqa: E402
EP = sys.argv[1]; E = ll.load(EP); O = E['out']; V = os.environ.get('V', 'v1')
TL = json.load(open(os.path.join(O, 'timeline.json')))
FULL = {'street', 'office', 'rows', 'endcard'}
rows = []


def row(q, name, ok, val, thr, near=None, note=''):
    rows.append(dict(q=q, ten=name, kq='ĐẠT' if ok else 'TRƯỢT', gia_tri=val, nguong=thr, sat=near or '', ghi_chu=note))


def nearv(v, thr, name):
    return f'{name}: {v} (ngưỡng {thr})' if thr and abs(v - thr) <= abs(thr) * 0.05 else None


def frames_of(p):
    return int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', p],
                              capture_output=True, text=True).stdout.strip() or 0)


def judder(p, tol=None):
    j = p + ('.near.json' if tol else '.judder.json')
    if not os.path.exists(j) or os.path.getmtime(j) < os.path.getmtime(p):
        subprocess.run(['/opt/cine/bin/python', f'{REPO}/scripts/p/judder.py', p, '--json', j] + (['--tol', str(tol)] if tol else []), capture_output=True)
    return json.load(open(j))


def loud(p):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', p, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = r[r.rfind('Summary:'):]; g = lambda k: float(s.split(k)[1].split()[0]); return g('I:'), g('Peak:')


units = [('seg', s, f"{O}/sec/{s['id']}.mkv") for s in TL['segments']] + [('short', s, f"{O}/shorts/{s['id']}.mkv") for s in TL['shorts']]
units = [u for u in units if os.path.exists(u[2])]
# Q1, Q2
J = {s['id']: judder(p) for _, s, p in units}


def stutter(p, tol=0.1, mov=0.5):   # khung gần trùng KẸP GIỮA chuyển động rõ (trung vị chênh 6 khung trước và sau > mov)
    w, h = 192, 108
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', f'scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.int16); d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    return [round((i + 1) / 24, 2) for i in range(6, len(d) - 6) if d[i] <= tol and np.median(d[i - 6:i]) > mov and np.median(d[i + 1:i + 7]) > mov]


NJ = {s['id']: {'loi': len(x), 't': x[:5]} for _, s, p in units for x in [stutter(p)]}
bad = {k: v['loi'] for k, v in J.items() if v['loi']}; row('Q1', 'Judder (giữ 2–12 khung, framemd5)', not bad, sum(J[k]['loi'] for k in J), 0, note=str(bad) if bad else f'{len(J)} tệp')
badn = {k: v['t'] for k, v in NJ.items() if v['loi']}; row('Q2', 'Khung gần trùng giữa chuyển động (tol 0,1)', not badn, sum(NJ[k]['loi'] for k in NJ), 0, note=str(badn) if badn else '')
# Q3
logs = {s['id']: json.load(open(p + '.log.json')) for _, s, p in units if os.path.exists(p + '.log.json')}
camb = {k: sum(1 for c in L['cam'] if c is not None and c <= 0.05) for k, L in logs.items()}; camb = {k: v for k, v in camb.items() if v}
flat = {}
for kind, s, p in units:
    if not any(sh['tpl'] in FULL - {'endcard'} for sh in s['shots']): continue
    w, h = (96, 54) if kind == 'seg' else (54, 96)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', f'select=not(mod(n\\,6)),scale={w * 4}:{h * 4},format=gray', '-vsync', '0', '-f', 'rawvideo', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, h * 4, w * 4).astype(np.float32)
    n = 0
    for i, fr in enumerate(a):
        f = i * 6
        if f < 8 or f > s['frames'] - 9: continue   # vùng mờ đầu/cuối đoạn
        hh, ww = fr.shape[0] // 16, fr.shape[1] // 16; tiles = fr[:hh * 16, :ww * 16].reshape(hh, 16, ww, 16).std(axis=(1, 3)); mean = fr.mean()
        if (tiles < 1.0).mean() > 0.85 and mean > 12: n += 1
    if n: flat[s['id']] = n
row('Q3', 'Máy xuyên hình học (log máy + khung phẳng)', not camb and not flat, sum(camb.values()) + sum(flat.values()), 0, note=f'log {camb} · phẳng {flat}' if camb or flat else '')
# Q4
for f in sorted(glob.glob(f"{O}/{E['id']}-{V}-*.mp4")) + sorted(glob.glob(f"{O}/shorts/{E['id']}-short-*.mp4")):
    I, TP = loud(f); nm = os.path.basename(f); part = re.search(r'-p\d\.mp4$', nm) is not None; tol = 2 if part else 1
    row('Q4', f'Loudness/TP {nm}', abs(I + 14) <= tol and TP <= -1, f'{I} LUFS / {TP} dBTP', f'−14±{tol} / ≤ −1', near=nearv(TP, -1, 'TP') if TP > -1.3 else None,
        note='phần bản xem: đối chiếu (chuẩn đo trên master)' if part else '')
# Q5, Q6
minr, mincap, raised = (99, None), {}, {}
for k, L in logs.items():
    thr = 30 if L['fmt'] == '9x16' else 18
    for e in L['text']:
        for it in e['items']:
            if it['out']: continue
            if it['ratio'] < minr[0]: minr = (it['ratio'], f"{k} f{e['f']} “{it['s']}”")
            if it['cap'] < mincap.get(k, (99,))[0]: mincap[k] = (it['cap'], thr, f"f{e['f']} “{it['s']}”")
    if L['raised']['raised']: raised[k] = L['raised']['raised']
row('Q5', 'Tương phản chữ thấp nhất', minr[0] >= 4.5, minr[0], 4.5, near=nearv(minr[0], 4.5, minr[1]), note=minr[1])
badc = {k: v for k, v in mincap.items() if v[0] < v[1] - 0.05}
worst = min(mincap.items(), key=lambda kv: kv[1][0] - kv[1][1]) if mincap else None
row('Q6', 'Cỡ chữ hoa tối thiểu (mọi khung mẫu)', not badc, f'{worst[1][0]} px ({worst[0]} {worst[1][2]})' if worst else '—', '18 / 30 px',
    near=nearv(worst[1][0], worst[1][1], 'cỡ chữ') if worst else None, note=(f'mẫu tự nâng cỡ: {raised}' if raised else '') + (f' TRƯỢT {badc}' if badc else ''))
# Q7
miss = []
for k, L in logs.items():
    sg = next(s for s in TL['segments'] + TL['shorts'] if s['id'] == k)
    for sh in sg['shots']:
        kinds = set(re.findall(r"'kind': '(actual|projection)'", str(sh['p'])))
        seen = ' '.join(it['s'] for e in L['text'] if sh['t0'] * 24 <= e['f'] < sh['t1'] * 24 for it in e['items'])
        for kd in kinds:
            if kd.upper() not in seen: miss.append(f"{k}/{sh['tpl']}@{sh['t0']:.1f}: thiếu {kd.upper()}")
row('Q7', 'Nhãn ACTUAL/PROJECTION khi có số', not miss, len(miss), 0, note='; '.join(miss[:6]))
# Q8
err, warn = ll.check(E)
row('Q8', 'Nguồn (toàn văn, không Wikipedia) + số khớp lời', not err, len(err), 0, note='; '.join(err[:4] + warn[:2]))
# Q9
fb = [f"{s['id']} {frames_of(p)}/{s['frames']}" for _, s, p in units if frames_of(p) != s['frames']]
m = f"{O}/{E['id']}-{V}-master.mp4"; mf = frames_of(m) if os.path.exists(m) else None
row('Q9', 'Số khung khớp timeline', not fb and (mf is None or mf == TL['tong_khung']), f"master {mf}/{TL['tong_khung']}", '= timeline', note='; '.join(fb))
# Q10
for f in sorted(glob.glob(f"{O}/{E['id']}-{V}-p?.mp4")):
    mb = os.path.getsize(f) / 1e6; row('Q10', f'Dung lượng {os.path.basename(f)}', mb <= 90, f'{mb:.1f} MB', '≤ 90 MB', near=nearv(round(mb, 1), 90, 'MB'))
for s in TL['shorts']: row('Q10', f"Thời lượng Short {s['id']}", s['t1'] <= 60, f"{s['t1']:.2f} s", '≤ 60 s', near=nearv(round(s['t1'], 2), 60, 's'))
# Q11
still = []
for k, L in logs.items():
    sg = next(s for s in TL['segments'] + TL['shorts'] if s['id'] == k); A = [c == '1' for c in L['act']]
    for sh in sg['shots']:
        if sh['tpl'] in FULL:
            for f in range(int(sh['t0'] * 24), min(len(A), int(sh['t1'] * 24))): A[f] = True
    sp = np.zeros(len(A), bool)
    for a, b in sg['speech']: sp[int(a * 24):int(b * 24) + 13] = True
    run, start = 0, 0
    for f in range(len(A)):
        if not A[f] and sp[f]: run += 1; start = start if run > 1 else f
        elif not A[f] and run: run += 0   # khoảng nghỉ giữa câu không cắt chuỗi
        else:
            if run > 72: still.append(f'{k} {start / 24:.1f}s ({run / 24:.1f} s)')
            run = 0
    if run > 72: still.append(f'{k} {start / 24:.1f}s ({run / 24:.1f} s)')
row('Q11', 'Chữ đứng > 3 s khi đang có lời', not still, len(still), 0, note='; '.join(still[:8]))

ok = all(r['kq'] == 'ĐẠT' for r in rows)
md = [f"# QC {E['id']} ({V}) — {'ĐẠT' if ok else 'TRƯỢT'}", '', '| Mục | Kiểm | Kết quả | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) | Ghi chú |', '|---|---|---|---|---|---|---|']
md += [f"| {r['q']} | {r['ten']} | **{r['kq']}** | {r['gia_tri']} | {r['nguong']} | {r['sat']} | {r['ghi_chu']} |" for r in rows]
open(f'{O}/qc.md', 'w').write('\n'.join(md) + '\n'); json.dump(rows, open(f'{O}/qc.json', 'w'), ensure_ascii=False, indent=1)
print('\n'.join(md)); sys.exit(0 if ok else 1)
