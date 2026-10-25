#!/bin/bash
# commit + đẩy khi checks/ đang sửa dở (chưa khoá): lưu bản vá WIP → cất checks/ (stash) → commit reports + checks-appeal (hook preflight) → push → lấy lại
# day.sh "<thông điệp commit>"
set -o pipefail; cd /home/user/cine-lab
git diff -- checks/ > reports/k1178/wip/checks-wip.patch; git ls-files --others --exclude-standard -- checks/ | while read f; do echo "=== MỚI $f"; done >> reports/k1178/wip/checks-wip.patch
tar czf reports/k1178/wip/checks-moi.tgz $(git ls-files --others --exclude-standard -- checks/) 2>/dev/null
d=$(git status --porcelain -- checks/ | wc -l)
[ "$d" -gt 0 ] && git stash push -q --include-untracked -- checks/
python3 -I checks/lock.py --verify | tail -1
git add reports/k1178 checks-appeal.md
git commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01E9Wh45VExSfuT6eX1vFkbj" 2>&1 | tail -3; rc=$?
git push -q -u origin claude/k1178-t4-london-rules-pdjfmz 2>&1 | tail -3
[ "$d" -gt 0 ] && git stash pop -q
git status --short -- checks/ | head -3; exit $rc
