#!/bin/bash
# P-2610b: chạy mọi selftest checks/ll/selftest_*.py, in dòng tổng mỗi bộ. Dùng: bash reports/p2610b/chay_selftest.sh <nhãn>
set -o pipefail
cd "$(dirname "$0")/../.." || exit 2
PY=/opt/cine/bin/python; rc=0
echo "== selftest ($1) @ $(git rev-parse --short=8 HEAD) $(date -u +%FT%TZ)"
python3 -I checks/lock.py --verify | tail -1 || rc=1
for f in checks/ll/selftest_*.py; do
  out=$($PY "$f" 2>&1); r=$?
  echo "$(basename $f .py) rc=$r :: $(echo "$out" | grep -E '[0-9]+ */ *[0-9]+|ĐẠT|TRƯỢT|PASS|FAIL' | tail -1)"
  [ $r = 0 ] || rc=1
done
echo "== tổng rc=$rc"; exit $rc
