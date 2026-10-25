import cv2, json, os, sys, numpy as np
A='/home/user/cine-lab/channel-k2/k2c-t4-02/animatic/omni'; det=cv2.FaceDetectorYN.create('/var/tmp/k1177/dl/yunet.onnx','',(320,320),0.5,0.3,5000)
out=[]; info={}
for tag in sys.argv[1:]:
    cap=cv2.VideoCapture(f'{A}/clip/{tag}.mp4'); F=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        F.append(f)
    H,W=F[0].shape[:2]; best=[]
    for i in range(0,len(F),2):
        det.setInputSize((W,H)); _,fa=det.detect(F[i])
        for z in ([] if fa is None else fa): best.append((z[3]/H,float(z[14]),i,z[:4].astype(int).tolist()))
    best.sort(reverse=True); info[tag]=best[:6]
    for r,s,i,(x,y,w,h) in best[:2]:
        im=F[i].copy(); cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0) if s>=0.6 else (0,160,255),2); cv2.putText(im,f'{tag} f{i} s{s:.2f} h/H {r:.3f}',(4,16),0,0.5,(0,255,255),1); out.append(im)
while len(out)%3: out.append(np.zeros_like(out[0]))
cv2.imwrite('/var/tmp/k1177/mat/max.jpg',np.vstack([np.hstack(out[j:j+3]) for j in range(0,len(out),3)]),[cv2.IMWRITE_JPEG_QUALITY,85])
for k,v in info.items(): print(k,[(round(a,3),round(b,2),c) for a,b,c,_ in v])
