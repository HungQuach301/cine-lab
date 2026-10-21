#!/usr/bin/env bash
# O1 lượt 2 (làm lại): KHÔNG gửi mặt nạ (lượt 1 có mặt nạ: gpt-image vẽ lại hình học — đổi đất/nước), lệnh -r2 (thêm câu "EDIT … pixel for pixel")
cd /home/user/cine-lab/reports/nc-n2p
for t in cang-vua cang-manh vay-ham-manh toan-canh-vua toan-canh-manh; do k=${t%-*}
  /opt/cine/bin/python -I ma/oai_edit.py --img ../nc-cpu/khung/A/cong-$k.jpg --prompt-file o1/lenh/$t-r2.txt --tag $t-l2 --out /var/tmp/n2p/o1/ai
done
echo O1L2-XONG
