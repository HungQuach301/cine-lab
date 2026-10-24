import json,sys
for f in sys.argv[1:]:
    d=json.load(open(f))
    for nua in sorted({x['nua'] for x in d}):
        X=[x for x in d if x['nua']==nua]; am=[x for x in X if x['loai']=='am']; du=[h for x in X if x['loai'] in ('duong','duong_thuc') for h in x['hit']]
        ks=sorted({h['d'] for h in du}); 
        print(f.split('/')[-1], nua, 'âm đạt', sum(x['dat'] for x in am),'/',len(am), [x['ca'] for x in am if not x['dat']][:8], '| bắt ≥8:', sum(h['bat'] for h in du if h['d']>=8),'/',sum(1 for h in du if h['d']>=8), '| <8:', sum(h['bat'] for h in du if h['d']<8),'/',sum(1 for h in du if h['d']<8), '| thừa', sum(x['thua'] for x in X if x['loai']=='duong'))
