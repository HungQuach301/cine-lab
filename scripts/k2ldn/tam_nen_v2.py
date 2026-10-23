#!/opt/cine/bin/python
"""LOOK-T4-V2 · TẤM NỀN N2+ cho 4 khung rộng máy cố định (Kinh thánh §15 b–c): chuẩn bị ảnh vào → ghép lại lớp (a) theo mặt nạ ID + khớp màu render VÀO tông tấm nền
→ cổng kiểm (i)–(iv) (kiem_n2p.py + vision_kiem.py: gpt-6.1-sol + claude-sonnet-5-5; q_thoi_dai.py của K chỉ CHẠY) → (v) nhấp nháy trên timelapse 3 s.
  tam_nen_v2.py prep <khung>                    → $V2/tn/<khung>/{vao.jpg, render.png, matna.png}
  tam_nen_v2.py ghep <khung> <tag> <ai.(jpg|png)>   → $V2/tn/<khung>/<tag>/{render-khop.png, ghep.png, ghep.jpg, ghep.json}
  tam_nen_v2.py kiem <khung> <tag>              → + <tag>-kiem.json (+ iii trong hộp địa hình, q_thoi_dai)
  tam_nen_v2.py tl <khung> <tag> [--clip ra.mp4] → (v) nhấp nháy: ghép tấm (640×360) + lớp (a) từng khung timelapse; đối chứng = cùng đường ghép với tấm = khung render đầu
Lớp (a) (luật §15 a, như T6 tiền kỳ): mọi điểm mặt nạ thuộc LOP_A (nhà/công trình/cầu/tường 'nha', thuyền 'tau', nhà xa ngoài hộp 'khac') + LỬA/KHÓI 3D (điểm ảnh khác nhau giữa
render có lửa và không lửa > 8/255, nở 2 px → nhãn 'lua'). Hộp địa hình đã dựng = mọi điểm KHÔNG phải 'suon' (đất xa ngoài hộp, look2.js) và không phải 'khac'/'troi'.
Phóng ảnh AI về 1920×1080: Lanczos (cv2.INTER_LANCZOS4) — không dùng bộ phóng AI."""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, str(Path(__file__).resolve().parent / 'ai'))
os.environ.setdefault('N2P_DIR', str(Path(__file__).resolve().parents[2] / 'reports/look-t4-v2'))
import n2p_lib as L  # noqa: E402
import kiem_n2p as K  # noqa: E402
V2 = Path(os.environ.get('V2_DIR', '/var/tmp/ldn/v2')); RR = V2 / 'r'
NAM = {'M1-rong': 1666, 'M1-trung': 1666, 'M3-rong': 1940, 'M4-rong': 2026}
REPO = Path(__file__).resolve().parents[2]; PY = '/opt/cine/bin/python'


def prep(k):
    d = V2 / 'tn' / k; d.mkdir(parents=True, exist_ok=True)
    R = cv2.imread(str(RR / k / 'lut.jpg')); M = cv2.imread(str(RR / f'{k}-mask1' / '00000.png'))   # khung V2 đã áp LUT kênh (look hợp nhất)
    if k == 'M3-rong':
        N = cv2.imread(str(RR / 'M3-rong-khonglua' / 'lut.jpg')); vao = N
        diff = np.abs(R.astype(np.int16) - N.astype(np.int16)).max(-1) > 8
        diff = cv2.dilate(diff.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        M = M.copy(); M[diff] = L.PAL['lua'][::-1]; pct = float(diff.mean() * 100)
    else: vao = R; pct = 0.0
    cv2.imwrite(str(d / 'vao.jpg'), vao, [cv2.IMWRITE_JPEG_QUALITY, 92]); cv2.imwrite(str(d / 'render.png'), R); cv2.imwrite(str(d / 'matna.png'), M)
    Lb = L.idmap(d / 'matna.png'); st = {n: round(float((Lb == i).mean() * 100), 2) for i, n in enumerate(L.NAMES) if (Lb == i).any()}
    json.dump({'khung': k, 'nam': NAM[k], 'lua_pct': round(pct, 2), 'lop_pct': st, 'sha_vao': L.sha_file(d / 'vao.jpg'), 'sha_render': L.sha_file(d / 'render.png')}, open(d / 'prep.json', 'w'), ensure_ascii=False, indent=1)
    print(k, 'lửa %', round(pct, 2), st)


def ghep(k, tag, ai):
    d = V2 / 'tn' / k; o = d / tag; o.mkdir(parents=True, exist_ok=True)
    R = cv2.imread(str(d / 'render.png')); H, W = R.shape[:2]; AI = cv2.resize(cv2.imread(str(ai)), (W, H), interpolation=cv2.INTER_LANCZOS4)
    Lb = L.idmap(d / 'matna.png', (W, H)); A = L.lop_mask(Lb, L.LOP_A); Ab = L.bao_ve(A, no=1, nho_px=60, no_nho=3)
    lab = lambda x: cv2.cvtColor(x, cv2.COLOR_BGR2LAB).astype(np.float32)
    Rl, Al = lab(R), lab(AI); mr, sr = Rl[Ab].mean(0), Rl[Ab].std(0) + 1e-3; ma, sa = Al[Ab].mean(0), Al[Ab].std(0) + 1e-3
    kk = np.array([0.7, 0.7, 0.7], np.float32)                          # khớp màu render VÀO tông tấm nền (một phép Lab toàn cục, tất định) — như T6 tiền kỳ
    RK = cv2.cvtColor(np.clip((Rl - mr) * (1 + kk * (sa / sr - 1)) + mr + kk * (ma - mr), 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    G, _ = L.ghep(RK, AI, Ab, feather=3, bao=False)
    cv2.imwrite(str(o / 'render-khop.png'), RK); cv2.imwrite(str(o / 'ghep.png'), G); cv2.imwrite(str(o / 'ghep.jpg'), G, [cv2.IMWRITE_JPEG_QUALITY, 93])
    rec = {'tag': tag, 'ai': str(ai), 'sha_ai': L.sha_file(ai), 'khop_mau': {'k': kk.tolist(), 'mean_render': mr.tolist(), 'mean_ai': ma.tolist(), 'std_render': sr.tolist(), 'std_ai': sa.tolist()},
           'pct_lop_a': round(float(A.mean() * 100), 2), 'pct_vung_bao_ve': round(float(Ab.mean() * 100), 2), 'pct_diem_anh_ai': round(float((~Ab).mean() * 100), 2), 'sha_ghep_png': L.sha_file(o / 'ghep.png')}
    json.dump(rec, open(o / 'ghep.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(rec)[:300])


def kiem(k, tag):
    d = V2 / 'tn' / k; o = d / tag; nam = NAM[k]
    cmd = [PY, '-I', str(REPO / 'scripts/k2ldn/ai/kiem_n2p.py'), '--render', str(o / 'render-khop.png'), '--ai', str(o / 'ghep.png'), '--da-ghep', '--id', str(d / 'matna.png'),
           '--nam', str(nam), '--tag', tag, '--out', str(o), '--noi', 'London'] + (['--t4'] if nam == 1666 else [])
    env = dict(os.environ); subprocess.run(cmd, check=False, env=env)
    J = json.load(open(o / f'{tag}-kiem.json'))
    R = cv2.imread(str(o / 'render-khop.png')); G = cv2.imread(str(o / 'ghep.png')); Lb = L.idmap(d / 'matna.png', (R.shape[1], R.shape[0]))
    Lh = Lb.copy(); Lh[np.isin(Lb, [L.NAMES.index('suon'), L.NAMES.index('khac')])] = L.NAMES.index('troi')   # chỉ trong hộp địa hình đã dựng
    _, k3h, _, _ = K.may(R, G, Lh)
    J['iii_doi_vung']['trong_hop_dia_hinh'] = dict(k3h, ghi_chu='cùng công thức T9/T9b, chỉ tính điểm thuộc hộp địa hình đã dựng (bỏ đất xa ngoài hộp và nhà xa) — phép (iii) đang được K-1.17.4 xét; KHÔNG dùng để tự nới')
    q = o / 'qtd'; q.mkdir(exist_ok=True)
    r = subprocess.run([PY, str(REPO / 'checks/ll/q_thoi_dai.py'), '--anh', str(o / 'ghep.png'), '--nam', str(nam), '--noi', 'London', '--out', str(q), '--api', '--json', str(q / 'qtd.json')],
                       capture_output=True, text=True, env=env)
    try: J['ii_thoi_dai']['q_thoi_dai'] = json.load(open(q / 'qtd.json'))
    except Exception: J['ii_thoi_dai']['q_thoi_dai'] = {'loi': (r.stdout + r.stderr)[-800:]}
    json.dump(J, open(o / f'{tag}-kiem.json', 'w'), ensure_ascii=False, indent=1)
    print(tag, 'đạt cả (i–iv, toàn khung):', J['dat_ca'], '| iii toàn khung', {x: J['iii_doi_vung'][x] for x in ('t9b_dat_thanh_nuoc_pct', 't9b_nuoc_thanh_dat_pct')}, '| trong hộp', {x: k3h[x] for x in ('t9b_dat_thanh_nuoc_pct', 't9b_nuoc_thanh_dat_pct')})


def flicker(frames, region):
    g = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for f in frames]
    return float(np.mean([np.abs(g[i + 1] - g[i])[region].mean() for i in range(len(g) - 1)]))


def tl(k, tag, clip=None):
    d = V2 / 'tn' / k; o = d / tag; W, H = 640, 360
    def lutdir(x):                                     # áp LUT kênh A cho cả dãy khung (ffmpeg lut3d, nội suy tứ diện — như look_lut.py ap)
        src = V2 / 'tl' / x; dst = src / 'lut'
        if not (dst / '00000.jpg').exists():
            dst.mkdir(exist_ok=True); lut = REPO / 'channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube'
            subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-start_number', '0', '-i', str(src / '%05d.jpg'), '-vf', f"lut3d=file='{lut}':interp=tetrahedral", '-q:v', '2', '-start_number', '0', str(dst / '%05d.jpg')], check=True)
        return sorted(dst.glob('[0-9]*.jpg'))
    fs = lutdir(k); nofire = lutdir(f'{k}-khonglua') if k == 'M3-rong' else None
    Lb = L.idmap(d / 'matna.png', (W, H)); A0 = L.lop_mask(Lb, [n for n in L.LOP_A if n != 'lua'])
    gh = json.load(open(o / 'ghep.json'))['khop_mau']; kk = np.array(gh['k'], np.float32); mr, sr, ma, sa = [np.array(gh[x], np.float32) for x in ('mean_render', 'std_render', 'mean_ai', 'std_ai')]
    plate = cv2.resize(cv2.imread(str(o / 'ghep.png')), (W, H), interpolation=cv2.INTER_AREA)
    def khop(x): l = cv2.cvtColor(x, cv2.COLOR_BGR2LAB).astype(np.float32); return cv2.cvtColor(np.clip((l - mr) * (1 + kk * (sa / sr - 1)) + mr + kk * (ma - mr), 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    out, ctl, raw = [], [], []; base0 = None
    for i, f in enumerate(fs):
        R = cv2.imread(str(f)); A = A0.copy()
        if nofire:
            N = cv2.imread(str(nofire[i])); A |= cv2.dilate((np.abs(R.astype(np.int16) - N.astype(np.int16)).max(-1) > 8).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        Ab = L.bao_ve(A, no=1, nho_px=20, no_nho=1); RK = khop(R)
        if base0 is None: base0 = RK.copy()
        out.append(L.ghep(RK, plate, Ab, feather=2, bao=False)[0]); ctl.append(L.ghep(RK, base0, Ab, feather=2, bao=False)[0]); raw.append(R)
    stat = ~(cv2.dilate(L.lop_mask(Lb, L.LOP_A).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0)
    rec = {'khung': len(fs), 'nhap_nhay_ghep': round(flicker(out, stat), 4), 'nhap_nhay_doi_chung': round(flicker(ctl, stat), 4), 'nhap_nhay_render_tho': round(flicker(raw, stat), 4)}
    rec['ty_le'] = round(rec['nhap_nhay_ghep'] / max(rec['nhap_nhay_doi_chung'], 1e-4), 3); rec['dat'] = rec['nhap_nhay_ghep'] <= 1.5 * max(rec['nhap_nhay_doi_chung'], 1e-4) + 0.01
    (o / 'tl').mkdir(exist_ok=True)
    for i, x in enumerate(out): cv2.imwrite(str(o / 'tl' / f'{i:05d}.jpg'), x, [cv2.IMWRITE_JPEG_QUALITY, 92])
    json.dump(rec, open(o / f'{tag}-v.json', 'w'), indent=1); print(tag, '(v)', rec)


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'prep': prep(sys.argv[2])
    elif c == 'ghep': ghep(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == 'kiem': kiem(sys.argv[2], sys.argv[3])
    elif c == 'tl': tl(sys.argv[2], sys.argv[3])
