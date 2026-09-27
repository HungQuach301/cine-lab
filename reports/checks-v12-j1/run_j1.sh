#!/usr/bin/env bash
# Phiên K — chạy J1 (v1.2) trên table read Cổng 2 của P: nháp 2 (đối tượng chính) và nháp 1 (bản bị khiếu nại).
# Dùng: bash reports/checks-v12-j1/run_j1.sh   (từ gốc repo, trên nhánh checks/v1.2)
set -u
ROOT=$(git rev-parse --show-toplevel); cd "$ROOT"
PY=/opt/cine/bin/python
B=origin/claude/cine-lab-m1-last-round-f1667s
OUT=reports/checks-v12-j1
W=$(mktemp -d)
git fetch -q origin claude/cine-lab-m1-last-round-f1667s
for d in tableread-d2 tableread; do
  for f in last-round-$d.mp4 last-round-$d.script.txt; do git show $B:reports/m1/cong2/$d/$f > $W/$f; done
  $PY checks/run.py $W/last-round-$d.mp4 --only J1 --out $OUT/$d; echo "exit $d: $?"
done
echo "Thư mục tạm: $W"
