import xml.etree.ElementTree as ET, math, json, sys, glob
nodes={}; ways={}; rels=[]
for f in sorted(glob.glob(sys.argv[1]+'/t*.osm')):
    r=ET.parse(f).getroot()
    for n in r.iter('node'): nodes[n.get('id')]=(float(n.get('lon')),float(n.get('lat')),{t.get('k'):t.get('v') for t in n.findall('tag')})
    for w in r.iter('way'): ways[w.get('id')]=([nd.get('ref') for nd in w.findall('nd')],{t.get('k'):t.get('v') for t in w.findall('tag')})
    for rr in r.iter('relation'):
        tg={t.get('k'):t.get('v') for t in rr.findall('tag')}
        if 'building' in tg: rels.append(rr.get('id'))
lat0=36.14; kx=111320*math.cos(math.radians(lat0)); ky=110574
def area(pts):
    xy=[((x+5.35)*kx,(y-lat0)*ky) for x,y in pts]; s=0
    for i in range(len(xy)-1): s+=xy[i][0]*xy[i+1][1]-xy[i+1][0]*xy[i][1]
    return abs(s)/2
zones={'pho_co_trong_tuong':(-5.3560,36.1335,-5.3470,36.1455),'loi_2km2':(-5.3600,36.1250,-5.3450,36.1500)}
out={}
for zn,(x0,y0,x1,y1) in zones.items():
    za=(x1-x0)*kx*(y1-y0)*ky
    b=[];
    for wid,(nds,tg) in ways.items():
        if 'building' not in tg: continue
        pts=[nodes[n][:2] for n in nds if n in nodes]
        if len(pts)<4: continue
        cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
        if not(x0<=cx<=x1 and y0<=cy<=y1): continue
        b.append(dict(a=area(pts),lv='building:levels' in tg,h='height' in tg,sd='start_date' in tg,hist=('historic' in tg or 'heritage' in tg),roof='roof:shape' in tg,t=tg.get('building')))
    A=sum(x['a'] for x in b)
    out[zn]=dict(dien_tich_vung_km2=round(za/1e6,3),so_toa=len(b),tong_dien_tich_mai_m2=round(A),ty_le_phu_mai=round(A/za,3),
      co_levels=sum(x['lv'] for x in b),co_height=sum(x['h'] for x in b),co_start_date=sum(x['sd'] for x in b),co_historic=sum(x['hist'] for x in b),co_roof_shape=sum(x['roof'] for x in b),
      toa_lon_500m2=sum(x['a']>500 for x in b),dien_tich_trung_vi=round(sorted(x['a'] for x in b)[len(b)//2]) if b else 0)
names=['King\'s Bastion','Moorish Castle','Tower of Homage','Landport','Southport','Charles V','Devil\'s Tower','Ragged Staff','South Bastion','Orange Bastion','Montagu','Princess Caroline','Grand Battery','Casemates','Prince Edward','Europa Point','Rosia','Old Mole','Waterport','Cathedral','Convent','Trafalgar Cemetery','North Bastion','Great Siege Tunnels','Lower St','Princess Anne']
g=[]
for src in (nodes.items(),):
    pass
for wid,(nds,tg) in ways.items():
    nm=tg.get('name','')
    if any(k.lower() in nm.lower() for k in names): g.append(('way',nm,tg.get('historic') or tg.get('building') or tg.get('military') or ''))
for nid,(x,y,tg) in nodes.items():
    nm=tg.get('name','')
    if nm and any(k.lower() in nm.lower() for k in names): g.append(('node',nm,tg.get('historic') or tg.get('tourism') or ''))
out['ten_diem_khong_che_osm']=sorted(set(g))
out['so_relation_building']=len(rels)
json.dump(out,sys.stdout,ensure_ascii=False,indent=1)
