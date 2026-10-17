import json, sys, shapely, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from shapely.geometry import shape, box
S, OUT = sys.argv[1], sys.argv[2]
BB = box(-14, 33, 6, 53)
land = [shape(f['geometry']).intersection(BB) for f in json.load(open('/root/.cache/nc-bd/ne/ne_50m_land.geojson'))['features'] if shape(f['geometry']).intersects(BB)]
LAND = shapely.union_all(land)
clio = [(f['properties']['Name'], shape(f['geometry'])) for f in json.load(open(f'{S}/clio-1782.geojson'))['features'] if not f['properties']['Name'].startswith('(')]
FAC = {'Kingdom of Great Britain': ('#b03a2e', 'Britain'), 'Kingdom of Spain': ('#c9a227', 'Spain'), 'Kingdom of France': ('#2e5c8a', 'France')}
def draw(ax, g, **k):
    for p in getattr(g, 'geoms', [g]):
        if p.geom_type == 'Polygon': xs, ys = p.exterior.xy; ax.fill(xs, ys, **k)
fig = plt.figure(figsize=(16, 9), dpi=60)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_facecolor('#d9cfb8')   # sepia biển
for g in land: draw(ax, g, fc='#efe4c8', ec='#6b5a3e', lw=0.8)
for n, g in clio:
    c, lab = FAC.get(n, ('#a89f8a', None)); g = g.intersection(LAND)
    draw(ax, g, fc=c, alpha=0.30 if lab else 0.12, ec=c, lw=2.2 if lab else 0.8)
# Gibraltar = điểm, không polygon
ax.plot(-5.35, 36.14, 'o', ms=13, mfc='#b03a2e', mec='white', mew=2.5)
ax.text(-5.1, 35.6, 'Gibraltar', fontsize=20, color='#2b2216', weight='bold')
# tuyến SƠ ĐỒ (chưa có claim)
import numpy as np
from scipy.interpolate import CubicSpline
wp=np.array([(-4.2,50.1),(-6.2,48.9),(-9.6,45.0),(-10.6,40.5),(-10.0,37.6),(-8.2,36.3),(-6.4,35.95),(-5.62,36.02)])
tt=np.r_[0,np.cumsum(np.hypot(*np.diff(wp,axis=0).T))]; cs=CubicSpline(tt,wp); u=np.linspace(0,tt[-1],200); xy=cs(u)
ax.plot(xy[:-6,0],xy[:-6,1],lw=4,ls=(0,(4,3)),color='#b03a2e')
ax.annotate('',xy=xy[-1],xytext=xy[-7],arrowprops=dict(arrowstyle='-|>',lw=4,color='#b03a2e',mutation_scale=30))
ax.text(-13.7, 47.3, 'Relief convoy\n(route: SCHEMATIC —\nclaims pending)', fontsize=17, color='#7a241c', weight='bold')
for x, y, t in [(-4.3, 40.2, 'SPAIN'), (1.0, 46.6, 'FRANCE'), (-1.6, 51.35, 'GREAT BRITAIN')]: ax.text(x, y, t, fontsize=22, color='#2b2216', weight='bold', ha='center')
ax.set_xlim(-14, 6); ax.set_ylim(33.6, 53); ax.set_xticks([]); ax.set_yticks([])
ax.add_patch(Rectangle((-13.8, 33.75), 9.6, 1.25, fc='#2b2216', alpha=0.82))
ax.text(-13.6, 34.1, 'approx. borders c. 1782 — Cliopatria (Seshat), CC BY 4.0', fontsize=17, color='white')
ax.text(5.6, 34.2, '1782', fontsize=40, color='#2b2216', weight='bold', ha='right')
# inset mẫu (cỡ 12 % diện tích khung: 0.3464 x 0.3464 cạnh)
w = 0.3464; h = 0.3464 * 16 / 9 * 9 / 16
fig.text(0.5, 0.975, 'NC-BD · KHUNG MINH HOẠ luật (a)(c): ranh giới thời kỳ có nhãn nguồn, Gibraltar là điểm, tuyến chuyển động; tuyến ở đây là SƠ ĐỒ, chưa có claim', ha='center', fontsize=11, color='#5a0000')
plt.savefig(OUT, dpi=60)
