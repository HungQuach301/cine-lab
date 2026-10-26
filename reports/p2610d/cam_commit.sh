#!/bin/bash
# P-2610d: preflight (pipefail) rồi commit chỉ khi có "— ĐẠT" và "PREFLIGHT ĐẠT". Dùng: bash reports/p2610d/cam_commit.sh "<thông điệp>"
set -o pipefail
cd "$(dirname "$0")/../.." || exit 2
out=$(bash tools/preflight.sh --staged 2>&1); rc=$?
echo "$out" | tail -8
if [ $rc = 0 ] && echo "$out" | grep -q -- '— ĐẠT' && echo "$out" | grep -q 'PREFLIGHT ĐẠT'; then
  git commit -q -F - <<MSG && git log --oneline -1
$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013TE19VfYkeapeiXMNATAAV
MSG
else echo "KHÔNG COMMIT: preflight chưa ĐẠT"; exit 1; fi
