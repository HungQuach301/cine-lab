import json, sys, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from shapely.geometry import shape, box
S=sys.argv[1]; BB=box(-5.42,36.09,-5.28,36.20)
fig,ax=plt.subplots(figsize=(7,6.2),dpi=90); ax.set_facecolor('#dfe8ee')
def draw(g,**k):
    for p in getattr(g,'geoms',[g]):
        if p.geom_type=='Polygon': xs,ys=p.exterior.xy; ax.fill(xs,ys,**k)
for f in json.load(open(f'{S}/ohm-1782-gib.geojson'))['features']:
    n=f['properties'].get('name:en') or f['properties'].get('name'); g=shape(f['geometry']).intersection(BB)
    if g.is_empty: continue
    c={'Gibraltar':'#c0392b','Spain':'#d4ac0d'}.get(n,'#999')
    draw(g,fc=c,alpha=0.35,ec=c,lw=1.2); 
for f in json.load(open('/root/.cache/nc-bd/ne/ne_10m_admin_0_disputed_areas.geojson'))['features']:
    if f['properties'].get('NAME')=='Gibraltar':
        g=shape(f['geometry']); xs,ys=g.exterior.xy; ax.plot(xs,ys,'k--',lw=1.2,label='Natural Earth 10m "disputed: Gibraltar" (7 đỉnh, bắc 36,141°)')
ax.axhline(36.1550,color='#c0392b',lw=0.8,ls=':',label='mép bắc polygon OHM "Gibraltar" (36,155°) — dùng cho 1713→nay')
ax.plot([],[],color='#d4ac0d',lw=4,alpha=.5,label='OHM "Spain" 1782-01-05→1798 (vùng biển 3 hải lý gồm cả)')
ax.set_xlim(-5.42,-5.28); ax.set_ylim(36.09,36.20); ax.set_aspect(1/0.807)
ax.set_title('Gibraltar 1782 theo OHM: đường hiện đại được gán cho cả 1713→nay.\nLúc 1782 không có "biên giới" ở đây: có chiến tuyến TBN 1730–35 (S032) và eo đất trung lập (S035).',fontsize=9)
ax.legend(fontsize=7.5,loc='lower right'); ax.tick_params(labelsize=7)
plt.tight_layout(); plt.savefig(sys.argv[2])
