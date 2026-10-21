#!/bin/bash
# ANIMATIC-T3 · đẩy CHECKPOINT định kỳ (lệnh chủ dự án 21/10 16:00: ≥ mỗi 30 phút tới hết phiên, kể cả khi chỉ đang dựng; không selftest).
#   CHU_KY=1500 setsid nohup bash scripts/k2tl/anim_ckpt.sh > /var/tmp/cine-out/log/ckpt.log 2>&1 &     (một lượt: ONCE=1 bash scripts/k2tl/anim_ckpt.sh)
# Chỉ stage reports/animatic-t3/CHECKPOINT.md; preflight --staged + --range trước khi đẩy; đẩy lỗi mạng thử lại 4 lần (2/4/8/16 s).
cd "$(dirname "$0")/../.." || exit 1; BR=ccr-d189108f-6mcz9k
while true; do
  /opt/cine/bin/python -I scripts/k2tl/anim_ckpt.py && git add reports/animatic-t3/CHECKPOINT.md
  if ! git diff --cached --quiet; then
    /opt/cine/bin/python -I scripts/common/preflight_scan.py --staged | tail -1 && git commit -q -m "ANIMATIC-T3 CHECKPOINT (đang làm): $(date -u +%H:%M) UTC

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QeLs3aouACksUwyyEpYcWt"
  fi
  /opt/cine/bin/python -I scripts/common/preflight_scan.py --range origin/$BR..HEAD | tail -1
  for w in 2 4 8 16 0; do git push -q origin $BR && break; [ $w = 0 ] && echo "ĐẨY LỖI"; sleep $w; done
  echo "$(date -u +%H:%M) đã đẩy $(git rev-parse --short HEAD)"
  [ -n "${ONCE:-}" ] && break; sleep ${CHU_KY:-1500}
done
