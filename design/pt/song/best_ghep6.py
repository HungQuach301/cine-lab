"""V6 · ghép các dải ngang của bản tốt nhất (best6.py, BEST_BORDER) thành một nền 'A tốt nhất' đủ lượt cho compose4/live6:
d2.png, depth.exr, cls.exr lấy theo dải; các lượt khác + lượt nắng + meta sao từ nền A sản xuất (chỉ khung trưa được dùng).
  /opt/cine/bin/python best_ghep6.py <nền A sx> <ra> <dải0_dir:y0,y1> <dải1_dir:y0,y1> ..."""
import os, sys, shutil, json, numpy as np, cv2
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lai'))
import lai_common as LC
A, OUT = sys.argv[1:3]; parts = [(p.split(':')[0], tuple(map(float, p.split(':')[1].split(',')))) for p in sys.argv[3:]]
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(A):
    if f not in ('d2.png', 'depth.exr', 'cls.exr'): shutil.copy(os.path.join(A, f), OUT)
d2 = None; dep = None; cls = None; meta = {'dai': [], 'nguoi3d': []}
for d, (y0, y1) in parts:
    im = cv2.imread(os.path.join(d, 'd2.png'), cv2.IMREAD_UNCHANGED); H = im.shape[0]
    r0, r1 = int(round(H * (1 - y1))), int(round(H * (1 - y0)))          # biên Blender đo từ dưới lên
    de = LC.exr(os.path.join(d, 'depth.exr')); cl = LC.exr(os.path.join(d, 'cls.exr'))
    if d2 is None: d2, dep, cls = im.copy(), de.copy(), cl.copy()
    d2[r0:r1] = im[r0:r1]; dep[r0:r1] = de[r0:r1]; cls[r0:r1] = cl[r0:r1]
    m = json.load(open(os.path.join(d, 'meta.json'))); meta['dai'].append({'dir': d, 'hang': [r0, r1], 'renders': m.get('renders'), 'nguoi3d': m.get('nguoi3d'), 'total_s': m.get('total_s')})
cv2.imwrite(os.path.join(OUT, 'd2.png'), d2)
import OpenEXR
for nm, arr in (('depth.exr', dep), ('cls.exr', cls)):
    OpenEXR.File({'compression': OpenEXR.ZIP_COMPRESSION, 'type': OpenEXR.scanlineimage}, {'V': np.ascontiguousarray(arr.astype(np.float32))}).write(os.path.join(OUT, nm))
m = json.load(open(os.path.join(OUT, 'meta.json'))); m['ban_tot_nhat'] = meta; json.dump(m, open(os.path.join(OUT, 'meta.json'), 'w'), indent=1, ensure_ascii=False)
print('ok', [x['hang'] for x in meta['dai']], 'render_s', [x['renders'][0]['render_s'] if x['renders'] else None for x in meta['dai']])
