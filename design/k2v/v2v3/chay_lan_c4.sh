#!/usr/bin/env bash
# lan_c4.sh: dựng c4 (C1a V7B) đủ 0–480 cho chế độ C (nối 20 s); 320–400 đã có ở src/c4B
S=/var/tmp/cine-out/v2v3/src; R=/var/tmp/cine-out/v2v3/dung_cua_so.sh
( $R c4 0 200 $S/c4a1 > $S/c4a1.log 2>&1; echo EXIT $? >> $S/c4a1.log ) &
( $R c4 200 320 $S/c4a2 > $S/c4a2.log 2>&1; echo EXIT $? >> $S/c4a2.log; $R c4 401 480 $S/c4a3 > $S/c4a3.log 2>&1; echo EXIT $? >> $S/c4a3.log ) &
wait
