#!/bin/bash
# ANIMATIC-T3 · đẩy CHECKPOINT định kỳ (lệnh chủ dự án 21/10 16:00: ≥ mỗi 30 phút tới hết phiên, kể cả khi chỉ đang dựng; không selftest).
#   CHU_KY=1500 setsid nohup bash scripts/k2tl/anim_ckpt.sh > /var/tmp/cine-out/log/ckpt.log 2>&1 &     (một lượt: ONCE=1 bash scripts/k2tl/anim_ckpt.sh)
# Chỉ stage reports/animatic-t3/CHECKPOINT.md; preflight --staged + --range trước khi đẩy; đẩy lỗi mạng thử lại 4 lần (2/4/8/16 s).
cd "$(dirname "$0")/../.." || exit 1; BR=${BR:-ccr-d189108f-6mcz9k}; CKF=${ANIM_CK:-reports/animatic-t3/CHECKPOINT.md}; TAG=${TAG:-ANIMATIC-T3}   # ANIM-V2: BR=k2c-t3-anim-v2 ANIM_CK=reports/animatic-t3-v2/CHECKPOINT.md TAG=ANIMATIC-T3-V2
while true; do
  /opt/cine/bin/python -I scripts/k2tl/anim_ckpt.py && git add $CKF
  if ! git diff --cached --quiet; then
    /opt/cine/bin/python -I scripts/common/preflight_scan.py --staged | tail -1 && git commit -q -m "$TAG CHECKPOINT (đang làm): $(date -u +%H:%M) UTC

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01YM8dqatyJS7XQeK9cGtZpW"
  fi
  /opt/cine/bin/python -I scripts/common/preflight_scan.py --range origin/$BR..HEAD | tail -1
  for w in 2 4 8 16 0; do git push -q -u origin HEAD:$BR && break; [ $w = 0 ] && echo "ĐẨY LỖI"; sleep $w; done
  echo "$(date -u +%H:%M) đã đẩy $(git rev-parse --short HEAD)"
  [ -n "${ONCE:-}" ] && break; sleep ${CHU_KY:-1500}
done
