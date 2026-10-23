#!/bin/bash
# P-2410: preflight (pipefail) rồi commit chỉ khi có "— ĐẠT" và "PREFLIGHT ĐẠT". Dùng: bash reports/p2410/cam_commit.sh "<thông điệp>"
set -o pipefail
cd "$(dirname "$0")/../.." || exit 2
out=$(bash tools/preflight.sh --staged 2>&1); rc=$?
echo "$out" | tail -8
if [ $rc = 0 ] && echo "$out" | grep -q -- '— ĐẠT' && echo "$out" | grep -q 'PREFLIGHT ĐẠT'; then
  git commit -q -F - <<MSG && git log --oneline -1
$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01UUt98vpP7r9M2iN8n91q5d
MSG
else echo "KHÔNG COMMIT: preflight chưa ĐẠT"; exit 1; fi
