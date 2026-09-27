#!/bin/bash
# Cổng 3 v3 — bước 4 kiểm toán C3 (RUN.md 3.7): render lại mặt nạ đúng các khung máy chọn, cùng lệnh, cùng độ phân giải; ghi render.log.
cd "$(dirname "$0")/.."; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
O=v2/out; SCENE=design/cong3/v2/page.js; SHA=$(sha256sum ../../$SCENE | cut -d' ' -f1)
for S in ${SHOTS:-s1_opening a_close_ida b_cas_bird c_s5_wide c_s5_medium d_s6_alley e_ending walk walk_cas}; do
  FR=$(/opt/cine/bin/python -c "import json;print(','.join(str(f) for f in json.load(open('$O/$S.audit/request.json'))['frames']))")
  echo "SCENE $SCENE SHA256 $SHA" > $O/$S.audit/render.log
  for f in ${FR//,/ }; do
    CMD="node design/cong3/shared/export_sidecars.js --page v2/page.js --shot $S --video design/cong3/v2/out/$S.mp4 --parts $f --scale 4 --args {\"char\":\"3d\"} --audit-dir design/cong3/v2/out/$S.audit/rerender"
    node shared/export_sidecars.js --page v2/page.js --shot $S --video $O/$S.mp4 --parts $f --scale 4 --args "{\"char\":\"3d\"}" --audit-dir $O/$S.audit/rerender 2>&1 | grep -v '^\[page\]' | tail -1 | cut -c1-200
    echo "FRAME $f CMD $CMD" >> $O/$S.audit/render.log
  done
done
echo XONG
