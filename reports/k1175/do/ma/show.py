import json,sys
d=json.load(open(sys.argv[1]))
for x in d:
    if x['loai'] in ('am','thuc'): print(x['nua'],x['nen'],x['ca'],'DAT' if x['dat'] else 'TRUOT', x['giua'], x['thua'], [ (t.get('x0'),t.get('sau_px'),t.get('rho'),t.get('alpha'),t.get('h_vat_px')) for t in x['thua_ct'][:3]])
    else:
        print(x['nua'],x['nen'],x['ca'],'bat',sum(h['bat'] for h in x['hit']),'/',len(x['hit']),'thua',x['thua'], x['giua'])
        for h in x['hit']:
            if not h['bat'] and h['d']>=6: print('    MISS',h['x0'],h['x1'],h['d'],[(s['x0'],s['sau_px'],s['truc'],s['rho'],s['dai']) for s in h['seg']])
