import json, sys, shapely, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import shape, box
S=sys.argv[1]; OUT=sys.argv[2]
BB=box(-10.5,35.5,4.5,52)
land=[shape(f['geometry']).intersection(BB) for f in json.load(open('/root/.cache/nc-bd/ne/ne_50m_land.geojson'))['features'] if shape(f['geometry']).intersects(BB)]
def hb(y):
    out=[]
    for f in json.load(open(f'/root/.cache/nc-bd/data/hb_world_{y}.geojson'))['features']:
        g=shape(f['geometry']); g=g if g.is_valid else g.buffer(0)
        if g.intersects(BB): out.append((f['properties'].get('NAME'), g.intersection(BB)))
    return out
def gj(p, key):
    return [(f['properties'].get(key) or f['properties'].get('name'), shape(f['geometry'])) for f in json.load(open(p))['features']]
cols=[('OpenHistoricalMap (CC0 + CC BY 4.0 từng đường)', lambda y: gj(f'{S}/ohm-{y}-full.geojson','name:en')),
      ('Cliopatria v0.2.1 (CC BY 4.0)', lambda y: [r for r in gj(f'{S}/clio-{y}.geojson','Name') if not str(r[0]).startswith('(')]),
      ('historical-basemaps (GPL-3.0)', lambda y: hb({1704:1700,1782:1783,1941:1938}[y]))]
pal=['#c0392b','#2e86c1','#d4ac0d','#239b56','#8e44ad','#ca6f1e','#17a589','#7f8c8d','#a93226','#5b2c6f','#b9770e','#1f618d']
fig,axs=plt.subplots(3,3,figsize=(12,13.2),dpi=80)
def draw(ax,g,**k):
    for p in getattr(g,'geoms',[g]):
        if p.geom_type=='Polygon':
            xs,ys=p.exterior.xy; ax.fill(xs,ys,**k)
        elif hasattr(p,'geoms'): draw(ax,p,**k)
for r,y in enumerate((1704,1782,1941)):
    for c,(t,fn) in enumerate(cols):
        ax=axs[r][c]; ax.set_facecolor('#dfe8ee')
        for g in land: draw(ax,g,fc='#efe9dc',ec='#555',lw=0.4)
        fs=fn(y); names=sorted({str(n) for n,_ in fs})
        for n,g in fs:
            col=pal[names.index(str(n))%len(pal)]
            g=g.intersection(shapely.union_all(land)) if c<2 else g
            draw(ax,g,fc=col,alpha=0.35,ec=col,lw=0.8)
        ax.plot(-5.35,36.14,marker='*',ms=9,color='k')
        ax.set_xlim(-10.5,4.5); ax.set_ylim(35.5,52); ax.set_aspect(1/0.7); ax.set_xticks([]); ax.set_yticks([])
        lab={1704:'1704',1782:'1782',1941:'1941'}[y]+('' if c<2 else f" (tệp {dict([(1704,1700),(1782,1783),(1941,1938)])[y]})")
        ax.set_title(f"{t}\n{lab} — {len(fs)} vùng", fontsize=9)
fig.suptitle('NC-BD · so 3 nguồn ranh giới lịch sử, Iberia–Pháp–Anh (★ = Gibraltar). Đất: Natural Earth 1:50m (PD). Ảnh kiểm, không dùng lên hình.', fontsize=10)
plt.tight_layout(); plt.savefig(OUT, dpi=80)
