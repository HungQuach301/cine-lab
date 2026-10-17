import json,hashlib,glob,re,subprocess,html,os,sys
files={}
for p in glob.glob('/var/tmp/cine-out/t3b/a*/**/*',recursive=True):
    if os.path.isfile(p) and os.path.getsize(p)<400e6:
        h=hashlib.sha256(open(p,'rb').read()).hexdigest(); files.setdefault(h,p)
def text(p):
    b=open(p,'rb').read()
    if b[:4]==b'%PDF':
        return subprocess.run(['pdftotext',p,'-'],capture_output=True).stdout.decode('utf8','ignore')
    t=b.decode('utf8','ignore')
    if '<html' in t.lower()[:5000] or '<!doctype' in t.lower()[:200]:
        t=re.sub(r'(?s)<(script|style).*?</\1>','',t); t=html.unescape(re.sub(r'<[^>]+>',' ',t))
    return t
import unicodedata
norm=lambda s: re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s.replace('ſ','s')).encode('ascii','ignore').decode().lower()).replace('f','s')
cache={}; res=[]
for f in ['a1/claims-a1.json','a2/claims-a2.json','a3/claims-a3.json']:
    for c in json.load(open(f))['claims']:
        h=c.get('file_sha256'); p=files.get(h)
        if not p: res.append((c['id'],'KHÔNG THẤY TỆP SHA')); continue
        if p not in cache: cache[p]=norm(text(p))
        q=c['trich_nguyen_van']; parts=[x for x in re.split(r'\s*(?:…|\.\.\.|\[\.\.\.\]|\[…\])\s*',q) if len(x.strip())>8]
        ok=all(norm(x) in cache[p] for x in parts)
        res.append((c['id'],'OK' if ok else 'KHÔNG KHỚP'))
bad=[r for r in res if r[1]!='OK']
print(len(res),'claim; khớp',len(res)-len(bad)); print(bad)
# chẩn đoán: tìm mảnh dài nhất khớp
for cid in [b[0] for b in bad]:
    for f in ['a1/claims-a1.json']:
        for c in json.load(open(f))['claims']:
            if c['id']!=cid: continue
            p=files.get(c['file_sha256'])
            if not p: print(cid,'no file'); continue
            T=cache[p]; q=norm(c['trich_nguyen_van']); 
            # dài nhất tiền tố khớp
            lo=0
            for k in range(20,len(q),20):
                if q[:k] in T: lo=k
                else: break
            print(cid, 'len',len(q),'tiền tố khớp',lo, '| quote:',c['trich_nguyen_van'][max(0,lo-10):lo+120].replace('\n',' '))
print('--- từng đoạn (cắt tại … / || / câu)')
for cid in [b[0] for b in bad]:
    c=[x for x in json.load(open('a1/claims-a1.json'))['claims'] if x['id']==cid][0]
    ps=[files.get(h) for h in [c['file_sha256']]]
    if c['id']=='V-A1-35':
        ps=[p for p in files.values() if 'sayer' in p.lower() or 'montgoog' in p.lower() or 'historyofgibralt' in p or 'historiadegibra' in p]
    T=''.join(cache.get(p) or norm(text(p)) for p in ps if p)
    segs=[s for s in re.split(r'…|\|\||\.\s|;\s|,\s',c['trich_nguyen_van']) if len(norm(s))>15]
    miss=[s.strip()[:70] for s in segs if norm(s) not in T]
    print(cid,f'{len(segs)-len(miss)}/{len(segs)} mảnh khớp; lệch:',miss[:3])
kj={}
for cid,r in res: kj[cid]='khớp nguyên khối' if r=='OK' else 'khớp theo mảnh (1 mảnh lệch do OCR/ngắt dòng) — đối chiếu ảnh trang'
json.dump(kj,open('me/kiem.json','w'),ensure_ascii=False)
