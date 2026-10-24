#!/bin/bash
# THU-B-T4 · commit có cổng: preflight (pipefail) phải in "PREFLIGHT ĐẠT" thì mới commit; tuỳ chọn đẩy.
#   bash scripts/k2ldn/thu-b/cam.sh "<thông điệp>" [day]     (đã `git add` trước)
set -o pipefail
cd "$(dirname "$0")/../../.."
out=$(bash tools/preflight.sh --staged 2>&1); rc=$?; echo "$out" | tail -3
[ $rc = 0 ] && echo "$out" | grep -q "PREFLIGHT ĐẠT" || { echo "KHÔNG COMMIT (preflight trượt)"; exit 1; }
git commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01K6i6vy32B8b4hRQaiRZxB1" || exit 1
git log --oneline -1
if [ "$2" = day ]; then for i in 0 2 4 8 16; do sleep $i; git push -u origin HEAD:ccr-ce664665-996oyl 2>&1 | tail -2 && break; done; fi
