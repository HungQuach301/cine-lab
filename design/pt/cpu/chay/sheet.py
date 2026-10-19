import cv2,sys,numpy as np,glob,os
# sheet.py out.jpg dirA dirB ... : mỗi cột một thư mục (ảnh đầu tiên), hàng = khung cổng
out=sys.argv[1]; dirs=sys.argv[2:]; G=['vay-ham','cang','pho-day','hero','toan-canh','bo-chien-su']
rows=[]
for g in G:
    r=[]
    for d in dirs:
        fs=sorted(glob.glob(f'{d}/{g}/*.jpg'))+sorted(glob.glob(f'{d}/{g}/*.png'))+sorted(glob.glob(f'{d}/cong-{g}.png'))
        im=cv2.imread(fs[0]) if fs else np.zeros((360,640,3),np.uint8)
        im=cv2.resize(im,(640,360),interpolation=cv2.INTER_AREA); cv2.putText(im,f'{os.path.basename(d)} {g}',(6,18),0,0.5,(0,255,255),1); r.append(im)
    rows.append(np.hstack(r))
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,88])
