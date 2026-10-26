#!/bin/bash
# BAN-CUOI-T4-A · Commons 429 kéo dài (IP proxy dùng chung): thăm dò 1 yêu cầu / 10 phút; khi API trả 200 → chạy lần lượt (≤ 1 yêu cầu/5 s, commons_bc.py) các việc trong $1 (mỗi dòng một lệnh commons_bc.py …).
#   setsid nohup bash scripts/k2ldn/bc/commons_cho.sh /var/tmp/bc/commons-viec.txt > /var/tmp/bc/log/commons.log 2>&1 &
cd "$(dirname "$0")/../../.."; UA="CineLab-research (+https://github.com/HungQuach301/cine-lab)"
while true; do
  c=$(curl -sS -o /dev/null -w "%{http_code}" -A "$UA" "https://commons.wikimedia.org/w/api.php?action=query&meta=siteinfo&format=json")
  echo "$(date -u +%H:%M:%S) thăm dò $c"; date +%s > /var/tmp/bc/commons.last
  [ "$c" = 200 ] && break; sleep 600
done
while IFS= read -r l; do [ -z "$l" ] && continue; echo "== $(date -u +%H:%M:%S) $l"; eval "/opt/cine/bin/python scripts/k2ldn/bc/commons_bc.py $l"; done < "$1"
echo COMMONS-XONG
