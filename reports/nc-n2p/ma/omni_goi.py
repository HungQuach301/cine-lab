#!/opt/cine/bin/python -I
"""NC-N2P · bọc lệnh gọi Gemini Omni Flash: GỌI NGUYÊN design/k2v/v2v/omni.py (NC-V2V, không sửa) với sổ riêng reports/nc-n2p/so-ai-gemini.jsonl (V2V_SO).
Chặn của phiên này (thay mức $40 của omni.py): mốc theo dõi $12; CHẶN AN TOÀN $18 — từ chối nếu tổng sổ + $1,15 (giá một lượt 720p 10 s đo ở NC-V2V) > 18.
HTTP 402 / hết hạn mức → ghi tệp DUNG-GEMINI và từ chối mọi lệnh sau (luật lệnh: dừng gọi Gemini ngay, kéo kết quả đã có, làm tiếp mục khác).
Cùng lỗi ≥ 3 lần liên tiếp → dừng.
  omni_goi.py --video in.mp4 --prompt-file p.txt --out ra.mp4 --tag c1-vua [--res 720p] [--prev ID] [--task extend]"""
import argparse, json, os, subprocess, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]; SO = REPO / 'reports/nc-n2p/so-ai-gemini.jsonl'; STOP = REPO / 'reports/nc-n2p/DUNG-GEMINI'
MOC, CHAN, LUOT = 12.0, 18.0, 1.15


def tong():
    return sum(float(json.loads(l).get('usd') or 0) for l in SO.read_text().splitlines() if l.strip()) if SO.exists() else 0.0


def loi_lien_tiep():
    if not SO.exists(): return 0, None
    rs = [json.loads(l) for l in SO.read_text().splitlines() if l.strip()]; n, last = 0, None
    for r in reversed(rs):
        if r.get('http') == 200: break
        k = (r.get('http'), json.dumps(r.get('loi'))[:120])
        if last is None or k == last: n += 1; last = k
        else: break
    return n, last


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--video', required=True); ap.add_argument('--prompt-file', required=True); ap.add_argument('--out', required=True); ap.add_argument('--tag', required=True)
    ap.add_argument('--res', default='720p'); ap.add_argument('--prev'); ap.add_argument('--task'); a = ap.parse_args()
    if STOP.exists(): sys.exit('DỪNG Gemini: ' + STOP.read_text())
    if tong() + LUOT > CHAN: sys.exit(f'CHẶN AN TOÀN: sổ Gemini {tong():.2f} + {LUOT} > {CHAN}')
    n, last = loi_lien_tiep()
    if n >= 3: sys.exit(f'DỪNG: cùng lỗi {n} lần liên tiếp {last}')
    cmd = [sys.executable, '-I', str(REPO / 'design/k2v/v2v/omni.py'), 'edit', '--video', a.video, '--prompt', Path(a.prompt_file).read_text().strip(), '--res', a.res, '--out', a.out, '--tag', a.tag]
    if a.prev: cmd += ['--prev', a.prev]
    if a.task: cmd += ['--task', a.task]
    r = subprocess.run(cmd, env=dict(os.environ, V2V_SO=str(SO)), capture_output=True, text=True)
    print(r.stdout[-3000:]); print(r.stderr[-1500:], file=sys.stderr)
    rs = [json.loads(l) for l in SO.read_text().splitlines() if l.strip()] if SO.exists() else []
    if rs and rs[-1].get('tag') == a.tag and rs[-1].get('http') in (402, 429) and ('prepay' in json.dumps(rs[-1].get('loi')).lower() or 'quota' in json.dumps(rs[-1].get('loi')).lower() or rs[-1].get('http') == 402):
        STOP.write_text(f"HTTP {rs[-1].get('http')} ở {a.tag}: {json.dumps(rs[-1].get('loi'))[:400]}\n"); print('GHI DUNG-GEMINI', file=sys.stderr)
    t = tong(); print(f'Gemini luỹ kế ${t:.2f}', file=sys.stderr)
    if t >= MOC: print(f'VƯỢT MỐC THEO DÕI Gemini ${MOC:.0f}', file=sys.stderr)
    sys.exit(r.returncode)


if __name__ == '__main__': main()
