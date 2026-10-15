#!/bin/bash
# NỀN TẢNG · kiểm trước commit/push (phiên Nền tảng 15/10/2026). Mọi phiên chạy trước khi đẩy; có thể cài làm git hook.
#   bash tools/preflight.sh                    # tệp đang stage (mặc định)
#   bash tools/preflight.sh --range origin/main..HEAD   # các commit sắp đẩy
#   bash tools/preflight.sh --all              # toàn repo (kiểm định kỳ)
# Kiểm: email / khoá bí mật · tệp > 5 MB ngoài LFS cho phép (tools/lfs-allow.txt) · checks/lock.py --verify · dấu xung đột merge ·
#       tệp giấy phép cho mỗi dòng sổ footage/ảnh ngoài · (báo) ảnh tư liệu chưa có trong RIGHTS/SOURCES. Chi tiết: scripts/common/preflight_scan.py.
# Cài hook (một lần mỗi bản clone; hook không theo git nên mỗi container mới phải cài lại — đặt trong scripts/env/verify.sh hoặc đầu phiên):
#   ln -sf ../../tools/preflight.sh .git/hooks/pre-commit
#   ln -sf ../../tools/preflight.sh .git/hooks/pre-push
# Bỏ qua khẩn cấp (phải ghi lý do trong báo cáo): git commit --no-verify / git push --no-verify.
set -u
REPO=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd); cd "$REPO" || exit 2
PY=/opt/cine/bin/python; [ -x $PY ] || PY=python3
HOOK=$(basename "$0"); ARGS=("$@")
if [ "$HOOK" = pre-push ]; then   # stdin: <local ref> <local sha> <remote ref> <remote sha>
  ARGS=(); Z=0000000000000000000000000000000000000000
  while read -r lref lsha rref rsha; do [ "$lsha" = $Z ] && continue
    if [ "$rsha" = $Z ]; then base=$(git merge-base "$lsha" origin/main 2>/dev/null || git rev-list --max-parents=0 "$lsha" | tail -1); else base=$rsha; fi
    ARGS=(--range "$base..$lsha"); done
  [ ${#ARGS[@]} -eq 0 ] && exit 0
elif [ "$HOOK" = pre-commit ]; then ARGS=(--staged); fi
[ ${#ARGS[@]} -eq 0 ] && ARGS=(--staged)
rc=0
$PY scripts/common/preflight_scan.py "${ARGS[@]}" || rc=1
if out=$($PY checks/lock.py --verify 2>&1); then echo "lock.py --verify: KHỚP"; else echo "CHẶN lock.py --verify: $out" | head -5; rc=1; fi
[ $rc = 0 ] && echo "PREFLIGHT ĐẠT" || echo "PREFLIGHT TRƯỢT — sửa các mục CHẶN rồi chạy lại"
exit $rc
