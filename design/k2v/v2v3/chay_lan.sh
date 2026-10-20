#!/usr/bin/env bash
# lan.sh: 2 làn dựng cửa sổ nguồn
S=/var/tmp/cine-out/v2v3/src; mkdir -p $S; R=/var/tmp/cine-out/v2v3/dung_cua_so.sh
( $R c2 80 161 $S/c2 > $S/c2.log 2>&1; echo EXIT $? >> $S/c2.log; $R c1 344 425 $S/c1 > $S/c1.log 2>&1; echo EXIT $? >> $S/c1.log ) &
( $R c4 320 401 $S/c4B > $S/c4B.log 2>&1; echo EXIT $? >> $S/c4B.log ) &
wait
