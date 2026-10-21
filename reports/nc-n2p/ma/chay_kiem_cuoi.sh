#!/usr/bin/env bash
# kiểm N2+ LƯỢT CUỐI cho mọi ảnh tĩnh (mã ghép cuối: bảo vệ (a) nở 1 px + vật nhỏ 3 px, khớp màu): O1 lượt 2 (6), tấm timelapse (2) — máy + 2 mô hình + q_thoi_dai.py (K);
# O1 lượt 1 (6): chỉ máy (T9) để so.
cd /home/user/cine-lab/reports/nc-n2p; O=/var/tmp/n2p/kiem-cuoi; mkdir -p $O
declare -A Y=([cang]=1780 [vay-ham]=1779 [toan-canh]=1781)
for k in cang vay-ham toan-canh; do for lv in vua manh; do t=$k-$lv
  /opt/cine/bin/python -I ma/kiem_n2p.py --render ../nc-cpu/khung/A/cong-$k.jpg --ai /var/tmp/n2p/o1/ai/$t-ai.jpg --id o1/mat-na/id-$k.png --nam ${Y[$k]} --tag $t-l1 --out $O --khop-mau --khong-goi
  /opt/cine/bin/python -I ma/kiem_n2p.py --render ../nc-cpu/khung/A/cong-$k.jpg --ai /var/tmp/n2p/o1/ai/$t-l2-ai.jpg --id o1/mat-na/id-$k.png --nam ${Y[$k]} --tag $t-l2 --out $O --khop-mau
  (cd /home/user/cine-lab && /opt/cine/bin/python checks/ll/q_thoi_dai.py --anh $O/$t-l2-ghep.png --nam ${Y[$k]} --noi Gibraltar --out $O/qtd-$t --api --json $O/qtd-$t.json | head -3)
done; done
for m in 1 2; do f=$([ $m = 1 ] && echo 168 || echo 408)
  /opt/cine/bin/python -I ma/kiem_n2p.py --render /var/tmp/n2p/tlmoc/rgb/00$f.jpg --ai /var/tmp/n2p/tlmoc/ai/tl-moc$m-ai.jpg --id /var/tmp/n2p/tlmoc/id/00$f.png --nam 1779 --tag tl-moc$m --out $O --khop-mau
  (cd /home/user/cine-lab && /opt/cine/bin/python checks/ll/q_thoi_dai.py --anh $O/tl-moc$m-ghep.png --nam 1779 --noi Gibraltar --out $O/qtd-tl-moc$m --api --json $O/qtd-tl-moc$m.json | head -3)
done
echo KIEM-CUOI-XONG
