"""Tuỳ chọn của qc.py: gọi bộ kiểm kênh 2 của K (checks/ll/k2check.py, checks 1.11) khi có (phiên V5a, 15/10/2026).
Chỉ CHẠY công cụ của K qua dòng lệnh đã công bố trong checks/K-1.11-BAO-CAO.md §2 — không import, không đọc mã checks/.
Chưa merge 1.11 (không có tệp) → bỏ qua êm: trả None, qc.py ghi một dòng chú thích, không thêm mục TRƯỢT."""
import json, os, subprocess

K2CHECK = os.path.join('checks', 'll', 'k2check.py')


def args_for(ep, out, v='v1', ep_id=None):
    """dòng lệnh k2check theo tệp có thật trong <out>: timeline, master, mix, thư mục log render."""
    a = [os.path.abspath(ep)]
    tl, mix, sec = os.path.join(out, 'timeline.json'), os.path.join(out, 'mix.json'), os.path.join(out, 'sec')
    m = os.path.join(out, f'{ep_id}-{v}-master.mp4') if ep_id else None
    if os.path.exists(tl): a += ['--tl', tl]
    if m and os.path.exists(m): a += ['--master', m]
    if os.path.exists(mix): a += ['--mix', mix]
    if os.path.isdir(sec) and any(f.endswith('.log.json') for f in os.listdir(sec)): a += ['--logs', sec]
    return a + ['--md', os.path.join(out, 'k2check.md'), '--json', os.path.join(out, 'k2check.json')]


def run(repo, ep, out, v='v1', ep_id=None, py='/opt/cine/bin/python', timeout=7200):
    """None nếu chưa có k2check.py; ngược lại dict(ok, val, note) cho một dòng của bảng qc."""
    tool = os.path.join(repo, K2CHECK)
    if not os.path.exists(tool): return None
    if not os.path.exists(py): py = 'python3'
    try:
        r = subprocess.run([py, tool] + args_for(ep, out, v, ep_id), cwd=repo, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return dict(ok=False, val='quá giờ', note=f'k2check chạy quá {timeout} s')
    j = os.path.join(out, 'k2check.json'); n = ''
    if os.path.exists(j):
        try:
            d = json.load(open(j, encoding='utf-8'))
            if isinstance(d, dict): n = ', '.join(f'{k}={d[k]}' for k in ('ket_qua', 'version', 'phien_ban') if k in d)
        except ValueError: pass
    tail = (r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or [''])[-1][:200]
    return dict(ok=r.returncode == 0, val=f'mã thoát {r.returncode}', note=(n + ' · ' if n else '') + f'{tail} · chi tiết {os.path.join(out, "k2check.md")}'.replace('|', '/'))
