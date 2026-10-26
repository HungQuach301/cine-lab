#!/bin/bash
# commit + đẩy khi checks/ đang sửa dở (chưa khoá): lưu bản vá WIP → cất checks/ (stash) → commit reports + checks-appeal (hook preflight) → push → lấy lại
# day.sh "<thông điệp commit>"
set -o pipefail; cd /home/user/cine-lab
git diff -- checks/ > reports/k1179/wip/checks-wip.patch; git ls-files --others --exclude-standard -- checks/ | while read f; do echo "=== MỚI $f"; done >> reports/k1179/wip/checks-wip.patch
tar czf reports/k1179/wip/checks-moi.tgz $(git ls-files --others --exclude-standard -- checks/) 2>/dev/null
d=$(git status --porcelain -- checks/ | wc -l)
[ "$d" -gt 0 ] && git stash push -q --include-untracked -- checks/
python3 -I checks/lock.py --verify | tail -1
git add reports/k1179 checks-appeal.md
out=$(bash tools/preflight.sh --staged 2>&1); echo "$out" | tail -4
echo "$out" | grep -q -- "— ĐẠT" && echo "$out" | grep -q "PREFLIGHT ĐẠT" || { echo "KHÔNG COMMIT: preflight chưa ĐẠT"; [ "$d" -gt 0 ] && git stash pop -q; exit 1; }
git commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Kpk4Cvp952oZTtkugqjFDz" 2>&1 | tail -3; rc=$?
git push -q -u origin ccr-196e0bda-gcj9iw 2>&1 | tail -3
[ "$d" -gt 0 ] && git stash pop -q
git status --short -- checks/ | head -3; exit $rc
