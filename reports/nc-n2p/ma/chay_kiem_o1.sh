#!/usr/bin/env bash
# kiểm N2+ đầy đủ (máy + 2 mô hình) cho O1 lượt 2 (khớp màu) — 6 ảnh
cd /home/user/cine-lab/reports/nc-n2p
declare -A Y=([cang]=1780 [vay-ham]=1779 [toan-canh]=1781)
for k in cang vay-ham toan-canh; do for lv in vua manh; do t=$k-$lv
  /opt/cine/bin/python -I ma/kiem_n2p.py --render ../nc-cpu/khung/A/cong-$k.jpg --ai /var/tmp/n2p/o1/ai/$t-l2-ai.jpg --id o1/mat-na/id-$k.png --nam ${Y[$k]} --tag $t-l2 --out /var/tmp/n2p/o1/kiem --khop-mau
done; done
echo KIEM-O1-XONG
