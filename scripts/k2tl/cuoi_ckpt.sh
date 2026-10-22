#!/bin/bash
# BAN-CUOI-T3 · đẩy CHECKPOINT định kỳ (≤ 30 phút): cập nhật khối trạng thái (cuoi_ckpt.py) → commit CHỈ tệp CHECKPOINT (pathspec) khi preflight in "— ĐẠT" → đẩy nhánh làm việc.
#   CHU_KY=1500 setsid nohup bash scripts/k2tl/cuoi_ckpt.sh > /var/tmp/cine-out/log/ckpt.log 2>&1 &
cd "$(dirname "$0")/../.." || exit 1; BR=k2c-t3-cuoi; CKF=reports/ban-cuoi-t3/CHECKPOINT.md; echo $$ > /var/tmp/cine-out/log/ckpt.pgid
while true; do
  /opt/cine/bin/python -I scripts/k2tl/cuoi_ckpt.py
  if ! git diff --quiet -- $CKF; then
    git add $CKF; OUT=$(/opt/cine/bin/python -I scripts/common/preflight_scan.py --staged 2>&1 | tail -1)
    if echo "$OUT" | grep -q "— ĐẠT"; then git commit -q -m "BAN-CUOI-T3 CHECKPOINT (đang làm): $(date -u +%H:%M) UTC

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HWCNoTiu8o9QBSYMrjTi4y" -- $CKF; else echo "PREFLIGHT không ĐẠT ($OUT) — không commit"; fi
  fi
  for w in 2 4 8 16 0; do git push -q -u origin HEAD:$BR && break; [ $w = 0 ] && echo "ĐẨY LỖI"; sleep $w; done
  echo "$(date -u +%H:%M) đã đẩy $(git rev-parse --short HEAD)"
  [ -n "${ONCE:-}" ] && break; sleep ${CHU_KY:-1500}
done
