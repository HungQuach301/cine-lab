#!/usr/bin/env bash
# O1 lượt 3 (làm lại lần 2) cho ảnh trượt bộ kiểm lượt 2: lệnh -r3 (bỏ "terraces/plots" đã gợi AI vẽ tường đá; cấm tường, lối mòn, động vật, đá/đảo trong nước)
cd /home/user/cine-lab/reports/nc-n2p
for t in cang-vua cang-manh toan-canh-vua toan-canh-manh; do k=${t%-*}
  /opt/cine/bin/python -I ma/oai_edit.py --img ../nc-cpu/khung/A/cong-$k.jpg --prompt-file o1/lenh/$t-r3.txt --tag $t-l3 --out /var/tmp/n2p/o1/ai
done
for m in 1 2; do f=$([ $m = 1 ] && echo 168 || echo 408)
  /opt/cine/bin/python -I ma/oai_edit.py --img /var/tmp/n2p/tlmoc/rgb/00$f.jpg --prompt-file tl/lenh/moc$m-r3.txt --tag tl-moc$m-l3 --out /var/tmp/n2p/tlmoc/ai
done
O=/var/tmp/n2p/kiem-cuoi; declare -A Y=([cang]=1780 [toan-canh]=1781)
for t in cang-vua cang-manh toan-canh-vua toan-canh-manh; do k=${t%-*}
  /opt/cine/bin/python -I ma/kiem_n2p.py --render ../nc-cpu/khung/A/cong-$k.jpg --ai /var/tmp/n2p/o1/ai/$t-l3-ai.jpg --id o1/mat-na/id-$k.png --nam ${Y[$k]} --tag $t-l3 --out $O --khop-mau
  (cd /home/user/cine-lab && /opt/cine/bin/python checks/ll/q_thoi_dai.py --anh $O/$t-l3-ghep.png --nam ${Y[$k]} --noi Gibraltar --out $O/qtd-$t-l3 --api --json $O/qtd-$t-l3.json | head -1)
done
for m in 1 2; do f=$([ $m = 1 ] && echo 168 || echo 408)
  /opt/cine/bin/python -I ma/kiem_n2p.py --render /var/tmp/n2p/tlmoc/rgb/00$f.jpg --ai /var/tmp/n2p/tlmoc/ai/tl-moc$m-l3-ai.jpg --id /var/tmp/n2p/tlmoc/id/00$f.png --nam 1779 --tag tl-moc$m-l3 --out $O --khop-mau
  (cd /home/user/cine-lab && /opt/cine/bin/python checks/ll/q_thoi_dai.py --anh $O/tl-moc$m-l3-ghep.png --nam 1779 --noi Gibraltar --out $O/qtd-tl-moc$m-l3 --api --json $O/qtd-tl-moc$m-l3.json | head -1)
done
echo O1L3-XONG
