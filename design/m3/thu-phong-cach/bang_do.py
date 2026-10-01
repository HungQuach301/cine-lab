"""Cine Lab · M3 THỬ PHONG CÁCH — bảng giây render mỗi khung (trung bình, trung vị, bỏ khung đầu) từ reports/m3/thu-phong-cach/do/*.timing.json."""
import glob, json, os, statistics as st
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../reports/m3/thu-phong-cach/do')
for p in sorted(glob.glob(D + '/*.timing.json')):
    r = json.load(open(p)); t = r['times']
    print(f"{os.path.basename(p):24s} {r['W']}x{r['H']}  khung {len(t):3d}  TB {st.mean(t):.3f}  trung vị {st.median(t):.3f}  TB bỏ khung đầu {st.mean(t[1:]) if len(t) > 1 else t[0]:.3f}")
