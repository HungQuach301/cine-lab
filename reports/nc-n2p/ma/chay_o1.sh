#!/usr/bin/env bash
cd /home/user/cine-lab/reports/nc-n2p
for k in cang vay-ham toan-canh; do for lv in vua manh; do
  /opt/cine/bin/python -I ma/oai_edit.py --img ../nc-cpu/khung/A/cong-$k.jpg --mask o1/mat-na/sua-$k.png --prompt-file o1/lenh/$k-$lv.txt --tag $k-$lv --out /var/tmp/n2p/o1/ai
done; done
echo O1-XONG
