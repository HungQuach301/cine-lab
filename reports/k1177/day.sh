#!/bin/bash
# đẩy khi checks/ đang sửa dở: cất checks/ (stash) → push (hook preflight) → lấy lại
set -o pipefail; cd /home/user/cine-lab
d=$(git status --porcelain -- checks/ | wc -l)
[ "$d" -gt 0 ] && git stash push -q -- checks/
git push -u origin claude/k1177-animatic-checks-nfbsbr 2>&1 | tail -4; rc=$?
[ "$d" -gt 0 ] && git stash pop -q
git status --short -- checks/ | head -3; exit $rc
