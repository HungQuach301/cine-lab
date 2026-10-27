#!/bin/bash
# BAN-CUOI-T4-B2a · nhịp CHECKPOINT (đẩy ≤ 30 phút): mỗi 25 phút ghi tiến độ dựng (tien-do-b2a.jsonl: shot đang chạy, khung đã ra) vào CHECKPOINT → commit (preflight) → đẩy; khoá flock chung với xong_b1.sh.
set -o pipefail
cd "$(dirname "$0")/../../.."; R=/var/tmp/bc/r
while ! grep -q "CHUOI-B2a-XONG" /var/tmp/bc/log/chuoi_b2a.log; do sleep 1500
  s=$(for d in $(tail -6 $R/tien-do-b2a.jsonl | /opt/cine/bin/python -c "import sys,json;print(' '.join(sorted({json.loads(l)['ten'] for l in sys.stdin if json.loads(l).get('chay')})))"); do [ -s $R/$d/log.json ] || echo -n "$d $(ls $R/$d 2>/dev/null | grep -c jpg) khung; "; done)
  n=$(grep -c '^[0-9a-f]\{64\}' channel-k2/k2c-t4-02/ban-cuoi/dung/SHA256SUMS)
  ( flock 9; echo "- $(date -u +%H:%M) UTC nhịp: $n tệp 1080p đã đẩy LFS; đang dựng: ${s:-—}; RAM trống $(free -m | awk '/Mem:/{print $7}') MB, đĩa trống $(df -h /var/tmp | awk 'NR==2{print $4}')" >> reports/ban-cuoi-t4-b2a/CHECKPOINT.md
    git add reports/ban-cuoi-t4-b2a/CHECKPOINT.md && bash reports/ban-cuoi-t4-b2a/cam_commit.sh "BAN-CUOI-T4-B2a: CHECKPOINT nhịp dựng" > /dev/null && git push -q origin HEAD ) 9>/var/tmp/bc/git.lock
done
