#!/opt/cine/bin/python
"""Sinh fixture tổng hợp cho selftest 1.16 (phiên K, 19/10/2026). Chạy lại được; kết quả đã commit cạnh tệp này.
  ep-t3/      tập T3 giả (khung_sach: true), 145 s thân phim + 2 thẻ phương pháp × 8 s; log shot, bảng nhịp, XEM CÂM, mô tả, lời khoá, claims,
              log chữ (dạng bo-tl), nam_khung, khối lai (log khung + sổ vân tổng hợp), lớp ranh
  vid/        v-ok.mp4 (3 shot × 12 s: máy cố định trôi 1 %/s · lia 6 %/s · đẩy máy 3 %/s phóng) · v-cat.mp4 (12 shot × 3 s), 320×180, 12 khung/s
Bản sao THẬT: v6/ (log khung + log chữ đoạn thử V6, sổ PT3 vân King's Bastion) · g1b/ (kiem.json phục chế G1b) — chép bằng tay, ghi nguồn ở README.
"""
import json, os, subprocess

import cv2
import numpy as np
import yaml

D = os.path.dirname(os.path.abspath(__file__))
FPS = 12


def jdump(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as f: json.dump(o, f, ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ tập T3 giả
def ep_t3():
    E = dict(id='k116-t3', title='K-1.16 fixture T3', channel='k2', khung_sach=True, out='/var/tmp/k116-fx', heroes={}, segments=[],
             log_shot='log-shot.json', nhip_vat='nhip-vat.json', xem_cam='xem-cam.json', phat_hanh=dict(mo_ta='mo-ta.md'), loi_khoa='loi-khoa.txt',
             claims_md='claims.md', nam_khung='nam-khung.json', log_chu='log-chu.json', ghost={'ghost-1782': {'nguon': 'Spilsbury plan 1782 + OSM'}},
             phuc_che=dict(kiem='../g1b/kiem.json', dung=[dict(anh='342-FH_000757.jpg', cong_cu='swin2sr_x2')]))
    LS, NV = [], []
    vung = ['eo', 'pho', 'vinh', 'nui', 'cang', 'bo']
    segs = []
    for k in range(12):   # 12 shot góc cao × 10 s, 6 điểm máy × 2 năm
        segs.append(dict(id=f'C{k:02d}', chuong=str(1 + k // 4), dur=10.0, goc='cao', diem=f'd{k % 6}', moc=1704 if k < 6 else 1782, vung=vung[k % 6]))
    segs.insert(4, dict(id='KA', chuong='2', dur=8.0, goc='neo', khung_neo=True, vung='pho-hep', moc=1782))
    segs.insert(9, dict(id='LT', chuong='3', dur=8.0, goc='thap', vung='pho', moc=1782))
    segs.insert(12, dict(id='IL', chuong='3', dur=9.0, goc='cao', im_lang=True, vung='vinh', moc=1782, diem='d2'))
    segs[0]['chuong'] = '0'
    for s in segs:
        hk = f"h_{s['id']}"
        E['heroes'][hk] = dict(hero='tl/fx', opt=dict(year=s['moc'], counter={'s': str(s['moc'])}, ghost='ghost-1782' if s['id'] == 'C06' else None), dur=s['dur'])
        sh = dict(tpl='plate', at=0, type='scene3d', vung=s['vung'], noi='thanh_pho' if 'pho' in s['vung'] else 'eo_dat',
                  cau='The Rock changes hands in 1704 after a short fight.' if s['id'] == 'C01' else None,
                  p=dict(sach=True, hero=hk, frame0=0))
        if s.get('khung_neo'): sh['khung_neo'] = True
        if s.get('im_lang'): sh['im_lang'] = True
        if s['id'] == 'C04': sh['p']['the_chuong'] = dict(s='1704 — The Rock changes hands', at=0.5, dur=2.5)
        if s['id'] == 'C08': sh['p']['the_chuong'] = dict(s='1779 — The Great Siege begins', at=0.5, dur=3.0)
        if s['id'] == 'C06': sh['p']['ghost'] = 'ghost-1782'
        sh = {k: v for k, v in sh.items() if v is not None}
        E['segments'].append(dict(id=s['id'], part=f"CH{s['chuong']}", chuong=s['chuong'], dur=s['dur'], beats=[dict(t=0.0, k='cut', s=s['id'])], shots=[sh]))
        LS.append(dict(shot=s['id'], goc=s['goc'], tl=True, vai='a sentry walks the Main Street patrol' if s['goc'] == 'thap' else '',
                       noi='thanh_pho' if 'pho' in s['vung'] else 'eo_dat', trong_pct=20.0, su_kien=[dict(t=2.0, k='xay', s='houses rise')],
                       diem_may=s.get('diem'), moc=s['moc'], bac='bậc 1 (Spilsbury plan) + bậc 5', nguon='Spilsbury plan 1782 + OSM',
                       ai_image=False, ai_texture=s['id'] == 'C03'))
        NV.append(dict(id=f"n-{s['id']}", chinh=True, cau='…', vat=[dict(loai='dem_nam', shot=s['id'])]))
    NV[4]['vat'] = [dict(loai='the_chuong', shot='C04')]
    pp_items = [['How this film was made', 'Built from British and Spanish records and maps: Drinkwater 1786, Montero 1860.', 'Every source is in the description.'],
                ['What is estimated', 'Estimated: building heights and coastline. AI retouched two street frames; no facts.']]
    for i, it in enumerate(pp_items):
        E['segments'].append(dict(id=f'PP{i + 1}', part='END', chuong='5', dur=8.0, the_phuong_phap=True, beats=[dict(t=0.0, k='cut', s='PP')],
                                  shots=[dict(tpl='plate', at=0, type='card', p=dict(sach=True, hero='h_C11', the_phuong_phap=True,
                                                                                    card=dict(type='list', title=it[0], items=[dict(s=x) for x in it[1:]])))]))
        LS.append(dict(shot=f'PP{i + 1}', goc='phang', tl=False))
    E['lai'] = dict(log_khung='lai/log-khung.jsonl', kiem_du_kien_van='lai/kiem-van.json', goi_api_van='lai/goi-api-van.jsonl')
    E['ban_do'] = dict(lop='lop.json')
    E['segments'][1]['shots'][0]['p']['lop'] = ['RANH1704']
    d = os.path.join(D, 'ep-t3')
    os.makedirs(d, exist_ok=True)
    yaml.safe_dump(E, open(os.path.join(d, 'episode.yaml'), 'w'), allow_unicode=True, sort_keys=False)
    jdump(os.path.join(d, 'log-shot.json'), LS)
    jdump(os.path.join(d, 'nhip-vat.json'), dict(nhip=NV))
    jdump(os.path.join(d, 'xem-cam.json'), dict(tat_tieng=True, cau_hoi=[f'Q{i + 1}' for i in range(8)], lan=1,
                                              nguoi_cham=[dict(id='ai-1', vai='ai', dung=7, tong=8), dict(id='ai-2', vai='ai', dung=6, tong=8),
                                                          dict(id='ai-3', vai='ai', dung=8, tong=8), dict(id='chu-du-an', vai='chu_du_an', dung=7, tong=8, ngay='2026-10-19')]))
    open(os.path.join(d, 'mo-ta.md'), 'w').write('Sources: Spilsbury plan 1782; OSM. Borders: Cliopatria (CC BY 4.0).\nAI use = Yes\n')
    open(os.path.join(d, 'loi-khoa.txt'), 'w').write('‹1a›\nThe Rock changes hands in 1704 after a short fight. Nobody expected it to last.\n')
    open(os.path.join(d, 'claims.md'), 'w').write('| C01 | Rock taken 1704 |\n')
    jdump(os.path.join(d, 'nam-khung.json'), [dict(shot='C00', nam_dem=1704, nam_max=dict(nha=1700)), dict(shot='C06', nam_dem=1782, nam_max=dict(nha=1781))])
    jdump(os.path.join(d, 'lop.json'), dict(W=1920, lop=[dict(id='RANH1704', loai='bien_gioi_lich_su', nam=1704, nguon='Cliopatria (CC BY 4.0)', nguon_doi_chieu='OHM',
                                                              lech_tb_px=1.0, giay_phep='CC-BY-4.0', features=[])]))
    # log chữ dạng bo-tl: bộ đếm suốt phim, chip 2,5 s ở C01, thẻ chương C04 góc dưới trái có mờ, thẻ PP
    T, L = 0.0, []
    st = {s['id']: (s['t0'], s['dur']) for s in [dict(id=x['id'], t0=sum(y['dur'] for y in E['segments'][:i]), dur=x['dur']) for i, x in enumerate(E['segments'])]}
    tot = sum(s['dur'] for s in E['segments'])
    for f in range(0, int(tot * 24), 12):
        t = f / 24; it = [dict(s='1704', role='year', cap=52.0, alpha=1.0, box=[60, 960, 220, 1020])]
        a, dd = st['C01']
        if a + 1.0 <= t < a + 3.5: it.append(dict(s='Gibraltar', role='where', cap=30.0, alpha=1.0, box=[1500, 60, 1800, 100]))
        a, dd = st['C04']
        if a + 0.5 <= t < a + 3.0: it.append(dict(s='1704 — The Rock changes hands', role='the_chuong', cap=34.0, alpha=0.4 if t < a + 1.0 or t >= a + 2.5 else 1.0, box=[60, 860, 900, 910]))
        L.append(dict(f=f, items=it))
    jdump(os.path.join(d, 'log-chu.json'), L)
    # khối lai: log khung (C03 vân), sổ vân tổng hợp sạch
    fr = []; f0 = 0
    for s in E['segments']:
        n = int(round(s['dur'] * 24))
        fr += [dict(f=f0 + i, shot=f"{s['id']}/0", ai_image=False, ai_texture=s['id'] == 'C03') for i in range(n)]; f0 += n
    os.makedirs(os.path.join(d, 'lai'), exist_ok=True)
    open(os.path.join(d, 'lai', 'log-khung.jsonl'), 'w').write(''.join(json.dumps(x) + '\n' for x in fr))
    jdump(os.path.join(d, 'lai', 'kiem-van.json'), dict(quy_tac='0 lỗi chắc mới dùng; rà mắt từng tệp; KHÔNG dựa chấm mù',
                                                        tep=[dict(tep='van_a.jpg', anh='van_a', ket_luan='dùng (0 lỗi chắc)', loi_chac=[], nghi_van=[]),
                                                             dict(tep='van_b.jpg', anh='van_b', ket_luan='LOẠI — lỗi chắc', loi_chac=['thêm cửa'], nghi_van=[])]))
    G = [dict(anh=a, ai_texture=True, model_req='gpt-image-x', model_resp='gpt-image-x', prompt='Re-texture the stone wall as weathered limestone ashlar, flat albedo, no new objects.',
              input=dict(file=f'{a}.png', mask=f'{a}_mask.png', mask_frac=0.98), usage=dict(total_tokens=100), usd=0.04, c2pa=True, date_utc='2026-10-18T00:00:00+00:00',
              http=200, file=f'{a}.jpg', sha256='0' * 64) for a in ('van_a', 'van_b')]
    open(os.path.join(d, 'lai', 'goi-api-van.jsonl'), 'w').write(''.join(json.dumps(x) + '\n' for x in G))


# ------------------------------------------------------------------ video tổng hợp
def texture(seed, W=1280, H=720):
    rng = np.random.default_rng(seed)
    b = cv2.GaussianBlur((rng.random((H, W)) * 255).astype(np.float32), (0, 0), 4)
    b = cv2.normalize(b, None, 20, 235, cv2.NORM_MINMAX)
    b += 25 * np.sin(np.linspace(0, 6, W))[None, :].astype(np.float32)   # tông khác nhau giữa các texture → histogram khác
    return np.clip(b + (seed % 5) * 12 - 24, 0, 255)


def shot_frames(tex, n, tx_pct_s=0.0, zoom_pct_s=0.0, w=320, h=180):
    out = []
    for i in range(n):
        t = i / FPS; s = 1 + zoom_pct_s / 100 * t; M = cv2.getRotationMatrix2D((640, 360), 0, s); M[0, 2] -= tx_pct_s / 100 * 640 * t
        im = cv2.warpAffine(tex, M, (1280, 720), borderMode=cv2.BORDER_REFLECT)[180:540, 320:960]
        out.append(cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA).astype(np.uint8))
    return out


def write(path, frames):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', '320x180', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '30', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for f in frames: p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()


def videos():
    d = os.path.join(D, 'vid'); os.makedirs(d, exist_ok=True)
    fr = shot_frames(texture(1), 12 * FPS, tx_pct_s=1.0) + shot_frames(texture(2), 12 * FPS, tx_pct_s=6.0) + shot_frames(texture(3), 12 * FPS, zoom_pct_s=3.0)
    write(os.path.join(d, 'v-ok.mp4'), fr)
    fr = sum((shot_frames(texture(10 + k), 3 * FPS, tx_pct_s=0.5) for k in range(12)), [])
    write(os.path.join(d, 'v-cat.mp4'), fr)


if __name__ == '__main__':
    ep_t3(); videos(); print('ok')
