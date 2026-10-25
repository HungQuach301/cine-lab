import cv2
A='/home/user/cine-lab/channel-k2/k2c-t4-02/animatic/omni'; det=cv2.FaceDetectorYN.create('/var/tmp/k1177/dl/yunet.onnx','',(320,320),0.5,0.3,5000)
cap=cv2.VideoCapture(f'{A}/clip/H2-03c-l1-360p.mp4'); n=int(cap.get(7)); cap.set(1,int(0.55*(n-1))); ok,f=cap.read()
det.setInputSize((640,360)); _,fa=det.detect(f); print([ (round(z[14],2), [int(v) for v in z[:4]]) for z in fa])
# cắt quanh mặt thẩm phán (x~330,y~130) rồi phóng về 640×360
for (cx,cy,s) in ((338,142,160),(338,142,260),(338,142,90)):
    x0,y0=cx-int(s*16/18),cy-s//2; cr=f[max(0,y0):y0+s, max(0,x0):x0+int(s*16/9)]
    im=cv2.resize(cr,(640,360),interpolation=cv2.INTER_CUBIC); _,fb=det.detect(im)
    print(s, cr.shape, [(round(float(z[14]),2), round(float(z[3])/360,3)) for z in (fb if fb is not None else [])])
    cv2.imwrite(f'/var/tmp/k1177/fx/up{s}.png',im)
