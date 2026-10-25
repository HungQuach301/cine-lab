import cv2, numpy as np, sys
A='/home/user/cine-lab/channel-k2/k2c-t4-02/animatic/omni'; det=cv2.FaceDetectorYN.create('/var/tmp/k1177/dl/yunet.onnx','',(320,320),0.5,0.3,5000)
tags=sys.argv[2:]; u=float(sys.argv[1]); out=[]
for tag in tags:
    cap=cv2.VideoCapture(f'{A}/clip/{tag}.mp4'); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); cap.set(cv2.CAP_PROP_POS_FRAMES,int(u*(n-1))); ok,f=cap.read()
    H,W=f.shape[:2]; det.setInputSize((W,H)); _,fa=det.detect(f); im=cv2.resize(f,(960,540)); k=1.5
    for j,z in enumerate([] if fa is None else fa):
        if z[3]/H<0.035: continue
        c=(0,255,0) if z[14]>=0.75 else (0,160,255); x,y,w,h=[int(v*k) for v in z[:4]]
        cv2.rectangle(im,(x,y),(x+w,y+h),c,1); cv2.putText(im,f'{z[14]:.2f}',(x,y-2),0,0.4,c,1)
    cv2.putText(im,f'{tag} u{u}',(4,530),0,0.6,(0,255,255),2); out.append(im)
while len(out)%2: out.append(np.zeros_like(out[0]))
cv2.imwrite(f'/var/tmp/k1177/mat/gt-{int(u*100)}-{tags[0][:6]}.jpg',np.vstack([np.hstack(out[j:j+2]) for j in range(0,len(out),2)]),[cv2.IMWRITE_JPEG_QUALITY,88])
