import json, sys, shapely, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shapely.geometry import shape, box
OUT = sys.argv[1]
fig = plt.figure(figsize=(16, 9), dpi=60)
bg = fig.add_axes([0, 0, 1, 1]); bg.set_facecolor('#7d8a92'); bg.set_xticks([]); bg.set_yticks([])
bg.text(0.5, 0.5, 'shot 3D (vd. 2m vịnh 13/9/1782)', ha='center', fontsize=30, color='white', transform=bg.transAxes)
bg.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, ec='white', ls='--', lw=1.5, transform=bg.transAxes)); bg.text(0.055, 0.92, 'vùng an toàn 5 %', color='white', fontsize=12, transform=bg.transAxes)
# inset: 12 % diện tích = 0.24 W x 0.5 H? -> chọn 0.30 W x 0.40 H = 12 %
x0, y0, W, H = 0.66, 0.53, 0.29, 0.41
ia = fig.add_axes([x0, y0, W, H]); ia.set_facecolor('#d9cfb8')
BB = box(-10.5, 34.5, 4.5, 44.5)
for f in json.load(open('/root/.cache/nc-bd/ne/ne_50m_land.geojson'))['features']:
    g = shape(f['geometry'])
    if g.intersects(BB):
        for p in getattr(g.intersection(BB), 'geoms', [g.intersection(BB)]):
            if p.geom_type == 'Polygon': xs, ys = p.exterior.xy; ia.fill(xs, ys, fc='#efe4c8', ec='#6b5a3e', lw=0.8)
ia.add_patch(Rectangle((-5.9, 35.75), 1.1, 0.8, fill=False, ec='#b03a2e', lw=3))
ia.plot(-5.35, 36.14, 'o', ms=8, mfc='#b03a2e', mec='white', mew=2)
ia.text(-3.6, 40.0, 'SPAIN', fontsize=16, weight='bold', color='#2b2216', ha='center'); ia.text(-5.0, 35.2, 'Gibraltar', fontsize=14, weight='bold', color='#2b2216')
ia.set_xlim(-10.5, 4.5); ia.set_ylim(34.5, 44.5); ia.set_aspect(1/0.8); ia.set_xticks([]); ia.set_yticks([])
for s in ia.spines.values(): s.set_edgecolor('white'); s.set_linewidth(4)
fig.text(x0 + 0.005, y0 - 0.04, 'Map: Natural Earth', fontsize=12, color='white')
fig.text(0.5, 0.01, f'NC-BD · KHUNG MINH HOẠ inset (b): góc trên phải, {W*H*100:.0f} % diện tích khung, trong vùng an toàn; hộp đỏ = khung máy đang nhìn', ha='center', fontsize=13, color='white')
plt.savefig(OUT, dpi=60)
print('inset area %', W*H*100)
