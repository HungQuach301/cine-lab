#!/opt/cine/bin/python
"""K-1.17.9 · chạy k2check trên tấm E của BAN-CUOI-T4-A (đầu vào CHỈ ĐỌC @bc1693b5, git archive vào /var/tmp/k1179/in) — 0 lệnh API.
Bộ đệm mô hình nhìn TÁI TẠO từ câu trả lời thô có trong git (`e/kiem/<tấm>/vision/<tấm>-{gpt,claude}.raw.txt`): khoá tính bằng chính hàm của
checks (q_n2p_vision.khoa_de + q_k1178.PROMPT_E điền danh sách mốc đo từ mat_na_ct) → k2check đọc bộ đệm như lượt gốc (không gọi mạng).
Khác lượt gốc của phiên A (nêu rõ): (1) không có bộ đệm q_thoi_dai (N2P-2 (b) không chạy — tệp O2 không vào git); (2) video đối chứng render
(`*-tl-render.mp4`) ngoài git → bỏ `n2p.video` (N2P-5 không đo) — cả 1.17.8 và 1.17.9 cùng điều kiện nên bảng hàng đổi không bị ảnh hưởng.
  e_k2.py <nhãn phiên bản> <thư mục ra> [tấm …]           (tấm = tên thư mục e/kiem/*, hoặc đường dẫn episode.yaml của tấm ghép thử KN-8)
"""
import glob, json, os, subprocess, sys, yaml

REPO = os.environ.get('K_REPO', '/home/user/cine-lab'); sys.path.insert(0, REPO)
IN = '/var/tmp/k1179/in/channel-k2/k2c-t4-02/ban-cuoi/e'


def abs_(base, p): return p if not p or os.path.isabs(p) else os.path.normpath(os.path.join(base, p))


def cache_tu_raw(E, ep_dir, vision_dir):
    import cv2
    from checks.ll import q_k1178 as K78, q_n2p as N, q_n2p_vision as QV
    C = {}
    for t in E['n2p']['tam']:
        tid = str(t['id']); rp, gp, mp = (abs_(ep_dir, t[k]) for k in ('render', 'ghep', 'mat_na'))
        R = cv2.imread(rp); H, W = R.shape[:2]; bang = K78.bang_e(t); L, names = N.idmap(mp, (W, H), bang)
        D = N.do_tam(rp, gp, mp, K78.lop_a_e(t), bang, None, bo_a=K78.BO_PX_E); G = cv2.imread(gp)
        if G.shape != R.shape: G = cv2.resize(G, (W, H), interpolation=cv2.INTER_AREA)
        CT, toa, _ = K78._ct(t, ep_dir, (W, H)); F = K78.chan_troi(R, G, L, names, D['_A'], CT, toa)
        pr = K78.PROMPT_E.format(noi=t.get('noi', E['n2p'].get('noi', '')) or 'the place', nam=int(float(t['nam'])), truoc='{truoc}', sau='{sau}',
                                 moc=K78.de_bai_e(F['toa'], W, H), loai=', '.join(f'"{a}" ({b})' for a, b in QV.LOAI.items()))
        k = QV.khoa_de(rp, gp, t['nam'], dict(prompt=pr, ver=K78.PROMPT_VER_E), ('gpt', 'claude'))
        res = {}
        for mh in ('gpt', 'claude'):
            f = os.path.join(vision_dir, f'{tid}-{mh}.raw.txt')
            if os.path.exists(f): res[mh] = dict(meta=dict(nguon='raw.txt trong git @bc1693b5'), json=QV.parse(open(f).read()))
        if len(res) == 2: C[k] = dict(ket_qua=res, prompt_ver=K78.PROMPT_VER_E, loi=None, chi_phi_usd=0.0)
    return C


def chay(nhan, ra, ep_path, vision_dir=None):
    ep_dir = os.path.dirname(ep_path); E = yaml.safe_load(open(ep_path)); tid = E['n2p']['tam'][0]['id']
    d = os.path.join(ra, tid); os.makedirs(d, exist_ok=True)
    for t in E['n2p']['tam']:
        for k in ('render', 'ghep', 'mat_na', 'mat_na_ct'):
            if t.get(k): t[k] = abs_(ep_dir, t[k])
    E['n2p'].pop('video', None); E['out'] = d; E['log_shot'] = abs_(ep_dir, E.get('log_shot', 'log-shot.json'))
    if vision_dir and os.path.isdir(vision_dir):
        json.dump(cache_tu_raw(E, ep_dir, vision_dir), open(os.path.join(d, 'n2p-vision-cache.json'), 'w'), ensure_ascii=False)
    yaml.safe_dump(E, open(os.path.join(d, 'episode.yaml'), 'w'), allow_unicode=True, sort_keys=False)
    tl = abs_(ep_dir, 'timeline.json')
    r = subprocess.run(['/opt/cine/bin/python', 'checks/ll/k2check.py', os.path.join(d, 'episode.yaml'), '--tl', tl, '--no-asr', '--cap'],
                       cwd=REPO, capture_output=True, text=True, env=dict(os.environ, NO_PROXY='*', no_proxy='*', HTTPS_PROXY='http://127.0.0.1:9', https_proxy='http://127.0.0.1:9'))
    open(os.path.join(d, f'k2check-{nhan}.md'), 'w').write(r.stdout + ('\n\n<!-- stderr -->\n' + r.stderr[-3000:] if r.returncode not in (0, 1) else ''))
    print(nhan, tid, 'rc', r.returncode, flush=True)


if __name__ == '__main__':
    nhan, ra = sys.argv[1], sys.argv[2]; tams = sys.argv[3:] or sorted(os.path.basename(p) for p in glob.glob(f'{IN}/kiem/*'))
    for x in tams:
        if x.endswith('.yaml'): chay(nhan, ra, x, os.path.join(os.path.dirname(x), 'vision'))
        else: chay(nhan, ra, f'{IN}/kiem/{x}/episode.yaml', f'{IN}/kiem/{x}/vision')
