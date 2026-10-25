#!/opt/cine/bin/python
"""THU-B-T4 · (D) ĐO khung toàn cảnh P1 fov 36°: V2 · D · D + vân nướng → reports/thu-b-t4/do/d-<khung>.json
  do_d.py <khung> …      (đọc $THUB/r/<khung>-{v2,d,d2}/00000.jpg + log.json; mặt nạ lớp -m1 (look3b) / -dm1 (look3d))
Đo: bão hoà HSV trung vị (cả khung, giữa), trời %, sương %, trời + sương % (thước look_do.py của LOOK-T4, chỉ CHẠY), chi tiết |Laplace|, s/khung (log), tam giác (ldn2.json),
kiểm công trình có tên KHÔNG đổi: ở biến thể D, điểm ảnh mặt nạ mã công trình (look2 --mask 2) không đổi (so V2) — xem báo cáo."""
import json, os, subprocess, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
THUB = os.environ.get('THUB', '/var/tmp/ldn/thub'); RR = f'{THUB}/r'; D = os.environ.get('LDN_DATA', '/var/tmp/ldn')
LUT = os.path.join(REPO, 'channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube'); OUT = os.path.join(REPO, 'reports/thu-b-t4/do'); os.makedirs(OUT, exist_ok=True)


def main():
    for k in sys.argv[1:]:
        res = {}
        for v, mk, lk in (('v2', 'm1', 'look2'), ('d', 'dm1', 'look3d'), ('d2', 'dm1', 'look3d')):
            src = f'{RR}/{k}-{v}/00000.jpg'
            if not os.path.exists(src): continue
            dst = f'{THUB}/test/{k}-{v}-lut.jpg'
            subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', src, '-vf', f"lut3d=file='{LUT}':interp=tetrahedral", '-q:v', '2', dst], check=True)
            r = subprocess.run(['/opt/cine/bin/python', os.path.join(REPO, 'scripts/k2ldn/look_do.py'), dst, '--mask', f'{RR}/{k}-{mk}/00000.png'], capture_output=True, text=True)
            m = json.loads(r.stdout); L = json.load(open(f'{RR}/{k}-{v}/log.json'))
            m.update(s_khung_1080=round(L['s_per_frame'], 2), setup_s=L.get('setup_s'), tam_giac=json.load(open(f'{D}/{lk}/ldn2.json'))['tam_giac'], tep=os.path.basename(dst))
            res[v] = m
        json.dump(res, open(f'{OUT}/d-{k}.json', 'w'), ensure_ascii=False, indent=1); print(k, json.dumps({v: {x: res[v].get(x) for x in ('bao_hoa_tv', 'troi_suong_pct', 's_khung_1080', 'tam_giac')} for v in res}, ensure_ascii=False))


if __name__ == '__main__': main()
