#!/bin/bash
# chạy mọi selftest kênh 2/LL trên cây hiện tại; ghi tóm tắt từng bộ + mã thoát. selftest_all.sh <tệp ra>
set -o pipefail; cd /home/user/cine-lab; out=$1; : > $out
python3 -I checks/lock.py --verify | tail -1 | sed 's/^/LOCK: /' >> $out
for f in checks/ll/selftest_*.py; do
  t0=$(date +%s); /opt/cine/bin/python $f > /var/tmp/k1178/st-$(basename $f .py).log 2>&1; rc=$?
  echo "$(basename $f) rc=$rc $(grep -E '^selftest|đúng kỳ vọng|ĐẠT|SAI' /var/tmp/k1178/st-$(basename $f .py).log | tail -1) ($(( $(date +%s) - t0 )) s) · SAI: $(grep -c '^SAI' /var/tmp/k1178/st-$(basename $f .py).log)" >> $out
done
ls checks/selftest/run_selftest.py >/dev/null 2>&1 && { /opt/cine/bin/python checks/selftest/run_selftest.py > /var/tmp/k1178/st-run_selftest.log 2>&1; echo "checks/selftest/run_selftest.py rc=$? $(tail -1 /var/tmp/k1178/st-run_selftest.log)" >> $out; }
echo XONG >> $out
