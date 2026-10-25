import cv2, glob, json, os, numpy as np
A='/home/user/cine-lab/channel-k2/k2c-t4-02/animatic/omni'; det=cv2.FaceDetectorYN.create('/var/tmp/k1177/dl/yunet.onnx','',(320,320),0.5,0.3,5000)
D=[]
for c in sorted(glob.glob(f'{A}/chon/*.txt')):
    tag=open(c).read().split()[0]; cap=cv2.VideoCapture(f'{A}/clip/{tag}.mp4'); i=0
    while True:
        ok,f=cap.read()
        if not ok: break
        if i%6==0:
            H,W=f.shape[:2]; det.setInputSize((W,H)); _,fa=det.detect(f)
            for z in ([] if fa is None else fa):
                x,y,w,h=[float(v) for v in z[:4]]
                if h/H<0.04: continue
                L=z[4:14].reshape(5,2); ed=np.linalg.norm(L[0]-L[1])/max(w,1)
                inside=all(x-0.1*w<=p[0]<=x+1.1*w and y-0.1*h<=p[1]<=y+1.1*h for p in L)
                x0,y0=max(0,int(x-0.2*w)),max(0,int(y-0.2*h)); cr=f[y0:int(y+1.2*h),x0:int(x+1.2*w)]
                if cr.size==0: continue
                cr=cv2.resize(cr,(96,96)); cv2.putText(cr,f'{z[14]:.2f}',(2,10),0,0.35,(0,255,255),1); cv2.putText(cr,f'{h/H:.2f}',(2,92),0,0.35,(0,255,255),1)
                D.append(dict(tag=tag,f=i,s=round(float(z[14]),3),r=round(h/H,3),ed=round(float(ed),3),inside=inside,cr=cr))
        i+=1
D.sort(key=lambda d:-d['s'])
print(len(D))
for k in range(0,len(D),60):
    S=[d['cr'] for d in D[k:k+60]]
    while len(S)%10: S.append(np.zeros((96,96,3),np.uint8))
    cv2.imwrite(f'/var/tmp/k1177/mat/crop-{k//60}.jpg',np.vstack([np.hstack(S[j:j+10]) for j in range(0,len(S),10)]))
json.dump([{k:v for k,v in d.items() if k!='cr'} for d in D],open('/var/tmp/k1177/mat/crops.json','w'),indent=0)
for j,d in enumerate(D[:60]): print(j,d['tag'],d['f'],d['s'],d['r'],d['ed'],d['inside'])
