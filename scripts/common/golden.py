#!/opt/cine/bin/python
"""NỀN TẢNG · hồi quy KHUNG VÀNG (phiên Nền tảng, 14/10/2026).

Dựng lại một khung cố định của mỗi tập đã phát hành bằng BỘ CÔNG CỤ HIỆN HÀNH (prep → cảnh 3D đúng khung → lớp chữ 2D),
rồi so với khung tham chiếu đã duyệt: khung master trong LFS (đọc thẳng qua HTTP, không tải cả tệp) hoặc ảnh 1080p đã commit.
Không sửa mã dựng; chỉ gọi scripts/k2|ll/{prep.py,ll.py,hero.js,render.js}. Không gọi API trả phí: prep chạy với proxy chặn
(HTTPS_PROXY=127.0.0.1:9) — lời phải có sẵn trong cache vo/, thiếu thì báo LỖI, không thu lại.

  golden.py run   [--only steel,t1,ll08,k2v4] [--out /var/tmp/golden]   → <out>/golden.json, <out>/<ca>/{moi,ref,diff,sheet}.png
  golden.py list

Số đo mỗi ca: pHash 64 bit (DCT 32×32 → 8×8, Hamming — cùng cách scripts/k2/lod_test.py), SSIM ảnh xám (Gauss σ 1,5),
lệch tuyệt đối TB (0–255), tỉ lệ điểm ảnh lệch > 24 mức, và các ô lệch trên lưới 16×9 (ô có > 3 % điểm ảnh lệch > 24 → vùng đổi).
Kết luận: KHỚP khi Hamming ≤ 6, SSIM ≥ 0,90 và không có ô lệch; LỆCH CỤC BỘ khi hai điều đầu đạt nhưng có ô lệch (chữ, nhãn, vật nhỏ
đổi — pHash một mình KHÔNG bắt được, đã thấy ở lần chạy đầu); LỆCH khi còn lại. Ngưỡng tạm, chỉnh sau 3 lần chạy có số đo; master đã qua
yuv420p crf 16 nên không thể giống bit. Không chặn gì: báo để P/chủ dự án xem sheet.jpg (tham chiếu | mới | diff ×4).
"""
import json, math, os, shutil, subprocess, sys, time, urllib.request
import numpy as np, yaml
from PIL import Image
from scipy.fft import dctn
from scipy.ndimage import gaussian_filter

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PY = '/opt/cine/bin/python'
NOPROXY = {'HTTPS_PROXY': 'http://127.0.0.1:9', 'https_proxy': 'http://127.0.0.1:9', 'HTTP_PROXY': 'http://127.0.0.1:9', 'http_proxy': 'http://127.0.0.1:9'}
FPS = 24
# Ca cố định. seg = đoạn; f = khung trong đoạn (shot cảnh 3D, ≈ 2 s sau đầu shot — dựng tuần tự từ khung 0 nên khung sớm = nhanh; cách ranh giới shot ≥ 1,5 s; không footage/ảnh ngoài git).
CASES = {
    'steel': dict(kind='k2', episode='channel-k2/k2g-ep01/episode.yaml', seg='01', f=48, spp=4,
                  # lời Steel: align.json chưa từng được commit cạnh vo/; bản sao duy nhất trong repo nằm ở bộ dữ liệu kiểm của K (chỉ đọc)
                  align_from='checks/ll/fixtures/k2g01/vo', no_repeat_check=True,
                  ref=dict(lfs_branch='release-k2g-ep01-v1', lfs_path='k2g-ep01-v1-master.mp4')),
    't1': dict(kind='k2', episode='channel-k2/k2c-t1-06/episode.yaml', seg='00', f=48, spp=4,
               ref=dict(lfs_branch='release-k2c-t1-06-v1', lfs_path='k2c-t1-06-v1-master.mp4')),
    'll08': dict(kind='ll', episode='reports/m3/ep08/episode.yaml', seg='03', f=48, spp=4,
                 ref=dict(lfs_branch='release-ll-ep08-v1', lfs_path='ll-ep08-v1-master.mp4')),
    # cuộn K2V4: master ngoài git (chỉ SHA) → tham chiếu là khung chấm mù vòng 5 (1280×720, trích từ cuộn 1080p đã duyệt), P1 = H 13,0 s
    'k2v4': dict(kind='k2', timeline='channel-k2/k2v4-mau/K2V4-reel.timeline.json', seg='H', f=312, spp=2,
                 ref=dict(image_key='channel-k2/k2v4-mau/kiem-mu/blind/key.json', pair='P1')),
}
TOOLS = {'k2': dict(prep=['scripts/k2/prep.py', 'prep'], hero='scripts/k2/hero.js', render='scripts/k2/render.js'),
         'll': dict(prep=['scripts/ll/ll.py', 'prep'], hero='scripts/ll/hero.js', render='scripts/ll/render.js')}
PH_MAX, SSIM_MIN = 6, 0.90


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def run(cmd, env=None, log=None, timeout=1800):
    e = dict(os.environ, **(env or {})); e.setdefault('K2V_CACHE', '/var/tmp/cine-out/k2v-cache')
    r = subprocess.run(cmd, cwd=REPO, env=e, capture_output=True, text=True, timeout=timeout)
    if log: open(log, 'a').write(f'$ {" ".join(cmd)[:400]}\n{r.stdout[-4000:]}\n{r.stderr[-4000:]}\n')
    return r


# ---------- số đo ----------
def phash(im):
    a = np.asarray(im.convert('L').resize((32, 32), Image.LANCZOS), dtype=np.float64)
    d = dctn(a, norm='ortho')[:8, :8].flatten(); return d > np.median(d[1:])


def ssim(a, b):
    a = a.astype(np.float64); b = b.astype(np.float64); C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2; g = lambda x: gaussian_filter(x, 1.5)
    ma, mb = g(a), g(b); va, vb, cab = g(a * a) - ma * ma, g(b * b) - mb * mb, g(a * b) - ma * mb
    return float((((2 * ma * mb + C1) * (2 * cab + C2)) / ((ma * ma + mb * mb + C1) * (va + vb + C2))).mean())


def compare(new, ref, outdir):
    if new.size != ref.size: new = new.resize(ref.size, Image.LANCZOS)
    A, B = np.asarray(new.convert('RGB'), dtype=np.int16), np.asarray(ref.convert('RGB'), dtype=np.int16)
    D = np.abs(A - B).max(axis=2)
    ham = int((phash(new) != phash(ref)).sum()); s = ssim(np.asarray(new.convert('L')), np.asarray(ref.convert('L')))
    Image.fromarray(np.clip(D * 4, 0, 255).astype(np.uint8)).save(os.path.join(outdir, 'diff.png'))
    w, h = ref.size; sheet = Image.new('RGB', (w * 3 // 2, h // 2))
    for i, im in enumerate([ref, new, Image.open(os.path.join(outdir, 'diff.png')).convert('RGB')]): sheet.paste(im.resize((w // 2, h // 2), Image.LANCZOS), (i * w // 2, 0))
    sheet.save(os.path.join(outdir, 'sheet.jpg'), quality=85)
    gh, gw = D.shape[0] // 9, D.shape[1] // 16
    cells = [(cx, cy) for cy in range(9) for cx in range(16) if (D[cy * gh:(cy + 1) * gh, cx * gw:(cx + 1) * gw] > 24).mean() > 0.03]
    ok = ham <= PH_MAX and s >= SSIM_MIN
    return dict(phash_hamming=ham, ssim=round(s, 4), mad=round(float(np.abs(A - B).mean()), 2), px_gt24_pct=round(100 * float((D > 24).mean()), 2),
                o_lech=len(cells), o_lech_ds=cells[:40], ket_qua='KHỚP' if ok and not cells else 'LỆCH CỤC BỘ' if ok else 'LỆCH')


# ---------- tham chiếu ----------
def lfs_href(branch, path):
    ptr = subprocess.run(['git', 'cat-file', '-p', f'origin/{branch}:{path}'], cwd=REPO, capture_output=True, text=True).stdout
    kv = dict(l.split(' ', 1) for l in ptr.splitlines() if ' ' in l); oid = kv['oid'].split(':')[1]; size = int(kv['size'])
    url = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=REPO, capture_output=True, text=True).stdout.strip()
    url = url[:-4] if url.endswith('.git') else url
    req = urllib.request.Request(url + '.git/info/lfs/objects/batch', method='POST', headers={'Accept': 'application/vnd.git-lfs+json', 'Content-Type': 'application/vnd.git-lfs+json'},
                                 data=json.dumps({'operation': 'download', 'transfers': ['basic'], 'objects': [{'oid': oid, 'size': size}]}).encode())
    j = json.load(urllib.request.urlopen(req, timeout=60)); return j['objects'][0]['actions']['download']['href'], oid


def ref_frame(c, gframe, outdir, log):
    R = c['ref']; p = os.path.join(outdir, 'ref.png')
    if 'lfs_branch' in R:
        href, oid = lfs_href(R['lfs_branch'], R['lfs_path'])
        ss = (gframe - 0.25) / FPS   # tìm chính xác: khung đầu tiên có pts ≥ ss = khung gframe
        r = run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{ss:.5f}', '-i', href, '-frames:v', '1', p], log=log, timeout=300)
        if r.returncode: raise RuntimeError('không trích được khung master: ' + r.stderr[-300:])
        return p, f"LFS {R['lfs_branch']}:{R['lfs_path']} (oid {oid[:12]}) khung {gframe}"
    key = json.load(open(os.path.join(REPO, R['image_key']))); k = key[R['pair']]
    src = os.path.join(os.path.dirname(os.path.join(REPO, R['image_key'])), R['pair'], k['moi'] + '.jpg'); shutil.copy(src, p)
    return p, f"{os.path.relpath(src, REPO)} (khung mới của cặp {R['pair']}, {k.get('moi_s')} s)"


# ---------- dựng ----------
def timeline_for(name, c, W, log, notes):
    if c.get('timeline'):
        TL = json.load(open(os.path.join(REPO, c['timeline'])))
        return TL, TL.get('heroes', {})
    E = yaml.safe_load(open(os.path.join(REPO, c['episode']), encoding='utf-8'))
    E['out'] = W; E.setdefault('vo_dir', os.path.join(os.path.dirname(c['episode']), 'vo'))
    E['shorts'] = []   # khung vàng chỉ cần đoạn; Short có thể thiếu align trong cache
    if c.get('align_from'):   # cache lời: mp3/txt từ vo_dir của tập + align.json từ nguồn chỉ đọc
        vd = os.path.join(W, 'vo'); os.makedirs(vd, exist_ok=True); src = os.path.join(REPO, E['vo_dir'])
        for f in os.listdir(src): _ln(os.path.join(src, f), os.path.join(vd, f))
        for f in os.listdir(os.path.join(REPO, c['align_from'])): _ln(os.path.join(REPO, c['align_from'], f), os.path.join(vd, f))
        E['vo_dir'] = vd
    ep = os.path.join(W, 'episode.yaml'); yaml.safe_dump(E, open(ep, 'w'), allow_unicode=True, sort_keys=False)
    T = TOOLS[c['kind']]
    r = run([PY] + T['prep'] + [ep], env=NOPROXY, log=log)
    if r.returncode and c.get('no_repeat_check') and 'LẶP GÓC MÁY' in (r.stdout + r.stderr):
        notes.append('prep chuẩn của bộ công cụ hiện hành CHẶN tập này: luật lặp góc máy (chủ dự án 12/10) ra đời sau khi tập phát hành; '
                     'khung vàng dựng bằng prep bỏ qua đúng phép kiểm đó (prep._load), không đổi gì khác')
        r = run([PY, '-c', 'import sys;sys.path.insert(0,"scripts/k2");import prep;prep.ll.load=prep._load;prep.ll.prep(sys.argv[1])', ep], env=NOPROXY, log=log)
    if r.returncode or not os.path.exists(os.path.join(W, 'timeline.json')):
        raise RuntimeError('prep lỗi: ' + (r.stderr or r.stdout)[-600:])
    TL = json.load(open(os.path.join(W, 'timeline.json')))
    H = json.load(open(os.path.join(W, 'heroes.json'))) if os.path.exists(os.path.join(W, 'heroes.json')) else {}
    return TL, H


def _ln(a, b):
    if os.path.lexists(b): os.remove(b)
    os.symlink(a, b)


def need_frames(sh, t_local):
    x = max(0.0, (t_local - sh['t0']) * FPS * (sh['p'].get('speed') or 1)) + (sh['p'].get('off') or 0); i0 = math.floor(x + 1e-6)
    return {i0, i0 + 1}


def run_case(name, c, out):
    W = os.path.join(out, name); shutil.rmtree(W, ignore_errors=True); os.makedirs(W); log = os.path.join(W, 'log.txt'); notes = []; t0 = time.time()
    TL, H = timeline_for(name, c, W, log, notes)
    seg = [s for s in TL['segments'] if s['id'] == c['seg']][0]; f = c['f']; tl = f / FPS; gframe = int(round(seg['t0'] * FPS)) + f
    # cảnh 3D: dựng đúng khung cần cho các shot plate đang hiện; các shot plate khác của đoạn chỉ cần thư mục (khung giữ chỗ, không vẽ)
    byd = {v['dir']: (k, v) for k, v in H.items()}; done = {}; hero_s = 0.0
    for sh in seg['shots']:
        if sh.get('tpl') != 'plate': continue
        d0 = sh['p']['dir']; k, hv = byd.get(d0) or (sh['p'].get('hero'), H.get(sh['p'].get('hero')))
        if hv is None: raise RuntimeError(f'không thấy cảnh 3D cho {d0}')
        nd = os.path.join(W, 'hero', os.path.basename(d0)); n = int(math.ceil(float(hv['dur']) * FPS)); sh['p']['dir'] = nd
        active = sh['t0'] <= tl < sh['t1']
        if active and nd not in done:
            # hero.js chỉ tất định khi dựng TUẦN TỰ từ khung 0 (đo 15/10: cảnh có người đi bộ k2c106/corner, --only 48 lệch khung 48
            # của lượt tuần tự tới 244 mức ở vùng người — trạng thái tích luỹ). Nên dựng 0..khung cần, chọn khung sớm trong shot.
            idx = list(range(0, min(n, max(need_frames(sh, tl)) + 1)))
            w, h = hv.get('size', [1920, 1080])
            cmd = ['node', TOOLS[c['kind']]['hero'], '--hero', hv['hero'], '--variant', hv.get('variant', 'a'), '--dur', str(hv['dur']), '--w', str(w), '--h', str(h),
                   '--spp', str(c['spp']), '--opt', json.dumps(hv.get('opt', {}), separators=(',', ':')), '--out', nd, '--only', ','.join(map(str, idx))]
            ts = time.time(); r = run(cmd, log=log); hero_s += time.time() - ts
            if r.returncode: raise RuntimeError(f'hero.js lỗi ({hv["hero"]}): ' + r.stderr[-600:])
            done[nd] = (hv['hero'], idx)
        os.makedirs(nd, exist_ok=True)
        real = sorted(x for x in os.listdir(nd) if x.endswith('.jpg'))
        if not real:   # shot không hiện ở khung này: một khung đen giữ chỗ
            Image.new('RGB', tuple(hv.get('size', [1920, 1080]))).save(os.path.join(nd, '00000.jpg')); real = ['00000.jpg']
        for i in range(n):
            p = os.path.join(nd, f'{i:05d}.jpg')
            if not os.path.exists(p): _ln(os.path.join(nd, real[0]), p)
    tlp = os.path.join(W, 'timeline.golden.json'); json.dump(TL, open(tlp, 'w'))
    sid = seg['id']; jd = os.path.join(W, 'jpg')
    r = run(['node', TOOLS[c['kind']]['render'], '--tl', tlp, '--seg', sid, '--out', os.path.join(W, 'x.mkv'), '--only', str(f), '--jpgdir', jd], log=log)
    jp = os.path.join(jd, f'{sid}_f{f:05d}.jpg')
    if r.returncode or not os.path.exists(jp): raise RuntimeError('render.js lỗi: ' + r.stderr[-600:])
    new = Image.open(jp).convert('RGB'); new.save(os.path.join(W, 'moi.png'))
    rp, rdesc = ref_frame(c, gframe, W, log)
    m = compare(new, Image.open(rp).convert('RGB'), W)
    return dict(ca=name, doan=sid, khung_trong_doan=f, khung_toan_tap=gframe, giay=round(gframe / FPS, 3), canh_3d={os.path.basename(k): v for k, v in done.items()},
                tham_chieu=rdesc, spp=c['spp'], **m, giay_dung_3d=round(hero_s, 1), giay_tong=round(time.time() - t0, 1), ghi_chu=notes)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('run', 'list'): sys.exit(__doc__)
    if sys.argv[1] == 'list':
        for k, c in CASES.items(): print(k, c.get('episode') or c.get('timeline'), 'đoạn', c['seg'], 'khung', c['f'])
        return
    out = arg('out', '/var/tmp/golden'); os.makedirs(out, exist_ok=True)
    only = (arg('only') or ','.join(CASES)).split(','); res = []; T0 = time.time()
    for k in only:
        try: res.append(run_case(k, CASES[k], out))
        except Exception as e: res.append(dict(ca=k, ket_qua='LỖI', loi=str(e)[-800:]))
        r = res[-1]; print(f"{k:6} {r['ket_qua']:5} " + (f"pHash {r['phash_hamming']}/64 · SSIM {r['ssim']} · MAD {r['mad']} · >24: {r['px_gt24_pct']} % · ô lệch {r['o_lech']}/144 · {r['giay_tong']} s" if 'ssim' in r else r.get('loi', '')[:300]), flush=True)
    S = dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), repo_head=subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.strip(),
             nguong=dict(phash_max=PH_MAX, ssim_min=SSIM_MIN), giay_tong=round(time.time() - T0, 1), ca=res)
    json.dump(S, open(os.path.join(out, 'golden.json'), 'w'), ensure_ascii=False, indent=1)
    print(f"tổng {S['giay_tong']} s → {os.path.join(out, 'golden.json')}")
    sys.exit(0 if all(r['ket_qua'] == 'KHỚP' for r in res) else 1)


if __name__ == '__main__':
    main()
