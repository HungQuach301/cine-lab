#!/opt/cine/bin/python
"""Sinh fixture 1.15 (phiên K, 18/10/2026). Chạy lại: /opt/cine/bin/python checks/ll/fixtures/k115/make_fixtures.py [--that <thư mục gốc dữ liệu thật>]
  ep-lai/   tập giả 60 s có một shot LAI 6 s (log mọi khung, log chữ, kiem-du-kien, goi-api, cặp PNG vùng bảo vệ, cặp đêm, khung LAI) — K-LAI-1…6, B
  bc/       bộ timelapse giả 10 s: mặt nạ có nuoc_pct/co_trong_pct, log vật, khung + mặt nạ + pháp tuyến hero (có vân) — BC2…BC4
  o2/       ảnh O2 (ve_co.py; 2 khung PT thật) + hop-co.json + cache.json (trả lời Claude đã ghi của lượt chạy thật 18/10)
  v5b2b/    SAO dữ liệu thật đoạn thử V5b-2b (origin/v5b2b reports/v5b2b/do + doan-thu/episode.yaml) — I8, BC2
  pt2/      SAO sổ thật PT2 (origin/pt2-lai reports/pt2: kiem-du-kien.json, ai-c/goi-api.jsonl, log/log-LAI-960x540.jsonl) — K-LAI-3/5/6 trên dữ liệu thật
Phần SAO chỉ chạy khi có --that (cây `git archive` của các nhánh trên); không có thì giữ bản đã commit."""
import json, os, shutil, sys

import cv2
import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
J = lambda p, x: json.dump(x, open(os.path.join(D, p), 'w'), ensure_ascii=False, indent=1)
FPS = 24
LABEL40 = 'Surface detail AI-assisted · layout, landmarks & flags from sources'[:40]


def mk(*p): os.makedirs(os.path.join(D, *p), exist_ok=True)


# ---------------------------------------------------------------- ep-lai
def ep_lai():
    mk('ep-lai'); mk('ep-lai', 'bao-ve'); mk('ep-lai', 'dem'); mk('ep-lai', 'khung-lai')
    ep = dict(id='k2c-t9-lai', title='Fixture LAI', out='/var/tmp/cine-out/k2c-t9-lai',
              segments=[dict(id='a', dur=30.0, shots=[dict(type='scene3d', p=dict(where='Gibraltar')), dict(type='scene3d', p=dict(where='Gibraltar'))]),
                        dict(id='b', dur=30.0, shots=[dict(type='scene3d', khung_neo=True, ai_image=True, p=dict(where='Gibraltar')), dict(type='card', p=dict())])],
              lai=dict(log_khung='log-khung.jsonl', log_chu='log-chu.json', kiem_du_kien='kiem-du-kien.json', goi_api='goi-api.jsonl', duyet='duyet.yaml',
                       bao_ve=[dict(lai='bao-ve/lai.png', a='bao-ve/a.png', mat_na='bao-ve/mat-na.png', bat_buoc='bao-ve/bat-buoc.png')],
                       dem=[dict(lai='dem/lai.png', a='dem/a.png')], khung_lai='khung-lai'))
    import yaml
    open(os.path.join(D, 'ep-lai', 'episode.yaml'), 'w').write('# Fixture K-1.15: tập 60 s, shot b/0 (30–36 s, khung 720–863) là khung neo LAI 1782.\n'
                                                             + yaml.safe_dump(ep, allow_unicode=True, sort_keys=False))
    with open(os.path.join(D, 'ep-lai', 'log-khung.jsonl'), 'w') as f:
        for i in range(60 * FPS):
            ai = 720 <= i < 864; sh = 'a/0' if i < 360 else 'a/1' if i < 720 else 'b/0' if i < 864 else 'b/1'
            f.write(json.dumps(dict(f=i, t=round(i / FPS, 3), ai_image=ai, nhan_phuong_phap=ai, shot=sh)) + '\n')
    J('ep-lai/log-chu.json', [dict(f=i, text=([dict(s=LABEL40, role='method', px1080=38.0, box=[40, 980, 760, 1026])] if 720 <= i < 864 else [])
                                                + [dict(s='1782', role='year', px1080=72.0, box=[40, 880, 200, 960])]) for i in range(0, 60 * FPS, 12)])
    J('ep-lai/kiem-du-kien.json', dict(phien='fixture', cach_kiem='so A↔LAI theo vùng + rà tay 200 %/400 %; KHÔNG dùng chấm mù', bang_chung='kiem/bang-chung.jpg',
                                       khung_neo={'k1782': dict(tam_C_dung='c-1782-d2-lan2.png (lần sinh 2)', loi_chac_cuoi=0, nghi_van_con_lai=0,
                                                                ngoai_le_cho_duyet=['X1'], duoc_dung=True)},
                                       tong=dict(loi_chac_truoc_xu_ly=1, loi_chac_cuoi=0, nghi_van_cuoi_nhe=0)))
    open(os.path.join(D, 'ep-lai', 'duyet.yaml'), 'w').write(yaml.safe_dump([dict(ma='X1', khung_neo='k1782', nguoi_ky='Chủ dự án', vai='chu_du_an', ngay='2026-10-18',
                                                                                  ket_luan='chap_nhan', ghi_chu='công-xon ban công: chi tiết phụ của vật bảo vệ')],
                                                                             allow_unicode=True, sort_keys=False))
    base = dict(khung_neo='k1782', moc=1782, ai_image=True, endpoint='POST /v1/images/edits', model_req='gpt-image-2.5-sunburst', model_resp='gpt-image-2.5-sunburst',
                prompt='Edit this photograph-like image: a narrow lane in Gibraltar in September 1782 … (prompt nguyên văn giả cho fixture, đủ dài > 40 ký tự)',
                mask=dict(pct_duoc_sua=65.7, quy_uoc='alpha 0 = được sửa'), input=dict(pass_='d2'), http=200, usage=dict(input_tokens=1946, output_tokens=1522),
                usd=0.0629, c2pa=True, date_utc='2026-10-18T00:01:48+00:00')
    g1 = dict(base, anh='c-1782-d2', lan_thu=1, file='c-1782-d2.png', sha256='a' * 64); g2 = dict(base, anh='c-1782-d2-lan2', lan_thu=2, file='c-1782-d2-lan2.png', sha256='b' * 64)
    for g in (g1, g2): g['input'] = {'pass': 'd2'}
    with open(os.path.join(D, 'ep-lai', 'goi-api.jsonl'), 'w') as f:
        for g in (g1, g2): f.write(json.dumps(g, ensure_ascii=False) + '\n')
    rng = np.random.default_rng(115); H, W = 180, 320
    A = rng.integers(40, 200, (H, W, 3), dtype=np.uint8); L = A.copy(); m = np.zeros((H, W), np.uint8); m[:60] = 255; m[60:, 250:] = 255   # trời + mép phải
    L[m == 0] = np.clip(A[m == 0].astype(int) + rng.integers(-40, 40, (int((m == 0).sum()), 3)), 0, 255).astype(np.uint8)
    bb = np.zeros_like(m); bb[:40] = 255
    for nm, x in (('a', A), ('lai', L), ('mat-na', m), ('bat-buoc', bb)): cv2.imwrite(os.path.join(D, 'ep-lai', 'bao-ve', nm + '.png'), x)
    dA = np.full((H, W, 3), 30, np.uint8); dA[60:, :] = 18; dL = np.clip(dA.astype(int) * 1.12, 0, 255).astype(np.uint8)   # đêm: LAI ≈ 1,25× độ chói tuyến tính
    cv2.imwrite(os.path.join(D, 'ep-lai', 'dem', 'a.png'), dA); cv2.imwrite(os.path.join(D, 'ep-lai', 'dem', 'lai.png'), dL)
    for k, s in enumerate((0.30, 0.34)):   # khung LAI bão hoà vừa (≤ 0,40)
        hsv = np.zeros((360, 640, 3), np.uint8); hsv[..., 0] = 15; hsv[..., 1] = int(255 * s); hsv[..., 2] = 170 + (np.indices((360, 640))[1] // 40 % 4 * 10)
        cv2.imwrite(os.path.join(D, 'ep-lai', 'khung-lai', f'{k:05d}.jpg'), cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])


# ---------------------------------------------------------------- bc
def hero_frame(rng, textured=True, H=360, W=640):
    """khung + mặt nạ (R 200, G 0, B 7 = hero id 7) + pháp tuyến: hero = khối nhà giữa khung"""
    im = np.full((H, W, 3), (200, 170, 140), np.uint8); mk_ = np.zeros((H, W, 3), np.uint8); N = np.zeros((H, W, 3), np.uint8); N[...] = (128, 255, 128)
    y0, y1, x0, x1 = 90, 300, 180, 460
    mk_[y0:y1, x0:x1] = (7, 0, 200)
    if textured:
        blk = rng.integers(90, 200, ((y1 - y0) // 6 + 1, (x1 - x0) // 8 + 1), dtype=np.uint8)
        tex = cv2.resize(blk, (x1 - x0, y1 - y0), interpolation=cv2.INTER_NEAREST)
        for c in range(3): im[y0:y1, x0:x1, c] = tex
        for x in range(x0 + 20, x1 - 20, 40): im[y0 + 30:y1 - 30:60, x:x + 14] = 30   # cửa sổ
        ang = (np.indices((y1 - y0, x1 - x0))[1] // 70) % 2   # mặt tường xoay ±35°
        nx = np.where(ang == 0, np.sin(np.radians(35)), -np.sin(np.radians(35))); nz = np.cos(np.radians(35))
        N[y0:y1, x0:x1, 2] = ((nx + 1) * 127.5).astype(np.uint8); N[y0:y1, x0:x1, 1] = 128; N[y0:y1, x0:x1, 0] = int((nz + 1) * 127.5)
    else:
        im[y0:y1, x0:x1] = (150, 175, 195)
        N[y0:y1, x0:x1] = (int((1 + 1) * 127.5), 128, 128)   # mọi pháp tuyến cùng hướng (BGR: z = 1)
    return im, mk_, N


def bc():
    mk('bc'); [mk('bc', 'hero', x) for x in ('khung', 'mat-na', 'phap-tuyen')]
    n = 10 * FPS
    M = [dict(f=i, noi='thanh_pho' if i < 120 else 'bien', content_pct=62.0 if i < 120 else 8.0, fabric_pct=55.0 if i < 120 else 3.0,
              nuoc_pct=8.0 if i < 120 else 70.0, co_trong_pct=12.0 if i < 120 else 0.0) for i in range(n)]
    J('bc/noi-dung-mask.json', M)
    V = []
    for i in range(0, n, 6):
        vat = [dict(id='q1', loai='quan', h_px=9.0 + (i % 24) / 12), dict(id='t1', loai='tau', h_px=14.0)]
        if i < 6: vat.append(dict(id='q2', loai='quan', h_px=4.0))   # khối vừa vào khung (≤ 0,25 s): không tính
        else: vat.append(dict(id='q2', loai='quan', h_px=7.5))
        V.append(dict(f=i, vat=vat))
    J('bc/log-vat.json', V)
    rng = np.random.default_rng(7)
    for f in range(130, 190, 12):
        im, m, N = hero_frame(rng, True)
        cv2.imwrite(os.path.join(D, 'bc', 'hero', 'khung', f'{f:05d}.jpg'), im, [cv2.IMWRITE_JPEG_QUALITY, 92])
        cv2.imwrite(os.path.join(D, 'bc', 'hero', 'mat-na', f'{f:05d}.png'), m); cv2.imwrite(os.path.join(D, 'bc', 'hero', 'phap-tuyen', f'{f:05d}.png'), N)
    J('bc/bo-tl.json', dict(ten='fixture BC (K-1.15)', fps=FPS, mat_na='noi-dung-mask.json', noi=[dict(t=[0.0, 5.0], noi='thanh_pho'), dict(t=[5.0, 10.0], noi='bien')],
                            log_vat='log-vat.json', hero_anh=dict(khung='hero/khung', mat_na='hero/mat-na', phap_tuyen='hero/phap-tuyen', hero_id=7)))


# ---------------------------------------------------------------- sao dữ liệu thật
def sao(that):
    v = os.path.join(that, 'v5b2b', 'reports', 'v5b2b'); mk('v5b2b')
    for p in ('do/bo-tl.json', 'do/campath.json.gz', 'do/log-chu.json', 'do/noi-dung-mask.json.gz', 'doan-thu/episode.yaml'):
        shutil.copy(os.path.join(v, p), os.path.join(D, 'v5b2b', os.path.basename(p)))
    p2 = os.path.join(that, 'pt2', 'reports', 'pt2'); mk('pt2')
    for p in ('kiem-du-kien.json', 'ai-c/goi-api.jsonl', 'log/log-LAI-960x540.jsonl'): shutil.copy(os.path.join(p2, p), os.path.join(D, 'pt2', os.path.basename(p)))


if __name__ == '__main__':
    ep_lai(); bc()
    if '--that' in sys.argv: sao(sys.argv[sys.argv.index('--that') + 1])
