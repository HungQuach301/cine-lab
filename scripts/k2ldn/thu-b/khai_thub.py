#!/opt/cine/bin/python
"""THU-B-T4 · lưu tấm vào git + khai n2p.tam (K-1.17.5 §7) + chạy k2check 1.17.5 (chỉ CHẠY, không đọc mã checks/) và trích hàng BE-MAT-NHA, N2P-1, N2P-3.
  khai_thub.py luu <khung> <tag> [cach…]   → channel-k2/k2c-t4-02/thu-b/tam/<khung>/ (render, mặt nạ, bóng, nha.json — một lần/khung) + <tag>/ (ghép, nền, ảnh AI 1080, video, json)
  khai_thub.py kiem <tên> <khung:tag:cach> … [--vision]  → channel-k2/k2c-t4-02/thu-b/kiem/<tên>/episode.yaml + k2check.md + hang.json
Đường dẫn trong episode.yaml là đường dẫn TƯƠNG ĐỐI tới thư mục yaml (tệp trong git, tái lập được)."""
import json, os, shutil, subprocess, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
THUB = os.environ.get('THUB', '/var/tmp/ldn/thub'); BP = f'{THUB}/bp'
G = os.path.join(REPO, 'channel-k2/k2c-t4-02/thu-b/tam'); KI = os.path.join(REPO, 'channel-k2/k2c-t4-02/thu-b/kiem')
NAM = {'M1-trung': 1666, 'M4-trung': 2026, 'B3-p4-1938': 1938}; SONG = {'M1-trung'}
CHUNG = ['render.png', 'matna.png', 'mat_na_nha.png', 'mat_na_mat.png', 'bong.png', 'albedo.png', 'nha.json', 'nha-chi-tiet.json', 'prep.json', 'do-duoc.png', 'vao.jpg', 'render-khong.png']
RIENG = ['ghep.png', 'nen.png', 'ghep.json', 'ai-1080.png', 'proj.png', 'proj.json', 'tl-anh_tinh.mp4', 'tl-chieu_3d.mp4', 'tl-render.mp4', 'khung0-v0.png', 'khung0-v1.png', 'khung0-v2.png', 'khung0-cuoi.png']


def luu(k, tag):
    d = os.path.join(G, k); os.makedirs(os.path.join(d, tag), exist_ok=True)
    for f in CHUNG:
        s = os.path.join(BP, k, f)
        if os.path.exists(s) and not os.path.exists(os.path.join(d, f)): shutil.copy2(s, os.path.join(d, f))
    for f in RIENG:
        s = os.path.join(BP, k, tag, f)
        if os.path.exists(s): shutil.copy2(s, os.path.join(d, tag, f))
    print('lưu', k, tag)


def kiem(ten, muc, vision=False):
    o = os.path.join(KI, ten); os.makedirs(o, exist_ok=True); rel = lambda p: os.path.relpath(p, o)
    tam = []
    for m in muc:
        k, tag, cach = m.split(':'); d = os.path.join(G, k); t = os.path.join(d, tag)
        e = dict(id=f'{k}-{tag}-{cach}', shot=k, render=rel(f'{d}/render.png'), ghep=rel(f'{t}/ghep.png'), mat_na=rel(f'{d}/matna.png'), nam=NAM[k], anh_tinh=True,
                 be_mat_nha_ai=True, mat_na_nha=rel(f'{d}/mat_na_nha.png'), mat_na_mat=rel(f'{d}/mat_na_mat.png'), bong=rel(f'{d}/bong.png'), nha=rel(f'{d}/nha.json'), nen_ai=False)
        if os.environ.get('LOP_A_KHAI') == '1':   # khai lớp (a) KHÔNG gồm nha_thuong (BE-MAT-NHA (b) giữ nhà không đo được = render) — chỉ để đo N2P-1 cho tấm BMN, ghi rõ trong báo cáo
            e['lop_a'] = ['pho', 'nha', 'trai', 'congsu', 'tau', 'co', 'pin', 'lua', 'nguoi', 'khac']
        if k in SONG: e['song'] = dict(render_co=rel(f'{d}/render.png'), render_khong=rel(f'{d}/render-khong.png'), nen=rel(f'{t}/nen.png'))
        if cach in ('anh_tinh', 'chieu_3d') and os.path.exists(f'{t}/tl-{cach}.mp4'):
            e['be_mat_nha_video'] = dict(ghep=rel(f'{t}/tl-{cach}.mp4'), render=rel(f'{t}/tl-render.mp4'), cach=cach, **({'tam': rel(f'{t}/ghep.png')} if cach == 'chieu_3d' else {}))
        tam.append(e)
    segs = [dict(id=f's{i}', dur=3.0, shots=[dict(id=x['shot'], at=0.0, tpl='scene3d')]) for i, x in enumerate(tam)]
    E = dict(id=f'thu-b-t4-{ten}', title='THU-B-T4 vòng thử (không phải tập)', brand='MOVING PARTS', channel='k2', khung_sach=True, kenh2_tu_t4=True, animatic=False, out=f'/var/tmp/ldn/thub/k2c/{ten}', segments=segs, n2p=dict(noi='London', t4=True, tam=tam))
    import yaml
    # log shot tối thiểu (trường theo RULES-LL 1.17.4 "Khai cho T4"): mỗi tấm một shot CODINH góc cao, lớp N2P = thời lượng, be_mat_nha_ai
    LS = [dict(shot=x['shot'], t0=3.0 * i, t1=3.0 * i + 3.0, dur=3.0, chuong='thu-b', goc='cao', tl=True, cu_may='CODINH', lop={'N2P': 3.0}, ai_nen=False, be_mat_nha_ai=True) for i, x in enumerate(tam)]
    json.dump(LS, open(os.path.join(o, 'log-shot.json'), 'w'), ensure_ascii=False, indent=1); E['log_shot'] = 'log-shot.json'
    yaml.safe_dump(E, open(os.path.join(o, 'episode.yaml'), 'w'), allow_unicode=True, sort_keys=False)
    # timeline TỔNG HỢP tối thiểu (cùng cấu trúc reports/k1172/do/mk_tl.py của K): mỗi tấm một đoạn 3 s — chỉ để k2check chạy được hàng N2P/BE-MAT-NHA
    TL = dict(id=E['id'], title=None, music=[], segments=[], heroes={}); t0 = 0.0
    for sg in segs:
        S = dict(id=sg['id'], dur=3.0, t0=t0, t1=t0 + 3.0, frames=72, speech=[], sfx=[], shots=[dict(sg['shots'][0], t0=0.0, t1=3.0)]); TL['segments'].append(S); t0 += 3.0
    TL['tong_s'] = t0; TL['tong_khung'] = int(round(t0 * 24)); os.makedirs(E['out'], exist_ok=True); json.dump(TL, open(os.path.join(o, 'timeline.json'), 'w'), ensure_ascii=False)
    cmd = [sys.executable, os.path.join(REPO, 'checks/ll/k2check.py'), os.path.join(o, 'episode.yaml'), '--tl', os.path.join(o, 'timeline.json'), '--no-asr', '--cap'] + (['--n2p-vision'] if vision else [])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    open(os.path.join(o, 'k2check.md'), 'w').write(r.stdout + ('\n\n<!-- stderr -->\n```\n' + r.stderr[-6000:] + '\n```\n' if r.stderr.strip() else ''))
    hang = [l for l in r.stdout.splitlines() if l.startswith('| BE-MAT-NHA') or l.startswith('| N2P-') or l.startswith('| LOCK') or l.startswith('| 1.17.5')]
    json.dump({'lenh': ' '.join(os.path.relpath(c, REPO) if c.startswith(REPO) else c for c in cmd), 'ma_thoat': r.returncode, 'hang': hang}, open(os.path.join(o, 'hang.json'), 'w'), ensure_ascii=False, indent=1)
    if os.path.isdir(E['out']): shutil.copytree(E['out'], os.path.join(o, 'vision'), dirs_exist_ok=True, ignore=shutil.ignore_patterns('*.jpg', '*.png'))   # nguyên văn mô hình nhìn + bộ đệm + chi phí (D6)
    print('mã thoát', r.returncode); print('\n'.join(h[:900] for h in hang))
    if not hang: print(r.stdout[-3000:], r.stderr[-3000:])


if __name__ == '__main__':
    if sys.argv[1] == 'luu': luu(sys.argv[2], sys.argv[3])
    else: kiem(sys.argv[2], [x for x in sys.argv[3:] if not x.startswith('--')], '--vision' in sys.argv)
