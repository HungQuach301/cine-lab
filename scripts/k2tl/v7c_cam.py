#!/opt/cine/bin/python
"""V7C · XEM CÂM (việc 3) — cùng 3 vai, cùng 4 câu, cùng giao thức V7B (scripts/k2tl/v7b_cam.py: `claude -p` ghim claude-sonnet-5-5, chỉ Read, thư mục tạm chỉ có tờ khung),
thêm mức 640×360 (V7B-D7; 320×180 giữ làm sàn). Chuỗi: 1 khung/2 s từ master KHÔNG phụ đề, không tiếng.
  v7c_cam.py to <master.mp4> [nhãn]      → reports/v7c/xem-cam/<nhãn>/r320/to-*.jpg (lưới 6 × 5) + r640/to-*.jpg (lưới 2 × 3, khung 640×360)
  v7c_cam.py run <nhãn> [r320|r640]      → phieu-R*.json (+ raw), cost.jsonl
  v7c_cam.py score <nhãn> [r320|r640]    → ket-qua.json (từ khoá; P đọc lại ghi riêng p-doc.json)"""
import json, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
import v7b_cam as B   # cùng vai, câu, đáp án khoá, thang chấm (không sửa v7b_cam.py)

ROOT = Path(__file__).resolve().parents[2]; W = ROOT / 'reports/v7c/xem-cam'; LOG = W / 'cost.jsonl'; MODEL = 'claude-sonnet-5-5'
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except Exception: F = ImageFont.load_default()
CAP = 8.0   # chặn chi phí Claude của riêng bước này ($); mốc theo dõi cả phiên $8, dừng báo $25

def sheets(master, nhan):
    tmp = Path(f'/var/tmp/cine-out/v7c/cam-{nhan}'); shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1.0', '-i', str(master), '-vf', 'fps=0.5,scale=640:360:flags=lanczos', str(tmp / 'k%03d.png')], check=True)
    fs = sorted(tmp.glob('k*.png'))
    for res, cols, per, sz in (('r320', 6, 30, (320, 180)), ('r640', 2, 6, (640, 360))):
        d = W / nhan / res; shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
        for j in range(0, len(fs), per):
            grp = fs[j:j + per]; rows = (len(grp) + cols - 1) // cols; cw, ch = sz[0] + 10, sz[1] + 25
            S = Image.new('RGB', (cols * cw, rows * ch), 'white'); D = ImageDraw.Draw(S)
            for i, f in enumerate(grp):
                n = j + i; x, y = (i % cols) * cw, (i // cols) * ch; D.text((x + 4, y + 2), f'#{n + 1:02d} · {1 + 2 * n:d} s', fill='black', font=F)
                S.paste(Image.open(f).resize(sz, Image.LANCZOS), (x + 4, y + 22))
            S.save(d / f'to-{j // per + 1:02d}.jpg', quality=88)
        print(res, len(fs), 'khung', len(list(d.glob('to-*.jpg'))), 'tờ')

def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if LOG.exists() else 0.0
def call(args):
    nhan, res, rk = args
    if spent() > CAP: raise SystemExit(f'dừng: ${spent():.2f}')
    d = W / nhan / res; sh = sorted(d.glob('to-*.jpg')); out = d / f'phieu-{rk}.json'
    prompt = B.PROMPT.format(persona=B.RATERS[rk], n=len(sh), names=', '.join(s.name for s in sh), qs='\n'.join(B.Q))
    with tempfile.TemporaryDirectory() as cwd:
        for s in sh: shutil.copy(s, cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, cwd=cwd, timeout=1200)
            try: j = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'v7c-xem-cam-{nhan}-{res}:{rk}', 'model': MODEL, 'served': sorted(j.get('modelUsage', {})), 'usd': j.get('total_cost_usd', 0)}) + '\n')
            (d / f'raw-{rk}.txt').write_text(j.get('result', ''))
            m = re.search(r'\{.*\}', j.get('result', ''), re.S)
            if m:
                try: out.write_text(json.dumps(json.loads(m.group(0)), ensure_ascii=False, indent=1)); return True
                except Exception: pass
    return False

def score(nhan, res):
    d = W / nhan / res; R = {}
    for rk in B.RATERS:
        p = d / f'phieu-{rk}.json'
        if not p.exists(): continue
        j = json.loads(p.read_text()); R[rk] = dict(diem={q: B.grade(q, j.get(q)) for q in B.KEY}, clarity=j.get('clarity'), tra_loi={q: j.get(q) for q in B.KEY}, lac=j.get('lost', []))
    tot = {q: sum(R[r]['diem'][q] for r in R) for q in B.KEY}
    out = dict(may=f'{MODEL} (claude -p, chỉ Read)', muc=res, thang='0/1/2 mỗi câu × 3 người = tối đa 6/câu', theo_cau=tot, tong=sum(tot.values()), toi_da=6 * len(B.KEY),
               clarity_tb=round(sum(R[r]['clarity'] or 0 for r in R) / max(1, len(R)), 2), nguoi=R, chi_phi_usd_luy_ke=round(spent(), 4))
    (d / 'ket-qua.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n'); print(res, json.dumps({k: out[k] for k in ('theo_cau', 'tong', 'toi_da', 'clarity_tb', 'chi_phi_usd_luy_ke')}, ensure_ascii=False))

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'to': sheets(Path(a[1]), a[2] if len(a) > 2 else 'v7c')
    else:
        nhan = a[1]; ress = [x for x in a[2:] if x in ('r320', 'r640')] or ['r320', 'r640']
        for res in ress:
            if a[0] == 'run':
                with ThreadPoolExecutor(3) as ex: print(res, dict(zip(B.RATERS, ex.map(call, [(nhan, res, rk) for rk in B.RATERS]))), f'${spent():.3f}')
            score(nhan, res)
