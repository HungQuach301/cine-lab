#!/opt/cine/bin/python
"""ANIMATIC-T4 · việc 6 — ẢNH ĐẦU minh hoạ M-d dựng từ CẢNH 3D (look2) ở máy tầm người 0–40 m (§15 f), cùng giờ/năm với hai shot 3D kẹp hai bên.
Mỗi shot MD → channel-k2/k2c-t4-02/animatic/md/<ma>-dau.json (1280×720, spp 8, 1 khung) → render_look.js → $ANIM_MD/<ma>/00000.jpg.
Độ cao máy = mặt đất LiDAR DTM (2026) + `h` (trên sông: mặt nước 0,6 m + `h`). Không AI ở bước này.
  md_dau.py [ma …]   (không đối số: mọi shot MD)"""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent)); import may_v2 as MV  # noqa: E402
REPO = MV.REPO; EP = MV.EP; OUT = EP / 'animatic/md'; R = Path(os.environ.get('ANIM_MD', '/var/tmp/anim/md'))
LD = Path(os.environ.get('LDN_DATA', '/var/tmp/ldn')) / 'lidar'
# ma: (máy E, N, cao trên đất | ('song', cao), nhìn E, N, cao nhìn trên đất, fov, thời gian)
CAM = {
 'H1-01a': ([532902, 180716], 3.0, [532898, 180800], 4.0, 50, ('h66', 1.10, 1.10)),
 'H1-01b': ([532896, 180752], 2.5, [532906, 180812], 10.0, 55, ('h66', 1.35, 1.35)),
 'H1-02': ([532842, 180676], 3.0, [532846, 180760], 5.0, 50, ('h66', 2.0, 2.0)),
 'H1-05a': ([532705, 180548], ('song', 3.0), [532765, 180622], 4.0, 50, ('h66', 9.0, 9.0)),
 'H1-05b': ([532650, 180505], ('song', 2.5), [532790, 180600], 8.0, 50, ('h66', 9.5, 9.5)),
 'H1-08a': ([532300, 180385], 2.5, [532480, 180880], 20.0, 45, ('h66', 19.2, 19.2)),
 'H1-10': ([532355, 181045], 3.0, [532250, 181062], 4.0, 50, ('h66', 34.0, 34.0)),
 'H1-12': ([532520, 180490], ('song', 2.5), [532700, 180820], 15.0, 50, ('h66', 44.0, 44.0)),
 'H1-14': ([532035, 181098], 3.0, [532100, 181140], 12.0, 50, ('h66', 93.5, 93.5)),
 'H1-17a': ([532700, 181760], 3.0, [532720, 181900], 3.0, 50, ('h66', 84.0, 84.0)),
 'H1-17b': ([532650, 181800], 3.0, [532800, 181850], 3.0, 50, ('h66', 90.5, 90.5)),
 'H1-19': ([532500, 181050], 3.0, [532600, 181055], 4.0, 50, ('h66', 130.0, 130.0)),
 'H2-01a': ([532300, 181100], 3.0, [532125, 181150], 25.0, 50, ('y', 1666.72, 1666.72, [9, 16, 11.0], 0)),
 'H2-01b': ([532450, 180950], 3.0, [532550, 180985], 3.0, 50, ('y', 1666.72, 1666.72, [9, 16, 14.0], 0)),
 'H2-03a': ([532400, 181000], 3.0, [532500, 181020], 1.0, 50, ('y', 1667.2, 1667.2, [3, 10, 11.0], 0)),
 'H2-04a': ([532500, 181100], 3.0, [532550, 181120], 6.0, 50, ('y', 1668.0, 1668.0, [6, 1, 11.0], 0)),
 'H2-04b': ([532600, 181150], 3.0, [532700, 181162], 4.0, 50, ('y', 1668.4, 1668.4, [6, 1, 15.0], 0)),
 'H2-13': ([532300, 180600], ('song', 2.0), [532118, 181150], 80.0, 45, ('y', 1711.0, 1711.0, [9, 1, 16.0], 0)),
 'H3-02a': ([532855, 180470], ('song', 3.0), [532790, 180560], 10.0, 50, ('y', 1758.0, 1758.0, [9, 1, 11.0], 0)),
 'H3-04b': ([532700, 181150], 2.0, [532800, 181160], 4.0, 50, ('y', 1935.0, 1935.0, [9, 1, 10.0], 0)),
 'H4-01b': ([532400, 181150], 2.0, [532200, 181150], 30.0, 50, ('d', [1940, 12, 29, 15.8], [1940, 12, 29, 15.8], 0)),
 'H4-03': ([532600, 180610], ('song', 2.0), [532700, 180760], 6.0, 50, ('h40', 3.0, 3.0)),
 'H4-04b': ([532060, 181140], 26.0, [532118, 181150], 70.0, 55, ('h40', 4.5, 4.5)),
 'H5-07a': ([532250, 180385], 2.0, [532118, 181150], 80.0, 40, ('d', [2026, 9, 2, 22.0], [2026, 9, 2, 22.0], 1)),
}


def dtm():
    M = json.loads((LD / 'meta.json').read_text()); A = np.load(LD / 'dtm_kham_1m.npy', mmap_mode='r'); return M, A


def ground(M, A, e, n):
    x0, y1 = M['bbox27700'][0], M['bbox27700'][3]
    i, j = int(y1 - n), int(e - x0)
    if 0 <= i < A.shape[0] and 0 <= j < A.shape[1]:
        v = float(A[i, j]); return v if np.isfinite(v) and v > -50 else 5.0
    return 5.0


def main(ids):
    B = json.loads((EP / 'BANG-SHOT-v2.json').read_text()); rows = {r['ma']: r for r in B['shot']}
    M, A = dtm(); OUT.mkdir(parents=True, exist_ok=True); R.mkdir(parents=True, exist_ok=True)
    for ma in (ids or [k for k in CAM]):
        (pe, ph, le, lh, fov, tg) = CAM[ma]
        z = 0.6 + ph[1] if isinstance(ph, tuple) else ground(M, A, *pe) + ph
        lz = ground(M, A, *le) + lh
        r = dict(rows[ma]); r = dict(r, cu_may='CODINH', may={'p': [*pe, round(z, 2)], 'l': [*le, round(lz, 2)], 'fov': fov}, tieu_diem_en=[*le, round(lz, 2)], them={})
        j = MV.shot_json(r, tg, 1 / 24, 0.0, ma + '-dau'); j.update(W=1280, H=720, spp=8, dur=1 / 24, md=True, vai=rows[ma]['vai'])
        p = OUT / f'{ma}-dau.json'; p.write_text(json.dumps(j, ensure_ascii=False))
        o = R / ma
        if not (o / '00000.jpg').exists():
            subprocess.run(['node', 'scripts/k2ldn/render_look.js', '--shot', str(p), '--out', str(o), '--page', 'look2', '--only', '0'], cwd=REPO, env=dict(os.environ, LDN_DATA=str(LD.parent)),
                           stdout=subprocess.DEVNULL, stderr=open(str(o) + '.log', 'w'))
        print(ma, j['look_ten'], j['keys'][0]['p'], (o / '00000.jpg').exists())


if __name__ == '__main__': main(sys.argv[1:])
